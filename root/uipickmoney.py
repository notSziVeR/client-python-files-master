#!/usr/bin/python
#-*- coding: iso-8859-1 -*-
import wndMgr
import ui
import ime
import uiScriptLocale
import localeInfo

import re
import grpText

class PickMoneyDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.unitValue = 1
		self.maxValue = 0
		self.eventAccept = 0

		self.OLD_SIZE = None

		self.isSplit = False
		self.isSplitExtend = False

		self.eventSplit = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/PickMoneyDialog.py")
		except:
			import exception
			exception.Abort("MoneyDialog.LoadDialog.LoadScript")

		try:
			self.board = self.GetChild("board")
			self.maxValueTextLine = self.GetChild("max_value")
			self.pickValueEditLine = self.GetChild("money_value")
			self.acceptButton = self.GetChild("accept_button")
			self.cancelButton = self.GetChild("cancel_button")

		except:
			import exception
			exception.Abort("MoneyDialog.LoadDialog.BindObject")

		self.pickValueEditLine.SetReturnEvent(ui.__mem_func__(self.OnAccept))
		self.pickValueEditLine.SetEscapeEvent(ui.__mem_func__(self.Close))
		self.acceptButton.SetEvent(ui.__mem_func__(self.OnAccept))
		self.cancelButton.SetEvent(ui.__mem_func__(self.Close))
		self.board.SetCloseEvent(ui.__mem_func__(self.Close))

		self.OLD_SIZE = {
			"width"		: self.board.GetWidth(),
			"height"	: self.board.GetHeight(),
		}

	def InitializeSplitWindow(self, event):
		self.SetSize(self.GetWidth(), self.GetHeight() + 53)
		self.board.SetSize(self.GetWidth(), self.GetHeight())

		self.acceptButton.ButtonText.Destroy()
		self.acceptButton.ButtonText = None

		self.acceptButton.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		self.acceptButton.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		self.acceptButton.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		self.acceptButton.SetText(uiScriptLocale.OK)

		self.acceptButton.SetPosition((self.board.GetWidth() - self.acceptButton.GetWidth()) / 2, 58)

		self.cancelButton.Hide()

		button = ui.Button()
		button.SetParent(self.board)
		button.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		button.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		button.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		button.SetPosition(0, 33 + 20 + 20 + 9)
		button.SetWindowHorizontalAlignCenter()

		self.eventSplit = event

		button.SAFE_SetEvent(self.__OnSplitButtonEvent)
		button.SetText("Rozdziel")
		button.Show()

		self.InsertChild("split_button", button)

		button = ui.ToggleButton()
		button.SetParent(self.board)
		button.SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
		button.SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
		button.SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
		button.SetPosition(0, 33 + 20 + 20 + 25 + 9)
		button.SetWindowHorizontalAlignCenter()
		button.SetToggleUpEvent(ui.__mem_func__(self.__DeactivateSplitItems))
		button.SetToggleDownEvent(ui.__mem_func__(self.__ActivateSplitItems))
		button.SetText("Paczki")
		button.Show()

		self.InsertChild("pack_button", button)
		self.isSplit = True

	def __ActivateSplitItems(self):
		self.SetSize(self.GetWidth(), self.GetHeight() + 26)
		self.board.SetSize(self.GetWidth(), self.GetHeight())

		thinBoard = ui.ThinBoardCircle()
		thinBoard.SetParent(self.board)
		thinBoard.SetPosition(0, 33 + 20 + 20 + 50 + 9)
		thinBoard.SetSize(self.GetWidth() - 32, 19)
		thinBoard.SetWindowHorizontalAlignCenter()
		thinBoard.Show()

		editLine = ui.EditLine()
		editLine.SetParent(thinBoard)
		editLine.SetPosition(3, 3)
		editLine.SetSize(thinBoard.GetWidth() - 3, thinBoard.GetHeight() - 3)
		editLine.SetNumberMode()
		editLine.SetReturnEvent(self.eventSplit)
		editLine.SetEscapeEvent(ui.__mem_func__(self.Close))
		editLine.SetMax(4)
		editLine.Show()

		self.pickValueEditLine.KillFocus()
		editLine.SetFocus()

		self.InsertChild("extend_split", (thinBoard, editLine, ))
		self.isSplitExtend = True

	def __DeactivateSplitItems(self):
		self.SetSize(self.GetWidth(), self.GetHeight() - 26)
		self.board.SetSize(self.GetWidth(), self.GetHeight())

		try:
			self.GetChild("extend_split")[1].KillFocus()

			map(lambda j : j.Destroy(), self.GetChild("extend_split"))
			map(lambda j : j.Hide(), self.GetChild("extend_split"))

			del self.ElementDictionary["extend_split"]
		except KeyError:
			print "Error"

		self.pickValueEditLine.SetFocus()
		self.isSplitExtend = False

	def __OnSplitButtonEvent(self):
		value = 0L

		try:
			value = long(self.GetChild("extend_split")[1].GetText())
		except (KeyError, ValueError, ):
			value = 0L

		self.eventSplit(value)
		self.eventSplit = None

	def Destroy(self):
		self.ClearDictionary()
		self.eventAccept = 0
		self.maxValue = 0
		self.pickValueEditLine = 0
		self.acceptButton = 0
		self.cancelButton = 0
		self.board = None

		self.OLD_SIZE = None

		self.isSplit = False
		self.isSplitExtend = False

		self.eventSplit = None

	def SetTitleName(self, text):
		self.board.SetTitleName(text)

	def SetAcceptEvent(self, event):
		self.eventAccept = event

	def SetMax(self, max):
		self.pickValueEditLine.SetMax(max)

	def GetValue(self):
		try:
			return long(self.pickValueEditLine.GetText())
		except ValueError:
			return 0L

	def __RedrawWindow(self, tLen):
		boxWidth = tLen * 4 + 20

		self.SetSize(self.GetWidth() + boxWidth, self.GetHeight())
		self.board.SetSize(self.GetWidth(), self.GetHeight())

		self.acceptButton.SetWindowHorizontalAlignCenter()
		self.cancelButton.SetWindowHorizontalAlignCenter()

		self.acceptButton.SetPosition(-6 - 61 / 2, self.acceptButton.GetLocalPosition()[1])
		self.cancelButton.SetPosition(6 + 61 / 2, self.acceptButton.GetLocalPosition()[1])

		print "After redrawing"

	def Open(self, maxValue, unitValue=1, bColored = False, bPlaceHolder = ""):
		width = self.GetWidth()
		(mouseX, mouseY) = wndMgr.GetMousePosition()

		if mouseX + width/2 > wndMgr.GetScreenWidth():
			xPos = wndMgr.GetScreenWidth() - width
		elif mouseX - width/2 < 0:
			xPos = 0
		else:
			xPos = mouseX - width/2

		self.SetPosition(xPos, mouseY - self.GetHeight() - 20)

		tLen = len(str(maxValue))

		if tLen > 4:
			self.__RedrawWindow(tLen)

		if bColored:
			maxValText = localeInfo.NumberToStringAsType(maxValue, True)
			maxValText = maxValText[:maxValText.rfind("Yang")] + localeInfo.SHOP_TYPE_MONEY
		else:
			maxValText = localeInfo.NumberToStringAsType(maxValue, False, "")
			maxValText = maxValText[:maxValText.rfind("Yang")]

		self.maxValueTextLine.SetText(" / " + maxValText)

		if len(bPlaceHolder) > 0:
			self.pickValueEditLine.SetOverlayText(bPlaceHolder)
		else:
			self.pickValueEditLine.SetText(str(unitValue))
		self.pickValueEditLine.SetFocus()

		self.unitValue = unitValue
		self.maxValue = maxValue
		self.Show()
		self.SetTop()

	def Close(self):
		self.SetSize(self.OLD_SIZE["width"], self.OLD_SIZE["height"])
		self.board.SetSize(self.OLD_SIZE["width"], self.OLD_SIZE["height"])

		# self.acceptButton.ButtonText.Destroy()
		# self.acceptButton.ButtonText = None

		# self.acceptButton.SetUpVisual("d:/ymir work/ui/public/middle_button_01.sub")
		# self.acceptButton.SetOverVisual("d:/ymir work/ui/public/middle_button_02.sub")
		# self.acceptButton.SetDownVisual("d:/ymir work/ui/public/middle_button_03.sub")
		# self.acceptButton.SetText(uiScriptLocale.OK)
		# self.acceptButton.SetPosition(19, 58)

		self.cancelButton.Show()

		try:
			self.GetChild("extend_split")[1].KillFocus()

			map(lambda j : j.Destroy(), self.GetChild("extend_split"))
			map(lambda j : j.Hide(), self.GetChild("extend_split"))

			del self.ElementDictionary["extend_split"]
		except KeyError:
			pass

		try:
			del self.ElementDictionary["split_button"]
			del self.ElementDictionary["pack_button"]
		except KeyError:
			pass

		self.isSplit = False
		self.isSplitExtend = False

		self.eventSplit = None

		self.pickValueEditLine.KillFocus()
		self.Hide()

	def OnAccept(self):
		text = self.pickValueEditLine.GetText()

		if len(text) != 0:
			text	= text.lower()
			textMoney = long(0L)

			if re.search(u"^[0-9]+([,.][0-9]{1,2})?([k]+)?$", text):
				textMoney = grpText.ConvertMoneyText(text)

			if text.isdigit() and textMoney == 0L:
				textMoney = long(text)

			if textMoney > 0L:
				if self.eventAccept:
					textMoney = min(textMoney, self.maxValue)
					self.eventAccept(textMoney)

		self.Close()

