from __future__ import annotations

from ase import units
from ase.md.bussi import Bussi


def build(atoms, cfg: dict):
    """
    NVT: Bussi stochastic velocity-rescaling thermostat.

    Required:
      md.timestep_fs
      state.temperature_K

    Optional:
      thermostat.bussi.taut_fs (default 100.0)
      safety.fix_com (default True)

    Notes:
      - No RNG is passed in. Runs are not bitwise reproducible.
    """
    md = cfg["md"]
    state = cfg["state"]

    timestep = float(md["timestep_fs"]) * units.fs
    temperature_K = float(state["temperature_K"])

    thermo = cfg.get("thermostat", {}).get("bussi", {})
    taut = float(thermo.get("taut_fs", 100.0)) * units.fs

    return Bussi(
        atoms=atoms,
        timestep=timestep,
        temperature_K=temperature_K,
        taut=taut,
    )

