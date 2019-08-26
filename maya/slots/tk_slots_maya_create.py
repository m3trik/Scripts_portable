import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Create(Init):
	def __init__(self, *args, **kwargs):
		super(Create, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('create')
		self.ui.progressBar.hide()

		self.node=None
		self.rotation = {'x':[90,0,0], 'y':[0,90,0], 'z':[0,0,90], '-x':[-90,0,0], '-y':[0,-90,0], '-z':[0,0,-90], 'last':[]}
		self.point=[0,0,0]
		self.history=[]


		#spinboxes on valueChanged; connect to sXXX method with index as arg
		self.spinboxes = self.getObject(self.ui, 's000-13')
		for i, s in enumerate(self.spinboxes):
			s.valueChanged.connect (lambda: self.sXXX(i)) #ie. self.ui.s000.valueChanged.connect (lambda: self.sXXX(0))



	def getAxis(self):
		'''

		'''
		if self.ui.chk000.isChecked():
			axis = 'x'
		elif self.ui.chk001.isChecked():
			axis = 'y'
		elif self.ui.chk002.isChecked():
			axis = 'z'
		if self.ui.chk003.isChecked(): #negative
			axis = '-'+axis
		return axis


	def rotateAbsolute(self, axis):
		'''
		undo previous rotation and rotate on the specified axis.
		uses an external rotation dictionary.
		args:	axis='string' - axis to rotate on. ie. '-x'
		'''
		axis = self.rotation[axis]

		rotateOrder = pm.xform (self.node, query=1, rotateOrder=1)
		pm.xform (self.node, preserve=1, rotation=axis, rotateOrder=rotateOrder, absolute=1)
		self.rotation['last'] = axis


	def sXXX(self, index=None):
		'''
		set node attributes from multiple spinbox values.
		args: index=int - optional index of the spinbox that called this function. ie. 5 from s005
		'''
		spinboxValues = {s.prefix().rstrip(': '):s.value() for s in self.spinboxes} #current spinbox values. ie. from s000 get the value of six and add it to the list
		self.setAttributesMEL(self.node, spinboxValues) #set attributes for the history node


	def t000(self):
		'''
		Set Translate X
		'''
		self.point[0] = float(self.ui.t000.text())
		pm.xform (self.node, translation=self.point, worldSpace=1, absolute=1)


	def t001(self):
		'''
		Set Translate Y
		'''
		self.point[1] = float(self.ui.t001.text())
		pm.xform (self.node, translation=self.point, worldSpace=1, absolute=1)


	def t002(self):
		'''
		Set Translate Z
		'''
		self.point[2] = float(self.ui.t002.text())
		pm.xform (self.node, translation=self.point, worldSpace=1, absolute=1)


	def t003(self):
		'''
		Set Name

		'''
		pm.rename(self.node.name() ,self.ui.t003.text())


	def chk000(self):
		'''
		Rotate X Axis

		'''
		self.setButtons(self.ui, checked='chk000',unchecked='chk001, chk002')
		if self.node:
			self.rotateAbsolute(self.getAxis())


	def chk001(self):
		'''
		Rotate Y Axis

		'''
		self.setButtons(self.ui, checked='chk001',unchecked='chk000, chk002')
		if self.node:
			self.rotateAbsolute(self.getAxis())


	def chk002(self):
		'''
		Rotate Z Axis

		'''
		self.setButtons(self.ui, checked='chk002',unchecked='chk000, chk001')
		if self.node:
			self.rotateAbsolute(self.getAxis())


	def chk003(self):
		'''
		Rotate Negative Axis
		'''
		if self.node:
			self.rotateAbsolute(self.getAxis())


	def chk005(self):
		'''
		Set Point

		'''
		#add support for averaging multiple components.
		selection = pm.ls (selection=1, flatten=1)
		try:
			self.point = pm.xform (selection, query=1, translation=1, worldSpace=1, absolute=1)
		except:
			print "# Warning: Nothing selected. Point set to origin [0,0,0]. #"
			self.point = [0,0,0]

		self.ui.t000.setText(str(self.point[0]))
		self.ui.t001.setText(str(self.point[1]))
		self.ui.t002.setText(str(self.point[2]))


	def cmb000(self):
		cmb = self.ui.cmb000

		self.ui.cmb001.clear()

		if cmb.currentIndex() == 0:
			polygons = ["Cube", "Sphere", "Cylinder", "Plane", "Circle", "Cone", "Pyramid", "Torus", "Tube", "GeoSphere", "Platonic Solids", "Text"]
			self.ui.cmb001.addItems(polygons)

		if cmb.currentIndex() == 1:
			nurbs = ["Cube", "Sphere", "Cylinder", "Cone", "Plane", "Torus", "Circle", "Square"]
			self.ui.cmb001.addItems(nurbs)

		if cmb.currentIndex() == 2:
			lights = ["Ambient", "Directional", "Point", "Spot", "Area", "Volume", "VRay Sphere", "VRay Dome", "VRay Rect", "VRay IES"]
			self.ui.cmb001.addItems(lights)


	def cmb002(self):
		'''
		Editors
		'''
		cmb = self.ui.cmb002
		
		files = ['']
		contents = self.comboBox(cmb, files, '::')

		index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				mel.eval('')
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Create Object
		'''
		axis = self.rotation[self.getAxis()] #get axis as [int list]

		#polygons
		if self.ui.cmb000.currentIndex() == 0:

			#cube:
			if self.ui.cmb001.currentIndex() == 0:
				self.node = pm.polyCube (axis=axis, width=5, height=5, depth=5, subdivisionsX=1, subdivisionsY=1, subdivisionsZ=1)

			#sphere:
			if self.ui.cmb001.currentIndex() == 1:
				self.node = pm.polySphere (axis=axis, radius=5, subdivisionsX=12, subdivisionsY=12)

			#cylinder:
			if self.ui.cmb001.currentIndex() == 2:
				self.node = pm.polyCylinder (axis=axis, radius=5, height=10, subdivisionsX=1, subdivisionsY=1, subdivisionsZ=1)

			#plane:
			if self.ui.cmb001.currentIndex() == 3:
				self.node = pm.polyPlane (axis=axis, width=5, height=5, subdivisionsX=1, subdivisionsY=1)

			#circle:
			if self.ui.cmb001.currentIndex() == 4:
				axis = next(key for key, value in self.rotation.items() if value==axis and key!='last') #get key from value, as createCircle takes the key (ie. 'x') as an argument.
				self.node = self.createCircle(axis=axis, numPoints=5, radius=5, mode=0)

			#Cone:
			if self.ui.cmb001.currentIndex() == 5:
				self.node = pm.polyCone (axis=axis, radius=5, height=5, subdivisionsX=1, subdivisionsY=1, subdivisionsZ=1)

			#Pyramid
			if self.ui.cmb001.currentIndex() == 6:
				self.node = pm.polyPyramid (axis=axis, sideLength=5, numberOfSides=5, subdivisionsHeight=1, subdivisionsCaps=1)

			#Torus:
			if self.ui.cmb001.currentIndex() == 7:
				self.node = pm.polyTorus (axis=axis, radius=10, sectionRadius=5, twist=0, subdivisionsX=5, subdivisionsY=5)

			#Pipe
			if self.ui.cmb001.currentIndex() == 8:
				self.node = pm.polyPipe (axis=axis, radius=5, height=5, thickness=2, subdivisionsHeight=1, subdivisionsCaps=1)

			#Soccer ball
			if self.ui.cmb001.currentIndex() == 9:
				self.node = pm.polyPrimitive(axis=axis, radius=5, sideLength=5, polyType=0)

			#Platonic solids
			if self.ui.cmb001.currentIndex() == 10:
				self.node = mel.eval("performPolyPrimitive PlatonicSolid 0;")


		#nurbs
		if self.ui.cmb000.currentIndex() == 1:

			#Cube
			if self.ui.cmb001.currentIndex() == 0:
				self.node = pm.nurbsCube (ch=1, d=3, hr=1, p=(0, 0, 0), lr=1, w=1, v=1, ax=(0, 1, 0), u=1)

			#Sphere
			if self.ui.cmb001.currentIndex() == 1:
				self.node = pm.sphere (esw=360, ch=1, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))

			#Cylinder
			if self.ui.cmb001.currentIndex() == 2:
				self.node = pm.cylinder (esw=360, ch=1, d=3, hr=2, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))

			#Cone
			if self.ui.cmb001.currentIndex() == 3:
				self.node = pm.cone (esw=360, ch=1, d=3, hr=2, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))

			#Plane
			if self.ui.cmb001.currentIndex() == 4:
				self.node = pm.nurbsPlane (ch=1, d=3, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 1, 0), lr=1)

			#Torus
			if self.ui.cmb001.currentIndex() == 5:
				self.node = pm.torus (esw=360, ch=1, d=3, msw=360, ut=0, ssw=0, hr=0.5, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))

			#Circle
			if self.ui.cmb001.currentIndex() == 6:
				self.node = pm.circle (c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(0, 1, 0))

			#Square
			if self.ui.cmb001.currentIndex() == 7:
				self.node = pm.nurbsSquare (c=(0, 0, 0), ch=1, d=3, sps=1, sl1=1, sl2=1, nr=(0, 1, 0))


		#lights
		if self.ui.cmb000.currentIndex() == 2:
			
			#
			if self.ui.cmb001.currentIndex() == 0:
				pass
		

		#set name
		if isinstance(self.node[0], (str,unicode)): #is type of:
			self.ui.t003.setText(self.node[0])
		else:
			self.ui.t003.setText(self.node[0].name())

		self.history.extend(self.node) #save current node to history
		self.rotation['last']=[] #reset rotation history

		#translate the newly created node
		pm.xform (self.node, translation=self.point, worldSpace=1, absolute=1)

		exclude = [u'message', u'caching', u'frozen', u'isHistoricallyInteresting', u'nodeState', u'binMembership', u'output', u'axis', u'axisX', u'axisY', u'axisZ', u'paramWarn', u'uvSetName', 'maya70']
		attributes = self.getAttributesMEL(self.node, exclude) #get list of attributes and their values using the transform node.
		self.setSpinboxes (self.ui, 's000-13', attributes)

		pm.select(self.node) #select the transform node so that you can see any edits


	def b001(self):
		'''
		
		'''
		pass

	def b002(self):
		'''
		
		'''
		pass

	def b003(self):
		'''
		
		'''
		pass

	def b004(self):
		'''
		
		'''
		pass








#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------


