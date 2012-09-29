import sys
import xml.etree.ElementTree
import urllib2
import os
import tempfile
import HTMLParser

def run_applescript(script):
	# write the script to a temporart file (os.popen doesn't like utf-8)
	temp = tempfile.NamedTemporaryFile(delete=False)
	temp.write(script.encode('utf-8'))
	temp.close()

	# execute the script, delete the temp file, and return the result
	result = os.popen('osascript ' + temp.name).read().strip()
	os.remove(temp.name)
	return result

def is_app_running(app):
	return run_applescript('tell application "System Events" to (name of processes) contains "' + app + '"') == "true"

def update_app_status(app, status):
	if is_app_running(app):
		status = HTMLParser.HTMLParser().unescape(status)
		status = status.replace('"', '\\"')
		status = status.replace("\\", "\\\\")
		run_applescript('tell application "' + app + '" to set status message to "' + status + '"')

def add_param(url, key, value):
	return url + key + "=" + value + "&"

# fetch the latest tweet that wasn't a reply, including RTs
url = 'http://api.twitter.com/1/statuses/user_timeline.xml?'
url = add_param(url, 'screen_name', sys.argv[1])
url = add_param(url, 'trim_user', '1')
url = add_param(url, 'include_rts', '1')
url = add_param(url, 'count', '1')
url = add_param(url, 'exclude_replies', '1')
url = add_param(url, 'include_entities', '1')

response = urllib2.urlopen(url)
html = response.read()

# parse the responce and get the status
statuses = xml.etree.ElementTree.XML(html)
status = statuses[0].find('text').text

# replace the url entities with the expanded urls
offset = 0

for url in statuses[0].find("entities").find("urls"):
	start = int(url.attrib['start']) + offset
	end = int(url.attrib['end']) + offset

	# take away the length of the original string, add the length of the replacment string
	offset = offset - (end - start) + len(url.find('expanded_url').text)

	status = status[:start] + url.find('expanded_url').text + status[end:]

print status

# Could add others here. Maybe it should be configurable 
update_app_status("Messages", status)
update_app_status("Adium", status)
