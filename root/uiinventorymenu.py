import ui

class InventoryMenuWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.isLoaded = 0

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def BindInterfaceClass(self, interface):
		from _weakref import proxy
		self.interface = proxy(interface)

	def Destroy(self):
		self.ClearDictionary()

		self.interface = None

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

		self.isLoaded = 0

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/inventorymenu.py")
		except:
			import exception
			exception.Abort("InventoryMenuWindow.LoadWindow.LoadObject")

		try:
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))

			self.SafeBoxButton = self.GetChild("SafeBox")
			self.ItemShopButton = self.GetChild("ItemShop")

			self.lStorageType = []
			for _ in range(4):
				self.lStorageType.append(self.GetChild("INVENTORY_MENU_STORAGE_0%d" % (_+1)))

			self.SafeBoxButton.SetEvent(ui.__mem_func__(self.__OnClickSafeBoxButton))
			self.ItemShopButton.SetEvent(ui.__mem_func__(self.__OnClickItemShopButton))

			for iKey, rValue in enumerate(self.lStorageType):
				rValue.SAFE_SetEvent(self.ClickSpecialStorage, iKey)

		except:
			import exception
			exception.Abort("InventoryMenuWindow.__LoadWindow.BindObject")

	def __OnClickSafeBoxButton(self):
		self.interface.AskSafeboxPassword()
		self.Close()

	def __OnClickItemShopButton(self):
		self.interface.AskMallPassword()
		self.Close()

	def ClickSpecialStorage(self, arg):
		self.interface.ToggleSpecialStorageWindow(arg)
		self.Close()

	def OnPressEscapeKey(self):
		self.Close()
		return True
