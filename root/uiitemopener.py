import ui
import app
import net
import chat
import player
import uiGuild
import uiToolTip
import localeInfo
import mouseModule
import item

from _weakref import proxy

class ItemOpener(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipInfo = uiToolTip.ItemToolTip()
		self.slot_pos = -1
		self.ttOpeningTime = 0
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.tooltipInfo = None
		self.slot_pos = -1
		self.board = None
		self.SlotWindow = None
		self.ButtonAccept = None
		self.ButtonDecline = None
		self.CheckBox = None
		self.InputValue = None
		self.ttOpeningTime = 0

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/item_opener.py")
		except:
			import exception
			exception.Abort("ItemOpener.__LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			self.SlotWindow = self.GetChild("SlotWindow")
			self.InputValue = self.GetChild("InputValue")
			self.CheckBox = self.GetChild("CheckBox")
			self.ButtonAccept = self.GetChild("ButtonAccept")
			self.ButtonDecline = self.GetChild("ButtonDecline")

			## Slot Window
			self.SlotWindow.SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
			self.SlotWindow.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
			self.SlotWindow.SetUnselectItemSlotEvent(ui.__mem_func__(self.__UseItemSlot))
			self.SlotWindow.SetUseSlotEvent(ui.__mem_func__(self.__UseItemSlot))
			self.SlotWindow.SetSelectEmptySlotEvent(ui.__mem_func__(self.__UseItemSlot))
			self.SlotWindow.SetSelectItemSlotEvent(ui.__mem_func__(self.__UseItemSlot))
			self.SlotWindow.RefreshSlot()

			self.InputValue.SetOverlayText(localeInfo.ITEM_OPENER_PLACEHOLDER_TEXT)
			## BuyButton
			self.ButtonAccept.SAFE_SetEvent(self.__AcceptAction)
			self.ButtonDecline.SAFE_SetEvent(self.__DeclineAction)

			self.SetCenterPosition()
			self.Hide()
		except:
			import exception
			exception.Abort("ItemOpener.__LoadWindow.BindObject")

	def	OpenWithSlot(self, slot_pos):
		self.__UpdateSlot(slot_pos)
		self.Open()

	def	__UpdateSlot(self, slot_pos):
		self.SlotWindow.SetItemSlot(0, player.GetItemIndex(slot_pos), player.GetItemCount(slot_pos))
		self.SlotWindow.RefreshSlot()
		self.slot_pos = slot_pos

	def	__Refresh(self, killFocus = False):
		self.ttOpeningTime = 0
		self.CheckBox.SetChecked(False)
		self.InputValue.SetText("")
		if killFocus:
			self.InputValue.KillFocus()
		else:
			self.InputValue.SetFocus()
		self.SlotWindow.ClearSlot(0)
		self.SlotWindow.RefreshSlot()
		self.slot_pos = -1

	def RefreshSlot(self):
		self.__UpdateSlot(self.slot_pos)

	def	__CheckConformation(self):
		return self.CheckBox.IsChecked()

	def	__AcceptAction(self):
		if self.__CheckConformation():
			net.SendChatPacket("/quick_open %d 0" % self.slot_pos)
			return

		if self.InputValue.GetText() != "":
			value = 0L
			try:
				value = long(self.InputValue.GetText())
			except (KeyError, ValueError, ):
				value = 0L

			if player.GetItemCount(self.slot_pos) < value:
				return

			net.SendChatPacket("/quick_open %d %d" % (self.slot_pos, value))

			# self.SlotWindow.SetItemSlot(0, player.GetItemIndex(self.slot_pos), player.GetItemCount(self.slot_pos) - value)
			# self.SlotWindow.RefreshSlot()
			return

		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ITEM_OPENER_MISSING_CONFORMATION)
		return

	def	__DeclineAction(self):
		self.Close()

	def	__UseItemSlot(self, slotPos):
		self.__Refresh()

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()

			mouseModule.mouseController.DeattachObject()

			if player.SLOT_TYPE_INVENTORY != attachedSlotType or player.GetItemIndex(attachedSlotPos) <= 0:
				return

			vnum = player.GetItemIndex(attachedSlotPos)
			item.SelectItem(vnum)
			if not item.GetItemType() == item.ITEM_TYPE_GIFTBOX:
				return

			self.__UpdateSlot(attachedSlotPos)

	def __OverInItem(self, slotIndex):
		if self.tooltipInfo:
			if self.slot_pos > -1:
				self.tooltipInfo.ClearToolTip()
				self.tooltipInfo.SetInventoryItem(self.slot_pos)

	def __OverOutItem(self):
		if self.tooltipInfo:
			self.tooltipInfo.HideToolTip()

	def	Close(self):
		self.__Refresh(True)
		self.Hide()

	def	Open(self):
		self.SetTop()
		self.SetCenterPosition()
		self.Show()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.Open()
