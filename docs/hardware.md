# Hardware and fasteners

[← Project](../README.md) · [Assembly](assembly.md)

M3 is used for the printed structure, board, duct supports, and lid. **PSU screws are #6-32 UNC.** Chassis fan-frame screws are a separate selection from the M3 duct through-bolts.

Unless a row says otherwise: washers are 0.5 mm thick and ≤7 mm OD; M3 nuts are 5.5 mm across flats × 2.4 mm high. Socket heads must fit the printed recesses (Ø5.5 × 3 mm for ducts/lid; ≤6 × 3 mm in the structural allowance).

## Chassis and lid

| Connection | Screws | Nuts | Washers |
|---|---|---:|---:|
| Four underside bridges | 8 × M3×14 | 8 | 16 |
| Three upper straps | 6 × M3×12 | 6 | 12 |
| Two longitudinal rod stops, if clear of longer rods | 2 × M3×18 | 2 | 4 |
| Motherboard | 9 × M3×5 starting selection; confirm PCB stack | — | As fitted |
| Rear GPU retention | M3×5 starting selection; count depends on actual brackets | — | As fitted |
| Four lid panels | 8 × M3×6 | — | 8 |
| Two PSUs | 8 × manufacturer-approved #6-32 screws; **open fit issue #2** | — | Per PSU specification |
| Six front + one rear chassis fan | 28 appropriate fan-frame screws | — | Per fan specification |

**Four steel rods:** Ø4 mm, front/rear crosswise plus both longitudinal. This build's stock is longer than the original 406.4 mm design stock. Check actual fit; leave the middle crosswise channel empty. The original five channels remain in the CAD.

## Heatserts

| Location | Count |
|---|---:|
| Motherboard standoffs | 9 |
| Rear card-retention ledge | 8 |
| Lid rim | 8 |
| Front-left floor | 6 |
| **Chassis total** | **31** |
| Original adjustable support sliders, if used | 8 |
| Original adjustable support saddles, if used | 4 |

Modeled insert: **ruthex RX-M3Sx4.0**, M3 thread, 4 mm long. Pocket: Ø4 × 5.2 mm blind with a small lead-in. Install flush. Existing fitted inserts count toward these totals. The Step 22 bar adds no heatserts.

## Step 22 bar and one fan stage

| Connection | Screws / bolts | Nuts | Washers |
|---|---|---:|---:|
| Bar feet to floor | 2 × M3×8 | — | 2 |
| Four captured lower fan corners | 4 × M3×45 | 4 | 8 |
| Remaining fan corners, old carrier removed | 12 × M3×40 | 12 | 24 |

These fan lengths assume one nominal 25 mm fan stage and 6 mm existing duct seats. Verify actual stack thickness. The old tall carrier used M3×55; removing it makes those bolts potentially too long.

## Original adjustable supports, only where retained

| Connection | Screws | Nuts | Washers |
|---|---|---:|---:|
| Two base rails to floor | 4 × M3×6 | — | 4 |
| Four sliders to base tracks | 8 × M3×10 | 8 | 8 |
| Four 10 mm riser/saddle stacks | 8 × M3×16 | — | 8 |
| Four duct ears to saddles | 4 × M3×8 | — | 4 |

For a deliberately changed riser stack, screw length was modeled as **total riser thickness + 6 mm**. Do not add the optional 2 mm shim blindly; the rigid duct/fan geometry and GPU seating still control alignment.
