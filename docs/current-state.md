# Current state

Source audit: September 18, 2026. Baseline commit: `61f04a0`, on
`phase-0/layered-package-layout`. This is a source-level assessment. No add-on
enable, UI, render, or export test was performed during the planning revision.

## What is present

| Area | Evidence | Assessment |
| --- | --- | --- |
| Entry point | [`__init__.py`](../__init__.py) delegates to [`blender/registry.py`](../blender/registry.py) | Central registration already exists; do not assign this again as new work |
| Registration | Five classes and `Scene.my_props` are registered and removed in reverse order | Basic lifecycle is present; partial-failure recovery and repeated enable/disable need testing |
| Packaging | [`blender_manifest.toml`](../blender_manifest.toml) declares version 0.1.0, Blender 4.5, MIT | A manifest exists; installation and support claims are unverified |
| Grid | [`operators/create_takeoff_grid.py`](../operators/create_takeoff_grid.py) | Creates individual sphere objects and materials; does not create flight paths |
| LED controls | [`operators/change_led_color.py`](../operators/change_led_color.py), [`props.py`](../props.py) | Static color and emission strength; no effect stack or timeline logic |
| Materials | [`materials/__init__.py`](../materials/__init__.py) | The import typo mentioned by the previous plan is already fixed |
| Package layout | `core/`, `algorithms/`, `exporters/`, `ui/` | Empty package markers, not implemented subsystems |
| Export and planning | [`operators/export_csv.py`](../operators/export_csv.py), [`utils/pathfinding.py`](../utils/pathfinding.py) | Unregistered export function and trajectory stub, both containing `pass` |
| Quality infrastructure | Tracked-file inventory and GitHub workflow listing | No add-on tests or CI, reference shows, benchmarks, or reproducible package procedure; the hosted Pages workflow only deploys the website |

The [testing and CI plan](testing-and-ci.md) adds explicit M0 requirements for
local test commands, automated pull-request checks, and merge enforcement.
These are planned work; publishing the plan does not install a test harness or
configure required checks.

## Problems to reproduce and address

1. **Creating a grid changes unrelated scene state.** The grid operator calls
   `configure_lighting_compositing()`. That function selects Filmic and clears the
   scene compositor's nodes. A creation tool must preserve a user's existing
   compositor, cameras, color management, and unrelated objects.
2. **The compositor code crosses a known API break.** It uses `scene.node_tree`,
   which Blender removed in 5.0. A grid operation reaches this code before it
   creates its drones. Porting the preview workflow is therefore separate from
   enabling the extension. See [Blender's migration notes](https://developer.blender.org/docs/release_notes/5.0/python_api/).
3. **Names currently act as identity.** The LED operator recognizes collection,
   object, material, and node names. Renaming an object or creating a second grid
   can break these assumptions. A stable drone identifier must survive renaming,
   point reordering, and save/load.
4. **The empty-scene path can fail.** With “Apply to All Drones” enabled and no
   collection named `Drones`, `drones_collection` is used without an assignment.
   Missing materials or emission nodes also need explicit handling.
5. **Failure is reported as success.** Insufficient grid capacity emits a warning
   but returns `FINISHED`. Neither creation nor color editing declares an undo
   policy. Test cancellation, undo/redo, repeated creation, and partial failure.
6. **Creation costs need measurement.** The operator creates a sphere through
   `bpy.ops` and a material for every drone. This is a plausible bottleneck, not
   evidence for a particular maximum drone count. Benchmark before replacing it.
7. **A pure module is not yet independently importable through the package.** The
   root import immediately imports the Blender registry and `bpy`. Future tests
   of `sirius.core` must account for package initialization; empty folders alone
   do not establish a Blender-independent core.
8. **Generated files are tracked.** Eight `.pyc` files under materials, operators,
   and panels remain in Git despite ignore rules. Remove those tracked artifacts
   during repository hygiene; preserve source and unrelated files.

The material helper also returns no material value and its caller retrieves the
new material by name. This is a useful ownership/design exercise, not a reason
to rewrite the whole package before the first working feature.

## Corrections to the previous plan

| Previous assumption | Revised treatment |
| --- | --- |
| Registry and import fix still need implementing | Preserve the work already present; verify behavior |
| A point cloud and fixed point indices are the settled architecture | Compare representations; store identity separately from storage order |
| Only `blender/` may import `bpy`, while operators and panels subclass Blender types | Blender-facing UI and integration may use Blender APIs; the numerical core may not |
| Native NLA automatically supplies a show editor | Prototype cue timing and native animation integration before choosing a timeline UI |
| Hungarian assignment and interpolation produce non-crossing paths | Assignment, trajectories, and continuous separation are distinct problems |
| A trapezoidal velocity profile bounds jerk | Acceleration jumps need separate treatment; choose a motion model deliberately |
| Grid generation should be sub-linear in drone count | Writing N drone records already requires O(N) work; measure time and memory |
| Five flight/export formats belong in the first MVP | Start with documented interchange; qualify each vendor adapter separately |
| CSV is generically flight-ready | CSV has no universal flight contract |
| PATH3 and Depence are already fully specified | Gather current specifications and receiver evidence before committing support |
| “4.5 or newer” is a support policy | Publish exact tested versions and upgrade gates |
| Preview and music arrive after all exporters | Put a useful preview and cue workflow into the first design demonstrator |

## How to continue

M0 in the [project plan](../project-plan.md) starts with a reproducible baseline
and small repairs. Keep the existing implementation as the working starting
point. Move or replace modules when a demonstrated requirement makes the change
useful, and keep the new behavior reviewable at each step.
