from __future__ import annotations

from ase import units
from ase.md.langevinbaoab import LangevinBAOAB


def build(atoms, cfg: dict):
    md = cfg["md"]
    state = cfg["state"]

    timestep = float(md["timestep_fs"]) * units.fs
    temperature_K = float(state["temperature_K"])
    pressure_au = float(state["pressure_bar"]) * units.bar

    # ASE convention: externalstress = -pressure for compression
    externalstress = -pressure_au

    baoab = cfg.get("barostat", {}).get("baoab", {})

    hydrostatic = bool(baoab.get("hydrostatic", False))

    T_tau = baoab.get("T_tau_fs", None)
    P_tau = baoab.get("P_tau_fs", None)

    T_tau = None if T_tau is None else float(T_tau) * units.fs
    P_tau = None if P_tau is None else float(P_tau) * units.fs

    P_mass = baoab.get("P_mass", None)
    P_mass = None if P_mass is None else float(P_mass)

    P_mass_factor = float(baoab.get("P_mass_factor", 1.0))
    disable_cell_langevin = bool(baoab.get("disable_cell_langevin", False))

    return LangevinBAOAB(
        atoms=atoms,
        timestep=timestep,
        temperature_K=temperature_K,
        externalstress=externalstress,
        hydrostatic=hydrostatic,
        T_tau=T_tau,
        P_tau=P_tau,
        P_mass=P_mass,
        P_mass_factor=P_mass_factor,
        disable_cell_langevin=disable_cell_langevin,
        rng=1
        )
