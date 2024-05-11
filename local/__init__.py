
from . import Type
from . import Size

def getType(text: str) -> Type:
	if text.startswith('0x'):
		for s in text[2:]:
			if s.upper() not in '0123456789ABCDEF': break
		else:
			return Type.HEX

	if text.startswith('b'):
		for s in text[1:]:
			if s.upper() not in '01': break
		else:
			return Type.BIT

	if text.count('.') == 1:
		for s in text.replace('.', ''):
			if s not in '0123456789': break
		else:
			return Type.FLT
	return Type.STR


class Bytes:
	def fromHex(text: Type.HEX) -> list:
		text = text[2:]
		if len(text) % 2 != 0:
			text = '0' + text
		return [int(text[i:i+2], 16) for i in range(0, len(text), 2)][::-1]
	
	def fromStr(text: Type.STR) -> list:
		return [ord(s) for s in text]
	
	def fromInt(text: Type.INT, length: int, signed: bool) -> list:
		value = int(text)
		return [i for i in int.to_bytes(value, length=length, byteorder='little', signed=signed)]
	

if __name__ == "__main__":
	x = Bytes.fromInt(251 + 256, 2, True)
	print(x)