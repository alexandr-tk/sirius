# Decisions and open questions

Revision: September 18, 2026. A recommendation in this document is not a completed
implementation. Record a decision's evidence and consequence when it is adopted.

## D01: Modern Blender support

**Recommended:** establish Blender 5.2 LTS as the first tested target. Exercise
upcoming builds as compatibility probes. Offer 4.5 support only if there is a
demonstrated user need and a passing matrix; do not let it constrain the first
implementation unnecessarily.

**Evidence:** [Blender's maintained releases](https://www.blender.org/releases/)
and [5.0 API breaks](https://developer.blender.org/docs/release_notes/5.0/python_api/).
**Next decision:** in M0, record exact builds, bundled Python, OS/architecture,
install tests, and the manifest support range. No version metadata changed in
this planning revision.

## D02: Open and local production pipeline

**Accepted product direction:** all essential authoring, solving, validation,
render setup, and implemented exporters are available as source and run locally.
No required proprietary computation backend or account. Optional integrations may
connect to other tools without making the local workflow incomplete.

Open-source dependencies are compatible with this goal. The implementer chooses
them deliberately, understands their contracts, and records licenses and packaging.
Personally writing Sirius does not require reimplementing Blender or every
numerical library, but opaque dependencies should not replace learning the problem.

## D03: Distribution license

**Current:** the repository and manifest say MIT. They remain unchanged.

**Required decision before public platform distribution:** Blender's
[Extensions Platform policy](https://docs.blender.org/manual/en/5.2/advanced/extensions/licenses.html)
requires GPL-3.0-or-later for add-ons and CC0 for included assets. The previous
plan's unconditional MIT-platform release claim was therefore incomplete.

**Recommendation:** choose a GPL-3.0-or-later extension distribution if the official
platform is the intended route. Review whether a separately distributed pure core
should retain a permissive license. Inventory authorship, reused code, icons,
fonts, example media, and dependencies before changing notices. An MIT notice on
Sirius does not establish the licensing of material imported from elsewhere.

The maintainer must make and record this choice; this plan does not relicense
existing work. It does not prevent local learning or numerical prototyping.

## D04: Drone representation

**Open:** retain ordinary objects for the first small working slice, then compare
shared meshes/materials, mesh points with instances, and native point clouds.

**Experiment:** create the same data at 64 and 1,000 drones; exercise selection,
per-drone colors, modifiers, save/load, direct time evaluation, background render,
and output identity. Measure time and memory. Expand at M9. Stable logical IDs
are required regardless of representation; no fixed-index identity shortcut.

## D05: Authoring state and evaluation

**Recommended contract:** `.blend` authoring data is authoritative; the adapter
produces immutable pure-data snapshots. Caches and generated geometry are derived.
**Proof required at M1–M3:** undo/save/reopen/direct seek reproduce the same result,
with no second mutable show state silently drifting from the scene.

## D06: Timeline interaction

**Open:** start with a cue list, native markers, and native animation controls.
Prototype Action/NLA integration with real retiming cases before choosing the
full timeline design. A custom timeline is justified only if the simpler UI fails
observed designer tasks. Do not build one solely to resemble a competing product.

## D07: Solvers and numerical dependencies

**Open:** learn assignment and motion on tiny cases with independent oracles;
choose a production solver from measured requirements. An assignment method alone
does not solve separation or dynamic feasibility.

**Decision gate at M5/M9:** correctness, determinism, failure behavior, complexity,
license, binary distribution, and support across Blender's actual Python runtimes.
Do not select a different production algorithm based on whatever happens to be
installed on the user's computer.

## D08: Export priority

**Recommended:** Sirius JSON/CSV, then VVIZ visualization, then one execution
toolchain with accessible specifications and a testing operator. SKYC, PATH/PATH3,
Vimdrones, and Depence are research candidates rather than promised first-release
support. Reorder them when an actual user and receiver access provide better evidence.

## D09: Validation and preview claims

**Required contract:** validation says which model and revision were checked;
previews say whether appearance is estimated or calibrated. No generic “safe
flight” badge, silent export override for failed mandatory checks, or guarantee
that a render predicts a particular camera/site without supporting evidence.

## D10: Scale and advanced integrations

**Qualification targets:** measure 64, 1,000, 5,000, and 10,000 drones. Set hardware
and workload budgets before implementation claims. Large scale may require
different data/solver choices, but the small reference evaluator remains useful.

**Separate future decisions:** live control, hazardous payload firing, concurrent
cloud editing, and hosted services. They are not prerequisites for a complete
open-source authoring and production-handoff extension.

## D11: Independent frontend and computational core

**Accepted direction, September 18, 2026:** develop Sirius's own Blender frontend
and open computational core from the current prototype. Skybrush is a reference
and possible interoperability target. Reusing its frontend is not the initial
implementation strategy.

**Reason:** control over the whole production workflow and direct understanding
of its architecture are project goals. Reuse could shorten development but would
also introduce another project's data model and backend contract. The independent
route includes responsibility for authoring, persistence, editing, and integration,
as well as the planner. Preserve useful existing code and grow working features.

**Consequence:** begin with a local library and a Blender adapter. Add worker
processes, a server, or external compatibility only when a concrete use requires
them. Revisit this decision if maintaining the frontend prevents progress on the
core, or an independently useful integration justifies a narrower scope.

## D12: Measured performance and product comparisons

**Required evidence:** follow the [evaluation plan](performance-and-evaluation.md).
Record workload, hardware, builds, quality settings, numerical coverage, and
backend mode before comparison. A fleet cap or unavailable paid feature is a
capability/access difference, not a runtime measurement.

Keep reference numerical cases and correctness checks while optimizing. Publish
task-specific results and known tradeoffs. Hardware budgets and supported capacity
remain to be qualified; no benchmark result exists in this planning revision.

## Decision entry format

For a new or revised choice, record the problem, constraints, two plausible
options, the smallest useful experiment, results, selected option, known costs,
and the condition that would justify revisiting it. Keep the record short and
link the implementation/test evidence when it exists.
