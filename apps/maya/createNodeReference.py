import maya.OpenMaya as om



# uses OpenMaya to create a neat little custom Python object that stores a reference to the Maya node, 
# regardless of the node’s name. Just get the object by name once, and as long as you keep that object in memory, 
# it doesn’t matter what the object name changes to; you’ll always have a pointer to it.


 
class MayaNode():
	'''
	
	'''
	def __init__(self, node_name):
		self._mobject = om.MObject()
		self._mdagpath = om.MDagPath()
		self._node = om.MFnDependencyNode()
		selection = om.MSelectionList()
		try:
			selection.add(node_name)
			selection.getDependNode(0, self._mobject)
			self._node = om.MFnDependencyNode(self._mobject)
			selection.getDagPath(0, self._mdagpath, om.MObject())
		except:
			pass
 
	def name(self, long=False):
		if self._mdagpath.isValid():
			if long:
				return self._mdagpath.fullPathName()
			return self._mdagpath.partialPathName()
		else:
			if not self._mobject.isNull():
				return self._node.name()
			return None









'''
First, the __init__ constructor for the object. We create default “empty” containers for an MObject, 
an MDagPath, an MFnDependencyNode, and an MSelectionList. The MObject is a sort of generic catch-all 
container for Maya API objects. A lot of functions will expect to write to an MObject. In C++, unlike 
Python, much of the time you’ll provide arguments to the function as variables to be overwritten; 
these are commonly marked with a “&” in the documentation. Functions like MSelectionList::getDependNode() 
have these “out” arguments, and expect you to provide an object of the correct type (in this case, an 
MObject) as an argument to be written to. The MDagPath object is a container that describes the 
DAG (Directed Acyclic Graph) path of an object in Maya; that is, the path in the Outliner, 
like |group1|polySphere1. We’ll use this to get the full name of DAG objects later on. 
Next is the MFnDependencyNode object. Any object in Maya that doesn’t show up in the Outliner is often 
referred to as a “Dependency Graph” or “DG” node… things like shaders, textures, etc. Since we want this 
MayaNode class to apply to any kind of node in the scene, we’re creating containers for both types just 
in case. Finally, the MSelectionList object, which is used to hold a list of objects… we’re just creating 
this so that we can use the handy getDependNode() and getDagPath() functions from that class.

Okay, deep breaths. Now that we’ve created these objects, we can actually try to turn them into something. 
First, we tell our MSelectionList object to add the node name that we want… this is the only time we’ll ever 
need to refer to this object by it’s “MEL-like” name. Once the list is populated with this one object, we 
can use its getDependNode() function to take the 0th index of our selection list (since there’s only ever 
one object in there) and return its MObject representation, binding it to self._mobject. This MObject isn’t 
specific enough, though, so we want to cast it as an MFnDependencyNode, which lets us use all the tasty 
functions associated with that class. We can do this by just using the constructor for MFnDependencyNode, 
passing that MObject handle as the argument, and we bind the result to self._node. Finally, we’re going to 
try to get an MDagPath instance, just in case this node is a DAG node, via the getDagPath() function. This 
is another of those weird functions that writes to an argument, so we pass it our MDagPath instance, 
self._mdagpath. The third argument there is just an empty placeholder; we don’t need it.

So now we have an MObject object, which can give us a convenient “pointer” to just about any object in Maya; 
a MFnDependencyNode object, which can get us some basic information about just about any node; and an MDagPath 
object, which we can use to get the DAG path of our node, just in case it’s a DAG node. Almost there!

Next is the name() function. We want this to return the name of the node, and optionally, the “long” name of 
the node (if it’s actually a DAG object, since only DAG objects have these long hierarchical names). We can 
tell if the MDagPath object we created actually is pointing to a real DAG node by using the MDagPath::isValid() 
function on the instance we stored as a class member earlier (self._mdagpath). If it is in fact a DAG object, 
we either return the full path or the short path, depending on the value of the long argument to the function. 
If it’s not, we do a last check to make sure that the object actually exists (by checking our MObject handle 
using the isValid() function), and then return the name of the MFnDependencyNode we stored for this object.

Now as long as this MayaObject instance we’ve created is resident in memory, it doesn’t matter what we name 
this object, or what we parent it to, or if there’s another object elsewhere with the same name… this MayaObject 
will always point to that object and return its current name anytime you call the name() function. This is 
incredibly useful!

That’s a long explanation for what should be a very simple little node, but there’s OpenMaya for you. Still, 
for those of you new to the API, little tools like this can go a long way with removing some of the restrictions 
and annoyances imposed by MEL (and the Python cmds module, since it’s just a wrapper around MEL). Take a look 
at the API docs for some of these object types… there’s a lot of other little conveniences you could build into 
this class if you’re so inclined.
'''