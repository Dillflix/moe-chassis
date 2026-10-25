# Build the print files locally

[← Project](../README.md) · [Print selection](printing.md) · [Dimensions](dimensions.md)

This repository publishes **Python, STEP geometry, guides, and CAD renders**. STL files and print ZIPs are generated locally. The saved STEP solids are the authoritative geometry for the printed build; the two open chassis fit bugs are still present.

## Quick start — all 34 print files

Use Python 3.12 on Linux. The dependency versions match the environment used for the export and checks.

```bash
git clone https://github.com/PraxisOG/moe-chassis.git
cd moe-chassis
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-cad.txt
python tools/export_prints.py
python tools/validate_package.py --prints build/print
python tools/package_prints.py
```

Because the repository is private, authenticate to GitHub with your usual Git credential helper or use your configured SSH clone URL. No token belongs in the repository.

The result is `build/print/`, grouped into `chassis`, `connectors`, `ducts`, `lid`, `cradles-and-shim`, and `legacy-carrier`, plus `build/MOE-Step22-Print-Pack.zip`. Read [print selection](printing.md): the 34 files include retained mounting alternatives, not 34 mandatory parts. Units are millimetres and scale is 100%.

The exporter refuses a nonempty output directory. On a second run, choose another directory:

```bash
python tools/export_prints.py --output build/print-second-run
```

For selected parts, use `chassis` (four quadrants and seven connectors), `ducts` (18 duct/support/carrier files), `lid` (four panels), or `bar` (one part):

```bash
python tools/export_prints.py bar --output build/bar-print
```

The complete-set validator and packager expect all 34 files. Exporting triangulates unchanged STEP surfaces, so STL bytes and triangle counts need not match the original meshes. Validation checks closed, consistently wound meshes, positive volume, bed placement, original print dimensions, and volumes within 0.05% of the supplied baseline meshes. The optional 2 mm shim uses the bottom 2 mm of the saved constant-section 10 mm riser; its original mesh was checked against that section.

## What can be regenerated parametrically?

| Part | Available source |
|---|---|
| Step 16 chassis and connectors | Saved 11-solid STEP assembly plus Python STL exporter; **original early construction script/timeline is not available** |
| Step 20 ducts and adjustable supports | CadQuery generators plus saved GPU-interface STEP input |
| Step 21 lid | CadQuery generator; saved chassis and ducts used for clearance checks |
| Step 22 retaining bar | CadQuery generator; saved chassis and ducts used for clearance checks |

Open [`cad/`](../cad) in Fusion 360 for direct solid editing. These STEP files do not provide a native Fusion feature timeline. The source distribution is self-contained: the STL exporter and generator wrapper require no external STL downloads.

## Run the available generators

```bash
python tools/rebuild.py ducts
python tools/rebuild.py lid
python tools/rebuild.py bar
```

Each command stages the scripts and STEP inputs into an isolated `build/<target>` directory. Outputs remain there; the published baseline is never overwritten. Use `--output PATH` for a different **empty** directory. These commands regenerate geometry, run its saved checks, and produce actual CAD renders. The duct pipeline also regenerates the optional shim instead of copying an external STL.

For renderers and lid lettering, install the DejaVu Sans fonts at `/usr/share/fonts/truetype/dejavu` (Ubuntu package `fonts-dejavu-core`) or adapt the font paths for another OS. The quick STEP-to-STL export does not require fonts. Rendering uses NumPy/Pillow and OpenCascade tessellation, not image generation.

## Before publishing a geometry revision

1. Preserve the printed baseline and use new names for changed parts.
2. Record changed dimensions, hardware stacks, and clearances.
3. Check solid validity, mesh integrity, hardware/tool access, and neighboring parts.
4. Provide an actual CAD render and update assembly and hardware instructions.
5. Update the expected print measurements only after reviewing an intentional geometry change.
6. Refresh the source manifest and validate:

```bash
python tools/update_manifest.py
python tools/validate_package.py
```

Physical fit is separate from CAD checks. Measure the rear-bracket interference before choosing a relief dimension; physically verify screw engagement for the approximately 2 mm PSU screw-bearing lands. The published geometry has not implemented either fix.
