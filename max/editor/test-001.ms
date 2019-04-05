
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