from __future__ import print_function
from builtins import super
from PySide2 import QtGui

from widgets.qMenu_ import QMenu_
from widgets.qLabel_ import QLabel_
from widgets.qComboBox_ import QComboBox_
from widgets.qCheckBox_ import QCheckBox_
from widgets.qToolButton_ import QToolButton_
from widgets.qWidget_MultiWidget import QWidget_MultiWidget as MultiWidget

import os
from tk_slots_ import Slots

#maya dependancies
try:
	import maya.mel as mel
	import pymel.core as pm
	import maya.OpenMayaUI as omUI

	import shiboken2

except ImportError as error:
	print(error)




class Init(Slots):
	'''
	App specific methods inherited by all other slot classes.
	'''
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)


	def info(self):
		'''
		Get current scene attributes. Only those with relevant values will be displayed.

		returns:
			{dict} - current object attributes.
		'''
		infoDict={}
		try:
			selection = pm.ls(selection=1)
		except NameError:
			return infoDict

		symmetry = pm.symmetricModelling(query=1, symmetry=1);
		if symmetry: axis = pm.symmetricModelling(query=1, axis=1); infoDict.update({'Symmetry Axis: ':axis.upper()}) #symmetry axis

		xformConstraint = pm.xformConstraint(query=True, type=True)
		if xformConstraint=='none': xformConstraint=None; infoDict.update({'Xform Constrait: ':xformConstraint}) #transform constraits

		if selection:
			if pm.selectMode(query=1, object=1): #object mode:
				if pm.selectType(query=1, allObjects=1): #get object/s

					selectedObjects = pm.ls(selection=1, objectsOnly=1)
					name_and_type = ['{0} : {1}'.format(i.name(), pm.objectType(i)) for i in selectedObjects] #ie. ['pCube1:transform', 'pSphere1:transform']
					infoDict.update({'Selection: ':name_and_type}) #currently selected objects by name and type.

					objectFaces = pm.polyEvaluate(selectedObjects, face=True)
					if type(objectFaces)==int:
						infoDict.update({'Faces: ':format(objectFaces, ',d')}) #add commas each 3 decimal places.

					# objectTris = pm.polyEvaluate(selectedObjects, triangle=True)
					# if type(objectTris)==int:
					# 	infoDict.update({'Tris: ':format(objectTris, ',d')}) #add commas each 3 decimal places.

			elif pm.selectMode(query=1, component=1): #component mode:
				if pm.selectType(query=1, vertex=1): #get vertex selection info
					vertices = pm.filterExpand(selectionMask=31)
					selectedVerts = [v.split('[')[-1].rstrip(']') for v in vertices] if vertices else [] #pm.polyEvaluate(vertexComponent=1);
					collapsedList = self.collapseList(selectedVerts, limit=6)
					numVerts = pm.polyEvaluate (selection[0], vertex=1)
					infoDict.update({'Vertices: '+str(len(selectedVerts))+'/'+str(numVerts):collapsedList}) #selected verts

				elif pm.selectType(query=1, edge=1): #get edge selection info
					edges = pm.filterExpand(selectionMask=32)
					selectedEdges = [e.split('[')[-1].rstrip(']') for e in edges] if edges else [] #pm.polyEvaluate(edgeComponent=1);
					collapsedList = self.collapseList(selectedEdges, limit=6)
					numEdges = pm.polyEvaluate (selection[0], edge=1)
					infoDict.update({'Edges: '+str(len(selectedEdges))+'/'+str(numEdges):collapsedList}) #selected edges

				elif pm.selectType(query=1, facet=1): #get face selection info
					faces = pm.filterExpand(selectionMask=34)
					selectedFaces = [f.split('[')[-1].rstrip(']') for f in faces] if faces else [] #pm.polyEvaluate(faceComponent=1);
					collapsedList = self.collapseList(selectedFaces, limit=6)
					numFaces = pm.polyEvaluate (selection[0], face=1)
					infoDict.update({'Faces: '+str(len(selectedFaces))+'/'+str(numFaces):collapsedList}) #selected faces


			# selectedUVs = pm.polyEvaluate(uvComponent=1); 
			# if type(selectedUvs)==int: infoDict.update({"Selected UV's: ":selectedUVs}) #selected uv's

		prevCommand = self.sb.prevCommand(docString=True); infoDict.update({"Prev Command: ":prevCommand})  #get button text from last used command
		# prevUi = self.sb.previousName(omitLevel=[0,1,2]); infoDict.update({"Prev UI: ":prevUi.replace('_', '').title()})  #get the last level 3 ui name string.
		# prevCamera = self.sb.prevCamera(docString=True); infoDict.update({"Prev Camera: ":prevCamera})  #get the previously used camera.

		return infoDict



	@staticmethod
	def loadPlugin(plugin):
		'''
		Loads A Plugin.
		
		args:
			plugin (str) = The desired plugin to load.

		ex. loadPlugin('nearestPointOnMesh')
		'''
		not pm.pluginInfo(plugin, query=True, loaded=True) and pm.loadPlugin(plugin)


	# ------------------------------------------------
	' Geometry'
	# ------------------------------------------------

	@staticmethod
	def getSelectedComponents(type_='vertices'):
		'''
		Get the component selection of the given type.
		'''
		types = {'vertices':31, 'edges':32, 'faces':34}

		components = pm.filterExpand(selectionMask=types[type_])
		selectedComponents = [c.split('[')[-1].rstrip(']') for c in components] if components else []

		return selectedComponents


	@staticmethod
	def getComponents(obj, type_='vertices'):
		'''
		Get the components of the given type from the given object.
		'''
		types = {'vertices':'vtx', 'edges':'e', 'faces':'f'}

		component = getattr(obj, types[type_])
		components = [component[n] for n in xrange(pm.polyEvaluate(obj, vertex=True))]

		return components


	@staticmethod
	def getNGons(obj, repair=False):
		'''
		Get any N-Gons from the given object.
		'''
		if nGons: #N-Sided Faces
			if repair: #Maya Bonus Tools: Convert N-Sided Faces To Quads
				try:
					mel.eval('bt_polyNSidedToQuad;')
				except:
					print('Maya Bonus Tools: Convert N-Sided Faces To Quads not found. (bt_polyNSidedToQuad;)')

			else: #Find And Select N-Gons
				pm.select(obj)
				#Change to Component mode to retain object highlighting for better visibility
				pm.changeSelectMode(component=1)
				#Change to Face Component Mode
				pm.selectType(smp=0, sme=1, smf=0, smu=0, pv=0, pe=1, pf=0, puv=0)
				#Select Object/s and Run Script to highlight N-Gons
				pm.polySelectConstraint(mode=3, type=0x0008, size=3)
				pm.polySelectConstraint(disable=1)
				#Populate an in-view message
				nGons = pm.polyEvaluate(faceComponent=1)
				self.viewPortMessage("<hl>"+str(nGons[0])+"</hl> N-Gon(s) found.")


	@staticmethod
	def getBorderFaces(faces, includeBordered=False):
		'''
		Get any faces attached to the given faces.
		args:
			faces (unicode, str, list) = faces to get bordering faces for.
			includeBordered (bool) = optional. return the bordered face with the results.
		returns:
			list - the border faces of the given faces.
		'''
		adjEdges = pm.polyListComponentConversion(faces, fromFace=1, toEdge=1)
		adjFaces = pm.polyListComponentConversion(adjEdges, toFace=1, fromEdge=1)
		expanded = pm.filterExpand(adjFaces, expand=True, selectionMask=34) #keep faces as individual elements.

		if includeBordered:
			return list(str(f) for f in expanded) #convert unicode to str.
		else:
			return list(str(f) for f in expanded if f not in faces) #convert unicode to str and exclude the original faces.


	@staticmethod
	def getContigiousIslands(faces, faceIslands=[]):
		'''
		Get a list containing sets of adjacent polygon faces grouped by islands.
		args:
			faces (list) = polygon faces to be filtered for adjacent.
			faceIslands (list) = optional. list of sets. ability to add faces from previous calls to the return value.
		returns:
			list of sets of adjacent faces.
		'''
		l=[]
		for face in faces:
			borderFaces = Init.getBorderFaces(face, includeBordered=1)
			l.append(set(f for f in borderFaces if f in faces))

		while len(l)>0: #combine sets in 'l' that share common elements.
			first, rest = l[0], l[1:] #python 3: first, *rest = l
			first = set(first)

			lf = -1
			while len(first)>lf:
				lf = len(first)

				rest2 = []
				for r in rest:
					if len(first.intersection(set(r)))>0:
						first |= set(r)
					else:
						rest2.append(r)     
				rest = rest2

			faceIslands.append(first)
			l = rest

		return faceIslands


	@staticmethod
	def getAllFacesOnAxis(obj, axis="-x", localspace=False):
		'''
		Get all faces on a specified axis

		args:
			obj=<geometry> - object to perform the operation on. 
			axis (str) = representing axis ie. "x"
			localspace=bool - specify world or local space
		ex. self.getAllFacesOnAxis(polyObject, 'y')
		'''
		i=0 #'x'
		if any ([axis=="y",axis=="-y"]):
			i=1
		if any ([axis=="z",axis=="-z"]):
			i=2

		if axis.startswith('-'): #any([axis=="-x", axis=="-y", axis=="-z"]):
			return list(face for face in pm.filterExpand(obj+'.f[*]', sm=34) if pm.exactWorldBoundingBox(face)[i] < -0.00001)
		else:
			return list(face for face in pm.filterExpand(obj+'.f[*]', sm=34) if pm.exactWorldBoundingBox(face)[i] > -0.00001)


	@staticmethod
	def getBorderEdgeFromFace(faces=None):
		'''
		Get border edges from faces. (edges not shared by any other face)

		args:
			faces (str, unicode, list) = ie. 'poly.f[696]' or ['polyShape.f[696]']. If no arguement is given, the current selection will be used.
		returns:
			list of border edges.
		ex. getBorderEdgeFromFace(['poly.f[696]', 'poly.f[705:708]'])
		'''
		if not faces: #if no faces passed in as arg, get current face selection
			faces = list(str(f) for f in pm.filterExpand(selectionMask=34))

		edges = list(str(i).replace('Shape.', '.', -1).split('|')[-1] for i in pm.ls(pm.polyListComponentConversion(faces, ff=1, te=1), flatten=1)) #get edges from the faces

		borderEdges=[]
		for edge in edges:
			edgeFaces = list(str(i).replace('Shape.', '.', -1).split('|')[-1] for i in pm.ls(pm.polyListComponentConversion(edge, fe=1, tf=1), flatten=1)) #get faces that share the edge.

			if len(edgeFaces)<2: #if the edge has only one shared face, it is a border edge.
				borderEdges.append(edge)
			else:
				for f in edgeFaces:
					if f not in faces: #else if the edge's shared face is not part of the selected faces, it is a border edge.
						borderEdges.append(edge)
						break

		return borderEdges


	@staticmethod
	def getVectorLength(x, y):
		'''
		Get the Magnitude of a Vector.

		args:
			x (tuple) = Point X.
			y (tuple) = Point Y.

		returns:
			(float) Magnitude Of The Vector.
		'''
		import math
		dX = x[0] - y[0]
		dY = x[1] - y[1]
		dZ = x[2] - y[2]

		length = math.sqrt( dX * dX + dY * dY + dZ * dZ )

		return length


	@staticmethod
	def getClosestVerts(set1, set2, tolerance=100):
		'''
		Find the two closest vertices between the two sets of vertices.

		args:
			set1 (list) = The first set of vertices.
			set2 (list) = The second set of vertices.
			tolerance (int) = Maximum search distance.

		returns:
			(set) closest vertex pair (<vertex from set1>, <vertex from set2>).
		'''
		closestDistance=tolerance
		closestVerts=None
		for v1 in set1:
			v1Pos = pm.pointPosition(v1, world=1)
			for v2 in set2:
				v2Pos = pm.pointPosition(v2, world=1)
				distance = Init.getVectorLength(v1Pos, v2Pos)

				if distance < closestDistance:
					closestDistance = distance
					if closestDistance < tolerance:
						closestVerts = (v1, v2)

		return closestVerts


	@staticmethod
	def getClosestVertex(vertices, obj, tolerance=10.0, freezeTransforms=False):
		'''
		Find the closest vertices from one set of vertices and the vertices of an object.

		args:
			vertices (list) = A set of vertices.
			obj (obj) = The reference object in which to find the closest vertex for each vertex in the list of given vertices.
			tolerance (float) = Maximum search distance.
			freezeTransforms (bool) = Reset the selected transform and all of its children down to the shape level.

		returns:
			(dict) closest vertex pairs {<vertex from set1>:<vertex from set2>}.

		ex. obj1, obj2 = selection
			vertices = Init.getComponents(obj1, 'vertices')
			closestVerts = getClosestVertex(vertices, obj2, tolerance=10)
		'''
		pm.undoInfo(openChunk=1)
		if freezeTransforms:
			pm.makeIdentity(obj, apply=True)

		obj2Shape = pm.listRelatives(obj, children=1, shapes=1)[0] #pm.listRelatives(obj, fullPath=False, shapes=True, noIntermediate=True)

		cpmNode = pm.ls(pm.createNode('closestPointOnMesh'))[0] #get the closestPointOnMesh node.
		pm.connectAttr(obj2Shape.outMesh, cpmNode.inMesh)

		closestVerts={}
		for v1 in vertices:
			v1Pos = pm.pointPosition(v1, world=True)
			pm.setAttr(cpmNode.inPosition, v1Pos[0], v1Pos[1], v1Pos[2], type="double3") #set a compound attribute

			index = pm.getAttr(cpmNode.closestVertexIndex) #vertex Index. | ie. result: [34]
			v2 = obj2Shape.vtx[index]

			v2Pos = pm.pointPosition(v2, world=True)
			distance = Init.getVectorLength(v1Pos, v2Pos)

			if distance < tolerance:
				closestVerts[v1] = v2

		pm.delete(cpmNode)
		pm.undoInfo(closeChunk=1)

		return closestVerts


	@staticmethod
	def snapClosestVerts(obj1, obj2, tolerance=10.0, freezeTransforms=False):
		'''
		Snap the vertices from object one to the closest verts on object two.

		args:
			obj1 (obj) = The object in which the vertices are moved from.
			obj2 (obj) = The object in which the vertices are moved to.
			tolerance (float) = Maximum search distance.
			freezeTransforms (bool) = Reset the selected transform and all of its children down to the shape level.
		'''
		vertices = Init.getComponents(obj1, 'vertices')
		closestVerts = Init.getClosestVertex(vertices, obj2, tolerance=tolerance, freezeTransforms=freezeTransforms)

		progressBar = mel.eval("$container=$gMainProgressBar");
		pm.progressBar(progressBar, edit=True, beginProgress=True, isInterruptable=True, status="Snapping Vertices ...", maxValue=len(closestVerts)) 

		pm.undoInfo(openChunk=1)
		for v1, v2 in closestVerts.items():
			if pm.progressBar(progressBar, query=True, isCancelled=True):
				break

			v2Pos = pm.pointPosition(v2, world=True)
			pm.xform(v1, translation=v2Pos, worldSpace=True)

			pm.progressBar(progressBar, edit=True, step=1)
		pm.undoInfo(closeChunk=1)

		pm.progressBar(progressBar, edit=True, endProgress=True)


	@staticmethod
	def alignVertices (mode, average=False, edgeloop=False):
		'''
		Align vertices.

		args:
			mode(int) = possible values are align: 0-YZ, 1-XZ, 2-XY, 3-X, 4-Y, 5-Z, 6-XYZ 
			average=bool - align to average of all selected vertices. else, align to last selected
			edgeloop=bool - align vertices in edgeloop from a selected edge
		ex. self.alignVertices(mode=3,average=True,edgeloop=True)
		'''
		pm.undoInfo (openChunk=True)
		selectTypeEdge = pm.selectType (query=True, edge=True)

		if edgeloop:
			mel.eval("SelectEdgeLoopSp;") #select edgeloop

		mel.eval('PolySelectConvert 3;') #convert to vertices
		
		selection=pm.ls(selection=1, flatten=1)
		lastSelected=pm.ls(tail=1, selection=1, flatten=1)
		alignTo=pm.xform(lastSelected, query=1, translation=1, worldSpace=1)
		alignX=alignTo[0]
		alignY=alignTo[1]
		alignZ=alignTo[2]
		
		if average:
			xyz=pm.xform(selection, query=1, translation=1, worldSpace=1)
			x = xyz[0::3]
			y = xyz[1::3]
			z = xyz[2::3]
			alignX = float(sum(x))/(len(xyz)/3)
			alignY = float(sum(y))/(len(xyz)/3)
			alignZ = float(sum(z))/(len(xyz)/3)

		if len(selection) == 0:
			viewPortMessage("No vertices selected")
			
		if len(selection)<2:
			viewPortMessage("Selection must contain at least two vertices")
			
		for vertex in selection:
			vertexXYZ=pm.xform(vertex, query=1, translation=1, worldSpace=1)
			vertX=vertexXYZ[0]
			vertY=vertexXYZ[1]
			vertZ=vertexXYZ[2]
			
			if mode == 0: #align YZ
				pm.xform(vertex, translation=(vertX, alignY, alignZ), worldSpace=1)
				
			if mode == 1: #align XZ
				pm.xform(vertex, translation=(alignX, vertY, alignZ), worldSpace=1)
				
			if mode == 2: #align XY
				pm.xform(vertex, translation=(alignX, alignY, vertZ), worldSpace=1)

			if mode == 3:
				pm.xform(vertex, translation=(alignX, vertY, vertZ), worldSpace=1)
			
			if mode == 4:
				pm.xform(vertex, translation=(vertX, alignY, vertZ), worldSpace=1)
			
			if mode == 5:
				pm.xform(vertex, translation=(vertX, vertY, alignZ), worldSpace=1)

			if mode == 6: #align XYZ
				pm.xform(vertex, translation=(alignX, alignY, alignZ), worldSpace=1)

		if selectTypeEdge:
			pm.selectType (edge=True)
		pm.undoInfo (closeChunk=True)


	@staticmethod
	def getPath(obj, components, type_=''):
		'''
		Query the polySelect command for the components along different edge paths.

		args:
			obj (obj) = The mesh object containing the components.
			components (obj) = The components used for the query (dependant on the operation type).
			type_ (str) = The desired return type. 'shortestEdgePath', 'edgeRing', 'edgeRingPath', 'edgeLoop', 'edgeLoopPath'.

		returns:
			(list) The components comprising the path.
		'''
		componentNumbers = [int(str(i).split('[')[-1].split(']')[0]) for i in components] #get the vertex numbers as integer values. ie. [818, 1380]

		edgesLong=None
		if type_=='shortestEdgePath':
			edgesLong = pm.polySelect(obj, query=1, shortestEdgePath=(componentNumbers[0], componentNumbers[1])) #(vtx, vtx)

		elif type_=='edgeRing':
			edgesLong = pm.polySelect(obj, query=1, edgeRing=componentNumbers) #(e..)

		elif type_=='edgeRingPath':
			edgesLong = pm.polySelect(obj, query=1, edgeRingPath=(componentNumbers[0], componentNumbers[1])) #(e, e)

		elif type_=='edgeLoop':
			edgesLong = pm.polySelect(obj, query=1, edgeLoop=componentNumbers) #(e..)

		elif type_=='edgeLoopPath':
			edgesLong = pm.polySelect(obj, query=1, edgeLoopPath=(componentNumbers[0], componentNumbers[1])) #(e, e)

		if not edgesLong:
			print('# Error: Unable to find path. #')
			return []

		path = ['{}.e[{}]'.format(obj, int(edge)) for edge in edgesLong]
		return path


	@staticmethod
	def getShortestPath(components=None, step=1):
		'''
		Get the shortest path between to vertices or edges.

		args:
			components (obj) = A Pair of vertices or edges.
			step (int) = step amount.

		returns:
			(list) the components that comprise the path as strings.
		'''
		type_ = Init.getObjectType(components[0])
		
		result=[]
		objects = set(pm.ls(components, objectsOnly=1))
		for obj in objects:

			if type_=='Polygon Edge':
				components = [pm.ls(pm.polyListComponentConversion(e, fromEdge=1, toVertex=1), flatten=1) for e in components]
				closestVerts = Init.getClosestVerts(components[0], components[1])
				edges = Init.getEdgePath(obj, closestVerts, 'shortestEdgePath')
				[result.append(e) for e in edges]

			elif type_=='Polygon Vertex':
				closestVerts = Init.getClosestVerts(components[0], components[1])
				edges = Init.getEdgePath(obj, closestVerts, 'shortestEdgePath')
				vertices = pm.ls(pm.polyListComponentConversion(edges, fromEdge=1, toVertex=1), flatten=1)
				[result.append(v) for v in vertices]

		return result


	@staticmethod
	def getPathAlongLoop(components=None, step=1):
		'''
		Get the shortest path between to vertices or edges along an edgeloop.

		args:
			components (obj) = A Pair of vertices, edges, or faces.
			step (int) = step amount.

		returns:
			(list) the components that comprise the path as strings.
		'''
		type_ = Init.getObjectType(components[0])
		
		result=[]
		objects = set(pm.ls(components, objectsOnly=1))
		for obj in objects:

			if type_=='Polygon Vertex':
				vertices=[]
				for component in components:
					edges = pm.ls(pm.polyListComponentConversion(component, fromVertex=1, toEdge=1), flatten=1)
					_vertices = pm.ls(pm.polyListComponentConversion(edges, fromEdge=1, toVertex=1), flatten=1)
					vertices.append(_vertices)

				closestVerts = Init.getClosestVerts(vertices[0], vertices[1])
				_edges = pm.ls(pm.polyListComponentConversion(components+[i for i in closestVerts], fromVertex=1, toEdge=1), flatten=1)

				edges=[]
				for edge in _edges:
					verts = pm.ls(pm.polyListComponentConversion(edge, fromEdge=1, toVertex=1), flatten=1)
					if closestVerts[0] in verts and components[0] in verts or closestVerts[1] in verts and components[1] in verts:
						edges.append(edge)

				edges = Init.getEdgePath(obj, edges, 'edgeLoopPath')

				vertices = [pm.ls(pm.polyListComponentConversion(edges, fromEdge=1, toVertex=1), flatten=1)]
				[result.append(v) for v in vertices]


			elif type_=='Polygon Edge':
				edges = Init.getEdgePath(obj, components, 'edgeLoopPath')
				[result.append(e) for e in edges]


			elif type_=='Polygon Face':
				vertices=[]
				for component in components:
					edges = pm.ls(pm.polyListComponentConversion(component, fromFace=1, toEdge=1), flatten=1)
					_vertices = pm.ls(pm.polyListComponentConversion(edges, fromEdge=1, toVertex=1), flatten=1)
					vertices.append(_vertices)

				closestVerts1 = Init.getClosestVerts(vertices[0], vertices[1])
				vertices[0].pop(vertices[0].index(closestVerts1[0])); vertices[1].pop(vertices[1].index(closestVerts1[1])) #delete the first set of closest verts
				closestVerts2 = Init.getClosestVerts(vertices[0], vertices[1]) #search for the next pair of closest verts

				_edges = pm.ls(pm.polyListComponentConversion(closestVerts1+closestVerts2, fromVertex=1, toEdge=1), flatten=1)
				edges=[]
				for edge in _edges:
					verts = pm.ls(pm.polyListComponentConversion(edge, fromEdge=1, toVertex=1), flatten=1)
					if closestVerts1[0] in verts and closestVerts2[0] in verts or closestVerts1[1] in verts and closestVerts2[1] in verts:
						edges.append(edge)

				edges = Init.getEdgePath(obj, edges, 'edgeRingPath')

				faces = pm.ls(pm.polyListComponentConversion(edges, fromEdge=1, toFace=1), flatten=1)
				[result.append(f) for f in faces]

		return result


	@staticmethod
	def getEdgeLoop(edges=None, step=1):
		'''
		Get the corresponding edgeloop(s) from the given edges.

		args:
			edges (list) = Polygon Edges.
			step (int) = step amount.

		returns:
			(list) the edges that comprise the edgeloops as strings.
		'''
		result=[]
		objects = set(pm.ls(edges, objectsOnly=1))
		for obj in objects:

			edges = Init.getEdgePath(obj, edges, 'edgeLoop')
			result.append(edges)

		return result


	@staticmethod
	def getEdgeRing(edges=None, step=1):
		'''
		Get the corresponding edgering(s) from the given edges.

		args:
			edges (list) = Polygon Edges.
			step (int) = step amount.

		returns:
			(list) the edges that comprise the edgerings as strings.
		'''
		result=[]
		objects = set(pm.ls(edges, objectsOnly=1))
		for obj in objects:

			edges = Init.getEdgePath(obj, edges, 'edgeRing')
			result.append(edges)

		return result


	@staticmethod
	def getComponentPoint(component, alignToNormal=False):
		'''
		Get the center point from the given component.

		args: alignToNormal=bool - 

		returns: [float list] - x, y, z  coordinate values.
		'''
		if ".vtx" in str(component):
			x = pm.polyNormalPerVertex (component, query=1, x=1)
			y = pm.polyNormalPerVertex (component, query=1, y=1)
			z = pm.polyNormalPerVertex (component, query=1, z=1)
			xyz = [sum(x) / float(len(x)), sum(y) / float(len(y)), sum(z) / float(len(z))] #get average
		elif ".e" in str(component):
			componentName = str(component).split(".")[0]
			vertices = pm.polyInfo (component, edgeToVertex=1)[0]
			vertices = vertices.split()
			vertices = [componentName+".vtx["+vertices[2]+"]",componentName+".vtx["+vertices[3]+"]"]
			x=[];y=[];z=[]
			for vertex in vertices:
				x_ = pm.polyNormalPerVertex (vertex, query=1, x=1)
				x.append(sum(x_) / float(len(x_)))
				y_ = pm.polyNormalPerVertex (vertex, query=1, y=1)
				x.append(sum(y_) / float(len(y_)))
				z_ = pm.polyNormalPerVertex (vertex, query=1, z=1)
				x.append(sum(z_) / float(len(z_)))
			xyz = [sum(x) / float(len(x)), sum(y) / float(len(y)), sum(z) / float(len(z))] #get average
		else:# elif ".f" in str(component):
			xyz = pm.polyInfo (component, faceNormals=1)
			xyz = xyz[0].split()
			xyz = [float(xyz[2]), float(xyz[3]), float(xyz[4])]

		if alignToNormal: #normal constraint
			normal = mel.eval("unit <<"+str(xyz[0])+", "+str(xyz[1])+", "+str(xyz[2])+">>;") #normalize value using MEL
			# normal = [round(i-min(xyz)/(max(xyz)-min(xyz)),6) for i in xyz] #normalize and round value using python

			constraint = pm.normalConstraint(component, object_,aimVector=normal,upVector=[0,1,0],worldUpVector=[0,1,0],worldUpType="vector") # "scene","object","objectrotation","vector","none"
			pm.delete(constraint) #orient object_ then remove constraint.

		vertexPoint = pm.xform (component, query=1, translation=1) #average vertex points on destination to get component center.
		x = vertexPoint [0::3]
		y = vertexPoint [1::3]
		z = vertexPoint [2::3]

		return list(round(sum(x) / float(len(x)),4), round(sum(y) / float(len(y)),4), round(sum(z) / float(len(z)),4))


	@staticmethod
	def createCircle(axis='y', numPoints=5, radius=5, center=[0,0,0], mode=0):
		'''
		Create a circular polygon plane.

		args:
			axis (str) = 'x','y','z' 
			numPoints(int) = number of outer points
			radius=int
			center=[float3 list] - point location of circle center
			mode(int) = 0 -no subdivisions, 1 -subdivide tris, 2 -subdivide quads
		ex. self.createCircle(axis='x', numPoints=20, radius=8, mode='tri')
		'''
		import math

		degree = 360/float(numPoints)
		radian = math.radians(degree) #or math.pi*degree/180 (pi * degrees / 180)

		vertexPoints=[]
		for _ in range(numPoints):
			# print("deg:", degree,"\n", "cos:",math.cos(radian),"\n", "sin:",math.sin(radian),"\n", "rad:",radian)
			if axis =='x': #x axis
				y = center[2] + (math.cos(radian) *radius)
				z = center[1] + (math.sin(radian) *radius)
				vertexPoints.append([0,y,z])
			if axis =='y': #y axis
				x = center[2] + (math.cos(radian) *radius)
				z = center[0] + (math.sin(radian) *radius)
				vertexPoints.append([x,0,z])
			else: # z axis
				x = center[0] + (math.cos(radian) *radius)
				y = center[1] + (math.sin(radian) *radius)
				vertexPoints.append([x,y,0]) #not working.

			radian = radian+math.radians(degree) #increment by original radian value that was converted from degrees
			#print(x,y,"\n")
			
		pm.undoInfo (openChunk=True)
		node = pm.polyCreateFacet (point=vertexPoints, name='pCircle')
		pm.polyNormal (node, normalMode=4) #4=reverse and propagate
		if mode==1:
			pm.polySubdivideFacet (divisions=1, mode=1)
		if mode==2:
			pm.polySubdivideFacet (divisions=1, mode=0)
		pm.undoInfo (closeChunk=True)

		return node


	def deleteAlongAxis(self, obj, axis):
		'''
		Delete components of the given mesh object along the specified axis.

		args:
			obj (obj) = Mesh object.
			axis (str) = Axis to delete on. ie. '-x' Components belonging to the mesh object given in the 'obj' arg, that fall on this axis, will be deleted. 
		'''
		for node in [n for n in pm.listRelatives(obj, allDescendents=1) if pm.objectType(n, isType='mesh')]: #get any mesh type child nodes of obj.
			faces = self.getAllFacesOnAxis(node, axis)
			if len(faces)==pm.polyEvaluate(node, face=1): #if all faces fall on the specified axis.
				pm.delete(node) #delete entire node
			else:
				pm.delete(faces) #else, delete any individual faces.

		self.viewPortMessage("Delete faces on <hl>"+axis.upper()+"</hl>.")



	# -----------------------------------------------
	' Normals'
	# -----------------------------------------------


	@staticmethod
	def getNormalVector(name=None):
		'''
		Get the normal vectors from the given poly object.
		If no argument is given the normals for the current selection will be returned.
		args:
			name (str) = polygon mesh or component.
		returns:
			dict - {int:[float, float, float]} face id & vector xyz.
		'''
		type_ = pm.objectType(name)

		if type_=='mesh': #get face normals
			normals = pm.polyInfo(name, faceNormals=1)

		elif type_=='transform': #get all normals for the given obj
			numFaces = pm.polyEvaluate(name, face=1) #returns number of faces as an integer
			normals=[]
			for n in range(0, numFaces): #for (number of faces):
				array = pm.polyInfo('{0}[{1}]'.format(name, n) , faceNormals=1) #get normal info from the rest of the object's faces
				string = ' '.join(array)
				n.append(str(string))

		else: #get face normals from the user component selection.
			normals = pm.polyInfo(faceNormals=1) #returns the face normals of selected faces

		regex = "[A-Z]*_[A-Z]* *[0-9]*: "

		dict_={}
		for n in normals:
			l = list(s.replace(regex,'') for s in n.split(' ') if s) #['FACE_NORMAL', '150:', '0.935741', '0.110496', '0.334931\n']

			key = int(l[1].strip(':')) #int face number as key ie. 150
			value = list(float(i) for i in l[-3:])  #vector list as value. ie. [[0.935741, 0.110496, 0.334931]]
			dict_[key] = value

		return dict_


	@staticmethod
	def getFacesWithSimilarNormals(faces, transforms=[], similarFaces=[], rangeX=0.1, rangeY=0.1, rangeZ=0.1):
		'''
		Get normals that fall within an X,Y,Z tolerance.
		args:
			faces (list) = ['polygon faces'] - faces to find similar normals for.
			similarFaces (list) = optional ability to add faces from previous calls to the return value.
			transforms (list) = [<shape nodes>] - objects to check faces on. If none are given the objects containing the given faces will be used.
			rangeX = float - x axis tolerance
			rangeY = float - y axis tolerance
			rangeZ = float - z axis tolerance
		returns:
			list - list of faces that fall within the normal range.
		'''
		faces = list(str(f) for f in faces) #work on a copy of the argument so that removal of elements doesn't effect the passed in list.
		for face in faces:
			normals = Init.getNormalVector(face)

			for k, v in normals.items():
				sX = v[0]
				sY = v[1]
				sZ = v[2]

				transforms = Init.getObjectFromComponent(face)

				for node in transforms:
					numFaces = pm.polyEvaluate(node, face=1)
					for faceNum in range(0, numFaces):
						face = '{0}.f[{1}]'.format(node, str(faceNum)) #assemble component name

						n = Init.getNormalVector(face)
						for k, v in n.items():
							nX = v[0]
							nY = v[1]
							nZ = v[2]

							if sX<=nX + rangeX and sX>=nX - rangeX and sY<=nY + rangeY and sY>=nY - rangeY and sZ<=nZ + rangeZ and sZ>=nZ - rangeZ:
								similarFaces.append(face)
								if face in faces: #If the face is in the loop que, remove it, as has already been evaluated.
									faces.remove(face)

		return similarFaces







	# ------------------------------------------------
	' DAG objects'
	# ------------------------------------------------

	@staticmethod
	def getObjectType(obj):
		'''
		Get the object type of a given object.

		args:
			obj (obj) = maya component.

		returns:
			(str) type
		'''
		types = {0:'Handle', 9:'Nurbs Curve', 10:'Nurbs Surfaces', 11:'Nurbs Curves On Surface', 12:'Polygon', 22:'Locator XYZ', 23:'Orientation Locator', 
			24:'Locator UV', 28:'Control Vertex', 30:'Edit Point', 31:'Polygon Vertex', 32:'Polygon Edge', 34:'Polygon Face', 35:'Polygon UV', 36:'Subdivision Mesh Point', 
			37:'Subdivision Mesh Edge', 38:'Subdivision Mesh Face', 39:'Curve Parameter Point', 40:'Curve Knot', 41:'Surface Parameter Point', 42:'Surface Knot', 
			43:'Surface Range', 44:'Trim Surface Edge', 45:'Surface Isoparm', 46:'Lattice Point', 47:'Particle', 49:'Scale Pivot', 50:'Rotate Pivot', 51:'Select Handle', 
			68:'Subdivision Surface', 70:'Polygon Vertex Face', 72:'NURBS Surface Face', 73:'Subdivision Mesh UV'}

		for k, v in types.items():
			if pm.filterExpand(obj, sm=k):
				return v


	@staticmethod
	def getObjectFromComponent(components):
		'''
		Get the object's transform node from the given components.
		args:
			components (str, list) = component name(s)
		returns:
			(dict) {transform node: [components of that node]}
			ie. {'pCube2': ['pCube2.f[21]', 'pCube2.f[22]', 'pCube2.f[25]'], 'pCube1': ['pCube1.f[21]', 'pCube1.f[26]']}
		'''
		if type(components) in [str,unicode]:
			components = [components]

		transforms={}
		for component in components:
			component = str(component)
			shapeNode = str(pm.listRelatives(component, parent=1)[0])
			transform = str(pm.listRelatives(shapeNode, parent=1)[0])

			try:
				transforms[transform].append(component)
			except:
				transforms[transform] = [component]

		return transforms


	@staticmethod
	def isGroup(node):
		'''
		Check if the given node is a group (has a transform AND has no shape children).
		'''
		if (pm.objectType(node, isType='transform')) and (not len(pm.listRelatives(node, shapes=1))):
			return True

		return False


	@staticmethod
	def getTransformNode(node=None, index=0, attributes=False, string=''):
		'''
		Get the transform node. 

		args:
			node (obj) = Node. If nothing is given, the current selection will be used.
			index (int) = Return the transform node at the given index. if Nothing is given, the full list will be returned. ie. index=[:-1] or index=0
			attributes (bool) = Return the attributes of the node, rather then the node itself.
			string (str) = 	List only the attributes that match the other criteria AND match the string(s) passed from this flag. String can be a regular expression.

		returns:
			(str) node
		'''
		if not node:
			node = pm.ls(sl=1)

		transforms = pm.ls(node, type='transform')
		if not transforms:
			shapeNodes = pm.ls(sl=1, objectsOnly=1)
			transforms = pm.listRelatives(shapeNodes, parent=1)

		if transforms and index is not None:
			transforms = transforms[index]
		
		if attributes:
			transforms = pm.listAttr(transforms, read=1, hasData=1, string=string)

		return transforms


	@staticmethod
	def getShapeNode(node=None, index=0, attributes=False, string=''):
		'''
		Get the shape node. 

		args:
			node (obj) = Node. If nothing is given, the current selection will be used.
			index (int) = Return the shape node at the given index. if Nothing is given, the full list will be returned. ie. index=[:-1] or index=0
			attributes (bool) = Return the attributes of the node, rather then the node itself.
			string (str) = 	List only the attributes that match the other criteria AND match the string(s) passed from this flag. String can be a regular expression.

		returns:
			(str) node
		'''
		if not node:
			pm.ls(sl=1, type='transform')

		shapes = pm.listRelatives(node, children=1, shapes=1) #get shape node from transform: returns list ie. [nt.Mesh('pConeShape1')]

		if shapes and index is not None:
			shapes = shapes[index]
		
		if attributes:
			shapes = pm.listAttr(shapes, read=1, hasData=1, string=string)

		return shapes


	@staticmethod
	def getHistoryNode(node=None, index=0, attributes=False, string=''):
		'''
		Get the history node. 

		args:
			node (obj) = Node. If nothing is given, the current selection will be used.
			index (int) = Return the transform node at the given index. if Nothing is given, the full list will be returned. ie. index=[:-1] or index=0
			attributes (bool) = Return the attributes of the node, rather then the node itself.
			string (str) = 	List only the attributes that match the other criteria AND match the string(s) passed from this flag. String can be a regular expression.

		returns:
			(str) node

		alt method: node.history()[-1]
		'''
		if not node:
			pm.ls(sl=1, type='transform')

		shapes = pm.listRelatives(node, children=1, shapes=1) #get shape node from transform: returns list ie. [nt.Mesh('pConeShape1')]
		connections = pm.listConnections(shapes, source=1, destination=0) #get incoming connections: returns list ie. [nt.PolyCone('polyCone1')]

		if connections and index is not None:
			connections = connections[index]

		if attributes:
			connections = pm.listAttr(connections, read=1, hasData=1, string=string)

		return connections


	@staticmethod
	def getAllParents(node):
		'''
		List ALL parents of an object
		'''
		objects = pm.ls(node, l=1)
		tokens=[]

		return objects[0].split("|")


	@staticmethod
	def getAttributesMEL(node, include=[], exclude=[]):
		'''
		Get node attributes and their corresponding values as a dict.

		args:
			node (obj) = Transform node.
			include (list) = Attributes to include. All other will be omitted. Exclude takes dominance over include. Meaning, if the same attribute is in both lists, it will be excluded.
			exclude (list) = Attributes to exclude from the returned dictionay. ie. ['Position','Rotation','Scale','renderable','isHidden','isFrozen','selected']

		returns:
			(dict) {'string attribute': current value}
		'''
		if not all((include, exclude)):
			exclude = ['message', 'caching', 'frozen', 'isHistoricallyInteresting', 'nodeState', 'binMembership', 'output', 'edgeIdMap', 'miterAlong', 'message',
					'axis', 'axisX', 'axisY', 'axisZ', 'paramWarn', 'uvSetName', 'createUVs', 'texture', 'maya70', 'inputPolymesh', 'maya2017Update1', 
					'manipMatrix', 'inMeshCache', 'faceIdMap', 'subdivideNgons', 'useOldPolyArchitecture', 'inputComponents', 
					'binMembership', 'maya2015', 'cacheInput', 'inputMatrix', 'forceParallel', 'autoFit', 'maya2016SP3', 'caching', 'output', 'vertexIdMap', 
					'useInputComp', 'worldSpace', 'taperCurve_Position', 'taperCurve_FloatValue', 'taperCurve_Interp',
					]

		# print('node:', node); print('attr:', pm.listAttr(node))
		attributes={} 
		for attr in pm.listAttr(node):
			if not attr in exclude and (attr in include if include else attr not in include): #ie. pm.getAttr('polyCube1.subdivisionsDepth')
				try:
					attributes[attr] = pm.getAttr(node+'.'+attr)
				except Exception as error:
					print (error)

		return attributes


	@staticmethod
	def setAttributesMEL(node, attributes):
		'''
		Set node attribute values using a dict. 

		args:
			node (obj) = Transform node.
			attributes (dict) = Attributes and their correponding value to set. ie. {'string attribute': value}

		ex call:
		self.setAttributesMEL(obj, {'smoothLevel':1})
		'''
		[pm.setAttr(node+'.'+attr, value) 
			for attr, value in attributes.items() 
				if attr and value] #ie. pm.setAttr('polyCube1.subdivisionsDepth', 5)


	@staticmethod
	def connectAttributes(attr, place, file):
		'''
		A convenience procedure for connecting common attributes between two nodes.

		args:
			attr () = 
			place () = 
			file () = 

		// Use convenience command to connect attributes which share 
		// their names for both the placement and file nodes.
		self.connectAttributes('coverage', 'place2d', fileNode')
		self.connectAttributes('translateFrame', 'place2d', fileNode')
		self.connectAttributes('rotateFrame', 'place2d', fileNode')
		self.connectAttributes('mirror', 'place2d', fileNode')
		self.connectAttributes('stagger', 'place2d', fileNode')
		self.connectAttributes('wrap', 'place2d', fileNode')
		self.connectAttributes('wrapV', 'place2d', fileNode')
		self.connectAttributes('repeatUV', 'place2d', fileNode')
		self.connectAttributes('offset', 'place2d', fileNode')
		self.connectAttributes('rotateUV', 'place2d', fileNode')

		// These two are named differently.
		connectAttr -f ( $place2d + ".outUV" ) ( $fileNode + ".uv" );
		connectAttr -f ( $place2d + ".outUvFilterSize" ) ( $fileNode + ".uvFilterSize" );
		'''
		pm.connectAttr((place + "." + attr), (file + "." + attr), f=1)






	# ------------------------------------------------
	' Ui'
	# ------------------------------------------------


	@classmethod
	def attr(cls, fn):
		'''
		Decorator for objAttrWindow.
		'''
		def wrapper(self, *args, **kwargs):
			self.setAttributeWindow(fn(self, *args, **kwargs))
		return wrapper

	def setAttributeWindow(self, obj, include=[], exclude=[]):
		'''
		Launch a popup window containing the given objects attributes.

		args:
			obj (obj) = The object to get the attributes of.
			include (list) = Attributes to include. All other will be omitted. Exclude takes dominance over include. Meaning, if the same attribute is in both lists, it will be excluded.
			exclude (list) = Attributes to exclude from the returned dictionay. ie. ['Position','Rotation','Scale','renderable','isHidden','isFrozen','selected']
		'''
		if obj is None:
			return

		if isinstance(obj, (list, set, tuple)):
			obj = obj[0]

		attributes = self.getAttributesMEL(obj, include=include, exclude=exclude)
		self.objAttrWindow(obj, attributes, self.setAttributesMEL)


	@staticmethod
	def getMayaMainWindow():
		'''
		Get the main Maya window as a QtWidgets.QMainWindow instance

		returns:
			QtGui.QMainWindow instance of the top level Maya windows
		'''
		ptr = omUI.MQtUtil.mainWindow()
		if ptr:
			return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)



	@staticmethod
	def convertToWidget(name):
		'''
		args:
			name (str) = name of a Maya UI element of any type.
			type_ = <qt object type> - default is QWidget

		returns:
			the corresponding QWidget or QAction.
			If the object does not exist, returns None
		'''
		ptr = omUI.MQtUtil.findControl(name)
		if ptr is None:
			ptr = omUI.MQtUtil.findLayout(name)
			if ptr is None:
				ptr = omUI.MQtUtil.findMenuItem(name)
		if ptr is not None:
			return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)



	@staticmethod
	def mainProgressBar(size, name="tk_progressBar", stepAmount=1):
		'''
		#add esc key pressed return False

		args:
			size (int) = total amount
			name (str) = name of progress bar created
	  		stepAmount(int) = increment amount

		example use-case:
		mainProgressBar (len(edges), progressCount)
			pm.progressBar ("tk_progressBar", edit=1, step=1)
			if pm.progressBar ("tk_progressBar", query=1, isCancelled=1):
				break
		pm.progressBar ("tk_progressBar", edit=1, endProgress=1)

	  	to use main progressBar: name=string $gMainProgressBar
	  	'''
		status = "processing: "+str(size)+"."
		edit=0
		if pm.progressBar(name, exists=1):
			edit=1
		pm.progressBar(name, edit=edit,
						beginProgress=1,
						isInterruptable=True,
						status=status,
						maxValue=size,
						step=stepAmount)



	@staticmethod
	def mainProgressBar(gMainProgressBar, numFaces, count):
		'''

		'''
		num=str(numFaces)
		status="iterating through " + num + " faces"
		pm.progressBar(gMainProgressBar, 
			edit=1, 
			status=status, 
			isInterruptable=True, 
			maxValue=count, 
			beginProgress=1)



	@staticmethod
	def viewPortMessage(message='', statusMessage='', assistMessage='', position='topCenter'):
		'''
		args:
			message (str) = The message to be displayed, (accepts html formatting). General message, inherited by -amg/assistMessage and -smg/statusMessage.
			statusMessage (str) = The status info message to be displayed (accepts html formatting).
			assistMessage (str) = The user assistance message to be displayed, (accepts html formatting).
			position (str) = position on screen. possible values are: topCenter","topRight","midLeft","midCenter","midCenterTop","midCenterBot","midRight","botLeft","botCenter","botRight"

		ex. self.viewPortMessage("shutting down:<hl>"+str(timer)+"</hl>")
		'''
		fontSize=10
		fade=1
		fadeInTime=0
		fadeStayTime=1000
		fadeOutTime=500
		alpha=75

		if message:
			pm.inViewMessage(message=message, position=position, fontSize=fontSize, fade=fade, fadeInTime=fadeInTime, fadeStayTime=fadeStayTime, fadeOutTime=fadeOutTime, alpha=alpha) #1000ms = 1 sec
		elif statusMessage:
			pm.inViewMessage(statusMessage=statusMessage, position=position, fontSize=fontSize, fade=fade, fadeInTime=fadeInTime, fadeStayTime=fadeStayTime, fadeOutTime=fadeOutTime, alpha=alpha) #1000ms = 1 sec
		elif assistMessage:
			pm.inViewMessage(assistMessage=assistMessage, position=position, fontSize=fontSize, fade=fade, fadeInTime=fadeInTime, fadeStayTime=fadeStayTime, fadeOutTime=fadeOutTime, alpha=alpha) #1000ms = 1 sec



	@staticmethod
	def outputText (text, window_title):
		'''
		output text
		'''
		#window_title = mel.eval(python("window_title"))
		window = str(pm.window(	widthHeight=(300, 300), 
								topLeftCorner=(65,265),
								maximizeButton=False,
								resizeToFitChildren=True,
								toolbox=True,
								title=window_title))
		scrollLayout = str(pm.scrollLayout(verticalScrollBarThickness=16, 
										horizontalScrollBarThickness=16))
		pm.columnLayout(adjustableColumn=True)
		text_field = str(pm.text(label=text, align='left'))
		print(text_field)
		pm.setParent('..')
		pm.showWindow(window)
		return

	# #output textfield parsed by ';'
	# def outputTextField2(text):
	# 	window = str(pm.window(	widthHeight=(250, 650), 
	# 							topLeftCorner=(50,275),
	# 							maximizeButton=False,
	# 							resizeToFitChildren=False,
	# 							toolbox=True,
	# 							title=""))
	# 	scrollLayout = str(pm.scrollLayout(verticalScrollBarThickness=16, 
	# 									horizontalScrollBarThickness=16))
	# 	pm.columnLayout(adjustableColumn=True)
	# 	print(text)
	# 	#for item in array:
	# 	text_field = str(pm.textField(height=20,
	# 										width=250, 
	# 										editable=False,
	# 										insertText=str(text)))
	# 	pm.setParent('..')
	# 	pm.showWindow(window)
	# 	return



	@staticmethod
	def outputscrollField (text, window_title, width, height):
		'''
		Create an output scroll layout.
		'''
		window_width  = width  * 300
		window_height = height * 600
		scroll_width  = width  * 294
		scroll_height = height * 590
		window = str(pm.window(	widthHeight=(window_width, window_height),
								topLeftCorner=(45, 0),
								maximizeButton=False,
								sizeable=False,
								title=window_title
								))
		scrollLayout = str(pm.scrollLayout(verticalScrollBarThickness=16, 
										horizontalScrollBarThickness=16))
		pm.columnLayout(adjustableColumn=True)
		text_field = str(pm.scrollField(text=(text),
		                                width=scroll_width,
		                                height=scroll_height,))
		print(window)
		pm.setParent('..')
		pm.showWindow(window)
		return



	@staticmethod
	def outputTextField (array, window_title):
		'''
		Create an output text field.
		'''
		window = str(pm.window(	widthHeight=(250, 650), 
								topLeftCorner=(65,275),
								maximizeButton=False,
								resizeToFitChildren=False,
								toolbox=True,
								title=window_title))
		scrollLayout = str(pm.scrollLayout(verticalScrollBarThickness=16, 
										horizontalScrollBarThickness=16))
		pm.columnLayout(adjustableColumn=True)
		for item in array:
			text_field = str(pm.textField(height=20,
											width=500, 
											editable=False,
											insertText=str(item)))
		pm.setParent('..')
		pm.showWindow(window)
		return






	# ------------------------------------------------
	' Scripting'
	# ------------------------------------------------


	@staticmethod
	def convertMelToPy(mel, excludeFromInput=[], excludeFromOutput=['from pymel.all import *','s pm']):
		'''
		Convert a string representing mel code into a string representing python code.

		args:
			mel (str) = string containing mel code.
			excludeFromInput (list) (list) = of strings specifying series of chars to strip from the Input.
			excludeFromOutput (list) (list) = of strings specifying series of chars to strip from the Output.
		
		mel2PyStr Parameters:
			currentModule (str) = The name of the module that the hypothetical code is executing in. In most cases you will leave it at its default, the __main__ namespace.
			pymelNamespace (str) = The namespace into which pymel will be imported. the default is '', which means from pymel.all import *
			forceCompatibility (bool) = If True, the translator will attempt to use non-standard python types in order to produce python code which more exactly reproduces the behavior of the original mel file, but which will produce 'uglier' code. Use this option if you wish to produce the most reliable code without any manual cleanup.
			verbosity (int) = Set to non-zero for a lot of feedback.
		'''
		from pymel.tools import mel2py
		import re

		l = filter(None, re.split('[\n][;]', mel))

		python=[]
		for e in l:
			if not e in excludeFromInput:
				try:
					py = mel2py.mel2pyStr(e, pymelNamespace='pm')
					for _ in excludeFromOutput:
						py = py.strip(_)
				except:
					py = e
				python.append(py)

		return ''.join(python)


	@staticmethod
	def commandHelp(command): #mel command help
		#args: command (str) = mel command
		command = ('help ' + command)
		modtext = (mel.eval(command))
		outputscrollField (modtext, "command help", 1.0, 1.0) #text, window_title, width, height


	@staticmethod
	def keywordSearch (keyword): #keyword command search
		#args: keyword (str) = 
		keyword = ('help -list' + '"*' + keyword + '*"')
		array = sorted(mel.eval(keyword))
		outputTextField(array, "keyword search")


	@staticmethod
	def queryRuntime (command): #query runtime command info
		type       = ('whatIs '                           + command + ';')
		catagory   = ('runTimeCommand -query -category '  + command + ';')
		command	   = ('runTimeCommand -query -command '   + command + ';')
		annotation = ('runTimeCommand -query -annotation '+ command + ';')
		type = (mel.eval(type))
		catagory = (mel.eval(catagory))
		command = (mel.eval(command))
		annotation = (mel.eval(annotation))
		output_text = '{}\n\n{}\n{}\n\n{}\n{}\n\n{}\n{}\n\n{}\n{}'.format(command, "Type:", type, "Annotation:", annotation, "Catagory:", catagory, "Command:", command)
		outputscrollField(output_text, "runTimeCommand", 1.0, 1.0) #text, window_title, width, height


	@staticmethod
	def searchMEL (keyword): #search autodest MEL documentation
		url = '{}{}{}'.format("http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/Commands/",keyword,".html")
		pm.showHelp (url, absolute=True)


	@staticmethod
	def searchPython (keyword): #Search autodesk Python documentation
		url = '{}{}{}'.format("http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/CommandsPython/",keyword,".html")
		pm.showHelp (url, absolute=True)


	@staticmethod
	def searchPymel (keyword): #search online pymel documentation
		url = '{}{}{}'.format("http://download.autodesk.com/global/docs/maya2014/zh_cn/PyMel/search.html?q=",keyword,"&check_keywords=yes&area=default")
		pm.showHelp (url, absolute=True)


	@staticmethod
	def currentCtx(): #get current tool context
		output_text = mel.eval('currentCtx;')
		outputscrollField(output_text, "currentCtx", 1.0, 1.0)


	@staticmethod
	def sourceScript(): #Source External Script file
		mel_checkBox = checkBox('mel_checkBox', query=1, value=1)
		python_checkBox = checkBox('python_checkBox', query=1, value=1)

		if mel_checkBox == 1:
			path = os.path.expandvars("%\CLOUD%/____graphics/Maya/scripts/*.mel")
			
		else:
			path = os.path.expandvars("%\CLOUD%/____graphics/Maya/scripts/*.py")

		file = pm.system.fileDialog (directoryMask=path)
		pm.openFile(file)


	@staticmethod
	def commandRef(): #open maya MEL commands list 
		pm.showHelp ('http://download.autodesk.com/us/maya/2011help/Commands/index.html', absolute=True)


	@staticmethod
	def globalVars(): #$g List all global mel variables in current scene
		mel.eval('scriptEditorInfo -clearHistory')
		array = sorted(mel.eval("env"))
		outputTextField(array, "Global Variables")


	@staticmethod
	def listUiObjects(): #lsUI returns the names of UI objects
		windows			= '{}\n{}\n{}\n'.format("Windows", "Windows created using ELF UI commands:", pm.lsUI (windows=True))
		panels			= '{}\n{}\n{}\n'.format("Panels", "All currently existing panels:", pm.lsUI (panels=True))
		editors			= '{}\n{}\n{}\n'.format("Editors", "All currently existing editors:", pm.lsUI (editors=True))
		controls		= '{}\n{}\n{}\n'.format("Controls", "Controls created using ELF UI commands: [e.g. buttons, checkboxes, etc]", pm.lsUI (controls=True))
		control_layouts = '{}\n{}\n{}\n'.format("Control Layouts", "Control layouts created using ELF UI commands: [e.g. formLayouts, paneLayouts, etc.]", pm.lsUI (controlLayouts=True))
		menus				= '{}\n{}\n{}\n'.format("Menus", "Menus created using ELF UI commands:", pm.lsUI (menus=True))
		menu_items	= '{}\n{}\n{}\n'.format("Menu Items", "Menu items created using ELF UI commands:", pm.lsUI (menuItems=True))
		contexts		= '{}\n{}\n{}\n'.format("Tool Contexts", "Tool contexts created using ELF UI commands:", pm.lsUI (contexts=True))
		output_text	= '{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(windows, panels, editors, menus, menu_items, controls, control_layouts, contexts)
		outputscrollField(output_text, "Ui Elements", 6.4, 0.85)





#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------





#deprecated -------------------------------------


	# @staticmethod
	# def shortestEdgePath():
	# 	'''
	# 	Select shortest edge path between (two or more) selected edges.
	# 	'''
	# 	#returns: list of lists. each containing an edge paths components
	# 	selectTypeEdge = pm.filterExpand (selectionMask=32) #returns True if selectionMask=Edges
	# 	if (selectTypeEdge): #if selection is polygon edges, convert to vertices.
	# 		mel.eval("PolySelectConvert 3;")
	# 	selection=pm.ls (selection=1, flatten=1)

	# 	vertList=[]

	# 	for objName in selection:
	# 		objName = str(objName) #ex. "polyShape.vtx[176]"
	# 		index1 = objName.find("[")
	# 		index2 = objName.find("]")
	# 		vertNum = objName[index1+1:index2] #ex. "176"
	# 		# position = pm.pointPosition(objName) 
	# 		object_ = objName[:index1-4] #ex. "polyShape"
	# 		# print(object_, index1, index2#, position)
	# 		vertList.append(vertNum)

	# 	if (selectTypeEdge):
	# 		pm.selectType (edge=True)

	# 	paths=[]
	# 	for index in xrange(3): #get edge path between vertList[0],[1] [1],[2] [2],[3] to make sure everything is selected between the original four vertices/two edges
	# 		edgePath = pm.polySelect(object_, shortestEdgePath=(int(vertList[index]), int(vertList[index+1])))
	# 		paths.append(edgePath)

	# 	return paths



	# def snapToClosestVertex(vertices, obj, tolerance=0.125):
	# 	'''
	# 	This Function Snaps Vertices To Onto The Reference Object.

	# 	args:
	# 		obj (str) = The object to snap to.
	# 		vertices (list) = The vertices to snap.
	# 		tolerance (float) = Max distance.
	# 	'''
	# 	Init.loadPlugin('nearestPointOnMesh')
	# 	nearestPointOnMeshNode = mel.eval('{} {}'.format('nearestPointOnMesh', obj))
	# 	pm.delete(nearestPointOnMeshNode)

	# 	pm.undoInfo(openChunk=1)
	# 	for vertex in vertices:

	# 		vertexPosition = pm.pointPosition(vertex, world=True)
	# 		pm.setAttr('{}.inPosition'.format(nearestPointOnMeshNode), vertexPosition[0], vertexPosition[1], vertexPosition[2])
	# 		associatedFaceId = pm.getAttr('{}.nearestFaceIndex'.format(nearestPointOnMeshNode))
	# 		vtxsFaces = pm.filterExpand(pm.polyListComponentConversion('{0}.f[{1}]'.format(obj, associatedFaceId), fromFace=True,  toVertexFace=True), sm=70, expand=True)

	# 		closestDistance = 2**32-1

	# 		closestPosition=[]
	# 		for vtxsFace in vtxsFaces:
	# 			associatedVtx = pm.polyListComponentConversion(vtxsFace, fromVertexFace=True, toVertex=True)
	# 			associatedVtxPosition = pm.pointPosition(associatedVtx, world=True)
				
	# 			distance = Init.getVectorLength(vertexPosition, associatedVtxPosition)

	# 			if distance<closestDistance:
	# 				closestDistance = distance
	# 				closestPosition = associatedVtxPosition
				
	# 			if closestDistance<tolerance:
	# 				pm.move(closestPosition[0], closestPosition[1], closestPosition[2], vertex, worldSpace=True)

	# 	# pm.delete(nearestPointOnMeshNode)
	# 	pm.undoInfo(closeChunk=1)








# def getContigiousIslands(faces, faceIslands=[]):
# 	'''
# 	Get a list containing sets of adjacent polygon faces grouped by islands.
# 	args:
# 		faces (list) = polygon faces to be filtered for adjacent.
# 		faceIslands (list) = optional. list of sets. ability to add faces from previous calls to the return value.
# 	returns:
# 		list of sets of adjacent faces.
# 	'''
# 	face=None
# 	faces = list(str(f) for f in faces) #work on a copy of the argument so that removal of elements doesn't effect the passed in list.
# 	prevFaces=[]

# 	for _ in range(len(faces)):
# 		# print ''
# 		if not face:
# 			try:
# 				face = faces[0]
# 				island=set([face])
# 			except:
# 				break

# 		adjFaces = [f for f in Init.getBorderFaces(face) if not f in prevFaces and f in faces]
# 		prevFaces.append(face)
# 		# print '-face     ','   *',face
# 		# print '-adjFaces ','  **',adjFaces
# 		# print '-prevFaces','    ',prevFaces

# 		try: #add face to current island if it hasn't already been added, and is one of the faces specified by the faces argument.
# 			island.add(adjFaces[0])
# 			face = adjFaces[0]

# 		except: #if there are no adjacent faces, start a new island set.
# 			faceIslands.append(island)
# 			face = None
# 			# print '-island   ','   $',island
# 			# print '\n',40*'-'
# 		faces.remove(prevFaces[-1])

# 	return faceIslands