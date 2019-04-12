
-- select edges within threshold

theThreshold = 50
include_open_edges = false

selEdges = #{}
theObj = $

eCount = polyOp.getNumEdges theObj
for e = 1 to eCount do
(
	theFaces = (polyOp.getEdgeFaces theObj e) as array
	if theFaces.count == 2 then
	(
	 theAngle = acos(dot (polyOp.getFaceNormal theObj theFaces[1]) (polyOp.getFaceNormal theObj theFaces[2])) 
		if theAngle >= theThreshold do selEdges[e] = true
	)	
	else 
		if include_open_edges do selEdges[e] = true
)
case classof (modPanel.getCurrentObject()) of
(
	Editable_Poly: polyOp.setEdgeSelection theObj selEdges 
	Edit_Poly: (modPanel.getCurrentObject()).SetSelection #Edge &selEdges 
)	
redrawViews()




-- -- Chamfer

-- modPanel.setCurrentObject $.modifiers[#Chamfer]
-- $.modifiers[#Chamfer].selectionoption = 1 --from selected edges
-- $.modifiers[#Chamfer].smoothingoption = 2
-- $.modifiers[#Chamfer].materialoption = 0
-- $.modifiers[#Chamfer].minangle = 30
-- $.modifiers[#Chamfer].useminangle = off
-- $.modifiers[#Chamfer].setmaterial = on
-- $.modifiers[#Chamfer].smoothtoadjacent = off
-- $.modifiers[#Chamfer].SmoothType = 1
-- $.modifiers[#Chamfer].smoothtoadjacent = off
-- $.modifiers[#Chamfer].smooththreshold = 45

