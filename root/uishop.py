import net
import player
import item
import snd
import shop
import net
import wndMgr
import app
import chat

import ui
import uiCommon
import mouseModule
import localeInfo
import constInfo

import chr

if gcGetEnable("ANCIENT_SHOP_MULTIPLE_BUY"):
	import uiMultipleAncientShopBuy

###################################################################################################
## Shop
class ShopDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.tooltipItem = 0
		self.xShopStart = 0
		self.yShopStart = 0
		self.questionDialog = None
		self.popup = None
		self.itemBuyQuestionDialog = None

		if gcGetEnable("ANCIENT_SHOP_MULTIPLE_BUY"):
			self.ancientShopMultipleBuyWindow = None
			self.vid = 0

		self.tabIdx = 0

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def RefreshTabs(self):
		self.categoryTabs = []

		if shop.GetTabCount() > 1:
			tabSize = {
				2 : "middle",
				3 : "small",
			}
			tabSize = tabSize[shop.GetTabCount()]
			tabXPosition = {
				2 : (21 + 8, 104 + 8),
				3 : (21 + 8, 71 + 8, 120 + 8),
			}
			tabXPosition = tabXPosition[shop.GetTabCount()]

			tabHeight = 0
			for i in xrange(shop.GetTabCount()):
				tab = ui.RadioButton()
				tab.SetParent(self)
				tab.SetUpVisual("d:/ymir work/ui/public/%s_button_01.sub" % tabSize)
				tab.SetOverVisual("d:/ymir work/ui/public/%s_button_02.sub" % tabSize)
				tab.SetDownVisual("d:/ymir work/ui/public/%s_button_03.sub" % tabSize)
				tab.SetText(shop.GetTabName(i))
				tab.SetPosition(tabXPosition[i], 43)
				tab.SAFE_SetEvent(self.__SetTabPage, i)
				tab.Show()
				tabHeight = tab.GetHeight()

				self.categoryTabs.append(tab)

		self.__SetTabPage(self.tabIdx)

	def __SetTabPage(self, index):
		self.tabIdx = index
		self.Refresh()

		if index < len(self.categoryTabs):
			for tab in self.categoryTabs:
				tab.SetUp()
			self.categoryTabs[index].Down()

	def UpdateHeight(self, newHeight):
		self.SetSize(self.GetWidth(), newHeight)
		self.Board.SetSize(self.GetWidth(), self.GetHeight())

	def __LocalToGlobalSlot(self, slotIdx):
		return self.tabIdx * shop.SHOP_SLOT_COUNT + slotIdx

	def Refresh(self):
		getItemID=shop.GetItemID
		getItemCount=shop.GetItemCount
		setItemID=self.itemSlotWindow.SetItemSlot
		for i in xrange(shop.SHOP_SLOT_COUNT):
			slotIdx = self.__LocalToGlobalSlot(i)

			itemCount = getItemCount(slotIdx)
			if itemCount <= 1:
				itemCount = 0

			if app.ENABLE_TRANSMUTATION_SYSTEM:
				setItemID(i, getItemID(slotIdx), itemCount, (1.0, 1.0, 1.0, 1.0), shop.GetItemTransmutate(i))
			else:
				setItemID(i, getItemID(slotIdx), itemCount)

		wndMgr.RefreshSlot(self.itemSlotWindow.GetWindowHandle())

	def SetItemData(self, pos, itemID, itemCount, itemPrice):
		shop.SetItemData(pos, itemID, itemCount, itemPrice)

	def LoadDialog(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "UIScript/shopdialog.py")
		except:
			import exception
			exception.Abort("ShopDialog.LoadDialog.LoadObject")

		if app.ENABLE_RENEWAL_SHOP_SELLING:
			self.iSelectedItems = 0
			self.iTotalMoney = 0
			self.interface = None

		try:
			GetObject = self.GetChild
			self.Board = GetObject("board")
			self.itemSlotWindow = GetObject("ItemSlot")
			self.btnBuy = GetObject("BuyButton")
			self.btnSell = GetObject("SellButton")
			self.btnClose = GetObject("CloseButton")
			if app.ENABLE_RENEWAL_SHOP_SELLING:
				self.tRenewalItems = {
					"SELECTED_TEXT": GetObject("selected_text"),
					"TOTAL_M_TEXT" : GetObject("total_money_text"),
					"ACCEPT_BTN"   : GetObject("sell_button"),
					"CLEAR_BUTTON" : GetObject("cancel_button"),
				}

		except:
			import exception
			exception.Abort("ShopDialog.LoadDialog.BindObject")

		self.itemSlotWindow.SetSlotStyle(wndMgr.SLOT_STYLE_NONE)
		self.itemSlotWindow.SAFE_SetButtonEvent("LEFT", "EMPTY", self.SelectEmptySlot)
		self.itemSlotWindow.SAFE_SetButtonEvent("LEFT", "EXIST", self.SelectItemSlot)
		self.itemSlotWindow.SAFE_SetButtonEvent("RIGHT", "EXIST", self.UnselectItemSlot)

		self.itemSlotWindow.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		self.itemSlotWindow.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		self.btnBuy.SetToggleUpEvent(ui.__mem_func__(self.CancelShopping))
		self.btnBuy.SetToggleDownEvent(ui.__mem_func__(self.OnBuy))

		self.btnSell.SetToggleUpEvent(ui.__mem_func__(self.CancelShopping))
		self.btnSell.SetToggleDownEvent(ui.__mem_func__(self.OnSell))

		self.btnClose.SetEvent(ui.__mem_func__(self.AskClosePrivateShop))

		self.Board.SetCloseEvent(ui.__mem_func__(self.Close))

		if app.ENABLE_RENEWAL_SHOP_SELLING:
			self.tRenewalItems["SELECTED_TEXT"].SetText(localeInfo.SHOP_RENEWAL_SELECTED_INFO % (localeInfo.NumberToString(self.iSelectedItems)))
			self.tRenewalItems["TOTAL_M_TEXT"].SetText(localeInfo.SHOP_RENEWAL_PRICE_INFO % (localeInfo.NumberToStringAsType(self.iTotalMoney, True)))

			self.tRenewalItems["ACCEPT_BTN"].SAFE_SetEvent(self.__RenewalAccept)
			self.tRenewalItems["CLEAR_BUTTON"].SAFE_SetEvent(self.RenewalClean)

		self.Refresh()

	if app.ENABLE_RENEWAL_SHOP_SELLING:
		def AppendInformation(self, bAdded, args):
			if (bAdded):
				self.iSelectedItems += 1
				self.iTotalMoney += args[0]
			else:
				self.iSelectedItems -= 1
				self.iTotalMoney -= args[0]

			self.tRenewalItems["SELECTED_TEXT"].SetText(localeInfo.SHOP_RENEWAL_SELECTED_INFO % (localeInfo.NumberToString(self.iSelectedItems)))
			self.tRenewalItems["TOTAL_M_TEXT"].SetText(localeInfo.SHOP_RENEWAL_PRICE_INFO % (localeInfo.NumberToStringAsType(self.iTotalMoney, True)))

		def __RenewalAccept(self):
			if self.interface:
				self.interface.RenewalShopAccept()

		def RenewalClean(self):
			self.iSelectedItems = 0
			self.iTotalMoney = 0

			self.tRenewalItems["SELECTED_TEXT"].SetText(localeInfo.SHOP_RENEWAL_SELECTED_INFO % (localeInfo.NumberToString(self.iSelectedItems)))
			self.tRenewalItems["TOTAL_M_TEXT"].SetText(localeInfo.SHOP_RENEWAL_PRICE_INFO % (localeInfo.NumberToStringAsType(self.iTotalMoney, True)))

			self.interface.ClearHighlight()
			self.CancelShopping()

		def BindInterface(self, interface):
			self.interface = interface

		def OnMouseLeftButtonDown(self):
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				self.interface.MakeHyperlinkTooltip(hyperlink)

	def Destroy(self):
		self.Close()
		self.ClearDictionary()

		self.tooltipItem = 0
		self.itemSlotWindow = 0
		self.btnBuy = 0
		self.btnSell = 0
		self.btnClose = 0
		self.questionDialog = None
		self.popup = None

		if gcGetEnable("ANCIENT_SHOP_MULTIPLE_BUY"):
			self.vid = 0

	def Open(self, vid):
		if gcGetEnable("ANCIENT_SHOP_MULTIPLE_BUY"):
			self.vid=int(vid)

		isPrivateShop = False
		isMainPlayerPrivateShop = False
		self.tabIdx = 0

		import chr
		if chr.IsNPC(vid):
			isPrivateShop = False
		else:
			isPrivateShop = True

		if player.IsMainCharacterIndex(vid):

			isMainPlayerPrivateShop = True

			self.btnBuy.Hide()
			self.btnSell.Hide()
			self.btnClose.Show()

		else:

			isMainPlayerPrivateShop = False
			self.btnBuy.Show()
			self.btnSell.Show()
			self.btnClose.Hide()

		shop.Open(isPrivateShop, isMainPlayerPrivateShop)
		self.RefreshTabs()
		self.Refresh()
		self.SetTop()
		self.Show()

		(self.xShopStart, self.yShopStart, z) = player.GetMainCharacterPosition()

	def Close(self):
		if self.itemBuyQuestionDialog:
			self.itemBuyQuestionDialog.Close()
			self.itemBuyQuestionDialog = None
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
		if self.questionDialog:
			self.OnCloseQuestionDialog()
		if gcGetEnable("ANCIENT_SHOP_MULTIPLE_BUY"):
			self.OnCloseMultipleAncientBuyWindow()
		shop.Close()
		net.SendShopEndPacket()
		if app.ENABLE_RENEWAL_SHOP_SELLING:
			self.RenewalClean()
		self.CancelShopping()
		self.tooltipItem.HideToolTip()
		self.Hide()

	def GetIndexFromSlotPos(self, slotPos):
		return self.tabIdx * shop.SHOP_SLOT_COUNT + slotPos

	def OnClickTabButton(self, idx):
		self.tabIdx = idx
		self.Refresh()

	def AskClosePrivateShop(self):
		questionDialog = uiCommon.QuestionDialog()
		questionDialog.SetText(localeInfo.PRIVATE_SHOP_CLOSE_QUESTION)
		questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnClosePrivateShop))
		questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
		questionDialog.Open()
		self.questionDialog = questionDialog

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		return True

	def OnClosePrivateShop(self):
		net.SendChatPacket("/close_shop")
		self.OnCloseQuestionDialog()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnBuy(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)
		app.SetCursor(app.BUY)
		self.btnSell.SetUp()

	def OnSell(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_SELL_INFO)
		app.SetCursor(app.SELL)
		self.btnBuy.SetUp()

	def CancelShopping(self):
		self.btnBuy.SetUp()
		self.btnSell.SetUp()
		app.SetCursor(app.NORMAL)

	def __OnClosePopupDialog(self):
		self.pop = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SellAttachedItem(self):

		if shop.IsPrivateShop():
			mouseModule.mouseController.DeattachObject()
			return

		attachedSlotType = mouseModule.mouseController.GetAttachedType()
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		attachedCount = mouseModule.mouseController.GetAttachedItemCount()
		attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

		if player.SLOT_TYPE_INVENTORY == attachedSlotType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:

			item.SelectItem(attachedItemIndex)

			if item.IsAntiFlag(item.ANTIFLAG_SELL):
				popup = uiCommon.PopupDialog()
				popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				popup.SetAcceptEvent(self.__OnClosePopupDialog)
				popup.SetAutoClose()
				popup.Open()
				self.popup = popup
				return

			itemtype = player.INVENTORY

			if player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedSlotType:
				itemtype = player.DRAGON_SOUL_INVENTORY

			itemPrice = item.GetISellItemPrice()

			if item.Is1GoldItem():
				itemPrice = attachedCount / itemPrice / 5
			else:
				itemPrice = itemPrice * max(1, attachedCount) / 5

			itemName = item.GetItemName()

			questionDialog = uiCommon.QuestionDialog()
			metinSlot = [player.GetItemMetinSocket(player.INVENTORY, attachedSlotPos, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
			attrSlot = [player.GetItemAttribute(player.INVENTORY, attachedSlotPos, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]
			questionDialog.SetTextPrice(localeInfo.DO_YOU_SELL_ITEM(itemName, attachedCount, itemPrice), buyVnum = attachedItemIndex, metinSlot = metinSlot, attrSlot = attrSlot)

			questionDialog.SetAcceptEvent(lambda arg1=attachedSlotPos, arg2=attachedCount, arg3 = itemtype: self.OnSellItem(arg1, arg2, arg3))
			questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			questionDialog.Open()
			self.questionDialog = questionDialog

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		else:
			snd.PlaySound("sound/ui/loginfail.wav")

		mouseModule.mouseController.DeattachObject()

	def OnSellItem(self, slotPos, count, itemtype):
		net.SendShopSellPacketNew(slotPos, count, itemtype)
		snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SelectEmptySlot(self, selectedSlotPos):

		isAttached = mouseModule.mouseController.isAttached()
		if isAttached:
			self.SellAttachedItem()

	def UnselectItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			self.AnswerBuyItem(False)

		selectedSlotPos = self.__LocalToGlobalSlot(selectedSlotPos)

		if gcGetEnable("ANCIENT_SHOP_MULTIPLE_BUY") and self.__CanRunMultipleAncientShopBuy():
			self.__OpenMulitpleAncientShopBuy(selectedSlotPos)
		else:
			self.AskBuyItem(selectedSlotPos)

	def SelectItemSlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			self.AnswerBuyItem(False)

		isAttached = mouseModule.mouseController.isAttached()
		selectedSlotPos = self.__LocalToGlobalSlot(selectedSlotPos)
		if isAttached:
			self.SellAttachedItem()
		else:
			if True == shop.IsMainPlayerPrivateShop():
				return

			curCursorNum = app.GetCursor()
			if app.BUY == curCursorNum:
				self.AskBuyItem(selectedSlotPos)

			elif app.SELL == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_SELL_INFO)

			else:
				selectedItemID = shop.GetItemID(selectedSlotPos)
				itemCount = shop.GetItemCount(selectedSlotPos)

				type = player.SLOT_TYPE_SHOP
				if shop.IsPrivateShop():
					type = player.SLOT_TYPE_PRIVATE_SHOP

				mouseModule.mouseController.AttachObject(self, type, selectedSlotPos, selectedItemID, itemCount)
				mouseModule.mouseController.SetCallBack("INVENTORY", ui.__mem_func__(self.DropToInventory))
				snd.PlaySound("sound/ui/pick.wav")

	def DropToInventory(self):
		attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
		self.AskBuyItem(attachedSlotPos)

	def AskBuyItem(self, slotPos):
		itemIndex = shop.GetItemID(slotPos)
		itemPrice = shop.GetItemPrice(slotPos)
		itemCount = shop.GetItemCount(slotPos)

		itemVnumPrice = shop.GetItemPriceVnum(slotPos)

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()

		itemBuyQuestionDialog = uiCommon.QuestionDialog()
		if itemVnumPrice != 0:
			item.SelectItem(itemVnumPrice)
			itemVnumPriceName = item.GetItemName()
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(shop.GetItemAttribute(itemVnumPrice, i))
			itemBuyQuestionDialog.SetTextPrice(localeInfo.DO_YOU_BUY_ITEM_FOR_ITEM(itemName, itemCount, itemPrice, itemVnumPriceName), itemVnumPrice, itemIndex, attrSlot = attrSlot)
		else:
			itemBuyQuestionDialog.SetTextPrice(localeInfo.DO_YOU_BUY_ITEM(itemName, itemCount, itemPrice), buyVnum = itemIndex)

		itemBuyQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerBuyItem(arg))
		itemBuyQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerBuyItem(arg))
		itemBuyQuestionDialog.Open()
		itemBuyQuestionDialog.pos = slotPos
		self.itemBuyQuestionDialog = itemBuyQuestionDialog

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def AnswerBuyItem(self, flag):

		if flag:
			pos = self.itemBuyQuestionDialog.pos
			net.SendShopBuyPacket(pos)

		self.itemBuyQuestionDialog.Close()
		self.itemBuyQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def SetItemToolTip(self, tooltipItem):
		if self.tooltipItem != 0:
			self.tooltipItem.HideToolTip()
		self.tooltipItem = tooltipItem

	def OverInItem(self, slotIndex):
		if mouseModule.mouseController.isAttached():
			return

		slotIndex = self.__LocalToGlobalSlot(slotIndex)
		if 0 != self.tooltipItem:
			self.tooltipItem.SetShopItem(slotIndex)

	def OverOutItem(self):
		if 0 != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def OnUpdate(self):
		USE_SHOP_LIMIT_RANGE = 1000

		(x, y, z) = player.GetMainCharacterPosition()
		if abs(x - self.xShopStart) > USE_SHOP_LIMIT_RANGE or abs(y - self.yShopStart) > USE_SHOP_LIMIT_RANGE:
			self.RemoveFlag("animate")
			self.Close()

	if gcGetEnable("ANCIENT_SHOP_MULTIPLE_BUY"):
			#@Private methods
		def __IsAncientShop(self):
			if not self.vid:
				return

			chr.SelectInstance(self.vid)
			return True
			# return (uiMultipleAncientShopBuy.ANCIENT_SHOP_VNUM == chr.GetRace())

		def ToolTipGetter(self):
			return self.__IsAncientShop()

		def __RefreshAncientShopTooltip(self):
			if not self.tooltipItem or\
				not self.__IsAncientShop():
				return

			import grp
			self.tooltipItem.AppendShortcut([app.DIK_LCONTROL, app.DIK_LSHIFT, app.DIK_RMBUTTON], "Kup")

		def __CanRunMultipleAncientShopBuy(self):
			return (self.__IsAncientShop() and\
					app.IsPressed(app.DIK_LCONTROL) and app.IsPressed(app.DIK_LSHIFT))

		def __OpenMulitpleAncientShopBuy(self, realSlotPos):
			self.ancientShopMultipleBuyWindow = uiMultipleAncientShopBuy.AncientShopMultipleBuyWindow()
			self.ancientShopMultipleBuyWindow.BuildPageInformation(realSlotPos)
			self.ancientShopMultipleBuyWindow.SetAcceptEvent(self.OnAcceptMultipleAncientBuyWindow, realSlotPos)
			self.ancientShopMultipleBuyWindow.SetCloseEvent(self.OnCloseMultipleAncientBuyWindow)
			self.ancientShopMultipleBuyWindow.Show()

			#@Public methods
		def OnAcceptMultipleAncientBuyWindow(self, realSlotPos):
			if not self.ancientShopMultipleBuyWindow:
				return

			_quantityValue = self.ancientShopMultipleBuyWindow.GetQuantityValue()
			if _quantityValue:
				net.SendShopMultipleBuyPacket(realSlotPos, _quantityValue)

			self.OnCloseMultipleAncientBuyWindow()

		def OnCloseMultipleAncientBuyWindow(self):
			if not self.ancientShopMultipleBuyWindow:
				return

			self.ancientShopMultipleBuyWindow.Hide()
			self.ancientShopMultipleBuyWindow = None

class MallPageDialog(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()

	def Open(self):
		scriptLoader = ui.PythonScriptLoader()
		scriptLoader.LoadScriptFile(self, "uiscript/mallpagedialog.py")

		self.GetChild("titlebar").SetCloseEvent(ui.__mem_func__(self.Close))

		(x, y)=self.GetGlobalPosition()
		x+=10
		y+=30

		MALL_PAGE_WIDTH = 600
		MALL_PAGE_HEIGHT = 480

		app.ShowWebPage(
			"http://metin2.co.kr/08_mall/game_mall/login_fail.htm",
			(x, y, x+MALL_PAGE_WIDTH, y+MALL_PAGE_HEIGHT))

		self.Lock()
		self.Show()

	def Close(self):
		app.HideWebPage()
		self.Unlock()
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
