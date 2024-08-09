import ui
import uiScriptLocale
import wndMgr
import player
import localeInfo
import net
import app
import constInfo
import uiToolTip
import item
import chat
import grp
import chr
import math
import uiCommon

import introInterface
import interfaceModule

MAX_MAKE_QUANTITY = 200
MAX_MATERIAL_COUNT = 5
MAX_MATERIAL_QUANTITY = 1000
USE_CUBE_DISTANCE = 1000

ROOT_PATH = "d:/ymir work/ui/game/cube/"

CUBE_CATEGORY_NAME = (
	localeInfo.CUBE_CATEGORY_WEAPONPVP,
	localeInfo.CUBE_CATEGORY_ARMORPVM,
	localeInfo.CUBE_CATEGORY_ARMORPVP,
	localeInfo.CUBE_CATEGORY_ACCESSORYPVM,
	localeInfo.CUBE_CATEGORY_ACCESSORYPVP,
	localeInfo.CUBE_CATEGORY_SHIELDSPVM,
	localeInfo.CUBE_CATEGORY_SHIELDSPVP,
	localeInfo.CUBE_CATEGORY_HELMETPVM,
	localeInfo.CUBE_CATEGORY_HELMETPVP,
	localeInfo.CUBE_CATEGORY_BRACELETPVM,
	localeInfo.CUBE_CATEGORY_BRACELETPVP,
	localeInfo.CUBE_CATEGORY_NECKLACEPVM,
	localeInfo.CUBE_CATEGORY_NECKLACEPVP,
	localeInfo.CUBE_CATEGORY_EARRINGSPVM,
	localeInfo.CUBE_CATEGORY_EARRINGSPVP,
	localeInfo.CUBE_CATEGORY_SHOESPVM,
	localeInfo.CUBE_CATEGORY_SHOESPVP,
	localeInfo.CUBE_CATEGORY_BELTPVM,
	localeInfo.CUBE_CATEGORY_BELTPVP,
	localeInfo.CUBE_CATEGORY_EVENT,
	localeInfo.CUBE_CATEGORY_ETC,
	localeInfo.CUBE_CATEGORY_PET,
	localeInfo.CUBE_CATEGORY_MOUNT,
	localeInfo.CUBE_CATEGORY_SOULS,
	localeInfo.CUBE_CATEGORY_SOULS_SCROLLS,
	localeInfo.CUBE_CATEGORY_REFINE_SCROLLS,
)

'''
dict = {
	1 : {
		"this" : categoryObject,
		"items" : {
			"71084.200" : {
				"this" : itemObject,
				"second" : [ itemIndex : secondObject1, itemIndex : secondObject2 ],
			},

			"71084.100" : {
				"this" : itemObject,
				"second" : [ itemIndex : secondObject1, itemIndex : secondObject2 ],
			},
		}
	}
}
'''

class ItemCategoryObject(ui.Button):
	def __init__(self):
		ui.Button.__init__(self)

		self.bStatus = False

		self.openImage = ui.ImageBox()
		self.openImage.AddFlag("not_pick")
		self.openImage.SetParent(self)
		self.openImage.SetPosition(4, 3)
		self.openImage.LoadImage(ROOT_PATH + "cube_menu_tab1_plus.sub")
		self.openImage.Show()

	def __del__(self):
		del self.openImage

		self.bStatus = False

		ui.Button.__del__(self)

	def SetStatus(self, isOpened):
		if isOpened:
			self.openImage.LoadImage(ROOT_PATH + "cube_menu_tab1_minus.sub")
		else:
			self.openImage.LoadImage(ROOT_PATH + "cube_menu_tab1_plus.sub")

		self.bStatus = isOpened

	def GetStatus(self):
		return self.bStatus

class ItemObject(ui.Button):
	def __init__(self, itemVnum, itemCount):
		ui.Button.__init__(self)

		self.bStatus = False
		self.makeCount = 0
		self.itemVnum = itemVnum

		self.openImage = ui.ImageBox()
		self.openImage.AddFlag("not_pick")
		self.openImage.SetParent(self)
		self.openImage.SetPosition(5, 5)
		self.openImage.LoadImage(ROOT_PATH + "cube_menu_tab2_plus.sub")
		self.openImage.Show()

		self.RefreshText()

	def __del__(self):
		del self.openImage

		self.bStatus = False
		self.makeCount = 0
		self.itemVnum = 0

		ui.Button.__del__(self)

	def SetStatus(self, isOpened):
		if isOpened:
			self.openImage.LoadImage(ROOT_PATH + "cube_menu_tab2_minus.sub")
		else:
			self.openImage.LoadImage(ROOT_PATH + "cube_menu_tab2_plus.sub")

		self.bStatus = isOpened
		self.RefreshText()

	def SetMakeCount(self, makeCount):
		self.makeCount = makeCount
		self.RefreshText()

	def RefreshText(self):
		self.AppendTextLineAllClear()

		item.SelectItem(self.itemVnum)

		itemName = "|cffc5b44a|H|h%s|h|r" % item.GetItemName() if self.bStatus else item.GetItemName()
		lineText = "%s" % itemName if not self.makeCount else "|cff8ab98e|H|h[%d]|h|r %s" % (self.makeCount, itemName)

		self.AppendTextLine(text = lineText, text_sort = "left", pos_x = 20, pos_y = 8)

	def GetStatus(self):
		return self.bStatus

class ItemDetailObject(ui.ToggleButton):
	def __init__(self, itemVnum, itemCount, succesPercent):
		ui.ToggleButton.__init__(self)

		self.itemVnum = 0
		self.itemCount = 0
		self.succesPercent = 0
		self.bStatus = False
		self.makeCount = 0

		self.SetItemInfo(itemVnum, itemCount, succesPercent)

	def __del__(self):
		self.itemVnum = 0
		self.itemCount = 0
		self.succesPercent = 0
		self.bStatus = False
		self.makeCount = 0

		ui.ToggleButton.__del__(self)

	def SetStatus(self, isSelected):
		self.bStatus = isSelected

	def SetItemInfo(self, itemVnum, itemCount, succesPercent):
		self.SetStatus(False)
		self.itemVnum = itemVnum
		self.itemCount = itemCount
		self.succesPercent = succesPercent

		self.AppendTextLineAllClear()

		item.SelectItem(self.itemVnum)
		lineText = "%s [%d%%]" % (item.GetItemName(), succesPercent) if not self.makeCount else "|cff8ab98e|H|h[%d]|h|r %s |cff8ab98e|H|h[%d%%]|h|r" % (self.makeCount, item.GetItemName(), succesPercent)
		self.AppendTextLine(text = lineText, text_sort = "left", pos_x = 20, pos_y = 8)

	def SetMakeCount(self, makeCount):
		self.makeCount = makeCount

		self.AppendTextLineAllClear()

		item.SelectItem(self.itemVnum)
		lineText = "%s [%d%%]" % (item.GetItemName(), self.succesPercent) if not self.makeCount else "|cff8ab98e|H|h[%d]|h|r %s |cff8ab98e|H|h[%d%%]|h|r" % (self.makeCount, item.GetItemName(), self.succesPercent)
		self.AppendTextLine(text = lineText, text_sort = "left", pos_x = 20, pos_y = 8)

	def GetStatus(self):
		return self.bStatus

class SmallScrollBar(ui.Window):
	SCROLLBAR_WIDTH = 4

	class MiddleBar(ui.DragButton):
		def __init__(self):
			ui.DragButton.__init__(self)
			self.AddFlag("movable")

		def MakeImage(self):
			middleBar = ui.Bar()
			middleBar.SetParent(self)
			middleBar.AddFlag("not_pick")
			middleBar.SetPosition(0, 0)
			middleBar.SetColor(grp.GenerateColor(0.83, 0.80, 0.75, 1.0))
			middleBar.Show()
			self.middleBar = middleBar

		def SetSize(self, width, height):
			ui.DragButton.SetSize(self, width, height)

			if self.middleBar:
				self.middleBar.SetSize(width, height)

	def __init__(self):
		ui.Window.__init__(self)

		self.tHeight = 0
		self.mbHeight = 0
		self.scrollStep = 0.20
		self.curPos = 0.0

		self.eventScroll = lambda *arg: None

	def __del__(self):
		ui.Window.__del__(self)

	def CreateScrollBar(self):
		barSlot = ui.Bar()
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		barSlot.SetColor(grp.GenerateColor(0.73, 0.70, 0.65, 0.5))
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(ui.__mem_func__(self.OnMove))
		middleBar.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.MiddleButtonDragEnd))
		middleBar.Show()
		middleBar.MakeImage()

		self.middleBar = middleBar
		self.barSlot = barSlot

	def Destroy(self):
		self.middleBar = None
		self.barSlot = None

		self.tHeight = 0
		self.mbHeight = 0
		self.scrollStep = 0.20
		self.curPos = 0.0

		self.eventScroll = lambda *arg: None

	def SetBgSize(self, height):
		self.SetSize(self.SCROLLBAR_WIDTH, height)

		if self.barSlot:
			self.barSlot.SetSize(self.SCROLLBAR_WIDTH, height)

		if self.middleBar:
			self.middleBar.SetRestrictMovementArea(0, 0, self.SCROLLBAR_WIDTH, height)

		self.tHeight = height

	def SetMiddleSize(self, height):
		if self.middleBar:
			self.middleBar.SetSize(self.SCROLLBAR_WIDTH, height)

		self.mbHeight = height

	def OnMove(self):
		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal) / float(self.tHeight - self.mbHeight)

		self.eventScroll()

	def MiddleButtonDragEnd(self):
		pass

	def GetPos(self):
		return self.curPos

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		self.middleBar.SetPosition(self.SCROLLBAR_WIDTH, int(pos * int(self.tHeight - self.mbHeight)))
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos - self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos + self.scrollStep)

	## ScrollBar Wheel Support
	def OnWheelMove(self, iLen):
		pos = self.GetPos()

		## Computing mouse move range (by percent)
		iLen = (float(abs(iLen)-100)/100.0)*(iLen/abs(iLen))

		## Mouse Inversion
		iLen *= -1

		pos += iLen
		self.SetPos(pos)
		return True

class CubeWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.SetWindowName("CubeWindow")

		self.Initialize()

	def Initialize(self):
		self.xStart = 0
		self.yStart = 0
		self.npcVnum = 0
		self.yPos = 4
		self.selectedItemIndex = -1
		self.posInList = -1
		self.makeCount = 1
		self.startPos = 0
		self.isIncrease = False

		self.titleBar = None
		self.itemListBoard = None
		self.scrollBar = None
		self.resultSlot = None
		self.materialSlot = None
		self.resultQty = None
		self.materialQty = [None for i in xrange(MAX_MATERIAL_COUNT)]
		self.yangText = None
		self.buttonOk = None
		self.buttonCancel = None
		self.qtySubButton = None
		self.qtyAddButton = None
		self.incPercentSlot = None
		self.incPercentText = None

		self.tooltipItem = None
		self.questionDialog = None

		if app.ENABLE_CUBE_RENEWAL_COPY_BONUS:
			self.copyBonusQuestionDialog = None
		self.wndInterface = None

		if constInfo.ENABLE_CUBE_MARK_MATERIAL:
			self.materialSlotList = []

		self.itemList = {}

		self.showDict = { "category" : [], "item" : [], "item_s" : [] }

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def BindInterface(self, interface):
		self.wndInterface = interface

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CubeRenewalWindow.py")
		except:
			import exception
			exception.Abort("CubeWindow.LoadDialog.LoadScript")

		try:
			self.titleBar = self.GetChild("board")
			self.itemListBoard = self.GetChild("item_list_board")
			self.resultSlot = self.GetChild("ResultSlot")
			self.materialSlot = self.GetChild("MaterialSlot")
			self.resultQty = self.GetChild("result_qty")
			self.yangText = self.GetChild("yang_text")
			for i in xrange(MAX_MATERIAL_COUNT):
				self.materialQty[i] = self.GetChild("material_qty_text_%d" % (i+1))

			self.buttonOk = self.GetChild("button_ok")
			self.buttonCancel = self.GetChild("button_cancel")
			self.qtySubButton = self.GetChild("qty_sub_button")
			self.qtyAddButton = self.GetChild("qty_add_button")
			self.incPercentSlot = self.GetChild("imporve_slot")
			self.incPercentText = self.GetChild("improve_text")
		except:
			import exception
			exception.Abort("CubeWindow.LoadDialog.BindObject")

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.__OnClickClose))
		self.yangText.SetText("0")

		scrollBar = SmallScrollBar()
		scrollBar.SetParent(self.itemListBoard)
		scrollBar.CreateScrollBar()
		scrollBar.SetBgSize(246)
		scrollBar.SetMiddleSize(90)
		scrollBar.SetPosition(7, 3)
		scrollBar.SetWindowHorizontalAlignRight()
		scrollBar.SetScrollEvent(ui.__mem_func__(self.__OnScrollItemList))
		scrollBar.Hide()
		self.scrollBar = scrollBar

		if app.ENABLE_MOUSE_WHEEL_EVENT:
			## ScrollBar Wheel Support
			self.SetScrollWheelEvent(self.scrollBar.OnWheelMove)

		self.resultSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInResultItem))
		self.resultSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		self.resultSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectResultSlot))

		self.incPercentSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInIncreaseItem))
		self.incPercentSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		self.incPercentSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemIncrease))
		self.incPercentSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__OnSelectItemIncrease))

		self.materialSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInMaterialItem))
		self.materialSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		self.materialSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectMaterialSlot))

		self.buttonOk.SetEvent(ui.__mem_func__(self.__OnClickCubeMake))
		self.buttonCancel.SetEvent(ui.__mem_func__(self.__OnClickClose))

		self.qtySubButton.SetEvent(ui.__mem_func__(self.__OnClickQtySubButton))
		self.qtyAddButton.SetEvent(ui.__mem_func__(self.__OnClickQtyAddButton))

		self.resultSlot.ClearSlot(0)
		self.incPercentSlot.ClearSlot(0)
		for m in xrange(MAX_MATERIAL_COUNT):
			self.materialSlot.ClearSlot(m)

		self.incPercentText.SetText(uiScriptLocale.CUBE_RENEWAL_BELT_IMPROVE)

		self.incPercentSlot.SetCoverButton(0, "assets/ui/elements/locked_slot/big.dds",\
													"assets/ui/elements/locked_slot/big.dds",\
													"assets/ui/elements/locked_slot/big.dds",\
													"assets/ui/elements/locked_slot/big.dds", False, False)

		self.incPercentSlot.SetAlwaysRenderCoverButton(0, True)

	def Destroy(self):
		self.itemList.clear()

		if self.questionDialog:
			self.questionDialog.Close()

		if app.ENABLE_CUBE_RENEWAL_COPY_BONUS:
			if self.copyBonusQuestionDialog:
				self.copyBonusQuestionDialog.Close()

		self.Initialize()
		self.ClearDictionary()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def Open(self, npcVnum = 20018):
		(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()
		self.npcVnum = npcVnum

		self.scrollBar.SetPos(0.0)
		self.RefreshCubeWindow()

		self.Show()
		self.SetCenterPosition()
		self.SetTop()

	def Close(self):
		self.itemList.clear()

		self.resultSlot.ClearSlot(0)
		self.incPercentSlot.DeactivateSlot(0)
		self.incPercentSlot.ClearSlot(0)
		for m in xrange(MAX_MATERIAL_COUNT):
			self.materialSlot.ClearSlot(m)

		self.incPercentText.SetText(uiScriptLocale.CUBE_RENEWAL_BELT_IMPROVE)

		if self.questionDialog:
			self.questionDialog.Close()
			self.questionDialog = None

		if app.ENABLE_CUBE_RENEWAL_COPY_BONUS:
			if self.copyBonusQuestionDialog:
				self.copyBonusQuestionDialog.Close()
				self.copyBonusQuestionDialog = None

		self.selectedItemIndex = -1
		self.posInList = -1
		self.makeCount = 1
		self.isIncrease = False
		self.startPos = 0
		self.npcVnum = 0
		self.showDict = { "category" : [], "item" : [], "item_s" : [] }

		self.resultQty.SetText("")
		for m in self.materialQty:
			m.SetText("")

		self.yangText.SetText("0")

		if constInfo.ENABLE_CUBE_MARK_MATERIAL:
			self.RefreshInventoryPage(True)

		self.Hide()

	def OnPressEscapeKey(self):
		self.__OnClickClose()
		return True

	def OnUpdate(self):
		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xStart) > USE_CUBE_DISTANCE or abs(y - self.yStart) > USE_CUBE_DISTANCE:
			self.RemoveFlag("animate")
			self.__OnClickClose()

	def RefreshCubeWindow(self):
		if not self.npcVnum:
			return

		cubeSize = player.GetCubeListSize(self.npcVnum)
		if not cubeSize:
			return

		for i in xrange(cubeSize):
			(itemIndex, itemPercent, _, bCategory, rewardItem, _, _, _, _) = player.GetCubeItem(self.npcVnum, i)

			if not bCategory in self.showDict["category"]:
				self.showDict["category"].append(bCategory)

			if not self.itemList.has_key(bCategory):
				catBtn = ItemCategoryObject()
				catBtn.SetParent(self.itemListBoard)
				catBtn.SetUpVisual(ROOT_PATH + "cube_menu_tab1.sub")
				catBtn.SetOverVisual(ROOT_PATH + "cube_menu_tab1.sub")
				catBtn.SetDownVisual(ROOT_PATH + "cube_menu_tab1.sub")
				catBtn.AppendTextLine(text = CUBE_CATEGORY_NAME[bCategory], text_sort = "left", pos_x = 30, pos_y = 9)
				catBtn.SetEvent(ui.__mem_func__(self.__OnClickCategory), bCategory)
				catBtn.Hide()

				self.itemList[bCategory] = { "this" : catBtn, "items" : {} }

			itemKey = "%d.%d" % (rewardItem[0], rewardItem[1])
			if not self.itemList[bCategory]["items"].has_key(itemKey):
				itemBtn = ItemObject(rewardItem[0], rewardItem[1])
				itemBtn.SetParent(self.itemListBoard)
				itemBtn.SetUpVisual(ROOT_PATH + "cube_menu_tab2.sub")
				itemBtn.SetOverVisual(ROOT_PATH + "cube_menu_tab2.sub")
				itemBtn.SetDownVisual(ROOT_PATH + "cube_menu_tab2.sub")
				itemBtn.SetEvent(ui.__mem_func__(self.__OnClickItem), itemKey, bCategory)
				itemBtn.Hide()

				self.itemList[bCategory]["items"][itemKey] = { "this" : itemBtn, "second" : {} }

			if self.itemList[bCategory]["items"].has_key(itemKey):
				if self.itemList[bCategory]["items"][itemKey]["second"].has_key(itemIndex):
					self.itemList[bCategory]["items"][itemKey]["second"][itemIndex].SetItemInfo(rewardItem[0], rewardItem[1], itemPercent)
					self.itemList[bCategory]["items"][itemKey]["second"][itemIndex].SetToggleUpEvent(ui.__mem_func__(self.__OnClickItemSecond), self.npcVnum, i)
					self.itemList[bCategory]["items"][itemKey]["second"][itemIndex].SetToggleDownEvent(ui.__mem_func__(self.__OnClickItemSecond), self.npcVnum, i)
				else:
					itemBtn = ItemDetailObject(rewardItem[0], rewardItem[1], itemPercent)
					itemBtn.SetParent(self.itemListBoard)
					itemBtn.SetUpVisual(ROOT_PATH + "cube_menu_tab3_default.sub")
					itemBtn.SetOverVisual(ROOT_PATH + "cube_menu_tab3_select.sub")
					itemBtn.SetDownVisual(ROOT_PATH + "cube_menu_tab3_select.sub")
					itemBtn.SetToggleUpEvent(ui.__mem_func__(self.__OnClickItemSecond), self.npcVnum, i)
					itemBtn.SetToggleDownEvent(ui.__mem_func__(self.__OnClickItemSecond), self.npcVnum, i)
					itemBtn.Hide()
					self.itemList[bCategory]["items"][itemKey]["second"][itemIndex] = itemBtn

		self.RefreshMakeCount()
		self.scrollBar.SetPos(0.0)
		self.SortInfoDict()
		self.RefreshShowList()
		self.CheckScrollBar()

	def SortInfoDict(self):
		self.showDict["category"] = sorted(self.showDict["category"])
		self.showDict["item"] = sorted(self.showDict["item"])
		self.showDict["item_s"] = sorted(self.showDict["item_s"])

	def CheckScrollBar(self):
		totalCount = len(self.showDict["category"]) + len(self.showDict["item"]) + len(self.showDict["item_s"])
		if totalCount > 12:
			self.scrollBar.Show()
			self.scrollBar.SetScrollStep(float(1.0 / (totalCount - 12)))
		else:
			self.scrollBar.Hide()

	def RefreshShowList(self):
		for catDict in self.itemList.values():
			catDict["this"].Hide()
			for itemDict in catDict["items"].values():
				itemDict["this"].Hide()
				for itemSecond in itemDict["second"].values():
					itemSecond.Hide()

		yPos = 4

		totalCount = len(self.showDict["category"]) + len(self.showDict["item"]) + len(self.showDict["item_s"])
		showCount = max(0, totalCount - 11)
		showStart = int(showCount * self.scrollBar.GetPos())
		showIndex = 0

		for c in self.showDict["category"]:
			category = self.GetCategory(c)
			if category:
				showIndex += 1
				if yPos + 20 > self.itemListBoard.GetHeight():
					continue

				if showIndex < showStart:
					category.Hide()
				else:
					category.SetPosition(4, yPos)
					category.Show()
					yPos += 20

				for i in self.showDict["item"]:
					item = self.GetItem(i, c)
					if item:
						showIndex += 1
						if yPos + 20 > self.itemListBoard.GetHeight():
							continue

						if showIndex < showStart:
							item.Hide()
						else:
							item.SetPosition(20, yPos)
							item.Show()
							yPos += 20

						for s in self.showDict["item_s"]:
							itemS = self.GetItemS(s, i, c)
							if itemS:
								showIndex += 1
								if yPos + 20 > self.itemListBoard.GetHeight():
									continue

								if showIndex < showStart:
									itemS.Hide()
								else:
									itemS.SetPosition(40, yPos)
									itemS.Show()
									yPos += 20

	def GetCategory(self, catIndex):
		if self.itemList.has_key(catIndex):
			if self.itemList[catIndex].has_key("this"):
				return self.itemList[catIndex]["this"]

		return None

	def GetItem(self, itemKey, catIndex):
		if self.itemList.has_key(catIndex):
			if self.itemList[catIndex].has_key("items"):
				if self.itemList[catIndex]["items"].has_key(itemKey):
					return self.itemList[catIndex]["items"][itemKey]["this"]

		return None

	def GetItemS(self, itemIndex, itemKey, catIndex):
		if self.itemList.has_key(catIndex):
			if self.itemList[catIndex].has_key("items"):
				if self.itemList[catIndex]["items"].has_key(itemKey):
					if self.itemList[catIndex]["items"][itemKey].has_key("second"):
						if self.itemList[catIndex]["items"][itemKey]["second"].has_key(itemIndex):
							return self.itemList[catIndex]["items"][itemKey]["second"][itemIndex]

		return None

	def GetItemSI(self, itemIndex):
		for catDict in self.itemList.values():
			for itemDict in catDict["items"].values():
				for key, itemSecond in itemDict["second"].iteritems():
					if key == itemIndex:
						return itemSecond

		return None

	def __OnClickClose(self):
		net.SendCubeClose()
		self.Close()

	def __OnClickCategory(self, catIndex):
		category = self.GetCategory(catIndex)
		if category:
			if not category.GetStatus():
				category.SetStatus(True)

				for key in self.itemList[catIndex]["items"].keys():
					if not key in self.showDict["item"]:
						self.showDict["item"].append(key)
			else:
				category.SetStatus(False)

				newList = []

				for i in self.showDict["item"]:
					if not i in self.itemList[catIndex]["items"].keys():
						newList.append(i)

				self.showDict["item"] = newList

			self.SortInfoDict()
			self.RefreshShowList()
			self.CheckScrollBar()

	def __OnClickItem(self, itemKey, catIndex):
		item = self.GetItem(itemKey, catIndex)
		if item:
			if not item.GetStatus():
				item.SetStatus(True)

				for key in self.itemList[catIndex]["items"][itemKey]["second"].keys():
					if not key in self.showDict["item_s"]:
						self.showDict["item_s"].append(key)
			else:
				item.SetStatus(False)

				newList = []

				for i in self.showDict["item_s"]:
					if not i in self.itemList[catIndex]["items"][itemKey]["second"].keys():
						newList.append(i)

				self.showDict["item_s"] = newList

			self.SortInfoDict()
			self.RefreshShowList()
			self.CheckScrollBar()

	def __OnClickItemSecond(self, npcVnum, iPos):
		curItem = self.GetItemSI(self.selectedItemIndex)
		if curItem:
			curItem.SetUp()

		self.resultSlot.ClearSlot(0)
		self.incPercentSlot.DeactivateSlot(0)
		self.incPercentSlot.ClearSlot(0)
		for m in xrange(MAX_MATERIAL_COUNT):
			self.materialSlot.ClearSlot(m)

		self.incPercentText.SetText(uiScriptLocale.CUBE_RENEWAL_BELT_IMPROVE)

		self.resultQty.SetText("")
		for m in self.materialQty:
			m.SetText("")

		if self.questionDialog:
			self.questionDialog.Close()
			self.questionDialog = None

		if app.ENABLE_CUBE_RENEWAL_COPY_BONUS:
			if self.copyBonusQuestionDialog:
				self.copyBonusQuestionDialog.Close()
				self.copyBonusQuestionDialog = None

		self.yangText.SetText("0")
		self.yangText.SetPackedFontColor(0xffdddddd)

		self.makeCount = 1
		self.isIncrease = False

		if constInfo.ENABLE_CUBE_MARK_MATERIAL:
			self.RefreshInventoryPage(True)

		tReturn = player.GetCubeItem(npcVnum, iPos)
		if type(tReturn).__name__ == "tuple": ## A little hardcoded
			(itemIndex, _, needGold, bCategory, rewardItem, copyBonus, incPercValue, incPercItem, materialList) = tReturn
			needGold = long(needGold)
			if itemIndex == self.selectedItemIndex:
				self.selectedItemIndex = -1
				self.posInList = -1

				if constInfo.ENABLE_CUBE_MARK_MATERIAL:
					self.RefreshInventoryPage(True)

				return

			self.selectedItemIndex = itemIndex
			self.posInList = iPos

			itemKey = "%d.%d" % (rewardItem[0], rewardItem[1])
			itemS = self.GetItemS(itemIndex, itemKey, bCategory)
			if itemS:
				itemS.Down()

			if constInfo.ENABLE_CUBE_MARK_MATERIAL:
				materialVnum = []
				for material in materialList:
					materialVnum.append(material[0])

				for i in xrange(player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT):
					itemVnum = player.GetItemIndex(i)
					if itemVnum in materialVnum:
						self.materialSlotList.append(i)

				self.RefreshInventoryPage()

			self.RefreshSelectText(needGold, rewardItem, incPercValue, incPercItem, materialList)

	def RefreshSelectText(self, needGold, rewardItem, incPercValue, incPercItem, materialList):
		realNeedGold = long(needGold * self.makeCount)
		self.yangText.SetText(localeInfo.AddPointToNumberString(realNeedGold))
		if player.GetElk() < realNeedGold:
			self.yangText.SetPackedFontColor(grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0))
		else:
			self.yangText.SetPackedFontColor(grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0))

		self.resultSlot.SetItemSlot(0, rewardItem[0], rewardItem[1])
		self.resultQty.SetText(str(rewardItem[1] * self.makeCount))

		if incPercItem[0] and incPercItem[1]:
			newTuple = (incPercItem[0], incPercItem[1] * self.makeCount)
			incPercItem = newTuple
			self.incPercentSlot.SetItemSlot(0, incPercItem[0], incPercItem[1])

		if self.isIncrease and incPercItem[0]:
			if player.GetItemCountByVnum(incPercItem[0]) < incPercItem[1]:
				self.isIncrease = False

		if self.isIncrease:
			self.incPercentSlot.ActivateSlot(0)

			incText = " (%d%%)" % (incPercValue)
			self.incPercentText.SetText(uiScriptLocale.CUBE_RENEWAL_BELT_IMPROVE + incText)
		else:
			self.incPercentSlot.DeactivateSlot(0)
			self.incPercentText.SetText(uiScriptLocale.CUBE_RENEWAL_BELT_IMPROVE)

		for i, material in enumerate(materialList):
			self.materialSlot.SetItemSlot(i, material[0], material[1])

			needCount = material[1] * self.makeCount
			myCount = player.GetItemCountByVnum(material[0])
			myCount = min(MAX_MATERIAL_QUANTITY, myCount)
			self.materialQty[i].SetText("%d/%d" % (myCount, needCount))

			if myCount >= needCount:
				self.materialSlot.UnlockSlot(i)
				self.materialQty[i].SetPackedFontColor(grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0))
			else:
				self.materialSlot.LockSlot(i)
				self.materialQty[i].SetPackedFontColor(grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0))

		self.RefreshMakeCount()

	def RefreshMakeCount(self):
		if not self.npcVnum:
			return

		cubeSize = player.GetCubeListSize(self.npcVnum)
		if not cubeSize:
			return

		for i in xrange(cubeSize):
			(itemIndex, itemPercent, needGold, bCategory, rewardItem, copyBonus, incPercValue, incPercItem, materialList) = player.GetCubeItem(self.npcVnum, i)

			checkMakeCount = self.makeCount if itemIndex == self.selectedItemIndex else 1

			haveAllMaterial = True
			for i, material in enumerate(materialList):
				needCount = material[1] * checkMakeCount
				if player.GetItemCountByVnum(material[0]) < material[1]:
					haveAllMaterial = False
					break

			if haveAllMaterial:
				itemKey = "%d.%d" % (rewardItem[0], rewardItem[1])
				item = self.GetItem(itemKey, bCategory)
				if item:
					item.SetMakeCount(checkMakeCount)
				else:
					item.SetMakeCount(0)

				itemS = self.GetItemS(itemIndex, itemKey, bCategory)
				if itemS:
					itemS.SetMakeCount(checkMakeCount)
				else:
					itemS.SetMakeCount(0)

	def Refresh(self):
		if self.selectedItemIndex == -1:
			return

		if self.posInList != -1 and self.npcVnum != 0:
			tReturn = player.GetCubeItem(self.npcVnum, self.posInList)
			if type(tReturn).__name__ == "tuple":
				(itemIndex, _, needGold, _, rewardItem, copyBonus, incPercValue, incPercItem, materialList) = tReturn

				needGold = long(needGold)
				self.RefreshSelectText(needGold, rewardItem, incPercValue, incPercItem, materialList)

	def __OverInResultItem(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			itemIndex = self.resultSlot.GetItemIndex(slotIndex)
			if itemIndex:
				self.tooltipItem.AddItemData(itemIndex, metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])
				#self.tooltipItem.SetHideTooltip(True)
				self.tooltipItem.ShowToolTip()

				if app.INGAME_WIKI:
					self.tooltipItem.AppendShortcut(*(introInterface.GetWindowConfig("shortcust_windows", introInterface.WIKI_WND, "desc")))

	def __SelectResultSlot(self, slotIndex):
		itemIndex = self.resultSlot.GetItemIndex(slotIndex)
		if itemIndex:
			if app.IsPressed(introInterface.GetWindowConfig("shortcust_windows", introInterface.ITEM_PREVIEW, "key")) and app.ENABLE_RENDER_TARGET_EXTENSION:
				item.SelectItem(itemIndex)
				if item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_COSTUME, item.ITEM_TYPE_TOGGLE):
					interfaceModule.GetInstance().OpenPreviewWindow(itemIndex)
					return

			if app.IsPressed(introInterface.GetWindowConfig("shortcust_windows", introInterface.WIKI_WND, "key")) and app.INGAME_WIKI:
				interfaceModule.GetInstance().wikiExtension_searchVnum(itemIndex)

	def __OverInMaterialItem(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			itemIndex = self.materialSlot.GetItemIndex(slotIndex)
			if itemIndex:
				self.tooltipItem.AddItemData(itemIndex, metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])
				#self.tooltipItem.SetHideTooltip(True)
				self.tooltipItem.ShowToolTip()

				if app.INGAME_WIKI:
					self.tooltipItem.AppendShortcut(*(introInterface.GetWindowConfig("shortcust_windows", introInterface.WIKI_WND, "desc")))

	def __OverInIncreaseItem(self, slotIndex):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			itemIndex = self.incPercentSlot.GetItemIndex(slotIndex)
			if itemIndex:
				self.tooltipItem.AddItemData(itemIndex, [0, 0, 0])
				self.tooltipItem.ShowToolTip()

	def __OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def __SelectMaterialSlot(self, slotIndex):
		itemIndex = self.materialSlot.GetItemIndex(slotIndex)
		if itemIndex:
			if app.IsPressed(introInterface.GetWindowConfig("shortcust_windows", introInterface.ITEM_PREVIEW, "key")) and app.ENABLE_RENDER_TARGET_EXTENSION:
				item.SelectItem(itemIndex)
				if item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_COSTUME, item.ITEM_TYPE_TOGGLE):
					interfaceModule.GetInstance().OpenPreviewWindow(itemIndex)
					return

			if app.IsPressed(introInterface.GetWindowConfig("shortcust_windows", introInterface.WIKI_WND, "key")) and app.INGAME_WIKI:
				interfaceModule.GetInstance().wikiExtension_searchVnum(itemIndex)

	def __OnScrollItemList(self):
		totalCount = len(self.showDict["category"]) + len(self.showDict["item"]) + len(self.showDict["item_s"])
		showCount = max(0, totalCount - 12)
		showStart = int(showCount * self.scrollBar.GetPos())

		if showStart != self.startPos:
			self.RefreshShowList()
			self.startPos = showStart

	def __OnClickCubeMake(self):
		if self.selectedItemIndex == -1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CUBE_PLEASE_SELECT)
			return

		if self.posInList != -1 and self.npcVnum != 0:
			tReturn = player.GetCubeItem(self.npcVnum, self.posInList)
			if type(tReturn).__name__ == "tuple":
				(_, _, needGold, _, rewardItem, copyBonus, _, _, materialList) = tReturn

				needGold = long(needGold)
				realNeedGold = long(needGold * self.makeCount)
				if player.GetElk() < realNeedGold:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CUBE_NOT_ENOUGH_GOLD)
					return

				haveMaterial = True
				for i, material in enumerate(materialList):
					realMaterialCount = material[1] * self.makeCount
					if player.GetItemCountByVnum(material[0]) < realMaterialCount:
						haveMaterial = False

				if not haveMaterial:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CUBE_NOT_ENOUGH_MATERIAL)
					return

				if copyBonus:
					fromVnum = 0
					metinSlot = []
					attrSlot = []
					for i, material in enumerate(materialList):
						item.SelectItem(material[0])
						# It's the right material, not let's find it in inventory
						foundMaterial = False
						if item.GetItemType() == item.ITEM_TYPE_WEAPON or item.GetItemType() == item.ITEM_TYPE_ARMOR:
							# Inventory search only
							for i in xrange(player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT):
								if player.GetItemIndex(i) == material[0]: # Bingo
									fromVnum = player.GetItemIndex(i)
									metinSlot = [player.GetItemMetinSocket(i, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]
									attrSlot = [player.GetItemAttribute(i, j) for j in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
									foundMaterial = True
									break

						if foundMaterial:
							break

					if fromVnum and metinSlot and attrSlot:
						copyBonusQuestionDialog = uiCommon.QuestionCopyBonusDialog()
						copyBonusQuestionDialog.SetAcceptEvent(ui.__mem_func__(self.SendCubeMakeDialog), True)
						copyBonusQuestionDialog.SetCancelEvent(ui.__mem_func__(self.SendCubeMakeDialog), False)
						copyBonusQuestionDialog.SetFromInfo(fromVnum, metinSlot, attrSlot)
						copyBonusQuestionDialog.SetToInfo(rewardItem[0])
						copyBonusQuestionDialog.npcVnum = self.npcVnum
						copyBonusQuestionDialog.selectedItemIndex = self.selectedItemIndex
						copyBonusQuestionDialog.makeCount = self.makeCount
						copyBonusQuestionDialog.isIncrease = self.isIncrease
						copyBonusQuestionDialog.Open()
						self.copyBonusQuestionDialog = copyBonusQuestionDialog
				else:
					net.SendCubeMake(self.npcVnum, self.selectedItemIndex, self.makeCount, self.isIncrease)
	if app.ENABLE_CUBE_RENEWAL_COPY_BONUS:
		def SendCubeMakeDialog(self, answer):
			if not self.copyBonusQuestionDialog:
				return

			if answer:
				npcVnum = self.copyBonusQuestionDialog.npcVnum
				selectedItemIndex = self.copyBonusQuestionDialog.selectedItemIndex
				makeCount = self.copyBonusQuestionDialog.makeCount
				isIncrease = self.copyBonusQuestionDialog.isIncrease

				net.SendCubeMake(npcVnum, selectedItemIndex, makeCount, isIncrease)

			self.copyBonusQuestionDialog.Close()
			self.copyBonusQuestionDialog = None
	def __OnClickQtySubButton(self):
		if self.selectedItemIndex == -1:
			return

		if self.posInList != -1 and self.npcVnum != 0:
			tReturn = player.GetCubeItem(self.npcVnum, self.posInList)
			if type(tReturn).__name__ == "tuple":
				(_, _, needGold, _, rewardItem, copyBonus, incPercValue, incPercItem, materialList) = tReturn

				needGold = long(needGold)
				self.makeCount = max(self.makeCount - 1, 1)
				self.RefreshSelectText(needGold, rewardItem, incPercValue, incPercItem, materialList)

	def __OnClickQtyAddButton(self):
		if self.selectedItemIndex == -1:
			return

		if self.posInList != -1 and self.npcVnum != 0:
			tReturn = player.GetCubeItem(self.npcVnum, self.posInList)
			if type(tReturn).__name__ == "tuple":
				(_, _, needGold, _, rewardItem, copyBonus, incPercValue, incPercItem, materialList) = tReturn

				needGold = long(needGold)
				newCount = min(self.makeCount + 1, 200)
				realNeedGold = long(needGold * newCount)
				if player.GetElk() < realNeedGold:
					return

				haveMaterial = True
				for i, material in enumerate(materialList):
					realMaterialCount = material[1] * newCount
					if player.GetItemCountByVnum(material[0]) < realMaterialCount:
						haveMaterial = False

				rewardCount = rewardItem[1] * newCount
				if haveMaterial and rewardCount <= MAX_MAKE_QUANTITY:
					self.makeCount = newCount
					self.RefreshSelectText(needGold, rewardItem, incPercValue, incPercItem, materialList)

	def __AnswerSelectIncrease(self, flag):
		if flag:
			self.isIncrease = True
			self.Refresh()

		self.questionDialog.Close()
		self.questionDialog = None

	def __OnSelectItemIncrease(self, slotIndex):
		itemIndex = self.incPercentSlot.GetItemIndex(slotIndex)
		if itemIndex:
			if self.isIncrease:
				self.isIncrease = False
				self.Refresh()
			else:
				questionDialog = uiCommon.QuestionDialog2()
				questionDialog.SetText1(localeInfo.CUBE_ASK_USE_INCREASE_1)
				questionDialog.SetText2(localeInfo.CUBE_ASK_USE_INCREASE_2)
				questionDialog.SetAcceptEvent(lambda arg = True: self.__AnswerSelectIncrease(arg))
				questionDialog.SetCancelEvent(lambda arg = False: self.__AnswerSelectIncrease(arg))
				questionDialog.Open()
				self.questionDialog = questionDialog

	if constInfo.ENABLE_CUBE_MARK_MATERIAL:
		def RefreshInventoryPage(self, isClear = False):
			if isClear:
				self.materialSlotList = []

			if self.wndInterface:
				self.wndInterface.RefreshCubeInventoryBag()

		def IsMaterial(self, slotIndex):
			if slotIndex in self.materialSlotList:
				return True

			return False