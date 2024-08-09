from localeinfo import NumberToString
import ui
import app
import net
import math
import time
import item
import player
import uiCommon
import uiToolTip
import localeInfo
import mouseModule

GAYA_CRAFTING_UPDATE_REQUEST = False

def NumberToMoneyString(n) :
	if n <= 0 :
		return "0 %s" % (localeInfo.GAYA_POINTS)

	return "%s %s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]), localeInfo.GAYA_POINTS)

class GayaCrafting(ui.ScriptWindow):

	GAYA_WINDOW_BASE_SIZE = (174, 78)
	GAYA_CRAFTING_DICT = {}
	GAYA_GRID_SIZE = (5, 1)
	GAYA_CRAFTING_LIST = 50927
	INVENTORY_PAGE_COUNT = 5

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.board = None
		self.wndCraftingItems = None
		self.ExitButton = None

	def	__LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/gaya_crafting.py")
		except:
			import exception
			exception.Abort("GayaCrafting.__LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("board")
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			self.wndCraftingItems = self.GetChild("CraftingItems")
			self.ExitButton = self.GetChild("ExitButton")
		except:
			import exception
			exception.Abort("GayaCrafting.__LoadWindow.BindObject")

		self.wndCraftingItems.SetUnselectItemSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.wndCraftingItems.SetUseSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.wndCraftingItems.SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
		self.wndCraftingItems.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))

		self.ExitButton.SAFE_SetEvent(self.Close)

		self.SetCenterPosition()
		self.SetTop()
		self.Hide()

	def	Refresh(self):
		self.GAYA_CRAFTING_DICT = {}
		crafting_slots = []

		for i in xrange(player.INVENTORY_SLOT_COUNT):
			if player.GetItemIndex(i) == self.GAYA_CRAFTING_LIST:
				crafting_slots.append(i)

		(w, h) = (self.board.GetWidth(), (max(math.ceil(float(len(crafting_slots))/float(self.GAYA_GRID_SIZE[0])), 1)*32)+self.GAYA_WINDOW_BASE_SIZE[1])
		self.SetSize(w, h)
		self.board.SetSize(w, h)
		self.ExitButton.SetPosition(0, 30)
		self.wndCraftingItems.ArrangeSlot(0, self.GAYA_GRID_SIZE[0], (h-self.GAYA_WINDOW_BASE_SIZE[1])/32, 32, 32, 0, 0)
		self.wndCraftingItems.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		self.wndCraftingItems.RefreshSlot()

		for slot in xrange(len(crafting_slots)):
			slot_num = crafting_slots[slot]
			self.wndCraftingItems.ClearSlot(slot)
			self.wndCraftingItems.SetItemSlot(slot, player.GetItemIndex(slot_num), player.GetItemCount(slot_num))
			self.GAYA_CRAFTING_DICT[slot] = (slot_num, player.GetItemIndex(slot_num))

		self.wndCraftingItems.RefreshSlot()
		self.tooltipItem.HideToolTip()

	def	__UseItemSlot(self, slot):
		net.SendChatPacket("/craft_gaya_item %d" % self.GAYA_CRAFTING_DICT[slot][0])

	def	__OverInItem(self, slot):
		if self.tooltipItem:
			if slot in self.GAYA_CRAFTING_DICT and self.GAYA_CRAFTING_DICT[slot][1] != 0:
				self.tooltipItem.ClearToolTip()
				self.tooltipItem.AddItemData(self.GAYA_CRAFTING_DICT[slot][1], [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])

	def	__OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def	Close(self):
		self.tooltipItem.HideToolTip()
		self.Hide()

	def	Open(self):
		self.Refresh()
		self.SetCenterPosition()
		self.Show()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.Open()

	def	OnUpdate(self):
		global GAYA_CRAFTING_UPDATE_REQUEST
		if GAYA_CRAFTING_UPDATE_REQUEST:
			self.Refresh()
			GAYA_CRAFTING_UPDATE_REQUEST = False

class GayaMarket(ui.ScriptWindow):

	GAYA_SHOP_MAX_COUNT = 9
	GAYA_UNLOCK_ITEM = 39064

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.NextRotation = 0
		self.GayaSlots = {"SLOTS" : [(-1, 0, 0, False) for i in xrange(self.GAYA_SHOP_MAX_COUNT)], "PRICES" : [None for i in xrange(self.GAYA_SHOP_MAX_COUNT)]}
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.questionDialog = uiCommon.QuestionDialog()
		self.popupDialog = uiCommon.PopupDialog()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.NextRotation = 0
		self.GayaSlots = {}
		self.tooltipItem = None
		self.questionDialog = None
		self.popupDialog = None
		self.board = None
		self.MarketSlots = None
		self.RotationTime = None
		self.RefreshButton = None

	def	__LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/gaya_market.py")
		except:
			import exception
			exception.Abort("GayaMarket.__LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("board")
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			self.MarketSlots = self.GetChild("SellItemSlot")
			self.RotationTime = self.GetChild("BuyRefreshTime")
			self.RefreshButton = self.GetChild("RefreshButton")
			for i in xrange(self.GAYA_SHOP_MAX_COUNT):
				self.GayaSlots["PRICES"][i] = self.GetChild("slot_%d_price" % (i+1))

		except:
			import exception
			exception.Abort("GayaMarket.__LoadWindow.BindObject")

		self.MarketSlots.SetSelectItemSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.MarketSlots.SetUnselectItemSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.MarketSlots.SetUseSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.MarketSlots.SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
		self.MarketSlots.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))

		for i in xrange(self.GAYA_SHOP_MAX_COUNT):
			self.MarketSlots.SetCoverButton(i, "d:/ymir work/ui/gaya_cover.tga",\
												"d:/ymir work/ui/gaya_cover.tga",\
												"d:/ymir work/ui/gaya_cover.tga",\
												"d:/ymir work/ui/public/slot_cover_button_01.sub",\
												True, True)

		self.RefreshButton.SAFE_SetEvent(self.__PullRotation)

		self.questionDialog = uiCommon.QuestionDialog()
		self.questionDialog.Hide()

		self.popupDialog = uiCommon.PopupDialog()
		self.popupDialog.Hide()

		self.SetCenterPosition()
		self.SetTop()
		self.Hide()

	def	UpdateGayaSlot(self, id, vnum, count, price, status):
		totalPrice = price*count

		self.GayaSlots["SLOTS"][id] = (vnum, count, totalPrice, status)
		self.GayaSlots["PRICES"][id].SetText("%d" % price)
		self.Refresh()

	def	SetNextRotationTime(self, tm):
		self.NextRotation = app.GetTime()+tm

	def	Refresh(self):
		for key in xrange(len(self.GayaSlots["SLOTS"])):
			(vnum, count, price, status) = self.GayaSlots["SLOTS"][key]
			if vnum == -1:
				self.MarketSlots.ClearSlot(key)
				continue

			## Setting up slot
			self.MarketSlots.SetItemSlot(key, vnum, count)

			## Putting cover
			if not status:
				self.MarketSlots.SetCoverButton(key, "d:/ymir work/ui/gaya_cover.tga",\
													"d:/ymir work/ui/gaya_cover.tga",\
													"d:/ymir work/ui/gaya_cover.tga",\
													"d:/ymir work/ui/gaya_cover.tga",\
													True, True)
			else:
				self.MarketSlots.SetCoverButton(key, "d:/ymir work/ui/public/slot_cover_button_01.sub",\
													"d:/ymir work/ui/public/slot_cover_button_01.sub",\
													"d:/ymir work/ui/public/slot_cover_button_01.sub",\
													"d:/ymir work/ui/public/slot_cover_button_01.sub",\
													True, True)

		## Refreshing slot
		self.MarketSlots.RefreshSlot()

	def	Clear(self):
		self.GayaSlots["SLOTS"] = [(-1, 0, 0, False) for i in xrange(self.GAYA_SHOP_MAX_COUNT)]
		for key in xrange(len(self.GayaSlots["SLOTS"])):
			self.GayaSlots["PRICES"][key].SetText("%d" % self.GayaSlots["SLOTS"][key][2])

	def	__UseItemSlot(self, slot):
		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()

			if player.SLOT_TYPE_INVENTORY != mouseModule.mouseController.GetAttachedType():
				return

			mouseModule.mouseController.DeattachObject()

			if self.GayaSlots["SLOTS"][slot][3] != False:
				return

			if player.GetItemIndex(attachedSlotPos) != self.GAYA_UNLOCK_ITEM:
				return

			self.questionDialog.SetText(localeInfo.GAYA_SLOT_UNLOCK_ASK_DIALOG % slot)
			self.questionDialog.SetAcceptEvent(lambda arg1 = slot, arg2 = attachedSlotPos : self.__UnlockSlot(arg1, arg2))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__CloseDialog))
			self.questionDialog.Open()
		else:
			if self.GayaSlots["SLOTS"][slot][3] != False:
				if self.GayaSlots["SLOTS"][slot][1] > player.GetGayaCount():
					self.popupDialog.SetText(localeInfo.GAYA_BUY_NOT_ENOUGH_MONEY)
					self.popupDialog.SetAutoClose()
					self.popupDialog.Open()
					return

				item.SelectItem(self.GayaSlots["SLOTS"][slot][0])
				self.questionDialog.SetText(localeInfo.GAYA_BUY_ASK_DIALOG % (item.GetItemName(), NumberToMoneyString(self.GayaSlots["SLOTS"][slot][2]) + " |Eemoticons/tooltip/gaya|e ?"))
				self.questionDialog.SetAcceptEvent(lambda arg = slot : self.__BuyItem(arg))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__CloseDialog))
				self.questionDialog.AutoResize(50)
				self.questionDialog.Open()
			else:
				self.popupDialog.SetText(localeInfo.GAYA_SLOT_LOCK_DIALOG)
				self.popupDialog.SetAutoClose()
				self.popupDialog.Open()

	def	__PullRotation(self, arg = None):
		if not arg:
			self.questionDialog.SetText(localeInfo.GAYA_ROTATION_ASK_DIALOG)
			self.questionDialog.SetAcceptEvent(lambda arg = True : self.__PullRotation(arg))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__CloseDialog))
			self.questionDialog.Open()
		else:
			net.SendChatPacket("/request_gaya_rotation")
			self.__CloseDialog()

	def	__UnlockSlot(self, slot, attachSlot):
		net.SendChatPacket("/unlock_gaya_slot %d %d" % (slot, attachSlot))
		self.__CloseDialog()

	def	__BuyItem(self, slot):
		net.SendChatPacket("/purchase_gaya_item %d" % slot)
		self.__CloseDialog()

	def	__CloseDialog(self):
		self.questionDialog.Close()

	def	__OverInItem(self, slot):
		if self.tooltipItem:
			if self.GayaSlots["SLOTS"][slot][3] != False:
				self.tooltipItem.ClearToolTip()
				self.tooltipItem.AddItemData(self.GayaSlots["SLOTS"][slot][0], [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])

	def	__OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def	Close(self):
		self.Hide()

	def	Open(self):
		self.Refresh()
		self.SetCenterPosition()
		self.Show()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.Open()

	def	OnUpdate(self):
		if self.NextRotation > 0:
			tm_format = max(self.NextRotation-app.GetTime(), 0)
			if app.GetTime() >= self.NextRotation:
				self.NextRotation = 0

			self.RotationTime.SetText(time.strftime("%M:%S", time.localtime(tm_format)))

