"""Package locally generated STLs; generated archives are not tracked by Git."""
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import argparse, subprocess, sys
ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--prints', type=Path, default=ROOT/'build/print')
ap.add_argument('--output', type=Path, default=ROOT/'build/MOE-Step22-Print-Pack.zip')
args = ap.parse_args()
subprocess.run([sys.executable, str(ROOT/'tools/validate_package.py'), '--prints', str(args.prints)], check=True)
args.output.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(args.output, 'w', ZIP_DEFLATED) as z:
    for p in sorted(args.prints.rglob('*.stl')):
        z.write(p, Path('print')/p.relative_to(args.prints))
    for p in [ROOT/'README.md', *sorted((ROOT/'docs').glob('*.md')), *sorted((ROOT/'renders').glob('*.png'))]:
        z.write(p, p.relative_to(ROOT))
    z.writestr('START_HERE.txt', 'MOE generated print pack: 34 STL files, including retained alternatives. Read docs/printing.md to choose the set. Both chassis fit bugs remain present. Full source, STEP geometry and guides: https://github.com/PraxisOG/moe-chassis\n')
print(f'Created {args.output}')
