from ..utils import String


def TYPE(cls):
	cls.__str__ = lambda self: self.__class__.__name__
	cls.__repr__ = lambda self: self.__class__.__name__
	return cls()


@TYPE # для определения числа ввиде витов (TYPE, STR): b1001010101
class BIN: ...
@TYPE
class BYTE: ...
@TYPE
class INT: ...
@TYPE
class UINT: ...
@TYPE
class HEX: ...
@TYPE
class STR: ...
@TYPE
class FLOAT: ...
@TYPE # для определения функций (TYPE, NAME, ARGS): функция(аргументы)
class FUNC: ...


def get(text):
	text = String(text)

	if len(text) == 0:
		return None, None

	if text.sw('b') and text[1:].only('01'):
		return BIN, text[1:]

	if text.only('0123456789'):
		return UINT, text

	if text.sw('-') and text[1:].only('0123456789'):
		return INT, text

	if text.count('.') == 1 and text.replace('.', '').only('0123456789'):
		return FLOAT, text

	if text.sw('0x') and text[2:].only('0123456789ABCDEF'):
		return HEX, text[2:]

	if text.sw('"') and text.ew('"'):
		if len(text) < 3:
			raise Exception("STR тип должен содержать больше 0 символов в двойных кавычках")
		return STR, text[1:-1]

	if text.sw("'") and text.ew("'"):
		if len(text) != 3:
			raise Exception("BYTE тип должен содержать 1 символ в одиночных кавычках")
		return BYTE, text[1:-1]
	return None, text


__all__ = [get, BIN, BYTE, INT, UINT, HEX, STR, FLOAT]