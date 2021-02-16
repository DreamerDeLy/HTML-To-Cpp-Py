import sys
import requests

from css_html_js_minify import process_single_html_file, process_single_js_file, process_single_css_file, html_minify, js_minify, css_minify
import htmlmin

use_api_for_css = True
use_api_for_js = True

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

def minify_css_by_api(css):
	payload = {'input': css}
	url = 'https://cssminifier.com/raw'
	print("Requesting CSS formatting. . .")
	r = requests.post(url, payload)
	return r.text

def minify_js_by_api(js):
	payload = {'input': js}
	url = 'https://javascript-minifier.com/raw'
	print("Requesting JS formatting. . .")
	r = requests.post(url, payload)
	return r.text

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
		file_type = "html"
		text = htmlmin.minify(text, remove_empty_space = True, remove_comments = True)
	elif i.split(".")[-1] == "css":
		file_type = "css"
		if (use_api_for_css):
			text = minify_css_by_api(text)
		else:
			text = css_minify(text)
	elif i.split(".")[-1] == "js":
		file_type = "js"
		if (use_api_for_js):
			text = minify_js_by_api(text)
		else:
			text = js_minify(text)
	else:
		file_type = "undefined"
		print("!file extention undetected")
	

	text = process_text(text)

	print("Text size {0} / {1}".format(len(text), len(text_save)))
	print(" --- ")

	f = open(result_file, "a")
	f.write("// Text len {0} / {1}\n".format(len(text), len(text_save)))
	f.write("const char " + file_type + "_file[] = "+text+";\n")
	f.close()
