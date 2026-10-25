from pathlib import Path
import sys,json
import cadquery as cq
from PIL import Image,ImageDraw,ImageFont

R=Path(__file__).parent;O=R/'duct_bar22';S=R/'assembly_sources/project'
sys.path.insert(0,str(S/'Sources'))
from software_render_views import render
BLUE=(.53,.67,.77);GOLD=(.94,.66,.22);DARK=(.34,.40,.45);STEEL=(.73,.75,.77)
bar=cq.importers.importStep(str(O/'MOE_Duct_Retaining_Bar_Step22.step')).val()
ctx=cq.importers.importStep(str(O/'MOE_Duct_Retaining_Bar_Step22_Context.step')).val()
ch=cq.importers.importStep(str(S/'References/6U_Chassis_Step_16.step')).val()
ducts=[cq.importers.importStep(str(S/f'Parts/Duct20_PAIR_{p}_DUCT.step')).val().translate((0,5,0)) for p in 'AB']
def box(x,y,z,a,b,c):return cq.Solid.makeBox(a,b,c,cq.Vector(x,y,z))
def cyl(r,h,x,y,z):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z),cq.Vector(0,1,0))
fans=[]
for x in (252,372):
 for z in (79.05,199.05):
  f=box(x-60,485,z-60,120,25,120).cut(cyl(57.5,25,x,485,z))
  for dx in (-52.5,52.5):
   for dz in (-52.5,52.5):f=f.cut(cyl(1.7,25,x+dx,485,z+dz))
  fans.append(f)
hw=[s for s in ctx.Solids() if s.BoundingBox().xlen<8 and s.BoundingBox().ylen<49 and s.BoundingBox().zmax<33]

# True geometry, no generated imagery. New print highlighted in gold.
render([(bar,GOLD,1)],O/'Step22_Bar_Isometric.png',(-1000,1000,1000),(312,517,30),86,size=(1100,730))
print('bar render',flush=True)
clip=box(185,455,0,255,92,112)
items=[(ch.intersect(clip),BLUE,1),(bar,GOLD,1)]
items += [(d.intersect(clip),BLUE,1) for d in ducts]
items += [(f.intersect(clip),DARK,1) for f in fans if f.BoundingBox().zmin<40]
items += [(h,STEEL,1) for h in hw]
render(items,O/'Step22_Mount_Detail.png',(-1000,1000,1000),(312,502,60),110,size=(1100,660))
print('detail render',flush=True)

# Side elevation is a dimensional CAD projection of the same BReps.
# Trace hidden-line-free silhouette edges via section outlines, with an exact
# datum sketch beneath the two isometrics for unambiguous fore-aft direction.
im=Image.new('RGB',(2200,1210),'#f6f8fa');d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans'
def t(x,y,s,n=26,b=False,col='#243d50'):
 d.text((x,y),s,font=ImageFont.truetype(font+('-Bold' if b else '')+'.ttf',n),fill=col)
t(40,26,'MOE / LOW DUCT RETAINING BAR',44,True)
t(42,86,'STEP 22  •  Gold = new print  •  Two existing floor inserts  •  No new heatserts',27)
im.paste(Image.open(O/'Step22_Bar_Isometric.png'),(0,131))
im.paste(Image.open(O/'Step22_Mount_Detail.png'),(1100,131))
t(45,822,'ONE PART / 240 × 19 × 24 mm',28,True)
t(1145,822,'INSTALLED DETAIL / lower fan corners captured',27,True)
t(45,867,'Two Ø120 scallops; 2 mm sole along the frame bottoms.',23)
t(1145,867,'Upper fans and upper duct geometry hidden for visibility.',23)

d.rounded_rectangle((40,927,2160,1168),radius=15,fill='#183449')
t(66,950,'CONFIRMED POSITION',27,True,'#efbb64')
t(66,997,'Fan intake face: 10 mm behind floor-insert centers.',28,True,'#ffffff')
t(66,1044,'Feet point forward, toward the six chassis intake fans.',24,False,'#d8e3ec')
t(66,1086,'Bench-fit the bar; lower the assembly; tighten two screws from above.',23,False,'#d8e3ec')

# Exact scaled side datum; rear left / front right, with physical parts to
# scale in Y. Z is compressed to show only the mounting region.
x0,ybase=1515,1101; k=12
def px(y):return x0+(y-510)*k
floor=19.05
def pz(z):return ybase-(z-floor)*4
d.rectangle((px(499),pz(42),px(510),pz(floor)),fill='#566f80',outline='#b5c9d8',width=2)
d.rectangle((px(510),pz(43.05),px(516),pz(floor)),fill='#e9aa47')
d.rectangle((px(514),pz(23.05),px(529),pz(floor)),fill='#e9aa47')
d.line((px(496),ybase,px(533),ybase),fill='#d8e3ec',width=3)
d.line((px(520),pz(30),px(520),ybase+16),fill='#ffffff',width=3)
d.line((px(510),953,px(520),953),fill='#ffffff',width=2)
for x in (px(510),px(520)):d.line((x,944,x,968),fill='#ffffff',width=2)
t(px(510)+6,962,'10 mm',22,True,'#ffffff')
t(px(499)-70,1121,'REAR  ←',21,True,'#d8e3ec')
t(px(520)+15,1121,'→  FRONT',21,True,'#d8e3ec')
im.save(O/'MOE_Duct_Retaining_Bar_Step22_Views.png')
print('poster complete',flush=True)
