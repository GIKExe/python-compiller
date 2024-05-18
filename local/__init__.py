import os

from . import Type


def parser(text):
	class d:
		slash = False
		string = False
		byte = False
		comment = False

	out = []
	line = [[""]]

	for si, s in enumerate(text):
		if d.comment:
			if s == '\n':
				d.comment = False

		elif d.slash:
			if s == 'n':
				line[-1][-1] += '\n'
			elif s == 't':
				line[-1][-1] += '\t'
			elif s == '"':
				line[-1][-1] += '"'
			elif s == "'":
				line[-1][-1] += "'"
			else:
				raise Exception("недопустимый символ после слеша в строке: "+s)
			d.slash = False

		elif d.string:
			if s == '\\':
				d.slash = True
				continue
			elif s == '"':
				d.string = False
			line[-1][-1] += s

		else:
			if s == '#':
				d.comment = True
				out.append([[""]])
				continue
			elif s == '"':
				d.string = True
			elif s == '\n':
				out.append(line)
				line = [[""]]
				continue
			elif s == ';':
				line.append([''])
				continue
			elif s == ' ':
				if len(line[-1][-1]) > 0:
					line[-1].append('')
				continue
			line[-1][-1] += s
			if si == len(text)-1:
				out.append(line)

	for li, line in enumerate(out):
		for si, subline in enumerate(line):

			# удаление пустых аргументов на подстроке
			data = {ti:text for ti, text in enumerate(subline)}
			for ti, text in list(data.items()):
				if not text: data.pop(ti)
			subline.clear()
			subline += list(data.values())

			# маркировка аргументов типом
			for ti, text in enumerate(subline):
				subline[ti] = Type.get(text)

	return out