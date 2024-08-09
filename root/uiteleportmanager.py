#-*- coding: iso-8859-1 -*-
import ui
import uiToolTip

import wndMgr
import background
import net
import player
import localeInfo
from _weakref import proxy

def	DEHASH_CATEGORY(sHash):
	iID, sName = sHash.split("|")
	return int(iID), sName.replace("_", " ")

def	DEHASH_ITEM(sHash):
	iMapIndex, iMinLevel, iMaxLevel, iEntranceX, iEntranceY = sHash.split("|")
	return int(iMapIndex), int(iMinLevel), int(iMaxLevel), int(iEntranceX), int(iEntranceY)

ROOT_PATH = "assets/ui/teleport_manager/{}"

class TeleportManagerInterface(ui.ScriptWindow):
	TELEPORT_ITEMS = dict()

	class CattegoryButton(ui.RadioButton):
		ROOT_PATH = "assets/ui/teleport_manager/{}"
		BUTTON_IMAGES = (ROOT_PATH.format("button_category_0.png"), ROOT_PATH.format("button_category_1.png"), ROOT_PATH.format("button_category_2.png"))

		def __init__(self, sHash):
			ui.RadioButton.__init__(self)

			global DEHASH_CATEGORY
			self.sHash = sHash
			self.iID, self.sName = DEHASH_CATEGORY(sHash)

			self.__Initialize()
			self.__Build()

		def __del__(self):
			ui.RadioButton.__del__(self)
			self.__Initialize()
			self.iID, self.sName = -1, ""

		def __Initialize(self):
			self.Objects = {}

		def SetParent(self, parent):
			ui.RadioButton.SetParent(self, parent)

			self.parent=proxy(parent)
			self.SAFE_SetEvent(self.parent.SelectItem, self)

		def __Build(self):
			self.SetUpVisual(self.BUTTON_IMAGES[0])
			self.SetOverVisual(self.BUTTON_IMAGES[1])
			self.SetDownVisual(self.BUTTON_IMAGES[2])
			self.SetButtonText(self.sName, 0, 4)

		def	SetButtonText(self, sTxt, iX = -1, iY = -1):
			if iX == -1 and iY == -1:
				self.SetText(sTxt)
			else:
				self.Objects["TITLE"] = ui.TextLine()
				self.Objects["TITLE"].SetParent(self)
				self.Objects["TITLE"].SetPosition(iX, iY)
				self.Objects["TITLE"].SetWindowHorizontalAlignCenter()
				self.Objects["TITLE"].SetHorizontalAlignCenter()
				self.Objects["TITLE"].SetText(getattr(localeInfo, "TELEPORT_MANAGER_CATEGORY_{}".format(sTxt), sTxt))
				self.Objects["TITLE"].SetPackedFontColor(0xffDFDDCE)
				self.Objects["TITLE"].Show()

		def	GetHash(self):
			return self.sHash

		def	GetID(self):
			return self.iID
	
	class ItemWindow(ui.ExpandedImageBox):
		ROOT_PATH = "assets/ui/teleport_manager/{}"
		BUTTON_TELEPORT = (ROOT_PATH.format("button_teleport_0.png"), ROOT_PATH.format("button_teleport_1.png"), ROOT_PATH.format("button_teleport_2.png"))

		def __init__(self, parent, bCategoryID, sCategoryName, sItemHash):
			global DEHASH_ITEM
			ui.ExpandedImageBox.__init__(self)

			self.iCategory = bCategoryID
			self.sHash = sItemHash
			self.sCategory = sCategoryName.split("|")[1].replace("_", " ")
			self.mapIndex, self.minLevel, self.maxLevel, self.entranceX, self.entranceY = DEHASH_ITEM(sItemHash)
			self.toolTip = self.__CreateToolTip()

			self.__Initialize()

			self.scriptParent = proxy(parent)

			self.__Build()

		def __del__(self):
			ui.ExpandedImageBox.__del__(self)
			self.__Initialize()
			self.sCategory, self.mapIndex, self.minLevel, self.maxLevel, self.entranceX, self.entranceY = "", 0, 0, 0, 0, 0
			self.toolTip = None

		def __Initialize(self):
			self.Objects = {}
			self.bDisabled = False

		def __Build(self):
			self.SetSize(331, 51)
			self.LoadImage(ROOT_PATH.format("item_0.png"))

			# Category
			self.Objects["CATEGORY"] = ui.TextLine()
			self.Objects["CATEGORY"].SetParent(self)
			self.Objects["CATEGORY"].SetPosition(25, -7)
			self.Objects["CATEGORY"].SetWindowVerticalAlignCenter()
			self.Objects["CATEGORY"].SetVerticalAlignCenter()
			self.Objects["CATEGORY"].SetText(getattr(localeInfo, "TELEPORT_MANAGER_CATEGORY_{}".format(self.sCategory), self.sCategory))
			self.Objects["CATEGORY"].SetPackedFontColor(0xFFb19d58)
			self.Objects["CATEGORY"].Show()

			## Map Name
			(name, x, y) = background.GetMapLocaleName(self.entranceX * 100, self.entranceY * 100)
			self.Objects["MAP_NAME"] = ui.TextLine()
			self.Objects["MAP_NAME"].SetParent(self)
			self.Objects["MAP_NAME"].SetPosition(25, 7)
			self.Objects["MAP_NAME"].SetWindowVerticalAlignCenter()
			self.Objects["MAP_NAME"].SetVerticalAlignCenter()
			if self.minLevel > 1:
				playerLevel = player.GetStatus(player.LEVEL)
				color = "cFFb9e7bc" if playerLevel > self.minLevel else "cFFb19d58"
				self.Objects["MAP_NAME"].SetText(getattr(localeInfo, "ATLAS_{}".format(name), name.replace("_", " ")) + " (Lv. |{}{}|r)".format(color, self.minLevel))
			else:
				self.Objects["MAP_NAME"].SetText(getattr(localeInfo, "ATLAS_{}".format(name), name.replace("_", " ")))

			self.Objects["MAP_NAME"].Show()

			## Button Teleport
			self.Objects["TELEPORT"] = ui.Button()
			self.Objects["TELEPORT"].SetParent(self)
			self.Objects["TELEPORT"].SetUpVisual(self.BUTTON_TELEPORT[0])
			self.Objects["TELEPORT"].SetOverVisual(self.BUTTON_TELEPORT[1])
			self.Objects["TELEPORT"].SetDownVisual(self.BUTTON_TELEPORT[2])
			self.Objects["TELEPORT"].SetDisableVisual(self.BUTTON_TELEPORT[2])
			self.Objects["TELEPORT"].SetPosition(self.Objects["TELEPORT"].GetWidth() + 20, self.GetHeight() / 2 - self.Objects["TELEPORT"].GetHeight() / 2)
			self.Objects["TELEPORT"].SetWindowHorizontalAlignRight()
			self.Objects["TELEPORT"].SetText(localeInfo.TELEPORT_MANAGER_BUTTON_TELEPORT, 2)
			self.Objects["TELEPORT"].SAFE_SetEvent(self.__Teleport)
			self.Objects["TELEPORT"].Show()

			playerLevel = player.GetStatus(player.LEVEL)

			if (playerLevel < self.minLevel):
				self.LoadImage(ROOT_PATH.format("item_2.png"))
				self.Objects["TELEPORT"].Disable()
				self.bDisabled = True

		def __CreateToolTip(self):

			toolTip = uiToolTip.ToolTip()
			toolTip.AutoAppendTextLine(localeInfo.TELEPORT_MANAGER_REQUIRES_HEADER)
			toolTip.AppendSpace(5)

			information = localeInfo.TELEPORT_MANAGER_REQUIRES_NOT_FIT
			for desc in information.split("|"):
				toolTip.AutoAppendTextLine(desc)

			toolTip.AppendHorizontalLine()

			playerLevel = player.GetStatus(player.LEVEL)
			color = "cFFb9e7bc" if playerLevel > self.minLevel else "cFFb19d58"
			toolTip.AutoAppendTextLine(localeInfo.TELEPORT_MANAGER_MIN_LV.format(color, self.minLevel))
			color = "cFFb9e7bc" if playerLevel < self.maxLevel else "cFFb19d58"
			toolTip.AutoAppendTextLine(localeInfo.TELEPORT_MANAGER_MIN_LV.format(color, self.maxLevel))

			toolTip.AlignHorizonalCenter()

			return toolTip

		def OnMouseOverIn(self):
			if self.bDisabled:
				self.LoadImage(ROOT_PATH.format("item_1.png"))

				if self.toolTip:
					self.toolTip.ShowToolTip()

		def OnMouseOverOut(self):
			if self.bDisabled:
				self.LoadImage(ROOT_PATH.format("item_2.png"))

				if self.toolTip:
					self.toolTip.HideToolTip()

		def	GetHash(self):
			return self.sHash

		def __Teleport(self):
			net.SendChatPacket("/teleport_action {}".format(self.mapIndex))
			self.scriptParent.Close()

		def OnUpdate(self):
			pass

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.__Initialize()

	def __Initialize(self):
		self.Objects = {}
		self.iCurrentCategory = 0

	def __LoadWindow(self):
		if not self.LoadScript(self, "uiscript/teleport_manager_window.py"):
			return

		getObj = self.GetChild

		getObj("BOARD").SetCloseEvent(ui.__mem_func__(self.Close))
		
		self.Objects["CATEGORIES_BOARD"] = getObj("SUB_BOARD_RIGHT")
		self.Objects["CATEGORIES"] = getObj("CATEGORIES_LIST_BOX")

		self.Objects["ITEMS_BOARD"] = getObj("SUB_BOARD_LEFT")
		self.Objects["ITEMS"] = getObj("ITEMS_LIST_BOX")

		## Handling ListBoxes
		self.Objects["CATEGORIES"].SetItemSize(166, 24)
		self.Objects["CATEGORIES"].SetViewItemCount(10)
		self.Objects["CATEGORIES"].SetItemStep(24 + 5)
		self.Objects["CATEGORIES"].SetSelectEvent(ui.__mem_func__(self.__OnSelectCategory))

		self.Objects["ITEMS"].SetItemSize(337, 51)
		self.Objects["ITEMS"].SetViewItemCount(6)
		self.Objects["ITEMS"].SetItemStep(51)
		self.Objects["ITEMS"].SetScrollBar(self.__MakeScrollBar(self.Objects["ITEMS_BOARD"], "scrollbar_field.png", "scrollbar_n.png", -2, 2.5))
		self.Objects["ITEMS"].SetScrollWheelEvent(self.Objects["ITEMS"].scrollBar.OnWheelMove)

		self.SetCenterPosition()

	def	__MakeScrollBar(self, nObject, sField, sCursor, xFill = 0, yFill = 0):
		newScroll = ui.ExpensiveScrollBar("assets/ui/teleport_manager/", sField, sCursor)
		newScroll.SetParent(self)
		newScroll.SetPosition(nObject.GetLocalPosition()[0] + (nObject.GetWidth() + xFill), nObject.GetLocalPosition()[1] + yFill)
		newScroll.Show()

		return newScroll

	def	__OnSelectCategory(self, selItem):
		for obj in self.Objects["CATEGORIES"].itemList:
			if obj == selItem:
				obj.Down()
			else:
				obj.SetUp()

		self.iCurrentCategory = selItem.GetID()
		self.__ClearItems()

		self.iCurrentCategory = self.iCurrentCategory
		if self.iCurrentCategory in self.TELEPORT_ITEMS:
			for rItem in self.TELEPORT_ITEMS[self.iCurrentCategory]:
				self.Objects["ITEMS"].AppendItem(rItem)

	def __ClearItems(self):
		for rItem in self.Objects["ITEMS"].itemList:
			rItem.Hide()

		self.Objects["ITEMS"].RemoveAllItems()

	""" Recv """
	def OnRecvClear(self):
		self.Objects["CATEGORIES"].RemoveAllItems()
		self.__ClearItems()

		self.TELEPORT_ITEMS = dict()

	def OnRecvCategory(self, sHash):
		global DEHASH_CATEGORY
		iID, sName = DEHASH_CATEGORY(sHash)

		bExists = False
		for rItem in self.Objects["CATEGORIES"].itemList:
			if rItem.GetHash() == sHash:
				bExists = True
				break

		if bExists:
			self.Objects["CATEGORIES"].RemoveItem(rItem)
			if self.iCurrentCategory == iID:
				self.__ClearItems()
				self.iCurrentCategory = -1
		else:
			self.Objects["CATEGORIES"].AppendItem(self.CattegoryButton(sHash))
			self.TELEPORT_ITEMS[iID] = []	

	def OnRecvItem(self, bCategoryID, sCategoryName, sItemHash):
		bExists = False
		if bCategoryID in self.TELEPORT_ITEMS:
			for rItem in self.TELEPORT_ITEMS[bCategoryID]:
				if rItem.GetHash() == sItemHash:
					bExists = True
					break
		if bExists:
			rItem.Hide()
			self.TELEPORT_ITEMS[bCategoryID].remove(rItem)
			for rItem2 in self.Objects["ITEMS"].itemList:
				if rItem2.GetHash() == sItemHash:
					self.Objects["ITEMS"].RemoveItem(rItem2)
		else:
			teleportItem = self.ItemWindow(self, bCategoryID, sCategoryName, sItemHash)

			if not bCategoryID in self.TELEPORT_ITEMS:
				self.TELEPORT_ITEMS[bCategoryID] = []

			self.TELEPORT_ITEMS[bCategoryID].append(teleportItem)
			if self.iCurrentCategory == bCategoryID:
				self.Objects["ITEMS"].AppendItem(teleportItem)
	""" """

	def	OnWheelMove(self, iLen):
		if not self.IsShow():
			return

		self.Objects["ITEMS"].scrollBar.OnScrollWheelEvent(iLen)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			## Seleting category
			self.__OnSelectCategory(self.Objects["CATEGORIES"].itemList[0])

			self.Show()
			self.SetTop()

	def Open(self):
		self.Show()
	
	def Close(self):
		self.Hide()

	def	OnUpdate(self):
		for rItem in self.Objects["ITEMS"].itemList:
			rItem.OnUpdate()
