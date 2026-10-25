"""Stage the original scripts with their inputs, without editing source CAD."""
from pathlib import Path
import argparse, shutil, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('target',choices=['ducts','lid','bar'])
ap.add_argument('--output',type=Path,help='Empty build directory; defaults to build/<target>')
args=ap.parse_args()
out=(args.output or ROOT/'build'/args.target).resolve()
if out.exists() and any(out.iterdir()):
    raise SystemExit(f'Output must be empty: {out}')
out.mkdir(parents=True,exist_ok=True)
def cp(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src,dst)
def run(name):
    print(f'Running {name}',flush=True)
    subprocess.run([sys.executable,str(out/name)],cwd=out,check=True)

if args.target=='ducts':
    for f in (ROOT/'source/step20').glob('*.py'):cp(f,out/f.name)
    cp(ROOT/'cad/chassis/6U_Chassis_Step_16.step',out/'6U_Chassis_Step_16.step')
    for f in (ROOT/'cad/references').glob('*.step'):cp(f,out/f.name)
    for name in ['trim_interface19.py','ducts_step20.py','finish_ducts20.py','check_ducts20_meshes.py','check_print20.py','check_fan_mounts20.py','render_ducts20.py']:
        run(name)
else:
    step='step21' if args.target=='lid' else 'step22'
    for f in (ROOT/'source'/step).glob('*.py'):cp(f,out/f.name)
    ref=out/'assembly_sources/project'
    cp(ROOT/'cad/chassis/6U_Chassis_Step_16.step',ref/'References/6U_Chassis_Step_16.step')
    for f in (ROOT/'cad/references').glob('*.step'):cp(f,ref/'References'/f.name)
    for f in (ROOT/'cad/ducts').glob('Duct20_*.step'):cp(f,ref/'Parts'/f.name)
    cp(ROOT/'source/step20/software_render_views.py',ref/'Sources/software_render_views.py')
    scripts=['lid_step21.py','check_lid21_meshes.py','render_lid21.py'] if args.target=='lid' else ['duct_bar22.py','render_bar22.py']
    for name in scripts:run(name)
print(f'Finished: {out}')
