"""Export the preserved STEP geometry as 34 oriented STLs, without redesigning it."""
from pathlib import Path
import argparse
import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
CHASSIS_NAMES = [
    'REAR_RIGHT', 'REAR_LEFT', 'FRONT_RIGHT', 'FRONT_LEFT',
    'BRIDGE_X_REAR', 'BRIDGE_X_FRONT', 'BRIDGE_Y_RIGHT', 'BRIDGE_Y_LEFT',
    'STRAP_RIGHT', 'STRAP_LEFT', 'STRAP_REAR',
]

def read(path):
    return cq.importers.importStep(str(path)).val()

def on_bed(shape):
    b = shape.BoundingBox()
    return shape.translate((-b.xmin, -b.ymin, -b.zmin))

def optional_shim(riser):
    """The existing optional shim is the bottom 2 mm of a constant-section riser.

    The original 2 mm STL and the 10 mm riser STL, scaled only in Z,
    matched to 0.000002 mm in the publication check. No new hole layout.
    """
    s = on_bed(riser)
    return s.intersect(cq.Solid.makeBox(26, 30, 2, cq.Vector(-1, -1, 0))).clean()

def export_all(out, target='all'):
    paths = []
    def save(shape, folder, name, tolerance=.06, angle=.1):
        if not shape.isValid() or len(shape.Solids()) != 1:
            raise ValueError(f'Invalid solid: {name}')
        path = out / folder / (name + '_Print.stl')
        path.parent.mkdir(parents=True, exist_ok=True)
        cq.exporters.export(on_bed(shape), str(path), tolerance=tolerance, angularTolerance=angle)
        paths.append(path)
        print(path.relative_to(out), flush=True)

    if target in ('all', 'chassis'):
        solids = read(ROOT/'cad/chassis/6U_Chassis_Step_16.step').Solids()
        if len(solids) != 11:
            raise ValueError('Expected the unchanged 11-solid Step 16 assembly')
        for name, shape in zip(CHASSIS_NAMES, solids):
            if name.startswith(('REAR_', 'FRONT_')):
                # +X is chassis left: the outside sidewall must touch the bed.
                shape = shape.rotate((0,0,0), (0,1,0), 90 if 'LEFT' in name else -90)
                folder = 'chassis'
            else:
                folder = 'connectors'
                if name == 'STRAP_REAR':
                    shape = shape.rotate((0,0,0), (1,0,0), 90)
                elif name.startswith('STRAP_'):
                    shape = shape.rotate((0,0,0), (0,1,0), 90)
            save(shape, folder, '6U_Step16_' + name)

    if target in ('all', 'ducts'):
        for path in sorted((ROOT/'cad/ducts').glob('Duct20_*.step')):
            shape = read(path)
            if path.stem.endswith('_DUCT'):
                shape = shape.rotate((0,0,0), (1,0,0), -90)
                folder = 'ducts'
            elif path.stem == 'Duct20_FAN_BANK_CARRIER':
                shape = shape.rotate((0,0,0), (1,0,0), 90)
                folder = 'legacy-carrier'
            else:
                folder = 'cradles-and-shim'
            save(shape, folder, path.stem)
        riser = read(ROOT/'cad/ducts/Duct20_PAIR_A_FRONT_RISER_10.step')
        save(optional_shim(riser), 'cradles-and-shim', 'Duct20_Optional_2mm_Height_Shim')

    if target in ('all', 'lid'):
        solids = read(ROOT/'cad/lid/MOE_Lid_Step21.step').Solids()
        if len(solids) != 4:
            raise ValueError('Expected four lid panels')
        for shape in solids:
            b = shape.BoundingBox()
            name = ('FRONT' if b.ymin > 250 else 'REAR') + '_' + ('LEFT' if b.xmin > 200 else 'RIGHT')
            save(shape, 'lid', 'Lid21_' + name, .03)

    if target in ('all', 'bar'):
        save(read(ROOT/'cad/ducts/MOE_Duct_Retaining_Bar_Step22.step'),
             'ducts', 'MOE_Duct_Retaining_Bar_Step22', .025, .08)
    expected = {'all':34, 'chassis':11, 'ducts':18, 'lid':4, 'bar':1}[target]
    if len(paths) != expected or len(set(paths)) != expected:
        raise ValueError(f'Expected {expected} unique outputs, got {len(paths)}')
    return paths

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('target', nargs='?', default='all', choices=['all','chassis','ducts','lid','bar'])
    ap.add_argument('--output', type=Path, default=ROOT/'build/print')
    args = ap.parse_args()
    out = args.output.resolve()
    if out.exists() and any(out.iterdir()):
        raise SystemExit(f'Output must be empty: {out}')
    out.mkdir(parents=True, exist_ok=True)
    paths = export_all(out, args.target)
    print(f'Exported {len(paths)} STLs to {out}')
