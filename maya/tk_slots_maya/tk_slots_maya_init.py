import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_ import Slot





class Init(Slot):
	def __init__(self, *args, **kwargs):
		super(Init, self).__init__(*args, **kwargs)



		# live surface #state and obj might need to be saved in external file
		# 'main' shorcut mode: ie. polygons, uv's, etc
		# pm.helpLine(width=20, height=8)
		# progress bar


	def info(self): #get current attributes. those with relavant values will be displayed.

		infoDict={}
		selection = pm.ls(selection=1)
		

		selectionCount = len(selection); infoDict.update({"Selection Count: ":selectionCount}) #number of selected objects
		currentSelection = [str(s) for s in pm.ls (selection=1)]; infoDict.update({"Current Selection: ":currentSelection}) #currently selected objects
		


		symmetry = pm.symmetricModelling(query=1, symmetry=1);
		if symmetry==1: symmetry=True; infoDict.update({"Symmetry State: ":symmetry}) #symmetry state
		if symmetry: axis = pm.symmetricModelling(query=1, axis=1); infoDict.update({"Symmetry Axis: ":axis}) #symmetry axis

		xformConstraint = pm.xformConstraint(query=True, type=True)
		if xformConstraint=='none': xformConstraint=None; infoDict.update({"Xform Constrait: ":xformConstraint}) #transform constraits


		if pm.selectType(query=1, vertex=1):
			selectedVerts = [v.split('[')[-1].rstrip(']') for v in pm.filterExpand(selectionMask=31)] #pm.polyEvaluate(vertexComponent=1);
			collapsedList = self.collapseList(selectedVerts)
			numVerts = pm.polyEvaluate (selection[0], vertex=1)
			infoDict.update({'Selected '+str(len(selectedVerts))+'/'+str(numVerts)+" Vertices: ":collapsedList}) #selected verts
			
		if pm.selectType(query=1, edge=1):
			selectedEdges = [e.split('[')[-1].rstrip(']') for e in pm.filterExpand(selectionMask=32)] #pm.polyEvaluate(edgeComponent=1);
			collapsedList = self.collapseList(selectedEdges)
			numEdges = pm.polyEvaluate (selection[0], Edge=1)
			infoDict.update({'Selected '+str(len(selectedEdges))+'/'+str(numEdges)+" Edges: ":collapsedList}) #selected edges
			
		if pm.selectType(query=1, facet=1):
			selectedFaces = [f.split('[')[-1].rstrip(']') for f in pm.filterExpand(selectionMask=34)] #pm.polyEvaluate(faceComponent=1);
			collapsedList = self.collapseList(selectedFaces)
			numFaces = pm.polyEvaluate (selection[0], face=1)
			infoDict.update({'Selected '+str(len(selectedFaces))+'/'+str(numFaces)+" Faces: ":collapsedList}) #selected faces

		
		# selectedUVs = pm.polyEvaluate(uvComponent=1); 
		# if type(selectedUvs)==int: infoDict.update({"Selected UV's: ":selectedUVs}) #selected uv's

		prevCommand = self.sb.prevCommand(docString=True); infoDict.update({"Previous Command: ":prevCommand})  #get button text from last used command

		#populate the textedit with any values
		t = self.ui.t000
		t.clear()
		for key, value in infoDict.iteritems():
			if value:
				t.append(key+str(value))




	# ------------------------------------------------
	' Geometry'
	# ------------------------------------------------




	#returns all faces on a specified axis
	@staticmethod
	def getAllFacesOnAxis(axis="-x", localspace=False):
		#args: axis='string' - representing axis ie. "x"
		#			localspace=bool - specify world or local space
		#ex. self.getAllFacesOnAxis ('y')
		sel = pm.ls(selection=1)

		if len(sel) >0:
			faceCount = pm.polyEvaluate(sel[0], face=1)
			faces = []
		else:
			traceback.print_exc()
			return

		index = 0
		if any ([axis=="y",axis=="-y"]):
			index = 1
		if any ([axis=="z",axis=="-z"]):
			index = 2

		for i in xrange(faceCount):
			attr = sel[0] + '.f[%d]' % i

			if any ([axis=="-x", axis=="-y", axis=="-z"]):
				# if pm.xform(attr, query=1, worldSpace=1, translation=1)[index] < 0:
				if pm.exactWorldBoundingBox (attr)[index] < -0.00001:
					faces.append(attr)
			else:
				# if pm.xform(attr, query=1, worldSpace=1, translation=1)[index] > 0:
				if pm.exactWorldBoundingBox (attr)[index] > -0.00001:
					faces.append(attr)

		return faces


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
		#args: mode=int - possible values are align: 0-YZ, 1-XZ, 2-XY, 3-X, 4-Y, 5-Z, 6-XYZ 
		#			average=bool - align to average of all selected vertices. else, align to last selected
		#			edgeloop=bool - align vertices in edgeloop from a selected edge
		#ex. self.alignVertices(mode=3,average=True,edgeloop=True)
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
	def createCircle(axis='y', numPoints=5, radius=5, center=[0,0,0], mode=0):
		#args: axis='string' - 'x','y','z' 
		#			numPoints=int - number of outer points
		#			radius=int
		#			center=[float3 list] - point location of circle center
		#			mode=int - 0 -no subdivisions, 1 -subdivide tris, 2 -subdivide quads
		#ex. self.createCircle(axis='x', numPoints=20, radius=8, mode='tri')
		import math

		degree = 360/float(numPoints)
		radian = math.radians(degree) #or math.pi*degree/180 (pi * degrees / 180)

		vertexPoints = []

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
		circle = pm.polyCreateFacet (point=vertexPoints, name='pCircle')
		pm.polyNormal (circle, normalMode=4) #4=reverse and propagate
		if mode==1:
			pm.polySubdivideFacet (divisions=1, mode=1)
		if mode==2:
			pm.polySubdivideFacet (divisions=1, mode=0)
		pm.undoInfo (closeChunk=True)

		return circle







	# ------------------------------------------------
	' DAG objects'
	# ------------------------------------------------



	@staticmethod
	def setAttributesOnSelected(attribute=None, value=None):
		#args: obj='string' - attribute to modify
		#			value=int - new attribute value
		#ex. self.setAttributesOnSelected (attribute=".smoothLevel", value=1)
		selection = pm.ls (selection=1, objectsOnly=1)
		if selection:
			for obj in selection:
				pm.setAttr (obj+attribute, value)
		else:
			print "// Warning: No polygon object selected.", attribute, value, "not applied."





	# ------------------------------------------------
	' Ui'
	# ------------------------------------------------


	#to use main progressBar: name=string $gMainProgressBar
	@staticmethod
	def mainProgressBar (size, name="tk_progressBar", stepAmount=1):
		#args: size=int - total amount
	  #			name='string' - name of progress bar created
	  #			stepAmount=int - increment amount
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
	def viewPortMessage (message='', statusMessage='', assistMessage='', position='topCenter'):
		#args: statusMessage='string' - message to display (accepts html formatting).
		#			position='string' - position on screen. possible values are: topCenter","topRight","midLeft","midCenter","midCenterTop","midCenterBot","midRight","botLeft","botCenter","botRight"
		#ex. self.viewPortMessage("shutting down:<hl>"+str(timer)+"</hl>")
		message=statusMessage; statusMessage=''
		pm.inViewMessage(message=message, statusMessage=statusMessage, assistMessage=assistMessage, position=position, fontSize=10, fade=1, fadeInTime=0, fadeStayTime=1000, fadeOutTime=500, alpha=75) #1000ms = 1 sec


	#output text
	@staticmethod
	def outputText (text, window_title):
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


	#output scroll layout
	@staticmethod
	def outputscrollField (text, window_title, width, height):
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


	#output text field
	@staticmethod
	def outputTextField (array, window_title):
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
	def convertMelToPy(melScript): #convert mel to python
		#args: melScript='string' - mel script to convert
		#returns: converted script as a string
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