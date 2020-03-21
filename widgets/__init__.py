# from importlib import import_module

# import os


# #import package modules
# modules = [os.path.splitext(i)[0] for i in os.listdir(os.path.dirname(__file__)) if i.endswith('.py')]

# if __name__=='__main__':
# 	__package__ = 'widgets'
# __all__ = [
# 	import_module('.{0}'.format(m), package=__package__) # import_module('.%s' % f, __package__)
# 	for m in modules
# 	if m is not '__init__'
# ]

# del import_module