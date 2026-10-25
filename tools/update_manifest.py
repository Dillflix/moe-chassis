"""Refresh published-file hashes; omit generated STLs, archives, and build outputs."""
from pathlib import Path
import hashlib, json
ROOT = Path(__file__).resolve().parents[1]
files = []
for p in sorted(ROOT.rglob('*')):
    rel = p.relative_to(ROOT)
    if not p.is_file() or any(x in {'.git','.venv','__pycache__','build','print','downloads'} for x in rel.parts): continue
    if str(rel) == 'checks/file-manifest.json' or p.suffix in {'.pyc','.log','.stl','.zip'}: continue
    data = p.read_bytes()
    files.append({'path':str(rel), 'size_bytes':len(data), 'sha256':hashlib.sha256(data).hexdigest()})
(ROOT/'checks/file-manifest.json').write_text(json.dumps({'note':'Source and STEP distribution; excludes this manifest and generated outputs.', 'files':files}, indent=2)+'\n')
print(f'Manifest updated: {len(files)} files')
