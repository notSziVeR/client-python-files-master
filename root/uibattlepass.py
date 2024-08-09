import ui
import grp
import app
import net
import item
import player
import wndMgr
import uiToolTip
import exception
import localeInfo

from datetime import datetime
from _weakref import proxy

BATTLE_PASS_UI_PATH = "d:/ymir work/ui/game/battle_pass/"

### Factory ###
def CreateBattlePassButton(eventFunc):
	btn = ui.Button()
	btn.SetUpVisual(BATTLE_PASS_UI_PATH + "battle_pass_normal.tga")
	btn.SetOverVisual(BATTLE_PASS_UI_PATH + "battle_pass_over.tga")
	btn.SetDownVisual(BATTLE_PASS_UI_PATH + "battle_pass_down.tga")
	btn.SetPosition(wndMgr.GetScreenWidth()-btn.GetWidth()-10, (wndMgr.GetScreenHeight()-btn.GetHeight())/2)
	btn.SAFE_SetEvent(eventFunc)
	btn.Hide()

	return btn
### ###

class NewScrollBar(ui.Window):
	def __init__(self, parent, path, scroll_cursor_image):
		ui.Window.__init__(self)
		self.SetParent(parent)

		self.mPos = 0.0
		self.eventScroll = lambda *arg: None
		self.disable = False
		self.__LoadWindow(path, parent, scroll_cursor_image)

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.mPos = 0.0
		self.eventScroll = None
		self.disable = False

	def	__LoadWindow(self, path, parent, scroll_cursor_image):
		## Size
		self.SetSize(parent.GetWidth(), parent.GetHeight())

		## ScrollCursor
		self.ScrollCursor = ui.DragButton()
		self.ScrollCursor.SetParent(self)
		self.ScrollCursor.SetPosition(0, 0)
		self.ScrollCursor.SetUpVisual(path+scroll_cursor_image)
		self.ScrollCursor.SetOverVisual(path+scroll_cursor_image)
		self.ScrollCursor.SetDownVisual(path+scroll_cursor_image)
		self.ScrollCursor.TurnOnCallBack()
		self.ScrollCursor.SetMoveEvent(ui.__mem_func__(self.__OnMove))
		self.ScrollCursor.SetRestrictMovementArea(0, 0, self.ScrollCursor.GetWidth(), self.GetHeight())
		self.ScrollCursor.Show()

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def	SetPos(self, pos):
		if self.disable:
			return

		self.mPos = pos
		self.__OnMove_Base(0, 0)

	def GetPos(self):
		return self.mPos

	def	Display(self, bShow):
		self.ScrollCursor.Hide()

	def	Disable(self):
		self.disable = True
		self.ScrollCursor.SetRestrictMovementArea(0, 0, self.ScrollCursor.GetWidth(), self.ScrollCursor.GetHeight())

	def	Enable(self):
		self.disable = False
		self.ScrollCursor.SetRestrictMovementArea(0, 0, self.ScrollCursor.GetWidth(), self.GetHeight())

	def	__OnMove_Base(self, x_f = -1, y_f = -1):
		if x_f == -1 and y_f == -1:
			(x, y) = self.GetMouseLocalPosition()
		else:
			(x, y) = (x_f, y_f)

		self.__OnMove()
		self.ScrollCursor.SetPosition(0, min(y, self.GetHeight()-self.ScrollCursor.GetHeight()))

	def	__OnMove(self):
		if self.disable:
			return

		(x, y) = self.GetMouseLocalPosition()
		self.mPos = float(min(max(0, y), self.GetHeight()))/float(self.GetHeight())
		self.eventScroll()

	if app.ENABLE_MOUSE_WHEEL_EVENT:
		## ScrollBar Wheel Support
		def OnWheelMove(self, iLen):
			if self.disable:
				return

			y = self.ScrollCursor.GetHeight()
			## Computing mouse move range (by percent)
			iLen = (float(abs(iLen)-100)/100.0)*(iLen/abs(iLen))

			## Mouse Inversion
			iLen *= -1

			## Recomputation
			self.mPos += iLen
			self.mPos = float(min(max(0.0, self.mPos), 1.0))

			## Scroll Cursor pos
			self.ScrollCursor.SetPosition(0, max(0, min(self.mPos*(self.GetHeight()-self.ScrollCursor.GetHeight()), self.GetHeight()-self.ScrollCursor.GetHeight())))

			self.eventScroll()
			return True

class ThinBoardLayered(ui.ThinBoardCircle):

	BASIC_COLOUR = grp.GenerateColor(255.0, 255.0, 255.0, 0.2)

	def	__init__(self):
		ui.ThinBoardCircle.__init__(self)
		self.wndLayer = None

		self.rLayerColour = self.BASIC_COLOUR
		self.__ReuildLayer()

	def	__del__(self):
		ui.ThinBoardCircle.__del__(self)

	def	SetSize(self, width, height):
		ui.ThinBoardCircle.SetSize(self, width, height)
		self.__ReuildLayer()

	def	SetColour(self, rColour):
		self.rLayerColour = rColour
		self.wndLayer.SetColor(self.rLayerColour)

	def	__ReuildLayer(self):

		## Wiping out an old object
		if self.wndLayer:
			self.wndLayer.Hide()
			del self.wndLayer

		## Recreacting
		self.wndLayer = ui.Bar()
		self.wndLayer.AddFlag("not_pick")
		self.wndLayer.SetParent(self)
		self.wndLayer.SetPosition(0, 0)
		self.wndLayer.SetSize(self.GetWidth(), self.GetHeight())
		self.wndLayer.SetColor(self.rLayerColour)
		self.wndLayer.Show()

class BattlePassInterface(ui.ScriptWindow):

	TYPE_TASK = 0
	TYPE_RANKING = 1
	OPTION_BUTTONS = {
						TYPE_TASK : [BATTLE_PASS_UI_PATH + "category_btn_1.tga", BATTLE_PASS_UI_PATH + "category_btn_1.tga", BATTLE_PASS_UI_PATH + "category_btn_2.tga", None, None],
						TYPE_RANKING : [BATTLE_PASS_UI_PATH + "category_btn_2.tga", BATTLE_PASS_UI_PATH + "category_btn_2.tga", BATTLE_PASS_UI_PATH + "category_btn_1.tga", None, None],
					}
	GRID_MAX_X = 10
	SLOT_X = 32
	SLOT_Y = 32

	TRANSLATION_UNIT = {
					"DIFFICULITY" : [localeInfo.BATTLE_PASS_DIFFICULITY_EASY, localeInfo.BATTLE_PASS_DIFFICULITY_MEDIUM, localeInfo.BATTLE_PASS_DIFFICULITY_HARD],
					"MONTHS" : ["", localeInfo.JANUARY, localeInfo.FEBRUARY, localeInfo.MARCH, localeInfo.APRIL, localeInfo.MAY, localeInfo.JUNE, localeInfo.JULY, localeInfo.AUGUST,
								localeInfo.SEPTEMBEER, localeInfo.OCTOBER, localeInfo.NOVEMBER, localeInfo.DECEMBER],
				}

	class TaskObject(ui.BorderA):

		WINDOW_SIZE = (295, 49)
		BUTTON_SIZE = 88

		TASK_IMAGE = BATTLE_PASS_UI_PATH + "task_image.tga"
		PROGRESS_EMPTY = BATTLE_PASS_UI_PATH + "total_progress_empty.tga"
		PROGRESS_FULL = BATTLE_PASS_UI_PATH + "total_progress_full.tga"

		def __init__(self, scriptParent, parent, sTitle, sDesc, iProgress):
			ui.BorderA.__init__(self)
			self.SetParent(parent)
			self.parent = proxy(parent)
			self.scriptParent = proxy(scriptParent)

			self.Objects = {}
			self.sTaskDesc = ""
			self.iProgress = 0
			self.tooltipItem = proxy(scriptParent.tooltipItem)
			self.lRewards = []
			self.__BuildWindow(sTitle, sDesc, iProgress)

		def __del__(self):
			ui.BorderA.__del__(self)
			self.Objects = {}
			self.sTaskDesc = ""
			self.iProgress = 0
			self.tooltipItem = None
			self.parent = None
			self.scriptParent = None
			self.lRewards = []

		def	__BuildWindow(self, sTitle, sDesc, iProgress):
			## Size
			self.SetSize(*self.WINDOW_SIZE)

			## Desc data
			self.sTaskDesc = getattr(localeInfo, sDesc, "NOT FOUND")

			## Task Image
			self.Objects["TASK_IMAGE"] = ui.ExpandedImageBox()
			self.Objects["TASK_IMAGE"].SetParent(self)
			self.Objects["TASK_IMAGE"].SetPosition(10, 0)
			self.Objects["TASK_IMAGE"].SetWindowVerticalAlignCenter()
			self.Objects["TASK_IMAGE"].LoadImage(self.TASK_IMAGE)
			self.Objects["TASK_IMAGE"].Show()

			## Task Title
			self.Objects["TASK_TITLE"] = ui.TextLine()
			self.Objects["TASK_TITLE"].SetParent(self)
			self.Objects["TASK_TITLE"].SetPosition(self.Objects["TASK_IMAGE"].GetLocalPosition()[0] + self.Objects["TASK_IMAGE"].GetWidth() + 10, -15)
			self.Objects["TASK_TITLE"].SetWindowVerticalAlignCenter()
			self.Objects["TASK_TITLE"].SetVerticalAlignCenter()
			self.Objects["TASK_TITLE"].SetText(self.Objects["TASK_TITLE"].SetText(getattr(localeInfo, sTitle, "NOT FOUND")))
			self.Objects["TASK_TITLE"].Show()

			## Task Progress Text
			self.Objects["TASK_PROGRESS_TEXT"] = ui.TextLine()
			self.Objects["TASK_PROGRESS_TEXT"].SetParent(self)
			self.Objects["TASK_PROGRESS_TEXT"].SetPosition(self.Objects["TASK_IMAGE"].GetLocalPosition()[0] + self.Objects["TASK_IMAGE"].GetWidth() + 10, 0)
			self.Objects["TASK_PROGRESS_TEXT"].SetWindowVerticalAlignCenter()
			self.Objects["TASK_PROGRESS_TEXT"].SetVerticalAlignCenter()
			self.Objects["TASK_PROGRESS_TEXT"].SetText(localeInfo.BATTLE_PASS_TASK_PROGRESS % iProgress)
			self.Objects["TASK_PROGRESS_TEXT"].Show()

			## Task Progress Gauge Empty
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"] = ui.ExpandedImageBox()
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"].SetParent(self)
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"].SetPosition(self.Objects["TASK_IMAGE"].GetLocalPosition()[0] + self.Objects["TASK_IMAGE"].GetWidth() + 10, 16)
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"].SetWindowVerticalAlignCenter()
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"].LoadImage(self.PROGRESS_EMPTY)
			self.Objects["TASK_PROGRESS_GAUGE_EMPTY"].Show()

			## Task Progress Gauge Full
			self.Objects["TASK_PROGRESS_GAUGE_FULL"] = ui.ExpandedImageBox()
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].SetParent(self.Objects["TASK_PROGRESS_GAUGE_EMPTY"])
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].SetPosition(8, 2)
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].LoadImage(self.PROGRESS_FULL)
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].SetPercentage(iProgress, 100)
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].Show()

			## Saving progress for further calculations
			self.iProgress = iProgress

			## Task Show Reward
			self.Objects["TASK_SHOW_REWARD"] = ui.Button()
			self.Objects["TASK_SHOW_REWARD"].SetParent(self)
			self.Objects["TASK_SHOW_REWARD"].SetPosition(self.GetWidth()-self.BUTTON_SIZE-10, 0)
			self.Objects["TASK_SHOW_REWARD"].SetWindowVerticalAlignCenter()
			self.Objects["TASK_SHOW_REWARD"].SetUpVisual("d:/ymir work/ui/public/large_button_01.sub")
			self.Objects["TASK_SHOW_REWARD"].SetOverVisual("d:/ymir work/ui/public/large_button_02.sub")
			self.Objects["TASK_SHOW_REWARD"].SetDownVisual("d:/ymir work/ui/public/large_button_03.sub")
			self.Objects["TASK_SHOW_REWARD"].SetText(localeInfo.BATTLE_PASS_SHOW_REWARDS)
			self.Objects["TASK_SHOW_REWARD"].SAFE_SetEvent(self.__ShowRewards)
			self.Objects["TASK_SHOW_REWARD"].Show()

		def	SetTaskProgress(self, iProgress):
			self.Objects["TASK_PROGRESS_TEXT"].SetText(localeInfo.BATTLE_PASS_TASK_PROGRESS % iProgress)
			self.Objects["TASK_PROGRESS_GAUGE_FULL"].SetPercentage(iProgress, 100)

			self.iProgress = iProgress

		def	AddReward(self, iVnum, iCount):
			item.SelectItem(iVnum)
			self.lRewards.append((iVnum, iCount, item.GetItemSize()[1]))

		def	GetProgress(self):
			return self.iProgress

		## Mouse Functions ##
		def	OnMouseOverIn(self):
			if self.tooltipItem:
				self.tooltipItem.ClearToolTip()

				for line in uiToolTip.SplitDescription(self.sTaskDesc, uiToolTip.DESC_WESTERN_MAX_COLS):
					self.tooltipItem.AppendTextLine(line)

				self.tooltipItem.ShowToolTip()

		def	OnMouseOverOut(self):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()
		## End of Mouse Functions ##

		def	__ShowRewards(self):
			## Sort it and print
			(sortedGrid, slotSize) = self.scriptParent.SortRewards(self.lRewards)
			self.scriptParent.OpenDropDialog(sortedGrid, slotSize)

	class RankingObject(ThinBoardLayered):

		WINDOW_SIZE = (301, 20)
		BASIC_COLOUR = 0x1E3FBF3F
		CLICKED_COLOUR = 0x1EC14242

		def	__init__(self, iNum, sName, sDt):
			ThinBoardLayered.__init__(self)
			self.parent = None
			self.Objects = {}

			self.__BuildWindow(iNum, sName, sDt)

		def	__del__(self):
			ThinBoardLayered.__del__(self)
			self.parent = None
			self.Objects = {}

		### LISTBOXEX. UI.PY ###
		def SetParent(self, parent):
			ThinBoardLayered.SetParent(self, parent)
			self.parent = proxy(parent)

		def OnMouseLeftButtonDown(self):
			if self.parent:
				self.parent.SelectItem(self)

		def OnRender(self):
			if self.parent:
				if self.parent.GetSelectedItem() != self:
					self.SetColour(self.BASIC_COLOUR)
				elif self.parent.GetSelectedItem() == self:
					self.SetColour(self.CLICKED_COLOUR)
		###

		def	__GenerateTextField(self, iX, iY, iWidth, iHeight):
			## Field
			wndField = ui.ThinBoardCircle()
			wndField.SetParent(self)
			wndField.SetPosition(iX, iY)
			wndField.SetWindowVerticalAlignCenter()
			wndField.SetSize(iWidth, iHeight)
			wndField.Show()

			## Text
			wndText = ui.MakeTextLine(wndField)
			wndText.SetPosition(0, -1)

			return wndField, wndText

		def	__BuildWindow(self, iNum, sName, sDt):
			## Size
			self.SetSize(*self.WINDOW_SIZE)

			## Num Field
			self.Objects["NUM_FIELD"], self.Objects["NUM_TEXT"] = self.__GenerateTextField(7, 0, 34, 14)
			self.Objects["NUM_TEXT"].SetText("%d" % iNum)

			## Name Field
			self.Objects["NAME_FIELD"], self.Objects["NAME_TEXT"] = self.__GenerateTextField(65, 0, 95, 14)
			self.Objects["NAME_TEXT"].SetText("%s" % sName)

			## DateTime Field
			self.Objects["DT_FIELD"], self.Objects["DT_TEXT"] = self.__GenerateTextField(194, 0, 95, 14)
			self.Objects["DT_TEXT"].SetText("%s" % sDt)

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Objects = {}
		self.currentType = self.TYPE_TASK
		self.ttEndDT = 0
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.dRewards = dict()
		self.lRewards = list()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.Objects = {}
		self.currentType = -1
		self.ttEndDT = 0
		self.tooltipItem = None
		self.dRewards = None
		self.lRewards = None

	def	__LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/battlepass.py")
		except:
			exception.Abort("BattlePassInterface.__LoadWindow.LoadObject")

		try:
			self.Objects["Board"] = self.GetChild("board")

			## Curtain
			self.Objects["BarCurtain"] = self.GetChild("BarCurtain")

			## Dialogs
			self.Objects["TaskList"] = self.GetChild("TaskList_Window")
			self.Objects["TaskListScroll"] = self.GetChild("TaskListScroll_Window")
			self.Objects["Ranking"] = self.GetChild("Ranking_Window")

			## Basic Info
			self.Objects["BasicInfo"] = {}
			self.Objects["BasicInfo"]["RadioButton"] = self.GetChild("BasicInfoOptions_RadioButton")
			self.Objects["BasicInfo"]["Difficulity"] = self.GetChild("BasicInfoOptions_DifficulityText")
			self.Objects["BasicInfo"]["Month"] = self.GetChild("BasicInfoOptions_MonthText")
			self.Objects["BasicInfo"]["Remaining"] = self.GetChild("BasicInfoOptions_RemainingTimeText")
			self.Objects["BasicInfo"]["Finished"] = self.GetChild("BasicInfoOptions_FinishedText")
			self.Objects["BasicInfo"]["Progress"] = self.GetChild("BasicInfoOptions_ProgressText")
			self.Objects["BasicInfo"]["RewardCollected"] = self.GetChild("BasicInfoOptions_RewardCollectedText")
			self.Objects["BasicInfo"]["CollectButton"] = self.GetChild("BasicInfoOptions_CollectButton")
			self.Objects["BasicInfo"]["RewardInfoButton"] = self.GetChild("BasicInfoOptions_RewardInfoButton")
		except:
			exception.Abort("BattlePassInterface.__LoadWindow.BindObject")

		## Board
		self.Objects["Board"].SetCloseEvent(ui.__mem_func__(self.Hide))

		## Curtain
		self.Objects["BarCurtain"].SetMouseLeftButtonDownEvent(self.Objects["BarCurtain"].Hide)
		self.Objects["BarCurtain"].Hide()

		## Option Button
		self.Objects["BasicInfo"]["RadioButton"].SAFE_SetEvent(self.__ChangeSite)
		self.OPTION_BUTTONS[self.TYPE_TASK][3] = self.Objects["TaskList"]
		self.OPTION_BUTTONS[self.TYPE_TASK][4] = self.Objects["Ranking"]

		self.OPTION_BUTTONS[self.TYPE_RANKING][3] = self.Objects["Ranking"]
		self.OPTION_BUTTONS[self.TYPE_RANKING][4] = self.Objects["TaskList"]

		## Collect&Reward Buttons
		self.Objects["BasicInfo"]["CollectButton"].SAFE_SetEvent(self.__RequestReward)
		self.Objects["BasicInfo"]["RewardInfoButton"].SAFE_SetEvent(self.__ShowMajorRewards)

		## Task ListBox
		self.Objects["TaskListBox"] = ui.ListBoxEx()
		self.Objects["TaskListBox"].SetParent(self.Objects["TaskList"])
		self.Objects["TaskListBox"].SetPosition(0, 0)
		self.Objects["TaskListBox"].SetItemSize(*self.TaskObject.WINDOW_SIZE)
		self.Objects["TaskListBox"].SetItemStep(self.TaskObject.WINDOW_SIZE[1])
		self.Objects["TaskListBox"].SetViewItemCount(5)
		self.Objects["TaskListBox"].Show()

		## Scroll
		self.Objects["TaskListBoxScroll"] = NewScrollBar(self.Objects["TaskListScroll"], BATTLE_PASS_UI_PATH, "scroll_bar.tga")
		self.Objects["TaskListBoxScroll"].SetPosition(0, 0)
		self.Objects["TaskListBoxScroll"].Show()

		self.Objects["TaskListBox"].SetScrollBar(self.Objects["TaskListBoxScroll"])

		## Ranking ListBox
		self.Objects["RankingListBox"] = ui.ListBoxEx()
		self.Objects["RankingListBox"].SetParent(self.Objects["Ranking"])
		self.Objects["RankingListBox"].SetPosition(0, 25)
		self.Objects["RankingListBox"].SetItemSize(*self.RankingObject.WINDOW_SIZE)
		self.Objects["RankingListBox"].SetItemStep(self.RankingObject.WINDOW_SIZE[1])
		self.Objects["RankingListBox"].SetViewItemCount(10)
		self.Objects["RankingListBox"].Show()

		if app.ENABLE_MOUSE_WHEEL_EVENT:
			## Wheel support
			self.SetScrollWheelEvent(self.Objects["TaskListBoxScroll"].OnWheelMove)

		## Default option
		self.__ChangeSite(self.TYPE_TASK)

		self.SetCenterPosition()
		self.SetTop()
		self.Hide()

	def	OpenDropDialog(self, sortedGrid, slotSize):
		## Bar Curtain
		self.Objects["BarCurtain"].Show()

		## Build pretty window
		self.Objects["PrettyCurtainWindow"] = ui.BorderA()
		self.Objects["PrettyCurtainWindow"].SetParent(self.Objects["BarCurtain"])
		self.Objects["PrettyCurtainWindow"].SetPosition(0, 0)
		self.Objects["PrettyCurtainWindow"].SetSize(slotSize[0]*self.SLOT_X + 20, slotSize[1]*self.SLOT_Y + 50)
		self.Objects["PrettyCurtainWindow"].SetWindowHorizontalAlignCenter()
		self.Objects["PrettyCurtainWindow"].SetWindowVerticalAlignCenter()
		self.Objects["PrettyCurtainWindow"].Show()

		## Text for pretty window
		self.Objects["PrettyCurtainTitle"] = ui.TextLine()
		self.Objects["PrettyCurtainTitle"].SetParent(self.Objects["PrettyCurtainWindow"])
		self.Objects["PrettyCurtainTitle"].SetPosition(0, 10)
		self.Objects["PrettyCurtainTitle"].SetWindowHorizontalAlignCenter()
		self.Objects["PrettyCurtainTitle"].SetHorizontalAlignCenter()
		self.Objects["PrettyCurtainTitle"].SetText(localeInfo.BATTLE_PASS_PRETTY_CURTAIN_TITLE)
		self.Objects["PrettyCurtainTitle"].Show()

		## Rebuild gridslot
		self.Objects["DropGridSlot"] = ui.GridSlotWindow()
		self.Objects["DropGridSlot"].SetParent(self.Objects["PrettyCurtainWindow"])
		self.Objects["DropGridSlot"].ArrangeSlot(0, slotSize[0], slotSize[1], self.SLOT_X, self.SLOT_X, 0, 0)
		self.Objects["DropGridSlot"].SetPosition((self.Objects["PrettyCurtainWindow"].GetWidth()-(slotSize[0]*self.SLOT_X))/2, 35)
		self.Objects["DropGridSlot"].SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		self.Objects["DropGridSlot"].SetOverInItemEvent(ui.__mem_func__(self.__OverInItem))
		self.Objects["DropGridSlot"].SetOverOutItemEvent(ui.__mem_func__(self.__OverOutItem))
		self.Objects["DropGridSlot"].Show()

		## Filling grid
		for iSlot, (iVnum, iCount) in sortedGrid.items():
			self.Objects["DropGridSlot"].SetItemSlot(iSlot, iVnum, iCount)

		## Refreshing grid
		self.Objects["DropGridSlot"].RefreshSlot()

		self.dRewards = sortedGrid

	def	SortRewards(self, lRewards):
		sortedGrid = dict()
		sortedList = sorted(lRewards, key=lambda elem : elem[2], reverse=True)

		iGridY = 1
		iX, iY = 0, 0
		matrix = dict()

		for iVnum, iCount, iSize in sortedList:
			if not iX+(iY*self.GRID_MAX_X) in matrix:
				## If item is longer that grid, extend it
				if iSize+iY > iGridY:
					iGridY = iSize+iY

				## Block slots below
				for x in xrange(iSize):
					matrix[iX + x*self.GRID_MAX_X] = 1

				## Put item into appropriate position
				sortedGrid[iX + iY*self.GRID_MAX_X] = (iVnum, iCount)

			iX += 1
			if iX >= self.GRID_MAX_X-1:
				iY += 1
				iX = 0

		return (sortedGrid, (self.GRID_MAX_X, iGridY))

	""" Broadcast """
	def	ClearInteface(self):
		self.Objects["TaskListBox"].RemoveAllItems()
		self.Objects["RankingListBox"].RemoveAllItems()

		self.lRewards = []

	def	RegisterBasicInfo(self, iDiff, iCurrentDT, iFinished, iCollected):
		self.Objects["BasicInfo"]["Difficulity"].SetText(localeInfo.BATTLE_PASS_DIFFICULITY % self.TRANSLATION_UNIT["DIFFICULITY"][iDiff])
		self.Objects["BasicInfo"]["Month"].SetText(localeInfo.BATTLE_PASS_CURRENT_MONTH % self.TRANSLATION_UNIT["MONTHS"][self.__GetMonth(iCurrentDT)])
		self.Objects["BasicInfo"]["Finished"].SetText(localeInfo.BATTLE_PASS_FINISHED_AT % (self.__DTToString(iFinished) if iFinished > 0 else "-"))
		self.Objects["BasicInfo"]["RewardCollected"].SetText(localeInfo.BATTLE_PASS_REWARD_COLLECTED % (localeInfo.YES if iCollected > 0 else localeInfo.NO))

		## Saving endtime
		self.ttEndDT = self.__CountEndTime(iCurrentDT)

	def	RegisterMajorReward(self, iVnum, iCount):
		item.SelectItem(iVnum)
		self.lRewards.append((iVnum, iCount, item.GetItemSize()[1]))

	def	RegisterTaskData(self, sTitle, sDesc, iProgress, iTaskID):
		if len(self.Objects["TaskListBox"].itemList) <= iTaskID:
			self.Objects["TaskListBox"].AppendItem(self.TaskObject(self, self.Objects["TaskListBox"], sTitle, sDesc, iProgress))
		else:
			self.Objects["TaskListBox"].itemList[iTaskID].SetTaskProgress(iProgress)

		## Recalculating total progress
		self.Objects["BasicInfo"]["Progress"].SetText(localeInfo.BATTLE_PASS_TOTAL_PROGRESS % self.__RecalculateTotalProgress())

	def	RegisterTaskReward(self, iTaskID, iVnum, iCount):
		self.Objects["TaskListBox"].itemList[iTaskID].AddReward(iVnum, iCount)

	def	RegisterHighScore(self, iID, sName, iDt):
		self.Objects["RankingListBox"].AppendItem(self.RankingObject(iID+1, sName, self.__DTToString(iDt)))
	""" """

	def	__OverInItem(self, slotNum):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()

			if slotNum in self.dRewards:
				self.tooltipItem.AddItemData(self.dRewards[slotNum][0], [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])

			self.tooltipItem.ShowToolTip()

	def	__OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def	__ChangeSite(self, iType = -1):
		self.currentType = iType if iType > -1 else int(not self.currentType)

		## Replace button outfit
		self.Objects["BasicInfo"]["RadioButton"].SetUpVisual(self.OPTION_BUTTONS[self.currentType][0])
		self.Objects["BasicInfo"]["RadioButton"].SetOverVisual(self.OPTION_BUTTONS[self.currentType][1])
		self.Objects["BasicInfo"]["RadioButton"].SetDownVisual(self.OPTION_BUTTONS[self.currentType][2])

		## Render appropriate dialog
		self.OPTION_BUTTONS[self.currentType][4].Hide()
		self.OPTION_BUTTONS[self.currentType][3].Show()

	def	__RequestReward(self):
		net.SendChatPacket("/battle_pass_collect_reward")

	def	__ShowMajorRewards(self):
		## Sort it and print
		(sortedGrid, slotSize) = self.SortRewards(self.lRewards)
		self.OpenDropDialog(sortedGrid, slotSize)

	def	__CountEndTime(self, iCurrentDT):
		dtNow = datetime.fromtimestamp(iCurrentDT)

		iYear = int(dtNow.strftime("%Y"))
		iMonth = int(dtNow.strftime("%m"))

		## In case if we hit eoty - switch month back to january
		if iMonth == len(self.TRANSLATION_UNIT["MONTHS"])-1:
			iMonth = 1
		else:
			iMonth += 1

		## Upgrade year in case if month is january
		if iMonth == 1:
			iYear += 1

		dtFuture = datetime(iYear, iMonth, 1)
		return app.GetTime() + (dtFuture-dtNow).total_seconds()

	def	__DTToString(self, iCurrentDT):
		return datetime.fromtimestamp(iCurrentDT).strftime("%Y-%m-%d, %H:%M:%S")

	def	__GetMonth(self, iCurrentDT):
		return int(datetime.fromtimestamp(iCurrentDT).strftime("%m"))

	def	__RecalculateTotalProgress(self):
		totalValue, totalProgress = 0, 0

		for obj in self.Objects["TaskListBox"].itemList:
			totalValue += 100
			totalProgress += obj.GetProgress()

		return max(1, totalProgress)*100/totalValue

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.Show()

	def	OnUpdate(self):
		if self.ttEndDT > 0:
			self.Objects["BasicInfo"]["Remaining"].SetText(localeInfo.BATTLE_PASS_REMAINING_TIME % localeInfo.SecondToDHM(self.ttEndDT-app.GetTime() if self.ttEndDT > app.GetTime() else "-"))


