import maya.standalone

maya.standalone.initialize(name='python')

import tk_main
maya.standalone.uninitialize()
