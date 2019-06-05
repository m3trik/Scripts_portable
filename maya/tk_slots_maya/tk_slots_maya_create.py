import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Create(Init):
	def __init__(self, *args, **kwargs):
		super(Create, self).__init__(*args, **kwargs)


		self.ui = self.sb.getUi('create')

		self.ui.cmb000.removeEventFilter(self.signal)
		self.ui.cmb001.removeEventFilter(self.signal)

		self.node=None
		self.rotation = {'x':[90,0,0], 'y':[0,90,0], 'z':[0,0,90], '-x':[-90,0,0], '-y':[0,-90,0], '-z':[0,0,-90], 'last':[]}
		self.point=[0,0,0]
		self.history=[]


		#spinboxes on valueChanged; connect to sXXX method with index as arg
		self.spinboxes = self.getObject(self.ui, 's000-13')
		for i, s in enumerate(self.spinboxes):
			s.valueChanged.connect (lambda: self.sXXX(i)) #ie. self.ui.s000.valueChanged.connect (lambda: self.sXXX(0))



	def getAxis(self):
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
		if isinstance(self.node, (str,unicode)): #is type of:
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


#deprecated:

# def setAttributes(self, index): #set history attributes
	# #arg: int (index of the spinbox that called this function)
	# node = str(self.history[-1]) if self.history else None #gets the history node
	# print 's00'+str(index)

	# if node:
	# 	v=[] #list of integer values
	# 	#get current spinbox objects
	# 	spinboxes = self.getObject(self.ui, 's000-11')
	# 	for spinbox in spinboxes:
	# 		v.append(int(spinbox.value())) #current spinbox values. ie. from s000 get the value of six and add it to the list

	# 	pm.select(str(self.history[-2])) #make sure the transform node is selected so that you can see any edits

	# 	axis = self.rotation['last']
	# 	pm.undoInfo(openChunk=1)

	# 	#polygons
	# 	if self.ui.cmb000.currentIndex() == 0:
	# 		if 'Cube' in node:
	# 			print node, index
	# 			if index ==0: #size
	# 				i=1; value = self.ui.s000.value()
	# 				if self.lastValue > value:
	# 					i=-1
	# 				w = pm.getAttr (node+'.width')+i
	# 				d = pm.getAttr (node+'.depth')+i
	# 				h = pm.getAttr (node+'.height')+i
	# 				pm.setAttr (node+'.width', w)
	# 				pm.setAttr (node+'.depth', d)
	# 				pm.setAttr (node+'.height',h)
	# 				self.setSpinboxes (self.ui, spinboxNames='s001-3', values=[('width',w),('depth',d),('height',h)])
	# 				self.lastValue = value
	# 			if any([index==1, index==2, index==3]): #width, depth, height
	# 				pm.setAttr (node+'.width', v[1])
	# 				pm.setAttr (node+'.depth', v[2])
	# 				pm.setAttr (node+'.height',v[3])
	# 				self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2]+v[3])])
	# 			pm.setAttr (node+'.subdivisionsWidth', v[4])
	# 			pm.setAttr (node+'.subdivisionsHeight', v[5])
	# 			pm.setAttr (node+'.subdivisionsDepth', v[6])

	# 		if 'Sphere' in node:
	# 			pm.setAttr (node+'.radius', v[0])
	# 			pm.setAttr (node+'.subdivisionsAxis', v[1])
	# 			pm.setAttr (node+'.subdivisionsHeight', v[2])

	# 		if 'Cylinder' in node:
	# 			if index ==0: #size
	# 				i=1; value = self.ui.s000.value()
	# 				if self.lastValue > value:
	# 					i=-1
	# 				r = pm.getAttr (node+'.radius')+i
	# 				h = pm.getAttr (node+'.height')+i
	# 				pm.setAttr (node+'.radius', r)
	# 				pm.setAttr (node+'.height', h)
	# 				self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('radius',r),('height',h)])
	# 				self.lastValue = value
	# 			if any([index==1, index==2]): #radius, height
	# 				pm.setAttr (node+'.radius', v[1])
	# 				pm.setAttr (node+'.height', v[2])
	# 				self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
	# 			pm.setAttr (node+'.subdivisionsAxis', v[3])
	# 			pm.setAttr (node+'.subdivisionsHeight', v[4])
	# 			pm.setAttr (node+'.subdivisionsCaps', v[5])
	# 			pm.setAttr (node+'.roundCap', v[6])

	# 		if 'Plane' in node:
	# 			if index ==0: #size
	# 				i=1; value = self.ui.s000.value()
	# 				if self.lastValue > value:
	# 					i=-1
	# 				w = pm.getAttr (node+'.width')+i
	# 				h = pm.getAttr (node+'.height')+i
	# 				pm.setAttr (node+'.width', w)
	# 				pm.setAttr (node+'.height',h)
	# 				self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('width',w),('height',h)])
	# 				self.lastValue = value
	# 			if any([index==1, index==2]): #width, height
	# 				pm.setAttr (node+'.width', v[1])
	# 				pm.setAttr (node+'.height',v[2])
	# 				self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
	# 			pm.setAttr (node+'.subdivisionsWidth', v[3])
	# 			pm.setAttr (node+'.subdivisionsHeight', v[4])

	# 		if 'polyCreateFace' in node: #circle
	# 			pm.delete()

	# 			axis = next(key for key, value in self.rotation.items() if value==axis and key!='last') #get key from value as createCircle takes the key string argument

	# 			circle = self.createCircle(axis=axis, radius=v[0], numPoints=v[1], mode=v[2])

	# 		if 'Cone' in node:
	# 			if index ==0: #size
	# 				i=1; value = self.ui.s000.value()
	# 				if self.lastValue > value:
	# 					i=-1
	# 				r = pm.getAttr (node+'.radius')+i
	# 				h = pm.getAttr (node+'.height')+i
	# 				pm.setAttr (node+'.radius', r)
	# 				pm.setAttr (node+'.height', h)
	# 				self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('radius',r),('height',h)])
	# 				self.lastValue = value
	# 			if any([index==1, index==2]): #radius, height
	# 				pm.setAttr (node+'.radius', v[1])
	# 				pm.setAttr (node+'.height', v[2])
	# 				self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
	# 			pm.setAttr (node+'.subdivisionsAxis', v[3])
	# 			pm.setAttr (node+'.subdivisionsHeight', v[4])
	# 			pm.setAttr (node+'.subdivisionsCap', v[5])
	# 			pm.setAttr (node+'.roundCap', v[6])

	# 		if 'Pyramid' in node:
	# 			if index ==1: #history option for 'side length' doesnt exist so delete and recreate
	# 				pm.delete()
	# 				pyramid = pm.polyPyramid (axis=axis, sideLength=self.ui.s001.value())
	# 			pm.setAttr (node+'.sideLength', v[0])
	# 			pm.setAttr (node+'.numberOfSides', v[2])
	# 			pm.setAttr (node+'.subdivisionsHeight', v[3])
	# 			pm.setAttr (node+'.subdivisionsCaps', v[4])

	# 		if 'Torus' in node:
	# 			if index ==0: #size
	# 				i=1; value = self.ui.s000.value()
	# 				if self.lastValue > value:
	# 					i=-1
	# 				r = pm.getAttr (node+'.radius')+i
	# 				s = pm.getAttr (node+'.sectionRadius')+i
	# 				pm.setAttr (node+'.radius', r)
	# 				pm.setAttr (node+'.sectionRadius', s)
	# 				self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('radius',r),('section radius',s)])
	# 				self.lastValue = value
	# 			if any([index==1, index==2]): #radius, section radius
	# 				pm.setAttr (node+'.radius', v[1])
	# 				pm.setAttr (node+'.sectionRadius', v[2])
	# 				self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
	# 			pm.setAttr (node+'.twist', v[3])
	# 			pm.setAttr (node+'.subdivisionsAxis', v[4])
	# 			pm.setAttr (node+'.subdivisionsHeight', v[5])

	# 		if 'Pipe' in node:
	# 			if index ==0: #size
	# 				i=1; value = self.ui.s000.value()
	# 				if self.lastValue > value:
	# 					i=-1
	# 				r = pm.getAttr (node+'.radius')+i
	# 				t = pm.getAttr (node+'.thickness')+i
	# 				pm.setAttr (node+'.radius', r)
	# 				pm.setAttr (node+'.thickness', t)
	# 				self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('radius',r),('thickness',t)])
	# 				self.lastValue = value
	# 			if any([index==1, index==2]): #radius, thickness
	# 				pm.setAttr (node+'.radius', v[1])
	# 				pm.setAttr (node+'.thickness', v[2])
	# 				self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
	# 			pm.setAttr (node+'.subdivisionsHeight', v[3])
	# 			pm.setAttr (node+'.subdivisionsCap', v[4])

	# 		if 'Primitive' in node: #Soccer Ball
	# 			if index ==0: #size
	# 				i=1; value = self.ui.s000.value()
	# 				if self.lastValue > value:
	# 					i=-1
	# 				r = pm.getAttr (node+'.radius')+i
	# 				s = pm.getAttr (node+'.sideLength')+i
	# 				pm.setAttr (node+'.radius', r)
	# 				pm.setAttr (node+'.sideLength', s)
	# 				self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('radius',r),('side length',s)])
	# 				self.lastValue = value
	# 			if any([index==1]): #radius
	# 				pm.setAttr (node+'.radius', v[1])
	# 				self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
	# 			if any([index==2]): #sideLength
	# 				pm.setAttr (node+'.sideLength', v[2])
	# 				self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])

	# 	#nurbs
	# 	if self.ui.cmb000.currentIndex() == 1:
	# 		#Sphere
	# 		if 'Sphere' in node:
	# 			pm.setAttr (node+'.radius', v[0])
	# 			pm.setAttr (node+'.startSweep', v[1])
	# 			pm.setAttr (node+'.endSweep', v[2])
	# 			pm.setAttr (node+'.sections', v[3])
	# 			pm.setAttr (node+'.spans', v[4])
	# 			pm.setAttr (node+'.heightRatio', v[5])

	# 		#Cube
	# 		if 'Cube' in node:
	# 			pm.setAttr (node+'.width', v[0])
	# 			pm.setAttr (node+'.lengthRatio', v[1])
	# 			pm.setAttr (node+'.heightRatio', v[2])
	# 			pm.setAttr (node+'.patchesU', v[3])
	# 			pm.setAttr (node+'.patchesV', v[4])

	# 		#Cylinder
	# 		if 'Cylinder' in node:
	# 			pm.setAttr (node+'.radius', v[0])
	# 			pm.setAttr (node+'.startSweep', v[1])
	# 			pm.setAttr (node+'.endSweep', v[2])
	# 			pm.setAttr (node+'.sections', v[3])
	# 			pm.setAttr (node+'.spans', v[4])
	# 			pm.setAttr (node+'.heightRatio', v[5])

	# 		#Cone
	# 		if 'Cone' in node:
	# 			pm.setAttr (node+'.radius', v[0])
	# 			pm.setAttr (node+'.startSweep', v[1])
	# 			pm.setAttr (node+'.endSweep', v[2])
	# 			pm.setAttr (node+'.sections', v[3])
	# 			pm.setAttr (node+'.spans', v[4])
	# 			pm.setAttr (node+'.heightRatio', v[5])

	# 		#Plane
	# 		if 'Plane' in node:
	# 			pm.setAttr (node+'.width', v[0])
	# 			pm.setAttr (node+'.lengthRatio', v[1])
	# 			pm.setAttr (node+'.patchesU', v[2])
	# 			pm.setAttr (node+'.patchesV', v[3])

	# 		#Torus
	# 		if 'Torus' in node:
	# 			pm.setAttr (node+'.radius', v[0])
	# 			pm.setAttr (node+'.startSweep', v[1])
	# 			pm.setAttr (node+'.endSweep', v[2])
	# 			pm.setAttr (node+'.sections', v[3])
	# 			pm.setAttr (node+'.spans', v[4])
	# 			pm.setAttr (node+'.heightRatio', v[5])
	# 			pm.setAttr (node+'.minorSweep', v[6])

	# 		#Circle
	# 		if 'Circle' in node:
	# 			pm.setAttr (node+'.normalX', v[0])
	# 			pm.setAttr (node+'.normalY', v[1])
	# 			pm.setAttr (node+'.normalZ', v[2])
	# 			pm.setAttr (node+'.centerX', v[3])
	# 			pm.setAttr (node+'.centerY', v[4])
	# 			pm.setAttr (node+'.centerZ', v[5])
	# 			pm.setAttr (node+'.radius', v[6])
	# 			pm.setAttr (node+'.sections', v[7])

	# 		#Square
	# 		if 'Square' in node:
	# 			pm.setAttr (node+'.normalX', v[0])
	# 			pm.setAttr (node+'.normalY', v[1])
	# 			pm.setAttr (node+'.normalZ', v[2])
	# 			pm.setAttr (node+'.centerX', v[3])
	# 			pm.setAttr (node+'.centerY', v[4])
	# 			pm.setAttr (node+'.centerZ', v[5])
	# 			pm.setAttr (node+'.sideLength1', v[6])
	# 			pm.setAttr (node+'.sideLength2', v[7])
	# 			pm.setAttr (node+'.spansPerSide', v[8])

	# 	#translate
	# 	pm.xform (node, translation=[self.ui.s009.value(),self.ui.s009.value(),self.ui.s009.value()], worldSpace=1, absolute=1)

	# 	pm.undoInfo(closeChunk=1)