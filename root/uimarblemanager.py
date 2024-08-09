import ui
import localeInfo
import uiScriptLocale
import uiToolTip

import dbg

import app
import marblemgr
import wndMgr
# import renderTarget
import nonplayer

import chat

from cff import CFF

class MarbleManager(ui.ScriptWindow):
	RENDER_TARGET_INDEX = 100

	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __Initialize(self):
		self.OBJECTS = {}
		self.activePage = 0
		self.activeCount = 0
		self.isActiveMission = False
		self.COOLDOWN = 0
		self.tTime = {}
		self.__LoadWindow()

	def Destroy(self):
		self.ClearDictionary()

	def __LoadWindow(self):
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/MarbleManagerWindow.py")

		except KeyError, msg:
			dbg.TraceError("MarbleManager #1")

		try:
			self.__BindObjects()

		except KeyError, msg:
			dbg.TraceError("MarbleManager #2 - %s" % str(msg))

		try:
			self.__BindEvents()

		except KeyError, msg:
			dbg.TraceError("MarbleManager #3 - %s" % str(msg))

	def __BindObjects(self):
		GetObject = self.GetChild
		self.OBJECTS["BOARD"] = GetObject("Board")
		self.OBJECTS["RENDER"] = GetObject("RenderTarget")

		self.OBJECTS["BUTTON_PREV"] = GetObject("prev_btn")
		self.OBJECTS["BUTTON_NEXT"] = GetObject("next_btn")

		self.OBJECTS["MARBLE_NAME"] = GetObject("HeaderText")
		self.OBJECTS["BUTTONS_COUNT"] = [GetObject("Button_MarbleCount_%d" % (i)) for i in xrange(5)]

		self.OBJECTS["DATA_REQUIRED"] = GetObject("DATA_REQUIRED")
		self.OBJECTS["DATA_KILLED_BAR"] = GetObject("DATA_KILLED_BAR")
		self.OBJECTS["DATA_KILLED"] = GetObject("DATA_KILLED")
		
		self.OBJECTS["DATA_TIME_BAR"] = GetObject("DATA_TIME_BAR")
		self.OBJECTS["DATA_TIME"] = GetObject("DATA_TIME")

		self.OBJECTS["BUTTON_ACCEPT"] = GetObject("AcceptButton")

	def __BindEvents(self):
		GetObject = self.GetChild

		self.OBJECTS["BOARD"].SetCloseEvent(self.Close)

		self.OBJECTS["BUTTON_PREV"].SAFE_SetEvent(self.PrevMarble)
		self.OBJECTS["BUTTON_NEXT"].SAFE_SetEvent(self.NextMarble)

		for i in xrange(5):
			self.OBJECTS["BUTTONS_COUNT"][i].SAFE_SetEvent(self.__SetMarbleCount, True, i)

		self.OBJECTS["BUTTON_ACCEPT"].SAFE_SetEvent(self.__EventAcceptButton)

	def CreateToolTip(self, title, descList):
		toolTip = uiToolTip.ToolTip()
		toolTip.SetTitle(title)
		toolTip.AppendSpace(7)

		for desc in descList:
			toolTip.AutoAppendTextLine(desc)

		toolTip.AlignHorizonalCenter()
		toolTip.SetTop()
		return toolTip

	def Open(self):
		self.__Initialize()
		self.__InitializeData()
		self.SetCenterPosition()
		self.SetTop()
		self.Show()

	def UpdateInformation(self):
		if self.IsShow():
			self.__AppendInformation(self.activePage, False)

	def Close(self):
		## Clear data
		marblemgr.MarbleClearData()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def __EventAcceptButton(self):
		(id, marbleVnum, requiredCount, bActiveMission, isExtandedCount, killed) = marblemgr.MarbleGetByIndex(self.activePage)

		if bActiveMission and killed != requiredCount:
			marblemgr.MarblePacketDeactive(self.activePage, False)
		else:
			marblemgr.MarblePacketActive(self.activePage, self.activeCount)

	def UpdateElement(self, key, *args):
		if key in self.OBJECTS:
			self.OBJECTS[key].SetText(str(args[0]))

	def PrevMarble(self):
		if self.isActiveMission:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.MARBLE_MANAGER_CANNOT_CHANGE_PAGE)
			return

		if self.activePage <= 0:
			self.activePage = marblemgr.MarbleGetCount()

		self.activePage -= 1
		self.__AppendInformation(self.activePage)

	def NextMarble(self):
		if self.isActiveMission:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.MARBLE_MANAGER_CANNOT_CHANGE_PAGE)
			return

		if self.activePage >= (marblemgr.MarbleGetCount() - 1):
			self.activePage = -1

		self.activePage += 1
		self.__AppendInformation(self.activePage)

	def __SetMarbleCount(self, bClicked = False, index = 0):
		(id, marbleVnum, requiredCount, bActiveMission, isExtandedCount, killed) = marblemgr.MarbleGetByIndex(self.activePage)

		if (bClicked and bActiveMission):
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.MARBLE_MANAGER_CANNOT_CHANGE_COUNT)
			return

		for (tKey, tButton) in enumerate(self.OBJECTS["BUTTONS_COUNT"]):
			if index != tKey:
				tButton.Enable()
			else:
				tButton.Disable()

		val = requiredCount * (index + 1 ) if bClicked else requiredCount
		self.UpdateElement("DATA_REQUIRED", val)

		self.activeCount = index

	def __AppendRender(self, race):
		LIGHT_POSITION_MOUNT = (50.0, -30.0, 440.0)
		self.OBJECTS["RENDER"].SetRenderTarget(race)
		self.OBJECTS["RENDER"].SetLightPosition(*LIGHT_POSITION_MOUNT)

	def __InitializeData(self):
		for i in range(marblemgr.MarbleGetCount()):
			(id, marbleVnum, requiredCount, bActiveMission, isExtandedCount, killed) = marblemgr.MarbleGetByIndex(i)

			if bActiveMission == marbleVnum:
				self.activePage = i
				self.isActiveMission = True

		self.__AppendInformation(self.activePage)

	def __AppendInformation(self, index = 0, bSetRender = True):
		(id, marbleVnum, requiredCount, bActiveMission, isExtandedCount, killed) = marblemgr.MarbleGetByIndex(index)

		if (bSetRender):
			self.__AppendRender(marbleVnum)

			self.UpdateElement("MARBLE_NAME", nonplayer.GetMonsterName(marbleVnum))
		else:
			if bActiveMission == marbleVnum:
				self.isActiveMission = True
			else:
				self.isActiveMission = False

		self.__SetMarbleCount(False, 0 if isExtandedCount == 0 else isExtandedCount - 1)

		if marbleVnum == bActiveMission:
			
			self.OBJECTS["DATA_KILLED_BAR"].SetPercentage(killed, requiredCount)
			self.UpdateElement("DATA_KILLED", killed)

			if (killed == requiredCount):
				self.OBJECTS["BUTTON_ACCEPT"].SetText(uiScriptLocale.MARBLE_MANAGER_BUTTON_RECEIVE)
			else:
				self.OBJECTS["BUTTON_ACCEPT"].SetText(uiScriptLocale.MARBLE_MANAGER_BUTTON_CANCEL)

		else:
			self.OBJECTS["BUTTON_ACCEPT"].SetText(uiScriptLocale.MARBLE_MANAGER_BUTTON_ACCEPT)
			if (bActiveMission):
				self.OBJECTS["BUTTON_ACCEPT"].Disable()
			else:
				self.OBJECTS["BUTTON_ACCEPT"].Enable()

			self.OBJECTS["DATA_KILLED_BAR"].SetPercentage(0, requiredCount)

			cooldownTime = marblemgr.MarbleGetCooldown(index)

			if (cooldownTime > 0):
				self.OBJECTS["BUTTON_ACCEPT"].Disable()
				self.UpdateElement("DATA_KILLED", "---")
				
				if self.activePage not in self.tTime:
					self.tTime[self.activePage] = []

				self.tTime[self.activePage].append({
					'TIME' : cooldownTime + app.GetTime()
 				})
			else:
				self.OBJECTS["BUTTON_ACCEPT"].Enable()
				self.OBJECTS["DATA_KILLED"].SetText("---")
				self.OBJECTS["DATA_TIME"].SetText("---")
				# self.OBJECTS["DATA_TIME_BAR"].SetPercentage(0, 100)

	def OnUpdate(self):
		if self.activePage in self.tTime and self.tTime[self.activePage][0].get("TIME") > app.GetTime():
			timeLeft = self.tTime[self.activePage][0].get("TIME") - app.GetTime()
			self.OBJECTS["DATA_TIME"].SetText(CFF.format(("|Eemoticons/tooltip/clock|e {}".format(localeInfo.SecondToHMS(timeLeft))), 'red'))
			# self.OBJECTS["DATA_TIME_BAR"].SetPercentage(app.GetTime(), self.tTime[self.activePage][0].get("TIME"))
		else:
			self.OBJECTS["DATA_TIME"].SetText("---")
			# self.OBJECTS["DATA_TIME_BAR"].SetPercentage(0, 100)

		if self.GetLeft() < 0:
			self.SetPosition(0, self.GetTop())
		elif self.GetRight() > wndMgr.GetScreenWidth():
			self.SetPosition(wndMgr.GetScreenWidth() - self.GetWidth(), self.GetTop())

		if self.GetTop() < 0:
			self.SetPosition(self.GetLeft(), 0)
		elif self.GetBottom() > wndMgr.GetScreenHeight():
			self.SetPosition(self.GetLeft(), wndMgr.GetScreenHeight() - self.GetHeight())
