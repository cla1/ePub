# -*- coding: utf-8 -*-
import sublime_plugin, sublime
import os, re, tempfile, codecs

def _import(fullpath):
	import sys
	path, filename = os.path.split(fullpath)
	filename, ext = os.path.splitext(filename)
	sys.path.append(path)
	module = __import__(filename)
	del sys.path[-1]
	return module

epub = _import(os.path.dirname(__file__)+'/epub')

class EPUB(sublime_plugin.EventListener):

	def on_load(self, view):
		if view and view.file_name() and view.file_name().endswith('epub'):
			self.epub_path = view.file_name()

			self.epub_file = epub.open_epub(self.epub_path)
			book = epub.Book(self.epub_file)

			BOOK = ''
			# for name, role, file_as in book.creators:
			#   BOOK += role+': '+name+"\n"

			# for name, role, file_as in book.contributors:
			#   BOOK += role+': '+name+"\n"

			# for date, event in book.dates:
			#   BOOK += event+': '+date+"\n"

			# for lang in book.languages:
			#   BOOK += 'Language: '+lang+"\n"

			# for name, content in book.metas:
			#   BOOK += name+': '+content+"\n"

			# for title1, title2 in book.metas:
			#   BOOK += 'Subject: '+title1+':'+title2+"\n"

			# for title, lang in book.titles:
			#   BOOK += title+': '+lang+"\n"

			# BOOK += 'Publisher:'+book.publisher+"\n"
			# BOOK += 'Description:'+book.description+"\n"

			# for uno, dos, tres in book.identifiers:
			#   BOOK += uno+','+dos+','+tres+"\n"

			for chapter in book.chapters:
				try:
					BOOK += str(Format(str(chapter.read().decode('utf-8'))))
				except:
					pass
			self.epub_file.close()

			tmp = tempfile.NamedTemporaryFile(delete=False)
			codecs.open(tmp.name, 'w+', 'utf-8').write((BOOK).strip())

			window = sublime.active_window()
			_view = window.open_file(tmp.name)

			window.focus_view(view)
			window.run_command('close')
			window.focus_view(_view)

			_view.settings().set("wrap_width", 70)

def Format(data):
	return re.sub('\n\s*\n', '\n\n', re.sub('\r\n', '\n', re.sub('&nbsp;', ' ', re.sub('/\*\*/', ' ', re.sub('<[^>]*>', '',  data)))))