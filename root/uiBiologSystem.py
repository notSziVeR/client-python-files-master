from introinterface import GetAssets
import ui, localeInfo, uiScriptLocale, colorInfo
import item, player, app, net
from itemWrapper import ItemToolTipDummy
import uiToolTip
from ui_event import Event

def GetAffectString(affectType, affectValue):
	if not affectType:
		return None

	try:
		return localeInfo.AFFECT_DICT[affectType](affectValue)
	except TypeError:
		return "UNKNOWN_VALUE[{}] {}".format(affectType, affectValue)
	except KeyError:
		return "UNKNOWN_TYPE[{}] {}".format(affectType, affectValue)

class BiologMission(ui.SimplyWindow):
	SIZE = (331, 310)
	ADDITIONAL_ITEMS = (71035, 172001)

	class BiologAffectElement(ui.ExpandedImageBox):
		def __init__(self, lConfig = ()):
			super(BiologMission.BiologAffectElement, self).__init__()

			self.__RunPreImageEvent()
			self.__Initialize(lConfig)

			if self.lConfig:
				self.__BuildAffectLine()

		def __del__(self):
			super(BiologMission.BiologAffectElement, self).__del__()

			#Private Methods
		def __RunPreImageEvent(self):
			self.LoadImage(GetAssets().format("biolog_manager/affect_line.png"))
			self.Show()

		def __Initialize(self, lConfig):
			self.lConfig = lConfig
			self.Objects = {}

		def __BuildAffectLine(self):
			applyString = uiToolTip.GetItemToolTipInstance().GetAffectString(self.lConfig[1], self.lConfig[2], False)
			if not applyString:
				return

			strip = applyString.find(":")

			self.Objects["AFF_TYPE"] = self.__GenerateAppendSmallField(197, 0, applyString[:strip])
			self.Objects["AFF_VALUE"] = self.__GenerateAppendSmallField(40, 196, applyString[strip + 1:])

		def __GenerateAppendSmallField(self, iWidth, iX, sTxt):
			newWnd = ui.Window()
			newWnd.SetParent(self)
			newWnd.SetSize(iWidth, self.GetHeight())
			newWnd.SetPosition(iX, 0)
			newWnd.SetWindowVerticalAlignCenter()
			newWnd.Show()

			self.Objects["TXT_%d_%s" % (iX, sTxt)] = ui.MakeTextLine(newWnd)
			self.Objects["TXT_%d_%s" % (iX, sTxt)].SetText(sTxt)

			return newWnd

			#Public Methods
		def Show(self):
			super(BiologMission.BiologAffectElement, self).Show()
		
		def Hide(self):
			super(BiologMission.BiologAffectElement, self).Hide()

	def __init__(self):
		super(BiologMission, self).__init__("UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)

	def __del__(self):
		super(BiologMission, self).__del__()

		# Private Methods
	def __Initialize(self):
		self.__CreateInterface()
		self._toolTip = ItemToolTipDummy(0)
		self.windowConfig["CONTROLS"] = dict()

	def __Destroy(self):
		self._toolTip = None

	def __CreateInterface(self):
		def BuildAdditional(iKey, lPos = (0, 0)):
			slot = ui.SlotWindow()
			slot.SetParent(image)
			slot.SetPosition(*lPos)
			slot.SetSize(33, 33)
			slot.SetOverInItemEvent(Event(self.__OnOverInItem, self.ADDITIONAL_ITEMS[iKey]))
			slot.SetOverOutItemEvent(self.__OnOverOutItem)
			slot.SetSlotBaseImage(GetAssets().format("biolog_manager/slot.png"), 1.0, 1.0, 1.0, 1.0)
			slot.AppendSlot(0, 0, 0, 33, 33)
			slot.Show()

			slot.SetItemSlot(0, self.ADDITIONAL_ITEMS[iKey], 0)

			checkbox = ui.CheckBox(sPath=GetAssets().format("biolog_manager/checkbox_{}"))
			checkbox.SetParent(image)
			checkbox.SetPosition(slot.GetLocalPosition()[0] + slot.GetWidth(), (slot.GetHeight() - checkbox.GetHeight()) / 2)
			checkbox.Show()

			return (slot, checkbox)

		## Base
		board = ui.MainBoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetSize(*self.GetSize())
		board.SetTitleName(localeInfo.BIOLOG_MANAGER_TITLE)
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.Show()

		self.AppendObject("board", board)

		base = ui.MainSubBoard("100")
		base.SetParent(self.GetObject("board"))
		base.SetPosition(5, 31)
		base.SetSize(self.GetObject("board").GetWidth() - base.GetLocalPosition()[0] * 2, self.GetObject("board").GetHeight() - (base.GetLocalPosition()[0] + base.GetLocalPosition()[1]))
		base.Show()

		self.AppendObject("base", base)

		## Top Header
		image = ui.MakeExpandedImageBox(self.GetObject("base"), GetAssets().format("biolog_manager/header_top.png"), 0, 0)
		image.SetWindowHorizontalAlignCenter()

		text = ui.MakeTextLineNew(image, 55, 0, "")
		text.SetWindowVerticalAlignCenter()
		text.SetVerticalAlignCenter()

		button = ui.MakeButton(image, 70, 0, "", GetAssets().format("biolog_manager/"), "bn1.png", "bn2.png", "bn3.png")
		button.SetWindowHorizontalAlignRight()
		button.SetWindowVerticalAlignCenter()
		button.SetEvent(Event(self.__RequestMissions))
		self.AppendObject("top_header", (image, text, button))

		## Progress Content
		image = ui.MakeExpandedImageBox(self.GetObject("base"), GetAssets().format("biolog_manager/required_name_background.png"), 0, self.GetObject("top_header", 0).GetLocalPosition()[1] + self.GetObject("top_header", 0).GetHeight())
		image.SetWindowHorizontalAlignCenter()
		
		text = ui.MakeTextLineNew(image, 5, -1, "")
		text.SetWindowVerticalAlignCenter()
		text.SetVerticalAlignCenter()

		progress = ui.MakeExpandedImageBox(image, GetAssets().format("biolog_manager/gauge.png"), 118, 0)
		progress.SetWindowHorizontalAlignRight()
		progress.SetWindowVerticalAlignCenter()
		progress.SetPercentage(50, 100)

		self.AppendObject("progress_content", (image, text, progress))

		## Main Content
		image = ui.MakeExpandedImageBox(self.GetObject("base"), GetAssets().format("biolog_manager/main_content.png"), 0, self.GetObject("progress_content", 0).GetLocalPosition()[1] + self.GetObject("progress_content", 0).GetHeight())
		image.SetWindowHorizontalAlignCenter()

		## Static width of bar with slot
		WIDTH = 68
		slot = ui.SlotWindow()
		slot.SetParent(image)
		slot.SetPosition((WIDTH - 33) / 2, (image.GetHeight() - 33) / 2)
		slot.SetSize(33, 33)
		slot.SetOverOutItemEvent(self.__OnOverOutItem)
		slot.SetSlotBaseImage(GetAssets().format("biolog_manager/slot.png"), 1.0, 1.0, 1.0, 1.0)
		slot.AppendSlot(0, 0, 0, 33, 33)
		slot.Show()

		header = [ui.TextLine() for _ in range(2)]
		lTexts = (uiScriptLocale.BIOLOG_MANAGER_ADDITIONAL_HEADER, localeInfo.BIOLOG_MANAGER_CHANCE)
		for _ in range(2):
			header[_].SetParent(image)
			header[_].SetText(lTexts[_])
			header[_].Show()

		header[0].SetPosition(70, 10)
		header[1].SetPosition(70, 40)

		checkboxes = [BuildAdditional(0, (170, 1)), BuildAdditional(1, (230, 1))]

		button = ui.MakeButton(image, 150, 36, "", GetAssets().format("biolog_manager/"), "button_0.png", "button_1.png", "button_2.png", localeInfo.BIOLOG_MANAGER_ACCEPT)
		button.SetEvent(Event(self.__CollectItem))
		self.AppendObject("main-content", (image, slot, header, checkboxes, button))

		## Cooldown Content
		image = ui.MakeExpandedImageBox(self.GetObject("base"), GetAssets().format("biolog_manager/time_background_positive.png"), 0, self.GetObject("main-content", 0).GetLocalPosition()[1] + self.GetObject("main-content", 0).GetHeight())
		image.SetWindowHorizontalAlignCenter()

		text = ui.MakeTextLineNew(image, 0, -2, "")
		text.SetWindowHorizontalAlignCenter()
		text.SetWindowVerticalAlignCenter()
		text.SetHorizontalAlignCenter()
		text.SetVerticalAlignCenter()

		checkbox = ui.CheckBox(sPath=GetAssets().format("biolog_manager/checkbox_{}"))
		checkbox.SetParent(image)
		checkbox.SetPosition(60, 0)
		checkbox.SetWindowHorizontalAlignRight()
		checkbox.SetWindowVerticalAlignCenter()
		checkbox.SetEvent(Event(self.__ReminderStatus))
		checkbox.Show()

		clock = ui.MakeExpandedImageBox(image, GetAssets().format("biolog_manager/clock.png"), 40, 0)
		clock.SetWindowHorizontalAlignRight()
		clock.SetWindowVerticalAlignCenter()

		self.AppendObject("cooldown-content", (image, text, checkbox, clock))

		## Rewards Content
		image = ui.MakeExpandedImageBox(self.GetObject("base"), GetAssets().format("biolog_manager/header_content.png"), 0, self.GetObject("cooldown-content", 0).GetLocalPosition()[1] + self.GetObject("cooldown-content", 0).GetHeight())
		image.SetWindowHorizontalAlignCenter()

		text = ui.MakeTextLine(image)
		text.SetText(localeInfo.BIOLOG_MANAGER_REWARD_TEXT)

		reward_content = ui.MakeExpandedImageBox(self.GetObject("base"), GetAssets().format("biolog_manager/reward_content.png"), 0, image.GetLocalPosition()[1] + image.GetHeight())
		reward_content.SetWindowHorizontalAlignCenter()

		reward_slot = ui.SlotWindow()
		reward_slot.SetParent(reward_content)
		reward_slot.SetPosition((68 - 33) / 2, (reward_content.GetHeight() - 33) / 2)
		reward_slot.SetSize(33, 33)
		reward_slot.SetOverOutItemEvent(self.__OnOverOutItem)
		reward_slot.SetSlotBaseImage(GetAssets().format("biolog_manager/slot.png"), 1.0, 1.0, 1.0, 1.0)
		reward_slot.AppendSlot(0, 0, 0, 33, 33)
		reward_slot.Show()

		tmpLine = self.BiologAffectElement()

		bonus_clipper = ui.ListBoxEx()
		bonus_clipper.SetParent(reward_content)
		bonus_clipper.SetPosition(68, 1)
		bonus_clipper.SetSize(*tmpLine.GetSize())
		bonus_clipper.SetItemSize(tmpLine.GetWidth(), tmpLine.GetHeight())
		bonus_clipper.SetItemStep(tmpLine.GetHeight() + 1)
		bonus_clipper.SetViewItemCount(3)
		bonus_clipper.Show()

		self.AppendObject("reward-content", (image, text, (reward_content, reward_slot), bonus_clipper))

	def __CollectItem(self):
		net.SendChatPacket("/request_biolog_collect {} {}".format(self.GetObject("main-content", 3)[0][1].IsChecked(), self.GetObject("main-content", 3)[1][1].IsChecked()))

	def __ReminderStatus(self):
		net.SendChatPacket("/request_biolog_timer {}".format(self.GetObject("cooldown-content", 2).IsChecked()))

	def __RequestMissions(self):
		net.SendChatPacket("/request_biolog_sets")

	def __OnOverInItem(self, vnum, slotIndex):
		self._toolTip.SetVnum(vnum)
		self._toolTip.ShowToolTip()

	def __OnOverOutItem(self):
		self._toolTip.HideToolTip()

	def RegisterMissionProgress(self, iKey, iCount, tTime, bReminder):
		self.windowConfig["CONTROLS"]["PROGRESS"] = {
			"key" : iKey,
			"count" : iCount,
			"time" : app.GetTime() + tTime,
			"reminder" : bReminder,
		}

		self.GetObject("cooldown-content", 2).SetChecked(bReminder)

	def RegisterMission(self, iLevel, iVnum, iCount, iChance):
		self.windowConfig["CONTROLS"]["MISSION"] = {
			"level" : iLevel,
			"item" : (iVnum, iCount),
			"chance" : iChance,
		}

	def RegisterRewardBasic(self, iVnum, iCount, bSelector):
		self.windowConfig["CONTROLS"]["REWARD"] = {
			"item" : (iVnum, iCount),
			"selector" : bSelector,
			"applies" : [],
		}

	def RegisterRewardAffect(self, iKey, iType, iValue):
		self.windowConfig["CONTROLS"]["REWARD"]["applies"].append((iKey, iType, iValue))

	def RegisterComponents(self):
		lConfig = self.windowConfig["CONTROLS"]["MISSION"]
		lRewards = self.windowConfig["CONTROLS"]["REWARD"]

		self.GetObject("top_header", 1).SetText(localeInfo.BIOLOG_MANAGER_REQUIRED_LEVEL + " {}".format(colorInfo.Colorize(localeInfo.BIOLOG_MANAGER_LEVEL_MISSION.format(lConfig.get("level")), 0xFFb19d58)))

		self.GetObject("cooldown-content", 2).SetChecked(True if self.windowConfig["CONTROLS"]["PROGRESS"] == 1 else False)

		item.SelectItem(lConfig.get("item")[0])
		self.GetObject("progress_content", 1).SetText(localeInfo.BIOLOG_MANAGER_REQUIRED_ITEM_TITLE + " {}".format(colorInfo.Colorize(item.GetItemName(), 0xFF8dad80)))
		self.GetObject("progress_content", 2).SetPercentage(self.windowConfig["CONTROLS"]["PROGRESS"].get("count", 0), lConfig.get("item")[1])

		self.GetObject("main-content", 1).SetItemSlot(0, lConfig.get("item")[0], lConfig.get("item")[1] - self.windowConfig["CONTROLS"]["PROGRESS"].get("count", 0))
		self.GetObject("main-content", 1).SetOverInItemEvent(Event(self.__OnOverInItem, lConfig.get("item")[0]))
		self.GetObject("main-content", 2)[1].SetText(localeInfo.BIOLOG_MANAGER_CHANCE.format(colorInfo.Colorize(str(lConfig.get("chance")) + "%", 0xFFb19d58)))
		
		self.GetObject("reward-content", 2)[1].ClearSlot(0)
		self.GetObject("reward-content", 2)[1].SetOverInItemEvent(Event(self.__OnOverInItem, lRewards.get("item", (0, 0))[0]))
		self.GetObject("reward-content", 2)[1].SetItemSlot(0, lRewards.get("item", (0, 0))[0], lRewards.get("item", (0, 0))[1])

		self.GetObject("reward-content", 3).RemoveAllItems()
		for _ in lRewards.get("applies"):
			tElement = self.BiologAffectElement(_)
			self.GetObject("reward-content", 3).AppendItem(tElement)

	def Close(self):
		self.Hide()

	def OnUpdate(self):
		if self.windowConfig["CONTROLS"]["PROGRESS"] and self.windowConfig["CONTROLS"]["PROGRESS"].get("time", 0):
			tTime = self.windowConfig["CONTROLS"]["PROGRESS"].get("time")
			if tTime >= app.GetTime():
				self.GetObject("cooldown-content", 0).LoadImage(GetAssets().format("biolog_manager/time_background_negative.png"))
				self.GetObject("cooldown-content", 1).SetText(localeInfo.BIOLOG_MANAGER_TIME_WAIT + localeInfo.SecondToHMS(tTime - app.GetTime()))
			else:
				self.GetObject("cooldown-content", 0).LoadImage(GetAssets().format("biolog_manager/time_background_positive.png"))
				self.GetObject("cooldown-content", 1).SetText(localeInfo.BIOLOG_MANAGER_TIME_TEXT)

class BiologSelector(ui.SimplyWindow):
	SIZE = (408, 204)

	class AffectElement(ui.ExpandedImageBox):
		def __init__(self, lConfig = ()):
			super(BiologSelector.AffectElement, self).__init__()

			self.__RunPreImageEvent()
			self.__Initialize(lConfig)

			if self.lConfig:
				self.__BuildAffectLine()

		def __del__(self):
			super(BiologSelector.AffectElement, self).__del__()

			#Private Methods
		def __RunPreImageEvent(self):
			self.LoadImage(GetAssets().format("biolog_manager/selector/element.png"))
			self.Show()

		def __Initialize(self, lConfig):
			self.lConfig = lConfig
			self.Objects = {}

		def __BuildAffectLine(self):
			applyString = uiToolTip.GetItemToolTipInstance().GetAffectString(self.lConfig[1], self.lConfig[2], False)
			if not applyString:
				return

			strip = applyString.find(":")

			self.Objects["AFF_KEY"] = self.__GenerateAppendSmallField(20, 0, str(self.lConfig[0] + 1) + ".")
			self.Objects["AFF_TYPE"] = self.__GenerateAppendSmallField(180, 20, colorInfo.Colorize(applyString[:strip], 0xFF8dad80))
			self.Objects["AFF_VALUE"] = self.__GenerateAppendSmallField(50, 195, colorInfo.Colorize(applyString[strip + 1:], 0xFFb19d58))
			self.Objects["AFF_BTN"] = ui.MakeButton(self, 295, 0, "", GetAssets().format("biolog_manager/selector/"), "btn_01.png", "btn_02.png", "btn_03.png", localeInfo.BIOLOG_MANAGER_BTN_CHOOSE)
			self.Objects["AFF_BTN"].SetEvent(Event(self.__CollectAffect))

		def __GenerateAppendSmallField(self, iWidth, iX, sTxt):
			newWnd = ui.Window()
			newWnd.SetParent(self)
			newWnd.SetSize(iWidth, self.GetHeight())
			newWnd.SetPosition(iX, 0)
			newWnd.SetWindowVerticalAlignCenter()
			newWnd.Show()

			self.Objects["TXT_%d_%s" % (iX, sTxt)] = ui.MakeTextLine(newWnd)
			self.Objects["TXT_%d_%s" % (iX, sTxt)].SetText(sTxt)

			return newWnd

		def __CollectAffect(self):
			net.SendChatPacket("/request_biolog_collect_affect {}".format(str(self.lConfig[0])))

			#Public Methods
		def Show(self):
			super(BiologSelector.AffectElement, self).Show()
		
		def Hide(self):
			super(BiologSelector.AffectElement, self).Hide()

	def __init__(self):
		super(BiologSelector, self).__init__("UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)

	def __del__(self):
		super(BiologSelector, self).__del__()

		# Private Methods
	def __Initialize(self):
		self.__CreateInterface()

	def __Destroy(self):
		self._toolTip = None

	def __CreateInterface(self):
		def __GenerateAppendSmallField(iWidth, iX, sTxt):
			newWnd = ui.Window()
			newWnd.SetParent(image)
			newWnd.SetSize(iWidth, image.GetHeight())
			newWnd.SetPosition(iX, 0)
			newWnd.SetWindowVerticalAlignCenter()
			newWnd.Show()

			text = ui.MakeTextLine(newWnd)
			text.SetText(sTxt)

			return (newWnd, text)

		## Base
		board = ui.MainBoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetSize(*self.GetSize())
		board.SetTitleName(localeInfo.BIOLOG_MANAGER_TITLE)
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.Show()

		self.AppendObject("board", board)

		base = ui.MainSubBoard("100")
		base.SetParent(self.GetObject("board"))
		base.SetPosition(5, 31)
		base.SetSize(self.GetObject("board").GetWidth() - base.GetLocalPosition()[0] * 2, self.GetObject("board").GetHeight() - (base.GetLocalPosition()[0] + base.GetLocalPosition()[1]))
		base.Show()

		self.AppendObject("base", base)

		## Top Header
		image = ui.MakeExpandedImageBox(self.GetObject("base"), GetAssets().format("biolog_manager/selector/header_top.png"), 0, 5	)
		image.SetWindowHorizontalAlignCenter()

		text = [ui.MakeTextLine(image) for _ in range(2)]
		text[0].SetText(colorInfo.Colorize("", 0xFFb19d58))
		text[1].SetText(colorInfo.Colorize("", 0xFFffffff))
		text[0].SetPosition(0, -6)
		text[1].SetPosition(0, 6)

		self.AppendObject("top-content", (image, text))

		# Content Header
		image = ui.MakeExpandedImageBox(self.GetObject("base"), GetAssets().format("biolog_manager/selector/header_content.png"), 0, self.GetObject("top-content", 0).GetLocalPosition()[1] + self.GetObject("top-content", 0).GetHeight() + 5)
		image.SetWindowHorizontalAlignCenter()

		# Build Header
		tConfig = [
			[20, 0, "#"],
			[180, 20, "Bonus"],
			[50, 200, "Warto��"],
			[70, 295, "Akcja"],
		]

		header_elements = []
		for (width, x, text) in tConfig:
			header_elements.append(__GenerateAppendSmallField(width, x, text))

		tmpLine = self.AffectElement()

		bonus_clipper = ui.ListBoxEx()
		bonus_clipper.SetParent(self.GetObject("base"))
		bonus_clipper.SetSize(tmpLine.GetWidth(), tmpLine.GetHeight() * 3)
		bonus_clipper.SetPosition((self.GetObject("base").GetWidth() - bonus_clipper.GetWidth()) / 2, image.GetLocalPosition()[1] + image.GetHeight())
		bonus_clipper.SetItemSize(tmpLine.GetWidth(), tmpLine.GetHeight())
		bonus_clipper.SetItemStep(tmpLine.GetHeight() + 1)
		bonus_clipper.SetViewItemCount(3)
		bonus_clipper.Show()

		self.AppendObject("main-content", (image, header_elements, bonus_clipper))

	def RegisterRewardAffect(self, iKey, iType, iValue):
		self.GetObject("main-content", 2).AppendItem(self.AffectElement((iKey, iType, iValue)))

	def RegisterComponents(self):
		pass

	def RequestClear(self):
		self.GetObject("main-content", 2).RemoveAllItems()

class BiologSets(ui.SimplyWindow):
	SIZE = (330, 321)

	class ClipperElement(ui.SimplyWindow):
		SIZE = (286, 75)
		def __init__(self, lConfig = {}):
			super(BiologSets.ClipperElement, self).__init__("UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)
			self.windowConfig["CONTROLS"] = lConfig

			if lConfig:
				self.__CreateElement()

		def __del__(self):
			super(BiologSets.ClipperElement, self).__del__()

		def __Initialize(self):
			pass

		def __Destroy(self):
			pass

			#Private Methods
		def __CreateElement(self):
			tMainConfig = self.windowConfig["CONTROLS"].get("MAIN")
			if not tMainConfig:
				return

			## Top Header
			image = ui.MakeExpandedImageBox(self, GetAssets().format("biolog_manager/sets/object_header_{}.png".format(tMainConfig.get("finished"))), 0, 5)
			image.SetWindowHorizontalAlignCenter()

			lStates = {
				0 : [localeInfo.BIOLOG_MANAGER_STATE_NOT_FINISHED, 0xFFac6968],
				1 : [localeInfo.BIOLOG_MANAGER_STATE_FINISHED, 0xFF8dad80],
			}

			item.SelectItem(tMainConfig.get("vnum"))
			text = ui.MakeTextLineNew(image, 0, -2, "{}. {} {} [{}]".format(colorInfo.Colorize(tMainConfig.get("key") + 1, 0xFFb19d58), colorInfo.Colorize("[Lv. {}]".format(tMainConfig.get("level")), 0xFF8dad80), item.GetItemName(), lStates[tMainConfig.get("finished")][0]))	
			text.SetPackedFontColor(lStates[tMainConfig.get("finished")][1])
			text.SetWindowVerticalAlignCenter()
			text.SetVerticalAlignCenter()

			button = ui.MakeButton(image, 19, 0, "", GetAssets().format("biolog_manager/sets/"), "reset_0.png", "reset_1.png", "reset_2.png")
			button.SetWindowHorizontalAlignRight()
			button.SetEvent(Event(self.__ResetAffect))
			if (tMainConfig.get("selector", 0) == 0) or (tMainConfig.get("finished", 0) == 0):
				button.Hide()

			self.AppendObject("header-content", (image, text, button))

			box = ui.BoxedBoard()
			box.SetParent(self)
			box.SetSize(self.GetObject("header-content", 0).GetWidth(), 50)
			box.SetPosition(self.GetObject("header-content", 0).GetLocalPosition()[0], self.GetObject("header-content", 0).GetLocalPosition()[1] + self.GetObject("header-content", 0).GetHeight())
			box.Show()

			self.AppendObject("main-content", box)

		def __ResetAffect(self):
			net.SendChatPacket("/request_biolog_reset {}".format(self.windowConfig["CONTROLS"]["MAIN"].get("key")))

		def AppendApply(self, lConfig):
			yPos = lConfig[0] * 15
			applyString = uiToolTip.GetItemToolTipInstance().GetAffectString(lConfig[2], lConfig[3], False)
			if not applyString:
				return

			lStates = {
				0 : 0xFFac6968,
				1 : 0xFF8dad80,
			}
			text = ui.MakeTextLineNew(self.GetObject("main-content"), 0, yPos, applyString)
			text.SetWindowHorizontalAlignCenter()
			text.SetHorizontalAlignCenter()
			if self.windowConfig["CONTROLS"]["MAIN"].get("finished", 0) == 0:
				text.SetPackedFontColor(lStates[0])
			else:
				text.SetPackedFontColor(lStates[lConfig[1]])
			self.AppendObject("apply-text", text, True)

		def __CollectAffect(self):
			net.SendChatPacket("/request_biolog_collect_affect {}".format(str(self.lConfig[0])))

			#Public Methods
		def Show(self):
			super(BiologSets.ClipperElement, self).Show()
		
		def Hide(self):
			super(BiologSets.ClipperElement, self).Hide()

		OnPressExitKey = OnPressEscapeKey = lambda *args, **kwargs : None

	def __init__(self):
		super(BiologSets, self).__init__("UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)

	def __del__(self):
		super(BiologSets, self).__del__()

		# Private Methods
	def __Initialize(self):
		self.__CreateInterface()
		self._toolTip = ItemToolTipDummy(0)
		self.windowConfig["CONTROLS"] = dict()

	def __Destroy(self):
		self._toolTip = None

	def __CreateInterface(self):
		## Base
		board = ui.MainBoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetSize(*self.GetSize())
		board.SetTitleName(localeInfo.BIOLOG_MANAGER_TITLE)
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.Show()

		self.AppendObject("board", board)

		base = ui.MainSubBoard("100")
		base.SetParent(self.GetObject("board"))
		base.SetPosition(5, 31)
		base.SetSize(self.GetObject("board").GetWidth() - base.GetLocalPosition()[0] * 2, self.GetObject("board").GetHeight() - (base.GetLocalPosition()[0] + base.GetLocalPosition()[1]))
		base.Show()

		self.AppendObject("base", base)

		## Top Header
		image = ui.MakeExpandedImageBox(self.GetObject("base"), GetAssets().format("biolog_manager/sets/header_top.png"), 0, 5)
		image.SetWindowHorizontalAlignCenter()

		text = ui.MakeTextLine(image)
		text.SetText(colorInfo.Colorize(localeInfo.BIOLOG_MANAGER_LIST_HEADER, 0xFFb19d58))

		self.AppendObject("top-content", (image, text))

		## Clipper
		tmp = self.ClipperElement()
		clipper = ui.ListBoxEx()
		clipper.SetParent(self.GetObject("base"))
		clipper.SetSize(tmp.GetWidth(), tmp.GetHeight() * 3)
		clipper.SetPosition((self.GetObject("base").GetWidth() - clipper.GetWidth()) / 2, self.GetObject("top-content", 0).GetLocalPosition()[1] + self.GetObject("top-content", 0).GetHeight())
		clipper.SetItemSize(tmp.GetWidth(), tmp.GetHeight())
		clipper.SetItemStep(tmp.GetHeight() + 1)
		clipper.SetViewItemCount(3)
		clipper.Show()

		scroll = ui.ExpensiveScrollBar(GetAssets().format("biolog_manager/sets/"), "scroll_base.png", "scroll.png")
		scroll.SetParent(self)
		scroll.SetPosition(clipper.GetLocalPosition()[0] + (clipper.GetWidth() + 5), clipper.GetLocalPosition()[1] + 33)
		scroll.Show()

		clipper.SetScrollBar(scroll)
		clipper.SetScrollWheelEvent(scroll.OnWheelMove)

		self.AppendObject("main-content", (clipper, scroll))

	def ClearSet(self):
		self.GetObject("main-content", 0).RemoveAllItems()
		self.windowConfig["CONTROLS"] = dict()

	def RegisterSet(self, iKey, bFinished, bSelector, iVnum, iLevel):
		self.windowConfig["CONTROLS"][iKey] = {"MAIN" : { "key" : iKey, "finished" : bFinished, "selector" : bSelector, "vnum" : iVnum,  "level" : iLevel }}

		self.windowConfig["CONTROLS"][iKey]["APPLIES"] = []

		self.GetObject("main-content", 0).AppendItem(self.ClipperElement(self.windowConfig["CONTROLS"][iKey]))

	def RegisterSetApply(self, iKey, iApplyKey, iSelected, iApplyType, iApplyValue):
		self.windowConfig["CONTROLS"][iKey]["APPLIES"].append((
			iApplyKey, iSelected, iApplyType, iApplyValue
		))

		self.GetObject("main-content", 0).itemList[iKey].AppendApply((iApplyKey, iSelected, iApplyType, iApplyValue))

	def Close(self):
		self.Hide()

	OnPressExitKey = OnPressEscapeKey = lambda *args, **kwargs : None