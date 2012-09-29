import os
import sys

plist = 'uk.co.mobbler.twims.plist'

def install(username):
	string = ""

	# read from the plist
	with open(os.path.realpath(plist), 'r') as f:
		string = f.read()

	# replace the plist strings
	string = string.replace("%PYTHON%", os.popen('which python').read().strip())
	string = string.replace("%SCRIPT%", os.path.realpath('twims.py'))
	string = string.replace("%USERNAME%", username)
	string = string.replace("%LOG_FILE%", os.path.expanduser('~/Library/Logs/twims.log'))

	if os.path.isfile(os.path.expanduser('~/Library/LaunchAgents/' + plist)):
		os.popen('launchctl unload -w ' + os.path.expanduser('~/Library/LaunchAgents/' + plist))

	# write the plist
	with open(os.path.expanduser('~/Library/LaunchAgents/' + plist), 'w') as f:
		string = f.write(string)

	# don't wait for a restart for launchd to notice this
	os.popen('launchctl load -w ' + os.path.expanduser('~/Library/LaunchAgents/' + plist))

	# run the script now so the user sees an immediate difference
	os.system('chmod a+x twims.py')
	os.system('python twims.py ' + username)

def uninstall():
	if os.path.isfile(os.path.expanduser('~/Library/LaunchAgents/' + plist)):
		os.popen('launchctl unload -w ' + os.path.expanduser('~/Library/LaunchAgents/' + plist))
		os.popen('rm ' + os.path.expanduser('~/Library/LaunchAgents/' + plist))

def usage():
	sys.exit('Usage:\nInstall: setup.py install <username>\nUninstall: setup.py rm\n')

# change the working directory to the script location 
os.chdir(os.path.dirname(os.path.realpath(__file__)))

# very basic argument parsing
if sys.argv[1] == "install":
	if len(sys.argv) < 3:
		usage()
	else:
		install(sys.argv[2])
elif sys.argv[1] == "rm":
	uninstall()
else:
	usage()