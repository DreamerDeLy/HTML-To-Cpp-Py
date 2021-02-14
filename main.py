from css_html_js_minify import process_single_html_file, process_single_js_file, process_single_css_file, html_minify, js_minify, css_minify
import htmlmin

result_file = "content/result.txt"

def process_text(text):
	output = "\""
	splitLines = False
	escapePercent = False

	for s in text:
		if s == '\f':
			output += "\\f"
		elif s == '\n':
			if splitLines:
				output += "\\n\"\n\""
			else:
				output += "\\n"
		elif s == '\r':
			output += "\\r"
		elif s == '\t':
			output += "\\t"
		elif s == '\"':
			output += "\\\""
		elif s == '\\':
			output += "\\\\"
		elif s == '%':
			if escapePercent:
				output += "%%"
			else:
				output += "%"
		else:
			output += s

	output += "\""

	return output

import glob

files_list_html = glob.glob('./content/*.html')
print("html:")
print(files_list_html)

files_list_css = glob.glob('./content/*.css')
print("css:")
print(files_list_css)

files_list_js = glob.glob('./content/*.js')
print("js:")
print(files_list_js)

files_list_all = files_list_html + files_list_css + files_list_js

print(" --- ")

f = open(result_file, "w")
f.write("")
f.close()

for i in files_list_all:
	file_type = ""

	print("File: "+i)
	f = open(i, "r")

	text = f.read()
	text_save = text

	if i.split(".")[-1] == "html":
		text = htmlmin.minify(text, remove_empty_space = True, remove_comments = True)
		file_type = "html"
	elif i.split(".")[-1] == "css":
		text = css_minify(text)
		file_type = "css"
	elif i.split(".")[-1] == "js":
		text = js_minify(text)
		file_type = "js"
	else:
		print("!file extention undetected")
		file_type = "undefined"
	

	text = process_text(text)

	print("Text size {0} / {1}".format(len(text), len(text_save)))
	print(" --- ")

	f = open(result_file, "a")
	f.write("// Text len {0} / {1}\n".format(len(text), len(text_save)))
	f.write("char " + file_type + "_file[] = "+text+"\n")
	f.close()
