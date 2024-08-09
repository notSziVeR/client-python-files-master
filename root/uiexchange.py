import ui
import app
import net
import grp
import chat
import item
import time
import wndMgr
import player
import uiCommon
import exchange
import localeInfo
import mouseModule
import uiPickMoney
from playerSettingModule import RACE_WARRIOR_M, RACE_WARRIOR_W, RACE_ASSASSIN_M, RACE_ASSASSIN_W, RACE_SURA_M, RACE_SURA_W, RACE_SHAMAN_M, RACE_SHAMAN_W
if app.ENABLE_WOLFMAN_CHARACTER:
	from playerSettingModule import RACE_WOLFMAN_M
from time import strftime
from datetime import datetime

import grid
import itemWrapper

if gcGetEnable("ENABLE_LOCK_EFFECTS"):
	EXCHANGE_COLOUR = (1.0, 1.0, 1.0, 0.3)

###################################################################################################
## Exchange
class ExchangeDialog(ui.ScriptWindow):
	FACE_IMAGE_DICT = {
		RACE_WARRIOR_M	: "icon/face/warrior_m.tga",
		RACE_WARRIOR_W	: "icon/face/warrior_w.tga",
		RACE_ASSASSIN_M	: "icon/face/assassin_m.tga",
		RACE_ASSASSIN_W	: "icon/face/assassin_w.tga",
		RACE_SURA_M		: "icon/face/sura_m.tga",
		RACE_SURA_W		: "icon/face/sura_w.tga",
		RACE_SHAMAN_M	: "icon/face/shaman_m.tga",
		RACE_SHAMAN_W	: "icon/face/shaman_w.tga",
		# RACE_WOLFMAN_M : "icon/face/wolfman_m.tga",
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		FACE_IMAGE_DICT.update({RACE_WOLFMAN_M : "icon/face/wolfman_m.tga",})

	class TextRenderer(ui.Window):
		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			chat.RenderWhisper("$EXCHANGE_CHAT$", x, y+8)

	def __init__(self, dlgInventory):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = 0
		self.xStart = 0
		self.yStart = 0

		self.interface = 0
		self.dlgInventory = dlgInventory

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadDialog(self):
		PythonScriptLoader = ui.PythonScriptLoader()
		if app.ENABLE_RENEWAL_EXCHANGE:
			PythonScriptLoader.LoadScriptFile(self, "uiscript/exchangedialog_new.py")
		## Owner
		self.OwnerSlot = self.GetChild("Owner_Slot")
		self.OwnerSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectOwnerEmptySlot))
		self.OwnerSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectOwnerItemSlot))
		self.OwnerSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInOwnerItem))
		self.OwnerSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.OwnerSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.RightClickItemSlot))
		self.OwnerMoney = self.GetChild("Owner_Money_Value")
		if not app.ENABLE_RENEWAL_EXCHANGE:
			self.OwnerAcceptLight = self.GetChild("Owner_Accept_Light")
			self.OwnerAcceptLight.Disable()
		self.OwnerMoneyButton = self.GetChild("Input_1")
		self.OwnerMoneyButton.SetEvent(ui.__mem_func__(self.OpenPickMoneyDialog))

		## Target
		self.TargetSlot = self.GetChild("Target_Slot")
		self.TargetSlot.SetOverInItemEvent(ui.__mem_func__(self.OverInTargetItem))
		self.TargetSlot.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		self.TargetMoney = self.GetChild("Target_Money_Value")
		if not app.ENABLE_RENEWAL_EXCHANGE:
			self.TargetAcceptLight = self.GetChild("Target_Accept_Light")
			self.TargetAcceptLight.Disable()

		## PickMoneyDialog
		dlgPickMoney = uiPickMoney.PickMoneyDialog()
		dlgPickMoney.LoadDialog()
		dlgPickMoney.SetAcceptEvent(ui.__mem_func__(self.OnPickMoney))
		dlgPickMoney.SetTitleName(localeInfo.EXCHANGE_MONEY)
		dlgPickMoney.SetMax(9)
		dlgPickMoney.Hide()
		self.dlgPickMoney = dlgPickMoney

		## Button
		self.AcceptButton = self.GetChild("Owner_Accept_Button")
		self.AcceptButton.SetToggleDownEvent(ui.__mem_func__(self.AcceptExchange))

		if app.ENABLE_RENEWAL_EXCHANGE:
			self.TargetAcceptButton = self.GetChild("Target_Accept_Button")

		self.Board = self.GetChild("board")
		self.Board.SetCloseEvent(net.SendExchangeExitPacket)

		if app.ENABLE_RENEWAL_EXCHANGE:
			ROOT = "d:/ymir work/ui/scroll_white/"
			self.FaceOwnerImage = self.GetChild("FaceOwner_Image")
			self.FaceTargetImage = self.GetChild("FaceTarget_Image")
			self.TargetText = self.GetChild("TargetText")
			self.OwnerText = self.GetChild("OwnerText")
			self.ExchangeLogs = self.GetChild("ExchangeLogs")
			self.listOwnerSlot = []
			self.listTargetSlot = []

			## Scroll
			self.scrollBar = self.GetChild("scrollbar")
			self.scrollBar.SetScrollEvent(ui.__mem_func__(self.OnScroll))
			self.scrollBar.SetPos(0.0)

			## Chat
			self.textRenderer = self.TextRenderer()
			self.textRenderer.SetParent(self.ExchangeLogs)
			self.textRenderer.SetPosition(5, 5)
			self.textRenderer.Show()

	def Destroy(self):
		print "---------------------------------------------------------------------------- DESTROY EXCHANGE"
		self.ClearDictionary()
		self.dlgPickMoney.Destroy()
		self.dlgPickMoney = 0
		self.OwnerSlot = 0
		self.OwnerMoney = 0
		if not app.ENABLE_RENEWAL_EXCHANGE:
			self.OwnerAcceptLight = 0
		self.OwnerMoneyButton = 0
		self.TargetSlot = 0
		self.TargetMoney = 0
		if not app.ENABLE_RENEWAL_EXCHANGE:
			self.TargetAcceptLight = 0
		self.AcceptButton = 0
		if app.ENABLE_RENEWAL_EXCHANGE:
			self.TargetAcceptButton = 0
			self.FaceOwnerImage = None
			self.FaceTargetImage = None
			self.TargetText = None
			self.OwnerText = None

		self.tooltipItem = 0
		self.interface = 0
		self.dlgInventory = None

	def OpenDialog(self):
		chat.ClearWhisper("$EXCHANGE_CHAT$")
		chat.CreateWhisper("$EXCHANGE_CHAT$")
		chat.SetWhisperBoxSize("$EXCHANGE_CHAT$", 370, 85)
		chat.SetRenderDownwards("$EXCHANGE_CHAT$", True)

		if app.ENABLE_RENEWAL_EXCHANGE:
			self.Board.SetTitleName(localeInfo.EXCHANGE_TITLE_LEVEL % (exchange.GetNameFromTarget(), exchange.GetLevelFromTarget()))
		else:
			self.Board.SetTitleName(localeInfo.EXCHANGE_TITLE % (exchange.GetNameFromTarget()))
		self.AcceptButton.Enable()
		self.AcceptButton.SetUp()
		if app.ENABLE_RENEWAL_EXCHANGE:
			self.TargetAcceptButton.Disable()
			self.TargetAcceptButton.SetUp()
			ownerI = exchange.GetRaceFromSelf()
			targetI = exchange.GetRaceFromTarget()

			self.FaceOwnerImage.SetRenderDistance(1000)
			self.FaceOwnerImage.SetLightPosition(*(50.0, 150.0, 350.0))
			self.FaceOwnerImage.SetRenderTarget(ownerI)

			self.FaceTargetImage.SetRenderDistance(1000)
			self.FaceTargetImage.SetLightPosition(*(50.0, 150.0, 350.0))
			self.FaceTargetImage.SetRenderTarget(targetI)

			targetText = "|cFF04DD04Lv. " + str(exchange.GetLevelFromTarget()) + "|r " + exchange.GetNameFromTarget()
			self.TargetText.SetText(targetText)
			ownerText = "|cFF04DD04Lv. " + str(player.GetStatus(player.LEVEL)) + "|r " + player.GetName()
			self.OwnerText.SetText(ownerText)

			self.AppendInformation(app.GetGlobalTimeStamp(), localeInfo.NEW_EXCHANGE_YOU_READY)

		self.Show()

		(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()

		if gcGetEnable("ENABLE_LOCK_EFFECTS"):
			self.dlgInventory.RegisterLockColour("EXCHANGE", EXCHANGE_COLOUR)

	def CloseDialog(self):
		wndMgr.OnceIgnoreMouseLeftButtonUpEvent()

		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if gcGetEnable("ENABLE_LOCK_EFFECTS"):
			self.dlgInventory.EraseLockElement("EXCHANGE")

		self.dlgPickMoney.Close()
		self.Hide()

	def AppendInformation(self, unixTime, info, error = False):
		if not error:
			chatType = chat.WHISPER_TYPE_CHAT
		else:
			chatType = chat.WHISPER_TYPE_SYSTEM

		time = datetime.fromtimestamp(unixTime).timetuple()
		chat.AppendWhisper(chatType, "$EXCHANGE_CHAT$", "["+strftime("%H:%M:%S", time) + "] "+info)

	def OnScroll(self):
		chat.SetWhisperPosition("$EXCHANGE_CHAT$", 1 - self.scrollBar.GetPos())

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def OpenPickMoneyDialog(self):

		# if exchange.GetElkFromSelf() > 0:
		# 	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANT_EDIT_MONEY)
		# 	return

		self.dlgPickMoney.Open(player.GetElk(), 1, True, "Put yang value")

	def OnPickMoney(self, money):
		net.SendExchangeElkAddPacket(money)

	def AcceptExchange(self):
		if app.ENABLE_RENEWAL_EXCHANGE:
			atLeastOneItem = 0
			atLeastOneYang = 0
			for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
				itemCount = exchange.GetItemCountFromTarget(i)
				if itemCount >= 1:
					atLeastOneYang = 1
					break

			if exchange.GetElkFromTarget() >= 1:
				atLeastOneYang = 1

			if atLeastOneItem or atLeastOneYang:
				net.SendExchangeAcceptPacket()
				self.AcceptButton.Disable()
			else:
				atLeastOneItem = 0
				atLeastOneYang = 0
				for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
					itemCount = exchange.GetItemCountFromSelf(i)
					if itemCount >= 1:
						atLeastOneYang = 1
						break

				if exchange.GetElkFromSelf() >= 1:
					atLeastOneYang = 1

				if atLeastOneItem or atLeastOneYang:
					self.questionDialog = uiCommon.QuestionDialog2()
					self.questionDialog.SetText1(localeInfo.NEW_EXCHANGE_ALERT1)
					self.questionDialog.SetText2(localeInfo.NEW_EXCHANGE_ALERT2)
					self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.AcceptQuestion))
					self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
					self.questionDialog.Open()
				else:
					net.SendExchangeAcceptPacket()
					self.AcceptButton.Disable()
		else:
			net.SendExchangeAcceptPacket()
			self.AcceptButton.Disable()

	if app.ENABLE_RENEWAL_EXCHANGE:
		def AcceptQuestion(self):
			net.SendExchangeAcceptPacket()
			self.AcceptButton.Disable()
			if self.questionDialog:
				self.questionDialog.Close()

			self.questionDialog = None

		def OnCloseQuestionDialog(self):
			if self.questionDialog:
				self.questionDialog.Close()

			self.questionDialog = None
			self.AcceptButton.Enable()
			self.AcceptButton.SetUp()

	def SelectOwnerEmptySlot(self, SlotIndex):

		if False == mouseModule.mouseController.isAttached():
			return

		if mouseModule.mouseController.IsAttachedMoney():
			net.SendExchangeElkAddPacket(mouseModule.mouseController.GetAttachedMoneyAmount())
		else:
			attachedSlotType = mouseModule.mouseController.GetAttachedType()

			if (player.SLOT_TYPE_INVENTORY == attachedSlotType
				or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType):

				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				SrcSlotNumber = mouseModule.mouseController.GetAttachedSlotNumber()
				DstSlotNumber = SlotIndex

				itemID = player.GetItemIndex(attachedInvenType, SrcSlotNumber)
				item.SelectItem(itemID)

				if item.IsAntiFlag(item.ANTIFLAG_GIVE):
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.EXCHANGE_CANNOT_GIVE)
					mouseModule.mouseController.DeattachObject()
					return

				net.SendExchangeItemAddPacket(attachedInvenType, SrcSlotNumber, DstSlotNumber)
				if gcGetEnable("ENABLE_LOCK_EFFECTS"):
					self.dlgInventory.AppendLockSlot("EXCHANGE", SrcSlotNumber)
					self.dlgInventory.RefreshBagSlotWindow()

		mouseModule.mouseController.DeattachObject()

	def RightClickItemSlot(self, SlotIndex):
		print "Requesting removal of", SlotIndex
		# self.RefreshLockedSlot()
		net.SendExchangeItemDelPacket(SlotIndex)

	def SelectOwnerItemSlot(self, SlotIndex):
		print "SelectOwnerItemSlot: ",SlotIndex
		if player.ITEM_MONEY == mouseModule.mouseController.GetAttachedItemIndex():
			money = mouseModule.mouseController.GetAttachedItemCount()
			net.SendExchangeElkAddPacket(money)

	if gcGetEnable("ENABLE_FAST_INTERACTION_EXCHANGE"):
		def BuildGrid(self):
			g = grid.Grid(6, 4, 1)

			for i in xrange(g.GetSize()):
				vnum = exchange.GetItemVnumFromSelf(i)
				if vnum == 0:
					continue

				count = exchange.GetItemCountFromSelf(i)
				if count == 0 and vnum != 71202:
					continue

				g.PutGlobal(itemWrapper.ItemGridWrapper(player.DUMMY_EXCHANGE, i), i)

			return g

	def HighlightSlots(self, isSelf):
		if isSelf:
			slotWindow = self.OwnerSlot
			getItemVnumFunc = exchange.GetItemVnumFromSelf
		else:
			slotWindow = self.TargetSlot
			getItemVnumFunc = exchange.GetItemVnumFromTarget

		for slotIndex in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemVnum = getItemVnumFunc(slotIndex)
			if itemVnum < 1:
				continue

			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			if itemType != item.ITEM_TYPE_WEAPON and itemType != item.ITEM_TYPE_ARMOR:
				continue

			itemName = item.GetItemName()
			_, itemHeight = item.GetItemSize()

			for plus in xrange(6, 9+1):
				if "+"+str(plus) in itemName or "+ "+str(plus) in itemName:
					print "Found",plus,"in the item name"

					for row in xrange(0, itemHeight):
						slotWindow.SetSlotHighlightedGreeen(slotIndex + row*6)

					break # Outside the plus loop

	def RefreshOwnerSlot(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromSelf(i)
			itemCount = exchange.GetItemCountFromSelf(i)
			if 1 == itemCount:
				itemCount = 0
			if app.ENABLE_TRANSMUTATION_SYSTEM:
				self.OwnerSlot.SetItemSlot(i, itemIndex, itemCount, (1.0, 1.0, 1.0, 1.0), exchange.GetItemTransmutateFromSelf(i))
			else:
				self.OwnerSlot.SetItemSlot(i, itemIndex, itemCount)

		self.HighlightSlots(True)
		self.OwnerSlot.RefreshSlot()

	def RefreshTargetSlot(self):
		for i in xrange(exchange.EXCHANGE_ITEM_MAX_NUM):
			itemIndex = exchange.GetItemVnumFromTarget(i)
			itemCount = exchange.GetItemCountFromTarget(i)
			if 1 == itemCount:
				itemCount = 0
			if app.ENABLE_TRANSMUTATION_SYSTEM:
				self.TargetSlot.SetItemSlot(i, itemIndex, itemCount, (1.0, 1.0, 1.0, 1.0), exchange.GetItemTransmutateFromTarget(i))
			else:
				self.TargetSlot.SetItemSlot(i, itemIndex, itemCount)

		self.HighlightSlots(False)
		self.TargetSlot.RefreshSlot()

	def Refresh(self):

		self.RefreshOwnerSlot()
		self.RefreshTargetSlot()

		self.OwnerMoney.SetText(localeInfo.NumberToString(exchange.GetElkFromSelf()))
		self.TargetMoney.SetText(localeInfo.NumberToString(exchange.GetElkFromTarget()))

		if exchange.GetAcceptFromSelf() == True:
			if not app.ENABLE_RENEWAL_EXCHANGE:
				self.OwnerAcceptLight.Down()
			else:
				self.OwnerSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 0.3500, 0.8500, 0.3500, 1.0)
		else:
			if self.AcceptButton.IsDown() == True:
				self.AppendInformation(app.GetGlobalTimeStamp(), localeInfo.NEW_EXCHANGE_YOU_ABORT)

			self.AcceptButton.Enable()
			self.AcceptButton.SetUp()
			if not app.ENABLE_RENEWAL_EXCHANGE:
				self.OwnerAcceptLight.SetUp()
			else:
				self.OwnerSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)

		if exchange.GetAcceptFromTarget() == True:
			if not app.ENABLE_RENEWAL_EXCHANGE:
				self.TargetAcceptLight.Down()
			else:
				self.TargetAcceptButton.Down()
				self.TargetSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 0.3500, 0.8500, 0.3500, 1.0)
		else:
			if not app.ENABLE_RENEWAL_EXCHANGE:
				self.TargetAcceptLight.SetUp()
			else:
				if self.TargetAcceptButton.IsDown() == True:
					self.AppendInformation(app.GetGlobalTimeStamp(), localeInfo.NEW_EXCHANGE_ABORT %  exchange.GetNameFromTarget())

				self.TargetAcceptButton.SetUp()
				self.TargetSlot.SetSlotBaseImage("d:/ymir work/ui/public/slot_base.sub", 1.0, 1.0, 1.0, 1.0)

	def OverInOwnerItem(self, slotIndex):

		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeOwnerItem(slotIndex)

	def OverInTargetItem(self, slotIndex):

		if 0 != self.tooltipItem:
			self.tooltipItem.SetExchangeTargetItem(slotIndex)

	def OverOutItem(self):

		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnTop(self):
		self.tooltipItem.SetTop()

	def OnUpdate(self):

		if self.GetLeft() < 0:
			self.SetPosition(0, self.GetTop())
		elif self.GetRight() > wndMgr.GetScreenWidth():
			self.SetPosition(wndMgr.GetScreenWidth() - self.GetWidth(), self.GetTop())

		if self.GetTop() < 0:
			self.SetPosition(self.GetLeft(), 0)
		elif self.GetBottom() > wndMgr.GetScreenHeight():
			self.SetPosition(self.GetLeft(), wndMgr.GetScreenHeight() - self.GetHeight())

		USE_EXCHANGE_LIMIT_RANGE = 1000

		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xStart) > USE_EXCHANGE_LIMIT_RANGE or abs(y - self.yStart) > USE_EXCHANGE_LIMIT_RANGE:
			(self.xStart, self.yStart, z) = player.GetMainCharacterPosition()
			if gcGetEnable("ENABLE_LOCK_EFFECTS"):
				self.dlgInventory.EraseLockElement("EXCHANGE")

			self.RemoveFlag("animate")
			net.SendExchangeExitPacket()


	def BindInterface(self, interface):
		self.interface = interface

	def OnMouseLeftButtonDown(self):
		hyperlink = ui.GetHyperlink()
		if hyperlink:
			self.interface.MakeHyperlinkTooltip(hyperlink)
