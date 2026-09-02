"""Unit tests for the bpy-free domain model in ``core/model.py``.

These tests run without Blender installed — they exercise only the
pure-Python dataclasses and their methods.
"""

import numpy as np
import pytest

from core.model import Drone, Formation, Geofence, Launchpad, Show


class TestGeofence:
    def test_default_values(self):
        gf = Geofence()
        assert gf.max_altitude == 150.0
        assert gf.min_pos.shape == (3,)
        assert gf.max_pos.shape == (3,)

    def test_contains_inside(self):
        gf = Geofence(
            min_pos=np.array([0.0, 0.0, 0.0]),
            max_pos=np.array([100.0, 100.0, 80.0]),
            max_altitude=80.0,
        )
        assert gf.contains(np.array([50.0, 50.0, 40.0]))

    def test_contains_outside(self):
        gf = Geofence(
            min_pos=np.array([0.0, 0.0, 0.0]),
            max_pos=np.array([100.0, 100.0, 80.0]),
            max_altitude=80.0,
        )
        assert not gf.contains(np.array([150.0, 50.0, 40.0]))
        assert not gf.contains(np.array([50.0, 50.0, 90.0]))

    def test_contains_boundary(self):
        gf = Geofence(
            min_pos=np.array([0.0, 0.0, 0.0]),
            max_pos=np.array([100.0, 100.0, 80.0]),
            max_altitude=80.0,
        )
        assert gf.contains(np.array([0.0, 0.0, 0.0]))
        assert gf.contains(np.array([100.0, 100.0, 80.0]))

    def test_contains_batch(self):
        gf = Geofence(
            min_pos=np.array([0.0, 0.0, 0.0]),
            max_pos=np.array([100.0, 100.0, 80.0]),
            max_altitude=80.0,
        )
        points = np.array([
            [50.0, 50.0, 40.0],
            [150.0, 50.0, 40.0],
            [50.0, 50.0, 90.0],
        ])
        result = gf.contains(points)
        assert result is True  # all must be inside


class TestDrone:
    def test_defaults(self):
        d = Drone(id=0)
        assert d.id == 0
        assert d.home.shape == (3,)
        assert d.color.shape == (3,)
        assert np.all(d.color == 1.0)

    def test_custom_values(self):
        d = Drone(
            id=42,
            home=np.array([10.0, 20.0, 0.0]),
            color=np.array([1.0, 0.0, 0.0]),
        )
        assert d.id == 42
        assert d.home[0] == 10.0
        assert d.color[0] == 1.0
        assert d.color[1] == 0.0


class TestLaunchpad:
    def test_capacity(self):
        lp = Launchpad(rows=5, cols=4)
        assert lp.capacity == 20

    def test_slot_position(self):
        lp = Launchpad(rows=3, cols=3, spacing=2.0, origin=np.array([10.0, 10.0, 0.0]))
        pos = lp.slot_position(1, 2)
        assert pos[0] == 14.0  # 10 + 2*2
        assert pos[1] == 12.0  # 10 + 1*2
        assert pos[2] == 0.0

    def test_all_slots_count(self):
        lp = Launchpad(rows=4, cols=6)
        slots = lp.all_slots()
        assert slots.shape == (24, 3)

    def test_all_slots_row_major(self):
        lp = Launchpad(rows=2, cols=2, spacing=1.0)
        slots = lp.all_slots()
        # Row 0: (0,0) and (1,0) in grid coords
        assert np.allclose(slots[0], [0.0, 0.0, 0.0])
        assert np.allclose(slots[1], [1.0, 0.0, 0.0])
        # Row 1: (0,1) and (1,1)
        assert np.allclose(slots[2], [0.0, 1.0, 0.0])
        assert np.allclose(slots[3], [1.0, 1.0, 0.0])


class TestFormation:
    def test_empty_formation(self):
        f = Formation(name="Empty")
        assert f.name == "Empty"
        assert f.drone_count == 0

    def test_drone_count(self):
        f = Formation(
            name="Square",
            positions=np.array([[0, 0, 0], [10, 0, 0], [10, 10, 0], [0, 10, 0]],
                                dtype=float),
        )
        assert f.drone_count == 4

    def test_default_duration(self):
        f = Formation()
        assert f.duration == 0.0


class TestShow:
    def test_empty_show(self):
        s = Show()
        assert s.drone_count == 0
        assert s.duration == 0.0
        assert len(s.formations) == 0

    def test_duration_sum(self):
        s = Show(
            formations=[
                Formation(duration=5.0),
                Formation(duration=10.0),
                Formation(duration=3.0),
            ],
        )
        assert s.duration == 18.0

    def test_drone_count_from_swarm(self):
        s = Show(drones=[Drone(id=i) for i in range(12)])
        assert s.drone_count == 12
