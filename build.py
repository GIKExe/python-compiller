import os
import sys

from colorama import just_fix_windows_console
just_fix_windows_console()

from colorama import Fore, Back, Style

def error(*args, **kwargs):
	print(Fore.RED, *args, Fore.RESET, **kwargs)
	exit()

def warn(*args, **kwargs):
	print(Fore.YELLOW, *args, Fore.RESET, **kwargs)

def normal(*args, **kwargs):
	print(Fore.GREEN, *args, Fore.RESET, **kwargs)

def info(*args, **kwargs):
	print(Fore.WHITE, *args, Fore.RESET, **kwargs)




class Line(list):
	def __init__(self, index, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.index = index
		self.counter = 0

	def get(self):
		if len(self) == 0: error(f'{self.index}: строка неожиданно закончилась')
		self.counter += 1
		return self.pop(0)

if len(sys.argv) < 2:
	error("Не указан путь к файлу")

path = sys.argv[1]
try:
	with open(path, "r", encoding="UTF8") as file:
		data = file.read()
except:
	print(Fore.RED)
	raise

out = []

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

def strToInt(string):
	if string.startswith("b"):
		return int(string[1:], 2)
	elif string.startswith("0x"):
		return int(string[2:], 16)
	elif (string.startswith('"') and string.endswith('"')) or (string.startswith("'") and string.endswith("'")):
		return ord(string[1:-1])
	else:
		return int(string)

for index, line in enumerate(lines):
	mode = "x16"
	if len(line) == 0:
		continue
	# print(line)
	com = line.get()
	if com.startswith("#") or len(com) <= 1:
		continue

	# if com in ("x16", "x32", "x64"):
	# 	mode = line[0]
	# 	com = line.get()

	if com == 'int':
		value = line.get()
		try: value = strToInt(value)
		except: print(Fore.RED); raise
		if value > BYTE:
			error(f'{index}:{line.counter}: значение для данной команды максимум {BYTE}')
		out += [0xCD, value]

	elif com == 'mov':
		reg = line.get()
		if reg == "AL":
			out += [0xB0]
		elif reg == "AH":
			out += [0xB4]
		elif reg == "CL":
			out += [0xB1]
		elif reg == "CH":
			out += [0xB5]
		elif reg == "DL":
			out += [0xB2]
		elif reg == "DH":
			out += [0xB6]
		elif reg == "BL":
			out += [0xB3]
		elif reg == "BH":
			out += [0xB7]
		else:
			error(f'{index}:{line.counter}: неподходящий регистр, доступны A-D x8 регистры')

		value = line.get()
		try: value = strToInt(value)
		except: print(Fore.RED); raise
		if value > BYTE:
			error(f'{index}:{line.counter}: значение для данной команды максимум {BYTE}')
		out += [value]

	elif com == 'db':
		value = line.get()
		try: value = strToInt(value)
		except: print(Fore.RED); raise
		if value > BYTE:
			error(f'{index}:{line.counter}: значение для данной команды максимум {BYTE}')
		out += [value]

	elif com == 'jmp':
		value = line.get()
		try: value = strToInt(value)
		except: print(Fore.RED); raise
		if value > BYTE:
			error(f'{index}:{line.counter}: значение для данной команды максимум {BYTE}')
		out += [0xEB, (BYTE + 1 + value) if value < 0 else value]

	else:
		error(f'{index}:{line.counter}: неизвестная команда {com}')


normal("компиляция завершена")
info("запись в файл...")

out += [0 for _ in range(510 - len(out))]
out += [0x55, 0xAA]
# print([ord(s) for s in out])
out = bytes(out)

with open(path+'.bin', 'wb') as file:
	file.write(out)

normal("готово!")