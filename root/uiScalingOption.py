import ui, cfg


class ScalingOption(ui.ScriptWindow):
	def __init__(self):
		super(ScalingOption, self).__init__()
		self.Objects = {}

		self.__BuildWindow()

	def __del__(self):
		self.Objects = {}

		super(ScalingOption, self).__del__()

	def Destroy(self):
		self.ClearDirectionary()
		self.Objects = {}

	def __BuildWindow(self):
		try: ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/scalingoption_main.py")
		except: return False
		
		GetObject = ui.__mem_func__(self.GetChild)

		(self.Objects["SLIDER_STONES"], self.Objects["SLIDER_BOSESS"]) = (GetObject("SLIDER_STONES"), GetObject("SLIDER_BOSESS"))
		return self.__BindActions()

	def __BindActions(self):
		try:

			curValue = int(cfg.Get(cfg.SAVE_OPTION, "SCALE_STONES", "100"))
			curValue /= 100
			self.Objects["SLIDER_STONES"].SetSliderPos(float(curValue) - 0.5)
			curValue = int(cfg.Get(cfg.SAVE_OPTION, "SCALE_BOSESS", "100"))
			curValue /= 100
			self.Objects["SLIDER_BOSESS"].SetSliderPos(float(curValue) - 0.5)

			self.Objects["SLIDER_STONES"].SetEvent(lambda : self.ScaleInstance("SCALE_STONES"))
			self.Objects["SLIDER_BOSESS"].SetEvent(lambda : self.ScaleInstance("SCALE_BOSESS"))

			return True
		except: return False

	def MINMAX(self, min, value, max):

		if value < min:
			return min

		elif value > max:
			return max
		else:
			return value

	def ScaleInstance(self, type):
		Objects = {
			"SCALE_STONES" : self.Objects["SLIDER_STONES"],
			"SCALE_BOSESS" : self.Objects["SLIDER_BOSESS"],
		}

		if not Objects.has_key(type):
			return

		Object = Objects[type]
		value = self.MINMAX(0.5, 0.5 + Object.GetSliderPos(), 1.5)
		
		cfg.Set(cfg.SAVE_OPTION, type, value * 100)

	def Open(self):
		self.SetCenterPosition()

		super(ScalingOption, self).Show()
		self.SetTop()

	def Close(self):
		super(ScalingOption, self).Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
