import localeInfo
import uiCommon
import item
import player
import net
import ui
import mouseModule
import uiToolTip
import chat

class TransmutationWindow(ui.ScriptWindow):
	questionDialog = None
	tooltipInfo = None
	popupDialog = None
	SlotsIndexes = [-1, -1]

	TRANSMUTATION_COST = 1000000000

	def __init__(self, inventoryWindow):
		ui.ScriptWindow.__init__(self)
		self.inventoryWindow = inventoryWindow
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/transmutation.py")
		except:
			import exception
			exception.Abort("TransmutationWindow.__LoadWindow.LoadObject")

		try:
			self.wndItem = self.GetChild("ChangeLookSlot")
			self.board = self.GetChild("board")
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			self.GetChild("Cost").SetText(localeInfo.NumberToStringAsType(self.TRANSMUTATION_COST, True))
			self.GetChild("AcceptButton").SetEvent(self.SendAccept)
			self.GetChild("CancelButton").SetEvent(self.Close)

			self.wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
			self.wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			self.wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			self.wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
			self.wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))

			self.tooltipInfo = uiToolTip.ItemToolTip()

			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.CHANGE_LOOK_CHANGE_ITEM)
			self.questionDialog.SetAcceptEvent(self.Accept)
			self.questionDialog.SetCancelEvent(self.Cancel)

			self.popupDialog = uiCommon.PopupDialog()

			self.SetCenterPosition()
		except:
			import exception
			exception.Abort("TransmutationWindow.__LoadWindow.BindObject")

	def	Destroy(self):
		self.ClearDictionary()
		self.wndItem = None
		self.board = None
		self.tooltipInfo = None
		self.questionDialog = None
		self.popupDialog = None
		self.inventoryWindow = None

	def Accept(self):
		net.SendChatPacket("/transmutate_item %d %d" % (self.SlotsIndexes[0], self.SlotsIndexes[1]))

	def Cancel(self):
		self.ClearGUI()
		self.questionDialog.Close()
		self.popupDialog.Close()

	def	UpdateWindow(self):
		self.Refresh()
		self.Show()

	def OnPressEscapeKey(self):
		self.Close()

	def Close(self):
		## Deleting Items For Sure
		for i in xrange(2):
			net.SendChatPacket("/transmutation_delete %d" % (i))

		self.ClearGUI()
		self.questionDialog.Close()
		self.popupDialog.Close()
		self.Hide()

	def	ClearGUI(self):
		for i in xrange(2):
			self.inventoryWindow.TransmutationSlots[self.SlotsIndexes[i]] = False
			self.SlotsIndexes[i] = -1
		self.Refresh()

	def SendAccept(self):
		if player.GetElk() < self.TRANSMUTATION_COST:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_NOT_ENOUGH_MONEY)
			return

		if self.SlotsIndexes[0] == -1 or self.SlotsIndexes[1] == -1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_INSERT_ITEM)
		else:
			self.questionDialog.Open()

	def	UpdateItemSlot(self, id, item):
		self.SlotsIndexes[id] = item

	def	Refresh(self):
		for i in xrange(2):
			slotNumber = self.SlotsIndexes[i]
			if slotNumber > -1:
				self.wndItem.SetItemSlot(i, player.GetItemIndex(slotNumber), 0)
			else:
				self.wndItem.ClearSlot(i)

		self.wndItem.RefreshSlot()
		self.inventoryWindow.RefreshBagSlotWindow()

	def	GetIterElement(self, iter, num):
		new_ele = iter+num
		if new_ele >= len(self.SlotsIndexes):
			return self.SlotsIndexes[0]
		else:
			return self.SlotsIndexes[new_ele]

	def	CheckItems(self, slotPos, baseSlot, itemType, itemSubType, itemGetAntiFlag):
		if self.SlotsIndexes[slotPos] > -1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_ITEM_EXISTS)
			return False

		other_slot = self.GetIterElement(slotPos, 1)

		if baseSlot == other_slot and other_slot != -1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_SAME_ITEMS)
			return False

		if player.GetItemIndex(baseSlot) == player.GetItemIndex(other_slot):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_SAME_ITEMS)
			return False

		if player.GetItemTransmutate(baseSlot) > 0 and slotPos == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_IS_ALREADY_CHANGED)
			return False

		if other_slot > -1:
			item.SelectItem(player.GetItemIndex(other_slot))

			if itemType != item.GetItemType() or itemSubType != item.GetItemSubType() or item.GetAntiFlag() != itemGetAntiFlag:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_OTHER_TYPES)
				return False

		if item.ITEM_TYPE_WEAPON == itemType and not itemSubType == item.WEAPON_ARROW or (item.ITEM_TYPE_ARMOR == itemType and itemSubType == item.ARMOR_BODY) or (itemType == item.ITEM_TYPE_COSTUME and itemSubType == item.COSTUME_TYPE_SASH):
			return True
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CHANGE_LOOK_DO_NOT_CHANGE_LOOK_ITEM)
			return False

	def OverInItem(self, slotIndex):
		if self.tooltipInfo and self.SlotsIndexes[slotIndex] != -1:
			self.tooltipInfo.SetInventoryItem(self.SlotsIndexes[slotIndex])

	def OverOutItem(self):
		if self.tooltipInfo:
			self.tooltipInfo.HideToolTip()

	def SelectEmptySlot(self, selectedSlotPos):
		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()

			if player.SLOT_TYPE_INVENTORY != attachedSlotType:
				mouseModule.mouseController.DeattachObject()
				return

			item.SelectItem(player.GetItemIndex(attachedSlotPos))

			if self.CheckItems(selectedSlotPos, attachedSlotPos, item.GetItemType(), item.GetItemSubType(), item.GetAntiFlag()):
				self.inventoryWindow.TransmutationSlots[attachedSlotPos] = True
				self.UpdateItemSlot(selectedSlotPos, attachedSlotPos)
				self.Refresh()
				if selectedSlotPos == 1:
					self.SetPopup(localeInfo.CHANGE_LOOK_AWARE)
				net.SendChatPacket("/transmutation_add %d %d" % (selectedSlotPos, attachedSlotPos))

			mouseModule.mouseController.DeattachObject()

	def UseItemSlot(self, selectedSlotPos):
		if self.SlotsIndexes[selectedSlotPos] != -1:
			self.inventoryWindow.TransmutationSlots[self.SlotsIndexes[selectedSlotPos]] = False
			self.UpdateItemSlot(selectedSlotPos, -1)
			self.Refresh()
			net.SendChatPacket("/transmutation_delete %d" % (selectedSlotPos))

	def	SetPopup(self, text):
		self.popupDialog.SetText(text)
		self.popupDialog.SetAutoClose()
		self.popupDialog.Open()

