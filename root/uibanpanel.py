import ui
import net
import chat

class BanPanel(ui.ScriptWindow):

	OPTIONS_NAMES = {
						0 : "PERM_BAN",
						1 : "IP_BAN",
						2 : "TIME_BAN",
						3 : "UNBAN",
						4 : "HARDWARE_BAN",
					}

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.RadioButtons = {}
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.RadioButtons = None
		self.NickName = None
		self.BanReason = None
		self.BanTime = None
		self.ButtonAccept = None

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/ban_panel.py")
		except:
			import exception
			exception.Abort("BanPanel.__LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			self.NickName = self.GetChild("NickNameEditLine")
			self.BanReason = self.GetChild("BanReasonEditLine")
			self.BanTime = self.GetChild("BanTimeEditLine")
			self.ButtonAccept = self.GetChild("ButtonAccept")

			for i in xrange(len(self.OPTIONS_NAMES)):
				self.RadioButtons[i] = (self.GetChild("ButtonOption%d" % (i+1)))
				self.RadioButtons[i].SAFE_SetEvent(self.__ChangeOption, i)

			self.ButtonAccept.SAFE_SetEvent(self.__PerformAction)

			self.NickName.SetReturnEvent(ui.__mem_func__(self.BanReason.SetFocus))
			self.NickName.SetTabEvent(ui.__mem_func__(self.BanReason.SetFocus))
			self.BanReason.SetReturnEvent(ui.__mem_func__(self.BanTime.SetFocus))
			self.BanReason.SetTabEvent(ui.__mem_func__(self.BanTime.SetFocus))
			self.BanTime.SetReturnEvent(ui.__mem_func__(self.NickName.SetFocus))
			self.BanTime.SetTabEvent(ui.__mem_func__(self.NickName.SetFocus))

			self.__ChangeOption(0)
			self.SetCenterPosition()
			self.Hide()
		except:
			import exception
			exception.Abort("BanPanel.__LoadWindow.BindObject")

	def	__ChangeOption(self, arg):
		self.cur_option = arg

		for id, but in self.RadioButtons.iteritems():
			if id == arg:
				self.RadioButtons[id].Down()
			else:
				self.RadioButtons[id].SetUp()

	def	__PerformAction(self):
		nickName = ""
		banReason = ""
		banTime = ""
		optionName = self.OPTIONS_NAMES[self.cur_option]

		nickName = self.NickName.GetText()
		if len(nickName) < 1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Nie podano nicku.")
			return

		if optionName != "UNBAN":
			banReason = self.BanReason.GetText()
			if len(banReason) < 1:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Nie podano powodu bana.")
				return

		if optionName == "TIME_BAN":
			banTime = self.BanTime.GetText()
			if len(banTime) < 1:
				chat.AppendChat(chat.CHAT_TYPE_INFO, "Nie podano czasu bana.")
				return

		if optionName in ("PERM_BAN", "IP_BAN", "HARDWARE_BAN"):
			net.SendChatPacket("/gm_ban %s %d %s" % (nickName, (self.cur_option+1), banReason.replace(" ", "|")))
		elif optionName == "TIME_BAN":
			net.SendChatPacket("/gm_ban %s %d %s %s" % (nickName, (self.cur_option+1), banReason.replace(" ", "|"), banTime))
		elif optionName == "UNBAN":
			net.SendChatPacket("/gm_ban %s %d" % (nickName, (self.cur_option+1)))

	def	Open(self):
		self.Show()
		self.SetTop()

	def	Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return TRUE

	def	UpdateWindow(self):
		if self.IsShow():
			self.Show()
		else:
			self.Hide()

