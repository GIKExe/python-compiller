

class String(str):
	from textwrap import wrap as __0z8y9jTL__wrap

	def __init__(self, *args, **kwargs):
		super().__init__()

	def __getitem__(self, key):
		return String(super().__getitem__(key))

	def wrap(self, *args, **kwargs):
		print(self, args, kwargs)
		return [String(i) for i in self.__0z8y9jTL__wrap(*args, **kwargs)]

	def split(self, *args, **kwargs):
		return [String(i) for i in super().split(*args, **kwargs)]

	def replace(self, *args, **kwargs):
		return String(super().replace(*args, **kwargs))

	def sw(self, *a, **b):
		return self.startswith(*a, **b)
	
	def ew(self, *a, **b):
		return self.startswith(*a, **b)
	
	def only(self, symbols):
		if len(self) == 0: return False
		for s in self:
			if s not in symbols: return False
		return True