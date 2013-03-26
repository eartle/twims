import os
import sys
import tweepy
import webbrowser
import random

consumer_key = 'StnWnI5AvrMn6FQ73DoSOA'
consumer_secret = 'lcykdASEQVM9T5s2kiJebX5zs2IbYfl9wnNx8Bw4U'

plist = 'uk.co.mobbler.twims.plist'

def install():

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	authorization_url = auth.get_authorization_url()

	raw_input("Press Enter to authenticate with Twitter...")

	webbrowser.open(authorization_url)

	verifier = raw_input("Please enter the PIN from Twitter to complete the authorization process: ")

	try:
		token = auth.get_access_token(verifier)
	except tweepy.TweepError:
		sys.exit('Authentication Error\n')

	string = ""

	# read from the plist
	with open(os.path.realpath(plist), 'r') as f:
		string = f.read()

	# replace the plist strings
	string = string.replace("%PYTHON%", os.popen('which python').read().strip())
	string = string.replace("%SCRIPT%", os.path.realpath('twims.py'))
	string = string.replace("%USERNAME%", auth.get_username())
	string = string.replace("%LOG_FILE%", os.path.expanduser('~/Library/Logs/twims.log'))
	string = string.replace("%ACCESS_TOKEN%", os.path.expanduser(token.key))
	string = string.replace("%ACCESS_TOKEN_SECRET%", os.path.expanduser(token.secret))

	if os.path.isfile(os.path.expanduser('~/Library/LaunchAgents/' + plist)):
		os.popen('launchctl unload -w ' + os.path.expanduser('~/Library/LaunchAgents/' + plist))

	# write the plist
	with open(os.path.expanduser('~/Library/LaunchAgents/' + plist), 'w') as f:
		string = f.write(string)

	# don't wait for a restart for launchd to notice this
	os.popen('launchctl load -w ' + os.path.expanduser('~/Library/LaunchAgents/' + plist))

	# run the script now so the user sees an immediate difference
	os.system('chmod a+x twims.py')
	os.system('python twims.py ' + auth.get_username() + ' ' + token.key + ' ' + token.secret )

def uninstall():
	if os.path.isfile(os.path.expanduser('~/Library/LaunchAgents/' + plist)):
		os.popen('launchctl unload -w ' + os.path.expanduser('~/Library/LaunchAgents/' + plist))
		os.popen('rm ' + os.path.expanduser('~/Library/LaunchAgents/' + plist))

def usage():
	sys.exit('Usage:\nInstall: setup.py install\nUninstall: setup.py rm\n')

# change the working directory to the script location 
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# very basic argument parsing
if sys.argv[1] == "install":
	if len(sys.argv) < 2:
		usage()
	else:
		install()
elif sys.argv[1] == "rm":
	uninstall()
else:
	usage()