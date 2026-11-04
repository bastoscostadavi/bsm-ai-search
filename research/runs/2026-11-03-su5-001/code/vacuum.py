#!/usr/bin/env python3
"""Exact, narrow SU(5) real-adjoint tree-level vacuum calculation.

Uses a sparse rational Gaussian-number basis for 24 Hermitian traceless matrices.
No external symbolic/numerical libraries are required. See the saved report for
normalizations, derivations, and limitations.
"""
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[1]
D = (F(2), F(2), F(2), F(-3), F(-3))
CONTROL = (F(1), F(1), F(1), F(1), F(-4))
A, B, VEV_SCALE = F(1), F(1), F(1)
M2 = (30 * A + 14 * B) * VEV_SCALE**2
ZERO = (F(0), F(0))


def gaussian_product(x, y):
    return (x[0] * y[0] - x[1] * y[1],
            x[0] * y[1] + x[1] * y[0])


def weighted_trace_xy(x, y, weight):
    """Sum_ij weight(i,j) X_ij Y_ji in exact rational arithmetic."""
    real = F(0)
    imaginary = F(0)
    for (i, j), value in x.items():
        product = gaussian_product(value, y.get((j, i), ZERO))
        real += weight(i, j) * product[0]
        imaginary += weight(i, j) * product[1]
    assert imaginary == 0
    return real


def trace_xy(x, y):
    return weighted_trace_xy(x, y, lambda i, j: F(1))


def trace_dx(x):
    result = sum(D[i] * x.get((i, i), ZERO)[0] for i in range(5))
    assert all(x.get((i, i), ZERO)[1] == 0 for i in range(5))
    return result


def hessian(x, y):
    s2 = sum(d**2 for d in D)
    # Polarization of delta^2 V, for c=0 in V's cubic invariant.
    return ((-M2 + A * s2) * trace_xy(x, y)
            + 2 * A * trace_dx(x) * trace_dx(y)
            + 2 * B * weighted_trace_xy(x, y, lambda i, j: D[i]**2 + D[j]**2)
            + 2 * B * weighted_trace_xy(x, y, lambda i, j: D[i] * D[j]))


def basis():
    result = []
    for i in range(5):
        for j in range(i + 1, 5):
            sector = 'octet' if j < 3 else ('triplet' if i >= 3 else 'goldstone')
            result.append((f'real_{i+1}{j+1}', sector,
                           {(i, j): (F(1), F(0)), (j, i): (F(1), F(0))}))
            result.append((f'imaginary_{i+1}{j+1}', sector,
                           {(i, j): (F(0), F(1)), (j, i): (F(0), F(-1))}))
    for label, sector, diagonal in [
        ('color_cartan_1', 'octet', (1, -1, 0, 0, 0)),
        ('color_cartan_2', 'octet', (1, 1, -2, 0, 0)),
        ('weak_cartan', 'triplet', (0, 0, 0, 1, -1)),
        ('radial', 'singlet', D),
    ]:
        result.append((label, sector, {(i, i): (F(d), F(0))
                                      for i, d in enumerate(diagonal) if d}))
    return result


def stabilizer(diagonal):
    # For Hermitian diagonal D, [T,D]_ij = (d_j-d_i) T_ij.
    multiplicities = sorted(Counter(diagonal).values(), reverse=True)
    dimension = sum(n**2 for n in multiplicities) - 1
    return {'eigenvalue_multiplicities': multiplicities,
            'unbroken_generators': dimension, 'broken_generators': 24 - dimension,
            'condition': '[T,D]_ij=(d_j-d_i)T_ij=0; sum_i T_ii=0'}


def encode(value):
    if isinstance(value, F):
        return str(value)
    raise TypeError(type(value).__name__)


def main():
    candidate_path = RUN / 'candidates/su5-r1.json'
    candidate_bytes = candidate_path.read_bytes()
    candidate = json.loads(candidate_bytes)
    # Reject a different gauge group or an incompatible explicit handoff.
    assert candidate['gauge_group'] == 'SU(5), simply connected'
    assert candidate['revision'] == 'r1'
    assert candidate['embedding']['hypercharge_generator'] == ['-1/3'] * 3 + ['1/2'] * 2
    candidate_hash = hashlib.sha256(candidate_bytes).hexdigest()
    assert candidate_hash == '7f29f55572e38804366c9a68b5e344dd5867de07e7e520401cc433169ddeb785'
    assert sum(D) == 0 and sum(CONTROL) == 0
    gradient = [(-M2 + A * sum(d**2 for d in D)) * d + 2 * B * d**3 for d in D]
    assert len(set(gradient)) == 1  # identity component removed by tracelessness
    vectors = basis()
    assert len(vectors) == 24
    kinetic = [[2 * trace_xy(x, y) for _, _, y in vectors] for _, _, x in vectors]
    mass_hessian = [[hessian(x, y) for _, _, y in vectors] for _, _, x in vectors]
    for i in range(24):
        assert kinetic[i][i] > 0
        for j in range(24):
            if i != j:
                assert kinetic[i][j] == 0 and mass_hessian[i][j] == 0
    physical = []
    for i, (label, sector, _) in enumerate(vectors):
        mass = mass_hessian[i][i] / kinetic[i][i]
        expected = {'octet': 5 * B, 'triplet': 20 * B, 'singlet': M2, 'goldstone': F(0)}[sector]
        assert mass == expected and mass >= 0
        physical.append({'direction': label, 'sector': sector, 'mass_squared': mass,
                         'kinetic_metric': kinetic[i][i], 'hessian': mass_hessian[i][i]})
    multiplicities = Counter(str(item['mass_squared']) for item in physical)
    assert multiplicities == {'0': 12, '5': 8, '20': 3, '44': 1}
    target = stabilizer(D)
    control = stabilizer(CONTROL)
    assert target['unbroken_generators'] == 12 and control['unbroken_generators'] == 16
    assert target['eigenvalue_multiplicities'] == [3, 2]
    assert control['eigenvalue_multiplicities'] == [4, 1]
    result = {
        'candidate_handoff': {'path': 'candidates/su5-r1.json', 'sha256': candidate_hash},
        'conventions': {'field': 'Hermitian traceless 5x5 Sigma', 'kinetic': 'L_kin=Tr(D_mu Sigma D^mu Sigma)', 'normalized_generators': 'Tr(T_A T_B)=delta_AB/2', 'rational_basis': 'Unnormalized orthogonal Hermitian basis; physical masses solve H x = m_scalar^2 K x with K_AB=2 Tr(B_A B_B)', 'hypercharge': 'Q=T3+Y; Y=diag(-1/3,-1/3,-1/3,1/2,1/2); target D=-6Y'},
        'renormalizable_invariants': ['Tr(Sigma^2)', 'Tr(Sigma^3)', '(Tr(Sigma^2))^2', 'Tr(Sigma^4)'],
        'potential': 'V=-m^2 Tr(Sigma^2)/2 + c Tr(Sigma^3)/3 + a (Tr(Sigma^2))^2/4 + b Tr(Sigma^4)/2',
        'parameters': {'m_squared': M2, 'c': F(0), 'a': A, 'b': B, 'v': VEV_SCALE},
        'target_vev_diagonal': D,
        'stationarity': {'unprojected_diagonal_gradient': gradient, 'projected_gradient': [x - sum(gradient)/5 for x in gradient], 'condition': 'm^2=(30a+14b)v^2 for c=0'},
        'boundedness': {'sufficient_region': 'a>0, b>0', 'proof': 'V4=a(Tr Sigma^2)^2/4 + b Tr Sigma^4/2 >= a(Tr Sigma^2)^2/4 > 0 for nonzero Hermitian Sigma; hence coercive quartic dominates the quadratic'},
        'target_stabilizer': {**target, 'lie_algebra': 'su(3)+su(2)+u(1)', 'group': 'S(U(3) x U(2)) = (SU(3) x SU(2) x U(1))/Z6'},
        'control_stabilizer': {**control, 'lie_algebra': 'su(4)+u(1)', 'group': 'S(U(4) x U(1)) = (SU(4) x U(1))/Z4', 'matches_target': False, 'note': 'This is a stabilizer control, not a claimed stationary point for the selected potential.'},
        'hessian': {'basis': [x[0] for x in vectors], 'matrix': mass_hessian, 'kinetic_metric': kinetic, 'directions': physical, 'mass_squared_multiplicities': dict(multiplicities)},
        'gauge_bosons': {'massless': 12, 'mass_squared_25_g_squared_v_squared': 12, 'normalization': 'L_gauge=-F_A^2/4; D_mu Sigma=partial_mu Sigma-i g[A_mu,Sigma]'},
        'local_stability_region': 'Within c=0 slice: a>0, b>0, m^2>0, v^2=m^2/(30a+14b). Gauge-normal scalar eigenvalues 5bv^2 (8),20bv^2 (3),m^2 (1) are strictly positive; remaining 12 are gauge orbit directions.',
        'global_minimality': 'unknown: no comparison of all inequivalent stationary orbits was performed',
        'limitations': ['cubic-free slice only; a Sigma->-Sigma symmetry can enforce c=0 in the scalar sector', 'tree-level calculation only', 'no electroweak Higgs or Yukawa completion', 'no neutrino, dark matter, or phenomenological viability conclusion'],
    }
    output = RUN / 'artifacts/vacuum.json'
    output.write_text(json.dumps(result, indent=2, default=encode) + '\n')
    print(json.dumps({'artifact': str(output.relative_to(RUN)), 'candidate_sha256': candidate_hash,
                      'target_unbroken_generators': target['unbroken_generators'],
                      'control_unbroken_generators': control['unbroken_generators'],
                      'mass_squared_multiplicities': dict(multiplicities),
                      'all_assertions_passed': True}, indent=2))


if __name__ == '__main__':
    main()
