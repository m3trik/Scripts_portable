ccfrom __future__ import print_function
from tk_slots_max_init import *

import os.path



class Create(Init):
	def __init__(self, *args, **kwargs):
		super(Create, self).__init__(*args, **kwargs)

		self.rotation = {'x':[90,0,0], 'y':[0,90,0], 'z':[0,0,90], '-x':[-90,0,0], '-y':[0,-90,0], '-z':[0,0,-90], 'last':[]}
		self.point=[0,0,0]
		self.history=[]


	@property
	def node(self):
		'''
		Get the Transform Node
		'''
		selection = [i for i in rt.selection]
		if not selection:
			return None

		transform = selection[0]
		if not self.create.txt003.text()==transform.name: #make sure the same field reflects the current working node.
			self.create.txt003.setText(transform.name)
			self.constructAttributesForNode(transform) #update the attribute values for the current node.

		return transform


	def pin(self, state=None):
		'''
		Context menu
		'''
		pin = self.create.pin

		if state is 'setMenu':
			pin.add(QComboBox_, setObjectName='cmb003', setToolTip='')
			return


	def cmb003(self, index=None):
		'''
		Editors
		'''
		cmb = self.create.cmb000

		if index is 'setMenu':
			list_ = ['']
			cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


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
		Undo previous rotation and rotate on the specified axis.
		uses an external rotation dictionary.
		args:
			axis (str) = axis to rotate on. ie. '-x'
			node (obj) = transform node.
		'''
		angle = [a for a in self.rotation[axis] if a!=0][0] #get angle. ie. 90 or -90
		axis = self.rotation[axis] #get axis list from string key. In 3ds max, the axis key is used as bool values, ie. [0, 90, 0] will essentially be used as [0,1,0]

		last = self.rotation['last']
		if last: #if previous rotation stored: undo previous rotation
			rt.rotate(node, rt.angleaxis(angle*-1, rt.point3(last[0], last[1], last[2]))) #multiplying the angle *1 inverts it. ie. -90 becomes 90
		
		rt.rotate(node, rt.angleaxis(angle, rt.point3(axis[0], axis[1], axis[2]))) #perform new rotation
		self.rotation['last'] = axis #store rotation
		rt.redrawViews()


	def s000(self, value=None):
		'''
		Set Translate X
		'''
		if self.node:
			self.point[0] = float(self.create.s000.value())
			self.node.pos = rt.point3(self.point[0], self.point[1], self.point[2])
			rt.redrawViews()


	def s001(self, value=None):
		'''
		Set Translate Y
		'''
		if self.node:
			self.point[1] = float(self.create.s001.value())
			self.node.pos = rt.point3(self.point[0], self.point[1], self.point[2])
			rt.redrawViews()


	def s002(self, value=None):
		'''
		Set Translate Z
		'''
		if self.node:
			self.point[2] = float(self.create.s002.value())
			self.node.pos = rt.point3(self.point[0], self.point[1], self.point[2])
			rt.redrawViews()


	def txt003(self):
		'''
		Set Name
		'''
		if self.node:
			self.node.name = self.create.txt003.text()


	def chk000(self, state=None):
		'''
		Rotate X Axis
		'''
		self.toggleWidgets(setChecked='chk000', setUnChecked='chk001,chk002')
		if self.node:
			self.rotateAbsolute(self.getAxis(), self.node)


	def chk001(self, state=None):
		'''
		Rotate Y Axis
		'''
		self.toggleWidgets(setChecked='chk001', setUnChecked='chk000,chk002')
		if self.node:
			self.rotateAbsolute(self.getAxis(), self.node)


	def chk002(self, state=None):
		'''
		Rotate Z Axis
		'''
		self.toggleWidgets(setChecked='chk002', setUnChecked='chk001,chk000')
		if self.node:
			self.rotateAbsolute(self.getAxis(), self.node)


	def chk003(self, state=None):
		'''
		Rotate Negative Axis
		'''
		if self.node:
			self.rotateAbsolute(self.getAxis(), self.node)


	@Slots.message
	def chk005(self, state=None):
		'''
		Set Point
		'''
		error=0
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
			error = 1
			self.point = [0,0,0]

		self.create.s000.setValue(self.point[0])
		self.create.s001.setValue(self.point[1])
		self.create.s002.setValue(self.point[2])

		if error==1:
			return 'Error: Nothing selected. Point set to origin [0,0,0].'


	def cmb000(self, index=None):
		'''
		Create: Select Base Type
		'''
		cmb = self.create.cmb000

		if index is 'setMenu':
			list_ = ['Mesh', 'Editable Poly', 'Editable Mesh', 'Editable Patch', 'NURBS', 'Light']
			cmb.addItems_(list_)
			return

		primitives = ["Cube", "Sphere", "Cylinder", "Plane", "Circle", "Cone", "Pyramid", "Torus", "Tube", "GeoSphere", "Text"] 
		extendedPrimitives = ['Hedra', 'Torus Knot', 'Chamfer Box', 'Chamfer Cylinder', 'Oil Tank', 'Capsule', 'Spindle', 'L-Extrusion', 'Gengon', 'C-Extrusion', 'RingWave', 'Hose', 'Prism'] #Extended Primitives:
		nurbs = ["Cube", "Sphere", "Cylinder", "Cone", "Plane", "Torus", "Circle", "Square"]
		lights = ["Ambient", "Directional", "Point", "Spot", "Area", "Volume", "VRay Sphere", "VRay Dome", "VRay Rect", "VRay IES"]

		if index in (0, 1, 2, 3): #shared menu. later converted to the specified type.
			self.create.cmb001.addItems_(primitives+extendedPrimitives, clear=True)

		if index==4:
			self.create.cmb001.addItems_(nurbs, clear=True)

		if index==5:
			self.create.cmb001.addItems_(lights, clear=True)


	def cmb002(self, index=None, attributes={}, clear=False, show=False):
		'''
		Get/Set Primitive Attributes.

		args:
			index (int) = parameter on activated, currentIndexChanged, and highlighted signals.
			attributes (dict) = Attibute and it's corresponding value. ie. {width:10}
			clear (bool) = Clear any previous items.
			show (bool) = Show the popup menu immediately after adding items.
		'''
		cmb = self.create.cmb002

		if index is 'setMenu':
			cmb.popupStyle = 'qmenu'
			return

		attributes = {k:v for k,v in attributes.items() if isinstance(v,(int, float, bool))} #get only attributes of int, float, bool type.

		n = len(attributes)
		if n and index is None:
			names = 's000-'+str(n-1)

			if clear:
				cmb.menu.clear()

			#add spinboxes
			[cmb.add('QDoubleSpinBox', setObjectName=name, minMax_='0.00-100 step1') for name in self.unpackNames(names)]

			#set values
			self.setSpinboxes(cmb, names, attributes)

			#set signal/slot connections
			self.connect_(names, 'valueChanged', self.sXXX, cmb)

			if show:
				cmb.showPopup()


	def constructAttributesForNode(self, node):
		'''
		Populate the attributes comboBox with attributes of the given node.

		args:
			node (obj) = Scene object.
		'''
		exclude = ['getmxsprop', 'setmxsprop', 'typeInHeight', 'typeInLength', 'typeInPos', 'typeInWidth', 'typeInDepth', 
			'typeInRadius', 'typeInRadius1', 'typeInRadius2', 'typeinCreationMethod', 'edgeChamferQuadIntersections', 
			'edgeChamferType', 'hemisphere', 'realWorldMapSize', 'mapcoords']

		attributes = self.getAttributesMax(node, exclude)
		self.cmb002(attributes=attributes, clear=True, show=True)


	def sXXX(self, index=None):
		'''
		Set node attributes from multiple spinbox values.

		args:
			index(int) = optional index of the spinbox that called this function. ie. 5 from s005
		'''
		spinboxValues = {s.prefix().rstrip(': '):s.value() for s in self.create.cmb002.children_()} #current spinbox values. ie. from s000 get the value of six and add it to the list
		self.setAttributesMax(self.node, spinboxValues) #set attributes for the history node


	@Slots.message
	def b000(self):
		'''
		Create Object
		'''
		axis = self.getAxis() #get axis as 'string'
		type_ = self.create.cmb000.currentText()
		index = self.create.cmb001.currentIndex()

		if not type_:
			type_ = 'Mesh' #set default type

		if type_ in ['Mesh', 'Editable Poly', 'Polygon', 'Editable Mesh', 'Editable Patch', 'NURBS']: #Primitives
			if index==0: #cube:
				node = rt.Box(width=15, length=15, height=15, lengthsegs=1, widthsegs=1, heightsegs=1)
			elif index==1: #sphere:
				node = rt.Sphere(radius=5, segs=12)
			elif index==2: #cylinder:
				node = rt.Cylinder(radius=5, height=10, sides=5, heightsegs=1, capsegs=1, smooth=True)
			elif index==3: #plane:
				node = rt.Plane(width=5, length=5, widthsegs=1, lengthsegs=1)
			elif index==4: #circle:
				mode = None
				axis = next(key for key, value in self.rotation.items() if value==axis and key!='last') #get key from value
				node = self.createCircle(axis=axis, numPoints=5, radius=5, mode=mode)
			elif index==5: #Cone:
				node = rt.Cone(radius1=5, radius2=1, height=5, capsegs=1, heightsegs=1, sides=12, smooth=True)
			elif index==6: #Pyramid
				node = rt.Pyramid(width=5, depth=3, height=5, widthsegs=1, depthSegs=1, heightsegs=1)
			elif index==7: #Torus:
				node = rt.Torus(radius1=10, radius2=5, segs=5)
			elif index==8: #Pipe
				node = rt.Tube(radius1=5, radius2=8, height=25, sides=12, capSegs=1, hightSegs=1)
			elif index==9: #Soccer ball
				node = rt.GeoSphere(radius=5, segs=2, baseType=2, smooth=True)

		if type_ in ['Hedra', 'Torus Knot', 'Chamfer Box', 'Chamfer Cylinder', 'Oil Tank', 'Capsule', 'Spindle', 'L-Extrusion', 'Gengon', 'C-Extrusion', 'RingWave', 'Hose', 'Prism']: #Extended Primitives:
			if index==10: #Hedra
				rt.Hedra(family=0, scalep=100, scaleq=100, scaler=100, mapcoords=True, radius=13.2914, pos=[2.80033,-6.07454,0], isSelected=True)
			elif index==11: #Torus Knot
				rt.Torus_Knot(smooth=2, Base_Curve=0, segments=120, sides=12, radius=12.9131, radius2=2.82649, p=2, q=3, Eccentricity=1, Twist=0, Lumps=0, Lump_Height=0, Gen_UV=1, U_Tile=1, V_Tile=1, U_Offset=0, V_Offset=0, Warp_Height=0, Warp_Count=0, pos=[1.17498,-28.5641,0], isSelected=True)
			elif index==12: #Chamfer Box
				rt.ChamferBox(width=25.9508, fillet=2.08099, length=21.103, height=10.9843, pos=[57.3517,3.11597,0.005], isSelected=True)
			elif index==13: #Chamfer Cylinder
				rt.ChamferCyl(radius=9.90455, height=20.6785, fillet=0.792669, pos=[13.4798,-19.4707,0], isSelected=True)
			elif index==14: #Oil Tank
				rt.OilTank(radius=9.40818, Cap_Height=2.35204, height=24.5722, Blend=0, sides=12, Height_Segments=1, Smooth_On=1, Slice_On=0, Slice_From=0, Slice_To=0, mapcoords=1, pos=[-0.580549,-43.851,0], isSelected=True)
			elif index==15: #Capsule
				rt.Capsule(radius=8.8111, height=28.4398, heighttype=0, sides=12, heightsegs=1, smooth=True, sliceon=False, slicefrom=0, sliceto=0, mapcoords=True, pos=[-9.87687,-6.62625,0], isSelected=True)
			elif index==16: #Spindle
				rt.Spindle(radius=8.22467, Cap_Height=2.42833, height=21.3872, Blend=0, sides=12, Height_Segments=1, cap_segments=5, Smooth_On=1, Slice_On=0, Slice_From=0, Slice_To=0, mapcoords=1, pos=[-6.07937,-23.7136,0], isSelected=True)
			elif index==17: #L-Extrusion
				rt.L_Ext(Side_Length=10.0896, Front_Length=-5.57165, centerCreate=False, pos=[23.9174,-54.3066,0], isSelected=True, Front_Width=2.52126, Side_Width=2.52126, height=12.0807)
			elif index==18: #Gengon
				rt.Gengon(sides=5, radius=11.053, fillet=1.19902, height=20.8109, Side_Segments=1, Fillet_Segments=1, Height_Segments=1, mapcoords=1, pos=[-12.2299,13.1004,0], isSelected=True)
			elif index==19: #C-Extrusion
				rt.C_Ext(Front_Length=-7.54399, Back_Length=-7.54399, Side_Length=8.52505, centerCreate=False, pos=[-5.72067,-60.0124,0], isSelected=True, Front_Width=1.38667, Back_Width=1.38667, Side_Width=1.38667, height=22.6349)
			elif index==20: #Ringwave
				rt.RingWave(time_on=0, time_growing=9600, display_until=16000, repeats=2, max_diameter=8.17418, ring_width=2.37046, ring_segments=200, Outer_Edge_Breakup=False, Major_Cycles_Outer=1, Major_Cycle_Flux_Outer=0, Major_Cycle_Flux_Per_Outer=16000, Minor_Cycles_Outer=1, Minor_Cycle_Flux_Outer=0, Minor_Cycle_Flux_Per_Outer=-16000, Inner_Edge_Breakup=True, Major_Cycles_Inner=11, Major_Cycle_Flux_Inner=25, Major_Cycle_Flux_Per_Inner=19360, Minor_Cycles_Inner=29, Minor_Cycle_Flux_Inner=10, Minor_Cycle_Flux_Per_Inner=-4320, height=0, Height_Segs=1, Radius_Segs=1, Mapping_Coords=True, Smoothing=True, pos=[14.9087,-62.8923,0], isSelected=True)
			elif index==21: #Hose
				rt.Hose(End_Placement_Method=1, Hose_Height=26.8204, Segments_Along_Hose=45, Smooth_Spring=0, Renderable_Hose=1, Hose_Cross_Section_Type=0, Round_Hose_Diameter=10.3709, Round_Hose_Sides=8, Rectangular_Hose_Width=10.3709, Rectangular_Hose_Depth=10.3709, Rectangular_Hose_Fillet_Size=0, Rectangular_Hose_Fillet_Segs=0, Rectangular_Hose_Section_Rotation=0, D_Section_Hose_Width=10.3709, D_Section_Hose_Depth=10.3709, D_Section_Hose_Fillet_Size=0, D_Section_Hose_Fillet_Segs=0, D_Section_Hose_Round_Segs=4, D_Section_Hose_Section_Rotation=0, Generate_Mapping_Coordinates=1, Flex_Section_Enabled=1, Flex_Section_Start=10, Flex_Section_Stop=90, Flex_Cycle_Count=5, Flex_Section_Diameter=-20, Top_Tension=100, Bottom_Tension=100, pos=[-24.722,-55.7553,0], isSelected=True)
			elif index==22: #Prism
				rt.Prism(side1Length=14.1038, side2Length=14.8447, side3Length=16.3529, height=22.8732, pos=[-13.7066,-71.6249,0], isSelected=True)


		#convert to the type selected in cmb000
		if type_ in ['Editable Poly', 'Polygons']: #Polygons
			rt.convertTo(node, rt.PolyMeshObject)

		elif type_=='NURBS': #NURBS
			rt.convertTo(node, rt.NURBSSurf)

		elif type_=='Editable Mesh': #Mesh
			rt.convertTo(node, rt.TriMeshGeometry)

		elif type_=='Editable Patch': #Patch
			rt.convertTo(node, rt.Editable_Patch)
		
		# lights
		elif type_=='Light': #Lights
			
			#
			if index==0:
				pass
			elif index==1:
				pass


		#set name
		if isinstance(node, (str,unicode)): #is type of:
			self.create.txt003.setText(node)
		else:
			self.create.txt003.setText(node.name)

		self.history.extend(node) #save current node to history
		self.rotation['last']=[] #reset rotation history

		#translate the newly created node
		node.pos = rt.point3(self.point[0], self.point[1], self.point[2])
		#rotate
		self.rotateAbsolute(axis, node)

		self.constructAttributesForNode(node)

		# if self.create.cmb000.currentIndex() == 0: #if create type: polygon; convert to editable poly
		# 	rt.convertTo(node, rt.PolyMeshObject) #convert after adding primitive attributes to spinboxes

		rt.select(node) #select the transform node so that you can see any edits
		rt.redrawViews()


	def createPrimitive(self, catagory1, catagory2):
		'''
		ie. createPrimitive('Polygons', 'Cube')
		args:
			catagory1 (str) = type
			catagory2 (str) = type
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


