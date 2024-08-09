import ui
import net
import app
import item
import player
import constInfo
import exception
import uiToolTip
import localeInfo

class TombolaWindow(ui.ScriptWindow):

	BLINK_EFFECT_BASE_PATH = "assets/ui/tombola/blink_effect/%d.tga"
	TOMBOLA_CONFIG = {}
	MAX_BLINK = 16
	BLINK_FRAME = 0.03
	MAX_CYCLE = 4

	def	__init__(self):
		ui.ScriptWindow.__init__(self)

		self.Objects = {}
		self.toolTipWindow = uiToolTip.ItemToolTip()
		self.iReward = -1
		self.ttNextBlink = 0.0
		self.iCurrentBlink = 0
		self.iCycle = 0
		self.iBlinkToGo = 0
		self.__LoadWindow()

	def	__del__(self):
		ui.ScriptWindow.__del__(self)

		self.Objects = {}
		self.toolTipWindow = None
		self.iReward = -1
		self.ttNextBlink = 0.0
		self.iCurrentBlink = 0
		self.iCycle = 0
		self.iBlinkToGo = 0
		self.blinkEffectImage = None

	def	__LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/tombola_window.py")
		except:
			exception.Abort("TombolaWindow.LoadDialog.LoadObject")

		try:
			self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Hide))
			
			## Spin Button
			self.Objects["SPIN"] = self.GetChild("Spin_Button")

			## Slots
			self.Objects["SLOTS"] = self.GetChild("Slots")

			## User Balance
			self.Objects["BALANCE"] = self.GetChild("User_Balance_Text")
		except:
			exception.Abort("TombolaWindow.LoadDialog.BindObject")

		self.Objects["SPIN"].SAFE_SetEvent(self.__SpinWheel)

		self.Objects["SLOTS"].SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
		self.Objects["SLOTS"].SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))

		self.__BuildBlinkEffect()
		self.SetCenterPosition()
		self.Hide()

	def	__BuildBlinkEffect(self):
		self.blinkEffectImage = ui.ImageBox()
		self.blinkEffectImage.SetParent(self.GetChild("main_board"))
		self.blinkEffectImage.SetPosition(0, 0)
		self.blinkEffectImage.Hide()

	def	__OverInItem(self, iSlot):
		if self.toolTipWindow:
			if iSlot in self.TOMBOLA_CONFIG:
				self.toolTipWindow.ClearToolTip()
				self.toolTipWindow.AddItemData(self.TOMBOLA_CONFIG[iSlot][0], self.__GetCurrentSockets(self.TOMBOLA_CONFIG[iSlot][0]))
				self.toolTipWindow.ShowToolTip()

	def	__OverOutItem(self):
		if self.toolTipWindow:
			self.toolTipWindow.HideToolTip()

	def	__SpinWheel(self):
		if self.iReward == -1:
			net.SendChatPacket("/tombola_spin")

	def	__GetCurrentSockets(self, itemVnum):
		item.SelectItem(itemVnum)
		bHasRealtimeFlag = False
		bHasLimitValue = 0
		metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)]

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if item.LIMIT_REAL_TIME == limitType:
				bHasRealtimeFlag = True
				bHasLimitValue = limitValue
				break

		if bHasRealtimeFlag:
			return [bHasLimitValue + app.GetGlobalTimeStamp()] + metinSlot[1:6]
		elif constInfo.IS_AUTO_POTION(itemVnum) or (item.GetItemType() == item.ITEM_TYPE_UNIQUE and item.GetValue(0) > 0):
			return metinSlot[0:2] + [item.GetValue(0)]

		return metinSlot

	""" Recv """
	def	RecvTombolaItem(self, iSlot, iVnum, iCount):
		self.TOMBOLA_CONFIG[iSlot] = (iVnum, iCount)
		self.Objects["SLOTS"].SetItemSlot(iSlot, iVnum, iCount)

	def	RecvTombolaStartSpin(self, iReward):
		self.iReward = iReward+1
		self.ttNextBlink = app.GetTime()

	def	RecvUpdateBalance(self, iBalance):
		self.Objects["BALANCE"].SetText(localeInfo.TOMBOLA_USER_BALANCE % iBalance)
	""" """

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.Show()

	def	OnUpdate(self):
		if self.iReward > -1:
			if self.ttNextBlink < app.GetTime():
				self.ttNextBlink = app.GetTime()+self.BLINK_FRAME
				if self.iCycle >= self.MAX_CYCLE and self.iCurrentBlink == self.iReward:
					if self.blinkEffectImage.IsShow():
						self.iBlinkToGo -= 1
						self.blinkEffectImage.Hide()
						if self.iBlinkToGo <= 0:
							net.SendChatPacket("/tombola_reward")
							self.iCurrentBlink = 0
							self.iReward = -1
							self.iCycle = 0
							self.iBlinkToGo = 0
					else:
						self.blinkEffectImage.Show()

					return

				self.iCurrentBlink += 1
				if self.iCurrentBlink > self.MAX_BLINK:
					self.iCurrentBlink = 1
					self.iCycle += 1
					if self.iCycle >= self.MAX_CYCLE:
						self.iBlinkToGo = 5

				self.blinkEffectImage.LoadImage(self.BLINK_EFFECT_BASE_PATH % self.iCurrentBlink)
				self.blinkEffectImage.Show()

