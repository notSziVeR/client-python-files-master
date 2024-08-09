from _weakref import proxy
import grp, app, wndMgr, item, chat, logsChat,\
 ui, localeInfo, utility, math, uiToolTip

def ConvertTimeStampToFormatedDate(timeStamp):
	from datetime import datetime
	dt_object = datetime.fromtimestamp(timeStamp)
	return dt_object.strftime("%m/%d/%Y, %H:%M:%S")

#Only activate this if we still get some type of lag
ENABLE_EXTEND_OPTIMIZATION = False

class MainLogsChat(ui.NewBoardWithTitleBar):
	class LogLine(ui.ExpandedImageBox):
		"""Static Values!
			Please dont touch on them!"""
		WINDOW_LINE_TEXT_SIZE = (137, 20)
		WINDOW_LINE_TEXT_POSITION = (19, 0)
		#@#

		LINE_BASE_IMAGE = "logline/line_base.tga" #The path of base image from log line
		TEXT_LINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.8) #Color of logs text
		LOG_INFO_IMAGE = "logline/information.tga" #The path of information image from log line

		def __init__(self, mainWnd, logType, logInformation, localPos):
			self.expandedLogInfo = None

			super(MainLogsChat.LogLine, self).__init__()

			if not mainWnd:
				return

			self.__Initialize(mainWnd, logType, logInformation)
			self.__BuildLineWindow(localPos)
			self.__BuildWindowObjects()

		def __del__(self):
			super(MainLogsChat.LogLine, self).__del__()

			#Private Methods
		def __Initialize(self, mainWnd, logType, logInformation):
			self.mainWnd = mainWnd
			self.logType = logType
			self.logInformation = logInformation

			self.initalLogLineEventInformation = [False, False, app.GetTime()]

			self.logSample = self.mainWnd.logHandler.LogLine(None, self.logType, self.logInformation, isSample = True)
			self.logSample.SetParent(self.mainWnd.scrollBoard)
			self.logSample.Hide()

			self.objLogType = None
			self.objWindowLineText = None
			self.objLineText = None
			self.objLogInfo = None

		def __BuildLineWindow(self, localPos):
			self.SetWindowName("MainWindowLogsChatLine")
			self.SetParent(self.mainWnd.scrollBoard)
			self.LoadImage(self.mainWnd.WINDOW_UI_PATH.format(self.LINE_BASE_IMAGE))
			self.SetPosition(*localPos)

			self.Show()

		def __BuildWindowObjects(self):
			self.objLogType = ui.ExpandedImageBox()
			self.objLogType.SetParent(self)
			if self.mainWnd.logHandler:
				if self.logType in self.logSample.LOGS_TYPES_IMAGE_PATH.keys():
					self.objLogType.LoadImage("{}{}.tga".format("icon/", self.logSample.LOGS_TYPES_IMAGE_PATH[self.logType][0]))
			self.objLogType.SetPosition(2, 2)
			self.objLogType.Show()

			self.objWindowLineText = ui.Window()
			self.objWindowLineText.SetParent(self)
			self.objWindowLineText.AddFlag("attach")
			self.objWindowLineText.SetSize(*self.WINDOW_LINE_TEXT_SIZE)
			self.objWindowLineText.SetPosition(*self.WINDOW_LINE_TEXT_POSITION)
			self.objWindowLineText.SetInsideRender(True)
			self.objWindowLineText.Show()

			def GetLogTextCenterXCoord(line_text_size):
				return (-((line_text_size - self.objWindowLineText.GetWidth()) / 2)\
						if line_text_size > self.objWindowLineText.GetWidth() else\
						((self.objWindowLineText.GetWidth() - line_text_size) / 2), 0)

			self.objLineText = ui.TextLine()
			self.objLineText.SetParent(self.objWindowLineText)
			self.objLineText.SetPackedFontColor(self.TEXT_LINE_COLOR)
			self.objLineText.SetWindowVerticalAlignCenter()
			self.objLineText.SetVerticalAlignCenter()
			self.objLineText.SetText(self.__ConvertLogInformationToText())
			log_text_pos = GetLogTextCenterXCoord(self.objLineText.GetTextSize()[0])
			self.objLineText.SetPosition(*log_text_pos)
			self.objLineText.Show()

			can_run_event = (log_text_pos[0] < 0)
			self.initalLogLineEventInformation = [can_run_event, can_run_event, app.GetTime()]

			self.objLogInfo = ui.ExpandedImageBox()
			self.objLogInfo.SetParent(self)
			self.objLogInfo.SetWindowHorizontalAlignRight()
			self.objLogInfo.LoadImage(self.mainWnd.WINDOW_UI_PATH.format(self.LOG_INFO_IMAGE))
			self.objLogInfo.SetPosition((self.objLogInfo.GetWidth() - 1), -1)
			self.objLogInfo.SetStringEvent("MOUSE_OVER_IN", ui.__mem_func__( self.ExpandLogInfo))
			self.objLogInfo.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__( self.HideExpandedLogInfo))
			self.objLogInfo.Show()

		def __ConvertLogInformationToText(self):
			(quantity, itemVnum, logTime) = self.logInformation
			log_text = ("[" + self.logSample.LOG_QUANTITY_CONVERT(quantity)[0] +\
					("x] " if self.logType not in [logsChat.LOG_TYPE_YANG, logsChat.LOG_TYPE_GAYA] else ""))

			if itemVnum:
				item.SelectItem(itemVnum)
				log_text += item.GetItemName()

			return log_text

			#Public Methods
		def ExpandLogInfo(self):
			if not (self.logSample or\
					objLogType):
				return

			logTypeEmoji = "|E{}|e".format(self.logSample.LOGS_TYPES_IMAGE_PATH[self.logType][0])
			typeInformationText = localeInfo.MAIN_LOGS_CHAT_WINDOW_EXPANDED_TYPE_TXT.format(self.logSample.LOG_QUANTITY_CONVERT(None)[1], logTypeEmoji)
			timeInformationText = localeInfo.MAIN_LOGS_CHAT_WINDOW_EXPANDED_HOUR_TXT.format(ConvertTimeStampToFormatedDate(self.logInformation[2]))

			lTIT, lHIT = (len(typeInformationText) - len(logTypeEmoji)), len(timeInformationText)
			thinBoardWidth = ((150 + (lTIT if lTIT > lHIT else lHIT) * 2) + (self.objLogType.GetWidth() * 2))

			if not self.expandedLogInfo:
				self.expandedLogInfo = uiToolTip.ToolTip(100)
				self.expandedLogInfo.HideToolTip()

			self.expandedLogInfo.ClearToolTip()
			self.expandedLogInfo.SetThinBoardSize(thinBoardWidth)
			self.expandedLogInfo.SetTitle(localeInfo.MAIN_LOGS_CHAT_WINDOW_EXPANDED_INFO_TITLE)
			self.expandedLogInfo.AppendSpace(5)
			self.expandedLogInfo.AppendTextLine(typeInformationText)
			self.expandedLogInfo.AppendHorizontalLine()
			self.expandedLogInfo.AppendTextLine(timeInformationText)
			self.expandedLogInfo.ShowToolTip()

		def HideExpandedLogInfo(self):
			if not self.expandedLogInfo:
				return

			self.expandedLogInfo.HideToolTip()

		def ReloadLogsLinesPositions(self):
			if not (self.objLineText or self.logSample):
				return

			(canRunEvent, rightSideEventState, lastEventTime) = self.initalLogLineEventInformation
			if not canRunEvent or\
				(app.GetTime() < (lastEventTime + self.logSample.TEXT_ANIMATION_PAUSE_TIME)):
				return

				#Lambda funcs declaration
			_positionAdjust = lambda x , y : (x + y) if rightSideEventState else (x - y)
			_runLocalEvent = lambda :	(self.objLineText.GetLocalPosition()[0] < self.logSample.ANIMATION_INIT_X_COMFORT_EYE)\
										if rightSideEventState else\
										((self.objLineText.GetLocalPosition()[0] + self.objLineText.GetTextSize()[0]) > self.objWindowLineText.GetWidth())
				#@#

			if _runLocalEvent():
				self.objLineText.SetPosition(*tuple(_positionAdjust(x, y) for x, y in zip(self.objLineText.GetLocalPosition(), [1, 0])))
			else:
				self.initalLogLineEventInformation[1] = (not rightSideEventState)
				self.initalLogLineEventInformation[2] = app.GetTime()

		def Hide(self):
			self.HideExpandedLogInfo()
			super(MainLogsChat.LogLine, self).Hide()

	"""Static Values!
		Please dont touch on them!"""
	WINDOW_SIZE = (250, 250)
	PEEK_WINDOW_SIZE = (175, 147)
	MAGIC_VALUE = 21
	#@#

	SCROLL_SPEED = 50 #Speed of scroll
	WINDOW_UI_PATH = "assets/ui/logschat/{}" #Main assets path of system

	def __init__(self):
		super(MainLogsChat, self).__init__()
		logsChat.UpdateLogChatHandler(logsChat.MAIN_HANDLER, self)

		self.__Initialize()
		self.__BuildWindow()
		self.__BuildWindowObjects()

	def __del__(self):
		logsChat.UpdateLogChatHandler(logsChat.MAIN_HANDLER, None)
		super(MainLogsChat, self).__del__()

		#Private Methods
	def __Initialize(self):
		self.interface = None
		self.logHandler = None

		self.logsLines = []
		#START FLOOD PROTECTION
		self.logsQueue = []
		#END FLOOD PROTECTION

		self.thinBoardBase = None
		self.separatorText = None
		self.peekWindow = None
		self.logsState = None
		self.scrollBoard = None
		self.scrollBar = None

		self.bInitialCall = True

	def __BuildWindow(self):
		self.SetWindowName("MainWindowLogsChat")
		self.SetSize(*self.WINDOW_SIZE)
		self.AddFlag("movable")
		self.AddFlag("float")
		self.AddFlag("animate")
		self.SetTitleName(localeInfo.MAIN_LOGS_CHAT_WINDOW_TITLE)
		self.SetCloseEvent(ui.__mem_func__(self.Hide))
		self.SetCenterPosition()

	def __BuildWindowObjects(self):
		self.thinBoardBase = ui.BoxedBoard()
		self.thinBoardBase.SetParent(self)
		self.thinBoardBase.AddFlag("attach")
		self.thinBoardBase.SetPosition(6, 28)
		self.thinBoardBase.SetSize(*tuple(x-y for x,y in zip(self.WINDOW_SIZE, [13, 35])))
		self.thinBoardBase.Show()

		self.background = ui.ExpandedImageBox()
		self.background.SetParent(self.thinBoardBase)
		self.background.SetPosition(2, 17)
		self.background.LoadImage(self.WINDOW_UI_PATH.format("background.tga"))
		self.background.Show()

		self.peekWindow = ui.Window()
		self.peekWindow.SetParent(self.background)
		self.peekWindow.AddFlag("attach")
		self.peekWindow.SetSize(*self.PEEK_WINDOW_SIZE)
		self.peekWindow.SetPosition(28, 29)
		self.peekWindow.SetInsideRender(True)
		self.peekWindow.Show()

		self.logsState = ui.TextLine()
		self.logsState.SetParent(self.peekWindow)
		self.logsState.SetWindowHorizontalAlignCenter()
		self.logsState.SetHorizontalAlignCenter()
		self.logsState.SetWindowVerticalAlignCenter()
		self.logsState.SetVerticalAlignCenter()
		self.logsState.SetText(localeInfo.MAIN_LOGS_CHAT_NO_LOGS)
		self.logsState.Show()

		self.scrollBoard = ui.Window()
		self.scrollBoard.SetParent(self.peekWindow)
		self.scrollBoard.AddFlag("attach")
		self.scrollBoard.SetPosition(0, 0)
		self.scrollBoard.Show()

		self.separatorText = ui.ExpandedImageBox()
		self.separatorText.SetParent(self.background)
		self.separatorText.SetPosition(27, 176)
		self.separatorText.LoadImage(self.WINDOW_UI_PATH.format("separator_text.tga"))
		self.separatorText.Show()

		self.__RegisterScrollBar()
		self.__ReloadWindowObjects()

	def __RegisterScrollBar(self):
		if app.ENABLE_MOUSE_WHEEL_EVENT:
			self.SetScrollWheelEvent(self.OnMouseWheel)
		self.scrollBar = utility.ReworkedScrollBar()
		self.scrollBar.SetParent(self.background)
		self.scrollBar.SetPosition(self.peekWindow.GetLocalPosition()[0] + self.peekWindow.GetWidth(), self.peekWindow.GetLocalPosition()[1])
		self.scrollBar.SetSize(7, self.peekWindow.GetHeight())
		self.scrollBar.SetScrollEvent(self.__OnScroll)
		self.scrollBar.SetScrollSpeed(self.SCROLL_SPEED)

		self.__ChangeScrollbar()

	def __ChangeScrollbar(self):
		if not self.scrollBar:
			return

		if self.scrollBoard.GetHeight() <= self.peekWindow.GetHeight():
			self.scrollBar.Hide()
		else:
			self.scrollBar.SetScale(self.peekWindow.GetHeight(), self.scrollBoard.GetHeight())
			self.scrollBar.SetPosScale((float(1) * abs(self.scrollBoard.GetLocalPosition()[1])) / (self.scrollBoard.GetHeight() - self.peekWindow.GetHeight()))
			self.scrollBar.Show()

	def __OnScroll(self, fScale):
		if not self.scrollBoard or\
			(self.scrollBar and self.scrollBar.GetBlockMoveState() is True):
			return

		curr = min(0, max(math.ceil((self.scrollBoard.GetHeight() - self.peekWindow.GetHeight()) * fScale * -1.0), -self.scrollBoard.GetHeight() + self.peekWindow.GetHeight()))
		self.scrollBoard.SetPosition(0, curr)

	def __ReloadScrollBoard(self):
		if not self.scrollBoard:
			return

		scrollBoardHeight = ((self.MAGIC_VALUE + self.logsLines[0].GetLocalPosition()[1]) if self.logsLines else 0)
		if self.scrollBoard.GetHeight() == scrollBoardHeight:
			return

		self.scrollBoard.SetSize(self.peekWindow.GetWidth(), scrollBoardHeight)

	def __ReloadLogsStateText(self):
		if not self.logsState:
			return

		self.logsState.Show() if not (self.logsLines and self.IsShow()) else self.logsState.Hide()

	def __ReloadWindowObjects(self):
		self.__ReloadScrollBoard()
		self.__ChangeScrollbar()
		self.__ReloadLogsStateText()

	def __ClearLogsLines(self):
		for obj in self.logsLines: obj.Hide()
		del self.logsLines[:]
		#START FLOOD PROTECTION
		del self.logsQueue[:]
		#END FLOOD PROTECTION

	def __LoadLogsLines(self):
		self.__ClearLogsLines()

		ret = logsChat.GetLogsInformations()
		if not ret:
			return

		logLineIdx = 1
		logsLinesLenght = len(ret)
		for (logType, logInformation) in ret:
			pre_y = ((logsLinesLenght - logLineIdx) * self.MAGIC_VALUE)
			self.logsLines.append(self.LogLine(self, logType, logInformation, (0, pre_y)))
			logLineIdx += 1

	def __ReloadLogLinesPositions(self):
		if not self.logsLines:
			return

		for logLine in self.logsLines:
			logLine.ReloadLogsLinesPositions()

	def __AddNewLog(self, logType, logInformation):
		log_y = (self.logsLines[-1].GetLocalPosition()[1] if self.logsLines else 0)
		self.logsLines.append(self.LogLine(self, logType, logInformation, (0, (log_y - self.MAGIC_VALUE))))

		#Public Methods
	def BINARY_HandlingLogInformation(self, logType, logInformation):
		#START FLOOD PROTECTION
		if len(self.logsLines) >= logsChat.AVOID_FLOOD_MAX_LOGS:

			if len(self.logsQueue) >= logsChat.MAX_LOGS_QUEUE and ENABLE_EXTEND_OPTIMIZATION:
				self.logsQueue.pop()

			self.logsQueue.insert(0, [logType, logInformation])
			return
		#END FLOOD PROTECTION

		self.__AddNewLog(logType, logInformation)

	def BINARY_ClearLogsInformation(self):
		self.__ClearLogsLines()

	def OnMouseWheel(self, length):
		if self.scrollBar and self.scrollBar.IsShow():
			return self.scrollBar.OnRunMouseWheelEvent(length)

		return False

	def OnUpdate(self):
		self.__ReloadLogLinesPositions()
		self.__ReloadWindowObjects()

		if self.logsLines:
			if (self.logsLines[-1].GetLocalPosition()[1] >= 0):
				# START FLOOD PROTECTION
				if self.logsQueue:
					self.__AddNewLog(*self.logsQueue[-1])

					self.logsQueue.pop()
					self.logsLines.pop(0)
				# END FLOOD PROTECTION

				self.scrollBar.SetBlockMoveEvent(False)
				return

			self.scrollBar.SetBlockMoveEvent(True)
			logsLinesLenght = len(self.logsLines)
			for logLineIdx in xrange(logsLinesLenght):
				tmpLog = self.logsLines[logLineIdx]

				log_y = tmpLog.GetLocalPosition()[1]
				#START FLOOD PROTECTION
				pre_y = ((logsLinesLenght + len(self.logsQueue) - logLineIdx) * self.MAGIC_VALUE)
				#END FLOOD PROTECTION
				if (log_y < pre_y):
					tmpLog.SetPosition(0, (log_y + 1))

	def BindInterface(self, interface):
		self.interface = proxy(interface)

	def BindLogsChatHandler(self, handler):
		self.logHandler = proxy(handler)

	def OnPressEscapeKey(self):
		self.Hide()
		return True

	def Show(self):
		if self.bInitialCall:
			self.__LoadLogsLines()
			self.bInitialCall = False

		super(MainLogsChat, self).Show()
		self.SetTop()

	def Hide(self):
		super(MainLogsChat, self).Hide()

"""This window only gonna appear when game client resolution allow them.
	In lower resolutions this window dont is used, but your methods yes\
	this class handles all logs in chat window."""
class LogsChatHandler(ui.ThinBoard):
	class LogLine(ui.Window):
		"""Static Values!
			Please dont touch on them!"""
		LOG_LINE_SIZE = (140, 14)
		#@#

		SPACE_BETWEEN_LOG_AND_IMAGE_TYPE = 5 #Space between log type image and log text
		TEXT_LINE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.8) #Color of logs text

		"""Syntax: LOG_TYPE : [image_path, adjust_pos_y]
			Brief:
				-> The adjust_pos_y was created to compensate the difference in sizes of\
					the various images, and to be able to center them in the best way"""
		LOGS_TYPES_IMAGE_PATH = {
			logsChat.LOG_TYPE_YANG : ["logschat/types/yang", 2],
			logsChat.LOG_TYPE_PICKUP : ["logschat/types/pickup", 1],
			logsChat.LOG_TYPE_EXCHANGE :["logschat/types/exchange", 1],
			logsChat.LOG_TYPE_SHOP : ["logschat/types/shop", 1],
			logsChat.LOG_TYPE_CHEST : ["logschat/types/chest", 1]
		}

		LOW_RESOLUTION_LOGS_IDENTIFY_EMOJI = "|Elogschat/log_chat_icon|e" #Arrow for identify log lines in chat lines

		"""Syntax: LOG_TYPE : convert_function, convert_text
			Brief:
				-> Converts the various types of quantities to text according to the type of the log in first element,\
					in second convert type number to information text
		"""
		LOG_QUANTITY_CONVERT = lambda obj, quantity :\
		{
			logsChat.LOG_TYPE_YANG : [localeInfo.NumberToMoneyDotStringWithoutMonetary(quantity), localeInfo.LOGS_CHAT_TYPE_YANG],
			logsChat.LOG_TYPE_PICKUP : [localeInfo.NumberToMoneyDotStringWithoutMonetary(quantity), localeInfo.LOGS_CHAT_TYPE_PICKUP],
			logsChat.LOG_TYPE_EXCHANGE : [localeInfo.NumberToMoneyDotStringWithoutMonetary(quantity), localeInfo.LOGS_CHAT_TYPE_EXCHANGE],
			logsChat.LOG_TYPE_SHOP : [localeInfo.NumberToMoneyDotStringWithoutMonetary(quantity), localeInfo.LOGS_CHAT_TYPE_SHOP],
			logsChat.LOG_TYPE_CHEST : [localeInfo.NumberToMoneyDotStringWithoutMonetary(quantity), localeInfo.LOGS_CHAT_TYPE_CHEST]
		}[getattr(obj, "logType")]

		TEXT_ANIMATION_PAUSE_TIME = 1 #Time when the text animation is stopped after the event phase change
		ANIMATION_INIT_X_COMFORT_EYE = 4 #X coordinate where the animation stop from right to left stop

		def __init__(self, parent, logType, logInformation, localPos = (5, 5), isSample = False):
			super(LogsChatHandler.LogLine, self).__init__()

			self.__Initialize(parent, logType, logInformation)

			if not isSample:
				self.__BuildLineWindow(localPos)
				self.__BuidLineObjects()
				self.__AdjustObjectsPositions()

		def __del__(self):
			super(LogsChatHandler.LogLine, self).__del__()

			#Private Methods
		def __Initialize(self, parent, logType, logInformation):
			self.mainWnd = parent
			self.logType = logType
			self.logInformation = logInformation

			self.initalLogLineEventInformation = [False, False, app.GetTime()]
			self.rightSideEvent = True

			self.objLineText = None

		def __BuildLineWindow(self, localPos):
			self.SetWindowName("WindowLogsChatLine")
			self.SetParent(self.mainWnd.peekWindow)
			self.SetSize(*self.LOG_LINE_SIZE)
			self.SetPosition(*localPos)

		def __BuidLineObjects(self):
				#Build Log Text
			self.objLineText = ui.TextLine()
			self.objLineText.SetParent(self)
			self.objLineText.SetPackedFontColor(self.TEXT_LINE_COLOR)
			self.objLineText.SetWindowVerticalAlignCenter()
			self.objLineText.SetVerticalAlignCenter()
			self.objLineText.SetText(self.ConvertLogInformationToText())
			self.objLineText.Show()

				#Build Log Type Image
			self.objLogType = ui.ExpandedImageBox()
			self.objLogType.SetParent(self)
			if self.logType in self.LOGS_TYPES_IMAGE_PATH.keys():
				self.objLogType.LoadImage("{}{}.tga".format("icon/", self.LOGS_TYPES_IMAGE_PATH[self.logType][0]))
			self.objLogType.Show()

				#Others
			self.initialRenderBox = self.objLineText.GetRenderBox()

		def __AdjustObjectsPositions(self):
			if not (self.objLineText or self.objLogType):
				return

			line_text_size = self.objLineText.GetTextSize()[0]
			def GetLogTextCenterXCoord():
				return -((line_text_size - self.GetWidth()) / 2)\
						if line_text_size > self.GetWidth() else\
						((self.GetWidth() - line_text_size) / 2)

			log_text_pos = [(GetLogTextCenterXCoord() - ((self.objLogType.GetWidth() + self.SPACE_BETWEEN_LOG_AND_IMAGE_TYPE) / 2)), 0]
			self.objLineText.SetPosition(*log_text_pos)

			log_type_pos = [(log_text_pos[0] + line_text_size + self.SPACE_BETWEEN_LOG_AND_IMAGE_TYPE),\
							(self.LOGS_TYPES_IMAGE_PATH[self.logType][1] if self.logType in self.LOGS_TYPES_IMAGE_PATH.keys() else 0)]
			self.objLogType.SetPosition(*log_type_pos)

				#Event Related
			can_run_event = (log_text_pos[0] < 0)
			self.initalLogLineEventInformation = [can_run_event, can_run_event, app.GetTime()]

			#Public Methods
		def GetLogLineTextHeight(self):
			return (self.objLineText.GetTextSize()[1] if self.objLineText else 0)

		def ConvertLogInformationToText(self, isLowResolutionText = False):
			(quantity, itemVnum, logTime) = self.logInformation
			log_text = (("|cFFffe3ad+" if not isLowResolutionText else "{}+ ".format(self.LOW_RESOLUTION_LOGS_IDENTIFY_EMOJI)) +\
						"[" + self.LOG_QUANTITY_CONVERT(quantity)[0] +\
						("x]|r " if self.logType not in [logsChat.LOG_TYPE_YANG, logsChat.LOG_TYPE_GAYA] else "]"))

			if self.logType == logsChat.LOG_TYPE_YANG:
				itemVnum = 1

			if itemVnum:
				item.SelectItem(itemVnum)
				log_text += " |cFFffffff" + item.GetItemName()

			if isLowResolutionText and self.logType in self.LOGS_TYPES_IMAGE_PATH.keys():
				log_text += " |E{}|e".format(self.LOGS_TYPES_IMAGE_PATH[self.logType][0])

			return log_text

		def OnUpdate(self):
			if not (self.objLineText or self.objLogType):
				return

			(canRunEvent, rightSideEventState, lastEventTime) = self.initalLogLineEventInformation
			if not canRunEvent or\
				(app.GetTime() < (lastEventTime + self.TEXT_ANIMATION_PAUSE_TIME)):
				return

				#Lambda funcs declaration
			_positionAdjust = lambda x , y : (x + y) if rightSideEventState else (x - y)
			_runLocalEvent = lambda :	(self.objLineText.GetLocalPosition()[0] < self.ANIMATION_INIT_X_COMFORT_EYE)\
										if rightSideEventState else\
										((self.objLogType.GetLocalPosition()[0] + self.objLogType.GetWidth()) > self.GetWidth())
				#@#

			if _runLocalEvent():
				self.objLineText.SetPosition(*tuple(_positionAdjust(x, y) for x, y in zip(self.objLineText.GetLocalPosition(), [1, 0])))
				self.objLogType.SetPosition(*tuple(_positionAdjust(x, y) for x, y in zip(self.objLogType.GetLocalPosition(), [1, 0])))
			else:
				self.initalLogLineEventInformation[1] = (not rightSideEventState)
				self.initalLogLineEventInformation[2] = app.GetTime()

	"""Static Values!
		Please dont touch on them!"""
	WINDOW_SIZE = (150, 215)
	WINDOW_POSITION = (180, wndMgr.GetScreenHeight() - 60)
	#@#

	"""Allow one image in the top of thinboard (is left as false because I still\
		haven't found nor had any good ideas for the image itself)"""
	ALLOW_HEADER_IMAGE = False
	HEADER_IMAGE_PATH = "icon/logschat/header_image.tga" #Path of header image

	def __init__(self):
		super(LogsChatHandler, self).__init__("UI_BOTTOM")
		logsChat.UpdateLogChatHandler(logsChat.LEFT_HANDLER, self)

		self.__Initialize()
		self.__BuildWindow()
		self.__BuildObjects()

	def __del__(self):
		logsChat.UpdateLogChatHandler(logsChat.LEFT_HANDLER, None)
		super(LogsChatHandler, self).__del__()

		#Private Methods
	def __Initialize(self):
		self.interface = None

		self.logsLines = []

		#START FLOOD PROTECTION
		self.logsQueue = []
		#END FLOOD PROTECTION

		self.windowExpanded = False
		self.isExpanding = False

		self.headerImage = None
		self.peekWindow = None
		self.eventWindow = None

	def __BuildWindow(self):
		self.SetWindowName("WindowLogsChat")
		self.SetInsideRender(True)
		self.SetSize(*self.WINDOW_SIZE)
		self.SetPosition(*self.WINDOW_POSITION)

		self.Hide()
		self.SetTop()

	def __BuildObjects(self):
		self.headerImage = ui.ExpandedImageBox()
		self.headerImage.SetParent(self)
		self.headerImage.SetPosition(0, -10)
		self.headerImage.LoadImage(self.HEADER_IMAGE_PATH)
		self.headerImage.Hide() if not self.ALLOW_HEADER_IMAGE else self.headerImage.Show()

		self.peekWindow = ui.Window()
		self.peekWindow.SetParent(self)
		self.peekWindow.AddFlag("attach")
		self.peekWindow.SetSize(*tuple(x - y for x,y in zip(self.WINDOW_SIZE, [0, 10])))
		self.peekWindow.SetPosition(0, 4)
		self.peekWindow.SetInsideRender(True)
		self.peekWindow.Show()

		self.eventWindow = ui.Window()
		self.eventWindow.SetParent(self)
		self.eventWindow.SetSize(*self.WINDOW_SIZE)
		self.eventWindow.SetPosition(0, 0)
		self.eventWindow.SetMouseLeftButtonDownEvent(ui.__mem_func__(self.UpdateWindowState))
		self.eventWindow.Show()

	def __HandleLowResolutionLog(self, logType, logInformation):
		logSample = self.LogLine(None, logType, logInformation, isSample = True)
		logSample.Hide()

		chat.AppendChat(chat.CHAT_TYPE_TALKING, logSample.ConvertLogInformationToText(True))

	def __AddNewLog(self, logType, logInformation):
		log_y = (self.logsLines[-1].GetLocalPosition()[1] if self.logsLines else 0)
		log_y_r = (self.logsLines[-1].GetHeight() if self.logsLines else 14) #14 -> LOG_LINE_SIZE

		self.logsLines.append(self.LogLine(self, logType, logInformation, (5, (log_y - log_y_r))))
		self.logsLines[-1].Show()

	def __ClearLogsLines(self):
		for obj in self.logsLines: obj.Hide()
		del self.logsLines[:]

	def __HandleWindowStatePosition(self):
		if len(self.logsLines) <= 1:
			return

		logHeihgth = self.logsLines[0].GetHeight()
		calcByLogsLines = (len(self.logsLines) * logHeihgth)
		topLimit = (wndMgr.GetScreenHeight() - self.GetHeight() - 25)

		startPos = topLimit
		if calcByLogsLines < self.GetHeight():
			startPos = (wndMgr.GetScreenHeight() - calcByLogsLines - 43)
			if startPos < topLimit:
				startPos = topLimit

		(x, y), initY = self.GetGlobalPosition(), self.WINDOW_POSITION[1]
		if self.windowExpanded: #Expand window
			if y <= startPos:
				self.isExpanding = False
				return

			self.isExpanding = True
			self.SetPosition(x, max(startPos, y - 4))
		elif y < initY: #Hide window event
			self.SetPosition(x, min(initY, y + 4))

	def __HandleLogsAnimation(self):
		if self.isExpanding:
			return

		if self.logsLines:
			if (self.logsLines[-1].GetLocalPosition()[1] >= 0):
				#START FLOOD PROTECTION
				if self.logsQueue:
					self.__AddNewLog(*self.logsQueue[-1])

					self.logsLines.pop(0)
					self.logsQueue.pop()
				#END FLOOD PROTECTION
				return

			logsLinesLenght = len(self.logsLines)
			for logLineIdx in xrange(logsLinesLenght):
				tmpLog = self.logsLines[logLineIdx]

				log_y = tmpLog.GetLocalPosition()[1]
				#START FLOOD PROTECTION
				pre_y = ((logsLinesLenght + len(self.logsQueue) - logLineIdx) * tmpLog.GetHeight()) + 5
				#END FLOOD PROTECTION
				if (log_y < pre_y):
					tmpLog.SetPosition(tmpLog.GetLocalPosition()[0], (log_y + 1))

		#Public Methods
	def BINARY_HandlingLogInformation(self, logType, logInformation):
		if logsChat.GetLowResolutionSystem():
			self.__HandleLowResolutionLog(logType, logInformation)
			return

		#START FLOOD PROTECTION
		if len(self.logsLines) >= logsChat.AVOID_FLOOD_MAX_LOGS:

			if len(self.logsQueue) >= logsChat.MAX_LOGS_QUEUE and ENABLE_EXTEND_OPTIMIZATION:
				self.logsQueue.pop()

			self.logsQueue.insert(0, [logType, logInformation])
			return
		#END FLOOD PROTECTION

		self.__AddNewLog(logType, logInformation)
		if not self.IsShow():
			self.Show()

	def BINARY_ClearLogsInformation(self):
		self.__ClearLogsLines()
		self.Hide()

	def BuildStaticLogsLines(self):
		ret = logsChat.GetLogsInformations()
		if not ret:
			#The window its hidded when was builded, but we confirm here another time
			if self.IsShow():
				self.Hide()
			return

		logLineIdx = 1
		logsLinesLenght = len(ret)
		for (logType, logInformation) in ret:
			pre_y = ((logsLinesLenght - logLineIdx) * 14)  #14 -> LOG_LINE_SIZE
			self.logsLines.append(self.LogLine(self, logType, logInformation, (5, pre_y)))
			self.logsLines[-1].Show()
			logLineIdx += 1

		self.Show()

	def UpdateWindowState(self):
		self.windowExpanded = not self.windowExpanded

	def BindInterface(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def OnUpdate(self):
		self.__HandleWindowStatePosition()
		self.__HandleLogsAnimation()

	def Show(self):
		if logsChat.GetLowResolutionSystem() or\
			not self.logsLines:
			return

		super(LogsChatHandler, self).Show()

	def Hide(self):
		super(LogsChatHandler, self).Hide()
