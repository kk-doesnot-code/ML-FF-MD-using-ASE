from __future__ import annotations

from ase import units
from ase.md.nptberendsen import NPTBerendsen


def build(atoms, cfg: dict):
    """
    Build an NPT Berendsen dynamics object.

    Required config keys:
      md.timestep_fs
      state.temperature_K
      state.pressure_bar

      barostat.berendsen.taut_fs
      barostat.berendsen.taup_fs
      barostat.berendsen.compressibility_per_bar
    """
    md_cfg = cfg["md"]
    state_cfg = cfg["state"]

    timestep_fs = md_cfg["timestep_fs"]
    timestep = timestep_fs * units.fs

    temperature_K = state_cfg["temperature_K"]

    pressure_bar = state_cfg["pressure_bar"]
    pressure_au = pressure_bar * units.bar

    barostat_cfg = cfg["barostat"]["berendsen"]

    taut_fs = barostat_cfg["taut_fs"]
    taup_fs = barostat_cfg["taup_fs"]

    taut = taut_fs * units.fs
    taup = taup_fs * units.fs

    compressibility_per_bar = barostat_cfg["compressibility_per_bar"]
    compressibility_au = compressibility_per_bar / units.bar

    dynamics = NPTBerendsen(
        atoms=atoms,
        timestep=timestep,
        temperature_K=temperature_K,
        pressure_au=pressure_au,
        taut=taut,
        taup=taup,
        compressibility_au=compressibility_au,
    )

    return dynamics
