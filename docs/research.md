# Research and references

Reviewed September 18, 2026. These sources inform the plan; they do not establish
that Sirius implements a feature or that a receiving application accepts its
files. Recheck moving `latest` pages before implementation and record the
specific version or commit used by an adapter.

## Product baseline

| Source | Relevant finding | Consequence for Sirius |
| --- | --- | --- |
| [Blender releases](https://www.blender.org/releases/) | Lists Blender 5.2 and 4.5 as maintained LTS releases | Use 5.2 as the proposed primary target; maintain a tested version matrix |
| [Skybrush Studio 4.2 release](https://www.skybrush.io/blog/2026-03-29-skybrush-studio-4.2/) | Explicitly describes Blender 5.0/5.1 support | Do not position Sirius around an outdated Blender-only comparison |
| [Skybrush Studio 5.0 release](https://www.skybrush.io/blog/2026-07-30-skybrush-studio-5.0/) | Adds grouping, experimental lighting presets, and visualization improvements | Benchmark current supported workflows; vendor performance claims are not Sirius measurements |
| [Skybrush Light Effects](https://docs.skybrush.io/public/skybrush-studio-for-blender/latest/panels/leds/light_effects.html) | Documents animated invisible mesh masks, layered effects, groups, ramps, and image sources | Masking is an existing industry capability; compare discoverability, editing effort, and reproducibility |
| [Skybrush source repository](https://github.com/skybrush-io/studio-blender) | The Blender add-on is GPL-3.0-or-later | Describe the exact local/open workflow Sirius aims to provide; avoid calling the whole alternative closed source |
| [Skybrush transition concepts](https://docs.skybrush.io/public/skybrush-studio-for-blender/latest/concepts.html#_transition_planning) | Automatic transitions use Studio Server calculations described as proprietary | Sirius's fully open planner is a substantive scope difference, separate from interface features |
| [Skybrush backend installation](https://docs.skybrush.io/public/skybrush-studio-for-blender/latest/install.html) | Studio Server handles planning and exports; licensed offline operation already exists | Distinguish complete open computation from offline operation alone; the live-control Skybrush Server is a different component |
| [Skybrush service-limit announcement](https://www.skybrush.io/blog/2025-02-04-skybrush-store/) | Announces a 64-drone community design-server limit effective March 1, 2025 | A service tier does not measure algorithmic capacity; use an appropriate backend or label a comparison unavailable |
| [Skybrush export panel](https://docs.skybrush.io/public/skybrush-studio-for-blender/latest/panels/safety_and_export/export.html) | Available exports depend on show type and license | A fully local, openly implemented export pipeline is a product goal, subject to vendor interoperability |
| [Verge Aero workflow overview](https://docs.verge.aero/drone-show-technology/how-drone-shows-work-an-overview) | Describes launchpads, formation allocation, site context, and audience considerations | Production requirements extend beyond shape generation |
| [SPH Drone Show Creator](https://www.droneshowsoftware.com/drone-show-creator) | Describes choreography and mixed media authoring | Evaluate complete designer tasks, including media, timing, and handoff |
| [SPH 2026.1.1 update](https://www.droneshowsoftware.com/news/drone-show-creator-2026-1-1-update-faster-visual-design-smarter-image-tools-and-universal-data-compatibility) | Describes CSV exchange and image/video projection updates | Import and lighting workflows deserve early evaluation |

The founder's experience with an older Skybrush workflow remains a useful design
input. The current documentation shows that invisible masks and newer Blender
support are already present. The opportunity proposed here is an easier lighting
workflow, reproducible previews, and an inspectable local production pipeline.
Those advantages remain hypotheses until designers compare actual tasks.
Sirius will implement its own frontend and open core. The
[evaluation protocol](performance-and-evaluation.md) defines how to test the
proposed advantages while keeping source availability, usability, numerical
quality, and speed as separate claims.

## Blender engineering references

- [Blender 5.0 Python API changes](https://developer.blender.org/docs/release_notes/5.0/python_api/):
  compositor changes and removal of the legacy Action API. Relevant to the
  prototype's compositor and future animation work.
- [Blender 4.4 animation changes](https://developer.blender.org/docs/release_notes/4.4/python_api/):
  Action slots and channel bags. Read the current version's API alongside these
  migration notes.
- [Attributes](https://docs.blender.org/api/5.2/bpy.types.Attribute.html):
  geometry domains and bulk attribute access. This does not by itself prove a
  complete editable point-cloud authoring pipeline.
- [Application handlers](https://docs.blender.org/api/5.2/bpy.app.handlers.html):
  lifecycle hooks and the warning about data mutation during rendering.
- [Extension creation](https://docs.blender.org/manual/en/4.2/advanced/extensions/getting_started.html):
  manifest, build, and validation workflow. This versioned reference documents
  the extension mechanism; verify the 5.2 CLI and manifest rules during M0.
- [Blender 5.2 view transforms](https://docs.blender.org/manual/en/5.2/render/color_management/displays_views.html):
  display appearance and tone mapping. A view transform must not become the
  encoding for exported LED commands.
- [Extension licenses](https://docs.blender.org/manual/en/5.2/advanced/extensions/licenses.html):
  the official platform requires GPL-3.0-or-later for add-ons and CC0 for included
  assets. The current MIT repository license was not changed in this revision.

Use migration notes alongside the target version's documentation. Test the
installed Blender build instead of treating a documentation link as proof of
add-on compatibility.

## Export evidence and unresolved questions

| Target | Primary reference | What remains unresolved |
| --- | --- | --- |
| Sirius interchange | To be specified and versioned in this project at M3 | Schema, units, timestamps, interpolation, and golden fixtures |
| VVIZ | [Verge's format reference](https://docs.verge.aero/drone-show-software/verge-design-studio/vviz-format) | Receiver-version tests, axis/heading examples, optional-channel behavior; the reference explicitly limits it to visualization and excludes external validation |
| SKYC | [Skybrush glossary](https://docs.skybrush.io/public/skybrush-live-doc/latest/appendix/glossary.html) and [export documentation](https://docs.skybrush.io/public/skybrush-studio-for-blender/latest/panels/safety_and_export/export.html) | Full archive/schema and trajectory/light encoding references, licensing of any reused implementation, offline generation, and receiver tests |
| PATH / PATH3 | [SPH workflow](https://www.droneshowsoftware.com/drone-show-business-from-the-inside) | Current versioned format specification, fixtures, and access to the receiving application; do not transfer limits between versions |
| Vimdrones | [Vendor export tutorial](https://shop.vimdrones.com/blogs/vimdrones-blog/export-drone-show-path-tutorial) | Its third-party raw export is distinct from its GCS export. A raw writer does not establish native GCS compatibility |
| Depence | [Depence R4 drone documentation](https://help.depence.com/depence-construction/drones) | Show Stream specification, permitted implementation, supported channels, and receiver tests; do not assume VVIZ is its native import format |

The Vimdrones tutorial's PATH/PATH3 settings describe that vendor's workflow.
They are not a universal SPH specification. In particular, the previous plan's
frame-count/rate assumptions must not become validation rules without better
evidence. The same caution applies to ambiguous wording in format examples.

## Learning references

These are original tutorials or documentation from their authors. Read the
explanation, solve a small example, then implement the Sirius case independently.

| Topic | Starting material | Use in the plan |
| --- | --- | --- |
| Python packages | [Python tutorial: modules and packages](https://docs.python.org/3/tutorial/modules.html#packages) | Understand the existing import/registration path at M0 |
| Behavior tests | [pytest: assertions](https://docs.pytest.org/en/stable/how-to/assert.html) | Small expected outcomes and useful failure messages at M0–M1 |
| Domain boundaries | [Cosmic Python: domain modeling](https://www.cosmicpython.com/book/chapter_01_domain_model) | Separate show meaning from Blender objects at M1; do not adopt the whole book's architecture |
| Mask fields | [The Book of Shaders: shapes](https://thebookofshaders.com/07/) | Learn distance fields and smooth boundaries before adapting the idea to 3D at M2 |
| Assignment | [CP-Algorithms: assignment/Hungarian algorithm](https://cp-algorithms.com/graph/hungarian-algorithm.html) | Start with the problem statement and tiny cost tables at M5; leave implementation listings until after an attempt |
| Motion timing | [Modern Robotics: point-to-point trajectories, part 2](https://modernrobotics.northwestern.edu/nu-gm-book-resource/9-1-and-9-2-point-to-point-trajectories-part-2-of-2/) | Compare polynomial, trapezoidal, and S-curve timing at M5 |
| Spatial queries | [Robert Nystrom: spatial partition](https://gameprogrammingpatterns.com/spatial-partition.html) | Understand broad-phase candidate reduction at M6/M9 |
| Path search | [Red Blob Games: introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html) | Build graph-search intuition when obstruction planning is needed; this is not a multi-drone deconfliction solution |

More advanced reading should be selected when a concrete obstacle appears.
For motion planning, that may mean multi-agent pathfinding, safe corridors,
trajectory optimization, or continuous collision detection. Record assumptions
and a small counterexample before adopting a method from a paper.
