import ui
import app
import net
import chat
import wndMgr
import datetime
import exception
import localeInfo

from _weakref import proxy

DEFAULT_COLOUR = 0xffffffff
ENABLE_COLOUR = 0xff00FF00
DISABLE_COLOUR = 0xffFF0000
SUSPECTED_COLOUR = 0xff00FFFF

class GMIdlePanel(ui.ScriptWindow):
	STATUS_COLOURS = (DISABLE_COLOUR, ENABLE_COLOUR, SUSPECTED_COLOUR)

	class PlayerInfo(ui.ListBoxEx.Item):
		def __init__(self):
			ui.ListBoxEx.Item.__init__(self)
			self.parent = None
			self.textBox = ui.TextLine()
			self.textBox.SetParent(self)

		def __del__(self):
			ui.ListBoxEx.Item.__del__(self)

		def SetParent(self, parent):
			ui.ListBoxEx.Item.SetParent(self, parent)
			self.parent = proxy(parent)

		def	GetText(self):
			return self.textBox.GetText()

		def	SetText(self, text, colour = DEFAULT_COLOUR):
			self.textBox.SetText(text)
			self.textBox.SetPackedFontColor(colour)
			self.textBox.Show()

		def OnMouseLeftButtonDown(self):
			return

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.listCounter = 0
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.listCounter = 0
		self.MessageSentText = None
		self.PlayerList = None
		self.ButtonClear = None
		self.ButtonSend = None

	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/GMIdlePanel.py")
		except:
			exception.Abort("GMIdlePanel.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild
			self.GetChild("Board").SetCloseEvent(ui.__mem_func__(self.Close))

			self.MessageSentText = GetObject("MessageSent_Text")
			self.PlayerList = GetObject("PlayerList_ListBox")
			self.PlayerList.SetScrollBar(self.GetChild("PlayerList_ScrollBar"))
			self.PlayerList.SetViewItemCount(14)
			self.ButtonClear = GetObject("PlayerList_ClearButton")
			self.ButtonSend = GetObject("PlayerList_SendButton")

			## Binding
			self.ButtonClear.SAFE_SetEvent(self.__ClearRecords)
			self.ButtonSend.SAFE_SetEvent(self.__SendNotification)

		except:
			exception.Abort("GMIdlePanel.LoadDialog.BindObject")

		self.SetCenterPosition()
		self.SetTop()
		self.Hide()

	## Recv
	def	UpdateCollectionCount(self, count):
		self.listCounter = count
		if count > 0:
			## Updating last date field
			self.MessageSentText.SetText(datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))

	def	UpdateAllPlayerStatus(self, status):
		for element in self.PlayerList.itemList:
			element.SetText(element.GetText(), self.STATUS_COLOURS[status])

	def	AddNewPlayer(self, p_name):
		self.listCounter -= 1
		new_player = self.PlayerInfo()
		new_player.SetText(p_name)
		self.PlayerList.AppendItem(new_player)

	def	UpdatePlayerStatus(self, p_name, status):
		for element in self.PlayerList.itemList:
			if element.GetText() == p_name:
				element.SetText(p_name, self.STATUS_COLOURS[status])
				return

	def	ErasePlayer(self, p_name):
		try:
			self.PlayerList.RemoveItem(p_name)
		except:
			return

	def	__ClearRecords(self):
		## Clearing interface
		self.PlayerList.RemoveAllItems()

		## Requesting Update
		self.listCounter = -1
		net.SendChatPacket("/notification_sender_request_list")

	def	__SendNotification(self):
		if self.listCounter != 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GM_IDLE_INTERFACE_EMPTY_LIST)
			return

		if self.PlayerList.IsEmpty():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GM_IDLE_INTERFACE_EMPTY_LIST1)
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GM_IDLE_INTERFACE_EMPTY_LIST2)
			return

		net.SendChatPacket("/notification_sender_send")

	def	Close(self):
		self.Hide()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.Show()

class IdlePanelAnswer(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.AcceptButton = None

	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/IdlePanelAnswer.py")
		except:
			exception.Abort("IdlePanelAnswer.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild
			self.GetChild("Board").SetCloseEvent(ui.__mem_func__(self.Close))
			self.AcceptButton = GetObject("AcceptButton")

			self.AcceptButton.SAFE_SetEvent(self.__SendNotification)
		except:
			exception.Abort("IdlePanelAnswer.LoadDialog.BindObject")

	def	__SendNotification(self):
		net.SendChatPacket("/notification_answer")
		self.Close()

	def	SetRandomPosition(self):
		## Setting constraints
		(x_max, y_max) = wndMgr.GetScreenWidth()-self.GetWidth()-100, wndMgr.GetScreenHeight()-self.GetHeight()-100
		self.SetPosition(app.GetRandom(0, x_max), app.GetRandom(0, y_max))

	def	Close(self):
		self.Hide()

	def	Open(self):
		self.SetRandomPosition()
		self.SetTop()
		self.Show()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.Open()

