from colorama import just_fix_windows_console
just_fix_windows_console()

from colorama import Fore, Back, Style

class Index:
	def __init__(self, li, si, ti):
		self.li = li
		self.si = si
		self.ti = ti

	def __str__(self):
		return f'{self.li+1:4}>{self.si+1}>{self.ti+1:2}:'

	def __repr__(self):
		return self.__str__()

def error(*args, **kwargs):
	print(Fore.RED, *args, Fore.RESET, **kwargs)
	exit()

def warn(*args, **kwargs):
	print(Fore.YELLOW, *args, Fore.RESET, **kwargs)

def normal(*args, **kwargs):
	print(Fore.GREEN, *args, Fore.RESET, **kwargs)

def info(*args, **kwargs):
	print(Fore.WHITE, *args, Fore.RESET, **kwargs)