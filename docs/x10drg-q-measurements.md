# X10DRG-Q measurement worksheet — R01

[Adaptation plan](x10drg-q-plan.md) · [Project](../README.md) · [Upstream datums](dimensions.md)

**Purpose:** replace the concept's bounding boxes and provisional positions with traceable physical interfaces before producing mounting parts. Blank cells mean **unknown**, not zero. The initial model is a layout study; do not drill, install standoffs or print a full enclosure from its assumed coordinates.

Record dimensions in **millimetres**, preferably with calipers for mounting features. For each result, record the part identifier, measuring tool, estimated uncertainty and a photograph or drawing reference. Do not convert a perspective photograph into final hole coordinates. Measurements taken with a ruler are useful for envelopes but may be insufficient for screw alignment.

## Datums and conventions

The chassis origin is its rear-right-bottom corner when viewed from the front. **+X is left, +Y is front, +Z is up**; the upstream floor top is **Z19.05**.

For each physical component, choose and photograph a local origin and axis direction before measuring. Record its transformation into chassis coordinates separately. For the motherboard, identify the rear I/O edge and one physical PCB corner; use that same corner for all hole, slot and connector coordinates. The manufacturer's quoted width/depth alone does not establish this transformation.

| Record | Value |
|---|---|
| Measurement date / person | |
| Measuring tools and estimated uncertainty | |
| Board model / PCB revision / serial reference | |
| Board local origin and axis photograph | |
| Board-to-chassis orientation / transform | |
| GPU labels used throughout this worksheet | Passive A / Passive B / Passive C / Active D |
| Photo/drawing location | |

## Priority 1 — blocks final layout and mounting CAD

### Motherboard outline, holes and datums

The product page says **386.1 × 335.3mm**; a manual says **384.04 × 335.28mm**. The concept reserves the larger envelope. Resolve the discrepancy on the actual board before creating edge fits or hole patterns.

| Feature | Reference / why needed | Measured value | Uncertainty / evidence |
|---|---|---|---|
| PCB outline X extent | Resolve manufacturer dimension discrepancy | | |
| PCB outline Y extent | Resolve manufacturer dimension discrepancy | | |
| PCB thickness | Sets standoff, screw and rear-bracket stack | | |
| PCB corner radii / outline cutouts | Tray edge and mounting clearance | | |
| Underside tallest component below PCB | Minimum tray clearance | | |
| Rear I/O opening position, width and height | Locate opening relative to PCB datum | | |
| I/O shield lip/retention allowance | Confirm shield or custom opening | | |
| Chosen PCB-bottom height above floor | Design selection after underside measurement | | |

There are **14 motherboard mounting holes**. Assign H01–H14 consistently on an annotated top-down image; this numbering is a measurement convention, not Supermicro's hole numbering. **No hole coordinates are supplied or inferred here.**

| Hole | Local X | Local Y | Hole diameter | Available support/contact diameter | Nearby underside/component exclusion | Evidence |
|---|---:|---:|---:|---:|---|---|
| H01 | | | | | | |
| H02 | | | | | | |
| H03 | | | | | | |
| H04 | | | | | | |
| H05 | | | | | | |
| H06 | | | | | | |
| H07 | | | | | | |
| H08 | | | | | | |
| H09 | | | | | | |
| H10 | | | | | | |
| H11 | | | | | | |
| H12 | | | | | | |
| H13 | | | | | | |
| H14 | | | | | | |

Cross-check at least two long diagonal hole-to-hole distances against the coordinate table before generating the tray. Confirm the standoff top contacts only the intended mounting pads.

### GPU slots and rear retention

Slots **2/4 belong to CPU1** and **6/8 to CPU2**. Their nominal adjacent-GPU center pitch is **40.64mm** (two PCIe positions). That relative pitch does **not** locate the four slots in the enclosure.

| Feature | Measured value | Uncertainty / evidence |
|---|---|---|
| Slot 2 card center plane from PCB local origin | | |
| Slot 4 card center plane from PCB local origin | | |
| Slot 6 card center plane from PCB local origin | | |
| Slot 8 card center plane from PCB local origin | | |
| PCIe connector seating datum height above PCB | | |
| PCIe connector/key position along the card | | |
| Installed bracket rear plane relative to PCB origin | | |
| Lower bracket tab width / thickness / protrusion | | |
| Bracket top flange overhang and screw-slot position | | |
| Space needed to insert/remove a card without bending its bracket | | |
| Screwdriver access with both NVLink bridges fitted | | |

The upstream GPU-flange interference remains open. Test the **actual bracket and top flange** in a small retention coupon before committing to a complete rear wall. Do not copy the upstream opening or assume adding an arbitrary relief resolves the defect.

### GPUs: measure each card, not one representative

| Feature | Passive A | Passive B | Passive C | Active D |
|---|---|---|---|---|
| Manufacturer / full part number / PCB or cooler revision | | | | |
| Overall length including bracket and protrusions | | | | |
| Maximum height above the installed PCIe seating datum | | | | |
| Maximum thickness including backplate and screw heads | | | | |
| Position of bracket exhaust/opening | | | | |
| NVLink connector location relative to card datum | | | | |
| Auxiliary power connector type / position / orientation | | | | |
| Mated plug protrusion and practical cable bend envelope | | | | |
| Passive inlet opening width × height and corner geometry | | | | N/A |
| Passive inlet opening position / accessible sealing land | | | | N/A |
| Heatsink through-flow direction confirmed from card construction | | | | N/A |
| Blower inlet diameter/shape and center | N/A | N/A | N/A | |
| Blower inlet unobstructed approach volume | N/A | N/A | N/A | |
| Safe support/contact surfaces clear of PCB components | | | | |

Record whether a duct can be removed without unplugging NVLink or removing the neighboring GPU. Keep any foam/gasket compression allowance explicit; it must not force a card away from its PCIe seating position.

### NVLink bridges

The required pairings are **2↔4** and **6↔8**. Two-slot bridge compatibility is a working assumption pending identification/measurement of both owned bridges. An `NV2` topology label describes active links, not bridge spacing.

| Feature | Bridge for slots 2↔4 | Bridge for slots 6↔8 |
|---|---|---|
| Manufacturer / part number / photograph | | |
| Connector center-to-center spacing | | |
| Body length × width × height | | |
| Top of body above installed GPU/PCB datum | | |
| Side overhang beyond card center planes | | |
| Clearance needed to fit/remove bridge | | |
| Fit confirmed with the intended passive/active card combination | | |

Create the final bridge keepout from the installed assembly, including any asymmetric body or latches. Do not scale a generic rectangular bridge representation into a clearance guarantee.

### Power supplies and cables

**Dual 850W is a candidate capacity, not a selected PSU model or approved electrical arrangement.** Power-connector inventories and physical dimensions can vary substantially between supplies with the same wattage.

| Feature | PSU A | PSU B |
|---|---|---|
| Manufacturer / exact model / hardware revision | | |
| Body width × height × depth | | |
| Intake/exhaust faces and required open volume | | |
| AC inlet / switch locations and external plug envelope | | |
| Mounting-hole pattern relative to chosen datum | | |
| Manufacturer screw type / permitted engagement | | |
| Modular connector face and connector positions | | |
| Mated modular plug protrusion / cable bend envelope | | |
| Available motherboard 24-pin / EPS / auxiliary leads | | |
| Available GPU leads and approved adapter details | | |

Before powered assembly, separately document PSU load allocation, each GPU's slot/auxiliary power sourcing, synchronization and shutdown/fault behavior. This worksheet supplies dimensional inputs only. It does not prescribe mains modifications or connector rewiring.

## Priority 2 — blocks cooling, lid and print segmentation

### CPU sockets, heatsinks, RAM and board connectors

The CPU silicon is reusable. The cooler mounting interface is a separate fit check: the target board has narrow ILM, while the ASUS factory cooler identification points to square ILM.

| Feature | CPU1 / bank 1 | CPU2 / bank 2 |
|---|---|---|
| Socket/CPU center in board coordinates | | |
| Cooler mounting-hole pattern measured | | |
| Actual cooler model and compatible mounting kit | | |
| Installed cooler overall width × depth × height | | |
| Fan inlet/exhaust direction and keepout | | |
| Screwdriver approach and installation sequence | | |
| Clearance to populated DIMMs and their latches | | |

For the eight-stick configuration, fill **A1/B1/C1/D1** and **E1/F1/G1/H1**, all with the P1/P2 prefixes printed on the motherboard. Record the **installed** DIMM height, not only Samsung's bare-module profile.

| Board service feature | Position/envelope to record | Measurement / evidence |
|---|---|---|
| 24-pin ATX, both 8-pin EPS and auxiliary 4-pin | Plug bodies, cable bends and removal access | |
| SATA, fan headers and any storage adapter | Connector/cable envelopes; access after GPUs fitted | |
| DIMM latches | Opening sweep and removal height | |
| IPMI/network/USB rear plugs | External cable bends and access | |
| Front-panel/reset/power connection | Connector and service access | |

### Fans, ducts and rack support

| Feature | Selection/measurement | Evidence |
|---|---|---|
| Fan model, width/height/depth, hole pitch | | |
| Fan performance curve and intended operating range | | |
| Duct-fan fastening stack and connector access | | |
| Gasket material, thickness and intended compression | | |
| Passive duct route length and minimum internal area | | |
| Blower inlet's independent fresh-air route | | |
| Rack shelf usable width/depth and load rating | | |
| Chassis support/contact locations on shelf | | |
| Rack front/rear clearance including plugs and lid service | | |
| Rack height available including shelf/feet/padding | | |

The concept's **634.20mm depth** is provisional. Check it against the actual rack shelf and cable clearances, not merely the rack's nominal outside depth. The original project used a shelf; rack ears and rail attachments are not established load paths for this revision.

### Printer and material

| Feature | Confirmed value |
|---|---|
| Printer manufacturer/model | |
| Usable X × Y × Z build volume, including toolhead restrictions | |
| Bed clips / purge / brim exclusion zones | |
| Nozzle size and intended layer height | |
| Intended filament/material and manufacturer | |
| Dimensional calibration / hole-fit coupon results | |
| Proposed section orientation and support constraints | |

The configurable **256mm** concept check is only a placeholder until this table is completed. The upstream main sections were designed for a Prusa XL; the user's printer is not yet known. Section limits must include brim/support allowances, not just the part's bounding box.

## Hardware stack worksheet

Complete this after the measured interface CAD exists. Existing upstream screw lengths do not automatically carry over when a wall, seat or mounting height changes.

| Joint | Materials and thicknesses in order | Fastener/thread | Required engagement | Bottoming allowance | Tool access | Physical result |
|---|---|---|---|---|---|---|
| Motherboard to standoff | | | | | | |
| Standoff/tray to chassis | | | | | | |
| GPU bracket retention | | | | | | |
| GPU non-PCB support | | | | | | |
| Passive duct to support | | | | | | |
| Duct fan to mount | | | | | | |
| PSU to screw-bearing land | | | | | | |
| Chassis section joint | | | | | | |
| Reinforcement retention | | | | | | |
| Lid attachment | | | | | | |

## Acceptance record

Keep **CAD checks**, **physical fit**, **electrical validation**, **thermal/acoustic testing** and **structural testing** as separate results. A green result in one column does not imply the others passed.

| Interface/test | CAD report/configuration | Physical test setup | Result and evidence | Remaining issue |
|---|---|---|---|---|
| 14-hole tray and board support | | | | |
| Four seated GPUs and bracket retention | | | | |
| Two installed NVLink bridges | | | | |
| Three passive duct seals and service access | | | | |
| Active blower inlet/exhaust clearance | | | | |
| PSU screw engagement and cable access | | | | |
| CPU/DIMM/VRM cooling access | | | | |
| Confirmed-printer part segmentation | | | | |
| GPU enumeration, PCIe links and NVLink topology | | | | |
| Simultaneous GPU thermal and clock stability | | | | |
| Enclosure/retention load and material creep | | | | |

Use the hardware references linked in the [adaptation plan](x10drg-q-plan.md) for nominal specifications. Retain measured evidence alongside the configuration that consumes it; do not replace unknown values with undocumented assumptions to make a CAD check pass.
