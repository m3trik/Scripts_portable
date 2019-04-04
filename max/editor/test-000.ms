


-- convert component selection type

-- obj = selection[1] --get selected object

-- vertices = getVertSelection obj --get selected Vertices
-- edges = polyop.getEdgesUsingVert obj vertices

-- setEdgeSelection obj edges --select the edges

-- max modify mode --switch to Modify panel
-- subObjectLevel =2 --edge selection mode
-- select(edges)


python """

for obj in rt.geometry:
	try:
		if obj.modifiers['TurboSmooth'].iterations:
			obj.modifiers['TurboSmooth'].iterations = 0
		else:
			renderIters = obj.modifiers['TurboSmooth'].renderIterations
			obj.modifiers['TurboSmooth'].iterations = renderIters
	except: pass
		
		"""


