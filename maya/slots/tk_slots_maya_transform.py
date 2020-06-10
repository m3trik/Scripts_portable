from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Transform(Init):
	def __init__(self, *args, **kwargs):
		super(Transform, self).__init__(*args, **kwargs)

		#set input masks for text fields
		# self.parentUi.t000.setInputMask("00.00") #change to allow for neg values

		try: #chk012, chk013 component constraints. query and set initial value
			state = pm.xformConstraint(query=True, type=True)
		
			if state == 'edge':
				self.parentUi.chk012.setChecked(True)
			else:
				self.parentUi.chk012.setChecked(False)
			#b021 object or world space
			if state == 'surface':
				self.parentUi.chk013.setChecked(True)
			else:
				self.parentUi.chk013.setChecked(False)

		except NameError:
			pass


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.parentUi.pin

		if state=='setMenu':
			pin.add(QComboBox_, setObjectName='cmb000', setToolTip='')

			return


	def cmb000(self, index=None):
		'''
		Editors
		'''
		cmb = self.parentUi.cmb000
		
		files = ['']
		contents = cmb.addItems_(files, '')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


	def chk005(self):
		'''
		Transform: Scale

		'''
		self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk008-9', setChecked='chk000-2')
		self.parentUi.s000.setValue(2)
		self.parentUi.s000.setSingleStep(1)


	def chk008(self):
		'''
		Transform: Move

		'''
		self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk005,chk009,chk000-2')
		self.parentUi.s000.setValue(0.1)
		self.parentUi.s000.setSingleStep(0.1)


	def chk009(self):
		'''
		Transform: Rotate

		'''
		self.toggleWidgets(self.parentUi, self.childUi, setChecked_False='chk005,chk008,chk000-2')
		self.parentUi.s000.setValue(45)
		self.parentUi.s000.setSingleStep(5)


	def chk010(self):
		'''
		Align: Auto Align

		'''
		if self.parentUi.chk010.isChecked():
			self.toggleWidgets(self.parentUi, self.childUi, setDisabled='b029-31')
		else:
			self.toggleWidgets(self.parentUi, self.childUi, setEnabled='b029-31')


	def chk012(self):
		'''
		Constrain To Edge

		'''
		if self.parentUi.chk012.isChecked():
			self.parentUi.chk013.setChecked(False)
			# pm.manipMoveSetXformConstraint(edge=True);
			pm.xformConstraint(type='edge')
		else:
			# pm.manipMoveSetXformConstraint(none=True);
			pm.xformConstraint(type='none')


	def chk013(self):
		'''
		Constrain To Surface

		'''
		if self.parentUi.chk013.isChecked():
			self.parentUi.chk012.setChecked(False)
			# pm.manipMoveSetXformConstraint(surface=True);
			pm.xformConstraint(type='surface')
		else:
			# pm.manipMoveSetXformConstraint(none=True);
			pm.xformConstraint(type='none')


	def transformChecks(self):
		floatXYZ = float(self.parentUi.s000.text())
		floatX=floatY=floatZ = 0

		if self.parentUi.chk005.isChecked():
			currentScale = pm.xform (query=1, scale=1)
			floatX = round(currentScale[0], 2)
			floatY = round(currentScale[1], 2)
			floatZ = round(currentScale[2], 2)

		if self.parentUi.chk000.isChecked():
			floatX = floatXYZ
		if self.parentUi.chk001.isChecked():
			floatY = floatXYZ
		if self.parentUi.chk002.isChecked():
			floatZ = floatXYZ

		xyz = [floatX, floatY, floatZ]
		return xyz


	def transform(self): #transform
		relative = bool(self.parentUi.chk003.isChecked())#Move absolute/relative toggle
		worldspace = bool(self.parentUi.chk004.isChecked())#Move object/worldspace toggle
		xyz = self.transformChecks()
		
		#Scale selected.
		if self.parentUi.chk005.isChecked():
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
		if self.parentUi.chk008.isChecked():
			pm.xform (relative=relative, worldSpace=worldspace, objectSpace=(not worldspace), translation=(xyz[0], xyz[1], xyz[2]))

		#Rotate selected
		if self.parentUi.chk009.isChecked():
			pm.xform (relative=relative, worldSpace=worldspace, objectSpace=(not worldspace), rotation=(xyz[0], xyz[1], xyz[2]))


	def tb000(self, state=None):
		'''
		Drop To Grid
		'''
		tb = self.currentUi.tb000
		if state=='setMenu':
			tb.add('QCheckBox', setText='Move to Origin', setObjectName='chk014', setChecked=True, setToolTip='Move to origin (xyz 0,0,0).')
			tb.add('QCheckBox', setText='Use Lowest Point', setObjectName='chk015', setToolTip='Use Lowest bounding box point (else mid point).')
			tb.add('QCheckBox', setText='Center Pivot', setObjectName='chk016', setChecked=True, setToolTip='Center pivot on objects bounding box.')
			return

		origin = tb.chk014.isChecked()
		bBoxLowestPoint = tb.chk015.isChecked()
		centerPivot = tb.chk016.isChecked()

		selection = pm.ls(selection=1, objectsOnly=1)

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


	@Slots.message
	def tb001(self, state=None):
		'''
		Align Vertices

		Auto Align finds the axis with the largest variance, and set the axis checkboxes accordingly before performing a regular align.
		'''
		tb = self.currentUi.tb001
		if state=='setMenu':
			tb.add('QCheckBox', setText='X Axis', setObjectName='chk029', setToolTip='Align X axis')
			tb.add('QCheckBox', setText='Y Axis', setObjectName='chk030', setToolTip='Align Y axis')
			tb.add('QCheckBox', setText='Z Axis', setObjectName='chk031', setToolTip='Align Z axis')
			tb.add('QCheckBox', setText='Align Loop', setObjectName='chk007', setToolTip='Align entire edge loop from selected edge(s).')
			tb.add('QCheckBox', setText='Average', setObjectName='chk006', setChecked=True, setToolTip='Align to last selected object or average.')
			tb.add('QCheckBox', setText='Auto Align', setObjectName='chk010', setChecked=True, setToolTip='')
			tb.add('QCheckBox', setText='Auto Align: Two Axes', setObjectName='chk011', setToolTip='')
			return

		if tb.chk010.isChecked(): #Auto Align: if checked; set coordinates for auto align:
			sel = pm.ls(selection=1)

			if not len(sel)==0:
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

				vertices = pm.polyListComponentConversion(fromEdge=1, toVertexFace=1)
				vertex = vertices[0] if vertices else None
				vertexTangent = pm.polyNormalPerVertex(vertex, query=True, xyz=True)

				tx = abs(round(vertexTangent[0], 4))
				ty = abs(round(vertexTangent[1], 4))
				tz = abs(round(vertexTangent[2], 4))

				axis = max(x,y,z)
				tangent = max(tx,ty,tz)

				if tb.chk011.isChecked(): #Auto Align: Two Axes
					if axis==x: #"yz"
						self.toggleWidgets(tb, setChecked='chk030-31', setChecked_False='chk029')
					if axis==y: #"xz"
						self.toggleWidgets(tb, setChecked='chk029,chk031', setChecked_False='chk030')
					if axis==z: #"xy"
						self.toggleWidgets(tb, setChecked='chk029-30', setChecked_False='chk031')
				else:
					if any ([axis==x and tangent==ty, axis==y and tangent==tx]): #"z"
						self.toggleWidgets(tb, setChecked='chk031', setChecked_False='chk029-30')
					if any ([axis==x and tangent==tz, axis==z and tangent==tx]): #"y"
						self.toggleWidgets(tb, setChecked='chk030', setChecked_False='chk029,chk031')
					if any ([axis==y and tangent==tz, axis==z and tangent==ty]): #"x"
						self.toggleWidgets(tb, setChecked='chk029', setChecked_False='chk030-31')
			else:
				return 'Warning: An edge must be selected.'

		#align
		x = tb.chk029.isChecked()
		y = tb.chk030.isChecked()
		z = tb.chk031.isChecked()
		avg = tb.chk006.isChecked()
		loop = tb.chk007.isChecked()

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


	def b000(self):
		'''
		Transform -

		'''
		#change the textfield to neg value and call transform
		textfield = float(self.parentUi.s000.value())
		if textfield >=0:
			newText = -textfield
			self.parentUi.s000.setValue(newText)
		self.transform()


	def b001(self):
		'''
		Transform +

		'''
		#change the textfield to pos value and call transform
		textfield = float(self.parentUi.s000.value())
		if textfield <0:
			newText = abs(textfield)
			self.parentUi.s000.setValue(newText)
		self.transform()


	def b002(self):
		'''
		Freeze Transformations

		'''
		# mel.eval("performFreezeTransformations(0);")
		pm.makeIdentity(apply=True) #freeze transforms
		# pm.makeIdentity (obj, apply=1, t=1, r=1, s=1, n=0, pn=1)


	def b003(self):
		'''
		Center Pivot Object

		'''
		mel.eval("CenterPivot;")


	def b005(self):
		'''
		Move To

		'''
		sel = rt.getCurrentSelection()

		source = sel[0]
		target = sel[1]
		#move object to center of the last selected items bounding box
		source.center = target.center


	@Slots.message
	def b012(self):
		'''
		Toggle: Make Live

		'''
		state = self.cycle([1,0], 'toggleMakeLive')

		obj = pm.ls(sl=1)[0]
		if not obj:
			return 'Error: Nothing Selected.'

		if state:
			pm.makeLive(obj)  #construction planes, nurbs surfaces and polygon meshes can be made live. makeLive supports one live object at a time.
			self.viewPortMessage('{0}:<hl>makeLive: On</hl>'.format(obj))
		else:
			pm.makeLive(none=True)
			self.viewPortMessage('{0}:<hl>makeLive: Off</hl>'.format(obj))


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


	def b032(self):
		'''
		Reset Pivot Transforms

		'''
		mel.eval('''
		{ string $objs[] = `ls -sl -type transform -type geometryShape`;
		if (size($objs) > 0) { xform -cp; } manipPivot -rp -ro; };
		''')




#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------