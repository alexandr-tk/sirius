# Validation and export

Sirius will produce design diagnostics first, then qualified handoff files for
specific receiving applications. No current exporter or validator is implemented.
This document defines the intended evidence and failure behavior.

## Four different claims

| Claim | Evidence needed |
| --- | --- |
| The file is well formed | Schema/format checks and a reader that accepts it |
| The file represents the intended show | Units, IDs, timing, motion, color, and declared losses compared with the source revision |
| The modeled motion satisfies selected constraints | Complete checks under stated trajectory, uncertainty, site, and fleet assumptions |
| The workflow is suitable for operational use | Qualified receiver behavior and review/testing by competent fleet operators |

None of these claims automatically establishes the next. The Blender extension
does not issue flight authorization or replace the receiving control system's
checks. It must make its assumptions and coverage inspectable.

## Inputs that must be explicit

A validation job consumes a frozen show revision, fleet profile, site profile,
time range, numerical settings, and evaluator version. It must know whether
motion is piecewise linear, polynomial, sampled from native animation, or generated
by a stateful simulation. Unsupported motion cannot be silently treated as linear.

Fleet profiles distinguish lateral and vertical limits, minimum separation,
vehicle extent, tracking error, timing error, launch/landing phases, yaw behavior,
and any anisotropic/downwash assumptions. They identify the source and version
of those values. Battery/duration checks state whether they use a simple duration
budget or a calibrated model, with its valid conditions. Weather and real-time
positioning quality remain external inputs, not facts derivable from a `.blend`.

Site profiles define local/world/geographic transforms, orientation, coordinate
reference and altitude datum, terrain, obstacles, ceiling/floor, permitted volumes,
and audience/keep-out zones. Unknown elevation or datum must not be replaced by a
plausible-looking zero. The footprint and accuracy requirements determine the
geographic conversion method; do not assume a flat approximation is always adequate.

## Checks and coverage

| Area | Checks | Failure examples |
| --- | --- | --- |
| Integrity | IDs, finite values, schema, sample ordering, complete drone/time coverage | Duplicate IDs, NaN, missing final state |
| Continuity | Defined motion/light intervals and permitted jumps | Teleport at a cue boundary, disconnected track |
| Motion | Speed, acceleration, jerk where supported, yaw/rate, joins | Bézier overshoot, discontinuous acceleration |
| Separation | Pair trajectories over time with the profile's margins | Safe endpoints but a close pass between them |
| Site | Obstacles, permitted volumes, altitude, terrain, audience zones | A segment exits a concave region between samples |
| Launch/return/land | Home mapping, phase-specific spacing/corridors and end behavior | Airborne rules incorrectly applied to a parked grid |
| Duration | Total flight duration and specified reserve/model assumptions | A retime exceeds a fleet's duration budget |
| Lighting | Channel/rate limits, missing media, unsupported payload channels | Flash aliased by an output rate, silently lost white channel |
| Export | Target capabilities, quantization/interpolation error, timing and coordinate conversion | Converted motion violates a limit the source satisfied |

Live viewport checks are fast diagnostics. A full report must cover the complete
requested domain. Point-sampled nearest-neighbor queries alone cannot guarantee
separation between frames. Spatial structures help find candidate pairs; narrow
checks still reason about those trajectories and their margins over intervals.

Use exact interval reasoning for supported simple motion or conservative bounds
and adaptive subdivision with recorded tolerances. Arbitrarily increasing sample
rate is not a proof. If a tolerance cannot be established, a calculation does not
finish, or a trajectory family is unsupported, mark the affected check incomplete
or unassessed. Never convert “no violation found” into “passed” without coverage.

Assignment minimizes an objective; it does not establish collision freedom.
Slowing all drones by the same factor can reduce speed and still preserve their
collision. Trapezoidal velocity timing includes acceleration discontinuities.
These cases belong in both tests and user-facing explanations of planner limits.

## Reports and invalidation

Each report records source/evaluated fingerprints, software and profile versions,
coverage, tolerance, assumptions, severity, drone IDs, time intervals, measured
values, limits, and check duration. The UI links a finding to the affected time
and location. Include plots/nearest-approach inspection and an exportable report.

Relevant edits invalidate the report. That includes masks/media for LED fidelity,
motion, timebase, scene units, device mapping, origin/orientation, profiles, and
target conversion settings. Persist the result's provenance, not just a green
status flag. Keep stale results visible as history, clearly associated with their
old revision.

Execution-target exports require completed, current mandatory checks and a
qualified adapter. Diagnostic and visualization exports may remain available
with their status attached. Hard violations and missing mandatory coverage cannot
be dismissed with a general “export anyway” switch. Any allowed warning
acknowledgment is specific, recorded, and tied to the exact revision.

## Export pipeline

1. Freeze and fingerprint the authoring inputs. Check assets and required profiles.
2. Evaluate full motion and LED programs at the precision needed by the target.
3. Validate the authored/evaluated show under its declared model.
4. Apply the target's units, axes, origin, timing, sampling/interpolation, channel
   encoding, compression, and quantization. Report unsupported data or losses.
5. Decode or otherwise independently reconstruct the target's effective behavior.
   Recheck errors and relevant constraints after conversion. Use the receiver's
   actual interpolation/hold rules rather than assuming them.
6. Write a complete temporary artifact/package, verify contents and checksums,
   then publish it to the chosen local destination atomically where supported.
7. Record receiving-application import/simulation evidence separately. If the
   receiver recompiles or optimizes paths, assess that resulting behavior too.

Sampling rates for motion and lighting can differ from Blender's frame rate and
from each other. Preserve fractional timestamps and the intended final state.
Do not silently cap rates, drop unsupported channels, or simplify trajectories.
Make approximation budgets explicit and reject conversions that exceed them.

## Interchange and adapter program

| Target | Planned role | Qualification requirements |
| --- | --- | --- |
| Sirius JSON | Open, versioned interchange containing show metadata and evaluated tracks | Publish schema, units, precision, interpolation, endpoints and example files; independent parser and migration tests |
| Sirius CSV | Readable tabular samples for analysis and exchange | Publish dialect and a metadata sidecar; timestamps, IDs, units, channel encoding and output ordering must be unambiguous |
| VVIZ | Visualization only | Pinned vendor reference; delta/time/heading and color-hold tests; actual viewer import |
| SKYC | Candidate handoff to Skybrush tools | Full versioned archive/encoding reference, offline writer, reuse-license review, receiver tests and downstream compilation checks |
| PATH / PATH3 | Candidate handoff to SPH tools | Separate versioned specifications and capability profiles; fixtures and receiving application tests |
| Vimdrones raw/native | Separate candidate interfaces | Name the exact interface; prove raw-file acceptance separately from native GCS compatibility |
| Depence Show Stream | Candidate production visualization | Obtain current format documentation and receiver access; qualify supported motion/light/heading channels |

The [VVIZ publisher](https://docs.verge.aero/drone-show-software/verge-design-studio/vviz-format)
explicitly describes its format as visualization data, unsuitable for external
validation. A visual round trip through it must not replace validation of the
actual execution representation.

Avoid a generic “Depence exporter” without a named interface. Its
[R4 documentation](https://help.depence.com/depence-construction/drones) identifies
Show Stream. Similarly, a vendor's tutorial settings are not a universal
specification for every variant of PATH or a guarantee of GCS support. See the
[source/evidence register](research.md#export-evidence-and-unresolved-questions).

## Adapter record required before support is advertised

- Format and receiver name/version; authoritative reference and reviewed date.
- Supported fields and modes, known omissions, limits, and required downstream tools.
- Unit/axis/handedness/origin/heading examples, including an asymmetric test scene.
- Horizontal and vertical datum, precision, and coordinate-conversion tests where relevant.
- Position/light rates, interpolation, quantization, compression, and error budgets.
- Stable ID ordering, logical-to-hardware/home mapping, missing-drone behavior,
  initial/final state and partial-range timing.
- Golden fixtures from independent or hand-derived evidence; not only files
  generated by the writer under test.
- Successful import and semantic inspection in the receiving application, with
  recorded build/profile. Mark this blocked when access is unavailable.
- Licensing/provenance for schemas, libraries, fixtures, and any reused code.

Capabilities should be visible before export so the user can choose a suitable
target. Export-time errors then explain a concrete problem and how to resolve it.

## Production package

Include the execution/interchange files, a manifest, source/evaluated/export
fingerprints, format/profile versions, validation evidence, vehicle/home mapping,
site origin/orientation/datum, cue/audio timing, required assets or references,
known limitations, and operator handoff notes. A review approval names those
exact hashes. A later edit or export conversion produces a new revision.

Handle insufficient disk space, interrupted writes, existing paths, and
cancellation without leaving a partial package that appears complete. Imported
archives need size limits, path traversal protection, schema checks, and no
automatic execution of embedded scripts. User-supplied Python plugins are trusted
code and must be presented as such.

## Verification strategy

The [testing and CI plan](testing-and-ci.md) specifies where these checks run,
how fixtures are maintained, and which results block a merge or release. Add
checks as each behavior is implemented, beginning in M0.

**Pure numerical tests:** hand-computed cases, invariants, property-based cases
where useful, and independent small oracles. Test units/time/IDs, effects,
assignment cost, interpolation, interval separation, and conversion errors.

**Blender integration:** install and lifecycle, actual operator behavior,
undo/redo, save/load and migrations, multi-scene isolation, evaluated modifiers,
direct seeking, callbacks, background sampling, and render-state restoration.
Run these inside a real Blender process. A fake `bpy` is not a substitute.

**Format conformance:** independent reading, boundary/rate/precision cases,
asymmetric coordinate tests, unsupported-channel cases, partial exports,
corrupted input, and actual receiving-application tests.

**Adversarial shows:** two drones swapping positions between sample times;
coincident paths; a near miss near a tolerance; tight/dense neighborhoods; a
concave geofence crossing; overshoot between keys; empty/one-drone shows; mixed
constraints; discontinuities; singular transforms; invalid numbers; stale caches;
unexpected frame rates; shifted origins; missing media; and canceled jobs.

**Performance and operational evidence:** benchmark fixtures with environment
records, long jobs, memory limits, receiver simulation, independent numerical
review, and qualified operator evaluation. Make unresolved findings release
blockers for the affected claim, not hidden TODOs.
