import maya.mel as mel
import pymel.core as pm

import os.path

from tk_slots_maya_init import Init





class Create(Init):
	def __init__(self, *args, **kwargs):
		super(Create, self).__init__(*args, **kwargs)


		

		self.rotation = {'x':[90,0,0], 'y':[0,90,0], 'z':[0,0,90], '-x':[-90,0,0], '-y':[0,-90,0], '-z':[0,0,-90], 'last':[]}
		self.lastValue=0
		self.point=[0,0,0]
		self.history = []


		self.ui.s000.valueChanged.connect (lambda: self.setAttributes(0))
		self.ui.s001.valueChanged.connect (lambda: self.setAttributes(1))
		self.ui.s002.valueChanged.connect (lambda: self.setAttributes(2))
		self.ui.s003.valueChanged.connect (lambda: self.setAttributes(3))
		self.ui.s004.valueChanged.connect (lambda: self.setAttributes(4))
		self.ui.s005.valueChanged.connect (lambda: self.setAttributes(5))
		self.ui.s006.valueChanged.connect (lambda: self.setAttributes(6))
		self.ui.s007.valueChanged.connect (lambda: self.setAttributes(7))
		self.ui.s008.valueChanged.connect (lambda: self.setAttributes(8))
		self.ui.s009.valueChanged.connect (lambda: self.setAttributes(9))
		self.ui.s010.valueChanged.connect (lambda: self.setAttributes(10))
		self.ui.s011.valueChanged.connect (lambda: self.setAttributes(11))


	def t000(self):
		'''
		Set Name

		'''
		newName = self.ui.t000.text()
		print 't000:', self.history, newName
		newName = pm.rename (self.history[-1], newName)
		self.history = newName
		print 'newName', newName, self.history

	def chk000(self):
		'''
		Rotate X Axis

		'''
		self.setButtons(self.ui, checked='chk000',unchecked='chk001, chk002')
		obj = pm.ls(sl=1)[0]
		if obj:
			axis = self.rotation['x']
			rotateOrder = pm.xform (obj, query=1, rotateOrder=1)
			pm.xform (obj, preserve=1, rotation=axis, rotateOrder=rotateOrder, absolute=1)
			self.rotation['last'] = axis
		else:
			print "# Warning: nothing selected #"

	def chk001(self):
		'''
		Rotate Y Axis

		'''
		self.setButtons(self.ui, checked='chk001',unchecked='chk000, chk002')
		obj = pm.ls(sl=1)[0]
		if obj:
			axis = self.rotation['y']
			rotateOrder = pm.xform (obj, query=1, rotateOrder=1)
			pm.xform (obj, preserve=1, rotation=axis, rotateOrder=rotateOrder, absolute=1)
			self.rotation['last'] = axis
		else:
			print "# Warning: nothing selected #"

	def chk002(self):
		'''
		Rotate Z Axis

		'''
		self.setButtons(self.ui, checked='chk002',unchecked='chk000, chk001')
		obj = pm.ls(sl=1)[0]
		if obj:
			axis = self.rotation['z']
			rotateOrder = pm.xform (obj, query=1, rotateOrder=1)
			pm.xform (obj, preserve=1, rotation=axis, rotateOrder=rotateOrder, absolute=1)
			self.rotation['last'] = axis
		else:
			print "# Warning: nothing selected #"

	def chk003(self):
		'''
		

		'''
		pass

	def chk004(self):
		'''
		

		'''
		pass

	def chk005(self):
		'''
		Set Point

		'''
		#add support for averaging multiple components.
		selection = pm.ls (selection=1, flatten=1)
		try:
			point = pm.xform (selection, query=1, translation=1, worldSpace=1, absolute=1)
			self.ui.s009.setValue(point[0]); self.ui.s010.setValue(point[1]); self.ui.s011.setValue(point[2])
			self.point = point #extend the list contents
			self.setButtons(self.ui, visible='s009-11')
		except:
			print "# Warning: Nothing selected. #"
			self.ui.s009.setValue(0); self.ui.s010.setValue(0); self.ui.s011.setValue(0)
			if self.point:
				del self.point[:]

	def cmb000(self):
		'''
		Set Create Type

		'''
		nurbs = ["Create", "Sphere", "Cube", "Cylinder", "Cone", "Plane", "Torus", "Circle", "Square"]
		polygons = ["Create", "Cube", "Sphere", "Cylinder", "Plane", "Circle", "Cone", "Pyramid", "Torus", "Tube", "Soccer Ball", "Platonic Solids", "Text"]
		lights = ["Create", "Ambient", "Directional", "Point", "Spot", "Area", "Volume", "VRay Sphere", "VRay Dome", "VRay Rect", "VRay IES"]

		if self.ui.cmb000.currentIndex() == 0: #polygons
			self.ui.cmb001.clear()
			self.ui.cmb001.addItems(polygons)

		if self.ui.cmb000.currentIndex() == 1: #nurbs
			self.ui.cmb001.clear()
			self.ui.cmb001.addItems(nurbs)

		if self.ui.cmb000.currentIndex() == 2: #lights
			self.ui.cmb001.clear()
			self.ui.cmb001.addItems(lights)

	def cmb001(self):
		'''
		Set Create Object

		'''
		if self.ui.cmb001.currentIndex() == 0:
			return #prevent referenced before assignment errors with inherited variables during initialization. 

		if self.ui.chk000.isChecked():
			axis = self.rotation['x']
		if self.ui.chk001.isChecked():
			axis = self.rotation['y']
		if self.ui.chk002.isChecked():
			axis = self.rotation['z']
		self.rotation['last'] = axis

		#nurbs
		if self.ui.cmb000.currentIndex() == 1:
			#Sphere
			if self.ui.cmb001.currentIndex() == 1:
				v = self.setSpinboxes (self.ui, values=[("radius",5),("start sweep",0),("end sweep",360),("sections",8),("spans",1),("height ratio",2)])
				node = pm.sphere (esw=360, ch=1, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))

			#Cube
			if self.ui.cmb001.currentIndex() == 2:
				v = self.setSpinboxes (self.ui, values=[("width",1),("length ratio",1),("height ratio",1),("patches U",1),("patches V",1)])
				node = pm.nurbsCube (ch=1, d=3, hr=1, p=(0, 0, 0), lr=1, w=1, v=1, ax=(0, 1, 0), u=1)

			#Cylinder
			if self.ui.cmb001.currentIndex() == 3:
				v = self.setSpinboxes (self.ui, values=[("radius",5),("start sweep",0),("end sweep",360),("sections",8),("spans",1),("height ratio",2)])
				node = pm.cylinder (esw=360, ch=1, d=3, hr=2, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))

			#Cone
			if self.ui.cmb001.currentIndex() == 4:
				v = self.setSpinboxes (self.ui, values=[("radius",5),("start sweep",0),("end sweep",360),("sections",8),("spans",1),("height ratio",2)])
				node = pm.cone (esw=360, ch=1, d=3, hr=2, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))

			#Plane
			if self.ui.cmb001.currentIndex() == 5:
				v = self.setSpinboxes (self.ui, values=[("width",1),("length ratio",1),("patches U",1),("patches V",1)])
				node = pm.nurbsPlane (ch=1, d=3, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 1, 0), lr=1)

			#Torus
			if self.ui.cmb001.currentIndex() == 6:
				v = self.setSpinboxes (self.ui, values=[("radius",5),("start sweep",0),("end sweep",360),("sections",8),("spans",4),("height ratio",1),("minor sweep",360)])
				node = pm.torus (esw=360, ch=1, d=3, msw=360, ut=0, ssw=0, hr=0.5, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))

			#Circle
			if self.ui.cmb001.currentIndex() == 7:
				v = self.setSpinboxes (self.ui, values=[("normal X",0),("normal Y",1),("normal Z",0),("center X",0),("center Y",0),("center Z",0),("radius",1),("sections",8)])
				node = pm.circle (c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(0, 1, 0))

			#Square
			if self.ui.cmb001.currentIndex() == 8:
				v = self.setSpinboxes (self.ui, values=[("normal X",0),("normal Y",1),("normal Z",0),("center X",0),("center Y",0),("center Z",0),("side length 1",1),("side length 2",1),("spans per side",1)])
				node = pm.nurbsSquare (c=(0, 0, 0), ch=1, d=3, sps=1, sl1=1, sl2=1, nr=(0, 1, 0))

		#lights
		if self.ui.cmb000.currentIndex() == 2:
			pass

		#polygons
		if self.ui.cmb000.currentIndex() == 0:
			#cube:
			if self.ui.cmb001.currentIndex() == 1:
				v = self.setSpinboxes (self.ui, values=[("size",15),("width",5),("depth",5),("height",5),("divisions X",1),("divisions Y",1),("divisions Z",1)])
				node = pm.polyCube (axis=axis, width=v[1], height=v[2], depth=v[3], subdivisionsX=v[4], subdivisionsY=v[5], subdivisionsZ=v[6])

			#sphere:
			if self.ui.cmb001.currentIndex() == 2:
				v = self.setSpinboxes (self.ui, values=[("size",5),("divisions X",1),("divisions Y",1)])
				node = pm.polySphere (axis=axis, radius=v[0], subdivisionsX=v[1], subdivisionsY=v[2])

			#cylinder:
			if self.ui.cmb001.currentIndex() == 3:
				v = self.setSpinboxes (self.ui, values=[("size",15),("radius",5),("height",10),("sides",5),("divisions height",1),("divisions caps",1),("round cap",0)])
				node = pm.polyCylinder (axis=axis, radius=v[1], height=(v[2]), subdivisionsX=v[3], subdivisionsY=v[4], subdivisionsZ=v[5])

			#plane:
			if self.ui.cmb001.currentIndex() == 4:
				v = self.setSpinboxes (self.ui, values=[("size",10),("width",5),("height",5),("divisions X",1),("divisions Y",1)])
				node = pm.polyPlane (axis=axis, width=v[1], height=v[2], subdivisionsX=v[3], subdivisionsY=v[4])

			#circle:
			if self.ui.cmb001.currentIndex() == 5:
				axis = next(key for key, value in self.rotation.items() if value==axis and key!='last') #get key from value as createCircle takes the key argument

				v = self.setSpinboxes (self.ui, values=[("size",5), ("sides",5), ("tri",0)])
				node = self.createCircle(axis=axis, numPoints=v[0], radius=v[1], mode=v[2])

			#Cone:
			if self.ui.cmb001.currentIndex() == 6:
				v = self.setSpinboxes (self.ui, values=[("size",10),("radius",5),("height",5),("divisions X",1),("divisions Y",1),("divisions Z",1),("round cap",0)])
				node = pm.polyCone (axis=axis, radius=v[1], height=v[2], subdivisionsX=v[3], subdivisionsY=v[4], subdivisionsZ=v[5])

			#Pyramid
			if self.ui.cmb001.currentIndex() == 7:
				v = self.setSpinboxes (self.ui, values=[("size",10),("side length",5),("sides",3),("divisions height",1),("divisions caps",1)])
				node = pm.polyPyramid (axis=axis, sideLength=5, numberOfSides=5, subdivisionsHeight=1, subdivisionsCaps=1)

			#Torus:
			if self.ui.cmb001.currentIndex() == 8:
				v = self.setSpinboxes (self.ui, values=[("size",20),("radius",10),("section radius",5),("twist",0),("divisions X",5),("divisions Y",5)])
				node = pm.polyTorus (axis=axis, radius=v[1], sectionRadius=v[2], twist=v[3], subdivisionsX=v[4], subdivisionsY=v[5])

			#Pipe
			if self.ui.cmb001.currentIndex() == 9:
				v = self.setSpinboxes (self.ui, values=[("size",10),("radius",5),("thickness",5),("divisions height",1),("divisions caps",1)])
				node = pm.polyPipe (axis=axis, radius=v[1], height=v[2], thickness=v[3], subdivisionsHeight=v[4], subdivisionsCaps=v[5])

			#Soccer ball
			if self.ui.cmb001.currentIndex() == 10:
				v = self.setSpinboxes (self.ui, values=[("size",10),("radius",5),("side length",5)])
				node = pm.polyPrimitive(axis=axis, radius=v[1], sideLength=v[2], polyType=0)

			#Platonic solids
			if self.ui.cmb001.currentIndex() == 11:
				mel.eval("performPolyPrimitive PlatonicSolid 0;")

		#translate the newly created node
		pm.xform (node, translation=self.point, worldSpace=1, absolute=1)
		#show text field and set name
		self.setButtons(self.ui, visible='t000')
		self.ui.t000.setText(str(node[0]))
		#set as current node for setting history
		self.history.extend(node)
		print 'self.history[0] (transform):', self.history[0]
		print 'self.history[1] (history):', self.history[1]

		self.ui.cmb001.setCurrentIndex(0)


	def setAttributes(self, index): #set history attributes
		#arg: int (index of the spinbox that called this function)
		node = str(self.history[-1]) if self.history else None #gets the history node
		print 's00'+str(index)

		if node:
			v=[] #list of integer values
			#get current spinbox objects
			spinboxes = self.getObject(self.ui, 's000-11')
			for spinbox in spinboxes:
				v.append(int(spinbox.value())) #current spinbox values. ie. from s000 get the value of six and add it to the list

			pm.select(str(self.history[-2])) #make sure the transform node is selected so that you can see any edits

			axis = self.rotation['last']
			pm.undoInfo(openChunk=1)

			#polygons
			if self.ui.cmb000.currentIndex() == 0:
				if 'Cube' in node:
					print node, index
					if index ==0: #size
						i=1; value = self.ui.s000.value()
						if self.lastValue > value:
							i=-1
						w = pm.getAttr (node+'.width')+i
						d = pm.getAttr (node+'.depth')+i
						h = pm.getAttr (node+'.height')+i
						pm.setAttr (node+'.width', w)
						pm.setAttr (node+'.depth', d)
						pm.setAttr (node+'.height',h)
						self.setSpinboxes (self.ui, spinboxNames='s001-3', values=[('width',w),('depth',d),('height',h)])
						self.lastValue = value
					if any([index==1, index==2, index==3]): #width, depth, height
						pm.setAttr (node+'.width', v[1])
						pm.setAttr (node+'.depth', v[2])
						pm.setAttr (node+'.height',v[3])
						self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2]+v[3])])
					pm.setAttr (node+'.subdivisionsWidth', v[4])
					pm.setAttr (node+'.subdivisionsHeight', v[5])
					pm.setAttr (node+'.subdivisionsDepth', v[6])

				if 'Sphere' in node:
					pm.setAttr (node+'.radius', v[0])
					pm.setAttr (node+'.subdivisionsAxis', v[1])
					pm.setAttr (node+'.subdivisionsHeight', v[2])

				if 'Cylinder' in node:
					if index ==0: #size
						i=1; value = self.ui.s000.value()
						if self.lastValue > value:
							i=-1
						r = pm.getAttr (node+'.radius')+i
						h = pm.getAttr (node+'.height')+i
						pm.setAttr (node+'.radius', r)
						pm.setAttr (node+'.height', h)
						self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('radius',r),('height',h)])
						self.lastValue = value
					if any([index==1, index==2]): #radius, height
						pm.setAttr (node+'.radius', v[1])
						pm.setAttr (node+'.height', v[2])
						self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
					pm.setAttr (node+'.subdivisionsAxis', v[3])
					pm.setAttr (node+'.subdivisionsHeight', v[4])
					pm.setAttr (node+'.subdivisionsCaps', v[5])
					pm.setAttr (node+'.roundCap', v[6])

				if 'Plane' in node:
					if index ==0: #size
						i=1; value = self.ui.s000.value()
						if self.lastValue > value:
							i=-1
						w = pm.getAttr (node+'.width')+i
						h = pm.getAttr (node+'.height')+i
						pm.setAttr (node+'.width', w)
						pm.setAttr (node+'.height',h)
						self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('width',w),('height',h)])
						self.lastValue = value
					if any([index==1, index==2]): #width, height
						pm.setAttr (node+'.width', v[1])
						pm.setAttr (node+'.height',v[2])
						self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
					pm.setAttr (node+'.subdivisionsWidth', v[3])
					pm.setAttr (node+'.subdivisionsHeight', v[4])

				if 'polyCreateFace' in node: #circle
					pm.delete()

					axis = next(key for key, value in self.rotation.items() if value==axis and key!='last') #get key from value as createCircle takes the key string argument

					circle = self.createCircle(axis=axis, radius=v[0], numPoints=v[1], mode=v[2])

				if 'Cone' in node:
					if index ==0: #size
						i=1; value = self.ui.s000.value()
						if self.lastValue > value:
							i=-1
						r = pm.getAttr (node+'.radius')+i
						h = pm.getAttr (node+'.height')+i
						pm.setAttr (node+'.radius', r)
						pm.setAttr (node+'.height', h)
						self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('radius',r),('height',h)])
						self.lastValue = value
					if any([index==1, index==2]): #radius, height
						pm.setAttr (node+'.radius', v[1])
						pm.setAttr (node+'.height', v[2])
						self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
					pm.setAttr (node+'.subdivisionsAxis', v[3])
					pm.setAttr (node+'.subdivisionsHeight', v[4])
					pm.setAttr (node+'.subdivisionsCap', v[5])
					pm.setAttr (node+'.roundCap', v[6])

				if 'Pyramid' in node:
					if index ==1: #history option for 'side length' doesnt exist so delete and recreate
						pm.delete()
						pyramid = pm.polyPyramid (axis=axis, sideLength=self.ui.s001.value())
					pm.setAttr (node+'.sideLength', v[0])
					pm.setAttr (node+'.numberOfSides', v[2])
					pm.setAttr (node+'.subdivisionsHeight', v[3])
					pm.setAttr (node+'.subdivisionsCaps', v[4])

				if 'Torus' in node:
					if index ==0: #size
						i=1; value = self.ui.s000.value()
						if self.lastValue > value:
							i=-1
						r = pm.getAttr (node+'.radius')+i
						s = pm.getAttr (node+'.sectionRadius')+i
						pm.setAttr (node+'.radius', r)
						pm.setAttr (node+'.sectionRadius', s)
						self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('radius',r),('section radius',s)])
						self.lastValue = value
					if any([index==1, index==2]): #radius, section radius
						pm.setAttr (node+'.radius', v[1])
						pm.setAttr (node+'.sectionRadius', v[2])
						self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
					pm.setAttr (node+'.twist', v[3])
					pm.setAttr (node+'.subdivisionsAxis', v[4])
					pm.setAttr (node+'.subdivisionsHeight', v[5])

				if 'Pipe' in node:
					if index ==0: #size
						i=1; value = self.ui.s000.value()
						if self.lastValue > value:
							i=-1
						r = pm.getAttr (node+'.radius')+i
						t = pm.getAttr (node+'.thickness')+i
						pm.setAttr (node+'.radius', r)
						pm.setAttr (node+'.thickness', t)
						self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('radius',r),('thickness',t)])
						self.lastValue = value
					if any([index==1, index==2]): #radius, thickness
						pm.setAttr (node+'.radius', v[1])
						pm.setAttr (node+'.thickness', v[2])
						self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
					pm.setAttr (node+'.subdivisionsHeight', v[3])
					pm.setAttr (node+'.subdivisionsCap', v[4])

				if 'Primitive' in node: #Soccer Ball
					if index ==0: #size
						i=1; value = self.ui.s000.value()
						if self.lastValue > value:
							i=-1
						r = pm.getAttr (node+'.radius')+i
						s = pm.getAttr (node+'.sideLength')+i
						pm.setAttr (node+'.radius', r)
						pm.setAttr (node+'.sideLength', s)
						self.setSpinboxes (self.ui, spinboxNames='s001-2', values=[('radius',r),('side length',s)])
						self.lastValue = value
					if any([index==1]): #radius
						pm.setAttr (node+'.radius', v[1])
						self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])
					if any([index==2]): #sideLength
						pm.setAttr (node+'.sideLength', v[2])
						self.setSpinboxes (self.ui, spinboxNames='s000', values=[('size',v[1]+v[2])])

			#nurbs
			if self.ui.cmb000.currentIndex() == 1:
				#Sphere
				if 'Sphere' in node:
					pm.setAttr (node+'.radius', v[0])
					pm.setAttr (node+'.startSweep', v[1])
					pm.setAttr (node+'.endSweep', v[2])
					pm.setAttr (node+'.sections', v[3])
					pm.setAttr (node+'.spans', v[4])
					pm.setAttr (node+'.heightRatio', v[5])

				#Cube
				if 'Cube' in node:
					pm.setAttr (node+'.width', v[0])
					pm.setAttr (node+'.lengthRatio', v[1])
					pm.setAttr (node+'.heightRatio', v[2])
					pm.setAttr (node+'.patchesU', v[3])
					pm.setAttr (node+'.patchesV', v[4])

				#Cylinder
				if 'Cylinder' in node:
					pm.setAttr (node+'.radius', v[0])
					pm.setAttr (node+'.startSweep', v[1])
					pm.setAttr (node+'.endSweep', v[2])
					pm.setAttr (node+'.sections', v[3])
					pm.setAttr (node+'.spans', v[4])
					pm.setAttr (node+'.heightRatio', v[5])

				#Cone
				if 'Cone' in node:
					pm.setAttr (node+'.radius', v[0])
					pm.setAttr (node+'.startSweep', v[1])
					pm.setAttr (node+'.endSweep', v[2])
					pm.setAttr (node+'.sections', v[3])
					pm.setAttr (node+'.spans', v[4])
					pm.setAttr (node+'.heightRatio', v[5])

				#Plane
				if 'Plane' in node:
					pm.setAttr (node+'.width', v[0])
					pm.setAttr (node+'.lengthRatio', v[1])
					pm.setAttr (node+'.patchesU', v[2])
					pm.setAttr (node+'.patchesV', v[3])

				#Torus
				if 'Torus' in node:
					pm.setAttr (node+'.radius', v[0])
					pm.setAttr (node+'.startSweep', v[1])
					pm.setAttr (node+'.endSweep', v[2])
					pm.setAttr (node+'.sections', v[3])
					pm.setAttr (node+'.spans', v[4])
					pm.setAttr (node+'.heightRatio', v[5])
					pm.setAttr (node+'.minorSweep', v[6])

				#Circle
				if 'Circle' in node:
					pm.setAttr (node+'.normalX', v[0])
					pm.setAttr (node+'.normalY', v[1])
					pm.setAttr (node+'.normalZ', v[2])
					pm.setAttr (node+'.centerX', v[3])
					pm.setAttr (node+'.centerY', v[4])
					pm.setAttr (node+'.centerZ', v[5])
					pm.setAttr (node+'.radius', v[6])
					pm.setAttr (node+'.sections', v[7])

				#Square
				if 'Square' in node:
					pm.setAttr (node+'.normalX', v[0])
					pm.setAttr (node+'.normalY', v[1])
					pm.setAttr (node+'.normalZ', v[2])
					pm.setAttr (node+'.centerX', v[3])
					pm.setAttr (node+'.centerY', v[4])
					pm.setAttr (node+'.centerZ', v[5])
					pm.setAttr (node+'.sideLength1', v[6])
					pm.setAttr (node+'.sideLength2', v[7])
					pm.setAttr (node+'.spansPerSide', v[8])

			#translate
			pm.xform (node, translation=[self.ui.s009.value(),self.ui.s009.value(),self.ui.s009.value()], worldSpace=1, absolute=1)

			pm.undoInfo(closeChunk=1)


	def b000(self):
		'''
		

		'''
		pass

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

	def b005(self):
		'''
		

		'''
		pass

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



#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------