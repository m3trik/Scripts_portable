from tk_slots_max_init import *


import os.path



class Create(Init):
	def __init__(self, *args, **kwargs):
		super(Create, self).__init__(*args, **kwargs)

		self.ui = self.sb.getUi('create')
		self.submenu = self.sb.getUi('create_submenu')

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
		Undo previous rotation and rotate on the specified axis.
		uses an external rotation dictionary.
		args:
			axis (str) = axis to rotate on. ie. '-x'
		'''
		angle = [a for a in self.rotation[axis] if a!=0][0] #get angle. ie. 90 or -90
		axis = self.rotation[axis] #get axis list from string key. In 3ds max, the axis key is used as bool values, ie. [0, 90, 0] will essentially be used as [0,1,0]

		last = self.rotation['last']
		if last: #if previous rotation stored: undo previous rotation
			rt.rotate(self.node, rt.angleaxis(angle*-1, rt.point3(last[0], last[1], last[2]))) #multiplying the angle *1 inverts it. ie. -90 becomes 90
		
		rt.rotate(self.node, rt.angleaxis(angle, rt.point3(axis[0], axis[1], axis[2]))) #perform new rotation
		self.rotation['last'] = axis #store rotation
		rt.redrawViews()


	def sXXX(self, index=None):
		'''
		Set node attributes from multiple spinbox values.
		args:
			index (int) = optional index of the spinbox that called this function. ie. 5 from s005
		'''
		spinboxValues = {s.prefix().rstrip(': '):s.value() for s in self.spinboxes} #current spinbox values. ie. from s000 get the value of six and add it to the list
		# print spinboxValues
		self.setAttributes(self.node, spinboxValues)
		rt.redrawViews()


	def t000(self):
		'''
		Set Translate X
		'''
		self.point[0] = float(self.ui.t000.text())
		self.node.pos = rt.point3(self.point[0], self.point[1], self.point[2])


	def t001(self):
		'''
		Set Translate Y
		'''
		self.point[1] = float(self.ui.t001.text())
		self.node.pos = rt.point3(self.point[0], self.point[1], self.point[2])


	def t002(self):
		'''
		Set Translate Z
		'''
		self.point[2] = float(self.ui.t002.text())
		self.node.pos = rt.point3(self.point[0], self.point[1], self.point[2])


	def t003(self):
		'''
		Set Name
		'''
		self.node.name = self.ui.t003.text()


	def chk000(self):
		'''
		Rotate X Axis
		'''
		self.toggleWidgets(self.ui, self.submenu, setChecked='chk000', setChecked_False='chk001,chk002')
		if self.node:
			self.rotateAbsolute(self.getAxis())
			

	def chk001(self):
		'''
		Rotate Y Axis
		'''
		self.toggleWidgets(self.ui, self.submenu, setChecked='chk001', setChecked_False='chk000,chk002')
		if self.node:
			self.rotateAbsolute(self.getAxis())


	def chk002(self):
		'''
		Rotate Z Axis
		'''
		self.toggleWidgets(self.ui, self.submenu, setChecked='chk002', setChecked_False='chk001,chk000')
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
		#add support for averaging multiple components and multiple component types.
		obj = rt.selection[0]
		if obj:
			if rt.subObjectLevel==1: #vertex
				vertex = rt.bitArrayToArray(rt.polyop.getVertSelection(obj))
				point = rt.polyop.getVert(obj, vertex[0]) #Returns the position of the specified vertex.
				self.point = point
			else:
				self.point = obj.position
		else:
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


	def cmb002(self, index=None):
		'''
		Editors
		'''
		cmb = self.ui.cmb002

		files = ['']
		contents = cmb.addItems_(files, ' ')

		if not index:
			index = cmb.currentIndex()
		if index!=0:
			if index==contents.index(''):
				pass
			cmb.setCurrentIndex(0)


	def b000(self):
		'''
		Create Object
		'''
		axis = self.getAxis() #get axis as 'string'

		# polygons
		if self.ui.cmb000.currentIndex() == 0:
			
			#cube:
			if self.ui.cmb001.currentIndex() == 0:
				self.node = rt.Box(width=15, length=15, height=15, lengthsegs=1, widthsegs=1, heightsegs=1)

			#sphere:
			if self.ui.cmb001.currentIndex() == 1:
				self.node = rt.Sphere(radius=5, segs=12)

			#cylinder:
			if self.ui.cmb001.currentIndex() == 2:
				self.node = rt.Cylinder(radius=5, height=10, sides=5, heightsegs=1, capsegs=1, smooth=True)

			#plane:
			if self.ui.cmb001.currentIndex() == 3:
				self.node = rt.Plane(width=5, length=5, widthsegs=1, lengthsegs=1)

			#circle:
			if self.ui.cmb001.currentIndex() == 4:
				mode = None
				axis = next(key for key, value in self.rotation.items() if value==axis and key!='last') #get key from value as createCircle takes the key argument
				self.node = self.createCircle(axis=axis, numPoints=5, radius=5, mode=mode)

			#Cone:
			if self.ui.cmb001.currentIndex() == 5:
				self.node = rt.Cone(radius1=5, radius2=1, height=5, capsegs=1, heightsegs=1, sides=12, smooth=True)

			#Pyramid
			if self.ui.cmb001.currentIndex() == 6:
				self.node = rt.Pyramid(width=5, depth=3, height=5, widthsegs=1, depthSegs=1, heightsegs=1)

			#Torus:
			if self.ui.cmb001.currentIndex() == 7:
				self.node = rt.Torus(radius1=10, radius2=5, segs=5)

			#Pipe
			if self.ui.cmb001.currentIndex() == 8:
				self.node = rt.Tube(radius1=5, radius2=8, height=25, sides=12, capSegs=1, hightSegs=1)

			#Soccer ball
			if self.ui.cmb001.currentIndex() == 9:
				self.node = rt.GeoSphere(radius=5, segs=2, baseType=2, smooth=True)

			#Platonic solids
			if self.ui.cmb001.currentIndex() == 10:
				pass

		# nurbs
		# if self.ui.cmb000.currentIndex() == 1:
			
		# 	#Cube
		# 	if self.ui.cmb001.currentIndex() == 0:
		# 		self.node = pm.nurbsCube (ch=1, d=3, hr=1, p=(0, 0, 0), lr=1, w=1, v=1, ax=(0, 1, 0), u=1)

		# 	#Sphere
		# 	if self.ui.cmb001.currentIndex() == 1:
		# 		self.node = pm.sphere (esw=360, ch=1, d=3, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))

		# 	#Cylinder
		# 	if self.ui.cmb001.currentIndex() == 2:
		# 		self.node = pm.cylinder (esw=360, ch=1, d=3, hr=2, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))

		# 	#Cone
		# 	if self.ui.cmb001.currentIndex() == 3:
		# 		self.node = pm.cone (esw=360, ch=1, d=3, hr=2, ut=0, ssw=0, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=1, ax=(0, 1, 0))

		# 	#Plane
		# 	if self.ui.cmb001.currentIndex() == 4:
		# 		self.node = pm.nurbsPlane (ch=1, d=3, v=1, p=(0, 0, 0), u=1, w=1, ax=(0, 1, 0), lr=1)

		# 	#Torus
		# 	if self.ui.cmb001.currentIndex() == 5:
		# 		self.node = pm.torus (esw=360, ch=1, d=3, msw=360, ut=0, ssw=0, hr=0.5, p=(0, 0, 0), s=8, r=1, tol=0.01, nsp=4, ax=(0, 1, 0))

		# 	#Circle
		# 	if self.ui.cmb001.currentIndex() == 6:
		# 		self.node = pm.circle (c=(0, 0, 0), ch=1, d=3, ut=0, sw=360, s=8, r=1, tol=0.01, nr=(0, 1, 0))

		# 	#Square
		# 	if self.ui.cmb001.currentIndex() == 7:
		# 		self.node = pm.nurbsSquare (c=(0, 0, 0), ch=1, d=3, sps=1, sl1=1, sl2=1, nr=(0, 1, 0))

		
		# lights
		if self.ui.cmb000.currentIndex() == 2:
			
			#
			if self.ui.cmb001.currentIndex() == 0:
				pass


		#set name
		if isinstance(self.node, (str,unicode)): #is type of:
			self.ui.t003.setText(self.node)
		else:
			self.ui.t003.setText(self.node.name)

		self.history.extend(self.node) #save current node to history
		self.rotation['last']=[] #reset rotation history

		#translate the newly created node
		self.node.pos = rt.point3(self.point[0], self.point[1], self.point[2])
		#rotate
		self.rotateAbsolute(axis)

		exclude = ['getmxsprop', 'setmxsprop', 'typeInHeight', 'typeInLength', 'typeInPos', 'typeInWidth', 'typeInDepth', 'typeInRadius', 'typeInRadius1', 'typeInRadius2', 'typeinCreationMethod']	
		attributes = self.getAttributes(self.node, exclude)
		self.setSpinboxes(self.ui, 's000-13', attributes)

		# if self.ui.cmb000.currentIndex() == 0: #if create type: polygon; convert to editable poly
		# 	rt.convertTo(self.node, rt.PolyMeshObject) #convert after adding primitive attributes to spinboxes

		rt.select(self.node) #select the transform node so that you can see any edits
		rt.redrawViews()


	def create(self, catagory1, catagory2):
		'''
		ie. create('Polygons', 'Cube')
		args:
			catagory1 (str) = type
			catagory2 (str) = type
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
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------


