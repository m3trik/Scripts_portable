try: import timeit, maya.mel as mel, pymel.core as pm;
except ImportError as error: print error
try: tk_scrollFieldReporter = pm.melGlobals['tk_scrollFieldReporter']; pm.scrollFieldReporter (tk_scrollFieldReporter, edit=1, clear=1)
except: pass


# from tk_slots_maya_init import Init as func
from tk_slots_ import Slot



class Test001(Slot):
	def __init__(self, *args, **kwargs):
		super(Test001, self).__init__(*args, **kwargs)


''' Start Code '''












# from random import triangular as tri


# r = tri(0,10,5)#(low,high,mode)

# xyz=[(0, 0, 0), (5, -r, 0), (10, r, 0), (15, -r, 0)]


# c = pm.curve (point=xyz, periodic=1)
# curve2 = pm.curve( pw=[(1, 0, 0, 5), (3, 5, 6, 5), (5, 6, 7, 5), (9, 9, 9, 5)] )
# print c
# pm.delete ("pCube1")

# import sys
# modules = [m for m in sys.modules.keys() if 'tk' in m]
# for module in modules:
# 	__import__(module); reload(m)

# print [m for m in locals() if 'tk' in m]
# # for module in modules:
# # 	reload()
# reload(tk_slots_)

# module = 'tk_slots_maya_edit'
# __import__(module)
# module = 'tk_slots_'
# if module not in locals() or module not in globals(): 
# 	print __import__(module), "8"
# else:
# 	print reload(module), "0"

# pm.curve( p=[(0, 0, 0), (0, -r, 5), (0, r, 10), (0, -r, 15)], k=[0,0,0,0,0,0] )


# import reimport
# for module in reimport.modified():
# 	print 'reimport', module
# 	reimport.reimport(module)


# def try_(expressions, exceptions='pass', showError_=True, *args, **kwargs):
# 	#args: expressions='string' - expression separated by ';'
# 	#			exceptions='string' - separated by ';'
# 	#			showError_=bool - hide or show any errors
# 	#returns: True if no errors occured, else: False
# 	#ex. try_('pm.ls(selection=1, objectsOnly=1)[0]', 'print "# Warning: Nothing selected #"')
# 	didCodeExecWithoutError=True
# 	for key,value in kwargs.iteritems(): #create variables for any kwargs passed in
# 		# exec('%s=%s' % (key,value))
# 		locals()[key]=value
# 	for expression in expressions.split(';'): #split string arg at ';'
# 		try:
# 			# print expression
# 			exec (expression.lstrip(" ")) #strip any leading whitespace
# 		except Exception as err:
# 			didCodeExecWithoutError=False #if any errors occur return False
# 			if showError_:
# 				print "# Error in try_(): "+str(err)+" #"
# 			exec (exceptions)
# 	return didCodeExecWithoutError
# # import tk_slots_
# # reload (tk_slots_)

# radialArrayObjList = ['pPlane1', 'pCone1_ins1', 'pCone1_ins2']
# # args = radialArrayObjList
# print try_ ('print args,kwargs;pm.delete(arg)', arg=radialArrayObjList)















# componentMode = pm.selectMode (query=1, component=1)
# if not componentMode:
# 	pm.selectMode (component=True)

# maskVertex = pm.selectType (query=True, vertex=True)
# maskEdge = pm.selectType (query=True, edge=True)
# maskFacet = pm.selectType (query=True, facet=True)


# #c++ embed window
# QWindow *window = QWindow::fromWinId(211812356)
# window>setFlags(Qt::FramelessWindowHint)

# QWidget *widget = QWidget::createWindowContainer(window)

# QVBoxLayout *layout = new QVBoxLayout(this)
# layout>addWidget(widget)
# this>setLayout(layout)

# from PySide2 import QtCore, QtWidgets

# groupBox = QtWidgets.QGroupBox("")
# radio1 = QtWidgets.QRadioButton("It's blue")
# radio2 = QtWidgets.QRadioButton("It isn't")
# radio1.setChecked(True)
# vbox = QtWidgets.QVBoxLayout()
# vbox.addWidget(radio1)
# vbox.addWidget(radio2)
# vbox.addStretch(1)
# groupBox.setLayout(vbox)
# # groupBox.setStyleSheet("QGroupBox { background-color: rgb(40, 40, 255); color: rgb(222, 222, 222)}")
# groupBox.setStyle(QtWidgets.QStyleFactory.create("plastique"))
# groupBox.show()

# vray = ['vrayformaya.mll','vrayformayapatch.mll']
# if pm.pluginInfo ('vrayformaya.mll', query=1, loaded=1):
#     pm.unloadPlugin (vray)
# else:
#     pm.loadPlugin (vray)
	 

# print pm.pluginInfo ('vrayformaya.mll', loaded=1)

# from PySide2 import QtGui, QtCore, QtWidgets
# import sys, os

# # subclass
# class CheckableComboBox(QtWidgets.QComboBox):
#     # once there is a checkState set, it is rendered
#     # here we assume default Unchecked
#     def addItem(self, item):
#         super(CheckableComboBox, self).addItem(item)
#         item = self.model().item(self.count()-1,0)
#         item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
#         item.setCheckState(QtCore.Qt.Unchecked)

#     def itemChecked(self, index):
#         item = self.model().item(i,0)
#         return item.checkState() == QtCore.Qt.Checked

# # the basic main()
# app = QtWidgets.QApplication(sys.argv)
# dialog = QtWidgets.QMainWindow()
# mainWidget = QtWidgets.QWidget()
# dialog.setCentralWidget(mainWidget)
# ComboBox = CheckableComboBox(mainWidget)
# for i in range(6):
#     ComboBox.addItem("Combobox Item " + str(i))

# import math
# trackSelectionOrder = pm.selectPref (query=1, trackSelectionOrder=1)
# componentMode = pm.selectMode (query=1, component=1)
# maskVertex = pm.selectType (query=1, vertex=1)
# components = pm.ls(selection=1, flatten=1)
# print components
# object_ = "pPlane2"#"VRayLightRect1"#pm.ls(selection=1, tail=1)[0]#"VRayLightRect1"#"pCube13"#

# object_ = pm.ls(selection=1, flatten=1)
# print object_
# # object_ = "pPlane"#"VRayLightRect1"#pm.ls(selection=1, tail=1)[0]#"VRayLightRect1"#"pCube13"#
# components = ["pCylinder1.vtx[8]", "pCylinder1.vtx[9]", "pCylinder1.vtx[10]"]

# # if all ([componentMode, maskVertex, len(components)>0]):
# if len(components)>0:
#     num=0
#     pm.undoInfo (openChunk=1)
#     for component in components:
#         if ".vtx" in str(component):
#             x = pm.polyNormalPerVertex (component, query=1, x=1)
#             y = pm.polyNormalPerVertex (component, query=1, y=1)
#             z = pm.polyNormalPerVertex (component, query=1, z=1)
#             xyz = [sum(x) / float(len(x)), sum(y) / float(len(y)), sum(z) / float(len(z))] #get average
#         elif ".e" in str(component):
#             componentName = str(component).split(".")[0]
#             vertices = pm.polyInfo (component, edgeToVertex=1)[0]
#             vertices = vertices.split()
#             vertices = [componentName+".vtx["+vertices[2]+"]",componentName+".vtx["+vertices[3]+"]"]
#             x=y=z=[]
#             for vertex in vertices:
#                 x_ = pm.polyNormalPerVertex (vertex, query=1, x=1)
#                 x.append(sum(x_) / float(len(x_)))
#                 y_ = pm.polyNormalPerVertex (vertex, query=1, y=1)
#                 x.append(sum(y_) / float(len(y_)))
#                 z_ = pm.polyNormalPerVertex (vertex, query=1, z=1)
#                 x.append(sum(z_) / float(len(z_)))
#             xyz = [sum(x) / float(len(x)), sum(y) / float(len(y)), sum(z) / float(len(z))] #get average
#         else:# elif ".f" in str(component):
#             xyz = pm.polyInfo (component, faceNormals=1)
#             xyz = xyz[0].split()
#             xyz = [float(xyz[2]), float(xyz[3]), float(xyz[4])]    
#         # print xyz

#         normal = mel.eval("unit <<"+str(xyz[0])+", "+str(xyz[1])+", "+str(xyz[2])+">>;") #normalize value using MEL
#         # normal = [round(i-min(xyz)/(max(xyz)-min(xyz)),6) for i in xyz] #normalize and round value using python
#         # print "normal:",normal

#         constraint = pm.normalConstraint(component, object_,
#                                         # aimVector=[0,1,0],
#                                         aimVector=normal,
#                                         upVector=[0,1,0],
#                                         worldUpVector=[0,1,0],
#                                         worldUpType="vector") # "scene","object","objectrotation","vector","none"
#         pm.delete(constraint) #orient object_ then from_ constraint.

#         vertexPoint = pm.xform (component, query=1, translation=1) #average vertex points on destination to get component center.
#         x = vertexPoint [0::3]
#         y = vertexPoint [1::3]
#         z = vertexPoint [2::3]
#         vertexPoint = [round(sum(x) / float(len(x)),4), round(sum(y) / float(len(y)),4), round(sum(z) / float(len(z)),4)]
#         # print "vertexPoint:",vertexPoint

#         pm.xform (object_, translation=vertexPoint)#, rotation=normalTangent)#, worldSpace=1) #move the object_

#         if component != components[len(components)-1]: #if not at the end of the list, create a new instance of the object_.
#             name = str(object_)+"_inst"+str(num)
#             pm.instance (object_, name=name)
#         num+=1
#     pm.undoInfo (closeChunk=1)

# else:
#     print "# Warning: Component list empty. #"



#create vray light
# mel.eval("select -r `shadingNode -asLight VRayLightRectShape`;")



#backup
# components = pm.ls(selection=1, flatten=1)
# object_ = "pPlane1"#"VRayLightRect1"#pm.ls(selection=1, tail=1)[0]#"VRayLightRect1"#"pCube13"#
# # print object_

# # if all ([componentMode, maskVertex, len(components)>0]):
# if len(components)>0:
#     num=0
#     pm.undoInfo (openChunk=1)
#     for component in components:
#         if ".vtx" in str(component):
#             x = pm.polyNormalPerVertex (component, query=1, x=1)
#             y = pm.polyNormalPerVertex (component, query=1, y=1)
#             z = pm.polyNormalPerVertex (component, query=1, z=1)
#             xyz = [sum(x) / float(len(x)), sum(y) / float(len(y)), sum(z) / float(len(z))] #get average
#         elif ".f" in str(component):
#             xyz = pm.polyInfo (component, faceNormals=1)
#             xyz = xyz[0].split()
#             xyz = [float(xyz[2]), float(xyz[3]), float(xyz[4])]
#         elif ".e" in str(component):
#             componentName = str(component).split(".")[0]
#             vertices = pm.polyInfo (component, edgeToVertex=1)[0]
#             vertices = vertices.split()
#             vertices = [componentName+".vtx["+vertices[2]+"]",componentName+".vtx["+vertices[3]+"]"]
#             x=y=z=[]
#             for vertex in vertices:
#                 x_ = pm.polyNormalPerVertex (vertex, query=1, x=1)
#                 x.append(sum(x_) / float(len(x_)))
#                 y_ = pm.polyNormalPerVertex (vertex, query=1, y=1)
#                 x.append(sum(y_) / float(len(y_)))
#                 z_ = pm.polyNormalPerVertex (vertex, query=1, z=1)
#                 x.append(sum(z_) / float(len(z_)))
#             xyz = [sum(x) / float(len(x)), sum(y) / float(len(y)), sum(z) / float(len(z))] #get average
#             print xyz

#         normal = mel.eval("unit <<"+str(xyz[0])+", "+str(xyz[1])+", "+str(xyz[2])+">>;") #normalize value
#         # normal = [round(float(i)/max(normal),2) for i in normal] #normalize value
#         # normal = [round((i)/sum(normal),2) for i in normal] #normalize value
#         # normal = [round(i-min(xyz)/(max(xyz)-min(xyz)),2) for i in xyz] #normalize value
#         print "normal:",normal

#         constraint = pm.normalConstraint(component, object_,
			
#                                         # aimVector=[0,1,0],
#                                         aimVector=normal,
#                                         upVector=[0,1,0],
#                                         # upVector=normal,

#                                         worldUpVector=[0,1,0],
#                                         worldUpType="vector"
#                                         ) # "scene","object","objectrotation","vector","none"
#         pm.delete(constraint) #orient object_ then from_ constraint.

#         vertexPoint = pm.xform (component, query=1, translation=1) #average vertex points on destination to get component center.
#         x = vertexPoint [0::3]
#         y = vertexPoint [1::3]
#         z = vertexPoint [2::3]
#         vertexPoint = [round(sum(x) / float(len(x)),4), round(sum(y) / float(len(y)),4), round(sum(z) / float(len(z)),4)]
#         print "vertexPoint:",vertexPoint

#         pm.xform (object_, translation=vertexPoint)#, rotation=normalTangent)#, worldSpace=1) #move the object_

#         name = str(object_)+"_inst"+str(num) #if not at the end of the list, create a new instance of the object_.
#         if component != components[len(components)-1]:
#             pm.instance (object_, name=name)
			
#         num+=1
#     pm.undoInfo (closeChunk=1)

# else:
#     print "# Warning: No components selected to align to. #"



# print pm.sets (set_, query=1, text=1)


# indexDict = {'selection': 'i020', 'scene': 'i018', 'rendering': 'i016', 'nurbs': 'i013', 'polygons': 'i014', 'preferences': 'i015', 'rigging': 'i017', 'create': 'i002', 'cameras': 'i001', 'transform': 'i022', 'init': 'i009', 'animation': 'i000', 'main': 'i011', 'fx': 'i005', 'i021': 'i007', 'i020': 'i006', 'i023': 'i008', 'lighting': 'i010', 'viewport': 'i024', 'edit': 'i004', 'uv': 'i023', 'texturing': 'i021', 'normals': 'i012', 'display': 'i003', 'scripting': 'i019'}


# # classDict {'selection': <class 'tk_maya_buttons.Selection'>, 'scene': <class 'tk_maya_buttons.Scene'>, 'rendering': <class 'tk_maya_buttons.Rendering'>, 'nurbs': <class 'tk_maya_buttons.Nurbs'>, 'polygons': <class 'tk_maya_buttons.Polygons'>, 'preferences': <class 'tk_maya_buttons.Preferences'>, 'rigging': <class 'tk_maya_buttons.Rigging'>, 'create': <class 'tk_maya_buttons.Create'>, 'cameras': <class 'tk_maya_buttons.Cameras'>, 'transform': <class 'tk_maya_buttons.Transform'>, 'animation': <class 'tk_maya_buttons.Animation'>, 'main': <class 'tk_maya_buttons.Main'>, 'fx': <class 'tk_maya_buttons.Fx'>, 'i021': <class 'tk_maya_buttons.I021'>, 'i020': <class 'tk_maya_buttons.I020'>, 'i023': <class 'tk_maya_buttons.I023'>, 'lighting': <class 'tk_maya_buttons.Lighting'>, 'viewport': <class 'tk_maya_buttons.Viewport'>, 'edit': <class 'tk_maya_buttons.Edit'>, 'uv': <class 'tk_maya_buttons.Uv'>, 'texturing': <class 'tk_maya_buttons.Texturing'>, 'normals': <class 'tk_maya_buttons.Normals'>, 'display': <class 'tk_maya_buttons.Display'>, 'scripting': <class 'tk_maya_buttons.Scripting'>}
# uiList = ['animation', 'cameras', 'create', 'display', 'edit', 'fx', 'i020', 'i021', 'i023', 'init', 'lighting', 'main', 'normals', 'nurbs', 'polygons', 'preferences', 'rendering', 'rigging', 'scene', 'scripting', 'selection', 'texturing', 'transform', 'uv', 'viewport']
# # uiSizeDict {'selection': [295, 234], 'scene': [203, 254], 'rendering': [195, 177], 'nurbs': [222, 320], 'polygons': [243, 418], 'preferences': [120, 234], 'rigging': [195, 203], 'create': [152, 330], 'cameras': [98, 188], 'transform': [259, 271], 'init': [300, 225], 'animation': [132, 200], 'main': [300, 225], 'fx': [195, 203], 'i021': [120, 289], 'i020': [120, 289], 'i023': [120, 289], 'lighting': [120, 289], 'viewport': [300, 225], 'edit': [252, 418], 'uv': [226, 244], 'texturing': [226, 222], 'normals': [245, 196], 'display': [237, 254], 'scripting': [412, 274]}
# # buttonDict {'init': {}, 'main': {'i007': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDFC8>, 'i006': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CF1C8>, 'i005': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CF108>, 'i004': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CD708>, 'i003': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CD848>, 'i011': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CF188>, 'i012': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CF2C8>, 'i013': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDF48>, 'i018': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDC08>, 'i021': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDB48>, 'i016': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CD948>, 'i009': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDCC8>, 'i008': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDB08>, 'i020': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CF208>, 'i017': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CD7C8>, 'i023': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CD988>, 'i014': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDA48>, 'i022': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CF088>, 'i019': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDD48>, 'v004': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CD9C8>, 'v005': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CF048>, 'v002': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDA88>, 'v003': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDC48>, 'v000': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CD748>, 'v001': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDB88>, 'i015': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDE48>, 'i024': <PySide2.QtWidgets.QPushButton object at 0x000002BCC01CDEC8>}}


# # # connectionDict {'main': {<PySide2.QtCore.SignalInstance object at 0x000002119FA9AC00>: <bound method Main.v003 of <tk_maya_buttons.Main object at 0x00000211B590A9B0>>, <PySide2.QtCore.SignalInstance object at 0x000002119FA9AC18>: <function <lambda> at 0x00000211B5911978>}}
# # # connectionDict {'main': {<PySide2.QtCore.SignalInstance object at 0x000002087D9DBC00>: <bound method Main.v003 of <tk_maya_buttons.Main object at 0x0000020814D86320>>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBC18>: <function <lambda> at 0x0000020814D889E8>, <PySide2.QtCore.SignalInstance object at 0x000002087E614EB8>: <function <lambda> at 0x0000020815343128>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBC48>: <function <lambda> at 0x0000020814D88828>, <PySide2.QtCore.SignalInstance object at 0x000002087E614F60>: <bound method Main.v002 of <tk_maya_buttons.Main object at 0x0000020814D86320>>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBC90>: <function <lambda> at 0x0000020814D88DD8>, <PySide2.QtCore.SignalInstance object at 0x000002087E614CC0>: <function <lambda> at 0x0000020814D88F98>, <PySide2.QtCore.SignalInstance object at 0x000002087E614900>: <function <lambda> at 0x00000208153430B8>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBD80>: <function <lambda> at 0x0000020814D88AC8>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBDE0>: <function <lambda> at 0x0000020814D88BA8>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBE58>: <bound method Main.v001 of <tk_maya_buttons.Main object at 0x0000020814D86320>>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBE28>: <function <lambda> at 0x0000020814D88908>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBA50>: <function <lambda> at 0x0000020814D88978>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBE70>: <function <lambda> at 0x0000020814D88F28>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBE88>: <function <lambda> at 0x0000020814D88C88>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBA98>: <function <lambda> at 0x0000020814D88CF8>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBEA0>: <function <lambda> at 0x0000020814D88D68>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBEB8>: <function <lambda> at 0x0000020814D88E48>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBAC8>: <function <lambda> at 0x0000020814D88EB8>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBAE0>: <function <lambda> at 0x0000020814D88C18>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBB10>: <function <lambda> at 0x0000020814D887B8>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBF30>: <function <lambda> at 0x0000020814D88A58>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBF60>: <bound method Main.v000 of <tk_maya_buttons.Main object at 0x0000020814D86320>>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBB70>: <bound method Main.v004 of <tk_maya_buttons.Main object at 0x0000020814D86320>>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBFA8>: <function <lambda> at 0x0000020814D88898>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBFC0>: <bound method Main.v005 of <tk_maya_buttons.Main object at 0x0000020814D86320>>, <PySide2.QtCore.SignalInstance object at 0x000002087D9DBBD0>: <function <lambda> at 0x0000020814D88B38>, <PySide2.QtCore.SignalInstance object at 0x000002087E6147E0>: <function <lambda> at 0x0000020815343048>}}
# # indexDict1 = {name:'i000'[:-len(str(uiList.index(name)))]+str(uiList.index(name)) for name in uiList}
# indexDict1 = {'i000'[:-len(str(num))]+str(num):name for num,name in enumerate(uiList)}
# indexDict2 = {name:'i000'[:-len(str(num))]+str(num) for num,name in enumerate(uiList)}
# print indexDict1
# print indexDict2

# uiList = "uiList = ['animation', 'cameras', 'create', 'display', 'edit', 'fx', 'i020', 'i021', 'i023', 'init', 'lighting', 'main', 'normals', 'nurbs', 'polygons', 'preferences', 'rendering', 'rigging', 'scene', 'scripting', 'selection', 'texturing', 'transform', 'uv', 'viewport'];"
# # dict1 = "{name:'i000'[:-len(str(uiList.index(name)))]+str(uiList.index(name)) for name in uiList}"
# # dict2 = "{name:'i000'[:-len(str(num))]+str(num) for num,name in enumerate(uiList)}"
# # print min(timeit.Timer(uiList+dict1).repeat(7, 1000))
# # print min(timeit.Timer(uiList+dict2).repeat(7, 1000))





#create error:
#line 263
#pm.select(str(self.history[-1][0])) #make sure the transform node is selected so that you can see any edits




# func = locate('tk_maya_shared_functions')

# print '-'*20
# # print func.cycle('componentID_01234')
# # print func.cycle('componentID_01234')
# # print func.cycle('componentID_01234')
# # print func.cycle('componentID_01234')
# print 'query', func.cycle('componentID_1234', query=1)
# print 'query', func.cycle('componentID_1234', query=1)
# print func.cycle('componentID_01234')
# print func.cycle('componentID_01234')
# print '-'*20

# # 0
# # 1
# # 2
# # 3
# # 4
# # 4
# # 4
# # 0



#fix init widgets lambda


# obj = pm.ls (sl=1)
# currentScale = pm.xform (obj, query=1, scale=1)
# pm.makeIdentity (obj, scale=1)