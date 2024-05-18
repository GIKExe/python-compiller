import math


from ..utils import String
from .. import Type
from ..Type import BIN, BYTE, UINT, INT, HEX, STR, FLOAT


def getSize(block):
	type, text = block[0], block[1]

	if type == BIN:
		return math.ceil(len(text) / 8)

	elif type == BYTE:
		return 1

	elif type == HEX:
		return math.ceil(len(text) / 2)

	elif type == STR:
		return len(text)

	elif type == UINT:
		value = int(text)
		if value < 0:
			raise Exception('получено отрицательное число, но не подписанное')
		text = hex(value)[2:]
		return math.ceil(len(text) / 2)

	elif type == INT:
		value = int(text)
		text = bin(abs(value))[1:]
		size = math.ceil(len(text) / 8)
		if abs(value) <= 2*(size*8-1) - (0 if value < 0 else 1):
			return size
		return size + 1
			
	elif type == FLOAT:
		# тут по идее только x32 и x64 ?
		# можно сделать и x16, но зачем?
		raise Exception('FLOAT тип ещё не поддерживется')
	return None


def getBytes(block):
	type, text = block[0], block[1]
	size = getSize(block)
	if type == BIN:
		text = ('0' * (size*8 - len(text))) + text
		return [int(i, 2) for i in String(text).wrap(8)]
