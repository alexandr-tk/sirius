# Performance and workflow evaluation

This is a plan for collecting evidence. Sirius has no measured performance or
competitive advantage recorded yet. The first baselines begin at M1; M9 expands
them into release benchmarks. Keep the fixtures small enough to understand before
adding scale.

## What a better production tool must demonstrate

| Area | Question | Evidence |
| --- | --- | --- |
| Complete open workflow | Can someone build and run every essential Sirius function locally? | Source and dependency inventory, documented build, offline authoring/solve/validate/export demonstration without an account |
| Lighting authoring | Can a designer create and revise the intended effect with less effort? | Same brief, completion time, errors, manual steps, recovery, and designer feedback |
| Preview delivery | Can the designer produce repeatable client stills and video with less setup? | Setup time, preserved scene state, render settings, reference images, and audio/timing checks |
| Planning | Can the planner produce useful valid motion within a practical resource budget? | Independently checked solution rate, runtime, memory, duration, travel, and constraint margins |
| Editing at scale | Does the interface remain responsive on a representative show? | Scrub latency, playback rate, edit response, memory, and cancellation under recorded settings |
| Handoff | Does another person or application receive the intended show? | Asset relocation, reopen, decoded output comparison, receiver tests, and revision-bound reports |

Judge these areas separately. A faster approximation, a cheaper workflow, and a
more accurate output are different outcomes. Report the benefit and its cost.

## Comparison protocol

Use a current stable Skybrush release as a named baseline where it supports the
task. Other tools may be added when their users and test environments are
available. Do not infer missing capabilities from an old version or an unfamiliar
workflow; use its documentation and an experienced user when possible.

For every comparison:

1. Record exact Sirius, Blender, comparison-tool, and backend versions; OS, CPU,
   GPU, RAM, power settings, renderer, and relevant numerical dependencies.
   Record the comparison tool's license/features and local or cloud backend mode.
2. Use the same input geometry, drone count, timebase, fleet/site constraints,
   manual locks, source media, and requested result. Pin the input files and seeds.
   Native implementations may differ; document any difference in supported scope.
3. Match rendering quality, effect sampling, interpolation/error tolerances, and
   validation coverage before comparing speed. Compare fast viewport modes with
   equivalent modes. Report quality differences when exact parity is unavailable.
4. Separate local computation from network latency, queue time, scene sampling,
   data transfer, and encoding. Also report total time seen by the designer.
   Measure cold starts and warm repeated use separately.
5. Repeat timed jobs and retain raw results. Start with at least five runs for
   long jobs, reporting median and range. Collect at least 100 defined interaction
   samples before reporting a 95th-percentile latency. Record failures and timeouts
   in the denominator rather than discarding them as outliers.
6. Publish fixture revisions, commands or manual steps, settings, results, and
   limitations with the claim. If assets cannot be shared, publish a representative
   redistributable fixture and identify the limit on reproducibility.

The free Skybrush design server has a documented service cap. Compare larger
solves using an authorized backend with the needed capacity, or record that the
comparison could not be run. Do not use a blocked request as evidence that Sirius
has a faster solver. Never weaken constraints or skip checks to obtain a result.
See the [source register](research.md#product-baseline).

## Workload corpus

Each fixture needs a purpose, source/provenance, units, parameters, expected
behavior, and a reproducible seed where relevant. Include representative production
tasks alongside adversarial cases; deliberately impossible cases test refusal
behavior, not successful-solve speed.

| Family | Cases | First stage |
| --- | --- | --- |
| Scene representation | 64 and 1,000 drones; create, select, rename, recolor, save/reopen, duplicate a show | M1 |
| Lighting | Moving masks, overlapping layers, image/video mapping, direct seek, reverse scrub, changed media and invalidated caches | M2–M3, expand at M8 |
| Designer revisions | Replace a logo, move a cue, revise a palette, change drone count, undo the change, and explain an unexpected color | M3–M4 |
| Motion | Sparse and dense formations, long travel, head-on swaps, locks, unequal groups, short durations, obstacles, staggered launch/return/landing | M5 |
| Validation | Between-sample conflict, curved overshoot, uncertainty margins, boundary crossing, stale data, unsupported trajectory, and canceled check | M6 |
| Export | Different sample rates and units, asymmetric axes, fractional times, RGBW loss, quantization, final samples, and changed downstream motion | M7 |
| Preview | Same still and sequence at defined quality; multiple cameras, missing assets, out-of-order frames, cancellation and resume | M3/M8 |
| Production scale | 64, 1,000, 5,000, and 10,000 drones; a ten-minute show, sparse/dense cases, realistic effects, and recorded export rates | M9 |

Use exhaustive or hand-derived small cases as correctness references. The large
fixtures measure scale and exercise integration; size does not make their output
correct. Keep a separate set of unseen variations to check that tuning has not
only improved the published examples.

## Budgets and supported capacity

Choose the reference hardware and a representative fixture before setting a
release budget. Initial targets for the 1,000-drone draft preview are at least
24 evaluated frames per second and warm direct-seek latency at or below 100 ms
for 95% of the defined interactions. These are proposed usability targets, not
observed results. Record resolution, effects, helper visibility, and level of
detail; dropping required LED evaluation cannot count as meeting the target.

At M1 record the baseline hardware, scene creation time, evaluation time, and peak
memory. At M3 add editing and preview budgets. At M5–M7 choose solve, validation,
and export time/memory budgets from the supported workload and operator needs.
At M9 publish the full matrix, including larger workloads that exceed a budget.
Do not invent timings now or move a budget after a failed run without recording
the reason and effect on the supported workload.

Record file size, temporary disk use, responsiveness during long jobs, and the
time to acknowledge cancellation and reclaim resources. A canceled job must not
leave apparently complete output. An implementation may report that a workload
exceeds its tested capacity; open source does not imply unlimited compute.

## Solver quality and optimization

Keep assignment cost, trajectory duration, path length, derivative limits,
separation margins, and resource consumption visible as distinct objectives.
The best assignment by one cost need not produce the best timed show. Compare
valid solutions under the same constraints and document designer tradeoffs.

Record solved, proven infeasible, budget exhausted, unsupported, and invalid
candidate as different outcomes. Unless a method establishes infeasibility,
failure to find a solution must remain a search failure. Validation coverage is
reported independently of the planner's confidence or success flag.

Profile before choosing vectorization, spatial indexing, caching, parallel work,
native code, or GPU computation. Optimize the measured bottleneck and include
data-copy, startup, packaging, and memory costs in the evaluation. Retain the
small reference implementation and compare behavior across seeds and edge cases.
Determinism means the documented result/tolerance holds under the supported
execution conditions; record any nondeterministic solver or hardware behavior.

Begin regression measurements when each subsystem first works. Use repeatable
microbenchmarks for diagnosis and complete designer tasks for release decisions.
A speedup is accepted only with its correctness/fidelity checks and a documented
tradeoff where behavior changes. Set a meaningful comparison margin before the
experiment, based on measurement variation and the designer's practical benefit.

Keep small deterministic correctness checks in pull-request CI. Run larger
benchmarks on a schedule and before release, following the
[testing and CI plan](testing-and-ci.md#scheduled-and-release-checks). Use a
recorded reference machine for timing comparisons; noisy shared-runner timings
are diagnostic evidence until a repeatable regression threshold is established.

## Adoption evidence

At M3 begin observing a designer complete a small task. At M8–M10 have external
designers and operators evaluate their normal revisions, preview delivery, and
handoff. Record assistance required, mistakes, recovery, and missing capabilities.
Do not equate preference for one demo with readiness to replace a production tool.

Include migration work: import existing evaluated tracks where supported, map
identities and home positions, preserve timing, relocate assets, and compare the
result in the receiver. Document authoring information that cannot be recovered
from an interchange file. Each pilot needs a supported workflow, acceptance
criteria agreed before the trial, and a record of unresolved blockers.

Publish narrow conclusions such as a measured reduction in mask-editing time on
a named workload. Broad claims of superiority require broader evidence. Numerical
review and the [export qualification requirements](validation-and-export.md) remain
necessary even when a designer prefers the workflow.
