from __future__ import annotations

from ase import units
from ase.md.nvtberendsen import NVTBerendsen


def build(atoms, cfg: dict):
    """
    NVT: Berendsen thermostat (weak coupling).

    Required:
      md.timestep_fs
      state.temperature_K

    Optional:
      thermostat.berendsen.taut_fs (default 100.0)
      safety.fix_com (default True)
    """
    md = cfg["md"]
    state = cfg["state"]

    timestep = float(md["timestep_fs"]) * units.fs
    temperature_K = float(state["temperature_K"])

    thermo = cfg.get("thermostat", {}).get("berendsen", {})
    taut = float(thermo.get("taut_fs", 100.0)) * units.fs

    fixcm = bool(cfg.get("safety", {}).get("fix_com", True))

    return NVTBerendsen(
        atoms=atoms,
        timestep=timestep,
        temperature_K=temperature_K,
        taut=taut,
        fixcm=fixcm,
    )
