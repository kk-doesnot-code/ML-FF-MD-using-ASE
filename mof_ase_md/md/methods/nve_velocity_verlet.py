from __future__ import annotations

from ase import units
from ase.md.verlet import VelocityVerlet


def build(atoms, cfg: dict):
    """
    NVE: Velocity Verlet dynamics.

    Required:
      md.timestep_fs
    """
    md = cfg["md"]
    timestep = float(md["timestep_fs"]) * units.fs

    return VelocityVerlet(
        atoms=atoms,
        timestep=timestep,
    )
