import ui
import app
import exception
import localeInfo

## https://www.geeksforgeeks.org/python-program-to-convert-integer-to-roman/
def convertToRoman(number):
	num = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
	sym = ["I", "IV", "V", "IX", "X", "XL", "L", "XC", "C", "CD", "D", "CM", "M"]
	i = 12

	sReturnString = ""
	while number:
		div = number // num[i]
		number %= num[i]

		while div:
			sReturnString += sym[i]
			div -= 1
		i -= 1

	return sReturnString

class DungeonTaskWindow(ui.ScriptWindow):

	STAGE_COUNT = 0
	STAGE_GAUGE_POS = (14, 31)
	STAGE_BUTTON_ALIGN = 5

	class StageButton(ui.ExpandedImageBox):

		DISABLED_IMAGE = "assets/ui/dungeon_task/button_stage_n.tga"
		ENABLED_IMAGE = "assets/ui/dungeon_task/button_stage_h.tga"

		def	__init__(self, iNum):
			ui.ExpandedImageBox.__init__(self)
			self.__BuildWindow(convertToRoman(iNum))

		def	__del__(self):
			ui.ExpandedImageBox.__del__(self)
			self.buttonName = None

		def	__radd__(self, rLeft):
			return self.GetWidth() + (rLeft.GetWidth() if type(rLeft) is not int else rLeft)

		def	__BuildWindow(self, sName):
			## Load Image
			self.LoadImage(self.DISABLED_IMAGE)

			## Put Text
			self.buttonName = ui.MakeTextLine(self)
			self.buttonName.SetPosition(0, -1)
			self.buttonName.SetText(sName)

		def	SetStageEnabled(self, bEnabled):
			self.LoadImage(self.DISABLED_IMAGE if not bEnabled else self.ENABLED_IMAGE)

	class StageGauge(ui.ExpandedImageBox):

		GAUGE_FULL = "assets/ui/dungeon_task/gauge_full.tga"
		GAUGE_EMPTY = "assets/ui/dungeon_task/gauge_empty.tga"

		def	__init__(self):
			ui.ExpandedImageBox.__init__(self)
			self.__BuildWindow()

		def	__del__(self):
			ui.ExpandedImageBox.__del__(self)
			self.imgGaugeFull = None
			self.textGauge = None

		def	__BuildWindow(self):
			## Load background (empty gauge)
			self.LoadImage(self.GAUGE_EMPTY)

			## Load full guage
			self.imgGaugeFull = ui.ExpandedImageBox()
			self.imgGaugeFull.SetParent(self)
			self.imgGaugeFull.SetPosition(0, 0)
			self.imgGaugeFull.LoadImage(self.GAUGE_FULL)
			self.imgGaugeFull.SetPercentage(0, 100)
			self.imgGaugeFull.Show()

			## Gauge overlay
			self.textGauge = ui.MakeTextLine(self.imgGaugeFull)
			self.textGauge.SetPosition(0, -1)
			self.textGauge.SetText("")

			## Show by default
			self.Show()

		def	SetProgress(self, iPerc):
			iPerc = min(iPerc, 100)
			self.imgGaugeFull.SetPercentage(iPerc, 100)
			self.textGauge.SetText(localeInfo.DUNGEON_TASK_TOTAL_PROGRESS % iPerc)

	def	__init__(self):
		ui.ScriptWindow.__init__(self)
		self.Objects = {}
		self.ttLocalTimerEnd = 0
		self.ttGlobalTimerEnd = 0
		self.__LoadWindow()

	def	__del__(self):
		ui.ScriptWindow.__del__(self)
		self.Objects = {}
		self.ttLocalTimerEnd = 0
		self.ttGlobalTimerEnd = 0

	def	Destroy(self):
		self.ClearDictionary()
		self.Objects = {}

	def	__LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/DungeonTaskWindow.py")
		except:
			exception.Abort("DungeonTaskWindow.__LoadWindow.LoadObject")

		try:
			self.Objects["Board"] = self.GetChild("Board")
			self.Objects["Stage_Label"] = self.GetChild("StageLabel")
			self.Objects["Stage_Gauge"] = self.StageGauge()
			self.Objects["Stage_Desc"] = self.GetChild("StageDescription")
			self.Objects["Stage_TimeLeft"] = self.GetChild("StageTimeLeft")
			self.Objects["Global_TimeLeft"] = self.GetChild("GlobalTimeLeft")
			self.Objects["Global_StageCount"] = self.GetChild("GlobalStageCount")

			## Stage buttons
			self.Objects["Stage_Buttons"] = dict()
		except:
			exception.Abort("DungeonTaskWindow.__LoadWindow.BindObject")

		## Set pos of gauge
		self.Objects["Stage_Gauge"].SetParent(self)
		self.Objects["Stage_Gauge"].SetPosition(*self.STAGE_GAUGE_POS)

		## Set global timer text
		self.Objects["Global_TimeLeft"].SetText(localeInfo.DUNGEON_TASK_GLOBAL_TL % "-")

		self.SetTop()
		self.Hide()

		# self.__RunTest()

	""" Recv """
	def	RecvTaskInfo(self, iNum, sTitle):
		if not iNum in self.Objects["Stage_Buttons"]:
			self.Objects["Stage_Buttons"][iNum] = self.StageButton(iNum)
			self.Objects["Stage_Buttons"][iNum].SetParent(self)
			self.Objects["Stage_Buttons"][iNum].SetPosition(0, -1)
			self.Objects["Stage_Buttons"][iNum].Show()

		## We need to refresh the order
		self.STAGE_COUNT = max(self.STAGE_COUNT, iNum)
		self.__RearrangeStageButtons()

	def	RecvGlobalTimer(self, iElapse):
		self.ttGlobalTimerEnd = app.GetTime() + iElapse

	def	RecvSetCurrentTask(self, iNum, sDesc, iCount, iProgress):
		if not iNum in self.Objects["Stage_Buttons"]:
			print iNum, "key not found!"
			return

		## Switch buttons
		for k, v in self.Objects["Stage_Buttons"].items():
			v.SetStageEnabled((k == iNum))

		## Set desc
		self.Objects["Stage_Desc"].SetText(sDesc)

		## Set local timer
		self.Objects["Stage_TimeLeft"].SetText(localeInfo.DUNGEON_TASK_STAGE_TL % "-")

		## Set stage num
		self.Objects["Global_StageCount"].SetText(localeInfo.DUNGEON_TASK_GLOBAL_SP % (iNum, self.STAGE_COUNT))

		## Set progress
		self.Objects["Stage_Gauge"].SetProgress(iProgress)

	def	RecvEndDungeon(self):
		## Mark everything as done
		for k, v in self.Objects["Stage_Buttons"].items():
			v.SetStageEnabled(True)

		## Clear timers
		self.ttLocalTimerEnd = app.GetTime()
		self.ttGlobalTimerEnd = app.GetTime()

		## Set progress
		self.Objects["Stage_Gauge"].SetProgress(100)

	def	RecvSetLocalTimer(self, iElapse):
		self.ttLocalTimerEnd = app.GetTime() + iElapse

	def	RecvUpdateCounter(self, iCount):
		## Place for further implementation
		pass

	def	RecvUpdateProgress(self, iProgress):
		self.Objects["Stage_Gauge"].SetProgress(iProgress)
	""" Recv """

	def	__RearrangeStageButtons(self):
		labelWidth = self.Objects["Stage_Label"].GetTextSize()[0]

		## Calculate total width
		totalWidth = labelWidth + sum(self.Objects["Stage_Buttons"].values())

		## Add alignment
		totalWidth += len(self.Objects["Stage_Buttons"]) * self.STAGE_BUTTON_ALIGN

		## Calculate entry position basing on the middle of board
		entryX = (self.Objects["Board"].GetWidth()-totalWidth)/2

		## Label goes as first
		self.Objects["Stage_Label"].SetPosition(entryX, self.Objects["Stage_Label"].GetLocalPosition()[1])
		entryX += labelWidth + self.STAGE_BUTTON_ALIGN

		## And then buttons
		for v in self.Objects["Stage_Buttons"].values():
			v.SetPosition(entryX, v.GetLocalPosition()[1])
			entryX += v.GetWidth() + self.STAGE_BUTTON_ALIGN

	def	__RunTest(self, bUpdate = False):
		if not bUpdate:
			## Random stages
			for i in xrange(1, 6):
				self.RecvTaskInfo(i, "TEST_%d" % i)

			## Random global time
			self.RecvGlobalTimer(app.GetRandom(60, 3600))

		## Random tasks
		self.RecvSetCurrentTask(app.GetRandom(1, 5), "SAMPLE DESC %d" % app.GetRandom(36000, 300000), 0, app.GetRandom(0, 100))

		## Random local timer
		self.RecvSetLocalTimer(app.GetRandom(60, 3600))

	def	OnUpdate(self):
		## Process timers
		for (rVar, rObj, sTxt) in ((self.ttGlobalTimerEnd, self.Objects["Global_TimeLeft"], localeInfo.DUNGEON_TASK_GLOBAL_TL), (self.ttLocalTimerEnd, self.Objects["Stage_TimeLeft"], localeInfo.DUNGEON_TASK_STAGE_TL)):
			if rVar >= app.GetTime():
				iDelta = rVar-app.GetTime()
				rObj.SetText(sTxt % ("-" if iDelta == 0 else localeInfo.SecondToDHMS(iDelta)))

