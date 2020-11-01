# from importlib import import_module
# import os


# modules = [os.path.splitext(i)[0] for i in os.listdir(os.path.dirname(__file__)) if i.endswith('.py')]

# __all__ = [
# 	import_module('.{0}'.format(m), package=__package__)
# 	for m in modules
# 	if m is not '__init__'
# ]

# del import_module