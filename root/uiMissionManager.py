import ui, math, utility, colorInfo, localeInfo
import app, item, nonplayer
from weakref import proxy
from ui_event import Event

class MissionManagerClass(ui.SimplyWindow):
	class PeekObject(ui.SimplyWindow):
		class PeekLine(ui.SimplyWindow):
			SIZE = (240, 80)
			def __init__(self, oParent, iTaskID, iProgress, dwEnemy, iCount):
				super(MissionManagerClass.PeekObject.PeekLine, self).__init__("UI", (), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)
				self.windowConfig["CONTROLS"] = { "PARENT" : proxy(oParent), "KEY" : iTaskID, "PROGRESS" : iProgress, "ENEMY" : dwEnemy, "COUNT" : iCount }
				self.windowConfig["CONTROLS"]['GRID'] = {
					"x" : 5,
					"y" : 1,
				}

				self.__CreateObject()

			def __del__(self):
				super(MissionManagerClass.PeekObject.PeekLine, self).__del__()

				#@Private Methods
			def __Initialize(self):
				pass

			def __Destroy(self):
				pass

			def __CreateObject(self):
				rBase = ui.Window()
				rBase.SetParent(self)
				rBase.SetPosition(0, 0)
				rBase.SetSize(*self.SIZE)
				rBase.Show()

				self.AppendObject("base", rBase)

				## Item
				rItemSlot = ui.MakeExpandedImageBox(rBase, GetAssets().format("mission_manager/slot.png"), 10, 5)
				rEye = ui.MakeButton(rItemSlot, (rItemSlot.GetWidth() - 22) / 2, ((rItemSlot.GetHeight() - 17) / 2), "", GetAssets().format("mission_manager/"), "btn_render_n.png", "btn_render_h.png", "btn_render_d.png")
				rEye.SetEvent(Event(self.windowConfig["CONTROLS"]["PARENT"].SetRender, self.windowConfig["CONTROLS"]["ENEMY"]))
				self.AppendObject("render_btn", (rItemSlot, rEye))

				## State
				rStateContent = ui.Window()
				rStateContent.SetParent(rBase)
				rStateContent.SetPosition(rItemSlot.GetWidth() + rItemSlot.GetLocalPosition()[0] * 2, rItemSlot.GetLocalPosition()[1])
				rStateContent.SetSize(172, rItemSlot.GetHeight())
				rStateContent.Show()
				
				# Texts
				rEnemyName = ui.MakeTextLineNew(rStateContent, 0, 0, "Kill {}".format(nonplayer.GetMonsterName(self.windowConfig["CONTROLS"]['ENEMY'])))
				rCounter = ui.MakeTextLineNew(rStateContent, 0, 0, "[{}/{}]".format((self.windowConfig["CONTROLS"]['PROGRESS'] * self.windowConfig["CONTROLS"]['COUNT']) / 100, self.windowConfig["CONTROLS"]['COUNT']))
				rCounter.SetWindowHorizontalAlignRight()
				rCounter.SetHorizontalAlignRight()

				# Progress
				rProgress = [ui.ExpandedImageBox() for _ in range(2)]
				rProgress[0].SetParent(rStateContent)
				rProgress[0].SetPosition(0, 22)
				rProgress[0].SetWindowHorizontalAlignCenter()
				rProgress[0].LoadImage(GetAssets().format("mission_manager/progress_bar_0.png"))
				rProgress[0].Show()

				rProgress[1].SetParent(rProgress[0])
				rProgress[1].SetPosition(0, 0)
				rProgress[1].LoadImage(GetAssets().format("mission_manager/progress_bar_1.png"))
				rProgress[1].SetPercentage(self.windowConfig["CONTROLS"]['PROGRESS'], 100)
				rProgress[1].Show()

				self.AppendObject("content", (rStateContent, rEnemyName, rCounter, rProgress))

				## Rewards
				rGridContent = ui.Window()
				rGridContent.SetParent(rBase)
				rGridContent.SetPosition(0, rStateContent.GetLocalPosition()[1] + rStateContent.GetHeight() + 10)
				rGridContent.SetWindowHorizontalAlignCenter()
				rGridContent.SetSize(34 * self.windowConfig["CONTROLS"]['GRID']['x'], 34 * self.windowConfig["CONTROLS"]['GRID']['y'])
				rGridContent.Show()

				self.AppendObject("grid", rGridContent)

				for _ in range(self.windowConfig["CONTROLS"]['GRID']['x']):
					rItemSlot = ui.MakeExpandedImageBox(self.GetObject("grid"), GetAssets().format("mission_manager/slot.png"), _ * 34, 0)

					self.AppendObject("reward_slots", rItemSlot, True)

			def __CreateRewardObject(self, iPos, iVnum, iCount):
				item.SelectItem(iVnum)
				w, h = item.GetItemSize()

				rItemImage = ui.MakeExpandedImageBox(self.GetObject("reward_slots", iPos), item.GetIconImageFileName(), (self.GetObject("reward_slots", iPos).GetWidth() - 32 * w) / 2, ((self.GetObject("reward_slots", iPos).GetHeight() - 32 * h) / 2))

				self.AppendObject("reward_icons", rItemImage, True)

				#Public Methods
			def Show(self):
				super(MissionManagerClass.PeekObject.PeekLine, self).Show()
			
			def Hide(self):
				super(MissionManagerClass.PeekObject.PeekLine, self).Hide()

			def AppendReward(self, iPos, iVnum, iCount):
				self.__CreateRewardObject(iPos, iVnum, iCount)

			def SetProgress(self, iProgress):
				self.windowConfig["CONTROLS"]["PROGRESS"] = iProgress
				self.GetObject("content", 2).SetText("[{}/{}]".format((self.windowConfig["CONTROLS"]['PROGRESS'] * self.windowConfig["CONTROLS"]['COUNT']) / 100, self.windowConfig["CONTROLS"]['COUNT']))
				self.GetObject("content", 3)[1].SetPercentage(self.windowConfig["CONTROLS"]['PROGRESS'], 100)

			OnPressExitKey = OnPressEscapeKey = lambda *args, **kwargs : None

		SIZE = (245, 261)
		def __init__(self, iKey, iTime):
			super(MissionManagerClass.PeekObject, self).__init__("UI", (), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)
			self.windowConfig["CONTROLS"] = { "KEY" : iKey, "TIME" : app.GetTime() + iTime}
			self.__CreateObject()
			self.__RegisterScrollBar()

		def __del__(self):
			super(MissionManagerClass.PeekObject, self).__del__()

			#@Private Methods
		def __Initialize(self):
			pass

		def __Destroy(self):
			pass

		def __CreateObject(self):
			def BuildHeader(sKey, iPos = (0, 0)):
				rHeader = ui.MakeExpandedImageBox(self.GetObject("base"), GetAssets().format("mission_manager/object_{}_header.png").format(sKey), iPos[0], iPos[1])
				rHeader.SetWindowHorizontalAlignCenter()
				rHeaderText = ui.MakeTextLineNew(rHeader, 0, -1, "")
				rHeaderText.SetWindowHorizontalAlignCenter()
				rHeaderText.SetHorizontalAlignCenter()
				rHeaderText.SetWindowVerticalAlignCenter()
				rHeaderText.SetVerticalAlignCenter()
				rHeaderText.SetPackedFontColor(0xFFb7b7b7)

				self.AppendObject("header_{}".format(sKey), (rHeader, rHeaderText))

				return rHeaderText

			def BuildTopContent():
				rBar = ui.Window()
				rBar.SetParent(self.GetObject("base"))
				rBar.SetSize(rBase.GetWidth(), 47)
				rBar.SetPosition(0, self.GetObject("header_top", 0).GetLocalPosition()[1] + self.GetObject("header_top", 0).GetHeight())
				rBar.Show()

				## Item
				rItemSlot = ui.MakeExpandedImageBox(rBar, GetAssets().format("mission_manager/slot.png"), 12, (rBar.GetHeight() - 32) / 2)
				item.SelectItem(self.windowConfig["CONTROLS"]["KEY"])
				w, h = item.GetItemSize()

				rItemImage = ui.MakeExpandedImageBox(rItemSlot, item.GetIconImageFileName(), (rItemSlot.GetWidth() - 32 * w) / 2, ((rItemSlot.GetHeight() - 32 * h) / 2))

				## Time
				rTimeHeader = ui.MakeTextLineNew(rBar, 10, 10, colorInfo.Colorize("Time to complete the mission", 0xFFb7b7b7))
				rTimeHeader.SetWindowHorizontalAlignCenter()
				rTimeHeader.SetHorizontalAlignCenter()
				rTimeHeader.SetPackedFontColor(0xFFb7b7b7)

				rTime = ui.MakeTextLineNew(rBar, 13, 10 + 12, colorInfo.Colorize("00:30:00", 0xFFb0822a))
				rTime.SetWindowHorizontalAlignCenter()
				rTime.SetHorizontalAlignCenter()
				rTime.SetPackedFontColor(0xFFb7b7b7)

				self.AppendObject("top_content", (rBar, rItemSlot, rItemImage, rTimeHeader, rTime))

			## Base
			rBase = ui.MakeExpandedImageBox(self, GetAssets().format("mission_manager/object_bg.png"), 0, 0)
			self.AppendObject("base", rBase)

			## Header Top
			BuildHeader("top", (0, 4)).SetText("Mission Hunter")

			## Top Content
			BuildTopContent()

			## Peek
			rPeek = ui.Window()
			rPeek.SetParent(rBase)
			rPeek.AddFlag("attach")
			rPeek.SetPosition(0, self.GetObject("top_content", 0).GetLocalPosition()[1] + self.GetObject("top_content", 0).GetHeight() - 2)
			rPeek.SetInsideRender(True)
			rPeek.SetSize(rBase.GetWidth(), rBase.GetHeight() - (self.GetObject("top_content", 0).GetLocalPosition()[1] + self.GetObject("top_content", 0).GetHeight()))
			rPeek.Show()	

			rContent = ui.Window()
			rContent.SetParent(rPeek)
			rContent.AddFlag("attach")
			rContent.SetPosition(0, 0)
			rContent.Show()

			self.AppendObject("PEEK", (rPeek, rContent))

			## Renderer
			rRender = ui.RenderTarget()
			rRender.SetParent(rBase)
			rRender.LoadImage(GetAssets().format("mission_manager/render_bg.png"))
			rRender.Hide()

			retButton = ui.MakeButton(rRender, (rRender.GetWidth() - 163) / 2, (rRender.GetHeight() - 26), "", GetAssets().format("mission_manager/"), "btn_ret_n.png", "btn_ret_h.png", "btn_ret_d.png")
			retButton.SetText("Back", 2)
			retButton.SetEvent(Event(self.RenderState, False))

			self.AppendObject("render", (rRender, retButton))

		def __CalculatePeek(self, sConfiguration = {}):
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

					iPosX = (self.GetObject(sConfiguration.get("sPeek", "PEEK"), 0).GetWidth() - self.GetObject("ITEMS", 0).GetWidth()) / 2 if bCenter else sConfiguration["lPadding"].get("pHorizontal", 0)[0] + (iCol * xSpace)
					iPosY = (iRows * (self.GetObject(sConfiguration.get("sElement", "ITEMS"), 0).GetHeight() + sConfiguration["lPadding"].get("pVertical")[0]))

					iPosX -= sConfiguration["lPadding"].get("pCenterX", 0)

					self.GetObject(sConfiguration.get("sElement", "ITEMS"), it).SetPosition(iPosX, iPosY)

					it += 1

			self.GetObject(sConfiguration.get("sPeek", "PEEK"), 1).SetSize(self.GetObject(sConfiguration.get("sPeek", "PEEK"), 0).GetWidth(), \
				(self.GetObject(sConfiguration.get("sElement", "ITEMS"), self.GetCountObject(sConfiguration.get("sElement", "ITEMS")) - 1).GetLocalPosition()[1] + \
					self.GetObject(sConfiguration.get("sElement", "ITEMS"), self.GetCountObject(sConfiguration.get("sElement", "ITEMS")) - 1).GetHeight()
				))

		def __RegisterScrollBar(self):
			scrollBar = utility.ReworkedScrollBar()
			scrollBar.SetParent(self)
			scrollBar.SetPosition(self.GetObject("PEEK", 0).GetLocalPosition()[0] + self.GetObject("PEEK", 0).GetWidth() - 10, self.GetObject("PEEK", 0).GetLocalPosition()[1])
			scrollBar.SetSize(8, self.GetObject("PEEK", 0).GetHeight() + 1)
			scrollBar.SetScrollEvent(self.__OnScroll)
			scrollBar.SetScrollSpeed(50)
			scrollBar.Show()
			
			self.AppendObject("SCROLLBAR", scrollBar)

			self.__ChangeScrollbar()

		def __ChangeScrollbar(self):
			if not self.GetObject("SCROLLBAR"):
				return
			
			if self.GetObject("PEEK", 1).GetHeight() <= self.GetObject("PEEK", 0).GetHeight():
				self.GetObject("SCROLLBAR").Hide()
			else:
				self.GetObject("SCROLLBAR").SetScale(self.GetObject("PEEK", 0).GetHeight(), self.GetObject("PEEK", 1).GetHeight())
				self.GetObject("SCROLLBAR").SetPosScale((float(1) * abs(self.GetObject("PEEK", 1).GetLocalPosition()[1])) / (self.GetObject("PEEK", 1).GetHeight() - self.GetObject("PEEK", 0).GetHeight()))
				self.GetObject("SCROLLBAR").Show()

		def __OnScroll(self, fScale):
			if not self.GetObject("PEEK", 1) or\
				(self.GetObject("SCROLLBAR") and self.GetObject("SCROLLBAR").GetBlockMoveState() is True):
				return
			
			curr = min(0, max(math.ceil((self.GetObject("PEEK", 1).GetHeight() - self.GetObject("PEEK", 0).GetHeight()) * fScale * -1.0), -self.GetObject("PEEK", 1).GetHeight() + self.GetObject("PEEK", 0).GetHeight()))
			self.GetObject("PEEK", 1).SetPosition(0, curr)

			#Public Methods
		def Show(self):
			super(MissionManagerClass.PeekObject, self).Show()
		
		def Hide(self):
			super(MissionManagerClass.PeekObject, self).Hide()

		def AddReward(self, iTaskID, iPos, iVnum, iCount):
			self.GetObject("ITEMS", iTaskID).AppendReward(iPos, iVnum, iCount)

		def AddTask(self, iTaskID, iProgress, dwEnemy, iCount):
			tElement = self.PeekLine(self, iTaskID, iProgress, dwEnemy, iCount)
			tElement.SetParent(self.GetObject("PEEK")[1])
			tElement.Show()

			self.AppendObject("ITEMS", tElement, True)

		def RefreshTask(self, iTaskID, iProgress):
			self.GetObject("ITEMS", iTaskID).SetProgress(iProgress)

		def RefreshElements(self):
			self.__CalculatePeek({
				"sPeek" : "PEEK",
				"sElement" : "ITEMS",
				"lPadding" : {
					"pHorizontal" : (0, 0),
					"pVertical" : (10, 0),
					"pCenterX" : 5,
				},
			})

			self.__ChangeScrollbar()

		def SetRender(self, rEnemy):
			self.GetObject("render", 0).SetRenderTarget(rEnemy)
			self.RenderState(True)
		
		def RenderState(self, bState = False):
			if (bState):
				self.GetObject("render", 0).Show()
			else:
				self.GetObject("render", 0).Hide()

		def GetKey(self):
			return self.windowConfig["CONTROLS"]["KEY"]

		def OnUpdate(self):
			if self.windowConfig["CONTROLS"]["TIME"] >= app.GetTime():
				self.GetObject("top_content", 4).SetText(colorInfo.Colorize(localeInfo.SecondToHMS(self.windowConfig["CONTROLS"]["TIME"] - app.GetTime()), 0xFFb0822a))

		OnPressExitKey = OnPressEscapeKey = lambda *args, **kwargs : None

	SIZE = (265, 298)
	def __init__(self):
		super(MissionManagerClass, self).__init__("UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)
	
	def __del__(self):
		super(MissionManagerClass, self).__del__()

	def __Initialize(self):
		self.__CreateInterface()
		self.__RegisterScrollBar()

	def __Destroy(self):
		pass

	def __CreateInterface(self):
		## Base
		board = ui.MainBoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetSize(*self.GetSize())
		board.SetTitleName("Missions")
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.Show()

		self.AppendObject("BOARD", board)

		## Peek
		peek = ui.Window()
		peek.SetParent(self.GetObject("BOARD"))
		peek.AddFlag("attach")
		peek.SetPosition(0, 31)
		peek.SetInsideRender(True)
		self.windowConfig["PEEK_SIZE"] = (self.SIZE[0] - peek.GetLocalPosition()[0] * 2, self.SIZE[1] - peek.GetLocalPosition()[1] - 5)
		peek.SetSize(*self.windowConfig["PEEK_SIZE"])
		peek.Show()

		content = ui.Window()
		content.SetParent(peek)
		content.AddFlag("attach")
		content.SetPosition(0, 0)
		content.Show()

		self.AppendObject("PEEK", (peek, content))

	def __CalculatePeek(self, sConfiguration = {}):
		def getPadding(sType):
			return self.GetObject(sConfiguration.get("sPeek", "PEEK"), 0).GetWidth() - (sConfiguration["lPadding"].get(sType, 0)[0] + sConfiguration["lPadding"].get(sType, 0)[1])

		xPerRow = max(0, int(math.floor((getPadding("pHorizontal") - self.GetObject(sConfiguration.get("sElement", "ITEMS"), 0)[1].GetWidth()) / self.GetObject(sConfiguration.get("sElement", "ITEMS"), 0)[1].GetWidth()))) + 1

		bCenter = False
		if xPerRow > 1:
			xSpace = float(getPadding("pHorizontal") - self.GetObject(sConfiguration.get("sElement", "ITEMS"), 0)[1].GetWidth()) / float(xPerRow - 1)
		else:
			bCenter = True

		yPerRow = int(math.ceil(float(self.GetCountObject(sConfiguration.get("sElement", "ITEMS"))) / float(xPerRow)))
		
		it = 0
		for iRows in xrange(yPerRow):
			for iCol in xrange(xPerRow):
				if it >= self.GetCountObject(sConfiguration.get("sElement", "ITEMS")):
					break

				iPosX = (self.GetObject("PEEK", 0).GetWidth() - self.GetObject("ITEMS", 0)[1].GetWidth()) / 2 if bCenter else sConfiguration["lPadding"].get("pHorizontal", 0)[0] + (iCol * xSpace)
				iPosY = (iRows * (self.GetObject(sConfiguration.get("sElement", "ITEMS"), 0)[1].GetHeight() + sConfiguration["lPadding"].get("pVertical")[0]))

				iPosX -= sConfiguration["lPadding"].get("pCenterX", 0)

				self.GetObject(sConfiguration.get("sElement", "ITEMS"), it)[1].SetPosition(iPosX, iPosY)

				it += 1
		
		self.GetObject("PEEK", 1).SetSize(self.GetObject("PEEK", 0).GetWidth(), \
			(self.GetObject(sConfiguration.get("sElement", "ITEMS"), self.GetCountObject(sConfiguration.get("sElement", "ITEMS")) - 1)[1].GetLocalPosition()[1] + \
				self.GetObject(sConfiguration.get("sElement", "ITEMS"), self.GetCountObject(sConfiguration.get("sElement", "ITEMS")) - 1)[1].GetHeight()
			))

	def __RegisterScrollBar(self):
		scrollBar = utility.ReworkedScrollBar()
		scrollBar.SetParent(self)
		scrollBar.SetPosition(self.GetObject("PEEK", 0).GetLocalPosition()[0] + self.GetObject("PEEK", 0).GetWidth() - 14, self.GetObject("PEEK", 0).GetLocalPosition()[1])
		scrollBar.SetSize(8, self.GetObject("PEEK", 0).GetHeight())
		scrollBar.SetScrollEvent(self.__OnScroll)
		scrollBar.SetScrollSpeed(50)
		scrollBar.Show()
		
		self.AppendObject("SCROLLBAR", scrollBar)

		self.__ChangeScrollbar()

	def __ChangeScrollbar(self):
		if not self.GetObject("SCROLLBAR"):
			return
		
		if self.GetObject("PEEK", 1).GetHeight() <= self.GetObject("PEEK", 0).GetHeight():
			self.GetObject("SCROLLBAR").Hide()
		else:
			self.GetObject("SCROLLBAR").SetScale(self.GetObject("PEEK", 0).GetHeight(), self.GetObject("PEEK", 1).GetHeight())
			self.GetObject("SCROLLBAR").SetPosScale((float(1) * abs(self.GetObject("PEEK", 1).GetLocalPosition()[1])) / (self.GetObject("PEEK", 1).GetHeight() - self.GetObject("PEEK", 0).GetHeight()))
			self.GetObject("SCROLLBAR").Show()

	def __OnScroll(self, fScale):
		if not self.GetObject("PEEK", 1) or\
			(self.GetObject("SCROLLBAR") and self.GetObject("SCROLLBAR").GetBlockMoveState() is True):
			return
		
		curr = min(0, max(math.ceil((self.GetObject("PEEK", 1).GetHeight() - self.GetObject("PEEK", 0).GetHeight()) * fScale * -1.0), -self.GetObject("PEEK", 1).GetHeight() + self.GetObject("PEEK", 0).GetHeight()))
		self.GetObject("PEEK", 1).SetPosition(0, curr)

	def __ClearItems(self):
		self.DeleteObject("ITEMS")

	""" RECV """
	def OnRecvClear(self):
		self.__ClearItems()

		self.windowConfig["ITEMS"] = dict()

	def OnRecvTask(self, iKey, iTime, iTaskID, iProgress, dwEnemy, iCount):
		if self.GetObject("ITEMS"):
			for rKey, rElement in self.GetObject("ITEMS"):
				if (iKey == rKey):
					rElement.AddTask(iTaskID, iProgress, dwEnemy, iCount)
					return

		tmpButton = self.PeekObject(iKey, iTime)
		tmpButton.SetParent(self.GetObject("PEEK")[1])
		tmpButton.Show()

		self.AppendObject("ITEMS", (iKey, tmpButton), True)

		tmpButton.AddTask(iTaskID, iProgress, dwEnemy, iCount)
	
	def OnRecvTaskRefresh(self, iKey, iTaskID, iProgress):
		if self.GetObject("ITEMS"):
			for rKey, rElement in self.GetObject("ITEMS"):
				if (iKey == rKey):
					rElement.RefreshTask(iTaskID, iProgress)
					return

	def OnRecvReward(self, iKey, iTaskID, iPos, iVnum, iCount):
		if self.GetObject("ITEMS"):
			for rKey, rElement in self.GetObject("ITEMS"):
				if (iKey == rKey):
					rElement.AddReward(iTaskID, iPos, iVnum, iCount)
					return

	def OnRecvRefresh(self):
		self.__CalculatePeek({
			"sPeek" : "PEEK",
			"sElement" : "ITEMS",
			"lPadding" : {
				"pHorizontal" : (0, 0),
				"pVertical" : (0, 0),
				"pCenterX" : 5 if self.GetCountObject("ITEMS") > 1 else 0,
			},
		})

		for rKey, rElement in self.GetObject("ITEMS"):
			rElement.RefreshElements()

		self.__ChangeScrollbar()
	""" ---- """

	def Close(self):
		self.Hide()
