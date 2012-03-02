all = {}

def handler(*types):
	def sub(func):
		module = func.__module__.split('.')[-1]
		if not module in all:
			all[module] = {}
		args = func.__code__.co_varnames[:func.__code__.co_argcount]
		all[module][func.func_name] = types, args, func
		return func
	return sub
