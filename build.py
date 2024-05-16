import os
import sys

from local import parser
from local import BIT, BYT, INT, HEX, STR, FLT
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
mode = 'x16'
position = (0x7C00 if BOOT else 0)
out = []
pointers = {}

regADx8 = {
	'AL': 0xB0, 'CL': 0xB1, 'DL': 0xB2, 'BL': 0xB3,
	'AH': 0xB4, 'CH': 0xB5, 'DH': 0xB6, 'BH': 0xB7,
}

def getSizeOfTextBlock(text):
	type = text[0]
	if type == BIT:
		return len(text[1]) // 8 + 1
	elif type == BYT:
		return 1
	elif type == HEX:
		return len(text[1]) // 2 + 1
	elif type == STR:
		return len(text[1])
	elif type == INT:
		# вот тут самое сложное...
		...
	elif type == FLT:
		# тут по идее только x32 и x64 ?
		# можно сделать и x16, но зачем?
		...
	return None

def textblockToByte(text):
	size = getSizeOfTextBlock(text)
	if text[0] == BIT:
		...
		# в доработке

for li, line in enumerate(lines):
	for si, subline in enumerate(line):
		# lines[line[subline[text(TYPE, STRING)]]]
		text = subline[0]
		if text[1] == None: continue
		if text[0] != None:
			warn(f'{li+1:3}{si+1:3}  1: начинается с данных: {text[0]}')
			continue

		# записиь в байт-регистры
		if text[1] in regADx8:
			out.append(regADx8[text[1]])
			if len(subline) < 2:
				error(f'{li+1:3}{si+1:3}  1-2: подстрока неожиданно закончилась. ожидалось: ("=",)')
			text = subline[1]
			if text[0] != None:
				error(f'{li+1:3}{si+1:3}  2: неверный тип: {text[0]}, ожидался: None')
			if text[1] == '=':
				if len(subline) < 3:
					error(f'{li+1:3}{si+1:3}  2-3: подстрока неожиданно закончилась. ожидалось: (BIT, BYT, INT, HEX,)')
				text = subline[2]
				if text[0] not in (BIT, BYT, INT, HEX,):
					error(f'{li+1:3}{si+1:3}  3: неверный тип: {text[0]}, ожидался: (BIT, BYT, INT, HEX,)')
				# перевести любой из типов в байт
				# добавить байт в out
			else:
				error(f'{li+1:3}{si+1:3}  2: неверный аргумент. ожидалось: ("=",)')
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