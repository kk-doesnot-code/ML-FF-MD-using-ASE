from __future__ import annotations

from pathlib import Path

from ase.io.trajectory import Trajectory
from ase.md import MDLogger


def attach_outputs(dyn, atoms, cfg: dict):
    """
    Attach trajectory + logger output writers to an ASE dynamics object.
    """
    output_cfg = cfg["output"]

    workdir = Path(output_cfg["workdir"])
    workdir.mkdir(parents=True, exist_ok=True)

    traj_filename = output_cfg["trajectory_file"]
    log_filename = output_cfg["log_file"]

    traj_path = workdir / traj_filename
    log_path = workdir / log_filename

    traj_interval = output_cfg["traj_interval"]
    log_interval = output_cfg["log_interval"]

    append_traj = output_cfg.get("append_trajectory", False)

    traj_mode = "a"
    if append_traj is False:
        traj_mode = "w"

    trajectory = Trajectory(
        str(traj_path),
        mode=traj_mode,
        atoms=atoms
    )

    dyn.attach(
        trajectory.write,
        interval=traj_interval
    )

    logging_cfg = cfg.get("logging", {})

    stress = logging_cfg.get("stress", True)
    per_atom = logging_cfg.get("per_atom", False)

    mode = logging_cfg.get("mode", "w")

    logger = MDLogger(
        dyn=dyn,
        atoms=atoms,
        logfile=str(log_path),
        stress=stress,
        peratom=per_atom,
        mode=mode
    )

    dyn.attach(
        logger,
        interval=log_interval
    )

    return traj_path, log_path
