import xml.dom.minidom as xml
import item
import player

_windowSets = dict()

def getWindowFromString(string):
	return _windowSets.get(string)

def load(filename):
	try:
		content = open(filename, "r").read()

		dom = xml.parseString(content)
	except Exception as e:
		import dbg
		dbg.TraceError("Failed to parse {}: {}".format(filename, e))
		return
