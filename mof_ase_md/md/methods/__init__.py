from __future__ import annotations

import importlib


METHOD_REGISTRY = {
    # NVE
    "velocity_verlet": {
        "ensemble": "nve",
        "module": "mof_ase_md.md.methods.nve_velocity_verlet",
        "callable": "build",
    },

    # NVT
    "langevin": {
        "ensemble": "nvt",
        "module": "mof_ase_md.md.methods.nvt_langevin",
        "callable": "build",
    },
    "nose_hoover_chain_nvt": {
        "ensemble": "nvt",
        "module": "mof_ase_md.md.methods.nvt_nose_hoover_chain",
        "callable": "build",
    },
    "bussi": {
        "ensemble": "nvt",
        "module": "mof_ase_md.md.methods.nvt_bussi",
        "callable": "build",
    },
    "andersen": {
        "ensemble": "nvt",
        "module": "mof_ase_md.md.methods.nvt_andersen",
        "callable": "build",
    },
    "nvt_berendsen": {
        "ensemble": "nvt",
        "module": "mof_ase_md.md.methods.nvt_berendsen",
        "callable": "build",
    },

    # NPT
    "npt_berendsen": {
        "ensemble": "npt",
        "module": "mof_ase_md.md.methods.npt_berendsen",
        "callable": "build",
    },
    "isotropic_mtk": {
        "ensemble": "npt",
        "module": "mof_ase_md.md.methods.npt_isotropic_mtk",
        "callable": "build",
    },
    "mtk": {
        "ensemble": "npt",
        "module": "mof_ase_md.md.methods.npt_mtk",
        "callable": "build",
    },
    "langevin_baoab": {
        "ensemble": "npt",
        "module": "mof_ase_md.md.methods.npt_langevin_baoab",
        "callable": "build",
    },
    "melchionna": {
        "ensemble": "npt",
        "module": "mof_ase_md.md.methods.npt_melchionna",
        "callable": "build",
    },
}


def get_method_info(method_name: str) -> dict:
    if method_name not in METHOD_REGISTRY:
        available = sorted(METHOD_REGISTRY.keys())
        raise ValueError(f"Unknown md.method '{method_name}'. Available: {available}")
    return METHOD_REGISTRY[method_name]


def get_builder(method_name: str):
    info = get_method_info(method_name)

    module_name = info["module"]
    callable_name = info["callable"]

    module = importlib.import_module(module_name)
    builder = getattr(module, callable_name)

    return builder

def list_methods() -> list[str]:
    """
    Return all registered md.method names (sorted).
    """
    return sorted(METHOD_REGISTRY.keys())


