# Sirius

![Sirius](assets/logo.png)

An early Blender add-on for drone-show design. The current prototype creates takeoff grids and changes drone LED colors. Animation, transition planning, flight-constraint checks, and export are planned.

**Status:** Alpha — under active development. See [project-plan.md](project-plan.md) for the full roadmap.

## Overview

The long-term goal is to design, animate, check, and export drone shows inside Blender. The current code is a grid-and-color prototype; it cannot yet produce or validate flight files.

## Features

**Planned (MVP)**
- Scalable swarm representation (Point Cloud + instances) for 1,000+ drones
- Takeoff grid / launchpad generation
- Formation generation from any mesh, curve, text, or logo with density and spacing control
- Per-drone and group LED color animation on the timeline
- Automatic formation-to-formation transitions (optimal slot assignment + velocity-profiled motion)
- Collision and feasibility validation (spacing, speed, acceleration, geofence, altitude) with live viewport feedback
- Multi-format export with coordinate-frame and sample-rate conversion

**Implemented**
- Parametric takeoff grid generation
- Per-drone LED color and emission control

## Planned architecture

The roadmap separates algorithms from Blender integration:

- **Core** — bpy-free data model and algorithms (assignment, collision, feasibility, interpolation, coordinate conversion)
- **Blender adapter** — thin `bpy` integration (swarm object, Geometry Nodes, handlers, viewport drawing via the `gpu` module)
- **Exporters** — format-agnostic trajectory sampler with one writer per target format
- **UI** — sidebar panels, operators, property groups

The target representation is a single Point Cloud with instanced proxies and a shared LED material. The current grid operator creates a separate mesh object and material for each drone; the core and exporter packages are placeholders.

## Requirements

- Blender 4.5 LTS or newer
- Use the Python runtime bundled with Blender; this add-on imports `bpy`.

## Installation

1. Build a source package from the repository root with `blender --command extension build`. No release ZIP is currently published. See the [Blender extension build documentation](https://docs.blender.org/manual/en/4.5/advanced/command_line/extension_arguments.html).
2. In Blender, open **Edit → Preferences → Get Extensions → Install from disk** and select the `.zip`.
3. Enable **Sirius**.

## Planned export formats

| Format | Type | Target stack |
| --- | --- | --- |
| CSV | Trajectory data | Generic |
| Vimdrones raw | Control-format target | Vimdrones GCS |
| UgCS PATH / PATH3 | Control-format target | SPH Engineering Drone Show Software |
| VVIZ | Visualization/interchange | Verge Aero, Finale3D, Depence, FWSim |
| Depence | Visualization | Syncronorm Depence |

None of these exporters is implemented yet. Format output and model-based constraint checks will require validation against the target control software and aircraft before operational use.

## Roadmap

The plan is phased around a minimum end-to-end MVP (create → animate → transition → validate → export), followed by accelerators and polish.

- **Phase 0** — Stabilize, restructure, scalable foundation
- **Phase 1** — Launchpad and formation generation
- **Phase 2** — Animation and LED
- **Phase 3** — Transitions and assignment
- **Phase 4** — Collision and feasibility validation
- **Phase 5** — Export engine
- **Phase 6** — Accelerators (geo-referencing, pyro, music sync, flocking, import round-trip) — post-MVP
- **Phase 7** — Polish and release

Full details, including proposed Blender API choices and the test strategy, are in [project-plan.md](project-plan.md).

## Contributing

Contributions are welcome. Pick an open issue labeled `phase-N` or `good first issue`, and read [project-plan.md](project-plan.md) for architecture and conventions before starting. The planned core algorithms and exporters should be testable without Blender; their implementation and tests are still to be written.

## License

[MIT](LICENSE)
