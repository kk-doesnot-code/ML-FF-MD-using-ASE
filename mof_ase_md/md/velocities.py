from __future__ import annotations
from ase.md.velocitydistribution import (
    MaxwellBoltzmannDistribution,
    Stationary,
    ZeroRotation
)

def initialize_velocities(atoms, cfg: dict):
    """
    Initialize velocities according to cfg["velocities"].
    """
    vel_cfg = cfg.get("velocities", {})

    initialize = vel_cfg.get("initialize", True)
    if initialize is False:
        return

    method = vel_cfg.get("method", "maxwell")

    temperature_K = None
    state_cfg = cfg.get("state", {})
    if "temperature_K" in state_cfg:
        temperature_K = state_cfg["temperature_K"]

    seed = vel_cfg.get("seed", None)

    if method == "none":
        pass

    elif method == "maxwell":
        if temperature_K is None:
            raise ValueError("velocities.method='maxwell' requires state.temperature_K")

        MaxwellBoltzmannDistribution(
            atoms,
            temperature_K=temperature_K,
        )

    else:
        raise ValueError(f"Unknown velocities.method: {method}")

    zero_com = vel_cfg.get("zero_com", True)
    if zero_com is True:
        Stationary(atoms)

    zero_rotation = vel_cfg.get("zero_rotation", False)
    if zero_rotation is True:
        ZeroRotation(atoms)