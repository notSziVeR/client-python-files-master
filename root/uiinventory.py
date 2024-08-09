#-*- coding: iso-8859-1 -*-
from introinterface import GetWindowConfig, gcGetEnable
import ui
import player
import mouseModule
import net
import app
import snd
import item
import player
import chat
import grp
import uiscriptlocale
import uiRefine
import uiAttachMetin
import uiCommon
import uiPrivateShopBuilder
import localeInfo
import constInfo
import ime
import wndMgr

if app.ENABLE_GAYA_SYSTEM:
	import uiGayaSystem

if gcGetEnable("ENABLE_NEW_SPLIT_ITEM"):
	import uiItemSplitter

if gcGetEnable("ENABLE_FAST_INTERACTION_MULTI_USE"):
	import uiitemopener

if gcGetEnable("ENABLE_HAND_SWITCHER"):
	import uiHandSwitcher

if app.SASH_ABSORPTION_ENABLE:
	import uisashsystem

import cfg

import utility
import exchange

import introInterface

import grid
import itemWrapper

import uiToolTip

import chr
import colorInfo

if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	import uiPrivateShop
	import privateShop

if app.GLOBAL_RANKING_ENABLE:
	import uiGlobalRanking

ITEM_MALL_BUTTON_ENABLE = True

ITEM_FLAG_APPLICABLE = 1 << 14

ROOT_PATH = "d:/ymir work/ui/game/inventory/"

if app.ENABLE_SPECIAL_STORAGE:
	class SpecialStorageInventoryWindow(ui.ScriptWindow):
		def __init__(self, wndInventory):
			import exception

			if not wndInventory:
				exception.Abort("wndInventory parameter must be set to InventoryWindow")
				return

			ui.ScriptWindow.__init__(self)

			self.isLoaded = 0
			self.wndInventory = wndInventory;

			self.iStorageType = 0
			self.iCurrentPage = 0

			self.__LoadWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def Show(self):
			self.__LoadWindow()
			self.RefreshSlot()

			ui.ScriptWindow.Show(self)

		def Close(self):
			self.Hide()

		def __LoadWindow(self):
			if self.isLoaded == 1:
				return

			self.isLoaded = 1

			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "UIScript/SpecialStorage.py")
			except:
				import exception
				exception.Abort("SpecialStorageInventoryWindow.LoadWindow.LoadObject")

			try:
				wndItemSlot = self.GetChild("ItemSlot")
				self.GetChild("board").SetCloseEvent(ui.__mem_func__(self.Close))
				self.GetChild("board").HandleButtonState("BTN_SORT", True)
				self.GetChild("board").SetSortEvent(ui.__mem_func__(self.__SortInventory))

				self.lStorageType = []
				self.lStoragePage = []

				## Type
				for i in xrange(item.SPECIAL_STORAGE_COUNT):
					self.lStorageType.append(self.GetChild("Storage_Tab_0%d" % (i+1, )))

				## Page
				for i in xrange(item.SPECIAL_STORAGE_PAGE_COUNT):
					self.lStoragePage.append(self.GetChild("Inventory_Tab_0%d" % (i+1, )))
			except:
				import exception
				exception.Abort("SpecialStorageInventoryWindow.LoadWindow.BindObject")

			## GridSlot
			wndItemSlot.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
			wndItemSlot.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
			wndItemSlot.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
			wndItemSlot.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
			wndItemSlot.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
			wndItemSlot.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))

			## Type
			for iKey, rValue in enumerate(self.lStorageType):
				rValue.SAFE_SetEvent(self.__UpdateType, iKey)

			## Page
			for iKey, rValue in enumerate(self.lStoragePage):
				rValue.SAFE_SetEvent(self.__UpdatePage, iKey)

			self.wndItemSlot = wndItemSlot

			self.__UpdateType(0)
			self.__UpdatePage(0)

			self.SetCenterPosition()

			if app.ENABLE_MOUSE_WHEEL_EVENT:
				self.SetScrollWheelEvent(self.OnWheelMove)

		if app.ENABLE_MOUSE_WHEEL_EVENT:
			def OnWheelMove(self, len):
				pos = 0
				if len < 0:
					pos = (self.iCurrentPage + 1) % item.SPECIAL_STORAGE_PAGE_COUNT

					if pos == 0:
						return True

					self.__UpdatePage(pos)
				else:
					pos = (self.iCurrentPage - 1) % item.SPECIAL_STORAGE_PAGE_COUNT

					if pos < 0:
						pos = -pos

					if pos == item.SPECIAL_STORAGE_PAGE_COUNT - 1:
						return True

					self.__UpdatePage(pos)

				return True

		def	GetSlotBase(self):
			return self.iStorageType*item.SPECIAL_STORAGE_PAGE_SIZE*item.SPECIAL_STORAGE_PAGE_COUNT + self.iCurrentPage*item.SPECIAL_STORAGE_PAGE_SIZE

		def OpenFromInvMenu(self, arg):
			self.__UpdateType(arg)

		def	__UpdateType(self, iKey):
			self.iStorageType = iKey
			self.RefreshSlot()

			for _iKey, rBut in enumerate(self.lStorageType):
				if _iKey == iKey:
					rBut.Down()
				else:
					rBut.SetUp()

		def	__UpdatePage(self, iKey):
			self.iCurrentPage = iKey
			self.RefreshSlot()

			for _iKey, rBut in enumerate(self.lStoragePage):
				if _iKey == iKey:
					rBut.Down()
				else:
					rBut.SetUp()

		def __SortInventory(self):
			net.SendChatPacket("/sort_inventory_by_storage_type %d" % (self.iStorageType + item.SPECIAL_STORAGE_BEGIN_ID))

		def RefreshSlot(self):
			getItemVNum=player.GetItemIndex

			for i in xrange(item.SPECIAL_STORAGE_PAGE_SIZE):
				slotNumber = item.SPECIAL_STORAGE_START_CELL + self.GetSlotBase() + i
				if app.ENABLE_TRANSMUTATION_SYSTEM:
					self.wndItemSlot.SetItemSlot(item.SPECIAL_STORAGE_START_CELL + i, getItemVNum(slotNumber), player.GetItemCount(slotNumber) if player.GetItemCount(slotNumber) > 1 else 0, (1.0, 1.0, 1.0, 1.0), player.GetItemTransmutate(slotNumber))
				else:
					self.wndItemSlot.SetItemSlot(item.SPECIAL_STORAGE_START_CELL + i, getItemVNum(slotNumber), player.GetItemCount(slotNumber) if player.GetItemCount(slotNumber) > 1 else 0)

				if app.ENABLE_RENEWAL_SHOP_SELLING:
					if slotNumber in self.wndInventory.gcGetSellingList:
						self.wndItemSlot.SetUnusableSlot(item.SPECIAL_STORAGE_START_CELL + i)
					else:
						self.wndItemSlot.SetUsableSlot(item.SPECIAL_STORAGE_START_CELL + i)

				if gcGetEnable("ENABLE_LOCK_EFFECTS"):
					## Lock support
					for dict_element in self.wndInventory.LockDict.itervalues():
						(colour, slot_list) = dict_element
						## Pet Item exception
						if slotNumber in slot_list:
							self.wndItemSlot.LockSlot(item.SPECIAL_STORAGE_START_CELL + i, colour)

				if app.ENABLE_HIGHLIGHT_NEW_ITEM:
					if slotNumber in self.wndInventory.liHighlightedItems:
						self.wndItemSlot.NewActivateSlot(item.SPECIAL_STORAGE_START_CELL + i)
					else:
						self.wndItemSlot.NewDeactivateSlot(item.SPECIAL_STORAGE_START_CELL + i)

			self.wndItemSlot.RefreshSlot()

		def Reposition(self, x, y):
			self.SetPosition(x - self.GetWidth() - 27, y)

if gcGetEnable("ENABLE_RIGHT_PANEL_INVENTORY"):
	class SideBar(ui.Window):
		SIDEBAR_PATH_PATTERN = "assets/ui/buttons/INV/{}"

		Y_SPACE = 30
		WIDTH = 29

		def __init__(self):
			ui.Window.__init__(self)

			self.AddFlag("animate")
			self.__buttons = []
			self.SetSize(self.WIDTH, 0)

			self.wToolTip = uiToolTip.ToolTip()

		def __del__(self):
			ui.Window.__del__(self)

			del self.__buttons[:]

		def AddButton(self, sKey, sIcon, callback):
			btn = ui.Button()
			btn.SetParent(self)
			btn.SetPosition(0, (len(self.__buttons) * self.Y_SPACE))
			btn.SetUpVisual(self.SIDEBAR_PATH_PATTERN.format(sIcon + "NORMAL.png"))
			btn.SetOverVisual(self.SIDEBAR_PATH_PATTERN.format(sIcon + "HOVER.png"))
			btn.SetDownVisual(self.SIDEBAR_PATH_PATTERN.format(sIcon + "DOWN.png"))
			btn.SetEvent(ui.__mem_func__(self.EventProgress), "MOUSE_LEFT_BUTTON_DOWN", callback)
			btn.SetOverEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_IN", sKey)
			btn.SetOverOutEvent(ui.__mem_func__(self.EventProgress), "MOUSE_OVER_OUT", sKey)

			btn.Show()

			self.__buttons.append(btn)

			self.SetSize(self.GetWidth(), (len(self.__buttons) * self.Y_SPACE))

		def Reposition(self, x, y):
			self.SetPosition(x - self.WIDTH, y + 35)

		def EventProgress(self, event_type, *args):
			if "MOUSE_OVER_IN" == event_type:
				if self.wToolTip:
					(pos_x, pos_y) = wndMgr.GetMousePosition()

					self.wToolTip.ClearToolTip()
					self.wToolTip.SetTitle(args[0])
					self.wToolTip.SetToolTipPosition(pos_x, pos_y - 25)
					self.wToolTip.Show()

			elif "MOUSE_OVER_OUT" == event_type:
				if self.wToolTip:
					self.wToolTip.Hide()

			elif "MOUSE_LEFT_BUTTON_DOWN" == event_type:
				args[0]()

		def OnUpdate(self):
			if self.wToolTip:
				pos_x, pos_y = wndMgr.GetMousePosition()
				self.wToolTip.SetToolTipPosition(pos_x, pos_y - 25)

if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
	class ExpandedMoneyBar(ui.Board):

		SCALING_QUEUE = (
							## SIZE, DISTANCE_BETWEEN
							(80, 18, app.ENABLE_GAYA_SYSTEM, "GAYA"), ## GAYA
							(90, 20, False, "ACHIEV"), ## ACHIEV
							(90, 20, app.ENABLE_CHEQUE_SYSTEM, "WON"), ## WON
							(152, 20, True, "GOLD"), ## YANG
						)
		WIN_SIZE = (424, 70)
		INV_WIDTH = 0
		EDGE_PADDING = 12

		def	__init__(self):
			ui.Board.__init__(self)
			self.tooltipItem = uiToolTip.ItemToolTip()
			self.Objects = dict()

			self.__LoadWindow()

		def	__del__(self):
			ui.Board.__del__(self)

		def	Destroy(self):
			self.tooltipItem = None
			self.Objects = None

		def	__LoadWindow(self):
			## Size
			self.SetSize(*self.WIN_SIZE)

			if app.ENABLE_GAYA_SYSTEM:
				## Gaya Icon
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 0)] = ui.ImageBox()
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 0)].SetParent(self)
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 0)].LoadImage("d:/ymir work/ui/gemshop/gemshop_gemicon.sub")
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 0)].SetPosition(12, 17)
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 0)].Show()

				## Gaya SlotBar
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 1)] = ui.ImageBox()
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 1)].SetParent(self)
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 1)].LoadImage("d:/ymir work/ui/public/parameter_slot_01.sub")
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 1)].SetPosition(30, 13)
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 1)].Show()

				## Gaya TextLine
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 2)] = ui.MakeTextLine(self.Objects["ELEMENT_%s_%d" % ("GAYA", 1)], False, False)
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 2)].SetWindowVerticalAlignCenter()
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 2)].SetWindowHorizontalAlignRight()
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 2)].SetVerticalAlignCenter()
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 2)].SetHorizontalAlignRight()
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 2)].SetPosition(5, 0)
				self.Objects["ELEMENT_%s_%d" % ("GAYA", 2)].SetPackedFontColor(0xFF57c8ff)

			## Won Icon
			if app.ENABLE_CHEQUE_SYSTEM:
				self.Objects["ELEMENT_%s_%d" % ("WON", 0)] = ui.Button()
				self.Objects["ELEMENT_%s_%d" % ("WON", 0)].SetParent(self)
				self.Objects["ELEMENT_%s_%d" % ("WON", 0)].SetUpVisual("d:/ymir work/ui/cheque.tga")
				self.Objects["ELEMENT_%s_%d" % ("WON", 0)].SetOverVisual("d:/ymir work/ui/cheque2.tga")
				self.Objects["ELEMENT_%s_%d" % ("WON", 0)].SetDownVisual("d:/ymir work/ui/cheque.tga")
				self.Objects["ELEMENT_%s_%d" % ("WON", 0)].SAFE_SetEvent(self.__ExchangeCurrency, 0)
				self.Objects["ELEMENT_%s_%d" % ("WON", 0)].SetPosition(182, 14)
				self.Objects["ELEMENT_%s_%d" % ("WON", 0)].SetToolTipWindow(self.__CreateToolTip(localeInfo.CHANGE_TO_WON))
				self.Objects["ELEMENT_%s_%d" % ("WON", 0)].Show()

				## Won SlotBar
				self.Objects["ELEMENT_%s_%d" % ("WON", 1)] = ui.ImageBox()
				self.Objects["ELEMENT_%s_%d" % ("WON", 1)].SetParent(self)
				self.Objects["ELEMENT_%s_%d" % ("WON", 1)].LoadImage("d:/ymir work/ui/public/parameter_slot_01.sub")
				self.Objects["ELEMENT_%s_%d" % ("WON", 1)].SetPosition(202, 13)
				self.Objects["ELEMENT_%s_%d" % ("WON", 1)].Show()

				## Won TextLine
				self.Objects["ELEMENT_%s_%d" % ("WON", 2)] = ui.MakeTextLine(self.Objects["ELEMENT_%s_%d" % ("WON", 1)])

			## Money Icon
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 0)] = ui.ImageBox()
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 0)].SetParent(self)
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 0)].LoadImage("d:/ymir work/ui/game/windows/money_icon.sub")
			# self.Objects["ELEMENT_%s_%d" % ("GOLD", 0)].SetUpVisual("d:/ymir work/ui/game/windows/money_icon.sub")
			# self.Objects["ELEMENT_%s_%d" % ("GOLD", 0)].SetOverVisual("d:/ymir work/ui/yang2.tga")
			# self.Objects["ELEMENT_%s_%d" % ("GOLD", 0)].SetDownVisual("d:/ymir work/ui/game/windows/money_icon.sub")
			# self.Objects["ELEMENT_%s_%d" % ("GOLD", 0)].SAFE_SetEvent(self.__ExchangeCurrency, 1)
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 0)].SetPosition(272, 15)
			# self.Objects["ELEMENT_%s_%d" % ("GOLD", 0)].SetToolTipWindow(self.__CreateToolTip(localeInfo.CHANGE_TO_YANG))
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 0)].Show()

			## Money SlotBar
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 1)] = ui.ImageBox()
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 1)].SetParent(self)
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 1)].LoadImage("d:/ymir work/ui/public/parameter_slot_04.sub")
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 1)].SetPosition(292, 13)
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 1)].Show()

			## Money TextLine
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 2)] = ui.MakeTextLine(self.Objects["ELEMENT_%s_%d" % ("GOLD", 1)], False, False)
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 2)].SetWindowVerticalAlignCenter()
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 2)].SetWindowHorizontalAlignRight()
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 2)].SetVerticalAlignCenter()
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 2)].SetHorizontalAlignRight()
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 2)].SetPosition(5, 0)
			self.Objects["ELEMENT_%s_%d" % ("GOLD", 2)].SetPackedFontColor(0xFFffc600)

			self.__GenerateWindowSize()
			self.Hide()

		if app.ENABLE_CHEQUE_SYSTEM:
			def	__ExchangeCurrency(self, iArg):
				net.SendChatPacket("/exchange_won_yang %d" % iArg)

		def	SetFlexPosition(self, iWidth, iHeight):
			self.SetPosition(iWidth-self.INV_WIDTH-self.GetWidth(), iHeight-self.GetHeight())

		def __CreateToolTip(self, title):
			toolTip = uiToolTip.ToolTip()
			toolTip.SetTitle(title)
			toolTip.AlignHorizonalCenter()

			return toolTip

		def	__GenerateWindowSize(self):
			iWinWidth = self.EDGE_PADDING
			for i, (iSize, iDist, bStat, sKey) in enumerate(self.SCALING_QUEUE):
				if not bStat: ## Skip if should not be displayed
					continue

				self.Objects["ELEMENT_%s_%d" % (sKey, 0)].SetPosition(iWinWidth, self.Objects["ELEMENT_%s_%d" % (sKey, 0)].GetLocalPosition()[1])
				self.Objects["ELEMENT_%s_%d" % (sKey, 1)].SetPosition(iWinWidth+iDist, self.Objects["ELEMENT_%s_%d" % (sKey, 1)].GetLocalPosition()[1])
				iWinWidth += iSize

			self.SetSize(iWinWidth, self.WIN_SIZE[1])

class CostumeWindow(ui.ScriptWindow):
	if gcGetEnable("ENABLE_HIDE_COSTUMES"):
		## ADDERS LEFT , TOP
		ADDERS = (3, 36 + 3)
		COSTUME_CONFIGURATION = {
			"HEAD"	:	{	"SLOT" : item.COSTUME_SLOT_HAIR,	"POS"	:	(ADDERS[0] + 59, ADDERS[1] + 37),	"STATUS" : False,	"TOOLTIP"	:	(uiscriptlocale.COSTUME_HAIR_OFF, uiscriptlocale.COSTUME_HAIR_ON)	},
			"BODY"	:	{	"SLOT" : item.COSTUME_SLOT_BODY,	"POS"	:	(ADDERS[0] + 58, ADDERS[1] + 78),	"STATUS" : False,	"TOOLTIP"	:	(uiscriptlocale.COSTUME_BODY_OFF, uiscriptlocale.COSTUME_BODY_ON)	},
			"WEAPON"	:	{	"SLOT" : item.COSTUME_SLOT_WEAPON,	"POS"	:	(ADDERS[0] + 10, ADDERS[1] + 62),	"STATUS" : False,	"TOOLTIP"	:	(uiscriptlocale.COSTUME_WEAPON_OFF, uiscriptlocale.COSTUME_WEAPON_ON)	},
			"SASH"	:	{	"SLOT" : item.COSTUME_SLOT_SASH,	"POS"	:	(ADDERS[0] + 10, ADDERS[1] + 22),	"STATUS" : False,	"TOOLTIP"	:	(uiscriptlocale.COSTUME_SASH_OFF, uiscriptlocale.COSTUME_SASH_ON)	},
		}

		COSTUME_BUTTONS = [
			"d:/ymir work/ui/game/inventory/costumes/button_show_0{}.png",
			"d:/ymir work/ui/game/inventory/costumes/button_hide_0{}.png",
		]

	def __init__(self, wndInventory):
		import exception

		if not wndInventory:
			exception.Abort("wndInventory parameter must be set to InventoryWindow")
			return

		ui.ScriptWindow.__init__(self)

		self.isLoaded = False

		self.wndInventory = wndInventory

		self.Objects = {}
		self.Objects["ToolTip"] = uiToolTip.ToolTip()
		self.Objects["ToolTip"].ClearToolTip()

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)
		self.Objects = {}

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/CostumeWindow.py")
		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.LoadObject")

		try:
			wndEquip = self.GetChild("CostumeSlot")
			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))

		except:
			import exception
			exception.Abort("CostumeWindow.LoadWindow.BindObject")

		## Equipment
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.wndInventory.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.wndInventory.OverOutItem))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.wndInventory.UseItemSlot))
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.wndInventory.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.wndInventory.SelectItemSlot))
		wndEquip.SetOverInEvent(ui.__mem_func__(self.wndInventory.OverInSlot))
		wndEquip.SetOverOutEvent(ui.__mem_func__(self.wndInventory.OverOutSlot))

		self.wndEquip = wndEquip

		if gcGetEnable("ENABLE_HIDE_COSTUMES"):
			self.__BuildHButtons()

	def Show(self):
		self.RefreshCostumeSlot()

		ui.ScriptWindow.Show(self)

	def Close(self):
		self.Hide()

	def RefreshCostumeSlot(self):
		self.wndEquip.RefreshItems(lambda slot : player.GetItemIndex(slot))
			
		self.__RefreshHOverlays()

	def Reposition(self, x, y):
		self.SetPosition(x - self.GetWidth() - 27, y)

	if gcGetEnable("ENABLE_HIDE_COSTUMES"):
		#@Public Method
		def RefreshHButton(self, sType, bInit = True):
			rConfig = self.COSTUME_CONFIGURATION.get(sType, None)
			if not rConfig:
				return

			rElement = self.Objects.get("H_{}".format(sType), None)
			if not rElement:
				return

			## Lets check if we have it deactivated
			bHActive = rConfig.get("STATUS")

			## We wanna set right now the color of image!
			rElement.LoadImage(self.COSTUME_BUTTONS[bHActive].format(1))

			if bInit:
				for sETypes in ["MOUSE_OVER_IN", "MOUSE_OVER_OUT", "MOUSE_LEFT_BUTTON_DOWN"]:
					rElement.SetEvent(ui.__mem_func__(self.__HEventProgress), sETypes, sType)
		
		#@Private Methods
		def __BuildHButtons(self):
			for sKey, iValues in self.COSTUME_CONFIGURATION.items():
				rImage = ui.ImageBoxNew()
				rImage.SetParent(self)
				rImage.SetPosition(*iValues.get("POS"))
				rImage.LoadImage(self.COSTUME_BUTTONS[0].format(1))
				rImage.Show()

				self.Objects["H_{}".format(sKey)] = rImage

				self.RefreshHButton(sKey)

		def __HEventProgress(self, sEventType, sType):
			rConfig = self.COSTUME_CONFIGURATION.get(sType)
			rElement = self.Objects.get("H_{}".format(sType))
			bStatus = rConfig.get("STATUS")
			sImage = self.COSTUME_BUTTONS[bStatus]

			if "MOUSE_OVER_IN" == sEventType:
				rElement.LoadImage(sImage.format(2))
				if not self.Objects.get("ToolTip"):
					return

				(pos_x, pos_y) = wndMgr.GetMousePosition()

				sText = rConfig.get("TOOLTIP")[bStatus]
				self.Objects["ToolTip"].ClearToolTip()
				self.Objects["ToolTip"].SetThinBoardSize(len(sText))
				self.Objects["ToolTip"].AppendTextLine(sText)
				self.Objects["ToolTip"].SetToolTipPosition(pos_x, pos_y - 5)
				self.Objects["ToolTip"].Show()

			elif "MOUSE_OVER_OUT" == sEventType:
				rElement.LoadImage(sImage.format(1))

				if not self.Objects.get("ToolTip"):
					return

				self.Objects["ToolTip"].HideToolTip()

			elif "MOUSE_LEFT_BUTTON_DOWN" == sEventType:
				rElement.LoadImage(sImage.format(3))
				self.__SendHCommand(sType)

		def __RefreshHOverlays(self):
			for sKey, rValues in self.COSTUME_CONFIGURATION.items():
				if rValues["STATUS"]:
					self.wndEquip.LockSlot(rValues["SLOT"])
				else:
					self.wndEquip.UnlockSlot(rValues["SLOT"])

		def __SendHCommand(self, sType):
			net.SendChatPacket("/user_costume_option {}".format(sType))

class InventoryWindow(ui.ScriptWindow):
	USE_TYPE_TUPLE = ("USE_CLEAN_SOCKET",
		"USE_CHANGE_ATTRIBUTE",
		"USE_ADD_ATTRIBUTE",
		"USE_ADD_ATTRIBUTE2",
		"USE_ADD_ACCESSORY_SOCKET",
		"USE_PUT_INTO_ACCESSORY_SOCKET",
		"USE_PUT_INTO_BELT_SOCKET",
		"USE_PUT_INTO_RING_SOCKET"
	)

	if app.ENABLE_USE_COSTUME_ATTR:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_CHANGE_COSTUME_ATTR", "USE_RESET_COSTUME_ATTR"])

	if app.ENABLE_REFINE_ELEMENT:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_ELEMENT_UPGRADE", "USE_ELEMENT_DOWNGRADE", "USE_ELEMENT_CHANGE"])

	if app.ENABLE_NEW_COSTUME_BONUS:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_ADD_COSTUME_ATTR_SPECIAL", "USE_REMOVE_COSTUME_ATTR"])

	if app.ENABLE_BELT_ATTR:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_ADD_BELT_ATTR", "USE_CHANGE_BELT_ATTR"])

	if app.ENABLE_ORE_REFACTOR:
		USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_REMOVE_ACCESSORY_SOCKET"])

	USE_TYPE_TUPLE = tuple(list(USE_TYPE_TUPLE) + ["USE_SPECIAL"])

	questionDialog = None
	tooltipItem = None

	wndRightPanel = None

	wndCostume = None
	isOpenedCostumeWindowWhenClosingInventory = 0

	if gcGetEnable("ENABLE_NEW_SPLIT_ITEM"):
		ItemSplitter = None

	if gcGetEnable("ENABLE_FAST_INTERACTION_MULTI_USE"):
		ItemOpener = None

	if gcGetEnable("ENABLE_HAND_SWITCHER"):
		HandSwitcher = None

	sellingSlotNumber = -1
	isLoaded = 0

	if app.ENABLE_HIGHLIGHT_NEW_ITEM:
		liHighlightedItems = []

	if gcGetEnable("ENABLE_ITEM_HIGHLIGHT_"):
		EFFECT_SLOTS = dict()

	if app.ENABLE_SPECIAL_STORAGE:
		wndSpecialStorage = None

	if gcGetEnable("ENABLE_LOCK_EFFECTS"):
		LockDict = dict()

	if app.ENABLE_TRANSMUTATION_SYSTEM:
		TransmutationSlots = {}
		New_Trans_Item = -1

	if gcGetEnable("ENABLE_RIGHT_PANEL_INVENTORY"):
		__sideBar = None
		
	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		wndPrivateShop			= None
		wndPrivateShopSearch	= None

	if app.GLOBAL_RANKING_ENABLE:
		wndGlobalRankingWindow = None

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.inventoryPageIndex = 0

		if app.ENABLE_RENEWAL_SHOP_SELLING:
			self.gcGetSellingList = []

		self.toolTip = None

		self.interface = None
		self.sortQuestionDialog = uiCommon.QuestionDialogSort()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Show(self):
		self.__LoadWindow()

		ui.ScriptWindow.Show(self)

		if gcGetEnable("ENABLE_RIGHT_PANEL_INVENTORY"):
			if self.__sideBar:
				self.__sideBar.Show()

		if self.isOpenedCostumeWindowWhenClosingInventory and self.wndCostume:
			x, y = self.GetGlobalPosition()
			self.wndCostume.Reposition(x, y)
			self.wndCostume.Show()

	def BindInterfaceClass(self, interface):
		self.interface = interface

	def __LoadWindow(self):
		if self.isLoaded == 1:
			return

		self.isLoaded = 1

		try:
			pyScrLoader = ui.PythonScriptLoader()

			if app.ENABLE_EXTEND_INVEN_SYSTEM:
				pyScrLoader.LoadScriptFile(self, "UIScript/InventoryWindow.py")
		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.LoadObject")

		try:
			wndItem = self.GetChild("ItemSlot")
			wndEquip = self.GetChild("EquipmentSlot")

			self.GetChild("TitleBar").SetCloseEvent(ui.__mem_func__(self.Close))
			self.GetChild("TitleBar").HandleButtonState("BTN_SORT", True)
			self.GetChild("TitleBar").SetSortEvent(ui.__mem_func__(self.sort_inventory))

			self.mallButton = self.GetChild2("MallButton")
			self.DSSButton = self.GetChild2("DSSButton")
			self.costumeButton = self.GetChild2("CostumeButton")

			self.inventoryTab = []
			for i in xrange(player.INVENTORY_PAGE_COUNT):
				self.inventoryTab.append(self.GetChild("Inventory_Tab_%02d" % (i+1)))

			if app.ENABLE_MOUSE_WHEEL_EVENT:
				self.SetScrollWheelEvent(self.OnWheelMove)

		except:
			import exception
			exception.Abort("InventoryWindow.LoadWindow.BindObject")

		## Item
		wndItem.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndItem.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndItem.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndItem.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndItem.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))

		## Equipment
		wndEquip.SetSelectEmptySlotEvent(ui.__mem_func__(self.SelectEmptySlot))
		wndEquip.SetSelectItemSlotEvent(ui.__mem_func__(self.SelectItemSlot))
		wndEquip.SetUnselectItemSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetUseSlotEvent(ui.__mem_func__(self.UseItemSlot))
		wndEquip.SetOverInItemEvent(ui.__mem_func__(self.OverInItem))
		wndEquip.SetOverOutItemEvent(ui.__mem_func__(self.OverOutItem))
		wndEquip.SetOverInEvent(ui.__mem_func__(self.OverInSlot))
		wndEquip.SetOverOutEvent(ui.__mem_func__(self.OverOutSlot))

		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.ClearToolTip()

		## Item Splitter
		if gcGetEnable("ENABLE_NEW_SPLIT_ITEM"):
			self.ItemSplitter = uiItemSplitter.ItemSplitter()

		## Item Opener
		if gcGetEnable("ENABLE_FAST_INTERACTION_MULTI_USE"):
			self.ItemOpener = uiitemopener.ItemOpener()

		## Hand Switcher
		if gcGetEnable("ENABLE_HAND_SWITCHER"):
			self.HandSwitcher = uiHandSwitcher.HandSwitcherClass()

		## RefineDialog
		self.refineDialog = uiRefine.RefineDialog()
		self.refineDialog.Hide()

		## AttachMetinDialog
		self.attachMetinDialog = uiAttachMetin.AttachMetinDialog()
		self.attachMetinDialog.Hide()

		for i in xrange(player.INVENTORY_PAGE_COUNT):
			self.inventoryTab[i].SetEvent(lambda arg=i: self.SetInventoryPage(arg))

		self.inventoryTab[0].Down()

		self.wndItem = wndItem
		self.wndEquip = wndEquip

		# MallButton
		if self.mallButton:
			self.mallButton.SetEvent(ui.__mem_func__(self.ClickMallButton))

		if self.DSSButton:
			self.DSSButton.SetEvent(ui.__mem_func__(self.ClickDSSButton))
			if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
				self.DSSButton.SetMouseRightButtonDownEvent(ui.__mem_func__(self.actionClickDSButton))
				self.DSSButtonToolTip = uiToolTip.ToolTip(100)
				self.DSSButtonToolTip.HideToolTip()
				self.DSSButton.SetOverEvent(ui.__mem_func__(self.ShowDSToolTip))
				self.DSSButton.SetOverOutEvent(ui.__mem_func__(self.HideDSToolTip))

		if app.ENABLE_SPECIAL_STORAGE:
			self.wndSpecialStorage = SpecialStorageInventoryWindow(self)

		if app.GLOBAL_RANKING_ENABLE:
			self.wndGlobalRankingWindow = uiGlobalRanking.GlobalRanking()

		if gcGetEnable("ENABLE_RIGHT_PANEL_INVENTORY"):
			x, y = self.GetGlobalPosition()
			self.__sideBar = SideBar()
			self.__sideBar.Reposition(x, y)

			self.__sideBar.AddButton(localeInfo.BTN_INVENTORY_EXTRA_INVENTORY, "BTN_EXTRA_INVENTORY_", lambda : self.interface.ToggleSpecialStorageWindow())
			self.__sideBar.AddButton(localeInfo.BTN_INVENTORY_WIKIPEDIA, "BTN_WIKIPEDIA_", lambda : self.interface.ToggleWikiNew())
			self.__sideBar.AddButton(localeInfo.BTN_INVENTORY_SWITCHER, "BTN_SWITCHER_", lambda : self.interface.ToggleSwitchbotWindow())
			self.__sideBar.AddButton(localeInfo.BTN_INVENTORY_LOCALIZATIONS, "BTN_LOCALIZATIONS_", lambda : self.interface.PositionManager_ToggleWindow())
			self.__sideBar.AddButton(localeInfo.BTN_INVENTORY_MARBLES, "BTN_MARBLES_", lambda : self.ToggleMarbleManager())
			self.__sideBar.AddButton(localeInfo.BTN_INVENTORY_TELEPORT, "BTN_TELEPORT_", lambda : self.__ToggleTeleportSystem())
			self.__sideBar.AddButton(localeInfo.BTN_INVENTORY_RANKING, "BTN_RANKING_", lambda : self.__ToggleRanking())
			# self.__sideBar.AddButton(localeInfo.BTN_INVENTORY_AMULETS, "BTN_AMULETS_", lambda : self.__ToggleAmuletInformation())

		## Costumes
		if self.costumeButton:
			self.costumeButton.SetEvent(ui.__mem_func__(self.ClickCostumeButton))

		self.wndCostume = CostumeWindow(self)
		self.wndCostume.Hide()

		## Refresh
		self.RefreshEquipSlotWindow()
		self.SetInventoryPage(0)
		self.RefreshItemSlot()
		self.RefreshStatus()

		if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
			self.actionDSButton(False)

	if app.ENABLE_AMULET_SYSTEM:
		def __ToggleAmuletInformation(self):
			if self.interface.wndAmuletSystem["INFORMATION"].IsShow():
				self.interface.wndAmuletSystem["INFORMATION"].Close()
			else:
				self.interface.wndAmuletSystem["INFORMATION"].Open()

	if app.ENABLE_TELEPORT_SYSTEM:
		def __ToggleTeleportSystem(self):
			net.SendChatPacket("/teleport_open")

	def ToggleBiologManager(self):
		net.SendChatPacket("/request_biolog")

	def ToggleMarbleManager(self):
		import marblemgr
		marblemgr.MarblePacketOpen()

	def __ToggleRanking(self):
		self.wndGlobalRankingWindow.UpdateWindow()

	def OverInSlot(self, slotPos):
		CATEGORIES = {
			player.EQUIPMENT_SLOT_START+0 : localeInfo.INVENTORY_TOOLTIP_SLOT_ARMOR,
			player.EQUIPMENT_SLOT_START+1 : localeInfo.INVENTORY_TOOLTIP_SLOT_HELMET,
			player.EQUIPMENT_SLOT_START+2 : localeInfo.INVENTORY_TOOLTIP_SLOT_BOOTS,
			player.EQUIPMENT_SLOT_START+3 : localeInfo.INVENTORY_TOOLTIP_SLOT_BRACKLETS,
			player.EQUIPMENT_SLOT_START+4 : localeInfo.INVENTORY_TOOLTIP_SLOT_WEAPON,
			player.EQUIPMENT_SLOT_START+5 : localeInfo.INVENTORY_TOOLTIP_SLOT_NECKLACE,
			player.EQUIPMENT_SLOT_START+6 : localeInfo.INVENTORY_TOOLTIP_SLOT_EARS,
			player.EQUIPMENT_SLOT_START+7 : localeInfo.INVENTORY_TOOLTIP_SLOT_UNIQUE_1,
			player.EQUIPMENT_SLOT_START+8 : localeInfo.INVENTORY_TOOLTIP_SLOT_UNIQUE_2,
			player.EQUIPMENT_SLOT_START+9 : localeInfo.INVENTORY_TOOLTIP_SLOT_BOWS,
			player.EQUIPMENT_SLOT_START+10 : localeInfo.INVENTORY_TOOLTIP_SLOT_SHIELD,
			item.EQUIPMENT_BELT : localeInfo.INVENTORY_TOOLTIP_SLOT_BELT,
			item.EQUIPMENT_PENDANT : localeInfo.INVENTORY_TOOLTIP_SLOT_TALISMAN,
			item.COSTUME_SLOT_SASH : localeInfo.INVENTORY_TOOLTIP_SLOT_SASH,

			item.COSTUME_SLOT_HAIR : localeInfo.INVENTORY_TOOLTIP_SLOT_HAIR,
			item.COSTUME_SLOT_BODY : localeInfo.INVENTORY_TOOLTIP_SLOT_COSTUME,
			item.COSTUME_SLOT_WEAPON : localeInfo.INVENTORY_TOOLTIP_SLOT_WEAPON_OVERLAY,

			item.WEAR_UNIQUE3 : localeInfo.INVENTORY_TOOLTIP_SLOT_UNIQUE_3,
			item.WEAR_UNIQUE4 : localeInfo.INVENTORY_TOOLTIP_SLOT_UNIQUE_4,

			item.COSTUME_SLOT_MOUNT : localeInfo.INVENTORY_TOOLTIP_SLOT_MOUNT_OVERLAY,
			item.COSTUME_SLOT_PET : localeInfo.INVENTORY_TOOLTIP_SLOT_PET_OVERLAY,

			item.EQUIPMENT_AMULET : localeInfo.INVENTORY_TOOLTIP_SLOT_AMULET,
		}

		if self.toolTip:
			text = CATEGORIES.get(slotPos, "")
			arglen = len(str(text))
			self.toolTip.ClearToolTip()
			self.toolTip.SetThinBoardSize(10 * arglen)
			self.toolTip.AppendTextLine(CATEGORIES.get(slotPos, ""))
			self.toolTip.ShowToolTip()

	def OverOutSlot(self):
		if self.toolTip:
			self.toolTip.ClearToolTip()
			self.toolTip.HideToolTip()

	if gcGetEnable("ENABLE_DSS_ACTIVE_EFFECT_BUTTON"):
		def actionClickDSButton(self):
			if player.GetStatus(player.LEVEL) < 30:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DS_QUALIFIED_LEVEL_TOO_LOW)
				return

			self.interface.wndDragonSoul.ActivateButtonClick()

		def actionDSButton(self, bAction):
			if bAction == True:
				self.DSSButton.SetUpVisual(GetAssets().format("buttons/DS/dss_inventory_button_01.tga"))
				self.DSSButton.SetOverVisual(GetAssets().format("buttons/DS/dss_inventory_button_02.tga"))
				self.DSSButton.SetDownVisual(GetAssets().format("buttons/DS/dss_inventory_button_03.tga"))
			else:
				self.DSSButton.SetUpVisual(GetAssets().format("buttons/DS/dss_inventory_off_button_01.tga"))
				self.DSSButton.SetOverVisual(GetAssets().format("buttons/DS/dss_inventory_off_button_02.tga"))
				self.DSSButton.SetDownVisual(GetAssets().format("buttons/DS/dss_inventory_off_button_03.tga"))

			self.__CreateDragonSoulButtonToolTip(bAction)

		def __CreateDragonSoulButtonToolTip(self, bActive = True):
			if not self.DSSButtonToolTip:
				return

			CONFIGURATION = {
				True : [
					colorInfo.Colorize(localeInfo.INVENTORY_TOOLTIP_DRAGON_SOUL_NAME, 0xFF4dff35),
					colorInfo.Colorize(localeInfo.INVENTORY_TOOLTIP_DRAGON_SOUL_ACTIVE, 0xFF4dff35),
					localeInfo.INVENTORY_TOOLTIP_DRAGON_SOUL_ACTIVE_QUICK
				],

				False : [
					colorInfo.Colorize(localeInfo.INVENTORY_TOOLTIP_DRAGON_SOUL_NAME, 0xFFff3535),
					colorInfo.Colorize(localeInfo.INVENTORY_TOOLTIP_DRAGON_SOUL_INACTIVE, 0xFFff3535),
					localeInfo.INVENTORY_TOOLTIP_DRAGON_SOUL_INACTIVE_QUICK,
				],
			}

			self.DSSButtonToolTip.ClearToolTip()
			self.DSSButtonToolTip.AppendTextLine(CONFIGURATION[bActive][0])
			self.DSSButtonToolTip.AppendTextLine(localeInfo.INVENTORY_TOOLTIP_DRAGON_SOUL_INFORMATION)
			self.DSSButtonToolTip.AppendTextLine(CONFIGURATION[bActive][1])
			self.DSSButtonToolTip.AppendHorizontalLine()

			self.DSSButtonToolTip.AppendShortcut([app.DIK_O], localeInfo.INVENTORY_TOOLTIP_DRAGON_SOUL_OPEN, bCenter = True)

			self.DSSButtonToolTip.AppendShortcut([app.DIK_RMBUTTON], CONFIGURATION[bActive][2], bCenter = True)

			self.DSSButtonToolTip.AppendShortcut([app.DIK_LSHIFT, app.DIK_O], CONFIGURATION[bActive][2], bCenter = True)

			self.DSSButtonToolTip.AppendSpace(3)

		def ShowDSToolTip(self):
			if self.DSSButtonToolTip:
				self.DSSButtonToolTip.ShowToolTip()

		def HideDSToolTip(self):
			if self.DSSButtonToolTip:
				self.DSSButtonToolTip.HideToolTip()

	def sort_inventory(self):
		if self.sortQuestionDialog.IsShow():
			self.sortQuestionDialog.Hide()
			return

		self.sortQuestionDialog = uiCommon.QuestionDialogSort()
		self.sortQuestionDialog.SetText1(localeInfo.CONCATENATE_SORT_DESC)
		self.sortQuestionDialog.SetText2(localeInfo.CONCATENATE_STACK_DESC)
		self.sortQuestionDialog.SetAcceptEvent(lambda arg="SORT": self.__Sort(arg))
		self.sortQuestionDialog.SetCancelEvent(lambda arg="STACK": self.__Sort(arg))
		self.sortQuestionDialog.SetDisableReturnKey(False)
		self.sortQuestionDialog.Open()

	def __Sort(self, bType):
		if bType == "SORT":
			net.SendChatPacket("/sort_inventory_by_storage_type 1")
		elif bType == "STACK":
			self.ConcatenateItems()

		self.sortQuestionDialog.Close()

	def	ConcatenateItems(self):
		## Dedicated class to make sure item matches all preferences
		class CItemFullData:
			def	__init__(self, slotIndex):
				self.slotIndex = slotIndex
				self.itemVnum = player.GetItemIndex(slotIndex)

				## Caching slots
				self.metinSlots = [player.GetItemMetinSocket(slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]

				## Caching attrs
				self.attrSlots = [player.GetItemAttribute(slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

			def	__del__(self):
				self.slotIndex = None
				self.itemVnum = None
				self.metinSlots = None
				self.attrSlots = None

			def	__hash__(self):
				return int(str(self.itemVnum) + "".join([str(x) for x in self.metinSlots]) + "".join([str(x[0]) + str(x[1]) for x in self.attrSlots]))

			def	__eq__(self, obj):
				return type(self) is type(obj) and hash(self) == hash(obj)

			def	__ne__(self, obj):
				return not type(self) is type(obj) or hash(self) != hash(obj)
				
		## Prepearing dict with joinable items
		ItemDict = dict()
		global SITE_MAX_NUM
		MAX_COUNT = 2000
		
		ITEM_FLAG_STACKABLE = 1 << 2

		## Gathering informations
		iSize = player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT
		if app.ENABLE_SPECIAL_STORAGE:
			iSize += item.SPECIAL_STORAGE_PAGE_SIZE*item.SPECIAL_STORAGE_PAGE_COUNT*item.SPECIAL_STORAGE_COUNT

		for i in xrange(iSize):
			itemVnum = player.GetItemIndex(i)
			if itemVnum == 0:
				continue

			if (player.GetItemFlags(i) & ITEM_FLAG_STACKABLE) == ITEM_FLAG_STACKABLE and player.GetItemCount(i) < MAX_COUNT:
				itemData = CItemFullData(i)
				#print hash(itemData), itemData in ItemDict
				if itemData in ItemDict:
					ItemDict[itemData].append(i)
				else:
					ItemDict[itemData] = [i]

		## Checking if there is joinable item
		if len(ItemDict) == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CONCATENATE_NO_ITEMS)
			return

		## Begin process
		for itemVnum, slotNumbers in ItemDict.items():
			if len(slotNumbers) <= 1:
				continue

			while len(slotNumbers) > 1:
				itemCount = player.GetItemCount(slotNumbers[0])
				while itemCount < MAX_COUNT and len(slotNumbers) > 1:
					self.__SendMoveItemPacket(slotNumbers[1], slotNumbers[0], min(player.GetItemCount(slotNumbers[1]), MAX_COUNT-itemCount))
					itemCount = player.GetItemCount(slotNumbers[0])

					if itemCount < MAX_COUNT:
						slotNumbers.pop(1)

				slotNumbers.pop(0)
	
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CONCATENATE_DONE)

	def Destroy(self):
		self.ClearDictionary()

		if gcGetEnable("ENABLE_NEW_SPLIT_ITEM"):
			self.ItemSplitter.Close()
			self.ItemSplitter = None

		if gcGetEnable("ENABLE_FAST_INTERACTION_MULTI_USE"):
			self.ItemOpener.Close()
			self.ItemOpener = None

		if gcGetEnable("ENABLE_HAND_SWITCHER"):
			self.HandSwitcher.Hide()
			self.HandSwitcher = None

		self.refineDialog.Destroy()
		self.refineDialog = 0

		self.attachMetinDialog.Destroy()
		self.attachMetinDialog = 0

		self.tooltipItem = None
		self.wndItem = 0
		self.questionDialog = None
		self.mallButton = None
		self.DSSButton = None
		self.interface = None

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndSpecialStorage:
				self.wndSpecialStorage.Destroy()
				self.wndSpecialStorage = 0
				
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.wndPrivateShop:
				self.wndPrivateShop = None
				
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch = None

		self.inventoryTab = []

		if app.ENABLE_SPECIAL_STORAGE:
			self.InventoryMenuButton = None

		if gcGetEnable("ENABLE_ITEM_HIGHLIGHT_"):
			self.EFFECT_SLOTS = dict()

		if gcGetEnable("ENABLE_LOCK_EFFECTS"):
			self.LockDict = None

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			self.TransmutationSlots = {}
			self.New_Trans_Item = -1

		if gcGetEnable("ENABLE_RIGHT_PANEL_INVENTORY"):
			if self.__sideBar:
				del self.__sideBar

		if app.GLOBAL_RANKING_ENABLE:
			if self.wndGlobalRankingWindow:
				self.wndGlobalRankingWindow.Hide()
				self.wndGlobalRankingWindow = None

		if self.wndCostume:
			self.wndCostume.Destroy()
			self.wndCostume = 0

	def Hide(self):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			self.OnCloseQuestionDialog()
			return

		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndSpecialStorage:
				self.wndSpecialStorage.Close()

		if gcGetEnable("ENABLE_NEW_SPLIT_ITEM"):
			if self.ItemSplitter:
				self.ItemSplitter.Close()

		if gcGetEnable("ENABLE_FAST_INTERACTION_MULTI_USE"):
			if self.ItemOpener:
				self.ItemOpener.Close()

		# if gcGetEnable("ENABLE_HAND_SWITCHER"):
		# 	if self.HandSwitcher:
		# 		self.HandSwitcher.Hide()

		if gcGetEnable("ENABLE_RIGHT_PANEL_INVENTORY"):
			if self.__sideBar:
				self.__sideBar.Hide()

		if self.wndCostume:
			self.isOpenedCostumeWindowWhenClosingInventory = self.wndCostume.IsShow()
			self.wndCostume.Close()

		if app.GLOBAL_RANKING_ENABLE:
			if self.wndGlobalRankingWindow:
				self.wndGlobalRankingWindow.Hide()

		wndMgr.Hide(self.hWnd)

	def Close(self):
		if app.ENABLE_LUCKY_BOX:
			if self.interface and self.interface.wndLuckyBoxWindow and self.interface.wndLuckyBoxWindow.IsShow():
				chat.AppendChat(chat.CHAT_TYPE_INFO, uiscriptlocale.CANNOT_MAKE_THIS)
				return

		self.Hide()

	if gcGetEnable("ENABLE_LOCK_EFFECTS"):
		## Lock Suppport
		def	RegisterLockColour(self, key, colour):
			if not key in self.LockDict:
				self.LockDict[key] = [colour, set()]

		def	AppendLockSlot(self, key, value):
			if key in self.LockDict:
				self.LockDict[key][1].add(value)

		def	EraseLockElement(self, key):
			if key in self.LockDict:
				del self.LockDict[key]
				self.RefreshWindows()

		def	RemoveLockSlot(self, key, slot):
			if key in self.LockDict:
				try:
					self.LockDict[key][1].remove(slot)
				except:
					return

		def HasLockedSlot(self, sKey, iSlot):
			if not self.LockDict.get(sKey):
				return False

			return (iSlot in self.LockDict[sKey][1])

		def RefreshWindows(self):
			self.wndSpecialStorage.RefreshSlot()
			self.RefreshBagSlotWindow()

		def FindToLockSlot(self, iKey, iVnum):
			itemList = []

			for i in xrange(player.INVENTORY_SLOT_COUNT):
				vnum = player.GetItemIndex(i)

				if vnum == 0:
					continue

				if vnum == iVnum:
					itemList.append(i)

			for item in itemList:
				self.AppendLockSlot(iKey, item)
		## End of support

	def SetInventoryPage(self, page):
		self.inventoryPageIndex = page
		for i in xrange(player.INVENTORY_PAGE_COUNT):
			if i!=page:
				self.inventoryTab[i].SetUp()

		self.RefreshBagSlotWindow()

	if app.ENABLE_MOUSE_WHEEL_EVENT:
		def OnWheelMove(self, len):
			pos = 0
			if len > 0:
				pos = (self.inventoryPageIndex + 1) % player.INVENTORY_PAGE_COUNT

				if pos == 0:
					return True

				self.SetInventoryPage(pos)
			else:
				pos = (self.inventoryPageIndex - 1) % player.INVENTORY_PAGE_COUNT
				if pos < 0:
					pos = -pos

				if pos == player.INVENTORY_PAGE_COUNT - 1:
					return True

				self.SetInventoryPage(pos)
			self.inventoryTab[pos].Down()
			return True

	def ClickMallButton(self):
		self.interface.ToggleInventoryMenuWindow()

	# DSSButton
	def ClickDSSButton(self):
		print "click_dss_button"
		self.interface.ToggleDragonSoulWindow()

	if app.ENABLE_SPECIAL_STORAGE:
		def ClickSpecialStorageButton(self, arg):
			print "Click Special Storage Button"
			if self.wndSpecialStorage:
				if self.wndSpecialStorage.IsShow():
					self.wndSpecialStorage.Hide()
				else:
					self.wndSpecialStorage.Show()
					self.wndSpecialStorage.OpenFromInvMenu(arg)
			else:
				self.wndSpecialStorage.Show()
				self.wndSpecialStorage.OpenFromInvMenu(arg)

			x, y = self.GetGlobalPosition()
			self.wndSpecialStorage.Reposition(x, y)

	def ClickCostumeButton(self):
		x, y = self.GetGlobalPosition()
		if self.wndCostume:
			if self.wndCostume.IsShow():
				self.wndCostume.Hide()
			else:
				self.wndCostume.Reposition(x, y)
				self.wndCostume.Show()

	if gcGetEnable("ENABLE_NEW_SPLIT_ITEM"):
		def OnPickItem(self, isIndex, count):
			itemSlotIndex = self.ItemSplitter.itemGlobalSlotIndex
			selectedItemVNum = player.GetItemIndex(itemSlotIndex)
			mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, count)

		def OnSplitItem(self, split_packages, count, packages):
			itemSlotIndex = self.ItemSplitter.itemGlobalSlotIndex

			if split_packages:
				self.__OnSplitItem(count, packages)
			else:
				self.OnPickItem(itemSlotIndex, count)

		def __OnSplitItem(self, itemCount = 0, packCount = 0):
			itemSlotIndex	= self.ItemSplitter.itemGlobalSlotIndex
			count			= itemCount
			try:
				splitCount		= player.GetItemCount(itemSlotIndex) / count
			except ZeroDivisionError:
				self.ItemSplitter.Close()
				return False

			if packCount > 0:
				splitCount	= packCount

			self.ItemSplitter.Close()

			if count == 0 or splitCount == 0:
				return False

			itemVnum = player.GetItemIndex(itemSlotIndex)
			if itemVnum == 0:
				return False

			item.SelectItem(itemVnum)
			(_, height) = item.GetItemSize()

			splitItemDict = {
				"index"		: itemSlotIndex,
				"height"	: height,
				"count"		: count,
				"times"		: splitCount,
			}

			itemCount = player.GetItemCount(splitItemDict["index"]) - (splitItemDict["count"] * splitItemDict["times"])
			if itemCount <= 0:
				splitItemDict["times"] = player.GetItemCount(itemSlotIndex) / count

			splitItemDict["times"] = max(0, splitItemDict["times"])

			if splitItemDict["times"] == 0 or player.GetItemIndex(splitItemDict["index"]) == 0:
				return False

			slotList = utility.GetEmptyItemPosList(splitItemDict["height"], len(self.inventoryTab), player.GetItemIndex)

			realItemCount = player.GetItemCount(splitItemDict["index"])
			for i in slotList[:splitItemDict["times"]]:
				if player.GetItemIndex(i) != 0:
					continue

				if realItemCount <= splitItemDict["count"]:
					return True

				if splitItemDict["times"] <= 0:
					return True

				if not self.__SendMoveItemPacket(splitItemDict["index"], i, splitItemDict["count"]):
					return False

				splitItemDict["times"] -= 1
				realItemCount -= splitItemDict["count"]

	if gcGetEnable("ENABLE_FAST_INTERACTIONS"):
		def BuildGrid(self):
			g = grid.Grid(player.INVENTORY_PAGE_COLUMN, player.INVENTORY_PAGE_ROW, player.INVENTORY_PAGE_COUNT)

			for i in xrange(g.GetSize()):
				vnum = player.GetItemIndex(i)
				if vnum == 0:
					continue

				count = player.GetItemCount(i)
				if count == 0 and vnum != 71202:
					continue

				g.PutGlobal(itemWrapper.ItemGridWrapper(player.INVENTORY, i), i)

			return g

	def __InventoryLocalSlotPosToGlobalSlotPos(self, local):
		if player.IsEquipmentSlot(local) or player.IsCostumeSlot(local) or (app.ENABLE_NEW_EQUIPMENT_SYSTEM and player.IsBeltInventorySlot(local)):
			return local

		if app.ENABLE_SPECIAL_STORAGE:
			if player.IsSpecialStorageSlot(local):
				return local + self.wndSpecialStorage.GetSlotBase()

		return self.inventoryPageIndex*player.INVENTORY_PAGE_SIZE + local

	def GetInventoryPageIndex(self):
		return self.inventoryPageIndex

	def RefreshBagSlotWindow(self):
		getItemVNum=player.GetItemIndex
		getItemCount=player.GetItemCount
		setItemVNum=self.wndItem.SetItemSlot

		for i in xrange(player.INVENTORY_PAGE_SIZE):
			slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)

			itemCount = getItemCount(slotNumber)
			if 0 == itemCount:
				self.wndItem.ClearSlot(i)
				continue
			elif 1 == itemCount:
				itemCount = 0

			itemVnum = getItemVNum(slotNumber)
			if app.ENABLE_TRANSMUTATION_SYSTEM:
				setItemVNum(i, itemVnum, itemCount, (1.0, 1.0, 1.0, 1.0), player.GetItemTransmutate(slotNumber))
			else:
				setItemVNum(i, itemVnum, itemCount)

			if constInfo.ENABLE_CUBE_MARK_MATERIAL:
				if itemVnum and self.interface:
					if self.interface.IsCubeMaterial(slotNumber):
						self.wndItem.ActivateSlot(i)
					else:
						self.wndItem.DeactivateSlot(i)

			item.SelectItem(itemVnum)
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()

			if app.ENABLE_TOGGLE_SYSTEM:
				if item.ITEM_TYPE_TOGGLE == itemType:
					metinSocket = [player.GetItemMetinSocket(slotNumber, j) for j in xrange(player.METIN_SOCKET_MAX_NUM)]

					if self.inventoryPageIndex > 0:
						slotNumber = slotNumber % (player.INVENTORY_PAGE_SIZE * self.inventoryPageIndex)

					isActivated = 0 != metinSocket[3]

					if isActivated:
						self.wndItem.ActivateSlot(slotNumber)
					else:
						self.wndItem.DeactivateSlot(slotNumber)

			if app.ENABLE_TRANSMUTATION_SYSTEM:
				if slotNumber in self.TransmutationSlots:
					if self.TransmutationSlots[slotNumber]:
						self.wndItem.ActivateChangeLookSlot(i)
					else:
						self.wndItem.DeactivateChangeLookSlot(i)

				if int(self.New_Trans_Item) == slotNumber:
					self.wndItem.ActivateChangeLookSlot(i)

			elif app.ENABLE_HIGHLIGHT_NEW_ITEM:
				if not slotNumber in self.liHighlightedItems:
					self.wndItem.DeactivateSlot(i)

			if gcGetEnable("ENABLE_ITEM_HIGHLIGHT_"):
				if slotNumber in self.EFFECT_SLOTS:
					if self.EFFECT_SLOTS[slotNumber][0]:
						self.wndItem.ActivateSlot(i)
					else:
						self.wndItem.DeactivateSlot(i)

			if app.ENABLE_RENEWAL_SHOP_SELLING:
				if slotNumber in self.gcGetSellingList:
					self.wndItem.SetUnusableSlot(i)

			if gcGetEnable("ENABLE_LOCK_EFFECTS"):
				## Lock support
				for dict_element in self.LockDict.itervalues():
					(colour, slot_list) = dict_element

					if slotNumber in slot_list:
						self.wndItem.LockSlot(i, colour)
			
			if app.SASH_ABSORPTION_ENABLE:
				for iKey in uisashsystem.PROCESS_SLOTS.iterkeys():
					if uisashsystem.PROCESS_SLOTS[iKey].get("Slot", -1) == slotNumber:
						lColors = [
							(15.0 / 255.0, 133.0 / 255.0, 45.0 / 255.0, 1.0),
							(133.0 / 255.0, 46.0 / 255.0, 15.0 / 255.0, 1.0),
						]

						if uisashsystem.PROCESS_SLOTS[iKey].get("Sett"):
							self.wndItem.ActivateSlot(i, lColors[iKey])
						else:
							self.wndItem.DeactivateSlot(i)

		if app.ENABLE_GAYA_SYSTEM:
			uiGayaSystem.GAYA_CRAFTING_UPDATE_REQUEST = True

		self.wndItem.RefreshSlot()
		if app.ENABLE_HIGHLIGHT_NEW_ITEM:
			self.__RefreshHighlights()

		## Support for att/def
		if app.SASH_ABSORPTION_ENABLE:
			if player.GetItemIndex(item.COSTUME_SLOT_SASH) > 0 and player.GetItemMetinSocket(item.COSTUME_SLOT_SASH, player.SASH_ABSORPTION_SOCKET) > 0:
				uisashsystem.SASH_ABSORPTION_ITEM = (player.GetItemMetinSocket(item.COSTUME_SLOT_SASH, player.SASH_ABSORPTION_SOCKET), player.GetItemMetinSocket(item.COSTUME_SLOT_SASH, player.SASH_TYPE_SOCKET))
				if hasattr(self, "interface") and self.interface:
					self.interface.wndCharacter.RefreshStatus()
			else:
				uisashsystem.SASH_ABSORPTION_ITEM = (0, 0)
				
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.wndPrivateShop and self.wndPrivateShop.IsShow():
				self.wndPrivateShop.RefreshLockedSlot()

	if app.ENABLE_HIGHLIGHT_NEW_ITEM:
		def HighlightSlot(self, slot):
			if not slot in self.liHighlightedItems:
				self.liHighlightedItems.append(slot)

		def __RefreshHighlights(self):
			for i in xrange(player.INVENTORY_PAGE_SIZE):
				slotNumber = self.__InventoryLocalSlotPosToGlobalSlotPos(i)
				if slotNumber in self.liHighlightedItems:
					self.wndItem.NewActivateSlot(i)

	def RefreshEquipSlotWindow(self):
		def GetItemCount(slot):
			count = player.GetItemCount(slot)
			if count <= 1:
				return 0

			return count

		self.wndEquip.RefreshItems(lambda slot: player.GetItemIndex(slot), GetItemCount)

		if self.wndCostume:
			self.wndCostume.RefreshCostumeSlot()

		if gcGetEnable("ENABLE_EQUIPMENT_LOCK_SLOT"):
			self.RefreshEquipmentLock()

	def RefreshItemSlot(self):
		self.RefreshBagSlotWindow()
		self.RefreshEquipSlotWindow()

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndSpecialStorage:
				self.wndSpecialStorage.RefreshSlot()

		if gcGetEnable("ENABLE_FAST_INTERACTION_MULTI_USE"):
			if self.ItemOpener.IsShow():
				self.ItemOpener.RefreshSlot()

		if gcGetEnable("ENABLE_LEGENDARY_STONES"):
			if self.interface and self.interface.wndLegendaryStones["STONES"] and \
				self.interface.wndLegendaryStones["STONES"].IsShow():
				self.interface.wndLegendaryStones["STONES"].AppendAdditionalItems()

		if gcGetEnable("ENABLE_HAND_SWITCHER"):
			if self.HandSwitcher.IsShow():
				self.HandSwitcher.BroadcastUpdate()

		if app.ENABLE_AMULET_SYSTEM:
			if self.interface and self.interface.wndAmuletSystem["INFORMATION"] and \
				self.interface.wndAmuletSystem["INFORMATION"].IsShow():
				self.interface.wndAmuletSystem["INFORMATION"].Refresh()

	def RefreshStatus(self):
		money = player.GetElk()

		if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
			if self.interface:
				self.interface.wndExpandedMoneyBar.Objects["ELEMENT_%s_%d" % ("GOLD", 2)].SetText(localeInfo.DottedNumber(money))

				if app.ENABLE_GAYA_SYSTEM:
					self.interface.wndExpandedMoneyBar.Objects["ELEMENT_%s_%d" % ("GAYA", 2)].SetText(localeInfo.DottedNumber(player.GetGayaCount()))

				if app.ENABLE_CHEQUE_SYSTEM:
					self.interface.wndExpandedMoneyBar.Objects["ELEMENT_%s_%d" % ("WON", 2)].SetText(localeInfo.DottedNumber(player.GetCheque()))

	def SetItemToolTip(self, tooltipItem):
		self.tooltipItem = tooltipItem

	def SellItem(self):
		if self.sellingSlotitemIndex == player.GetItemIndex(self.sellingSlotNumber):
			if self.sellingSlotitemCount == player.GetItemCount(self.sellingSlotNumber):
				net.SendShopSellPacketNew(self.sellingSlotNumber, self.questionDialog.count, player.INVENTORY)
				snd.PlaySound("sound/ui/money.wav")
		self.OnCloseQuestionDialog()

	def OnDetachMetinFromItem(self):
		if None == self.questionDialog:
			return

		self.__SendUseItemToItemPacket(self.questionDialog.sourcePos, self.questionDialog.targetPos)
		self.OnCloseQuestionDialog()

	def OnCloseQuestionDialog(self):
		if not self.questionDialog:
			return

		self.questionDialog.Close()
		self.questionDialog = None
		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	## Slot Event
	def SelectEmptySlot(self, selectedSlotPos):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		selectedSlotPos = self.__InventoryLocalSlotPosToGlobalSlotPos(selectedSlotPos)

		if mouseModule.mouseController.isAttached():

			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				#@fixme011 BEGIN (block ds equip)
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				#@fixme011 END

				itemCount = player.GetItemCount(attachedSlotPos)
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()

				if app.IsPressed(app.DIK_LSHIFT):
					self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, 1)
					mouseModule.mouseController.DeattachObject()
					mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, attachedSlotPos, attachedItemIndex, itemCount - 1)
					return
				else:
					self.__SendMoveItemPacket(attachedSlotPos, selectedSlotPos, attachedCount)

				if item.IsRefineScroll(attachedItemIndex):
					self.wndItem.SetUseMode(False)

			elif app.ENABLE_SWITCHBOT and player.SLOT_TYPE_SWITCHBOT == attachedSlotType:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.SWITCHBOT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

			elif player.SLOT_TYPE_PRIVATE_SHOP == attachedSlotType:
				if app.ENABLE_PREMIUM_PRIVATE_SHOP:
					if not uiPrivateShopBuilder.IsBuildingPrivateShop():
						self.wndPrivateShop.SendItemCheckoutPacket(attachedSlotPos, selectedSlotPos)
						mouseModule.mouseController.DeattachObject()
						return
						
				mouseModule.mouseController.RunCallBack("INVENTORY")

			elif player.SLOT_TYPE_BUFF_EQUIPMENT == attachedSlotType and app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
				attachedCount = mouseModule.mouseController.GetAttachedItemCount()
				net.SendItemMovePacket(player.BUFF_EQUIPMENT, attachedSlotPos, player.INVENTORY, selectedSlotPos, attachedCount)

			elif player.SLOT_TYPE_SHOP == attachedSlotType:
				net.SendShopBuyPacket(attachedSlotPos)

			elif player.SLOT_TYPE_SAFEBOX == attachedSlotType:

				if player.ITEM_MONEY == attachedItemIndex:
					net.SendSafeboxWithdrawMoneyPacket(mouseModule.mouseController.GetAttachedItemCount())
					snd.PlaySound("sound/ui/money.wav")

				else:
					net.SendSafeboxCheckoutPacket(attachedSlotPos, selectedSlotPos)

			elif player.SLOT_TYPE_MALL == attachedSlotType:
				net.SendMallCheckoutPacket(attachedSlotPos, selectedSlotPos)

			mouseModule.mouseController.DeattachObject()

	def SelectItemSlot(self, itemSlotIndex):
		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS() == 1:
			return

		lItemSlotIndex = itemSlotIndex
		itemSlotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(itemSlotIndex)

		## Hand Switcher
		if gcGetEnable("ENABLE_HAND_SWITCHER"):
			if self.HandSwitcher and not self.HandSwitcher.CanMoveItem(itemSlotIndex):
				return

		if app.ENABLE_RENEWAL_SHOP_SELLING:
			if itemSlotIndex in self.gcGetSellingList:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_ITEM_ON_SELL_LIST)
				return

		if mouseModule.mouseController.isAttached():
			attachedSlotType = mouseModule.mouseController.GetAttachedType()
			attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemVID = mouseModule.mouseController.GetAttachedItemIndex()

			if player.SLOT_TYPE_INVENTORY == attachedSlotType:
				#@fixme011 BEGIN (block ds equip)
				attachedInvenType = player.SlotTypeToInvenType(attachedSlotType)
				if player.IsDSEquipmentSlot(attachedInvenType, attachedSlotPos):
					mouseModule.mouseController.DeattachObject()
					return
				#@fixme011 END

				self.__DropSrcItemToDestItemInInventory(attachedItemVID, mouseModule.SlotTypeToWindowType(attachedSlotType), attachedSlotPos, player.INVENTORY, itemSlotIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			curCursorNum = app.GetCursor()
			if app.SELL == curCursorNum:
				self.__SellItem(itemSlotIndex)

			elif app.BUY == curCursorNum:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SHOP_BUY_INFO)

			elif app.IsPressed(app.DIK_LALT):
				link = player.GetItemLink(itemSlotIndex)
				ime.PasteString(link)

			elif app.IsPressed(introInterface.GetWindowConfig("shortcust_items", introInterface.ITEM_SPLIITER, "key")):
				itemCount = player.GetItemCount(itemSlotIndex)

				if itemCount > 1:
					if gcGetEnable("ENABLE_NEW_SPLIT_ITEM"):
						# self.dlgPickItem.SetTitleName(localeInfo.PICK_ITEM_TITLE)
						self.ItemSplitter.SetAcceptEvent(ui.__mem_func__(self.OnSplitItem))
						self.ItemSplitter.AddItem(itemSlotIndex)
						self.ItemSplitter.Open()
						self.ItemSplitter.itemGlobalSlotIndex = itemSlotIndex

			elif app.IsPressed(app.DIK_LCONTROL):
				itemIndex = player.GetItemIndex(itemSlotIndex)
				
				if app.ENABLE_PREMIUM_PRIVATE_SHOP:
					if self.wndPrivateShop and self.wndPrivateShop.IsShow():
						self.wndPrivateShop.AttachItemToPrivateShop(itemSlotIndex, player.SLOT_TYPE_INVENTORY)
						return
						
					if self.wndPrivateShopSearch and self.wndPrivateShopSearch.IsShow():
						self.wndPrivateShopSearch.SelectItem(itemIndex)
						return

				if True == item.CanAddToQuickSlotItem(itemIndex):
					player.RequestAddToEmptyLocalQuickSlot(player.SLOT_TYPE_INVENTORY, itemSlotIndex)
				else:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.QUICKSLOT_REGISTER_DISABLE_ITEM)

				itemIndex = player.GetItemIndex(itemSlotIndex)

				self.interface.OpenPreviewWindow(itemIndex)

			# elif app.IsPressed(introInterface.GetWindowConfig("shortcust_items", introInterface.ITEM_PREVIEW, "key")) and app.ENABLE_RENDER_TARGET_EXTENSION and item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR, item.ITEM_TYPE_COSTUME, item.ITEM_TYPE_TOGGLE):
			# 	itemIndex = player.GetItemIndex(itemSlotIndex)

			# 	self.interface.OpenPreviewWindow(itemIndex)
			# 	return

			else:
				selectedItemVNum = player.GetItemIndex(itemSlotIndex)
				itemCount = player.GetItemCount(itemSlotIndex)
				mouseModule.mouseController.AttachObject(self, player.SLOT_TYPE_INVENTORY, itemSlotIndex, selectedItemVNum, itemCount)

				if self.__IsUsableItemToItem(selectedItemVNum, itemSlotIndex):
					self.wndItem.SetUseMode(True)
					if gcGetEnable("ENABLE_SWITCH_ITEMS"):
						self.wndItem.SetSwitchMode(False)
				else:
					self.wndItem.SetUseMode(False)
					if gcGetEnable("ENABLE_SWITCH_ITEMS"):
						self.wndItem.SetSwitchMode(True)

				snd.PlaySound("sound/ui/pick.wav")

	def __DropSrcItemToDestItemInInventory(self, srcItemVID, srcItemSlotType, srcItemSlotPos, dstItemSlotType, dstItemSlotPos):
		if srcItemSlotPos == dstItemSlotPos:
			return

		if app.SASH_ABSORPTION_ENABLE:
			if player.GetItemIndex(srcItemSlotPos) == player.SASH_ABSORPTION_RELEASE_ITEM:
				net.SendChatPacket("/release_sash_absorption %d %d" % (dstItemSlotPos, srcItemSlotPos))
				return

		# cyh itemseal 2013 11 08
		if app.ENABLE_SOULBIND_SYSTEM and item.IsSealScroll(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.IsRefineScroll(srcItemVID):
			self.RefineItem(srcItemSlotPos, dstItemSlotPos)
			self.wndItem.SetUseMode(False)

		elif item.IsMetin(srcItemVID):
			self.AttachMetinToItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsDetachScroll(srcItemVID):
			self.DetachMetinFromItem(srcItemSlotPos, dstItemSlotPos)

		elif item.IsKey(srcItemVID):
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif (player.GetItemFlags(srcItemSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		elif item.GetUseType(srcItemVID) in self.USE_TYPE_TUPLE:
			self.__SendUseItemToItemPacket(srcItemSlotPos, dstItemSlotPos)

		else:
			#snd.PlaySound("sound/ui/drop.wav")

			if player.IsEquipmentSlot(dstItemSlotPos):

				if item.IsEquipmentVID(srcItemVID):
					self.__UseItem(srcItemSlotPos)

			else:
				self.__SendMoveItemPacket(srcItemSlotPos, dstItemSlotPos, 0)
				#net.SendItemMovePacket(srcItemSlotPos, dstItemSlotPos, 0)

	if app.ENABLE_RENEWAL_SHOP_SELLING:
		def __SellItem(self, itemPosition):
			if not player.IsEquipmentSlot(itemPosition):
				itemIndex = player.GetItemIndex(itemPosition)
				itemCount = player.GetItemCount(itemPosition)

				item.SelectItem(itemIndex)
				if item.IsAntiFlag(item.ANTIFLAG_SELL):
					popup = uiCommon.PopupDialog()
					popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
					popup.SetAcceptEvent(self.__OnClosePopupDialog)
					popup.SetAutoClose()
					popup.Open()
					self.popup = popup
					return

				itemPrice = item.GetISellItemPrice()
				if item.Is1GoldItem():
					itemPrice = itemCount / itemPrice / 5
				else:
					itemPrice = itemPrice * itemCount / 5

				if self.interface:
					if itemPosition in self.gcGetSellingList:
						self.gcGetSellingList.remove(itemPosition)

						self.interface.RenewalShopAppendInformation(False, itemPrice, itemPosition)

						self.wndSpecialStorage.RefreshSlot()
						self.wndItem.SetUsableSlot(itemPosition)

						if len(self.gcGetSellingList) == 0:
							self.interface.RefreshSellingPrice()
					else:
						self.gcGetSellingList.append(itemPosition)

						self.interface.RenewalShopAppendInformation(True, itemPrice, itemPosition)

						self.wndSpecialStorage.RefreshSlot()
						self.__HighlightSellingItems(itemPosition)

				# constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		def __HighlightSellingItems(self, slot):
			if slot >= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex:
				slot -= player.INVENTORY_PAGE_SIZE*self.inventoryPageIndex

			self.wndItem.SetUnusableSlot(slot)

		def ClearHighlightSellingItems(self):
			for i in xrange(len(self.gcGetSellingList)):
				if self.wndItem:
					self.wndItem.SetUsableSlot(self.gcGetSellingList[i])

			self.gcGetSellingList = []

			if self.wndSpecialStorage:
				self.wndSpecialStorage.RefreshSlot()

		def AskSellingItems(self):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.ASKING_ABOUT_SELLING)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItemsRenewal))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		def GetSellingList(self):
			return self.gcGetSellingList

		def SellItemsRenewal(self):
			for i in xrange(len(self.gcGetSellingList)):
				itemSlot = self.gcGetSellingList[i]
				itemCount = player.GetItemCount(itemSlot)
				net.SendShopSellPacketNew(itemSlot, itemCount, player.INVENTORY)

			snd.PlaySound("sound/ui/money.wav")
			self.OnCloseQuestionDialog()
			self.ClearHighlightSellingItems()
			self.interface.RefreshSellingPrice()
			self.RefreshBagSlotWindow()
	else:
		def __SellItem(self, itemSlotPos):
			if not player.IsEquipmentSlot(itemSlotPos):
				self.sellingSlotNumber = itemSlotPos
				itemIndex = player.GetItemIndex(itemSlotPos)
				itemCount = player.GetItemCount(itemSlotPos)

				self.sellingSlotitemIndex = itemIndex
				self.sellingSlotitemCount = itemCount

				item.SelectItem(itemIndex)
				## 20140220
				if item.IsAntiFlag(item.ANTIFLAG_SELL):
					popup = uiCommon.PopupDialog()
					popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
					popup.SetAcceptEvent(self.__OnClosePopupDialog)
					popup.SetAutoClose()
					popup.Open()
					self.popup = popup
					return

				itemPrice = item.GetISellItemPrice()

				if item.Is1GoldItem():
					itemPrice = itemCount / itemPrice / 5
				else:
					itemPrice = itemPrice * itemCount / 5

				item.GetItemName(itemIndex)
				itemName = item.GetItemName()

				self.questionDialog = uiCommon.QuestionDialog()
				self.questionDialog.SetText(localeInfo.DO_YOU_SELL_ITEM(itemName, itemCount, itemPrice))
				self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.SellItem))
				self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
				self.questionDialog.Open()
				self.questionDialog.count = itemCount

				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def __OnClosePopupDialog(self):
		self.pop = None

	def RefineItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if player.REFINE_OK != player.CanRefine(scrollIndex, targetSlotPos):
			return

		###########################################################
		self.__SendUseItemToItemPacket(scrollSlotPos, targetSlotPos)
		#net.SendItemUseToItemPacket(scrollSlotPos, targetSlotPos)
		return
		###########################################################

		###########################################################
		#net.SendRequestRefineInfoPacket(targetSlotPos)
		#return
		###########################################################

		result = player.CanRefine(scrollIndex, targetSlotPos)

		if player.REFINE_ALREADY_MAX_SOCKET_COUNT == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_MORE_SOCKET)

		elif player.REFINE_NEED_MORE_GOOD_SCROLL == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NEED_BETTER_SCROLL)

		elif player.REFINE_CANT_MAKE_SOCKET_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_SOCKET_DISABLE_ITEM)

		elif player.REFINE_NOT_NEXT_GRADE_ITEM == result:
			#snd.PlaySound("sound/ui/jaeryun_fail.wav")
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_UPGRADE_DISABLE_ITEM)

		elif player.REFINE_CANT_REFINE_METIN_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.REFINE_OK != result:
			return

		self.refineDialog.Open(scrollSlotPos, targetSlotPos)

	def DetachMetinFromItem(self, scrollSlotPos, targetSlotPos):
		scrollIndex = player.GetItemIndex(scrollSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		if not player.CanDetach(scrollIndex, targetSlotPos):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_METIN_INSEPARABLE_ITEM)
			return

			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.OnDetachMetinFromItem))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.OnCloseQuestionDialog))
			self.questionDialog.Open()
			self.questionDialog.sourcePos = scrollSlotPos
			self.questionDialog.targetPos = targetSlotPos
		else:
			if app.ENABLE_DELETE_SINGLE_STONE:
				net.SendRequestDeleteSocket(net.SUBHEADER_REQUEST_DELETE_SOCKET_OPEN, targetSlotPos)

	def AttachMetinToItem(self, metinSlotPos, targetSlotPos):
		metinIndex = player.GetItemIndex(metinSlotPos)
		targetIndex = player.GetItemIndex(targetSlotPos)

		item.SelectItem(metinIndex)
		itemName = item.GetItemName()

		result = player.CanAttachMetin(metinIndex, targetSlotPos)

		if player.ATTACH_METIN_NOT_MATCHABLE_ITEM == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_CAN_NOT_ATTACH(itemName))

		if player.ATTACH_METIN_NO_MATCHABLE_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_SOCKET(itemName))

		elif player.ATTACH_METIN_NOT_EXIST_GOLD_SOCKET == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_NO_GOLD_SOCKET(itemName))

		elif player.ATTACH_METIN_CANT_ATTACH_TO_EQUIPMENT == result:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.REFINE_FAILURE_EQUIP_ITEM)

		if player.ATTACH_METIN_OK != result:
			return

		self.attachMetinDialog.Open(metinSlotPos, targetSlotPos)

	def OverOutItem(self):
		self.wndItem.SetUsableItem(False)
		if None != self.tooltipItem:
			self.tooltipItem.HideToolTip()

	if gcGetEnable("ENABLE_SWITCH_ITEMS"):
		def __CanSwitchItem(self, srcPos, srcItemVnum, dstPos):
			item.SelectItem(srcItemVnum)
			srcW, srcH = item.GetItemSize()
			# check if there is no item at the top that is out of bounds
			col = dstPos % player.INVENTORY_PAGE_COLUMN
			row = dstPos / player.INVENTORY_PAGE_COLUMN
			for i in xrange(row-1, -1, -1):
				curPos = i * player.INVENTORY_PAGE_COLUMN + col
				curPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(curPos)
				dstVnum = player.GetItemIndex(curPosGlobal)
				if dstVnum != 0:
					item.SelectItem(dstVnum)
					dstW, dstH = item.GetItemSize()
					if i + dstH - 1 >= row:
						return False
					else:
						break # if the first item is found and not in row-range then it's okay ;)
			# check if there is no item at the bottom that is too large
			dstPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(dstPos)
			for i in xrange(srcH):
				dstVnum = player.GetItemIndex(dstPosGlobal + i * player.INVENTORY_PAGE_COLUMN)
				if dstVnum != 0:
					item.SelectItem(dstVnum)
					dstW, dstH = item.GetItemSize()
					if i + dstH > srcH:
						return False

			# item switchable
			return True

	def OverInItem(self,overSlotPos ):
		if gcGetEnable("ENABLE_ITEM_HIGHLIGHT_"):
			if self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos) in self.EFFECT_SLOTS and self.EFFECT_SLOTS[self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)][0]:
				if not self.EFFECT_SLOTS[self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)][1]:
					self.wndItem.DeactivateSlot(overSlotPos)
					self.EFFECT_SLOTS[self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)][0] = False

		overSlotPosGlobal = self.__InventoryLocalSlotPosToGlobalSlotPos(overSlotPos)
		self.wndItem.SetUsableItem(False)

		if gcGetEnable("ENABLE_SWITCH_ITEMS"):
			self.wndItem.SetSwitchableItem(False)

		if app.ENABLE_HIGHLIGHT_NEW_ITEM and overSlotPosGlobal in self.liHighlightedItems:
			self.liHighlightedItems.remove(overSlotPosGlobal)
			self.wndItem.NewDeactivateSlot(overSlotPos)
			self.wndSpecialStorage.wndItemSlot.NewDeactivateSlot(overSlotPos)

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			if int(self.New_Trans_Item) == overSlotPosGlobal:
				self.New_Trans_Item = -1
				self.wndItem.DeactivateChangeLookSlot(overSlotPosGlobal)

		if mouseModule.mouseController.isAttached():
			attachedItemType = mouseModule.mouseController.GetAttachedType()
			if player.SLOT_TYPE_INVENTORY == attachedItemType:

				attachedSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
				attachedItemVNum = mouseModule.mouseController.GetAttachedItemIndex()

				if attachedItemVNum==player.ITEM_MONEY: # @fixme005
					pass

				if gcGetEnable("ENABLE_SWITCH_ITEMS"):
					if self.__IsUsableItemToItem(attachedItemVNum, attachedSlotPos):
						if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPosGlobal):
							self.wndItem.SetUsableItem(True)
							self.ShowToolTip(overSlotPosGlobal)
							return

					realDstPos = self.wndItem.GetPickedSlotNumber(False)
					if not self.__CanSwitchItem(attachedSlotPos, attachedItemVNum, realDstPos):
						self.wndItem.SetSwitchableItem(False)
					else:
						self.wndItem.SetSwitchableItem(True)
				else:
					if self.__CanUseSrcItemToDstItem(attachedItemVNum, attachedSlotPos, overSlotPosGlobal):
						self.wndItem.SetUsableItem(True)
						self.ShowToolTip(overSlotPosGlobal)
						return

		self.ShowToolTip(overSlotPosGlobal)

	def __IsUsableItemToItem(self, srcItemVNum, srcSlotPos):
		if app.SASH_ABSORPTION_ENABLE:
			if srcItemVNum == player.SASH_ABSORPTION_RELEASE_ITEM:
				return True

		if item.IsRefineScroll(srcItemVNum):
			return True
		elif item.IsMetin(srcItemVNum):
			return True
		elif item.IsDetachScroll(srcItemVNum):
			return True
		elif item.IsKey(srcItemVNum):
			return True
		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True
		else:
			if item.GetUseType(srcItemVNum) in self.USE_TYPE_TUPLE:
				return True

		return False

	def __CanUseSrcItemToDstItem(self, srcItemVNum, srcSlotPos, dstSlotPos):
		if srcSlotPos == dstSlotPos:
			return False

		if app.SASH_ABSORPTION_ENABLE:
			if srcItemVNum == player.SASH_ABSORPTION_RELEASE_ITEM:
				return self.__CanReleaseSash(dstSlotPos)

		if item.IsRefineScroll(srcItemVNum):
			if player.REFINE_OK == player.CanRefine(srcItemVNum, dstSlotPos):
				return True
		elif item.IsMetin(srcItemVNum):
			if player.ATTACH_METIN_OK == player.CanAttachMetin(srcItemVNum, dstSlotPos):
				return True
		elif item.IsDetachScroll(srcItemVNum):
			if player.DETACH_METIN_OK == player.CanDetach(srcItemVNum, dstSlotPos):
				return True
		elif item.IsKey(srcItemVNum):
			if player.CanUnlock(srcItemVNum, dstSlotPos):
				return True

		elif (player.GetItemFlags(srcSlotPos) & ITEM_FLAG_APPLICABLE) == ITEM_FLAG_APPLICABLE:
			return True

		else:
			useType=item.GetUseType(srcItemVNum)
			chat.AppendChat(1, useType)

			if "USE_CLEAN_SOCKET" == useType:
				if self.__CanCleanBrokenMetinStone(dstSlotPos):
					return True
			elif "USE_CHANGE_ATTRIBUTE" == useType:
				if self.__CanChangeItemAttrList(dstSlotPos):
					return True

			elif "USE_ADD_ATTRIBUTE" == useType:
				if self.__CanAddItemAttr(srcItemVNum, dstSlotPos):
					return True
			elif "USE_ADD_ATTRIBUTE2" == useType:
				if self.__CanAddItemAttr(srcItemVNum, dstSlotPos):
					return True
			elif "USE_ADD_ACCESSORY_SOCKET" == useType:
				if self.__CanAddAccessorySocket(dstSlotPos):
					return True
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == useType:
				if self.__CanPutAccessorySocket(dstSlotPos, srcItemVNum):
					return True;

			elif "USE_PUT_INTO_BELT_SOCKET" == useType:
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				print "USE_PUT_INTO_BELT_SOCKET", srcItemVNum, dstItemVNum

				item.SelectItem(dstItemVNum)

				if item.ITEM_TYPE_BELT == item.GetItemType():
					return True

			elif useType == "USE_ADD_BELT_ATTR" or useType == "USE_CHANGE_BELT_ATTR":
				dstItemVNum = player.GetItemIndex(dstSlotPos)
				item.SelectItem(dstItemVNum)
				if item.GetItemType() == item.ITEM_TYPE_BELT:
					return True

			elif app.ENABLE_USE_COSTUME_ATTR and "USE_CHANGE_COSTUME_ATTR" == useType:
				if self.__CanChangeCostumeAttrList(dstSlotPos):
					return True
			elif app.ENABLE_USE_COSTUME_ATTR and "USE_RESET_COSTUME_ATTR" == useType:
				if self.__CanResetCostumeAttr(dstSlotPos):
					return True

			elif useType == "USE_SPECIAL":
				if srcItemVNum == 90000:
					dstItemVNum = player.GetItemIndex(dstSlotPos)
					item.SelectItem(dstItemVNum)
					if item.GetItemType() != item.ITEM_TYPE_COSTUME or \
						item.GetItemSubType() != item.COSTUME_TYPE_SASH:
						return False

					if player.GetItemMetinSocket(dstSlotPos, 1) == 0:
						return False

					return True

			elif useType == "USE_ELEMENT_UPGRADE":
				if app.ENABLE_REFINE_ELEMENT and self.__CanRefineElementUpgrade(dstSlotPos):
					return True

			elif useType == "USE_ELEMENT_DOWNGRADE":
				if app.ENABLE_REFINE_ELEMENT and self.__CanRefineElementDowngrade(dstSlotPos):
					return True

			elif useType == "USE_ELEMENT_CHANGE":
				if app.ENABLE_REFINE_ELEMENT and self.__CanRefineElementChange(dstSlotPos):
					return True

			elif app.ENABLE_NEW_COSTUME_BONUS:
				if useType == "USE_ADD_COSTUME_ATTR_SPECIAL":
					dstItemVNum = player.GetItemIndex(dstSlotPos)
					if item.GetItemType(dstItemVNum) == item.ITEM_TYPE_COSTUME:
						item.SelectItem(srcItemVNum)

						if item.GetItemSubType(dstItemVNum) == item.GetValue(0):
							return True

			elif app.ENABLE_ORE_REFACTOR:
				if useType == "USE_REMOVE_ACCESSORY_SOCKET":
					dstItemVNum = player.GetItemIndex(dstSlotPos)
					item.SelectItem(dstItemVNum)
					if item.GetItemType() == item.ITEM_TYPE_ARMOR and item.GetItemSubType() in (item.ARMOR_EAR, item.ARMOR_NECK, item.ARMOR_WRIST):
						return True
					if item.GetItemType() == item.ITEM_TYPE_BELT:
						return True

	if app.SASH_ABSORPTION_ENABLE:
		def __CanReleaseSash(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if not (item.GetItemType() != item.ITEM_TYPE_COSTUME and item.GetItemSubType() != item.COSTUME_TYPE_SASH):
				return False

			return (player.GetItemMetinSocket(dstSlotPos, player.SASH_ABSORPTION_SOCKET) > 0)

	def __CanCleanBrokenMetinStone(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.ITEM_TYPE_WEAPON == item.GetItemType() or item.ITEM_TYPE_ARMOR == item.GetItemType():
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				if player.GetItemMetinSocket(dstSlotPos, i) == constInfo.ERROR_METIN_STONE:
					return True

		return False

	def __CanChangeItemAttrList(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM): #@Fix - visual bug when try change itens without attributes
			if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
				return True

		return False

	if app.ENABLE_USE_COSTUME_ATTR:
		def __CanChangeCostumeAttrList(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if item.GetItemType() != item.ITEM_TYPE_COSTUME:
				return False

			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM): #@Fix - visual bug when try change itens without attributes
				if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
					return True

			return False

		def __CanResetCostumeAttr(self, dstSlotPos):
			dstItemVNum = player.GetItemIndex(dstSlotPos)
			if dstItemVNum == 0:
				return False

			item.SelectItem(dstItemVNum)

			if item.GetItemType() != item.ITEM_TYPE_COSTUME:
				return False

			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM): #@Fix - visual bug when try change itens without attributes
				if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
					return True

			return False

	if app.ENABLE_REFINE_ELEMENT:
		# The checks bellow are just for that yellow effect that appear on slot
		# so you can remove them if you wish
		def __CanRefineElementUpgrade(self, dstSlotPos):
			dstItemVnum = player.GetItemIndex(dstSlotPos)
			dstItemElement = player.GetItemRefineElement(dstSlotPos)

			# if dstItemElement:
			# 	return False

			dstElemLevel = int(dstItemElement / 10000000 % 10)

			# Already max level
			if dstElemLevel == item.REFINE_ELEMENT_MAX:
				return False

			if not dstItemVnum:
				return False

			item.SelectItem(dstItemVnum)

			# Not a weapon
			if item.GetItemType() != item.ITEM_TYPE_WEAPON:
				return False

			# Can't be done on a < +7 weapon
			if item.GetRefineLevel() < item.ELEMENT_MIN_REFINE_LEVEL:
				return False

			# Not enough yang
			if player.GetElk() < item.REFINE_ELEMENT_UPGRADE_YANG:
				return False

			return True

		def __CanRefineElementDowngrade(self, dstSlotPos):
			dstItemVnum = player.GetItemIndex(dstSlotPos)
			dstItemElement = player.GetItemRefineElement(dstSlotPos)

			# Element is 0 so nothing to downgrade
			if not dstItemElement:
				return False

			if not dstItemVnum:
				return False

			item.SelectItem(dstItemVnum)

			if item.GetItemType() != item.ITEM_TYPE_WEAPON:
				return False

			if player.GetElk() < item.REFINE_ELEMENT_DOWNGRADE_YANG:
				return False

			return True

		def __CanRefineElementChange(self, dstSlotPos):
			dstItemVnum = player.GetItemIndex(dstSlotPos)
			dstItemElement = player.GetItemRefineElement(dstSlotPos)

			if not dstItemElement:
				return False

			if not dstItemVnum:
				return False

			item.SelectItem(dstItemVnum)

			if item.GetItemType() != item.ITEM_TYPE_WEAPON:
				return False

			if player.GetElk() < item.REFINE_ELEMENT_CHANGE_YANG:
				return False

			return True

	def __CanPutAccessorySocket(self, dstSlotPos, mtrlVnum):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		if app.ENABLE_ORE_REFACTOR:
			item.SelectItem(mtrlVnum)
			availableEquipments = [
				item.GetValue(2),
				item.GetValue(3),
				item.GetValue(4),
			]

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_ARMOR:
			return False

		if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
			return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		if app.ENABLE_ORE_REFACTOR:
			zeroedVnum = dstItemVNum - (dstItemVNum % 10)

			if not zeroedVnum in availableEquipments:
				return False
		else:
			if mtrlVnum != constInfo.GET_ACCESSORY_MATERIAL_VNUM(dstItemVNum, item.GetItemSubType()):
				return False

		if curCount>=maxCount:
			return False

		return True

	def __CanAddAccessorySocket(self, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if item.GetItemType() != item.ITEM_TYPE_BELT:
			if item.GetItemType() != item.ITEM_TYPE_ARMOR:
				return False

			if not item.GetItemSubType() in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				return False

		curCount = player.GetItemMetinSocket(dstSlotPos, 0)
		maxCount = player.GetItemMetinSocket(dstSlotPos, 1)

		ACCESSORY_SOCKET_MAX_SIZE = 3
		if maxCount >= ACCESSORY_SOCKET_MAX_SIZE:
			return False

		return True

	def __CanAddItemAttr(self, srcItemVNum, dstSlotPos):
		dstItemVNum = player.GetItemIndex(dstSlotPos)
		if dstItemVNum == 0:
			return False

		item.SelectItem(dstItemVNum)

		if not item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
			return False

		attrCount = 0
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM): #@Fix - visual bug when try change itens without attributes
			if player.GetItemAttribute(dstSlotPos, i)[0] != 0:
				attrCount += 1

		item.SelectItem(srcItemVNum)
		
		addedWhole = item.GetValue(1) > 0

		if attrCount < 5 if addedWhole else 4:
			return True

		return False

	def ShowToolTip(self, slotIndex):
		if None != self.tooltipItem:
			self.tooltipItem.SetInventoryItem(slotIndex)
			self.tooltipItem.InventoryAppendSellingPrice(slotIndex)

			if gcGetEnable("ENABLE_LEGENDARY_STONES"):
				if self.interface and self.interface.wndLegendaryStones:
					for sKey in self.interface.wndLegendaryStones:
						## We doesn't care about passive window
						if sKey == "PASSIVE":
							continue
					
						if self.interface.wndLegendaryStones[sKey].IsShow():
							self.tooltipItem.AppendShortcut([app.DIK_RMBUTTON, app.DIK_LALT], "Move to Legendary Stone Window")
							break
						

	def OnTop(self):
		if None != self.tooltipItem:
			self.tooltipItem.SetTop()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def UseItemSlot(self, slotIndex):
		curCursorNum = app.GetCursor()
		if app.SELL == curCursorNum:
			return

		if constInfo.GET_ITEM_QUESTION_DIALOG_STATUS():
			return

		slotIndex = self.__InventoryLocalSlotPosToGlobalSlotPos(slotIndex)

		if app.SASH_ABSORPTION_ENABLE:
			if (item.GetItemType() == item.ITEM_TYPE_COSTUME and item.GetItemSubType() == item.COSTUME_TYPE_SASH) and uisashsystem.IS_OPEN_COMBINATION:
				net.SendChatPacket("/sash_register_system_combination %d %d" % (-1, slotIndex))
				return

			if uisashsystem.IS_OPEN_ABSORPTION:
				if (uisashsystem.SashAbsorption().AutoPutItem(slotIndex)):
					return

		if gcGetEnable("ENABLE_LEGENDARY_STONES"):
			if self.interface and self.interface.wndLegendaryStones:
				for sKey in self.interface.wndLegendaryStones:
					## We doesn't care about passive window
					if sKey == "PASSIVE":
						continue

					if self.interface.wndLegendaryStones[sKey].IsShow() and app.IsPressed(app.DIK_LALT):
						if self.interface.wndLegendaryStones[sKey].PutItem(slotIndex):
							return

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			if self.wndDragonSoulRefine.IsShow():
				self.wndDragonSoulRefine.AutoSetItem((player.INVENTORY, slotIndex), 1)
				return

		if app.ENABLE_TREASURE_BOX_LOOT:
			if app.IsPressed(introInterface.GetWindowConfig("shortcust_items", introInterface.ITEM_CHECK_INFO, "key")):
				itemVnum = player.GetItemIndex(player.INVENTORY, slotIndex)
				if itemVnum in introInterface.GetWindowConfig("system", "treasure_box", "EMPTY_TREASURE_BOX_VNUM"):
					chat.AppendChat(1, localeInfo.LACK_OF_INFORMATION)
				elif itemVnum in introInterface.GetWindowConfig("system", "treasure_box", "TREASURE_BOX_ITEMS"):
					self.interface.OpenBoxLootWindow(itemVnum)
				else:
					net.SendRequestTreasureBoxLoot(itemVnum)
				return

		if app.ENABLE_SPECIAL_STORAGE:
			if app.IsPressed(introInterface.GetWindowConfig("shortcust_windows", introInterface.STORAGE_WND, "key")) and self.wndSpecialStorage.IsShow() and slotIndex < player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT:
				net.SendChatPacket("/transfer_to_special_storage %d" % slotIndex)
				return

			elif app.IsPressed(introInterface.GetWindowConfig("shortcust_windows", introInterface.STORAGE_WND, "key")) and self.wndSpecialStorage.IsShow() and slotIndex > player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT:
				self.__TransferItemToEmptyPos(slotIndex)
				return

		## SafeBox Support
		if gcGetEnable("ENABLE_FAST_INTERACTION_SAFEBOX") and app.IsPressed(introInterface.GetWindowConfig("shortcust_windows", introInterface.SAFEBOX_WND, "key")):
			safeboxWindow = self.interface.GetSafeboxWindow()
			if safeboxWindow and safeboxWindow.IsShow():
				g = safeboxWindow.BuildGrid()
				iw = itemWrapper.ItemGridWrapper(player.INVENTORY, slotIndex)
				pos = g.FindBlank(iw)
				if pos != -1:
					net.SendSafeboxCheckinPacket(player.INVENTORY, slotIndex, pos)
					return

		## Exchange Support
		if gcGetEnable("ENABLE_FAST_INTERACTION_EXCHANGE") and app.IsPressed(introInterface.GetWindowConfig("shortcust_windows", introInterface.EXCHANGE_WND, "key")):
			exchangeWindow = self.interface.GetExchangeWindow()
			if exchangeWindow and exchangeWindow.IsShow():
				g = exchangeWindow.BuildGrid()
				iw = itemWrapper.ItemGridWrapper(player.INVENTORY, slotIndex)
				pos = g.FindBlank(iw)
				if pos != -1:
					net.SendExchangeItemAddPacket(player.INVENTORY, slotIndex, pos)
					self.AppendLockSlot("EXCHANGE", slotIndex)
					return

		self.__UseItem(slotIndex)
		mouseModule.mouseController.DeattachObject()
		self.OverOutItem()

	if app.ENABLE_SPECIAL_STORAGE:
		def	__TransferItemToEmptyPos(self, attachedPos):
			## Building grid
			gridPool = [0 for x in xrange(player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT)]

			## Filling grid
			for i in xrange(player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT):
				itemVnum = player.GetItemIndex(i)
				if gridPool[i] > 0:
					continue

				if itemVnum > 0:
					item.SelectItem(itemVnum)
					(iWidth, iHeight) = item.GetItemSize()
					for a in xrange(iHeight):
						gridPool[i + a*5] = 1

				## If empty grid was found
				if gridPool[i] == 0:
					print attachedPos, i, 0
					self.__SendMoveItemPacket(attachedPos, i, 0)
					return

			## If no slot was found
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Not empty space.")

	def __UseItem(self, slotIndex):
		ItemVNum = player.GetItemIndex(slotIndex)
		item.SelectItem(ItemVNum)
			
		if ItemVNum == privateShop.PRIVATE_SHOP_SLOT_UNLOCK_ITEM:
			self.wndPrivateShop.OpenUnlockSlotDialog(slotIndex)
			return

		if app.ENABLE_RENEWAL_SHOP_SELLING:
			if app.IsPressed(introInterface.GetWindowConfig("shortcust_windows", introInterface.SHOP_WND, "key")) and self.interface.dlgShop.IsShow():
				# itemPrice = item.GetISellItemPrice()

				# if itemPrice < 1:
				# 	popup = uiCommon.PopupDialog()
				# 	popup.SetText(localeInfo.SHOP_CANNOT_SELL_ITEM)
				# 	popup.SetAutoClose()
				# 	popup.Open()
				# 	self.popup = popup
				# 	return

				# if itemPrice > 1:
				self.__SellItem(slotIndex)
				return

		if item.IsFlag(item.ITEM_FLAG_CONFIRM_WHEN_USE):
			self.questionDialog = uiCommon.QuestionDialog()
			self.questionDialog.SetText(localeInfo.INVENTORY_REALLY_USE_ITEM)
			self.questionDialog.SetAcceptEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnAccept))
			self.questionDialog.SetCancelEvent(ui.__mem_func__(self.__UseItemQuestionDialog_OnCancel))
			self.questionDialog.Open()
			self.questionDialog.slotIndex = slotIndex

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

		else:
			self.__SendUseItemPacket(slotIndex)
			#net.SendItemUsePacket(slotIndex)

	def __UseItemQuestionDialog_OnCancel(self):
		self.OnCloseQuestionDialog()

	def __UseItemQuestionDialog_OnAccept(self):
		self.__SendUseItemPacket(self.questionDialog.slotIndex)
		self.OnCloseQuestionDialog()

	def __SendUseItemToItemPacket(self, srcSlotPos, dstSlotPos, srcSlotType = player.INVENTORY, dstSlotType = player.INVENTORY):
		src_item_vnum = player.GetItemIndex(srcSlotType, srcSlotPos)

		if gcGetEnable("ENABLE_HAND_SWITCHER"):
			if self.HandSwitcher:
				uType = item.GetUseType(src_item_vnum)
				if (self.HandSwitcher.CanChangeItem(uType, srcSlotPos, dstSlotPos)):
					# If we have it opened just pass the action
					if self.HandSwitcher.IsShow():
						return

					self.HandSwitcher.SetConfiguration(srcSlotPos, dstSlotPos)
					self.HandSwitcher.Show()
					return

		net.SendItemUseToItemPacket(srcSlotPos, dstSlotPos)

	def __SendUseItemPacket(self, slotPos):
		## ItemOpener
		if gcGetEnable("ENABLE_FAST_INTERACTION_MULTI_USE"):
			if player.GetItemCount(slotPos) > 1 and app.IsPressed(introInterface.GetWindowConfig("shortcust_items", introInterface.ITEM_MULTI_USE, "key")):
				item.SelectItem(player.GetItemIndex(slotPos))
				if introInterface.GetWindowConfig("shortcust_items", introInterface.ITEM_MULTI_USE, "check")(slotPos, player.GetItemIndex(slotPos), item):
					self.ItemOpener.OpenWithSlot(slotPos)
					return

		net.SendItemUsePacket(slotPos)

	def __SendMoveItemPacket(self, srcSlotPos, dstSlotPos, srcItemCount):		
		net.SendItemMovePacket(srcSlotPos, dstSlotPos, srcItemCount)
		return True

	def SetDragonSoulRefineWindow(self, wndDragonSoulRefine):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoulRefine = wndDragonSoulRefine

	def OnMoveWindow(self, x, y):
		if self.interface:
			if app.ENABLE_LUCKY_BOX and self.interface.wndLuckyBoxWindow and self.interface.wndLuckyBoxWindow.IsShow():
				self.interface.wndLuckyBoxWindow.AdjustPosition()

		if gcGetEnable("ENABLE_RIGHT_PANEL_INVENTORY"):
			if self.__sideBar:
				self.__sideBar.Reposition(x, y)

		# if self.wndCostume.IsShow():
		# 	self.wndCostume.Reposition(x, y)

		# if app.ENABLE_SPECIAL_STORAGE:
		# 	if self.wndSpecialStorage.IsShow():
		# 		self.wndSpecialStorage.Reposition(x, y)

	if gcGetEnable("ENABLE_EQUIPMENT_LOCK_SLOT"):
		def GetEquipmentLockStatus(self, iSlot):
			return constInfo.EQUIPMENT_LOCK_INFO.get(iSlot, None)

		def RefreshEquipmentLock(self):
			for key, values in constInfo.EQUIPMENT_LOCK_INFO.items():
				self.ApplyEquipmentLock(key, not values.get("STATUS", False))

		def ApplyEquipmentLock(self, iSlot, bStatus = False):
			iSlot = iSlot + player.EQUIPMENT_SLOT_START
			if bStatus:
				self.wndEquip.SetCoverButton(iSlot, "assets/ui/elements/locked_slot/big.dds",\
															"assets/ui/elements/locked_slot/big.dds",\
															"assets/ui/elements/locked_slot/big.dds",\
															"assets/ui/elements/locked_slot/big.dds", False, False)

				self.wndEquip.SetAlwaysRenderCoverButton(iSlot, True)
			else:
				self.wndEquip.DeleteCoverButton(iSlot)
				
	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def BindPrivateShopClass(self, window):
			self.wndPrivateShop = window
			
		def BindPrivateShopSearchClass(self, window):
			self.wndPrivateShopSearch = window	
