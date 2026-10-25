MOE - STEP 21 LID / REVISION 25
5 October 2026. Four new lid panels for the existing Step16 / compatible Step15 rim mounts.

HEIGHT AND DIMENSIONS
Nominal 6U envelope: 266.70 mm (10.50 in).
Existing chassis height: 260.35 mm (10.25 in).
Lid skin: 4.00 mm; ribs above the skin: 1.00 mm.
Lid/body maximum: 265.35 mm (10.44685 in).
Specified screw heads: 265.05 mm maximum.
Complete modeled assembly maximum: 265.35 mm.
Margin below nominal 6U: 1.35 mm (0.05315 in).
Width/depth remain 444.50 x 584.20 mm (17.5 x 23 in).
The flat underside sits on the existing rim at Z260.35; nothing projects down into the fan space.
Nominal clearance to the existing 240 mm front/duct fan envelopes stays 1.30 mm.

PRINT THESE FOUR FILES, ONCE EACH
Lid21_REAR_RIGHT_Print.stl   (RR)  226.10 x 295.95 x 5.00 mm
Lid21_REAR_LEFT_Print.stl    (RL)  222.10 x 295.95 x 5.00 mm
Lid21_FRONT_RIGHT_Print.stl  (FR)  226.10 x 291.95 x 5.00 mm
Lid21_FRONT_LEFT_Print.stl   (FL)  222.10 x 291.95 x 5.00 mm
All STLs are in millimetres, already flat on the bed, ribs and engraved IDs up.
Use PETG and your established profile. Support material is not intended; the inclined seams are 45 degrees.
Use a brim if needed to keep these broad panels flat. Do not scale to fit; all four fit a 350 mm Prusa XL bed.
The lid is a cover, not a load-bearing shelf. Do not stack equipment on it.

HARDWARE
8 x M3 x 6 mm socket-head cap screws (length below head).
8 x M3 washers, 0.50 mm thick, outside diameter no more than 7.00 mm.
Use the eight existing M3 rim heatsets, installed FLUSH with the rim.
Required screw envelope: head no more than 5.50 mm diameter x 3.00 mm high.
No new heatsets, nuts, glue or chassis modifications are required.
Each hole is 3.40 mm through with an 8.00 mm diameter, 2.80 mm deep counterbore.
The counterbore leaves a 1.20 mm bearing skin over the existing boss.
With the specified washer, a 6 mm screw penetrates 4.30 mm below the insert top and has 0.90 mm nominal clearance above the blind pocket bottom.
Do not substitute M3 x 8: it would exceed the modeled blind-pocket depth.

INSTALLATION
Left/right are named standing at the chassis front, looking toward the rear.
1. Check the eight rim inserts are flush and that the rim and lid undersides are free of debris.
2. Lower RR (rear-right) onto the rim first. Loosely start its two screws, with a washer beneath each head inside the counterbore.
3. Lower RL (rear-left), then FR (front-right), then FL (front-left). The 45-degree inclined overlap edges must settle naturally. All panels install from above.
4. Start all eight screws before snugging them. Each panel uses the two inserts on its outer sidewall. The modeled seam clearance is 0.30 mm; do not pull or crush seams closed with the screws.
5. Snug by hand without dimpling the counterbore lands. The lid must rest on the rim, not on fans, the cooler or wiring. Check fan rotors still turn freely.
6. Check the finished height and straightness with the lid fitted. Nominal 1.35 mm headroom is small enough that warping, proud inserts or extra washers matter.
To remove: undo the relevant screws and lift panels in reverse order, FL then FR then RL then RR.

MOUNT COORDINATES (MM, EXISTING CHASSIS DATUM)
X is measured from the right exterior; Y from the rear exterior; Z is height above the chassis underside.
RR: X7.50 at Y65 and Y185.
RL: X437.00 at Y65 and Y185.
FR: X7.50 at Y320 and Y530.
FL: X437.00 at Y320 and Y530.
The top seams are at X222.25 and Y292.10. Their inclined faces shift 4 mm across the skin thickness.

VERIFIED IN CAD
Four valid single solids; four closed, consistently wound STL meshes.
No nominal panel-panel or panel-chassis volume intersections.
Sampled vertical installation paths are clear in the stated order.
Eight screw/washer stacks clear the lid and existing bosses; screw-driver access is clear.
Lid clears the current Step20 duct parts, both duct-fan-stage reference envelopes, front fan frames and upper PSU envelope.
The underside never goes below the original rim. Downward print surfaces pass a 45-degree overhang screen, excluding the first layer.
The existing chassis STEP is unchanged, including the user's four-rod build and previously reported PCIe bracket clearance issue.

PRACTICAL LIMITS
The height calculation starts at the chassis underside; separate rack-shelf thickness, feet or padding are not included. Check actual usable rack space.
Actual print warp, heat-related sag, hardware tolerances, unmodeled wiring/CPU cooler and physical fan clearance still need checking. The cover is not airtight or load-rated.

FILES
Print ZIP: the four STL panels, this guide, dimension/check reports and the isometric render.
MOE_Lid_Step21.step: the four lid panels in assembly coordinates.
MOE_Chassis_With_Lid_Step21.step: existing chassis, lid and reference screw/washer envelopes; hardware reference bodies are not print parts.
Project ZIP: both assembled STEP files, individual STEP/STL files, source scripts and original reference geometry needed to rebuild/check.

SOURCES
Existing Step16 chassis and Step20 duct CAD; Rev24 project dimensions.
Rack height reference: Hammond PBPA series, 6U = 10.50 in:
https://www.hammfg.com/dci/products/accessories/pbpa
M3 DIN 912 / ISO 4762 head-envelope reference (5.5 mm diameter, 3 mm high; select 6 mm length for this lid):
https://accu-components.com/us/metric-cap-head-screws/156805-SSC-M3-55-A4-BL
