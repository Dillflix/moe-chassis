# X10DRG-Q PSU options and cable budget

Research checked **25 October 2026**. Prices are Canadian dollars before tax and delivery; retailer stock and promotions can change.

**No PSU has been selected or purchased, and the X10DRG-Q has not been ordered.** This is a purchasing shortlist and a mechanical/cable budget for the proposed four-RTX-8000 build. It is not an approved wiring map or a validated dual-PSU electrical design.

[Adaptation plan](x10drg-q-plan.md) · [Measurement worksheet](x10drg-q-measurements.md)

## Mechanical reservation

For the R02 layout, reserve **160mm PSU body depth ×150mm width ×86mm height**, plus a **provisional 30mm cable-exit zone** at the modular connector face. The resulting depth reservation is 190mm per PSU, excluding any separate intake/exhaust clearance. Allow supports to accommodate 140mm, 150mm and 160mm bodies.

The candidates below are 140–150mm deep, leaving some adjustment within that body reservation. The 30mm cable zone is a design assumption, not a manufacturer-approved bend allowance. The selected connectors, latch access and actual cable routing must be checked before the mounts and nearby ducts are fixed. PSU screw engagement, inlet access and rear AC connector/switch access remain separate interfaces.

## Canadian shortlist

| Exact model | Body depth × width × height | Rated output on 120V AC | Included EPS/CPU cables | Included conventional PCIe power cables | Canadian offer observed 25 October 2026 |
|---|---|---|---|---|---|
| **MSI MAG A850GL PCIE5** | **140 ×150 ×86mm** | **850W total**, 846W on +12V; 100–240V input | **2 separate 4+4 cables** | **2 cables with 2 plugs each**: four 6+2 plugs; separate native 16-pin cable also supplied | [Memory Express MX00125992](https://www.memoryexpress.com/Products/MX00125992): **$149.99**; Burnaby 5, Langley 8, Vancouver 10+, online 10+ |
| **MSI MAG A1000GL PCIE5** | **150 ×150 ×86mm** | **1000W total**, 999.6W on +12V; 100–240V input | **2 separate 4+4 cables** | **2 cables with 2 plugs each**: four 6+2 plugs; separate native 16-pin cable also supplied | [Memory Express MX00129339](https://www.memoryexpress.com/Products/MX00129339): **$179.99**; Burnaby 9, Langley 4, Vancouver 5, online 10+ |
| **Corsair RM850e 2025, CP-9020296-NA** | **140 ×150 ×86mm** | **850W total**, 70.8A on +12V; 100–240V input | **2 separate 4+4 cables**, 750mm | **1 standalone 6+2 cable**, plus **1 cable from the PSU's dedicated 12V-2x6 socket to two 6+2 plugs**; three conventional GPU plugs total | [Memory Express MX00132465](https://www.memoryexpress.com/Products/MX00132465): **$184.99**; Burnaby 2, Langley 1, Vancouver 4, online 9 |
| **Corsair RM1000e 2025, CP-9020297-NA** | **140 ×150 ×86mm** | **1000W total**, 83.3A on +12V; 100–240V input | **2 separate 4+4 cables**, 750mm | **2 standalone 6+2 cables**, plus **1 cable from the PSU's dedicated 12V-2x6 socket to two 6+2 plugs**; four conventional GPU plugs total | [Memory Express MX00132467](https://www.memoryexpress.com/Products/MX00132467): **$239.99**; Burnaby 2, online 2 |

The MSI offers showed a sale deadline of **30 October 2026, 03:59 EDT**. Both MSI models advertise a ten-year limited warranty; Corsair RMe has a seven-year warranty. These are supported retail families with documented protections and full-range AC input. This research does not constitute a lifetime-reliability comparison.

The MSI products are the lower-price shortlist. Corsair's advantage for this particular build is the verified source of additional compatible EPS cables below. Extra MSI EPS cables remain a sourcing condition; no official Canadian retail listing for the required additional MSI leads was verified.

All four candidates have **five shared CPU/PCIe 8-pin modular sockets**, in addition to their dedicated newer GPU-power socket and motherboard/peripheral connections. The shared socket label describes the PSU end: the cable determines whether its component end is CPU/EPS or PCIe. Manufacturer-supplied connector-panel images were inspected for the port count.

A third-family alternative is the [Seasonic FOCUS GX-850 ATX 3.1 / 2024](https://www.newegg.ca/seasonic-usa-focus-gx-atx-3-atx-3-1-850-w-80-plus-gold-certified-power-supplies-gx-850/p/N82E16817151271): 140mm body depth, full 850W output on 100–240V input, two separate EPS cables and three separate single-plug PCIe cables. Newegg Canada showed **$229.99**, sold and shipped by Newegg. It is a compatible size alternative, but not the leading budget offer at that price.

### Corsair inventory discrepancy

The shared **2025 RMe manual** lists two standalone PCIe cables for the RM850e, whereas the **exact CP-9020296-NA product page and its cable photograph show one**. This budget uses the conservative exact-SKU inventory: one standalone cable on the RM850e, two on the RM1000e. The additional 12V-2x6-to-dual-6+2 cable is a separate included item; it is not two independent cable runs.

Use the official manual for the 140mm body dimensions and electrical output ratings. Some retailer and product-page fields contain conflicting copied values. Older **2023 RM850e/RM1000e** models have different cable kits; the family name alone is insufficient to substitute them into this table.

## Required component connections

| Component | Required input | Direct-cable budget |
|---|---|---|
| X10DRG-Q main input | 24-pin ATX | 1 motherboard cable from the primary PSU |
| CPU1 and CPU2 motherboard inputs | Two 8-pin EPS | 2 separate EPS runs from the primary PSU |
| Motherboard auxiliary input | 4-pin CPU-style power | 1 further EPS4+4 run from the primary PSU, using one half |
| Three passive RTX 8000s | Reference cards use 8-pin CPU/EPS-style auxiliary input | 3 separate compatible EPS runs, subject to checking the actual OEM cards |
| One active/blower RTX 8000 | PCIe8 + PCIe6 auxiliary inputs | Budget 2 separate PCIe cable runs, using 6+2 as 8 and 6 respectively |

Supermicro instructs connecting **all four motherboard power inputs**. Keep the 24-pin, both CPU8-pin inputs and the auxiliary4-pin input on the **primary PSU** in either allocation considered here.

The direct-EPS approach therefore needs **six EPS cable runs**, plus the motherboard cable and two PCIe cable runs. Two of the listed PSUs supply only **four EPS cables total**, so their stock kits alone are incomplete.

For Corsair, the genuine [CP-8920141 Type4 EPS4+4 cable, 650mm](https://www.corsair.com/ca/en/p/pc-components-accessories/cp-8920141/type-4-sleeved-black-8-pin-4-4-atx12v-eps12v-cable-compatible-with-all-corsair-type-4-pin-out-psu-cp-8920141) was **$5.99 and in stock** at Corsair Canada. Two additional leads add **$11.98**, before delivery and tax. These Type4 cables match the shortlisted Type4 Corsair supplies; they do not establish compatibility with an MSI modular socket. Check that their 650mm length reaches the selected routes.

The NVIDIA passive-card brief also describes a correctly wired CPU-to-PCIe adapter arrangement. That is an alternative to a direct compatible EPS lead, not permission to plug an ordinary PCIe8 connector into the passive card. If adapters are selected, redraw the complete cable and modular-port budget around the exact adapter and its required PCIe feeds. A pair of plugs on one daisy-chain cable must not silently be counted as two separate runs.

## Candidate allocation and modular-port budgets

These allocations make the remaining design choice concrete. **Neither has been electrically validated.** All GPU slots receive power through the primary-powered motherboard, regardless of which supply feeds the GPU's auxiliary connector.

| Allocation | Primary PSU shared CPU/PCIe sockets | Secondary PSU shared CPU/PCIe sockets | Additional cable implication |
|---|---|---|---|
| **A — all GPU auxiliary inputs on secondary** | **3 EPS**: CPU1, CPU2, motherboard auxiliary4; 3 of 5 sockets | **3 EPS +2 separate PCIe runs**: three passive cards and blower; 5 of 5 sockets | One extra EPS cable per PSU. If the secondary is an RM850e and the design retains two standalone PCIe runs, it needs one additional compatible standalone PCIe cable beyond the stock kit. Its included dual-output cable is a different routing option, not the specified two-run arrangement. |
| **B — blower auxiliary inputs on primary** | **3 EPS +2 separate PCIe runs**; 5 of 5 sockets | **3 EPS** for the passive cards; 3 of 5 sockets | One extra EPS cable per PSU. The primary needs two standalone PCIe runs: both MSI candidates and the RM1000e include them; the RM850e has only one in the conservative inventory. |

The primary 24-pin motherboard cable uses its own modular connection, outside the five-port count. Peripheral cables and the synchronizer also need their corresponding connections and routing, but do not consume these CPU/PCIe sockets.

Allocation B gives the blower card one PSU for both slot and auxiliary power and shifts some load off the secondary. Its three passive cards still have primary-supplied slots and secondary-supplied auxiliary inputs. Allocation A splits those sources on all four cards. **The slot/auxiliary supply relationship, startup/shutdown behavior and fault response require review before an energized prototype.** A startup synchronizer controls on/off; it does not combine the outputs into one supply or validate those relationships.

## Load accounting for the two allocations

Use **250W per passive reference card** and **295W for the active reference board** as the uncapped planning values: **1045W total GPU board power**. These values already include PCIe-slot draw. Do not add another 300W to the system's GPU total.

For a transparent comparison, let each card's slot draw be between 0 and the **75W slot allowance**, let the two CPUs have a provisional **110W combined allowance**, and let **R** represent the remaining motherboard, memory, storage, fans and conversion overhead. The 110W figure is based on two 55W CPU TDPs; it is not a measured guarantee of CPU input consumption.

| Allocation | Primary load expression at uncapped GPU values | Secondary GPU auxiliary load expression | Consequence |
|---|---|---|---|
| A | `110 + R + sum(all four slot draws)`; at most `410 + R` under this slot allowance | `1045 - sum(all four slot draws)` | A secondary850W cannot be justified merely by assuming all slots supply75W. Lower actual slot draw raises its auxiliary load. The expression ranges from745W to1045W before any secondary-powered non-GPU loads. |
| B | `110 + R + 295 + sum(three passive slot draws)`; at most `630 + R` | `750 - sum(three passive slot draws)`; at most750W | Better partition for two850W candidates on this simplified stock-power budget. If `R = 100–190W`, the primary upper allowance is730–820W; the upper end leaves little margin on850W. A1000W primary gives more room. |

The individual upper bounds do not occur simultaneously and must not be added together. Both rows preserve the same system total, **`1155 + R` watts**, or approximately1255–1345W for the illustrative `R = 100–190W` range.

At four **200W GPU board-power caps**, total GPU power becomes800W. Allocation A's secondary GPU auxiliary demand is then at most800W; allocation B's secondary is at most600W, and its primary upper expression is `535 + R`. These are planning calculations, not measured loads or a validation of the split-supply arrangement. The caps also must not be treated as a hardware-enforced startup/fault limit.

## Pair costs and remaining selection

| Candidate pair | PSU subtotal | Known extra EPS cost | What remains before selecting it |
|---|---:|---:|---|
| 2× MSI MAG A850GL | **$299.98** | Not sourced | Verify compatible additional EPS leads and final allocation; both bodies140mm. |
| MSI MAG A1000GL + A850GL | **$329.98** | Not sourced | Verify compatible additional EPS leads;1000W primary is the stronger allocation-B candidate; bodies150/140mm. |
| 2× Corsair RM850e2025 | **$369.98** | **$11.98**; **$381.96 combined** | The two-standalone-PCIe-run allocation also needs an additional compatible PCIe cable on the supply feeding the blower, or a separately reviewed use of its included dual-output cable. Both bodies140mm. |
| Corsair RM1000e2025 + RM850e2025 | **$424.98** | **$11.98**; **$436.96 combined** | With1000W primary and allocation B, stock PCIe cables plus the two extra EPS leads satisfy the stated connector inventory. Electrical allocation and physical routing remain unvalidated. Both bodies140mm. |

Subtotals exclude tax, delivery, synchronization hardware and any additional PCIe cable or GPU adapter. **Matching connector inventory is not the same as validating the wiring arrangement.** The budget MSI pair and the easier-to-source Corsair cable ecosystem should remain alternatives until the exact cable map and hardware checks are complete.

## Sources and verification notes

- [MSI A850GL specifications](https://ca.msi.com/Power-Supply/MAG-A850GL-PCIE5/Specification) and [product page](https://ca.msi.com/Power-Supply/MAG-A850GL-PCIE5): dimensions,100–240V input, power table and separate cable counts. [Manufacturer modular-panel image](https://storage-asset.msi.com/global/picture/image/feature/power/MAG/A750GL-PCIE5/need-img.png), linked by that page, shows five CPU/PCIe sockets.
- [MSI A1000GL specification sheet](https://storage-asset.msi.com/datasheet/power-supply/ca/MAG-A1000GL-PCIE5.pdf) and [product page](https://ca.msi.com/Power-Supply/MAG-A1000GL-PCIE5):150mm depth,100–240V input, power table and cable counts. [Manufacturer modular-panel image](https://storage-asset.msi.com/global/picture/image/feature/power/MAG/mag-a1250gl-pcie5/images/need-img.png), linked by the page, shows five CPU/PCIe sockets. Confirm the actual SKU/revision against the shipping unit; marketing assets are shared across some model pages.
- [MSI US official A1000GL listing](https://us-store.msi.com/Power-Supply/MAG-A1000GL-PCIE5) and the linked Canadian retailer listings: ten-year advertised limited warranty. The Canadian product pages contain some older ATX3.0 marketing text while current retailer listings describe ATX3.1; the basic dimensions and cable budget agree, but verify the exact supplied revision.
- [Corsair RMe2025 manual](https://www.corsair.com/ca/en/explorer/diy-builder/power-supply-units/corsair-rme-series-2025/): dimensions, electrical ratings, EPS4+4 use on a4-pin motherboard input and warranty.
- Exact Corsair product pages: [RM850e CP-9020296-NA](https://www.corsair.com/ca/en/p/psu/cp-9020296-na/rme-series-rm850e-fully-modular-low-noise-atx-power-supply-cp-9020296-na) and [RM1000e CP-9020297-NA](https://www.corsair.com/ca/en/p/psu/cp-9020297-na/rme-series-rm1000e-fully-modular-low-noise-atx-power-supply-cp-9020297-na). Manufacturer-supplied [850W connector-panel photo](https://c1.neweggimages.com/productimage/nb640/17-139-336-05.png) and [1000W connector-panel photo](https://c1.neweggimages.com/productimage/nb640/17-139-337-05.png) show five CPU/PCIe sockets.
- [Corsair genuine Type4 EPS cable CP-8920141](https://www.corsair.com/ca/en/p/pc-components-accessories/cp-8920141/type-4-sleeved-black-8-pin-4-4-atx12v-eps12v-cable-compatible-with-all-corsair-type-4-pin-out-psu-cp-8920141): observed Canadian price, stock,650mm length and compatible cable family.
- [Seasonic FOCUS GX ATX3.1](https://seasonic.com/focus-gx-atx-3/): dimensions, input/output specifications, cable counts and ten-year warranty for the third-family alternative.
- [Supermicro power FAQ39086](https://www.supermicro.com/en/support/faqs/faq.php?faq=39086) and [X10DRG-Q manual](https://www.supermicro.com/manuals/motherboard/C612/MNL-1677.pdf): connect24-pin, both8-pin and auxiliary4-pin inputs.
- [NVIDIA passive RTX8000 server-card brief](https://www.nvidia.com/content/dam/en-zz/Solutions/design-visualization/quadro-product-literature/NVIDIA-Quadro-RTX-8000-PCIe-Server-Card-PB-FINAL-1219.pdf):250W passive reference card, CPU-style8-pin input and supported adapter arrangements. [NVIDIA active RTX8000 specifications](https://www.nvidia.com/en-gb/products/workstations/quadro/rtx-8000/) and [Leadtek active-card specifications](https://www.leadtek.com/eng/products/workstation_graphics(2)/NVIDIA_Quadro_RTX8000(20830)/detail):295W reference board power and PCIe8+6 power inputs.
- [NVIDIA engineer discussion of separate slot/auxiliary supplies](https://forums.developer.nvidia.com/t/power-supply-for-titan-xp/51059): rationale for treating independent supplies as an integration question rather than certifying a layout from wattage and a startup cable alone. It is not a qualification report for this RTX8000/X10DRG-Q combination.
