#!/usr/bin/python
#-*- coding: iso-8859-1 -*-
import localeInfo
import ui
import item
import player
import net
from _weakref import proxy

def getLocaleName(key):
	localeDict = {
		"title" : localeInfo.REMOVE_STONE_WINDOW_TITLE,
		"pull"	: localeInfo.REMOVE_STONE_WINDOW_BUTTON_REMOVE,
		"empty" : localeInfo.REMOVE_STONE_WINDOW_FREE_SLOT,
	}
	return localeDict.get(key, "#" + str(key))

SOCKET_START_INDEX = 10
METIN_SOCKET_MAX_NUM = 3

class RemoveStoneWindow(ui.SimplyWindow):
	def __init__(self):
		ui.SimplyWindow.__init__(self, "UI", ("movable", "float", ), 242, 128 + 64, self._Initialize, self._Destroy)

	def __del__(self):
		ui.SimplyWindow.__del__(self)

	def _Initialize(self):
		self.slotIndex = -1
		self.socketIndex = 0
		self.itemToolTip = None

		board = ui.Board()
		board.SetParent(self)
		board.SetSize(164, 32)
		board.SetWindowHorizontalAlignCenter()
		board.SetWindowVerticalAlignBottom()
		board.SetPosition(0, board.GetHeight())
		board.Show()

		self.AppendObject("board", board, True)

		board = ui.BoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetSize(self.GetWidth(), self.GetHeight() - 30)
		board.SetTitleName(getLocaleName("title"))
		board.SetCloseEvent(lambda *args : net.SendRequestDeleteSocket(net.SUBHEADER_REQUEST_DELETE_SOCKET_CLOSE))
		board.Show()

		self.AppendObject("board", board, True)

		button = ui.Button()
		button.SetParent(self.GetObject("board", 0))
		button.SetUpVisual("d:/ymir work/ui/game/myshop_deco/select_btn_01.sub")
		button.SetOverVisual("d:/ymir work/ui/game/myshop_deco/select_btn_02.sub")
		button.SetDownVisual("d:/ymir work/ui/game/myshop_deco/select_btn_03.sub")
		button.SetPosition(0, button.GetHeight() + 8)
		button.SetWindowHorizontalAlignCenter()
		button.SetWindowVerticalAlignBottom()
		button.SetText(getLocaleName("pull"))
		button.SAFE_SetEvent(self.__OnClickButtonEvent)
		button.Show()

		self.AppendObject("button", button, True)

		bar = ui.Bar()
		bar.SetParent(self.GetObject("board", 1))
		bar.SetPosition(0, 30)
		bar.SetSize(self.GetWidth() - 12, self.GetHeight() - 32 - 30 - 8)
		bar.SetWindowHorizontalAlignCenter()
		bar.SetColor(0x90000000)
		bar.Show()

		self.AppendObject("bar", bar)

		gridTable = ui.GridSlotWindow()
		gridTable.SetParent(self.GetObject("bar"))
		gridTable.SetPosition(8, 0)
		gridTable.ArrangeSlot(0, 1, 3, 32, 32, 0, 0)
		gridTable.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		gridTable.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
		gridTable.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))
		gridTable.SetWindowVerticalAlignCenter()
		gridTable.Show()

		self.AppendObject("grid_table", gridTable)

		line = ui.Line()
		line.SetParent(self.GetObject("bar"))
		line.SetPosition(8 + 32 + 8, 0)
		line.SetSize(0, bar.GetHeight())
		line.SetColor(0x70FFFFFF)
		line.Show()

		self.AppendObject("line", line, True)

		slot = ui.SlotWindow()
		slot.SetParent(self.GetObject("bar"))
		slot.SetPosition(48, 0)
		slot.SetSize(self.GetWidth() - 48, 118)
		slot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		slotIndexList = (
			{ "index" : SOCKET_START_INDEX + 0, "x" : 8, "y" : 4,		"width" : 32,	"height" : 32 },
			{ "index" : SOCKET_START_INDEX + 1, "x" : 8, "y" : 32 + 13,	"width" : 32,	"height" : 32 },
			{ "index" : SOCKET_START_INDEX + 2, "x" : 8, "y" : 86,		"width" : 32,	"height" : 32 },
		)
		slot.SAFE_SetButtonEvent("LEFT", "EXIST", self.__OnUnselectItemSlot)
		slot.SAFE_SetButtonEvent("RIGHT", "EXIST", self.__OnUnselectItemSlot)
		slot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInItem))
		slot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutItem))
		[slot.AppendSlot(i["index"], i["x"], i["y"], i["width"], i["height"]) for i in slotIndexList]
		slot.Show()

		self.AppendObject("slot", slot)

		textLine = [ui.TextLine() for _ in range(3)]
		textLine[0].SetParent(self.GetObject("slot"))
		textLine[0].SetPosition(44, 1)
		textLine[0].Show()
		textLine[1].SetParent(self.GetObject("slot"))
		textLine[1].SetPosition(44, 42)
		textLine[1].Show()
		textLine[2].SetParent(self.GetObject("slot"))
		textLine[2].SetPosition(44, 83)
		textLine[2].Show()

		self.AppendObject("text", textLine)

	def _Destroy(self):
		self.slotIndex = -1
		self.socketIndex = 0
		self.itemToolTip = None

	def __ClearItems(self):
		self.slotIndex = -1
		self.socketIndex = 0

		for i in range(METIN_SOCKET_MAX_NUM):
			self.GetObject("text", i).SetText(getLocaleName("empty"))
			self.GetObject("slot").DeactivateSlot(10 + i)
			self.GetObject("slot").ClearSlot(10 + i)

		self.GetObject("grid_table").ClearSlot(0)

		self.GetObject("grid_table").RefreshSlot()
		self.GetObject("slot").RefreshSlot()

	def __OnUnselectItemSlot(self, slotIndex):
		slotIndex -= SOCKET_START_INDEX

		if player.GetItemMetinSocket(self.slotIndex, slotIndex) <= 1:
			return False

		self.socketIndex ^= (1 << slotIndex)

		if self.socketIndex & (1 << slotIndex):
			self.GetObject("slot").ActivateSlot(SOCKET_START_INDEX + slotIndex)
		else:
			self.GetObject("slot").DeactivateSlot(SOCKET_START_INDEX + slotIndex)

	def __OnOverInItem(self, slotIndex):
		if self.slotIndex == -1:
			return False

		if not self.itemToolTip:
			return False

		if slotIndex == 0:
			self.itemToolTip.SetInventoryItem(self.slotIndex)
		else:
			slotIndex -= SOCKET_START_INDEX
			self.itemToolTip.SetItemToolTip(player.GetItemMetinSocket(self.slotIndex, slotIndex))

	def __OnOverOutItem(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()

	def __OnClickButtonEvent(self):
		if not self.socketIndex:
			return False

		net.SendRequestDeleteSocket(net.SUBHEADER_REQUEST_DELETE_SOCKET_DELETE, self.socketIndex)

		self.OnPressExitKey()

	def SetItemToolTip(self, itemToolTip):
		self.itemToolTip = proxy(itemToolTip)

	def RemoveStoneSetItem(self, slotIndex):
		if player.GetItemIndex(player.INVENTORY, slotIndex) == 0:
			return False

		self.__ClearItems()

		self.slotIndex = slotIndex
		self.GetObject("grid_table").SetItemSlot(0, player.GetItemIndex(player.INVENTORY, slotIndex), 0)

		for i in range(METIN_SOCKET_MAX_NUM):
			itemVnum = player.GetItemMetinSocket(slotIndex, i)
			if itemVnum <= 1:
				self.GetObject("text", i).SetText(getLocaleName("empty"))
				continue
			self.GetObject("slot").SetItemSlot(SOCKET_START_INDEX + i, itemVnum, 0)

			item.SelectItem(itemVnum)
			self.GetObject("text", i).SetText(item.GetItemName())

		self.GetObject("grid_table").RefreshSlot()
		self.GetObject("slot").RefreshSlot()

	def Close(self):
		self.__OnOverOutItem()
		self.Hide()

	OnPressExitKey = OnPressEscapeKey = lambda *args : net.SendRequestDeleteSocket(net.SUBHEADER_REQUEST_DELETE_SOCKET_CLOSE)


