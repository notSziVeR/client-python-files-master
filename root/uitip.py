#-*- coding: iso-8859-1 -*-
import ui
import grp
import app

import wndMgr
import player

import localeInfo

class TextBar(ui.Window):
	def __init__(self, width, height):
		ui.Window.__init__(self)
		self.handle = grp.CreateTextBar(width, height)

	def __del__(self):
		ui.Window.__del__(self)
		grp.DestroyTextBar(self.handle)

	def ClearBar(self):
		grp.ClearTextBar(self.handle)

	def SetClipRect(self, x1, y1, x2, y2):
		grp.SetTextBarClipRect(self.handle, x1, y1, x2, y2)

	def TextOut(self, x, y, text):
		grp.TextBarTextOut(self.handle, x, y, text)

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		grp.RenderTextBar(self.handle, x, y)

	def SetTextColor(self, r, g, b):
		grp.TextBarSetTextColor(self.handle, r, g, b)

	def GetTextExtent(self, text):
		return grp.TextBarGetTextExtent(self.handle, text)

class Lines(ui.Window):
	STATE_NONE = 0
	STATE_SCROLLING = 1

	def __init__(self, width, lines, fontSize=12, scrollTime=3.0, textColor=(1, 1, 1), big=False):
		ui.Window.__init__(self)
		font = localeInfo.UI_DEF_FONT_BOLD if big else localeInfo.UI_DEF_FONT
		self.padding = 5.0
		self.SetSize(width, lines * (fontSize + self.padding))
		self.lineCount = lines
		self.shown = []
		self.lines = []
		for i in range(lines * 2):
			line = ui.TextLine()
			line.SetParent(self)
			line.SetFontName(font)
			line.SetFontColor(*textColor)
			if big:
				line.SetWindowHorizontalAlignCenter()
			self.lines.append(line)
		self.fontSize = fontSize
		self.scrollTime = scrollTime
		self.nextScroll = 0
		self.state = self.STATE_NONE
		self.scrollDif = 0
		self.scrollRate = 1  # *60 px per second
		self.curL = -lines
		self.text = []

	def OnUpdate(self):
		if self.state == self.STATE_SCROLLING and len(self.shown) != 0:
			scroll = min(self.scrollRate, self.scrollDif)
			for l in self.shown:
				x, y = l.GetLocalPosition()
				l.SetPosition(int(x), int(y - scroll))
				l.SetClipRect(-x, -y, self.GetWidth() - x, self.GetHeight() - y)
			self.scrollDif -= scroll
			if self.scrollDif <= 0:
				move = []
				for l in self.shown:
					x, y = l.GetLocalPosition()
					if y < -self.fontSize:  # should be out of screen by now
						move.append(l)
				for l in move:
					self.shown.remove(l)
					l.Hide()
					self.lines.append(l)
					self.curL -= 1

				self._TryAdd()
				self.state = self.STATE_NONE
				self.nextScroll = app.GetTime() + self.scrollTime

		elif app.GetTime() > self.nextScroll:
			self.scrollDif = self.GetHeight()
			self.state = self.STATE_SCROLLING

	def GetShownCount(self):
		return len(self.shown) + len(self.text)

	def _TryAdd(self):
		added = 0
		for text in self.text:
			if len(self.lines) == 0:
				break

			l = self.lines.pop()
			l.SetText(text)
			l.Show()
			y = (self.lineCount + self.curL) * (self.fontSize + self.padding) + (
				self.scrollDif if self.scrollDif == self.GetHeight() else 0)
			l.SetPosition(0, int(y))
			l.SetClipRect(0, 0, self.GetWidth(), self.GetHeight() - y)
			self.shown.append(l)
			self.curL += 1
			added += 1

		del self.text[:added]

	def AddText(self, text):
		self.text.append(text)
		if len(self.shown) == 0:
			self.state = self.STATE_NONE
			self.nextScroll = app.GetTime() + self.scrollTime
		if self.state != self.STATE_SCROLLING:
			self._TryAdd()

	def SetPosition(self, x, y):
		ui.Window.SetPosition(self, int(x), int(y))
		for l in self.shown + self.lines:
			l.SetClipRect(x, y, x + self.GetWidth(), y + self.GetHeight())

class TipBoard(ui.Bar):
	def __init__(self):
		ui.Bar.__init__(self)

		self.AddFlag("not_pick")
		self.tipList = []
		self.curPos = 0
		self.dstPos = 0
		self.nextScrollTime = 0

		self.width = 370

		self.SetPosition(0, 70)
		self.SetSize(370, 20)
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.0))
		self.SetWindowHorizontalAlignCenter()

		self.SetInsideRender(True)

		self.imgBg = ui.ImageBox( )
		self.imgBg.SetParent( self )
		self.imgBg.SetPosition( 0, 0 )
		self.imgBg.LoadImage("assets/ui/tips/tip.tga")
		self.imgBg.Show()

		self.lines = Lines(370, 1)
		self.lines.SetParent(self)
		self.lines.SetPosition(3, 2)
		self.lines.Show()

	def SetTip(self, text):
		self.lines.AddText(text)

		if not self.IsShow():
			self.Show()

	def OnUpdate(self):
		if self.lines.GetShownCount() == 0:
			self.Hide()
			return

class BigTextBar(TextBar):
	def __init__(self, width, height, fontSize):
		ui.Window.__init__(self)
		self.handle = grp.CreateBigTextBar(width, height, fontSize)


class BigBoard(ui.Bar):

	SCROLL_WAIT_TIME = 5.0
	TIP_DURATION = 10.0
	FONT_WIDTH	= 18
	FONT_HEIGHT	= 18
	LINE_WIDTH  = 500
	LINE_HEIGHT	= FONT_HEIGHT + 5
	STEP_HEIGHT = LINE_HEIGHT * 2
	LINE_CHANGE_LIMIT_WIDTH = 350

	FRAME_IMAGE_FILE_NAME_LIST = [
		"season1/interface/oxevent/frame_0.sub",
		"season1/interface/oxevent/frame_1.sub",
		"season1/interface/oxevent/frame_2.sub",
	]

	FRAME_IMAGE_STEP = 256

	FRAME_BASE_X = -20
	FRAME_BASE_Y = -12

	def __init__(self):
		ui.Bar.__init__(self)

		self.AddFlag("not_pick")
		self.tipList = []
		self.curPos = 0
		self.dstPos = 0
		self.nextScrollTime = 0

		self.SetPosition(0, 150)
		self.SetSize(512, 55)
		self.SetColor(grp.GenerateColor(0.0, 0.0, 0.0, 0.5))
		self.SetWindowHorizontalAlignCenter()

		self.__CreateTextBar()
		self.__LoadFrameImages()


	def __LoadFrameImages(self):
		x = self.FRAME_BASE_X
		y = self.FRAME_BASE_Y
		self.imgList = []
		for imgFileName in self.FRAME_IMAGE_FILE_NAME_LIST:
			self.imgList.append(self.__LoadImage(x, y, imgFileName))
			x += self.FRAME_IMAGE_STEP

	def __LoadImage(self, x, y, fileName):
		img = ui.ImageBox()
		img.SetParent(self)
		img.AddFlag("not_pick")
		img.LoadImage(fileName)
		img.SetPosition(x, y)
		img.Show()
		return img

	def __del__(self):
		ui.Bar.__del__(self)

	def Destroy(self):
		self.Hide()

		ui.Bar.Destroy(self)
	def __CreateTextBar(self):

		x, y = self.GetGlobalPosition()

		self.textBar = BigTextBar(self.LINE_WIDTH, 300, self.FONT_HEIGHT)
		self.textBar.SetParent(self)
		self.textBar.SetPosition(6, 8)
		self.textBar.SetTextColor(242, 231, 193)
		self.textBar.SetClipRect(0, y+8, wndMgr.GetScreenWidth(), y+8+self.STEP_HEIGHT)
		self.textBar.Show()

	def __CleanOldTip(self):
		curTime = app.GetTime()
		leaveList = []
		for madeTime, text in self.tipList:
			if curTime + self.TIP_DURATION <= madeTime:
				leaveList.append(text)

		self.tipList = leaveList

		if not leaveList:
			self.textBar.ClearBar()
			self.Hide()
			return

		self.__RefreshBoard()

	def __RefreshBoard(self):

		self.textBar.ClearBar()

		if len(self.tipList) == 1:
			checkTime, text = self.tipList[0]
			(text_width, text_height) = self.textBar.GetTextExtent(text)
			self.textBar.TextOut((500-text_width)/2, (self.STEP_HEIGHT-8-text_height)/2, text)

		else:
			index = 0
			for checkTime, text in self.tipList:
				(text_width, text_height) = self.textBar.GetTextExtent(text)
				self.textBar.TextOut((500-text_width)/2, index*self.LINE_HEIGHT, text)
				index += 1

	def SetTip(self, text):

		if not app.IsVisibleNotice():
			return

		curTime = app.GetTime()
		self.__AppendText(curTime, text)
		self.__RefreshBoard()

		self.nextScrollTime = curTime + 1.0

		if not self.IsShow():
			self.curPos = -self.STEP_HEIGHT
			self.dstPos = -self.STEP_HEIGHT
			self.textBar.SetPosition(3, 8 - self.curPos)
			self.Show()

	def __AppendText(self, curTime, text):
		import dbg
		prevPos = 0
		while 1:
			curPos = text.find(" ", prevPos)
			if curPos < 0:
				break

			(text_width, text_height) = self.textBar.GetTextExtent(text[:curPos])
			if text_width > self.LINE_CHANGE_LIMIT_WIDTH:
				self.tipList.append((curTime, text[:prevPos]))
				self.tipList.append((curTime, text[prevPos:]))
				return

			prevPos = curPos + 1

		self.tipList.append((curTime, text))

	def OnUpdate(self):

		if not self.tipList:
			self.Hide()
			return

		if app.GetTime() > self.nextScrollTime:
			self.nextScrollTime = app.GetTime() + self.SCROLL_WAIT_TIME

			self.dstPos = self.curPos + self.STEP_HEIGHT

		if self.dstPos > self.curPos:
			self.curPos += 1
			self.textBar.SetPosition(3, 8 - self.curPos)

			if self.curPos > len(self.tipList)*self.LINE_HEIGHT:
				self.curPos = -self.STEP_HEIGHT
				self.dstPos = -self.STEP_HEIGHT

				self.__CleanOldTip()

if gcGetEnable("ENABLE_LEFT_POPUP"):
	class LeftTipBoard(ui.ScriptWindow):
		PAGE_BASE_POS = (-169, 240)
		PAGE_SIZE = (169, 35)
		WAIT_TIME = 4

		def __init__(self):
			def IntializeWindow():
				self.AddFlag("not_pick")
				self.SetSize(*self.PAGE_SIZE)
				self.SetWindowVerticalAlignBottom()
				self.SetPosition(*self.PAGE_BASE_POS)
				self.Hide()

			ui.ScriptWindow.__init__(self, "UI_BOTTOM")
			IntializeWindow()

			self.__Initialize()
			self.__InitializeObjects()

		def __Initialize(self):
			self.textLine = None
			self.window_bg = None

			self.wndWidth = self.GetWidth()

			self.isActiveSlide = False
			self.isActiveSlideOut = False
			self.endTime = 0

			self.actual_text = ""
			self.tipCache = []

		def __InitializeObjects(self):
			self.window_bg = ui.ImageBox()
			self.window_bg.SetParent(self)
			self.window_bg.LoadImage("assets/ui/tips/base_tip.tga")
			self.window_bg.Show()

			x, y = self.GetGlobalPosition()
			self.textLine = TextBar(370, 300)
			self.textLine.SetParent(self.window_bg)
			self.textLine.SetTextColor(*(255,204,153))
			self.textLine.SetWindowVerticalAlignCenter()
			self.textLine.SetPosition(10, -2)
			self.textLine.SetClipRect(0, y, 165, y+35)
			self.textLine.Hide()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def Destroy(self):
			self.Close()

		def SetTip(self, *args):
			if self.IsShow():
				(base_text, type) = args
				if type == "FRIEND" and base_text == player.GetMainCharacterName():
					return

				self.tipCache.append((base_text, type))
				return

			self.textLine.ClearBar()

			if self.LoadTip(*args) is False:
				return

			self.tipCache = []
			self.Show()

			self.isActiveSlide = True
			self.endTime = app.GetGlobalTimeStamp() + self.WAIT_TIME

		def LoadTip(self, base_text, type):
			m_type = {
				"FRIEND" : "Gracz {} zalogowa³ siê.",
				"SHOP" : "{}",
				"STUFF" : "{}",
				"TEAM" : "Administrator {} zalogowa³ siê",
			}

			if not m_type.has_key(type):	return False
			if type == "FRIEND" and base_text == player.GetMainCharacterName():
				return False

			self.actual_text = m_type[type].format(str(base_text))
			self.textLine.TextOut(0, -2, self.actual_text)
			self.SetPosition(*self.PAGE_BASE_POS)
			return True

		def Close(self):
			self.Hide()

		def OnUpdate(self):
			# if (self.isActiveSlide is True or self.isActiveSlideOut is True or\
			# 	len(self.tipCache) != 0 or self.IsShow()):
			# 	self.isActiveSlide = False
			# 	self.isActiveSlideOut = False
			# 	self.tipCache = []
			# 	self.textLine.ClearBar()
			# 	self.Close()
			# 	return

			if self.endTime - app.GetGlobalTimeStamp() <= 0 and self.isActiveSlideOut == False and self.isActiveSlide == True:
				self.isActiveSlide = False
				self.isActiveSlideOut = True
				self.textLine.Hide()

			if self.isActiveSlide and self.isActiveSlide == True:
				x, y = self.GetLocalPosition()
				if x < 0:	self.SetPosition(min(0, x + 4), y)
				else:
					(text_width, text_height) = self.textLine.GetTextExtent(self.actual_text)

					if not self.textLine.IsShow():
						self.textLine.SetPosition(-text_width, -2)
						self.textLine.Show()

					x, y = self.textLine.GetLocalPosition()
					if x <= -text_width:
						self.textLine.SetPosition(self.wndWidth, y)
					else:
						self.textLine.SetPosition(x - 1, y)

			elif self.isActiveSlideOut and self.isActiveSlideOut == True:
				x, y = self.GetLocalPosition()
				if x > -(self.wndWidth):
					self.SetPosition(x - 4, y)
				elif x <= -(self.wndWidth):
					self.isActiveSlideOut = False
					if len(self.tipCache) != 0:
						self.LoadNextTip()
					else:
						self.Close()

		def LoadNextTip(self):
			self.textLine.ClearBar()
			self.LoadTip(*self.tipCache[0])
			del self.tipCache[0]
			self.isActiveSlide = True
			self.endTime = app.GetGlobalTimeStamp() + self.WAIT_TIME
