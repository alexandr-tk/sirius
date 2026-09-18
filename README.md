<img src="assets/logo.png" alt="Sirius logo" width="96" height="96" align="right">

# Sirius

Open-source drone-show design, lighting, and production tools for Blender.

Sirius is being built for the full design workflow: create formations, choreograph
movement, animate LEDs, preview the show, check constraints, and prepare exports
for other production tools. The priorities are expressive lighting, useful render
previews, and a local workflow whose algorithms and file formats can be inspected.

The project will develop its own Blender authoring tools and an open computational
core for planning, validation, and export. Essential functions will run locally
without an account, proprietary solver, or drone-count license tier. Compatibility
with other show tools will be added through documented adapters.

**Status: early prototype.** The source contains a takeoff-grid generator and
static LED controls. Animation, trajectory planning, validation, render presets,
and exporters remain to be implemented. No output is qualified for flight use.

## Planned workflow

- Create formations from curves, text, logos, meshes, and reusable assets.
- Design LED animation with layered effects, moving mask objects, gradients,
  image projection, groups, and cues tied to the show timeline.
- Plan transitions, takeoff, and landing against explicit fleet and site limits.
- Preview a frame or a complete show with cameras, scenery, exposure, and LED
  appearance presets suitable for client review and marketing.
- Inspect validation results and export a reproducible package for a named
  downstream application and version.

These are development goals. The [project plan](project-plan.md) defines the
milestones and the evidence needed to call each feature complete.

## Blender support

Development is planned around **Blender 5.2 LTS**. Blender's
[release listing](https://www.blender.org/releases/) identifies 5.2 and 4.5 as
maintained LTS releases as of September 18, 2026.

The current manifest still declares a 4.5 minimum. That metadata is not a tested
compatibility matrix: the prototype needs changes for Blender 5.x, including its
compositor integration. Milestone M0 establishes a verified development build and
updates the metadata. Support for additional versions will be listed only after
testing. See the [source audit](docs/current-state.md).

## Export plans

| Target | Intended use | Status |
| --- | --- | --- |
| Sirius JSON and CSV | Documented interchange, debugging, and round-trip tests | Planned first |
| VVIZ | Visualization in compatible applications | Planned |
| Skybrush SKYC | Handoff to the Skybrush toolchain | Research candidate |
| SPH PATH / PATH3 | Handoff to Drone Show Software | Research candidates |
| Vimdrones | Handoff to a documented Vimdrones workflow | Research candidate |
| Depence Show Stream | Production visualization | Research candidate |

No exporter is implemented. A file extension or a successful write does not
establish compatibility. Each adapter needs a format reference, representative
files, and tests in its receiving application. The
[validation and export plan](docs/validation-and-export.md) records these gates.

## Development

Start with the [current state](docs/current-state.md), then the
[architecture](docs/architecture.md) and [contribution guide](CONTRIBUTING.md).
The repository does not yet provide a verified release package or test harness.
Use a disposable Blender file when exploring the prototype; grid creation
currently changes scene compositing settings.

The planned core handles show data, lighting, validation, and file conversion
without depending on Blender. The Blender integration supplies authoring tools,
scene evaluation, and previews. This separation will allow numerical behavior to
be tested independently of the interface.

## Documentation

- [Roadmap and release criteria](project-plan.md)
- [Architecture and data ownership](docs/architecture.md)
- [Lighting and render workflows](docs/lighting-and-preview.md)
- [Validation, export, and interoperability](docs/validation-and-export.md)
- [Testing, continuous integration, and release checks](docs/testing-and-ci.md)
- [Performance and workflow evaluation](docs/performance-and-evaluation.md)
- [Research and source references](docs/research.md)
- [Decisions and open questions](docs/decisions.md)

## License

The repository is currently licensed under [MIT](LICENSE). The licensing decision
for distribution through Blender's official Extensions Platform remains open;
see [D03](docs/decisions.md#d03-distribution-license).
