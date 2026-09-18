# Contributing to Sirius

Sirius is an early prototype. The [source audit](docs/current-state.md) describes
what exists; the [project plan](project-plan.md) describes intended behavior.
Discuss substantial features or architectural changes in an issue before starting
them, especially exporters, persistence, and trajectory planning.

## Development setup

Use a dedicated Blender test profile and disposable `.blend` files. The prototype
currently changes compositing settings during grid creation and still needs the
Blender 5.x migration work listed in M0. Do not use client or operational show
files for initial testing.

Blender 5.2 LTS is the planned primary target. Record the exact build, operating
system, architecture, and bundled Python version when testing. A host Python
virtual environment can run pure numerical tests once that harness exists; it
does not replace testing Blender integration in Blender itself.

The test harness, add-on CI, and release packaging procedure are not implemented
yet. M0 establishes them through the [testing and CI plan](docs/testing-and-ci.md).
It defines local checks, pull-request checks, test fixtures, and release evidence.
Use Blender's documented extension build/validation mechanism on a reviewed
staging directory containing the intended source and assets.
Inspect the resulting archive: Git ignore rules alone do not control its contents.
Exclude private notes, virtual environments, caches, source-control metadata,
temporary output, and third-party assets that are not licensed for distribution.

## Changes and review

Keep each change focused on one observable behavior. Describe the problem, the
result, and the verification performed. Include a small reproduction for a bug
and identify checks that were not run.

Once M0 establishes the check commands, run the relevant checks locally before
opening a pull request. GitHub Actions will run the required checks again; branch
rules must require their success before merge. Optional local Git hooks can catch
mistakes earlier, but contributors must not need a hook to run the same checks.
Manual Blender and receiver observations supplement automated results. Record
the build, steps, and outcome whenever a check cannot run in CI.

Pure show data and numerical behavior must remain independent of Blender. UI and
scene adapters may use Blender APIs. Preserve stable drone identity, explicit
units/time, non-destructive editing, and deterministic evaluation. Read the
[architecture](docs/architecture.md) before changing these boundaries.

Use meaningful tests for numerical behavior, persistence, destructive operations,
and format contracts. UI integration needs an actual Blender check. Export support
requires testing in the named receiving application; a self-generated golden file
alone is insufficient. Do not mark an unavailable receiving application as tested.

Document the origin and license of reused code, dependencies, fonts, media, and
fixtures. Do not include private customer shows in an issue or test corpus without
permission. Changes to distribution licensing require an explicit maintainer
decision; see [D03](docs/decisions.md#d03-distribution-license).

## Bug reports

Include the Sirius commit/version, Blender build, OS, minimal reproduction steps,
expected and observed behavior, and relevant traceback. Add a small sanitized
`.blend` only when needed. For motion/export issues, include units, timebase,
profiles, target/version, and the smallest data that reproduces the problem.

For a defect that could affect an operational export, state the affected version
and workflow clearly. Avoid implying that a corrected design file has already
been qualified for use on a fleet.
