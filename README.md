# ML-FF-MD-using-ASE

Run Molecular Dynamics (MD) for MOF structures using ASE dynamics and an ML force field (ORB) wrapped as an ASE calculator.

## Features
- YAML config-driven runs (no editing code for parameters)
- Supports multiple ensembles and methods:
  - **NVE**: velocity_verlet
  - **NVT**: langevin, nose_hoover_chain_nvt, bussi, andersen, nvt_berendsen
  - **NPT**: npt_berendsen, isotropic_mtk, mtk, langevin_baoab, melchionna
- Automatic defaults (method-specific) + config validation
- Writes trajectory, log, final structure, and resolved config copy

## Quickstart

### 1) Validate a config
python -m mof_ase_md.cli validate examples/npt_isotropic_mtk.yaml

### 2) List available methods
python -m mof_ase_md.cli list-methods

### 3) Run MD
python -m mof_ase_md.cli run examples/npt_isotropic_mtk.yaml

### 4) Print resolved config (defaults applied)
python -m mof_ase_md.cli print-config examples/npt_isotropic_mtk.yaml

