"""Pytest configuration and shared fixtures for Sirius.

This conftest makes the test suite runnable in two modes:

1. **Headless (no Blender)** — the default.  Tests import from
   ``core/`` and ``algorithms/`` directly.  No ``bpy`` is needed
   because the domain model is pure Python.

2. **With Blender** — when running inside ``blender --background
   --python -m pytest`` (or via ``pytest-blender``), ``bpy`` is
   available and integration tests can exercise the adapter layer.

The ``need_bpy`` marker below is used to skip Blender-dependent tests
when running headlessly.
"""

import pytest


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers",
        "need_bpy: mark a test as requiring Blender's bpy module. "
        "Skipped automatically when bpy is not importable.",
    )


def _bpy_available() -> bool:
    try:
        import bpy  # noqa: F401
        return True
    except ImportError:
        return False


BPY_AVAILABLE = _bpy_available()


def pytest_collection_modifyitems(config, items):
    """Skip tests marked ``need_bpy`` when bpy is not importable."""
    if BPY_AVAILABLE:
        return
    skip_bpy = pytest.mark.skip(reason="bpy not available (headless mode)")
    for item in items:
        if "need_bpy" in item.keywords:
            item.add_marker(skip_bpy)


# --- Shared fixtures -------------------------------------------------

@pytest.fixture
def simple_geofence():
    """A standard 500 m × 500 m × 150 m geofence centered on the origin."""
    from core.model import Geofence
    import numpy as np
    return Geofence(
        min_pos=np.array([-250.0, -250.0, 0.0]),
        max_pos=np.array([250.0, 250.0, 150.0]),
        max_altitude=150.0,
    )


@pytest.fixture
def small_launchpad():
    """A 3×2 launchpad with 3 m spacing at the origin."""
    from core.model import Launchpad
    return Launchpad(rows=3, cols=2, spacing=3.0)


@pytest.fixture
def sample_drones(small_launchpad):
    """Six drones positioned on the small launchpad grid."""
    from core.model import Drone
    import numpy as np
    drones = []
    slot_idx = 0
    for r in range(small_launchpad.rows):
        for c in range(small_launchpad.cols):
            drones.append(Drone(
                id=slot_idx,
                home=small_launchpad.slot_position(r, c),
            ))
            slot_idx += 1
    return drones


@pytest.fixture
def sample_show(small_launchpad, sample_drones, simple_geofence):
    """A minimal show with one formation holding all drones at their home slots."""
    from core.model import Show, Formation
    import numpy as np
    positions = np.array([d.home for d in sample_drones])
    formation = Formation(
        name="Home",
        positions=positions,
        duration=5.0,
    )
    return Show(
        name="Test Show",
        launchpad=small_launchpad,
        drones=sample_drones,
        formations=[formation],
        geofence=simple_geofence,
    )
