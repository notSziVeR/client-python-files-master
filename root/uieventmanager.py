import ui
import app
import net
import wndMgr
import uiCommon
import uiToolTip
import localeInfo

from _weakref import proxy

EVENT_LIST = {
				"SERVER_RATE" : ("server_rate.tga", "server_rate"),
				"GM_HIDE_AND_SEEK" : ("gm_hide_and_seek.tga", "gm_hide_and_seek"),
				"OX_EVENT" : ("ox_event.tga", "ox_event"),
				"MOON_TREASURE" : ("moon_treasure.tga", "moon_treasure"),
				"METIN_DEFEND" : ("metin_defend.tga", "metin_defend"),
			}

EVENT_TOOLTIP = {
					"SERVER_RATE" : (localeInfo.EVENT_MANAGER_TITLE_1, localeInfo.EVENT_MANAGER_DESC_1),
					"GM_HIDE_AND_SEEK" : (localeInfo.EVENT_MANAGER_TITLE_2, localeInfo.EVENT_MANAGER_DESC_2),
					"OX_EVENT" : (localeInfo.EVENT_MANAGER_TITLE_3, localeInfo.EVENT_MANAGER_DESC_3),
					"MOON_TREASURE" : (localeInfo.EVENT_MANAGER_TITLE_4, localeInfo.EVENT_MANAGER_DESC_4),
					"METIN_DEFEND" : (localeInfo.EVENT_MANAGER_TITLE_5, localeInfo.EVENT_MANAGER_DESC_5),
				}

def	IncrementBeyondValue(val, max_val):
	val += 1
	if val >= max_val:
		val = 0

	return val

EVENT_TITLE_COLOUR = 0xff12c35e
EVENT_DESC_COLOUR = 0xff12b2ff
EVENT_TIME_COLOUR = 0xffefeb2d

class EventManager(ui.BoardWithTitleBar):
	class EventElement(ui.ThinBoard):
		def	__init__(self, parent, key, image):
			ui.ThinBoard.__init__(self)
			self.key = key
			self.parent = parent
			self.time_data = 0
			self.enable = True
			self.toolTip = self.__CreateToolTip()
			self.SetParent(parent)
			self.__LoadWindow(image)

		def	__def__(self):
			ui.ThinBoard.__del__(self)
			self.EventImage = None
			self.TimeLeft_SlotBar = None
			self.Text_TimeLeft = None
			self.ActionButton = None
			self.enable = False
			self.toolTip = None

			if self.uiTimeWizard:
				self.uiTimeWizard.Close()
				self.uiTimeWizard = None

		def	__LoadWindow(self, image):
			## Main Window
			self.SetSize(120, 140)

			## Event Image
			self.EventImage = ui.ExpandedImageBox()
			self.EventImage.SetParent(self)
			self.EventImage.SetPosition(0, 10)
			self.EventImage.SetWindowHorizontalAlignCenter()
			self.EventImage.LoadImage(image)
			self.EventImage.SetStringEvent("MOUSE_OVER_IN", self.__ShowToolTip)
			self.EventImage.SetStringEvent("MOUSE_OVER_OUT", self.__HideToolTip)
			self.EventImage.Show()

			## TimeLeft SlotBar
			self.TimeLeft_SlotBar = ui.SlotBar()
			self.TimeLeft_SlotBar.SetParent(self)
			self.TimeLeft_SlotBar.SetSize(100, 15)
			self.TimeLeft_SlotBar.SetPosition(0, 91)
			self.TimeLeft_SlotBar.SetWindowHorizontalAlignCenter()
			self.TimeLeft_SlotBar.Show()

			## TimeLeft Text
			self.Text_TimeLeft = ui.TextLine()
			self.Text_TimeLeft.SetParent(self.TimeLeft_SlotBar)
			self.Text_TimeLeft.SetPosition(0, 0)
			self.Text_TimeLeft.SetWindowHorizontalAlignCenter()
			self.Text_TimeLeft.SetWindowVerticalAlignCenter()
			self.Text_TimeLeft.SetHorizontalAlignCenter()
			self.Text_TimeLeft.SetVerticalAlignCenter()
			self.Text_TimeLeft.SetText(localeInfo.SecondToHMS(0))
			self.Text_TimeLeft.Show()

			## Start/Stop Button
			self.ActionButton = ui.Button()
			self.ActionButton.SetParent(self)
			self.ActionButton.SetPosition(0, 115)
			self.ActionButton.SetWindowHorizontalAlignCenter()
			self.ActionButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.ActionButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.ActionButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.ActionButton.SAFE_SetEvent(self.__UseButton)
			self.ActionButton.Show()

			## Time Wizard
			self.uiTimeWizard = uiCommon.TimeWizard()
			self.uiTimeWizard.SetAcceptEvent(lambda argSelf = proxy(self) : net.SendChatPacket("/event_manager_update %s 1 %d" % (argSelf.key, argSelf.uiTimeWizard.GetTimeInSeconds())))
			self.uiTimeWizard.Close()

			self.__UpdateButtonStatus()

		def	GetKey(self):
			return self.key

		def	UpdateTimeData(self, new_time):
			self.time_data = app.GetTime()+new_time
			if self.time_data > 0:
				self.enable = False
			else:
				self.enable = True

			self.__UpdateButtonStatus()

		def	__UpdateButtonStatus(self):
			if self.enable:
				self.ActionButton.SetText(localeInfo.EVENT_MANAGER_PANEL_ENABLE)
			else:
				self.ActionButton.SetText(localeInfo.EVENT_MANAGER_PANEL_DISABLE)

		def	__UseButton(self):
			if not self.enable:
				net.SendChatPacket("/event_manager_update %s 0" % self.key)
			else:
				self.uiTimeWizard.Open()

		def __CreateToolTip(self):
			global EVENT_TITLE_COLOUR, EVENT_DESC_COLOUR, EVENT_TIME_COLOUR
			(title, descList) = EVENT_TOOLTIP[self.key]

			toolTip = uiToolTip.ToolTip()
			toolTip.AutoAppendTextLine(title, EVENT_TITLE_COLOUR)
			toolTip.AppendSpace(5)

			for desc in descList.split("|"):
				toolTip.AutoAppendTextLine(desc, EVENT_DESC_COLOUR)

			toolTip.AlignHorizonalCenter()
			return toolTip

		def __ShowToolTip(self):
			if self.toolTip:
				self.toolTip.ShowToolTip()

		def __HideToolTip(self):
			if self.toolTip:
				self.toolTip.HideToolTip()

		def	Close(self):
			self.uiTimeWizard.Close()
			self.Hide()

		def	OnUpdate(self):
			if self.time_data > 0:
				if self.time_data >= app.GetTime():
					self.Text_TimeLeft.SetText(localeInfo.SecondToHMS(self.time_data-app.GetTime()))
				else:
					self.enable = True
					self.__UpdateButtonStatus()

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.EventElements = []
		self.__LoadWindow()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
		self.EventElements = []

	def	__LoadWindow(self):
		global EVENT_LIST
		## Title
		self.SetTitleName(localeInfo.EVENT_MANAGER_PANEL_TITLE)
		self.SetCloseEvent(ui.__mem_func__(self.Close))

		## Main Window
		self.SetSize(120 * 4 + 30, 140 + 140*(len(EVENT_LIST)/4) + 50)
		self.AddFlag("movable")

		## Adding Elements
		c, r = 0, 0
		for k, v in EVENT_LIST.iteritems():
			element = self.EventElement(self, k, "d:/ymir work/ui/game/event_manager/small/%s" % v[0])
			element.SetPosition(15 + (120*r), 40 + (140*c))
			element.Show()
			self.EventElements.append(element)

			r = IncrementBeyondValue(r, 4)
			if r == 0:
				c += 1

		self.SetCenterPosition()
		self.SetTop()
		self.Hide()

	def	UpdateEventElement(self, key, new_time):
		for element in self.EventElements:
			if element.GetKey() == key:
				element.UpdateTimeData(new_time)

	def	Clear(self):
		for obj in self.EventElements:
			obj.Close()

	def	Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def	Close(self):
		self.Hide()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.Open()

class EventLayer(ui.Window):

	WINDOW_BASE_SIZE = (115, 94)
	MINIMAP_HEIGHT = 200

	class EventImage(ui.ImageBox):
		def	__init__(self, parent, my_key, end_time):
			ui.ImageBox.__init__(self)
			self.SetParent(parent)
			self.parent = parent
			self.my_key = my_key
			self.end_time = end_time
			self.toolTip = self.__CreateToolTip()
			self.__LoadWindow()

		def	__del__(self):
			ui.ImageBox.__del__(self)
			self.my_key = 0
			self.end_time = 0
			self.toolTip = None

		def	__LoadWindow(self):
			global EVENT_LIST
			self.LoadImage("d:/ymir work/ui/game/event_manager/big/%s" % EVENT_LIST[self.my_key][0])

			self.SetStringEvent("MOUSE_OVER_IN", self.__ShowToolTip)
			self.SetStringEvent("MOUSE_OVER_OUT", self.__HideToolTip)
			self.Show()

		def __CreateToolTip(self):
			global EVENT_TITLE_COLOUR, EVENT_DESC_COLOUR, EVENT_TIME_COLOUR
			(title, descList) = EVENT_TOOLTIP[self.my_key]

			toolTip = uiToolTip.ToolTip()
			toolTip.SetParent(self)
			toolTip.SetFollow(False)

			toolTip.AutoAppendTextLine(title, EVENT_TITLE_COLOUR)
			toolTip.AppendSpace(5)

			for desc in descList.split("|"):
				toolTip.AutoAppendTextLine(desc, EVENT_DESC_COLOUR)

			toolTip.AppendSpace(5)
			toolTip.AutoAppendTextLine(localeInfo.EVENT_MANAGER_LAYER_TIMELEFT + self.end_time, EVENT_TIME_COLOUR)

			toolTip.AlignHorizonalCenter()
			toolTip.SetPosition(-toolTip.GetWidth(), 0)
			return toolTip

		def __ShowToolTip(self):
			if self.toolTip:
				self.toolTip.ShowToolTip()

		def __HideToolTip(self):
			if self.toolTip:
				self.toolTip.HideToolTip()

	def	__init__(self):
		ui.Window.__init__(self)
		self.event_list = {}
		self.Objects = []
		self.__Initialize()

	def	__del__(self):
		ui.Window.__del__(self)
		self.event_list = {}
		self.Objects = []

	def	__Clear(self):
		for obj in self.Objects:
			obj.Hide()
			del obj

		self.Objects = []
		self.SetSize(0, 0)

	def	__Initialize(self):
		## Window Size
		self.SetSize(self.WINDOW_BASE_SIZE[0], self.WINDOW_BASE_SIZE[1])

		## Window Position
		self.SetPosition(wndMgr.GetScreenWidth()-self.WINDOW_BASE_SIZE[0], self.MINIMAP_HEIGHT+50)

		self.SetTop()
		self.Hide()

	def	__RedrawWindow(self, e_key, e_time, bFull = False):
		## Window Size
		self.SetSize(self.WINDOW_BASE_SIZE[0], (self.WINDOW_BASE_SIZE[1]*max(1, len(self.event_list)) if not bFull else self.WINDOW_BASE_SIZE[1]))

		## Picking last appended event
		if not bFull:
			self.__CreateAndAppendImage(e_key, e_time)
		else:
			self.__Clear()
			for key, val in self.event_list.iteritems():
				self.SetSize(self.WINDOW_BASE_SIZE[0], self.GetHeight()+self.WINDOW_BASE_SIZE[1])
				self.__CreateAndAppendImage(key, val)

		self.SetTop()
		self.Show()

	def	__CreateAndAppendImage(self, e_key, e_time):
		new_obj = self.EventImage(self, e_key, e_time)
		new_obj.SetPosition(0, self.GetHeight()-self.WINDOW_BASE_SIZE[1])
		self.Objects.append(new_obj)

	def	AddEvent(self, e_key, e_time):
		global EVENT_LIST
		if not e_key in EVENT_LIST:
			print "There is no event named: ", e_key
			return

		if not e_key in self.event_list:
			self.event_list[e_key] = e_time
			self.__RedrawWindow(e_key, e_time)

	def	RemoveEvent(self, e_key):
		global EVENT_LIST
		if not e_key in EVENT_LIST:
			print "There is no event named: ", e_key
			return

		if e_key in self.event_list:
			del self.event_list[e_key]
			self.__RedrawWindow(e_key, 0, True)

	def	Close(self):
		self.Hide()

