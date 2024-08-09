import ui
import player
import item
import uiToolTip

class DiscardItemWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__slot = -1
		self.__window = -1
		self.itemToolTip = uiToolTip.ItemToolTip()

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/discarditemwindow.py")
		except:
			import exception
			exception.Abort("DiscardItemWindow.__LoadWindow.LoadScript")

		self.board = self.GetChild("Board")
		self.wndItem = self.GetChild("ItemSlot0")
		self.wndItemWindow = self.GetChild("ItemWindowTop0")
		self.itemName = self.GetChild("ItemNameText0")
		self.dropButton = self.GetChild("DropBtn")
		self.destroyButton = self.GetChild("DestroyBtn")
		self.cancelButton = self.GetChild("CancelBtn")

	def SetItemSlot(self, slot, window):
		self.__slot = slot
		self.__window = window

		itemVnum = player.GetItemIndex(window, slot)
		itemCount = player.GetItemCount(window, slot)
		item.SelectItem(itemVnum)
		w, h = item.GetItemSize()

		self.wndItem.SetItemSlot(0, itemVnum, 0 if itemCount == 1 else itemCount)
		self.wndItem.SetPosition((self.wndItemWindow.GetWidth() - 32 * w)/2, (self.wndItemWindow.GetHeight() - h * 32)/2)

		self.board.SetTitleName(item.GetItemName())
		self.itemName.SetText(item.GetItemName())

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_DROP):
			self.dropButton.Disable()

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_DESTROY):
			self.destroyButton.Disable()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(self.__slot, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(self.__slot, i))

		# self.itemToolTip.SetItemToolTip(itemVnum)
		self.itemToolTip.AddItemData(itemVnum, metinSlot, attrSlot, bShowIcon = True)
		self.itemToolTip.HideToolTip()

		self.dropButton.SetToolTipWindow(self.itemToolTip)
		self.destroyButton.SetToolTipWindow(self.itemToolTip)

	def SetCloseEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)

	def SetDropEvent(self, event):
		self.dropButton.SetEvent(event)

	def SetDestroyEvent(self, event):
		self.destroyButton.SetEvent(event)

	def Open(self):
		self.SetCenterPosition()
		self.Show()

	def Close(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()

		self.Hide()
