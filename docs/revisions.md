# Revision and fit history

## X10DRG-Q / RTX 8000 variant — R02, 25 October 2026

The owner confirmed a Bambu P1S, no PSU selection and an unpurchased
X10DRG-Q. R02 gives each passive card a dedicated 120mm fan and divides
its duct into two fitted sections with a removable split collar. The upper
route rises at approximately 44.7 degrees over the middle transition.
All 12 duct/collar pieces per variant fit the configured P1S envelope with
a 5mm brim reservation and the normal cutter exclusion.

The 634.2mm candidate has no modeled component intersections; the 584.2mm
layout retains three PSU/duct clashes. PSU body/cable-zone sensitivity is
reported explicitly. A four-piece short joint sample is cropped from the
actual mating solids for the first physical fit test. Its 0.3mm-per-side
clearance and M3x16 friction collar still need print/fit/seal/pull testing.

Source, STEP, actual CAD views, saved-mesh reports and 13 regression tests
are supplied. Original upstream and R01 geometry remain unchanged. This
is a fit-prototype milestone, not a full enclosure or thermal/structural
release. See [R02 assembly and checks](x10drg-q-r02.md),
[P1S constraints](p1s-printing.md) and [PSU/cable options](x10drg-q-psu-options.md).

## X10DRG-Q / RTX 8000 variant — R01, 25 October 2026

The Dillflix fork starts a separate parametric layout study for the X10DRG-Q,
four RTX 8000 cards (three passive, one blower), two NVLink pairs and two ATX
PSUs. This revision adds the design plan, measurement requirements, generator,
actual CAD views and machine-readable geometry reports. Published upstream
STEP solids and the original 34-part print set are unchanged.

Two separate 30 × 30 × 5mm PSU screw-seat coupons compare a proposed 2mm
local land with the original 5mm wall. STEP, regenerated on-bed STL, CAD
views and mesh checks are provided; actual screw fit is pending.

R01 is not a manufacturing release. The motherboard outline sources disagree
by approximately 2mm along the rear edge; mounting-hole and absolute slot/I/O
coordinates are not dimensioned in the available documentation. Provisional
envelopes must not be used as drilling templates. Both upstream physical fit
issues remain open. See the [variant plan](x10drg-q-plan.md).

## Upstream baseline

| Design step | What is included | Status |
|---|---|---|
| Step 15 / 16 chassis | Four quadrants, seven connectors, five rod channels, lid mounts; Step 16 front-left adds six floor inserts | Printed baseline. Rear GPU top-flange and PSU screw-seat bugs remain open. |
| Step 20 ducts | Two paired rigid ducts with exposed mounting-corner recesses; original adjustable supports and full carrier | Printed geometry. Builder reported awkward mount installation/fit. |
| Step 21 lid | Four overlapping panels on the existing eight rim mounts | CAD/mesh checks saved; nominal total height 265.35 mm. Physical fit not reported here. |
| Step 22 bar | Low retaining bar, fan intake faces 10 mm behind front inserts | CAD/mesh and nominal hardware/access checks saved. Physical fit pending. |
| Repository publication, 23 October 2026 | Current Markdown instructions, CAD views, source wrapper, and two GitHub bugs | Documentation/package change only; no production geometry edited. |

## Source publication, 25 October 2026

Per the builder's request, prebuilt STLs and ZIPs are omitted from Git. The Python exporter regenerates all 34 print files from the preserved STEP solids, including the optional shim. The duct pipeline no longer depends on a copied STL. The early chassis construction script is unavailable; its saved STEP assembly is included unchanged. No fit bugs were fixed by this packaging change.

## As-built rod change

The builder's rods are longer than the original 406.4 mm stock. Only the front/rear crosswise rods and both longitudinal rods are used. The middle crosswise channel stays empty. Earlier illustrations may show all five reference rods; those do not describe the current four-rod assembly.

## Open physical fit bugs

1. [Rear GPU bracket top flanges need more rearward clearance](https://github.com/PraxisOG/moe-chassis/issues/1). Measure the interference before setting a new clearance dimension.
2. [PSU screw-bearing lands should be approximately 2 mm](https://github.com/PraxisOG/moe-chassis/issues/2). Current thick seats do not allow the standard screws to retain the supplies adequately.

These issues request future changes. The original printed chassis remains available unchanged for traceability and compatibility. A closed CAD-intersection check does not resolve either physical defect.
