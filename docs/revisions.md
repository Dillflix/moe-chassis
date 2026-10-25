# Revision and fit history

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
