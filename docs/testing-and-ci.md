# Testing and continuous integration

**Status: planned.** Sirius has no add-on test harness or automated add-on checks
yet. The existing GitHub Pages workflow deploys the website. M0 introduces local
tests, GitHub Actions checks, and required results before merge. Later milestones
extend that coverage as features become real.

Continuous integration (CI) runs the repository's checks automatically when code
changes. It should reproduce checks a contributor can run locally and preserve
enough evidence to investigate a failure. Passing CI establishes only the behavior
and environments covered by those checks.

## Build the first checks in M0

Start with one reproducible defect, one small numerical example, and their tests.
Verify that the tests fail for the intended reason, then pass after the repair.
Keep the first suite small enough to understand without a framework project.

Document the runtime and local commands as each check is implemented. CI must
invoke those same entry points. Keep ordinary Python tests independent of `bpy`;
exercise Blender behavior in a real Blender process with a disposable profile
and test files. Record Blender's exact build and bundled Python version instead
of assuming the host interpreter matches it.

After the local checks work, add the pull-request jobs below, then configure
their required status checks. Demonstrate both a blocked failing PR and a passing
corrected revision. Do not merge the deliberate failure. A workflow file or an
empty passing suite is insufficient evidence that the checks protect `main`.

## Checks on pull requests

Run these on pull requests and pushes to `main`. Begin with one pinned primary
Blender build and runner environment; expand only as support is verified.

| Check | Initial scope | Evidence retained |
| --- | --- | --- |
| Source and documentation | Formatting/lint checks for maintained source, local documentation links, and unexpected generated files | Clear file/line diagnostics; no automatic code rewrites |
| Pure Python | Small behavioral tests of existing numerical/data rules, import independence, invalid inputs, and deterministic results | Test results, case counts, runtime/dependency versions |
| Blender integration | Regression cases for the M0 repairs, including preservation of unrelated scene state and empty-scene behavior | Blender build, tracebacks, test results, minimal failure artifacts |
| Extension package | Build and validate a reviewed staging directory, inspect archive contents, install the resulting archive in a fresh profile, and exercise enable/disable/re-enable | Package manifest/file list, artifact hash, installation and lifecycle results |

Add tests for identity/time/persistence in M1, mask boundaries and direct seeking
in M2, and preview/interchange fidelity in M3. M4–M8 add formation/cue behavior,
planner constraints, independent validation, format conformance, and rendering.
The [validation plan](validation-and-export.md#verification-strategy) defines the
cases; each feature brings its relevant cases into CI when implemented.

UI-dependent behavior such as undo, editor context, and interactive callbacks
may need a foreground Blender session. Automate it where the environment permits;
otherwise record a repeatable manual check with its exact build and result.
A background test or fake Blender module does not establish UI coverage.

The package check must test the built archive, not just source imports. Exclude
private notes, customer shows, caches, virtual environments, Git metadata, and
unlicensed assets. Keep release contents explicit and inspect them after building.

## Test files and expected results

Use a small, documented test layout separating ordinary Python tests, Blender
integration, format conformance, and shared fixtures. Create each area when its
first test needs it; empty folders do not count as coverage.

- Prefer tiny, readable JSON/CSV fixtures for show data and file contracts. Use a
  minimal `.blend` when Blender state is necessary. Record how to recreate it,
  its Blender version, purpose, source/license, and expected behavior.
- Derive expected results from hand-worked examples, a documented specification,
  or an independent reference. Saving the implementation's current output as a
  golden file does not prove it correct. Review intentional fixture changes.
- Add boundary and failure cases as well as normal shows: invalid values, missing
  data, interrupted writes, stale results, non-default timebases, and collisions
  between samples. Retain small adversarial examples when a bug is discovered.
- Use seeded randomized/property-based tests where they expose useful invariants.
  Record the seed and reduce failures to reproducible cases. Keep PR runs bounded;
  longer searches belong in scheduled runs.

Use temporary output directories and isolated Blender settings. Test setup and
cleanup must preserve unrelated files and scenes. Fixtures must not require
client data, private credentials, or an external service to exercise the core.

## Required checks and local hooks

Give required checks stable, distinct names. After observing their successful
runs, configure branch protection or a ruleset to require them on `main`, including
normal maintainer merges. Verify enforcement with a temporary PR that deliberately
breaks a test; confirm the failed required check is the merge blocker. Repair the
test and preserve the failing and corrected run links as M0 evidence.

Run the initial required workflow on every PR, including documentation changes.
Avoid path filters that leave a required check pending. If selective execution
is added later, its final gate must still report and verify all applicable job
results; a skipped prerequisite must not hide a failure. GitHub documents these
[required-check pitfalls](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks).

Propagate test and Blender-script failures to a nonzero process exit. Fail on a
crash, timeout, or unexpectedly empty test run. Do not mark a required suite
optional to make a PR green. Known exclusions need a reason and a stated coverage
gap; missing tools or unavailable environments must be visible in the report.

Pin check dependencies and the Blender artifact, verifying its checksum. Keep
fork-PR checks unprivileged and free of secrets; do not run contributed code in a
privileged workflow. Set job timeouts and retain diagnostic logs and small failure
artifacts. Record dependency/build updates so a changed environment is reviewable.

Optional local Git hooks may run the fast checks before a commit or push. Provide
the same commands without hooks, and keep CI authoritative: local hooks can be
absent or skipped. A hook must not silently rewrite project code.

## Scheduled and release checks

Expand these checks as the corresponding features arrive, without waiting for M10:

| Cadence | Coverage | Decision |
| --- | --- | --- |
| Scheduled compatibility runs | Declared Blender/OS combinations, installation, persistence/migrations, integration fixtures, and offline operation | Investigate regressions and resolve them before claiming the affected combination is supported |
| Scheduled numerical and scale runs | Longer adversarial/property-based searches, large shows, cancellation, memory growth, and the benchmark corpus | Preserve failures and measurements; reproduce timing changes on reference hardware |
| Scheduled render checks | Representative frames/clips on recorded engines and hardware, with documented image tolerances and human review where needed | Separate renderer variation from changes to the sampled show or LED program |
| Before release | All required suites on the release commit; the actual packaged artifact; fresh installs/upgrades; supported matrix; long-show runs; applicable receiver tests | Block the affected release/support claim until failures and mandatory coverage gaps are resolved |

Choose the initial schedule after measuring runtime and cost. Development Blender
builds can be an advisory migration check; they do not become supported merely
because a nightly run passed. Record untested GPU/platform combinations explicitly.

Large performance runs follow the [evaluation plan](performance-and-evaluation.md).
Establish hardware, repetitions, variation, and meaningful thresholds before
making wall-clock timing a merge gate. Numerical correctness and export fidelity
remain required even when a faster implementation is being evaluated.

Release evidence identifies the commit, artifact hash, check runs, environment
matrix, known exclusions, and manual Blender/receiver records. Retain it with the
release rather than relying on temporary CI logs alone. Receiving-application and
operator qualification follow the [export gates](validation-and-export.md); a
passing automated suite cannot replace unavailable receiver evidence.
