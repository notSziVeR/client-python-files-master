#!/usr/bin/python
#-*- coding: iso-8859-1 -*-
import exchange
import player
import item
import net
import constInfo

import grp, ui, math

def GetExchangeEmptyPos(itemHeight, getItemIndex):
	player.EXCHANGE_PAGE_X_SLOTCOUNT	= 6
	player.EXCHANGE_PAGE_Y_SLOTCOUNT	= 4
	player.EXCHANGE_PAGE_SIZE			= player.EXCHANGE_PAGE_X_SLOTCOUNT * player.EXCHANGE_PAGE_Y_SLOTCOUNT

	if player.EXCHANGE_PAGE_X_SLOTCOUNT * player.EXCHANGE_PAGE_Y_SLOTCOUNT > exchange.EXCHANGE_ITEM_MAX_NUM:
		player.EXCHANGE_PAGE_SIZE = exchange.EXCHANGE_ITEM_MAX_NUM

	getStartIndex = lambda arg : 0

	curPageGrid = [0] * (player.EXCHANGE_PAGE_SIZE)
	for y in xrange(player.EXCHANGE_PAGE_Y_SLOTCOUNT - itemHeight + 1):
		for x in xrange(player.EXCHANGE_PAGE_X_SLOTCOUNT):
			slotIndex = y * player.EXCHANGE_PAGE_X_SLOTCOUNT + x
			itemVnum = getItemIndex(slotIndex)
			if curPageGrid[y * player.EXCHANGE_PAGE_X_SLOTCOUNT + x] == 0 and itemVnum == 0:
				success = True

				for i in xrange(itemHeight):
					currentSlotIndex = y * player.EXCHANGE_PAGE_X_SLOTCOUNT + x + i * player.EXCHANGE_PAGE_X_SLOTCOUNT
					if getItemIndex(currentSlotIndex) != 0:
						success = False
						break

				if success == True:
					return y * player.EXCHANGE_PAGE_X_SLOTCOUNT + x
			elif itemVnum != 0:
				item.SelectItem(itemVnum)
				(_, height) = item.GetItemSize()
				for i in xrange(height):
					curPageGrid[(y + i) * player.EXCHANGE_PAGE_X_SLOTCOUNT + x] = 1

	return -1

def GetEmptyItemPosList(itemHeight, pageCount, getItemIndex):
	player.INVENTORY_PAGE_X_SLOTCOUNT = 5
	player.INVENTORY_PAGE_Y_SLOTCOUNT = 9

	getStartIndex = lambda arg : arg * player.INVENTORY_PAGE_SIZE

	slotList = []
	for page in xrange(pageCount):
		curPageGrid = [0] * (player.INVENTORY_PAGE_SIZE)
		for y in xrange(player.INVENTORY_PAGE_Y_SLOTCOUNT - itemHeight + 1):
			for x in xrange(player.INVENTORY_PAGE_X_SLOTCOUNT):
				slotIndex = getStartIndex(page) + y * player.INVENTORY_PAGE_X_SLOTCOUNT + x
				itemVnum = getItemIndex(slotIndex)
				if curPageGrid[y * player.INVENTORY_PAGE_X_SLOTCOUNT + x] == 0 and itemVnum == 0:
					success = True

					for i in xrange(itemHeight):
						currentSlotIndex = getStartIndex(page) + y * player.INVENTORY_PAGE_X_SLOTCOUNT + x + i * player.INVENTORY_PAGE_X_SLOTCOUNT
						if getItemIndex(currentSlotIndex) != 0:
							success = False
							break

					if success == True:
						slotList.append(getStartIndex(page) + y * player.INVENTORY_PAGE_X_SLOTCOUNT + x)

				elif itemVnum != 0:
					item.SelectItem(itemVnum)
					(_, tempHeight) = item.GetItemSize()
					for i in xrange(tempHeight):
						curPageGrid[(y + i) * player.INVENTORY_PAGE_X_SLOTCOUNT + x] = 1

	return slotList

def GetEmptyItemPos(itemHeight, pageCount, getItemIndex):
	getStartIndex = lambda arg : arg * player.INVENTORY_PAGE_SIZE

	for page in xrange(pageCount):
		curPageGrid = [0] * (player.INVENTORY_PAGE_SIZE)
		for y in xrange(player.INVENTORY_PAGE_COLUMN - itemHeight + 1):
			for x in xrange(player.INVENTORY_PAGE_ROW):
				slotIndex = getStartIndex(page) + y * player.INVENTORY_PAGE_COLUMN + x
				itemVnum = getItemIndex(slotIndex)
				if curPageGrid[y * player.INVENTORY_PAGE_ROW + x] == 0 and itemVnum == 0:
					success = True

					for i in xrange(itemHeight):
						currentSlotIndex = getStartIndex(page) + y * player.INVENTORY_PAGE_ROW + x + i * player.INVENTORY_PAGE_COLUMN
						if getItemIndex(currentSlotIndex) != 0:
							success = False
							break

					if success == True:
						return getStartIndex(page) + y * player.INVENTORY_PAGE_ROW + x

				elif itemVnum != 0:
					item.SelectItem(itemVnum)
					(_, tempHeight) = item.GetItemSize()
					for i in xrange(tempHeight):
						curPageGrid[(y + i) * player.INVENTORY_PAGE_COLUMN + x] = 1

	return -1

def GetEmptyItemPosOfflineShop(itemHeight, itemDict):
	getItemIndex = lambda i : 0 if not i in itemDict else player.GetItemIndex(*itemDict[i])

	INVENTORY_PAGE_ROW = 6
	INVENTORY_PAGE_COLUMN = 10

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
					curPageGrid[(y + i) * INVENTORY_PAGE_ROW + x] = 1

	return -1

def ClickSortInventoryButton():
	itemDict = {}
	for i in range(player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT):
		itemVnum = player.GetItemIndex(i)
		itemCount = player.GetItemCount(i)

		if not itemVnum: continue
		if itemCount == constInfo.ITEM_COUNT_MAX: continue

		item.SelectItem(itemVnum)
		if not item.IsFlag(item.ITEM_FLAG_STACKABLE) or item.IsAntiFlag(item.ITEM_ANTIFLAG_STACK): continue

		if itemVnum in itemDict:
			if itemCount > player.GetItemCount(itemDict[itemVnum]):
				itemDict[itemVnum] = i
		else:
			itemDict[itemVnum] = i

	for (itemVnum, index) in itemDict.iteritems():
		itemCount = player.GetItemCount(index)
		for i in range(player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT):
			if index == i: continue
			if player.GetItemIndex(i) != itemVnum: continue
			if player.GetItemCount(i) == constInfo.ITEM_COUNT_MAX: continue

			count = player.GetItemCount(i)
			if (itemCount + count >= constInfo.ITEM_COUNT_MAX):
				count = constInfo.ITEM_COUNT_MAX - itemCount

			net.SendItemMovePacket(i, index, count)
			itemCount += count

			if itemCount >= constInfo.ITEM_COUNT_MAX:
				break

class ReworkedScrollBar(ui.Window):
	class MiddleBar(ui.DragButton):
		def __init__(self, horizontal_scroll):
			super(ReworkedScrollBar.MiddleBar, self).__init__()
			self.AddFlag("movable")

			self.horizontal_scroll = horizontal_scroll

			self.middle = ui.Bar()
			self.middle.SetParent(self)
			self.middle.AddFlag("attach")
			self.middle.AddFlag("not_pick")
			self.middle.SetColor(0xff3e3834)
			self.middle.SetSize(1, 1)
			self.middle.Show()

		def __del__(self):
			super(ReworkedScrollBar.MiddleBar, self).__del__()

		def SetStaticScale(self, size):
			(base_width, base_height) = (self.middle.GetWidth(), self.middle.GetHeight())

			if not self.horizontal_scroll:
				super(ReworkedScrollBar.MiddleBar, self).SetSize(base_width, size)
				self.middle.SetSize(base_width, size)
			else:
				super(ReworkedScrollBar.MiddleBar, self).SetSize(size, base_height)
				self.middle.SetSize(size, base_height)

		def SetSize(self, selfSize, fullSize):
			(base_width, base_height) = (self.middle.GetWidth(), self.middle.GetHeight())

			if not self.horizontal_scroll:
				super(ReworkedScrollBar.MiddleBar, self).SetSize(base_width, float((selfSize*1.0)/ int(fullSize)) * selfSize)
				self.middle.SetSize(base_width, float((selfSize*1.0)/ int(fullSize)) * selfSize)
			else:
				super(ReworkedScrollBar.MiddleBar, self).SetSize(float((selfSize*1.0)/ int(fullSize)) * selfSize, base_height)
				self.middle.SetSize(float((selfSize*1.0)/ int(fullSize)) * selfSize, base_height)

		def SetStaticSize(self, size):
			size = max(2, size)

			if not self.horizontal_scroll:
				super(ReworkedScrollBar.MiddleBar, self).SetSize(size, self.middle.GetHeight())
				self.middle.SetSize(size, self.middle.GetHeight())
			else:
				super(ReworkedScrollBar.MiddleBar, self).SetSize(self.middle.GetWidth(), size)
				self.middle.SetSize(self.middle.GetWidth(), size)

	def __init__(self, horizontal_scroll = False):
		super(ReworkedScrollBar, self).__init__()

		self.horizontal_scroll = horizontal_scroll

		self.blockMoveEvent = False
		self.scrollEvent = None
		self.scrollSpeed = 1

		self.bars = []
		for i in xrange(9):
			br = ui.Bar()
			br.SetParent(self)
			br.AddFlag("attach")
			br.AddFlag("not_pick")
			br.SetColor([grp.GenerateColor(0.306, 0.306, 0.306, 1.0), grp.GenerateColor(0.306, 0.306, 0.306, 0.0)][i == 8])
			if not (i % 2 == 0): br.SetSize(1, 1)
			br.Show()

			self.bars.append(br)

		self.middleBar = self.MiddleBar(self.horizontal_scroll)
		self.middleBar.SetParent(self)
		self.middleBar.SetMoveEvent(ui.__mem_func__(self.OnScrollMove))
		self.middleBar.Show()

	def __del__(self):
		super(ReworkedScrollBar, self).__del__()

	def OnScrollMove(self):
		if not self.scrollEvent:
			return

		arg = float(self.middleBar.GetLocalPosition()[1] - 1) / float(self.GetHeight() - 2 - self.middleBar.GetHeight()) if not self.horizontal_scroll else\
				float(self.middleBar.GetLocalPosition()[0] - 1) / float(self.GetWidth() - 2 - self.middleBar.GetWidth())

		self.scrollEvent(arg)

	def SetScrollEvent(self, func):
		self.scrollEvent = ui.__mem_func__(func)

	def SetScrollSpeed(self, speed):
		self.scrollSpeed = speed

	def SetBlockMoveEvent(self, state):
		self.blockMoveEvent = state

	def GetBlockMoveState(self):
		return self.blockMoveEvent

	def OnMouseLeftButtonDown(self):
		if self.GetBlockMoveState() is True:
			return

		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()

		if not self.horizontal_scroll:
			if xMouseLocalPosition == 0 or xMouseLocalPosition == self.GetWidth():
				return

			y_pos = (yMouseLocalPosition - self.middleBar.GetHeight() / 2)
			self.middleBar.SetPosition(1, y_pos)
		else:
			if yMouseLocalPosition == 0 or yMouseLocalPosition == self.GetHeight():
				return

			x_pos = (xMouseLocalPosition - self.middleBar.GetWidth() / 2)
			self.middleBar.SetPosition(x_pos, 1)

		self.OnScrollMove()

	def SetSize(self, w, h):
		(width, height) = (max(3, w), max(3, h))

		ui.Window.SetSize(self, width, height)

		self.bars[0].SetSize(1, (height - 2))
		self.bars[0].SetPosition(0, 1)
		self.bars[2].SetSize((width - 2), 1)
		self.bars[2].SetPosition(1, 0)
		self.bars[4].SetSize(1, (height - 2))
		self.bars[4].SetPosition((width - 1), 1)
		self.bars[6].SetSize((width - 2), 1)
		self.bars[6].SetPosition(1, (height - 1))
		self.bars[8].SetSize((width - 2), (height - 2))
		self.bars[8].SetPosition(1, 1)

		self.bars[1].SetPosition(0, 0)
		self.bars[3].SetPosition((width - 1), 0)
		self.bars[5].SetPosition((width - 1), (height - 1))
		self.bars[7].SetPosition(0, (height - 1))

		if not self.horizontal_scroll:
			self.middleBar.SetStaticSize(width - 2)
			self.middleBar.SetSize(12, self.GetHeight())
		else:
			self.middleBar.SetStaticSize(height - 2)
			self.middleBar.SetSize(12, self.GetWidth())

		self.middleBar.SetRestrictMovementArea(1, 1, width - 2, height - 2)

	def OnRunMouseWheelEvent(self, length):
		if self.GetBlockMoveState() is True:
			return

		if not self.horizontal_scroll:
			val = min(max(1, self.middleBar.GetLocalPosition()[1] - (length * 0.01) * self.scrollSpeed), self.GetHeight() - self.middleBar.GetHeight() - 1)
			self.middleBar.SetPosition(1, val)
		else:
			val = min(max(1, self.middleBar.GetLocalPosition()[0] - (length * 0.01) *  self.scrollSpeed), self.GetWidth() - self.middleBar.GetWidth() - 1)
			self.middleBar.SetPosition(val, 1)

		self.OnScrollMove()
		return True

	def SetScale(self, selfSize, fullSize):
		self.middleBar.SetSize(selfSize, fullSize)

	def SetStaticScale(self, r_size):
		self.middleBar.SetStaticScale(r_size)

	def SetPosScale(self, fScale):
		pos = (math.ceil((self.GetHeight() - 2 - self.middleBar.GetHeight()) * fScale) + 1) if not self.horizontal_scroll else\
				(math.ceil((self.GetWidth() - 2 - self.middleBar.GetWidth()) * fScale) + 1)

		self.SetPos(pos)

	def GetPos(self):
		return ((float(1) * self.middleBar.GetLocalPosition()[1]) / self.GetHeight())

	def SetPos(self, pos):
		wPos = (1, pos) if not self.horizontal_scroll else (pos, 1)
		self.middleBar.SetPosition(*wPos)
