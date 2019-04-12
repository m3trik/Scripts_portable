-- -- clean up unused vertices
macroScript Vertex_cleaner category:"Shiva Tools" tooltip:"Vertex Cleaner 1.0 by Shiva"
(



global rltVertexCleaner
local  vx_2edges = #()
local vx_weight = #()
local  vx_selected = #()


fn vx_sort trash_val =
(

if  vx_2edges.count > 0 do (
			vx_selected = #()			
			for i = 1 to vx_2edges.count do	(				 
				if vx_weight[i] <= ( trash_val / 50 ) then append vx_selected vx_2edges[i]		
				)	--end of FOR i
			polyop.setvertselection $ vx_selected
			redrawViews()	
			
			)	--end of IF
)


try destroyDialog rltVertexCleaner catch()

rollout rltVertexCleaner "VertexCleaner" width:180 height:20
(
	spinner tresh "Threshold:" pos:[20,1] width:90 height:20 range:[0,100,10] type:#float enabled:true
	button btnCreate "Clean it!" pos:[110,1] width:50 height:16 tooltip:"start cleaning" enabled:true
	hyperLink homepage "?" address:"http://www.shiva3d.net/" pos:[165,1] 
	

	on tresh changed val do
	(
		vx_sort ( tresh.value )
	)
	
	
	on btnCreate pressed do
	(
		undo on(
		
					vx_sort ( tresh.value )
					polyop.setvertselection $  vx_selected
					$.EditablePoly.Remove ()
					redrawViews()	
		) -- end undo


	try destroyDialog rltVertexCleaner catch()
	str = "Vertices removed: " +  vx_selected.count as string
	messagebox str title:"Result"
	
	)	-- end on btnCreate pressed

)	-- end rollout rltVertexCleaner



if classof $ == Editable_poly then 
	(
	if subobjectlevel == 1 then 
		(     -- start the action
			
		sel = polyop.getVertSelection $  -- get the selected vertices
		selcount = sel as array

		for i = 1 to selcount.count do		-- collecting all vertex with 2 edges
			(
			vi = selcount[i]
			edg = polyOp.getEdgesUsingVert $ vi  -- get the edges that use the vertice
			quantos = edg as array
			if quantos.count  == 2 then 
				(
				append vx_2edges vi
				
				
				polyop.setvertselection $ vi
				vi_pos = polyop.getVert $ vi				

				vmass1 = polyop.getVertsUsingEdge $ quantos[1] as array
				if vmass1[1] == vi then vi_1 = vmass1[2] else vi_1 = vmass1[1]
				vi_1_vec = normalize( polyop.getVert $ vi_1 - vi_pos )
					
				vmass2 = polyop.getVertsUsingEdge $ quantos[2] as array
				if vmass2[1] == vi then vi_2 = vmass2[2] else vi_2 = vmass2[1]
				vi_2_vec = normalize( polyop.getVert $ vi_2 - vi_pos )
					
				vi_fin = length ( vi_1_vec + vi_2_vec )
				
				append vx_weight vi_fin
				
				) -- end of IF
			) -- end of For i

	--	polyop.setvertselection $ vx_2edges
	--	redrawViews()	
			
		createDialog rltVertexCleaner  180 18 ( mouse.screenpos.x - 100 ) ( mouse.screenpos.y - 20 )
	
		vx_sort ( rltVertexCleaner.tresh.value )
		
		)
	else messagebox "You should select vertices first." title: "Vertex Cleaner"
	)
	else messagebox "The object selected isn't a editable poly or nothing is selected." title: "Vertex Cleaner"
)












-- macroScript SelEdgesByAngle 
--     category:"PolyMeshTools" 
--     buttontext:"Edges By Angle"
--     tooltip:"Select Edges By Angle"
--    (
--    	local theThreshold = 30
--    	local include_open_edges = false	
--    	local auto_preview_selection = true
--    	fn filter_function =
--    	(
--    		theObj = modPanel.getCurrentObject()
--  	subObjectLevel == 2 and selection.count == 1 and (classof theObj == Editable_Poly or (classof theObj == Edit_Poly and theObj.enabled and theObj.enabledInViews))
--    	)
--    	on isEnabled return filter_function()
--    	on isVisible return filter_function()
--    	
--    	fn perform_selection =
--    	(
--    		selEdges = #{}
--    		theObj = $
--    		
--    		eCount = polyOp.getNumEdges theObj
--    		for e = 1 to eCount do
--    		(
--    			theFaces = (polyOp.getEdgeFaces theObj e) as array
--    			if theFaces.count == 2 then
--    			(
--  			 theAngle = acos(dot (polyOp.getFaceNormal theObj theFaces[1]) (polyOp.getFaceNormal theObj theFaces[2])) 
--  				if theAngle >= theThreshold do selEdges[e] = true
--    			)	
--    			else 
--  				if include_open_edges do selEdges[e] = true
--    		)
--    		case classof (modPanel.getCurrentObject()) of
--    		(
--  			Editable_Poly: polyOp.setEdgeSelection theObj selEdges 
--   		    Edit_Poly: (modPanel.getCurrentObject()).SetSelection #Edge &selEdges 
--    		)	
--    		redrawViews()	
--    	)
--    
--    	on execute do perform_selection()
--    	
--    	on altExecute theType do
--    	(
--    		rollout SelEdgesByAngle_Rollout "Select Edges By Angle"
--    		(
--  			checkbox include_open "Include Open Edges" checked:include_open_edges
--  		 spinner threshold_value "Angle Threshold" range:[0,180,theThreshold] type:#float fieldwidth:60
--  		 checkbutton preview_selection "Preview" width:85 across:2 align:#left checked:auto_preview_selection
--    			button select_now "Update" width:85 align:#right
--    			on threshold_value changed val do 
--    			(
--    				theThreshold = val
--  			if preview_selection.checked and filter_function() do perform_selection()
--    			)	
--    			on include_open changed state do 
--    			(
--    				include_open_edges = state
--  				if filter_function() do perform_selection()
--    			)	
--  			on preview_selection changed state do auto_preview_selection = state
--  			on select_now pressed do if filter_function() do perform_selection()
--    		)
--    		createDialog SelEdgesByAngle_Rollout 200 70 
--    	)
--    )






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






----------------------------------------------------------------------------------------
--   Script Name:	MeshDetails
--	 Version:		v0.21
--	 Started:       02/16/01
--	 Last Modified: 02/19/01
--   Description:	Displays Face Material IDs, Vertex and Face 
--					Indices of Mesh Objects in the Viewport
--	 Code by:		Borislav Petrov [Boboland]		bobo@email.archlab.tuwien.ac.at
--   Idea by:       Michael Franck
----------------------------------------------------------------------------------------


-- -- macroscript MeshDetails category:"Bobo_s Tools"
-- (

-- global mesh_details_floater,mesh_details_roll

-- fn update_mid_display obj mode offset use_sel =
-- (
-- m_ver = maxversion()
-- m_ver = m_ver[1]
-- gw.setTransform(Matrix3 1) 
-- try
-- (
-- if mode > 3 then
-- (
-- num_verts = obj.mesh.numverts
-- vert_sel = getvertselection obj.mesh
-- for v = 1 to num_verts do
-- (
-- 	if vert_sel[v] == true or not use_sel then
-- 	(
-- 	txt = "MeshDetails: "+ (v as string) +" / " +  (num_verts as string)
-- 	pushprompt txt
-- 	mesh_details_roll.prog_display.value = (100.0*v/num_verts)
-- 	in coordsys local 
-- 	(
-- 	vert_mid = getvert obj.mesh v
-- 	norm = getnormal obj.mesh v
-- 	)
-- 	in coordsys world vert_mid += (norm*offset)
-- 	vert_mid *= obj.transform
-- 	
-- 		if m_ver < 4000 then 
-- 		gw.text vert_mid (v as string) 
-- 		else		
-- 		gw.text vert_mid (v as string) color:((color 100 100 255)*v/num_verts)
-- 	)	
-- )--end v loop		
-- )
-- else
-- (
-- num_faces = obj.mesh.numfaces
-- face_sel = getfaceselection obj.mesh
-- last_id = 0
-- for f = 1 to num_faces  do
-- (
-- 	if face_sel[f] == true or not use_sel then
-- 	(
-- 	txt = "MeshDetails: "+ (f as string) +" / " +  (num_faces as string)
-- 	pushprompt txt
-- 	mesh_details_roll.prog_display.value = (100.0*f/num_faces)
-- 	face = getface obj.mesh f
-- 	m_id = getfacematId obj.mesh f
-- 	if m_id != last_id or mode != 1 then
-- 	(
-- 		
-- 		in coordsys local 
-- 		(
-- 			norm = getfacenormal obj.mesh f
-- 			vert1 = getvert obj.mesh face.x
-- 			vert2 = getvert obj.mesh face.y
-- 			vert3 = getvert obj.mesh face.z
-- 		)
-- 		vert_mid = (vert1+vert2+vert3)/3.0
-- 		in coordsys world vert_mid += (norm*offset)
-- 	
-- 		vert_mid *= obj.transform
-- 		if mode < 3 then
-- 		(
-- 		if m_ver < 4000 then 
-- 		gw.text vert_mid (m_id as string) 
-- 		else		
-- 		gw.text vert_mid (m_id as string) color:(color 255 255 100)
-- 		)
-- 		if mode == 3 then
-- 		(
-- 		if m_ver < 4000 then 
-- 		gw.text vert_mid (f as string) 
-- 		else		
-- 		gw.text vert_mid (f as string) color:((color 100 255 100)*f/num_faces)
-- 		)
-- 	)--end if
-- 	)
-- 	last_id = m_id
-- )--end f loop
-- )--end if mode 4
-- )--end try
-- catch()
-- )--end fn


-- rollout mesh_details_roll "MeshDetails"
-- (
-- radiobuttons detail_mode "Display" labels:#("Material ID Groups","All Material IDs","Face Index","Vertex Index")
-- spinner n_offset "Normal Offset" range:[0,100,5] fieldwidth:35
-- checkbox use_selection "SubObject Sel. Only"
-- button display_it "UPDATE DISPLAY" height:30 width:120 align:#center
-- progressbar prog_display height:6 width:120 align:#center

-- on display_it pressed do
-- (
-- max views redraw
-- s_t = timestamp()
-- for obj in selection do
-- (
-- update_mid_display obj detail_mode.state n_offset.value use_selection.state
-- )--end obj loop
-- gw.enlargeUpdateRect #whole 
-- gw.updateScreen() 
-- e_t = timestamp()
-- txt = "MeshDetails Ready in " + (e_t-s_t) as string +"ms."
-- pushprompt txt
-- mesh_details_roll.prog_display.value = 0
-- )--end on
-- )--end roll

-- try(closerolloutfloater mesh_details_floater)catch()
-- mesh_details_floater = newrolloutfloater "MeshDetails" 160 240 100 100
-- addrollout mesh_details_roll mesh_details_floater
-- )--end script
