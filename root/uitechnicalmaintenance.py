import ui
import net
import chat
import uiCommon
import localeInfo

import introInterface
import webbrowser
import colorInfo

class Maintenance_Panel(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.TimeWizardDialog = uiCommon.TimeWizard()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.board = None
		self.TimeoutText = None
		self.ReasonText = None
		self.ReasonEditLine = None
		self.StatusTextLine = None
		self.ScheduleButton = None
		self.CancelationButton = None
		self.PostponeButton = None

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/maintenance_panel.py")
		except:
			import exception
			exception.Abort("Maintenance_Panel.__LoadWindow.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.board.SetCloseEvent(ui.__mem_func__(self.Close))
			self.TimeoutText = self.GetChild("Timeout_TextLine")
			self.ReasonText = self.GetChild("Reason_TextLine")
			self.ReasonEditLine = self.GetChild("Reason_EditLine")
			self.StatusText = self.GetChild("Status_TextLine")
			self.ScheduleButton = self.GetChild("Schedule_Button")
			self.CancelationButton = self.GetChild("Cancelation_Button")
			self.PostponeButton = self.GetChild("Postpone_Button")

			## Buttons
			self.ScheduleButton.SAFE_SetEvent(self.__ScheduleMaintenance)
			self.CancelationButton.SAFE_SetEvent(self.__CancelMaintenance)
			self.PostponeButton.SAFE_SetEvent(self.__PostponeMaintenance)
		except:
			import exception
			exception.Abort("Maintenance_Panel.__LoadWindow.BindObject")

		self.SetCenterPosition()
		self.Hide()

	def	RecvUpdate(self, sRsn, sTimeoutFormatted):
		if sRsn != "CANCELED":
			self.StatusText.SetText(localeInfo.TECHNICAL_MAINTENANCE_SCHEDULED)
			self.ReasonText.SetText(sRsn.replace("_", " "))
			self.ReasonText.Show()
			self.TimeoutText.SetText(sTimeoutFormatted.replace("_", " "))
			self.ReasonEditLine.Hide()
		else:
			self.StatusText.SetText(localeInfo.TECHNICAL_MAINTENANCE_NOT_SCHEDULED)
			self.ReasonText.SetText("")
			self.ReasonText.Hide()
			self.TimeoutText.SetText("-")
			self.ReasonEditLine.Show()

	def	__GetReason(self):
		rsn = self.ReasonText.GetText()
		return rsn.replace(" ", "_")

	def	__ScheduleMaintenance(self):
		self.TimeWizardDialog.SetAcceptEvent(ui.__mem_func__(self.__ScheduleMaintenance_Apply))
		self.TimeWizardDialog.Open()

	def	__CancelMaintenance(self):
		## Picking reason from textline (should exist, otherwise how the hell would we postpone not existing event?)
		rsn = self.__GetReason()
		if len(rsn) <= 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.TECHNICAL_MAINTENANCE_MISSING_REASON)
			return

		net.SendChatPacket("/tech_maint_cancel %s" % rsn)

	def	__PostponeMaintenance(self):
		self.TimeWizardDialog.SetAcceptEvent(ui.__mem_func__(self.__PostponeMaintenance_Apply))
		self.TimeWizardDialog.Open()

	def	__ScheduleMaintenance_Apply(self):
		tm = self.TimeWizardDialog.GetTimeInSeconds()
		rsn = self.ReasonEditLine.GetText()

		if tm <= 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.TECHNICAL_MAINTENANCE_BAD_TIME)
			return

		if len(rsn) <= 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.TECHNICAL_MAINTENANCE_MISSING_REASON)
			return

		net.SendChatPacket("/tech_maint_add %s %d" % (rsn.replace(" ", "_"), tm))

	def	__PostponeMaintenance_Apply(self):
		tm = self.TimeWizardDialog.GetTimeInSeconds()
		## Picking reason from textline (should exist, otherwise how the hell would we postpone not existing event?)
		rsn = self.__GetReason()

		if tm <= 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.TECHNICAL_MAINTENANCE_BAD_TIME)
			return

		if len(rsn) <= 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.TECHNICAL_MAINTENANCE_MISSING_REASON)
			return

		net.SendChatPacket("/tech_maint_delay %s %d" % (rsn, tm))

	def	Close(self):
		self.Hide()

	def	Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		if self.ReasonEditLine.IsShow():
			self.ReasonEditLine.SetFocus()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.Show()

class Maintenance_Alert(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.ReasonText = None
		self.StartTimeText = None
		self.ChangelogButton = None

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/maintenance_alert.py")
		except:
			import exception
			exception.Abort("Maintenance_Alert.__LoadWindow.LoadObject")

		try:
			self.ReasonText = self.GetChild("Reason_Text")
			self.StartTimeText = self.GetChild("Start_Time_Text")
			self.ChangelogButton = self.GetChild("Changelog_Button")
		except:
			import exception
			exception.Abort("Maintenance_Alert.__LoadWindow.BindObject")
		
		self.ChangelogButton.SetEvent(ui.__mem_func__(self.OpenChangelog))
		self.Hide()

	def	RecvUpdate(self, sRsn, sStartTime):
		self.ReasonText.SetText(localeInfo.TECHNICAL_MAINTENANCE_ALERT_REASON_INFO + " " + colorInfo.Colorize(sRsn.replace("_", " "), 0xFFb96d78))
		self.StartTimeText.SetText(localeInfo.TECHNICAL_MAINTENANCE_ALERT_TIME_INFO + " " + colorInfo.Colorize(sStartTime.replace("_", " ") + "!", 0xFFA8B0A8))

		self.SetTop()

		if sRsn == "CANCELED":
			self.Hide()
		else:
			self.Show()
	
	def OpenChangelog(self):
		webbrowser.open_new(introInterface.GetWindowConfig("links", "changelog"),)

	def	Close(self):
		self.Hide()

	def	Open(self):
		self.SetTop()
		self.Show()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.Show()

