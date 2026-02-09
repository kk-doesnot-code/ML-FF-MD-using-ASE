from __future__ import annotations
from ase.io import read


def load_atoms(cfg: dict):
    """
    Load an ASE Atoms object from the structure file defined in config.
    """
    system_cfg = cfg["system"]
    
    input_path = system_cfg["input_file"]
    fmt = system_cfg.get("format", None)

    if fmt is not None:
        atoms = read(input_path, format=fmt)
    else:
        atoms = read(input_path)

    atoms.pbc = bool(system_cfg["pbc"])

    charge = system_cfg.get("charge", None)
    spin = system_cfg.get("spin", None)

    if charge is not None:
        atoms.info["charge"] = charge

    if spin is not None:
        atoms.info["spin"] = spin

    return atoms
