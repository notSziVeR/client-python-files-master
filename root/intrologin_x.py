#-*- coding: iso-8859-1 -*-
import locale
from threading import local
import ui
import net
import snd
import musicInfo
import wndMgr
import localeInfo
import systemSetting

import ime
import app

import introInterface
import constInfo

import uiToolTip

from cff import CFF

if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "check_channel"):
	import ServerStateChecker

class LoginWindow(ui.ScriptWindow):
	def __init__(self, stream):
		super(LoginWindow, self).__init__()

		net.SetPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(self)

		(self.Objects, self.Languages) = ({}, {})
		self.stream = stream
		self.ToolTip = None

	def __del__(self):
		net.ClearPhaseWindow(net.PHASE_WINDOW_LOGIN, self)
		net.SetAccountConnectorHandler(0)

		(self.Objects, self.Languages) = ({}, {})
		super(LoginWindow, self).__del__()

	def Open(self):
		self.loginFailureMsgDict={

			"ALREADY"	: localeInfo.LOGIN_FAILURE_ALREAY,
			"NOID"		: localeInfo.LOGIN_FAILURE_NOT_EXIST_ID,
			"WRONGPWD"	: localeInfo.LOGIN_FAILURE_WRONG_PASSWORD,
			"FULL"		: localeInfo.LOGIN_FAILURE_TOO_MANY_USER,
			"SHUTDOWN"	: localeInfo.LOGIN_FAILURE_SHUTDOWN,
			"REPAIR"	: localeInfo.LOGIN_FAILURE_REPAIR_ID,
			"BLOCK"		: localeInfo.LOGIN_FAILURE_BLOCK_ID,
			"WRONGMAT"	: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER,
			"QUIT"		: localeInfo.LOGIN_FAILURE_WRONG_MATRIX_CARD_NUMBER_TRIPLE,
			"BESAMEKEY"	: localeInfo.LOGIN_FAILURE_BE_SAME_KEY,
			"NOTAVAIL"	: localeInfo.LOGIN_FAILURE_NOT_AVAIL,
			"NOBILL"	: localeInfo.LOGIN_FAILURE_NOBILL,
			"BLKLOGIN"	: localeInfo.LOGIN_FAILURE_BLOCK_LOGIN,
			"WEBBLK"	: localeInfo.LOGIN_FAILURE_WEB_BLOCK,
			"BADSCLID"	: localeInfo.LOGIN_FAILURE_WRONG_SOCIALID,
			"AGELIMIT"	: localeInfo.LOGIN_FAILURE_SHUTDOWN_TIME,

			"VERSION"	: localeInfo.LOGIN_FAILURE_VERSION,
			"INVALID"	: localeInfo.LOGIN_FAILURE_INVALID,
			"HARDBAN"	: localeInfo.LOGIN_FAILURE_HARDWAREBAN,
		}

		if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
			self.loginFailureMsgDict.update({"WRONGPIN" : "localeInfo.LOGIN_FAILURE_WRONG_PIN"})

		self.loginFailureFuncDict = {
			"QUIT"		: app.Exit,
		}

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("LoginWindow")

		self.__LoadScript("uiscript/loginwindow_sano.py")

		if musicInfo.loginMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/" + musicInfo.loginMusic)

		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		ime.AddExceptKey(91)
		ime.AddExceptKey(93)

		if introInterface.GetWindowConfig("save_info", "account"):
			data = introInterface.RegistryHandle.Instance().GetRegistryValue("account")
			if data:
				self.Objects["Remember"].SetChecked(True)

			if self.Objects["Remember"].IsChecked():
				data = data.split("|", 1)

				self.Objects["ID_EditLine"].SetText(data[0])
				self.Objects["PWD_EditLine"].SetText(data[1])
				if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
					if introInterface.GetWindowConfig("save_info", "pin"):
						self.Objects["PIN_EditLine"].SetText(data[2])
						self.__FocusPin()
						self.Objects["PIN_EditLine"].SetEndPosition()
				else:
					self.__FocusPassword()
					self.Objects["PWD_EditLine"].SetEndPosition()

		if introInterface.GetWindowConfig("save_info", "channel"):
			channelID = introInterface.RegistryHandle.Instance().GetRegistryValue("channel")
			if type(channelID) != bool:
				self.__SetChannelData(int(channelID))
			else:
				self.__SetChannelData(0)
		else:
			self.__SetChannelData(0)

		if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "check_channel"):
			self.__CreateServerStateChecker()

		self.CreateAccount()

		self.Show()

		app.ShowCursor()

	def Close(self):
		if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "check_channel"):
			ServerStateChecker.Initialize(self)

		if len(musicInfo.loginMusic) != 0 and len(musicInfo.selectMusic) != 0:
			snd.FadeOutMusic("BGM/" + musicInfo.loginMusic)

		if self.stream.popupWindow:
			self.stream.popupWindow.Close()

		if self.Objects["ID_EditLine"]:
			self.Objects["ID_EditLine"].KillFocus()
		if self.Objects["PWD_EditLine"]:
			self.Objects["PWD_EditLine"].KillFocus()

		if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
			if self.Objects["PIN_EditLine"]:
				self.Objects["PIN_EditLine"].KillFocus()

		introInterface.AccountHandle.Instance().SaveToRegistry()

		self.ClearDictionary()
		self.Hide()

		ime.ClearExceptKey()

	def OnConnectFailure(self):
		snd.PlaySound("sound/ui/loginfail.wav")
		self.PopupNotifyMessage(localeInfo.LOGIN_CONNECT_FAILURE, lambda *args: None)

	def OnHandShake(self):
		snd.PlaySound("sound/ui/loginok.wav")
		self.PopupDisplayMessage(localeInfo.LOGIN_CONNECT_SUCCESS)

	def OnLoginStart(self):
		self.PopupDisplayMessage(localeInfo.LOGIN_PROCESSING)

	def OnLoginFailure(self, error, errorValue, ban_reason):
		try:
			loginFailureMsg = self.loginFailureMsgDict[error]
		except KeyError:
			loginFailureMsg = localeInfo.LOGIN_FAILURE_UNKNOWN + error

		loginFailureFunc = self.loginFailureFuncDict.get(error, self.EmptyFunc)

		if loginFailureMsg.find("%d") >= 0:
			loginFailureMsg = loginFailureMsg % errorValue
		elif loginFailureMsg.find("%s") >= 0:
			loginFailureMsg = loginFailureMsg % localeInfo.SecondToDHMS(errorValue)

		self.PopupNotifyMessage(loginFailureMsg, loginFailureFunc, ban_reason = ban_reason)

		snd.PlaySound("sound/ui/loginfail.wav")

	def EmptyFunc(self):
		pass

	def __LoadScript(self, fileName):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, fileName)
		except Exception:
			import exception
			exception.Abort("LoginWindow.__LoadScript.LoadObject")
		try:
			GetObject = self.GetChild

			self.Objects["ID_EditLine"]  = GetObject("ID_EditLine")
			self.Objects["PWD_EditLine"] = GetObject("PWD_EditLine")

			if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
				self.Objects["PIN_EditLine"]	= GetObject("PIN_EditLine")

			self.Objects["Remember"]     = GetObject("Remember")
			self.Objects["LoginButton"]  = GetObject("LoginButton")
			self.Objects["Channels"]     = [GetObject("Channel%d" % i) for i in range(len(introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "server")))]

			self.Objects["RecoveryPassword"] = GetObject("RecoveryPassword")
			accountMax          = introInterface.GetWindowConfig("lenght_data", "account")
			self.accountObjects = {}
			for i in xrange(accountMax):
				self.accountObjects[i] = [GetObject("account_name_%d" % i), GetObject("account_button_save_%d" % i), GetObject("account_button_delete_%d" % i), GetObject("account_button_load_%d" % i)]

			# self.Objects["ExitButton"]   = GetObject("ExitButton")

			for lIndex in xrange(app.LANGUAGE_MAX_NUM):
				lShort = app.GetLanguageByID(lIndex, True)
				self.Languages.update({lIndex : ui.MakeButton(GetObject("LanguageSpace"), 30 + (lIndex * (44 + 4)), (GetObject("LanguageSpace").GetHeight() - 25) / 2 , "",\
					"assets/ui/login/languages/", "{}_norm.png".format(lShort), "{}_down.png".format(lShort), "{}_down.png".format(lShort))})

			# self.advise_render_window = GetObject("render_window")
			# self.advise_render_window.SetInsideRender(True)

			# self.advise_text = GetObject("advise_text")
			# self.advise_text.SetPosition(self.advise_render_window.GetWidth() + 5, -1)
			# self.advise_text_size = self.advise_text.GetTextSize()[0]

		except Exception:
			import exception
			exception.Abort("LoginWindow.__LoadScript.BindObject")

		self.Objects["ID_EditLine"].SetReturnEvent(self.__FocusPassword)
		self.Objects["ID_EditLine"].SetTabEvent(self.__FocusPassword)

		if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
			self.Objects["PWD_EditLine"].SetReturnEvent(ui.__mem_func__(self.__FocusPin))
			self.Objects["PWD_EditLine"].SetTabEvent(self.__FocusPin)
		else:
			self.Objects["PWD_EditLine"].SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
			self.Objects["PWD_EditLine"].SetTabEvent(self.__FocusLogin)

		if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
			self.Objects["PWD_EditLine"].SetReturnEvent(ui.__mem_func__(self.__OnClickLoginButton))
			self.Objects["PIN_EditLine"].SetTabEvent(self.__FocusLogin)

		self.Objects["Remember"].SAFE_SetEvent(self.__rememberData)
		# self.Objects["Remember"].SAFE_SetOverInData("Zaznacz aby zapamiêtaæ ostatnie zalogowane konto.")

		self.__FocusLogin()

		accountMax          = introInterface.GetWindowConfig("lenght_data", "account")

		self.ToolTip = uiToolTip.ToolTip()
		self.ToolTip.ClearToolTip()

		for i in xrange(accountMax):
			self.accountObjects[i][1].SAFE_SetEvent(self.__OnAccountButtonEvent, "save", i)
			self.accountObjects[i][1].SetOverEvent(ui.__mem_func__(self.__CreateToolTip), CFF.format(localeInfo.LOGIN_TOOLTIP_ACCOUNT_SAVE, "#ffdda9") +  " " + CFF.format(localeInfo.LOGIN_TOOLTIP_ACCOUNT_PRESS, "#ffffff") + CFF.format("SHIFT + F{}".format(i + 1), "#ffdda9"))
			self.accountObjects[i][2].SetOverEvent(ui.__mem_func__(self.__CreateToolTip), CFF.format(localeInfo.LOGIN_TOOLTIP_ACCOUNT_DELETE, "#ffdda9") + " " + CFF.format(localeInfo.LOGIN_TOOLTIP_ACCOUNT_PRESS, "#ffffff") + CFF.format("SHIFT + F{}".format(i + 1), "#ffdda9"))
			self.accountObjects[i][3].SetOverEvent(ui.__mem_func__(self.__CreateToolTip), CFF.format(localeInfo.LOGIN_TOOLTIP_ACCOUNT_LOAD, "#ffdda9") + " " + CFF.format(localeInfo.LOGIN_TOOLTIP_ACCOUNT_PRESS, "#ffffff") + CFF.format("F{}".format(i + 1), "#ffdda9"))

			self.accountObjects[i][1].SetOverOutEvent(ui.__mem_func__(self.__HideToolTip))
			self.accountObjects[i][2].SetOverOutEvent(ui.__mem_func__(self.__HideToolTip))
			self.accountObjects[i][3].SetOverOutEvent(ui.__mem_func__(self.__HideToolTip))

		self.Objects["LoginButton"].SAFE_SetEvent(self.__OnClickLoginButton)
		for button in self.Objects["Channels"]:
			button.SAFE_SetEvent(self.__SetChannelData, self.Objects["Channels"].index(button))
			iFit = self.Objects["Channels"].index(button) + 1
			button.ShowToolTip = lambda arg = CFF.format("Channel", "#ffdda9") + CFF.format(localeInfo.LOGIN_TOOLTIP_ACCOUNT_PRESS, "#ffffff") + CFF.format("CTRL + F{}".format(iFit), "#ffdda9"): self.__CreateToolTip(arg)
			button.HideToolTip = lambda arg = None: self.__HideToolTip()

		[self.Languages[key].SetEvent(ui.__mem_func__(self.__ChangeLanguage), key) for key in self.Languages.keys()]
		[self.Languages[key].SetOverEvent(ui.__mem_func__(self.__CreateToolTip), app.GetLanguageByID(key, False), 0, -20) for key in self.Languages.keys()]
		[self.Languages[key].SetOverOutEvent(ui.__mem_func__(self.__HideToolTip)) for key in self.Languages.keys()]

		self.Objects["RecoveryPassword"].SetEvent(ui.__mem_func__(self.__RecoveryPassword))
		# self.Objects["ExitButton"].SAFE_SetEvent(self.OnPressExitKey)

		self.__RefreshLanguageList()

	def __CreateToolTip(self, type, xFill = 0, yFill = 0):
		(pos_x, pos_y) = wndMgr.GetMousePosition()

		arglen = len(str(type))

		self.ToolTip.ClearToolTip()
		# self.ToolTip.SetThinBoardSize(5 * arglen)
		self.ToolTip.SetToolTipPosition(pos_x + xFill, pos_y + yFill)
		self.ToolTip.AppendTextLine(getattr(localeInfo, "LANGUAGE_NAME_{}".format(type), type), 0xFFffffff)
		self.ToolTip.Show()

	def __HideToolTip(self):
		if self.ToolTip:
			self.ToolTip.Hide()

	def __RefreshLanguageList(self):
		for key in self.Languages.keys():
			lButton = self.Languages[key]
			if (app.GetLanguage() == key):
				lButton.Down()
				lButton.Disable()
			else:
				lButton.SetUp()
				lButton.Enable()

	def __ChangeLanguage(self, key):
		if (app.GetLanguage() == key) or key not in list(self.Languages.keys()):
			return

		self.Languages[key].Disable()
		self.Languages[key].Down()
		
		app.SetLanguage(key)
		app.Restart()

	def __FocusLogin(self):
		self.Objects["ID_EditLine"].SetFocus()

	def __FocusPassword(self):
		self.Objects["PWD_EditLine"].SetFocus()

	def __FocusPin(self):
		self.Objects["PIN_EditLine"].SetFocus()

	def __RecoveryPassword(self):
		import webbrowser
		webbrowser.open_new(introInterface.GetWindowConfig("links", "recovery"),)

	def __rememberData(self):
		if not self.Objects["Remember"].IsChecked():
			if introInterface.RegistryHandle.Instance().GetRegistryValue("account"):
				introInterface.RegistryHandle.Instance().DeleteRegistryTree("account")

	def CreateAccount(self):
		accountMax = introInterface.GetWindowConfig("lenght_data", "account")
		[self.__CreateAccount(i) for i in range(accountMax)]

	def __CreateAccount(self, i):
		accountHandle = introInterface.AccountHandle.Instance()
		accountData = accountHandle(i)

		if accountData != None:
			self.accountObjects[i][0].SetText(accountData[introInterface.POS_ID])
			self.accountObjects[i][3].SAFE_SetEvent(self.__OnAccountButtonEvent, "load", i)
			self.accountObjects[i][1].Hide()
			self.accountObjects[i][2].Show()
			self.accountObjects[i][2].SAFE_SetEvent(self.__OnAccountButtonEvent, "delete", i)
		else:
			self.accountObjects[i][0].SetText(introInterface.GetLocaleText("default_text"))
			self.accountObjects[i][1].Show()
			self.accountObjects[i][2].Hide()

	def __OnAccountButtonEvent(self, event, *args):
		accountHandle = introInterface.AccountHandle.Instance()

		index = 0
		if len(args) > 0:
			index = int(args[0])

		if event == "save":
			if index == -1 or accountHandle(index) != None:
				self.PopupNotifyMessage(introInterface.GetLocaleText("full"), lambda *args: None, bCheck = "RED")
				return False

			if self.__ValidateUserInformation():
				value = "{0}|{1}".format(self.Objects["ID_EditLine"].GetText(), self.Objects["PWD_EditLine"].GetText())
				if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
					if introInterface.GetWindowConfig("save_info", "pin"):
						value += "|{0}".format(self.Objects["PIN_EditLine"].GetText())

				accountHandle.UpdateAccount(index, value)
				self.PopupNotifyMessage(introInterface.GetLocaleText("success"), lambda *args: None, bCheck = "BLUE")
				self.CreateAccount()
			else:
				self.PopupNotifyMessage(introInterface.GetLocaleText("no_input"), lambda *args: None, bCheck = "RED")

		elif event == "load":
			if accountHandle(index) == None:
				self.PopupNotifyMessage(introInterface.GetLocaleText("empty"), lambda *args: None, bCheck = "RED")
				return False

			self.Objects["ID_EditLine"].SetText(accountHandle(index)[introInterface.POS_ID])
			self.Objects["PWD_EditLine"].SetText(accountHandle(index)[introInterface.POS_PWD])

			if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
				if introInterface.GetWindowConfig("save_info", "pin"):
					self.Objects["PIN_EditLine"].SetText(accountHandle(index)[introInterface.POS_PIN])
				else:
					self.__FocusPin()
					return
			else:
				self.__FocusPassword()

			self.__OnClickLoginButton()

		elif event == "delete":
			if accountHandle(index) == None:
				self.PopupNotifyMessage(introInterface.GetLocaleText("empty"), bCheck = "RED")
				return False

			accountHandle.UpdateAccount(index, "")
			self.PopupNotifyMessage(introInterface.GetLocaleText("delete"), bCheck = "RED")
			self.CreateAccount()

		return True

	def __ValidateUserInformation(self):
		myId = self.Objects["ID_EditLine"].GetText()
		myPasswd = self.Objects["PWD_EditLine"].GetText()

		if len(myId) == 0 or\
			len(myPasswd) == 0:
			return False

		return True

	def __OnClickLoginButton(self):
		id = self.Objects["ID_EditLine"].GetText()
		pwd = self.Objects["PWD_EditLine"].GetText()

		pin = ""
		if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
			pin = self.Objects["PIN_EditLine"].GetText()

		if introInterface.GetWindowConfig("save_info", "account") and self.__ValidateUserInformation():
			if self.Objects["Remember"].IsChecked():
				saveData = "{}|{}".format(id, pwd)
				if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
					if introInterface.GetWindowConfig("save_info", "pin"):
						saveData += "|{0}".format(pin)

				introInterface.RegistryHandle.Instance().SetRegistryValue("account", saveData)

		if len(id) == 0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_ID, lambda *args: None)
			return

		if len(pwd) == 0:
			self.PopupNotifyMessage(localeInfo.LOGIN_INPUT_PASSWORD, lambda *args: None)
			return

		self.Connect(id, pwd, pin)

	def Connect(self, id, pwd, pin = ""):
		try:
			if bool(constInfo.SEQUENCE_PACKET_ENABLE) == True:
				net.SetPacketSequenceMode()
		except AttributeError:
			print "Sequence packets are disabled"

		if self.stream.popupWindow:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.LOGIN_CONNETING, lambda *args: None, localeInfo.UI_CANCEL)

		if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
			self.stream.SetLoginInfo(id, pwd, pin)
		else:
			self.stream.SetLoginInfo(id, pwd)

		self.stream.Connect()

		introInterface.LUA_SetValue(id)

	def __SetChannelData(self, index):
		for button in self.Objects["Channels"]:
			button.SetUp()

		self.Objects["Channels"][index].Down()

		if introInterface.GetWindowConfig("save_info", "channel"):
			introInterface.RegistryHandle.Instance().SetRegistryValue("channel", index)

		self.stream.SetConnectInfo(
			introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "ip"),
			self.__GetChannelData(index),
			introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "ip"),
			self.__GetChannelData("LOGIN")
		)

		net.SetMarkServer(introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "ip"), self.__GetChannelData("GUILD_MARK"))
		app.SetGuildMarkPath("10.tga")
		app.SetGuildSymbolPath("10")
		net.SetServerInfo("{}".format(self.__GetChannelData("SERVERINFO", index + 1)[0]))

	def __GetChannelData(self, arg, *args):
		if isinstance(arg, int):
			return introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "server")[arg]
		elif arg == "LOGIN":
			return introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "login")
		elif arg == "GUILD_MARK":
			return introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "guildmark_port")
		elif arg == "SERVERINFO":
			return introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "serverinfo")[1] % (introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "serverinfo")[0], args[0])

	def PopupDisplayMessage(self, msg):
		if not self.stream.popupWindow:
			return False

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg)

	def PopupNotifyMessage(self, msg, func = lambda *args: None, bCheck = "", ban_reason = ""):
		if not self.stream.popupWindow:
			return False

		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)

	def OnKeyDown(self, key):
		if self.stream.popupWindow.IsShow():
			return False

		i = key - app.DIK_F1
		if i >= 0 and i <= introInterface.GetWindowConfig("lenght_data", "account") - 1:
			emptyAccount = introInterface.AccountHandle.Instance()(i) == None
			
			if app.IsPressed(app.DIK_LCONTROL):
				return self.__SetChannelData(i)

			if not emptyAccount:
				if app.IsPressed(app.DIK_LSHIFT):
					return self.__OnAccountButtonEvent("delete", i)

			return self.__OnAccountButtonEvent("save" if emptyAccount else "load", i)

		return False

	# def __RefreshAdvisePosition(self):
	# 	(x, y) = self.advise_text.GetLocalPosition()
	# 	if ((x + self.advise_text_size) < 0):
	# 		self.advise_text.SetPosition(self.advise_render_window.GetWidth() + 5, y)
	# 	else:
	# 		self.advise_text.SetPosition(x-1, y)

	if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "check_channel"):	
		def NotifyChannelState(self, addrKey, state):
			pass

		def __CreateServerStateChecker(self):
			ServerStateChecker.Initialize()
			ServerStateChecker.Create(self)

			channel = 1
			for port in introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "server"):
				ServerStateChecker.AddChannel(channel, introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "ip"), port)
				channel += 1

			# for i in xrange(len(introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "server"))):
			# 	ServerStateChecker.AddChannel(introInterface.DEFAULT_SERVER, introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "ip"), introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "server")[i])

			ServerStateChecker.Request()

	def OnUpdate(self):
		# self.__RefreshAdvisePosition()

		if introInterface.GetWindowConfig("miscellaneous", "loginwindow", "check_channel"):	
			ServerStateChecker.Update()

	def OnPressExitKey(self):
		self.stream.SetPhaseWindow(0)
		return True
