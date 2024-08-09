from re import S
import app
import net
import player
import item
import ui
import uiToolTip
import mouseModule
import localeInfo
import uiCommon
import constInfo
if gcGetEnable("ENABLE_REFINE_ITEM_DESCRIPTION"):
	TOOLTIP_DATA = {
		'materials' : [],
		'slot_count': 0
	}

import introInterface
import interfaceModule
import wndMgr

import colorInfo

if gcGetEnable("ENABLE_LOCK_EFFECTS"):
	REFINE_COLOUR = (0.6, 0.9, 1.0, 0.3)

class RefineDialog(ui.ScriptWindow):

	makeSocketSuccessPercentage = ( 100, 33, 20, 15, 10, 5, 0 )
	upgradeStoneSuccessPercentage = ( 30, 29, 28, 27, 26, 25, 24, 23, 22 )
	upgradeArmorSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )
	upgradeAccessorySuccessPercentage = ( 99, 88, 77, 66, 33, 33, 33, 33, 33 )
	upgradeSuccessPercentage = ( 99, 66, 33, 33, 33, 33, 33, 33, 33 )

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadScript()

		self.scrollItemPos = 0
		self.targetItemPos = 0

	def __LoadScript(self):

		self.__LoadQuestionDialog()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refinedialog.py")

		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.successPercentage = self.GetChild("SuccessPercentage")
			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.Close)
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.BindObject")

		##if 936 == app.GetDefaultCodePage():
		if constInfo.ENABLE_REFINE_PCT:
			self.successPercentage.Show()
		else:
			self.successPercentage.Hide()

		toolTip = uiToolTip.ItemToolTip()
		toolTip.SetParent(self)
		toolTip.SetPosition(15, 38)
		toolTip.SetFollow(False)
		toolTip.Show()
		self.toolTip = toolTip

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.Close))

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __LoadQuestionDialog(self):
		self.dlgQuestion = ui.ScriptWindow()

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self.dlgQuestion, "uiscript/questiondialog2.py")
		except:
			import exception
			exception.Abort("RefineDialog.__LoadQuestionDialog.LoadScript")

		try:
			GetObject=self.dlgQuestion.GetChild
			GetObject("message1").SetText(localeInfo.REFINE_DESTROY_WARNING)
			GetObject("message2").SetText(localeInfo.REFINE_WARNING2)
			GetObject("accept").SetEvent(ui.__mem_func__(self.Accept))
			GetObject("cancel").SetEvent(ui.__mem_func__(self.dlgQuestion.Hide))
		except:
			import exception
			exception.Abort("SelectCharacterWindow.__LoadQuestionDialog.BindObject")

	def Destroy(self):
		self.ClearDictionary()
		self.board = 0
		self.successPercentage = 0
		self.titleBar = 0
		self.toolTip = 0
		self.dlgQuestion = 0

	def GetRefineSuccessPercentage(self, scrollSlotIndex, itemSlotIndex):

		if -1 != scrollSlotIndex:
			if player.IsRefineGradeScroll(scrollSlotIndex):
				curGrade = player.GetItemGrade(itemSlotIndex)
				itemIndex = player.GetItemIndex(itemSlotIndex)

				item.SelectItem(itemIndex)
				itemType = item.GetItemType()
				itemSubType = item.GetItemSubType()

				if item.ITEM_TYPE_METIN == itemType:

					if curGrade >= len(self.upgradeStoneSuccessPercentage):
						return 0
					return self.upgradeStoneSuccessPercentage[curGrade]

				elif item.ITEM_TYPE_ARMOR == itemType:

					if item.ARMOR_BODY == itemSubType:
						if curGrade >= len(self.upgradeArmorSuccessPercentage):
							return 0
						return self.upgradeArmorSuccessPercentage[curGrade]
					else:
						if curGrade >= len(self.upgradeAccessorySuccessPercentage):
							return 0
						return self.upgradeAccessorySuccessPercentage[curGrade]

				else:

					if curGrade >= len(self.upgradeSuccessPercentage):
						return 0
					return self.upgradeSuccessPercentage[curGrade]

		for i in xrange(player.METIN_SOCKET_MAX_NUM+1):
			if 0 == player.GetItemMetinSocket(itemSlotIndex, i):
				break

		return self.makeSocketSuccessPercentage[i]

	def Open(self, scrollItemPos, targetItemPos):
		self.scrollItemPos = scrollItemPos
		self.targetItemPos = targetItemPos

		percentage = self.GetRefineSuccessPercentage(scrollItemPos, targetItemPos)

		if 0 == percentage:
			return
		self.successPercentage.SetText(localeInfo.REFINE_SUCCESS_PROBALITY % (percentage))

		itemIndex = player.GetItemIndex(targetItemPos)
		self.toolTip.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))
		if app.ENABLE_TRANSMUTATION_SYSTEM:
			self.toolTip.AddItemData(itemIndex, metinSlot, 0, 0, player.GetItemTransmutate(targetItemPos))
		else:
			self.toolTip.AddItemData(itemIndex, metinSlot)

		self.UpdateDialog()
		self.SetTop()
		self.Show()

	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 30
		newHeight = self.toolTip.GetHeight() + 98
		self.board.SetSize(newWidth, newHeight)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	def OpenQuestionDialog(self):
		percentage = self.GetRefineSuccessPercentage(-1, self.targetItemPos)
		if 100 == percentage:
			self.Accept()
			return

		self.dlgQuestion.SetTop()
		self.dlgQuestion.Show()

	def Accept(self):
		net.SendItemUseToItemPacket(self.scrollItemPos, self.targetItemPos)
		self.Close()

	def Close(self):
		self.dlgQuestion.Hide()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True

class RefineDialogNew(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()
		self.isLoaded = False

	def __Initialize(self):
		self.dlgQuestion = None
		self.children = []
		self.vnum = 0
		self.targetItemPos = 0
		self.dialogHeight = 0
		self.cost = 0
		self.percentage = 0
		self.type = 0

		if app.ENABLE_FAST_REFINE_OPTION:
			self.isRefined = False

	def __LoadScript(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/refinedialog.py")

		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.LoadObject")

		try:
			self.board = self.GetChild("Board")
			self.titleBar = self.GetChild("TitleBar")
			self.probText = self.GetChild("SuccessPercentage")
			self.costText = self.GetChild("Cost")
			self.successPercentage = self.GetChild("SuccessPercentage")
			self.GetChild("AcceptButton").SetEvent(self.OpenQuestionDialog)
			self.GetChild("CancelButton").SetEvent(self.CancelRefine)
		except:
			import exception
			exception.Abort("RefineDialog.__LoadScript.BindObject")

		if constInfo.ENABLE_REFINE_PCT:
			self.successPercentage.Show()
		else:
			self.successPercentage.Hide()

		toolTip = uiToolTip.ItemToolTip()
		toolTip.SetParent(self)
		toolTip.SetFollow(False)
		toolTip.SetPosition(15, 38)
		toolTip.Show()
		self.toolTip = toolTip

		self.slotList = []
		for i in xrange(3):
			slot = self.__MakeSlot()
			slot.SetParent(toolTip)
			slot.SetWindowVerticalAlignCenter()
			self.slotList.append(slot)

		itemImage = self.__MakeItemImage()
		itemImage.SetParent(toolTip)
		itemImage.SetWindowVerticalAlignCenter()
		itemImage.SetPosition(-35, 0)
		self.itemImage = itemImage

		self.titleBar.SetCloseEvent(ui.__mem_func__(self.CancelRefine))
		if app.ENABLE_FAST_REFINE_OPTION:
			self.TitleToolTip = uiToolTip.ToolTip()
			self.TitleToolTip.ClearToolTip()

			self.titleBar.HandleButtonState("BTN_CHBOX", True)
			self.titleBar.HandleButtonGetter("BTN_CHBOX").SetOverEvent(ui.__mem_func__(self.__CreateToolTip))
			self.titleBar.HandleButtonGetter("BTN_CHBOX").SetOverOutEvent(ui.__mem_func__(self.__HideToolTip))

		if gcGetEnable("ENABLE_REFINE_ITEM_DESCRIPTION"):
			self.tooltipItem = uiToolTip.ItemToolTip()
			self.tooltipItem.Hide()

		self.isLoaded = True

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def __MakeSlot(self):
		slot = ui.ImageBox()
		slot.LoadImage("d:/ymir work/ui/public/slot_base.sub")
		slot.Show()
		self.children.append(slot)
		return slot

	def __MakeItemImage(self):
		itemImage = ui.ImageBox()
		itemImage.Show()
		self.children.append(itemImage)
		return itemImage

	def __MakeThinBoard(self):
		thinBoard = ui.ThinBoard()
		thinBoard.SetParent(self)
		thinBoard.Show()
		self.children.append(thinBoard)
		return thinBoard

	def Destroy(self):
		self.ClearDictionary()
		self.dlgQuestion = None
		self.board = 0
		self.probText = 0
		self.costText = 0
		self.titleBar = 0
		self.toolTip = 0
		self.successPercentage = None
		self.slotList = []
		self.children = []

	if app.ENABLE_FAST_REFINE_OPTION:
		def IsRefined(self):
			return self.isRefined == True

	def Open(self, targetItemPos, nextGradeItemVnum, cost, prob, type, can_fast_refine, addPercent, iSashRefine):
		if False == self.isLoaded:
			self.__LoadScript()

		if app.ENABLE_FAST_REFINE_OPTION:
			isRefined = self.IsRefined()
		self.__Initialize()

		if app.ENABLE_FAST_REFINE_OPTION:
			if not self.IsShow() or not can_fast_refine:
				self.titleBar.HandleButtonGetter("BTN_CHBOX").SetChecked(False)

			self.titleBar.HandleButtonGetter("BTN_CHBOX").SetVisible(can_fast_refine)

		self.targetItemPos = targetItemPos
		self.vnum = nextGradeItemVnum
		self.cost = cost
		self.percentage = prob

		addChance = 0
		self.type = type

		addChance += addPercent

		sText = localeInfo.REFINE_SUCCESS_PROBALITY

		if addChance:
			sText = sText % self.percentage
			fIndex = sText.find(str(self.percentage))

			sText = sText[:fIndex] + colorInfo.Colorize(sText[fIndex:], 0xFFf4be00) + colorInfo.Colorize(" ({}%)".format(addChance), 0xFF82ff7d)
			self.probText.SetText(sText)
		else:
			sText = sText % self.percentage
			fIndex = sText.find(str(self.percentage))

			sText = sText[:fIndex] + colorInfo.Colorize(sText[fIndex:], 0xFFf4be00)
			self.probText.SetText(sText)

		bPrice = localeInfo.NumberToStringAsType(self.cost, True, "")
		self.costText.SetText(localeInfo.REFINE_COST_NEW + " {}".format(bPrice))
		self.costText.SetPackedFontColor(0xffdddddd)

		self.toolTip.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(targetItemPos, i))

		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(targetItemPos, i))
		if app.ENABLE_TRANSMUTATION_SYSTEM:
			if app.ENABLE_REFINE_ELEMENT:
				self.toolTip.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot, type, player.GetItemTransmutate(targetItemPos), player.GetItemRefineElement(targetItemPos), sashRefineItem = iSashRefine)
			else:
				self.toolTip.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot, type, player.GetItemTransmutate(targetItemPos))
		else:
			if app.ENABLE_REFINE_ELEMENT:
				self.toolTip.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot, type, player.GetItemRefineElement(targetItemPos))
			else:
				self.toolTip.AddRefineItemData(nextGradeItemVnum, metinSlot, attrSlot, type)

		item.SelectItem(nextGradeItemVnum)
		self.itemImage.LoadImage(item.GetIconImageFileName())
		xSlotCount, ySlotCount = item.GetItemSize()
		for slot in self.slotList:
			slot.Hide()
		for i in xrange(min(3, ySlotCount)):
			self.slotList[i].SetPosition(-35, i*32 - (ySlotCount-1)*16)
			self.slotList[i].Show()

		if app.ENABLE_FAST_REFINE_OPTION:
			self.dialogHeight = self.toolTip.GetHeight() + 46

			if self.IsShow() and self.HandleReturnButton() and isRefined:
				self.OpenQuestionDialog(True)
		else:
			self.dialogHeight = self.toolTip.GetHeight() + 46

		if gcGetEnable("ENABLE_LOCK_EFFECTS"):
			interfaceModule.GetInstance().wndInventory.EraseLockElement("REFINE")
			interfaceModule.GetInstance().wndInventory.RegisterLockColour("REFINE", REFINE_COLOUR)

		self.UpdateDialog()

		self.SetTop()
		self.Show()

	def Close(self):
		if gcGetEnable("ENABLE_LOCK_EFFECTS"):
			interfaceModule.GetInstance().wndInventory.EraseLockElement("REFINE")
			interfaceModule.GetInstance().wndInventory.RefreshWindows()

		self.dlgQuestion = None
		self.Hide()

	if gcGetEnable("ENABLE_REFINE_ITEM_DESCRIPTION"):
		def __MakeItemSlot(self, slotIndex):
			slot = ui.SlotWindow()
			slot.SetParent(self)
			slot.SetSize(32, 32)
			slot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
			slot.AppendSlot(slotIndex, 0, 0, 32, 32)
			slot.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
			slot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
			slot.SetSelectItemSlotEvent(ui.__mem_func__(self.OnSelectSlot))

			slot.RefreshSlot()
			slot.Show()
			self.children.append(slot)
			return slot

		def OverInItem(self, slotIndex):
			if slotIndex > len(TOOLTIP_DATA['materials']):
				return

			if self.tooltipItem:
				self.tooltipItem.ClearToolTip()
				self.tooltipItem.AddItemData(TOOLTIP_DATA['materials'][slotIndex], 0, 0, 0, 0, window_type = player.INVENTORY)

				self.tooltipItem.AlignHorizonalCenter()

				self.tooltipItem.ShowToolTip()

				if app.INGAME_WIKI:
					self.tooltipItem.AppendShortcut(*(introInterface.GetWindowConfig("shortcust_windows", introInterface.WIKI_WND, "desc")))

		def OverOutItem(self):
			if self.tooltipItem:
				self.tooltipItem.HideToolTip()

		def OnSelectSlot(self, slotIndex):
			itemIndex = TOOLTIP_DATA['materials'][slotIndex]
			if app.IsPressed(introInterface.GetWindowConfig("shortcust_windows", introInterface.WIKI_WND, "key")) and app.INGAME_WIKI:
				interfaceModule.GetInstance().wikiExtension_searchVnum(itemIndex)

	def AppendMaterial(self, vnum, count):
		if gcGetEnable("ENABLE_REFINE_ITEM_DESCRIPTION"):
			slotIndex = len(TOOLTIP_DATA['materials'])

			slot = self.__MakeItemSlot(slotIndex)
			slot.SetPosition(15, self.dialogHeight - 10)
			slot.SetItemSlot(slotIndex, vnum, count)

			TOOLTIP_DATA['materials'].append(vnum)

		else:
			slot = self.__MakeSlot()
			slot.SetParent(self)
			slot.SetPosition(15, self.dialogHeight - 10)

			itemImage = self.__MakeItemImage()
			itemImage.SetParent(slot)
			item.SelectItem(vnum)
			itemImage.LoadImage(item.GetIconImageFileName())

		thinBoard = self.__MakeThinBoard()
		if app.ENABLE_FAST_REFINE_OPTION:
			thinBoard.SetPosition(50, self.dialogHeight - 10)
		else:
			thinBoard.SetPosition(50, self.dialogHeight)
		thinBoard.SetSize(191, 20)

		textLine = ui.TextLine()
		textLine.SetParent(thinBoard)
		textLine.SetFontName(localeInfo.UI_DEF_FONT)

		if gcGetEnable("ENABLE_REFINE_MARKING_REQUIRED"):
			if player.GetItemCountByVnum(vnum) < count:
				textLine.SetPackedFontColor(0xffFF0033)
			else:
				textLine.SetPackedFontColor(0xffdddddd)

		#textLine.SetPackedFontColor(0xffdddddd)
		if gcGetEnable("ENABLE_REFINE_MARKING_REQUIRED"):
			textLine.SetText("%s x%d (%d)" % (item.GetItemName(), count, player.GetItemCountByVnum(vnum)))
		else:
			textLine.SetText("%s x %02d" % (item.GetItemName(), count))

		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.SetWindowVerticalAlignCenter()
		textLine.SetVerticalAlignCenter()
		textLine.SetPosition(15, 0)

		textLine.Show()
		self.children.append(textLine)

		self.dialogHeight += 34

		if gcGetEnable("ENABLE_LOCK_EFFECTS"):
			interfaceModule.GetInstance().wndInventory.FindToLockSlot("REFINE", vnum)
			interfaceModule.GetInstance().wndInventory.RefreshWindows()

		self.UpdateDialog()

	def UpdateDialog(self):
		newWidth = self.toolTip.GetWidth() + 60
		newHeight = self.dialogHeight + 75
		newHeight -= 15

		self.board.SetSize(newWidth, newHeight)
		self.toolTip.SetPosition(15 + 35, 38)
		self.titleBar.SetWidth(newWidth-15)
		self.SetSize(newWidth, newHeight)

		(x, y) = self.GetLocalPosition()
		self.SetPosition(x, y)

	if app.ENABLE_FAST_REFINE_OPTION:
		def __CreateToolTip(self):
			if not self.TitleToolTip:
				return

			(pos_x, pos_y) = wndMgr.GetMousePosition()

			self.TitleToolTip.ClearToolTip()
			self.TitleToolTip.AppendShortcut([app.DIK_RETURN], localeInfo.QUICK_ACTION_CHECKBOX_REFINE, bCenter = True, bSpace = False)
			self.TitleToolTip.SetToolTipPosition(pos_x, pos_y - 5)
			self.TitleToolTip.Show()

		def __HideToolTip(self):
			if not self.TitleToolTip:
				return

			self.TitleToolTip.HideToolTip()

		def HandleReturnButton(self):
			return self.titleBar.HandleButtonGetter("BTN_CHBOX").IsChecked()

		def OnPressReturnKey(self):
			if self.HandleReturnButton():
				self.Accept()
				return True

	def OpenQuestionDialog(self, onlyQuestDlg = False):
		# if 100 == self.percentage:
		# 	self.Accept()
		# 	return

		# if 5 == self.type:
		# 	self.Accept()
		# 	return

		dlgQuestion = uiCommon.QuestionDialog2()
		dlgQuestion.SetText2(localeInfo.REFINE_WARNING2)
		dlgQuestion.SetAcceptEvent(ui.__mem_func__(self.Accept))
		dlgQuestion.SetCancelEvent(ui.__mem_func__(dlgQuestion.Close))

		if 3 == self.type:
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_1)
			dlgQuestion.SetText2(localeInfo.REFINE_DESTROY_WARNING_WITH_BONUS_PERCENT_2)
		elif 2 == self.type:
			dlgQuestion.SetText1(localeInfo.REFINE_DOWN_GRADE_WARNING)
		else:
			dlgQuestion.SetText1(localeInfo.REFINE_DESTROY_WARNING)


		if app.ENABLE_ORE_REFACTOR:
			item.SelectItem(self.vnum)
			iNextItem = (self.vnum / 10 != player.GetItemIndex(self.targetItemPos) / 10)

			if (iNextItem and (item.GetItemType() == item.ITEM_TYPE_WEAPON and item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR))):
				dlgQuestion.SetText2("Care! The ore will be removed!")

		dlgQuestion.Open()
		self.dlgQuestion = dlgQuestion

	def Accept(self):
		print "RefineAccept"
		if app.ENABLE_FAST_REFINE_OPTION:
			bCanRefine = self.HandleReturnButton()
			net.SendRefinePacket(self.targetItemPos, self.type, bCanRefine)
			self.isRefined = True

			if not bCanRefine:
				self.Close()
		else:
			net.SendRefinePacket(self.targetItemPos, self.type)
			self.Close()

	def CancelRefine(self):
		if gcGetEnable("ENABLE_REFINE_ITEM_DESCRIPTION"):
			TOOLTIP_DATA['materials'] = []
		net.SendRefinePacket(255, 255)
		self.Close()

	def OnPressEscapeKey(self):
		self.CancelRefine()
		return True
