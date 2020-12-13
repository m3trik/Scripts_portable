from __future__ import print_function
from builtins import super
import os

from PySide2 import QtGui, QtWidgets, QtCore

from ui import widgets
from tk_slots_ import Slots

# Maya dependancies
try:
	import maya.mel as mel
	import pymel.core as pm
	import maya.OpenMayaUI as OpenMayaUI

	import shiboken2

except ImportError as error:
	print(error)



class Init(Slots):
	'''
	App specific methods inherited by all other slot classes.
	'''
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		try:
			self.init.hud.shown.connect(self.construct_hud)
		except AttributeError: #(an inherited class)
			pass


	def construct_hud(self):
		'''
		Add current scene attributes to the hud lineEdit.
		Only those with relevant values will be displayed.
		'''
		hud = self.init.hud

		try:
			selection = pm.ls(selection=1)
		except NameError:
			return

		symmetry = pm.symmetricModelling(query=1, symmetry=1);
		if symmetry:
			axis = pm.symmetricModelling(query=1, axis=1)
			hud.insertText('Symmetry Axis: <font style="color: Yellow;">{}'.format(axis.upper())) #symmetry axis

		xformConstraint = pm.xformConstraint(query=True, type=True)
		if xformConstraint=='none':
			xformConstraint=None
		if xformConstraint:
			hud.insertText('Xform Constrait: <font style="color: Yellow;">{}'.format(xformConstraint)) #transform constraits

		if selection:
			if pm.selectMode(query=1, object=1): #object mode:
				if pm.selectType(query=1, allObjects=1): #get object/s

					selectedObjects = pm.ls(selection=1, objectsOnly=1)
					name_and_type = ['<font style="color: Yellow;">{0}<font style="color: LightGray;">:{1}'.format(i.name(), pm.objectType(i)) for i in selectedObjects] #ie. ['pCube1:transform', 'pSphere1:transform']
					name_and_type_str = str(name_and_type).translate(None, '[]\'') #format as single string.
					hud.insertText('Selected: {}'.format(name_and_type_str)) #currently selected objects by name and type.

					objectFaces = pm.polyEvaluate(selectedObjects, face=True)
					if type(objectFaces)==int:
						hud.insertText('Faces: <font style="color: Yellow;">{}'.format(objectFaces, ',d')) #add commas each 3 decimal places.

					objectTris = pm.polyEvaluate(selectedObjects, triangle=True)
					if type(objectTris)==int:
						hud.insertText('Tris: <font style="color: Yellow;">{}'.format(objectTris, ',d')) #add commas each 3 decimal places.

					objectUVs = pm.polyEvaluate(selectedObjects, uvcoord=True)
					if type(objectUVs)==int:
						hud.insertText('UVs: <font style="color: Yellow;">{}'.format(objectUVs, ',d')) #add commas each 3 decimal places.

			elif pm.selectMode(query=1, component=1): #component mode:
				if pm.selectType(query=1, vertex=1): #get vertex selection info
					type_ = 'Verts'
					num_selected = pm.polyEvaluate(vertexComponent=1)
					total_num = pm.polyEvaluate(selection, vertex=1)

				elif pm.selectType(query=1, edge=1): #get edge selection info
					type_ = 'Edges'
					num_selected = pm.polyEvaluate(edgeComponent=1)
					total_num = pm.polyEvaluate(selection, edge=1)

				elif pm.selectType(query=1, facet=1): #get face selection info
					type_ = 'Faces'
					num_selected = pm.polyEvaluate(faceComponent=1)
					total_num = pm.polyEvaluate(selection, face=1)

				elif pm.selectType(query=1, polymeshUV=1): #get uv selection info
					type_ = 'UVs'
					num_selected = pm.polyEvaluate(uvComponent=1)
					total_num = pm.polyEvaluate(selection, uvcoord=1)

				try:
					hud.insertText('Selected {}: <font style="color: Yellow;">{} <font style="color: LightGray;">/{}'.format(type_, num_selected, total_num)) #selected components
				except NameError:
					pass


		prevCommand = self.sb.prevCommand(docString=True)
		if prevCommand:
			hud.insertText('Prev Command: <font style="color: Yellow;">{}'.format(prevCommand))  #get button text from last used command

		# prevUi = self.sb.previousName(omitLevel=[0,1,2])
		# hud.insertText('Prev UI: {}'.format(prevUi.replace('_', '').title())) #get the last level 3 ui name string.

		# prevCamera = self.sb.prevCamera(docString=True)
		# hud.insertText('Prev Camera: {}'.format(prevCamera)) #get the previously used camera.


	@staticmethod
	def loadPlugin(plugin):
		'''
		Loads A Plugin.
		
		:Parameters:
			plugin (str) = The desired plugin to load.

		ex. loadPlugin('nearestPointOnMesh')
		'''
		not pm.pluginInfo(plugin, query=True, loaded=True) and pm.loadPlugin(plugin)






	# ------------------------------------------------
	' Geometry'
	# ------------------------------------------------

	@staticmethod
	def getComponents(componentType=None, objects=None, selection=False, returnType=unicode, returnNodeType='shape', flatten=False):
		'''
		Get the components of the given type.

		:Parameters:
			componentType (str) = The desired component mask. valid values are: 'vtx'(vertices), 'e'(edges), 'f'(faces), 'cv'(control vertices).
			objects (obj)(list) = The object(s) to get the components of.
			selection (bool) = Filter to currently selected objects.
			returnType (type) = The desired returned object type. (valid: unicode(default, str, int, object)
			returnNodeType (str) = Specify whether the components are returned with the transform or shape nodes (valid only with str and unicode returnTypes). (valid: 'transform', 'shape'(default)) ex. 'pCylinder1.f[0]' or 'pCylinderShape1.f[0]'
			flatten (bool) = Flattens the returned list of objects so that each component is identified individually.

		:Return:
			(list)(dict) Dependant on flags.

		ex. getComponents('f', obj, returnType=object)
		'''
		if not componentType: #get component type from the current selection.
			if selection:
				o = pm.ls(sl=1)
				t = Init.getObjectType(o)
				types = {'Polygon Vertex':'vtx', 'Polygon Edge':'e', 'Polygon Face':'f'}
				componentType = types[t] if t in types else None
				if not componentType:
					return
			else:
				return

		mask = {'vtx':31, 'e':32, 'f':34, 'cv':28}
		components=[]

		if selection:
			if objects:
				transforms = pm.ls(objects, sl=1, transforms=1)
				if transforms: #get ALL selected components, FILTERING for those of the given transform object(s).
					selected_shapes=[]
					for obj in transforms:
						selected_shapes+=pm.ls('{}.{}[*]'.format(obj, componentType), flatten=flatten)
				else: #get selected components, FILTERING for those of the given tranform object(s).
					shapes = Init.getShapeNode(objects)
					selected_shapes = pm.ls(shapes, sl=1)
				components = pm.filterExpand(selected_shapes, selectionMask=mask[componentType], expand=flatten)
			else:
				transforms = pm.ls(sl=1, transforms=1)
				if transforms:
					for obj in transforms: #get ALL selected components, for each selected transform object.
						components+=pm.ls('{}.{}[*]'.format(obj, componentType), flatten=flatten)
				else: ##get selected components.
					components = pm.filterExpand(selectionMask=mask[componentType], expand=flatten)
		else:
			for obj in pm.ls(objects):
				components+=pm.ls('{}.{}[*]'.format(obj, componentType), flatten=flatten)

		if not components:
			components=[]

		if returnType is unicode:
			if returnNodeType=='transform':
				result = [unicode(''.join(c.rsplit('Shape', 1))) for c in components]
			else:
				result = [unicode(c) for c in components]

		elif returnType is str:
			if returnNodeType=='transform':
				result = [str(''.join(c.rsplit('Shape', 1))) for c in components]
			else:
				result = [str(c) for c in components]

		elif returnType is int:
			result={}
			for c in components:
				obj = pm.ls(c, objectsOnly=1)[0]
				num = c.split('[')[-1].rstrip(']')

				if flatten:
					componentNum = int(num)
				else:
					n = [int(n) for n in num.split(':')]
					componentNum = tuple(n) if len(n)>1 else n[0]

				if obj in result:
					result[obj].append(componentNum)
				else:
					result[obj] = [componentNum]

		elif returnType is object:
			result = pm.ls(components)

		return result


	@staticmethod
	def getUvShellSets(objects=None, returnType='shells'):
		'''
		Get All UV shells and their corresponding sets of faces.

		:Parameters:
			objects (obj)(list) = Polygon object(s) or Polygon face(s).
			returnType (str) = The desired returned type. valid values are: 'shells', 'shellIDs'. If None is given, the full dict will be returned.

		:Return:
			(list)(dict) dependant on the given returnType arg. ex. {0L:[[MeshFace(u'pShape.f[0]'), MeshFace(u'pShape.f[1]')], 1L:[[MeshFace(u'pShape.f[2]'), MeshFace(u'pShape.f[3]')]}
		'''
		if not objects:
			objects = pm.ls(selection=1, objectsOnly=1, transforms=1, flatten=1)

		if not isinstance(objects, (list, set, tuple)):
			objects=[objects]

		objectType = Init.getObjectType(objects[0])
		if objectType=='Polygon Face':
			faces = objects
		else:
			faces = Init.getComponents('f', objects)

		shells={}
		for face in faces:
			shell_Id = pm.polyEvaluate(face, uvShellIds=True)

			try:
				shells[shell_Id[0]].append(face)
			except KeyError:
				try:
					shells[shell_Id[0]]=[face]
				except IndexError:
					pass

		if returnType=='shells':
			shells = shells.values()
		elif returnType=='shellIDs':
			shells = shells.keys()

		return shells


	@staticmethod
	def getUvShellBorderEdges(objects):
		'''
		Get the edges that make up any UV islands of the given objects.

		:Parameters:
			objects (str)(obj)(list) = Polygon mesh objects.

		:Return:
			(list) uv border edges.
		'''
		mesh_edges=[]
		for obj in pm.ls(objects, objectsOnly=1):
			try: # Try to get edges from provided objects.
				mesh_edges.extend(pm.ls(pm.polyListComponentConversion(obj, te=True), fl=True, l=True))
			except:
				pass

		if len(mesh_edges)<=0: # Error if no valid objects were found
			raise RuntimeError('No valid mesh objects or components were provided.')

		pm.progressWindow(t='Find UV Border Edges', pr=0, max=len(mesh_edges), ii=True) # Start progressWindow
		
		uv_border_edges = list() # Find and return uv border edges
		for edge in mesh_edges:  # Filter through the mesh(s) edges.

			if pm.progressWindow(q=True, ic=True): # Kill if progress window is cancelled
				pm.progressWindow(ep=True)  # End progressWindow
				raise RuntimeError('Cancelled by user.')

			pm.progressWindow(e=True, s=1, st=edge) # Update the progress window status
			
			edge_uvs = pm.ls(pm.polyListComponentConversion(edge, tuv=True), fl=True)
			edge_faces = pm.ls(pm.polyListComponentConversion(edge, tf=True), fl=True)
			if len(edge_uvs) > 2:  # If an edge has more than two uvs, it is a uv border edge.
				uv_border_edges.append(edge)
			elif len(edge_faces) < 2:  # If an edge has less than 2 faces, it is a border edge.
				uv_border_edges.append(edge)

		pm.progressWindow(ep=True) # End progressWindow

		return uv_border_edges


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
				Init.viewPortMessage("<hl>"+str(nGons[0])+"</hl> N-Gon(s) found.")


	@staticmethod
	def getContigiousIslands(faces, faceIslands=[]):
		'''
		Get a list containing sets of adjacent polygon faces grouped by islands.

		:Parameters:
			faces (list) = Polygon faces to be filtered for adjacent.
			faceIslands (list) = optional. list of sets. ability to add faces from previous calls to the return value.

		:Return:
			(list) of sets of adjacent faces.
		'''
		l=[]
		faces = pm.ls(faces, flatten=1)
		for face in faces:
			borderFaces = Init.getBorderComponents(face, returnType='faces', borderType='component', flatten=True)
			l.append(set([f for f in borderFaces if f in faces]))

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

		:Parameters:
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
	def getBorderComponents(x, returnType='unchanged', borderType='object', flatten=False):
		'''
		Get any object border components from a given component(s) or a polygon object.

		:Parameters:
			x (obj)(list) = Component(s) (or a polygon object) to find any border components for.
			returnType (str) = The desired returned component type. (valid: 'vertices', 'edges', 'faces', 'unchanged'(default, the returnType will be the same as the given object type))
			borderType (str) = The desired border type. (valid: 'component', 'object'(default))
			flatten (bool) = Flattens the returned list of objects so that each component is identified individually.

		:Return:
			(list)

		ex. borderVertices = getBorderComponents(selection, returnType='vertices', borderType='component', flatten=True)
		'''
		if not isinstance(x,(list,tuple,set)): #assure that x is iterable.
			x = [x]

		object_type = Init.getObjectType(x[0])
		if object_type=='Polygon':
			x = Init.getComponents('e', x)
		elif object_type=='Polygon Vertex':
			x = pm.polyListComponentConversion(x, fromVertex=1, toEdge=1)
		elif object_type=='Polygon Face':
			x = pm.polyListComponentConversion(x, fromFace=1, toEdge=1)

		result=[]
		edges = pm.ls(x, flatten=1)
		for edge in edges:

			if borderType is 'object': #get edges that form the border of the object.
				attachedFaces = pm.ls(pm.polyListComponentConversion(edge, fromEdge=1, toFace=1), flatten=1)
				if len(attachedFaces) is 1:
					result.append(edge)

			elif borderType is 'component' and not object_type=='Polygon': #get edges that form the border of the given components.
				attachedFaces = pm.ls(pm.polyListComponentConversion(edge, fromEdge=1, toFace=1), flatten=0)
				attachedEdges = pm.ls(pm.polyListComponentConversion(attachedFaces, fromFace=1, toEdge=1), flatten=1)
				for e in attachedEdges:
					if e not in edges:
						result.append(edge)
						break

		if returnType is 'unchanged': #if no returnType is specified, return the same type of component as given. in the case of 'Polygon' object, edges will be returned.
			returnType = object_type if not object_type=='Polygon' else 'Polygon Edge'
		#convert back to the original component type and flatten /un-flatten list.
		if returnType in ('Polygon Vertex', 'vertices', 'vertex', 'vtx'):
			result = pm.ls(pm.polyListComponentConversion(result, fromEdge=1, toVertex=1), flatten=flatten) #vertices.
		elif returnType in ('Polygon Edge', 'edges', 'edge', 'e'):
			result = pm.ls(pm.polyListComponentConversion(result, fromEdge=1, toEdge=1), flatten=flatten) #edges.
		elif returnType in ('Polygon Face', 'faces', 'face', 'f'):
			result = pm.ls(pm.polyListComponentConversion(result, fromEdge=1, toFace=1), flatten=flatten) #faces.

		return result


	@staticmethod
	def getDistanceBetweenTwoObjects(obj1, obj2):
		'''
		Get the magnatude of a vector using the center points of two given objects.

		:Parameters:
			obj1 (obj)(str) = Object, object name, or point (x,y,z).
			obj2 (obj)(str) = Object, object name, or point (x,y,z).

		:Return:
			(float)

		# xmin, ymin, zmin, xmax, ymax, zmax = pm.exactWorldBoundingBox(startAndEndCurves)
		'''
		x1, y1, z1 = pm.objectCenter(obj1)
		x2, y2, z2 = pm.objectCenter(obj2)

		from math import sqrt
		distance = sqrt(pow((x1-x2),2) + pow((y1-y2),2) + pow((z1-z2),2))

		return distance


	@staticmethod
	def getClosestCV(x, curves, tolerance=0.0):
		'''
		Find the closest control vertex between the given vertices, CVs, or objects and each of the given curves.

		:Parameters:
			x (str)(obj)(list) = Polygon vertices, control vertices, objects, or points given as (x,y,z) tuples.
			curves (str)(obj)(list) = The reference object in which to find the closest CV for each vertex in the list of given vertices.
			tolerance (int)(float) = Maximum search distance. Default is 0.0, which turns off the tolerance flag.

		:Return:
			(dict) closest vertex/cv pairs (one pair for each given curve) ex. {<vertex from set1>:<vertex from set2>}.

		ex. 
			vertices = Init.getComponents('vtx', objects)
			closestVerts = getClosestCV(curve0, curves)
		'''
		pm.undoInfo(openChunk=True)
		x = pm.ls(x, flatten=1) #assure x arg is a list (if given as str or single object).

		npcNode = pm.ls(pm.createNode('nearestPointOnCurve'))[0] #create a nearestPointOnCurve node.

		result={}
		for curve in pm.ls(curves):

			pm.connectAttr(curve.worldSpace, npcNode.inputCurve, force=1) #Connect the curve's worldSpace geometry to the npc node.

			for i in x:
				if not isinstance(i, (tuple, list, set)):
					pos = pm.pointPosition(i)
				else:
					pos = i
				pm.setAttr(npcNode.inPosition, pos)

				distance = Init.getDistanceBetweenTwoPoints(pos, pm.getAttr(npcNode.position))
				p = pm.getAttr(npcNode.parameter)
				if not tolerance:
					result[i] = p
				elif distance < tolerance:
					result[i] = p

		pm.delete(npcNode)

		pm.undoInfo(closeChunk=True)

		return result


	@staticmethod
	def getCvInfo(c, returnType='cv', filter_=[]):
		'''
		Get a dict containing CV's of the given curve(s) and their corresponding point positions.

		:Parameters:
			c (str)(obj)(list) = Curves or CVs to get CV info from.
			returnType (str) = The desired returned values. Default is 'cv'.
				valid values are: 
				'cv' - Return a list of all CV's for the given curves.
				'count' - Return an integer representing the total number of cvs for each of the curves given.
				'parameter', 'position', 'index', 'localPosition', 'tangent', 'normalizedTangent', 'normal', 'normalizedNormal', 'curvatureRadius', 'curvatureCenter'
				- Return a dict with CV's as keys and the returnType as their corresponding values.
				ex. {NurbsCurveCV(u'polyToCurveShape7.cv[5]'): [-12.186520865542082, 15.260936896515751, -369.6159740743584]}
			filter_ (str)(obj)(list) = Value(s) to filter for in the returned results.

		:Return:
			(dict)(list)(int) returns a list if more than one object is returned, else just a single value.

		ex. cv_tan = getCvInfo(curve.cv[0:2],'tangent') #get CV tangents for cvs 0-2.
		ex. cvParam = getCvInfo(curve, 'parameters') #get the curves CVs and their corresponding U parameter values.
		ex. filtered = getCvInfo(<curve>, 'normal', <normal>) #filter results for those that match the given value.
		'''
		result={}
		for curve in pm.ls(c):

			if '.cv' in str(curve): #if CV given.
				cvs = curve
				curve = pm.listRelatives(cvs, parent=1)
			else: #if curve(s) given
				cvs = curve.cv

			parameters = Init.getClosestCV(cvs, curve) #use getClosestCV to get the parameter location for each of the curves CVs.
			for cv, p in parameters.items():

				if returnType is 'position': # Get cv position
					v = pm.pointOnCurve(curve, parameter=p, position=True)
				elif returnType is 'localPosition':
					v = pm.getAttr(cv) # local cv position
				elif returnType is 'tangent': # Get cv tangent
					v = pm.pointOnCurve(curve, parameter=p, tangent=True)
				elif returnType is 'normalizedTangent':
					v = pm.pointOnCurve(curve, parameter=p, normalizedTangent=True)
				elif returnType is 'normal': # Get cv normal
					v = pm.pointOnCurve(curve, parameter=p, normal=True)
				elif returnType is 'normalizedNormal':
					v = pm.pointOnCurve(curve, parameter=p, normalizedNormal=True) #Returns the (x,y,z) normalized normal of curve1 at parameter 0.5.
				elif returnType is 'curvatureRadius': # Get cv curvature
					v = pm.pointOnCurve(curve, parameter=p, curvatureRadius=True) #Returns the curvature radius of curve1 at parameter 0.5.
				elif returnType is 'curvatureCenter':
					v = pm.pointOnCurve(curve, parameter=p, curvatureCenter=True)
				elif returnType is 'parameter': # Return the CVs parameter.
					v = p
				elif returnType is 'count': # total number of cv's for the curve.
					result[curve] = len(Init.getCvInfo(curve))
					break
				elif returnType is 'index': # index of the cv
					s = str(cv)
					v = int(s[s.index('[')+1:s.index(']')])
				else:
					v = None

				result[cv] = v

		if returnType is 'cv':
			result = result.keys()

		if filter_:
			if not isinstance(filter_, (tuple, set, list)):
				filter_ = list(filter_)
			try:
				result = {k:v for k,v in result.items() if any((v in filter_, v==filter_))}
			except AttributeError:
				result = [i for i in result if any((i in filter_, i==filter_))]

		if len(result) is 1:
			try:
				result = result.values()[0]
			except AttributeError, TypeError:
				result = result[0]

		return result


	@staticmethod
	def getCrossProductOfCurves(curves, normalize=1, values=False):
		'''
		Get the cross product of two vectors using points derived from the given curves.

		:Parameters:
			curves (str)(obj)(list) = Nurbs curve(s).
			normalize (float) = (0) Do not normalize. (1) Normalize standard. (value other than 0 or 1) Normalize using the given float value as desired length.
			values (bool) = Return only a list of the cross product vector values [(<Vx>, <Vy>, <Vz>)] instead of the full dict {<curve1>:(<Vx>, <Vy>, <Vz>)}.

		:Return:
			(dict)(list)
		'''
		result={}
		for curve in pm.ls(curves):
			p0 = pm.objectCenter(curve)

			cvs = Init.getComponents('cv', curve, returnType=object, flatten=1)
			cvPos = Init.getCvInfo(curve, 'position')
			p1 = cvPos[cvs[0]]
			p2 = cvPos[cvs[(len(cvs)/2)]]

			n1 = Init.getCrossProduct(p0, p1, p2, normalize=normalize)

			result[curve] = n1

		if values:
			result = result.values()
		return result


	@staticmethod
	def getClosestVerts(set1, set2, tolerance=100):
		'''
		Find the two closest vertices between the two sets of vertices.

		:Parameters:
			set1 (list) = The first set of vertices.
			set2 (list) = The second set of vertices.
			tolerance (int) = Maximum search distance.

		:Return:
			(list) closest vertex pairs by order of distance (excluding those not meeting the tolerance). (<vertex from set1>, <vertex from set2>).

		ex. verts1 = Init.getComponents('vtx', 'pCube1')
			verts2 = Init.getComponents('vtx', 'pCube2')
			closestVerts = getClosestVerts(verts1, verts2)
		'''
		vertPairsAndDistance={}
		for v1 in set1:
			v1Pos = pm.pointPosition(v1, world=1)
			for v2 in set2:
				v2Pos = pm.pointPosition(v2, world=1)
				distance = Init.getDistanceBetweenTwoPoints(v1Pos, v2Pos)
				if distance<tolerance:
					vertPairsAndDistance[(v1, v2)] = distance

		import operator
		sorted_ = sorted(vertPairsAndDistance.items(), key=operator.itemgetter(1))

		vertPairs = [i[0] for i in sorted_]

		return vertPairs


	@staticmethod
	def getClosestVertex(vertices, obj, tolerance=0.0, freezeTransforms=False):
		'''
		Find the closest vertex of the given object for each vertex in the list of given vertices.

		:Parameters:
			vertices (list) = A set of vertices.
			obj (obj) = The reference object in which to find the closest vertex for each vertex in the list of given vertices.
			tolerance (float) = Maximum search distance. Default is 0.0, which turns off the tolerance flag.
			freezeTransforms (bool) = Reset the selected transform and all of its children down to the shape level.

		:Return:
			(dict) closest vertex pairs {<vertex from set1>:<vertex from set2>}.

		ex. obj1, obj2 = selection
			vertices = Init.getComponents('vtx', obj1)
			closestVerts = getClosestVertex(vertices, obj2, tolerance=10)
		'''
		pm.undoInfo(openChunk=True)
		if freezeTransforms:
			pm.makeIdentity(obj, apply=True)

		obj2Shape = pm.listRelatives(obj, children=1, shapes=1)[0] #pm.listRelatives(obj, fullPath=False, shapes=True, noIntermediate=True)

		cpmNode = pm.ls(pm.createNode('closestPointOnMesh'))[0] #create a closestPointOnMesh node.
		pm.connectAttr(obj2Shape.outMesh, cpmNode.inMesh, force=1) #object's shape mesh output to the cpm node.

		closestVerts={}
		for v1 in pm.ls(vertices, flatten=1):
			v1Pos = pm.pointPosition(v1, world=True)
			pm.setAttr(cpmNode.inPosition, v1Pos[0], v1Pos[1], v1Pos[2], type="double3") #set a compound attribute

			index = pm.getAttr(cpmNode.closestVertexIndex) #vertex Index. | ie. result: [34]
			v2 = obj2Shape.vtx[index]

			v2Pos = pm.pointPosition(v2, world=True)
			distance = Init.getDistanceBetweenTwoPoints(v1Pos, v2Pos)

			if not tolerance:
				closestVerts[v1] = v2
			elif distance < tolerance:
				closestVerts[v1] = v2

		pm.delete(cpmNode)
		pm.undoInfo(closeChunk=True)

		return closestVerts


	@staticmethod
	def snapClosestVerts(obj1, obj2, tolerance=10.0, freezeTransforms=False):
		'''
		Snap the vertices from object one to the closest verts on object two.

		:Parameters:
			obj1 (obj) = The object in which the vertices are moved from.
			obj2 (obj) = The object in which the vertices are moved to.
			tolerance (float) = Maximum search distance.
			freezeTransforms (bool) = Reset the selected transform and all of its children down to the shape level.
		'''
		vertices = Init.getComponents('vtx', obj1)
		closestVerts = Init.getClosestVertex(vertices, obj2, tolerance=tolerance, freezeTransforms=freezeTransforms)

		progressBar = mel.eval("$container=$gMainProgressBar");
		pm.progressBar(progressBar, edit=True, beginProgress=True, isInterruptable=True, status="Snapping Vertices ...", maxValue=len(closestVerts)) 

		pm.undoInfo(openChunk=True)
		for v1, v2 in closestVerts.items():
			if pm.progressBar(progressBar, query=True, isCancelled=True):
				break

			v2Pos = pm.pointPosition(v2, world=True)
			pm.xform(v1, translation=v2Pos, worldSpace=True)

			pm.progressBar(progressBar, edit=True, step=1)
		pm.undoInfo(closeChunk=True)

		pm.progressBar(progressBar, edit=True, endProgress=True)


	@staticmethod
	def alignVertices (mode, average=False, edgeloop=False):
		'''
		Align vertices.

		:Parameters:
			mode (int) = possible values are align: 0-YZ, 1-XZ, 2-XY, 3-X, 4-Y, 5-Z, 6-XYZ 
			average (bool) = align to average of all selected vertices. else, align to last selected
			edgeloop (bool) = align vertices in edgeloop from a selected edge

		ex. self.alignVertices(mode=3, average=True, edgeloop=True)
		'''
		pm.undoInfo (openChunk=True)
		selectTypeEdge = pm.selectType (query=True, edge=True)

		if edgeloop:
			mel.eval("SelectEdgeLoopSp;") #select edgeloop

		mel.eval('PolySelectConvert 3;') #convert to vertices
		
		selection = pm.ls(selection=1, flatten=1)
		lastSelected = pm.ls(tail=1, selection=1, flatten=1)
		alignTo = pm.xform(lastSelected, query=1, translation=1, worldSpace=1)
		alignX = alignTo[0]
		alignY = alignTo[1]
		alignZ = alignTo[2]
		
		if average:
			xyz = pm.xform(selection, query=1, translation=1, worldSpace=1)
			x = xyz[0::3]
			y = xyz[1::3]
			z = xyz[2::3]
			alignX = float(sum(x))/(len(xyz)/3)
			alignY = float(sum(y))/(len(xyz)/3)
			alignZ = float(sum(z))/(len(xyz)/3)

		if len(selection)<2:
			if len(selection)==0:
				Init.viewPortMessage("No vertices selected")
			Init.viewPortMessage("Selection must contain at least two vertices")

		for vertex in selection:
			vertexXYZ = pm.xform(vertex, query=1, translation=1, worldSpace=1)
			vertX = vertexXYZ[0]
			vertY = vertexXYZ[1]
			vertZ = vertexXYZ[2]
			
			modes = {
				0:(vertX, alignY, alignZ), #align YZ
				1:(alignX, vertY, alignZ), #align XZ
				2:(alignX, alignY, vertZ), #align XY
				3:(alignX, vertY, vertZ),
				4:(vertX, alignY, vertZ),
				5:(vertX, vertY, alignZ),
				6:(alignX, alignY, alignZ), #align XYZ
			}

			pm.xform(vertex, translation=modes[mode], worldSpace=1)

		if selectTypeEdge:
			pm.selectType (edge=True)
		pm.undoInfo (closeChunk=True)


	@staticmethod
	def findNonManifoldVertex(objects, select=True):
		'''
		Locate a connected vertex of non-manifold geometry where the faces share a single vertex.

		:Parameters:
			objects (str)(obj) = A polygon mesh or a list of meshes.
			select (bool) = Select any found non-manifold vertices. (default is True)

		:Return:
			(list) any found non-manifold verts.
		'''
		pm.undoInfo(openChunk=True)

		nonManifoldVerts=set()

		vertices = Init.getComponents('vtx', objects)
		for vertex in vertices:

			connected_faces = pm.polyListComponentConversion(vertex, fromVertex=1, toFace=1) #pm.mel.PolySelectConvert(1) #convert to faces
			connected_faces_flat = pm.ls(connected_faces, flatten=1) #selectedFaces = pm.ls(sl=1, flatten=1)

			#get a list of the edges of each face that is connected to the original vertex.
			edges_sorted_by_face=[]
			for face in connected_faces_flat:

				connected_edges = pm.polyListComponentConversion(face, fromFace=1, toEdge=1) #pm.mel.PolySelectConvert(1) #convert to faces
				connected_edges_flat = pm.ls(connected_edges, flatten=1) #selectedFaces = pm.ls(sl=1, flatten=1)

				edges_sorted_by_face.append(connected_edges_flat)


			out=[] #1) take first set A from list. 2) for each other set B in the list do if B has common element(s) with A join B into A; remove B from list. 3) repeat 2. until no more overlap with A. 4) put A into outpup. 5) repeat 1. with rest of list.
			while len(edges_sorted_by_face)>0:
				first, rest = edges_sorted_by_face[0], edges_sorted_by_face[1:] #first, *rest = edges
				first = set(first)

				lf = -1
				while len(first)>lf:
					lf = len(first)

					rest2=[]
					for r in rest:
						if len(first.intersection(set(r)))>0:
							first |= set(r)
						else:
							rest2.append(r)     
					rest = rest2

				out.append(first)
				edges_sorted_by_face = rest

			if len(out)>1:
				nonManifoldVerts.add(vertex)

		pm.undoInfo(closeChunk=True)

		if select:
			pm.select(nonManifoldVerts, add=1)
		return nonManifoldVerts


	@staticmethod
	def splitNonManifoldVertex(vertex, select=True):
		'''
		Separate a connected vertex of non-manifold geometry where the faces share a single vertex.

		:Parameters:
			vertex (str)(obj) = A single polygon vertex.
			select (bool) = Select the vertex after the operation. (default is True)
		'''
		pm.undoInfo(openChunk=True)

		connected_faces = pm.polyListComponentConversion(vertex, fromVertex=1, toFace=1) #pm.mel.PolySelectConvert(1) #convert to faces
		connected_faces_flat = pm.ls(connected_faces, flatten=1) #selectedFaces = pm.ls(sl=1, flatten=1)

		pm.polySplitVertex(vertex)

		#get a list for the vertices of each face that is connected to the original vertex.
		verts_sorted_by_face=[]
		for face in connected_faces_flat:

			connected_verts = pm.polyListComponentConversion(face, fromFace=1, toVertex=1) #pm.mel.PolySelectConvert(1) #convert to faces
			connected_verts_flat = pm.ls(connected_verts, flatten=1) #selectedFaces = pm.ls(sl=1, flatten=1)

			verts_sorted_by_face.append(connected_verts_flat)


		out=[] #1) take first set A from list. 2) for each other set B in the list do if B has common element(s) with A join B into A; remove B from list. 3) repeat 2. until no more overlap with A. 4) put A into outpup. 5) repeat 1. with rest of list.
		while len(verts_sorted_by_face)>0:
			first, rest = verts_sorted_by_face[0], verts_sorted_by_face[1:] #first, *rest = edges
			first = set(first)

			lf = -1
			while len(first)>lf:
				lf = len(first)

				rest2=[]
				for r in rest:
					if len(first.intersection(set(r)))>0:
						first |= set(r)
					else:
						rest2.append(r)     
				rest = rest2

			out.append(first)
			verts_sorted_by_face = rest


		for vertex_set in out:
			pm.polyMergeVertex(vertex_set, distance=0.001)

		pm.select(vertex_set, deselect=1) #deselect the vertices that were selected during the polyMergeVertex operation.
		if select:
			pm.select(vertex, add=1)

		pm.undoInfo(closeChunk=True)


	@staticmethod
	def getEdgePath(components, returnType=''):
		'''
		Query the polySelect command for the components along different edge paths.

		:Parameters:
			components (str)(obj)(list) = The components used for the query (dependant on the operation type).
			returnType (str) = The desired return type. 'shortestEdgePath', 'edgeRing', 'edgeRingPath', 'edgeLoop', 'edgeLoopPath'.

		:Return:
			(list) The components comprising the path.
		'''
		components = pm.ls(components, flatten=1)
		obj = Init.getObjectFromComponent(components[0])
		componentNumbers = Init.getComponents(components, returnType=int, flatten=1).values()[0] #get the vertex numbers as integer values. ie. [818, 1380]

		edgesLong=None
		if returnType=='shortestEdgePath':
			edgesLong = pm.polySelect(obj, query=1, shortestEdgePath=(componentNumbers[0], componentNumbers[1])) #(vtx, vtx)

		elif returnType=='edgeRing':
			edgesLong = pm.polySelect(obj, query=1, edgeRing=componentNumbers) #(e..)

		elif returnType=='edgeRingPath':
			edgesLong = pm.polySelect(obj, query=1, edgeRingPath=(componentNumbers[0], componentNumbers[1])) #(e, e)

		elif returnType=='edgeLoop':
			edgesLong = pm.polySelect(obj, query=1, edgeLoop=componentNumbers) #(e..)

		elif returnType=='edgeLoopPath':
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

		:Parameters:
			components (obj) = A Pair of vertices or edges.
			step (int) = step amount.

		:Return:
			(list) the components that comprise the path as strings.
		'''
		type_ = Init.getObjectType(components[0])
		
		result=[]
		objects = set(pm.ls(components, objectsOnly=1))
		for obj in objects:

			if type_=='Polygon Edge':
				components = [pm.ls(pm.polyListComponentConversion(e, fromEdge=1, toVertex=1), flatten=1) for e in components]
				closestVerts = Init.getClosestVerts(components[0], components[1])[0]
				edges = Init.getEdgePath(closestVerts, 'shortestEdgePath')
				[result.append(e) for e in edges]

			elif type_=='Polygon Vertex':
				closestVerts = Init.getClosestVerts(components[0], components[1])[0]
				edges = Init.getEdgePath(closestVerts, 'shortestEdgePath')
				vertices = pm.ls(pm.polyListComponentConversion(edges, fromEdge=1, toVertex=1), flatten=1)
				[result.append(v) for v in vertices]

		return result


	@staticmethod
	def getPathAlongLoop(components=None, step=1):
		'''
		Get the shortest path between to vertices or edges along an edgeloop.

		:Parameters:
			components (obj) = A Pair of vertices, edges, or faces.
			step (int) = step amount.

		:Return:
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

				closestVerts = Init.getClosestVerts(vertices[0], vertices[1])[0]
				_edges = pm.ls(pm.polyListComponentConversion(list(components)+list(closestVerts), fromVertex=1, toEdge=1), flatten=1)

				edges=[]
				for edge in _edges:
					verts = pm.ls(pm.polyListComponentConversion(edge, fromEdge=1, toVertex=1), flatten=1)
					if closestVerts[0] in verts and components[0] in verts or closestVerts[1] in verts and components[1] in verts:
						edges.append(edge)

				edges = Init.getEdgePath(edges, 'edgeLoopPath')

				vertices = [pm.ls(pm.polyListComponentConversion(edges, fromEdge=1, toVertex=1), flatten=1)]
				[result.append(v) for v in vertices]


			elif type_=='Polygon Edge':
				edges = Init.getEdgePath(components, 'edgeLoopPath')
				[result.append(e) for e in edges]


			elif type_=='Polygon Face':
				vertices=[]
				for component in components:
					edges = pm.ls(pm.polyListComponentConversion(component, fromFace=1, toEdge=1), flatten=1)
					_vertices = pm.ls(pm.polyListComponentConversion(edges, fromEdge=1, toVertex=1), flatten=1)
					vertices.append(_vertices)

				closestVerts1 = Init.getClosestVerts(vertices[0], vertices[1])[0]
				closestVerts2 = Init.getClosestVerts(vertices[0], vertices[1])[1] #get the next pair of closest verts

				_edges = pm.ls(pm.polyListComponentConversion(closestVerts1+closestVerts2, fromVertex=1, toEdge=1), flatten=1)
				edges=[]
				for edge in _edges:
					verts = pm.ls(pm.polyListComponentConversion(edge, fromEdge=1, toVertex=1), flatten=1)
					if closestVerts1[0] in verts and closestVerts2[0] in verts or closestVerts1[1] in verts and closestVerts2[1] in verts:
						edges.append(edge)

				edges = Init.getEdgePath(edges, 'edgeRingPath')

				faces = pm.ls(pm.polyListComponentConversion(edges, fromEdge=1, toFace=1), flatten=1)
				[result.append(f) for f in faces]

		return result


	@staticmethod
	def getEdgeLoop(edges=None, step=1):
		'''
		Get the corresponding edgeloop(s) from the given edges.

		:Parameters:
			edges (list) = Polygon Edges.
			step (int) = step amount.

		:Return:
			(list) the edges that comprise the edgeloops as strings.
		'''
		result=[]
		objects = set(pm.ls(edges, objectsOnly=1))
		for obj in objects:
			edges = Init.getEdgePath(pm.ls(edges, flatten=1), 'edgeLoop')
			[result.append(i) for i in edges]

		return result


	@staticmethod
	def getEdgeRing(edges=None, step=1):
		'''
		Get the corresponding edgering(s) from the given edges.

		:Parameters:
			edges (list) = Polygon Edges.
			step (int) = step amount.

		:Return:
			(list) the edges that comprise the edgerings as strings.
		'''
		result=[]
		objects = set(pm.ls(edges, objectsOnly=1))
		for obj in objects:

			edges = Init.getEdgePath(pm.ls(edges, flatten=1), 'edgeRing')
			[result.append(i) for i in edges]

		return result


	@staticmethod
	def getComponentPoint(component, alignToNormal=False):
		'''
		Get the center point from the given component.

		:Parameters: alignToNormal=bool - 

		:Return: [float list] - x, y, z  coordinate values.
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

		:Parameters:
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


	@staticmethod
	def deleteAlongAxis(obj, axis):
		'''
		Delete components of the given mesh object along the specified axis.

		:Parameters:
			obj (obj) = Mesh object.
			axis (str) = Axis to delete on. ie. '-x' Components belonging to the mesh object given in the 'obj' arg, that fall on this axis, will be deleted. 
		'''
		for node in [n for n in pm.listRelatives(obj, allDescendents=1) if pm.objectType(n, isType='mesh')]: #get any mesh type child nodes of obj.
			faces = Init.getAllFacesOnAxis(node, axis)
			if len(faces)==pm.polyEvaluate(node, face=1): #if all faces fall on the specified axis.
				pm.delete(node) #delete entire node
			else:
				pm.delete(faces) #else, delete any individual faces.

		Init.viewPortMessage("Delete faces on <hl>"+axis.upper()+"</hl>.")



	# -----------------------------------------------
	' Normals'
	# -----------------------------------------------


	@staticmethod
	def getNormalVector(name=None):
		'''
		Get the normal vectors from the given poly object.
		If no argument is given the normals for the current selection will be returned.
		:Parameters:
			name (str) = polygon mesh or component.
		:Return:
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

		regEx = "[A-Z]*_[A-Z]* *[0-9]*: "

		dict_={}
		for n in normals:
			l = list(s.replace(regEx,'') for s in n.split(' ') if s) #['FACE_NORMAL', '150:', '0.935741', '0.110496', '0.334931\n']

			key = int(l[1].strip(':')) #int face number as key ie. 150
			value = list(float(i) for i in l[-3:])  #vector list as value. ie. [[0.935741, 0.110496, 0.334931]]
			dict_[key] = value

		return dict_


	@staticmethod
	def getFacesWithSimilarNormals(faces, transforms=[], similarFaces=[], rangeX=0.1, rangeY=0.1, rangeZ=0.1, returnType=unicode, returnNodeType='transform'):
		'''
		Filter for faces with normals that fall within an X,Y,Z tolerance.

		:Parameters:
			faces (list) = ['polygon faces'] - faces to find similar normals for.
			similarFaces (list) = optional ability to add faces from previous calls to the return value.
			transforms (list) = [<shape nodes>] - objects to check faces on. If none are given the objects containing the given faces will be used.
			rangeX = float - x axis tolerance
			rangeY = float - y axis tolerance
			rangeZ = float - z axis tolerance
			returnType (type) = The desired returned object type. (valid: unicode(default, str, int, object)
			returnNodeType (str) = Specify whether the components are returned with the transform or shape nodes (valid only with str and unicode returnTypes). (valid: 'transform', 'shape'(default)) ex. 'pCylinder1.f[0]' or 'pCylinderShape1.f[0]'

		:Return:
			(list) faces that fall within the given normal range.

		ex. getFacesWithSimilarNormals(selectedFaces, rangeX=0.5, rangeY=0.5, rangeZ=0.5)
		'''
		faces = pm.ls(faces, flatten=1) #work on a copy of the argument so that removal of elements doesn't effect the passed in list.
		for face in faces:
			normals = Init.getNormalVector(face)

			for k, v in normals.items():
				sX = v[0]
				sY = v[1]
				sZ = v[2]

				if not transforms:
					transforms = Init.getObjectFromComponent(face)

				for node in transforms:
					for f in Init.getComponents('f', node, returnType=returnType, returnNodeType=returnNodeType, flatten=1):

						n = Init.getNormalVector(f)
						for k, v in n.items():
							nX = v[0]
							nY = v[1]
							nZ = v[2]

							if sX<=nX + rangeX and sX>=nX - rangeX and sY<=nY + rangeY and sY>=nY - rangeY and sZ<=nZ + rangeZ and sZ>=nZ - rangeZ:
								similarFaces.append(f)
								if f in faces: #If the face is in the loop que, remove it, as has already been evaluated.
									faces.remove(f)

		return similarFaces









	# ------------------------------------------------
	' TRANSFORMATION'
	# ------------------------------------------------

	@staticmethod
	def aimObjectAt(obj, target_pos, aim_vect=(1,0,0), up_vect=(0,1,0)):
		'''
		Aim supplied object at supplied world space position.

		Args:
			obj (str)(obj) = Transform node.
			target_pos (tuple) = The (x,y,z) world position to aim at.
			aim_vect (tuple) = Local axis to aim at the target position.
			up_vect (tuple) = Secondary axis aim vector.
		 '''
		target = pm.createNode('transform')

		pm.xform(target, translation=target_pos, absolute=True)
		const = pm.aimConstraint((target, obj), aim=aim_vect, worldUpVector=up_vect, worldUpType="vector")

		pm.delete(const, target)


	@staticmethod
	def rotateAxis(obj, target_pos):
		''' 
		Aim transform <obj> at world space point <target>.
		All rotations in rotated channel, geometry is transformed so it does not appear to move during this transformation

		Args:
			obj (str)(obj) = Transform node.
			target_pos (tuple) = An (x,y,z) world position.
		'''
		obj = pm.ls(obj)[0]
		Init.aimObjectAt(obj, target_pos)

		try:
			c = obj.v[:]
		except TypeError:
			c = obj.cv[:]

		wim = pm.getAttr(obj.worldInverseMatrix)
		pm.xform(c, matrix=wim)

		pos = pm.xform(obj, q=True, translation=True, absolute=True, worldSpace=True)
		pm.xform(c, translation=pos, relative=True, worldSpace=True)


	@staticmethod
	def getOrientation(obj, returnType='point'):
		'''
		Get an objects orientation.

		:Parameters:
			obj (str)(obj) = The object to get the orientation of.
			returnType (str) = The desired returned value type. (valid: 'point', 'vector')(default: 'point')

		:Return:
			(tuple)
		'''
		obj = pm.ls(obj)[0]

		world_matrix = pm.xform(obj, q=True, matrix=True, worldSpace=True)
		rAxis = pm.getAttr(obj.rotateAxis)
		if any((rAxis[0], rAxis[1], rAxis[2])):
			print('# Warning: {} has a modified .rotateAxis of {} which is included in the result. #'.format(obj, rAxis))

		if returnType is 'vector':
			from maya.api.OpenMaya import MVector

			result = (
				MVector(world_matrix[0:3]),
				MVector(world_matrix[4:7]),
				MVector(world_matrix[8:11])
			)

		else:
			result = (
				world_matrix[0:3],
				world_matrix[4:7],
				world_matrix[8:11]
			)

		return result









	# ------------------------------------------------
	' DAG objects'
	# ------------------------------------------------

	@staticmethod
	def getMelGlobals(keyword=None, caseSensitive=False):
		'''
		Get global MEL variables.

		:Parameters:
			keyword (str) = search string.

		:Return:
			(list)
		'''
		variables = [
			v for v in sorted(mel.eval('env')) 
				if not keyword 
					or (v.count(keyword) if caseSensitive else v.lower().count(keyword.lower()))
		]

		return variables


	@staticmethod
	def getObjectType(obj, returnType='objectType'):
		'''
		Get the type of a given object.

		:Parameters:
			obj (obj) = A single maya component.
			returnType (str) = Specify the desired return value type. 'mask' will return the maya mask value as an integer. (valid: 'objectType', 'mask')(default: 'objectType')

		:Return:
			(str)(int) matching type from the types dict.
		'''
		types = {0:'Handle', 9:'Nurbs Curve', 10:'Nurbs Surfaces', 11:'Nurbs Curves On Surface', 12:'Polygon', 22:'Locator XYZ', 23:'Orientation Locator', 
			24:'Locator UV', 28:'Control Vertex', 30:'Edit Point', 31:'Polygon Vertex', 32:'Polygon Edge', 34:'Polygon Face', 35:'Polygon UV', 36:'Subdivision Mesh Point', 
			37:'Subdivision Mesh Edge', 38:'Subdivision Mesh Face', 39:'Curve Parameter Point', 40:'Curve Knot', 41:'Surface Parameter Point', 42:'Surface Knot', 
			43:'Surface Range', 44:'Trim Surface Edge', 45:'Surface Isoparm', 46:'Lattice Point', 47:'Particle', 49:'Scale Pivot', 50:'Rotate Pivot', 51:'Select Handle', 
			68:'Subdivision Surface', 70:'Polygon Vertex Face', 72:'NURBS Surface Face', 73:'Subdivision Mesh UV'}

		for k, v in types.items():
			if pm.filterExpand(obj, sm=k):
				return v if returnType is 'objectType' else k


	@staticmethod
	def getObjectFromComponent(components, returnType='transform'):
		'''
		Get the object's transform, shape, or history node from the given components.

		:Parameters:
			components (str)(obj(list) = Component(s).
			returnType (str) = The desired returned node type. (valid: 'transform','shape','history')(default: 'transform')

		:Return:
			(dict) {transform node: [components of that node]}
			ie. {'pCube2': ['pCube2.f[21]', 'pCube2.f[22]', 'pCube2.f[25]'], 'pCube1': ['pCube1.f[21]', 'pCube1.f[26]']}
		'''
		if not isinstance(components,(list, tuple, set)):
			components = [components]

		result={}
		for component in components:
			shapeNode = pm.listRelatives(component, parent=1)[0]
			transform = pm.listRelatives(shapeNode, parent=1)[0]

			if returnType is 'transform':
				node = transform
			elif returnType is 'shape':
				node = shapeNode
			elif returnType is 'history':
				history = pm.listConnections(shapeNode, source=1, destination=0)[0] #get incoming connections: returns list ie. [nt.PolyCone('polyCone1')]
				node = history

			try:
				result[node].append(component)
			except:
				result[node] = [component]

		return result


	@staticmethod
	def isGroup(node):
		'''
		Check if the given node is a group (has a transform AND has no shape children).
		'''
		if (pm.objectType(node, isType='transform')) and (not len(pm.listRelatives(node, shapes=1))):
			return True

		return False


	@staticmethod
	def getTransformNode(node=None, index=0, attributes=False, regEx=''):
		'''
		Get the transform node. 

		:Parameters:
			node (obj) = Node. If nothing is given, the current selection will be used.
			index (int) = Return the transform node at the given index. if Nothing is given, the full list will be returned. ie. index=[:-1] or index=0
			attributes (bool) = Return the attributes of the node, rather then the node itself.
			regEx (str) = 	List only the attributes that match the string(s) passed from this flag. String can be a regular expression.

		:Return:
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
			transforms = pm.listAttr(transforms, read=1, hasData=1, string=regEx)

		return transforms


	@staticmethod
	def getShapeNode(node=None, index=0, attributes=False, regEx=''):
		'''
		Get the shape node. 

		:Parameters:
			node (obj) = Node. If nothing is given, the current selection will be used.
			index (int) = Return the shape node at the given index. if Nothing is given, the full list will be returned. ie. index=[:-1] or index=0
			attributes (bool) = Return the attributes of the node, rather then the node itself.
			regEx (str) = 	List only the attributes that match the string(s) passed from this flag. String can be a regular expression.

		:Return:
			(str) node
		'''
		if not node:
			pm.ls(sl=1, type='transform')

		shapes = pm.listRelatives(node, children=1, shapes=1) #get shape node from transform: returns list ie. [nt.Mesh('pConeShape1')]
		if not shapes:
			shapes = pm.ls(node, type='shape')

		if shapes and index is not None:
			shapes = shapes[index]
		
		if attributes:
			shapes = pm.listAttr(shapes, read=1, hasData=1, string=regEx)

		return shapes


	@staticmethod
	def getHistoryNode(node=None, index=0, attributes=False, regEx=''):
		'''
		Get the history node. 

		:Parameters:
			node (obj) = Node. If nothing is given, the current selection will be used.
			index (int) = Return the transform node at the given index. if Nothing is given, the full list will be returned. ie. index=[:-1] or index=0
			attributes (bool) = Return the attributes of the node, rather then the node itself.
			regEx (str) = 	List only the attributes that match the string(s) passed from this flag. String can be a regular expression.

		:Return:
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
			connections = pm.listAttr(connections, read=1, hasData=1, string=regEx)

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

		:Parameters:
			node (obj) = Transform node.
			include (list) = Attributes to include. All other will be omitted. Exclude takes dominance over include. Meaning, if the same attribute is in both lists, it will be excluded.
			exclude (list) = Attributes to exclude from the returned dictionay. ie. ['Position','Rotation','Scale','renderable','isHidden','isFrozen','selected']

		:Return:
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
					attributes[attr] = pm.getAttr(node+'.'+attr, silent=True)
				except Exception as error:
					print (error)

		return attributes


	@staticmethod
	def setAttributesMEL(node, attributes):
		'''
		Set node attribute values using a dict. 

		:Parameters:
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

		:Parameters:
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


	@staticmethod
	def getMayaMainWindow():
		'''
		Get the main Maya window as a QtWidgets.QMainWindow instance

		:Return:
			QtGui.QMainWindow instance of the top level Maya windows
		'''
		ptr = OpenMayaUI.MQtUtil.mainWindow()
		if ptr:
			return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)


	@staticmethod
	def convertToWidget(name):
		'''
		:Parameters:
			name (str) = name of a Maya UI element of any type. ex. name = mel.eval('$tmp=$gAttributeEditorForm') (from MEL global variable)

		:Return:
			(QWidget) If the object does not exist, returns None
		'''
		for f in ('findControl', 'findLayout', 'findMenuItem'):
			ptr = getattr(OpenMayaUI.MQtUtil, f)(name) #equivalent to: ex. OpenMayaUI.MQtUtil.findControl(name)
			if ptr:
				return shiboken2.wrapInstance(long(ptr), QtWidgets.QWidget)


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

		:Parameters:
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
	def mainProgressBar(size, name="tk_progressBar", stepAmount=1):
		'''
		#add esc key pressed return False

		:Parameters:
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
		:Parameters:
			message (str) = The message to be displayed, (accepts html formatting). General message, inherited by -amg/assistMessage and -smg/statusMessage.
			statusMessage (str) = The status info message to be displayed (accepts html formatting).
			assistMessage (str) = The user assistance message to be displayed, (accepts html formatting).
			position (str) = position on screen. possible values are: topCenter","topRight","midLeft","midCenter","midCenterTop","midCenterBot","midRight","botLeft","botCenter","botRight"

		ex. viewPortMessage("shutting down:<hl>"+str(timer)+"</hl>")
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

		:Parameters:
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
		#:Parameters: command (str) = mel command
		command = ('help ' + command)
		modtext = (mel.eval(command))
		outputscrollField (modtext, "command help", 1.0, 1.0) #text, window_title, width, height


	@staticmethod
	def keywordSearch (keyword): #keyword command search
		#:Parameters: keyword (str) = 
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


# def getBorderFacesOfFaces(faces, includeBordered=False):
# 	'''
# 	Get any faces attached to the given faces.

# 	:Parameters:
# 		faces (unicode, str, list) = faces to get bordering faces for.
# 		includeBordered (bool) = optional. return the bordered face along with the results.

# 	:Return:
# 		list - the border faces of the given faces.
# 	'''
# 	adjEdges = pm.polyListComponentConversion(faces, fromFace=1, toEdge=1)
# 	adjFaces = pm.polyListComponentConversion(adjEdges, toFace=1, fromEdge=1)
# 	expanded = pm.filterExpand(adjFaces, expand=True, selectionMask=34) #keep faces as individual elements.

# 	if includeBordered:
# 		return list(str(f) for f in expanded) #convert unicode to str.
# 	else:
# 		return list(str(f) for f in expanded if f not in faces) #convert unicode to str and exclude the original faces.



	# def getComponents(objects, type_, flatten=True):
	# 	'''
	# 	Get the components of the given type from the given object.

	# 	:Parameters:
	# 		objects (obj)(list) = The polygonal object(s) to get the components of.
	# 		flatten (bool) = Flattens the returned list of objects so that each component is identified individually. (much faster)

	# 	:Return:
	# 		(list) component objects.
	# 	'''
	# 	if isinstance(objects, (str, unicode)):
	# 		objects = pm.ls(objects)

	# 	if not isinstance(objects, (list, set, tuple)):
	# 		objects=[objects]

	# 	types = {'vertices':'vtx', 'edges':'e', 'faces':'f'}

	# 	components=[]
	# 	for obj in objects:
	# 		cmpts = pm.ls('{}.{}[*]'.format(obj, types[type_]), flatten=flatten)
	# 		components+=cmpts

	# 	return components


	# @staticmethod
	# def getSelectedComponents(componentType, objects=None, returnType=str):
	# 	'''
	# 	Get the component selection of the given type.

	# 	:Parameters:
	# 		componentType (str) = The desired component type. (valid values are: 'vertices', 'edges', 'faces')
	# 		objects (obj)(list) = If polygonal object(s) are given, then only selected components from those object(s) will be returned.
	# 		returnType (str) = Desired output style.
	# 				ex. str (default) = [u'test_cube:pCube1.vtx[0]']
	# 					int = {nt.Mesh(u'test_cube:pCube1Shape'): set([0])}
	# 					object = [MeshVertex(u'test_cube:pCube1Shape.vtx[0]')]

	# 	:Return:
	# 		(list)(dict) components (based on given 'componentType' and 'returnType' value).
	# 	'''
	# 	types = {'vertices':31, 'edges':32, 'faces':34}

	# 	if objects:
	# 		selection = pm.ls(objects, sl=1)
	# 		components = pm.filterExpand(selection, selectionMask=types[componentType])
	# 	else:
	# 		components = pm.filterExpand(selectionMask=types[componentType])


	# 	if returnType is str:
	# 		selectedComponents = components

	# 	if returnType is int:
	# 		selectedComponents={}
	# 		for c in components:
	# 			obj = pm.ls(c, objectsOnly=1)[0]
	# 			componentNum = int(c.split('[')[-1].rstrip(']'))

	# 			if obj in selectedComponents:
	# 				selectedComponents[obj].add(componentNum)
	# 			else:
	# 				selectedComponents[obj] = {componentNum}

	# 	if returnType is object:
	# 		attrs = {'vertices':'vtx', 'edges':'e', 'faces':'f'}
	# 		selectedComponents = [getattr(pm.ls(c, objectsOnly=1)[0], attrs[componentType])[n] for n, c in enumerate(components)] if components else []


	# 	return selectedComponents


# @staticmethod
# 	def getUvShellSets(objects=None):
# 		'''
# 		Get All UV shells and their corresponding sets of faces.

# 		:Parameters:
# 			objects (obj)(list) = Polygon object(s).

# 		:Return:
# 			(dict) ex. {0L:[[MeshFace(u'pShape.f[0]'), MeshFace(u'pShape.f[1]')], 1L:[[MeshFace(u'pShape.f[2]'), MeshFace(u'pShape.f[3]')]}
# 		'''
# 		if not objects:
# 			objects = pm.ls(selection=1, objectsOnly=1, transforms=1, flatten=1)

# 		if not isinstance(objects, (list, set, tuple)):
# 			objects=[objects]

# 		shells={}
# 		for obj in objects:
# 			faces = Init.getComponents(obj, 'f')
# 			for face in faces:
# 				shell_Id = pm.polyEvaluate(face, uvShellIds=True)

# 				try:
# 					shells[shell_Id[0]].append(face)
# 				except KeyError:
# 					try:
# 						shells[shell_Id[0]]=[face]
# 					except IndexError:
# 						pass

# 		return shells



# @staticmethod
# 	def getSelectedComponents(type_, obj=None):
# 		'''
# 		Get the component selection of the given type.

# 		:Parameters:
# 			obj (obj) = If a polygonal object is given, then only selected components from that object will be returned.

# 		:Return:
# 			(list) component objects.
# 		'''
# 		types = {'vertices':31, 'edges':32, 'faces':34}

# 		if obj:
# 			components = pm.filterExpand(pm.ls(obj, sl=1), selectionMask=types[type_])
# 		else:
# 			components = pm.filterExpand(selectionMask=types[type_])

# 		selectedComponents = [c.split('[')[-1].rstrip(']') for c in components] if components else []

# 		return selectedComponents

# def getClosestVerts(set1, set2, tolerance=100):
# 		'''
# 		Find the two closest vertices between the two sets of vertices.

# 		:Parameters:
# 			set1 (list) = The first set of vertices.
# 			set2 (list) = The second set of vertices.
# 			tolerance (int) = Maximum search distance.

# 		:Return:
# 			(list) closest vertex pair (<vertex from set1>, <vertex from set2>).
# 		'''
# 		closestDistance=tolerance
# 		closestVerts=None
# 		for v1 in set1:
# 			v1Pos = pm.pointPosition(v1, world=1)
# 			for v2 in set2:
# 				v2Pos = pm.pointPosition(v2, world=1)
# 				distance = Init.getDistanceBetweenTwoPoints(v1Pos, v2Pos)

# 				if distance < closestDistance:
# 					closestDistance = distance
# 					if closestDistance < tolerance:
# 						closestVerts = [v1, v2]

# 		return closestVerts


	# @staticmethod
	# def shortestEdgePath():
	# 	'''
	# 	Select shortest edge path between (two or more) selected edges.
	# 	'''
	# 	#:Return: list of lists. each containing an edge paths components
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

	# 	:Parameters:
	# 		obj (str) = The object to snap to.
	# 		vertices (list) = The vertices to snap.
	# 		tolerance (float) = Max distance.
	# 	'''
	# 	Init.loadPlugin('nearestPointOnMesh')
	# 	nearestPointOnMeshNode = mel.eval('{} {}'.format('nearestPointOnMesh', obj))
	# 	pm.delete(nearestPointOnMeshNode)

	# 	pm.undoInfo(openChunk=True)
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
				
	# 			distance = Init.getDistanceBetweenTwoPoints(vertexPosition, associatedVtxPosition)

	# 			if distance<closestDistance:
	# 				closestDistance = distance
	# 				closestPosition = associatedVtxPosition
				
	# 			if closestDistance<tolerance:
	# 				pm.move(closestPosition[0], closestPosition[1], closestPosition[2], vertex, worldSpace=True)

	# 	# pm.delete(nearestPointOnMeshNode)
	# 	pm.undoInfo(closeChunk=True)








# def getContigiousIslands(faces, faceIslands=[]):
# 	'''
# 	Get a list containing sets of adjacent polygon faces grouped by islands.
# 	:Parameters:
# 		faces (list) = polygon faces to be filtered for adjacent.
# 		faceIslands (list) = optional. list of sets. ability to add faces from previous calls to the return value.
# 	:Return:
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

# 		adjFaces = [f for f in Init.getBorderComponents(face) if not f in prevFaces and f in faces]
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