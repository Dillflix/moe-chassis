# Bambu P1S printing constraints

[Project](../README.md) · [Measurement worksheet](x10drg-q-measurements.md) · [Development](development.md)

The owner has confirmed a **Bambu P1S**. Use its normal printer profile, including the filament-cutter exclusion, when checking the new chassis parts. A CAD envelope check establishes a possible placement; it does not establish a successful slice, print, hardware fit or operating-temperature rating.

## Verified printer profile

Bambu advertises a **256 × 256 × 256mm** build volume. Its product-page footnote specifies a **250mm default printable height** in Bambu Studio and identifies the cutter stopper as an obstruction to part of the bed. This project does not rely on unlocking the extra height or disabling the cutter exclusion.

The official Bambu Studio profiles were checked on **2026-10-25**. For the **P1S with a 0.4mm nozzle**, the inheritance chain resolves as follows:

| Profile | Relevant value |
|---|---|
| `Bambu Lab P1S 0.4 nozzle.json` | Inherits `fdm_bbl_3dp_001_common`; overrides `bed_exclude_area` with `(0,0), (18,0), (18,28), (0,28)` |
| `fdm_bbl_3dp_001_common.json` | Inherits `fdm_machine_common`; sets the bed polygon to `(0,0), (256,0), (256,256), (0,256)` |
| `fdm_machine_common.json` | Sets `printable_height` to `250` |

The P1S override is the applicable exclusion: the **18 × 28mm front-left corner**, in the slicer's bed coordinates. Do not add the larger exclusion from the inherited common profile as a second P1S exclusion. These slicer coordinates are separate from the chassis assembly's coordinate convention.

The linked profiles follow Bambu's `master` branch and may change. Check the installed printer/nozzle profile before slicing, especially if the nozzle, machine preset or startup sequence differs from this reference.

## Conservative part envelope and placement

Use **220 × 220 × 240mm** as the conservative maximum envelope for an individual oriented part. Reserve **5mm on every side in X/Y** for a brim. This is a project design allowance, not a smaller manufacturer specification.

For the largest square part, one explicit placement is:

| Envelope | Slicer X range | Slicer Y range | Slicer Z range |
|---|---:|---:|---:|
| Part body | 27–247mm | 18–238mm | 0–240mm |
| Body plus 5mm brim reservation | 22–252mm | 13–243mm | — |

That footprint clears the cutter exclusion by **4mm in X**, stays **4mm inside the right bed edge**, and has **13mm front/rear margins**. The 240mm body height leaves 10mm below the default height limit. The brim reservation must include any brim-to-object gap; if the selected gap, supports or other generated features extend farther than the allowance, check their actual sliced envelope instead.

A blanket **230 × 230mm part plus a 5mm brim does not pass this check**. Its 240 × 240mm footprint has only 16mm of translational room on a 256mm bed. An axis-aligned placement therefore cannot move completely past either the 18mm-wide or 28mm-deep excluded corner. A smaller part or a measured shape-specific placement may fit, but the larger square is not a valid general allowance.

Longer narrow parts can still fit. For example, a **220 × 230mm body** oriented with its 220mm side along slicer X can use body ranges **X27–247, Y13–243mm**. Its 5mm brim reservation occupies **X22–252, Y8–248mm**. Check each part's actual orientation and footprint rather than treating 220mm as the printer's absolute limit.

## Before printing a generated part

1. Import the oriented STL in millimetres at **100% scale**. A mesh normalized to the origin does not encode the bed placement above; position it in Bambu Studio and verify the result.
2. Use one part per plate for this placement check, with normal layer-by-layer printing. Sequential printing and multiple-part packing require their own toolhead-clearance checks.
3. Slice with the actual material, plate, nozzle, brim and support settings. Inspect the cutter corner, bed edges, generated supports, thin walls, joint features and any unsupported internal surfaces. Keep the standard machine exclusion enabled.
4. Print the mating-joint or screw-seat sample first. Record material, orientation and measured clearance before printing the full duct segments.

The exported mesh and CAD checks do not substitute for a slicer preview. A footprint pass does not assess overhangs, warping, seam strength, joint retention or airflow leakage.

## Prototype material and operating use

**PETG can be used for fit prototypes and joint coupons** to assess assembly, screw access and the chosen clearances. Record the actual filament and print settings. A successful PETG fit print is not evidence that the same part can support hardware or retain its shape in the running server.

Final material selection remains open. It depends on the measured temperatures at the ducts and mounts, sustained mechanical loads, joint behavior and the selected material's documented properties. Validate the chosen material and printed geometry under the intended operating conditions before treating them as final enclosure parts. No final material or temperature rating is established by this revision.

## Primary sources

- [Bambu P1S Canadian product specifications and print-volume footnotes](https://ca.store.bambulab.com/products/p1s?variant=44863489409264)
- [Official P1S 0.4mm machine profile](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/machine/Bambu%20Lab%20P1S%200.4%20nozzle.json)
- [Official inherited Bambu common machine profile](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/machine/fdm_bbl_3dp_001_common.json)
- [Official base machine profile](https://github.com/bambulab/BambuStudio/blob/master/resources/profiles/BBL/machine/fdm_machine_common.json)
