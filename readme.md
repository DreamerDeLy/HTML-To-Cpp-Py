# HTML/CSS/JS files to C++ variable convert

Script for minify and convert HTML/CSS/JS files to C++ variables. For example, to create a web interface in Arduino / ESP8266 / ES32 projects.

## Usage

Move your files to `content/` folder and run script. Result will be put at `result.txt` file.

**Input file:**
```html
<a id="wlanpass"></a>
<table>
	<tr>
		<td>SSID&nbsp;</td>
		<td>
			<input type="text" name="wlanssid" id="wlanssid" placeholder="Enter name" value="" maxlength="34" />
		</td>
	</tr>
	<tr>
		<td>Password&nbsp;</td>
		<td>
			<input type="password" name="wlanpass" id="wlanpass" placeholder="Enter password" value="" maxlength="64" />
		</td>
	</tr>
</table>
<br />
```

**Result:**
```c++
// Text len 304 / 365
const char html_file[] = "<a id=wlanpass></a><table><tr><td>SSID&nbsp;</td><td><input type=text name=wlanssid id=wlanssid placeholder=\"Enter name\" value maxlength=34></td></tr><tr><td>Password&nbsp;</td><td><input type=password name=wlanpass id=wlanpass placeholder=\"Enter password\" value maxlength=64></td></tr></table><br>";

```