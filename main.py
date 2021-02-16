import sys
import requests
import glob

from css_html_js_minify import process_single_html_file, process_single_js_file, process_single_css_file, html_minify, js_minify, css_minify
import htmlmin

use_api_for_html = False # use WEB service for HTML minify
use_api_for_css = True # use WEB service for CSS minify
use_api_for_js = True # use WEB service for JS minify

split_lines = False # split output into multiple lines
escape_percent = False # escape % character to %% (for printf formatting string)

result_file = "content/result.txt" # output file

def process_text(text):
	output = "\""

	for s in text:
		if s == '\f':
			output += "\\f"
		elif s == '\n':
			if split_lines:
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
			if escape_percent:
				output += "%%"
			else:
				output += "%"
		else:
			output += s

	output += "\""

	return output

def minify_html_by_api(html):
	payload = {'input': html}
	url = 'https://html-minifier.com/raw'
	print("Requesting HTML formatting. . .")
	r = requests.post(url, payload)
	return r.text

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
		if (use_api_for_html):
			text = minify_html_by_api(text)
		else:
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
