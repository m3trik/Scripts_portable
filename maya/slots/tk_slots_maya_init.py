import maya.mel as mel
import pymel.core as pm
import maya.OpenMayaUI as omUI

from PySide2 import QtGui, QtWidgets
import shiboken2

import os.path

from tk_slots_ import Slot





class Init(Slot):
	def __init__(self, *args, **kwargs):
		super(Init, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('init')






	def info(self):
		'''
		get current attributes. those with relevant values will be displayed.
		'''
		infoDict={}
		selection = pm.ls(selection=1)


		symmetry = pm.symmetricModelling(query=1, symmetry=1);
		if symmetry: axis = pm.symmetricModelling(query=1, axis=1); infoDict.update({'Symmetry Axis: ':axis.upper()}) #symmetry axis

		xformConstraint = pm.xformConstraint(query=True, type=True)
		if xformConstraint=='none': xformConstraint=None; infoDict.update({'Xform Constrait: ':xformConstraint}) #transform constraits

		if selection:
			if pm.selectMode(query=1, object=1): #object mode:
				if pm.selectType(query=1, allObjects=1): #get object/s
					selectedObjects={}; [selectedObjects.setdefault(str(pm.objectType(s)),[]).append(str(s)) for s in pm.ls(selection=1, objectsOnly=1)] #for any selected objects, set object type as key and append object names as value. if key doesn't exist, use setdefault to initialize an empty list and append. ie. {'joint': ['joint_root_0', 'joint_lower_L8', 'joint_lower_L3']}
					infoDict.update({'Objects: ':selectedObjects}) #currently selected objects

			elif pm.selectMode(query=1, component=1): #component mode:
				if pm.selectType(query=1, vertex=1): #get vertex selection info
					selectedVerts = [v.split('[')[-1].rstrip(']') for v in pm.filterExpand(selectionMask=31)] #pm.polyEvaluate(vertexComponent=1);
					collapsedList = self.collapseList(selectedVerts)
					numVerts = pm.polyEvaluate (selection[0], vertex=1)
					infoDict.update({'Vertices: '+str(len(selectedVerts))+'/'+str(numVerts):collapsedList}) #selected verts
					
				elif pm.selectType(query=1, edge=1): #get edge selection info
					selectedEdges = [e.split('[')[-1].rstrip(']') for e in pm.filterExpand(selectionMask=32)] #pm.polyEvaluate(edgeComponent=1);
					collapsedList = self.collapseList(selectedEdges)
					numEdges = pm.polyEvaluate (selection[0], edge=1)
					infoDict.update({'Edges: '+str(len(selectedEdges))+'/'+str(numEdges):collapsedList}) #selected edges
					
				elif pm.selectType(query=1, facet=1): #get face selection info
					selectedFaces = [f.split('[')[-1].rstrip(']') for f in pm.filterExpand(selectionMask=34)] #pm.polyEvaluate(faceComponent=1);
					collapsedList = self.collapseList(selectedFaces)
					numFaces = pm.polyEvaluate (selection[0], face=1)
					infoDict.update({'Faces: '+str(len(selectedFaces))+'/'+str(numFaces):collapsedList}) #selected faces


			# selectedUVs = pm.polyEvaluate(uvComponent=1); 
			# if type(selectedUvs)==int: infoDict.update({"Selected UV's: ":selectedUVs}) #selected uv's

		prevCommand = self.sb.prevCommand(docString=True); infoDict.update({"Previous Command: ":prevCommand})  #get button text from last used command

		#populate the textedit with any values
		t = self.ui.t000
		t.clear()
		for key, value in infoDict.iteritems():
			if value:
				highlight = QtGui.QColor(255, 255, 0)
				baseColor = QtGui.QColor(185, 185, 185)

				t.setTextColor(baseColor)
				t.append(key) #t.append(key+str(value))
				t.setTextColor(highlight)
				t.insertPlainText(str(value))


		#construct buttons for any previous commands.
		ui = self.sb.getUi('main')
		for num, w in enumerate(self.getObject(ui, 'v024-29'), 1): #num starting from 1
			try:
				w.setText(self.sb.prevCommand(docString=1, as_list=1)[-num]) #prevCommand docString
				self.resizeAndCenterWidget(w)
				w.show()
			except: pass


	




	# ------------------------------------------------
	' Geometry'
	# ------------------------------------------------




	#returns all faces on a specified axis
	@staticmethod
	def getAllFacesOnAxis(obj, axis="-x", localspace=False):
		'''
		args:
			obj=<geometry> - object to perform the operation on. 
			axis='string' - representing axis ie. "x"
			localspace=bool - specify world or local space
		ex. self.getAllFacesOnAxis(polyObject, 'y')
		'''
		i=0 #'x'
		if any ([axis=="y",axis=="-y"]):
			i=1
		if any ([axis=="z",axis=="-z"]):
			i=2

		if axis.startswith('-'): #any([axis=="-x", axis=="-y", axis=="-z"]):
			return [face for face in pm.filterExpand(obj+'.f[*]', sm=34) if pm.exactWorldBoundingBox(face)[i] < -0.00001]
		else:
			return [face for face in pm.filterExpand(obj+'.f[*]', sm=34) if pm.exactWorldBoundingBox(face)[i] > -0.00001]



	@staticmethod
	def getBorderEdgeFromFace(faces=None):
		'''
		get border edges from faces.
		args:
			faces='string'/unicode or list of faces. ie. 'poly.f[696]' or 'polyShape.f[696]'
		returns:
			list of border edges.
		ex. getBorderEdgeFromFace(['poly.f[696]', 'poly.f[705:708]'])
		'''
		if not faces: #if no faces passed in as arg, get current face selection
			faces = [str(f) for f in pm.filterExpand(selectionMask=34)]

		edges = [str(i).replace('Shape.', '.', -1).split('|')[-1] for i in pm.ls(pm.polyListComponentConversion(faces, ff=1, te=1), flatten=1)] #get edges from the faces

		borderEdges=[]
		for edge in edges:
			edgeFaces = [str(i).replace('Shape.', '.', -1).split('|')[-1] for i in pm.ls(pm.polyListComponentConversion(edge, fe=1, tf=1), flatten=1)] #get faces that share the edge.

			if len(edgeFaces)<2: #if the edge has only one shared face, it is a border edge.
				borderEdges.append(edge)
			else:
				for f in edgeFaces:
					if f not in faces: #else if the edge's shared face is not part of the selected faces, it is a border edge.
						borderEdges.append(edge)
						break

		return borderEdges



	#select shortest edge path between (two or more) selected edges
	@staticmethod
	def shortestEdgePath():
		#returns: list of lists. each containing an edge paths components
		selectTypeEdge = pm.filterExpand (selectionMask=32) #returns True if selectionMask=Edges
		if (selectTypeEdge): #if selection is polygon edges, convert to vertices.
			mel.eval("PolySelectConvert 3;")
		selection=pm.ls (selection=1, flatten=1)

		vertList=[]

		for objName in selection:
			objName = str(objName) #ex. "polyShape.vtx[176]"
			index1 = objName.find("[")
			index2 = objName.find("]")
			vertNum = objName[index1+1:index2] #ex. "176"
			# position = pm.pointPosition(objName) 
			object_ = objName[:index1-4] #ex. "polyShape"
			# print object_, index1, index2#, position
			vertList.append(vertNum)

		if (selectTypeEdge):
			pm.selectType (edge=True)

		paths=[]
		for index in xrange(3): #get edge path between vertList[0],[1] [1],[2] [2],[3] to make sure everything is selected between the original four vertices/two edges
			edgePath = pm.polySelect(object_, shortestEdgePath=(int(vertList[index]), int(vertList[index+1])))
			paths.append(edgePath)

		return paths


	#align vertices
	@staticmethod
	def alignVertices (mode, average=False, edgeloop=False):
		'''
		args:
			mode=int - possible values are align: 0-YZ, 1-XZ, 2-XY, 3-X, 4-Y, 5-Z, 6-XYZ 
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
	def getComponentPoint(component, alignToNormal=False):
		'''
		get the center point from the given component.
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

		return [round(sum(x) / float(len(x)),4), round(sum(y) / float(len(y)),4), round(sum(z) / float(len(z)),4)]



	@staticmethod
	def createCircle(axis='y', numPoints=5, radius=5, center=[0,0,0], mode=0):
		'''
		args:
			axis='string' - 'x','y','z' 
			numPoints=int - number of outer points
			radius=int
			center=[float3 list] - point location of circle center
			mode=int - 0 -no subdivisions, 1 -subdivide tris, 2 -subdivide quads
		ex. self.createCircle(axis='x', numPoints=20, radius=8, mode='tri')
		'''
		import math

		degree = 360/float(numPoints)
		radian = math.radians(degree) #or math.pi*degree/180 (pi * degrees / 180)

		vertexPoints=[]
		for _ in range(numPoints):
			# print "deg:", degree,"\n", "cos:",math.cos(radian),"\n", "sin:",math.sin(radian),"\n", "rad:",radian
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
			#print x,y,"\n"
			
		pm.undoInfo (openChunk=True)
		node = pm.polyCreateFacet (point=vertexPoints, name='pCircle')
		pm.polyNormal (node, normalMode=4) #4=reverse and propagate
		if mode==1:
			pm.polySubdivideFacet (divisions=1, mode=1)
		if mode==2:
			pm.polySubdivideFacet (divisions=1, mode=0)
		pm.undoInfo (closeChunk=True)

		return node







	# ------------------------------------------------
	' DAG objects'
	# ------------------------------------------------



	@staticmethod
	def getAttributesMEL(node, exclude=None):
		'''
		get history node attributes:values using the transform node. 
		args:
			node=transform node
			exclude='string or unicode list' - attributes to exclude from the returned dictionay

		returns:
			dictionary {'string attribute': current value}
		'''
		#get shape node from transform:
		shapes = pm.listRelatives(node, children=1, shapes=1) #returns list ie. [nt.Mesh(u'pConeShape1')]
		#incoming connections:
		historyNode = pm.listConnections(shapes, source=1, destination=0) #returns list ie. [nt.PolyCone(u'polyCone1')]
		node = historyNode[0].name() #get the string name from the history node

		return {attr:pm.getAttr(node+'.'+attr) for attr in pm.listAttr(node) if attr not in exclude}



	@staticmethod
	def setAttributesMEL(node, attributes):
		'''
		sets given attributes for the history node using the transform node.
		args:
			node=transform node
			attributes=dictionary {'string attribute': value} - attributes and their correponding value to set
		'''
		#get shape node from transform:
		shapes = pm.listRelatives(node, children=1, shapes=1) #returns list ie. [nt.Mesh(u'pConeShape1')]
		#incoming connections:
		historyNode = pm.listConnections(shapes, source=1, destination=0) #returns list ie. [nt.PolyCone(u'polyCone1')]
		node = historyNode[0].name() #get the string name from the history node

		[pm.setAttr(node+'.'+attr, value) for attr, value in attributes.iteritems() if attr and value]



	@staticmethod
	def setAttributesOnSelected(attribute=None, value=None):
		'''
		args:
			obj='string' - attribute to modify
			value=int - new attribute value
		ex. self.setAttributesOnSelected (attribute=".smoothLevel", value=1)
		'''
		selection = pm.ls (selection=1, objectsOnly=1)
		if selection:
			for obj in selection:
				pm.setAttr (obj+attribute, value)
		else:
			print "// Warning: No polygon object selected.", attribute, value, "not applied."






	# ------------------------------------------------
	' Ui'
	# ------------------------------------------------



	@staticmethod
	def getMayaMainWindow():
		'''
		Get the main Maya window as a QtGui.QMainWindow instance
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
			name='string' - name of a Maya UI element of any type.
			type_=<qt object type> - default is QWidget
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
	def mainProgressBar (size, name="tk_progressBar", stepAmount=1):
		'''
		args:
			size=int - total amount
			name='string' - name of progress bar created
	  		stepAmount=int - increment amount
	  	to use main progressBar: name=string $gMainProgressBar
	  	'''
		status = "processing: "+str(size)+"."
		edit=0
		if pm.progressBar (name, exists=1):
			edit=1
		pm.progressBar (name, edit=edit,
						beginProgress=1,
						isInterruptable=True,
						status=status,
						maxValue=size,
						step=stepAmount)

		#add esc key pressed return False

		# example use-case:
		# mainProgressBar (len(edges), progressCount)
		# 	pm.progressBar ("tk_progressBar", edit=1, step=1)
		# 	if pm.progressBar ("tk_progressBar", query=1, isCancelled=1):
		# 		break
		# pm.progressBar ("tk_progressBar", edit=1, endProgress=1)



	@staticmethod
	def viewPortMessage(message='', statusMessage='', assistMessage='', position='topCenter'):
		'''
		args:
			message='string' - The message to be displayed, (accepts html formatting). General message, inherited by -amg/assistMessage and -smg/statusMessage.
			statusMessage='string' - The status info message to be displayed (accepts html formatting).
			assistMessage='string' - The user assistance message to be displayed, (accepts html formatting).
			position='string' - position on screen. possible values are: topCenter","topRight","midLeft","midCenter","midCenterTop","midCenterBot","midRight","botLeft","botCenter","botRight"
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
		print text_field
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
	# 	print text
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
		output scroll layout
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
		print window
		pm.setParent('..')
		pm.showWindow(window)
		return



	@staticmethod
	def outputTextField (array, window_title):
		'''
		output text field
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
	def convertMelToPy(melScript):
		'''
		convert mel to python
		args:
			melScript='string' - mel script to convert
		returns:
			converted script as a string
		'''
		from pymel.tools import mel2py
		# convert to single line
		translation = [mel2py.mel2pyStr(e+';') for e in melScript.split(';')] #get list of python commands from a mel string
		pythonScript = [s.lstrip('from pymel.all import *') for s in translation] #strip import string from each index
		print " ".join(pythonScript) #get single string from list
		return pythonScript #list of python commands
		#print to outputscrollField
		# outputscrollField (python_script, "mel2py", 1.0, 1.0) #text, window_title, width, height


	@staticmethod
	def commandHelp(command): #mel command help
		#args: command='string' - mel command
		command = ('help ' + command)
		modtext = (mel.eval(command))
		outputscrollField (modtext, "command help", 1.0, 1.0) #text, window_title, width, height


	@staticmethod
	def keywordSearch (keyword): #keyword command search
		#args: keyword='string' - 
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
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------