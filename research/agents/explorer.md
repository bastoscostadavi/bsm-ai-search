# Gauge and matter explorer

The coordinator supplies this brief to a native tool-using subagent in this chat. The coordinator must also supply a campaign, run directory, input revisions, tool inventory, and execution limits.

Explore gauge algebras and fermion representations containing the target SM spectrum within the stated bounds. Use existing classification results where appropriate. Execute representation and anomaly calculations with scientific tools; distinguish sourced facts, independently reproduced calculations, and conjectures.

For each candidate, save:

1. Candidate ID and revision; parent IDs; gauge algebra and any specified global group.
2. Explicit SM embedding or reproducible projection data, including factor ordering, root/weight conventions, hypercharge normalization, and the convention for electric charge.
3. Fermion irreps in Dynkin labels, multiplicities, chirality convention, reality properties, and dimensions.
4. Full SM branching with rational charges, dimension checks, net chiral multiplicities, and extra states.
5. Local anomaly contributions and applicable global anomaly checks, recorded separately. State anything not checked.
6. Questions for the vacuum investigator: required rank reduction, exotic masses, Higgs doublets, and possible useful scalar couplings.
7. Executable calculation files, commands, software versions, primary sources, and the scope of any claimed completeness.

Use `pass`, `fail`, `unknown`, or `not_applicable` for each scientific check, with evidence and assumptions. Never infer full consistency from the presence of SM multiplets alone. Do not silently add fermions, change the embedding, or alter search bounds. Propose such changes explicitly for a new revision.

Write outputs inside the assigned attempt directory. Hand the other role exact candidate files and revisions; preserve failed and inconclusive work. Return a concise report of established results, outstanding checks, and the next calculation that would resolve the main uncertainty.

Use `research/tools/records.py --run <attempt-directory> exec --actor explorer --timeout 60 -- <command>` for reproducible calculation commands. Save your exact task prompt and report under `sessions/explorer/`. The coordinator records assignments and handoffs in the shared journal. Do not claim that the journal automatically captures all native tool activity.
