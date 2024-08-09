import app
import dbg

class Manager:
	def __init__(self, filename):
		self.translations = {}
		self.missingKeys = {}

		try:
			self.load(filename)
		except Exception as e:
			self.__out("Failed to load {} with message: {}".format(filename, e))

	def __del__(self):
		self.translations = None

	def load(self, filename):
		f = open(filename, "r")

		translations = {}
		lines = f.readlines()

		for i in xrange(0, len(lines), 2):
			key = lines[i][:-1]
			value = lines[i + 1][:-1]

			translations[key] = value

		f.close()

		self.translations = translations

	def __error(self, string, translated, exception, **kwargs):
		self.__out("Localization Error: {}".format(type(exception)))
		self.__out("    Original String: {}".format(string))
		self.__out("    Translated String: {}".format(translated))
		self.__out("    Exception Message: {}".format(exception))
		self.__out("    Format Arguments: {}".format(str(kwargs)))
		self.__out("    Locale: {}".format(app.GetLocalePath()))

	def __out(self, string):
		dbg.TraceError(string)
		pass

	def get(self, string, **kwargs):
		ret = self.translations.get(string, None)

		if not ret:
			if not self.missingKeys.has_key(string):
				self.__out("Localization {} is missing string: {}".format(app.GetLocalePath(), string))
				self.missingKeys[string] = True

			ret = string

		try:
			return ret
		except Exception, e:
			self.__error(string, ret, e, **kwargs)
			return ret

_manager = Manager(app.GetLocalePath() + "/ui.txt")

def get(string, **kwargs):
	global _manager
	return _manager.get(string, **kwargs)
