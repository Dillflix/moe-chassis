# Step 20 rounded fan mounting corners

Revision 24 replaces the two Step19 main duct prints with rounded corner recesses. All other Step19 parts are retained. The following Step19 construction and assembly details remain applicable. The Step16 chassis, bases, sliders, 10 mm risers and fan carrier are unchanged. Use this complete current print set to avoid mixing superseded parts.

Two rigid paired modules provide four isolated GPU passages. The fan adapters are now integral with the main ducts. There are no TPU couplers, internal mounting screws or upper screwdriver holes. Each module attaches through two external ears in the open gap between its two passages; four M3×8 socket screws and four 0.5 mm washers enter the saddle heatsets from above. The screw holes through the ears are 5 mm diagonal diamonds for sideways printing; these are mounting holes outside the air passages, not ventilation holes.

## Rounded fan corners

Sixteen R5 rounded recesses expose the four mounting corners of each fan. Holes are Ø3.4 on the retained105×105 pattern. Each screw seat is6 mm thick, at Y474 behind the fan face at Y480. Approximately2 mm of radial wall material separates each recess from its adjacent passage; tapered closed ends avoid support material. These mounts use the documented M3 through-bolts, washers and nuts, not short coarse-thread fan screws.

Assemble the fans to the ducts before installing the modules in the chassis. Insert the long M3 bolts from the fan intake side. Washers and nuts sit in the duct recesses; hold the nuts with a5.5 mm nut driver through the corner relief. The nominal axial tool clearance isØ8. All16 washer seats and nut/driver envelopes were checked in CAD. Hardware assumptions remain head Ø5.5×3,washer Ø7×0.5.

## Interface trim and print orientation

The old GPU screw flange and material extending beyond the supported rear-wall footprint are trimmed away. This removes the old GPU mounting holes. The stepped outlet shape, 40.64 mm card pitch and nose material supported by the walls behind it remain. The removed material is supplied as a reference STEP and highlighted in red in the trim render. Actual fit at the cards remains to be checked.

Print both paired modules with the fan mounting face flat on the bed and the GPU interfaces at the top. The supplied STLs already have this orientation and minimum Z=0. Nominal print height is219 mm. A 2 mm central strip reaches the fan mounting face so the divider starts on the bed rather than bridging an entire fan aperture. It is stationary duct material at the frame face; check clearance to the actual fan rotor before powering up.

The integral fan transition runs Y445–478 (33 mm), replacing the short steep adapter and coupler gap. Sloping attachment feet have 4.10 mm runs for 4.05 mm rise. A CAD surface-normal check rejects downward-facing duct surfaces steeper than45 degrees from the build direction, except the first-layer fan face. Small cross-bridges between passages remain at the external support feet, approximately9–13 mm across. This geometry is intended for printing without generated support; bridge quality and first-layer adhesion still depend on the PETG profile. The STL set includes the unchanged supports and carrier in their separate print orientations.

## Fixed fit and support adjustment

The rigid module holds the existing nominal interface and fan datums. The 2×2 fan bank stays at X252/372 and Z79.05/199.05. Stage1 occupies Y480–505; the 20 mm carrier occupies505–525; optional stage2 occupies525–550. Existing front-fan reference starts554.2, leaving4.2 mm between frames with stage2 installed.

The support slots and risers allow the cradles to seat beneath the rigid ducts. Once the fan bank is fixed, they do not provide independent movement of the GPU outlets. If physical alignment differs, change the CAD offset/height and reprint the affected module as requested. Do not use mounting screws to force a rigid duct into the cards. No GPU attachment screws are used.

## Hardware

| Location | Required hardware |
|---|---|
| Bases to floor | 4 M3×6 socket screws +4 washers |
| Lateral clamps | 8 M3×10 socket screws +8 washers +8 M3 nuts |
| Nominal 10 mm risers | 8 M3×16 socket screws +8 washers |
| External duct ears | 4 M3×8 socket screws +4 washers |
| Carrier to floor | 2 M3×8 socket screws +2 washers |
| One duct fan stage | 16 M3×55 +32 washers +16 nuts |
| Two duct fan stages | Substitute16 M3×80; same washers and nuts |
| New heatsets | 12 RX-M3Sx4.0:8 in sliders,4 in revised saddles |

Hardware assumptions: M3 nuts5.5 AF×2.4; washers0.5 thick,OD≤7; socket headsØ≤5.5×3. The four external M3×8 screws engage the saddle inserts by approximately3.45 mm. Do not reuse the previous countersunk M3×10 duct screws. Existing six floor heatsets are reused. The optional2 mm shim replaces the nominal10 mm riser when needed; riser screw length remains total riser thickness +6 mm.

## Assembly

1. Install the twelve heatsets. Put the eight side-loading nuts in the base tracks, then loosely fit bases, sliders, risers and revised saddles.
2. Set the rigid duct modules on the saddles. Insert the four M3×8 screws and washers directly through the external ears between the passages. No tool passes through an air passage.
3. Attach the carrier and fan stack with airflow toward the GPUs. Check alignment against the actual cards before tightening. Adjust support position to obtain even seating; revise the rigid model if outlet alignment differs.
4. Check rotor, lid, power-plug and front-fan clearance. With bolts inserted from the fan intake side, the second-stage screw heads have only0.7 mm nominal clearance to the front fan reference with the specified hardware.

Seventeen nominal PETG parts are included:2 ducts,2 bases,4 sliders,4 risers,4 saddles and1 carrier. The optional2 mm shim makes18 supplied meshes. No TPU parts are needed. Fan envelopes and removed-interface material are references, not print parts. The project archive contains assembled STEP, individual STEP and STLs, sources, checks, renders and updated dimensions. Cooling and physical fit remain untested. Stop here for review.

## Rebuilding

Place the Python sources, reference STEP inputs and the optional Step18 shim STL together in one working directory. Run trim_interface19.py, ducts_step20.py, finish_ducts19.py, check_ducts19_meshes.py, check_print20.py, then render_ducts19.py using Python with CadQuery/OCP, NumPy and Pillow. The document updater also requires python-docx and the included Rev23 document backup.
