"""File: root/uiMultipleAncientShopBuy.py"""

__author__ = "Zorls"
__copyright__ = "Copyright 2021, Rodnia2"

__version__ = "1.0.0"
__maintainer__ = "Zorls"
__status__ = "Production"

import ui, uiScriptLocale, shop,\
 item, ime, wndMgr, grp, localeInfo

ANCIENT_SHOP_VNUM = 9003 #NPC from ancient shop vnum
MAXIMUM_MULTIPLE_BUY_ITENS = 2000 #Maximum quantity of itens the player can buy at same time

class AncientShopMultipleBuyWindow(ui.ScriptWindow):
	"""Static Values, the design from this window
		its based in this page size values, dont touch in them"""
	WINDOW_SIZE = (170, 110) #Size of window AND board
	EDITLINE_SIZE = (60, 18) #Size from editline

	def __init__(self):
		super(AncientShopMultipleBuyWindow, self).__init__()

		self.__RunPreWindowEvent()
		self.__Initialize()
		self.__LoadWindow()

	def __del__(self):
		super(AncientShopMultipleBuyWindow, self).__del__()

		#@Private methods
	def __RunPreWindowEvent(self):
		for flag in ["movable", "float"]:
			self.AddFlag(flag)
		self.SetSize(*self.WINDOW_SIZE)
		self.Hide()

	def __Initialize(self):
		self.loadedWindow = False

		self.mainBoard = None

		self.priceText = None

		self.quantitySlot = None
		self.quantityValue = None
		self.informationText = None

		self.acceptButton = None
		self.cancelButton = None

		self.acceptEvent = (ui.__mem_func__(self.Hide),)
		self.closeEvent = (ui.__mem_func__(self.Hide),)

		self.shopPos = -1

	def __LoadWindow(self):
		if self.loadedWindow is True:
			return

		self.mainBoard = ui.DragonBoardWithTitleBar()
		self.mainBoard.SetParent(self)
		self.mainBoard.AddFlag("attach")
		self.mainBoard.SetSize(*self.WINDOW_SIZE)
		self.mainBoard.SetCloseEvent(ui.__mem_func__(self.RunCloseEvent))
		self.mainBoard.Show()

		self.priceText = ui.ExtendedTextLine()
		self.priceText.SetParent(self)
		self.priceText.SetPosition(0, 25)
		self.priceText.Show()

		#Quantity Slot Related
		self.quantitySlot = ui.MakeExpandedImageBox(self.mainBoard,\
							"d:/ymir work/ui/public/Parameter_Slot_02.sub", 20, 34 + 20)

		self.quantityValue = ui.EditLine()
		self.quantityValue.SetParent(self.quantitySlot)
		self.quantityValue.SetSize(*self.EDITLINE_SIZE)
		self.quantityValue.SetPosition(3, 2)
		self.quantityValue.SetMax(len(str(MAXIMUM_MULTIPLE_BUY_ITENS)))
		self.quantityValue.SetNumberMode()
		self.quantityValue.SetEscapeEvent(ui.__mem_func__(self.RunCloseEvent))
		self.quantityValue.SetReturnEvent(ui.__mem_func__(self.RunAcceptEvent))
		self.quantityValue.SetUpdateEvent(ui.__mem_func__(self.RunUpdateEvent))
		self.quantityValue.Show()

		self.informationText = ui.MakeTextLineNew(self.quantitySlot, 66, 3,\
							"/ {}".format(MAXIMUM_MULTIPLE_BUY_ITENS))

		#Buttons Related
		_buttonsImagePath = ["d:/ymir work/ui/public/",\
							"middle_button_01.sub", "middle_button_02.sub", "middle_button_03.sub"]

		self.acceptButton = ui.MakeButton(self.mainBoard, 19, 58 + 20, "", *_buttonsImagePath)
		self.acceptButton.SetEvent(ui.__mem_func__(self.RunAcceptEvent))
		self.acceptButton.SetText(uiScriptLocale.OK)

		self.cancelButton = ui.MakeButton(self.mainBoard, 90, 58 + 20, "", *_buttonsImagePath)
		self.cancelButton.SetEvent(ui.__mem_func__(self.RunCloseEvent))
		self.cancelButton.SetText(uiScriptLocale.CANCEL)

		self.loadedWindow = True

		#@Public methods
	def BuildPageInformation(self, shopPos):
		"""Adjust position of window if the position of\
			same its out for screen game"""
		def _adjust_rect_position(position):
			screenrect = (wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
			finalPos = tuple(x+y for x,y in zip(position, self.WINDOW_SIZE))
			newPos = [0,0]

			for positionIdx in xrange(len(self.WINDOW_SIZE)):
				if finalPos[positionIdx] > screenrect[positionIdx]: #Check the limit of window
					newPos[positionIdx] = (screenrect[positionIdx] - finalPos[positionIdx])
				else: #Check the init position of window
					newPos[positionIdx] = max(position[positionIdx], 0)

			return newPos

		item.SelectItem(shop.GetItemID(shopPos))
		self.mainBoard.SetTitleName(item.GetItemName())

		_wndPos = tuple(x-y for x,y in zip(self.GetMouseLocalPosition(), self.WINDOW_SIZE))
		self.SetPosition(*_adjust_rect_position(_wndPos))

		if self.quantityValue:
			self.quantityValue.SetText(str(1))
			self.quantityValue.SetFocus()
			ime.SetCursorPosition(len(self.quantityValue.GetText()) + 1)

		self.shopPos = shopPos

		if self.priceText:
			self.AppendPriceText(shopPos)

	def GetQuantityValue(self, returnAdjustValue = True):
		if not self.quantityValue or\
			(self.quantityValue and not self.quantityValue.GetText().isdigit()):
			return 0

		_value = int(self.quantityValue.GetText())
		return (min(_value, MAXIMUM_MULTIPLE_BUY_ITENS) if returnAdjustValue is True else _value)

	def SetAcceptEvent(self, event, *args):
		self.acceptEvent = (ui.__mem_func__(event), args)

	def SetCloseEvent(self, event, *args):
		self.closeEvent = (ui.__mem_func__(event), args)

	def RunAcceptEvent(self):
		if self.acceptEvent:
			apply(*self.acceptEvent)

	def RunCloseEvent(self):
		if self.closeEvent:
			apply(*self.closeEvent)

	def RunUpdateEvent(self):
		_value = self.GetQuantityValue(returnAdjustValue = False)
		if not (_value or self.quantityValue):
			return

		if _value > MAXIMUM_MULTIPLE_BUY_ITENS:
			self.quantityValue.SetText(str(MAXIMUM_MULTIPLE_BUY_ITENS))

		if _value <= MAXIMUM_MULTIPLE_BUY_ITENS:
			self.AppendPriceText(self.shopPos)

	def AppendPriceText(self, shopPos):
		iPrice = shop.GetItemPrice(shopPos)
		iPriceVnum = shop.GetItemPriceVnum(shopPos)

		iQuanity = self.GetQuantityValue(True)

		if iPriceVnum != 0:
			item.SelectItem(iPriceVnum)

		if self.priceText:
			_firstData = "Cena: "
			_secondData = "<TEXT color=" + str(grp.GenerateColor(0.85, 0.85, 0.85, 1.0)) + " text=\"%s\">"
			
			if iPriceVnum != 0:
				_thirdData = (_secondData % localeInfo.NumberToString(iQuanity * iPrice) + "x") + "<IMAGE path=\"" + item.GetIconImageFileName() + "\"> "
				self.priceText.SetPosition(0, 25)
			else:
				_thirdData = (_secondData % localeInfo.NumberToStringAsType(iQuanity * iPrice))
				self.priceText.SetPosition(0, 33)

			self.priceText.SetWindowHorizontalAlignCenter()

			self.priceText.SetText(_firstData + _thirdData)

	def OnPressEscapeKey(self):
		self.Hide()
		return True

	def Show(self):
		super(AncientShopMultipleBuyWindow, self).Show()
		self.SetTop()

	def Hide(self):
		super(AncientShopMultipleBuyWindow, self).Hide()
