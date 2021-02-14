from css_html_js_minify import process_single_html_file, process_single_js_file, process_single_css_file, html_minify, js_minify, css_minify

html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Bootstrap Case</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body> 
<div class="container">
  <h2>Well</h2>
  <div class="well">Basic Well</div>
</div>
</body>
</html>
"""

minified = html_minify(html)
# print(minified)

output = "\""
splitLines = False
escapePercent = False

for s in html:
	if s == '\f':
		output += "\\f"
	elif s == '\n':
		if splitLines:
			output += "\\n\"\n\"";
		else:
			output += "\\n";
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

print(output)
