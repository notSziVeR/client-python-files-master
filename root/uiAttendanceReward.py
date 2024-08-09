import ui, colorInfo, ItemWrapper
import item, net

import math

class AttendanceManagerClass(ui.SimplyWindow):
	class PeekObject(ui.SimplyWindow):
		SIZE = (60, 75)
		def __init__(self, iKey, bCollected, iCurrDay, iRewardVnum, iRewardCount, eType):
			super(AttendanceManagerClass.PeekObject, self).__init__("UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)
			self.windowConfig["CONTROLS"] = { "KEY" : iKey, "COLLECTED" : bCollected, "CUR_DAY" : iCurrDay, "REWARD" : (iRewardVnum, iRewardCount), "TYPE" : eType}
			self.__CreateObject()

		def __del__(self):
			super(AttendanceManagerClass.PeekObject, self).__del__()

			#@Private Methods
		def __Initialize(self):
			self.__toltip = ItemWrapper.ItemToolTipDummy(0)

		def __Destroy(self):
			self.__toltip = None

		def __CreateObject(self):
			#Base
			rBase = ui.MakeExpandedImageBox(self, "assets/ui/attendance_reward/object_bg_{}.png".format(self.windowConfig["CONTROLS"]["TYPE"]), 0, 0)
			self.AppendObject("BASE", rBase)

			## Header
			sText = colorInfo.Colorize("Special", 0xFFd0af3b) if self.windowConfig["CONTROLS"]["TYPE"] == 1 else "Day {}".format(self.GetKey()) 
			rDay = ui.MakeTextLineNew(rBase, 0, 0, sText)
			rDay.SetWindowHorizontalAlignCenter()
			rDay.SetHorizontalAlignCenter()
			self.AppendObject("DAY_TEXT", rDay)

			## Item Image
			item.SelectItem(self.GetReward()[0])
			w, h = item.GetItemSize()

			rSlot = ui.SlotWindow()
			rSlot.SetParent(rBase)
			rSlot.SetPosition((rBase.GetWidth() - 32 * w) / 2, ((rBase.GetHeight() - 32 * h) / 2) + 5)
			rSlot.SetSize(32, 32)
			rSlot.SetOverInItemEvent(self.__OnOverInItem)
			rSlot.SetOverOutItemEvent(self.__OnOverOutItem)
			rSlot.AppendSlot(0, 0, 0, 32, 32)
			rSlot.Show()

			rSlot.ClearSlot(0)
			rSlot.SetItemSlot(0, self.GetReward()[0], self.GetReward()[1])
			rSlot.RefreshSlot()

			self.AppendObject("ICON", rSlot)

			## Claimed Icon
			tImage = ui.MakeExpandedImageBox(rBase, "assets/ui/attendance_reward/claimed_icon.png", 0, (rBase.GetHeight() - 25) / 2 + 5)
			tImage.SetWindowHorizontalAlignCenter()

			tClaimed = ui.MakeTextLineNew(rBase, 0, 3, colorInfo.Colorize("Claimed", 0xFF40b170))
			tClaimed.SetWindowHorizontalAlignCenter()
			tClaimed.SetHorizontalAlignCenter()
			tClaimed.SetWindowVerticalAlignBottom()
			tClaimed.SetVerticalAlignBottom()

			self.AppendObject("COLLECTED", (tImage, tClaimed))

			## Collect Button
			tButton = ui.MakeButton(rBase, 0, 17, "", "assets/ui/attendance_reward/", "btn_collect_0.png", "btn_collect_0.png", "btn_collect_0.png", "Claim")
			tButton.SetWindowHorizontalAlignCenter()
			tButton.SetWindowHorizontalAlignCenter()
			tButton.SetWindowVerticalAlignBottom()
			tButton.SetWindowVerticalAlignBottom()
			tButton.SetEvent(ui.__mem_func__(self.__Collect))
			tButton.Hide()
			
			self.AppendObject("COLLECT", tButton)

			self.__ManageState()

		def __Collect(self):
			net.SendChatPacket("/attendance_collect")

		def __OnOverInItem(self, iKey):
			self.__toltip.SetVnum(self.GetReward()[0])
			self.__toltip.ShowToolTip()

		def __OnOverOutItem(self):
			self.__toltip.HideToolTip()

		def __ManageState(self):
			if self.windowConfig["CONTROLS"].get("COLLECTED"):
				for iKey in xrange(self.GetCountObject("COLLECTED")):
					self.GetObject("COLLECTED", iKey).Show()
				
				self.GetObject("COLLECT").Hide()
				return

			for iKey in xrange(self.GetCountObject("COLLECTED")):
				self.GetObject("COLLECTED", iKey).Hide()
			
			if (self.GetKey() == self.windowConfig["CONTROLS"].get("CUR_DAY")):
				self.GetObject("COLLECT").Show()

			#Public Methods
		def Show(self):
			super(AttendanceManagerClass.PeekObject, self).Show()
		
		def Hide(self):
			super(AttendanceManagerClass.PeekObject, self).Hide()

		def GetKey(self):
			return self.windowConfig["CONTROLS"].get("KEY", -1)

		def GetReward(self):
			return self.windowConfig["CONTROLS"].get("REWARD", ())

		def GetCollected(self):
			return self.windowConfig["CONTROLS"].get("COLLECTED", False)

		def RefreshElement(self, bCollected):
			self.windowConfig["CONTROLS"]["COLLECTED"] = bCollected

			self.__ManageState()

		OnPressExitKey = OnPressEscapeKey = lambda *args, **kwargs : None

	SIZE = (445, 585)

	def __init__(self):
		super(AttendanceManagerClass, self).__init__("UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)
	
	def __del__(self):
		super(AttendanceManagerClass, self).__del__()

	def __Initialize(self):
		self.windowConfig["texts"] = {
			"top" :
			{
				"x" : 100,
				"y" : 20,
				"text" : (
					colorInfo.Colorize("Log in to game everyday to receive special rewards.", 0xFF9c4828),
					"Every 5 days you have a chance to get better grade items.",
				)
			},

			"bottom" :
			{
				"x" : 0,
				"y" : 20,
				"text" : (
					colorInfo.Colorize("You have collected {} of {} daily rewards.", 0xFFb19d58),
					"You need {} more rewards to get |cFFd0af3bSpecial Monthly Reward.",
				)
			},
		}

		self.__CreateInterface()

	def __Destroy(self):
		pass

	def __CreateInterface(self):
		## Base
		board = ui.MainBoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetSize(*self.GetSize())
		board.SetTitleName("Attendance Reward")
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.Show()

		self.AppendObject("base", board)
		
		## Top Panel
		rPanel = ui.MakeExpandedImageBox(board, "assets/ui/attendance_reward/top_panel.png", 0, 31)
		rPanel.SetWindowHorizontalAlignCenter()

		for iNum, sLine in enumerate(self.windowConfig["texts"]['top']['text']):
			rText = ui.MakeTextLineNew(rPanel, self.windowConfig["texts"]['top']['x'], self.windowConfig["texts"]['top']['y'] + (iNum * 14), sLine)
			rText.SetOutline()
			self.AppendObject("top_panel_texts", rText, True)

		self.AppendObject("top_panel", rPanel)

		## Main Panel
		rPanel = ui.MakeExpandedImageBox(board, "assets/ui/attendance_reward/main_panel.png", 0, rPanel.GetLocalPosition()[1] + rPanel.GetHeight() + 2)
		rPanel.SetWindowHorizontalAlignCenter()

		tHeader = ui.MakeTextLineNew(rPanel, 0, 6, colorInfo.Colorize("Your rewards", 0xFFb19d58))
		tHeader.SetWindowHorizontalAlignCenter()
		tHeader.SetHorizontalAlignCenter()

		self.AppendObject("main_panel", (rPanel, tHeader))

		## Peek Window
		rPeek = ui.Window()
		rPeek.SetParent(rPanel)
		rPeek.AddFlag("attach")
		rPeek.SetPosition(0, 26)
		rPeek.SetInsideRender(True)
		rPeek.SetSize(rPanel.GetWidth(), rPanel.GetHeight() - 26)
		rPeek.Show()

		rContent = ui.Window()
		rContent.SetParent(rPeek)
		rContent.AddFlag("attach")
		rContent.SetPosition(0, 0)
		rContent.Show()

		self.AppendObject("peek_panel", (rPeek, rContent))

		## Bottom Panel
		rPanel = ui.MakeExpandedImageBox(board, "assets/ui/attendance_reward/bottom_panel.png", 0, rPanel.GetLocalPosition()[1] + rPanel.GetHeight() + 2)
		rPanel.SetWindowHorizontalAlignCenter()

		for iNum, sLine in enumerate(self.windowConfig["texts"]['bottom']['text']):
			rText = ui.MakeTextLineNew(rPanel, self.windowConfig["texts"]['bottom']['x'], self.windowConfig["texts"]['bottom']['y'] + (iNum * 14), sLine)
			rText.SetWindowHorizontalAlignCenter()
			rText.SetHorizontalAlignCenter()
			rText.SetOutline()
			self.AppendObject("bottom_panel_texts", rText, True)

		self.AppendObject("bottom_panel", rPanel)

	def CalculatePeek(self, sConfiguration = {}):
		def getPadding(sType):
			return self.GetObject(sConfiguration.get("sPeek", "PEEK"), 0).GetWidth() - (sConfiguration["lPadding"].get(sType, 0)[0] + sConfiguration["lPadding"].get(sType, 0)[1])

		xPerRow = max(0, int(math.floor((getPadding("pHorizontal") - self.GetObject(sConfiguration.get("sElement", "ITEMS"), 0).GetWidth()) / self.GetObject(sConfiguration.get("sElement", "ITEMS"), 0).GetWidth()))) + 1

		bCenter = False
		if xPerRow > 1:
			xSpace = float(getPadding("pHorizontal") - self.GetObject(sConfiguration.get("sElement", "ITEMS"), 0).GetWidth()) / float(xPerRow - 1)
		else:
			bCenter = True

		yPerRow = int(math.ceil(float(self.GetCountObject(sConfiguration.get("sElement", "ITEMS"))) / float(xPerRow)))
		
		it = 0
		for iRows in xrange(yPerRow):
			for iCol in xrange(xPerRow):
				if it >= self.GetCountObject(sConfiguration.get("sElement", "ITEMS")):
					break

				iPosX = (self.GetObject(sConfiguration.get("sPeek"), 0).GetWidth() - self.GetObject("ITEMS", 0).GetWidth()) / 2 if bCenter else sConfiguration["lPadding"].get("pHorizontal", 0)[0] + (iCol * xSpace)
				iPosY = (iRows * (self.GetObject(sConfiguration.get("sElement", "ITEMS"), 0).GetHeight() + sConfiguration["lPadding"].get("pVertical")[0]))

				self.GetObject(sConfiguration.get("sElement", "ITEMS"), it).SetPosition(iPosX, iPosY)

				it += 1
		
		self.GetObject(sConfiguration.get("sPeek"), 1).SetSize(self.GetObject(sConfiguration.get("sPeek"), 0).GetWidth(), \
			(self.GetObject(sConfiguration.get("sElement", "ITEMS"), self.GetCountObject(sConfiguration.get("sElement", "ITEMS")) - 1).GetLocalPosition()[1] + \
				self.GetObject(sConfiguration.get("sElement", "ITEMS"), self.GetCountObject(sConfiguration.get("sElement", "ITEMS")) - 1).GetHeight()
			))

	def __ClearItems(self):
		self.DeleteObject("ITEMS")

	def __GetCollected(self):
		iFinished = 0
		for iKey in xrange(self.GetCountObject("ITEMS")):
			if self.GetObject("ITEMS", iKey).GetCollected():
				iFinished += 1

		return iFinished

	def __ManageObjectCollected(self, bGetter = False):
		iFinished = self.__GetCollected()
		
		if iFinished >= (self.GetCountObject("ITEMS") - 1):
			self.GetObject("bottom_panel_texts", 0).SetText(colorInfo.Colorize("You have collected Special Monthly Reward.", 0xFFb19d58))
			self.GetObject("bottom_panel_texts", 1).Hide()
			return

		self.GetObject("bottom_panel_texts", 0).SetText(self.windowConfig["texts"]['bottom']['text'][0].format(iFinished, self.GetCountObject("ITEMS") - 1))
		self.GetObject("bottom_panel_texts", 1).SetText(self.windowConfig["texts"]['bottom']['text'][1].format((self.GetCountObject("ITEMS") - 1) - iFinished))

		if bGetter:
			return (iFinished, self.GetCountObject("ITEMS"))

	""" RECV """
	def OnRecvClear(self):
		self.__ClearItems()

	def OnRecvBasic(self, eMonth, iCurDay):
		self.windowConfig["CUR_MONTH"] = eMonth
		self.windowConfig["CUR_DAY"] = iCurDay

	def OnRecvObject(self, iKey, bCollected, iRewardVnum, iRewardCount, eType):
		tmpButton = self.PeekObject(iKey, bCollected, self.windowConfig["CUR_DAY"], iRewardVnum, iRewardCount, eType)
		tmpButton.SetParent(self.GetObject("peek_panel")[1])
		tmpButton.Show()

		self.AppendObject("ITEMS", tmpButton, True)

	def OnRecvRefreshObject(self, iKey, bCollected):
		self.GetObject("ITEMS", iKey - 1).RefreshElement(bCollected)

	def OnRecvRefresh(self):
		self.CalculatePeek({
			"sPeek" : "peek_panel",
			"sElement" : "ITEMS",
			"lPadding" : {
				"pHorizontal" : (1, 1),
				"pVertical" : (1, 0),
			},
		})

		self.__ManageObjectCollected()
	""" ---- """

	def Close(self):
		self.Hide()

	# OnPressExitKey = OnPressEscapeKey = lambda *args, **kwargs : None
