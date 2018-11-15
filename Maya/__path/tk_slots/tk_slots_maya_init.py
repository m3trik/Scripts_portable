from PySide2 import QtGui

import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_ import Slot



class Init(Slot):
	def __init__(self, *args, **kwargs):
		super(Init, self).__init__(*args, **kwargs)

		#init widgets
		self.initWidgets(self)


		# self.ui.t000.clearFocus()
		self.ui.t000.viewport().setAutoFillBackground(False)
		self.ui.t000.setTextBackgroundColor(QtGui.QColor(50, 50, 50))


		# live surface #state and obj might need to be saved in external file
		# 'main' shorcut mode: ie. polygons, uv's, etc
		# pm.helpLine(width=20, height=8)
		# progress bar


	def info(self): #get current attributes. those with relavant values will be displayed.
		info={}
		selection = pm.ls(selection=1)
		objects = pm.ls(selection=1, objectsOnly=1)
		value = len(objects); info.update({"selected objects: ":value}) #number of selected objects
		currentSelection = [str(s) for s in pm.ls (selection=1)]; info.update({"Current Selection: ":currentSelection}) #currently selected objects
		
		if selection: numQuads = pm.polyEvaluate (selection[0], face=1); info.update({"Num Quads: ":numQuads}) #number of faces

		symmetry = pm.symmetricModelling(query=1, symmetry=1);
		if symmetry==1: symmetry=True; info.update({"symmetry: ":symmetry}) #symmetry state
		if symmetry: axis = pm.symmetricModelling(query=1, axis=1); info.update({"symmetry axis: ":axis}) #symmetry axis

		xformConstraint = pm.xformConstraint(query=True, type=True)
		if xformConstraint=='none': xformConstraint=None; info.update({"xform constrait: ":xformConstraint}) #transform constraits

		value = pm.polyEvaluate(vertexComponent=1); info.update({"selected vertices: ":value}) #selected verts
		value = pm.polyEvaluate(edgeComponent=1); info.update({"selected edges: ":value}) #selected edges
		value = pm.polyEvaluate(faceComponent=1); info.update({"selected faces: ":value}) #selected faces
		value = pm.polyEvaluate(uvComponent=1); info.update({"selected uv's: ":value}) #selected uv's

		#populate the textedit with any values
		for key, value in info.iteritems():
			if value:
				# self.ui.t000.setText(key+str(value)+'<br>') #<br> html break newline
				self.ui.t000.setHtml(key+str(value)+'<br>') #<br> html break newline




	# ------------------------------------------------
	' Geometry'
	# ------------------------------------------------




	#returns all faces on a specified axis
	def getAllFacesOnAxis(self, axis="-x", localspace=False):
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
	def shortestEdgePath(self):
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
	def alignVertices (self, mode, average=False, edgeloop=False):
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




	def createCircle(self, axis='y', numPoints=5, radius=5, center=[0,0,0], mode=None):
		#args: axis='string' - 'x','y','z' 
		#			numPoints=int - number of outer points
		#			radius=int
		#			center=[float3 list] - point location of circle center
		#			mode='string' - 'None' no subdivisions, 'tri' subdivide tris, 'quad' subdivide quads
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
		if mode=="tri":
			pm.polySubdivideFacet (divisions=1, mode=1)
		if mode=="quad":
			pm.polySubdivideFacet (divisions=1, mode=0)
		pm.undoInfo (closeChunk=True)

		return circle







	# ------------------------------------------------
	' DAG objects'
	# ------------------------------------------------




	def setAttributesOnSelected(self, attribute=None, value=None):
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




	#returns a list of objects from a supplied range, or string list.
	def getObject(self, class_, objectNames, range_=None, showError_=True):
		#args: class_=class object
		#			 objectNames='string' - single name when used with range arg. ie. 's'  else; names separated by ','. ie. ['s000,s001,s002'] 
		#			 range_=[int list] - integers representing start, end of range. used with single string type objectName.  ie. [2,10]
		#		 	 showError=bool - show attribute error if item doesnt exist
		#returns: list of corresponding objects
		#ex. self.getObject(self.ui, 's', [0,10])  or  self.getObject(self.ui, ['s000,s002,s011'])
		if range_: #if range is given; generate list within given range_
			start, stop = range_[0], range_[1] #add a numberical suffix to the object name within the given range.
			names = [str(objectNames)+'000'[:-len(str(num))]+str(num) for num in range(start,stop)] #build list of name strings within given range
		else: #use the list of names passed in as objectName
			names = objectNames.split(',')
		objects=[]
		for name in names:
			# if hasattr(class_, name):
			try:
				objects.append(getattr(class_, name)) #equivilent to:(self.ui.m000)
			# elif showError_:
			except: 
				if showError_:
					print "# Error:"+str(class_)+" has no attribute "+str(name)+" #"
				else: pass
		return objects


	#init signals, button states etc. for a stacked widget class
	def initWidgets(self, class_):
		#arg: class_=class instance

		if class_.__class__.__name__ != 'Create':
			#ex. self.initWidgets(self)
			for comboBox in getObject(class_, 'cmb', [0,50], False):
				# combobox.currentIndexChanged.connect(self.combobox.objectName())
				comboBox()

		# print 'initWidgets', class_.__class__.__name__
		if class_.__class__.__name__ == 'Create':
			setButtons(class_.ui, invisible='s000,s010,s011,t000')
			#temp fix for function below calling setAttributes with only last arg
			class_.ui.s000.valueChanged.connect (lambda: class_.setAttributes(0))
			class_.ui.s001.valueChanged.connect (lambda: class_.setAttributes(1))
			class_.ui.s002.valueChanged.connect (lambda: class_.setAttributes(2))
			class_.ui.s003.valueChanged.connect (lambda: class_.setAttributes(3))
			class_.ui.s004.valueChanged.connect (lambda: class_.setAttributes(4))
			class_.ui.s005.valueChanged.connect (lambda: class_.setAttributes(5))
			class_.ui.s006.valueChanged.connect (lambda: class_.setAttributes(6))
			class_.ui.s007.valueChanged.connect (lambda: class_.setAttributes(7))
			class_.ui.s008.valueChanged.connect (lambda: class_.setAttributes(8))
			class_.ui.s009.valueChanged.connect (lambda: class_.setAttributes(9))
			class_.ui.s010.valueChanged.connect (lambda: class_.setAttributes(10))
			class_.ui.s011.valueChanged.connect (lambda: class_.setAttributes(11))
			spinboxes = getObject(class_.ui, 's', [0,12], False)
			for index, spinbox in enumerate(spinboxes):
				# spinbox.valueChanged.connect (lambda i=index: class_.setAttributes(i)) #use lambda to call method with argument: index of spinbox
				spinbox.setVisible(False)


	def comboBox(self, comboBox, items, title=None):
		#args: comboBox=QComboBox object - list of items to fill the comboBox with
		#			title='string' - optional value for the first index of the comboboxs list
		#returns: combobox's current item list
		#ex. self.comboBox (self.ui.cmb003, ["Import file", "Import Options"], "Import")
		comboBox.blockSignals(True) #to keep clear from triggering currentIndexChanged
		comboBox.clear()
		items = items+['refresh'] #refresh string is a temp work around. until we override to call comboBox on open insead of index change.
		if title:
			comboBox.addItem(title)
		comboBox.addItems(items)
		comboBox.blockSignals(False)
		if title:
			return [title]+items
		else:
			return items


	class CheckableComboBox(QtWidgets.QComboBox):
		# once there is a checkState set, it is rendered
		# here we assume default Unchecked
		def addItem(self, item):
			super(CheckableComboBox, self).addItem(item)
			item = self.model().item(self.count()-1,0)
			item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
			item.setCheckState(QtCore.Qt.Unchecked)

		def checkIndex(self, index):
			item = self.model().item(index,0)
			return item.checkState() == QtCore.Qt.Checked


	#to use main progressBar: name=string $gMainProgressBar
	def mainProgressBar (self, size, name="tk_progressBar", stepAmount=1):
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


	#ex. set various states for multiple buttons at once  
	def setButtons (self, ui, checked=None, unchecked=None, enable=None, disable=None, visible=None, invisible=None):
		#args: setButtons=dynamic ui object
		#			checked/unchecked/enable/disable/visible/invisible=string - the names of buttons to modify separated by ','. ie. 'b000,b001,b022'
		#ex. self.setButtons(self.ui, disable=['b000'], unchecked=['b009,b010,b012'])
		if checked:
			checked = getObject(ui,checked)
			[button.setChecked(True) for button in checked]
			
		if unchecked:
			unchecked = getObject(ui,unchecked)
			[button.setChecked(False) for button in unchecked]
				
		if enable:
			enable = getObject(ui,enable)
			[button.setEnabled(True) for button in enable]
				
		if disable:
			disable = getObject(ui,disable)
			[button.setDisabled(True) for button in disable]
				
		if visible:
			visible = getObject(ui,visible)
			[button.setVisible(True) for button in visible]
				
		if invisible:
			invisible = getObject(ui,invisible)
			[button.setVisible(False) for button in invisible]
				


	def setSpinboxes(self, ui, values, range_=[0,9], spinboxNames=None):
		#args: spinboxNames=[string list] - spinbox string object names (used in place of the range argument). ie. ['s000,s001,s002']
		#			 range_=[int list] - [int start, int end] of spinbox range. ie. spinboxes 2-10.  ie. [2,10]
		#			 values=int or [tuple list] - tuple representing a string prefix and value, and/or just a value. [(string prefix,int value)] ie. [("size",5), 20, ("width",8)]
		#returns: list of values without prefix
		#ex. self.setSpinboxes (self.ui, values=[("width",1),("length ratio",1),("patches U",1),("patches V",1)])
		if spinboxNames: #get spinbox objects
			spinboxes = getObject(ui, spinboxNames)
		else:
			spinboxes = getObject(ui, 's', range_)

		#clear previous values
		for spinbox in spinboxes:
			spinbox.blockSignals(True) #block signals to keep from calling method on valueChanged
			spinbox.setPrefix('')
			spinbox.setValue(0)
			spinbox.setDisabled(True)
			spinbox.setVisible(False)

		values_=[] #list of values to return.
		#set new values
		for i, value in enumerate(values):
			spinboxes[i].setVisible(True)
			spinboxes[i].setEnabled(True)
			if type(value) == tuple:
				spinboxes[i].setPrefix(value[0]+':  ')
				spinboxes[i].setValue(value[1])
				values_.append(value[1])
			else:
				spinboxes[i].setValue(value)
				values_.append(value)
			spinboxes[i].blockSignals(False)

		return values_


	cycleDict={}
	#used for maintaining toggling sequences for multiple objects simultaniously
	def cycle(self, id_sequence, query=False): #toggle between numbers in a given sequence
		#args: id_sequence=string or int list - id_numberical sequence ie. 'name_123' or [1,2,3].
		#			takes the string argument and splits it at '_'
		#			converting the second numberical half to integers and putting them in a list.
		#			each time this function is called, it returns the next number in that list
		#			using the original string as a unique id.
		#ex. self.cycle('componentID_01234')
		try:
			if query:
				return int(cycleDict[id_sequence][-1]) #get the current value ie. 0
			value = cycleDict[id_sequence] #check if key exists. if so return the value. ie. value = [1,2,3]
		except KeyError: #else create sequence list for the given key
			id_ = id_sequence.split('_')[0] #ie. name
			sequence = id_sequence.split('_')[1] #ie. 123
			cycleDict[id_sequence] = [i for i in list(sequence)] #ie. {name_123:[1,2,3]}
		value = cycleDict[id_sequence][0] #get the next value ie. 1
		cycleDict[id_sequence] = cycleDict[id_sequence][1:]+[value] #move the value to the end of the list ie. {name_123:[2,3,1]}
		return int(value) #return an integer from string value


	def try_ (self, expressions, exceptions='pass', showError_=True):
		#args: expressions='string' - expression separated by ';'
		#			exceptions='string' - separated by ';'
		#			showError_=bool - hide or show any errors
		#returns: True if no errors occured, else: False
		#ex. self.try_('pm.ls(selection=1, objectsOnly=1)[0]', 'print "# Warning: Nothing selected #"')
		pass_=True
		for expression in expressions.split(';'): #split string arg at ';'
			try:
				print expression
			except Exception as err:
				pass_=False #if any errors occur return False
				if showError_:
					print "# Error: "+str(err)+" #"
				exec (exceptions)
			return pass_


	def viewPortMessage (self, message='', statusMessage='', assistMessage='', position='topCenter'):
		#args: statusMessage='string' - message to display (accepts html formatting).
		#			position='string' - position on screen. possible values are: topCenter","topRight","midLeft","midCenter","midCenterTop","midCenterBot","midRight","botLeft","botCenter","botRight"
		#ex. self.viewPortMessage("shutting down:<hl>"+str(timer)+"</hl>")
		message=statusMessage; statusMessage=''
		pm.inViewMessage(message=message, statusMessage=statusMessage, assistMessage=assistMessage, position=position, fontSize=10, fade=1, fadeInTime=0, fadeStayTime=1000, fadeOutTime=500, alpha=75) #1000ms = 1 sec


	#output text
	def outputText (self, text, window_title):
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
	def outputscrollField (self, text, window_title, width, height):
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
	def outputTextField (self, array, window_title):
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



	def convertMelToPy(self, melScript): #convert mel to python
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


	def commandHelp(self, command): #mel command help
		#args: command='string' - mel command
		command = ('help ' + command)
		modtext = (mel.eval(command))
		outputscrollField (modtext, "command help", 1.0, 1.0) #text, window_title, width, height


	def keywordSearch (self, keyword): #keyword command search
		#args: keyword='string' - 
		keyword = ('help -list' + '"*' + keyword + '*"')
		array = sorted(mel.eval(keyword))
		outputTextField(array, "keyword search")


	def queryRuntime (self, command): #query runtime command info
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


	def searchMEL (self, keyword): #search autodest MEL documentation
		url = '{}{}{}'.format("http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/Commands/",keyword,".html")
		pm.showHelp (url, absolute=True)


	def searchPython (self, keyword): #Search autodesk Python documentation
		url = '{}{}{}'.format("http://help.autodesk.com/cloudhelp/2017/ENU/Maya-Tech-Docs/CommandsPython/",keyword,".html")
		pm.showHelp (url, absolute=True)


	def searchPymel (self, keyword): #search online pymel documentation
		url = '{}{}{}'.format("http://download.autodesk.com/global/docs/maya2014/zh_cn/PyMel/search.html?q=",keyword,"&check_keywords=yes&area=default")
		pm.showHelp (url, absolute=True)


	def currentCtx (self): #get current tool context
		output_text = mel.eval('currentCtx;')
		outputscrollField(output_text, "currentCtx", 1.0, 1.0)


	def sourceScript (self): #Source External Script file
		mel_checkBox = checkBox('mel_checkBox', query=1, value=1)
		python_checkBox = checkBox('python_checkBox', query=1, value=1)

		if mel_checkBox == 1:
			path = os.path.expandvars("%\CLOUD%/____graphics/Maya/scripts/*.mel")
			
		else:
			path = os.path.expandvars("%\CLOUD%/____graphics/Maya/scripts/*.py")

		file = pm.system.fileDialog (directoryMask=path)
		pm.openFile(file)


	def commandRef (self): #open maya MEL commands list 
		pm.showHelp ('http://download.autodesk.com/us/maya/2011help/Commands/index.html', absolute=True)


	def globalVars (self): #$g List all global mel variables in current scene
		mel.eval('scriptEditorInfo -clearHistory')
		array = sorted(mel.eval("env"))
		outputTextField(array, "Global Variables")


	def listUiObjects (self): #lsUI returns the names of UI objects
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





#print module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------