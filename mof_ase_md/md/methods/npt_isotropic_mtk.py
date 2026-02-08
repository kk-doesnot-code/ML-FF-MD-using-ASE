from __future__ import annotations

from ase import units
from ase.md.nose_hoover_chain import IsotropicMTKNPT


def build(atoms, cfg: dict):
    """
    Build an IsotropicMTKNPT dynamics object.

    Requires config:
      md.timestep_fs
      state.temperature_K
      state.pressure_bar

      thermostat.nose_hoover_chain.tdamp_fs
      thermostat.nose_hoover_chain.tchain
      thermostat.nose_hoover_chain.tloop   (optional)

      barostat.mtk.pdamp_fs
      barostat.mtk.pchain
      barostat.mtk.ploop    (optional)
    """
    md_cfg = cfg["md"]
    state_cfg = cfg["state"]

    timestep_fs = md_cfg["timestep_fs"]
    timestep = timestep_fs * units.fs

    temperature_K = state_cfg["temperature_K"]

    pressure_bar = state_cfg["pressure_bar"]
    pressure_au = pressure_bar * units.bar

    thermostat_cfg = cfg.get("thermostat", {})
    nhc_cfg = thermostat_cfg.get("nose_hoover_chain", {})

    tdamp_fs = nhc_cfg.get("tdamp_fs", 100.0)
    tdamp = tdamp_fs * units.fs

    tchain = nhc_cfg.get("tchain", 3)
    tloop = nhc_cfg.get("tloop", 1)

    barostat_cfg = cfg.get("barostat", {})
    mtk_cfg = barostat_cfg.get("mtk", {})

    pdamp_fs = mtk_cfg.get("pdamp_fs", 1000.0)
    pdamp = pdamp_fs * units.fs

    pchain = mtk_cfg.get("pchain", 3)
    ploop = mtk_cfg.get("ploop", 1)

    dynamics = IsotropicMTKNPT(
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

    return dynamics
