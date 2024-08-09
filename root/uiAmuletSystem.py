import ui, itemWrapper, mouseModule, uiToolTip, uiScriptLocale, colorInfo, localeInfo
import net, player, item, util, chat
from _weakref import proxy

#TODO -> Let's do a simple function to handle whole state of buttons
ROOT_PATH = "assets/ui/amulet_system/{}"

class AmuletInformationClass(ui.ScriptWindow):
	## BASE | ADDITIONAL
	APPLY_CONFIGURATION = (2, 4)

	## Configuration
	UPGRADE_INFORMATION = dict()

	class RefineQuestion(ui.SimplyWindow):
		SIZE = (445, 235)

		def __init__(self, parent):
			ui.SimplyWindow.__init__(self, "UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)

			self.Objects["PARENT"] = proxy(parent)
			self.__BuildWindow()

		def __del__(self):
			ui.SimplyWindow.__del__(self)

			#@Private Methods
		def __Initialize(self):
			self.Objects = {}

		def __Destroy(self):
			self.Objects = {}

		def __BuildWindow(self):
			## Build base
			board = ui.MainBoardWithTitleBar()
			board.SetParent(self)
			board.SetPosition(0, 0)
			board.SetTitleName(uiScriptLocale.AMULET_SYSTEM_REFINE_TITLE)
			board.SetCloseEvent(ui.__mem_func__(self.Hide))
			board.SetSize(self.GetWidth(), self.GetHeight())
			board.Show()

			self.AppendObject("board", board)

			## Top Container
			background = ui.ImageBoxNew()
			background.SetParent(self.GetObject("board"))
			background.LoadImage(ROOT_PATH.format("information/question_dialog/top_bg.png"))
			background.SetPosition(0, 31)
			background.SetWindowHorizontalAlignCenter()
			background.Show()

			header = ui.ImageBox()
			header.SetParent(background)
			header.LoadImage(ROOT_PATH.format("information/question_dialog/top_header.png"))
			header.SetPosition(0, 1)
			header.SetWindowHorizontalAlignCenter()
			header.Show()

			header_text = ui.MakeTextLine(header)
			header_text.SetText(uiScriptLocale.AMULET_SYSTEM_REFINE_HEADER)
			
			## APPLY_TYPE
			apply_type_input = ui.ImageBoxNew()
			apply_type_input.SetParent(background)
			apply_type_input.LoadImage(ROOT_PATH.format("information/question_dialog/apply_input_0.png"))
			apply_type_input.SetPosition(7.5, header.GetHeight() + (background.GetHeight() - header.GetHeight()) / 2 - apply_type_input.GetHeight() / 2)
			apply_type_input.Show()

			apply_type_text = ui.MakeTextLine(apply_type_input)
			apply_type_text.SetText("-")

			## APPLY_STATE
			apply_state_input = ui.ImageBoxNew()
			apply_state_input.SetParent(apply_type_input)
			apply_state_input.LoadImage(ROOT_PATH.format("information/question_dialog/apply_input_1.png"))
			apply_state_input.SetPosition(0, 0)
			apply_state_input.SetWindowHorizontalAlignRight()
			apply_state_input.Show()

			apply_state_text = ui.MakeExtendedTextLine(apply_state_input)
			apply_state_text.SetText("--")

			self.AppendObject("top_container", (background, header, header_text, apply_type_input, apply_type_text, apply_state_input, apply_state_text, ))

			## Bottom Container
			background = ui.ImageBoxNew()
			background.SetParent(self.GetObject("board"))
			background.LoadImage(ROOT_PATH.format("information/question_dialog/bottom_bg.png"))
			background.SetPosition(0, background.GetHeight() + 7)
			background.SetWindowHorizontalAlignCenter()
			background.SetWindowVerticalAlignBottom()
			background.Show()

			text = ui.TextLine()
			text.SetParent(background)
			text.SetWindowHorizontalAlignCenter()
			text.SetWindowVerticalAlignCenter()
			text.SetHorizontalAlignCenter()
			text.SetVerticalAlignCenter()
			text.SetPosition(0, -10)
			text.SetText("")
			text.Show()

			button = [ui.Button() for _ in xrange(2)]
			button = tuple(button)

			lTexts = [uiScriptLocale.AMULET_SYSTEM_REFINE_BUTTON_ACCEPT, uiScriptLocale.AMULET_SYSTEM_REFINE_BUTTON_CLOSE]
			for _ in xrange(2):
				button[_].SetParent(background)
				button[_].SetWindowHorizontalAlignCenter()
				button[_].SetWindowVerticalAlignBottom()
				button[_].SetUpVisual(ROOT_PATH.format("information/question_dialog/btn_01.png"))
				button[_].SetOverVisual(ROOT_PATH.format("information/question_dialog/btn_02.png"))
				button[_].SetDownVisual(ROOT_PATH.format("information/question_dialog/btn_03.png"))
				button[_].SetText(lTexts[_])
				button[_].Show()

			button[0].SetPosition(-40, button[0].GetHeight() + 5)
			button[1].SetPosition(40, button[0].GetHeight() + 5)

			self.AppendObject("bottom_container", (background, text, button, ))

			self.SetTop()
			self.SetCenterPosition()

		def __AppendRefineItems(self, iGrade):
			## Lets delete at beggin old object's of data
			self.DeleteObject("middle_container")
			self.__UpdateSize(True)

			rGold = item.GetValue(2) * max(1, item.GetValue(0))
			self.GetObject("bottom_container", 1).SetText(localeInfo.AMULET_COMBINATION_CRAFTING_REQUIRED_MONEY + " {}".format(localeInfo.DottedNumber(rGold)))

			yPos = self.GetObject("top_container", 0).GetLocalPosition()[1] + self.GetObject("top_container", 0).GetHeight()
			iHeight = 0

			for it, val in enumerate(self.Objects["PARENT"].UPGRADE_INFORMATION):
				background = ui.ImageBoxNew()
				background.SetParent(self.GetObject("board"))
				background.LoadImage(ROOT_PATH.format("information/question_dialog/middle_bg.png"))
				background.SetPosition(0, yPos)
				background.SetWindowHorizontalAlignCenter()
				background.Show()

				slot_img = ui.ImageBoxNew()
				slot_img.SetParent(background)
				slot_img.SetPosition(25, 0)
				slot_img.SetWindowVerticalAlignCenter()
				slot_img.LoadImage(ROOT_PATH.format("information/slot.png"))
				slot_img.Show()

				item_img = ui.ImageBoxNew()
				item_img.SetParent(slot_img)
				item_img.SetPosition(0, 0)
				item_img.LoadImage(ROOT_PATH.format("information/slot.png"))
				item_img.Show()

				slot_bar = ui.ImageBoxNew()
				slot_bar.SetParent(slot_img)
				slot_bar.SetPosition(slot_img.GetWidth() + 5, 0)
				slot_bar.LoadImage(ROOT_PATH.format("information/question_dialog/middle_content.png"))
				slot_bar.Show()

				slot_name = ui.MakeTextLine(slot_bar)
				item.SelectItem(val.get("V"))
				slot_name.SetText("{}x {}".format(val.get("C"), item.GetItemName()))

				##
				item_img.LoadImage(item.GetIconImageFileName())
				item_img.SetPosition((slot_img.GetWidth() - item_img.GetWidth()) / 2, (slot_img.GetHeight() - item_img.GetHeight()) / 2)

				iHeight = background.GetHeight()
				yPos += iHeight

				self.AppendObject("middle_container", (background, slot_img, item_img, slot_bar, slot_name, ), True)

			## Update size
			iMultipler = ((yPos - (self.GetObject("top_container", 0).GetLocalPosition()[1] + self.GetObject("top_container", 0).GetHeight())) / iHeight) - 1

			if iMultipler >= 1:
				self.__UpdateSize(yPos = iMultipler * iHeight)

		def __UpdateSize(self, bReset = False, yPos = 0):
			if (bReset):
				self.SetSize(*self.SIZE)
			else:
				self.SetSize(self.GetWidth(), self.GetHeight() + yPos)

			self.GetObject("board").SetSize(*self.GetSize())

			self.SetCenterPosition()

			#@Public Methods
		def BindInformation(self, dInformation = {}):
			self.GetObject("board").SetTitleName(dInformation.get("sTitle", "Upgrade"))

			(bg, header, headerText, aTypeInput, aTypeText, aStateInput, aStateText, ) = self.GetObject("top_container")

			if dInformation.get("socket") == -1:
				aStateText.SetText("<IMAGE path=\"{}\">".format(ROOT_PATH.format("information/apply_lock_icon.png")))
			else:
				aStateText.SetText("|cFF4da6ff{}/{}|r".format(dInformation.get("socket", 0), dInformation.get("max_up", 0)))

			fValue = localeInfo.GetFormattedNumberString(dInformation.get("attr")[1])

			sApply = uiToolTip.GetItemToolTipInstance().GetAffectString(dInformation.get("attr")[0], fValue, False)
			sApplyColor, sApplyValue = uiToolTip.GetItemToolTipInstance().GetAttributeColor(0, dInformation.get("attr")[1], dInformation.get("attr")[0], False)
			aTypeText.SetText(uiToolTip.GetItemToolTipInstance().GetFormattedColorString(sApply, fValue, sApplyValue, 1))
			aTypeText.SetPackedFontColor(sApplyColor)

			self.__AppendRefineItems(dInformation.get("socket", 0))

		def SetAcceptEvent(self, sCommand):
			self.GetObject("bottom_container", 2)[0].SetEvent(lambda : (net.SendChatPacket(sCommand), self.Close()))

	def __init__(self):
		super(AmuletInformationClass, self).__init__()

		self.__Initialize()
		self.__BuildWindow()

		self.__Reset()

	def __del__(self):
		return super(AmuletInformationClass, self).__del__()

	def Destroy(self):
		self.ClearDictionary()
		self.Objects = {}

	def __Initialize(self):
		self.Objects = {}

	def __BuildWindow(self):
		if not self.LoadScript(self, "uiscript/AmuletInformation_Window.py"):
			return

		GetObject = self.GetChild

		self.Objects["Item_Container"] = itemWrapper.ItemContainer()
		self.Objects["Item_Container"].SetOnSetItem(self.__OnSetItem)

		self.Objects["Board"] = GetObject("AmuletInformation-Board")
		self.Objects["Slot"] = GetObject("AmuletInformation-ItemSlot")

		self.Objects["Applys"] = [GetObject("AmuletInformation-ApplyText_{}".format(i)) for i in xrange(self.APPLY_CONFIGURATION[0] + self.APPLY_CONFIGURATION[1])]
		self.Objects["ApplysUpgradeLevel"] = [GetObject("AmuletInformation-ApplyUpgradeText_{}".format(i)) for i in xrange(self.APPLY_CONFIGURATION[0] + self.APPLY_CONFIGURATION[1])]

		self.Objects["ApplysWindow"] = [GetObject("AmuletInformation-ApplyWindow_{}".format(i)) for i in xrange(self.APPLY_CONFIGURATION[0] + self.APPLY_CONFIGURATION[1])]
		self.Objects["ApplysActionUnlock"] = [GetObject("AmuletInformation-ApplyActionUnlock_{}".format(i)) for i in xrange(self.APPLY_CONFIGURATION[0] + self.APPLY_CONFIGURATION[1])]
		self.Objects["ApplysActionUpgrade"] = [GetObject("AmuletInformation-ApplyActionUpgrade_{}".format(i)) for i in xrange(self.APPLY_CONFIGURATION[0] + self.APPLY_CONFIGURATION[1])]

		## Lets build checkboxes for window
		self.Objects["ApplysActionCheckBox"] = []
		for i in xrange(2, self.APPLY_CONFIGURATION[0] + self.APPLY_CONFIGURATION[1]):
			chBox = ui.CheckBox()
			chBox.SetParent(self.Objects["ApplysWindow"][i])
			chBox.SetPosition(63, 0)
			chBox.SetWindowVerticalAlignCenter()
			chBox.SetWindowHorizontalAlignRight()
			chBox.Show()
			
			self.Objects["ApplysActionCheckBox"].append(chBox)

		self.Objects["Reroll"] = GetObject("Reroll")

		self.Objects["Question"] = self.RefineQuestion(self)

		return self.__BindActions()

	def __BindActions(self):
		self.Objects["Board"].SetCloseEvent(ui.__mem_func__(self.Close))

		self.Objects["Slot"].SetSelectEmptySlotEvent(self.__OnSelectEmptySlot)
		self.Objects["Slot"].SetSelectItemSlotEvent(self.__OnSelectItemSlot)
		self.Objects["Slot"].SetOverInItemEvent(self.__OnOverInItem)
		self.Objects["Slot"].SetOverOutItemEvent(self.__OnOverOutItem)

		for i in xrange(self.APPLY_CONFIGURATION[0] + self.APPLY_CONFIGURATION[1]):
			self.Objects["ApplysActionUnlock"][i].SAFE_SetEvent(self.__UpgradeApply, i)
			self.Objects["ApplysActionUpgrade"][i].SAFE_SetEvent(self.__UpgradeApply, i)

		self.Objects["Reroll"].SAFE_SetEvent(self.__Reroll)

		self.SetCenterPosition()

	## Communication
	def __UpgradeApply(self, index):
		if self.Objects.get("Question"):
			## We need to select the main item to get correct data
			item.SelectItem(self.Objects["Item_Container"].GetVnum(0))
			tInformation = { "sTitle" : "Upgrade", "socket" : player.GetItemMetinSocket(player.INVENTORY, self.Objects["Item_Container"].GetPosition(0), index), \
				"attr" : player.GetItemAttribute(player.INVENTORY, self.Objects["Item_Container"].GetPosition(0), index) , "max_up" : item.GetValue(1) }

			if tInformation.get("socket") == tInformation.get("max_up"):
				return

			self.Objects["Question"].BindInformation(tInformation)
			self.Objects["Question"].SetAcceptEvent("/amulet_upgrade_apply {} {}".format(self.Objects["Item_Container"].GetPosition(0), index))
			self.Objects["Question"].OpenWindow()

	def __Reroll(self):
		iBit = 0
		
		for it in range(len(self.Objects["ApplysActionCheckBox"])):
			chBox = self.Objects["ApplysActionCheckBox"][it]
			if chBox.IsChecked():
				iBit = iBit | pow(2, it)

		net.SendChatPacket("/amulet_roll {} {}".format(self.Objects["Item_Container"].GetPosition(0), iBit))
	## Communication end

	def __Reset(self):
		self.Objects["Item_Container"].Clear()

	def __OnSetItem(self, slotIndex):
		self.__RefreshItems()

	def __RefreshItems(self):
		self.Objects["Slot"].RefreshItems(self.Objects["Item_Container"].GetVnum, self.Objects["Item_Container"].GetCount)

		pkItem = self.Objects["Item_Container"].GetItem(0)
		if not pkItem:
			# ## Resetting
			for iterator in xrange(self.APPLY_CONFIGURATION[0] + self.APPLY_CONFIGURATION[1]):
				self.Objects["Applys"][iterator].SetText("")
				self.Objects["ApplysUpgradeLevel"][iterator].SetText("")
				self.Objects["ApplysActionUpgrade"][iterator].Hide()
				self.Objects["ApplysActionUnlock"][iterator].Disable()
			return

		self.__AppendApplys()

	def __AppendApplys(self):
		pkItem = self.Objects["Item_Container"].GetItem(0)
		if not pkItem:
			return

		lSockets = [player.GetItemMetinSocket(player.INVENTORY, self.Objects["Item_Container"].GetPosition(0), i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		lAttrs = [player.GetItemAttribute(player.INVENTORY, self.Objects["Item_Container"].GetPosition(0), i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

		lToolTipInstace = pkItem.GetToolTip()
		if not lToolTipInstace:
			return

		for iterator in xrange(self.APPLY_CONFIGURATION[0] + self.APPLY_CONFIGURATION[1]):
			aType = lAttrs[iterator][0]
			aValue = lAttrs[iterator][1]

			if (aType == 0 and aValue == 0):
				self.Objects["ApplysActionUpgrade"][iterator].Hide()
				self.Objects["ApplysActionUnlock"][iterator].Disable()
				continue
			
			self.Objects["ApplysActionUnlock"][iterator].Enable()

			fValue = localeInfo.GetFormattedNumberString(aValue)

			sApply = lToolTipInstace.GetAffectString(aType, fValue, False)
			sApplyColor, sApplyValue = lToolTipInstace.GetAttributeColor(iterator, aValue, aType, False)
			self.Objects["Applys"][iterator].SetText(lToolTipInstace.GetFormattedColorString(sApply, fValue, sApplyValue, 1))
			self.Objects["Applys"][iterator].SetPackedFontColor(sApplyColor)

			if lSockets[iterator] == -1:
				self.Objects["ApplysUpgradeLevel"][iterator].SetText("<IMAGE path=\"{}\">".format("assets/ui/amulet_system/information/apply_lock_icon.png"))
				self.Objects["ApplysActionUpgrade"][iterator].Hide()

			else:
				self.Objects["ApplysUpgradeLevel"][iterator].SetText("<TEXT outline=1 text=\"|cFF4da6ff{}/{}\">".format(lSockets[iterator], item.GetValue(1)))
				self.Objects["ApplysActionUpgrade"][iterator].Show()

			self.Objects["ApplysUpgradeLevel"][iterator].SetWindowHorizontalAlignCenter()
			self.Objects["ApplysUpgradeLevel"][iterator].SetWindowVerticalAlignCenter()
			
			## If we have maximum bonus we should lock button!
			if lSockets[iterator] == item.GetValue(1):
				self.Objects["ApplysActionUpgrade"][iterator].Hide()
				self.Objects["ApplysActionUnlock"][iterator].Disable()

	def __ManageButton(self, sKey, iKey):
		if not self.Objects[sKey].get(iKey):
			return

		pObject = self.Objects[sKey]

	def __SetItem(self, slotIndex, i):
		self.Objects["Item_Container"].SetItem(slotIndex, i)

	def __GetItem(self, slotIndex):
		return self.Objects["Item_Container"].GetItem(slotIndex)

	def __OnSelectEmptySlot(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			slotType = mouseModule.mouseController.GetAttachedType()
			position = mouseModule.mouseController.GetAttachedSlotNumber()

			if not util.IsInventorySlotType(slotType):
				return

			windowType = mouseModule.SlotTypeToWindowType(slotType)
			newItem = itemWrapper.ItemToolTipWrapper(windowType, position)

			vnum = newItem.GetVnum()

			item.SelectItem(vnum)
			if item.GetItemType() != item.ITEM_TYPE_AMULET:
				return

			mouseModule.mouseController.DeattachObject()

			net.SendChatPacket("/amulet_upgrade_info {}".format(position))

			self.__SetItem(slotIndex, newItem)

	def __OnSelectItemSlot(self, slotIndex):
		self.__SetItem(slotIndex, None)

	def __OnOverInItem(self, slotIndex):
		playerItem = self.__GetItem(slotIndex)
		if not playerItem:
			return

		playerItem.ShowToolTip()

	def __OnOverOutItem(self):
		uiToolTip.GetItemToolTipInstance().HideToolTip()

		#@ Public Methods
	##Recv
	def OnRecvUpgradeClear(self):
		self.UPGRADE_INFORMATION = []

	def OnRecvUpgradeInfo(self, iVnum, iCount):
		self.UPGRADE_INFORMATION.append({
			"V" : iVnum,
			"C" : iCount,
		})

	## Recv end

	def Refresh(self):
		self.__RefreshItems()

	def Open(self):
		super(AmuletInformationClass, self).Show()
		self.SetCenterPosition()
		self.Show()

	def Close(self):
		super(AmuletInformationClass, self).Hide()

		self.__Reset()

	def OnPressEscapeKey(self):
		self.Close()
		return True

class AmuletCombinationClass(ui.SimplyWindow):
	SIZE = (220, 300)
	SLOT_TYPE_AMULET = 0
	SLOT_TYPE_ITEM = 1
	SLOT_TYPE_RESULT = 2
	SLOT_TYPE_ADDITIONAL = 3

	def __init__(self):
		ui.SimplyWindow.__init__(self, "UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)
		
	def __del__(self):
		ui.SimplyWindow.__del__(self)

	def __Initialize(self):
		## Build base
		board = ui.MainBoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetTitleName(uiScriptLocale.AMULET_SYSTEM_COMBINATION_TITLE)
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.SetSize(self.GetWidth(), self.GetHeight())
		board.Show()

		self.AppendObject("board", board)

		background = ui.ImageBox()
		background.SetParent(self.GetObject("board"))
		background.SetPosition(0, 33)
		background.SetWindowHorizontalAlignCenter()
		background.LoadImage(ROOT_PATH.format("refine/background.png"))
		background.Show()
		
		self.AppendObject("background", background)

		slot = ui.SlotWindow()
		slot.SetParent(self.GetObject("background"))
		slot.SetPosition((self.GetObject("background").GetWidth() - 34) / 2, 25)
		slot.SetSize(self.GetWidth() - 40, 118)
		slot.SetSlotBaseImage(ROOT_PATH.format("refine/slot_additional.png"), 1.0, 1.0, 1.0, 1.0)
		slot.SetSelectEmptySlotEvent(self.__OnSelectEmptySlot)
		slot.SetSelectItemSlotEvent(self.__OnSelectItemSlot)
		slot.SetOverInItemEvent(self.__OnOverInItem)
		slot.SetOverOutItemEvent(self.__OnOverOutItem)
		slotIndexList = (
			{ "index" : 0, "x" : 0, "y" : 0,		"width" : 32,	"height" : 32 },
			{ "index" : 1, "x" : 0, "y" : 38,		"width" : 32,	"height" : 32 },
			{ "index" : 2, "x" : 0, "y" : 100,		"width" : 32,	"height" : 32 },
			{ "index" : 3, "x" : 50, "y" : 38,		"width" : 32,	"height" : 32 },
		)
		[slot.AppendSlot(i["index"], i["x"], i["y"], i["width"], i["height"]) for i in slotIndexList]
		slot.Show()

		self.AppendObject("slot", slot)

		rMoney = ui.TextLine()
		rMoney.SetParent(self.GetObject("board"))
		rMoney.SetPosition(0, 225)
		rMoney.SetWindowHorizontalAlignCenter()
		rMoney.SetHorizontalAlignCenter()
		rMoney.SetText(localeInfo.NumberToStringAsType(0, True))
		rMoney.Show()
		
		self.AppendObject("upgrade_gold", rMoney)

		rChance = ui.TextLine()
		rChance.SetParent(self.GetObject("board"))
		rChance.SetPosition(0, 235)
		rChance.SetWindowHorizontalAlignCenter()
		rChance.SetHorizontalAlignCenter()
		rChance.SetText(uiScriptLocale.AMULET_SYSTEM_COMBINATION_CHANCE.format(colorInfo.Colorize(str(0) + "%", 0xFFffd169)))
		rChance.Show()
		
		self.AppendObject("upgrade_chance", rChance)

		button = ui.Button()
		button.SetParent(self.GetObject("board"))
		button.SetPosition(0, 255)
		button.SetUpVisual(ROOT_PATH.format("information/button_0.png"))
		button.SetOverVisual(ROOT_PATH.format("information/button_1.png"))
		button.SetDownVisual(ROOT_PATH.format("information/button_2.png"))
		button.SetWindowHorizontalAlignCenter()
		button.SetText(uiScriptLocale.AMULET_SYSTEM_COMBINATION_BUTTON_ACCEPT)
		button.SAFE_SetEvent(self.__Process)
		button.Show()

		self.AppendObject("button", button)

		self.AppendObject("item_container", itemWrapper.ItemContainer())
		self.GetObject("item_container").SetOnSetItem(self.__OnSetItem)

	def __Destroy(self):
		self.__Reset()

	def __Reset(self):
		self.GetObject("item_container").Clear()
		self.GetObject("upgrade_chance").SetText(uiScriptLocale.AMULET_SYSTEM_COMBINATION_CHANCE.format(colorInfo.Colorize(str(0) + "%", 0xFFffd169)))
		self.GetObject("upgrade_gold").SetText(localeInfo.NumberToStringAsType(0, True))

	def __OnSetItem(self, slotIndex):
		self.__RefreshItems(slotIndex)

	def __RefreshItems(self, slotIndex):
		for it in xrange(3):
			self.GetObject("slot").ClearSlot(it)

			if it == self.SLOT_TYPE_RESULT:
				self.GetObject("slot").SetItemSlot(it, self.GetObject("item_container").GetItem(it), 0)
			else:
				self.GetObject("slot").SetItemSlot(it, self.GetObject("item_container").GetVnum(it), 0)

			self.GetObject("slot").RefreshSlot()

		if self.GetObject("item_container").GetItemCount() == 0:
			self.GetObject("upgrade_chance").SetText(uiScriptLocale.AMULET_SYSTEM_COMBINATION_CHANCE.format(colorInfo.Colorize(str(0) + "%", 0xFFffd169)))
			self.GetObject("upgrade_gold").SetText(localeInfo.NumberToStringAsType(0, True))
			self.GetObject("slot").SetItemSlot(self.SLOT_TYPE_ADDITIONAL, self.windowConfig["required-vnum"], 0)

		if slotIndex == self.SLOT_TYPE_AMULET:
			if not self.GetObject("item_container").GetItem(slotIndex):
				return

			self.GetObject("slot").ClearSlot(self.SLOT_TYPE_ADDITIONAL)
			item.SelectItem(self.GetObject("item_container").GetVnum(slotIndex))

			self.GetObject("slot").SetItemSlot(self.SLOT_TYPE_ADDITIONAL, self.windowConfig["required-vnum"], item.GetValue(5))

			if player.GetItemCountByVnum(self.windowConfig["required-vnum"]) < item.GetValue(5):
				self.GetObject("slot").LockSlot(self.SLOT_TYPE_ADDITIONAL)
			else:
				self.GetObject("slot").UnlockSlot(self.SLOT_TYPE_ADDITIONAL)

			self.GetObject("slot").RefreshSlot()

	def __SetItem(self, slotIndex, i):
		self.GetObject("item_container").SetItem(slotIndex, i)

	def __GetItem(self, slotIndex):
		return self.GetObject("item_container").GetItem(slotIndex)
	
	def __OnSelectEmptySlot(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			slotType = mouseModule.mouseController.GetAttachedType()
			position = mouseModule.mouseController.GetAttachedSlotNumber()

			if not util.IsInventorySlotType(slotType):
				return

			windowType = mouseModule.SlotTypeToWindowType(slotType)
			newItem = itemWrapper.ItemToolTipWrapper(windowType, position)
			
			for iPos, cItem in self.GetObject("item_container"):
				if iPos in (self.SLOT_TYPE_RESULT, self.SLOT_TYPE_ADDITIONAL):
					continue

				if cItem.GetPosition() == position:
					return

			vnum = newItem.GetVnum()

			item.SelectItem(vnum)
			if item.GetItemType() != item.ITEM_TYPE_AMULET:
				return
			
			mouseModule.mouseController.DeattachObject()
			net.SendChatPacket("/amulet_combine_register {} {}".format(slotIndex, position))

	def __OnSelectItemSlot(self, slotIndex):
		net.SendChatPacket("/amulet_combine_register {} {}".format(slotIndex, -1))

	def __OnOverInItem(self, slotIndex):
		if slotIndex  == self.SLOT_TYPE_RESULT:
			pMainItem = self.__GetItem(0)
			if not pMainItem:
				return

			dummy = itemWrapper.ItemToolTipDummy(self.GetObject("item_container").GetItem(slotIndex))
			dummy.SetAttrSlot([player.GetItemAttribute(player.INVENTORY, pMainItem.GetPosition(), i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)])

			dummy.ShowToolTip()
			dummy.GetToolTip().AppendTextLine(colorInfo.Colorize(localeInfo.AMULET_RANDOM_APPLY_TEXT, 0xFFdf80ff))
			return

		elif slotIndex == self.SLOT_TYPE_ADDITIONAL:
			return

		playerItem = self.__GetItem(slotIndex)
		if not playerItem:
			return

		playerItem.ShowToolTip()

	def __OnOverOutItem(self):
		uiToolTip.GetItemToolTipInstance().HideToolTip()

	def __Process(self):
		net.SendChatPacket("/amulet_combine_process")

	def Close(self):
		self.Hide()
		net.SendChatPacket("/amulet_combine_close")
		self.__Reset()

	## Recv
	def RegisterAdditional(self, iVnum):
		self.windowConfig["required-vnum"] = iVnum
		item.SelectItem(self.windowConfig["required-vnum"])

		self.GetObject("slot").SetItemSlot(self.SLOT_TYPE_ADDITIONAL, self.windowConfig["required-vnum"], 0)

		if player.GetItemCountByVnum(self.windowConfig["required-vnum"]) < item.GetValue(5):
			self.GetObject("slot").LockSlot(self.SLOT_TYPE_ADDITIONAL)
		else:
			self.GetObject("slot").UnlockSlot(self.SLOT_TYPE_ADDITIONAL)

		self.GetObject("slot").RefreshSlot()

	def RegisterChance(self, iChance):
		self.GetObject("upgrade_chance").SetText(uiScriptLocale.AMULET_SYSTEM_COMBINATION_CHANCE.format(colorInfo.Colorize(str(iChance) + "%", 0xFFffd169)))

	def RegisterGold(self, iGold):
		self.GetObject("upgrade_gold").SetText(localeInfo.NumberToStringAsType(iGold, True))

	def RegisterItem(self, iSlotNum, iSlotItem, iVnum = -1):
		nItem = None if iSlotItem == -1 else itemWrapper.ItemToolTipWrapper(player.INVENTORY, iSlotItem)
		self.__SetItem(iSlotNum, iVnum if iVnum > -1 else nItem)

	def Reset(self):
		self.__Reset()
	## End Recv

class AmuletCraftingClass(ui.SimplyWindow):
	SIZE = (250, 300)

	def __init__(self):
		ui.SimplyWindow.__init__(self, "UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)

	def __del__(self):
		ui.SimplyWindow.__del__(self)

	def __Initialize(self):

		self.windowConfig["grid_size"] = {
			"x" : 4,
			"y" : 3,
		}

		## Build base
		board = ui.MainBoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetTitleName(uiScriptLocale.AMULET_COMBINATION_CRAFTING_TITLE)
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.SetSize(self.GetWidth(), self.GetHeight())
		board.Show()

		self.AppendObject("board", board)

		## Main Container
		gridTable = ui.GridSlotWindow()
		gridTable.SetParent(self.GetObject("board"))
		gridTable.SetPosition(0, 40)
		gridTable.ArrangeSlot(0, self.windowConfig["grid_size"]["x"], self.windowConfig["grid_size"]["y"], 32, 32, 0, 0)
		gridTable.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		gridTable.SetWindowHorizontalAlignCenter()
		gridTable.SetSelectEmptySlotEvent(self.__OnSelectEmptySlot)
		gridTable.SetSelectItemSlotEvent(self.__OnSelectItemSlot)
		gridTable.SetOverInItemEvent(self.__OnOverInItem)
		gridTable.SetOverOutItemEvent(self.__OnOverOutItem)
		gridTable.Show()

		self.AppendObject("grid_table", gridTable)

		slot_reward = ui.SlotWindow()
		slot_reward.SetParent(self.GetObject("board"))
		slot_reward.SetPosition(0, 40 + 32 * 3 + 32)
		slot_reward.SetSize(32, 32)
		slot_reward.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		slot_reward.AppendSlot(0, 0, 0, 32, 32)
		slot_reward.SetWindowHorizontalAlignCenter()
		slot_reward.Show()

		self.AppendObject("slot_reward", slot_reward)

		rMoney = ui.TextLine()
		rMoney.SetParent(self.GetObject("board"))
		rMoney.SetPosition(0, 200)
		rMoney.SetWindowHorizontalAlignCenter()
		rMoney.SetHorizontalAlignCenter()
		rMoney.SetText(uiScriptLocale.AMULET_COMBINATION_CRAFTING_REQUIRED_MONEY)
		rMoney.Show()
		
		self.AppendObject("required_money", rMoney)

		button = ui.Button()
		button.SetParent(self.GetObject("board"))
		button.SetPosition(0, 220)
		button.SetUpVisual(ROOT_PATH.format("information/button_0.png"))
		button.SetOverVisual(ROOT_PATH.format("information/button_1.png"))
		button.SetDownVisual(ROOT_PATH.format("information/button_2.png"))
		button.SetWindowHorizontalAlignCenter()
		button.SetText(uiScriptLocale.AMULET_COMBINATION_CRAFTING_BUTTON_ACCEPT)
		button.SAFE_SetEvent(self.__Process)
		button.Show()

		self.AppendObject("button", button)

		self.AppendObject("item_container", itemWrapper.ItemContainer())
		self.GetObject("item_container").SetOnSetItem(self.__OnSetItem)

	def __Destroy(self):
		self.__Reset()

	def __Reset(self):
		self.GetObject("item_container").Clear()

	def __OnSetItem(self, slotIndex):
		self.__RefreshItems(slotIndex)

	def __RefreshItems(self, slotIndex):
		self.GetObject("grid_table").ClearSlot(slotIndex)
		self.GetObject("grid_table").SetItemSlot(slotIndex, self.GetObject("item_container").GetVnum(slotIndex), 0)
		self.GetObject("grid_table").RefreshSlot()

		iTotalReward = 0
		iTotalMoney = 0
		for slot in range(self.GetObject("item_container").GetItemCount()):
			item.SelectItem(self.GetObject("item_container").GetVnum(slot))
			iTotalMoney += item.GetValue(3)
			iTotalReward += item.GetValue(4)

		if iTotalReward:
			self.GetObject("slot_reward").SetItemSlot(0, self.windowConfig["reward_vnum"], iTotalReward)
			self.GetObject("slot_reward").UnlockSlot(0)
		else:
			self.GetObject("slot_reward").ClearSlot(0)
			self.GetObject("slot_reward").LockSlot(0)

		self.GetObject("slot_reward").RefreshSlot()

		self.GetObject("required_money").SetText(localeInfo.NumberToStringAsType(iTotalMoney, True))

	def __SetItem(self, slotIndex, i):
		self.GetObject("item_container").SetItem(slotIndex, i)

	def __GetItem(self, slotIndex):
		return self.GetObject("item_container").GetItem(slotIndex)

	def __OnSelectEmptySlot(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			slotType = mouseModule.mouseController.GetAttachedType()
			position = mouseModule.mouseController.GetAttachedSlotNumber()

			if not util.IsInventorySlotType(slotType):
				return

			windowType = mouseModule.SlotTypeToWindowType(slotType)
			newItem = itemWrapper.ItemToolTipWrapper(windowType, position)
			
			for iPos, cItem in self.GetObject("item_container"):
				if cItem.GetPosition() == position:
					return

			vnum = newItem.GetVnum()

			item.SelectItem(vnum)
			if item.GetItemType() != item.ITEM_TYPE_AMULET:
				return

			mouseModule.mouseController.DeattachObject()

			self.__SetItem(slotIndex, newItem)

	def __OnSelectItemSlot(self, slotIndex):
		self.__SetItem(slotIndex, None)

	def __OnOverInItem(self, slotIndex):
		playerItem = self.__GetItem(slotIndex)
		if not playerItem:
			return

		playerItem.ShowToolTip()

	def __OnOverOutItem(self):
		uiToolTip.GetItemToolTipInstance().HideToolTip()

	def __Process(self):
		for iPos, cItem in self.GetObject("item_container"):
			net.SendChatPacket("/amulet_crafting_process {}".format(cItem.GetPosition()))

		self.__Reset()

	def Close(self):
		self.Hide()
		self.__Reset()

	## Recv
	def OnRecvRegisterReward(self, iVnum):
		self.windowConfig["reward_vnum"] = iVnum

		self.GetObject("slot_reward").SetItemSlot(0, self.windowConfig["reward_vnum"])
		self.GetObject("slot_reward").LockSlot(0)
	## End Recv
