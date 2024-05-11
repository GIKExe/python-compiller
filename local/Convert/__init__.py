from .. import Type
from .. import getType

def hexToInt(text: Type.STR) -> Type.INT:
	return int(text[2:], 16)

def bitToInt(text: Type.BIT) -> Type.INT:
	return int(text[1:], 1)

def autoToInt(text: str) -> Type.INT:
	t = getType(text)
	if t is Type.HEX:
		text = hexToInt(text)
	elif t is Type.BIT:
		text = bitToInt(text)
	return (text, t)