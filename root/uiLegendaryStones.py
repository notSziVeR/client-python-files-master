"""File: root/uiCrafting.py"""

import itemWrapper, constInfo, interfaceModule
import ui, util, wndMgr, item, uiToolTip, mouseModule, localeInfo, uiScriptLocale, net, player, app
import math, random
from cff import CFF

class LegendaryStonesPassiveWindow(ui.MainBoardWithTitleBar):
	WINDOW_SIZE = [315, 256 + 33]
	PEEK_WINDOW_SIZE = [290, 246]
	PADDING_BETWEEN = -1
	SCROLL_SPEED = 50

	class WindowObject(ui.ExpandedImageBox):
		SIZE = [280, 49]

		def __init__(self):
			super(LegendaryStonesPassiveWindow.WindowObject, self).__init__()
			self.__BuildObject()
			self.Objects = {}
			self.Data = {}

			self.itemID = 0
			self.ToolTip = itemWrapper.ItemToolTipDummy(0)

		def __del__(self):
			return super(LegendaryStonesPassiveWindow.WindowObject, self).__del__()

		def __BuildObject(self):
			self.SetSize(*self.SIZE)
			# self.LoadImage()

		def AppendData(self, iVnum, iGived, iRequired, bUpdate = False):
			self.Data[iVnum] = (iGived, iRequired)
			self.itemID = iVnum
			
			if bUpdate:
				self.__Update()
				return

			self.__RegisterData()

		def __RegisterData(self):
			self.Objects["Slot"] = ui.ImageBoxNew()
			self.Objects["Slot"].SetParent(self)
			self.Objects["Slot"].SetSize(32, 32)
			self.Objects["Slot"].LoadImage("assets/ui/passive_system/slot.tga")
			self.Objects["Slot"].SetPosition(30, self.GetHeight() / 2 - self.Objects["Slot"].GetHeight() / 2)
			self.Objects["Slot"].SetEvent(self.__OverInItem, "MOUSE_OVER_IN")
			self.Objects["Slot"].SetEvent(self.__OverOutItem, "MOUSE_OVER_OUT")
			self.Objects["Slot"].Show()

			item.SelectItem(self.itemID)

			w, h = item.GetItemSize()

			self.Objects["ItemImage"] = ui.ExpandedImageBox()
			self.Objects["ItemImage"].SetParent(self.Objects["Slot"])
			self.Objects["ItemImage"].AddFlag("not_pick")
			self.Objects["ItemImage"].LoadImage(item.GetIconImageFileName())
			self.Objects["ItemImage"].SetPosition((self.Objects["Slot"].GetWidth() - 32 * w) / 2, (self.Objects["Slot"].GetHeight() - h * 32)/2)
			self.Objects["ItemImage"].Show()

			self.Objects["TextLine"] = ui.TextLine()
			self.Objects["TextLine"].SetParent(self)
			self.Objects["TextLine"].SetText("Oddano:")
			self.Objects["TextLine"].SetPosition(self.GetWidth() / 2 - self.Objects["TextLine"].GetTextSize()[0] / 2, self.GetHeight() / 2 - self.Objects["TextLine"].GetTextSize()[1] / 2)
			self.Objects["TextLine"].Show()

			IMAGES = [
				"assets/ui/passive_system/buttons/button_accept_0_norm.tga",
				"assets/ui/passive_system/buttons/button_accept_0_hover.tga",
				"assets/ui/passive_system/buttons/button_accept_0_down.tga",
				"assets/ui/passive_system/buttons/button_accept_1_norm.tga"
			]

			self.Objects["DataImage"] = ui.ExpandedImageBox()
			self.Objects["DataImage"].SetParent(self)
			self.Objects["DataImage"].AddFlag("not_pick")
			self.Objects["DataImage"].LoadImage("assets/ui/passive_system/background_data_0.tga")
			self.Objects["DataImage"].SetPosition(self.Objects["TextLine"].GetLocalPosition()[0] + self.Objects["TextLine"].GetTextSize()[0], self.GetHeight() / 2 - self.Objects["DataImage"].GetHeight() / 2)
			self.Objects["DataImage"].Show()

			self.Objects["TextLine_Data"] = ui.TextLine()
			self.Objects["TextLine_Data"].SetParent(self.Objects["DataImage"])
			self.Objects["TextLine_Data"].SetText("0/12")
			self.Objects["TextLine_Data"].SetPosition(0, self.Objects["DataImage"].GetHeight() / 2 - self.Objects["TextLine_Data"].GetTextSize()[1] / 2)
			self.Objects["TextLine_Data"].SetWindowHorizontalAlignCenter()
			self.Objects["TextLine_Data"].SetHorizontalAlignCenter()
			self.Objects["TextLine_Data"].Show()

			self.Objects["Button"] = ui.Button()
			self.Objects["Button"].SetParent(self)
			self.Objects["Button"].SetUpVisual(IMAGES[0])
			self.Objects["Button"].SetOverVisual(IMAGES[1])
			self.Objects["Button"].SetDownVisual(IMAGES[2])
			self.Objects["Button"].SetDisableVisual(IMAGES[3])
			pos_y = self.GetHeight() / 2 - self.Objects["Button"].GetHeight() / 2 
			self.Objects["Button"].SetPosition(self.GetWidth() - (self.Objects["Button"].GetWidth() + 30), pos_y)
			self.Objects["Button"].SAFE_SetEvent(self.__GiveRequiredItem)
			self.Objects["Button"].Show()

			self.__Update()

		def getData(self):
			return self.Data.get(self.itemID)

		def completedTask(self):
			return self.getData()[0] == self.getData()[1]

		def __OverInItem(self):
			self.ToolTip.SetVnum(self.itemID)
			self.ToolTip.ShowToolTip()

		def __OverOutItem(self):
			self.ToolTip.HideToolTip()

		def __Update(self):
			MAIN = "assets/ui/passive_system/"
			IMAGES = [
				["{}{}".format(MAIN, "background_0.tga"), "{}{}".format(MAIN, "background_1.tga")],
				["{}{}".format(MAIN, "background_2.tga"), "{}{}".format(MAIN, "background_3.tga")]
			]

			isOdd = self.itemID % 2 == 0
			if self.completedTask():
				self.LoadImage("{}".format(IMAGES[1][0] if isOdd else IMAGES[1][0]))
				self.Objects["Slot"].LoadImage("assets/ui/passive_system/slot2.tga")
				self.Objects["TextLine"].SetPackedFontColor(0xFF64ad3c)
				self.Objects["TextLine_Data"].SetPackedFontColor(0xFF64ad3c)
				self.Objects["Button"].Disable()
			else:
				self.Objects["Slot"].LoadImage("assets/ui/passive_system/slot.tga")
				self.LoadImage("{}".format(IMAGES[0][0] if isOdd else IMAGES[0][1]))
				self.Objects["TextLine"].SetPackedFontColor(0xFFc7c7c7)
				self.Objects["TextLine_Data"].SetPackedFontColor(0xFFc7c7c7)

			self.Objects["TextLine_Data"].SetText("{}/{}".format(self.getData()[0], self.getData()[1]))


		def __GiveRequiredItem(self):
			net.SendChatPacket("/legendary_stones_passive_up {}".format(self.itemID))

	def __init__(self):
		super(LegendaryStonesPassiveWindow, self).__init__()
		self.__Initialize()

		self.__InitializeWindow()

	def __del__(self):
		return super(LegendaryStonesPassiveWindow, self).__del__()

	def __Initialize(self):
		self.AddFlag("animate")
		self.information = {
			"main" : { "sub_board" : None, "peek_window" : None, "scroll_board" : None,\
				"scrollBar" : None, "window_objects" : [] }
		}

	def __InitializeWindow(self):
		self.SetWindowName("LegendaryStonesPassiveWindow")
		self.SetSize(*self.WINDOW_SIZE)
		for flag in ["movable", "float"]:
			self.AddFlag(flag)
		self.SetTitleName(uiScriptLocale.LEGENDARY_STONES_SYSTEM_PASSIVE_WINDOW_TITLE)
		self.SetCloseEvent(ui.__mem_func__(self.Close))
		self.SetCenterPosition()

		sManager = self.information["main"]

		sManager["sub_board"] = ui.MainSubBoard()
		sManager["sub_board"].SetParent(self)
		sManager["sub_board"].AddFlag("attach")
		sManager["sub_board"].SetPosition(7, 30)
		sManager["sub_board"].SetSize(self.PEEK_WINDOW_SIZE[0] + 2, self.PEEK_WINDOW_SIZE[1] + 6)
		sManager["sub_board"].Show()

		sManager["peek_window"] = ui.Window()
		sManager["peek_window"].SetParent(self)
		sManager["peek_window"].SetInsideRender(True)
		sManager["peek_window"].AddFlag("attach")
		sManager["peek_window"].SetPosition(10, 33)
		sManager["peek_window"].SetSize(*self.PEEK_WINDOW_SIZE)
		sManager["peek_window"].Show()

		sManager["scroll_board"] = ui.Window()
		sManager["scroll_board"].SetParent(sManager["peek_window"])
		sManager["scroll_board"].AddFlag("attach")
		sManager["scroll_board"].SetPosition(0, 0)
		sManager["scroll_board"].Show()

		self.__RegisterScrollBar()

	def __RegisterScrollBar(self):
		if app.ENABLE_MOUSE_WHEEL_EVENT:
			self.SetScrollWheelEvent(self.OnMouseWheel)

		sManage = self.information["main"]
		sManage["scrollBar"] = util.ReworkedScrollBar()
		sManage["scrollBar"].SetParent(self)
		sManage["scrollBar"].SetPosition(sManage["peek_window"].GetLocalPosition()[0] + sManage["peek_window"].GetWidth(), sManage["peek_window"].GetLocalPosition()[1])
		sManage["scrollBar"].SetSize(7, sManage["peek_window"].GetHeight())
		sManage["scrollBar"].SetScrollEvent(self.__OnScroll)
		sManage["scrollBar"].SetScrollSpeed(self.SCROLL_SPEED)

		self.__ChangeScrollbar()

	def OnMouseWheel(self, length):
		sManage = self.information["main"]
		if sManage["scrollBar"] and sManage["scrollBar"].IsShow():
			return sManage["scrollBar"].OnRunMouseWheelEvent(length)

		return False

	def __ChangeScrollbar(self):
		sManage = self.information["main"]
		if not sManage["scrollBar"]:
			return

		if sManage["scroll_board"].GetHeight() <= sManage["peek_window"].GetHeight():
			sManage["scrollBar"].Hide()
		else:
			sManage["scrollBar"].SetScale(sManage["peek_window"].GetHeight(), sManage["scroll_board"].GetHeight())
			sManage["scrollBar"].SetPosScale((float(1) * abs(sManage["scroll_board"].GetLocalPosition()[1])) / (sManage["scroll_board"].GetHeight() - sManage["peek_window"].GetHeight()))
			sManage["scrollBar"].Show()
	
	def __OnScroll(self, fScale):
		sManage = self.information["main"]
		if not sManage["scroll_board"] or\
			(sManage["scrollBar"] and sManage["scrollBar"].GetBlockMoveState() is True):
			return

		curr = min(0, max(math.ceil((sManage["scroll_board"].GetHeight() - sManage["peek_window"].GetHeight()) * fScale * -1.0), -sManage["scroll_board"].GetHeight() + sManage["peek_window"].GetHeight()))
		sManage["scroll_board"].SetPosition(0, curr)
	
	def __ReloadScrollBoard(self):
		sManage = self.information["main"]
		for button in sManage["window_objects"]:
			mxSize = button.GetLocalPosition()[1] + button.GetHeight()
			if mxSize > sManage["scroll_board"].GetHeight():
				sManage["scroll_board"].SetSize(sManage["peek_window"].GetWidth(), mxSize)

	def Clear(self):
		constInfo.LEGENDARY_PASSIVE_INFO = {}

	def RegisterData(self, args):
		(iterator, iVnum, iGived, iRequired) = (int(args[0]), int(args[1]), int(args[2]), int(args[3]))

		constInfo.LEGENDARY_PASSIVE_INFO[int(iterator)] = (iVnum, iGived, iRequired)

		sManager = self.information["main"]

		if len(sManager["window_objects"]) <= iterator:
			tmp = self.WindowObject()
			tmp.SetParent(sManager["scroll_board"])
			tmp.SetPosition(0, (iterator * (tmp.GetHeight() + self.PADDING_BETWEEN)))
			tmp.AppendData(iVnum, iGived, iRequired)
			tmp.Show()

			sManager["window_objects"].append(tmp)
		else:
			sManager["window_objects"][iterator].AppendData(iVnum, iGived, iRequired, True)

		self.__ReloadScrollBoard()
		self.__ChangeScrollbar()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Show(self):
		super(LegendaryStonesPassiveWindow, self).Show()
	
	def Close(self):
		super(LegendaryStonesPassiveWindow, self).Hide()

class LegendaryStonesCraftingMinerals(ui.ScriptWindow):
	""" Static values """
	CRAFTING_GRID_SIZE = (6, 2)
	CRAFTING_CONFIGURATION = {
		0 : {
			"reward_" : 1,
		},

		1 : {
			"reward_" : 1,
		},

		2 : {
			"reward_" : 2,
		},

		3 : {
			"reward_" : 3,
		},

		4 : {
			"reward_" : 4,
		},
	}

	CONFIGURATION = dict()

	def __init__(self):
		super(LegendaryStonesCraftingMinerals, self).__init__()
		self.__Initialize()

		self.__Reset()

	def __del__(self):
		return super(LegendaryStonesCraftingMinerals, self).__del__()

	def __Initialize(self):
		if not self.LoadScript(self, "uiscript/legendary_stones_crafting_minerals.py"):
			return

		getObj = self.GetChild

		self.MAIN = {
			"BOARD" : getObj("BOARD"),
			"SLOTS" : getObj("ITEMS"),
			"REWARD" : getObj("REWARD_ITEM"),
			"COST" : getObj("COST"),
			"CRAFT" : getObj("CRAFT"),
			"INFO" : getObj("BOX_INFO"),
		}

		self.items = itemWrapper.ItemContainer()
		self.items.SetOnSetItem(self.OnSetItem)

		self.MAIN["SLOTS"].SetSelectEmptySlotEvent(self.OnSelectEmptySlot)
		self.MAIN["SLOTS"].SetSelectItemSlotEvent(self.OnSelectItemSlot)
		self.MAIN["SLOTS"].SetOverInItemEvent(self.OnOverInItem)
		self.MAIN["SLOTS"].SetOverOutItemEvent(self.OnOverOutItem)
		
		self.MAIN["COST"].SetText(localeInfo.NumberToStringAsType(0, True))
		
		self.MAIN["CRAFT"].SetEvent(self.OnAccept)
		self.MAIN["BOARD"].SetCloseEvent(self.Close)

		self.MAIN["REWARD"].SetOverInItemEvent(self.OnOverInItemReward)
		self.MAIN["REWARD"].SetOverOutItemEvent(self.OnOverOutItem)

		for i in xrange(len(self.CRAFTING_CONFIGURATION)):
			yPos = 5 + (i * 14)

			Line = ui.MakeTextLineNew(self.MAIN["INFO"], 0, yPos, "{} |cFFb9e7bc+{}|r |Eemoticons/crafting/arrow|e {}x |cFFb5a676{}|r".format(uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_MINERALS_WINDOW_SOUL_TEXT, i, self.CRAFTING_CONFIGURATION[i]["reward_"], uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_MINERALS_WINDOW_MINERALS_TEXT))
			Line.SetHorizontalAlignCenter()
			Line.SetWindowHorizontalAlignCenter()

			self.Children.append(Line)

		self.SetCenterPosition()

	def __Reset(self):
		self.items.Clear()

	def RegisterData(self, Args):
		if (len(Args) < 4):
			return

		(bPos, wSlot, iCountPer, iPricePer) = (int(Args[0]), int(Args[1]), int(Args[2]), int(Args[3]))

		newItem = itemWrapper.ItemToolTipWrapper(player.INVENTORY, wSlot)

		if wSlot == -1:
			newItem = None

			if self.CONFIGURATION.get(bPos):
				self.CONFIGURATION.pop(bPos)
		else:
			if not bPos in self.CONFIGURATION:
				self.CONFIGURATION[bPos] = {"SLOT" : wSlot, "COUNT" : iCountPer, "PRICE" : iPricePer}

		if interfaceModule.GetInstance() and interfaceModule.GetInstance().wndInventory:
			interfaceModule.GetInstance().wndInventory.RemoveLockSlot("MINERALS", self.items.GetPosition(bPos))
			interfaceModule.GetInstance().wndInventory.RefreshWindows()

		self.items.SetItem(bPos, newItem)

	def PutItem(self, slotIndex):
		iVnum = player.GetItemIndex(player.INVENTORY, slotIndex)
		item.SelectItem(iVnum)

		## Checking the type of item!
		if item.GetItemType() != item.ITEM_TYPE_METIN:
			return False

		## Checking its same item!
		for iPos, cItem in self.items:
			if cItem.GetPosition() == slotIndex:
				return False

		for slot in xrange(self.CRAFTING_GRID_SIZE[0] * self.CRAFTING_GRID_SIZE[1]):
			if not self.items.GetVnum(slot):
				## Right now we gonna put the item
				net.SendChatPacket("/legendary_stones_craft_set {} {} {}".format(0, slot, slotIndex))
				return True

		return False

	def GetItem(self, slotIndex):
		return self.items.GetItem(slotIndex)

	def RefreshItems(self):
		iTotalCount = 0
		iTotalMoney = 0
		for slot in xrange(self.CRAFTING_GRID_SIZE[0] * self.CRAFTING_GRID_SIZE[1]):
			self.MAIN["SLOTS"].ClearSlot(slot)
			self.MAIN["SLOTS"].SetItemSlot(slot, self.items.GetVnum(slot), self.items.GetCount(slot))
			
			if self.items.GetVnum(slot):
				item.SelectItem(self.items.GetVnum(slot))

				gPlus = int(item.GetItemName().split("+")[1])

				if gPlus in self.CRAFTING_CONFIGURATION:
					if self.CONFIGURATION.get(slot):
						iTotalCount += self.CONFIGURATION[slot].get("COUNT", 0) * self.items.GetCount(slot)
						iTotalMoney += self.CONFIGURATION[slot].get("PRICE", 0) * self.items.GetCount(slot)

		self.MAIN["SLOTS"].RefreshSlot()

		self.MAIN["REWARD"].ClearSlot(0)
		if iTotalCount:
			self.MAIN["REWARD"].SetItemSlot(0, self.CONFIGURATION.get("REWARD"), iTotalCount)
			self.MAIN["REWARD"].UnlockSlot(0)
		else:
			self.MAIN["REWARD"].SetItemSlot(0, self.CONFIGURATION.get("REWARD"))
			self.MAIN["REWARD"].LockSlot(0)
		
		self.MAIN["REWARD"].RefreshSlot()

		self.MAIN["COST"].SetText(localeInfo.NumberToStringAsType(iTotalMoney, True))

	def OnSelectEmptySlot(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			slotType = mouseModule.mouseController.GetAttachedType()
			position = mouseModule.mouseController.GetAttachedSlotNumber()

			if not util.IsInventorySlotType(slotType):
				return

			windowType = mouseModule.SlotTypeToWindowType(slotType)
			newItem = itemWrapper.ItemToolTipWrapper(windowType, position)

			vnum = newItem.GetVnum()

			item.SelectItem(vnum)
			if item.GetItemType() != item.ITEM_TYPE_METIN:
				return

			## Checking its same item!
			for iPos, cItem in self.items:
				if cItem.GetPosition() == position:
					return False

			mouseModule.mouseController.DeattachObject()

			net.SendChatPacket("/legendary_stones_craft_set {} {} {}".format(0, slotIndex, position))
			# self.SetItem(slotIndex, newItem)

	def OnSelectItemSlot(self, slotIndex):
		# self.SetItem(slotIndex, None)
		net.SendChatPacket("/legendary_stones_craft_set {} {} {}".format(0, slotIndex, -1))

	def OnOverInItem(self, slotIndex):
		playerItem = self.GetItem(slotIndex)
		if not playerItem:
			return

		playerItem.ShowToolTip()

	def OnOverOutItem(self):
		uiToolTip.GetItemToolTipInstance().HideToolTip()
	
	def OnOverInItemReward(self, slot):
		if not uiToolTip.GetItemToolTipInstance():
			return

		uiToolTip.GetItemToolTipInstance().ClearToolTip()

		uiToolTip.GetItemToolTipInstance().AddItemData(self.CONFIGURATION["REWARD"], metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])

	def OnSetItem(self, slotIndex):
		self.RefreshItems()

		if interfaceModule.GetInstance() and interfaceModule.GetInstance().wndInventory:
			interfaceModule.GetInstance().wndInventory.AppendLockSlot("MINERALS", self.items.GetPosition(slotIndex))
			interfaceModule.GetInstance().wndInventory.RefreshWindows()

	def OnAccept(self):
		for slotIndex, i in self.items:
			net.SendChatPacket("/legendary_stones_craft_run {} {}".format(0, i.GetPosition()))
		
		self.__Reset()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Open(self):
		super(LegendaryStonesCraftingMinerals, self).Show()
		if interfaceModule.GetInstance() and interfaceModule.GetInstance().wndInventory:
			interfaceModule.GetInstance().wndInventory.EraseLockElement("MINERALS")
			interfaceModule.GetInstance().wndInventory.RegisterLockColour("MINERALS", (0.6, 0.9, 1.0, 0.3))

			interfaceModule.GetInstance().wndInventory.EraseLockElement("MINERALS_LOCKED")
			interfaceModule.GetInstance().wndInventory.RegisterLockColour("MINERALS_LOCKED", (0.3, 0.3, 0.6, 0.3))

			## Gathering total size!
			iSize = player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT
			if app.ENABLE_SPECIAL_STORAGE:
				iSize += item.SPECIAL_STORAGE_PAGE_SIZE*item.SPECIAL_STORAGE_PAGE_COUNT*item.SPECIAL_STORAGE_COUNT

			for i in xrange(iSize):
				itemVnum = player.GetItemIndex(i)
				if itemVnum == 0:
					continue

				item.SelectItem(itemVnum)

				if item.GetItemType() != item.ITEM_TYPE_METIN:
					interfaceModule.GetInstance().wndInventory.AppendLockSlot("MINERALS_LOCKED", i)

			interfaceModule.GetInstance().wndInventory.RefreshWindows()

	def Close(self):
		if interfaceModule.GetInstance() and interfaceModule.GetInstance().wndInventory:
			interfaceModule.GetInstance().wndInventory.EraseLockElement("MINERALS")

		self.__Reset()

		super(LegendaryStonesCraftingMinerals, self).Hide()

	def UpdateWindow(self, iValue):
		if self.IsShow():
			self.Close()
		else:
			self.CONFIGURATION["REWARD"] = iValue
			self.MAIN["REWARD"].SetItemSlot(0, self.CONFIGURATION.get("REWARD"))
			self.MAIN["REWARD"].LockSlot(0)
			self.Open()

class LegendaryStonesCraftingShards(ui.ScriptWindow):
	""" Static values """
	CRAFTING_GRID_SIZE = (6, 2)
	CONFIGURATION = dict()

	def __init__(self):
		super(LegendaryStonesCraftingShards, self).__init__()
		self.__Initialize()

		self.__Reset()

	def __del__(self):
		return super(LegendaryStonesCraftingShards, self).__del__()

	def __Initialize(self):
		if not self.LoadScript(self, "uiscript/legendary_stones_crafting_shards.py"):
			return

		getObj = self.GetChild

		self.MAIN = {
			"BOARD" : getObj("BOARD"),
			"SLOTS" : getObj("ITEMS"),
			"REWARD" : getObj("REWARD_ITEM"),
			"COST" : getObj("COST"),
			"CRAFT" : getObj("CRAFT"),
		}

		self.items = itemWrapper.ItemContainer()
		self.items.SetOnSetItem(self.OnSetItem)

		self.MAIN["SLOTS"].SetSelectEmptySlotEvent(self.OnSelectEmptySlot)
		self.MAIN["SLOTS"].SetSelectItemSlotEvent(self.OnSelectItemSlot)
		self.MAIN["SLOTS"].SetOverInItemEvent(self.OnOverInItem)
		self.MAIN["SLOTS"].SetOverOutItemEvent(self.OnOverOutItem)
		
		self.MAIN["COST"].SetText(localeInfo.NumberToStringAsType(0, True))
		
		self.MAIN["CRAFT"].SetEvent(self.OnAccept)
		self.MAIN["BOARD"].SetCloseEvent(self.Close)

		self.MAIN["REWARD"].SetOverInItemEvent(self.OnOverInItemReward)
		self.MAIN["REWARD"].SetOverOutItemEvent(self.OnOverOutItem)

		self.SetCenterPosition()

	def __Reset(self):
		self.items.Clear()

	def RegisterData(self, Args):
		if (len(Args) < 4):
			return

		(bPos, wSlot, iCountPer, iPricePer) = (int(Args[0]), int(Args[1]), int(Args[2]), int(Args[3]))

		newItem = itemWrapper.ItemToolTipWrapper(player.INVENTORY, wSlot)

		if wSlot == -1:
			newItem = None

			if self.CONFIGURATION.get(bPos):
				self.CONFIGURATION.pop(bPos)
		else:
			if not bPos in self.CONFIGURATION:
				self.CONFIGURATION[bPos] = {"SLOT" : wSlot, "COUNT" : iCountPer, "PRICE" : iPricePer}

		self.items.SetItem(bPos, newItem)

	def PutItem(self, slotIndex):
		iVnum = player.GetItemIndex(player.INVENTORY, slotIndex)
		item.SelectItem(iVnum)

		## Checking the type of item!
		if item.GetItemType() != item.ITEM_TYPE_METIN:
			return False

		## Checking its same item!
		for iPos, cItem in self.items:
			if cItem.GetPosition() == slotIndex:
				return False

		for slot in xrange(self.CRAFTING_GRID_SIZE[0] * self.CRAFTING_GRID_SIZE[1]):
			if not self.items.GetVnum(slot):
				## Right now we gonna put the item
				net.SendChatPacket("/legendary_stones_craft_set {} {} {}".format(1, slot, slotIndex))
				return True

		return False

	def GetItem(self, slotIndex):
		return self.items.GetItem(slotIndex)

	def RefreshItems(self):
		iTotalCount = 0
		iTotalMoney = 0
		for slot in xrange(self.CRAFTING_GRID_SIZE[0] * self.CRAFTING_GRID_SIZE[1]):
			self.MAIN["SLOTS"].ClearSlot(slot)
			self.MAIN["SLOTS"].SetItemSlot(slot, self.items.GetVnum(slot), self.items.GetCount(slot))
			
			if self.items.GetVnum(slot):
				if self.CONFIGURATION.get(slot):
					iTotalCount += self.CONFIGURATION[slot].get("COUNT", 0) * self.items.GetCount(slot)
					iTotalMoney += self.CONFIGURATION[slot].get("PRICE", 0) * self.items.GetCount(slot)

		self.MAIN["SLOTS"].RefreshSlot()

		self.MAIN["REWARD"].ClearSlot(0)
		if iTotalCount:
			self.MAIN["REWARD"].SetItemSlot(0, self.CONFIGURATION.get("REWARD"), iTotalCount)
			self.MAIN["REWARD"].UnlockSlot(0)
		else:
			self.MAIN["REWARD"].SetItemSlot(0, self.CONFIGURATION.get("REWARD"))
			self.MAIN["REWARD"].LockSlot(0)
		
		self.MAIN["REWARD"].RefreshSlot()

		self.MAIN["COST"].SetText(localeInfo.NumberToStringAsType(iTotalMoney, True))

	def OnSelectEmptySlot(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			slotType = mouseModule.mouseController.GetAttachedType()
			position = mouseModule.mouseController.GetAttachedSlotNumber()

			if not util.IsInventorySlotType(slotType):
				return

			windowType = mouseModule.SlotTypeToWindowType(slotType)
			newItem = itemWrapper.ItemToolTipWrapper(windowType, position)

			vnum = newItem.GetVnum()

			item.SelectItem(vnum)
			if item.GetItemType() != item.ITEM_TYPE_METIN:
				return

			## Checking its same item!
			for iPos, cItem in self.items:
				if cItem.GetPosition() == position:
					return False

			mouseModule.mouseController.DeattachObject()

			net.SendChatPacket("/legendary_stones_craft_set {} {} {}".format(1, slotIndex, position))
			# self.SetItem(slotIndex, newItem)

	def OnSelectItemSlot(self, slotIndex):
		# self.SetItem(slotIndex, None)
		net.SendChatPacket("/legendary_stones_craft_set {} {} {}".format(1, slotIndex, -1))

	def OnOverInItem(self, slotIndex):
		playerItem = self.GetItem(slotIndex)
		if not playerItem:
			return

		playerItem.ShowToolTip()

	def OnOverOutItem(self):
		uiToolTip.GetItemToolTipInstance().HideToolTip()

	def OnOverInItemReward(self, slot):
		if not uiToolTip.GetItemToolTipInstance():
			return

		uiToolTip.GetItemToolTipInstance().ClearToolTip()

		uiToolTip.GetItemToolTipInstance().AddItemData(self.CONFIGURATION["REWARD"], metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])

	def OnSetItem(self, slotIndex):
		self.RefreshItems()

	def OnAccept(self):
		for slotIndex, i in self.items:
			net.SendChatPacket("/legendary_stones_craft_run {} {}".format(1, i.GetPosition()))

		self.__Reset()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Open(self):
		super(LegendaryStonesCraftingShards, self).Show()
	
	def Close(self):
		super(LegendaryStonesCraftingShards, self).Hide()

	def UpdateWindow(self, iValue):
		if self.IsShow():
			self.Close()
		else:
			self.CONFIGURATION["REWARD"] = iValue
			self.MAIN["REWARD"].SetItemSlot(0, self.CONFIGURATION.get("REWARD"))
			self.MAIN["REWARD"].LockSlot(0)
			self.Open()

class LegendaryStonesCraftingStones(ui.ScriptWindow):
	""" Static values """
	CRAFTING_GRID_SIZE = (5, 2)
	STONE_EXCHANGE_ADDER = 100
	STONE_EXCHANGE_PERCENT_PER = 10

	CONFIGURATION = dict()

	def __init__(self):
		super(LegendaryStonesCraftingStones, self).__init__()
		self.__Initialize()

		self.__Reset()
		self.counter = (app.GetTime(), 0)

	def __del__(self):
		self.counter = (app.GetTime(), 0)
		return super(LegendaryStonesCraftingStones, self).__del__()

	def __Initialize(self):
		if not self.LoadScript(self, "uiscript/legendary_stones_crafting_stones.py"):
			return

		getObj = self.GetChild

		self.MAIN = {
			"BOARD" : getObj("BOARD"),
			"ADD_ITEMS" : getObj("ADDITIONAL_ITEMS"),
			"SLOTS" : getObj("ITEMS"),
			"PERCENT" : getObj("REWARD_PERCENT"),
			"REWARD" : getObj("REWARD_ITEM"),
			"CRAFT" : getObj("CRAFT"),
		}

		self.items = itemWrapper.ItemContainer()
		self.items.SetOnSetItem(self.OnSetItem)

		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.HideToolTip()

		self.MAIN["ADD_ITEMS"].SetOverInItemEvent(self.OnOverInAdditional)
		self.MAIN["ADD_ITEMS"].SetOverOutItemEvent(self.OnOverOutItem)

		self.MAIN["SLOTS"].SetSelectEmptySlotEvent(self.OnSelectEmptySlot)
		self.MAIN["SLOTS"].SetSelectItemSlotEvent(self.OnSelectItemSlot)
		self.MAIN["SLOTS"].SetOverInItemEvent(self.OnOverInItem)
		self.MAIN["SLOTS"].SetOverOutItemEvent(self.OnOverOutItem)

		self.MAIN["CRAFT"].SetEvent(self.OnAccept)
		self.MAIN["BOARD"].SetCloseEvent(self.Close)

		self.MAIN["REWARD"].SetOverInItemEvent(self.OnOverInReward)
		self.MAIN["REWARD"].SetOverOutItemEvent(self.OnOverOutReward)

		self.SetCenterPosition()

	def __Reset(self):
		self.items.Clear()

	def GetItem(self, slotIndex):
		return self.items.GetItem(slotIndex)

	def OnSelectEmptySlot(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			slotType = mouseModule.mouseController.GetAttachedType()
			position = mouseModule.mouseController.GetAttachedSlotNumber()

			if not util.IsInventorySlotType(slotType):
				return

			windowType = mouseModule.SlotTypeToWindowType(slotType)
			newItem = itemWrapper.ItemToolTipWrapper(windowType, position)

			vnum = newItem.GetVnum()

			item.SelectItem(vnum)
			if item.GetItemType() != item.ITEM_TYPE_METIN:
				return

			mouseModule.mouseController.DeattachObject()

			net.SendChatPacket("/legendary_stones_exchange_set {} {}".format(slotIndex, position))

	def OnSelectItemSlot(self, slotIndex):
		net.SendChatPacket("/legendary_stones_exchange_set {} {}".format(slotIndex, -1))

	def getSortedItems(self):
		counts = {}
		for slotIndex, item in self.items:
			counts[item.GetVnum()] = counts.get(item.GetVnum(), 0) + 1
		
		return counts

	def Clear(self):
		self.__Reset()
		self.MAIN["REWARD"].ClearSlot(0)
		self.MAIN["REWARD"].RefreshSlot()

	def RegisterData(self, Args):
		if (len(Args) < 2):
			return

		(bPos, wSlot) = (int(Args[0]), int(Args[1]))

		newItem = itemWrapper.ItemToolTipWrapper(player.INVENTORY, wSlot)

		if wSlot == -1:
			newItem = None

		self.items.SetItem(bPos, newItem)

	def PutItem(self, slotIndex):
		iVnum = player.GetItemIndex(player.INVENTORY, slotIndex)
		item.SelectItem(iVnum)

		## Checking the type of item!
		if item.GetItemType() != item.ITEM_TYPE_METIN:
			return False

		## Checking its same item!
		for iPos, cItem in self.items:
			if cItem.GetPosition() == slotIndex:
				return False

		for slot in xrange(self.CRAFTING_GRID_SIZE[0] * self.CRAFTING_GRID_SIZE[1]):
			if not self.items.GetVnum(slot):
				## Right now we gonna put the item
				net.SendChatPacket("/legendary_stones_exchange_set {} {}".format(slot, slotIndex))
				return True

		return False

	def SetConfiguration(self, Args):
		if (len(Args) < 2):
			return

		if not "ADDITIONAL" in self.CONFIGURATION:
			self.CONFIGURATION["ADDITIONAL"] = []

		self.CONFIGURATION["ADDITIONAL"].append({
			"iVnum" : int(Args[0]),
			"iCount" : int(Args[1])
		})

	def OnOverInItem(self, slotIndex):
		playerItem = self.GetItem(slotIndex)
		if not playerItem:
			return

		playerItem.ShowToolTip()

	def OnOverOutItem(self):
		uiToolTip.GetItemToolTipInstance().HideToolTip()

	def OnOverInAdditional(self, slot):
		if not uiToolTip.GetItemToolTipInstance():
			return

		uiToolTip.GetItemToolTipInstance().ClearToolTip()

		uiToolTip.GetItemToolTipInstance().AddItemData(self.CONFIGURATION["ADDITIONAL"][slot].get("iVnum", 0), metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])

	def OnOverInReward(self, slot):
		if not self.toolTip:
			return

		self.toolTip.ClearToolTip()

		self.toolTip.AppendTextLine("{} |Eemoticons/crafting/arrow|e".format(uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_STONES_WINDOW_CHANCE_HEADER), 0xFFcfccbb)

		items = self.getSortedItems()
		for k, v in items.iteritems():
			item.SelectItem(k + self.STONE_EXCHANGE_ADDER)
			self.toolTip.AutoAppendTextLine("|cFF89b88d{}|r |Eemoticons/crafting/arrow|e ".format(item.GetItemName()) + CFF.format("{}%".format(v * self.STONE_EXCHANGE_PERCENT_PER), "#ffd169"))

		self.toolTip.ResizeToolTip()
		self.toolTip.ShowToolTip()

	def OnOverOutReward(self):
		if not self.toolTip:
			return

		self.toolTip.HideToolTip()

	def AppendCraftPercent(self):
		self.MAIN["PERCENT"].SetText(uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_STONES_WINDOW_CHANCE + " " + CFF.format("{}%".format(self.CONFIGURATION.get("CHANCE", 0)), "#ffd169"))

	def AppendAdditionalItems(self):
		bCraftDisable = False

		for iKey in xrange(len(self.CONFIGURATION.get("ADDITIONAL"))):
			self.MAIN["ADD_ITEMS"].ClearSlot(iKey)
			self.MAIN["ADD_ITEMS"].SetItemSlot(iKey, self.CONFIGURATION["ADDITIONAL"][iKey].get("iVnum", 0), self.CONFIGURATION["ADDITIONAL"][iKey].get("iCount", 1))
			self.MAIN["ADD_ITEMS"].LockSlot(iKey)
			self.MAIN["ADD_ITEMS"].RefreshSlot()

			if (player.GetItemCountByVnum(self.CONFIGURATION["ADDITIONAL"][iKey].get("iVnum", 0)) < self.CONFIGURATION["ADDITIONAL"][iKey].get("iCount") or player.GetItemCountByVnum(self.CONFIGURATION["ADDITIONAL"][iKey].get("iVnum", 0)) == 0):
				bCraftDisable = True
				self.MAIN["ADD_ITEMS"].LockSlot(iKey)
			else:
				self.MAIN["ADD_ITEMS"].UnlockSlot(iKey)

		if bCraftDisable:
			self.MAIN["CRAFT"].Disable()
		else:
			self.MAIN["CRAFT"].Enable()

	def OnSetItem(self, slotIndex):
		for slot in xrange(self.CRAFTING_GRID_SIZE[0] * self.CRAFTING_GRID_SIZE[1]):
			self.MAIN["SLOTS"].ClearSlot(slot)

			self.MAIN["SLOTS"].SetItemSlot(slot, self.items.GetVnum(slot), 1)
			self.MAIN["SLOTS"].RefreshSlot()

	def OnAccept(self):
		net.SendChatPacket("/legendary_stones_exchange_run")

	def OnUpdate(self):
		if self.items.GetItemCount() > 0:
			if app.GetTime() >= self.counter[0]:
				sortedItems = self.getSortedItems()

				if len(sortedItems) == 0:
					return

				if self.counter[1] == len(sortedItems):
					self.counter = (self.counter[0], len(sortedItems) - 1)

				self.MAIN["REWARD"].ClearSlot(0)
				iVnum = list(sortedItems.items()[self.counter[1]])[0]
				if iVnum > 0:
					iVnum += self.STONE_EXCHANGE_ADDER
				self.MAIN["REWARD"].SetItemSlot(0, iVnum)
				self.MAIN["REWARD"].RefreshSlot()

				val = self.counter[1] + 1 if self.counter[1] + 1 != len(sortedItems) else 0
				self.counter = (app.GetTime() + 0.5, min(val, len(sortedItems)))
		else:
			self.MAIN["REWARD"].ClearSlot(0)
			self.MAIN["REWARD"].RefreshSlot()

	def Open(self):
		self.AppendCraftPercent()
		self.AppendAdditionalItems()
		net.SendChatPacket("/legendary_stones_exchange_start")
		super(LegendaryStonesCraftingStones, self).Show()
	
	def Close(self):
		net.SendChatPacket("/legendary_stones_exchange_cancel")
		self.Clear()
		super(LegendaryStonesCraftingStones, self).Hide()

	def OnPressEscapeKey(self):
		self.Clear()
		self.Close()
		return True

	def UpdateWindow(self, iValue):
		if self.IsShow():
			self.Close()
		else:
			self.CONFIGURATION["CHANCE"] = iValue
			self.Open()

class LegendaryStonesRefine(ui.ScriptWindow):
	""" Static values """
	CRAFTING_GRID_SIZE = (1, 3)
	CONFIGURATION = dict()

	def __init__(self):
		super(LegendaryStonesRefine, self).__init__()
		self.__Initialize()

		self.__Reset()

	def __del__(self):
		return super(LegendaryStonesRefine, self).__del__()

	def __Initialize(self):
		if not self.LoadScript(self, "uiscript/legendary_stones_refine.py"):
			return

		getObj = self.GetChild

		self.MAIN = {
			"BOARD" : getObj("BOARD"),
			"SLOTS" : getObj("ITEMS"),
			"ADDITIONAL" : getObj("ADDITIONAL_ITEM"),
			"COST" : getObj("COST"),
			"CRAFT" : getObj("CRAFT"),
			"CANCEL" : getObj("CANCEL"),
		}

		self.items = itemWrapper.ItemContainer()
		self.items.SetOnSetItem(self.OnSetItem)

		# self.MAIN["SLOTS"].SetCoverButton(self.CRAFTING_GRID_SIZE[1] - 1, "assets/ui/passive_system/refine/slot_reward.png", "assets/ui/passive_system/refine/slot_reward.png", "assets/ui/passive_system/refine/slot_reward.png")
		# self.MAIN["SLOTS"].SetAlwaysRenderCoverButton(self.CRAFTING_GRID_SIZE[1] - 1)

		self.MAIN["SLOTS"].SetSelectEmptySlotEvent(self.OnSelectEmptySlot)
		self.MAIN["SLOTS"].SetSelectItemSlotEvent(self.OnSelectItemSlot)
		self.MAIN["SLOTS"].SetOverInItemEvent(self.OnOverInItem)
		self.MAIN["SLOTS"].SetOverOutItemEvent(self.OnOverOutItem)

		self.MAIN["ADDITIONAL"].SetOverInItemEvent(self.OnOverInAdditional)
		self.MAIN["ADDITIONAL"].SetOverOutItemEvent(self.OnOverOutItem)

		self.MAIN["COST"].SetText(localeInfo.NumberToStringAsType(0, True))
		
		self.MAIN["CRAFT"].SetEvent(self.OnAccept)
		self.MAIN["CANCEL"].SetEvent(self.Close)
		self.MAIN["BOARD"].SetCloseEvent(self.Close)

		self.SetCenterPosition()

	def __Reset(self):
		self.items.Clear()

	def RegisterData(self, Args):
		if (len(Args) < 2):
			return

		(bPos, wSlot) = (int(Args[0]), int(Args[1]))

		newItem = itemWrapper.ItemToolTipWrapper(player.INVENTORY, wSlot)

		if wSlot == -1:
			newItem = None

		self.items.SetItem(bPos, newItem)
		if bPos == 0:
			self.items.SetItem(self.CRAFTING_GRID_SIZE[1] - 1, newItem)

	def PutItem(self, slotIndex):
		iVnum = player.GetItemIndex(player.INVENTORY, slotIndex)
		item.SelectItem(iVnum)

		## Checking the type of item!
		if item.GetItemType() != item.ITEM_TYPE_METIN:
			return False

		## Checking its same item!
		for iPos, cItem in self.items:
			if cItem.GetPosition() == slotIndex:
				return False

			if cItem.GetVnum() != iVnum:
				return False

		for slot in xrange(self.CRAFTING_GRID_SIZE[0] * self.CRAFTING_GRID_SIZE[1]):
			if not self.items.GetVnum(slot):
				## Right now we gonna put the item
				net.SendChatPacket("/legendary_stones_refine_set {} {}".format(slot, slotIndex))
				return True

		return False

	def SetConfiguration(self, Args):
		if (len(Args) < 2):
			return

		self.CONFIGURATION["ADDITIONAL"] = {"iVnum" : int(Args[0]), "iCount" : int(Args[1])}

	def Clear(self):
		self.__Reset()
		if (player.GetItemCountByVnum(self.CONFIGURATION.get("ADDITIONAL")["iVnum"]) == 0):
			self.MAIN["ADDITIONAL"].LockSlot(0)
		else:
			self.MAIN["ADDITIONAL"].UnlockSlot(0)

	def GetItem(self, slotIndex):
		return self.items.GetItem(slotIndex)

	def RefreshItems(self):
		for slot in xrange(self.CRAFTING_GRID_SIZE[0] * self.CRAFTING_GRID_SIZE[1]):
			self.MAIN["SLOTS"].ClearSlot(slot)
			self.MAIN["SLOTS"].SetItemSlot(slot, self.items.GetVnum(slot), self.items.GetCount(slot))

		self.MAIN["SLOTS"].RefreshSlot()

	def OnSelectEmptySlot(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			slotType = mouseModule.mouseController.GetAttachedType()
			position = mouseModule.mouseController.GetAttachedSlotNumber()

			if not util.IsInventorySlotType(slotType):
				return

			windowType = mouseModule.SlotTypeToWindowType(slotType)
			newItem = itemWrapper.ItemToolTipWrapper(windowType, position)

			vnum = newItem.GetVnum()

			item.SelectItem(vnum)
			if item.GetItemType() != item.ITEM_TYPE_METIN:
				return

			for pos, i in self.items:
				if i.GetVnum() != vnum:
					return

			mouseModule.mouseController.DeattachObject()

			net.SendChatPacket("/legendary_stones_refine_set {} {}".format(slotIndex, position))

	def OnSelectItemSlot(self, slotIndex):
		net.SendChatPacket("/legendary_stones_refine_set {} {}".format(slotIndex, -1))

	def OnOverInItem(self, slotIndex):
		playerItem = self.GetItem(slotIndex)
		if not playerItem:
			return

		playerItem.ShowToolTip(slotIndex == self.CRAFTING_GRID_SIZE[1] - 1)

	def OnOverOutItem(self):
		uiToolTip.GetItemToolTipInstance().HideToolTip()

	def OnOverInAdditional(self, slotIndex):
		if not uiToolTip.GetItemToolTipInstance():
			return

		uiToolTip.GetItemToolTipInstance().ClearToolTip()

		uiToolTip.GetItemToolTipInstance().AddItemData(self.CONFIGURATION["ADDITIONAL"]["iVnum"], metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])

	def OnSetItem(self, slotIndex):
		self.RefreshItems()

	def OnAccept(self):
		net.SendChatPacket("/legendary_stones_refine_run")

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Open(self):
		self.MAIN["COST"].SetText(localeInfo.NumberToStringAsType(int(self.CONFIGURATION.get("PRICE", 0)), True))
		self.MAIN["ADDITIONAL"].SetItemSlot(0, self.CONFIGURATION.get("ADDITIONAL")["iVnum"], self.CONFIGURATION.get("ADDITIONAL")["iCount"])

		if (player.GetItemCountByVnum(self.CONFIGURATION.get("ADDITIONAL")["iVnum"]) == 0):
			self.MAIN["ADDITIONAL"].LockSlot(0)
		else:
			self.MAIN["ADDITIONAL"].UnlockSlot(0)

		super(LegendaryStonesRefine, self).Show()

	def Close(self):
		self.Clear()
		net.SendChatPacket("/legendary_stones_refine_cancel")
		super(LegendaryStonesRefine, self).Hide()

	def UpdateWindow(self, iValue):
		if self.IsShow():
			self.Close()
		else:
			self.CONFIGURATION["PRICE"] = iValue
			self.Open()