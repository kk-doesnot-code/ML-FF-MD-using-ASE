from __future__ import annotations

from pathlib import Path
import yaml

from ase.io import write

from mof_ase_md.config.defaults import apply_defaults
from mof_ase_md.config.loader import load_config
from mof_ase_md.config.validator import validate_config
from mof_ase_md.system.atoms import load_atoms
from mof_ase_md.calculator.orb import build_orb_calculator
from mof_ase_md.md.velocities import initialize_velocities
from mof_ase_md.md.dynamics import make_dynamics
from mof_ase_md.md.outputs import attach_outputs


def run(config_path: str) -> None:
    """
    Main orchestration function for a single-ensemble ASE MD run.
    """
    # ---- load + validate config ----
    cfg = load_config(config_path)
    cfg = apply_defaults(cfg)
    cfg = validate_config(cfg)

    # ---- prepare output directory ----
    output_cfg = cfg["output"]
    workdir = Path(output_cfg["workdir"])
    workdir.mkdir(parents=True, exist_ok=True)

    # ---- load atoms ----
    atoms = load_atoms(cfg)

    # ---- attach calculator ----
    calculator = build_orb_calculator(cfg)
    atoms.calc = calculator

    # ---- velocities ----
    initialize_velocities(atoms, cfg)

    # ---- dynamics ----
    dynamics = make_dynamics(atoms, cfg)

    # ---- outputs ----
    attach_outputs(dynamics, atoms, cfg)

    # ---- run ----
    md_cfg = cfg["md"]
    total_steps = md_cfg["total_steps"]

    dynamics.run(total_steps)

    # ---- write final structure ----
    final_name = output_cfg.get("final_structure", "final.xyz")
    final_path = workdir / final_name

    write(str(final_path), atoms)

    # ---- copy config used ----
    write_copy = output_cfg.get("write_config_copy", True)
    if write_copy is True:
        dst = workdir / "config_used.yaml"
        with open(dst, "w", encoding="utf-8") as f:
            yaml.safe_dump(cfg, f, sort_keys=False)


    print("RUN COMPLETE")
    print("Workdir:", workdir)
    print("Final structure:", final_path)
