import app
import ui
import uiToolTip
import uiCommon
import mouseModule
import constInfo
import localeInfo
import net
import player
import item
import chr
import effect
import dbg
import background
import grp
import chat
import wndMgr

ENABLE_COMPLETION_EFFECT = True

class FindLettersWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.Initialize()
		self.LoadWindow()

	def Initialize(self):
		self.titleBar = None
		self.titleLetters = None
		self.lettersWindowBack = None
		self.lettersWindow = None
		self.errorPopup = None
		self.questionDialog = None

		if ENABLE_COMPLETION_EFFECT:
			self.scoreTextEffect = None
			self.scoreEffect1 = None
			self.scoreEffect2 = None
			self.scoreEffect3 = None

		self.letterBackSlotList = []
		self.letterSlotList = []
		self.lettersDict = {}

		self.rewardStart = 0
		self.rewardList = []
		self.rewardText = []
		self.rewardDict = {}

		self.rewardLeftButton = None
		self.rewardRightButton = None
		self.tooltipItem = None

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Initialize()

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/FindLettersWindow.py")
		except:
			import exception
			exception.Abort("FindLettersWindow.LoadDialog.LoadScript")

		try:
			self.titleBar = self.GetChild("TitleBar")
			self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

			self.titleLetters = self.GetChild("LettersTitleText")

			self.lettersWindowBack = self.GetChild("LettersWindowBack")
			self.lettersWindow = self.GetChild("LettersWindow")

			if ENABLE_COMPLETION_EFFECT:
				self.scoreTextEffect = self.GetChild("score_completion_text_effect")
				self.scoreTextEffect.SetEndFrameEvent( ui.__mem_func__(self.__ScoreTextEffectEndFrameEvent) )
				self.scoreTextEffect.Hide()

				self.scoreEffect1 = self.GetChild("score_completion_effect1")
				self.scoreEffect2 = self.GetChild("score_completion_effect2")
				self.scoreEffect3 = self.GetChild("score_completion_effect3")
				self.scoreEffect1.Hide()
				self.scoreEffect2.Hide()
				self.scoreEffect3.Hide()
				self.scoreEffect1.SetEndFrameEvent(ui.__mem_func__(self.__ScoreEffectEndFrameEvent1))
				self.scoreEffect2.SetEndFrameEvent(ui.__mem_func__(self.__ScoreEffectEndFrameEvent2))
				self.scoreEffect3.SetEndFrameEvent(ui.__mem_func__(self.__ScoreEffectEndFrameEvent3))

				self.scoreEffect1.SetKeyFrameEvent(ui.__mem_func__(self.__ScoreEffectKeyFrameEvent1))
				self.scoreEffect2.SetKeyFrameEvent(ui.__mem_func__(self.__ScoreEffectKeyFrameEvent2))

				self.__ClearScoreCompletionEffect()

			self.rewardLeftButton = self.GetChild("RewardLeftButton")
			self.rewardRightButton = self.GetChild("RewardRightButton")
		except:
			import exception
			exception.Abort("FindLettersWindow.LoadDialog.BindObject")

		self.rewardLeftButton.SetEvent(ui.__mem_func__(self.OnClickPrevReward))
		self.rewardRightButton.SetEvent(ui.__mem_func__(self.OnClickNextReward))

		self.tooltipItem = uiToolTip.ItemToolTip()
		self.tooltipItem.Hide()

		for i in xrange(20):
			tempSlotBack = ui.ImageBox()
			tempSlotBack.SetParent(self.lettersWindowBack)
			tempSlotBack.Show()
			self.letterBackSlotList.append(tempSlotBack)

			tempSlot = ui.SlotWindow()
			tempSlot.SetParent(self.lettersWindow)
			tempSlot.AppendSlot(0, 0, 0, 32, 32)
			tempSlot.SetSize(32, 32)
			tempSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectLetterSlot), i)
			tempSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectLetterSlot), i)
			tempSlot.Show()
			self.letterSlotList.append(tempSlot)

		for i in xrange(4):
			tempImg = ui.ImageBox()
			tempImg.SetParent(self.GetChild("RewardImageBG%d" % i))
			tempImg.SetEvent(ui.__mem_func__(self.OverInItem), "MOUSE_OVER_IN", i)
			tempImg.SetEvent(ui.__mem_func__(self.OverOutItem), "MOUSE_OVER_OUT")
			tempImg.SetWindowHorizontalAlignCenter()
			tempImg.SetWindowVerticalAlignCenter()
			tempImg.SetPosition(0, -9)
			tempImg.Show()
			self.rewardList.append(tempImg)

			tempText = ui.TextLine()
			tempText.SetParent(self.GetChild("RewardImageBG%d" % i))
			tempText.SetWindowHorizontalAlignCenter()
			tempText.SetWindowVerticalAlignBottom()
			tempText.SetHorizontalAlignCenter()
			tempText.SetPosition(0, 16)
			tempText.Show()
			self.rewardText.append(tempText)

	def AddLetter(self, iPos, iAsciiChar, iIsFilled):
		if self.lettersDict.has_key(iPos):
			self.lettersDict[iPos][0] = iAsciiChar
			self.lettersDict[iPos][1] = iIsFilled

			self.RefreshSlots()
		else:
			self.lettersDict[iPos] = [ iAsciiChar, iIsFilled ]

	def AddReward(self, iPos, itemVnum, itemCount):
		if self.rewardDict.has_key(iPos):
			self.rewardDict[iPos][0] = itemVnum
			self.rewardDict[iPos][1] = itemCount

			self.RefreshSlots()
		else:
			self.rewardDict[iPos] = [ itemVnum, itemCount ]

	def FinishEvent(self):
		self.lettersDict = {}
		for img in self.letterBackSlotList:
			img.Hide()

		for slot in self.letterSlotList:
			slot.Hide()

		if ENABLE_COMPLETION_EFFECT:
			self.__ClearScoreCompletionEffect()
			self.scoreEffect1.Show()

	def GetPhase(self):
		phase = ""
		for key, value in self.lettersDict.iteritems():
			if value[0] == 0:
				continue

			if value[0] == 95:
				phase += " "
			else:
				phase += "%c" % value[0]

		return phase.title()

	def GetRowSize(self):
		rowSize = { 1 : 0, 2 : 0 }
		for i in xrange(20):
			x, y = self.letterSlotList[i].GetLocalPosition()

			if y == 0:
				rowSize[1] += 42
			elif y == 50:
				rowSize[2] += 42
			elif y == -75:
				rowSize[1] += 22
			elif y == -76:
				rowSize[2] += 22

		return rowSize

	def SetRowsAlignCenter(self):
		rowSize = self.GetRowSize()

		for i in xrange(20):
			x, y = self.letterSlotList[i].GetLocalPosition()

			if y == 0:
				self.letterBackSlotList[i].SetPosition((446 - rowSize[1]) / 2 + x, y)
				self.letterSlotList[i].SetPosition((446 - rowSize[1]) / 2 + x, y)
			elif y == 50:
				self.letterBackSlotList[i].SetPosition((446 - rowSize[2]) / 2 + x, y)
				self.letterSlotList[i].SetPosition((446 - rowSize[2]) / 2 + x, y)

	def ArangeSlots(self):
		startPos, curX, curRow = 0, 0, 1

		for key, value in self.lettersDict.iteritems():
			if not value[0]:
				self.letterSlotList[key].SetPosition(402, -73)
				self.letterSlotList[key].Hide()
				continue

			if value[0] == 95:
				startPos = key
				curX += 15
				self.letterSlotList[key].SetPosition(402, -74 - curRow)
				self.letterSlotList[key].Hide()
				continue

			if curX >= 420:
				curX = 0
				curRow += 1
				self.letterSlotList[startPos].SetPosition(402, -72)
				self.letterSlotList[startPos].Hide()
				for i in range(startPos + 1, key):
					self.letterBackSlotList[i].SetPosition(curX, 50 * (curRow - 1))
					self.letterBackSlotList[i].Show()
					self.letterSlotList[i].SetPosition(curX, 50 * (curRow - 1))
					self.letterSlotList[i].Show()
					curX += 42

			self.letterBackSlotList[key].SetPosition(curX, 50 * (curRow - 1))
			self.letterBackSlotList[key].Show()
			self.letterSlotList[key].SetPosition(curX, 50 * (curRow - 1))
			self.letterSlotList[key].Show()
			curX += 42

		self.SetRowsAlignCenter()

	def RefreshSlots(self):
		for key, value in self.lettersDict.iteritems():
			if value[0] == 0 or value[0] == 95:
				continue

			image = "d:/ymir work/ui/game/find_letters/full_slot.tga"
			iconAlpha = 1.0
			if not value[1]:
				image = "d:/ymir work/ui/game/find_letters/empty_slot.tga"
				iconAlpha = 0.5

			self.letterBackSlotList[key].LoadImage(image)

			realVnum = 90500 + value[0]
			item.SelectItem(realVnum)
			itemIcon = item.GetIconImage()
			(width, height) = item.GetItemSize()
			self.letterSlotList[key].ClearSlot(0)
			self.letterSlotList[key].SetSlot(0, 0, width, height, itemIcon, (1.0, 1.0, 1.0, iconAlpha))
			self.letterSlotList[key].SetSlotCount(0, 0)

			if not value[1]:
				emptyCover = "d:/ymir work/ui/game/find_letters/empty_slot_cover.tga"
				self.letterSlotList[key].SetCoverButton(0, emptyCover, emptyCover, emptyCover, emptyCover, False, False)
				self.letterSlotList[key].SetAlwaysRenderCoverButton(0, True)
			else:
				self.letterSlotList[key].DeleteCoverButton(0)

	def OverInItem(self, eventType, rewardIndex):
		if self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			if self.rewardDict.has_key(self.rewardStart + rewardIndex):
				self.tooltipItem.AddItemData(self.rewardDict[self.rewardStart + rewardIndex][0], metinSlot = [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)])
				self.tooltipItem.ShowToolTip()

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnClickPrevReward(self):
		if self.rewardStart == 0:
			return

		self.rewardStart -= 1
		self.RefreshRewards()

	def OnClickNextReward(self):
		if self.rewardStart + 4 == len(self.rewardDict.keys()):
			return

		self.rewardStart += 1
		self.RefreshRewards()

	def RefreshRewards(self):
		for img in self.rewardList:
			img.Hide()

		for text in self.rewardText:
			text.Hide()

		self.rewardLeftButton.Show()
		self.rewardRightButton.Show()
		if self.rewardStart == 0:
			self.rewardLeftButton.Hide()

		if self.rewardStart + 4 == len(self.rewardDict.keys()):
			self.rewardRightButton.Hide()

		for i in xrange(4):
			if i < len(self.rewardList) and i < len(self.rewardText) and self.rewardDict.has_key(self.rewardStart + i):
				item.SelectItem(self.rewardDict[self.rewardStart + i][0])
				self.rewardList[i].LoadImage(item.GetIconImageFileName())
				self.rewardList[i].Show()

				#self.rewardText[i].SetText("%d x %s" % (self.rewardDict[self.rewardStart + i][1], str(item.GetItemName())))
				self.rewardText[i].SetText("(x%d) szt." % self.rewardDict[self.rewardStart + i][1])
				self.rewardText[i].Show()

	def SelectLetterSlot(self, slotNumber, letterIndex = 0):
		print "SelectLetterSlot", slotNumber, letterIndex
		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			mouseModule.mouseController.DeattachObject()

			if attachedItemIndex < 90500 or attachedItemIndex > 90600: # not a letter
				return False

			letterAscii = attachedItemIndex % 100
			if (letterAscii < 48 or (letterAscii > 57 and letterAscii < 65) and letterAscii > 90): # not a valid letter
				self.OpenErrorPopup(translate("This is not a valid letter."))
				return False

			if not self.lettersDict.has_key(letterIndex): # not a letter slot
				self.OpenErrorPopup(translate("This slot can't be filled."))
				return False

			if self.lettersDict[letterIndex][0] != letterAscii: # different letter
				self.OpenErrorPopup(translate("This letter can't go in this slot."))
				return False

			if self.lettersDict[letterIndex][1] == 1: # Already a letter here
				self.OpenErrorPopup(translate("This slot already have a letter."))
				return False

			self.OpenQuestionDialog(letterIndex, attachedSlotPos)

	def OpenErrorPopup(self, message):
		if not self.errorPopup:
			errorPopup = uiCommon.PopupDialog()
			self.errorPopup = errorPopup

		self.errorPopup.SetText(message)
		self.errorPopup.SetAutoClose(True)
		self.errorPopup.Open()

	def OpenQuestionDialog(self, letterIndex, slotPos):
		if not self.questionDialog:
			questionDialog = uiCommon.QuestionDialog()
			questionDialog.SetText(translate("Are you sure you want to add this letter here ?"))
			questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnAddLetterAccept))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog = questionDialog

		self.questionDialog.Open()
		self.questionDialog.letterIndex = letterIndex
		self.questionDialog.slotPos = slotPos

	def OnAddLetterAccept(self):
		if None == self.questionDialog:
			return

		net.SendChatPacket("/find_letters_add %d %d" % (self.questionDialog.letterIndex, self.questionDialog.slotPos))
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def Destroy(self):
		self.ClearDictionary()
		self.Initialize()

	def Open(self):
		self.ArangeSlots()
		self.RefreshSlots()
		self.RefreshRewards()

		self.titleLetters.SetText(self.GetPhase())

		self.Show()
		self.SetCenterPosition()
		self.SetTop()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	if ENABLE_COMPLETION_EFFECT:
		def __ClearScoreCompletionEffect(self):
			if self.scoreTextEffect:
				self.scoreTextEffect.Hide()
				self.scoreTextEffect.ResetFrame()
				self.scoreTextEffect.SetDelay(6)

			if self.scoreEffect1:
				self.scoreEffect1.Hide()
				self.scoreEffect1.ResetFrame()
				self.scoreEffect1.SetDelay(6)

			if self.scoreEffect2:
				self.scoreEffect2.Hide()
				self.scoreEffect2.ResetFrame()
				self.scoreEffect2.SetDelay(6)

			if self.scoreEffect3:
				self.scoreEffect3.Hide()
				self.scoreEffect3.ResetFrame()
				self.scoreEffect3.SetDelay(6)

		def __ScoreTextEffectEndFrameEvent(self):
			if self.scoreTextEffect:
				self.scoreTextEffect.Hide()

			self.Close()

		def __ScoreEffectKeyFrameEvent1(self, cur_frame):
			if cur_frame == 2:
				if self.scoreTextEffect:
					self.scoreTextEffect.Show()
				if self.scoreEffect2:
					self.scoreEffect2.Show()

		def __ScoreEffectKeyFrameEvent2(self, cur_frame):
			if cur_frame == 1:
				if self.scoreEffect3:
					self.scoreEffect3.Show()

		def __ScoreEffectEndFrameEvent1(self):
			if self.scoreEffect1:
				self.scoreEffect1.Hide()

		def __ScoreEffectEndFrameEvent2(self):
			if self.scoreEffect2:
				self.scoreEffect2.Hide()

		def __ScoreEffectEndFrameEvent3(self):
			if self.scoreEffect3:
				self.scoreEffect3.Hide()

class FindLettersButton(ui.Window):
	def __init__(self):
		ui.Window.__init__(self)

		self.SetPosition(wndMgr.GetScreenWidth() - 260, 10)
		self.SetSize(124, 60)

		self.openButton = None
		self.Initialize()

	def __del__(self):
		ui.Window.__del__(self)

	def Destroy(self):
		self.openButton = None

	def Initialize(self):
		self.openButton = ui.Button()
		self.openButton.SetParent(self)
		self.openButton.SetPosition(0, 0)
		self.openButton.SetUpVisual("d:/ymir work/ui/game/find_letters/open_button_01.tga")
		self.openButton.SetOverVisual("d:/ymir work/ui/game/find_letters/open_button_02.tga")
		self.openButton.SetDownVisual("d:/ymir work/ui/game/find_letters/open_button_03.tga")
		self.openButton.SetEvent(ui.__mem_func__(self.RequestOpenFindLetters))
		self.openButton.Hide()

	def BindInterface(self, interface):
		self.interface = interface

	def RequestOpenFindLetters(self):
		if self.interface:
			if self.interface.wndFindLettersWindow:
				if self.interface.wndFindLettersWindow.IsShow():
					self.interface.wndFindLettersWindow.Close()
					return

		net.SendChatPacket("/find_letters_request")

	def ShowButton(self):
		if self.openButton:
			self.openButton.Show()

	def HideButton(self):
		if self.openButton:
			self.openButton.Hide()