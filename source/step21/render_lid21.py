from pathlib import Path
import sys,json
import cadquery as cq
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).parent;O=R/'lid_step21';S=R/'assembly_sources/project'
sys.path.insert(0,str(S/'Sources'))
from software_render_views import render
BLUE=(.53,.67,.77);GOLD=(.92,.65,.25);DARK=(.38,.43,.48)
names=['REAR_RIGHT','REAR_LEFT','FRONT_RIGHT','FRONT_LEFT']
ch=cq.importers.importStep(str(S/'References/6U_Chassis_Step_16.step')).val()
parts={n:cq.importers.importStep(str(O/f'Lid21_{n}.step')).val() for n in names}
ctx=cq.importers.importStep(str(O/'MOE_Chassis_With_Lid_Step21.step')).val()
hardware=[s for s in ctx.Solids() if s.BoundingBox().xlen<8 and s.BoundingBox().ylen<8 and s.BoundingBox().zmax>261]
assert len(hardware)==16
items=[(ch,BLUE,1)]+[(p,GOLD,1) for p in parts.values()]+[(p,DARK,1) for p in hardware]
render(items,O/'Lid21_Installed.png',(-1000,1000,1000),(222,292,137),391,size=(1400,1040))
print('installed',flush=True)
shifts={'REAR_RIGHT':(-17,-17,65),'REAR_LEFT':(17,-17,65),'FRONT_RIGHT':(-17,17,65),'FRONT_LEFT':(17,17,65)}
render([(ch,BLUE,1)]+[(p.translate(shifts[n]),GOLD,1) for n,p in parts.items()],O/'Lid21_Exploded.png',(-1000,1000,1000),(222,292,158),416,size=(1400,1040))
print('exploded',flush=True)
im=Image.new('RGB',(2800,1460),'#f6f8fa');d=ImageDraw.Draw(im)
F='/usr/share/fonts/truetype/dejavu/DejaVuSans'
def t(x,y,s,n=30,b=False,col='#243d50'):d.text((x,y),s,font=ImageFont.truetype(F+('-Bold' if b else '')+'.ttf',n),fill=col)
t(46,26,'MOE / LOW-PROFILE LID',57,True)
t(49,102,'STEP 21  •  Four flat-printing panels  •  Existing eight rim mounts',31)
im.paste(Image.open(O/'Lid21_Installed.png'),(0,157));im.paste(Image.open(O/'Lid21_Exploded.png'),(1400,157))
t(50,1162,'CLOSED / 265.35 mm maximum height',33,True)
t(1450,1162,'EXPLODED / gold = new lid parts',33,True)
t(50,1220,'4 mm skin + 1 mm top ribs; underside stays at the existing rim.',27)
t(1450,1220,'45° overlap seams; install RR → RL → FR → FL.',27)
d.rounded_rectangle((43,1292,2757,1415),radius=16,fill='#183449')
t(77,1312,'6U = 266.70 mm',37,True,'#ffffff')
t(706,1312,'Clearance: 1.35 mm',37,True,'#efbb64')
t(1482,1312,'8 × M3×6 + 0.5 mm washers',37,True,'#ffffff')
t(79,1369,'Screw heads peak at 265.05 mm. Nominal CAD dimensions; check the finished print for warp and clearance.',25,False,'#d5e0e8')
im.save(O/'MOE_Lid_Step21_Isometric.png')
print('poster complete',flush=True)
