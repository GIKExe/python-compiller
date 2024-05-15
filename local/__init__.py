import os



# from . import Type
# from . import Size


# def getType(text: str) -> Type:
# 	if text.startswith('0x'):
# 		for s in text[2:]:
# 			if s.upper() not in '0123456789ABCDEF': break
# 		else:
# 			return Type.HEX

# 	if text.startswith('b'):
# 		for s in text[1:]:
# 			if s.upper() not in '01': break
# 		else:
# 			return Type.BIT

# 	if text.count('.') == 1:
# 		for s in text.replace('.', ''):
# 			if s not in '0123456789': break
# 		else:
# 			return Type.FLT
# 	return Type.STR


# class Bytes:
# 	def fromHex(text: Type.HEX) -> list:
# 		text = text[2:]
# 		if len(text) % 2 != 0:
# 			text = '0' + text
# 		return [int(text[i:i+2], 16) for i in range(0, len(text), 2)][::-1]
	
# 	def fromStr(text: Type.STR) -> list:
# 		return [ord(s) for s in text]
	
# 	def fromInt(text: Type.INT, length: int, signed: bool) -> list:
# 		value = int(text)
# 		return [i for i in int.to_bytes(value, length=length, byteorder='little', signed=signed)]
	

# class Line(list):
# 	def __init__(self, index, *args, **kwargs):
# 		super().__init__(*args, **kwargs)
# 		self.index = index
# 		self.counter = 0

# 	def get(self) -> str:
# 		if len(self) == 0: error(f'{self.index}: строка неожиданно закончилась')
# 		self.counter += 1
# 		return self.pop(0)
	


class BIT: ...
class INT: ...
class HEX: ...
class STR: ...
class FLT: ...

class String(str):
	def sw(self, *a, **b):
		return self.startswith(*a, **b)
	
	def ew(self, *a, **b):
		return self.startswith(*a, **b)
	
	def only(self, symbols):
		for s in self:
			if s not in symbols: return False
		return True


_type = type
def type(text):
	text = String(text)

	if text.sw('b') and text.only('01'):
		return BIT
	if text.sw('0x') and text.only('0123456789ABCDEF'):
		return HEX
	

def parser(text):
	class d:
		slash = False
		string = False
		byte = False

	out = []
	line = [[""]]

	for s in text:
		if d.slash:
			if s == 'n':
				line[-1][-1] += '\n'
			elif s == 't':
				line[-1][-1] += '\t'
			elif s == '"':
				line[-1][-1] += '"'
			elif s == "'":
				line[-1][-1] += "'"
			else:
				raise Exception("недопустимый символ после слеша в строке: "+s)
			d.slash = False

		elif d.string:
			if s == '\\':
				d.slash = True
				continue
			elif s == '"':
				d.string = False
			line[-1][-1] += s

		else:
			if s == '"':
				d.string = True
			elif s == '\n':
				out.append(line)
				line = [[""]]
				continue
			elif s == ';':
				line.append([''])
				continue
			elif s == ' ':
				line[-1].append('')
				continue
			line[-1][-1] += s

	return out


if __name__ == "__main__":
	with open(R'C:\Users\GIKExe\Desktop\python-compiller\test.txt', 'r', encoding="UTF8") as file:
		text = file.read()
	
	out = parser(text)
	for line in out:
		print(line)