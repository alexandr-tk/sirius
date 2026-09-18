# Lighting and preview workflows

These requirements put LED authoring and useful previews into M2–M3, then expand
them for production in M8. All features here are planned.

## The first interaction

A designer creates a small formation, chooses a color, and adds a spherical mask.
The mask appears as an editable guide. Moving it through the formation changes
only the LEDs inside it. The guide remains available for editing and evaluation
while being absent from the final image.

The designer sets the effect's start/end times and feathering, then adds a second
effect above it. Scrubbing, playing backward, jumping to a frame, reopening the
file, and rendering that frame produce the same LED values. A selected-drone
inspector explains which effects contribute to its current color.

This is the first complete lighting behavior. It should work before advanced
pathfinding or vendor-specific export.

## Effect contract

Every effect has a persistent ID, name, time range, target group, coordinate space,
mask, color source, intensity/opacity, blend operation, and revision. Random effects
also have a stored seed. Missing inputs have an explicit error state.

The light program combines a base value and ordered effect layers. Define whether
an operation replaces, mixes, adds, multiplies, or takes the maximum of channels;
define how opacity and intensity participate. Keep preview and export on that same
definition. Clamp/quantize only at a documented boundary and expose clipped values.

Start with one blend operation and a sphere. Add mute, solo, reorder, duplicate,
group selection, and a readout before adding a large effects catalog. A user must
be able to explain an unexpected color without inspecting generated node trees.

## Masks

| Capability | Required behavior | Stage |
| --- | --- | --- |
| Sphere | Inside/outside and feathered boundary in an explicit space | M2 |
| Plane, box, cylinder | Transformed primitive fields; controlled extent and inversion | M8 |
| Closed mesh | Evaluated geometry, membership definition, transform support, invalid-mesh diagnosis | M8 |
| Curve proximity | Distance/falloff around a curve with defined sampling error | M8 |
| Combined masks | Union/intersection/subtraction or defined field composition | M8 |
| Group/attribute mask | Combine spatial influence with stable group membership | M4/M8 |
| Debug display | Boundary guides, membership/weight view, selected-drone explanation | Begin M2 |

Specify local versus world distances, the effect of nonuniform/negative scale,
boundary tolerance, and what happens to self-intersecting, open, or degenerate
meshes. A distance to the nearest surface is not by itself an inside/outside test.
Do not describe a transformed approximate distance as an exact world-space distance.

Render visibility and evaluation visibility are separate. Hiding a mask must not
remove it from the data needed to evaluate the effect. Test masks with animated
parents and modifiers, deletion, replacement, and save/reload.

## Color and media sources

Expand from solid colors to ramps, spatial gradients, time gradients, waves,
chases, noise/sparkles, and image/video projection. Each has a stated coordinate
mapping, repeat/wrap/clamp behavior, filtering, time offset, and missing-media rule.

For video, record media frame rate, show-time mapping, seeking, interpolation, and
color conversion. For flicker and flashes, show what the selected LED output rate
can represent. Sampling a fast effect too slowly can change the pattern; exporters
must report that loss instead of silently suggesting faithful playback.

Reusable effects must include or resolve the referenced masks, images, ramps,
clips, and profile versions. “Export preset” cannot mean only copying object names
and hoping the receiving file contains the same objects.

## Timing and editing

Effects can use absolute show time or an offset relative to a cue. Moving a cue
moves attached effects. Stretching a cue, changing tempo, and repeating an effect
are distinct operations with explicit rules. Preview the consequences and support
undo. Mask animation and effect timing must stay intelligible when both are retimed.

Begin with named markers and manual music cues. Add tempo maps, waveform support,
reusable clips, and optional beat detection later. Automatic beat detection is a
suggestion the designer can edit. The audio start offset belongs to the show data
and must be preserved in review exports.

Manual color keys remain useful for local adjustments. Define their priority
relative to procedural effects, and make baking reversible. Baking records its
source revision and sample rate; it must not silently destroy the editable stack.

## LED signal and visual appearance

Keep three related values distinguishable:

1. The artistic color/intensity requested by the light program.
2. The device channels after fleet-specific calibration, limits, and encoding.
3. The appearance rendered by Blender through light geometry, camera, atmosphere,
   exposure, glare, and a display transform.

Offer an inspection mode for channels and a presentation mode for the camera.
Changing a view transform or glow strength affects presentation only. Source-image
decoding and LED encoding must not apply gamma twice. RGBW mapping needs an
explicit white-emitter assumption and a declared policy when the target only
supports RGB.

For realistic previews, model the visible emitter's apparent size, directionality,
intensity/color response, distance, and camera exposure. Bloom/glare alone is not a
calibrated LED model. Use measured fleet data where available and mark estimated
parameters. Protect saturated color readability while acknowledging highlight
rolloff in the chosen view transform. See [Blender's view-transform reference](https://docs.blender.org/manual/en/5.2/render/color_management/displays_views.html).

## Preview commands

**Preview frame** uses the chosen audience camera and current show time. **Preview
range** and **Preview full show** use the same evaluation and offer a draft/final
quality choice, resolution, frame range, audio offset, and destination. A render
queue can later cover several cameras and delivery aspect ratios.

The initial implementation should create a separate owned preview scene or an
equally reversible setup. It must preserve user cameras, world, compositor,
materials, color management, frame, selection, and render settings. Re-running
setup updates its own data without accumulating duplicate nodes or collections.

Provide a useful camera, ground/context, sky, and emission/glare preset first.
Later add imported site scenery, atmospheric conditions, lens/exposure controls,
EEVEE draft and Cycles final options, and documented quality/performance tradeoffs.
Separate the technical overview camera from the audience/marketing camera.

Render to an image sequence for resumable long jobs. Video delivery should state
codec availability, frame rate, resolution, color settings, and audio timing.
Headless jobs must use the same scene/evaluator contract. Cancellation and failed
frames leave recoverable output and restore editor state.

Every deliverable records the show revision, camera, render profile, software
versions, and whether physical appearance is calibrated or estimated. An old
approved image must not appear to describe a newer show revision.

## Acceptance cases

| Case | Evidence |
| --- | --- |
| Mask sweep | Hand-predicted inside/outside/boundary colors agree with samples |
| Scale and parenting | Rotated, translated, scaled, and animated masks follow the stated space contract |
| Overlapping effects | Reordering layers changes output exactly as the defined blend rules predict |
| Arbitrary time | Direct seek, reverse scrub, and sequential playback agree |
| Hidden helpers | Guides remain evaluable but never appear in final output |
| Retiming | Moving/stretching a cue updates attached effects and audio relationships correctly |
| Media | Missing files, changed contents, video seeks, and source color spaces are diagnosed |
| Persistence | Reopen and asset relocation reproduce the same effects and sampled channels |
| Preview isolation | Existing scene/compositor survives setup, rendering, cancellation, and cleanup |
| Render agreement | A sampled LED buffer agrees with the one used to drive the rendered revision |
| Display independence | Exposure/view/glare edits leave exported LED channels unchanged |
| Device limits | RGBW conversion, clipping, brightness limits, and output-rate losses are visible |
| Batch rendering | Out-of-order frames and resumed jobs preserve revision and timing |

Compare numeric buffers exactly or with stated tolerances. Use image comparisons
with tolerances appropriate to the renderer/GPU, plus visual review; a pixel-perfect
image hash across every device is not a sensible universal release requirement.
