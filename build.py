import os
import sys
import math
from textwrap import wrap

from local import parser
from local import BIN, BYTE, INT, HEX, STR, FLOAT
from local.Log import *

BOOT = '-boot' in sys.argv

if len(sys.argv) < 2:
	error("Не указан путь к файлу")

path = sys.argv[1]
try:
	with open(path, "r", encoding="UTF8") as file:
		text = file.read()
except:
	print(Fore.RED)
	raise

lines = parser(text)
# print(lines)
# exit()

mode = 'x16'
position = (0x7C00 if BOOT else 0)
out = []

regADx8 = {
	'AL': 0xB0, 'CL': 0xB1, 'DL': 0xB2, 'BL': 0xB3,
	'AH': 0xB4, 'CH': 0xB5, 'DH': 0xB6, 'BH': 0xB7,
}


jmpNone = {}
pointers = {}

for li, line in enumerate(lines):
	for si, subline in enumerate(line):
		# lines[line[subline[text(TYPE, STRING)]]]
		if len(subline) < 1: continue
		index = Index(li, si, 0)
		text = subline[0]
		if text[1] == None: continue
		if text[0] != None:
			warn(index, f'начинается с данных: {text[0]}')
			continue

		if text[1] == 'bios':
			out.append(0xCD)
			index.ti += 1
			if len(subline) < 2:
				error(index, f'подстрока неожиданно закончилась. ожидалось: (BIN, BYTE, INT, STR)')

		# записиь в байт-регистры
		if text[1] in regADx8 and False:
			out.append(regADx8[text[1]])
			index.ti += 1
			if len(subline) < 2:
				error(index, f'подстрока неожиданно закончилась. ожидалось: ("=",)')
			text = subline[1]
			if text[0] != None:
				error(index, f'неверный тип: {text[0]}, ожидался: None')
			if text[1] == '=':
				index.ti += 1
				if len(subline) < 3:
					error(index, f'подстрока неожиданно закончилась. ожидалось: (BIN, BYT, INT, HEX,)')
				text = subline[2]
				if text[0] not in (BIN, BYT, INT, HEX,):
					error(index, f'неверный тип: {text[0]}, ожидался: (BIN, BYT, INT, HEX,)')

				raw = blockToBytes(text)
				if len(raw) != 1:
					error(index, f'неверный размер аргумента: {len(raw)}, ожидался: 1 байт')
				out += raw
			else:
				error(index, f'неверный аргумент. ожидалось: ("=",)')
		print(*[z[1] for z in subline])
			
	# com = line.get()
	# if com.startswith("#") or len(com) <= 1: continue
	# if com in ('x16', 'x32', 'x64'): mode = com; continue

	# if com == 'bios':
	# 	x = line.get()
	# 	try: x = strToInt(x)
	# 	except: print(Fore.RED); raise
	# 	if x > BYTE:
	# 		error(f'{index}:{line.counter}: значение для данной команды максимум {BYTE}')
	# 	out += [0xCD, x]

	# elif com == 'mov':
	# 	reg = line.get().upper()
	# 	regADx8 = {'AL': 0xB0, 'AH': 0xB4, 'CL': 0xB1, 'CH': 0xB5,
	# 					   'DL': 0xB2, 'DH': 0xB6, 'BL': 0xB3, 'BH': 0xB7}
		
	# 	if reg in regADx8:
	# 		out.append(regADx8[reg])
	# 		x = line.get()
	# 		try: x = strToInt(x)
	# 		except: print(Fore.RED); raise
	# 		if x > BYTE:
	# 			error(f'{index}:{line.counter}: значение для данной команды максимум {BYTE}')
	# 		out += [x]
	# 	else:
	# 		error(f'{index}:{line.counter}: неподходящий регистр, доступны A-D x8 регистры')

	# elif com == 'db':
	# 	x = line.get()
	# 	try: x = strToInt(x)
	# 	except: print(Fore.RED); raise
	# 	if x > BYTE:
	# 		error(f'{index}:{line.counter}: значение для данной команды максимум {BYTE}')
	# 	out += [x]

	# elif com == 'jmp':
	# 	# https://www.felixcloutier.com/x86/jmp
	# 	x = line.get()
	# 	x, t = Convert.autoToInt(x)
	# 	if t is Type.STR:
	# 		if x == ':':
	# 			x = -2
	# 		elif x not in pointers:
	# 			error(f'{index}:{line.counter}: указатель не определён')
	# 		else:
	# 			x = 0

	# 	if mode == 'x16':
	# 		if isSigned(x, 1):
	# 			out += [0xEB] + Bytes.fromInt(x, 1, True)
	# 		elif isSigned(x, 2):
	# 			out += [0xE9] + Bytes.fromHex(x, 2, True)
	# 	else:
	# 		error(f'в режиме {mode} данная команда не работает')

	# elif com.startswith(":") and len(com) > 1:
	# 	pointers[com[1:]] = len(out)

	# else:
	# 	error(f'{index}:{line.counter}: неизвестная команда {com}')


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