import ui
import localeInfo
import app
import ime
import uiScriptLocale
import chat
import grp
import uiToolTip
import player
import item
import wndMgr
import time
import constInfo
import net

import introInterface
import re

if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	import player
	import uiToolTip

class PopupDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadDialog()
		self.acceptEvent = lambda *arg: None

		self.button_text = ""
		self.is_autoclose = False
		self.autoclose_timer = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/PopupDialog.py")

			self.board = self.GetChild("board")
			self.message = self.GetChild("message")
			self.acceptButton = self.GetChild("accept")
			self.acceptButton.SetEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		if self.is_autoclose:
			self.autoclose_timer = app.GetTime() + GetWindowConfig("system", "popup", "DIALOG_REMAINING_TIME")

		buttonText = self.acceptButton.GetText( )

		if not buttonText:
			self.SetButtonName( uiScriptLocale.OK )

	def Close(self):
		self.Hide()
		self.acceptEvent()

		try: # avoiding ReferenceError weakly-referenced object no longer exists
			self.SetButtonName(self.button_text)
			self.is_autoclose = False
		except:
			pass

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
		ui.ScriptWindow.Destroy(self)

	def SetWidth(self, width):
		height = self.board.GetHeight()
		self.message.SetWidth(width - 25 * 2)
		self.board.SetSize(width, height)
		self.SetSize(self.board.GetRealWidth(), self.board.GetRealHeight())
		self.SetCenterPosition()
		self.UpdateRect()
		self.UpdateHeight()

	def SetHeight(self, height):
		width = self.board.GetWidth()
		self.acceptButton.SetPosition(self.acceptButton.GetLeft(), 63 - 105 + height)
		self.board.SetSize(width, height)
		self.SetSize(self.board.GetRealWidth(), self.board.GetRealHeight())
		self.SetCenterPosition()
		self.UpdateRect()

	def SetText(self, text):
		self.message.SetText(text)
		self.UpdateHeight()

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetButtonName(self, name):
		self.acceptButton.SetText(name)
		self.button_text = name

	"""
		Sets the is_autoclose flag which is used by the OnUpdate method
		to automatical close this dialog after a certain time. Call this
		method before the Open-method.

		Parameters
		----------
		flag: bool
			The autoclose flag.
	"""
	def SetAutoClose(self, flag = True):
		if not GetWindowConfig("system", "popup", "DIALOG_REMAINING_TIME_ENABLED"):
			return

		self.is_autoclose = flag

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

	"""
		Used for timing the autoclose functionallity.
		It also refresh the button-text by adding the remaining time.
		After the remaining time is 0 the dialog is closing and the
		is_autoclose flag is set to False again.
	"""
	def OnUpdate(self):
		if self.IsShow() and self.is_autoclose:
			current_time = app.GetTime()

			self.acceptButton.SetText(
				"%s (%.1f Sek)" % (self.button_text, self.autoclose_timer - current_time)
			)

			if self.autoclose_timer < current_time:
				self.Close()

	def UpdateHeight(self):
		height = self.message.GetRealHeight() + self.message.GetTop() + self.acceptButton.GetTop()
		self.board.SetSize(self.board.GetWidth(), height)
		self.SetSize(self.board.GetRealWidth(), self.board.GetRealHeight())
		self.UpdateRect()
		self.SetCenterPosition()

	def OnPressReturnKey(self):
		self.acceptButton.CallEvent()
		return True

class InputDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialog.py")

		getObject = self.GetChild
		self.board = getObject("Board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputSlot = getObject("InputSlot")
		self.inputValue = getObject("InputValue")

	def Open(self):
		self.inputValue.SetFocus()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputSlot = None
		if self.inputValue.IsFocus():
			self.inputValue.KillFocus()
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetNumberMode(self):
		self.inputValue.SetNumberMode()

	def SetSecretMode(self):
		self.inputValue.SetSecret()

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		width = length * 6 + 10
		self.SetBoardWidth(max(width + 50, 160))
		self.SetSlotWidth(width)
		self.inputValue.SetMax(length)

	def SetSlotWidth(self, width):
		self.inputSlot.SetSize(width, self.inputSlot.GetHeight())
		self.inputValue.SetSize(width, self.inputValue.GetHeight())
		if self.IsRTL():
			self.inputValue.SetPosition(self.inputValue.GetWidth(), 0)

	def SetBoardWidth(self, width):
		self.SetSize(max(width + 50, 160), self.GetHeight())
		self.board.SetSize(max(width + 50, 160), self.GetHeight())
		if self.IsRTL():
			self.board.SetPosition(self.board.GetWidth(), 0)
		self.UpdateRect()

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)
		self.inputValue.SetReturnEvent(event)

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.SetEscapeEvent(event)

	def GetText(self):
		return self.inputValue.GetText()

class InputDialogWithDescription(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription.py")
		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description = getObject("Description")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription(self, text):
		self.description.SetText(text)

class InputDialogWithDescription2(InputDialog):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()

	def __del__(self):
		InputDialog.__del__(self)

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/inputdialogwithdescription2.py")

		try:
			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = getObject("InputSlot")
			self.inputValue = getObject("InputValue")
			self.description1 = getObject("Description1")
			self.description2 = getObject("Description2")

		except:
			import exception
			exception.Abort("InputDialogWithDescription.LoadBoardDialog.BindObject")

	def SetDescription1(self, text):
		self.description1.SetText(text)

	def SetDescription2(self, text):
		self.description2.SetText(text)

class QuestionDialog(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.isEnabledReturnKey = True
		self.__CreateDialog()
		self.isShop = False

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		ui.ScriptWindow.Destroy(self)

		self.board = None
		self.textLine = None
		self.acceptButton = None
		self.cancelButton = None
		self.isShop = False

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event):
		self.acceptButton.SAFE_SetEvent(event)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAcceptEvent(self, event):
		self.acceptButton.SetEvent(event)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

		self.AutoResize(20)
	
	def SetTextPrice(self, text, itemVnum = 1, buyVnum = 0, metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)], attrSlot = 0):
		sText = text
		item.SelectItem(itemVnum)
		sText += "<IMAGE path={}>".format(item.GetIconImageFileName()) + " ?"

		self.textLine.SetText(sText)

		self.AutoResize(20)

		if buyVnum:
			toolTip = uiToolTip.ItemToolTip()

			toolTip.AddItemData(buyVnum, metinSlot, attrSlot, bShowIcon = True)
			toolTip.HideToolTip()

			self.acceptButton.SetToolTipWindow(toolTip)

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def AutoResize(self, extraWidth = 0):
		self.SetWidth(self.textLine.GetTextWidth() + extraWidth)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def SetDisableReturnKey(self, state = True):
		self.isEnabledReturnKey = state

	def OnPressReturnKey(self):
		if self.isEnabledReturnKey:
			self.acceptButton.CallEvent()
		
		return True

class QuestionDialog2(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def Destroy(self):
		ui.ScriptWindow.Destroy(self)

		self.board = None
		self.textLine1 = None
		self.textLine2 = None
		self.acceptButton = None
		self.cancelButton = None

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def SetText1(self, text, alignLeft = False):
		self.textLine1.SetText(text)
		if alignLeft == True:
			self.textLine1.SetPosition(15, 30)
			self.textLine1.SetWindowHorizontalAlignLeft()
			self.textLine1.SetHorizontalAlignLeft()
		else:
			self.textLine1.SetPosition(0, 25)
			self.textLine1.SetWindowHorizontalAlignCenter()
			self.textLine1.SetHorizontalAlignCenter()

	def SetText2(self, text, alignLeft = False):
		self.textLine2.SetText(text)
		if alignLeft == True:
			self.textLine2.SetPosition(15, 50)
			self.textLine2.SetWindowHorizontalAlignLeft()
			self.textLine2.SetHorizontalAlignLeft()
		else:
			self.textLine2.SetPosition(0, 50)
			self.textLine2.SetWindowHorizontalAlignCenter()
			self.textLine2.SetHorizontalAlignCenter()

	def AutoResize(self, minWidth = 30):
		if self.textLine1.GetTextSize()[0] > self.textLine2.GetTextSize()[0]:
			self.SetWidth(self.textLine1.GetTextSize()[0] + minWidth)
		else:
			self.SetWidth(self.textLine2.GetTextSize()[0] + minWidth)

class QuestionDialog3(ui.ScriptWindow):

	def __init__(self, acceptOnEnter = True):
		ui.ScriptWindow.__init__(self)
		self.acceptOnEnter = acceptOnEnter
		self.slot_pos = -1
		self.item_vnum = -1
		self.itemToolTip = None
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		QuestionDialog.Destroy(self)

		self.board = None
		self.textLine = None
		self.accept1Button = None
		self.accept2Button = None
		self.cancelButton = None

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog3.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.accept1Button = self.GetChild("btn_drop")
		self.accept2Button = self.GetChild("btn_destroy")
		self.cancelButton = self.GetChild("btn_cancel")

		self.itemToolTip = uiToolTip.ItemToolTip()
		self.accept1Button.SetToolTipWindow(self.itemToolTip)
		self.accept2Button.SetToolTipWindow(self.itemToolTip)

	def Open(self):
		if self.itemToolTip:
			self.itemToolTip.ClearToolTip()

			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(player.GetItemMetinSocket(self.slot_pos, i))

			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(player.GetItemAttribute(self.slot_pos, i))

			self.itemToolTip.AddItemData(self.item_vnum, metinSlot, attrSlot)
			self.itemToolTip.HideToolTip()

		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()

		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAccept1Event(self, event, *args):
		apply(self.accept1Button.SAFE_SetEvent, (event,) + args)

	def SAFE_SetAccept2Event(self, event, *args):
		apply(self.accept2Button.SAFE_SetEvent, (event,) + args)

	def SAFE_SetCancelEvent(self, event):
		self.cancelButton.SAFE_SetEvent(event)

	def SetAccept1Event(self, event, *args):
		apply(self.accept1Button.SetEvent, (event,) + args)

	def SetAccept2Event(self, event, *args):
		apply(self.accept2Button.SetEvent, (event,) + args)

	def SetCancelEvent(self, event):
		self.cancelButton.SetEvent(event)

	def SetText(self, text):
		self.textLine.SetText(text)

	def SetAccept1Text(self, text):
		self.accept1Button.SetText(text)

	def SetAccept2Text(self, text):
		self.accept2Button.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def Accept(self):
		self.accept1Button.SimulClick()

	def OnPressEscapeKey(self):
		self.Close()
		return True

class QuestionDialogSort(QuestionDialog):

	def __init__(self):
		QuestionDialog.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		QuestionDialog.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialogsort.py")

		self.board = self.GetChild("board")
		self.TitleBar = self.GetChild("TitleBar")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

		self.TitleBar.SetCloseEvent(self.Close)

	def Close(self):
		self.Hide()

	def SetText1(self, text):
		self.textLine1.SetText(text)

	def SetText2(self, text):
		self.textLine2.SetText(text)

class QuestionDialogMultiLine(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__CreateDialog()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialogmultiline.py")

		self.board = self.GetChild("board")
		self.textLine = self.GetChild("message")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def SAFE_SetAcceptEvent(self, event, *args):
		apply(self.acceptButton.SAFE_SetEvent, (event,) + args)

	def SAFE_SetCancelEvent(self, event, *args):
		apply(self.cancelButton.SAFE_SetEvent, (event,) + args)

	def SetAcceptEvent(self, event, *args):
		apply(self.acceptButton.SetEvent, (event,) + args)

	def SetCancelEvent(self, event, *args):
		apply(self.cancelButton.SetEvent, (event,) + args)

	def SetText(self, text):
		self.textLine.SetText(text)
		self.UpdateSize()

	def SetAcceptText(self, text):
		self.acceptButton.SetText(text)

	def SetCancelText(self, text):
		self.cancelButton.SetText(text)

	def Accept(self):
		self.acceptButton.SimulClick()

	def UpdateSize(self):
		height = self.textLine.GetTop() + self.textLine.GetRealHeight() + 50
		self.__SetSize(self.GetWidth(), height)

	def __SetSize(self, width, height):
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.textLine.SetWidth(width - 30)
		self.UpdateRect()
		self.SetCenterPosition()

	def OnPressEscapeKey(self):
		self.Close()
		return True

class QuestionDialogWithTimeLimit(QuestionDialog2):

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.__CreateDialog()
		self.endTime = 0
		self.timeOverMsg = 0
		self.timeOverEvent = 0
		self.timeOverEventArgs = 0

	def __del__(self):
		QuestionDialog2.__del__(self)

	def __CreateDialog(self):
		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/questiondialog2.py")

		self.board = self.GetChild("board")
		self.textLine1 = self.GetChild("message1")
		self.textLine2 = self.GetChild("message2")
		self.acceptButton = self.GetChild("accept")
		self.cancelButton = self.GetChild("cancel")

	def Open(self, timeout):
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

		self.endTime = app.GetTime() + timeout

	def SetTimeOverEvent(self, event, *args):
		self.timeOverEvent = event
		self.timeOverEventArgs = args

	def SetTimeOverMsg(self, msg):
		self.timeOverMsg = msg

	def OnTimeOver(self):
		if self.timeOverEvent:
			apply(self.timeOverEvent, self.timeOverEventArgs)
		if self.timeOverMsg:
			chat.AppendChat(chat.CHAT_TYPE_INFO, self.timeOverMsg)

	def SetCancelOnTimeOver(self):
		self.isCancelOnTimeover = True

	def OnUpdate(self):
		leftTime = max(0, self.endTime - app.GetTime())
		self.SetText2("{} ({:.1f})".format(localeInfo.TOOLTIP_TIME_HEADER, leftTime))
		if leftTime<0.5:
			if self.timeOverMsg:
				chat.AppendChat(chat.CHAT_TYPE_INFO, self.timeOverMsg)

			if self.isCancelOnTimeover:
				self.cancelButton.CallEvent()

class MoneyInputDialog(ui.ScriptWindow):
	PARSE_REGEX = re.compile(r"(\d+)((,|\.)(\d+))?(k*)")

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.moneyHeaderText = localeInfo.MONEY_INPUT_DIALOG_SELLPRICE
		self.__CreateDialog()
		self.SetMaxLength(12)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		ui.ScriptWindow.Destroy(self)

		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.moneyText = None

	def __CreateDialog(self):

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/moneyinputdialog.py")

		getObject = self.GetChild
		self.board = self.GetChild("board")
		self.acceptButton = getObject("AcceptButton")
		self.cancelButton = getObject("CancelButton")
		self.inputValue = getObject("InputValue")
		# self.inputValue.SetNumberMode()
		self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
		self.moneyText = getObject("MoneyValue")

		self.acceptEvent = None

		self.acceptButton.SetEvent(self.OnAccept)
		self.inputValue.OnIMEReturn = self.OnAccept

	def Open(self):
		self.inputValue.SetText("")
		self.inputValue.SetFocus()
		self.__OnValueUpdate()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.board = None
		self.acceptButton = None
		self.cancelButton = None
		self.inputValue = None
		self.Hide()

	def SetTitle(self, name):
		self.board.SetTitleName(name)

	def SetFocus(self):
		self.inputValue.SetFocus()

	def SetMaxLength(self, length):
		#length = min(9, length)
		self.inputValue.SetMax(length)

	def SetMoneyHeaderText(self, text):
		self.moneyHeaderText = text

	def SetAcceptEvent(self, event):
		self.acceptEvent = event

	def SetCancelEvent(self, event):
		self.board.SetCloseEvent(event)
		self.cancelButton.SetEvent(event)
		self.inputValue.SetEscapeEvent(event)

	def OnAccept(self):
		value = self.GetValue()
		self.SetValue(value)

		if self.acceptEvent:
			self.acceptEvent()

	def SetValue(self, value):
		value=str(value)

		if value > 0:
			self.inputValue.SetText(str(value))
		else:
			self.inputValue.SetText("")

		self.__OnValueUpdate()
		ime.SetCursorPosition(len(value))

	def GetValue(self):
		text = self.inputValue.GetText()
		money = 0

		match = self.PARSE_REGEX.search(text)
		if match:
			preDecimal = match.group(1)
			decimal = match.group(4)
			thousands = match.group(5)

			number = preDecimal

			thousands = thousands.replace("k", "000")
			if decimal:
				decimalLength = min(len(decimal), len(thousands))
				if decimalLength < len(decimal):
					number += decimal[:decimalLength]
				else:
					number += decimal
				number += thousands[decimalLength:]
			else:
				number += thousands

			money = long(number)

		return money

	def GetText(self):
		return self.inputValue.GetText()

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.inputValue)
		self.moneyText.SetText(self.moneyHeaderText + localeInfo.NumberToMoneyString(self.GetValue()))

if gcGetEnable("EVENT_MANAGER_ENABLE"):
	class TimeWizard(ui.ScriptWindow):

		MIN_VALUE = 0
		MAX_VALUE = 9

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.clickEvent_NEW = lambda argSelf = self : argSelf.Close()
			self.Objects = {}
			self.__LoadWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)
			self.clickEvent_NEW = None
			self.Objects = {}

		def	__LoadWindow(self):

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/timewizard_dialog.py")

			getObject = self.GetChild
			getObject("Board").SetCloseEvent(ui.__mem_func__(self.Close))
			self.AcceptButton = getObject("Accept_Button")

			## Hours
			self.Objects["HOURS"] = ((getObject("Hours_Text_1"), getObject("Hours_Text_2")), \
			((getObject("Hours_ButtonUp_1"), getObject("Hours_ButtonDown_1")), (getObject("Hours_ButtonUp_2"), getObject("Hours_ButtonDown_2"))))

			## Minutes
			self.Objects["MINUTES"] = ((getObject("Minutes_Text_1"), getObject("Minutes_Text_2")), \
			((getObject("Minutes_ButtonUp_1"), getObject("Minutes_ButtonDown_1")), (getObject("Minutes_ButtonUp_2"), getObject("Minutes_ButtonDown_2"))))

			## Seconds
			self.Objects["SECONDS"] = ((getObject("Seconds_Text_1"), getObject("Seconds_Text_2")), \
			((getObject("Seconds_ButtonUp_1"), getObject("Seconds_ButtonDown_1")), (getObject("Seconds_ButtonUp_2"), getObject("Seconds_ButtonDown_2"))))

			## Binding
			self.Objects["HOURS"][1][0][0].SAFE_SetEvent(self.__UpdateTimeValue_UP, "HOURS", 0)
			self.Objects["HOURS"][1][0][1].SAFE_SetEvent(self.__UpdateTimeValue_DOWN, "HOURS", 0)
			self.Objects["HOURS"][1][1][0].SAFE_SetEvent(self.__UpdateTimeValue_UP, "HOURS", 1)
			self.Objects["HOURS"][1][1][1].SAFE_SetEvent(self.__UpdateTimeValue_DOWN, "HOURS", 1)

			self.Objects["MINUTES"][1][0][0].SAFE_SetEvent(self.__UpdateTimeValue_UP, "MINUTES", 0)
			self.Objects["MINUTES"][1][0][1].SAFE_SetEvent(self.__UpdateTimeValue_DOWN, "MINUTES", 0)
			self.Objects["MINUTES"][1][1][0].SAFE_SetEvent(self.__UpdateTimeValue_UP, "MINUTES", 1)
			self.Objects["MINUTES"][1][1][1].SAFE_SetEvent(self.__UpdateTimeValue_DOWN, "MINUTES", 1)

			self.Objects["SECONDS"][1][0][0].SAFE_SetEvent(self.__UpdateTimeValue_UP, "SECONDS", 0)
			self.Objects["SECONDS"][1][0][1].SAFE_SetEvent(self.__UpdateTimeValue_DOWN, "SECONDS", 0)
			self.Objects["SECONDS"][1][1][0].SAFE_SetEvent(self.__UpdateTimeValue_UP, "SECONDS", 1)
			self.Objects["SECONDS"][1][1][1].SAFE_SetEvent(self.__UpdateTimeValue_DOWN, "SECONDS", 1)

			self.AcceptButton.SAFE_SetEvent(self.ForwardedClickEvent)
			self.Hide()

		def	SetAcceptEvent(self, func):
			self.clickEvent_NEW = func

		def	ForwardedClickEvent(self):
			(self.clickEvent_NEW)()
			self.Close()

		def	__UpdateTimeValue_UP(self, key, num):
			cur_val = int(self.Objects[key][0][num].GetText())
			cur_val += 1

			if cur_val > self.MAX_VALUE:
				cur_val = self.MIN_VALUE

			self.Objects[key][0][num].SetText(str(cur_val))

		def	__UpdateTimeValue_DOWN(self, key, num):
			cur_val = int(self.Objects[key][0][num].GetText())
			cur_val -= 1

			if cur_val < self.MIN_VALUE:
				cur_val = self.MAX_VALUE

			self.Objects[key][0][num].SetText(str(cur_val))

		def	GetTimeInSeconds(self):
			sec = 0

			## Hours
			sec += int((self.Objects["HOURS"][0][0].GetText() + self.Objects["HOURS"][0][1].GetText()))*60*60

			## Minutes
			sec += int((self.Objects["MINUTES"][0][0].GetText() + self.Objects["MINUTES"][0][1].GetText()))*60

			## Seconds
			sec += int((self.Objects["SECONDS"][0][0].GetText() + self.Objects["SECONDS"][0][1].GetText()))

			return sec

		def	Close(self):
			self.Hide()

		def	Open(self):
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def	UpdateWindow(self):
			if self.IsShow():
				self.Close()
			else:
				self.Open()

if app.ENABLE_ADMIN_MANAGER:
	class DoubleInputDialogWithDescription(ui.ScriptWindow):
		def __init__(self):
			ui.ScriptWindow.__init__(self)

			self.__CreateDialog()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self):

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/doubleinputdialogwithdescription.py")

			getObject = self.GetChild
			self.board = getObject("Board")
			self.acceptButton = getObject("AcceptButton")
			self.cancelButton = getObject("CancelButton")
			self.inputSlot = [getObject("InputSlot1"), getObject("InputSlot2")]
			self.inputValue = [getObject("InputValue1"), getObject("InputValue2")]
			self.description = [getObject("Description1"), getObject("Description2")]
			self.maxLen = [0, 0]

			self.inputValue[0].SAFE_SetReturnEvent(self.inputValue[1].SetFocus)
			self.inputValue[0].SetTabEvent(ui.__mem_func__(self.inputValue[1].SetFocus))

		def Open(self):
			self.SetFocus()
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.ClearDictionary()
			self.board = None
			self.acceptButton = None
			self.cancelButton = None
			self.inputSlot = None
			self.inputValue = None
			self.Hide()

		def SoftClose(self):
			for i in xrange(2):
				self.inputValue[i].KillFocus()
			self.Hide()

		def SetTitle(self, name):
			self.board.SetTitleName(name)

		def SetNumberMode(self, index = -1):
			if index == -1:
				for i in xrange(2):
					self.SetNumberMode(i)
			else:
				self.inputValue[index].SetNumberMode()

		def SetSecretMode(self, index = -1):
			if index == -1:
				for i in xrange(2):
					self.SetSecretMode(i)
			else:
				self.inputValue[index].SetSecret()

		def SetFocus(self, index = 0):
			self.inputValue[index].SetFocus()

		def SetMaxLength(self, length, index = -1):
			if index == -1:
				for i in xrange(2):
					self.SetMaxLength(length, i)
			else:
				width = length * 6 + 10
				self.maxLen[index] = width
				maxWidth = max(self.maxLen[1 - index], width)
				self.SetBoardWidth(max(maxWidth + 50, 160))
				self.SetSlotWidth(width, index)
				self.inputValue[index].SetMax(length)

		def SetSlotWidth(self, width, index = -1):
			if index == -1:
				for i in xrange(2):
					self.SetSlotWidth(width, i)
			else:
				self.inputSlot[index].SetSize(width, self.inputSlot[index].GetHeight())
				self.inputValue[index].SetSize(width, self.inputValue[index].GetHeight())
				if self.IsRTL():
					self.inputValue[index].SetPosition(self.inputValue[index].GetWidth(), 0)

		def GetDisplayWidth(self, index):
			return self.inputSlot[index].GetWidth()

		def SetDisplayWidth(self, width, index = -1):
			if index == -1:
				for i in xrange(2):
					self.SetEditWidth(width, i)
			else:
				self.maxLen[index] = width
				maxWidth = max(self.maxLen[1 - index], width)
				self.SetBoardWidth(max(maxWidth + 50, 160))
				self.SetSlotWidth(width, index)

		def SetBoardWidth(self, width):
			self.SetSize(max(width + 50, 160), self.GetHeight())
			self.board.SetSize(max(width + 50, 160), self.GetHeight())
			if self.IsRTL():
				self.board.SetPosition(self.board.GetWidth(), 0)
			self.UpdateRect()

		def SetAcceptEvent(self, event):
			self.acceptButton.SetEvent(event)
			self.inputValue[1].SetReturnEvent(event)

		def SetCancelEvent(self, event):
			self.board.SetCloseEvent(event)
			self.cancelButton.SetEvent(event)
			for i in xrange(2):
				self.inputValue[i].SetEscapeEvent(event)

		def GetText(self, index):
			return self.inputValue[index].GetText()

		def SetDescription(self, text, index = -1):
			if index == -1:
				for i in xrange(2):
					self.SetDescription(text, i)
			else:
				self.description[index].SetText(text)

	class QuestionDialogAdmin(ui.ScriptWindow):

		def __init__(self, acceptOnEnter = True):
			ui.ScriptWindow.__init__(self)
			self.acceptOnEnter = acceptOnEnter
			self.__CreateDialog()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self):
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/questiondialogadmin.py")

			self.board = self.GetChild("board")
			self.textLine = self.GetChild("message")
			self.accept1Button = self.GetChild("accept1")
			self.accept2Button = self.GetChild("accept2")
			self.cancelButton = self.GetChild("cancel")

		def Open(self):
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Close(self):
			self.Hide()

		def SetWidth(self, width):
			height = self.GetHeight()
			self.SetSize(width, height)
			self.board.SetSize(width, height)
			self.SetCenterPosition()
			self.UpdateRect()

		def SAFE_SetAccept1Event(self, event, *args):
			apply(self.accept1Button.SAFE_SetEvent, (event,) + args)

		def SAFE_SetAccept2Event(self, event, *args):
			apply(self.accept2Button.SAFE_SetEvent, (event,) + args)

		def SAFE_SetCancelEvent(self, event):
			self.cancelButton.SAFE_SetEvent(event)

		def SetAccept1Event(self, event, *args):
			apply(self.accept1Button.SetEvent, (event,) + args)

		def SetAccept2Event(self, event, *args):
			apply(self.accept2Button.SetEvent, (event,) + args)

		def SetCancelEvent(self, event):
			self.cancelButton.SetEvent(event)

		def SetText(self, text):
			self.textLine.SetText(text)

		def SetAccept1Text(self, text):
			self.accept1Button.SetText(text)

		def SetAccept2Text(self, text):
			self.accept2Button.SetText(text)

		def SetCancelText(self, text):
			self.cancelButton.SetText(text)

		def Accept(self):
			self.accept1Button.SimulClick()

		def OnPressEscapeKey(self):
			self.Close()
			return True

if app.ENABLE_CUBE_RENEWAL_COPY_BONUS:
	class QuestionCopyBonusDialog(ui.ScriptWindow):
		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.fromItemVnum = 0
			self.toItemVnum = 0
			self.fromSockets = []
			self.fromAttrs = []
			self.itemToolTip = None
			self.__CreateDialog()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self):
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/questioncopybonusdialog.py")

			self.board = self.GetChild("board")
			self.textLine1 = self.GetChild("message1")
			self.textLine2 = self.GetChild("message2")
			self.acceptButton = self.GetChild("accept")
			self.cancelButton = self.GetChild("cancel")
			self.fromSlot = self.GetChild("FromSlot")
			self.toSlot = self.GetChild("ToSlot")

			self.fromSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInFromItem))
			self.fromSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

			self.toSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInToItem))
			self.toSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

			# Because ymir is shit
			self.toSlot.SetWindowHorizontalAlignRight()

			self.itemToolTip = uiToolTip.ItemToolTip()

		def SetFromInfo(self, itemVnum, sockets, attrs):
			self.fromItemVnum = itemVnum
			self.fromSockets = sockets
			self.fromAttrs = attrs

			self.fromSlot.SetItemSlot(0, self.fromItemVnum, 1)

			item.SelectItem(self.fromItemVnum)
			hasAttr = True if (self.fromAttrs and self.fromAttrs[0][0] != item.APPLY_NONE) else False
			itemName = ("|cffffc700|H|h[%s]|h|r" % item.GetItemName()) if hasAttr else ("|cfff1e6c0|H|h[%s]|h|r" % item.GetItemName())
			self.textLine1.SetText(localeInfo.CUBE_ITEM_WILL_BE_COMBINED_FROM.format(itemName))

		def SetToInfo(self, itemVnum):
			self.toItemVnum = itemVnum
			self.toSlot.SetItemSlot(0, self.toItemVnum, 1)

			item.SelectItem(self.toItemVnum)
			hasAttr = True if (self.fromAttrs and self.fromAttrs[0][0] != item.APPLY_NONE) else False
			itemName = ("|cffffc700|H|h[%s]|h|r" % item.GetItemName()) if hasAttr else ("|cfff1e6c0|H|h[%s]|h|r" % item.GetItemName())
			self.textLine2.SetText(localeInfo.CUBE_ITEM_WILL_BE_COMBINED_TO.format(itemName))

			maxTextWidth = max(self.textLine1.GetTextSize()[0], self.textLine2.GetTextSize()[0])
			self.SetSize(115 + maxTextWidth, 115)
			self.board.SetSize(115 + maxTextWidth, 115)
			self.SetCenterPosition()
			self.UpdateRect()

		def Open(self):
			if self.itemToolTip:
				self.itemToolTip.HideToolTip()

			self.SetCenterPosition()
			self.SetTop()
			self.SetFocus()
			self.Show()

		def Close(self):
			if self.itemToolTip:
				self.itemToolTip.HideToolTip()
			self.Hide()

		def OverInFromItem(self, slotNumber):
			if self.itemToolTip and self.fromItemVnum and self.fromSockets and self.fromAttrs:
				self.itemToolTip.ClearToolTip()
				self.itemToolTip.AddItemData(self.fromItemVnum, self.fromSockets, self.fromAttrs)
				self.itemToolTip.ShowToolTip()

		def OverInToItem(self, slotNumber):
			if self.itemToolTip and self.toItemVnum and self.fromSockets and self.fromAttrs:
				self.itemToolTip.ClearToolTip()
				self.itemToolTip.AddItemData(self.toItemVnum, self.fromSockets, self.fromAttrs)
				self.itemToolTip.ShowToolTip()

		def OverOutItem(self):
			if self.itemToolTip:
				self.itemToolTip.HideToolTip()

		def SetAcceptEvent(self, event, *args):
			self.acceptButton.SetEvent(event, *args)

		def SetCancelEvent(self, event, *args):
			self.cancelButton.SetEvent(event, *args)

		def OnPressEscapeKey(self):
			self.Close()
			return True

		def OnIMEReturn(self):
			if self.acceptButton:
				self.acceptButton.CallEvent()

			return True

class BuyFailPopupDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.LoadDialog()
		self.itemVnum = 0
		self.itemToolTip = None
		self.closeEvent = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/BuyFailPopupDialog.py")

			self.board = self.GetChild("board")
			self.firstText = self.GetChild("firstText")
			self.testWindow = self.GetChild("testWindow")
			self.itemImage = self.GetChild("itemImage")
			self.secondText = self.GetChild("secondText")
			self.accceptButton = self.GetChild("accept")
			self.accceptButton.SetEvent(ui.__mem_func__(self.Close))

			self.secondText.Hide()

			self.itemImage.SetEvent(ui.__mem_func__(self.OverInItem), "MOUSE_OVER_IN")
			self.itemImage.SetEvent(ui.__mem_func__(self.OverOutItem), "MOUSE_OVER_OUT")
			self.itemImage.Hide()
		except:
			import exception
			exception.Abort("PopupDialog.LoadDialog.BindObject")

	def SetCloseEvent(self, event):
		self.closeEvent = event

	def Open(self):
		self.SetCenterPosition()
		self.SetTop()
		self.SetFocus()
		self.Show()

	def Close(self):
		self.Hide()
		self.itemVnum = 0
		self.secondText.Hide()
		self.itemImage.Hide()

		if self.closeEvent:
			self.closeEvent()

		if self.itemToolTip:
			self.itemToolTip.ClearToolTip()
			self.itemToolTip.HideToolTip()

	def Destroy(self):
		self.Close()
		self.ClearDictionary()
		self.itemToolTip = None

	def SetWidth(self, width):
		height = self.GetHeight()
		self.SetSize(width, height)
		self.board.SetSize(width, height)
		self.SetCenterPosition()
		self.UpdateRect()

	def AutoResize(self, minWidth = 30):
		if self.itemVnum:
			self.SetWidth(self.firstText.GetTextSize()[0] + self.itemImage.GetWidth() + self.secondText.GetTextSize()[0] + 6 + minWidth)
			self.testWindow.SetSize(self.firstText.GetTextSize()[0] + self.itemImage.GetWidth() + self.secondText.GetTextSize()[0] + 6, 32)
		else:
			self.SetWidth(self.firstText.GetTextSize()[0] + minWidth)
			self.testWindow.SetSize(self.firstText.GetTextSize()[0], 32)

	def SetText(self, text):
		if self.itemVnum:
			item.SelectItem(self.itemVnum)
			splitText = text.split("|")
			self.firstText.SetText(splitText[0])

			self.itemImage.LoadImage(item.GetIconImageFileName())
			self.itemImage.SetPosition(self.firstText.GetTextSize()[0] + 2, 0)
			self.itemImage.Show()

			self.secondText.SetText(splitText[1])
			self.secondText.SetPosition(self.firstText.GetTextSize()[0] + self.itemImage.GetWidth() + 4, 15)
			self.secondText.Show()
		else:
			self.firstText.SetText(text)

	def SetItem(self, itemVnum):
		self.itemVnum = itemVnum

		if not self.itemToolTip:
			self.itemToolTip = uiToolTip.ItemToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))

		self.itemToolTip.ClearToolTip()
		self.itemToolTip.AddItemData(self.itemVnum, metinSlot, attrSlot)
		self.itemToolTip.HideToolTip()

	def OverInItem(self, eventArg):
		if self.itemToolTip:
			self.itemToolTip.ShowToolTip()

	def OverOutItem(self, eventArg):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnIMEReturn(self):
		self.Close()
		return True

if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	class PrivateShopPriceInputDialog(ui.ScriptWindow):

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.toolTip = None
			self.cancelEvent = None
			self.itemVnum = -1
			self.itemCount = 1
			self.inputMarketPrice = False
			self.marketGoldValue = 0
			self.marketChequeValue = 0
			self.__CreateDialog()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def __CreateDialog(self):

			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/privateshoppriceinputdialog.py")

			self.board = self.GetChild("board")
			self.acceptButton = self.GetChild("AcceptButton")
			self.cancelButton = self.GetChild("CancelButton")
			self.inputValue = self.GetChild("InputValue")
			self.inputMoneyText = self.GetChild("InputMoneyText")
			self.marketMoneyText = self.GetChild("MarketMoneyValue")
			self.priceHintButton = self.GetChild("PriceHintButton")
			self.marketPriceButton = self.GetChild("MarketPriceButton")

			self.inputValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)

			self.priceHintButton.SetShowToolTipEvent(ui.__mem_func__(self.__OnOverInButton), "PRICE_HINT")
			self.priceHintButton.SetHideToolTipEvent(ui.__mem_func__(self.__OnOverOutButton))

			self.marketPriceButton.SetEvent(ui.__mem_func__(self.__OnClickMarketPriceButton))
			self.marketPriceButton.SetShowToolTipEvent(ui.__mem_func__(self.__OnOverInButton), "AUTO_MARKET_PRICE_INPUT")
			self.marketPriceButton.SetHideToolTipEvent(ui.__mem_func__(self.__OnOverOutButton))
			
			if app.ENABLE_PRIVATE_SHOP_CHEQUE:
				self.inputChequeText = self.GetChild("InputChequeText")
				self.marketChequeText = self.GetChild("MarketChequeValue")
				self.inputChequeValue = self.GetChild("InputValue_Cheque")

				self.inputChequeValue.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)
				self.inputChequeValue.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickChequeEditLine)
				self.inputChequeValue.SetTabEvent(self.inputValue.SetFocus)
				self.inputValue.OnMouseLeftButtonDown = ui.__mem_func__(self.__ClickValueEditLine)
				self.inputValue.SetTabEvent(self.inputChequeValue.SetFocus)

			self.toolTip = uiToolTip.ToolTip()
			self.toolTip.HideToolTip()

		def Open(self):
			self.inputValue.SetFocus()
			self.__OnValueUpdate()
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

		def Clear(self):
			self.itemVnum = -1
			self.itemCount = 1
			self.marketGoldValue = 0
			self.marketChequeValue = 0

			self.inputValue.SetText("")
			if app.ENABLE_PRIVATE_SHOP_CHEQUE:
				self.inputChequeValue.SetText("")

		def Close(self):
			self.Clear()
			self.cancelEvent()
			self.Hide()

		def SetItemVnum(self, vnum):
			self.itemVnum = vnum

		def GetItemVnum(self):
			return self.itemVnum
			
		def SetItemCount(self, count):
			self.itemCount = count

		def GetItemCount(self):
			return self.itemCount

		def SetTitle(self, name):
			self.board.SetTitleName(name)

		def SetFocus(self):
			self.inputValue.SetFocus()

		def KillFocus(self):
			if self.inputValue.IsFocus():
				self.inputValue.KillFocus()
			
			elif app.ENABLE_PRIVATE_SHOP_CHEQUE and self.inputChequeValue.IsFocus():
				self.inputChequeValue.KillFocus()

		def SetAcceptEvent(self, event):
			self.acceptButton.SetEvent(event)
			self.inputValue.SetReturnEvent(event)

			if app.ENABLE_PRIVATE_SHOP_CHEQUE:
				self.inputChequeValue.SetReturnEvent(event)

		def SetCancelEvent(self, event):
			self.cancelEvent = event

			self.board.SetCloseEvent(self.Close)
			self.cancelButton.SetEvent(self.Close)
			self.inputValue.SetEscapeEvent(self.Close)

			if app.ENABLE_PRIVATE_SHOP_CHEQUE:
				self.inputChequeValue.SetEscapeEvent(self.Close)

		def SetValue(self, value):
			value=str(value)
			self.inputValue.SetText(value)
			self.__OnValueUpdate()
			ime.SetCursorPosition(len(value)+1)		

		def GetText(self):
			if len(self.inputValue.GetText()) <= 0:
				return "0"

			return self.inputValue.GetText()
			
		def SetMarketValue(self, gold, cheque):
			self.marketGoldValue = gold * self.itemCount
			self.marketChequeValue = cheque * self.itemCount

			if gold:
				self.marketMoneyText.SetText(localeInfo.NumberToMoneyString(gold))
				
				if self.inputMarketPrice:
					self.InputMarketPrice()
			else:
				self.marketMoneyText.SetText(localeInfo.PREMIUM_PRIVATE_SHOP_MARKET_PRICE_NOT_AVAILABLE)
				
			if app.ENABLE_PRIVATE_SHOP_CHEQUE:
				if not gold and not cheque:
					self.marketChequeText.Hide()
				else:
					self.marketChequeText.SetText(localeInfo.NumberToMoneyStringNoUnit(cheque) + " " + localeInfo.CHEQUE_SYSTEM_UNIT_WON)
					self.marketChequeText.Show()

					if self.inputMarketPrice:
						self.InputMarketPrice()

		if app.ENABLE_PRIVATE_SHOP_CHEQUE:
			def SetCheque(self, cheque):
				cheque=str(cheque)
				self.inputChequeValue.SetText(cheque)
				self.__OnValueUpdate()
				ime.SetCursorPosition(len(cheque)+1)
			
			def __ClickChequeEditLine(self) :
				self.inputChequeValue.SetFocus()
				if len(self.inputChequeValue.GetText()) <= 0:
					self.inputChequeValue.SetText("")

			def __ClickValueEditLine(self) :
				self.inputValue.SetFocus()
				if len(self.inputValue.GetText()) <= 0:
					self.inputValue.SetText("")
							
			def GetCheque(self):
				if len(self.inputChequeValue.GetText()) <= 0:
					return "0"

				return self.inputChequeValue.GetText()
				
			def __OnValueUpdate(self):
				if self.inputValue.IsFocus() :
					ui.EditLine.OnIMEUpdate(self.inputValue)

					money = self.inputValue.GetText()
					if len(money) <= 0:
						money = "0"
					else:
						k_pos = money.find('K')
						if k_pos >= 0:
							money = money[:k_pos] + '000' * money.count('K')

					self.inputMoneyText.SetText(localeInfo.NumberToMoneyString(int(money)))

				elif self.inputChequeValue.IsFocus() :
					ui.EditLine.OnIMEUpdate(self.inputChequeValue)

					cheque = self.inputChequeValue.GetText()
					if len(cheque) <= 0:
						cheque = "0"

					self.inputChequeText.SetText(localeInfo.NumberToMoneyStringNoUnit(int(cheque)) + " " + localeInfo.CHEQUE_SYSTEM_UNIT_WON)
				else:
					pass
	
		else:
			def __OnValueUpdate(self):
				ui.EditLine.OnIMEUpdate(self.inputValue)

		def __OnClickMarketPriceButton(self):
			if self.inputMarketPrice:
				self.inputMarketPrice = False

				self.marketPriceButton.SetUpVisual("d:/ymir work/ui/game/premium_private_shop/mini_empty_button_default.sub")
				self.marketPriceButton.SetOverVisual("d:/ymir work/ui/game/premium_private_shop/mini_empty_button_over.sub")
				self.marketPriceButton.SetDownVisual("d:/ymir work/ui/game/premium_private_shop/mini_empty_button_down.sub")
			else:
				self.inputMarketPrice = True

				self.marketPriceButton.SetUpVisual("d:/ymir work/ui/game/premium_private_shop/mini_accept_button_default.sub")
				self.marketPriceButton.SetOverVisual("d:/ymir work/ui/game/premium_private_shop/mini_accept_button_over.sub")
				self.marketPriceButton.SetDownVisual("d:/ymir work/ui/game/premium_private_shop/mini_accept_button_down.sub")

				self.InputMarketPrice()

		def InputMarketPrice(self):
			if self.marketGoldValue > 0:
				self.SetValue(str(self.marketGoldValue))

			if app.ENABLE_PRIVATE_SHOP_CHEQUE:
				if self.marketChequeValue > 0:
					self.SetCheque(str(self.marketChequeValue))

		def __OnOverInButton(self, button):
			self.toolTip.ClearToolTip()

			if button == "PRICE_HINT":
				self.toolTip.SetThinBoardSize(len(localeInfo.PREMIUM_PRIVATE_SHOP_MARKET_PRICE_HINT_MSG) * 4 + 50, 10)
				self.toolTip.AppendTextLine(localeInfo.PREMIUM_PRIVATE_SHOP_MARKET_PRICE_HINT_MSG, self.toolTip.SPECIAL_TITLE_COLOR)

			elif button == "AUTO_MARKET_PRICE_INPUT":
				self.toolTip.SetThinBoardSize(len(localeInfo.PREMIUM_PRIVATE_SHOP_AUTO_MARKET_PRICE_INPUT_TOOLTIP) * 4 + 50, 10)
				self.toolTip.AppendTextLine(localeInfo.PREMIUM_PRIVATE_SHOP_AUTO_MARKET_PRICE_INPUT_TOOLTIP, self.toolTip.SPECIAL_TITLE_COLOR)

			self.toolTip.ShowToolTip()
				
			
		def __OnOverOutButton(self):
			if 0 != self.toolTip:
				self.toolTip.HideToolTip()

		def OnPressEscapeKey(self):
			self.Close()
			return True