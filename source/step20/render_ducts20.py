from pathlib import Path
import cadquery as cq,json
from PIL import Image,ImageDraw,ImageFont
from software_render_views import render
O=Path(__file__).parent;gold=(.90,.63,.22);blue=(.56,.69,.78);gray=(.34,.38,.42)
parts={n:cq.importers.importStep(str(O/f'Duct20_{n}.step')).val() for n in json.loads((O/'ducts20_manifest.json').read_text())['part_names']}
ch=cq.importers.importStep(str(O/'6U_Chassis_Step_16.step')).val();fans=cq.importers.importStep(str(O/'Duct18_Fan_Envelopes_Reference.step')).val()
clip=cq.Solid.makeBox(450,590,145,cq.Vector(0,0,0));region=cq.Solid.makeBox(500,40,280,cq.Vector(0,444.99,0))
items=[(ch.intersect(clip),blue,1),(fans,gray,1)]
for n,p in parts.items():
 if n.endswith('_DUCT'):items.extend([(p.cut(region),blue,1),(p.intersect(region),gold,1)])
 else:items.append((p,blue,1))
render(items,O/'qa_duct20_context.png',(-1000,1000,1000),(222,292,100),350,size=(1200,1000))
p=parts['PAIR_A_DUCT'].intersect(region)
render([(p,gold,1)],O/'qa_duct20_detail.png',(1000,-1000,1000),(252,462,139),145,size=(1100,1000))
im=Image.new('RGB',(2300,1280),'#f6f8fa');im.paste(Image.open(O/'qa_duct20_context.png'),(0,120));im.paste(Image.open(O/'qa_duct20_detail.png'),(1200,120));d=ImageDraw.Draw(im)
def t(x,y,s,n=25,b=False):d.text((x,y),s,font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if b else '')+'.ttf',n),fill='#243d50')
t(35,25,'STEP 20 / EXPOSED FAN MOUNTING CORNERS',38,True)
t(35,80,'Gold: rounded fan-end recesses • four accessible M3 mounting holes per fan',28)
t(35,1130,'Installed assembly • chassis cutaway',28,True)
t(1230,1130,'Two-fan module • viewed from the duct side',27,True)
t(35,1175,'Fan positions, GPU interfaces and cradles retained.',25)
t(1230,1175,'Main taper hidden to expose all eight corner recesses.',24)
t(35,1220,'R5 corner recesses • Ø3.4 mm through holes • 105 × 105 mm pattern • 6 mm screw-bearing thickness',26)
im.save(O/'V620_Duct_System_Step20_Isometric.png')
print('Step20 render complete')
