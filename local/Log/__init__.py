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