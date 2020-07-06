from __future__ import print_function
from tk_slots_max_init import *

import os.path



class Pivot(Init):
	def __init__(self, *args, **kwargs):
		super(Pivot, self).__init__(*args, **kwargs)

		self.parentUi = self.sb.getUi('pivot')
		self.childUi = self.sb.getUi('pivot_submenu')


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

		if index=='setMenu':
			list_ = ['']
			items = cmb.addItems_(list_, '')
			return

		# if index>0:
		# 	if index==cmb.items.index(''):
		# 		pass
		# 	cmb.setCurrentIndex(0)


	def cmb001(self, index=None):
		'''
		Center Pivot
		'''
		cmb = self.parentUi.cmb001

		if index=='setMenu':
			list_ = ['Component', 'Object', 'World', 'Object Top', 'Object Bottom', 'Object Center Left', 
				'Object Center Right', 'Object Bottom Left', 'Object Bottom Right', 'Object Top Left', 'Object Top Right']
			cmb.addItems_(list_, 'Center Pivot')
			return

		if index>0:
			if index==cmb.items.index('Component'):
				rt.CenterPivot(rt.selection) #Same as Hierarchy/Pivot/Affect Pivot Only - Center to Object.
			if index==cmb.items.index('Object'):
				self.centerPivot(rt.selection)
			if index==cmb.items.index('World'):
				rt.selection.pivot = [0,0,0] #center pivot world 0,0,0
			if index==cmb.items.index('Object Top'):
				[setattr(obj, 'pivot', [obj.position.x, obj.position.y, obj.max.z]) for obj in rt.selection] #Move the pivot to the top of the object
			if index==cmb.items.index('Object Bottom'):
				[setattr(obj, 'pivot', [obj.position.x, obj.position.y, obj.min.z]) for obj in rt.selection] #Move the pivot to the bottom of the object
			if index==cmb.items.index('Object Center Left'):
				[setattr(obj, 'pivot', [obj.min.x, obj.position.y, obj.position.z]) for obj in rt.selection] #Move the pivot to the Center left of the object
			if index==cmb.items.index('Object Center Right'):
				[setattr(obj, 'pivot', [obj.max.x, obj.position.y, obj.position.z]) for obj in rt.selection] #Move the pivot to the Center right of the object
			if index==cmb.items.index('Object Bottom Left'):
				[setattr(obj, 'pivot', [obj.min.x, obj.position.y, obj.min.z]) for obj in rt.selection] #Move the pivot to the Bottom left of the object
			if index==cmb.items.index('Object Bottom Right'):
				[setattr(obj, 'pivot', [obj.max.x, obj.position.y, obj.min.z]) for obj in rt.selection] #Move the pivot to the Bottom right of the object
			if index==cmb.items.index('Object Top Left'):
				[setattr(obj, 'pivot', [obj.min.x, obj.position.y, obj.max.z]) for obj in rt.selection] #Move the pivot to the Top left of the object
			if index==cmb.items.index('Object Top Right'):
				[setattr(obj, 'pivot', [obj.max.x, obj.position.y, obj.max.z]) for obj in rt.selection] #Move the pivot to the Topright of the object
			cmb.setCurrentIndex(0)


	@Slots.message
	def tb000(self, state=None):
		'''
		Reset Pivot
		'''
		tb = self.currentUi.tb000
		if not tb.containsMenuItems:
			tb.add('QCheckBox', setText='Reset Pivot Scale', setObjectName='chk000', setChecked=True, setToolTip='')
			tb.add('QCheckBox', setText='Reset Pivot Transform', setObjectName='chk001', setChecked=True, setToolTip='')
			tb.add('QCheckBox', setText='Reset XForm', setObjectName='chk002', setToolTip='')
			if state=='setMenu':
				return

		if tb.chk000: #Reset Pivot Scale
			rt.ResetScale(rt.selection) #Same as Hierarchy/Pivot/Reset Scale.
		
		if tb.chk001: #Reset Pivot Transform
			rt.ResetTransform(rt.selection) #Same as Hierarchy/Pivot/Reset Transform.

		if tb.chk002: #reset XForm
			rt.ResetXForm(rt.selection) #Same as the Reset XForm utility in the Utilities tab - applies XForm modifier to node, stores the current transformations in the gizmo and resets the object transformations.
			return 'Result: ResetXForm '+str([obj.name for obj in rt.selection])

		# rt.ResetPivot(rt.selection) #Same as Hierarchy/Pivot/Reset Pivot.


	def b000(self):
		'''
		Center Pivot: Object
		'''
		self.cmb001(index=2)


	def b001(self):
		'''
		Center Pivot: Component
		'''
		self.cmb001(index=1)


	def b002(self):
		'''
		Center Pivot: World
		'''
		self.cmb001(index=3)


	def b003(self):
		'''
		Center Pivot: Bounding Box
		'''
		self.cmb001(index=4)


	def b004(self):
		'''
		Bake Pivot
		'''
		print ('no function')


	@staticmethod
	def centerPivot(objects):
		'''
		Center the rotation pivot on the given objects.
		'''
		for obj in objects:
			rt.toolMode.coordsys(obj) #Center Pivot Object
			obj.pivot = obj.center





	





#module name
print(os.path.splitext(os.path.basename(__file__))[0])
# -----------------------------------------------
# Notes
# -----------------------------------------------

# maxEval('max tti')

# maxEval('macros.run \"PolyTools\" \"TransformTools\")

