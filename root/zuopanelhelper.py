import ui
from _weakref import proxy
import wndMgr
import item

class ZuoPanelHelper(ui.ScriptWindow):

	MAX_SLOT_SIZE = 10
	BOARD_BASE_X = 200
	BOARD_BASE_Y = 100

	class ListBoxItem(ui.ListBoxEx.Item):
		def __init__(self):
			ui.ListBoxEx.Item.__init__(self)
			self.parent = None
			self.textBox = ui.TextLine()
			self.textBox.SetParent(self)

		def SetParent(self, parent):
			ui.ListBoxEx.Item.SetParent(self, parent)
			self.parent = proxy(parent)

		def __del__(self):
			ui.ListBoxEx.Item.__del__(self)

		def	GetText(self):
			return self.textBox.GetText()

		def OnRender(self):
			x, y = wndMgr.GetMousePosition()
			mx, my = self.GetGlobalPosition()
			if (x >= mx and x <= mx+self.GetWidth()) and (y >= my and y <= my+self.GetHeight()):
				self.OnSelectedRender()

		def	SetText(self, text):
			self.textBox.SetText(text)
			self.textBox.Show()

		def OnMouseLeftButtonDown(self):
			if self.parent:
				self.parent.SelectItem(self)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()
		self.ListBox = None
		self.Thin = None
		self.Item_List = {}

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()

		self.ListBox = None
		self.board = None
		self.ItemName_SlotBar = None

	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/ZuoPanelHelper.py")
		except:
			import exception
			exception.Abort("OfflineShopDialogSearcher.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild
			self.board = GetObject("board")
			self.ItemName = GetObject("ItemName")
			self.ItemName_SlotBar = GetObject("ItemName_SlotBar")

		except:
			import exception
			exception.Abort("OfflineShopDialogSearcher.LoadDialog.BindObject")

		self.board.SetCloseEvent(ui.__mem_func__(self.Hide))

		self.ItemName.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)

	def	CreateListBox(self):
		self.Item_List = {}
		## ListBox
		self.Thin = ui.SlotBar()
		self.Thin.SetParent(self)
		self.Thin.SetWindowHorizontalAlignCenter()
		self.Thin.SetSize(150, 15)

		self.ListBox = ui.ListBoxEx()
		self.ListBox.SetParent(self.Thin)
		self.ListBox.SetPosition(3, 0)
		self.ListBox.SetItemSize(130, 15)
		self.ListBox.SetItemStep(15)
		self.ListBox.SetSelectEvent(lambda empty_arg: self.Search(empty_arg))

		## Fetching Items by Name
		if self.ItemName.GetText() != "":
			item.GetItemsByName(self.ItemName.GetText())
		else:
			self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)
			return

		if len(self.Item_List) == 0:
			self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)
			return
		else:
			self.Item_List = collections.OrderedDict(sorted(self.Item_List.items(), key = lambda x: x[1]))

		self.ListBox.SetViewItemCount(min(len(self.Item_List), self.MAX_SLOT_SIZE))
		self.ListBox.UpdateSize()
		self.Thin.SetSize(self.Thin.GetWidth(), self.ListBox.GetHeight())

		## Adding Items to the ListBox
		for i in self.Item_List.iterkeys():
			line = self.ListBoxItem()
			line.SetText(i)
			self.ListBox.AppendItem(line)

		## Reseting Board Size
		self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)

		x, y = self.ItemName_SlotBar.GetLocalPosition()
		y += 17
		self.Thin.SetPosition(0, y)

		## Creating ScrollBar
		if len(self.Item_List) > self.MAX_SLOT_SIZE:
			self.ScrollBar = ui.ScrollBar()
			self.ScrollBar.SetParent(self.Thin)
			self.ScrollBar.SetPosition(self.Thin.GetWidth()-14, 5)
			self.ListBox.SetScrollBar(self.ScrollBar)

			## Setting Size
			self.ScrollBar.SetScrollBarSize(self.ListBox.GetHeight()-10)

			## ScrollBar Wheel Support
			self.SetScrollWheelEvent(self.ScrollBar.OnWheelMove)

		## Resizing board
		if (y+self.ListBox.GetHeight()) > self.BOARD_BASE_Y:
			self.UpdateSize(self.BOARD_BASE_X, y+self.ListBox.GetHeight()+5)

		self.Thin.Show()
		self.ListBox.Show()
		if len(self.Item_List) > self.MAX_SLOT_SIZE:
			self.ScrollBar.Show()

	def	Search(self, empty_arg):
		if self.ListBox != None:
			selitem = self.ListBox.GetSelectedItem()
			if selitem.GetText() in self.Item_List:
				net.SendChatPacket("/offlineshop_search %d" % (self.Item_List[selitem.GetText()]))

				## Updating highlighted item
				global OFFLINESHOP_SEARCH_VNUM
				OFFLINESHOP_SEARCH_VNUM = self.Item_List[selitem.GetText()]

		self.Clear()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.ItemName)
		self.CreateListBox()

	def	AddItemName(self, name, vnum):
		self.Item_List[name] = vnum

	def	Clear(self):
		self.ItemName.SetText("")
		self.Item_List = {}
		if self.ListBox != None:
			self.ListBox.Hide()
			self.ListBox = None
		if self.Thin != None:
			self.Thin.Hide()
			self.Thin = None

		self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)

	def	UpdateSize(self, x, y):
		self.SetSize(x, y)
		self.board.SetSize(x, y)

	def	Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def	UpdateWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.Clear()
			self.Show()
			self.ItemName.SetFocus()