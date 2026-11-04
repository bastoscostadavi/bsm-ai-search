"""Coordinator verification: fresh-directory reproduction and polynomial Hessian."""
from fractions import Fraction as F
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

RUN = Path(__file__).resolve().parents[1]


def multiply(x, y):
    # Independent full matrix multiplication over Q(i).
    result = {}
    for (i, j), (a, b) in x.items():
        for (k, l), (c, d) in y.items():
            if j == k:
                real, imag = result.get((i, l), (F(0), F(0)))
                result[i, l] = (real + a*c - b*d, imag + a*d + b*c)
    return {key: val for key, val in result.items() if val != (0, 0)}


def potential(x):
    x2 = multiply(x, x)
    x4 = multiply(x2, x2)
    tr2 = sum(x2.get((i, i), (0, 0))[0] for i in range(5))
    tr4 = sum(x4.get((i, i), (0, 0))[0] for i in range(5))
    return -F(44, 2)*tr2 + F(1, 4)*tr2**2 + F(1, 2)*tr4


def add(x, y):
    return {key: (x.get(key, (0, 0))[0] + y.get(key, (0, 0))[0],
                  x.get(key, (0, 0))[1] + y.get(key, (0, 0))[1]) for key in x.keys() | y.keys()}


def main():
    spec = importlib.util.spec_from_file_location('vacuum', RUN / 'code/vacuum.py')
    vacuum = importlib.util.module_from_spec(spec)
    # Avoid writing __pycache__ into the archived calculation directory.
    sys.dont_write_bytecode = True
    spec.loader.exec_module(vacuum)
    base = {(i, i): (d, F(0)) for i, d in enumerate(vacuum.D)}

    def curvature(direction):
        def at(t):
            return potential(add(base, {key: (t*a, t*b) for key, (a, b) in direction.items()}))
        f0 = at(F(0))
        s1 = at(F(1)) + at(F(-1)) - 2*f0
        s2 = at(F(2)) + at(F(-2)) - 2*f0
        # Exact cancellation of the quartic term in this degree-four polynomial.
        return (16*s1 - s2) / 12

    basis = vacuum.basis()
    for _, _, direction in basis:
        assert curvature(direction) == vacuum.hessian(direction, direction)
    mixed = 0
    for i in range(24):
        for j in range(i + 1, 24):
            x, y = basis[i][2], basis[j][2]
            cross = (curvature(add(x, y)) - curvature(x) - curvature(y)) / 2
            assert cross == vacuum.hessian(x, y)
            mixed += 1

    with tempfile.TemporaryDirectory() as temporary:
        clean = Path(temporary)
        for folder in ['code', 'candidates']:
            shutil.copytree(RUN / folder, clean / folder)
        (clean / 'artifacts').mkdir()
        for role in ['explorer', 'vacuum']:
            subprocess.run([sys.executable, str(clean / 'code' / f'{role}.py')], cwd=clean, capture_output=True, text=True, check=True, timeout=60)
            original = json.loads((RUN / 'artifacts' / f'{role}.json').read_text())
            reproduced = json.loads((clean / 'artifacts' / f'{role}.json').read_text())
            assert original == reproduced, f'{role} output changed in fresh directory'
    required = {'check_id', 'candidate_id', 'candidate_revision', 'status', 'statement', 'scope', 'assumptions', 'approximation', 'evidence_paths', 'limitations'}
    counts = {}
    for source in ['explorer', 'vacuum']:
        checks = json.loads((RUN / 'checks' / f'{source}.json').read_text())
        for check in checks:
            assert required <= check.keys()
            assert check['candidate_revision'] == 'r1'
            assert check['status'] in {'pass', 'fail', 'unknown', 'not_applicable'}
            for relative in check['evidence_paths']:
                assert (RUN / relative).is_file(), relative
            counts[check['status']] = counts.get(check['status'], 0) + 1
    result = {'fresh_directory_reproduction': ['explorer', 'vacuum'], 'exact_polynomial_diagonal_curvatures': 24, 'exact_polynomial_mixed_curvatures': mixed, 'scientific_check_status_counts': counts, 'all_assertions_passed': True, 'limitation': 'Reproduction and consistency checks are not independent proof of complete model viability.'}
    (RUN / 'artifacts/review.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
