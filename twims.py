# -*- coding: utf-8 -*-
import sys
import tweepy
import subprocess
import time
import HTMLParser

consumer_key = 'StnWnI5AvrMn6FQ73DoSOA'
consumer_secret = 'lcykdASEQVM9T5s2kiJebX5zs2IbYfl9wnNx8Bw4U'

def run_applescript(script):
	# execute the script
	return subprocess.Popen(['osascript', '-e', script.encode('utf-8')], stdout=subprocess.PIPE).stdout.read().strip()

def is_app_running(app):
	return run_applescript('tell application "System Events" to (name of processes) contains "' + app + '"') == "true"

def update_app_status(app, status):
	if is_app_running(app):
		status = HTMLParser.HTMLParser().unescape(status)
		status = status.replace('"', '\\"')
		status = status.replace("\\", "\\\\")
		run_applescript(u'tell application "' + app + u'" to set status message to "' + status + u'"')

def add_param(url, key, value):
	return url + key + "=" + value + "&"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(sys.argv[2], sys.argv[3])

api = tweepy.API(auth)
result = api.user_timeline(screen_name=sys.argv[1], trim_user=1, include_rts=1, count=1, exclude_replies=1)

# parse the responce and get the status
status = result[0].text

# replace the url entities with the expanded urls
offset = 0

for url in result[0].entities['urls']:
	start = int(url['indices'][0]) + offset
	end = int(url['indices'][1]) + offset

	# take away the length of the original string, add the length of the replacment string
	offset = offset - (end - start) + len(url['expanded_url'])

	status = status[:start] + url['expanded_url'] + status[end:]

print status.encode('utf-8')

# Could add others here. Maybe it should be configurable 
update_app_status("Messages", status)
update_app_status("Adium", status)
