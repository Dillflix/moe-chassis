"""Validate published links/hashes; optionally check all 34 generated STLs."""
from pathlib import Path
import argparse, hashlib, json, re, struct
ROOT = Path(__file__).resolve().parents[1]
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--prints', type=Path, help='Complete output of tools/export_prints.py')
args = ap.parse_args()
errors = []
for p in [ROOT/'README.md', *ROOT.glob('docs/*.md'), ROOT/'docs/archive/README.md', ROOT/'checks/README.md']:
    for match in re.finditer(r'!?\[[^\]]*\]\(([^)]+)\)', p.read_text()):
        link = match.group(1).split('#')[0]
        if not link or re.match(r'\w+://', link): continue
        if not (p.parent/link).exists(): errors.append(f'Broken link: {p.relative_to(ROOT)} -> {link}')
manifest = json.loads((ROOT/'checks/file-manifest.json').read_text())
for f in manifest['files']:
    p = ROOT/f['path']
    if not p.exists() or p.stat().st_size != f['size_bytes'] or hashlib.sha256(p.read_bytes()).hexdigest() != f['sha256']:
        errors.append(f'Manifest mismatch: {f["path"]}')
if args.prints:
    import numpy as np
    baseline = json.loads((ROOT/'checks/print-baseline.json').read_text())['parts']
    stls = {str(p.relative_to(args.prints)):p for p in args.prints.rglob('*.stl')}
    if set(stls) != set(baseline):
        errors.append(f'Print set differs: missing {set(baseline)-set(stls)}, extra {set(stls)-set(baseline)}')
    for name, p in stls.items():
        data = p.read_bytes()
        if len(data) < 84: errors.append(f'Short STL: {name}'); continue
        n = struct.unpack_from('<I', data, 80)[0]
        if len(data) != 84 + 50*n or n == 0: errors.append(f'Invalid binary STL: {name}'); continue
        dtype = np.dtype([('normal','<f4',3), ('v','<f4',(3,3)), ('attr','<u2')])
        v = np.frombuffer(data, dtype=dtype, count=n, offset=84)['v'].astype(float)
        _, inv = np.unique(np.round(v.reshape(-1,3),5), axis=0, return_inverse=True)
        faces = inv.reshape(-1,3)
        edges = np.concatenate([faces[:,[0,1]], faces[:,[1,2]], faces[:,[2,0]]])
        edges = edges[edges[:,0] != edges[:,1]]
        _, idx, counts = np.unique(np.sort(edges,axis=1), axis=0, return_inverse=True, return_counts=True)
        winding = np.bincount(idx, weights=np.where(edges[:,0]<edges[:,1], 1, -1))
        volume = np.sum(np.einsum('ij,ij->i', v[:,0], np.cross(v[:,1],v[:,2])))/6
        if not np.all(counts == 2) or not np.all(winding == 0) or volume <= 0:
            errors.append(f'Mesh topology: {name}')
        if abs(float(v[:,:,2].min())) > .001: errors.append(f'STL not on bed: {name}')
        if name in baseline:
            expected = baseline[name]
            if not np.allclose(v.max((0,1))-v.min((0,1)), expected['bounds_mm'], rtol=0, atol=.002):
                errors.append(f'Print bounds changed: {name}')
            if abs(volume/expected['volume_mm3']-1) > .0005:
                errors.append(f'Volume differs from original print by >0.05%: {name}')
    print(f'Checked {len(stls)} generated STLs against the original print geometry.')
if errors: raise SystemExit('\n'.join(errors))
print(f'PASS: documentation links and {len(manifest["files"])} file hashes valid' + ('; all meshes closed, consistently wound, on bed, and baseline-sized.' if args.prints else '.'))
