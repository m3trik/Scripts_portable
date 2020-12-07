from __future__ import print_function
from tk_slots_maya_init import *

import os.path



class Create(Init):
	def __init__(self, *args, **kwargs):
		super(Create, self).__init__(*args, **kwargs)

		self.rotation = {'x':[90,0,0], 'y':[0,90,0], 'z':[0,0,90], '-x':[-90,0,0], '-y':[0,-90,0], '-z':[0,0,-90], 'last':[]}
		self.point=[0,0,0]


	@property
	def node(self):
		'''
		Get the Transform Node
		'''
		transform = Init.getTransformNode()
		if transform:
			if not self.create.txt003.text()==transform.name(): #make sure the same field reflects the current working node.
				self.create.txt003.setText(transform.name())

		return transform


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.create.pin

		if state is 'setMenu':
			pin.contextMenu.add(widgets.TkComboBox, setObjectName='cmb000', setToolTip='')
			return


	def cmb003(self, index=None):
		'''
		Editors
		'''
		cmb = self.create.cmb003
		
		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		if index>0:
			if index==cmb.items.index(''):
				pass
			cmb.setCurrentIndex(0)


	def getAxis(self):
		'''

		'''
		if self.create.chk000.isChecked():
			axis = 'x'
		elif self.create.chk001.isChecked():
			axis = 'y'
		elif self.create.chk002.isChecked():
			axis = 'z'
		if self.create.chk003.isChecked(): #negative
			axis = '-'+axis
		return axis


	def rotateAbsolute(self, axis, node):
		'''
		undo previous rotation and rotate on the specified axis.
		uses an external rotation dictionary.

		:Parameters:
			axis (str) = axis to rotate on. ie. '-x'
			node (obj) = transform node.
		'''
		axis = self.rotation[axis]

		rotateOrder = pm.xform(node, query=1, rotateOrder=1)
		pm.xform(node, preserve=1, rotation=axis, rotateOrder=rotateOrder, absolute=1)
		self.rotation['last'] = axis


	def s000(self, value=None):
		'''
		Set Translate X
		'''
		if self.node:
			self.point[0] = float(self.create.s000.value())
			pm.xform (self.node, translation=self.point, worldSpace=1, absolute=1)


	def s001(self, value=None):
		'''
		Set Translate Y
		'''
		if self.node:
			self.point[1] = float(self.create.s001.value())
			pm.xform (self.node, translation=self.point, worldSpace=1, absolute=1)


	def s002(self, value=None):
		'''
		Set Translate Z
		'''
		if self.node:
			self.point[2] = float(self.create.s002.value())
			pm.xform (self.node, translation=self.point, worldSpace=1, absolute=1)


	def txt003(self):
		'''
		Set Name
		'''
		if self.node:
			pm.rename(self.node.name(), self.create.txt003.text())


	def chk000(self, state=None):
		'''
		Rotate X Axis
		'''
		self.toggleWidgets(setChecked='chk000', setUnChecked='chk001, chk002')
		if self.node:
			self.rotateAbsolute(self.getAxis(), self.node)


	def chk001(self, state=None):
		'''
		Rotate Y Axis
		'''
		self.toggleWidgets(setChecked='chk001', setUnChecked='chk000, chk002')
		if self.node:
			self.rotateAbsolute(self.getAxis(), self.node)


	def chk002(self, state=None):
		'''
		Rotate Z Axis
		'''
		self.toggleWidgets(setChecked='chk002', setUnChecked='chk000, chk001')
		if self.node:
			self.rotateAbsolute(self.getAxis(), self.node)


	def chk003(self, state=None):
		'''
		Rotate Negative Axis
		'''
		if self.node:
			self.rotateAbsolute(self.getAxis(), self.node)


	def chk005(self, state=None):
		'''
		Set Point
		'''
		#add support for averaging multiple components.
		selection = pm.ls(selection=1, flatten=1)
		try:
			self.point = pm.xform(selection, query=1, translation=1, worldSpace=1, absolute=1)
		except:
			self.point = [0,0,0]
			print('Warning: Nothing selected. Point set to origin [0,0,0].')

		self.create.s000.setValue(self.point[0])
		self.create.s001.setValue(self.point[1])
		self.create.s002.setValue(self.point[2])


	def cmb000(self, index=None):
		'''

		'''
		cmb = self.create.cmb000

		if index is 'setMenu':
			list_ = ['Polygon', 'NURBS', 'Light']
			cmb.addItems_(list_)
			return

		if index==0: #shared menu. later converted to the specified type.
			self.cmb001(0)

		if index==1:
			self.cmb001(1)

		if index==2:
			self.cmb001(2)


	def cmb001(self, index=None):
		'''

		'''
		cmb = self.create.cmb001

		if index is 'setMenu':
			list_ = ["Cube", "Sphere", "Cylinder", "Plane", "Circle", "Cone", "Pyramid", "Torus", "Tube", "GeoSphere", "Platonic Solids", "Text"]
			cmb.addItems_(list_)
			return

		polygons = ["Cube", "Sphere", "Cylinder", "Plane", "Circle", "Cone", "Pyramid", "Torus", "Tube", "GeoSphere", "Platonic Solids", "Text"]
		nurbs = ["Cube", "Sphere", "Cylinder", "Cone", "Plane", "Torus", "Circle", "Square"]
		lights = ["Ambient", "Directional", "Point", "Spot", "Area", "Volume", "VRay Sphere", "VRay Dome", "VRay Rect", "VRay IES"]

		if index==0: #shared menu. later converted to the specified type.
			cmb.addItems_(polygons, clear=True)

		if index==1:
			cmb.addItems_(nurbs, clear=True)

		if index==2:
			cmb.addItems_(lights, clear=True)


	@Init.attr
	def b000(self):
		'''
		Create Object
		'''
		axis = self.rotation[self.getAxis()] #get axis as [int list]
		type_ = self.create.cmb000.currentText()
		index = self.create.cmb001.currentIndex()

		#polygons
		if type_=='Polygon':
			if index==0: #cube:
				node = pm.polyCube (axis=axis, width=5, height=5, depth=5, subdivisionsX=1, subdivisionsY=1, subdivisionsZ=1)
			elif index==1: #sphere:
				node = pm.polySphere (axis=axis, radius=5, subdivisionsX=12, subdivisionsY=12)
			elif index==2: #cylinder:
				node = pm.polyCylinder (axis=axis, radius=5, height=10, subdivisionsX=1, subdivisionsY=1, subdivisionsZ=1)
			elif index==3: #plane:
				node = pm.polyPlane (axis=axis, width=5, height=5, subdivisionsX=1, subdivisionsY=1)
			elif index==4: #circle:
				axis = next(key for key, value in self.rotation.items() if value==axis and key!='last') #get key from value, as createCircle takes the key (ie. 'x') as an argument.
				node = self.createCircle(axis=axis, numPoints=5, radius=5, mode=0)
			elif index==5: #Cone:
				node = pm.polyCone (axis=axis, radius=5, height=5, subdivisionsX=1, subdivisionsY=1, subdivisionsZ=1)
			elif index==6: #Pyramid
				node = pm.polyPyramid (axis=axis, sideLength=5, numberOfSides=5, subdivisionsHeight=1, subdivisionsCaps=1)
			elif index==7: #Torus:
				node = pm.polyTorus (axis=axis, radius=10, sectionRadius=5, twist=0, subdivisionsX=5, subdivisionsY=5)
			elif index==8: #Pipe
				node = pm.polyPipe (axis=axis, radius=5, height=5, thickness=2, subdivisionsHeight=1, subdivisionsCaps=1)
			elif index==9: #Soccer ball
				node = pm.polyPrimitive(axis=axis, radius=5, sideLength=5, polyType=0)
			elif index==10: #Platonic solids
				node = mel.eval("performPolyPrimitive PlatonicSolid 0;")

		#nurbs
		if type_=='NURBS':
			if index==0: #Cube
				node = pm.nurbsCube (ch=1, d=3, hr=1, p=(0, 0, 0), lr=1, w=1, v=1, ax=(0, 1, 0), u=1)
			elif index==1: #Sphere
				node = pm.sphere (esw=360, ch=1, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))
			elif index==2: #Cylinder
				node = pm.cylinder (esw=360, ch=1, d=3, hr=2, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))
			elif index==3: #Cone
				node = pm.cone (esw=360, ch=1, d=3, hr=2, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))
			elif index==4: #Plane
				node = pm.nurbsPlane (ch=1, d=3, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 1, 0), lr=1)
			elif index==5: #Torus
				node = pm.torus (esw=360, ch=1, d=3, msw=360, ut=0, ssw=0, hr=0.5, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))
			elif index==6: #Circle
				node = pm.circle (c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(0, 1, 0))
			elif index==7: #Square
				node = pm.nurbsSquare (c=(0, 0, 0), ch=1, d=3, sps=1, sl1=1, sl2=1, nr=(0, 1, 0))

		#lights
		if type_=='Light':
			if index==0: #
				pass


		#set name
		if isinstance(node[0], (str,unicode)): #is type of:
			self.create.txt003.setText(node[0])
		else:
			self.create.txt003.setText(node[0].name())

		self.rotation['last']=[] #reset rotation history

		#translate the newly created node
		pm.xform(node, translation=self.point, worldSpace=1, absolute=1)

		pm.select(node) #select the transform node so that you can see any edits

		return self.getHistoryNode(node)


	def createPrimitive(self, catagory1, catagory2):
		'''
		ie. createPrimitive('Polygons', 'Cube')
		:Parameters:
			type1 (str) = 
			type2 (str) = 
		'''
		cmb000 = self.create.cmb000
		cmb001 = self.create.cmb001

		cmb000.setCurrentIndex(cmb000.findText(catagory1))
		cmb001.setCurrentIndex(cmb001.findText(catagory2))
		self.b000()
		self.tk.hide()


	def b001(self):
		'''
		Create poly cube
		'''
		self.createPrimitive('Polygon', 'Cube')


	def b002(self):
		'''
		Create poly sphere
		'''
		self.createPrimitive('Polygon', 'Sphere')


	def b003(self):
		'''
		Create poly cylinder
		'''
		self.createPrimitive('Polygon', 'Cylinder')


	def b004(self):
		'''
		Create poly plane
		'''
		self.createPrimitive('Polygon', 'Plane')









#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------


