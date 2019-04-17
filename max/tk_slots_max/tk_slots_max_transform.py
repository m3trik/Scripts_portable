import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path

from tk_slots_max_init import Init





class Transform(Init):
	def __init__(self, *args, **kwargs):
		super(Transform, self).__init__(*args, **kwargs)

		
		self.ui = self.sb.getUi('transform')

		#set input masks for text fields
		# self.ui.t000.setInputMask("00.00") #change to allow for neg values

		#chk012, chk013 component constraints. query and set initial value
		# state = pm.xformConstraint(query=True, type=True)
		# if state == 'edge':
		# 	self.ui.chk012.setChecked(True)
		# else:
		# 	self.ui.chk012.setChecked(False)
		# #b021 object or world space
		# if state == 'surface':
		# 	self.ui.chk013.setChecked(True)
		# else:
		# 	self.ui.chk013.setChecked(False)

	def chk005(self):
		'''
		Transform: Scale

		'''
		self.setButtons(self.ui, unchecked='chk008,chk009',checked='chk000,chk001,chk002')
		self.ui.s000.setValue(2)
		self.ui.s000.setSingleStep(1)

	def chk008(self):
		'''
		Transform: Move

		'''
		self.setButtons(self.ui, unchecked='chk005,chk009,chk000,chk001,chk002')
		self.ui.s000.setValue(0.1)
		self.ui.s000.setSingleStep(0.1)

	def chk009(self):
		'''
		Transform: Rotate

		'''
		self.setButtons(self.ui, unchecked='chk005,chk008,chk000,chk001,chk002')
		self.ui.s000.setValue(45)
		self.ui.s000.setSingleStep(5)

	def chk010(self):
		'''
		Align: Auto Align

		'''
		if self.ui.chk010.isChecked():
			self.setButtons(self.ui, disable='b029,b030,b031')
		else:
			self.setButtons(self.ui, enable='b029,b030,b031')

	def chk012(self):
		'''
		Constrain To Edge

		'''
		if self.ui.chk012.isChecked():
			self.ui.chk013.setChecked(False)
			# pm.manipMoveSetXformConstraint(edge=True);
			pm.xformConstraint(type='edge')
		else:
			# pm.manipMoveSetXformConstraint(none=True);
			pm.xformConstraint(type='none')

	def chk013(self):
		'''
		Constrain To Surface

		'''
		if self.ui.chk013.isChecked():
			self.ui.chk012.setChecked(False)
			# pm.manipMoveSetXformConstraint(surface=True);
			pm.xformConstraint(type='surface')
		else:
			# pm.manipMoveSetXformConstraint(none=True);
			pm.xformConstraint(type='none')

	def s000(self): #
		pass

	def transformChecks(self):
		floatXYZ = float(self.ui.s000.text())
		floatX=floatY=floatZ = 0

		if self.ui.chk005.isChecked():
			currentScale = pm.xform (query=1, scale=1)
			floatX = round(currentScale[0], 2)
			floatY = round(currentScale[1], 2)
			floatZ = round(currentScale[2], 2)

		if self.ui.chk000.isChecked():
			floatX = floatXYZ
		if self.ui.chk001.isChecked():
			floatY = floatXYZ
		if self.ui.chk002.isChecked():
			floatZ = floatXYZ

		xyz = [floatX, floatY, floatZ]
		return xyz

	def transform(self): #transform
		relative = bool(self.ui.chk003.isChecked())#Move absolute/relative toggle
		worldspace = bool(self.ui.chk004.isChecked())#Move object/worldspace toggle
		xyz = self.transformChecks()
		
		#Scale selected.
		if self.ui.chk005.isChecked():
			if xyz[0] != -1: #negative values are only valid in relative mode and cannot scale relatively by one so prevent the math below which would scale incorrectly in this case.
				#convert the decimal place system xform uses for negative scale values to an standard negative value
				if xyz[0] < 0:
					xyz[0] = xyz[0]/10.*2.5
				if xyz[1] < 0:
					xyz[1] = xyz[1]/10.*2.5
				if xyz[2] < 0:
					xyz[2] = xyz[2]/10.*2.5
				pm.xform (relative=relative, worldSpace=worldspace, objectSpace=(not worldspace), scale=(xyz[0], xyz[1], xyz[2]))
	
		#Move selected relative/absolute, object/worldspace by specified amount.
		if self.ui.chk008.isChecked():
			pm.xform (relative=relative, worldSpace=worldspace, objectSpace=(not worldspace), translation=(xyz[0], xyz[1], xyz[2]))

		#Rotate selected
		if self.ui.chk009.isChecked():
			pm.xform (relative=relative, worldSpace=worldspace, objectSpace=(not worldspace), rotation=(xyz[0], xyz[1], xyz[2]))

	def b000(self):
		'''
		Transform -

		'''
		#change the textfield to neg value and call transform
		textfield = float(self.ui.s000.value())
		if textfield >=0:
			newText = -textfield
			self.ui.s000.setValue(newText)
		self.transform()

	def b001(self):
		'''
		Transform +

		'''
		#change the textfield to pos value and call transform
		textfield = float(self.ui.s000.value())
		if textfield <0:
			newText = abs(textfield)
			self.ui.s000.setValue(newText)
		self.transform()

	def b002(self):
		'''
		Freeze Transformations

		'''
		maxEval('macros.run \"Animation Tools\" \"FreezeTransform\"')
		
	def b003(self):
		'''
		Center Pivot Object

		'''
		for obj in rt.selection:
			rt.toolMode.coordsys(obj)
			obj.pivot = obj.center
		
	def b004(self):
		'''
		Align Vertices

		'''

		#a previous version of this has been translated to max
		if self.ui.chk010.isChecked(): #if checked; set coordinates for auto align:
			sel = pm.ls (selection=1)

			if len(sel) != 0:
				point = pm.xform(sel[0], q=True, t=True, ws=True)
				#vertex point 1
				x1 = round(point[0], 4)
				y1 = round(point[1], 4)
				z1 = round(point[2], 4)

				#vertex point 2
				x2 = round(point[3], 4)
				y2 = round(point[4], 4)
				z2 = round(point[5], 4)

				#find the axis with the largest variance to determine direction.
				x = abs(x1-x2)
				y = abs(y1-y2)
				z = abs(z1-z2)

				vertex = pm.polyListComponentConversion (fromEdge=1, toVertexFace=1)[0]
				vertexTangent = pm.polyNormalPerVertex (vertex, query=True, xyz=True)

				tx = abs(round(vertexTangent[0], 4))
				ty = abs(round(vertexTangent[1], 4))
				tz = abs(round(vertexTangent[2], 4))

				axis = max(x,y,z)
				tangent = max(tx,ty,tz)

				if self.ui.chk011.isChecked():
					if axis == x: #"yz"
						self.setButtons(self.ui, checked='b030,b031', unchecked='b029')
					if axis == y: #"xz"
						self.setButtons(self.ui, checked='b029,b031', unchecked='b030')
					if axis == z: #"xy"
						self.setButtons(self.ui, checked='b029,b030', unchecked='b031')
				else:
					if any ([axis == x and tangent == ty, axis == y and tangent == tx]): #"z"
						self.setButtons(self.ui, checked='b031', unchecked='b029,b030')
					if any ([axis == x and tangent == tz, axis == z and tangent == tx]): #"y"
						self.setButtons(self.ui, checked='b030', unchecked='b029,b031')
					if any ([axis == y and tangent == tz, axis == z and tangent == ty]): #"x"
						self.setButtons(self.ui, checked='b029', unchecked='b030,b031')
			else:
				print "// Warning: An edge must be selected. //"
				return

		#align
		x = self.ui.b029.isChecked()
		y = self.ui.b030.isChecked()
		z = self.ui.b031.isChecked()
		avg = self.ui.chk006.isChecked()
		loop = self.ui.chk007.isChecked()

		if all ([x, not y, not z]): #align x
			self.alignVertices(mode=3,average=avg,edgeloop=loop)

		if all ([not x, y, not z]): #align y
			self.alignVertices(mode=4,average=avg,edgeloop=loop)

		if all ([not x, not y, z]): #align z
			self.alignVertices(mode=5,average=avg,edgeloop=loop)

		if all ([not x, y, z]): #align yz
			self.alignVertices(mode=0,average=avg,edgeloop=loop)

		if all ([x, not y, z]): #align xz
			self.alignVertices(mode=1,average=avg,edgeloop=loop)

		if all ([x, y, not z]): #align xy
			self.alignVertices(mode=2,average=avg,edgeloop=loop)

		if all ([x, y, z]): #align xyz
			self.alignVertices(mode=6,average=avg,edgeloop=loop)

	def b005(self):
		'''
		Move To

		'''
		sel = [s for s in rt.getCurrentSelection()] #rebuild selection array in python.

		objects = sel[:-1]
		target = sel[-1]
		#move object(s) to center of the last selected items bounding box
		for obj in objects: 
			obj.center = target.center

	def b006(self):
		'''
		

		'''
		pass

	def b007(self):
		'''
		

		'''
		pass

	def b008(self):
		'''
		

		'''
		pass

	def b009(self):
		'''
		

		'''
		pass

	def b010(self):
		'''
		

		'''
		pass

	def b011(self):
		'''
		

		'''
		pass

	def b012(self):
		'''
		Make Live

		'''
		objects = pm.ls (sl=1)[0] #construction planes, nurbs surfaces and polygon meshes can be made live. makeLive supports one live object at a time.
		pm.makeLive(obj)
		print str(obj)+'is live.' 

	def b013(self):
		'''
		Drop To Grid

		'''
		origin = self.ui.chk014.isChecked()
		bBoxLowestPoint = self.ui.chk015.isChecked()
		centerPivot = self.ui.chk016.isChecked()

		selection = pm.ls (selection=1, objectsOnly=1)

		for obj in selection:
			osPivot = pm.xform (obj, query=1, rotatePivot=1, objectSpace=1) #save the object space obj pivot
			wsPivot = pm.xform (obj, query=1, rotatePivot=1, worldSpace=1) #save the world space obj pivot
			if origin:
				pm.undoInfo (openChunk=1)
				#position the pivot
				pm.xform (obj, centerPivots=1) #center pivot
				plane = pm.polyPlane (name='alignTo_temp')
				if not bBoxLowestPoint:
					y = 'Mid' #possible values are: 'Max','Mid','Min'
				else:
					y = 'Min'
				pm.align (obj, plane, atl=1, x='Mid', y=y, z='Mid')
				if not centerPivot:
					pm.xform (obj, rotatePivot=osPivot, objectSpace=1) #return pivot to orig position
				pm.delete (plane)
				pm.select(obj)
				pm.undoInfo (closeChunk=1)
			else:
				pm.makeIdentity (obj, apply=1, t=1, r=1, s=1, n=0, pn=1) #freeze transforms to ensure the bounding box is not rotated
				bBox = pm.exactWorldBoundingBox(obj) #get bounding box world space coords
				if not bBoxLowestPoint:
					y = float(bBox[4])-float(bBox[1]) #get mid point (ymax-ymin)
				else:
					y = float(bBox[1]) #get lowest point (ymin)
				pm.undo() #undo freezetransforms
				pm.xform (obj, rotatePivot=(wsPivot[0], y, wsPivot[2]), worldSpace=1) #reset the pivot to the lowest point in world space
				destinationPoint = pm.xform (obj, query=1, pivots=1, worldSpace=1) #query the new pivot location
				if not bBoxLowestPoint:
					y = destinationPoint[1] #mid point
				else:
					y = destinationPoint[4] #lowest point
				pm.xform (obj, translation=(0, -y, 0), relative=1) #move the object to the pivot location
				if centerPivot:
					pm.xform (obj, centerPivots=1) #center the pivot
				else:
					pm.xform (obj, rotatePivot=osPivot, objectSpace=1) #return pivot to orig position
				pm.select(selection) #retore the original selection

	def b014(self):
		'''
		Center Pivot Component

		'''
		[pm.xform (s, centerPivot=1) for s in pm.ls (sl=1, objectsOnly=1, flatten=1)]
		# mel.eval("moveObjectPivotToComponentCentre;")

	def b015(self):
		'''
		Center Pivot World

		'''
		mel.eval("xform -worldSpace -pivots 0 0 0;")

	def b016(self):
		'''
		Set To Bounding Box

		'''
		mel.eval("bt_alignPivotToBoundingBoxWin;")

	def b017(self):
		'''
		Bake Pivot

		'''
		mel.eval("BakeCustomPivot;")

	def b018(self):
		'''
		Snap Align Objects: Align Objects

		'''
		mel.eval("performAlignObjects 1;")

	def b019(self):
		'''
		Align 1 Points

		'''
		mel.eval("SnapPointToPointOptions;")

	def b020(self):
		'''
		Align 2 Points

		'''
		mel.eval("Snap2PointsTo2PointsOptions;")

	def b021(self):
		'''
		Align 3 Points

		'''
		mel.eval("Snap3PointsTo3PointsOptions;")

	def b022(self):
		'''
		Align Tool

		'''
		mel.eval("setToolTo alignToolCtx;")

	def b023(self):
		'''
		Orient To Vertex/Edge

		'''
		mel.eval("orientToTool;")

	def b024(self):
		'''
		Snap To Component

		'''
		mel.eval("bt_snapAlignObjectToComponent;")

	def b025(self):
		'''
		Snap Together

		'''
		mel.eval("setToolTo snapTogetherToolCtx;")

	def b026(self):
		'''
		Maya Bonus Tools: Snap Align Objects To Component Options

		'''
		mel.eval("bt_snapAlignObjectToComponentOptions;")

	def b027(self):
		'''
		

		'''
		mel.eval("")

	def b028(self):
		'''
		

		'''
		mel.eval("")

	def b029(self):
		'''
		

		'''
		mel.eval("")

	def b030(self):
		'''
		

		'''
		mel.eval("")

	def b031(self):
		'''
		

		'''
		mel.eval("")

	def b032(self):
		'''
		Reset Pivot Transforms

		'''
		maxEval('''
		{ string $objs[] = `ls -sl -type transform -type geometryShape`;
		if (size($objs) > 0) { xform -cp; } manipPivot -rp -ro; };
		''')





	





#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------

# maxEval('max tti')

# maxEval('macros.run \"PolyTools\" \"TransformTools\"')

