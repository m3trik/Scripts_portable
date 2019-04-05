

-- convert component selection type

-- obj = selection[1] --get selected object

-- vertices = getVertSelection obj --get selected Vertices
-- edges = polyop.getEdgesUsingVert obj vertices

-- setEdgeSelection obj edges --select the edges

-- max modify mode --switch to Modify panel
-- subObjectLevel =2 --edge selection mode
-- select(edges)


-- create an initial list of edge pairs so that it works for multiple loops.
-- (
-- 	$.convertselection #Face #Edge
-- 	_edges = (polyop.getEdgeSelection $) as array
-- 	_faces = (polyop.getFaceSelection $) as array
-- 	for i in _edges do 
-- 	(
-- 		if ((($.getEdgeFace i 1) == _faces[1] and ($.getEdgeFace i 2) == _faces[2]))
-- 		then
-- 		(
-- 			polyop.setEdgeSelection $ i
-- 			$.SelectEdgeRing()
-- 			$.convertselection #Edge #Face
-- 		)
-- 	)
-- )
-- import tk_slots_max_init.Slots.py as Slots 

-- slots = Slots()


-- print slots.classInfo(obj)













-- re-create "Get All Scene Materials"

-- sme.DeleteView 1 -- empty out the views
-- sme_view = sme.GetView (sme.CreateView "AllMaterials") -- create a new view
-- for mat in sceneMaterials do (
-- 	sme_view.createNode mat [0,0]
-- )

-- actionMan.executeAction 369891408 "40060"  -- SME: Lay Out All
