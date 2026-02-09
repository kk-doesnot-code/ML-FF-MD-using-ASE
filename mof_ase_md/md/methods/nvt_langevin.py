from __future__ import annotations

from ase import units
from ase.md.langevin import Langevin


def build(atoms, cfg: dict):
    """
    NVT: Langevin dynamics (stochastic thermostat).

    Required:
      md.timestep_fs
      state.temperature_K
      thermostat.langevin.friction_per_fs (or default 0.01)

    Optional:
      safety.fix_com (bool) default True

    Notes:
      - No RNG is passed in. Runs are not bitwise reproducible.
    """
    md = cfg["md"]
    state = cfg["state"]

    timestep = float(md["timestep_fs"]) * units.fs
    temperature_K = float(state["temperature_K"])

    thermo = cfg.get("thermostat", {}).get("langevin", {})
    friction_per_fs = float(thermo.get("friction_per_fs", 0.01))
    friction = friction_per_fs / units.fs

    fixcm = bool(cfg.get("safety", {}).get("fix_com", True))

    return Langevin(
        atoms=atoms,
        timestep=timestep,
        temperature_K=temperature_K,
        friction=friction,
        fixcm=fixcm,
    )
