from __future__ import annotations

from ase import units
from ase.md.melchionna import MelchionnaNPT


METHOD = "npt_melchionna"
ENSEMBLE = "npt"


def build(atoms, cfg: dict):
    """
    Melchionna NPT dynamics (Nose-Hoover thermostat + Parrinello-Rahman barostat).

    ASE signature:
      MelchionnaNPT(atoms, timestep, temperature_K=..., externalstress=...,
                    ttime=..., pfactor=..., mask=...)
    """
    md = cfg["md"]
    state = cfg["state"]

    timestep = float(md["timestep_fs"]) * units.fs
    temperature_K = float(state["temperature_K"])
    pressure_au = float(state["pressure_bar"]) * units.bar

    mel = cfg.get("barostat", {}).get("melchionna", {})

    # In MelchionnaNPT docs: scalar p corresponds to tensor (-p,-p,-p,0,0,0),
    # so giving +pressure_au means compression (good).
    externalstress = pressure_au

    ttime = mel.get("ttime_fs", None)
    ttime = None if ttime is None else float(ttime) * units.fs

    pfactor = mel.get("pfactor", None)
    pfactor = None if pfactor is None else float(pfactor)

    mask = mel.get("mask", None)

    return MelchionnaNPT(
        atoms=atoms,
        timestep=timestep,
        temperature_K=temperature_K,
        externalstress=externalstress,
        ttime=ttime,
        pfactor=pfactor,
        mask=mask,
    )
