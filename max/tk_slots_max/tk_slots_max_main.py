import MaxPlus; maxEval = MaxPlus.Core.EvalMAXScript
from pymxs import runtime as rt

import os.path


from tk_slots_max_init import Init





class Main(Init):
	def __init__(self, *args, **kwargs):
		super(Main, self).__init__(*args, **kwargs)



	def v000(self): #Extrude
		self.hotBox.sb.getMethod('polygons','b006')
		print "# Result: perform extrude #"

	def v001(self): #Bridge
		self.hotBox.sb.getMethod('polygons','b005')
		print "# Result: bridge #"

	def v002(self): #Multi-cut tool
		self.hotBox.sb.getMethod('polygons','b012')
		print "# Result: multi-cut #"

	def v003(self): #Delete history
		self.hotBox.sb.getMethod('edit','b016')
		print "# Result: delete history #"

	def v004(self): #Delete
		self.hotBox.sb.getMethod('edit','b032')
		print "# Result: delete #"

	def v005(self): #
		pass

	def v006(self): #Toggle mode
		self.cycle('shortCutMode_01234')

	def v007(self): #Minimize main application
		mel.eval("minimizeApp;")
		self.hotBox.hbHide()


	def cmb000(self): #Display
		cmb = self.hotBox.ui.cmb000
		index = cmb.currentIndex() #get current index before refreshing list
		list_ = [
		'Toggle visibility', 
		'Hide Selected',
		'Show Selected',
		'Show Geometry',
		'XRay Selected',
		'Un-XRay All',
		'XRay Other',
		'Filter Objects',
		'Toggle Component ID Display',
		'Wireframe Non-Active',
		'Template selected',
		]
		self.comboBox (cmb, list_, "Display")

		if index!=0:
			if index==1: #Toggle visibility
				sel = [s for s in rt.getCurrentSelection()]

				for obj in sel:
					if obj.visibility == True:
						obj.visibility = False
					else:
						obj.visibility = True

			if index==2: #Hide Selected
				sel = [s for s in rt.getCurrentSelection()]
	
				for obj in sel:
					if not obj.isHiddenInVpt:
						obj.isHidden = True

			if index==3: #Show selected
				sel = [s for s in rt.getCurrentSelection()]
	
				for obj in sel:
					if obj.isHiddenInVpt:
						obj.isHidden = False

			if index==4: #Show Geometry
				geometry = rt.geometry

				for obj in geometry:
					if obj.isHiddenInVpt:
						obj.isHidden = False

			if index==5: #Xray selected
				sel = [s for s in rt.getCurrentSelection()]

				for s in sel:
					s.xray = True

			if index==6: #Un-Xray all
				geometry = [g for g in rt.geometry]

				for g in geometry:
					g.xray = False

			if index==7: #Xray other
				sel = [s for s in rt.getCurrentSelection()]

				geometry = [g for g in rt.geometry]

				for g in geometry:
					if g not in sel:
						g.xray = True

			if index==8: #Filter objects
				pass

			if index==9: #toggle component ID display
				index = self.cycle('componentID_01234')

				visible = pm.polyOptions (query=1, displayItemNumbers=1)
				dinArray = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]

				if index == 4:
					i=0
					for _ in range(4):
						if visible[i] == True:
							pm.polyOptions (relative=1, displayItemNumbers=dinArray[i], activeObjects=1)
						i+=1

				if visible[index] != True and index != 4:
					pm.polyOptions (relative=1, displayItemNumbers=dinArray[index], activeObjects=1)

					i=0
					for _ in range(4):
						if visible[i] == True and i != index:
							pm.polyOptions (relative=1, displayItemNumbers=dinArray[i], activeObjects=1)
						i+=1

				if index == 0:
					self.viewPortMessage("[1,0,0,0] <hl>vertIDs</hl>.")
				if index == 1:
					self.viewPortMessage("[0,1,0,0] <hl>edgeIDs</hl>.")
				if index == 2:
					self.viewPortMessage("[0,0,1,0] <hl>faceIDs</hl>.")
				if index == 3:
					self.viewPortMessage("[0,0,0,1] <hl>compIDs(UV)</hl>.")
				if index == 4:
					self.viewPortMessage("component ID <hl>Off</hl>.")

			if index==10: #wireframe non active (wireframe all but the selected item)
				viewport = rt.viewport.activeViewport

				state = self.cycle('wireframeInactive_01')

				if state:
					if not rt.viewport.isWire():
						self.maxUiSetChecked("415", 62, 163, True) #set viewport to wireframe
					self.maxUiSetChecked("40212", 62, 130, True) #Shade selected objects Checked
				else:
					self.maxUiSetChecked("40212", 62, 130, False) #Shade selected objects unchecked

			if index==11: #Template selected
				sel = [s for s in rt.getCurrentSelection()]

				for obj in sel:
					if obj.isFrozen == True:
						obj.isFrozen = False
					else:
						obj.isFrozen = True

			if index==12:
				pass

			if index==13:
				pass

			if index==14:
				pass

			if index==15:
				pass

			cmb.setCurrentIndex(0)



	def cmb001(self): #Recent Commands
		cmb = self.hotBox.ui.cmb001
		index = cmb.currentIndex() #get current index before refreshing list
		print self.hotBox.prevCommand
		list_ = [dict_.values() for dict_ in self.hotBox.prevCommand] #ie. get value 'muti-cut tool' form [{'b000':'multi-cut tool'}]
		print list_
		if not list_:
			return None
		# print self.hotBox.prevCommand 
		# print self.hotBox.prevCommand[index]
		self.comboBox (cmb, list_, "Recent")

		if index!=0:
			for key in self.hotBox.prevCommand[index]:
				key()
			cmb.setCurrentIndex(0)




#module name
print os.path.splitext(os.path.basename(__file__))[0]
# -----------------------------------------------
# Notes
# -----------------------------------------------




# component mode:vertex
# 		pm.selectMode (component=True)
# 		pm.selectType (subdivMeshPoint=1, polymeshVertex=True)
# 		self.viewPortMessage("<hl>vertex</hl> mask.")

# component mode:edge
# 		pm.selectMode (component=True)
# 		pm.selectType (subdivMeshEdge=1, polymeshEdge=True)
# 		self.viewPortMessage("<hl>edge</hl> mask.")

# component mode:facet
# 		pm.selectMode (component=True)
# 		pm.selectType (subdivMeshFace=1, polymeshFace=True)
# 		self.viewPortMessage("<hl>facet</hl> mask.")

# object mode
# 		pm.selectMode (object=True)
# 		self.viewPortMessage("<hl>object</hl> mode.")

# component mode:uv
# 		pm.selectMode (component=True)
# 		pm.selectType (subdivMeshUV=True, polymeshUV=True)
# 		self.viewPortMessage("<hl>UV</hl> mask.")