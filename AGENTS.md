# Working on MOE

- Read README.md, docs/revisions.md, and the relevant open issue before changing geometry.
- The current chassis, ducts, lid, and bar are versioned physical artifacts. Preserve the printed baseline; give changed geometry a new revision and clearly identify affected parts.
- Follow the existing coordinate convention: +X left, +Y front, +Z up; floor Z19.05.
- Keep renders derived from actual CAD. Highlight changed parts in gold; do not generate illustrative fake CAD.
- Distinguish geometry checks from physical fit/strength/thermal testing.
- For a geometry change, provide STEP, oriented STL, dimensions, a CAD render, and relevant solid/mesh/interference checks.
- Update assembly instructions and hardware stack lengths whenever a mounting interface changes.
- Keep new defects open until the requested physical acceptance criteria are satisfied; nominal CAD checks alone are insufficient.
