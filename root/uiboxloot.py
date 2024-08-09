#!/usr/bin/python
#-*- coding: iso-8859-1 -*-
import ui
import item
import uiScriptLocale

from _weakref import proxy

def getLocaleName(key):
	localeDict = {
		"title" : uiScriptLocale.BOX_LOOT_TITLE,
	}
	return localeDict.get(key, "#" + key)

class BoxLootWindow(ui.SimplyWindow):
	def __init__(self):
		ui.SimplyWindow.__init__(self, "UI", ("movable", "float"), 272, 70, self._Initialize, self._Destroy)

	def __del__(self):
		ui.SimplyWindow.__del__(self)

	def _Initialize(self):
		self.itemToolTip = None
		self.itemSlotDict = {}

		self.windowConfig["default_grid_size"] = 8

		board = ui.BoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetTitleName(getLocaleName("title"))
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.SetSize(self.GetWidth(), self.GetHeight())
		board.Show()

		self.AppendObject("board", board)

		bar = ui.Bar()
		bar.SetParent(self.GetObject("board"))
		bar.SetPosition(0, 30)
		bar.SetSize(self.GetWidth() - 2 * 8, self.GetHeight() - 8 - 30)
		bar.SetWindowHorizontalAlignCenter()
		bar.SetColor(0x60000000)
		bar.Show()

		self.AppendObject("bar", bar)

		gridTable = ui.GridSlotWindow()
		gridTable.SetParent(self.GetObject("bar"))
		gridTable.SetPosition(0, 0)
		gridTable.SetOverInItemEvent(ui.__mem_func__(self._OnOverInItem))
		gridTable.SetOverOutItemEvent(ui.__mem_func__(self._OnOverOutItem))
		gridTable.SetWindowHorizontalAlignCenter()
		gridTable.Show()

		self.AppendObject("grid_table", gridTable)

	def _Destroy(self):
		self.itemToolTip = None
		self.itemSlotDict = {}

	def _OnOverInItem(self, slotIndex):
		if self.itemToolTip:
			if self.itemSlotDict.get(slotIndex, 0):
				self.itemToolTip.SetItemToolTip(self.itemSlotDict[slotIndex])

	def _OnOverOutItem(self):
		if self.itemToolTip:
			self.itemToolTip.HideToolTip()

	def _GetEmptySlotIndex(self, itemHeight):
		getItemIndex = lambda i : self.itemSlotDict.get(i, 0)

		INVENTORY_PAGE_ROW = self.windowConfig["default_grid_size"]
		INVENTORY_PAGE_COLUMN = 32

		curPageGrid = [0] * (INVENTORY_PAGE_ROW * INVENTORY_PAGE_COLUMN)
		for y in xrange(INVENTORY_PAGE_COLUMN - itemHeight + 1):
			for x in xrange(INVENTORY_PAGE_ROW):
				slotIndex = y * INVENTORY_PAGE_ROW + x
				itemVnum = getItemIndex(slotIndex)
				if curPageGrid[y * INVENTORY_PAGE_ROW + x] == 0 and itemVnum == 0:
					success = True

					for i in xrange(itemHeight):
						currentSlotIndex = y * INVENTORY_PAGE_ROW + x + i * INVENTORY_PAGE_ROW
						if getItemIndex(currentSlotIndex) != 0:
							success = False
							break

					if success == True:
						return y * INVENTORY_PAGE_ROW + x

				elif itemVnum != 0:
					item.SelectItem(itemVnum)
					(_, tempHeight) = item.GetItemSize()
					for i in xrange(tempHeight):
						curPageGrid[(y + i) * INVENTORY_PAGE_ROW + x] = tempHeight

		return -1

	def _GetMaxColumn(self):
		getItemIndex = lambda i : self.itemSlotDict.get(i, 0)

		INVENTORY_PAGE_ROW = self.windowConfig["default_grid_size"]
		INVENTORY_PAGE_COLUMN = 32

		curPageGrid = {}
		for y in xrange(INVENTORY_PAGE_COLUMN):
			for x in xrange(INVENTORY_PAGE_ROW):
				slotIndex = y * INVENTORY_PAGE_ROW + x
				itemVnum = getItemIndex(slotIndex)

				if itemVnum != 0:
					item.SelectItem(itemVnum)
					(_, tempHeight) = item.GetItemSize()
					for i in xrange(tempHeight):
						curPageGrid[(y + i) * INVENTORY_PAGE_ROW + x] = itemVnum

		return max(curPageGrid) / self.windowConfig["default_grid_size"]

	def _UpdateSize(self, col):
		self.SetSize(self.GetWidth(), 32 * col + 30 + 9)
		self.GetObject("board").SetSize(*self.GetSize())
		self.GetObject("bar").SetSize(self.GetWidth() - 2 * 8, self.GetHeight() - 8 - 30)

		self.SetCenterPosition()

	def SetItemToolTip(self, itemToolTip):
		self.itemToolTip = proxy(itemToolTip)

	def RefreshWindow(self, itemIndex):
		if not itemIndex in GetWindowConfig("system", "treasure_box", "TREASURE_BOX_ITEMS"):
			return False

		self.itemSlotDict = {}

		for (itemVnum, _) in GetWindowConfig("system", "treasure_box", "TREASURE_BOX_ITEMS")[itemIndex]:
			item.SelectItem(itemVnum)

			(_, height) = item.GetItemSize()
			slotIndex = self._GetEmptySlotIndex(height)

			if slotIndex != -1:
				self.itemSlotDict[slotIndex] = itemVnum

		col = self._GetMaxColumn()
		col += 1
		self._UpdateSize(col)

		self.GetObject("grid_table").ArrangeSlot(0, self.windowConfig["default_grid_size"], col, 32, 32, 0, 0)
		self.GetObject("grid_table").SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		self.GetObject("grid_table").SetWindowHorizontalAlignCenter()

		for slotIndex, itemVnum in self.itemSlotDict.iteritems():
			self.GetObject("grid_table").SetItemSlot(slotIndex, itemVnum, 0)

		self.GetObject("grid_table").RefreshSlot()

		item.SelectItem(itemIndex)
		self.GetObject("board").SetTitleName(item.GetItemName())


