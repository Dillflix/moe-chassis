# X10DRG-Q adaptation plan — R01 / R02

[Project](../README.md) · [Measurement worksheet](x10drg-q-measurements.md) · [Upstream dimensions](dimensions.md) · [Revision history](revisions.md)

## Decision and release status

Adapt MOE's construction approach for a **Supermicro X10DRG-Q, four Quadro RTX 8000 cards, two NVLink pairs, three passive GPU coolers and one active blower cooler**. Preserve the upstream Step 15/16 chassis and Steps 20–22 unchanged. The X10DRG-Q work is a separate revision.

**R01 is a layout and duct concept, not a manufacturing release.** It uses bounding solids and explicit assumptions to explore fit. It does not contain a measured motherboard mounting pattern, validated GPU interfaces, a selected PSU installation or production-ready chassis sections. A successful CAD build does not establish electrical compatibility, physical fit, printed strength or cooling performance.

The user has selected the X10DRG-Q as the leading motherboard candidate and reports **C$35 shipping** for the examined offer. The user confirmed on 25 October 2026 that the board has **not been ordered**, the printer is a **Bambu P1S**, and **no PSUs are selected**. This plan assumes reuse of the existing CPUs, GPUs and RAM; it does not record a purchase.

## Requirements and decisions

| Requirement | Current decision | Evidence or remaining condition |
|---|---|---|
| Four double-width RTX 8000s | Direct motherboard mounting in slots **2, 4, 6 and 8** | Board supports four PCIe 3.0 ×16 connections; exact card envelope and bracket geometry still require measurement. |
| Two NVLink pairs | Pair slots **2↔4** and **6↔8** | Each pair remains connected to one CPU. Reserve bridge clearance; installed bridge spacing and body dimensions are unconfirmed. |
| Existing CPUs | Reuse **2× Xeon E5-2630L v4** | Board BIOS must be **2.0 or newer**. Both CPUs are needed for all four GPU slots. |
| Existing RAM | Prefer **8×32GB Samsung M392A4K40BM0-CRC**, **256GB** | One DIMM per channel, four per CPU. These CPUs limit operation to **2133 MT/s**, despite the DIMMs' 2400 rating. |
| Six-stick alternative | Keep 192GB possible, but design around eight sticks | Six sticks leave memory channels unpopulated. No six-stick population arrangement is prescribed by this concept. |
| CPU cooling | Plan for **narrow-ILM-compatible** coolers | The original ASUS factory cooler is identified as square ILM in the linked manufacturer material; confirm the actual installed heatsinks before attempting reuse. |
| Three passive GPUs | Three separate sealed outlet paths from a fan/plenum assembly | V620 duct outlet geometry is not reusable as an RTX 8000 interface without measurement. |
| One active GPU | Separate fresh-air access to its blower inlet and an unobstructed bracket exhaust | Keep the blower cooler fitted. Its inlet must not be enclosed inside a passive-card duct or blocked by a neighboring part. |
| Power supplies | Reserve **two ATX PSU envelopes**, each up to 160mm body depth, plus a provisional 30mm cable zone | No model selected. [Compact Canadian candidates and cable inventory](x10drg-q-psu-options.md); cable bends and final load allocation remain unverified. |
| Printer | **Bambu P1S**, confirmed; design print bodies within **220 × 220 × 240mm** | [P1S profile and placement](p1s-printing.md) account for a 5mm brim, the cutter exclusion and the default 250mm height. R01 retains its historical provisional 256mm check. |
| Rack support | Shelf-supported custom enclosure | Upstream has no load-bearing rack ears. Rail or rack attachment needs a separate measured design and structural assessment. |

### CPU, memory and PCIe facts

The two E5-2630L v4 processors are a compatible supported CPU family for this board. Each provides four memory channels and 40 PCIe 3.0 lanes. CPU1 owns GPU slots 2 and 4; CPU2 owns slots 6 and 8. The four GPU links are native CPU connections, not four downstream links sharing a PCIe switch uplink. This preserves two CPU-local GPU groups; it does not create a four-card NVLink fabric or guarantee cross-socket CUDA peer access.

For eight identical 32GB modules, populate:

| CPU | Slots | Capacity |
|---|---|---:|
| CPU1 | **P1-DIMMA1, P1-DIMMB1, P1-DIMMC1, P1-DIMMD1** | 128GB |
| CPU2 | **P2-DIMME1, P2-DIMMF1, P2-DIMMG1, P2-DIMMH1** | 128GB |

Samsung documents this module family as a 32GB, 2Rx4, 1.2V ECC RDIMM with a very low profile. The board supports that memory class. Exact-SKU qualification and the condition of the owned sticks are not established by the CAD project.

### Power interfaces to account for

The motherboard uses **24-pin ATX, two 8-pin CPU/EPS connectors and one auxiliary 4-pin connector**. Supermicro instructs connecting all four. Their cable exits and bend space belong in the layout.

Reference passive RTX 8000 documentation describes an **8-pin CPU-style auxiliary input**; the active workstation card uses **8-pin plus 6-pin PCIe inputs**. Confirm each actual card and any adapter before selecting cables. Similar-looking CPU/EPS and PCIe connectors are not interchangeable. Modular cables must match the selected PSU's pinout.

R01 does **not** implement a dual-PSU electrical design. In particular, it does not specify PSU-to-GPU load assignment, PCIe-slot versus auxiliary supply sourcing, power-on synchronization, fault behavior or PSU sense wiring. These must be settled before an energized prototype. No mains wiring modifications are proposed.

## What we retain and what changes

| Upstream feature | Treatment |
|---|---|
| Sectional printed construction with metal reinforcement | Retain the approach; recalculate sections, joints, rod paths and hardware for the new footprint and printer. |
| Coordinate convention | Retain **+X left, +Y front, +Z up**, with the floor top at **Z19.05**. |
| Existing chassis STEP | Preserve as the printed baseline and a comparison reference. It is not a parametric source for a larger board. |
| Nine motherboard standoffs | Replace with a measured **14-hole X10DRG-Q pattern** in a later revision. R01 must not invent hole coordinates. |
| Eight-position rear PCIe opening | Redesign around the X10DRG-Q's full rear layout and selected GPU slots. The upstream opening is not a validated fit. |
| Two paired V620 ducts | Replace the interfaces and flow distribution with **three passive-card paths plus a blower inlet keepout**. |
| Step 20 supports and Step 22 bar | Reuse ideas only. Their original coordinates and hardware stacks are not valid for the new motherboard footprint. |
| Dual PSU mounting | Reposition/rebuild once actual PSU bodies and connector clearances are known. Preserve independent intake/exhaust access. |
| Lid and service openings | Redesign to clear both CPU coolers, the two NVLink bridges and GPU power-cable exits. |

### Layout datums and unresolved dimensions

The manufacturer's product page gives the board as **386.1 × 335.3mm**, while a manual dimension states **384.04 × 335.28mm**. Reserve the larger **386.1 × 335.3mm** envelope for the concept. Neither value is a substitute for measuring the board and its mounting-hole centers.

The current layout candidate places the board envelope at **X25, Y20.918**, with its forward edge at **Y356.218**. These are **design placement values**, not measured GPU-slot or motherboard-hole coordinates. The GPU slot origin, CPU/socket locations and all 14 hole centers remain unknown.

The larger board reaches beyond the upstream **Y350** floor-support row. Existing low duct rails/supports can therefore collide with the board. The revised support concept starts forward of it, around **Y370 or greater**, subject to the complete measured envelopes.

The upstream shell is **444.50 × 584.20 × 260.35mm**. R01 compares that baseline with a **634.20mm-deep candidate** to investigate space for PSU cable exits and GPU duct routing. This depth is a design candidate, not a selected final chassis size. Changing shell depth also changes reinforcement, print splits, lid seams and rack-shelf support requirements.

## Cooling approach

Use a common intake region or fan bank feeding three **individually bounded passive-card passages**. Each passage needs a measured outlet matching its card's heatsink/shroud opening, removable sealing and a support independent of the GPU PCB. Prevent air from bypassing the heatsink through a large open gap around the duct.

The active card needs a separate path that supplies its radial blower inlet while allowing hot air to leave through its rear bracket. Do not assume that a duct blowing at the end of a blower card cools it in the same way as a passive card. Its side inlet, neighboring-card spacing and NVLink body must be included in interference checks.

Fan diameter alone is not an acceptance test. Fan selection depends on the pressure required by the measured ducts and passive heatsinks, inlet restriction and the selected GPU power limits. A reduced-speed setting is a tuning target to verify under load; it is not evidence that passive-card cooling is sufficient. Keep motherboard VRMs, DIMMs and both CPU coolers in the airflow plan as well.

The generated R01 routes two half-column inlets and one full-column inlet
from the four-fan bank: inlet areas are **14,400 / 14,400 / 28,800mm²**.
This unequal **1:1:2** allocation is an unresolved routing choice, not a
balanced cooling design. A common distribution plenum or three dedicated
fans should be evaluated before fixing the final duct architecture.

### First geometry results

| Variant | Model result | Print-envelope result |
|---|---|---|
| Compact, 584.20mm deep | Two intersections between PSU cable reservations and the slot-8 duct | All three concept shells fit the provisional 256mm cube in the exported orientation |
| Extended, 634.20mm deep | No intersections or enclosure-boundary violations among modeled envelopes | All three shells are 290.60mm long in the print orientation; need segmentation or a larger printer |

These results use actual saved STL facets for bounds, closed-mesh/winding
and bed-contact checks. Full rectangular fan volumes include rotor space
in collision checks, even though the renders show cutaway fan frames.
The model lacks measured mounting interfaces and GPU power-plug keepouts;
the extended result therefore does not establish a complete hardware fit.

## R02 development direction

The confirmed P1S removes the need to keep the printer envelope provisional.
R02 is a separate generator and set of artifacts: three dedicated 120mm
duct fans, one per passive card, with segmented ducts and removable joints.
Equal fan inlet areas remove R01's 1:1:2 allocation; they do **not** prove
equal airflow or adequate heatsink cooling. R01 remains available for comparison.

The immediate physical prototype is a small duct-joint sample, followed by
the measured GPU outlet interface. Motherboard standoffs and the rear wall
remain deferred until the actual board or an authoritative dimensioned drawing
provides hole, slot and I/O coordinates. PSU selection can proceed independently
using the [shortlist](x10drg-q-psu-options.md), but its connector inventory and
cable routing must be settled before freezing the mounts.

## Implementation milestones and acceptance gates

| Stage | Deliverable | Acceptance gate | Status |
|---|---|---|---|
| **1 — R01 concept** | Configurable CadQuery layout; board/card/bridge/PSU envelopes; three passive duct concepts; blower inlet keepout; baseline versus deeper-shell comparison | Valid intended solids; dimension and interference reports; actual-CAD top/overview renders; unresolved inputs explicitly marked | **Generated and reviewed; not printable production hardware** |
| **2 — Measured interface model** | Verified motherboard holes, slot origin, rear I/O, GPU brackets, cooler and power-connector envelopes | Every critical coordinate traceable to measurement or dimensioned manufacturer drawing; no guessed mounting holes | Pending measurement |
| **3 — Prototype interfaces** | Small motherboard-standoff, GPU-bracket, duct-outlet and PSU-mount coupons; measured hardware stacks | Dry fit on actual hardware; screws engage without bottoming; connectors and tools remain accessible | [PSU screw-seat samples](psu-fit-samples.md) implemented; physical tests and other interfaces pending |
| **4 — Enclosure revision** | New chassis sections, joints, reinforcement, mounts, retention, lid and ducts | No unintended interference; assembly order demonstrated; each oriented print fits the confirmed printer; mechanical support assessed | Pending |
| **5 — Powered validation** | Completed power/cabling plan and instrumented cooling tests | Correct GPU links/NVLink pairs and RAM detection; all cards maintain intended clocks under simultaneous load; acceptable measured temperatures/noise | Pending |
| **6 — Manufacturing release** | Published STEP, source, dimensions, CAD renders and relevant checks; local STL export instructions; assembly/hardware guide | Physical fit and thermal/structural acceptance recorded; remaining limitations disclosed | Pending |

Do not mark upstream issue [#1, GPU bracket top-flange clearance](https://github.com/PraxisOG/moe-chassis/issues/1), or [#2, PSU screw-bearing lands](https://github.com/PraxisOG/moe-chassis/issues/2), resolved because R01 builds or renders. Both remain open on the preserved baseline. The new rear-retention and PSU interfaces also need their own physical acceptance. The approximate 2mm PSU screw land requested upstream is a starting design requirement, not a universal screw-engagement specification.

## Build and published artifacts

The dedicated concept builder is separate from the exporter for the 34 upstream print files:

```bash
python tools/build_x10drg_q.py --output build/x10drg-q-r01
```

An explicit configuration can be supplied with:

```bash
python tools/build_x10drg_q.py --output build/x10drg-q-r01 --config source/x10drg_q_r01/layout.json
```

The builder refuses a nonempty output directory. It generates **compact 584.20mm** and **extended 634.20mm** variant directories, each containing `layout.step`, `checks.json`, `dimensions.json` and `renders/overview.png` / `renders/top.png`; a combined `comparison.json` records the comparison. Review the actual reports before interpreting a check as passed. Local duct STL output under `concept-only/` represents concept geometry, **not production print parts**. No full-chassis printable model is supplied by R01.

After review, the tracked concept artifacts belong under `cad/x10drg-q-r01/`, `renders/x10drg-q-r01/` and `checks/x10drg-q-r01/`. Follow the repository's existing policy: **STLs and print ZIPs remain local under `build/`; do not commit them.** A saved report describes only the configuration from which it was generated. Regenerate reports and renders after changing parameters.

A separate [PSU screw-seat sample](psu-fit-samples.md) compares an approximately **2mm screw-bearing land** with the **5mm upstream baseline**. These small samples test screw access/engagement; they are not full PSU mounting plates and do not close upstream issue #2. Follow that guide for its dedicated builder and hardware test.

Before geometry publication, update the relevant assembly steps and hardware stack lengths, run the repository package validation, and refresh the manifest. Parent project documentation and the manifest are maintained separately from this plan.

## Sources

- [Supermicro X10DRG-Q specifications](https://www.supermicro.com/en/products/motherboard/X10DRG-Q): supported CPU family, BIOS requirement, DIMMs, PCIe and product-page dimensions.
- [Supermicro X10DRG-Q manual](https://www.supermicro.com/manuals/motherboard/C612/MNL-1677.pdf): board layout, 14 mounting holes, PCIe ownership, DIMM labels, connectors and BIOS settings. Manual revisions and rounded dimensions can differ.
- [Supermicro motherboard power FAQ 39086](https://www.supermicro.com/en/support/faqs/faq.php?faq=39086): connect 24-pin, both 8-pin and the auxiliary 4-pin motherboard supply connectors.
- [Intel E5-2630L v4 specifications](https://www.intel.com/content/www/us/en/products/sku/92978/intel-xeon-processor-e52630l-v4-25m-cache-1-80-ghz/specifications.html): four memory channels, DDR4-2133 ceiling, 40 PCIe 3.0 lanes and 55W TDP per CPU.
- [Samsung DDR4 product guide, May 2018](https://download.semiconductor.samsung.com/resources/product-guide/DDR4_Product_guide_May.18.pdf) and [M392A4K40BM0-CRC40 SPD document](https://download.semiconductor.samsung.cn/resources/data-sheet/M392A4K40BM0-CRC40-0.pdf): module family, RDIMM/ECC organization, voltage and speed.
- [NVIDIA Quadro RTX 8000 passive server-card product brief](https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/quadro-product-literature/NVIDIA-Quadro-RTX-8000-PCIe-Server-Card-PB-FINAL-1219.pdf): passive-card mechanical, power and cooling requirements. Check the actual OEM cards against this reference.
- [ASUS ESC4000 G3 factory parts](https://www.asus.com/ca-en/networking-iot-servers/servers/rack-servers/esc4000_g3/techspec/) and [ASUS-produced RS700 product printout](https://www.azken.com/download/BAREBONE_ASUS_RS700-E8-RS8-V2.pdf): cooler part 13071-00091400 and its square-ILM description. Actual installed cooler identity still needs checking.
- [Supermicro X10DRG-Q heatsink FAQ 29074](https://www.supermicro.com/en/support/faqs/faq.php?faq=29074): an example compatible cooler; not a purchasing decision.
- [Upstream project](https://github.com/PraxisOG/moe-chassis), [dimensions](dimensions.md), [hardware](hardware.md), [development](development.md) and [revisions](revisions.md): preserved baseline, build policy and known fit history.
