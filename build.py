import os
import sys


from local import getType, Type, Convert, Bytes, Line, parseLines
from local.Log import *


BOOT = '-boot' in sys.argv


if len(sys.argv) < 2:
	error("Не указан путь к файлу")

path = sys.argv[1]
try:
	with open(path, "r", encoding="UTF8") as file:
		data = file.read()
except:
	print(Fore.RED)
	raise



if "\r\n" in data:
	lines = list(data.split("\r\n"))
elif "\n" in data:
	lines = list(data.split("\n"))
else:
	lines = [data]

for index, line in enumerate(lines):
	if " " in line:
		line = Line(index, line.split(" "))
	else:
		line = Line(index, (line,))
	lines[index] = line

normal(f"прочитано {len(lines)} строк\n")


BYTE = 2**8-1
WORD = 2**16-1
D_WORD = 2**32-1
Q_WORD = 2**64-1

out = []
pointers = {}

def isSigned(x, size=1):
	if size < 1:
		error('!!! isSignedSize >= 1')
	size = 8*size-1
	return (x >= -2**size and x <= 2**size-1)

def strToInt(string):
	if string.startswith("$") and len(string) > 1:
		return string[1:]
	if string.startswith("b"):
		return int(string[1:], 2)
	elif string.startswith("0x"):
		return int(string[2:], 16)
	elif (string.startswith('"') and string.endswith('"')) or (string.startswith("'") and string.endswith("'")):
		return ord(string[1:-1])
	else:
		return int(string)

mode = 'x16'
position = (0x7C00 if BOOT else 0)

for index, line in enumerate(lines):
	if len(line) == 0: continue
	com = line.get()
	if com.startswith("#") or len(com) <= 1: continue
	if com in ('x16', 'x32', 'x64'): mode = com; continue

	if com == 'bios':
		x = line.get()
		try: x = strToInt(x)
		except: print(Fore.RED); raise
		if x > BYTE:
			error(f'{index}:{line.counter}: значение для данной команды максимум {BYTE}')
		out += [0xCD, x]

	elif com == 'mov':
		reg = line.get().upper()
		regADx8 = {'AL': 0xB0, 'AH': 0xB4, 'CL': 0xB1, 'CH': 0xB5,
						   'DL': 0xB2, 'DH': 0xB6, 'BL': 0xB3, 'BH': 0xB7}
		
		if reg in regADx8:
			out.append(regADx8[reg])
			x = line.get()
			try: x = strToInt(x)
			except: print(Fore.RED); raise
			if x > BYTE:
				error(f'{index}:{line.counter}: значение для данной команды максимум {BYTE}')
			out += [x]
		else:
			error(f'{index}:{line.counter}: неподходящий регистр, доступны A-D x8 регистры')

	elif com == 'db':
		x = line.get()
		try: x = strToInt(x)
		except: print(Fore.RED); raise
		if x > BYTE:
			error(f'{index}:{line.counter}: значение для данной команды максимум {BYTE}')
		out += [x]

	elif com == 'jmp':
		# https://www.felixcloutier.com/x86/jmp
		x = line.get()
		x, t = Convert.autoToInt(x)
		if t is Type.STR:
			if x == ':':
				x = -2
			elif x not in pointers:
				error(f'{index}:{line.counter}: указатель не определён')
			else:
				x = 0

		if mode == 'x16':
			if isSigned(x, 1):
				out += [0xEB] + Bytes.fromInt(x, 1, True)
			elif isSigned(x, 2):
				out += [0xE9] + Bytes.fromHex(x, 2, True)
		else:
			error(f'в режиме {mode} данная команда не работает')

	elif com.startswith(":") and len(com) > 1:
		pointers[com[1:]] = len(out)

	else:
		error(f'{index}:{line.counter}: неизвестная команда {com}')


normal("компиляция завершена")
info("запись в файл...")

if BOOT:
	if len(out) > 510:
		error("файл больше boot сектора")
	out += [0 for _ in range(510 - len(out))]
	out += [0x55, 0xAA]

out = bytes(out)

if '\\' in path:
	filename = path.split('\\')[-1]
	name = filename.split('.')[0] if '.' in filename else filename
else:
	name = path.split('.')[0] if '.' in path else path

with open(f'out\\{name}.bin', 'wb') as file:
	file.write(out)

normal("готово!")