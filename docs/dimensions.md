# Dimensions and datums

[← Project](../README.md)

Dimensions below come from the saved CAD and build notes. Values are nominal, not a report of measured print accuracy.

| Feature | mm |
|---|---|
| Overall chassis W × D × H | 444.50 × 584.20 × 260.35 |
| Base / wall rise / ordinary wall | 19.05 / 241.30 / 5.00 |
| Clear ordinary interior W × D | 434.50 × 574.20 |
| Lid skin / upper ribs | 4.00 / 1.00 |
| Closed maximum height / nominal 6U | 265.35 / 266.70 |
| Motherboard reference PCB | 304.80 × 266.70 × 1.57 |
| Motherboard standoff rise | 6.35 above floor |
| I/O shield opening / mounting edge | 158.75 × 44.45 / 1.20 |
| Common rear PCIe opening | 162.56 × 111.64; eight positions at 20.32 pitch |
| Lower bracket-tab channel | 162.56 long × 3.60 fore-aft; floor Z14.46 |
| Front fan array | 360 wide × 240 tall; six 120 mm positions |
| Chassis fan openings / screw pitch | Ø115 / 105 × 105 |
| Chassis fan screw-bearing thickness | 2.00 |
| PSU reference body, each | 125 inward × 150 fore-aft × 86 high |
| PSU exhaust-face recess | 38.10 from right exterior |
| Opposed PSU intake gap | 59.30 nominal in the central opening |
| Current PSU screw-panel thickness | 5.00; requested future local screw lands approximately 2.00 |
| Rod / channel diameter | 4.00 / 4.30 |

## Coordinates

The origin is the chassis **rear-right-bottom corner** when standing at the front looking toward the rear. **+X points left, +Y points toward the front, +Z points up.** Floor top is Z19.05; rim is Z260.35.

| Datum | Coordinates in mm |
|---|---|
| Six duct-support floor inserts | X260 and X400, each at Y350 / 430 / 520 |
| Front intake centers | X139.5 / 259.5 / 379.5; Z79.05 / 199.05 |
| Duct fan centers | X252 / 372; Z79.05 / 199.05 |
| Step 22 duct-fan intake faces | Y510; 10 mm behind the Y520 insert centers |
| Lid RR screws | X7.5, Y65 / 185 |
| Lid RL screws | X437, Y65 / 185 |
| Lid FR screws | X7.5, Y320 / 530 |
| Lid FL screws | X437, Y320 / 530 |

The Step 22 context uses one nominal 25 mm fan stage and translates the older duct reference 5 mm forward to meet the reported fan-face position. It is an illustration of the clarified datum, not an instruction to move already-fitted ducts or GPUs.

For full lid/bar calculations see [`docs/reference`](reference); exact saved checks are in [`checks`](../checks). The chassis STEP is the baseline for geometry not listed here.

Rack-height reference: [Hammond PBPA, 6U = 10.50 inches](https://www.hammfg.com/dci/products/accessories/pbpa). Separate rack support, feet, and padding are not included in the modeled enclosure height.
