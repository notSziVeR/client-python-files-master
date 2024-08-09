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

import uiScriptLocale

SLOT_DISABLE = "d:/ymir work/ui/pet/skill_button/skill_enable_button.sub"

class LuckyBoxWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.Initialize()
		self.LoadWindow()

	def Initialize(self):
		self.titleBar = None
		self.boxImage = None
		self.refreshButton = None

		self.priceBox = None
		self.priceName = None
		self.priceValue = None

		self.itemSlots = None
		self.keepButton = None
		self.rewardEffect = None
		self.tooltipItem = None
		self.interface = None

		self.alreadyOpen = []

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Initialize()

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/LuckyBoxWindow.py")
		except:
			import exception
			exception.Abort("DungeonListWindow.LoadDialog.LoadScript")

		try:
			self.titleBar = self.GetChild("TitleBar")
			self.titleBar.HandleButtonState("BTN_INFO", True)

			self.boxImage = self.GetChild("ItemImage")
			self.refreshButton = self.GetChild("RefreshButton")
			self.keepButton = self.GetChild("KeepButton")

			self.priceBox = self.GetChild("PriceBox")
			self.priceName = self.GetChild("PriceName")
			self.priceValue = self.GetChild("PriceValue")

			self.itemSlots = self.GetChild("ItemSluts")
			self.rewardEffect = self.GetChild("RewardEffect")
		except:
			import exception
			exception.Abort("DungeonListWindow.LoadDialog.BindObject")

		self.rewardEffect.Hide()

		self.titleBar.SetInfoToolTip(self.__CreateGameTypeToolTip(uiScriptLocale.LUCKY_BOX_INFORMATION_1))

		self.boxImage.SetEvent(ui.__mem_func__(self.OverInBox), "mouse_over_in")
		self.boxImage.SetEvent(ui.__mem_func__(self.OverOutItem), "mouse_over_out")

		self.refreshButton.SetEvent(ui.__mem_func__(self.SendRefresh))
		self.keepButton.SetEvent(ui.__mem_func__(self.SendKeep))

		self.itemSlots.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlots.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

	def __CreateGameTypeToolTip(self, title):
		toolTip = uiToolTip.ToolTip()
		toolTip.SetTitle(title)
		toolTip.AppendSpace(5)
		toolTip.AutoAppendTextLine(uiScriptLocale.LUCKY_BOX_INFORMATION_2)
		toolTip.AutoAppendTextLine(uiScriptLocale.LUCKY_BOX_INFORMATION_3)
		toolTip.AutoAppendTextLine(uiScriptLocale.LUCKY_BOX_INFORMATION_4)

		toolTip.AlignHorizonalCenter()
		return toolTip

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def BindInterface(self, interface):
		self.interface = interface

	def SendRefresh(self):
		net.SendLuckyBoxAction(0)

	def SendKeep(self):
		net.SendLuckyBoxAction(1)

	def RefreshInfo(self):
		boxVnum = player.GetLuckyBoxVnum()
		if boxVnum:
			item.SelectItem(boxVnum)
			self.boxImage.LoadImage(item.GetIconImageFileName())

			standardPrice = item.GetValue(0)
			for i in xrange(item.GetValue(1) - 1):
				standardPrice *= 2

			if standardPrice == player.GetLuckyBoxPrice():
				self.refreshButton.Disable()
				#self.keepButton.EnableFlash()
			else:
				self.refreshButton.Enable()
				#self.keepButton.DisableFlash()

		refreshCost = player.GetLuckyBoxPrice()
		self.priceValue.SetText(localeInfo.NumberToMoneyString(refreshCost))

		if player.GetMoney() < refreshCost:
			self.priceValue.SetPackedFontColor(0xffff1c49)
		else:
			self.priceValue.SetPackedFontColor(0xffdddddd)

		# for i in xrange(self.itemSlots.GetSlotCount()):
		# 	(vnum, count, is_reward) = player.GetLuckyBoxItemInfo(i)
		# 	if vnum:
		# 		if is_reward:
		# 			self.itemSlots.SetItemSlot(i, vnum, count)
		# 			self.itemSlots.EnableCoverButton(i)

		# 			self.rewardEffect.SetPosition(15 + ((i % 8) * 32), 105 + ((i / 8) * 32))
		# 			self.rewardEffect.Show()
		# 		else:
		# 			self.itemSlots.SetItemSlot(i, vnum, count)

		for i in xrange(self.itemSlots.GetSlotCount()):
			(vnum, count, is_reward) = player.GetLuckyBoxItemInfo(i)
			if vnum:
				if is_reward:
					self.rewardEffect.SetPosition(15 + ((i % 8) * 32), 105 + ((i / 8) * 32))
					self.rewardEffect.Show()

					self.alreadyOpen.append(i)
				else:
					self.itemSlots.SetItemSlot(i, 0)
					self.itemSlots.SetCoverButton(i, "d:/ymir work/ui/game/quest/slot_button_01.sub",\
														"d:/ymir work/ui/game/quest/slot_button_01.sub",\
														"d:/ymir work/ui/game/quest/slot_button_01.sub",\
														SLOT_DISABLE, False, False)

					self.itemSlots.SetAlwaysRenderCoverButton(i, True)
					self.itemSlots.DisableCoverButton(i)

				if i in self.alreadyOpen:
					self.itemSlots.SetItemSlot(i, vnum, count)
					self.itemSlots.EnableCoverButton(i)


	def OverInBox(self):
		boxVnum = player.GetLuckyBoxVnum()
		if boxVnum and self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(boxVnum, [0, 0, 0, 0, 0, 0, 0])
			self.tooltipItem.ShowToolTip()

	def OverInItem(self, slotIndex):
		(vnum, count, is_reward) = player.GetLuckyBoxItemInfo(slotIndex)
		if vnum and self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(vnum, [0, 0, 0, 0, 0, 0, 0])
			self.tooltipItem.ShowToolTip()

	def OverOutItem(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def Destroy(self):
		self.ClearDictionary()
		self.Initialize()

	def Open(self):
		self.RefreshInfo()
		self.AdjustPosition()

		self.Show()
		self.SetTop()

	def Close(self):
		self.rewardEffect.Hide()

		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

		self.alreadyOpen = []

		self.Hide()

	def AdjustPosition(self):
		if self.interface and self.interface.wndInventory and self.interface.wndInventory.GetGlobalPosition():
			x, y = self.interface.wndInventory.GetGlobalPosition()
			self.SetPosition(x - 285, y)
