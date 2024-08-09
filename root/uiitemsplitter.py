import ui
import player
import item
import wndMgr
import dbg
import math

class ItemSplitter(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.LoadDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.OBJECTS = {}
		self.eventAccept = None
		self.itemIndex, self.itemCount = 0, 0

	def Destroy(self):
		self.ClearDictionary()
		self.__Initialize()

	def LoadDialog(self):
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/item_splitter.py")

		except KeyError, msg:
			dbg.TraceError("ItemSplitter #1")

		try:
			self.__BindObjects()

		except KeyError, msg:
			dbg.TraceError("ItemSplitter #2 - %s" % str(msg))

		try:
			self.__BindEvents()

		except KeyError, msg:
			dbg.TraceError("ItemSplitter #3 - %s" % str(msg))

	def __BindObjects(self):
		GetObject = self.GetChild
		self.OBJECTS["BOARD"] = GetObject("Board")

		self.OBJECTS["SLOT"] = GetObject("Slot_0")
		self.OBJECTS["PACKAGES"] = GetObject("ValueOuter")
		self.OBJECTS["VALUES"] = [GetObject("Value_%d" % (i)) for i in xrange(2)]

		self.OBJECTS["ACCEPT"] = GetObject("accept_button")
		self.OBJECTS["CANCEL"] = GetObject("cancel_button")

	def __BindEvents(self):
		self.OBJECTS["BOARD"].SetCloseEvent(self.Close)

		self.OBJECTS["VALUES"][0].SetReturnEvent(self.OBJECTS["VALUES"][1].SetFocus())
		self.OBJECTS["VALUES"][0].SetTabEvent(self.OBJECTS["VALUES"][1].SetFocus())
		self.OBJECTS["VALUES"][0].OnIMEUpdate = ui.__mem_func__(self.OnCountUpdate)

		self.OBJECTS["VALUES"][1].SetReturnEvent(self.AcceptEvent)
		self.OBJECTS["VALUES"][1].OnIMEUpdate = ui.__mem_func__(self.OnPackageUpdate)

		self.OBJECTS["ACCEPT"].SetEvent(self.AcceptEvent)
		self.OBJECTS["CANCEL"].SetEvent(self.CloseEvent)

	def GetCountValue(self, returnAdjustValue = True):
		if not self.OBJECTS["VALUES"] or\
			(self.OBJECTS["VALUES"] and not self.OBJECTS["VALUES"][0].GetText().isdigit()):
			return 0
		
		_value = int(self.OBJECTS["VALUES"][0].GetText())
		return (min(_value, self.itemCount) if returnAdjustValue is True else _value)

	def OnCountUpdate(self):
		ui.EditLine.OnIMEUpdate(self.OBJECTS["VALUES"][0])

		iQuanity = self.GetCountValue(True)
		self.OBJECTS["SLOT"].SetItemSlot(0, self.itemIndex, iQuanity)

		iQuanity = self.GetCountValue(False)

		if iQuanity > self.itemCount:
			self.OBJECTS["VALUES"][0].SetText(str(self.itemCount))

	def GetPackagesValue(self):
		if not self.OBJECTS["VALUES"] or\
			(self.OBJECTS["VALUES"] and not self.OBJECTS["VALUES"][1].GetText().isdigit()):
			return 0

		return (int(self.OBJECTS["VALUES"][1].GetText()))

	def OnPackageUpdate(self):
		ui.EditLine.OnIMEUpdate(self.OBJECTS["VALUES"][1])

		iQuanity = self.GetCountValue(False)
		_value = self.GetPackagesValue()

		if iQuanity * _value > self.itemCount:
			mVal = int(math.ceil(self.itemCount / iQuanity))

			self.OBJECTS["VALUES"][1].SetText(str(mVal))
			self.OBJECTS["PACKAGES"].SetText(str(mVal))
		else:
			self.OBJECTS["PACKAGES"].SetText(str(_value))

	def SetAcceptEvent(self, event):
		self.eventAccept = event

	def AcceptEvent(self):
		value = 0L

		try:
			value = long(self.OBJECTS["VALUES"][1].GetText())
		except (KeyError, ValueError, ):
			value = 0L
		
		if self.eventAccept:
			self.eventAccept(self.GetPackagesValue() > 1, self.GetCountValue(False), value)

		self.Close()

	def CloseEvent(self):
		self.Close()

	def AddItem(self, slotIndex):
		self.itemIndex = player.GetItemIndex(slotIndex)
		self.itemCount = player.GetItemCount(slotIndex)

		item.SelectItem(self.itemIndex)

		self.OBJECTS["BOARD"].SetTitleName(item.GetItemName())
		self.OBJECTS["SLOT"].SetItemSlot(0, self.itemIndex, 1)

		self.OBJECTS["PACKAGES"].SetText(str(self.itemCount))

	def Open(self):
		width = self.GetWidth()
		(mouseX, mouseY) = wndMgr.GetMousePosition()

		if mouseX + width / 2 > wndMgr.GetScreenWidth():
			xPos = wndMgr.GetScreenWidth() - width
		elif mouseX - width / 2 < 0:
			xPos = 0
		else:
			xPos = mouseX - width / 2

		self.SetPosition(xPos, mouseY - self.GetHeight() - 20)

		self.OBJECTS["VALUES"][0].SetText(str(1))
		self.OBJECTS["VALUES"][0].SetFocus()

		self.OBJECTS["VALUES"][1].SetText(str(1))
		self.OBJECTS["PACKAGES"].SetText(str(1))

		# self.OBJECTS["SLOT_DATA"][1].SetText("1x")

		self.Show()
		self.SetTop()

	def Close(self):
		self.OBJECTS["VALUES"][0].KillFocus()
		self.OBJECTS["VALUES"][1].KillFocus()

		for i in xrange(2):
			self.OBJECTS["VALUES"][i].SetText("")

		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
