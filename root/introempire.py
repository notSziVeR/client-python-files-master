import ui, net, wndMgr, dbg, app, event, _weakref, localeInfo, uiScriptLocale, exception

class SelectEmpireWindow(ui.ScriptWindow):
	DESCRIPTION_EMPIRE_EVENT_MAX_LINES = 5
	EMPIRE_DESCRIPTION_TEXT_FILE_NAME = {
		net.EMPIRE_A : uiScriptLocale.EMPIREDESC_A,
		net.EMPIRE_C : uiScriptLocale.EMPIREDESC_C
	}
	
	class EmpireButton(ui.Window):
		def __init__(self, owner, arg):
			super(SelectEmpireWindow.EmpireButton, self).__init__()
			self.owner = owner
			self.arg = arg
		
		def __del__(self):
			super(SelectEmpireWindow.EmpireButton, self).__del__()
		
		def OnMouseOverIn(self):
			self.owner.OnOverInEmpire(self.arg)
		
		def OnMouseOverOut(self):
			self.owner.OnOverOutEmpire(self.arg)
		
		def OnMouseLeftButtonDown(self):
			if self.owner.empireID != self.arg:
				self.owner.OnSelectEmpire(self.arg)
	
	class DescriptionBox(ui.Window):
		def __init__(self):
			super(SelectEmpireWindow.DescriptionBox, self).__init__()
			self.descIndex = 0
		
		def __del__(self):
			super(SelectEmpireWindow.DescriptionBox, self).__del__()
		
		def SetIndex(self, index):
			self.descIndex = index
		
		def OnRender(self):
			event.RenderEventSet(self.descIndex)
	
	def __init__(self, stream):
		super(SelectEmpireWindow, self).__init__()
		net.SetPhaseWindow(net.PHASE_WINDOW_EMPIRE, self)
		
		self.stream						= stream
		self.empireID					= [net.EMPIRE_A, net.EMPIRE_C][app.GetRandom(0, 1)]
		self.descIndex					= 0
		self.empireArea					= {}
		self.empireAreaFlag				= {}
		self.empireFlag					= {}
		self.empireAreaButton			= {}
		self.empireAreaCurAlpha			= { net.EMPIRE_A:0.0, net.EMPIRE_C:0.0 }
		self.empireAreaDestAlpha		= { net.EMPIRE_A:0.0, net.EMPIRE_C:0.0 }
		self.empireAreaFlagCurAlpha		= { net.EMPIRE_A:0.0, net.EMPIRE_C:0.0 }
		self.empireAreaFlagDestAlpha	= { net.EMPIRE_A:0.0, net.EMPIRE_C:0.0 }
		self.empireFlagCurAlpha		= { net.EMPIRE_A:0.0,  net.EMPIRE_C:0.0 }
		self.empireFlagDestAlpha		 = { net.EMPIRE_A:0.0, net.EMPIRE_C:0.0 }
	
	def __del__(self):
		super(SelectEmpireWindow, self).__del__()
		net.SetPhaseWindow(net.PHASE_WINDOW_EMPIRE, 0)
	
	def Close(self):
		self.ClearDictionary()
		
		self.leftButton			= None
		self.rightButton		= None
		self.selectButton		= None
		self.exitButton			= None
		self.textBoard			= None
		self.descriptionBox		= None
		self.empireArea			= None
		self.empireAreaButton	= None
		
		self.KillFocus()
		self.Hide()
		
		app.HideCursor()
		event.Destroy()
	
	def Open(self):
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetWindowName("SelectEmpireWindow")
		
		if not self.__LoadScript("uiscript/selectempirewindow.py"):
			dbg.TraceError("SelectEmpireWindow.Open - __LoadScript Error")
			return
		
		self.OnSelectEmpire(self.empireID)
		self.__CreateButtons()
		self.__CreateDescriptionBox()
		
		self.Show()
		app.ShowCursor()
	
	def __CreateButtons(self):
		for (key, img) in self.empireArea.items():
			(x, y) = img.GetGlobalPosition()
			img.SetAlpha(0.0)
			
			btn = self.EmpireButton(_weakref.proxy(self), key)
			btn.SetParent(self)
			btn.SetPosition(x, y)
			btn.SetSize(img.GetWidth(), img.GetHeight())
			btn.Show()
			
			self.empireAreaButton[key] = btn
	
	def __CreateDescriptionBox(self):
		self.descriptionBox = self.DescriptionBox()
		self.descriptionBox.Show()
	
	def OnOverInEmpire(self, arg):
		self.empireAreaDestAlpha[arg] = 1.0
	
	def OnOverOutEmpire(self, arg):
		if arg != self.empireID:
			self.empireAreaDestAlpha[arg] = 0.0
	
	NAMES = {
		net.EMPIRE_A: localeInfo.EMPIRE_A,
		net.EMPIRE_B:localeInfo.EMPIRE_B,
		net.EMPIRE_C:localeInfo.EMPIRE_C,
	}

	def OnSelectEmpire(self, arg):
		for key in self.empireArea.keys():
			self.empireAreaDestAlpha[key] = 0.0
			self.empireAreaFlagDestAlpha[key] = 0.0
			self.empireFlagDestAlpha[key] = 0.0
		
		self.empireAreaDestAlpha[arg] = 1.0
		self.empireAreaFlagDestAlpha[arg] = 1.0
		self.empireFlagDestAlpha[arg] = 1.0
		self.empireID = arg
		
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet(self.EMPIRE_DESCRIPTION_TEXT_FILE_NAME[arg])
		event.SetVisibleLineCount(self.descIndex, self.DESCRIPTION_EMPIRE_EVENT_MAX_LINES)
		event.SetRestrictedCount(self.descIndex, 37)
		
		if self.DESCRIPTION_EMPIRE_EVENT_MAX_LINES >= event.GetTotalLineCount(self.descIndex):
			self.GetChild("prev_text_button").Hide()
			self.GetChild("next_text_button").Hide()
		else:
			self.GetChild("prev_text_button").Show()
			self.GetChild("next_text_button").Show()

		self.EmpireName.SetText(self.NAMES[arg])

	def PrevDescriptionPage(self):
		if True == event.IsWait(self.descIndex):
			if event.GetVisibleStartLine(self.descIndex) - self.DESCRIPTION_EMPIRE_EVENT_MAX_LINES >= 0:
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) - self.DESCRIPTION_EMPIRE_EVENT_MAX_LINES)
				event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)
	
	def NextDescriptionPage(self):
		if True == event.IsWait(self.descIndex):
			event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) + self.DESCRIPTION_EMPIRE_EVENT_MAX_LINES)
			event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)

	def __LoadScript(self, fileName):
		try: ui.PythonScriptLoader().LoadScriptFile(self, fileName)
		except: exception.Abort("SelectEmpireWindow.__LoadScript.LoadObject")
		
		GetObject = ui.__mem_func__(self.GetChild)
		try:
			self.leftButton						= GetObject("left_button")
			self.rightButton					= GetObject("right_button")
			self.selectButton					= GetObject("select_button")
			self.exitButton						= GetObject("exit_button")
			self.textBoard						= GetObject("text_board")
			self.empireArea[net.EMPIRE_A]		= GetObject("EmpireArea_A")
			self.empireArea[net.EMPIRE_C]		= GetObject("EmpireArea_C")
			self.empireAreaFlag[net.EMPIRE_A]	= GetObject("EmpireAreaFlag_A")
			self.empireAreaFlag[net.EMPIRE_C]	= GetObject("EmpireAreaFlag_C")
			self.empireFlag[net.EMPIRE_A]		= GetObject("EmpireFlag_A")
			self.empireFlag[net.EMPIRE_C]		= GetObject("EmpireFlag_C")
			self.EmpireName						= GetObject("EmpireName")
		except: exception.Abort("SelectEmpireWindow.__LoadScript.BindObject")
		
		GetObject("prev_text_button").SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
		GetObject("next_text_button").SetEvent(ui.__mem_func__(self.NextDescriptionPage))
		self.selectButton.SetEvent(ui.__mem_func__(self.ClickSelectButton))
		self.exitButton.SetEvent(ui.__mem_func__(self.ClickExitButton))
		self.leftButton.SetEvent(ui.__mem_func__(self.ClickLeftButton))
		self.rightButton.SetEvent(ui.__mem_func__(self.ClickRightButton))
		
		[flag.SetAlpha(0.0) for flag in self.empireAreaFlag.values()]
		[flag.SetAlpha(0.0) for flag in self.empireFlag.values()]
		
		return True
	
	def ClickLeftButton(self):
		self.empireID = (net.EMPIRE_A if self.empireID == net.EMPIRE_C else net.EMPIRE_C)
		self.OnSelectEmpire(self.empireID)
	
	def ClickRightButton(self):
		self.empireID = (net.EMPIRE_A if self.empireID == net.EMPIRE_C else net.EMPIRE_C)
		self.OnSelectEmpire(self.empireID)
	
	def ClickSelectButton(self):
		if self.empireID not in [net.EMPIRE_A, net.EMPIRE_C]:
			return
		
		net.SendSelectEmpirePacket(self.empireID)
		self.stream.SetCreateCharacterPhase()
	
	def ClickExitButton(self):
		self.stream.SetLoginPhase()
	
	def OnUpdate(self):
		(xposEventSet, yposEventSet) = self.textBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+7))
		self.descriptionBox.SetIndex(self.descIndex)
		
		self.__UpdateAlpha(self.empireArea, self.empireAreaCurAlpha, self.empireAreaDestAlpha)
		self.__UpdateAlpha(self.empireAreaFlag, self.empireAreaFlagCurAlpha, self.empireAreaFlagDestAlpha)
		self.__UpdateAlpha(self.empireFlag, self.empireFlagCurAlpha, self.empireFlagDestAlpha)
	
	def __UpdateAlpha(self, dict, curAlphaDict, destAlphaDict):
		for (key, img) in dict.items():
			curAlpha = curAlphaDict[key]
			destAlpha = destAlphaDict[key]
			
			if abs(destAlpha - curAlpha) / 10 > 0.0001:
				curAlpha += (destAlpha - curAlpha) / 7
			else:
				curAlpha = destAlpha
			
			curAlphaDict[key] = curAlpha
			img.SetAlpha(curAlpha)
	
	def OnPressEscapeKey(self):
		self.ClickExitButton()
		return True
		
	def OnPressExitKey(self):
		self.ClickExitButton()
		return True

class ReselectEmpireWindow(SelectEmpireWindow):
	def ClickSelectButton(self):
		net.SendSelectEmpirePacket(self.empireID)
		self.stream.SetCreateCharacterPhase()
	
	def ClickExitButton(self):
		self.stream.SetSelectCharacterPhase()
