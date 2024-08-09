import ui
import net
import item
import player
import uiCommon
import uiToolTip
import localeInfo
import mouseModule
import wndMgr
import app

#TODO Lets check why we have problem with the slots after rewarping while we have items in slot :o
#TODO Lets do OnImeReturn!
PROCESS_SLOTS = {}
SASH_ABSORPTION_ITEM = (0, 0)
IS_OPEN_COMBINATION = False
IS_OPEN_ABSORPTION = False

class SashCombination(ui.ScriptWindow):

	## (vnum, slot_id)
	SASH_LIST = {i : {"VNUM" : 0, "SLOT" : -1} for i in xrange(3)}
	BASE_SLOT_NUM = 0
	RESULT_SLOT_NUM = 2
	MAX_UPGRADE_VALUE = 3

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.questionDialog = uiCommon.QuestionDialog()
		self.popupDialog = uiCommon.PopupDialog()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.board = None
		self.wndSashSlots = None
		self.CostLabel = None
		self.PercentLabel = None
		self.AcceptButton = None
		self.CancelButton = None
		self.questionDialog = None

		global IS_OPEN_COMBINATION
		IS_OPEN_COMBINATION = False

	def	__LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/sash_combination.py")
		except:
			import exception
			exception.Abort("SashCombination.__LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("board")
			self.wndSashSlots = self.GetChild("AcceSlot")
			self.CostLabel = self.GetChild("Cost")
			self.PercentLabel = self.GetChild("Percent")
			self.AcceptButton = self.GetChild("AcceptButton")
			self.CancelButton = self.GetChild("CancelButton")
		except:
			import exception
			exception.Abort("SashCombination.__LoadWindow.BindObject")

		self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

		self.TitleToolTip = uiToolTip.ToolTip()
		self.TitleToolTip.ClearToolTip()

		self.GetChild("board").HandleButtonState("BTN_CHBOX", True)
		self.GetChild("board").HandleButtonGetter("BTN_CHBOX").SetOverEvent(ui.__mem_func__(self.__CreateToolTip))
		self.GetChild("board").HandleButtonGetter("BTN_CHBOX").SetOverOutEvent(ui.__mem_func__(self.__HideToolTip))

		self.wndSashSlots.SetSelectItemSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.wndSashSlots.SetUnselectItemSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.wndSashSlots.SetUseSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.wndSashSlots.SetSelectEmptySlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.wndSashSlots.SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
		self.wndSashSlots.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))

		self.AcceptButton.SAFE_SetEvent(self.__StartProcess)
		self.CancelButton.SAFE_SetEvent(self.Close)

		self.questionDialog.Hide()

		self.popupDialog.SetWidth(400)
		self.popupDialog.Hide()

		self.CostLabel.SetText(localeInfo.SASH_SYSTEM_PRICE_TEXT.format(localeInfo.NumberToStringAsType(0, True)))
		self.PercentLabel.SetText(localeInfo.SASH_SYSTEM_CHANCE_TEXT.format(0))

		self.SetCenterPosition()
		self.SetTop()
		self.Hide()

	def __CreateToolTip(self):
		if not self.TitleToolTip:
			return

		(pos_x, pos_y) = wndMgr.GetMousePosition()

		self.TitleToolTip.ClearToolTip()
		self.TitleToolTip.AppendShortcut([app.DIK_RETURN], localeInfo.QUICK_ACTION_CHECKBOX_REFINE, bCenter = True, bSpace = False)
		self.TitleToolTip.SetToolTipPosition(pos_x, pos_y - 5)
		self.TitleToolTip.Show()

	def __HideToolTip(self):
		if not self.TitleToolTip:
			return

		self.TitleToolTip.HideToolTip()

	def HandleReturnButton(self):
		return self.GetChild("board").HandleButtonGetter("BTN_CHBOX").IsChecked()

	def OnPressReturnKey(self):
		if self.HandleReturnButton():
			self.__StartProcess()
			return True

	def	UpdateSlot(self, slot_num, vnum, slot_inv):
		global PROCESS_SLOTS
		if vnum <= 0:
			PROCESS_SLOTS[slot_num] = { "Sett" : False, "Slot" : -1 }

		self.SASH_LIST[slot_num]["VNUM"] = vnum
		self.SASH_LIST[slot_num]["SLOT"] = slot_inv

		## Additonal support for erasing/warnings
		if slot_num == (self.RESULT_SLOT_NUM-1):
			if vnum > 0:
				## Warning
				self.popupDialog.SetText("localeInfo.SASH_SYSTEM_COMBINATION_WARNING")
				self.popupDialog.Open()

		if slot_num != self.RESULT_SLOT_NUM and slot_inv > -1:
			PROCESS_SLOTS[slot_num] = { "Sett" : True, "Slot" : slot_inv } if vnum > 0 else { "Sett" : False, "Slot" : -1 }
			item.SelectItem(self.SASH_LIST[slot_num]["VNUM"])

		self.Refresh()

	def	UpdateCost(self, cost):
		self.CostLabel.SetText(localeInfo.SASH_SYSTEM_PRICE_TEXT.format(localeInfo.NumberToStringAsType(cost, True)))

		iVnum = self.SASH_LIST[self.BASE_SLOT_NUM]["VNUM"]
		iPercent = 0
		if iVnum > 0:
			item.SelectItem(self.SASH_LIST[self.BASE_SLOT_NUM]["VNUM"])
			iPercent = item.GetValue(player.SASH_REFINE_CHANCE_ITEM_VALUE)

		self.PercentLabel.SetText(localeInfo.SASH_SYSTEM_CHANCE_TEXT.format(iPercent))

	def	Clear(self):
		global PROCESS_SLOTS
		for k in PROCESS_SLOTS.iterkeys():
			PROCESS_SLOTS[k] = { "Sett" : False, "Slot" : -1 }

		self.SASH_LIST = {i : {"VNUM" : 0, "SLOT" : -1} for i in xrange(3)}
		self.Refresh()

		self.CostLabel.SetText(localeInfo.SASH_SYSTEM_PRICE_TEXT.format(localeInfo.NumberToStringAsType(0, True, "")))
		self.PercentLabel.SetText(localeInfo.SASH_SYSTEM_CHANCE_TEXT.format(0))

	def	Refresh(self):
		for k, v in self.SASH_LIST.items():
			if v["VNUM"] > 0:
				self.wndSashSlots.SetItemSlot(k, v["VNUM"], 0)
			else:
				self.wndSashSlots.ClearSlot(k)

		self.wndSashSlots.RefreshSlot()

	def	__UseItemSlot(self, slot_num):
		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_INVENTORY != mouseModule.mouseController.GetAttachedType():
				return

			mouseModule.mouseController.DeattachObject()

			## No need to pull result slot
			if slot_num == self.RESULT_SLOT_NUM:
				return

			item.SelectItem(player.GetItemIndex(attachedSlotPos))
			if item.GetItemType() != item.ITEM_TYPE_COSTUME and item.GetItemSubType() != item.COSTUME_TYPE_SASH:
				return

			net.SendChatPacket("/sash_register_system_combination %d %d" % (slot_num, attachedSlotPos))
		else:
			net.SendChatPacket("/sash_register_system_combination %d %d" % (slot_num, -1))

	def	__OverInItem(self, slot_num):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()

			if self.SASH_LIST[slot_num]["VNUM"] > 0:
				if slot_num != self.RESULT_SLOT_NUM:
					self.tooltipItem.SetInventoryItem(self.SASH_LIST[slot_num]["SLOT"])
				else:
					## Fetching sockets
					metinSlot = [player.GetItemMetinSocket(self.SASH_LIST[self.BASE_SLOT_NUM]["SLOT"], i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
					## Fetching attrs
					attrSlot = [player.GetItemAttribute(self.SASH_LIST[self.BASE_SLOT_NUM]["SLOT"], i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

					item.SelectItem(self.SASH_LIST[slot_num]["VNUM"])

					bItemsIntegrity = (self.SASH_LIST[self.BASE_SLOT_NUM]["VNUM"] == self.SASH_LIST[slot_num]["VNUM"])

					if item.GetValue(0) == player.SASH_TYPE_LEGENDARY and bItemsIntegrity:
						metinSlot[player.METIN_SOCKET_MAX_NUM - 1] = min(metinSlot[player.SASH_TYPE_SOCKET] + self.MAX_UPGRADE_VALUE, player.SASH_ABSORPTION_VALUE_MAX)
					elif item.GetValue(0) == player.SASH_TYPE_LEGENDARY:
						metinSlot[player.METIN_SOCKET_MAX_NUM - 1] = player.SASH_ABSORPTION_LEGENDARY_MAX
					else:
						metinSlot[player.SASH_TYPE_SOCKET] = item.GetValue(0) * player.SASH_ABSORPTION_BASE_VALUE

					self.tooltipItem.AddItemData(self.SASH_LIST[slot_num]["VNUM"], metinSlot, attrSlot)

	def	__OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def	__StartProcess(self, arg = False):
		if not arg:
			for v in self.SASH_LIST.itervalues():
				if v["VNUM"] <= 0:
					return

			self.questionDialog.SetText("localeInfo.SASH_SYSTEM_COMBINATION_TEXT")
			self.questionDialog.SetAcceptEvent(lambda arg = True: self.__StartProcess(arg))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__CloseDialog))
			self.questionDialog.Open()
		else:
			net.SendChatPacket("/process_sash_system_combination")
			self.__CloseDialog()

	def	__CloseDialog(self):
		self.questionDialog.Close()

	def	Close(self):
		self.Clear()
		net.SendChatPacket("/sash_system_cancel")
		self.Hide()

		global IS_OPEN_COMBINATION
		IS_OPEN_COMBINATION = False

	def	Open(self):
		self.Refresh()
		self.SetCenterPosition()
		self.Show()

		global IS_OPEN_COMBINATION
		IS_OPEN_COMBINATION = True

	def	UpdateWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.Open()

class SashAbsorption(ui.ScriptWindow):

	## (vnum, slot_id)
	ITEM_LIST = {i : {"VNUM" : 0, "SLOT" : -1} for i in xrange(3)}
	BASE_SLOT_NUM = 0
	ITEM_SLOT_NUM = 1
	RESULT_SLOT_NUM = 2

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.questionDialog = uiCommon.QuestionDialog()
		self.popupDialog = uiCommon.PopupDialog()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.board = None
		self.wndItemSlots = None
		self.AcceptButton = None
		self.CancelButton = None
		self.questionDialog = None
		global IS_OPEN_ABSORPTION
		IS_OPEN_ABSORPTION = False

	def	__LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/sash_absorption.py")
		except:
			import exception
			exception.Abort("SashAbsorption.__LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("board")
			self.wndItemSlots = self.GetChild("AcceSlot")
			self.AcceptButton = self.GetChild("AcceptButton")
			self.CancelButton = self.GetChild("CancelButton")
		except:
			import exception
			exception.Abort("SashAbsorption.__LoadWindow.BindObject")

		self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

		self.wndItemSlots.SetSelectItemSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.wndItemSlots.SetUnselectItemSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.wndItemSlots.SetUseSlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.wndItemSlots.SetSelectEmptySlotEvent(ui.__mem_func__(self.__UseItemSlot))
		self.wndItemSlots.SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
		self.wndItemSlots.SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))

		self.AcceptButton.SAFE_SetEvent(self.__StartProcess)
		self.CancelButton.SAFE_SetEvent(self.Close)

		self.questionDialog.Hide()

		self.popupDialog.SetWidth(400)
		self.popupDialog.Hide()

		self.SetCenterPosition()
		self.SetTop()
		self.Hide()

	def	UpdateSlot(self, slot_num, vnum, slot_inv):
		global PROCESS_SLOTS
		if vnum <= 0:
			PROCESS_SLOTS[slot_num] = { "Sett" : False, "Slot" : -1 }

		self.ITEM_LIST[slot_num]["VNUM"] = vnum
		self.ITEM_LIST[slot_num]["SLOT"] = slot_inv

		## Additonal support for erasing/warnings
		if slot_num == self.BASE_SLOT_NUM:
			self.ITEM_LIST[self.RESULT_SLOT_NUM]["VNUM"] = vnum
		elif slot_num == self.ITEM_SLOT_NUM:
			if vnum > 0:
				## Warning
				self.popupDialog.SetText("localeInfo.SASH_SYSTEM_ABSORPTION_WARNING")
				self.popupDialog.Open()

		if slot_num != self.RESULT_SLOT_NUM and slot_inv > -1:
			PROCESS_SLOTS[slot_num] = { "Sett" : True, "Slot" : slot_inv } if vnum > 0 else { "Sett" : False, "Slot" : -1 }

		self.Refresh()

	def	Clear(self):
		global PROCESS_SLOTS
		for k in PROCESS_SLOTS.iterkeys():
			PROCESS_SLOTS[k] = { "Sett" : False, "Slot" : - 1 }

		self.ITEM_LIST = {i : {"VNUM" : 0, "SLOT" : -1} for i in xrange(3)}
		self.Refresh()

	def	Refresh(self):
		for k, v in self.ITEM_LIST.items():
			if v["VNUM"] > 0:
				self.wndItemSlots.SetItemSlot(k, v["VNUM"], 0)
			else:
				self.wndItemSlots.ClearSlot(k)

		self.wndItemSlots.RefreshSlot()

	def	__UseItemSlot(self, slot_num):
		if mouseModule.mouseController.isAttached():

			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			if player.SLOT_TYPE_INVENTORY != mouseModule.mouseController.GetAttachedType():
				return

			mouseModule.mouseController.DeattachObject()

			if slot_num == self.RESULT_SLOT_NUM:
				return

			if not self.__CheckItem(player.GetItemIndex(attachedSlotPos), slot_num):
				return

			net.SendChatPacket("/sash_register_system_absorption %d %d" % (slot_num, attachedSlotPos))
		else:
			net.SendChatPacket("/sash_register_system_absorption %d %d" % (slot_num, -1))

	def	__OverInItem(self, slot_num):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()

			if self.ITEM_LIST[slot_num]["VNUM"] > 0:
				if slot_num != self.RESULT_SLOT_NUM:
					self.tooltipItem.SetInventoryItem(self.ITEM_LIST[slot_num]["SLOT"])
				else:
					## Fetching sockets
					metinSlot = [player.GetItemMetinSocket(self.ITEM_LIST[self.ITEM_SLOT_NUM]["SLOT"], i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]

					## Set the absorption rate
					metinSlot[player.SASH_TYPE_SOCKET] = player.GetItemMetinSocket(self.ITEM_LIST[self.BASE_SLOT_NUM]["SLOT"], player.SASH_TYPE_SOCKET)

					if self.ITEM_LIST[self.ITEM_SLOT_NUM]["SLOT"] > -1:
						## Fetching attrs
						attrSlot = [player.GetItemAttribute(self.ITEM_LIST[self.ITEM_SLOT_NUM]["SLOT"], i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

						## Visualisation of further item
						metinSlot[player.SASH_ABSORPTION_SOCKET] = self.ITEM_LIST[self.ITEM_SLOT_NUM]["VNUM"]
					else:
						## Fetching attrs
						attrSlot = [(0, 0) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

					self.tooltipItem.AddItemData(self.ITEM_LIST[slot_num]["VNUM"], metinSlot, attrSlot)

	def	__OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def	__StartProcess(self, arg = False):
		if not arg:
			for v in self.ITEM_LIST.itervalues():
				if v["VNUM"] <= 0:
					return

			self.questionDialog.SetText("localeInfo.SASH_SYSTEM_ABSORPTION_TEXT")
			self.questionDialog.SetAcceptEvent(lambda arg = True: self.__StartProcess(arg))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__CloseDialog))
			self.questionDialog.Open()
		else:
			net.SendChatPacket("/process_sash_system_absorption")
			self.__CloseDialog()

	def	__CloseDialog(self):
		self.questionDialog.Close()

	def	__CheckItem(self, vnum, slot_num):
		item.SelectItem(vnum)

		if slot_num == self.BASE_SLOT_NUM:
			return (item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_SASH)
		elif slot_num == self.ITEM_SLOT_NUM:
			if (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() in (item.WEAPON_ARROW, item.WEAPON_QUIVER)):
				return False

			return item.GetItemType() == item.ITEM_TYPE_WEAPON
		else:
			return False

	def AutoPutItem(self, iSlot):
		for k, v in self.ITEM_LIST.items():
			if k == self.RESULT_SLOT_NUM:
				return False

			if v['VNUM'] <= 0:
				if self.__CheckItem(player.GetItemIndex(iSlot), k):
					net.SendChatPacket("/sash_register_system_absorption %d %d" % (k, iSlot))
					return True

		return False

	def	Close(self):
		self.Clear()
		net.SendChatPacket("/sash_system_cancel")
		self.Hide()

		global IS_OPEN_ABSORPTION
		IS_OPEN_ABSORPTION = False

	def	Open(self):
		self.Refresh()
		self.SetCenterPosition()
		self.Show()

		global IS_OPEN_ABSORPTION
		IS_OPEN_ABSORPTION = True

	def	UpdateWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.Open()

