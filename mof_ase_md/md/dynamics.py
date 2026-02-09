from __future__ import annotations

from mof_ase_md.md.methods import get_method_info, get_builder


def make_dynamics(atoms, cfg: dict):
    md_cfg = cfg["md"]

    ensemble = md_cfg["ensemble"]
    method = md_cfg["method"]

    info = get_method_info(method)
    expected_ensemble = info["ensemble"]

    if ensemble != expected_ensemble:
        raise ValueError(
            "Ensemble/method mismatch. "
            f"md.ensemble='{ensemble}' but md.method='{method}' requires '{expected_ensemble}'."
        )

    builder = get_builder(method)
    dynamics = builder(atoms, cfg)

    return dynamics
