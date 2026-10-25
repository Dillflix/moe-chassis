# Saved checks

These are the existing CAD and mesh reports for Steps 20, 21, and 22. They check properties such as valid solids, closed meshes, nominal intersections, screw/driver clearance, and selected print overhangs.

They do **not** establish physical fit, structural strength, cooling performance, or creep resistance. The two open chassis fit bugs were found on the physical print despite prior nominal geometry checks.

`file-manifest.json` records SHA-256 hashes and sizes for the source/STEP distribution. `tools/validate_package.py` checks local Markdown links and the manifest. Add `--prints build/print` to check all 34 regenerated meshes against the dimensions and volumes in `print-baseline.json`, measured from the original STL set. Checks include watertightness, winding, bed placement, and positive volume.

The complete STEP-to-STL export was executed successfully for publication. All 34 regenerated meshes passed these checks. The saved Step 20–22 reports above describe the earlier generator runs; they are not claims of new physical testing.
