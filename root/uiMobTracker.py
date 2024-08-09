from introinterface import GetAssets
import ui, colorInfo
import localeInfo
import nonplayer
import grp, app, net
from ui_event import Event

class MobTrackerClass(ui.SimplyWindow):
	SIZE = (520, 480)

	class MobTrackerClassCattegoryButton(ui.RadioButton):
		BUTTON_IMAGES = (GetAssets().format("tracker_manager/btn_0.png"), GetAssets().format("tracker_manager/btn_1.png"), GetAssets().format("tracker_manager/btn_1.png"))

		def __init__(self):
			super(MobTrackerClass.MobTrackerClassCattegoryButton, self).__init__()
			self.__Initialize()

		def __del__(self):
			super(MobTrackerClass.MobTrackerClassCattegoryButton, self).__del__()

		## Private
		def __Initialize(self):
			self.key = -1
			self.SetUpVisual(self.BUTTON_IMAGES[0])
			self.SetOverVisual(self.BUTTON_IMAGES[1])
			self.SetDownVisual(self.BUTTON_IMAGES[2])

		def SetParent(self, parent):
			super(MobTrackerClass.MobTrackerClassCattegoryButton, self).SetParent(parent)

			self.SAFE_SetEvent(parent.SelectItem, self)

			#@Public Methods
		def BindInformations(self, setKey):
			self.key = setKey
			self.SetText("{} {}".format(colorInfo.Colorize("Lv {}.".format(nonplayer.GetMonsterLevel(setKey)), 0xFFc2b883), colorInfo.Colorize(nonplayer.GetMonsterName(setKey), 0xFF944945)))

		def GetKey(self):
			return self.key

		def Show(self):
			super(MobTrackerClass.MobTrackerClassCattegoryButton, self).Show()
		
		def Hide(self):
			super(MobTrackerClass.MobTrackerClassCattegoryButton, self).Hide()

	class MobTrackerClassContentElement(ui.SimplyWindow):
		SIZE = (296, 26)
		BUTTON_IMAGES = (GetAssets().format("tracker_manager/btn_0.png"), GetAssets().format("tracker_manager/btn_1.png"), GetAssets().format("tracker_manager/btn_1.png"))

		def __init__(self):
			super(MobTrackerClass.MobTrackerClassContentElement, self).__init__("UI", ("float", "attach"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)

		def __del__(self):
			super(MobTrackerClass.MobTrackerClassContentElement, self).__del__()

		## Private
		def __Initialize(self):
			## Base
			base = ui.MakeExpandedImageBox(self, GetAssets().format("tracker_manager/content_element_0.png"), 0, 0)
			self.AppendObject("base", base)

		def __Destroy(self):
			self.windowConfig["data"] = {}

		def __FormatTime(self, time):
			return ("|Etracker/clock|e " + colorInfo.Colorize(localeInfo.SecondToHMS(time - app.GetTime()), 0xFFf6af95) if time >= app.GetTime() else colorInfo.Colorize("Alive", 0xFF5c873c))

			#@Public Methods
		def BindInformations(self, parent, iterator, data):
			self.windowConfig["data"] = data

			self.GetObject("base").LoadImage(GetAssets().format("tracker_manager/content_element_{}.png".format(int(data["id"] % 2 == 0))))

			## Number
			number = ui.MakeTextLine(self.GetObject("base"), False, True, 13, -1, "{}.".format(colorInfo.Colorize(str(iterator + 1), 0xFFc2b883)))
			self.AppendObject("number", number)

			## State
			time_space = ui.Window()
			time_space.SetParent(self.GetObject("base"))
			time_space.SetSize(80, self.GetObject("base").GetHeight())
			time_space.SetPosition(30, 0)
			time_space.Show()
			time_space.text = ui.MakeTextLine(time_space, True, True, 0, 0)

			time_space.text.SetText(self.__FormatTime(data["delay"]))
			self.AppendObject("time", time_space)

			## Coordinates
			coordinates_space = ui.Window()
			coordinates_space.SetParent(self.GetObject("base"))
			coordinates_space.SetSize(80, self.GetObject("base").GetHeight())
			coordinates_space.SetPosition(110, 0)
			coordinates_space.Show()
			coordinates_space.text = ui.MakeTextLine(coordinates_space, True, True, 0, 0)

			coordinates_space.text.SetText(colorInfo.Colorize("({}, {})".format(data["cords"][0] / 100, data["cords"][1] / 100), 0xFFc2b883))
			self.AppendObject("coordinates", coordinates_space)

			## Button
			_buttonsImagePath = [GetAssets().format("tracker_manager/"),\
								"btn_teleport_0.png", "btn_teleport_1.png", "btn_teleport_2.png"]
			
			button = ui.MakeButton(self.GetObject("base"), 190, 1, "", *_buttonsImagePath, text = "Teleport")
			button.SetEvent(Event(parent.Teleport, data["id"]))

			self.AppendObject("button", button)

		def AppendDelay(self, iDelay):
			self.windowConfig["data"]["delay"] = iDelay
		
		def GetKey(self):
			return self.windowConfig["data"].get("key", -1)

		def GetID(self):
			return self.windowConfig["data"].get("id", -1)

		def Show(self):
			super(MobTrackerClass.MobTrackerClassContentElement, self).Show()
		
		def Hide(self):
			super(MobTrackerClass.MobTrackerClassContentElement, self).Hide()

		def OnUpdate(self):
			self.GetObject("time").text.SetText(self.__FormatTime(self.windowConfig["data"]["delay"]))

		OnPressExitKey = OnPressEscapeKey = lambda *args, **kwargs : None

	def __init__(self):
		super(MobTrackerClass, self).__init__("UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)

	def __del__(self):
		super(MobTrackerClass, self).__del__()

		# Private Methods
	def __Initialize(self):
		self.__CreateInterface()
		self.windowConfig["CONTROLS"] = dict()

	def __Destroy(self):
		self.windowConfig["CONTROLS"] = dict()

	def __CreateInterface(self):
		## Base
		board = ui.MainBoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetSize(*self.GetSize())
		board.SetTitleName("Tracker")
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.Show()

		self.AppendObject("board", board)

		## Main Element
		image = ui.MakeExpandedImageBox(self.GetObject("board"), GetAssets().format("tracker_manager/main_bg.png"), 3, 28)
		header = ui.MakeExpandedImageBox(image, GetAssets().format("tracker_manager/main_header.png"), 0, 5)
		header.SetWindowHorizontalAlignCenter()

		text = ui.MakeTextLine(header, x = 1, y = -5)
		text.SetText(colorInfo.Colorize("", 0Xffcdcdcd))

		render = ui.MakeRenderTarget(image, lSize = (300, 200), lPos = (5, 30), sBackground = GetAssets().format("tracker_manager/render_transparent.png"))

		info_image = ui.MakeExpandedImageBox(image, GetAssets().format("tracker_manager/main_info_background.png"), 0, 239)
		info_image.SetWindowHorizontalAlignCenter()
		info_image.text = [ui.TextLine() for _ in range(3)]
		yPos = 7
		for _ in info_image.text:
			_.SetParent(info_image)
			_.SetPosition(0, yPos)
			_.SetWindowHorizontalAlignCenter()
			_.SetHorizontalAlignCenter()
			_.SetText("")
			_.SetPackedFontColor(0xFFc2b883)
			_.Show()
			yPos += 21

		clipper_header = ui.MakeExpandedImageBox(image, GetAssets().format("tracker_manager/main_header.png"), 0, 314)
		clipper_header.SetWindowHorizontalAlignCenter()
		clipper_header.text = ui.MakeTextLine(clipper_header, x = 1, y = -5)
		clipper_header.text.SetText(colorInfo.Colorize("Lokacje", 0Xffcdcdcd))

		tmp = self.MobTrackerClassContentElement()

		clipper = ui.ListBoxEx()
		clipper.SetParent(image)
		clipper.SetSize(image.GetWidth(), tmp.GetHeight() * 4)
		clipper.SetPosition((image.GetWidth() - tmp.GetWidth()) / 2, clipper_header.GetLocalPosition()[1] + header.GetHeight() - 2)
		clipper.SetItemSize(tmp.GetWidth(), tmp.GetHeight())
		clipper.SetItemStep(tmp.GetHeight() - 1)
		clipper.SetViewItemCount(4)
		clipper.Show()

		self.AppendObject("main-content", (image, header, text, render, info_image, clipper_header, clipper))

		## Cattegory
		image = ui.MakeExpandedImageBox(self.GetObject("board"), GetAssets().format("tracker_manager/right_bg.png"), 0, 28)
		image.SetPosition(image.GetWidth() + 3, 28)
		image.SetWindowHorizontalAlignRight()

		header = ui.MakeExpandedImageBox(image, GetAssets().format("tracker_manager/right_header.png"), 0, 5)
		header.SetWindowHorizontalAlignCenter()

		text = ui.MakeTextLine(header, x = 1, y = -5)
		text.SetText(colorInfo.Colorize("Boss List", 0Xffcdcdcd))

		tmp = self.MobTrackerClassCattegoryButton()

		clipper = ui.ListBoxEx()
		clipper.SetParent(image)
		clipper.SetSize(image.GetWidth(), tmp.GetHeight() * 3)
		clipper.SetPosition((image.GetWidth() - tmp.GetWidth()) / 2, header.GetLocalPosition()[1] + header.GetHeight())
		clipper.SetItemSize(tmp.GetWidth(), tmp.GetHeight())
		clipper.SetItemStep(tmp.GetHeight() + 1)
		clipper.SetViewItemCount(3)
		clipper.SetSelectEvent(ui.__mem_func__(self.__SelectSet))
		clipper.Show()

		self.AppendObject("right-content", (image, header, text, clipper))

	def __SelectSet(self, set):
		for oset in self.GetObject("right-content", 3).itemList:
			if oset == set:
				oset.Down()
			else:
				oset.SetUp()

		## We have to clear whole data list, or update it atleast!
		self.GetObject("main-content", 6).RemoveAllItems()
		if self.windowConfig["CONTROLS"].has_key(set.GetKey()):
			self.GetObject("main-content", 2).SetText("Lv. {} {}".format(nonplayer.GetMonsterLevel(set.GetKey()), colorInfo.Colorize(nonplayer.GetMonsterName(set.GetKey()), 0xFFc2b883)))
			self.GetObject("main-content", 3).SetRenderTarget(set.GetKey())

			self.GetObject("main-content", 4).text[0].SetText("Czas odnowienia: {}".format(colorInfo.Colorize(localeInfo.SecondToMS(self.windowConfig["CONTROLS"][set.GetKey()]["cooldown"]), 0xFFcdcdcd)))
			# self.GetObject("main-content", 4).text[1].SetText("Siemanko")
			# self.GetObject("main-content", 4).text[2].SetText("Siemanko")

			for key, data in self.windowConfig["CONTROLS"][set.GetKey()]["elements"].items():
				obj = self.MobTrackerClassContentElement()
				obj.BindInformations(self, self.GetObject("main-content", 6).GetItemCount(), data)
				self.GetObject("main-content", 6).AppendItem(obj)

	def ClearSet(self):
		self.windowConfig["CONTROLS"] = dict()
		self.GetObject("main-content", 3).DestroyRender()
		self.GetObject("right-content", 3).RemoveAllItems()
		self.GetObject("main-content", 6).RemoveAllItems()

	def RegisterSet(self, iKey, iID, iCooldown, iDelay, lPos = (0, 0)):
		if self.windowConfig["CONTROLS"].has_key(iKey):
			if not self.GetObject("main-content", 6).IsEmpty():
				for obj in self.GetObject("main-content", 6).itemList:
					if obj.GetKey() == iKey and obj.GetID() == iID:
						self.GetObject("main-content", 6).itemList[iID - 1].AppendDelay(iDelay)
						self.windowConfig["CONTROLS"][iKey]["elements"][iID]["delay"] = iDelay
						break
				return

			self.windowConfig["CONTROLS"][iKey]["elements"][iID] = { "key" : iKey, "id" : iID, "delay" : iDelay, "cords" : lPos}
			return

		self.windowConfig["CONTROLS"][iKey] = { "cooldown" : iCooldown, "elements" : {} }
		self.windowConfig["CONTROLS"][iKey]["elements"][iID] = { "key" : iKey, "id" : iID, "delay" : iDelay, "cords" : lPos }

		obj = self.MobTrackerClassCattegoryButton()
		obj.BindInformations(iKey)

		self.GetObject("right-content", 3).AppendItem(obj)

	def Teleport(self, id):
		net.SendChatPacket("/request_tracker_teleport {}".format(id))
		self.Close()
	
	def Close(self):
		self.Hide()

	# OnPressExitKey = OnPressEscapeKey = lambda *args, **kwargs : None