# Choose the print set

[← Project](../README.md) · [Build the STLs](development.md)

All files are in millimetres. Use 100% scale. The Python exporter places the STLs in the intended print orientations. The chassis was designed around a Prusa XL; always check the slicer footprint and fit on your actual machine.

Run `python tools/export_prints.py` to create **34 STLs** across the current build and retained alternatives. It is not an instruction to print all 34 indiscriminately.

| Folder | Files | Selection / orientation |
|---|---:|---|
| `build/print/chassis` | 4 | Main quadrants; sidewall on the bed. Read the two chassis fit bugs before reprinting. |
| `build/print/connectors` | 7 | Four underside bridges and three upper straps; broad mounting face on the bed. |
| `build/print/ducts` | 3 | Pair A + Pair B ducts, **fan face down**; new retaining bar, **underside down**. |
| `build/print/lid` | 4 | All panels flat, ribs/IDs up. |
| `build/print/cradles-and-shim` | 15 | Fourteen original support parts plus one optional 2 mm shim. Retain only what seats naturally under your fitted ducts. |
| `build/print/legacy-carrier` | 1 | Older full-height carrier, replaced by Step 22 for this build; generated only as an alternative/reference. |

## Material and orientation

Use PETG with your established profile. The major parts were designed around avoiding generated support in their specified orientations; this does not replace the slicer preview. The duct bodies have short foot bridges, and thin walls, bores, and first-layer lips still need inspection.

For the small Step 22 bar, 0.20 mm layers, four perimeters, five top/bottom layers, and 40% infill are a starting profile. Its footprint is 240 × 19 mm and height 24 mm; a brim can help the long narrow base. This profile is a starting point, not a tested structural rating.

The lid panels are at most 226.10 × 295.95 × 5 mm. Keep them flat, with the 4 mm skin and 1 mm ribs intact. Do not scale them to compensate for warping.

## Preserve the printed baseline

The files here retain the known rear GPU-bracket and PSU screw-seat issues. The exporter does not silently correct either chassis defect. Future fixes should get new revisioned filenames and physical fit notes.

The front-left Step 16 quadrant adds the six floor insert pockets. The other three quadrants and all seven chassis connectors remain compatible with Step 15.
