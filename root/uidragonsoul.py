from introinterface import gcGetEnable
import ui
import player
import mouseModule
import net
import app
import snd
import item
import chat
import grp
import uiScriptLocale
import uiRefine
import uiAttachMetin
import uiCommon
import uiPrivateShopBuilder
import localeInfo
import constInfo
import ime
import uiInventory
import sys
from _weakref import proxy

import interfaceModule
import uiToolTip
import wndMgr

if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
	import cfg
	
ITEM_FLAG_APPLICABLE = 1 << 14

if gcGetEnable("SAVE_WND_POSITION_DRAGON_SOUL"):
	import cfg

class DragonSoulWindow(ui.ScriptWindow):
	KIND_TAP_TITLES = [uiScriptLocale.DRAGONSOUL_TAP_TITLE_1, uiScriptLocale.DRAGONSOUL_TAP_TITLE_2,
			uiScriptLocale.DRAGONSOUL_TAP_TITLE_3, uiScriptLocale.DRAGONSOUL_TAP_TITLE_4, uiScriptLocale.DRAGONSOUL_TAP_TITLE_5, uiScriptLocale.DRAGONSOUL_TAP_TITLE_6]
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.questionDialog = None
		self.tooltipItem = None
		self.sellingSlotNumber = -1
		self.isLoaded = 0
		self.isActivated = False
		self.isSetted = False
		self.DSKindIndex = 0
		self.tabDict = None
		self.tabButtonDict = None
		if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
			self.deckPageIndex = int(cfg.Get(cfg.SAVE_GENERAL, "DS_ACTIVATE_PAGE", "0"))
		else:
			self.deckPageIndex = 0
		self.inventoryPageIndex = 0
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.wndPrivateShop			= None
			self.wndPrivateShopSearch	= None
		self.SetWindowName("DragonSoulWindow")
		self.interface = None

		if app.ENABLE_DS_SET:
			self.iSetType = -1
			self.dsIgnoreCallback = False

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		if gcGetEnable("SAVE_WND_POSITION_DRAGON_SOUL"):
			if int(cfg.Get(cfg.SAVE_OPTION, "save_wnd_pos", "0")):
				x, y = map(int, cfg.Get(cfg.SAVE_GENERAL, "wnd_pos_ds", "0 0").split(" "))
				if x and y:
					self.SetPosition(x, y)
			else:
				self.SetCenterPosition()

		if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
			isStandardPage = int(cfg.Get(cfg.SAVE_GENERAL, "DS_ACTIVATE_PAGE", "0"))

			if self.deckPageIndex == isStandardPage:
				self.standardPage.SetChecked(True)

		ui.ScriptWindow.Show(self)

	if gcGetEnable("SAVE_WND_POSITION_DRAGON_SOUL"):
		def OnMoveWindow(self, x, y):
			cfg.Set(cfg.SAVE_GENERAL, "wnd_pos_ds", ("%d %d") % (x, y))

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "dragonsoulwindow.py")


		except:
			import exception
			exception.Abort("dragonsoulwindow.LoadWindow.LoadObject")
		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")
			self.activateButton = self.GetChild("activate")
			self.deckTab = []
			self.deckTab.append(self.GetChild("deck1"))
			self.deckTab.append(self.GetChild("deck2"))
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.inventoryTab = []
			self.inventoryTab.append(self.GetChild("Inventory_Tab_01"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_02"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_03"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_04"))
			self.inventoryTab.append(self.GetChild("Inventory_Tab_05"))
			self.TabControl = self.GetChild("TabControl")
			self.InventoryControl  = self.GetChild("InventoryControl")
			self.DSRefine_Button  = self.GetChild("DSRefine_Button")
			self.tabDict = {
				0	: self.GetChild("Tab_01"),
				1	: self.GetChild("Tab_02"),
				2	: self.GetChild("Tab_03"),
				3	: self.GetChild("Tab_04"),
				4	: self.GetChild("Tab_05"),
				5	: self.GetChild("Tab_06"),
			}
			self.tabButtonDict = {
				0	: self.GetChild("Tab_Button_01"),
				1	: self.GetChild("Tab_Button_02"),
				2	: self.GetChild("Tab_Button_03"),
				3	: self.GetChild("Tab_Button_04"),
				4	: self.GetChild("Tab_Button_05"),
				5	: self.GetChild("Tab_Button_06"),
			}
			self.tabText = self.GetChild("tab_text_area")

			if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
				self.standardPage = self.GetChild("standardPage")

		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")
		## DragonSoul Kind Tap
		for (tabKey, tabButton) in self.tabButtonDict.items():
			tabButton.SetEvent(ui.__mem_func__(self.SetDSKindIndex), tabKey)
		## Item
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptyEquipSlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectEquipItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseEquipItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseEquipItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInEquipItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutEquipItem))

		## Deck
		self.deckTab[0].SetToggleDownEvent(lambda arg=0: self.SetDeckPage(arg))
		self.deckTab[1].SetToggleDownEvent(lambda arg=1: self.SetDeckPage(arg))
		self.deckTab[0].SetToggleUpEvent(lambda arg=0: self.__DeckButtonDown(arg))
		self.deckTab[1].SetToggleUpEvent(lambda arg=1: self.__DeckButtonDown(arg))
		# self.deckTab[0].Down()

		## Grade button
		self.inventoryTab[0].SetEvent(lambda arg=0: self.SetInventoryPage(arg))
		self.inventoryTab[1].SetEvent(lambda arg=1: self.SetInventoryPage(arg))
		self.inventoryTab[2].SetEvent(lambda arg=2: self.SetInventoryPage(arg))
		self.inventoryTab[3].SetEvent(lambda arg=3: self.SetInventoryPage(arg))
		self.inventoryTab[4].SetEvent(lambda arg=4: self.SetInventoryPage(arg))
		self.inventoryTab[0].Down()
		## Etc
		self.wndItem = wndItem
		self.wndEquip = wndEquip

		self.dlgQuestion = uiCommon.QuestionDialog2()
		self.dlgQuestion.Close()

		self.activateButton.SetToggleDownEvent(ui.__mem_func__(self.ActivateButtonClick))
		self.activateButton.SetToggleUpEvent(ui.__mem_func__(self.ActivateButtonClick))
		self.wndPopupDialog = uiCommon.PopupDialog()

		##
		self.listHighlightedSlot = []

		self.DSRefine_Button.SAFE_SetEvent(self.__OpenRefineWindow)

		## Refresh
		self.SetInventoryPage(0)
		self.RefreshItemSlot()
		self.RefreshEquipSlotWindow()
		self.RefreshBagSlotWindow()
		self.SetDSKindIndex(0)
		self.activateButton.Enable()
		self.deckTab[self.deckPageIndex].Down()
		self.activateButton.SetUp()

		if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
			self.standardPage.SetEvent(self.__selectStandardPage)
			self.standardPage.Disable()

		if app.ENABLE_MOUSE_WHEEL_EVENT:
			self.SetScrollWheelEvent(self.OnWheelMove)

	if app.ENABLE_MOUSE_WHEEL_EVENT:
		def OnWheelMove(self, len):
			pos = 0
			if len > 0:
				if self.TabControl.IsInPosition():
					pos = (self.DSKindIndex + 1) % 6

					if pos == 0:
						return True

					self.SetDSKindIndex(pos)
				elif self.wndItem.IsInPosition() or self.InventoryControl.IsInPosition():
					pos = (self.inventoryPageIndex + 1) % 5

					if pos == 0:
						return True

					self.SetInventoryPage(pos)
				else:
					pos = (self.deckPageIndex -1) % 2

					if pos == 0:
						return True

					self.SetDeckPage(pos)

			else:
				if self.TabControl.IsInPosition():
					pos = (self.DSKindIndex - 1) % 6
					if pos < 0:
						pos = -pos

					if pos == 6 - 1:
						return True

					self.SetDSKindIndex(pos)
				elif self.wndItem.IsInPosition() or self.InventoryControl.IsInPosition():
					pos = (self.inventoryPageIndex -1) % 5
					if pos < 0:
						pos = -pos

					if pos == 5 - 1:
						return True

					self.SetInventoryPage(pos)
				else:
					pos = (self.deckPageIndex -1) % 2
					if pos < 0:
						pos = -pos

					if pos == 2 - 1:
						return True

					self.SetDeckPage(pos)
			return True

	def BindInterfaceClass(self, interface):
		self.interface = proxy(interface)

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.activateButton = 0
		self.questionDialog = None
		self.mallButton = None
		self.inventoryTab = []
		self.deckTab = []
		self.equipmentTab = []
		self.tabDict = None
		self.tabButtonDict = None
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.wndPrivateShop			= None
			self.wndPrivateShopSearch	= None
		self.interface = None

	def Close(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()
		self.Hide()

	def __DeckButtonDown(self, deck):
		self.deckTab[deck].Down()

	def SetInventoryPage(self, page):
		if self.inventoryPageIndex != page:
			self.__HighlightSlot_ClearCurrentPage()
		self.inventoryPageIndex = page
		self.inventoryTab[(page+1)%5].SetUp()
		self.inventoryTab[(page+2)%5].SetUp()
		self.inventoryTab[(page+3)%5].SetUp()
		self.inventoryTab[(page+4)%5].SetUp()
		self.inventoryTab[self.inventoryPageIndex].Down()
		self.RefreshBagSlotWindow()

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

	def RefreshEquipSlotWindow(self):
		if self.isActivated:
			self.ActivateEquipSlotWindow(self.deckPageIndex)

		for i in xrange(6):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
			itemVnum = player.GetItemIndex(slotNumber)

			self.wndEquip.SetItemSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i, itemVnum, 0)
			self.wndEquip.EnableSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)

			if itemVnum != 0:
				item.SelectItem(itemVnum)
				for j in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(j)

					remain_time = 999
					if item.LIMIT_REAL_TIME == limitType:
						remain_time = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 0) - app.GetGlobalTimeStamp()
					elif item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
						remain_time = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 0) - app.GetGlobalTimeStamp()
					elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						remain_time = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 0)

					if remain_time <= 0:
						self.wndEquip.DisableSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)
						break

		self.wndEquip.RefreshSlot()

	def ActivateEquipSlotWindow(self, deck):
		for i in xrange(6):
			if deck == 2:
				plusCount = 6
			else:
				plusCount = 0
			# slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i + plusCount)
			# if player.GetItemIndex(slotNumber) != 0:
			# 	self.wndEquip.ActivateSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i + plusCount)

			if i == 0:
				self.wndEquip.ActivateSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i + plusCount, (234.0 / 255.0, 234.0 / 255.0, 234.0 / 255.0, 1.0))

			elif i == 1:
				self.wndEquip.ActivateSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i + plusCount,
													(228.0 / 255.0, 27.0 / 255.0, 49.0 / 255.0, 1.0))
			elif i == 2:
				self.wndEquip.ActivateSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i + plusCount,
													(86.0 / 255.0, 180.0 / 255.0, 47.0 / 255.0, 1.0))
			elif i == 3:
				self.wndEquip.ActivateSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i + plusCount,
													(0.0 / 255.0, 160.0 / 255.0, 228.0 / 255.0, 1.0))
			elif i == 4:
				self.wndEquip.ActivateSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i + plusCount,
													(223.0 / 255.0, 143.0 / 255.0, 40.0 / 255.0, 1.0))
			elif i == 5:
				self.wndEquip.ActivateSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i + plusCount,
													(153.0 / 255.0, 153.0 / 255.0, 153.0 / 255.0, 1.0))

	def DeactivateEquipSlotWindow(self):
		for i in xrange(12):
			self.wndEquip.DeactivateSlot(player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i)

	def RefreshStatus(self):
		self.RefreshItemSlot()

	def __InventoryLocalSlotPosToGlobalSlotPos(self, window_type, local_slot_pos, bActivePage = False):
		if player.INVENTORY == window_type:
			return (int(cfg.Get(cfg.SAVE_GENERAL, "DS_ACTIVATE_PAGE", "0")) if bActivePage else self.deckPageIndex) * player.DRAGON_SOUL_EQUIPMENT_FIRST_SIZE + local_slot_pos

		return (self.DSKindIndex * 5 * player.DRAGON_SOUL_PAGE_SIZE) + self.inventoryPageIndex * player.DRAGON_SOUL_PAGE_SIZE + local_slot_pos

	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVnum=self.wndItem.SetItemSlot
		for i in xrange(player.DRAGON_SOUL_PAGE_SIZE):
			self.wndItem.EnableSlot(i)
			#<- dragon soul kind
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, i)

			itemCount = getItemCount(player.DRAGON_SOUL_INVENTORY, slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0
			itemVnum = getItemVNum(player.DRAGON_SOUL_INVENTORY, slotNumber)

			setItemVnum(i, itemVnum, itemCount)

			if itemVnum != 0:
				item.SelectItem(itemVnum)
				for j in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(j)

					remain_time = 999
					if item.LIMIT_REAL_TIME == limitType:
						remain_time = player.GetItemMetinSocket(player.DRAGON_SOUL_INVENTORY, slotNumber, 0)
					elif item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
						remain_time = player.GetItemMetinSocket(player.DRAGON_SOUL_INVENTORY, slotNumber, 0)
					elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						remain_time = player.GetItemMetinSocket(player.DRAGON_SOUL_INVENTORY, slotNumber, 0)

					if remain_time <= 0:
						self.wndItem.DisableSlot(i)
						break

		self.__HighlightSlot_RefreshCurrentPage()
		self.wndItem.RefreshSlot()
		
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.wndPrivateShop:
				self.wndPrivateShop.RefreshLockedSlot()

	def ShowToolTip(self, window_type, slotIndex):
		if None != self.tooltipItem:
			if player.INVENTORY == window_type:
				self.tooltipItem.SetInventoryItem(slotIndex)
			else:
				self.tooltipItem.SetInventoryItem(slotIndex, player.DRAGON_SOUL_INVENTORY)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()
			
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.wndPrivateShop:
				self.wndPrivateShop.RefreshLockedSlot()

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OverInItem(self, overSlotPos):
		self.wndItem.NewDeactivateSlot(overSlotPos)
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, overSlotPos)
		try:
			self.listHighlightedSlot.remove(overSlotPos)
		except:
			pass

		self.wndItem.SetUsableItem(False)
		self.ShowToolTip(player.DRAGON_SOUL_INVENTORY, overSlotPos)

	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, slotIndex)
		if 0 == player.GetItemMetinSocket(player.DRAGON_SOUL_INVENTORY, slotIndex, 0):
			self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_EXPIRED)
			self.wndPopupDialog.SetAutoClose()
			self.wndPopupDialog.Open()
			return

		self.__EquipItem(slotIndex)

	def __EquipItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, slotIndex)
		item.SelectItem(ItemVNum)
		subType = item.GetItemSubType()
		equipSlotPos = player.DRAGON_SOUL_EQUIPMENT_SLOT_START + self.deckPageIndex * player.DRAGON_SOUL_EQUIPMENT_FIRST_SIZE + subType
		srcItemPos = (player.DRAGON_SOUL_INVENTORY, slotIndex)
		dstItemPos = (player.INVENTORY, equipSlotPos)
		self.__OpenQuestionDialog(True, srcItemPos, dstItemPos)

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, itemSlotIndex)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			#@fixme011 BEGIN (changed behavior)
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					srcItemPos = (attachedInvenType, attachedSlotPos)
					dstItemPos = (player.DRAGON_SOUL_INVENTORY, itemSlotIndex)
					self.__OpenQuestionDialog(False, srcItemPos, dstItemPos)
				else:
					ITEM_USE = 3
					ITEM_EXTRACT = 31
					item.SelectItem(attachedItemVID)
					if item.GetItemType(attachedItemVID) == ITEM_EXTRACT or\
						item.GetItemType(attachedItemVID) == ITEM_USE and\
						item.GetItemSubType(attachedItemVID) in (item.USE_TIME_CHARGE_PER, item.USE_TIME_CHARGE_FIX):
						net.SendItemUseToItemPacket(attachedInvenType, attachedSlotPos, player.DRAGON_SOUL_INVENTORY, itemSlotIndex)

			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedInvenType:
				net.SendItemUseToItemPacket(attachedInvenType, attachedSlotPos, player.DRAGON_SOUL_INVENTORY, itemSlotIndex)
			#@fixme011 END

			mouseModule.mouseController.DeattachObject()


		else:
			curCursorNum = app.GetCursor()

			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)
			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(player.DRAGON_SOUL_INVENTORY, itemSlotIndex)
				ime.PasteString(link)
			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)
				
				if app.ENABLE_PREMIUM_PRIVATE_SHOP:
					if self.wndPrivateShop and self.wndPrivateShop.IsShow():
						self.wndPrivateShop.AttachItemToPrivateShop(itemSlotIndex, player.SLOT_TYPE_DRAGON_SOUL_INVENTORY)
						return
						
					if self.wndPrivateShopSearch and self.wndPrivateShopSearch.IsShow():
						self.wndPrivateShopSearch.SelectItem(itemIndex)
						return
			else:
				selectedItemVNum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, itemSlotIndex)
				itemCount = player.GetItemCount(player.DRAGON_SOUL_INVENTORY, itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_DRAGON_SOUL_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
				self.wndItem.SetUseMode(False)
				snd.PlaySound("sound/ui/pick.wav")

	def __SellItem(self, itemSlotPos):
		if not player.IsDSEquipmentSlot(player.DRAGON_SOUL_INVENTORY, itemSlotPos):
			self.sellingSlotNumber = itemSlotPos
			itemIndex = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, itemSlotPos)
			itemCount = player.GetItemCount(player.DRAGON_SOUL_INVENTORY, itemSlotPos)

			item.SelectItem(itemIndex)

			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.SetAutoClose()
				popup.Open()
				self.popup = popup
				return

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = itemCount / itemPrice / 5
			else:
				itemPrice = itemPrice * itemCount / 5

			item.GetItemName(itemIndex)
			itemName = item.GetItemName()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.count = itemCount

	def SellItem(self):
		net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.DRAGON_SOUL_INVENTORY)
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if self.questionDialog:
			self.questionDialog.Close()

		self.questionDialog = None

	def __OnClosePopupDialog(self):
		self.pop = None

	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, selectedSlotPos)
		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			if player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				if app.ENABLE_PREMIUM_PRIVATE_SHOP:
					if not uiPrivateShopBuilder.IsBuildingPrivateShop():
						self.wndPrivateShop.SendItemCheckoutPacket(attachedSlotPos, selectedSlotPos)
						mouseModule.mouseController.DeattachObject()
						return
						
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:
				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, player.DRAGON_SOUL_INVENTORY, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, player.DRAGON_SOUL_INVENTORY, selectedSlotPos)

			#@fixme011 BEGIN (changed behavior)
			elif player.SLOT_TYPE_INVENTORY == attachedSlotType:
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					srcItemPos = (attachedInvenType, attachedSlotPos)
					dstItemPos = (player.DRAGON_SOUL_INVENTORY, selectedSlotPos)
					self.__OpenQuestionDialog(False, srcItemPos, dstItemPos)

			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
				itemCount = player.GetItemCount(attachedInvenType, attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()

				self.__SendMoveItemPacket(attachedInvenType, attachedSlotPos, player.DRAGON_SOUL_INVENTORY, selectedSlotPos, attachedCount)
			#@fixme011 END

			mouseModule.mouseController.DeattachObject()

	def UseItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, slotIndex)
		try:
			if self.wndDragonSoulRefine.IsShow():
				if uiPrivateShopBuilder.IsBuildingPrivateShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
					return
				self.wndDragonSoulRefine.AutoSetItem((player.DRAGON_SOUL_INVENTORY, slotIndex), 1)
				return
		except:
			pass

		self.__UseItem(slotIndex)

		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	def __SendMoveItemPacket(self, srcSlotWindow, srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemMovePacket(srcSlotWindow , srcSlotPos, dstSlotWindow, dstSlotPos, srcItemCount)

	def OverOutEquipItem(self):
		self.OverOutItem()

	def OverInEquipItem(self, overSlotPos):
		overSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, overSlotPos)
		self.wndItem.SetUsableItem(False)
		self.ShowToolTip(player.INVENTORY, overSlotPos)

	def UseEquipItemSlot(self, slotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, slotIndex)

		self.__UseEquipItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutEquipItem()

	def __UseEquipItem(self, slotIndex):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_ITEM_FAILURE_PRIVATE_SHOP)
			return

		self.__OpenQuestionDialog(False, (player.INVENTORY, slotIndex), (1, 1))


	def SelectEquipItemSlot(self, itemSlotIndex):

		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return
		elif app.BUY == curCursorNum:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
			return


		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, itemSlotIndex)

		if app.IsPressed(app.DIK_LALT):
			link = player.GetItemLink(player.INVENTORY, itemSlotIndex)
			ime.PasteString(link)
			return

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_INVENTORY == attachedSlotType and itemSlotIndex == attachedSlotPos:
				mouseModule.mouseController.DeattachObject() #@fixme011
				return

			#@fixme011 BEGIN (enable only the extract items so far)
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()
			attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				ITEM_USE = 3
				ITEM_EXTRACT = 31
				item.SelectItem(attachedItemVID)
				if item.GetItemType(attachedItemVID) == ITEM_EXTRACT or\
					item.GetItemType(attachedItemVID) == ITEM_USE and\
					item.GetItemSubType(attachedItemVID) in (item.USE_TIME_CHARGE_PER, item.USE_TIME_CHARGE_FIX):
					net.SendItemUseToItemPacket(attachedInvenType, attachedSlotPos, player.INVENTORY, itemSlotIndex)
			#@fixme011 END

			mouseModule.mouseController.DeattachObject()
		else:
			selectedItemVNum = player.GetItemIndex(player.INVENTORY, itemSlotIndex)
			itemCount = player.GetItemCount(player.INVENTORY, itemSlotIndex)
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)
			self.wndItem.SetUseMode(False)
			snd.PlaySound("sound/ui/pick.wav")

	def SelectEmptyEquipSlot(self, selectedSlot):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, selectedSlot)

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
				if 0 == player.GetItemMetinSocket(player.DRAGON_SOUL_INVENTORY, attachedSlotPos, 0):
					self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_EXPIRED)
					self.wndPopupDialog.SetAutoClose()
					self.wndPopupDialog.Open()
					return

				item.SelectItem(attachedItemIndex)
				subType = item.GetItemSubType()
				if subType != (selectedSlot - player.DRAGON_SOUL_EQUIPMENT_SLOT_START):
					self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNMATCHED_SLOT)
					self.wndPopupDialog.SetAutoClose()
					self.wndPopupDialog.Open()
				else:
					srcItemPos = (player.DRAGON_SOUL_INVENTORY, attachedSlotPos)
					dstItemPos = (player.INVENTORY, selectedSlotPos)
					self.__OpenQuestionDialog(True, srcItemPos, dstItemPos)

			mouseModule.mouseController.DeattachObject()

	def __OpenQuestionDialog(self, Equip, srcItemPos, dstItemPos):
		self.srcItemPos = srcItemPos
		self.dstItemPos = dstItemPos

		self.dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.__Accept))
		self.dlgQuestion.SetCancelEvent(ui.__mem_func__(self.__Cancel))

		if Equip:
			self.dlgQuestion.SetText1(localeInfo.DRAGON_SOUL_EQUIP_WARNING1)
			self.dlgQuestion.SetText2(localeInfo.DRAGON_SOUL_EQUIP_WARNING2)
		else:
			self.dlgQuestion.SetText1(localeInfo.DRAGON_SOUL_UNEQUIP_WARNING1)
			self.dlgQuestion.SetText2(localeInfo.DRAGON_SOUL_UNEQUIP_WARNING2)

		self.dlgQuestion.Open()

	def __Accept(self):
		if (-1, -1) == self.dstItemPos:
			net.SendItemUsePacket(*self.srcItemPos)
		else:
			self.__SendMoveItemPacket(*(self.srcItemPos + self.dstItemPos + (0,)))
		self.dlgQuestion.Close()

	def __Cancel(self):
		self.srcItemPos = (0, 0)
		self.dstItemPos = (0, 0)
		self.dlgQuestion.Close()


	def SetDSKindIndex(self, kindIndex):
		if self.DSKindIndex != kindIndex:
			self.__HighlightSlot_ClearCurrentPage()

		self.DSKindIndex = kindIndex

		for (tabKey, tabButton) in self.tabButtonDict.items():
			if kindIndex!=tabKey:
				tabButton.SetUp()

		for tabValue in self.tabDict.itervalues():
			tabValue.Hide()

		self.tabDict[kindIndex].Show()
		self.tabText.SetText(DragonSoulWindow.KIND_TAP_TITLES[kindIndex])

		self.RefreshBagSlotWindow()


	if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
		def __selectStandardPage(self):
			isStandardPage = int(cfg.Get(cfg.SAVE_GENERAL, "DS_ACTIVATE_PAGE", "0"))

			if isStandardPage != self.deckPageIndex:
				cfg.Set(cfg.SAVE_GENERAL, "DS_ACTIVATE_PAGE", self.deckPageIndex)

				self.standardPage.SetChecked(True)
				self.standardPage.Disable()

	def SetDeckPage(self, page):
		if page == self.deckPageIndex:
			return

		if self.isActivated:
			self.DeactivateDragonSoul()
			net.SendChatPacket("/dragon_soul deactivate")
		self.deckPageIndex = page
		self.deckTab[page].Down()
		self.deckTab[(page+1)%2].SetUp()

		if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
			isStandardPage = int(cfg.Get(cfg.SAVE_GENERAL, "DS_ACTIVATE_PAGE", "0"))

			if self.deckPageIndex == isStandardPage:
				self.standardPage.SetChecked(True)
				self.standardPage.Disable()
			else:
				self.standardPage.SetChecked(False)
				self.standardPage.Enable()

		self.RefreshEquipSlotWindow()

	if app.ENABLE_DS_SET:
		def ActivateSet(self, iSetType):
			self.iSetType = iSetType

		def DeactivateSet(self):
			self.iSetType = -1

		def GetSetType(self):
			if not self.isActivated:
				return -1
			
			return self.iSetType

		def IsDSPageFull(self):
			import player
			return player.IsDSPageFull(self.deckPageIndex)

	def ActivateDragonSoulByExtern(self, deck):
		self.isActivated = True
		self.activateButton.Down()
		self.deckPageIndex = deck
		self.deckTab[deck].Down()
		self.deckTab[(deck+1)%2].SetUp()
		self.RefreshEquipSlotWindow()

		if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
			self.interface.wndInventory.actionDSButton(self.isActivated)

			isStandardPage = int(cfg.Get(cfg.SAVE_GENERAL, "DS_ACTIVATE_PAGE", "0"))

			if self.deckPageIndex == isStandardPage:
				self.standardPage.SetChecked(True)
				self.standardPage.Disable()
			else:
				self.standardPage.SetChecked(False)
				self.standardPage.Enable()

		self.ActivateEquipSlotWindow(deck)

	def DeactivateDragonSoul(self):
		self.isActivated = False
		self.activateButton.SetUp()

		if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
			self.interface.wndInventory.actionDSButton(self.isActivated)

		self.DeactivateEquipSlotWindow()

	def ActivateButtonClick(self):
		if player.GetStatus(player.LEVEL) < 30:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DS_QUALIFIED_LEVEL_TOO_LOW)
			return

		self.isActivated = self.isActivated ^ True
		if app.ENABLE_DS_SET:
			self.dsIgnoreCallback = True

		if self.isActivated:
			if self.__CanActivateDeck():
				if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
					net.SendChatPacket("/dragon_soul activate " + str(cfg.Get(cfg.SAVE_GENERAL, "DS_ACTIVATE_PAGE", "0")))
				else:
					net.SendChatPacket("/dragon_soul activate " + str(self.deckPageIndex))
			else:
				self.isActivated = False
				self.activateButton.SetUp()
		else:
			net.SendChatPacket("/dragon_soul deactivate")

	def ActivateButtonClickByKey(self):
		if player.GetStatus(player.LEVEL) < 30:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DS_QUALIFIED_LEVEL_TOO_LOW)
			return

		self.isActivated = self.isActivated ^ True
		if self.isActivated:
			if self.__CanActivateDeck():
				if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
					net.SendChatPacket("/dragon_soul activate " + str(cfg.Get(cfg.SAVE_GENERAL, "DS_ACTIVATE_PAGE", "0")))
				else:
					net.SendChatPacket("/dragon_soul activate " + str(self.deckPageIndex))
			else:
				self.isActivated = False
				self.activateButton.SetUp()
		else:
			net.SendChatPacket("/dragon_soul deactivate")

	def __CanActivateDeck(self):
		canActiveNum = 0
		for i in xrange(6):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.INVENTORY, player.DRAGON_SOUL_EQUIPMENT_SLOT_START + i, bActivePage = True)
			itemVnum = player.GetItemIndex(slotNumber)
			if itemVnum != 0:
				item.SelectItem(itemVnum)
				isNoLimit = True
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
						isNoLimit = False
						remain_time = player.GetItemMetinSocket(player.INVENTORY, slotNumber, 0)
						if 0 != remain_time:
							canActiveNum += 1
							break
				if isNoLimit:
					canActiveNum += 1

		return canActiveNum > 0


	def __HighlightSlot_ClearCurrentPage(self):
		for i in xrange(self.wndItem.GetSlotCount()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, i)
			self.wndItem.NewDeactivateSlot(i)
			if slotNumber in self.listHighlightedSlot:
				self.listHighlightedSlot.remove(slotNumber)

	def __HighlightSlot_RefreshCurrentPage(self):
		for i in xrange(self.wndItem.GetSlotCount()):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, i)
			if slotNumber in self.listHighlightedSlot:
				self.wndItem.NewActivateSlot(i)

	def HighlightSlot(self, slot):
		if not slot in self.listHighlightedSlot:
			self.listHighlightedSlot.append (slot)

	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			from _weakref import proxy
			self.wndDragonSoulRefine = proxy(wndDragonSoulRefine)

	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def BindPrivateShopClass(self, window):
			self.wndPrivateShop = window
			
		def BindPrivateShopSearchClass(self, window):
			self.wndPrivateShopSearch = window	

		def GetDSKindIndex(self):
			return self.DSKindIndex
		
		def GetInventoryPageIndex(self):
			return self.inventoryPageIndex

	def __OpenRefineWindow(self):
		if self.wndDragonSoulRefine.IsShow():
			self.wndDragonSoulRefine.Hide()
		else:
			self.wndDragonSoulRefine.Show()
			
class DragonSoulRefineWindow(ui.ScriptWindow):
	REFINE_TYPE_GRADE, REFINE_TYPE_STEP, REFINE_TYPE_STRENGTH = xrange(3)
	DS_SUB_HEADER_DIC = {
		REFINE_TYPE_GRADE : player.DS_SUB_HEADER_DO_UPGRADE,
		REFINE_TYPE_STEP : player.DS_SUB_HEADER_DO_IMPROVEMENT,
		REFINE_TYPE_STRENGTH : player.DS_SUB_HEADER_DO_REFINE
	}
	REFINE_STONE_SLOT, DRAGON_SOUL_SLOT = xrange(2)

	INVALID_DRAGON_SOUL_INFO = -1

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = None
		self.sellingSlotNumber = -1
		self.isLoaded = 0
		self.refineChoiceButtonDict = None
		self.doRefineButton = None
		self.wndMoney = None
		self.refineItemLoop = None
		self.refineLoopTime = 0

		if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
			self.wndPercent = None
			self.firstItem = -1
			self.secondItem = -1

		self.TitleToolTip = uiToolTip.ToolTip()
		self.TitleToolTip.ClearToolTip()

		self.SetWindowName("DragonSoulRefineWindow")
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()
		ui.ScriptWindow.Show(self)

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return
		self.isLoaded = 1
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, uiScriptLocale.LOCALE_UISCRIPT_PATH + "dragonsoulrefinewindow.py")

		except:
			import exception
			exception.Abort("dragonsoulrefinewindow.LoadWindow.LoadObject")
		try:
			wndRefineSlot = self.GetChild("RefineSlot")
			wndResultSlot = self.GetChild("ResultSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.GetChild("TitleBar").HandleButtonState("BTN_CHBOX", True)
			self.GetChild("TitleBar").HandleButtonGetter("BTN_CHBOX").SetOverEvent(ui.__mem_func__(self.__CreateToolTip))
			self.GetChild("TitleBar").HandleButtonGetter("BTN_CHBOX").SetOverOutEvent(ui.__mem_func__(self.__HideToolTip))

			self.refineChoiceButtonDict = {
				self.REFINE_TYPE_GRADE	: self.GetChild("GradeButton"),
				self.REFINE_TYPE_STEP: self.GetChild("StepButton"),
				self.REFINE_TYPE_STRENGTH	: self.GetChild("StrengthButton"),
			}
			self.doRefineButton = self.GetChild("DoRefineButton")
			self.wndMoney = self.GetChild("Money_Slot")
			if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
				self.wndPercent = self.GetChild("Percent_Slot")
			if app.ENABLE_DS_REFINE_ALL:
				self.doAllRefineButton = self.GetChild("DoAllRefineButton")

		except:
			import exception
			exception.Abort("DragonSoulRefineWindow.LoadWindow.BindObject")


		## Item Slots
		wndRefineSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInRefineItem))
		wndRefineSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		wndRefineSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.__SelectRefineEmptySlot))
		wndRefineSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.__SelectRefineItemSlot))
		wndRefineSlot.SetUseSlotEvent(ui.__mem_func__(self.__SelectRefineItemSlot))
		wndRefineSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.__SelectRefineItemSlot))

		wndResultSlot.SetOverInItemEvent(ui.__mem_func__(self.__OverInResultItem))
		wndResultSlot.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		self.wndRefineSlot = wndRefineSlot
		self.wndResultSlot = wndResultSlot

		## Button
		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].SetToggleDownEvent(self.__ToggleDownGradeButton)
		self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].SetToggleDownEvent(self.__ToggleDownStepButton)
		self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].SetToggleDownEvent(self.__ToggleDownStrengthButton)
		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].SetToggleUpEvent(lambda : self.__ToggleUpButton(self.REFINE_TYPE_GRADE))
		self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].SetToggleUpEvent(lambda : self.__ToggleUpButton(self.REFINE_TYPE_STEP))
		self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].SetToggleUpEvent(lambda : self.__ToggleUpButton(self.REFINE_TYPE_STRENGTH))
		self.doRefineButton.SetEvent(self.__PressDoRefineButton)

		if app.ENABLE_DS_REFINE_ALL:
			self.doAllRefineButton.SetEvent(self.__PressDoAllRefineButton)

		## Dialog
		self.wndPopupDialog = uiCommon.PopupDialog()

		self.currentRefineType = self.REFINE_TYPE_GRADE
		self.refineItemInfo = {}
		self.resultItemInfo = {}
		self.currentRecipe = {}

		self.wndMoney.SetText(localeInfo.NumberToStringAsType(0))

		if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
			self.wndPercent.SetText(localeInfo.DRAGONSOUL_REFINE_PERCENT + " |cFFf4be00{}%|r".format("0"))
		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].Down()

		self.__Initialize()

	def Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.wndItem = 0
		self.wndEquip = 0
		self.activateButton = 0
		self.questionDialog = None
		self.mallButton = None
		self.inventoryTab = []
		self.deckTab = []
		self.equipmentTab = []
		self.tabDict = None
		self.tabButtonDict = None

	def Close(self):
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.__FlushRefineItemSlot()
		player.SendDragonSoulRefine(player.DRAGON_SOUL_REFINE_CLOSE)
		self.Hide()

	def Show(self):
		self.currentRefineType = self.REFINE_TYPE_GRADE
		self.wndMoney.SetText(localeInfo.NumberToStringAsType(0))

		if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
			self.wndPercent.SetText(localeInfo.DRAGONSOUL_REFINE_PERCENT + " |cFFf4be00{}%|r".format("0"))
		self.refineChoiceButtonDict[self.REFINE_TYPE_GRADE].Down()
		self.refineChoiceButtonDict[self.REFINE_TYPE_STEP].SetUp()
		self.refineChoiceButtonDict[self.REFINE_TYPE_STRENGTH].SetUp()

		self.Refresh()

		ui.ScriptWindow.Show(self)

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def __Initialize(self):
		self.currentRecipe = {}
		self.refineItemInfo = {}
		self.resultItemInfo = {}

		if self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			self.refineSlotLockStartIndex = 2
		else:
			self.refineSlotLockStartIndex = 1

		for i in xrange(self.refineSlotLockStartIndex):
			self.wndRefineSlot.HideSlotBaseImage(i)

		self.wndMoney.SetText(localeInfo.NumberToStringAsType(0))

		if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
			self.wndPercent.SetText(localeInfo.DRAGONSOUL_REFINE_PERCENT + " |cFFf4be00{}%|r".format("0"))

	def __FlushRefineItemSlot(self):
		## Item slot settings
		for invenType, invenPos, itemCount in self.refineItemInfo.values():
			remainCount = player.GetItemCount(invenType, invenPos)
			player.SetItemCount(invenType, invenPos, remainCount + itemCount)
		self.__Initialize()

	def __ToggleUpButton(self, idx):
		#if self.REFINE_TYPE_GRADE == self.currentRefineType:
		self.refineChoiceButtonDict[idx].Down()

	def __ToggleDownGradeButton(self):
		if self.REFINE_TYPE_GRADE == self.currentRefineType:
			return
		self.refineChoiceButtonDict[self.currentRefineType].SetUp()
		self.currentRefineType = self.REFINE_TYPE_GRADE
		self.__FlushRefineItemSlot()
		self.Refresh()

	def __ToggleDownStepButton(self):
		if self.REFINE_TYPE_STEP == self.currentRefineType:
			return
		self.refineChoiceButtonDict[self.currentRefineType].SetUp()
		self.currentRefineType = self.REFINE_TYPE_STEP
		self.__FlushRefineItemSlot()
		self.Refresh()

	def __ToggleDownStrengthButton(self):
		if self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			return
		self.refineChoiceButtonDict[self.currentRefineType].SetUp()
		self.currentRefineType = self.REFINE_TYPE_STRENGTH
		self.__FlushRefineItemSlot()
		self.Refresh()

	def __PopUp(self, message):
		self.wndPopupDialog.SetText(message)
		self.wndPopupDialog.SetAutoClose()
		self.wndPopupDialog.Open()

	def __SetItem(self, inven, dstSlotIndex, itemCount):
		invenType, invenPos = inven

		if dstSlotIndex >= self.refineSlotLockStartIndex:
			return False

		itemVnum = player.GetItemIndex(invenType, invenPos)
		maxCount = player.GetItemCount(invenType, invenPos)

		if itemCount > maxCount:
			raise Exception, ("Invalid attachedItemCount(%d). (base pos (%d, %d), base itemCount(%d))" % (itemCount, invenType, invenPos, maxCount))
			#return False

		if DragonSoulRefineWindow.REFINE_TYPE_STRENGTH == self.currentRefineType:
			if self.__IsDragonSoul(itemVnum):
				dstSlotIndex = 1
			else:
				dstSlotIndex = 0

		if dstSlotIndex in self.refineItemInfo:
			return False

		if False == self.__CheckCanRefine(itemVnum):
			return False

		player.SetItemCount(invenType, invenPos, maxCount - itemCount)
		self.refineItemInfo[dstSlotIndex] = (invenType, invenPos, itemCount)
		self.Refresh()

		return True

	def __CheckCanRefine(self, vnum):
		if self.REFINE_TYPE_GRADE == self.currentRefineType:
			return self.__CanRefineGrade(vnum)

		elif self.REFINE_TYPE_STEP == self.currentRefineType:
			return self.__CanRefineStep(vnum)

		elif self.REFINE_TYPE_STRENGTH == self.currentRefineType:
			return self.__CanRefineStrength(vnum)

		else:
			return False



	def __CanRefineGrade(self, vnum):
		ds_info = self.__GetDragonSoulTypeInfo(vnum)

		if DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO == ds_info:
			self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
			return False

		if self.currentRecipe:
			ds_type, grade, step, strength = ds_info
			cur_refine_ds_type, cur_refine_grade, cur_refine_step, cur_refine_strength = self.currentRecipe["ds_info"]
			if not (cur_refine_ds_type == ds_type and cur_refine_grade == grade):
				self.__PopUp(localeInfo.DRAGON_SOUL_INVALID_DRAGON_SOUL)
				return False
		else:
			self.currentRecipe = self.__GetRefineGradeRecipe(vnum)

			if self.currentRecipe:
				self.refineSlotLockStartIndex = self.currentRecipe["need_count"]
				self.wndMoney.SetText(localeInfo.NumberToStringAsType(self.currentRecipe["fee"]))
				if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
					self.wndPercent.SetText(localeInfo.DRAGONSOUL_REFINE_PERCENT + " |cFFf4be00{}%|r".format(self.currentRecipe["percent"]))
				return True
			else:
				self.__PopUp(localeInfo.DRAGON_SOUL_CANNOT_REFINE)
				return False

	def __CanRefineStep (self, vnum):
		ds_info = self.__GetDragonSoulTypeInfo(vnum)

		if DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO == ds_info:
			self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
			return False

		if self.currentRecipe:
			ds_type, grade, step, strength = ds_info
			cur_refine_ds_type, cur_refine_grade, cur_refine_step, cur_refine_strength = self.currentRecipe["ds_info"]
			if not (cur_refine_ds_type == ds_type and cur_refine_grade == grade and cur_refine_step == step):
				self.__PopUp(localeInfo.DRAGON_SOUL_INVALID_DRAGON_SOUL)
				return False
		else:
			self.currentRecipe = self.__GetRefineStepRecipe(vnum)

			if self.currentRecipe:
				self.refineSlotLockStartIndex = self.currentRecipe["need_count"]
				self.wndMoney.SetText(localeInfo.NumberToStringAsType(self.currentRecipe["fee"]))
				if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
					self.wndPercent.SetText(localeInfo.DRAGONSOUL_REFINE_PERCENT + " |cFFf4be00{}%|r".format(self.currentRecipe["percent"]))
				return True

			else:
				self.__PopUp(localeInfo.DRAGON_SOUL_CANNOT_REFINE)
				return False

	def __CanRefineStrength (self, vnum):
		if self.__IsDragonSoul(vnum):
			ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)

			import dragon_soul_refine_settings
			if strength >= dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["strength_max_table"][grade][step]:
				self.__PopUp(localeInfo.DRAGON_SOUL_CANNOT_REFINE_MORE)
				return False

			else:
				if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
					self.AppendStrengthPercent(strength = strength)
				return True
		else:
			if self.currentRecipe:
				self.__PopUp(localeInfo.DRAGON_SOUL_IS_NOT_DRAGON_SOUL)
				return False
			else:
				refineRecipe = self.__GetRefineStrengthInfo(vnum)

				if refineRecipe:
					self.secondItem = vnum
					self.currentRecipe = refineRecipe
					self.wndMoney.SetText(localeInfo.NumberToStringAsType(self.currentRecipe["fee"]))
					if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
						self.AppendStrengthPercent(vnum = vnum)
					return True
				else:
					self.__PopUp(localeInfo.DRAGON_SOUL_NOT_DRAGON_SOUL_REFINE_STONE)
					return False

	if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
		def AppendStrengthPercent(self, strength = -1, vnum = -1):
			if strength > -1:
				self.firstItem = strength

			if vnum > -1:
				self.secondItem = vnum

			if self.firstItem >= 0 and self.secondItem > 0:
				percent = self.__GetRefineStrengthPercent(self.firstItem, self.secondItem)

				self.wndPercent.SetText(localeInfo.DRAGONSOUL_REFINE_PERCENT + " |cFFf4be00{}%|r".format(percent))

	def __GetRefineGradeRecipe (self, vnum):
		ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)
		try:
			import dragon_soul_refine_settings

			return	{
				"ds_info"		: (ds_type, grade, step, strength),
				"need_count"	: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["grade_need_count"][grade],
				"fee"			: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["grade_fee"][grade],
				"percent"		: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["grade_percent"][grade]
			}
		except Exception as e:
			sys_err("ERROR#1: ", str(e))
			return None

	def __GetRefineStepRecipe (self, vnum):
		ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)
		try:
			import dragon_soul_refine_settings

			return	{
				"ds_info"		: (ds_type, grade, step, strength),
				"need_count"	: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["step_need_count"][step],
				"fee"			: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["step_fee"][step],
				"percent"		: dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["step_percent"][step]
			}
		except Exception as e:
			sys_err("ERROR#2: ", str(e))
			return None

	def __GetRefineStrengthInfo (self, itemVnum):
		try:
			item.SelectItem(itemVnum)
			if not (item.ITEM_TYPE_MATERIAL == item.GetItemType() \
					and (item.MATERIAL_DS_REFINE_NORMAL <= item.GetItemSubType() and item.GetItemSubType() <= item.MATERIAL_DS_REFINE_HOLLY)):
				return None

			import dragon_soul_refine_settings
			return { "fee" : dragon_soul_refine_settings.strength_fee[item.GetItemSubType()] }
		except:
			return None

	if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
		def __GetRefineStrengthPercent (self, strength, itemVnum):
			try:
				item.SelectItem(itemVnum)
				if not (item.ITEM_TYPE_MATERIAL == item.GetItemType() \
						and (item.MATERIAL_DS_REFINE_NORMAL <= item.GetItemSubType() and item.GetItemSubType() <= item.MATERIAL_DS_REFINE_HOLLY)):
					return None

				import dragon_soul_refine_settings

				return dragon_soul_refine_settings.STRENGTH_PERCENTS[item.GetItemSubType()][strength]
			except:
				return None

	def __IsDragonSoul(self, vnum):
		item.SelectItem(vnum)
		return item.GetItemType() == item.ITEM_TYPE_DS

	def __GetDragonSoulTypeInfo(self, vnum):
		if not self.__IsDragonSoul(vnum):
			return DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO
		ds_type = vnum / 10000
		grade = vnum % 10000 /1000
		step = vnum % 1000 / 100
		strength = vnum % 100 / 10

		return (ds_type, grade, step, strength)

	def __MakeDragonSoulVnum(self, ds_type, grade, step, strength):
		return ds_type * 10000 + grade * 1000 + step * 100 + strength * 10

	def __SelectRefineEmptySlot(self, selectedSlotPos):
		try:
			if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
				return

			if selectedSlotPos >= self.refineSlotLockStartIndex:
				return

			if mouseModule.mouseController.isAttached():
				attachedSlotType = mouseModule.mouseController.GetAttachedType()
				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
				attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
				mouseModule.mouseController.DeattachObject()

				if uiPrivateShopBuilder.IsBuildingPrivateShop():
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
					return

				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

				if player.INVENTORY == attachedInvenType and player.IsEquipmentSlot(attachedSlotPos):
					return

				if player.INVENTORY != attachedInvenType and player.DRAGON_SOUL_INVENTORY != attachedInvenType:
					return

				if True == self.__SetItem((attachedInvenType, attachedSlotPos), selectedSlotPos, attachedItemCount):
					self.Refresh()

		except Exception, e:
			import dbg
			dbg.TraceError("Exception : __SelectRefineEmptySlot, %s" % e)

	def __SelectRefineItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		try:
			if not selectedSlotPos in self.refineItemInfo:
				if mouseModule.mouseController.isAttached():
					attachedSlotType = mouseModule.mouseController.GetAttachedType()
					attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
					attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
					attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
					mouseModule.mouseController.DeattachObject()

					if uiPrivateShopBuilder.IsBuildingPrivateShop():
						chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.MOVE_ITEM_FAILURE_PRIVATE_SHOP)
						return

					attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)

					if player.INVENTORY == attachedInvenType and player.IsEquipmentSlot(attachedSlotPos):
						return

					if player.INVENTORY != attachedInvenType and player.DRAGON_SOUL_INVENTORY != attachedInvenType:
						return

					self.AutoSetItem((attachedInvenType, attachedSlotPos), 1)
				return
			elif mouseModule.mouseController.isAttached():
				return

			attachedInvenType, attachedSlotPos, attachedItemCount = self.refineItemInfo[selectedSlotPos]
			selectedItemVnum = player.GetItemIndex(attachedInvenType, attachedSlotPos)

			invenType, invenPos, itemCount = self.refineItemInfo[selectedSlotPos]
			remainCount = player.GetItemCount(invenType, invenPos)
			player.SetItemCount(invenType, invenPos, remainCount + itemCount)
			del self.refineItemInfo[selectedSlotPos]

			if not self.refineItemInfo:
				self.__Initialize()
			else:
				item.SelectItem(selectedItemVnum)
				if (item.ITEM_TYPE_MATERIAL == item.GetItemType() \
					and (item.MATERIAL_DS_REFINE_NORMAL <= item.GetItemSubType() and item.GetItemSubType() <= item.MATERIAL_DS_REFINE_HOLLY)):
					self.currentRecipe = {}
					self.wndMoney.SetText(localeInfo.NumberToStringAsType(0))

					if gcGetEnable("ENABLE_DS_REFINE_PERCENT"):
						self.wndPercent.SetText(localeInfo.DRAGONSOUL_REFINE_PERCENT + " |cFFf4be00{}%|r".format(0))
				else:
					pass

		except Exception, e:
			import dbg
			dbg.TraceError("Exception : __SelectRefineItemSlot, %s" % e)

		self.Refresh()

	def __OverInRefineItem(self, slotIndex):
		if self.refineItemInfo.has_key(slotIndex):
			inven_type, inven_pos, item_count = self.refineItemInfo[slotIndex]
			self.tooltipItem.SetInventoryItem(inven_pos, inven_type)

	def __OverInResultItem(self, slotIndex):
		if self.resultItemInfo.has_key(slotIndex):
			inven_type, inven_pos, item_count = self.resultItemInfo[slotIndex]
			self.tooltipItem.SetInventoryItem(inven_pos, inven_type)

	def __OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def __PressDoRefineButton(self):
		for i in xrange(self.refineSlotLockStartIndex):
			if not i in self.refineItemInfo:
				self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_NOT_ENOUGH_MATERIAL)
				self.wndPopupDialog.SetAutoClose()
				self.wndPopupDialog.Open()

				return

		player.SendDragonSoulRefine(DragonSoulRefineWindow.DS_SUB_HEADER_DIC[self.currentRefineType], self.refineItemInfo)

	if app.ENABLE_DS_REFINE_ALL:
		def CheckCanRefineSimple(self, vnum):
			if self.REFINE_TYPE_GRADE == self.currentRefineType:
				return self.CanRefineGradeSimple(vnum)

			elif self.REFINE_TYPE_STEP == self.currentRefineType:
				return self.CanRefineStepSimple(vnum)

			elif self.REFINE_TYPE_STRENGTH == self.currentRefineType:
				return self.CanRefineStrengthSimple(vnum)

			else:
				return False

		def CanRefineGradeSimple(self, vnum):
			ds_info = self.__GetDragonSoulTypeInfo(vnum)

			if DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO == ds_info:
				return False

			currentRecipe = self.__GetRefineGradeRecipe(vnum)
			if not currentRecipe:
				return False

			ds_type, grade, step, strength = ds_info
			cur_refine_ds_type, cur_refine_grade, cur_refine_step, cur_refine_strength = currentRecipe["ds_info"]
			if not (cur_refine_ds_type == ds_type and cur_refine_grade == grade):
				return False

			return True

		def CanRefineStepSimple(self, vnum):
			ds_info = self.__GetDragonSoulTypeInfo(vnum)

			if DragonSoulRefineWindow.INVALID_DRAGON_SOUL_INFO == ds_info:
				return False

			currentRecipe = self.__GetRefineStepRecipe(vnum)
			if not currentRecipe:
				return False

			ds_type, grade, step, strength = ds_info
			cur_refine_ds_type, cur_refine_grade, cur_refine_step, cur_refine_strength = currentRecipe["ds_info"]
			if not (cur_refine_ds_type == ds_type and cur_refine_grade == grade and cur_refine_step == step):
				return False

			return True

		def CanRefineStrengthSimple(self, vnum):
			if self.__IsDragonSoul(vnum):
				ds_type, grade, step, strength = self.__GetDragonSoulTypeInfo(vnum)

				import dragon_soul_refine_settings
				if strength >= dragon_soul_refine_settings.dragon_soul_refine_info[ds_type]["strength_max_table"][grade][
					step]:
					return False

				else:
					return True

			else:
				return False

		def HasNeedCount(self, needVnum, needCount):
			getItemVNum = player.GetItemIndex

			count = 0
			for i in xrange(player.DRAGON_SOUL_PAGE_SIZE):
				# <- dragon soul kind
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, i)
				itemVnum = getItemVNum(player.DRAGON_SOUL_INVENTORY, slotNumber)
				if itemVnum != 0 and needVnum == itemVnum:
					count = count + 1

			return count >= needCount

		def __InventoryLocalSlotPosToGlobalSlotPos(self, window_type, local_slot_pos):
			if player.EQUIPMENT == window_type:
				return self.wndDragonSoul.deckPageIndex * player.DRAGON_SOUL_EQUIPMENT_FIRST_SIZE + local_slot_pos

			return (self.wndDragonSoul.DSKindIndex * player.DRAGON_SOUL_PAGE_COUNT * player.DRAGON_SOUL_PAGE_SIZE) + \
				self.wndDragonSoul.inventoryPageIndex * player.DRAGON_SOUL_PAGE_SIZE + local_slot_pos

		def __RefineOther(self, iType):
			iTypes = {
				DragonSoulRefineWindow.REFINE_TYPE_STEP : {
					"cPerRefine" : self.refineSlotLockStartIndex,
					"refIndex" : 0,
					"aVnum" : 0,
				},
				DragonSoulRefineWindow.REFINE_TYPE_STRENGTH : {
					"cPerRefine" : 1,
					"refIndex" : 1,
					"aVnum" : 100300,
				},
			}

			if not iTypes.has_key(iType):
				return

			conf = iTypes[iType]
			if not conf["refIndex"] in self.refineItemInfo:
				self.wndPopupDialog.SetText("localeInfo.DRAGON_SOUL_REFINE_ALL_NO_MATERIAL")
				self.wndPopupDialog.Open()
				return

			inven_type, inven_pos, item_count = self.refineItemInfo[conf["refIndex"]]
			vnum = player.GetItemIndex(inven_type, inven_pos)
			if vnum == 0:
				return

			getItemVNum = player.GetItemIndex

			if iType == DragonSoulRefineWindow.REFINE_TYPE_STEP:
				for i in xrange(player.DRAGON_SOUL_PAGE_SIZE):
					# <- dragon soul kind
					slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(player.DRAGON_SOUL_INVENTORY, i)
					itemVnum = getItemVNum(player.DRAGON_SOUL_INVENTORY, slotNumber)
					if itemVnum == vnum and self.HasNeedCount(itemVnum, conf["cPerRefine"]) and self.CheckCanRefineSimple(
							itemVnum):

						self.AutoSetItem((player.DRAGON_SOUL_INVENTORY, slotNumber + 1), 1)
						if len(self.refineItemInfo) >= conf["cPerRefine"]:
							player.SendDragonSoulRefine(DragonSoulRefineWindow.DS_SUB_HEADER_DIC[self.currentRefineType],
														self.refineItemInfo)

							self.refineItemInfo = {}
				
				return

			sNumber = self.refineItemInfo[conf["refIndex"]][1]
			iVnum = getItemVNum(player.DRAGON_SOUL_INVENTORY, sNumber)
			if iVnum == 0:
				return

			self.__RefineStrength(conf, iVnum)

		def __getMillis(self):
			import time
			return time.clock() * 100

		def __RefineStrength(self, conf, iVnum):
			if not self.CheckCanRefineSimple(iVnum):
				self.refineItemLoop = None
				self.refineLoopTime = 0
				return

			if len(self.refineItemInfo) >= conf["cPerRefine"]:
				player.SendDragonSoulRefine(DragonSoulRefineWindow.DS_SUB_HEADER_DIC[self.currentRefineType],
											self.refineItemInfo)

			self.refineItemLoop = [conf, iVnum]
			self.refineLoopTime = self.__getMillis()

		def OnUpdate(self):
			if self.refineItemLoop != None:
				conf, vnum = self.refineItemLoop
				deltaTime = self.__getMillis() - self.refineLoopTime

				if len(self.refineItemInfo) > conf["cPerRefine"]:
					sNumber = self.refineItemInfo[conf["refIndex"]][1]
					iVnum = player.GetItemIndex(player.DRAGON_SOUL_INVENTORY, sNumber)

					if iVnum != vnum:
						self.__RefineStrength(conf, iVnum)
						return

				if deltaTime > 50:
					self.refineItemLoop = None
					
		def __PressDoAllRefineButton(self):
			if self.REFINE_TYPE_GRADE == self.currentRefineType:
				player.SendDragonSoulRefine(player.DS_SUB_HEADER_DO_UPGRADE_ALL, self.wndDragonSoul.DSKindIndex, self.wndDragonSoul.inventoryPageIndex)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Refresh(self):
		self.__RefreshRefineItemSlot()
		self.__ClearResultItemSlot()

		if app.ENABLE_DS_REFINE_ALL:
			if self.REFINE_TYPE_GRADE == self.currentRefineType:
				self.doAllRefineButton.Show()
			else:
				self.doAllRefineButton.Hide()

	def __RefreshRefineItemSlot(self):
		try:
			for slotPos in xrange(self.wndRefineSlot.GetSlotCount()):
				self.wndRefineSlot.ClearSlot(slotPos)
				if slotPos < self.refineSlotLockStartIndex:
					if slotPos in self.refineItemInfo:
						invenType, invenPos, itemCount = self.refineItemInfo[slotPos]
						itemVnum = player.GetItemIndex(invenType, invenPos)

						# if itemVnum:
						if itemVnum:
							self.wndRefineSlot.SetItemSlot(slotPos, player.GetItemIndex(invenType, invenPos), itemCount)
						else:
							del self.refineItemInfo[slotPos]

					if not slotPos in self.refineItemInfo:
						try:
							reference_vnum = 0
							if DragonSoulRefineWindow.REFINE_TYPE_STRENGTH == self.currentRefineType:
								if DragonSoulRefineWindow.REFINE_STONE_SLOT == slotPos:
									reference_vnum = 100300
							else:
								reference_vnum = self.__MakeDragonSoulVnum(*self.currentRecipe["ds_info"])
							if 0 != reference_vnum:
								item.SelectItem(reference_vnum)
								itemIcon = item.GetIconImage()
								(width, height) = item.GetItemSize()
								self.wndRefineSlot.SetSlot(slotPos, 0, width, height, itemIcon, (1.0, 1.0, 1.0, 0.5))
								self.wndRefineSlot.SetSlotCount(slotPos, 0)
						except:
							pass
					self.wndRefineSlot.HideSlotBaseImage(slotPos)
				# slotPos >= self.refineSlotLockStartIndex:
				else:
					if slotPos in self.refineItemInfo:
						invenType, invenPos, itemCount = self.refineItemInfo[slotPos]
						remainCount = player.GetItemCount(invenType, invenPos)
						player.SetItemCount(invenType, invenPos, remainCount + itemCount)
						del self.refineItemInfo[slotPos]
					self.wndRefineSlot.ShowSlotBaseImage(slotPos)

			if not self.refineItemInfo:
				self.__Initialize()

			self.wndRefineSlot.RefreshSlot()
		except Exception, e:
			import dbg
			dbg.TraceError("Exception : __RefreshRefineItemSlot, %s" % e)

	def __GetEmptySlot(self, itemVnum = 0):
		if DragonSoulRefineWindow.REFINE_TYPE_STRENGTH == self.currentRefineType:
			if 0 == itemVnum:
				return -1

			if self.__IsDragonSoul(itemVnum):
				if not DragonSoulRefineWindow.DRAGON_SOUL_SLOT in self.refineItemInfo:
					return DragonSoulRefineWindow.DRAGON_SOUL_SLOT
			else:
				if not DragonSoulRefineWindow.REFINE_STONE_SLOT in self.refineItemInfo:
					return DragonSoulRefineWindow.REFINE_STONE_SLOT
		else:
			for slotPos in xrange(self.wndRefineSlot.GetSlotCount()):
				if not slotPos in self.refineItemInfo:
					return slotPos

		return -1

	def AutoSetItem(self, inven, itemCount):
		invenType, invenPos = inven
		itemVnum = player.GetItemIndex(invenType, invenPos)
		emptySlot = self.__GetEmptySlot(itemVnum)
		if -1 == emptySlot:
			return

		self.__SetItem((invenType, invenPos), emptySlot, itemCount)

	def __ClearResultItemSlot(self):
		self.wndResultSlot.ClearSlot(0)
		self.resultItemInfo = {}

	def Refill(self):
		current = self.refineItemInfo
		self.__Initialize()

		for idx, value in current.iteritems():
			invenType, invenPos, itemCount = value
			iCurrentCount = player.GetItemCount(invenType, invenPos)
			self.__SetItem((invenType, invenPos), idx, iCurrentCount)

		# if 
	def RefineSucceed(self, inven_type, inven_pos):
		if self.currentRefineType != DragonSoulRefineWindow.REFINE_TYPE_STRENGTH:
			self.__Initialize()
		else:
			self.Refill()
		self.Refresh()

		itemCount = player.GetItemCount(inven_type, inven_pos)
		if itemCount > 0:
			self.resultItemInfo[0] = (inven_type, inven_pos, itemCount)
			self.wndResultSlot.SetItemSlot(0, player.GetItemIndex(inven_type, inven_pos), itemCount)

	def	RefineFail(self, reason, inven_type, inven_pos):
		if net.DS_SUB_HEADER_REFINE_FAIL == reason:
			if self.currentRefineType != DragonSoulRefineWindow.REFINE_TYPE_STRENGTH:
				self.__Initialize()
			else:
				self.Refill()
			self.Refresh()
			itemCount = player.GetItemCount(inven_type, inven_pos)
			if itemCount > 0:
				self.resultItemInfo[0] = (inven_type, inven_pos, itemCount)
				self.wndResultSlot.SetItemSlot(0, player.GetItemIndex(inven_type, inven_pos), itemCount)
		else:
			self.Refresh()

	def SetInventoryWindows(self, wndInventory, wndDragonSoul):
		self.wndInventory = wndInventory
		self.wndDragonSoul = wndDragonSoul

	def __CreateToolTip(self):
		if not self.TitleToolTip:
			return

		(pos_x, pos_y) = wndMgr.GetMousePosition()

		self.TitleToolTip.ClearToolTip()
		self.TitleToolTip.AppendShortcut([app.DIK_RETURN], localeInfo.QUICK_ACTION_CHECKBOX_DRAGON_SOUL, bCenter = True, bSpace = False)
		self.TitleToolTip.SetToolTipPosition(pos_x, pos_y - 5)
		self.TitleToolTip.Show()

	def __HideToolTip(self):
		if not self.TitleToolTip:
			return

		self.TitleToolTip.HideToolTip()

	def HandleReturnButton(self):
		return self.GetChild("TitleBar").HandleButtonGetter("BTN_CHBOX").IsChecked()

	def OnPressReturnKey(self):
		if self.HandleReturnButton():
			self.__PressDoRefineButton()
			return True
