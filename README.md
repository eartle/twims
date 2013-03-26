# twims - Twitter to IM Status

This a tool to update your status message in Adium.app and Messages.app to your last tweet. It includes 'new style' RTs, excludes replies, and converts t.co links to their expanded versions.

To install you will need to clone this repository and then run setup.py in a terminal like this:

```
python setup.py install
```

You will asked to auth with Twitter and then enter the verification code.

Your status will be updated immediately and then refreshed every 60 seconds. 

If you decide you don't want your IM status updated anymore you can uninstall like this:

```
python setup.py rm
```

## Tech notes

* Uses launchd and not crontab (I'm a good boy) 
* The scripts are python, but the actual status message update is done through AppleScript (nice)

## Things to do:

* User configurable refresh rate (currently just does every 60 seconds)
* User configurable apps (is there anything other than Messages and Adium this would work on?)

