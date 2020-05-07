from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Create(Init):
	def __init__(self, *args, **kwargs):
		super(Create, self).__init__(*args, **kwargs)

		self.ui = self.parentUi #self.ui = self.sb.getUi(self.__class__.__name__)

		self.node=None
		self.rotation = {'x':[90,0,0], 'y':[0,90,0], 'z':[0,0,90], '-x':[-90,0,0], '-y':[0,-90,0], '-z':[0,0,-90], 'last':[]}
		self.point=[0,0,0]
		self.history=[]


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
		args:	axis (str) = axis to rotate on. ie. '-x'
		'''
		axis = self.rotation[axis]

		rotateOrder = pm.xform (self.node, query=1, rotateOrder=1)
		pm.xform (self.node, preserve=1, rotation=axis, rotateOrder=rotateOrder, absolute=1)
		self.rotation['last'] = axis


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
		transform = self.node[0]
		pm.rename(transform.name() ,self.ui.t003.text())


	def chk000(self):
		'''
		Rotate X Axis

		'''
		self.toggleWidgets(self.ui, self.childUi, setChecked='chk000', setChecked_False='chk001, chk002')
		if self.node:
			self.rotateAbsolute(self.getAxis())


	def chk001(self):
		'''
		Rotate Y Axis

		'''
		self.toggleWidgets(self.ui, self.childUi, setChecked='chk001', setChecked_False='chk000, chk002')
		if self.node:
			self.rotateAbsolute(self.getAxis())


	def chk002(self):
		'''
		Rotate Z Axis

		'''
		self.toggleWidgets(self.ui, self.childUi, setChecked='chk002', setChecked_False='chk000, chk001')
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
			print("# Warning: Nothing selected. Point set to origin [0,0,0]. #")
			self.point = [0,0,0]

		self.ui.t000.setText(str(self.point[0]))
		self.ui.t001.setText(str(self.point[1]))
		self.ui.t002.setText(str(self.point[2]))


	def cmb000(self):
		'''

		'''
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


	def cmb002(self, index=None, values={}, clear=False, show=False):
		'''
		Get/Set Primitive Attributes.

		args:
			index (int) = parameter on activated, currentIndexChanged, and highlighted signals.
			values (dict) = Attibute and it's corresponding value. ie. {u'width': 10}
			clear (bool) = Clear any previous items.
			show (bool) = Show the popup menu immediately after adding items.
		'''
		cmb = self.ui.cmb002

		n = len(values)
		if n and index is None:
			cmb.popupStyle = 'qmenu'

			names = 's000-'+str(n-1)

			if clear:
				cmb.menu.clear()

			#add spinboxes
			[cmb.add('QDoubleSpinBox', setObjectName=name, preset_='0.00-100 step1') for name in self.unpackNames(names)]

			#set values
			self.setSpinboxes(cmb, names, values)

			#set signal/slot connections
			self.connect(names, 'valueChanged', self.sXXX, cmb)

			if show:
				cmb.showPopup()


	def sXXX(self, index=None):
		'''
		Set node attributes from multiple spinbox values.

		args:
			index(int) = optional index of the spinbox that called this function. ie. 5 from s005
		'''
		spinboxValues = {s.prefix().rstrip(': '):s.value() for s in self.ui.cmb002.menuItems()} #get current spinbox values. ie. {width:10} from spinbox prefix and value.
		self.setAttributesMEL(self.node, spinboxValues) #set attributes for the history node


	# def cmb002(self, index=None):
	# 	'''
	# 	Editors
	# 	'''
	# 	cmb = self.ui.cmb002
		
	# 	files = ['']
	# 	contents = cmb.addItems_(files, ' ')

	# 	if not index:
	# 		index = cmb.currentIndex()
	# 	if index!=0:
	# 		if index==contents.index(''):
	# 			mel.eval('')
	# 		cmb.setCurrentIndex(0)


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
		attributes = self.getAttributesMEL(self.node, exclude) #get dict of attributes and their values using the transform node.
		self.cmb002(values=attributes, clear=True, show=True)

		pm.select(self.node) #select the transform node so that you can see any edits


	def create(self, catagory1, catagory2):
		'''
		ie. create('Polygons', 'Cube')
		args:
			type1 (str) = 
			type2 (str) = 
		'''
		cmb000 = self.ui.cmb000
		cmb001 = self.ui.cmb001

		cmb000.setCurrentIndex(cmb000.findText(catagory1))
		cmb001.setCurrentIndex(cmb001.findText(catagory2))
		self.b000()


	def b001(self):
		'''
		Create poly cube
		'''
		self.create('Polygon', 'Cube')


	def b002(self):
		'''
		Create poly sphere
		'''
		self.create('Polygon', 'Sphere')


	def b003(self):
		'''
		Create poly cylinder
		'''
		self.create('Polygon', 'Cylinder')


	def b004(self):
		'''
		Create poly plane
		'''
		self.create('Polygon', 'Plane')









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------


