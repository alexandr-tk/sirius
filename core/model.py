"""Bpy-free data model for drone show choreography.

All classes in this module are pure Python dataclasses with no Blender
dependencies. They form the authoritative source of truth for a show's
structure — the ``blender/`` adapter layer reads and writes these
objects, while algorithms (assignment, collision, interpolation) operate
on them directly.

See ``project-plan.md`` §1.3–§1.5 for the architectural rationale behind
keeping the domain model Blender-free.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np


@dataclass
class Geofence:
    """Bounding volume that constrains where drones may fly.

    The fence is defined as an axis-aligned bounding box in meters,
    expressed in the show's local coordinate frame (Blender Z-up).

    Attributes
    ----------
    min_pos : np.ndarray
        Minimum X/Y/Z coordinates drones may occupy, shape (3,).
    max_pos : np.ndarray
        Maximum X/Y/Z coordinates drones may occupy, shape (3,).
    max_altitude : float
        Hard ceiling above the ground plane (Z >= 0).  ``max_pos[2]``
        should be consistent with this value, but ``max_altitude`` is
        checked separately because it has operational meaning
        (regulatory / safety) distinct from the bounding box.
    """

    min_pos: np.ndarray = field(default_factory=lambda: np.zeros(3))
    max_pos: np.ndarray = field(default_factory=lambda: np.array([500.0, 500.0, 150.0]))
    max_altitude: float = 150.0

    def contains(self, point: np.ndarray) -> bool:
        """Return True if *point* (shape (3,) or (N, 3)) is inside the fence."""
        point = np.asarray(point)
        if point.ndim == 1:
            return bool(
                np.all(point >= self.min_pos)
                and np.all(point <= self.max_pos)
                and point[2] <= self.max_altitude
            )
        return bool(
            np.all(point >= self.min_pos, axis=-1).all()
            and np.all(point <= self.max_pos, axis=-1).all()
            and np.all(point[..., 2] <= self.max_altitude)
        )


@dataclass
class Drone:
    """A single drone in the show.

    Attributes
    ----------
    id : int
        Stable, non-reorderable identifier.  Assignment algorithms change
        *slots*, never identity (see ``project-plan.md`` §1.4 — "stable
        point index / drone_id").
    home : np.ndarray
        Takeoff position on the launchpad grid, shape (3,).
    color : np.ndarray
        Current LED color as RGB float values in [0, 1], shape (3,).
    """

    id: int
    home: np.ndarray = field(default_factory=lambda: np.zeros(3))
    color: np.ndarray = field(default_factory=lambda: np.ones(3))


@dataclass
class Launchpad:
    """Takeoff grid layout.

    Attributes
    ----------
    rows : int
        Number of rows in the grid.
    cols : int
        Number of columns in the grid.
    spacing : float
        Distance between adjacent drones in meters (uniform X/Y).
    origin : np.ndarray
        World-space origin of the grid's first slot, shape (3,).
    """

    rows: int = 10
    cols: int = 10
    spacing: float = 3.0
    origin: np.ndarray = field(default_factory=lambda: np.zeros(3))

    @property
    def capacity(self) -> int:
        """Maximum number of drones the grid can hold."""
        return self.rows * self.cols

    def slot_position(self, row: int, col: int) -> np.ndarray:
        """Return the world-space position for grid slot (*row*, *col*)."""
        return self.origin + np.array([col * self.spacing, row * self.spacing, 0.0])

    def all_slots(self) -> np.ndarray:
        """Return an (N, 3) array of all slot positions, row-major."""
        positions = []
        for r in range(self.rows):
            for c in range(self.cols):
                positions.append(self.slot_position(r, c))
        return np.array(positions)


@dataclass
class Formation:
    """A named set of target positions for the swarm at a point in time.

    Attributes
    ----------
    name : str
        Human-readable label for the formation.
    positions : np.ndarray
        Target positions for N drones, shape (N, 3).  The order of rows
        corresponds to drone assignment (which drone goes to which slot),
        resolved by the assignment algorithm — not by identity.
    colors : Optional[np.ndarray]
        Per-drone LED colors, shape (N, 3) or None if unspecified.
    duration : float
        Time in seconds the swarm should hold this formation before
        transitioning to the next.
    """

    name: str = ""
    positions: np.ndarray = field(default_factory=lambda: np.empty((0, 3)))
    colors: Optional[np.ndarray] = None
    duration: float = 0.0

    @property
    def drone_count(self) -> int:
        """Number of drones referenced by this formation."""
        return self.positions.shape[0] if self.positions.ndim == 2 else 0


@dataclass
class Show:
    """Top-level container for a complete drone show.

    A Show holds the launchpad definition, an ordered list of formations,
    the swarm of drones, and the geofence.  It is the primary object
    passed between the UI layer and the core algorithms.

    Attributes
    ----------
    name : str
        Show title.
    launchpad : Launchpad
        Takeoff grid definition.
    drones : list[Drone]
        The swarm, indexed by ``Drone.id``.
    formations : list[Formation]
        Ordered sequence of formations the swarm transitions through.
    geofence : Geofence
        Safety bounding volume.
    fps : float
        Timeline frame rate used for time<->frame conversion.
    """

    name: str = "Untitled Show"
    launchpad: Launchpad = field(default_factory=Launchpad)
    drones: list[Drone] = field(default_factory=list)
    formations: list[Formation] = field(default_factory=list)
    geofence: Geofence = field(default_factory=Geofence)
    fps: float = 30.0

    @property
    def drone_count(self) -> int:
        """Number of drones in the swarm."""
        return len(self.drones)

    @property
    def duration(self) -> float:
        """Total show duration in seconds (sum of formation durations)."""
        return sum(f.duration for f in self.formations)
