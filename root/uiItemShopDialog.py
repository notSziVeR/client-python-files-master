import ui
import app
import net
import item
import time
import wndMgr
import player
import uiCommon
import datetime
import exception
import constInfo
import uiToolTip
import localeInfo
import webbrowser

from _weakref import proxy

def	DEHASH_ITEM(sHash):
	iVnum, iCount, iPrice, tMetinSlot, tDiscount, tSpecialOffer = sHash.split("|")
	return int(iVnum), int(iCount), int(iPrice), [int(iSocket) for iSocket in tMetinSlot.split("/")], [int(iRec) for iRec in tDiscount.split("/")], [int(iRec) for iRec in tSpecialOffer.split("/")]

def	DEHASH_CATEGORY(sHash):
	iID, sName, tDiscount = sHash.split("|")
	return int(iID) + 1, sName.replace("_", " "), [int(iRec) for iRec in tDiscount.split("/")]

def	NumberToMoneyString_DC(money):
	return "%s DC" % ('.'.join([ i-3<0 and str(money)[:i] or str(money)[i-3:i] for i in range(len(str(money))%3, len(str(money))+1, 3) if i ]))

class ItemShopDialog(ui.ScriptWindow):

	ITEM_SHOP_ITEMS = dict()
	SPECIAL_OFFER_ID = 0
	ITEMSHOP_DONATE_BUTTON_URL = "https://xamia.bz/dashboard/payments"

	class CategoryButton(ui.RadioButton):

		BUTTON_IMAGES = ("itemshop/category_button_n.png", "itemshop/category_button_h.png", "itemshop/category_button_h.png")

		def	__init__(self, sHash):
			global DEHASH_CATEGORY
			ui.RadioButton.__init__(self)

			self.sHash = sHash
			self.iID, self.sName, self.tDiscount = DEHASH_CATEGORY(sHash)

			self.Objects = {}
			self.SetUpVisual(self.BUTTON_IMAGES[0])
			self.SetOverVisual(self.BUTTON_IMAGES[1])
			self.SetDownVisual(self.BUTTON_IMAGES[2])
			self.SetButtonText(self.sName)

		def	__del__(self):
			ui.RadioButton.__del__(self)
			self.iID, self.sName, self.tDiscount = -1, "", (0, 0)
			self.Objects = {}

		def SetParent(self, parent):
			ui.RadioButton.SetParent(self, parent)

			self.parent=proxy(parent)
			self.SAFE_SetEvent(self.parent.SelectItem, self)

		def	SetButtonText(self, sTxt):
			self.Objects["TITLE"] = ui.TextLine()
			self.Objects["TITLE"].SetParent(self)
			self.Objects["TITLE"].SetPosition(0, 0)
			self.Objects["TITLE"].SetWindowHorizontalAlignCenter()
			self.Objects["TITLE"].SetHorizontalAlignCenter()
			self.Objects["TITLE"].SetWindowVerticalAlignCenter()
			self.Objects["TITLE"].SetVerticalAlignCenter()
			self.Objects["TITLE"].SetText(sTxt)
			self.Objects["TITLE"].SetPackedFontColor(0xffDCDBD8)
			self.Objects["TITLE"].Show()

		def	GetHash(self):
			return self.sHash

		def	GetID(self):
			return self.iID

		def	GetName(self):
			return self.sName

		def	Rehash(self, sHash):
			global DEHASH_CATEGORY
			self.sHash = sHash
			self.iID, self.sName, self.tDiscount = DEHASH_CATEGORY(sHash)

	class ItemWindow(ui.ImageBox):

		BASE_IMAGE = "itemshop/item_window.png"
		WINDOW_SIZE = (228, 116)
		BUTTON_PURCHASE = ("itemshop/button_purchase_n.png", "itemshop/button_purchase_h.png", "itemshop/button_purchase_d.png")

		###
		COSTUME_BODY = 0
		COSTUME_HAIR = 1
		COSTUME_WEAPON = 2
		SPECIAL_ATTR_CONFIG = {
								COSTUME_BODY : (((item.APPLY_ATTBONUS_HUMAN, 5), (item.APPLY_CRITICAL_PCT, 5)), ((item.APPLY_ATTBONUS_MONSTER, 5), (item.APPLY_CRITICAL_PCT, 5))),
								COSTUME_HAIR : (((item.APPLY_MAX_HP, 1000), (item.APPLY_SKILL_DAMAGE_BONUS, 3)), ((item.APPLY_MAX_HP, 1000), (item.APPLY_ATT_GRADE_BONUS, 30))),
								COSTUME_WEAPON : (((item.APPLY_CAST_SPEED, 10), (item.APPLY_ATTBONUS_HUMAN, 5), (item.APPLY_PENETRATE_PCT, 5)), ((item.APPLY_ATT_SPEED, 10), (item.APPLY_ATTBONUS_MONSTER, 5), (item.APPLY_PENETRATE_PCT, 5))),
							}

		def	__init__(self, parent, winParent, sItemHash):
			global DEHASH_ITEM
			ui.ImageBox.__init__(self)

			self.scriptParent = proxy(parent)
			self.windowParent = proxy(winParent)
			self.sHash = sItemHash
			self.iVnum, self.iCount, self.iPrice, self.tMetinSlot, self.iDiscount, self.tSpecialOffer = DEHASH_ITEM(sItemHash)
			self.ttDiscountTime = 0
			self.Objects = {}
			self.toolTipItem = uiToolTip.ItemToolTip()

			self.__BuildWindow()

		def	__del__(self):
			ui.ImageBox.__del__(self)
			self.iVnum, self.iCount, self.iPrice, self.tMetinSlot, self.iDiscount, self.tSpecialOffer = 0, 0, 0, list(), list(), list()
			self.ttDiscountTime = 0
			self.Objects = {}
			self.toolTipItem = None

		def	__BuildWindow(self):
			## Image
			self.LoadImage(self.BASE_IMAGE)

			## Image Window
			self.Objects["IMAGE_WINDOW"] = ui.Window()
			self.Objects["IMAGE_WINDOW"].SetParent(self)
			self.Objects["IMAGE_WINDOW"].SetPosition(9, 3)
			self.Objects["IMAGE_WINDOW"].SetSize(45, 110)
			self.Objects["IMAGE_WINDOW"].SAFE_SetOverInEvent(self.__OverInItem)
			self.Objects["IMAGE_WINDOW"].SAFE_SetOverOutEvent(self.__OverOutItem)
			self.Objects["IMAGE_WINDOW"].Show()

			## Image
			item.SelectItem(self.iVnum)
			self.Objects["IMAGE"] = ui.ImageBox()
			self.Objects["IMAGE"].SetParent(self.Objects["IMAGE_WINDOW"])
			self.Objects["IMAGE"].AddFlag("not_pick")
			self.Objects["IMAGE"].SetWindowHorizontalAlignCenter()
			self.Objects["IMAGE"].SetWindowVerticalAlignCenter()
			self.Objects["IMAGE"].LoadImage(item.GetIconImageFileName())
			self.Objects["IMAGE"].Show()

			## Special Offer
			self.Objects["SPECIAL_OFFER"] = ui.TextLine()
			self.Objects["SPECIAL_OFFER"].SetParent(self)
			self.Objects["SPECIAL_OFFER"].SetPosition(223, 55)

			if self.IsSpecialOffer() and self.tSpecialOffer[0] == 1:
				if self.tSpecialOffer[1] >= 1:
					self.Objects["SPECIAL_OFFER"].SetText(localeInfo.ITEMSHOP_SPECIAL_OFFER_LIMITED_QUANTITY % self.tSpecialOffer[1])

			self.Objects["SPECIAL_OFFER"].Show()

			## TimeLimit
			self.Objects["TIME_LIMIT"] = ui.TextLine()
			self.Objects["TIME_LIMIT"].SetParent(self)
			self.Objects["TIME_LIMIT"].SetPosition(111, 55)
			self.Objects["TIME_LIMIT"].SetText(localeInfo.ITEMSHOP_ITEM_TIME % self.__GetTimeLeft())
			self.Objects["TIME_LIMIT"].SetPackedFontColor(0xffE1E1D1)
			self.Objects["TIME_LIMIT"].Show()

			## Main board
			self.Objects["MAIN_BOARD"] = ui.Window()
			self.Objects["MAIN_BOARD"].SetParent(self)
			self.Objects["MAIN_BOARD"].SetPosition(57, 3)
			self.Objects["MAIN_BOARD"].SetSize(168, 110)
			self.Objects["MAIN_BOARD"].Show()

			## Name
			self.Objects["NAME"] = ui.TextLine()
			self.Objects["NAME"].SetParent(self.Objects["MAIN_BOARD"])
			self.Objects["NAME"].SetPosition(0, 11)
			self.Objects["NAME"].SetWindowHorizontalAlignCenter()
			self.Objects["NAME"].SetHorizontalAlignCenter()
			self.Objects["NAME"].SetText(item.GetItemName())
			self.Objects["NAME"].Show()

			## Count
			self.Objects["COUNT"] = ui.TextLine()
			self.Objects["COUNT"].SetParent(self.Objects["MAIN_BOARD"])
			self.Objects["COUNT"].SetPosition(0, 63)
			self.Objects["COUNT"].SetWindowHorizontalAlignCenter()
			self.Objects["COUNT"].SetHorizontalAlignCenter()
			self.Objects["COUNT"].SetText(localeInfo.ITEMSHOP_ITEM_QUANTITY % self.iCount)
			self.Objects["COUNT"].Show()

			## Price
			self.Objects["PRICE"] = ui.TextLine()
			self.Objects["PRICE"].SetParent(self.Objects["MAIN_BOARD"])
			self.Objects["PRICE"].SetPosition(0, 26)
			self.Objects["PRICE"].SetWindowHorizontalAlignCenter()
			self.Objects["PRICE"].SetHorizontalAlignCenter()
			self.Objects["PRICE"].SetText(localeInfo.ITEMSHOP_ITEM_PRICE % NumberToMoneyString_DC(self.iPrice))
			self.Objects["PRICE"].SetPackedFontColor(0xffD2B15F)
			self.Objects["PRICE"].Show()

			## Button Purchase
			self.Objects["PURCHASE"] = ui.Button()
			self.Objects["PURCHASE"].SetParent(self.Objects["MAIN_BOARD"])
			self.Objects["PURCHASE"].SetPosition(50, 87)
			self.Objects["PURCHASE"].SetUpVisual(self.BUTTON_PURCHASE[0])
			self.Objects["PURCHASE"].SetOverVisual(self.BUTTON_PURCHASE[1])
			self.Objects["PURCHASE"].SetDownVisual(self.BUTTON_PURCHASE[2])
			self.Objects["PURCHASE"].SAFE_SetEvent(self.__PurchaseItem)
			self.Objects["PURCHASE"].Show()

		def	__PurchaseItem(self):
			self.scriptParent.AskBuyItem(self)

		def	__OverInItem(self):
			if self.toolTipItem:
				self.toolTipItem.ClearToolTip()
				self.toolTipItem.AddItemData(self.iVnum, self.__GetCurrentSockets(), self.__DeduceItemAttributes())
				self.toolTipItem.ShowToolTip()

		def	__OverOutItem(self):
			if self.toolTipItem:
				self.toolTipItem.HideToolTip()

		def	GetHash(self):
			return self.sHash

		def	IsSpecialOffer(self):
			return self.tSpecialOffer[1] > 0

		def	Rehash(self, sHash):
			global DEHASH_ITEM
			self.sHash = sHash
			self.iVnum, self.iCount, self.iPrice, self.tMetinSlot, self.iDiscount, self.tSpecialOffer = DEHASH_ITEM(sHash)

			## Name
			item.SelectItem(self.iVnum)
			self.Objects["NAME"].SetText(item.GetItemName())

			## TimeLimit
			self.Objects["TIME_LIMIT"].SetText(localeInfo.ITEMSHOP_ITEM_TIME % self.__GetTimeLeft())

			## Count
			self.Objects["COUNT"].SetText(localeInfo.ITEMSHOP_ITEM_QUANTITY % self.iCount)

			## Price
			self.Objects["PRICE"].SetText(localeInfo.ITEMSHOP_ITEM_PRICE % NumberToMoneyString_DC(self.iPrice))

			## Image
			self.Objects["IMAGE"].LoadImage(item.GetIconImageFileName())

			if not self.IsSpecialOffer():
				self.Objects["SPECIAL_OFFER"].SetText("")
			elif self.IsSpecialOffer() and self.tSpecialOffer[0] == 1:
				if self.tSpecialOffer[1] <= 0:
					self.Hide()
				else:
					self.Objects["SPECIAL_OFFER"].SetText(localeInfo.ITEMSHOP_SPECIAL_OFFER_LIMITED_QUANTITY % self.tSpecialOffer[1])

		def	__GetTimeLeft(self):
			item.SelectItem(self.iVnum)
			bHasRealtimeFlag = False

			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = True
					break

			if bHasRealtimeFlag:
				return localeInfo.SecondToDHMS(self.tMetinSlot[0])
			elif constInfo.IS_AUTO_POTION(self.iVnum) or (item.GetItemType() == item.ITEM_TYPE_UNIQUE and item.GetValue(0) > 0):
				return localeInfo.SecondToDHMS(item.GetValue(0)*60)

			return localeInfo.ITEMSHOP_ITEM_TIME_NO_LIMIT

		def	__GetCurrentSockets(self):
			item.SelectItem(self.iVnum)
			bHasRealtimeFlag = False

			for i in xrange(item.LIMIT_MAX_NUM):
				(limitType, limitValue) = item.GetLimit(i)

				if item.LIMIT_REAL_TIME == limitType:
					bHasRealtimeFlag = True
					break

			if bHasRealtimeFlag:
				return [self.tMetinSlot[0] + app.GetGlobalTimeStamp()] + self.tMetinSlot[1:9]
			elif constInfo.IS_AUTO_POTION(self.iVnum) or (item.GetItemType() == item.ITEM_TYPE_UNIQUE and item.GetValue(0) > 0):
				return self.tMetinSlot[0:2] + [item.GetValue(0)] + self.tMetinSlot[3:9]

			return self.tMetinSlot

		def	__DeduceItemAttributes(self):
			item.SelectItem(self.iVnum)
			if item.GetItemType() == item.ITEM_TYPE_COSTUME:
				attrKey = self.tMetinSlot[1]-1
				iCostumeSpecialType = self.COSTUME_WEAPON if item.GetValue(0) == 1 else item.GetItemSubType()

				if iCostumeSpecialType in self.SPECIAL_ATTR_CONFIG:
					if attrKey >= 0 and attrKey < len(self.SPECIAL_ATTR_CONFIG[iCostumeSpecialType]):
						return self.SPECIAL_ATTR_CONFIG[iCostumeSpecialType][attrKey] + ((0, 0),) * (player.ATTRIBUTE_SLOT_MAX_NUM-len(self.SPECIAL_ATTR_CONFIG[iCostumeSpecialType][attrKey]))

			return 0

		def	OnUpdate(self):
			if self.tSpecialOffer[1] > 0:
				if self.tSpecialOffer[0] == 0:
					if self.ttDiscountTime == 0:
						self.ttDiscountTime = self.tSpecialOffer[1] - int(time.time())

					if self.ttDiscountTime >= app.GetTime():
						self.Objects["SPECIAL_OFFER"].SetText(localeInfo.ITEMSHOP_SPECIAL_OFFER_LIMITED_TIME % localeInfo.SecondToDHMS(self.ttDiscountTime-app.GetTime()))
					else:
						self.tSpecialOffer = (0, 0)
						self.ttDiscountTime = 0
						self.Hide()

		def SetPosition(self, iX, iY):
			ui.ImageBox.SetPosition(self, iX, iY)

			(itemAbsoluteX, itemAbsoluteY) = (iX + self.Objects["PURCHASE"].GetLocalPosition()[0], iY + self.Objects["PURCHASE"].GetLocalPosition()[1])
			if ((itemAbsoluteX + self.Objects["PURCHASE"].GetWidth()) > self.windowParent.GetWidth() or itemAbsoluteX <= 0) or ((itemAbsoluteY + self.Objects["PURCHASE"].GetHeight()) > self.windowParent.GetHeight() or itemAbsoluteY <= 0):
				self.Objects["PURCHASE"].Hide()
			else:
				self.Objects["PURCHASE"].Show()

	def	__init__(self):
		ui.ScriptWindow.__init__(self)

		self.Objects = {}
		self.iCurrentCategory = -1
		self.itemBuyQuestionDialog = uiCommon.QuestionDialog()
		self.__LoadWindow()

	def	__del__(self):
		ui.ScriptWindow.__del__(self)
		self.tooltipItem = None
		self.Objects = {}
		self.iCurrentCategory = -1
		self.itemBuyQuestionDialog = None

	def	Destroy(self):
		self.ClearDictionary()
		self.tooltipItem = None
		self.Objects = {}
		self.iCurrentCategory = -1
		self.itemBuyQuestionDialog = None

	def	__LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/itemshop_main.py")
		except:
			exception.Abort("ItemShopDialog.__LoadWindow.LoadObject")

		try:
			self.GetChild("Exit_Button").SetEvent(ui.__mem_func__(self.Close))

			## Texts
			# self.Objects["GREETINGS"] = self.GetChild("Greetings_Text")
			self.Objects["CASH"] = self.GetChild("Cash_Text")
			self.Objects["CATEGORY_NAME"] = self.GetChild("Category_Name_Text")

			## Category listbox
			self.Objects["CATEGORIES"] = self.GetChild("Category_ListBox")

			## Items window
			self.Objects["ITEMS"] = self.GetChild("Items_ListBox")

			## Donate button
			self.Objects["DONATE"] = self.GetChild("Donate_Button")
		except:
			exception.Abort("ItemShopDialog.__LoadWindow.BindObject")

		## Buttons
		self.Objects["DONATE"].SAFE_SetEvent(self.__TopUpAccount)

		## ListBox
		self.Objects["CATEGORIES"].SetItemSize(137, 39)
		self.Objects["CATEGORIES"].SetViewItemCount(9)
		self.Objects["CATEGORIES"].SetItemStep(43)
		self.Objects["CATEGORIES"].SetScrollBar(self.__MakeScrollBar("scrollbar_categories_field.png", "scroll_cat_n.png", 160, 87))
		self.Objects["CATEGORIES"].SetSelectEvent(ui.__mem_func__(self.__OnSelectCategory))
		self.Objects["CATEGORIES"].SetScrollWheelEvent(self.Objects["CATEGORIES"].scrollBar.OnWheelMove)

		self.Objects["ITEMS"].SetScrollBar(self.__MakeScrollBar("scrollbar_items_field.png", "scroll_cat_n.png", 917, 87))
		self.Objects["ITEMS"].SetScrollWheelEvent(self.Objects["ITEMS"].scrollBar.OnWheelMove)

		self.SetScrollWheelEvent(self.OnWheelMove)

		## Building special category
		self.__BuildSpecialOfferCategory()

		## Seleting category
		self.OnRecvCashUpdate(0)
		self.__OnSelectCategory(self.Objects["CATEGORIES"].itemList[0])

		self.SetCenterPosition()
		self.Hide()

	def	__BuildSpecialOfferCategory(self):
		self.Objects["CATEGORIES"].AppendItem(self.CategoryButton("%d|%s|0/0" % (self.SPECIAL_OFFER_ID-1, localeInfo.ITEMSHOP_SPECIAL_OFFER_TITLE)))
		self.ITEM_SHOP_ITEMS[self.SPECIAL_OFFER_ID] = []

	def	__MakeScrollBar(self, sField, sCursor, iX, iY):
		newScroll = ui.NewScrollBarItemShop("itemshop/", sField, sCursor)
		newScroll.SetParent(self)
		newScroll.SetPosition(iX, iY)
		newScroll.Show()

		return newScroll

	def	__TopUpAccount(self):
		webbrowser.open(self.ITEMSHOP_DONATE_BUTTON_URL)

	def	__OnSelectCategory(self, selItem):
		for obj in self.Objects["CATEGORIES"].itemList:
			if obj == selItem:
				obj.Down()
			else:
				obj.SetUp()

		self.Objects["CATEGORY_NAME"].SetText(selItem.GetName())
		self.iCurrentCategory = selItem.GetID()
		self.__ClearItems()

		if self.iCurrentCategory in self.ITEM_SHOP_ITEMS:
			for rItem in self.ITEM_SHOP_ITEMS[self.iCurrentCategory]:
				self.Objects["ITEMS"].AppendItem(rItem)

	def	__ClearItems(self):
		for rItem in self.Objects["ITEMS"].itemList:
			rItem.Hide()

		self.Objects["ITEMS"].RemoveAllItems()

	""" Recv """
	def	OnRecvClear(self):
		self.Objects["CATEGORIES"].RemoveAllItems()
		self.__ClearItems()

		self.ITEM_SHOP_ITEMS = dict()

		## Rebuild special offers button
		self.__BuildSpecialOfferCategory()

	def	OnRecvCategory(self, sHashOld, sHashNew):
		global DEHASH_CATEGORY
		iID, sName, tDiscount = DEHASH_CATEGORY(sHashOld)

		bExists = False
		for rItem in self.Objects["CATEGORIES"].itemList:
			if rItem.GetHash() == sHashOld:
				bExists = True
				break

		if bExists:
			if sHashNew == "0":
				self.Objects["CATEGORIES"].RemoveItem(rItem)
				if self.iCurrentCategory == iID:
					self.__ClearItems()
					self.iCurrentCategory = -1
			elif sItemHash != sHashNew:
				rItem.Rehash(sHashNew)
		else:
			self.Objects["CATEGORIES"].AppendItem(self.CategoryButton(sHashOld))
			self.ITEM_SHOP_ITEMS[iID] = []

	def	OnRecvItem(self, bCategoryID, sItemHash, sItemHashNew):
		bCategoryID += 1

		bExists = False
		if bCategoryID in self.ITEM_SHOP_ITEMS:
			for rItem in self.ITEM_SHOP_ITEMS[bCategoryID]:
				if rItem.GetHash() == sItemHash:
					bExists = True
					break

		if bExists:
			if sItemHashNew == "0":
				rItem.Hide()
				self.ITEM_SHOP_ITEMS[bCategoryID].remove(rItem)
				for rItem2 in self.Objects["ITEMS"].itemList:
					if rItem2.GetHash() == sItemHash:
						self.Objects["ITEMS"].RemoveItem(rItem2)
			elif sItemHash != sItemHashNew:
				rItem.Rehash(sItemHashNew)
		else:
			itemShopItem = self.ItemWindow(self, self.Objects["ITEMS"], sItemHash)
			if itemShopItem.IsSpecialOffer():
				bCategoryID = self.SPECIAL_OFFER_ID

			if not bCategoryID in self.ITEM_SHOP_ITEMS:
				self.ITEM_SHOP_ITEMS[bCategoryID] = []

			self.ITEM_SHOP_ITEMS[bCategoryID].append(itemShopItem)
			if self.iCurrentCategory == bCategoryID:
				self.Objects["ITEMS"].AppendItem(itemShopItem)

	def	OnRecvCashUpdate(self, iCash):
		global NumberToMoneyString_DC
		self.Objects["CASH"].SetText(NumberToMoneyString_DC(iCash))

	def	OnRecvSpecialOfferUpdate(self, sOldHash, sNewHash):
		global DEHASH_ITEM
		bExists = False
		for rItem in self.ITEM_SHOP_ITEMS[self.SPECIAL_OFFER_ID]:
			if rItem.GetHash() == sOldHash:
				bExists = True
				break

		if bExists:
			self.iVnum, self.iCount, self.iPrice, self.tMetinSlot, self.iDiscount, self.tSpecialOffer = DEHASH_ITEM(sItemHash)
			if self.tSpecialOffer[1] > 0:
				rItem.Rehash(sNewHash)
			else:
				self.ITEM_SHOP_ITEMS[self.SPECIAL_OFFER_ID].remove(rItem)
				if rItem in self.Objects["ITEMS"].itemList:
					self.Objects["ITEMS"].RemoveItem(rItem)
		else:
			itemShopItem = self.ItemWindow(self, self.Objects["ITEMS"], sOldHash)
			self.ITEM_SHOP_ITEMS[self.SPECIAL_OFFER_ID].append(itemShopItem)
			if self.iCurrentCategory == self.SPECIAL_OFFER_ID:
				self.Objects["ITEMS"].AppendItem(itemShopItem)
	""" """

	def AskBuyItem(self, rItem):
		global NumberToMoneyString_DC
		itemIndex = rItem.iVnum
		itemPrice = rItem.iPrice
		itemCount = rItem.iCount

		item.SelectItem(itemIndex)
		itemName = item.GetItemName()

		self.itemBuyQuestionDialog.SetText(localeInfo.DO_YOU_BUY_ITEM_FROM_ITEMSHOP(itemName, itemCount, NumberToMoneyString_DC(itemPrice)))
		self.itemBuyQuestionDialog.SetAcceptEvent(lambda me = proxy(self), arg=TRUE: me.AnswerBuyItem(arg))
		self.itemBuyQuestionDialog.SetCancelEvent(lambda me = proxy(self), arg=FALSE: me.AnswerBuyItem(arg))
		self.itemBuyQuestionDialog.Open()
		self.itemBuyQuestionDialog.pos = rItem.GetHash()

	def AnswerBuyItem(self, flag):

		if flag:
			pos = self.itemBuyQuestionDialog.pos
			net.SendChatPacket("/itemshop_purchase %s" % pos)

		self.itemBuyQuestionDialog.Close()

	def	OnWheelMove(self, iLen):
		if not self.IsShow():
			return

		xMouse, yMouse = wndMgr.GetMousePosition()

		## Category
		(category_x, category_y) = self.Objects["CATEGORIES"].GetGlobalPosition()
		(category_xEnd, category_yEnd) = (category_x + self.Objects["CATEGORIES"].GetWidth(), category_y + self.Objects["CATEGORIES"].GetHeight())
		if xMouse >= category_x and xMouse <= category_xEnd:
			if yMouse >= category_y and yMouse <= category_yEnd:
				self.Objects["CATEGORIES"].scrollBar.OnScrollWheelEvent(iLen)
				return

		## Items
		(items_x, items_y) = self.Objects["ITEMS"].GetGlobalPosition()
		(items_xEnd, items_yEnd) = (items_x + self.Objects["ITEMS"].GetWidth(), items_y + self.Objects["ITEMS"].GetHeight())
		if xMouse >= items_x and xMouse <= items_xEnd:
			if yMouse >= items_y and yMouse <= items_yEnd:
				self.Objects["ITEMS"].scrollBar.OnScrollWheelEvent(iLen)
				return

	def	Close(self):
		net.SendChatPacket("/request_itemshop")
		self.Hide()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			# self.Objects["GREETINGS"].SetText(localeInfo.ITEMSHOP_GREETINGS % player.GetName())
			self.Show()
			self.SetTop()

	def	OnUpdate(self):
		for rItem in self.Objects["ITEMS"].itemList:
			rItem.OnUpdate()

