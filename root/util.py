"""Util - DOCUMENTATION

This file was created for the purpose of maintaining one fixed in-game design.
All common design class's and methods need to bere, do that and we can
control all in game aspect, only changing the content inside this module.

This file has to be imported as a module and contains the following class's:
	* ReworkedScrollBar - create our scrollbar instead default UI module scrollbar
	* SimpleTextLoader - create one simple text loader for load all our text files
	* RadioButton - create one radio button based in expanded image class
	
	brief:
		::All this class's can be called like UI class's, you dont necessary need to use
			the methods that will be talked about below;

Also contain some methods that interact with the reference classes above:
	* MakeSimpleTextLoader:
		brief:
			::Usually this method is used to load several loaders in a loop, e.g:
				-----------------------
				for args in [
					[ control_variable, peekWindow size, parent, position (tuple), file for load or None],
				]:
					if (not utils.MakeSimpleTextLoader(self, *args)):
						import exception
						exception.Abort("!!exception!!")
				-----------------------
			::It is necessary a method present in the class that calls this method called BindLoaderObject, e.g:
				-----------------------
				def BindLoaderObject(self, idx, obj):
					dLoaders = {control_variable : variable_name, (...)}
					if idx not in dLoaders:
						return False
					
					setattr(self, dLoaders[idx], obj)
					return True
				-----------------------
				
				::The argument idx its the control_variable in dLoaders dictionary and variable_name its the variable\
					you want to assign the object, e.g:
						
						-> variable who gonna save the loader: self.myLoader
						-> control value for this variable: 1
						
						dLoaders = {1 : "myLoader"}
		args:
			::mainWnd -> main class where you call the method;
			::idx -> controls the variable that goes bind by created object;
			::size -> size of SimpleTextLoader peekWindow;
			::parent -> parent of created object;
			::pos -> position from created object in parent window;
			::loadFileName (None) -> this argument have None as default value, but you can use them sending\
										the file who loader gonna load;

Other methods available:
	* GetRandomCharBasedInItem:
		brief:
			::Usually this method is used to get one race that can use the item that was sent as an argument;
		
		args:
			::itemVnum -> the id of the item we want to get a race that can use it;
"""

import grp, ui, pack, localeInfo, math, wndMgr, dbg,\
 item, player, app

def IsInventorySlotType(slotType):
	return slotType == player.SLOT_TYPE_INVENTORY

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
			self.middle.SetColor(0xFF5f5f5f)
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

class RadioButton(ui.ScriptWindow):
	def __init__(self):
		super(RadioButton, self).__init__()
		
		self.__Initialize()
		self.__BuildPage()
	
	def __del__(self):
		super(RadioButton, self).__del__()
	
		#Private Methods
	def __Initialize(self):
		self.loadedWindow = False
		
		self.base_board = None
		self.invStagesWindow = None
		
		self.buttonState = 0
		self.button_images = []
	
	def __BuildPage(self):
		if self.loadedWindow is True:
			return
		
		self.base_board = ui.ExpandedImageBox()
		self.base_board.SetParent(self)
		self.base_board.SetPosition(0, 0)
		self.base_board.Show()
		
		self.invStagesWindow = ui.Window()
		self.invStagesWindow.SetParent(self)
		self.invStagesWindow.SetPosition(0, 0)
		self.invStagesWindow.SetOverInEvent(ui.__mem_func__(self.OnHover))
		self.invStagesWindow.SetOverOutEvent(ui.__mem_func__(self.OnUp))
		self.invStagesWindow.SetMouseLeftButtonDownEvent(ui.__mem_func__(self.OnDown))
		self.invStagesWindow.Show()
		
		self.loadedWindow = True
	
	def __ReloadButtonSize(self):
		self.SetSize(self.base_board.GetWidth(), self.base_board.GetHeight())
		self.invStagesWindow.SetSize(self.base_board.GetWidth(), self.base_board.GetHeight())
	
		#Public Methods
	def SetButtonVisual(self, images):
		if not isinstance(images, list):
			return
		
		if len(images) != 3:
			return
		
		self.button_images = images
		self.base_board.LoadImage(self.button_images[self.buttonState])
		self.__ReloadButtonSize()
	
	def SAFE_SetClickEvent(self, event, *args):
		self.clickEvent = (ui.__mem_func__(event), args)
	
	def OnUp(self, forceEvent = False):
		if forceEvent is False:
			if not self.base_board or\
				self.buttonState == 2:
				return
		
		self.buttonState = 0
		self.base_board.LoadImage(self.button_images[self.buttonState])
	
	def OnHover(self):
		if not self.base_board or\
			self.buttonState == 2:
			return
		
		self.buttonState = 1
		self.base_board.LoadImage(self.button_images[self.buttonState])
	
	def OnDown(self, runEvent = True):
		if not self.base_board or\
			self.buttonState == 2:
			return
		
		self.buttonState = 2
		self.base_board.LoadImage(self.button_images[self.buttonState])
		
		if runEvent is True:
			if self.clickEvent:
				apply(*self.clickEvent)
	
	def Show(self):
		super(RadioButton, self).Show()
	
	def Hide(self):
		super(RadioButton, self).Hide()

class Button(ui.ScriptWindow):
	DEFAULT_BUTTON_STATE = 0
	HOVER_BUTTON_STATE = 1
	DOWN_BUTTON_STATE = 2
	
	def __init__(self):
		super(Button, self).__init__()
		
		self.__Initialize()
		self.__BuildPage()
	
	def __del__(self):
		super(Button, self).__del__()
	
		#Private Methods
	def __Initialize(self):
		self.loadedWindow = False
		
		self.buttonTextInfo = None
		self.base_board = None
		self.invStagesWindow = None
		
		self.last_button_state = self.DEFAULT_BUTTON_STATE
		self.button_images = []
	
	def __BuildPage(self):
		if self.loadedWindow is True:
			return
		
		self.base_board = ui.ExpandedImageBox()
		self.base_board.SetParent(self)
		self.base_board.SetPosition(0, 0)
		self.base_board.Show()
		
		self.invStagesWindow = ui.Window()
		self.invStagesWindow.SetParent(self)
		self.invStagesWindow.SetPosition(0, 0)
		self.invStagesWindow.SetOverInEvent(ui.__mem_func__(self.OnHover))
		self.invStagesWindow.SetOverOutEvent(ui.__mem_func__(self.OnUp))
		self.invStagesWindow.SetMouseLeftButtonDownEvent(ui.__mem_func__(self.OnDown))
		self.invStagesWindow.SetOnMouseLeftButtonUpEvent(ui.__mem_func__(self.OnUpAfterDown))
		self.invStagesWindow.Show()
		
		self.loadedWindow = True
	
	def __ReloadButtonSize(self):
		self.SetSize(self.base_board.GetWidth(), self.base_board.GetHeight())
		self.invStagesWindow.SetSize(self.base_board.GetWidth(), self.base_board.GetHeight())
	
		#Public Methods
	def CreateTextLine(self, text, x, y, config = []):
		if self.buttonTextInfo:
			return
		
		self.buttonTextInfo = ui.TextLine()
		self.buttonTextInfo.SetParent(self.base_board)
		self.buttonTextInfo.SetPosition(x, y)
		self.buttonTextInfo.SetText(text)
		
		c_dic = {
			"text_horizontal_align_center" : self.buttonTextInfo.SetHorizontalAlignCenter,
			"text_horizontal_align_right" : self.buttonTextInfo.SetHorizontalAlignRight,
			"text_horizontal_align_left" : self.buttonTextInfo.SetHorizontalAlignLeft,
			
			"text_vertical_align_center" : self.buttonTextInfo.SetVerticalAlignCenter,
			"text_vertical_align_top" : self.buttonTextInfo.SetVerticalAlignTop,
			"text_vertical_align_bottom" : self.buttonTextInfo.SetVerticalAlignBottom,
			
			"window_horizontal_align_center" : self.buttonTextInfo.SetWindowHorizontalAlignCenter,
			"window_horizontal_align_right" : self.buttonTextInfo.SetWindowHorizontalAlignRight,
			"window_horizontal_align_left" : self.buttonTextInfo.SetWindowHorizontalAlignLeft,
			
			"window_vertical_align_center" : self.buttonTextInfo.SetWindowVerticalAlignCenter,
			"window_vertical_align_top" : self.buttonTextInfo.SetWindowVerticalAlignTop,
			"window_vertical_align_bottom" : self.buttonTextInfo.SetWindowVerticalAlignBottom,
			
			"refact_text_horizontal_align_right" : [self.buttonTextInfo.SetPosition, (self.base_board.GetWidth() - self.buttonTextInfo.GetTextSize()[0] - x, y)],
		}
		
		for flag in config:
			if flag in c_dic.keys():
				if (isinstance(c_dic[flag], list)):
					c_dic[flag][0](*c_dic[flag][1])
				else:
					c_dic[flag]()
		
		self.buttonTextInfo.Show()
	
	def SetButtonVisual(self, images):
		if not isinstance(images, list):
			return
		
		if len(images) != 3:
			return
		
		self.button_images = images
		self.base_board.LoadImage(self.button_images[self.last_button_state])
		self.__ReloadButtonSize()
	
	def SAFE_SetClickEvent(self, event, *args):
		self.clickEvent = (ui.__mem_func__(event), args)
	
	def OnUp(self):
		if self.base_board:
			self.last_button_state = self.DEFAULT_BUTTON_STATE
			self.base_board.LoadImage(self.button_images[self.last_button_state])
	
	def OnHover(self):
		if self.base_board:
			self.last_button_state = self.HOVER_BUTTON_STATE
			self.base_board.LoadImage(self.button_images[self.last_button_state])
	
	def OnDown(self):
		if self.base_board:
			self.last_button_state = self.DOWN_BUTTON_STATE
			self.base_board.LoadImage(self.button_images[self.last_button_state])
	
	def OnUpAfterDown(self):
		if self.invStagesWindow and self.invStagesWindow.IsIn():
			if self.base_board:
				self.OnUp()
				if self.clickEvent:
					apply(*self.clickEvent)
	
	def OnUpdate(self):
		if (self.invStagesWindow and not self.invStagesWindow.IsIn()) and self.last_button_state != self.DEFAULT_BUTTON_STATE:
			self.OnUp()
	
	def Show(self):
		super(Button, self).Show()
	
	def Hide(self):
		super(Button, self).Hide()

def MakeSimpleTextLoader(mainWnd, idx, size, parent, pos, loadFileName = None):
	if not mainWnd:
		return False
	
	obj = SimpleTextLoader(size)
	obj.SetParent(parent)
	obj.AddFlag("attach")
	obj.SetPosition(*pos)
	obj.Show()
	
	if loadFileName:
		obj.LoadFile(loadFileName)
	
	return mainWnd.BindLoaderObject(idx, obj)

def GetRandomCharBasedInItem(itemVnum):
	item.SelectItem(itemVnum)
	
	ASSASSINS 		= [ player.MAIN_RACE_ASSASSIN_W, player.MAIN_RACE_ASSASSIN_M ]
	WARRIORS 		= [ player.MAIN_RACE_WARRIOR_W, player.MAIN_RACE_WARRIOR_M ]
	SURAS 			= [ player.MAIN_RACE_SURA_W, player.MAIN_RACE_SURA_M ]
	SHAMANS 		= [ player.MAIN_RACE_SHAMAN_W, player.MAIN_RACE_SHAMAN_M ]
	ITEM_CHARACTERS = [ ASSASSINS, WARRIORS, SURAS, SHAMANS ]
	
	SEX_FEMALE		= 0
	SEX_MALE		= 1
	ITEM_SEX		= [ SEX_FEMALE, SEX_MALE ]
	
	if item.IsAntiFlag( item.ITEM_ANTIFLAG_MALE ):
		ITEM_SEX.remove( SEX_MALE )
	if item.IsAntiFlag( item.ITEM_ANTIFLAG_FEMALE ):
		ITEM_SEX.remove( SEX_FEMALE )
	if item.IsAntiFlag( item.ITEM_ANTIFLAG_WARRIOR ):
		ITEM_CHARACTERS.remove( WARRIORS )
	if item.IsAntiFlag( item.ITEM_ANTIFLAG_SURA ):
		ITEM_CHARACTERS.remove( SURAS )
	if item.IsAntiFlag( item.ITEM_ANTIFLAG_ASSASSIN ):
		ITEM_CHARACTERS.remove( ASSASSINS )
	if item.IsAntiFlag( item.ITEM_ANTIFLAG_SHAMAN ):
		ITEM_CHARACTERS.remove( SHAMANS )
	
	return ITEM_CHARACTERS[app.GetRandom(0, len(ITEM_CHARACTERS) - 1)][ITEM_SEX[app.GetRandom(0, len(ITEM_SEX) - 1)]]

def IntegerToRoman(num):
	val = [
		1000, 900, 500, 400,
		100, 90, 50, 40,
		10, 9, 5, 4,
		1
	]

	syb = [
		"M", "CM", "D", "CD",
		"C", "XC", "L", "XL",
		"X", "IX", "V", "IV",
		"I"
	]

	roman_num = ""
	i = 0

	while  num > 0:
		for _ in range(num // val[i]):
			roman_num += syb[i]
			num -= val[i]
		i += 1

	return roman_num
