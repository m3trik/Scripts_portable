import pymel.core as pm

# Close ports if they were already open under another configuration
try:
    pm.commandPort(name=":7001", close=True)
except:
    pm.warning('Could not close port 7001 (maybe it is not opened yet...)')
try:
    pm.commandPort(name=":7002", close=True)
except:
    pm.warning('Could not close port 7002 (maybe it is not opened yet...)')

# Open new ports
pm.commandPort(name=":7001", sourceType="mel")
pm.commandPort(name=":7002", sourceType="python")