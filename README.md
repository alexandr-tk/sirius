# Sirius

![Sirius](assets/logo.png)

Open-source drone light-show animation tool for Blender. Design formations and flight paths of any complexity, validate them for safe flight, and export to the data formats used by modern drone-control software.

**Status:** Alpha — under active development. See [project-plan.md](project-plan.md) for the full roadmap.

## Overview

Sirius brings professional drone-show choreography into the Blender viewport. It bridges artistic animation and hardware deployment: generate formations from arbitrary 3D objects, animate drones and their LEDs, compute safe transitions between formations, validate against real-world flight constraints, and export for real shows.

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

## Architecture

A layered design keeps the hard logic testable and Blender-version-isolated:

- **Core** — bpy-free data model and algorithms (assignment, collision, feasibility, interpolation, coordinate conversion)
- **Blender adapter** — thin `bpy` integration (swarm object, Geometry Nodes, handlers, viewport drawing via the `gpu` module)
- **Exporters** — format-agnostic trajectory sampler with one writer per target format
- **UI** — sidebar panels, operators, property groups

Drones are represented as a single Point Cloud (data backbone) with instanced visual proxies and one shared LED material, driven by Geometry Nodes for formation generation and native F-Curves/NLA for animation.

## Requirements

- Blender 4.5 LTS or newer
- Python 3.11+

## Installation

1. Download the latest release `.zip`.
2. In Blender, open **Edit → Preferences → Get Extensions → Install from disk** and select the `.zip`.
3. Enable **Sirius**.

## Export Formats

| Format | Type | Target stack |
| --- | --- | --- |
| CSV | Flight-ready | Generic |
| Vimdrones raw | Flight-ready | Vimdrones GCS |
| UgCS PATH / PATH3 | Flight-ready | SPH Engineering Drone Show Software |
| VVIZ | Visualization/interchange | Verge Aero, Finale3D, Depence, FWSim |
| Depence | Visualization | Syncronorm Depence |

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

Full details, including verified Blender API decisions and the test strategy, are in [project-plan.md](project-plan.md).

## Contributing

Contributions are welcome. Pick an open issue labeled `phase-N` or `good first issue`, and read [project-plan.md](project-plan.md) for architecture and conventions before starting. Core algorithm and exporter modules are pure Python and unit-testable without Blender.

## License

[MIT](LICENSE)
