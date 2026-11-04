#!/usr/bin/env python3
"""Narrow exact SU(5) branching/anomaly benchmark; Python standard library only.

Weights are represented by fundamental-index occupations. Their common trace
component is immaterial on traceless SU(5) Cartan generators. Irrep names follow
the exterior-power identities described in the accompanying report, rather
than an implemented general highest-weight decomposition algorithm.
"""
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations
import json
from pathlib import Path
import platform

RUN = Path(__file__).resolve().parents[1]
Y = [F(-1, 3)] * 3 + [F(1, 2)] * 2
H3 = [F(1), F(2), F(-3), F(0), F(0)]
H2 = [F(0), F(0), F(0), F(1), F(-1)]


def dot(weight, generator):
    return sum((a * b for a, b in zip(weight, generator)), F(0))


def exterior_weights(rank, sign=1):
    return [tuple(sign if i in indices else 0 for i in range(5))
            for indices in combinations(range(5), rank)]


def trace(weights, generator, power):
    return sum((dot(weight, generator) ** power for weight in weights), F(0))


def branching(weights, names):
    groups = defaultdict(list)
    for weight in weights:
        groups[dot(weight, Y)].append(weight)
    output = []
    for charge, members in sorted(groups.items()):
        label, color, weak, particle = names[charge]
        assert len(members) == color * weak
        output.append({"representation": label, "hypercharge": str(charge),
                       "dimension": len(members), "particle": particle,
                       "weights": [list(w) for w in members]})
    assert sum(item["dimension"] for item in output) == len(weights)
    return output


def anomaly_contributions(groups):
    result = {}
    for group in groups:
        weights = group["weights"]
        # Normalize A(3)=1 and T(3)=T(2)=1/2; raw traces determine the rest.
        result[group["particle"]] = {
            "SU3_cubed": trace(weights, H3, 3) / F(-18),
            "SU3_squared_U1": sum(dot(w, H3)**2 * dot(w, Y) for w in weights) / F(28),
            "SU2_squared_U1": sum(dot(w, H2)**2 * dot(w, Y) for w in weights) / F(4),
            "U1_cubed": trace(weights, Y, 3),
            "gravity_squared_U1": trace(weights, Y, 1),
        }
    totals = {key: sum((row[key] for row in result.values()), F(0))
              for key in next(iter(result.values()))}
    assert all(value == 0 for value in totals.values())
    return result, totals


def main():
    fundamental = exterior_weights(1)
    conjugate = exterior_weights(1, sign=-1)
    ten = exterior_weights(2)
    b5 = branching(fundamental, {
        F(-1, 3): ("(3,1)", 3, 1, "fundamental color triplet"),
        F(1, 2): ("(1,2)", 1, 2, "fundamental weak doublet"),
    })
    bbar = branching(conjugate, {
        F(1, 3): ("(3bar,1)", 3, 1, "d^c"),
        F(-1, 2): ("(1,2)", 1, 2, "L"),
    })
    b10 = branching(ten, {
        F(-2, 3): ("(3bar,1)", 3, 1, "u^c"),
        F(1, 6): ("(3,2)", 3, 2, "Q"),
        F(1): ("(1,1)", 1, 1, "e^c"),
    })
    assert len(fundamental) == len(conjugate) == 5 and len(ten) == 10
    assert len(ten + conjugate) == 15

    # For traceless H, sum_{i<j}(h_i+h_j)^3=(N-4)sum_i h_i^3.
    # SU(5) has one cubic invariant, so the ratio fixes its local cubic anomaly.
    cartans = [[1, 2, 3, 4, -10], [1, 1, 1, 1, -4], [2, 2, 2, -3, -3]]
    cubic = []
    for values in cartans:
        assert sum(values) == 0
        denominator = trace(fundamental, values, 3)
        assert denominator != 0
        ratios = {"5": F(1), "5bar": trace(conjugate, values, 3) / denominator,
                  "10": trace(ten, values, 3) / denominator}
        assert ratios["5bar"] == -1 and ratios["10"] == 1
        cubic.append({"cartan": values, "traces": {"5": denominator,
                      "5bar": trace(conjugate, values, 3),
                      "10": trace(ten, values, 3)}, "ratios": ratios,
                      "three_generation_total": 3 * (ratios["10"] + ratios["5bar"])})

    contributions, totals = anomaly_contributions(b10 + bbar)
    three = {key: 3 * value for key, value in totals.items()}
    doublets = sum(item["dimension"] // 2 for item in b10 + bbar
                   if item["representation"].endswith(",2)"))
    assert doublets == 4 and (3 * doublets) % 2 == 0

    conjugate_labels = {"(3,2)": "(3bar,2)", "(3bar,1)": "(3,1)",
                        "(1,2)": "(1,2)", "(1,1)": "(1,1)"}
    spectrum = {(x["representation"], F(x["hypercharge"])): 3 for x in b10 + bbar}
    net_spectrum = []
    for item in b10 + bbar:
        key = item["representation"], F(item["hypercharge"])
        opposite = conjugate_labels[key[0]], -key[1]
        net = spectrum[key] - spectrum.get(opposite, 0)
        assert net == 3
        net_spectrum.append({"particle": item["particle"], "representation": item["representation"],
                             "hypercharge": item["hypercharge"], "net_left_handed_multiplicity": net})

    # phi(A,B,z)=diag(z^-2 A,z^3 B); kernel z^6=1. Check exact phases mod 1.
    kernel = []
    for k in range(6):
        z_phase = F(k, 6)
        a_phase, b_phase = 2 * z_phase, -3 * z_phase
        assert (3 * a_phase).denominator == 1 and (2 * b_phase).denominator == 1
        assert (-2 * z_phase + a_phase).denominator == 1
        assert (3 * z_phase + b_phase).denominator == 1
        kernel.append({"z_phase_turns": str(z_phase), "A_central_phase_turns": str(a_phase % 1),
                       "B_central_phase_turns": str(b_phase % 1)})

    result = {
        "candidate_id": "su5", "candidate_revision": "r1", "python": platform.python_version(),
        "arithmetic": "fractions.Fraction, exact", "fundamental_hypercharge": Y,
        "branchings": {"5": b5, "5bar": bbar, "10": b10},
        "SU5_cubic_anomaly": cubic,
        "SM_local_anomaly_contributions_per_generation": contributions,
        "SM_local_anomaly_totals_per_generation": totals,
        "SM_local_anomaly_totals_three_generations": three,
        "SM_fermion_dimensions": {"one_generation": 15, "three_generations": 45},
        "net_chiral_spectrum": net_spectrum,
        "SU2_Witten_doublet_count": {"per_generation": doublets, "three_generations": 3 * doublets,
                                    "scope": "ordinary SU(2) doublet anomaly on spin spacetime; not a complete bordism-anomaly analysis"},
        "subgroup_kernel": kernel,
        "subgroup_global_form": "S(U(3) x U(2)) isomorphic to (SU(3) x SU(2) x U(1))/Z6",
        "limitations": ["Only this fixed embedding and these exterior-power representations are calculated.",
                        "Group labels are assigned using exterior-power identities, not a general branching algorithm.",
                        "No scalar potential, Yukawa viability, neutrino mass, dark matter, or phenomenology is established.",
                        "The ordinary SU(2) Witten test is separate from a complete global anomaly classification."],
    }
    text = json.dumps(result, indent=2, default=lambda x: str(x) if isinstance(x, F) else x) + "\n"
    (RUN / "artifacts/explorer.json").write_text(text)
    print(text, end="")


if __name__ == "__main__":
    main()
