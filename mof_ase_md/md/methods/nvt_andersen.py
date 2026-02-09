from __future__ import annotations

from ase import units
from ase.md.andersen import Andersen


def build(atoms, cfg: dict):
    """
    NVT: Andersen thermostat (stochastic collisions).

    Required:
      md.timestep_fs
      state.temperature_K

    Optional:
      thermostat.andersen.collision_probability (default 0.002)

    Notes:
      - No RNG is passed in. Runs are not bitwise reproducible.
    """
    md = cfg["md"]
    state = cfg["state"]

    timestep = float(md["timestep_fs"]) * units.fs
    temperature_K = float(state["temperature_K"])

    thermo = cfg.get("thermostat", {}).get("andersen", {})
    collision_probability = float(thermo.get("collision_probability", 0.002))

    andersen_prob = float(thermo.get("andersen_prob", 0.002))

    return Andersen(
        atoms=atoms,
        timestep=timestep,
        temperature_K=temperature_K,
        # collision_probability=collision_probability,
        andersen_prob=andersen_prob,
    )
