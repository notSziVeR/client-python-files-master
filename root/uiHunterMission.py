import ui, exception, localeInfo, uiToolTip
import nonplayer, item, player
from _weakref import proxy

class HunterClass(ui.ScriptWindow):
	HUNTER_ITEMS = dict()
	CATTEGORY_BUTTON_ALIGN = 20
	ROOT_PATH = "assets/ui/hunter_missions/{}"

	class CattegoryButton(ui.RadioButton):
		HUNTER_ROOT_BUTTONS = "assets/ui/hunter_missions/buttons/{}.png"

		def __init__(self, eCategoryID):
			ui.RadioButton.__init__(self)
			self.eCategoryID = eCategoryID

			self.__Initialize()
			self.__BuildObject()

		def __del__(self):
			ui.RadioButton.__del__(self)

		def __Initialize(self):
			self.Objects = {}

		def __BuildObject(self):
			##Layer
			self.SetUpVisual(self.HUNTER_ROOT_BUTTONS.format("cattegory_button_norm"))
			self.SetOverVisual(self.HUNTER_ROOT_BUTTONS.format("cattegory_button_over"))
			self.SetDownVisual(self.HUNTER_ROOT_BUTTONS.format("cattegory_button_down"))

			## Title
			self.Objects["TITLE"] = ui.TextLine()
			self.Objects["TITLE"].SetParent(self)
			self.Objects["TITLE"].AddFlag("not_pick")
			self.Objects["TITLE"].SetPosition(0, -1)
			self.Objects["TITLE"].SetHorizontalAlignCenter()
			self.Objects["TITLE"].SetWindowHorizontalAlignCenter()
			self.Objects["TITLE"].SetVerticalAlignCenter()
			self.Objects["TITLE"].SetWindowVerticalAlignCenter()
			self.Objects["TITLE"].SetText(getattr(localeInfo, "HUNTER_MISSION_CATTEGORY_TITLE_{}".format(self.eCategoryID), "Not found in locale_game"))
			self.Objects["TITLE"].Show()

	class MissionItem(ui.ExpandedImageBox):
		ITEM_SIZE = (440, 80)
		ROOT_PATH = "assets/ui/hunter_missions/{}"

		def __init__(self, pParent):
			ui.ExpandedImageBox.__init__(self)

			self.scriptParent = proxy(pParent)
			self.ItemToolTip = uiToolTip.ItemToolTip()
			self.ToolTip = uiToolTip.ToolTip()
			self.ToolTip.ClearToolTip()

			self.__Initialize()

		def __del__(self):
			ui.ExpandedImageBox.__del__(self)
			self.__Initialize()

		def __Initialize(self):
			self.Objects = {}
			self.ObjectData = {}

			self.bDone = False

			## Load Background
			self.LoadImage(self.ROOT_PATH.format("item_0.png"))

		def LoadData(self, **Args):
			if len(Args) == 0:
				return

			self.ObjectData.update({"data" : Args})

			bFinished = 0
			if Args["iCurrentCount"] == Args["wRequiredCount"]:
				self.LoadImage(self.ROOT_PATH.format("item_1.png"))
				bFinished = 1

			self.Objects["RENDERER"] = ui.RenderTarget()
			self.Objects["RENDERER"].SetParent(self)
			self.Objects["RENDERER"].SetPosition(0, 0)
			self.Objects["RENDERER"].SetSize(103, 103)
			self.Objects["RENDERER"].LoadImage(self.ROOT_PATH.format("render_space.png"))
			self.Objects["RENDERER"].SetRenderTarget(Args["wTargetVnum"])
			self.Objects["RENDERER"].SetLightPosition(*(50.0, 150.0, 350.0))
			if Args["wTargetVnum"] == 1093:
				self.Objects["RENDERER"].SetRenderDistance(1100)
			self.Objects["RENDERER"].SetRotationMode(True)
			self.Objects["RENDERER"].Show()

			self.Objects["SPACE_OF_TITLE"] = ui.ExpandedImageBox()
			self.Objects["SPACE_OF_TITLE"].SetParent(self)
			self.Objects["SPACE_OF_TITLE"].SetPosition(123, 27)
			self.Objects["SPACE_OF_TITLE"].LoadImage(self.ROOT_PATH.format("item_text_space.png"))
			self.Objects["SPACE_OF_TITLE"].Show()

			self.Objects["NAME_OF_MONSTER"] = ui.TextLine()
			self.Objects["NAME_OF_MONSTER"].SetParent(self.Objects["SPACE_OF_TITLE"])
			self.Objects["NAME_OF_MONSTER"].SetPosition(5, 1)
			self.Objects["NAME_OF_MONSTER"].SetHorizontalAlignLeft()
			self.Objects["NAME_OF_MONSTER"].SetWindowHorizontalAlignLeft()
			self.Objects["NAME_OF_MONSTER"].SetWindowVerticalAlignCenter()
			self.Objects["NAME_OF_MONSTER"].SetVerticalAlignCenter()
			sText = localeInfo.HUNTER_MISSION_TITLE_OF_ITEM.format(nonplayer.GetMonsterName(Args["wTargetVnum"]), Args["wRequiredCount"])
			self.Objects["NAME_OF_MONSTER"].SetText(sText)
			self.Objects["NAME_OF_MONSTER"].SetPackedFontColor(0xFF787878)
			self.Objects["NAME_OF_MONSTER"].Show()

			self.Objects["SPACE_OF_PROGRESS"] = ui.ExpandedImageBox()
			self.Objects["SPACE_OF_PROGRESS"].SetParent(self)
			self.Objects["SPACE_OF_PROGRESS"].SetPosition(123, 58)
			self.Objects["SPACE_OF_PROGRESS"].LoadImage(self.ROOT_PATH.format("item_text_space.png"))
			self.Objects["SPACE_OF_PROGRESS"].Show()

			self.Objects["COUNT_OF_KILLED"] = ui.TextLine()
			self.Objects["COUNT_OF_KILLED"].SetParent(self.Objects["SPACE_OF_PROGRESS"])
			self.Objects["COUNT_OF_KILLED"].SetPosition(5, 0)
			self.Objects["COUNT_OF_KILLED"].SetHorizontalAlignLeft()
			self.Objects["COUNT_OF_KILLED"].SetWindowHorizontalAlignLeft()
			self.Objects["COUNT_OF_KILLED"].SetWindowVerticalAlignCenter()
			self.Objects["COUNT_OF_KILLED"].SetVerticalAlignCenter()
			sText = localeInfo.HUNTER_MISSION_COUNT_OF_KILLED.format(Args["iCurrentCount"], Args["wRequiredCount"])
			self.Objects["COUNT_OF_KILLED"].SetText(sText)
			self.Objects["COUNT_OF_KILLED"].SetPackedFontColor(0xFF787878)
			self.Objects["COUNT_OF_KILLED"].Show()

			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"] = ui.ExpandedImageBox()
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"].SetParent(self)
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"].SetPosition(123, 20)
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"].SetWindowVerticalAlignBottom()
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"].LoadImage(self.ROOT_PATH.format("total_progress_empty.png"))
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"].Show()

			self.Objects["TASK_PROGRESS_GAUGE_FULL"] = ui.ExpandedImageBox()
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].SetParent(self.Objects["TASK_PROGRESS_GAUGE_EMPTY"])
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].SetPosition(8, 2)
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].LoadImage(self.ROOT_PATH.format("total_progress_full.png"))
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].SetPercentage(Args["iCurrentCount"] * 100 / Args["wRequiredCount"], 100)
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].Show()

			self.Objects["REWARD_CONTENT"] = ui.ExpandedImageBox()
			self.Objects["REWARD_CONTENT"].SetParent(self)
			self.Objects["REWARD_CONTENT"].LoadImage(self.ROOT_PATH.format("reward_space_{}.png".format(bFinished)))
			self.Objects["REWARD_CONTENT"].SetWindowHorizontalAlignRight()
			self.Objects["REWARD_CONTENT"].SetPosition(131 + 20, self.GetHeight() / 2 - self.Objects["REWARD_CONTENT"].GetHeight() / 2)
			self.Objects["REWARD_CONTENT"].Show()

			TYPE_ITEM = 1

			iRewardType = Args["eRewardType"]
			
			# Checking the type of the reward
			if iRewardType == TYPE_ITEM:
				item.SelectItem(Args["wRewardItemVnum"])

				self.Objects["REWARD"] = ui.SlotWindow()
				self.Objects["REWARD"].SetParent(self.Objects["REWARD_CONTENT"])
				w, h = item.GetItemSize()
				
				sX, sY = ((self.Objects["REWARD_CONTENT"].GetWidth() - 32 * w) / 2, (self.Objects["REWARD_CONTENT"].GetHeight() - h * 32) / 2)
				self.Objects["REWARD"].SetPosition(sX, sY)
				self.Objects["REWARD"].AppendSlot(0, 0, 0, 32, h * 32)
				self.Objects["REWARD"].SetSize(w * 32, h * 32)
				self.Objects["REWARD"].SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
				self.Objects["REWARD"].SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
				self.Objects["REWARD"].Show()

				self.Objects["REWARD"].SetItemSlot(0, Args["wRewardItemVnum"], Args["iRewardItemCount"])
			else:
				self.Objects["REWARD"] = ui.ImageBox()
				self.Objects["REWARD"].SetParent(self.Objects["REWARD_CONTENT"])
				self.Objects["REWARD"].LoadImage(self.ROOT_PATH.format("reward_type_bonus.png"))

				sX, sY = ((self.Objects["REWARD_CONTENT"].GetWidth() - self.Objects["REWARD"].GetWidth()) / 2, (self.Objects["REWARD_CONTENT"].GetHeight() - self.Objects["REWARD"].GetHeight()) / 2)

				self.Objects["REWARD"].SetPosition(sX, sY)

				self.Objects["REWARD"].SetStringEvent("MOUSE_OVER_IN", ui.__mem_func__(self.OverInRewardBonus))
				self.Objects["REWARD"].SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.OverOutRewardBonus))
				self.Objects["REWARD"].Show()

		def UpdateProgress(self, **Args):
			sText = localeInfo.HUNTER_MISSION_COUNT_OF_KILLED.format(Args["iCurrentCount"], Args["wRequiredCount"])
			self.Objects["COUNT_OF_KILLED"].SetText(sText)

			self.Objects["TASK_PROGRESS_GAUGE_FULL"].SetPercentage(Args["iCurrentCount"] * 100 / Args["wRequiredCount"], 100)

			if Args["iCurrentCount"] == Args["wRequiredCount"]:
				self.LoadImage(self.ROOT_PATH.format("item_1.png"))
				self.Objects["REWARD_CONTENT"].LoadImage(self.ROOT_PATH.format("reward_space_1.png"))

		def GetTarget(self):
			return self.ObjectData["data"]["wTargetVnum"]
		
		def IsFinished(self):
			return self.Objects["data"]["iCurrentCount"] == self.Objects["data"]["wRequiredCount"]

		def OverInRewardBonus(self):
			if self.ToolTip:
				self.ToolTip.ClearToolTip()
				
				affString = self.GetAffectString(self.ObjectData["data"]["eRewardApplyType"], self.ObjectData["data"]["iRewardApplyValue"])
				if affString:
					self.ToolTip.AppendTextLine(affString)
				self.ToolTip.Show()

		def OverOutRewardBonus(self):
			if self.ToolTip:
				self.ToolTip.ClearToolTip()
				self.ToolTip.HideToolTip()

		def OverInItem(self, slotPos):
			if self.ItemToolTip:
				self.ItemToolTip.ClearToolTip()
				self.ItemToolTip.AddItemData(self.ObjectData["data"]["wRewardItemVnum"], metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])

		def OverOutItem(self):
			if self.ItemToolTip:
				self.ItemToolTip.Hide()

		def GetAffectString(self, affectType, affectValue):
			if 0 == affectType:
				return None

			if 0 == affectValue:
				return None

			try:
				return localeInfo.AFFECT_DICT[affectType].format(affectValue)
			except TypeError:
				return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
			except KeyError:
				return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__BuildWindow()

	def __del__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()

	def Destroy(self):
		self.ClearDictionary()
		self.Objects = {}
		self.iCurrentCategory = -1

	def __Initialize(self):
		self.Objects = {}
		self.iCurrentCategory = -1

	def __BuildWindow(self):
		try: ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/HunterMission_Window.py")
		except:
			exception.Abort("HunterMission.__BuildWindow.LoadDir")
			return False

		try:
			GetObject = ui.__mem_func__(self.GetChild)
			
			self.Objects["BOARD"] = GetObject("HunterMission_Board")
			self.Objects["HEADER"] = GetObject("HunterMission_Content_HederImage")
			self.Objects["HEADER_TEXT"] = GetObject("HunterMission_Content_HederImage_NameText")
			self.Objects["CATEGORIES_CONTENT"] = GetObject("HunterMission_Content_Category")
			self.Objects["CATEGORIES_LABEL"] = GetObject("HunterMission_Content_CategoryText")
			self.Objects["CATEGORIES"] = dict()
			self.Objects["ITEMS_CONTENT"] = GetObject("HunterMission_Content_Data")
			self.Objects["ITEMS"] = GetObject("HunterMission_ItemsListBox")

			tmpItem = self.MissionItem(self)
			tmpItem.Hide()

			self.Objects["ITEMS"].SetItemSize(tmpItem.GetWidth(), tmpItem.GetHeight())
			self.Objects["ITEMS"].SetItemStep(tmpItem.GetHeight() - 1)
			self.Objects["ITEMS"].SetViewItemCount(4)
			self.Objects["ITEMS"].SetScrollBar(self.__MakeScrollBar(self.Objects["ITEMS_CONTENT"], "scrollbar_field.png", "scrollbar_n.png", -9, 8))
			self.Objects["ITEMS"].SetScrollWheelEvent(self.Objects["ITEMS"].scrollBar.OnWheelMove)

		except:
			exception.Abort("HunterMission.__BuildWindow.LoadObject")

		self.SetCenterPosition()
		self.SetTop()

		return self.__BindActions()

	def __BindActions(self):
		try:
			self.Objects["BOARD"].SetCloseEvent(ui.__mem_func__(self.Close))

			return True
		except: return False

	def	__MakeScrollBar(self, nObject, sField, sCursor, xFill = 0, yFill = 0):
		newScroll = ui.ExpensiveScrollBar("assets/ui/hunter_missions/", sField, sCursor)
		newScroll.SetParent(self)
		newScroll.SetPosition(nObject.GetLocalPosition()[0] + (nObject.GetWidth() + xFill), nObject.GetLocalPosition()[1] + yFill)
		newScroll.Show()

		return newScroll

	def	OnWheelMove(self, iLen):
		if not self.IsShow():
			return

		self.Objects["ITEMS"].scrollBar.OnScrollWheelEvent(iLen)

	def SelectCategory(self, iCategoryID = 0):
		for obj in self.Objects["CATEGORIES"].values():
			obj.SetUp()

		self.Objects["CATEGORIES"].values()[iCategoryID].Down()

		self.iCurrentCategory = iCategoryID
		self.__ClearItems()

		if self.iCurrentCategory in self.HUNTER_ITEMS:
			for rItem in self.HUNTER_ITEMS[self.iCurrentCategory]:
				self.Objects["ITEMS"].AppendItem(rItem, bSorted = True)

		self.Objects["HEADER"].LoadImage(self.ROOT_PATH.format("headers/header_{}.png".format(self.iCurrentCategory)))
		self.Objects["HEADER_TEXT"].SetText(getattr(localeInfo, "HUNTER_MISSION_CATTEGORY_TITLE_{}".format(self.iCurrentCategory), "Not found in locale_game"))

	def __ClearItems(self):
		for rItem in self.Objects["ITEMS"].itemList:
			rItem.Hide()

		self.Objects["ITEMS"].RemoveAllItems()

	"""Recv"""
	def OnRecvClear(self):
		for v in self.Objects["CATEGORIES"].values():
			v.Hide()

		## Resetting the categories dict
		self.Objects["CATEGORIES"] = dict()

		self.__ClearItems()
		self.HUNTER_ITEMS = dict()

	def OnRecvCategory(self, eCategoryID):
		if not eCategoryID in self.Objects["CATEGORIES"]:
			self.Objects["CATEGORIES"][eCategoryID] = self.CattegoryButton(eCategoryID)
			self.Objects["CATEGORIES"][eCategoryID].SetParent(self.Objects["CATEGORIES_CONTENT"])
			self.Objects["CATEGORIES"][eCategoryID].SetPosition(0, self.Objects["CATEGORIES_CONTENT"].GetHeight() / 2- self.Objects["CATEGORIES"][eCategoryID].GetHeight() / 2)
			self.Objects["CATEGORIES"][eCategoryID].SetEvent(ui.__mem_func__(self.SelectCategory), eCategoryID)
			self.Objects["CATEGORIES"][eCategoryID].Show()

		self.__RerrangeCattegory()

	def OnRecvItem(self, eCategoryID, wTargetVnum, wRequiredCount, iCurrentCount, eRewardType, wRewardItemVnum, iRewardItemCount, eRewardApplyType, iRewardApplyValue):
		bExists = False
		rItem = None

		if eCategoryID in self.HUNTER_ITEMS:
			for rItem in self.HUNTER_ITEMS[eCategoryID]:
				if rItem.GetTarget() == wTargetVnum:
					bExists = True
					rItem = rItem
					break

		if bExists:
			for rItem2 in self.Objects["ITEMS"].itemList:
				if rItem2.GetTarget() == wTargetVnum:
					rItem2.UpdateProgress(wRequiredCount = wRequiredCount, iCurrentCount = iCurrentCount)
		else:
			missionItem = self.MissionItem(self)
			missionItem.LoadData(wTargetVnum = wTargetVnum, wRequiredCount = wRequiredCount, iCurrentCount = iCurrentCount, eRewardType = eRewardType, wRewardItemVnum = wRewardItemVnum, iRewardItemCount = iRewardItemCount, eRewardApplyType = eRewardApplyType, iRewardApplyValue = iRewardApplyValue)
			missionItem.bDone =  wRequiredCount == iCurrentCount

			if not eCategoryID in self.HUNTER_ITEMS:
				self.HUNTER_ITEMS[eCategoryID] = []

			self.HUNTER_ITEMS[eCategoryID].append(missionItem)
			if self.iCurrentCategory == eCategoryID:
				self.Objects["ITEMS"].AppendItem(missionItem, bSorted = True)

	"""Recv"""
	def __RerrangeCattegory(self):
		## Calculate total width
		totalWidth = self.Objects["CATEGORIES_LABEL"].GetTextSize()[0]

		## Add alignment
		totalWidth += len(self.Objects["CATEGORIES"]) * self.CATTEGORY_BUTTON_ALIGN

		## Calculate entry position basing on the middle of board
		entryX = ((self.Objects["CATEGORIES_CONTENT"].GetWidth() / 2) -totalWidth)/2

		## Label goes as first
		entryX += self.CATTEGORY_BUTTON_ALIGN / 2

		## And then buttons
		for v in self.Objects["CATEGORIES"].values():
			v.SetPosition(entryX, v.GetLocalPosition()[1])
			entryX += v.GetWidth() + self.CATTEGORY_BUTTON_ALIGN

	def UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.Show()

			if self.Objects["CATEGORIES"].values():
				self.SelectCategory(0)

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True