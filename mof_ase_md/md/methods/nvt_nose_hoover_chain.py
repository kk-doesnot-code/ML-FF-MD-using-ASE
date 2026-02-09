from __future__ import annotations

from ase import units
from ase.md.nose_hoover_chain import NoseHooverChainNVT


def build(atoms, cfg: dict):
    """
    NVT: Nose-Hoover Chain thermostat (deterministic).

    Required:
      md.timestep_fs
      state.temperature_K

    Optional (defaults provided):
      thermostat.nose_hoover_chain.tdamp_fs (default 100.0)
      thermostat.nose_hoover_chain.tchain   (default 3)
      thermostat.nose_hoover_chain.tloop    (default 1)
    """
    md = cfg["md"]
    state = cfg["state"]

    timestep = float(md["timestep_fs"]) * units.fs
    temperature_K = float(state["temperature_K"])

    nhc = cfg.get("thermostat", {}).get("nose_hoover_chain", {})

    tdamp = float(nhc.get("tdamp_fs", 100.0)) * units.fs
    tchain = int(nhc.get("tchain", 3))
    tloop = int(nhc.get("tloop", 1))

    return NoseHooverChainNVT(
        atoms=atoms,
        timestep=timestep,
        temperature_K=temperature_K,
        tdamp=tdamp,
        tchain=tchain,
        tloop=tloop,
    )
