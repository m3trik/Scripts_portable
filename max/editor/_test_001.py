try: from pymxs import runtime as rt; import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript;from tk_switchboard import Switchboard; sb = Switchboard();from tk_slots_max_init import Init as func;
except: pass



def getModifier(obj, modifier, index=0):
	'''
	Gets (and sets (if needed)) the given modifer for the given object at the given index.
	
	args:
		obj = <object> - the object to add or retrieve the modifier from.
		modifier = 'string' - modifier name.
		index = int - place modifier before given index. default is at the top of the stack.
					Negative indices place the modifier from the bottom of the stack.
	returns:
		modifier
	'''
	m = obj.modifiers[modifier]
	if not m:
		m = getattr(rt, modifier)()
		if index<0:
			index = index+len(obj.modifiers)+1 #
		rt.addModifier(obj, m, before=index)
	if not rt.modPanel.getCurrentObject()==m:
		print rt.modPanel.getCurrentObject(), m
		rt.modPanel.setCurrentObject(m)
	return m


obj = rt.selection[0]
uv = getModifier(obj, 'Unwrap_UVW', -1)
# uv.breakSelected()
# uv.detachEdgeVertices()
# uv.weldSelected()
# uv.WeldAllShared()
# uv.stitchVerts(True, 1.0)
# uv.FlattenBySmoothingGroup(False, False, 0.2)
# uv.pack(1, 0.01, True, False, True) #Lets you pack the texture vertex elements so that they fit within a square space.
# uv.unwrap2.setFreeFormMode(True)
# uv.relax(1, 0.01, True, True)
# uv.straighten()


# rt.subobjectLevel = 2


# kw = ''
# limit = None #int or None - limit amount of returned results.
# print [i for i in dir(uv) if kw in i or kw.title() in i or kw.swapcase() in i or kw.upper() in i or kw.lower() in i][:limit]




['DisplayPixelUnits', 
'MirrorGeomSelection', 'MirrorSelectionAxis', 'MirrorSelectionThreshold', 
'PaintFallOff', 'PaintFallOffType', 'PaintFullStrength', 'PaintMoveBrush', 
'RelaxMoveBrush', 
'SelectionPreview', 
'TextureCheckerMaterial', 
'TypeInLinkUV', 
'autoPin', 
'baseMaterial', 'baseMaterial_list', 
'buttonpanel_height1', 'buttonpanel_height2', 'buttonpanel_visible', 'buttonpanel_width', 
'checkerMaterial', 
'edgeSnap', 
'editorHWnd', 'editorViewHWnd', 
'filterPin', 
'gridSnap', 
'groupDensity', 'groupDisplay', 'groupName', 
'localDistortion', 
'peelAutoEdit', 
'quick_map_align', 'quick_map_preview', 
'renderuv_edgeColor', 'renderuv_edgealpha', 'renderuv_fillColor', 'renderuv_fillalpha', 'renderuv_fillmode', 'renderuv_force2sided', 'renderuv_height', 'renderuv_invisibleedges', 'renderuv_overlapColor', 'renderuv_seamColor', 'renderuv_seamedges', 'renderuv_showframebuffer', 'renderuv_showoverlap', 'renderuv_visibleedges', 'renderuv_width',  
'showImageAlpha', 'showTileGridlines', 
'splinemap_advanceMethod', 'splinemap_display', 'splinemap_iterations', 'splinemap_manualseams', 'splinemap_node', 'splinemap_projectiontype', 'splinemap_resampleCount', 'splinemap_uoffset', 'splinemap_uscale', 'splinemap_voffset', 'splinemap_vscale', 
'texMapIDList', 'texMapList', 
'toolBarVisible', 
'vertexSnap', 
'weldOnlyShared']




# print [i for i in rt.selection]

# #for i in rt.materials:
# #	print i



# obj = rt.selection[0]

# symmetry = obj.modifiers[rt.Symmetry]

# if symmetry:
# 	sym = mod.axis;
# 	if sym==0: axis='x';
# 	if sym==1: axis='y';
# 	if sym==2: axis='z';

# print axis.upper()


#~ creaseAmount = 1



#~ obj = rt.selection[0]

#~ obj.EditablePoly.makeHardEdges(1) #1=flag bit 1 : 'is selected'
#~ obj.EditablePoly.setEdgeData(1, creaseAmount)

# def bitArrayIndex(bitArray):
# 	return [i for i, bit in enumerate(bitArray) if bit==1]


# creaseAmount = 5*0.1

# for obj in rt.selection:
# 	obj.EditablePoly.setEdgeData(1, creaseAmount)

# 	edges = bitArrayIndex(rt.polyop.getEdgeSelection(obj))
# 	print edges
# 	for edge in edges:
# 		print edge
# 		edgeVerts = rt.polyop.getEdgeVerts(obj, edge)
# 		normal = rt.averageSelVertNormal(obj)
# 		for vertex in edgeVerts:
# 			rt.setNormal(obj, vertex, normal)

#~ print bitIndex([0,0,1,1])




#~ for obj in rt.selection:
	#~ vertices = [i.index for i in obj.selectedVerts]

	#~ target = rt.polyOp.getVert(obj, vertices[-1])
	#~ for v in vertices[1:]:
		#~ rt.polyop.weldVerts (obj, vertices[0], v, target)



# print func.tk('classInfo')



# @staticmethod
# def toggleSmoothPreview():
# 	toggle = func.cycle([0,1], 'toggleSmoothPreview') #toggle 0/1

# 	geometry = rt.selection #if there is a selection; perform operation on those object/s
# 	if not len(geometry): #else: perform operation on all scene geometry.
# 		geometry = rt.geometry



# 	for obj in geometry:
# 		if toggle==0: #preview off
# 			level = tkDict['previousSmoothPreviewLevel']
# 			func.setSubObjectLevel(level) #restore previous subObjectLevel
# 			obj.modifiers['TurboSmooth'].iterations = 0 #set subdivision levels to 0.
# 			func.displayWireframeOnMesh(True)

# 		else: #preview on
# 			tkDict['previousSmoothPreviewLevel'] = rt.subObjectLevel #store previous subObjectLevel
# 			func.setSubObjectLevel(0)
# 			renderIters = obj.modifiers['TurboSmooth'].renderIterations #get renderIter value.
# 			obj.modifiers['TurboSmooth'].iterations = renderIters #apply to iterations value.
# 			func.displayWireframeOnMesh(False)

# toggleSmoothPreview()
