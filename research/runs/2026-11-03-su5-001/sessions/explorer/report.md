# Explorer result, completed by the coordinator

The explorer subagent saved its script, calculation output, and candidate before its session ended with a usage-limit error. The coordinator reviewed those files and wrote this report and the check records afterward. This is not a claim that the specialist session finished its report.

## Exact embedding and branching

Use Y=diag(-1/3,-1/3,-1/3,1/2,1/2), Q=T3+Y, and left-handed Weyl fermions. Fundamental weights are single-index occupations; the 10 weights are unordered pairs of distinct fundamental indices. Charges are computed with Fraction arithmetic. Under the 3+2 block split:

- 5 -> (3,1)_{-1/3} + (1,2)_{1/2}.
- 5bar -> (3bar,1)_{1/3} + (1,2)_{-1/2}.
- 10 -> (3bar,1)_{-2/3} + (3,2)_{1/6} + (1,1)_1.

The pair sectors are exterior-square color (3bar), color times weak, and exterior-square weak (singlet). These identities identify the irreps; grouping charges alone is not a general irrep algorithm. Dimensions are 5,5,10; each 10+5bar is 15 Weyl components and three generations give 45, with net chiral multiplicity three for each SM multiplet and no additional fermions.

## Anomaly derivation

For traceless H=diag(h_i), sum_{i<j}(h_i+h_j)^3=(N-4)sum_i h_i^3. Thus the SU(5) antisymmetric 10 has cubic coefficient +1 relative to the 5, while the 5bar has -1. The code checks three nontrivial Cartan generators. Uniqueness of the SU(5) symmetric cubic invariant makes this ratio sufficient for the local cubic anomaly in this fixed case.

For the SM subgroup the code evaluates traces of H3=diag(1,2,-3,0,0), H2=diag(0,0,0,1,-1), and Y. With A(3)=1 and T(3)=T(2)=1/2, the normalized SU(3)^3, SU(3)^2Y, SU(2)^2Y, Y^3 and mixed gravitational-Y sums vanish separately. Other mixed nonabelian traces vanish by traceless generators; SU(2) has no local cubic invariant. There are 3 colored weak doublets plus 1 lepton doublet per generation, hence an even total of twelve. The ordinary Witten parity test passes on spin spacetime. A complete global anomaly classification remains unknown.

## Global subgroup and handoff

The map (A,B,z)->diag(z^-2 A,z^3 B) has z^6=1 in its kernel, with A=z^2 I3 and B=z^-3 I2. It produces S(U(3)xU(2)) isomorphic to (SU(3)xSU(2)xU(1))/Z6. The integer charge generator here is 6Y. The code verifies all six kernel phases exactly.

The frozen candidate is candidates/su5-r1.json with SHA-256 7f29f55572e38804366c9a68b5e344dd5867de07e7e520401cc433169ddeb785. Its scalar, electroweak and Yukawa completions were explicitly deferred. The vacuum calculation consumes this exact file.

## Reproduction and evidence

From this attempt directory: `python3 code/explorer.py`. Output is artifacts/explorer.json; recorded command outputs live in commands/. Structured claims are in checks/explorer.json. No external Python packages are used.

## Literature context

[Georgi and Glashow, Unity of All Elementary-Particle Forces](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.32.438) is the original SU(5) proposal. [Witten, An SU(2) anomaly](https://doi.org/10.1016/0370-2693(82)90728-6) supplies the ordinary doublet-anomaly context. The branching, kernel and trace values above are reproduced by the saved code rather than taken as computed outputs from those references.
