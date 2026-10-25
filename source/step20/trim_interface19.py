import cadquery as cq
s=cq.importers.importStep('V620_Two_GPU_Interface.step').val()
prisms=[]
for f in s.Faces():
 b=f.BoundingBox()
 if abs(b.ymin+23)<1e-4 and abs(b.ymax+23)<1e-4:
  prisms.append(cq.Solid.extrudeLinear(f.outerWire(),f.innerWires(),cq.Vector(0,43.001,0)))
t=s.intersect(cq.Compound.makeCompound(prisms),tol=.0001).clean()
cq.exporters.export(t,'V620_Trimmed_Interface_Step19.step')
cq.exporters.export(s.cut(t,tol=.0001),'V620_Interface_Trim_Removed_Reference.step')
print('trimmed',t.isValid(),len(t.Solids()),'volume removed',s.Volume()-t.Volume())
for f in t.Faces():
 n=f.normalAt();b=f.BoundingBox()
 if n.y<-.65:print('Downface',round(f.Area(),3),tuple(round(v,3) for v in n.toTuple()),[round(v,3) for v in (b.xmin,b.xmax,b.ymin,b.ymax,b.zmin,b.zmax)])
