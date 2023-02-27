import os
import requests
import glob
from fnmatch import fnmatch

from css_html_js_minify import process_single_html_file, process_single_js_file, process_single_css_file, html_minify, js_minify, css_minify
import htmlmin

use_api_for_html = False # use WEB service for HTML minify
use_api_for_css = True # use WEB service for CSS minify
use_api_for_js = True # use WEB service for JS minify

split_lines = False # split output into multiple lines
escape_percent = False # escape % character to %% (for printf formatting string)

result_file = "content/result.h" # output file

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
	url = "https://www.toptal.com/developers/html-minifier/api/raw"
	print("Requesting HTML formatting. . .")
	r = requests.post(url, payload)
	return r.text

def minify_css_by_api(css):
	payload = {'input': css}
	url = "https://www.toptal.com/developers/cssminifier/api/raw"
	print("Requesting CSS formatting. . .")
	r = requests.post(url, payload)
	return r.text

def minify_js_by_api(js):
	payload = {'input': js}
	url = "https://www.toptal.com/developers/javascript-minifier/api/raw"
	print("Requesting JS formatting. . .")
	r = requests.post(url, payload)
	return r.text


# For the given path, get the List of all files in the directory tree 
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

# Get files 
files_list_all = getListOfFiles("./content/")
print(" --- ")

# Clear file
f = open(result_file, "w")
f.write("")
f.close()

# Statistics
saved_space_by_type = { }

# Supported file types
text_file_types = ["html", "css", "js", "svg"]

# Process files 
for i in files_list_all:
	print("File: " + i)
	file_type = i.split(".")[-1]

	if file_type in text_file_types:
		printed_file_name = file_type + i.replace("." + file_type, "").replace(".", "_").replace("\\", "_").replace("/", "_").replace("-", "")

		# Read original file
		f = open(i, "r")
		text = f.read()

		# Save length before processing
		len_before = len(text)

		if file_type == "html":
			if (use_api_for_html):
				text = minify_html_by_api(text)
			else:
				text = htmlmin.minify(text, remove_empty_space = True, remove_comments = True)
		elif file_type == "css":
			if (use_api_for_css):
				text = minify_css_by_api(text)
			else:
				text = css_minify(text)
		elif file_type == "js":
			if (use_api_for_js):
				text = minify_js_by_api(text)
			else:
				text = js_minify(text)
		else:
			print("Not supported type")
		
		len_after = len(text)
		saved_space_by_type[file_type] = (len_before - len_after)

		text = process_text(text)

		print("Text size {0} / {1}".format(len_after, len_before))
		print(" --- ")

		# Write to result file
		f = open(result_file, "a")
		f.write("// Length {0} / {1}\n".format(len_after, len_before))
		f.write("const char " + printed_file_name + "[] = "+text+";\n")
		f.close()
	else:
		print("Not a text file")

total_saved_space = 0

print()
print("Saved space by file type: ")

for x, y in saved_space_by_type.items():
	print("{0}: {1}".format(x, y))
	total_saved_space += y
print()

print("Total saved space: ")
print(total_saved_space)

print()
print(" --- ")
