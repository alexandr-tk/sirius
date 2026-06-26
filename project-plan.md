# Sirius — Architectural Project Plan

> Open-source Blender add-on for designing professional drone light-show animations and exporting
> them to real-world drone-control formats. Target: **Blender 5.x** (latest alpha, manual at 5.1).
> License: MIT. Status of this document: **developer-ready architectural roadmap** (planning only).

---

## 0. Methodology Note (how this plan was produced)

Per the project-roadmap-architect protocol, the end-to-end user-workflow section (§6) and the test
strategy (§7) are normally delegated to dedicated sub-agents (`@usecase-architect`,
`@test-suite-architect`). In this environment those agents are not available as discrete tools, so
this document **integrates those sections directly**, produced by the architect role and grounded
entirely in the verified facts of the project brief (domain model, export specs, Blender 5.x API
constraints) plus the authoritative sources cited inline. Every non-obvious API recommendation was
checked against the current Blender manual / API docs (no deprecated APIs are proposed). If the user
later runs a change through a real `@usecase-architect` / `@test-suite-architect` pass, only §6 and
§7 are expected to be amended; the architecture and phases (§2–§5) are stable.

**Verification performed for this plan:**
- Read every file in the current repo (confirms the blocking `ImportError`, `bpy.ops`-in-loop,
  one-material-per-drone, and the two `pass` stubs).
- Confirmed the **VVIZ** spec against `https://docs.verge.aero/drone-show-software/verge-design-studio/vviz-format`.
- Confirmed Blender 5.1 manual pages for **Point Cloud** (`/modeling/point_cloud/`), **Geometry
  Nodes** features (Node-Based Tools, Gizmos, Baking, Import nodes CSV/OBJ/PLY/STL/TXT/VDB), the
  **Extensions** getting-started page, and editors (Dope Sheet / Graph Editor / NLA / VSE).

---

## 1. Executive Summary & Architecture Overview

### 1.1 Vision & success bar
Sirius must let anyone author drone-show animations of arbitrary complexity inside Blender and
export them to the data formats consumed by real drone-control stacks. The credibility bar is "an
open alternative to Verge Aero Design Studio / SPH Engineering Drone Show Creator / Vimdrones
Designer." Concrete success criteria:

- Generate formations of **N drones** (scale target **~1000**) from arbitrary Blender 3D objects.
- Animate per-drone **position** and **LED color** (RGB/RGBW) over time, synced to the timeline.
- Compute **safe transitions** between formations (optimal assignment + time-parameterized motion +
  collision/feasibility validation).
- **Export** to CSV, Vimdrones raw, UgCS PATH/PATH3, VVIZ, and Depence with correct
  coordinate/unit/sample-rate conversion.
- Ship as a modern **Blender Extension** (`blender_manifest.toml`), MIT, documented, tested.

### 1.2 Current state assessment (Phase 0 input)
The repository is a ~309-line **throwaway alpha prototype**, conceptually useful but **not an
architectural foundation**:

| Problem | Evidence | Impact |
|---|---|---|
| **Blocking import bug** | `materials/__init__.py` imports `configure_lighting_copositing` (typo, missing `m`); the defined function is `configure_lighting_compositing` | Add-on fails to **enable** as-is |
| **Doesn't scale** | `operators/create_takeoff_grid.py` calls `bpy.ops.mesh.primitive_uv_sphere_add(...)` in a nested loop, one mesh object **and** one material per drone | O(N) ops calls + O(N) materials → unusable past ~100 drones, context-fragile |
| **No domain model** | `props.py` only has grid dimensions + color; no Formation/Drone/Show/Transition concepts | Cannot represent a real show |
| **No animation system** | No keyframes, no timeline integration, color only as a static material tweak | Cannot author motion or synced LEDs |
| **No transitions / collision / feasibility** | `utils/pathfinding.py` is a `pass` stub | Core value missing |
| **No real export** | `operators/export_csv.py` is a `pass` stub, not even registered | Core value missing |
| **Weak naming / structure** | `bpy.types.Scene.my_props`; flat operator/panel/prop split | Hard to extend |

**Decision:** treat the prototype as a *reference for intent* (modular props/operators/panels split,
LED emission + Fog-Glare compositing) and **rebuild on a clean layered architecture**. Phase 0
hardens + restructures rather than bolting features onto the grid operator. Per-module rebuild vs.
refactor is specified in the phase tables.

### 1.3 Layered architecture

```
                              ┌─────────────────────────────────────────────┐
   Blender UI layer           │  panels/  operators/  gizmos/  draw handlers │  bpy.types.Panel/Operator,
   (thin, bpy-only)           │  (N-panel "Sirius", UILists, gpu overlays)    │  GizmoGroup, SpaceView3D.draw_handler_add
                              └───────────────────────┬─────────────────────┘
                                                      │ reads/writes via adapter
                              ┌───────────────────────▼─────────────────────┐
   bpy integration adapter    │  blender/  (scene_state, swarm_object,       │  bpy, mathutils, gpu, bmesh,
   (bpy-facing glue)          │  material_factory, node_groups, handlers)    │  depsgraph evaluation
                              └───────────────────────┬─────────────────────┘
                                                      │ pure data in/out
              ┌───────────────┬───────────────────────┼───────────────────────┬──────────────────┐
              ▼               ▼                       ▼                       ▼                  ▼
      ┌──────────────┐ ┌──────────────┐      ┌────────────────┐      ┌────────────────┐  ┌────────────────┐
   core/         │ algorithms/   │        exporters/        │      importers/          │  georef/        │
   data model    │ assignment,   │        unified trajectory│      round-trip          │  coord frames,  │
   (dataclasses) │ collision,    │        model + writers  │      (CSV/VVIZ in)       │  lat/lon, units │
   NO bpy        │ interpolation │        NO bpy            │      NO bpy              │  NO bpy         │
      └──────────────┘ └──────────────┘      └────────────────┘      └────────────────┘  └────────────────┘
                          ▲ pure-Python, fully unit-testable WITHOUT Blender ▲
```

**Golden rule:** every algorithm (assignment, collision, interpolation, coordinate conversion,
format encoders/decoders) lives in **bpy-free** modules so it is unit-testable headlessly. The
`blender/` adapter is the only layer that imports `bpy`, and it does so exclusively to translate
between the pure data model and Blender's scene graph. This is what makes the heavy logic testable
and keeps Blender version churn isolated to one layer.

### 1.4 Primary drone representation (DECISION)

**Authoritative source of truth = a bpy-free `Show` data model.** The Blender scene holds a **single
"Swarm" object** (Point Cloud when N is large; an Instanced mesh for visual fidelity) whose
per-point attributes are *derived* from the Show model at evaluation time.

| Need | Representation | Why |
|---|---|---|
| Scale to ~1000 drones | **Point Cloud object** + per-point custom attributes (`drone_id`, `color` RGBW, `target_slot`, `home_pos`, `flags`) | First-class Blender object type, far lighter than thousands of meshes+materials; attributes are Geometry-Nodes-readable and exportable. Manual: `/modeling/point_cloud/` |
| Nice viewport LED look | **Instance on Points** (small emission proxy) over the swarm | Thousands of cheap instances render the "LED bloom" look; one shared material, not one-per-drone |
| Per-drone authored paths | **Curves** (one poly/Bezier spline per drone), editable in the viewport, *opt-in* for hand-tweaks | Curves are lightweight & natively editable; a separate time map (Show model) resolves the spatial-curve-vs-time problem |
| Drone identity across the show | **Stable point index / `drone_id`** (never reordered by us; assignment only changes *slot*, not identity) | Required by UgCS (begin-scene order must match end-scene order) and by stable export |

> Point Cloud vs. instances: Point Cloud is the *data backbone* (scale + attributes + export source);
> instances are the *visual skin*. We never depend on instance count for correctness — export reads
> the evaluated swarm attributes, not rendered pixels.

### 1.5 Recommended target package layout

```
sirius/
├─ blender_manifest.toml          # modern Extension packaging (§2.1)
├─ __init__.py                    # register/unregister (loads manifest meta too)
├─ core/                          # bpy-FREE: data model + pure logic (unit-tested)
│  ├─ __init__.py
│  ├─ model.py                    # Show, Launchpad, Formation, FormationGroup,
│  │                              #   FormationSequence, Drone, Transition, Payload, Geofence
│  ├─ ids.py                      # stable drone id allocation
│  └─ units.py                    # meters, time<->frame, sample-rate math
├─ algorithms/                    # bpy-FREE
│  ├─ __init__.py
│  ├─ assignment.py               # Hungarian (scipy if present else pure-python)
│  ├─ interpolation.py            # trapezoidal velocity-profile time parameterization
│  ├─ collision.py                # min-spacing (KDTree iface), geofence (BVH iface)
│  ├─ feasibility.py              # vmax/amax/jerk/altitude/density validators
│  └─ flocking.py                 # boids (accelerator phase)
├─ exporters/                     # bpy-FREE writers
│  ├─ __init__.py
│  ├─ trajectory.py               # unified internal TrajectorySample model + sampler
│  ├─ coord.py                    # Blender Z-up <-> ogl/ENU/NED, lat/lon anchoring
│  ├─ csv_writer.py
│  ├─ vimdrones_writer.py
│  ├─ ugcs_writer.py
│  ├─ vviz_writer.py
│  └─ depence_writer.py
├─ importers/                     # bpy-FREE parsers (round-trip, accelerator phase)
│  ├─ csv_reader.py
│  └─ vviz_reader.py
├─ blender/                       # ONLY layer that imports bpy
│  ├─ __init__.py
│  ├─ registry.py                 # central class register/unregister
│  ├─ scene_state.py              # Scene <-> Show serialization (read/write into .blend)
│  ├─ swarm_object.py             # Point Cloud + attributes create/update
│  ├─ node_groups.py              # reusable GeoNodes group factory (distribute/instance)
│  ├─ material_factory.py         # single shared LED emission material
│  ├─ compositing.py              # Filmic + Fog Glare (carried from prototype, fixed)
│  ├─ handlers.py                 # depsgraph_update_post / frame_change_post / msgbus
│  ├─ draw.py                     # gpu overlays (violations, geofence, ids, ribbons)
│  └─ gizmos.py                   # spacing/density interactive handles
├─ operators/                     # thin bpy operators (call core/algorithms/exporters)
│  ├─ launchpad.py  formations.py  led.py  transitions.py  validate.py  export.py  ...
├─ panels/                        # N-panel "Sirius" + UILists
├─ props/                         # PropertyGroups (renamed from my_props)
├─ tests/                         # pytest + headless bpy harness
└─ assets/                        # node group .blends, presets, logo
```

---

## 2. Verified Blender 5.x API Decisions (non-deprecated building blocks)

Every subsystem below uses **current** APIs only. The single most important deprecation to avoid:
**`bgl` was removed in Blender 4.0+.** All viewport drawing uses the `gpu` module.

### 2.1 Packaging — modern Extensions system
Ship `blender_manifest.toml` (the modern install path; legacy `bl_info` is kept for backward
compatibility but is secondary). Schema per manual
`/advanced/extensions/getting_started.html`:

```toml
schema_version = "1.0.0"
id = "sirius"
version = "0.1.0"
name = "Sirius"
tagline = "Design drone light-show animations and export to flight-ready formats"
maintainer = "Alexandr Tkachyov"
type = "add-on"
blender_version_min = "5.0.0"
tags = ["3D View", "Animation", "Import-Export"]
license = ["SPDX:MIT"]
permissions = { files = "Export show data (CSV/VVIZ/UgCS/Vimdrones) to disk" }
```
`permissions.files` is required because we write export files. (We do not need `camera`,
`microphone`, or `network`.)

### 2.2 Viewport drawing — `gpu` module (NOT `bgl`)
Manual/API: `https://docs.blender.org/api/latest/gpu.html`,
`gpu_extras.batch.for_shader`, `bpy.types.SpaceView3D.draw_handler_add`.

```python
# Illustrative (NOT production code) — correct, non-deprecated pattern
import gpu
from gpu_extras.batch import batch_for_shader

def _draw_violations(self, context):
    shader = gpu.shader.from_builtin('UNIFORM_COLOR')        # or 'SMOOTH_COLOR'
    shader.uniform_float("color", (1.0, 0.0, 0.0, 1.0))
    batch = batch_for_shader(shader, 'POINTS', {"pos": self._violating_positions})
    shader.bind(); batch.draw(shader)

# registration:
SpaceView3D = bpy.types.SpaceView3D
handle = SpaceView3D.draw_handler_add(_draw_violations, (self, None), 'WINDOW', 'POST_VIEW')
# ... SpaceView3D.draw_handler_remove(handle, 'WINDOW') on unregister
```
Use `'POLYLINE_SMOOTH_COLOR'` for path ribbons, `'SMOOTH_COLOR'` for per-drone-colored points.
`POST_VIEW` = world space; `POST_PIXEL` = screen space (for drone-ID labels).

### 2.3 Formation generation — Geometry Nodes (idiomatic engine)
Manual: `/modeling/geometry_nodes/`. Reusable node groups driven by a GeoNodes modifier; evaluate
with the depsgraph. Key nodes: **Distribute Points on Faces** (scatter on meshes/curves/text),
**Resample Curve** (even spacing on splines), **String to Curves** (text/logos), **Instance on
Points** (LED proxies), **Store Named Attribute** (write `drone_id`/`color`).

Blender 5.x Geometry Nodes also gives us **Node-Based Tools**, **Gizmos** (linear/dial/transform),
**Baking**, and **Import nodes** (CSV/OBJ/PLY/STL/TXT/VDB) — leverage Import→CSV for reference
trajectories and Node Tools as interactive formation editors. A **"Scatter on Surface" modifier**
also exists as a built-in primitive.

```python
# Illustrative: read evaluated swarm positions
deps = context.evaluated_depsgraph_get()
eval_obj = swarm_obj.evaluated_get(deps)
# Point cloud: positions via attribute, or convert via to_mesh() for instance/mesh swarms
```

### 2.4 Swarm object — Point Cloud + custom attributes
Manual: `/modeling/point_cloud/`. A Point Cloud object holds N points and named attributes
(point domain), readable by GeoNodes and by exporters. This is lighter than thousands of mesh
objects and avoids the one-material-per-drone trap. (`bpy.data.pointclouds.new`, point attributes
via `pointcloud.attributes.new(name, type, 'POINT')`.)

### 2.5 Animation — reuse native system (do NOT reinvent)
Manual: `/editors/dope_sheet/`, `/editors/graph_editor/`, `/editors/nla/`. Author via
`obj.keyframe_insert(...)` / Action F-Curves; Dope Sheet & Graph Editor for editing; NLA for
composing formation "clips" as strips (maps naturally to the professional Composer timeline:
Launch → elements → Return as NLA strips). Per-drone LED color via animated custom properties or a
GeoNodes color field sampled over time.

> Do **not** build a custom animation editor. Use the Dope Sheet/Graph Editor/NLA. We only add a
> thin "Composer-like" panel that creates/aligns NLA strips.

### 2.6 Real-time evaluation — depsgraph + handlers + msgbus
Always read **evaluated** data inside handlers (never live `bpy.data`). Use
`bpy.app.handlers.depsgraph_update_post` / `frame_change_post` for live feasibility recalculation
and LED refresh, and `bpy.msgbus.subscribe_rna` for cheap property-change reactions.

```python
# Illustrative: subscribe to a property change
bpy.msgbus.subscribe_rna(
    key=(context.scene.sirius_props, "drone_count"),
    owner=owner, args=(context,), notify=_on_count_changed,
)
bpy.msgbus.publish_rna  # available where needed
```

### 2.7 Collision / spatial math — `mathutils`
- `mathutils.kdtree` — nearest-neighbour → minimum-spacing checks, O(n log n).
  API: `https://docs.blender.org/api/latest/mathutils.kdtree.html`
- `mathutils.bvhtree` — mesh/volume proximity → geofence & obstacle collision.
  API: `https://docs.blender.org/api/latest/mathutils.bvhtree.html`
- `mathutils.Vector`/`Matrix`/quaternions, `bmesh` for mesh queries.

> The **algorithms** layer wraps these behind a bpy-free interface (e.g. a pure-Python `KDTree`
> shim, or dependency-injected spatial index) so unit tests can run without Blender.

### 2.8 Assignment problem — Hungarian algorithm
Use `scipy.optimize.linear_sum_assignment` when scipy is available; otherwise a vendored
pure-Python Hungarian implementation. **Decision needed (§8):** vendor scipy, lazy-load it, or ship
the pure-Python fallback only.

### 2.9 Performance — avoid `bpy.ops` in hot loops
Use the data API; batch creation; cache heavy computations; for long generation/validation jobs use
a modal operator + `context.window_manager.event_timer` and report progress via
`context.window_manager.progress_begin/update/end`. This is the direct fix for the prototype's
`bpy.ops`-in-a-loop bottleneck.

### 2.10 UI — N-panel + UILists + gizmos
Sidebar (`bl_space_type='VIEW_3D'`, `bl_region_type='UI'`, `bl_category='Sirius'`),
`bpy.types.UIList` for formation/drone lists, `bpy.props` PropertyGroups, popovers, and
`bpy.types.GizmoGroup` handles for interactive spacing/density editing.

---

## 3. Domain Data Model → Blender Mapping

Mirrors the professional pipeline (Verge/SPH/Vimdrones). Each concept maps to a Blender-native home.

| Domain object | Core dataclass (`core/model.py`, bpy-free) | Blender home |
|---|---|---|
| **Show** | root: formations[], sequences[], launchpad, geofence, global_ref_frame, time range, fps | `Scene.sirius_show` (serialized PropertyGroup) |
| **Launchpad** | drone_count, pool of takeoff *shapes* (Grid/Circle/Rectangle/Polygon/Arbitrary), spacing, overflow shape, launch sequence/stagger, agent_def | Swarm object home positions + a GeoNodes "launchpad" group |
| **Formation** | anchor point; source object ref; allocation (Flexible%/Fixed count); min/max slots; exclude_from_lighting; per-slot target positions | A Blender object (mesh/curve/text) + a "Formation" PropertyGroup entry; target slots computed via GeoNodes |
| **FormationGroup** | collection of elements sharing one anchor; per-element allocation weights | Blender Collection + group PropertyGroup |
| **FormationSequence** | subset transition between elements; allocation mode; overflow; apply-color-source-before | NLA strip / a "Sequence" PropertyGroup driving a Transition |
| **Drone** | stable `id`, home pos, current slot assignment per formation, per-time color keyframes | Point index + `drone_id` attribute + color attribute |
| **Transition** | from→to formations, assignment map (id→slot), duration, velocity profile, stagger | Computed path samples; optionally per-drone Curve |
| **Payload** | Light {lumens, colorType RGB/RGBW, sourceType dome/spotlight} or Pyro {eventTime, vdl, pan, tilt} | Per-drone attribute / payload PropertyGroup |
| **Geofence** | box/polygon bounds, altitude ceil/floor, density limit, vmax/amax/jerk | Helper object(s) + Geofence PropertyGroup; drawn via `gpu` |

**Identity invariant (critical for UgCS):** a drone's `id`/point-index is **stable for the entire
show**. Transitions reassign *slots*, never identities. The begin-scene drone order must equal the
end-scene order (UgCS PATH requirement).

---

## 4. Phased Implementation Roadmap

Notation: **[R]** = rebuild from scratch, **[F]** = fix/port from prototype, **[N]** = new.
Dependencies are cumulative (each phase depends on all earlier ones unless noted).

> **MVP boundary:** **Phases 0–5 are the MVP** — the minimum slice that produces a drone-show
> animation end-to-end (create → animate → transition → validate → export to a real control format).
> **Phases 6–7 are post-MVP.** See §9 for the governing rule.

### Phase 0 — Stabilize, Restructure, Scalable Foundation
**Objective:** make the add-on enable cleanly, introduce the layered architecture + bpy-free core,
and replace the non-scalable swarm/material approach.

- **[F]** Fix blocking `ImportError`: rename import to `configure_lighting_compositing` (correct spelling) in `materials/__init__.py`.
- **[N]** `blender_manifest.toml` (§2.1) + keep minimal `bl_info`.
- **[N]** New package layout (§1.5); central `blender/registry.py` for register/unregister.
- **[N]** Rename `Scene.my_props` → `Scene.sirius_props`; move props into `props/`.
- **[N]** `core/model.py` — dataclass skeletons (Show/Launchpad/Formation/Drone/Geofence).
- **[N]** `blender/swarm_object.py` — create single Point-Cloud/Mesh swarm + per-point attributes; **[R]** `CreateTakeoffGrid` to populate the swarm via the **data API** (no `bpy.ops` in loops).
- **[N]** `blender/material_factory.py` — **one** shared LED emission material (kills the one-material-per-drone trap); **[F]** port `create_drone_emission_material` to the shared factory.
- **[F]** `blender/compositing.py` — port Filmic + Fog-Glare setup (now spelled correctly).
- **[N]** `tests/` harness: pytest + headless Blender runner; `conftest` bootstraps `bpy` via `blender --background --python` (or `pytest-blender`).
- **[N]** Pure-Python unit tests for `core/model.py` (no bpy).

**DoD:** add-on installs via drag-drop Extension install AND via legacy `bl_info`; enabling produces
no errors; a 10×10 swarm is created as a single object with one shared material; `pytest -q` passes
on the core tests; perf of grid creation is sub-linear in N (no `bpy.ops` in loop).
**Risk:** Point Cloud API editability limits → mitigation: keep swarm object swappable (Point Cloud
vs. instanced mesh) behind `swarm_object.py`.
**Test milestone:** T0 (registry round-trip, swarm creation, no-deprecated-API linter gate).

### Phase 1 — Launchpad & Formation Generation
**Objective:** generate takeoff grids and arbitrary formations at controllable density/spacing.

- **[N]** Launchpad generator: takeoff shapes Grid/Circle/Rectangle/Polygon/Arbitrary; spacing enforcement + overflow shape; drone count auto-cap; staggered launch.
- **[N]** `blender/node_groups.py` — reusable GeoNodes groups: **Distribute Points on Faces** (mesh scatter), **Resample Curve** (spline formations), **String to Curves** (text/logos/QR), density + spacing controls exposed on the modifier.
- **[N]** Formation→slot sampling: read evaluated target positions via depsgraph; produce a slot list per formation.
- **[N]** `algorithms/assignment.py` — Hungarian assignment of drones→slots (min total travel): **lazy-load `scipy.optimize.linear_sum_assignment`**, fall back to a bundled pure-Python Hungarian if scipy is absent (correctness identical, both unit-tested vs. brute force).
- **[N]** Formation PropertyGroup + UIList; operators to create a formation from the active object.

**DoD:** user can turn any mesh/curve/text object into a formation with a density slider and a
spacing constraint; drones auto-assign to nearest slots; overflow drones go to the overflow shape.
**Risk:** GeoNodes API drift across 5.x alphas → pin tested node-tree templates in `assets/`.
**Test milestone:** T1 (formation sampling, Hungarian correctness vs. brute force on small N).

### Phase 2 — Animation & LED
**Objective:** author per-drone position + color over the timeline, synced to scene fps.

- **[N]** Timeline integration: map Show time ↔ scene frames (`core/units.py`); define show frame range.
- **[N]** Per-drone LED color keyframes (RGB/RGBW) over time; apply to selection/group/all (port `ChangeLEDColor` intent to the shared material + color attribute).
- **[N]** `blender/handlers.py` — `frame_change_post`/msgbus live LED refresh from the Show model.
- **[F]** Compositing bloom extended (per-formation color, intensity).
- **[N]** Composer panel: thin NLA-strip helper (Launch → elements → Return) — no custom anim editor.

**DoD:** scrubbing the timeline animates drone positions and LED colors; color keyframes appear in
the Dope Sheet; the shared emission material reflects per-drone colors.
**Risk:** per-point color animation throughput at N=1000 → mitigation: drive color via a single
GeoNodes color field sampled by time, not per-point F-Curves.
**Test milestone:** T2 (time↔frame math, color keyframe serialization).

### Phase 3 — Transitions & Assignment
**Objective:** compute safe formation→formation transitions (the core "who goes where, how").

- **[N]** `algorithms/interpolation.py` — time-parameterized motion (trapezoidal velocity profile honoring vmax/amax/jerk) per drone; staggered start.
- **[N]** Transition operator: given two formations, run Hungarian to map id→slot, then interpolate; output path samples (and optionally a per-drone Curve for editing).
- **[N]** FormationGroup/FormationSequence partial-subset transitions (Flexible%/Fixed allocation).

**DoD:** selecting two formations and "Create Transition" produces smooth, staggered, non-crossing
motion that respects vmax/amax; per-drone paths are editable as curves.
**Risk:** identity preservation across transitions → enforced by id invariant (slots only).
**Test milestone:** T3 (assignment identity stability, velocity-profile feasibility vs. limits).

### Phase 4 — Collision & Feasibility Validation
**Objective:** continuously validate safety and surface violations.

- **[N]** `algorithms/collision.py` + `algorithms/feasibility.py`: min-spacing (KDTree), vmax/amax/jerk, geofence volume (BVH), altitude ceil/floor, density limits.
- **[N]** `blender/draw.py` — `gpu` overlays: highlight violating drones/segments, draw geofence box, spacing heat-map, drone IDs.
- **[N]** Feasibility report (counts, worst offenders) + "block unsafe export" toggle.
- **[N]** Live recalculation via `depsgraph_update_post` (debounced) reading evaluated data.

**DoD:** any spacing/speed/geofence violation is highlighted live in the viewport and listed in the
report; export refuses (or warns) when violations exist.
**Risk:** KDTree/BVH rebuild cost per frame at N=1000 → cache + incremental updates + debounce.
**Test milestone:** T4 (deterministic violation detection on synthetic scenes).

### Phase 5 — Export Engine
**Objective:** export to all five formats with correct conversion. (Full spec in §5.)

- **[N]** `exporters/trajectory.py` — unified `TrajectorySample` model + sampler at a configurable **export sample rate** (decoupled from viewport fps).
- **[N]** `exporters/coord.py` — Blender Z-up ↔ `ogl`/ENU/NED, lat/lon anchoring around the global reference frame, unit (meters), Vimdrones "Z Axis Rotate".
- **[N]** Writers: `csv_writer.py`, `vimdrones_writer.py`, `ugcs_writer.py` (**both PATH and PATH3**, both first-class — not flagged/experimental), `vviz_writer.py`, `depence_writer.py`.
- **[N]** Export UI: format selector, sample-rate, coordinate-frame/global-ref inputs, validation gate.
- **[N]** Manifest `permissions.files` (already declared in Phase 0).
- **[N]** Minimal **show-origin anchor** (lat/lon/alt) consumed by `coord.py` for VVIZ/Depence `globalReferenceFrame` and UgCS georeferencing (full geo-ref UI is Phase 6).

**DoD:** a known show exports to all five formats (PATH + PATH3 both valid); outputs validated
against **golden reference files** (incl. VVIZ delta-reconstruction round-trip and UgCS ≤4 fps /
order / 12 000-frame constraints).
**Risk:** format spec ambiguity (UgCS PATH3 "Beta", Depence least-documented) → pin each writer to
its documented constraints and treat the golden-file diff as that format's fidelity gate.
**Test milestone:** T5 (golden-file diff per format; delta reconstruction; rate-cap enforcement).

### Phase 6 — Accelerators (high-value, **post-MVP**)
> Per the §9 MVP rule, everything here is a committed feature but is **not required to produce an
> animation end-to-end**, so it is sequenced after the MVP (Phases 0–5).

- **Geo-ref tooling:** full UI for the **ENU tangent-plane** origin anchor (map/click-to-set origin,
  CRS presets, real-world units); audience/readability helpers. (The minimal anchor ships in Phase 5.)
- **Pyro payloads (model + full authoring UI):** event-time triggers, VDL descriptors, pan/tilt;
  emitted by the VVIZ and Depence writers. *(MVP Light-only payloads first; pyro authoring lands here.)*
- **QR/text/logo generators:** dedicated builders (reuse String-to-Curves + scatter).
- **Music/beat sync:** full VSE audio-lane cues + `eventTags` (song/effect/pyro start markers); optional beat-detection later.
- **Flocking controller** (boids) in `algorithms/flocking.py`.
- **Import round-trip:** `importers/` (CSV/VVIZ → Show model → Blender) for editing existing shows.
- Reusable show-effect **assets/presets**; batch multi-show export.
- Previsualization LED materials/bloom extensions.

**DoD per item:** feature works end-to-end with at least one golden test.
**Test milestone:** T6 (round-trip parity: export then import yields equivalent Show; pyro payload round-trip through VVIZ/Depence).

### Phase 7 — Polish & Release
- Documentation (user guide + developer/architecture docs), README rewrite, examples.
- Performance pass: 1000-drone benchmark gate (generation, validation, export under target times).
- Graceful degradation (Progressive/Reduced modes), error handling, logging.
- Extension-platform packaging (tagged release, screenshots), v1.0.

**DoD:** installable Extension; passes full test matrix on Blender 5.1; 1000-drone show authored,
validated, and exported; documented.

---

## 5. Export Architecture

### 5.1 Unified internal trajectory model (bpy-free)
A single sampler reduces the Show to a list, per drone, of `TrajectorySample`s:

```
TrajectorySample: t (s), frame, x, y, z (m, Blender space), heading (deg),
                  r, g, b (0-255), optional w (0-255), optional pyro events[]
```

The **export sample rate** is independent of the viewport fps (resamples the authored motion), so we
can satisfy per-format constraints (e.g. UgCS ≤4 fps, Vimdrones fps = scene fps). Identity order is
preserved (begin-scene order == end-scene order).

### 5.2 Coordinate / unit / rate conversion (`exporters/coord.py`)
- **Units:** Blender default = meters. Keep meters internally.
- **Frames:** Blender is Z-up right-handed. Targets:
  - **VVIZ `ogl`** = X right, Y up, Z forward. Map Blender `(x, y, z)` (z = up, y = forward) →
    ogl `(x, z, -y)` (right = x, up = z, forward = -y). Expose as a configurable axis-remap matrix.
  - **ENU / NED** (UgCS variants) via axis remap; **Vimdrones** + "Z Axis Rotate" offset.
- **Geo-anchoring:** VVIZ `globalReferenceFrame {lat,lon,alt}` is the real-world origin of local
  (0,0,0). Convert local **ENU** (East-North-Up) offsets to lat/lon via a **flat-earth tangent-plane
  approximation** around the anchor (the de-facto drone-show standard; accurate across a ~1 km show
  footprint; matches UgCS conventions too).
- **Sample rate:** decouple export fps from viewport fps; clamp per format.

### 5.3 Per-format writers (exact encoding rules from verified specs)

**A) Generic CSV** — common denominator. Columns `frame, drone_id, x, y, z, r, g, b` (variants with
`yaw`/heading). One file, sampled at export fps.

**B) Vimdrones raw** — **one file per drone**, named `<id>.txt` (e.g. `1.txt`). Each line:
`frame_number  x  y  z  r  g  b` (space-separated; r,g,b integers 0–255). fps = Blender scene fps
(override-able via export rate). Apply "Z Axis Rotate" if set.

**C) UgCS PATH / PATH3** (SPH / `ugcs/ddc`):
- **Frame-rate cap:** PATH ≤ **4 fps**; total ≤ **~12,000 frames (~8m20s)**. **PATH3** is the newer
  variant and is a **first-class writer** (not experimental); both honor the same identity rule.
- **Order invariant:** drone order in the **last** formation must match the **begin** scene →
  enforced by the stable-id invariant; the writer emits drones in begin-scene order.
- Axis/units follow UgCS conventions (configurable remap).

**D) VVIZ** (Verge Visualization — **visualization/interchange, NOT flight-ready**, per spec):
- Header: `version`, `performanceName`, `coordinateFrame:"ogl"`, `globalReferenceFrame{lat,lon,alt}`,
  `defaultPositionRate` (Hz, position step), `defaultColorRate` (Hz, color step),
  `timeOffsetSecs`.
- `eventTags[]`: `{time(sec), tagType(EffectStart|SongStart|PyroStart), tagID, color{r,g,b}}` for
  audio/video/pyro sync.
- `performances[]` each = `agentDescription` + `payloadDescription[]`:
  - `agentDescription`: `homeX/homeY/homeZ` + `homeH` (heading deg) start pose, `airframe` id,
    `agentTraversal[]` = **delta-compressed** steps `{dx,dy,dz,dh,dt}` — reconstruct absolute pose by
    accumulating deltas from `home` (dt in seconds; if absent, `dt = 1/defaultPositionRate`).
  - `payloadDescription[]`: `type:"Light"` `{lumens, colorType(RGB|RGBW), sourceType("dome"|"spotlight"),
    payloadActions[]}` where each action is `{r,g,b 0-255, optional frames}` = hold that color for
    `frames` steps at `defaultColorRate` (1 step if `frames` absent) **OR** `type:"Pyro"`
    `{eventTime(sec), vdl, pan, tilt}`.
- Writer must (1) convert to `ogl`, (2) delta-compress positions, (3) run-length-encode color into
  `payloadActions` with `frames` holds, (4) emit event tags from the timeline.

**E) Depence** (Syncronorm) — positions, rotations, LED colors, pyro payloads; previz target.

**Verification gate:** delta-reconstruction round-trip (home + Σ deltas == sampler output), and
color hold-length sum == show color-rate × duration.

### 5.4 Flight-ready vs. visualization split
- **Flight-ready (absolute per-frame poses):** CSV, Vimdrones raw, UgCS PATH/PATH3.
- **Visualization/interchange (delta-compressed / rich metadata):** VVIZ, Depence.
The unified sampler feeds both branches; writers pick the representation. Export is blocked by the
feasibility gate (Phase 4) unless the user explicitly overrides.

---

## 6. End-to-End User Workflows (use-case section)

Each workflow names the **entry actor**, **goal**, **steps in the UI**, the **Blender/API surface
touched**, and **acceptance criteria**. These double as integration-test narratives.

### UC-1 — First-show quickstart (onboarding)
- **Actor:** new user. **Goal:** launchpad → one formation → simple color → export CSV.
- **Steps:** open Sirius N-panel → set drone count + spacing → *Create Launchpad* (Phase 0/1) →
  add a Text object "HI" → *Create Formation from Active* with density slider (Phase 1) → set LED
  color + *Create Transition* (Phase 3) → set frame range → *Export → CSV* (Phase 5).
- **Acceptance:** CSV rows == `frame,drone_id,x,y,z,r,g,b`; drone count matches; positions in meters.

### UC-2 — Logo/text/QR formation show
- **Actor:** designer. **Goal:** turn a logo mesh / text / QR into a held formation.
- **Steps:** import logo (or *Add Text* / *Generate QR* in Phase 6) → *Create Formation* (GeoNodes
  Distribute/Resample/String-to-Curves) → tune density/spacing → assign → hold over a frame range.
- **Acceptance:** formation points lie on the source object's surface; spacing constraint honored.

### UC-3 — Music-synced multi-formation show with transitions
- **Actor:** show designer. **Goal:** a timed sequence of formations synced to audio.
- **Steps:** import audio into VSE (Phase 6) → place formations at beat times → *Create Transition*
  between each (Hungarian + trapezoidal profile) → set per-formation LED palettes (Phase 2) →
  NLA/Composer to align clips.
- **Acceptance:** transitions are non-crossing and within vmax/amax; colors change on beat frames.

### UC-4 — Feasibility-checked & exported to a vendor format
- **Actor:** pilot/operator. **Goal:** a flight-ready file the field can fly.
- **Steps:** *Validate* (Phase 4) → review violation report + viewport highlights → fix spacing/speed
  → choose format (Vimdrones/UgCS/VVIZ) → set sample rate + geo-ref → *Export*.
- **Acceptance:** zero violations at export; output passes the golden-file check; UgCS file ≤4 fps
  and order-invariant; VVIZ deltas reconstruct correctly.

### UC-5 — Round-trip edit of an existing show
- **Actor:** designer. **Goal:** import a previously exported show, tweak, re-export.
- **Steps:** *Import CSV/VVIZ* (Phase 6 importers) → reconstruct Show model + swarm → edit one
  drone's path/LED → *Export*.
- **Acceptance:** import-then-export yields a Show equivalent to the source (within tolerance).

### UC-6 — Large 1000-drone stadium show
- **Actor:** power user. **Goal:** author/validate/export at scale without freezing.
- **Steps:** 1000-drone launchpad (Point-Cloud backbone) → several dense formations → transitions →
  validate (debounced KDTree/BVH) → export VVIZ + CSV.
- **Acceptance:** viewport stays interactive; generation/validation/export complete within Phase 7
  benchmark targets; no `bpy.ops`-in-loop regressions.

### Edge cases to cover (in tests §7)
- Target formation needs **more** drones than exist → overflow shape (Launchpad).
- Target needs **fewer** drones → flexible/fixed allocation + min/max slots.
- Transition would violate vmax/amax → validator flags; writer blocks/overrides.
- UgCS show longer than ~8m20s or >12000 frames → block with message.
- RGBW payloads (white channel) preserved through CSV-extended / VVIZ.
- Geo-ref anchor missing → warn, default to local-only (no lat/lon).
- Depgraph-read during handler uses **evaluated** data (never live `bpy.data`).

---

## 7. Test Strategy (test-suite section)

### 7.1 Layers
1. **Pure-Python unit tests (no Blender)** — `core/`, `algorithms/`, `exporters/`, `importers/`,
   `georef/`. Fast, CI-friendly. This is where correctness of assignment, interpolation, collision,
   feasibility, coordinate conversion, and format encoders lives.
2. **Blender integration tests (headless)** — invoke `bpy` via
   `blender --background --python tests/run_blender_tests.py` (or `pytest-blender`). Covers swarm
   creation, GeoNodes formation sampling, handlers, draw registration, end-to-end operators.
3. **Golden-file tests** — one reference output per export format; diff current export against it.
4. **Performance gate** — benchmark N=1000 generation/validation/export against targets.

### 7.2 Tooling
- `pytest` + a `conftest.py` that provides a headless `bpy` fixture.
- A tiny "deprecated-API linter" gate (`rg` for `bgl`, `user_preferences`, `bpy.ops` inside loops)
  in CI to prevent regressions.

### 7.3 Test milestones (mapped to phases)
| ID | Phase | Coverage focus |
|---|---|---|
| T0 | 0 | registry round-trip; swarm creation; no-deprecated-API gate |
| T1 | 1 | formation sampling (mesh/curve/text); Hungarian vs. brute-force on small N; density/spacing |
| T2 | 2 | time↔frame; color keyframe serialization; RGBW round-trip |
| T3 | 3 | assignment identity stability; trapezoidal profile respects vmax/amax/jerk; non-crossing |
| T4 | 4 | deterministic violation detection (spacing/speed/geofence/altitude/density); overlay wiring |
| T5 | 5 | golden-file diff per format; VVIZ delta reconstruction; UgCS ≤4fps & order invariant; Vimdrones per-file |
| T6 | 6 | import round-trip parity; QR/text generators; boids stability |
| T7 | 7 | 1000-drone perf gate; full Extension install; docs build |

### 7.4 Representative pure-Python test ideas (no code here, just intent)
- `assignment`: a 3-drone↔3-slot case with a known unique optimum → assert exact mapping.
- `vviz_writer`: feed a fixed `TrajectorySample` list → assert header fields, that
  `home + Σ(dx,dy,dz)` equals the sampler's absolute positions, and that `Σ color frames` equals
  `duration × defaultColorRate`.
- `coord`: Blender `(0,1,0)` → `ogl` `(0,0,-1)`; ENU tangent-plane lat/lon offset within tolerance.
- `ugcs_writer`: feed a 6 fps trajectory → assert output decimated to ≤4 fps; feed 13000 frames →
  assert it refuses.

---

## 8. Deprecated / Avoid List (anti-regression)

| Do NOT use | Use instead |
|---|---|
| `bgl` (removed in 4.0) | `gpu` module + `gpu_extras.batch` + `SpaceView3D.draw_handler_add` |
| `context.user_preferences` | `context.preferences` |
| `bpy.ops.*` inside hot loops / per-drone | data API, batch creation, modal+`event_timer` |
| One material/object per drone | single shared LED material + Point Cloud / instances |
| Reading live `bpy.data` inside handlers | read **evaluated** depsgraph data |
| Reinventing an animation editor | Dope Sheet / Graph Editor / NLA |
| Reordering drone identity | stable `drone_id`/point-index; only slots change |
| Relying only on legacy `bl_info` | ship `blender_manifest.toml` (Extensions) |

---

## 9. Confirmed Decisions (locked)

1. **Hungarian algorithm — `scipy.optimize.linear_sum_assignment`, lazy-loaded + pure-Python fallback.**
   scipy is the most optimal, best-documented, and easiest-to-test choice, so it is the primary path.
   It is **not vendored** (keeps the Extension light); at runtime we try `import scipy.optimize` and,
   if absent, transparently fall back to a bundled pure-Python Hungarian. Both paths are unit-tested
   against brute force, so correctness is identical regardless of whether scipy is installed.
2. **Primary swarm representation — Point Cloud (data backbone) + Instance-on-Points (visual skin), single shared LED material.** Confirmed.
3. **Minimum Blender version — `blender_version_min = "5.0.0"`** (developed against the 5.1 alpha). No 4.x support. Confirmed.
4. **UgCS PATH3 — full writer now (NOT behind an experimental flag).** Implemented as a complete,
   first-class export target alongside PATH, encoding to the documented PATH3 constraints.
5. **Depence format — full launch target now.** Treated as a first-class writer from the start (the
   least-documented of the five, so its golden-file test is the acceptance gate for its fidelity).
6. **Pyro payloads — modeled AND fully authored now (model + authoring UI).** Because pyro is not
   required to produce end-to-end *animations*, it is scheduled in the **post-MVP accelerator phase
   (Phase 6)** — but when built there it is a complete feature (data model + UI), not deferred.
7. **Geo-referencing — local ENU (East-North-Up) tangent-plane / flat-earth approximation, anchored
   at the show origin.** This is the best fit for this project: it is the de-facto standard for drone
   shows (local meters → real-world via a single lat/lon/alt anchor), is simple and well-documented,
   is accurate across a typical ~1 km show footprint, and is what the target export stacks expect
   (matches the VVIZ `globalReferenceFrame` and UgCS conventions). Full UTM/MGRS is NOT pursued.
   The **minimal origin anchor** lives in the **MVP export phase** (Phase 5, needed for VVIZ/Depence
   `globalReferenceFrame`); richer geo-ref tooling (map anchor picker, CRS presets) is Phase 6.
8. **Music sync — included now as a full (not cut) feature, scheduled post-MVP (Phase 6)** per the
   MVP rule (not required to produce an animation end-to-end). Implements VSE audio-lane cues +
   `eventTags`; full beat-detection remains optional/later.

### MVP boundary (governing sequencing rule)
**The MVP = Phases 0–5: the minimum slice that produces a drone-show animation end-to-end** (create →
animate → transition → validate → export to a real control format). **Phase 6 (accelerators) and
Phase 7 (polish) are explicitly post-MVP.** Anything the user approved as "include now" but that is
*not required to produce an animation end-to-end* (pyro, music sync, QR/text generators, flocking,
import round-trip, presets, full geo-ref tooling) is kept in the plan as a committed feature but
**sequenced into Phase 6+**, never blocking the end-to-end MVP. Export formats are end-to-end
essential, so PATH3 and Depence stay in the MVP export phase.

---

## 10. Summary

This plan rebuilds Sirius on a **bpy-free core + thin Blender adapter** so the hard parts
(assignment, collision, feasibility, coordinate conversion, five export encoders) are unit-testable
and version-isolated. The **Point Cloud + instances** swarm solves the prototype's scalability
failure; **Geometry Nodes** provides idiomatic formation generation; **native F-Curves/NLA** provides
animation without a custom editor; the **`gpu` module** provides modern viewport feedback. The
phases move from *stabilize → generate → animate → transition → validate → export* (the **MVP**,
Phases 0–5) then *accelerate → polish* (post-MVP, Phases 6–7), each with explicit deliverables,
dependencies, risks, and a test milestone. The export engine is format-agnostic at its core (unified
`TrajectorySample` sampler) with one writer per real-world format — **CSV, Vimdrones, UgCS PATH and
PATH3, VVIZ, Depence** — encoding exactly per the verified specs, with ENU geo-anchoring and an
export sample rate decoupled from the viewport fps.

**Next action for the implementer:** all §9 decisions are locked — begin **Phase 0**.
