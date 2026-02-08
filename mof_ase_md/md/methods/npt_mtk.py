from __future__ import annotations

from ase import units
from ase.md.nose_hoover_chain import MTKNPT


METHOD = "npt_mtk"
ENSEMBLE = "npt"


def build(atoms, cfg: dict):
    """
    Full (flexible cell) Martyna–Tobias–Klein (MTK) NPT dynamics.

    ASE signature:
      MTKNPT(atoms, timestep, temperature_K, pressure_au, tdamp, pdamp,
             tchain=3, pchain=3, tloop=1, ploop=1)
    """
    md = cfg["md"]
    state = cfg["state"]

    timestep = float(md["timestep_fs"]) * units.fs
    temperature_K = float(state["temperature_K"])
    pressure_au = float(state["pressure_bar"]) * units.bar

    nhc = cfg.get("thermostat", {}).get("nose_hoover_chain", {})
    mtk = cfg.get("barostat", {}).get("mtk", {})

    tdamp = float(nhc.get("tdamp_fs", 100.0)) * units.fs
    pdamp = float(mtk.get("pdamp_fs", 1000.0)) * units.fs

    tchain = int(nhc.get("tchain", 3))
    tloop = int(nhc.get("tloop", 1))

    pchain = int(mtk.get("pchain", 3))
    ploop = int(mtk.get("ploop", 1))

    return MTKNPT(
        atoms=atoms,
        timestep=timestep,
        temperature_K=temperature_K,
        pressure_au=pressure_au,
        tdamp=tdamp,
        pdamp=pdamp,
        tchain=tchain,
        pchain=pchain,
        tloop=tloop,
        ploop=ploop,
    )
