# Vacuum result, completed by the coordinator

The vacuum subagent saved code/vacuum.py before its session ended with a usage-limit error. Its original draft is retained as sessions/vacuum/agent-draft.py. The coordinator strengthened candidate-file validation, ran the calculation, reviewed its formulas, and wrote this report and the structured checks. The specialist session itself did not complete.

## Scope and invariants

Sigma is a Hermitian traceless 5x5 real adjoint field. Conjugation-invariant polynomials are symmetric functions of its real eigenvalues. With Tr Sigma=0, the renormalizable nonconstant invariant types are Tr Sigma^2, Tr Sigma^3, (Tr Sigma^2)^2 and Tr Sigma^4. We use

V = -m^2 Tr(Sigma^2)/2 + c Tr(Sigma^3)/3 + a (Tr(Sigma^2))^2/4 + b Tr(Sigma^4)/2.

The benchmark restricts c=0. A Sigma->-Sigma scalar-sector symmetry can enforce that slice; compatibility with a later full interaction sector is not established. It is not a scan of the general cubic potential.

## Stabilizers and stationarity

For diagonal D, [T,D]_ij=(d_j-d_i)T_ij. Multiplicities 3+2 yield 3^2+2^2-1=12 unbroken generators: su(3)+su(2)+u(1), globally S(U(3)xU(2)). Multiplicities 4+1 in the control yield 16 and su(4)+u(1), globally S(U(4)xU(1)). The control intentionally fails the SM target and is not claimed stationary for the benchmark couplings.

At Sigma=v diag(2,2,2,-3,-3), Tr Sigma^2=30v^2. The unconstrained diagonal gradient is (-m^2+a Tr Sigma^2)d_i+2b d_i^3. It is proportional to the identity when m^2=(30a+14b)v^2; its projection onto traceless fluctuations therefore vanishes. For a=b=v=1, m^2=44 and the five unconstrained components are all -12, with zero projected gradient.

## Boundedness and physical Hessian

For a>0,b>0, V4 >= a(Tr Sigma^2)^2/4 > 0 for nonzero Hermitian Sigma. The coercive quartic dominates the quadratic, establishing boundedness in this sufficient region.

Use Lkin=Tr(D_mu Sigma D^mu Sigma), and normalized generators with Tr(TA TB)=deltaAB/2. The calculation uses an unnormalized rational Hermitian basis of 24 directions, records K_AB=2Tr(BA BB), computes the full Hessian H, and solves the diagonal generalized mass problem Hx=m_scalar^2 Kx. The basis includes real and imaginary off-diagonal entries, two color Cartans, one weak Cartan, and the radial direction.

Polarizing the quartic gives, at c=0,

H(X,Y)=(-m^2+a Tr D^2)Tr(XY)+2a Tr(DX)Tr(DY)+2b Tr[(D_i^2+D_j^2)X_ij Y_ji]+2b Tr[D_i D_j X_ij Y_ji],

where the final two expressions denote sums over i,j. The saved script implements these sums exactly over rational real/imaginary pairs. At the benchmark point physical mass squares are 5 for 8 octet modes, 20 for 3 triplet modes, and 44 for the radial singlet. Twelve zero modes are the broken-generator gauge orbit directions. Thus the vacuum is locally stable modulo gauge orbits. Within the c=0 slice, a,b,m^2>0 gives the analogous positive masses 5bv^2,20bv^2,m^2. There are twelve massive gauge bosons with M^2=25g^2v^2 in the stated conventions, and twelve massless ones; this gauge-mass value follows analytically from the commutator and is not a separate full gauge-matrix implementation.

The coordinator's code/review.py checks all 24 diagonal and 276 mixed Hessian entries independently by exact degree-four polynomial evaluation of the full potential, rather than reusing the polarized Hessian formula.

## Limits and reproduction

Global minimality remains unknown: no exhaustive comparison of inequivalent stationary orbits is performed. Loop corrections, electroweak Higgs/Yukawa completion, neutrinos, dark matter, unification and proton-decay constraints remain deferred. This is a known-model workflow benchmark, not a viable new BSM model.

From the attempt directory run `python3 code/vacuum.py`; output is artifacts/vacuum.json. Run `python3 code/review.py` to check the Hessian and clean-directory reproduction. Structured results are in checks/vacuum.json.

The original [SU(5) proposal](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.32.438) supplies historical context. The invariant reduction, stationarity, boundedness and scalar masses reported here are explicit calculations in the saved normalization, not masses quoted from a differently normalized source.
