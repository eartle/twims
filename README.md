# twims - Twitter to IM Status

This a tool to update your status message in Adium.app and Messages.app to your last tweet. It includes 'new style' RTs, excludes replies, and converts t.co links to their expanded versions.

To install you will need to clone this repository and then run setup.py in a terminal like this:

```
python setup.py install <Twitter username>
```

Your status will be updated immediately and then refreshed every 60. 

If you decide you don't want your statuses updated anymore you can uninstall like this:

```
python setup.py rm
```

To do a one-off status change do this:

```
python twims.py <Twitter username>
```

## Tech notes

* Uses launchd and not crontab (I'm a good boy) 
* The scripts are python, but the actual status message update is done through AppleScript (nice)

## Things to do:

* Use a Twitter API account so that we get a bigger rate limit (only really necessary if API version  1 is getting deprecated).
* User configurable refresh rate (currently just does every 60 seconds)
* User configurable apps (is there anything other than Messages and Adium this would work on?)

