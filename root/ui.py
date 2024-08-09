import app
import ime
import grp
import snd
import wndMgr
import item
import skill
import localeInfo
import dbg
# MARK_BUG_FIX
import guild
# END_OF_MARK_BUG_FIX
import constInfo

import math
import colorsys
import grp
import time

from _weakref import proxy

from ui_event import MakeEvent, Event, MakeCallback

BACKGROUND_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)
DARK_COLOR = grp.GenerateColor(0.2, 0.2, 0.2, 1.0)
BRIGHT_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

DEFAULT_TEXT_COLOR = 0.8549

SELECT_COLOR = grp.GenerateColor(0.0, 0.0, 0.5, 0.3)

WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.5)
HALF_WHITE_COLOR = grp.GenerateColor(1.0, 1.0, 1.0, 0.2)

createToolTipWindowDict = {}
def RegisterCandidateWindowClass(codePage, candidateWindowClass):
	EditLine.candidateWindowClassDict[codePage]=candidateWindowClass
def RegisterToolTipWindow(type, createToolTipWindow):
	createToolTipWindowDict[type]=createToolTipWindow

createMultiToolTipWindowDict = {}
def RegisterMultiToolTipWindow(type, createMultiToolTipWindow):
	createMultiToolTipWindowDict[type] = createMultiToolTipWindow

app.SetDefaultFontName(localeInfo.UI_DEF_FONT)

## Window Manager Event List##
##############################
## "OnMouseLeftButtonDown"
## "OnMouseLeftButtonUp"
## "OnMouseLeftButtonDoubleClick"
## "OnMouseRightButtonDown"
## "OnMouseRightButtonUp"
## "OnMouseRightButtonDoubleClick"
## "OnMouseDrag"
## "OnSetFocus"
## "OnKillFocus"
## "OnMouseOverIn"
## "OnMouseOverOut"
## "OnRender"
## "OnUpdate"
## "OnKeyDown"
## "OnKeyUp"
## "OnTop"
## "OnIMEUpdate" ## IME Only
## "OnIMETab"	## IME Only
## "OnIMEReturn" ## IME Only
##############################
## Window Manager Event List##


class __mem_func__:
	class __noarg_call__:
		def __init__(self, cls, obj, func):
			self.cls=cls
			self.obj=proxy(obj)
			self.func=proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj)

	class __arg_call__:
		def __init__(self, cls, obj, func):
			self.cls=cls
			self.obj=proxy(obj)
			self.func=proxy(func)

		def __call__(self, *arg):
			return self.func(self.obj, *arg)

	def __init__(self, mfunc):
		if mfunc.im_func.func_code.co_argcount>1:
			self.call=__mem_func__.__arg_call__(mfunc.im_class, mfunc.im_self, mfunc.im_func)
		else:
			self.call=__mem_func__.__noarg_call__(mfunc.im_class, mfunc.im_self, mfunc.im_func)

	def __call__(self, *arg):
		return self.call(*arg)

class Window(object):
	def SetClickEvent(self, event):
		self.clickEvent = __mem_func__(event)

	def OnMouseLeftButtonDown(self):
		if self.clickEvent:
			self.clickEvent()

	def NoneMethod(cls):
		pass

	NoneMethod = classmethod(NoneMethod)

	def __init__(self, layer = "UI"):
		self.clickEvent = None
		self.hWnd = None
		self.parentWindow = 0

		self.moveWindowEvent = None

		self.mouseLeftButtonDownEvent = None
		self.mouseLeftButtonDownArgs = None

		self.mouseLeftButtonUpEvent = None
		self.mouseLeftButtonUpArgs = None

		self.mouseRightButtonDownEvent = None
		self.mouseRightButtonDownArgs = None

		self.mouseMoveEvent = None
		self.mouseLeftButtonDoubleClickEvent = None
		self.updateLockedCursorEvent = None

		self.overInEvent = None
		self.overInArgs = None
		self.overOutEvent = None
		self.overOutArgs = None

		self.renderEvent = None
		self.renderArgs = None

		## ScrollBar Wheel Support
		self.scrollPtr = None

		if app.ENABLE_QUEST_RENEWAL:
			self.propertyList = {}

			self.baseX = 0
			self.baseY = 0

		self.RegisterWindow(layer)
		self.Hide()

		self.SetWindowName("NONAME_Window")

	def __del__(self):
		wndMgr.Destroy(self.hWnd)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.Register(self, layer)

	def Destroy(self):
		pass

	def GetWindowHandle(self):
		return self.hWnd

	def AddFlag(self, style):
		wndMgr.AddFlag(self.hWnd, style)

	def RemoveFlag(self, flag):
		wndMgr.RemoveFlag(self.hWnd, flag)

	def IsRTL(self):
		return wndMgr.IsRTL(self.hWnd)

	def SetWindowName(self, Name):
		wndMgr.SetName(self.hWnd, Name)

	def GetWindowName(self):
		return wndMgr.GetName(self.hWnd)

	def SetParent(self, parent):
		wndMgr.SetParent(self.hWnd, parent.hWnd)

	def SetParentProxy(self, parent):
		self.parentWindow=proxy(parent)
		wndMgr.SetParent(self.hWnd, parent.hWnd)

	def GetParentProxy(self):
		return self.parentWindow

	def SetPickAlways(self):
		wndMgr.SetPickAlways(self.hWnd)

	def SetClipRect(self, left, top, right, bottom):
		return wndMgr.SetClipRect(self.hWnd, left, top, right, bottom)

	def SetWindowHorizontalAlignLeft(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_LEFT)

	def SetWindowHorizontalAlignCenter(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_CENTER)

	def SetWindowHorizontalAlignRight(self):
		wndMgr.SetWindowHorizontalAlign(self.hWnd, wndMgr.HORIZONTAL_ALIGN_RIGHT)

	def SetWindowVerticalAlignTop(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_TOP)

	def SetWindowVerticalAlignCenter(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_CENTER)

	def SetWindowVerticalAlignBottom(self):
		wndMgr.SetWindowVerticalAlign(self.hWnd, wndMgr.VERTICAL_ALIGN_BOTTOM)

	def SetTop(self):
		wndMgr.SetTop(self.hWnd)

	def Show(self):
		wndMgr.Show(self.hWnd)

	def Hide(self):
		wndMgr.Hide(self.hWnd)

	if app.__BL_CLIP_MASK__:	
		def SetClippingMaskRect(self, left, top, right, bottom):
			wndMgr.SetClippingMaskRect(self.hWnd, left, top, right, bottom)
			
		def SetClippingMaskWindow(self, clipping_mask_window):
			wndMgr.SetClippingMaskWindow(self.hWnd, clipping_mask_window.hWnd)

	def SetVisible(self, isVisible):
		if isVisible:
			self.Show()
		else:
			self.Hide()

	def Lock(self):
		wndMgr.Lock(self.hWnd)

	def Unlock(self):
		wndMgr.Unlock(self.hWnd)

	def IsShow(self):
		return wndMgr.IsShow(self.hWnd)

	def UpdateRect(self):
		wndMgr.UpdateRect(self.hWnd)

	def SetSize(self, width, height):
		wndMgr.SetWindowSize(self.hWnd, width, height)

	def GetWidth(self):
		return wndMgr.GetWindowWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetWindowHeight(self.hWnd)

	def GetLeft(self):
		x, y = self.GetLocalPosition()
		return x

	def GetGlobalLeft(self):
		x, y = self.GetGlobalPosition()
		return x

	def GetTop(self):
		x, y = self.GetLocalPosition()
		return y

	def GetGlobalTop(self):
		x, y = self.GetGlobalPosition()
		return y

	def GetRight(self):
		return self.GetLeft() + self.GetWidth()

	def GetBottom(self):
		return self.GetTop() + self.GetHeight()

	def GetLocalPosition(self, parent = None):
		if parent:
			(my_x, my_y) = self.GetGlobalPosition()
			(parent_x, parent_y) = parent.GetGlobalPosition()

			return (my_x - parent_x, my_y - parent_y)
		else:
			return wndMgr.GetWindowLocalPosition(self.hWnd)

	def GetGlobalPosition(self):
		return wndMgr.GetWindowGlobalPosition(self.hWnd)

	def GetMouseLocalPosition(self):
		return wndMgr.GetMouseLocalPosition(self.hWnd)

	def GetRect(self):
		return wndMgr.GetWindowRect(self.hWnd)

	def SetPosition(self, x, y):
		wndMgr.SetWindowPosition(self.hWnd, x, y)

	def SetCenterPosition(self, x = 0, y = 0):
		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()) / 2 + x, (wndMgr.GetScreenHeight() - self.GetHeight()) / 2 + y)

	def GetRealWidth(self):
		return self.GetWidth()

	def GetRealHeight(self):
		return self.GetHeight()

	def SetFocus(self):
		wndMgr.SetFocus(self.hWnd)

	def IsFocus(self):
		return wndMgr.IsFocus(self.hWnd)

	def KillFocus(self):
		wndMgr.KillFocus(self.hWnd)

	def GetChildCount(self):
		return wndMgr.GetChildCount(self.hWnd)

	if app.INGAME_WIKI:
		def IsIn(self, checkChilds = False):
			return wndMgr.IsIn(self.hWnd, checkChilds)

		def GetRenderBox(self):
			return wndMgr.GetRenderBox(self.hWnd)

		def SetInsideRender(self, val):
			wndMgr.SetInsideRender(self.hWnd, val)

		def AdjustSize(self):
			x, y = self.GetTextSize()
			wndMgr.SetWindowSize(self.hWnd, x, y)
	else:
		def IsIn(self):
			return wndMgr.IsIn(self.hWnd)
			
	def IsInWindowRect(self):
		return wndMgr.IsInWindowRect(self.hWnd)

	def IsInPosition(self):
		xMouse, yMouse = wndMgr.GetMousePosition()
		x, y = self.GetGlobalPosition()
		return xMouse >= x and xMouse < x + self.GetWidth() and yMouse >= y and yMouse < y + self.GetHeight()

	def SetOnMouseLeftButtonUpEvent(self, event):
		self.mouseLeftButtonUpEvent = event

	def SetMouseMoveEvent(self, event):
		self.mouseMoveEvent = event

	def OnMouseLeftButtonUp(self):
		if self.mouseLeftButtonUpEvent:
			self.mouseLeftButtonUpEvent()

	def OnMouseMove(self):
		if self.mouseMoveEvent:
			self.mouseMoveEvent()

	def SetMouseLeftButtonDownEvent(self, event, *args):
		self.mouseLeftButtonDownEvent = event
		self.mouseLeftButtonDownArgs = args

	def OnMouseLeftButtonDown(self):
		if self.mouseLeftButtonDownEvent:
			apply(self.mouseLeftButtonDownEvent, self.mouseLeftButtonDownArgs)

	def SetMouseLeftButtonDoubleClickEvent(self, event):
		self.mouseLeftButtonDoubleClickEvent = event

	def OnMouseLeftButtonDoubleClick(self):
		if self.mouseLeftButtonDoubleClickEvent:
			self.mouseLeftButtonDoubleClickEvent()

	def SetMouseRightButtonDownEvent(self, event, *args):
		self.mouseRightButtonDownEvent = event
		self.mouseRightButtonDownArgs = args

	def OnMouseRightButtonDown(self):
		if self.mouseRightButtonDownEvent:
			apply(self.mouseRightButtonDownEvent, self.mouseRightButtonDownArgs)

	def SetMoveWindowEvent(self, event):
		self.moveWindowEvent = event

	def OnMoveWindow(self, x, y):
		if self.moveWindowEvent:
			self.moveWindowEvent(x, y)

	def SAFE_SetOverInEvent(self, func, *args):
		self.overInEvent = __mem_func__(func)
		self.overInArgs = args

	def SetOverInEvent(self, func, *args):
		self.overInEvent = func
		self.overInArgs = args

	def SAFE_SetOverOutEvent(self, func, *args):
		self.overOutEvent = __mem_func__(func)
		self.overOutArgs = args

	def SetOverOutEvent(self, func, *args):
		self.overOutEvent = func
		self.overOutArgs = args

	def OnMouseOverIn(self):
		if self.overInEvent:
			apply(self.overInEvent, self.overInArgs)

	def OnMouseOverOut(self):
		if self.overOutEvent:
			apply(self.overOutEvent, self.overOutArgs)

	def SAFE_SetRenderEvent(self, event, *args):
		self.renderEvent = __mem_func__(event)
		self.renderArgs = args

	def ClearRenderEvent(self):
		self.renderEvent = None
		self.renderArgs = None

	def OnRender(self):
		if self.renderEvent:
			apply(self.renderEvent, self.renderArgs)

	def SetLeft(self, x):
		wndMgr.SetWindowPosition(self.hWnd, x, self.GetTop())

	def SavePosition(self):
		self.baseX = self.GetLeft()
		self.baseY = self.GetTop()

	def UpdatePositionByScale(self, scale):
		self.SetPosition(self.baseX * scale, self.baseY * scale)

	if app.ENABLE_QUEST_RENEWAL:
		def SetProperty(self, propName, propValue):
			self.propertyList[propName] = propValue

		def GetProperty(self, propName):
			if propName in self.propertyList:
				return self.propertyList[propName]

			return None

	## ScrollBar Wheel Support
	def	OnScrollWheelEvent(self, iLen):
		if self.scrollPtr:
			return self.scrollPtr(iLen)
		else:
			return False

	def	SetScrollWheelEvent(self, evnt):
		## ScrollBar Wheel Support
		self.scrollPtr = __mem_func__(evnt)

	def LockCursor(self):
		wndMgr.LockCursor(self.hWnd)

	def UnlockCursor(self):
		wndMgr.UnlockCursor(self.hWnd)

	def SetUpdateLockedCursorEvent(self, event):
		self.updateLockedCursorEvent = event

	def OnUpdateLockedCursor(self, xdif, ydif):
		if self.updateLockedCursorEvent:
			self.updateLockedCursorEvent(xdif, ydif)

class CheckBox(Window):

	STATE_UNSELECTED = 0
	STATE_SELECTED = 1

	def __init__(self, layer = "UI", sPath = "assets/ui/checkbox/checkbox_{}", sUnselected = "unselected.png", sSelected = "selected.png"):
		Window.__init__(self, layer)

		self.state = self.STATE_UNSELECTED
		self.eventFunc = None
		self.eventArgs = None

		self.overIn = ""

		self.btnBox = {
			self.STATE_UNSELECTED : self.__init_MakeButton(sPath.format(sUnselected)),
			self.STATE_SELECTED : self.__init_MakeButton(sPath.format(sSelected)),
		}

		text = TextLine()
		text.SetParent(self)
		text.SetWindowVerticalAlignCenter()
		text.SetVerticalAlignCenter()
		text.Show()
		self.text = text

		self.__Refresh()

		self.SetWindowName("NONAME_CheckBox")

	def __del__(self):
		Window.__del__(self)

	def LoadResources(self, sPath = "assets/ui/checkbox/checkbox_{}", sUnselected = "unselected.png", sSelected = "selected.png"):
		self.btnBox = {
			self.STATE_UNSELECTED : self.__init_MakeButton(sPath.format(sUnselected)),
			self.STATE_SELECTED : self.__init_MakeButton(sPath.format(sSelected)),
		}

		self.__Refresh()

	def __ConvertPath(self, path, subStr):
		if path.find("%s") != -1:
			return path % subStr
		else:
			return path

	def __init_MakeButton(self, path, disablePath = None):
		btn = Button()
		btn.SetParent(self)
		btn.SetWindowVerticalAlignCenter()
		btn.SetUpVisual(self.__ConvertPath(path, "01"))
		btn.SetOverVisual(self.__ConvertPath(path, "02"))
		btn.SetDownVisual(self.__ConvertPath(path, "03"))
		if disablePath:
			btn.SetDisableVisual(disablePath)
		else:
			btn.SetDisableVisual(self.__ConvertPath(path, "01"))
		btn.SAFE_SetEvent(self.OnClickButton)
		btn.baseWidth = btn.GetWidth()
		return btn

	def __UpdateRect(self):
		if self.text.GetText():
			width = self.btnBox[self.state].baseWidth + 5 + self.text.GetTextWidth()
		else:
			width = self.btnBox[self.state].baseWidth
		height = max(self.btnBox[self.state].GetHeight(), self.text.GetTextHeight())
		self.SetSize(width, height)

		self.btnBox[self.state].SetSize(width, self.btnBox[self.state].GetHeight())
		self.text.SetPosition(self.btnBox[self.state].baseWidth + 5, 0)

		self.text.UpdateRect()
		self.btnBox[self.state].UpdateRect()
		self.UpdateRect()

	def SetOverEvent(self, func, *args):
		for btn in self.btnBox.values():
			btn.SetOverEvent(func)

	def SetOverOutEvent(self, func, *args):
		for btn in self.btnBox.values():
			btn.SetOverOutEvent(func)

	def __Refresh(self):
		self.__UpdateRect()

		self.btnBox[self.STATE_UNSELECTED].SetVisible(self.state == self.STATE_UNSELECTED)
		self.btnBox[self.STATE_SELECTED].SetVisible(self.state == self.STATE_SELECTED)

	def SAFE_SetOverInData(self, data):
		self.btnBox[self.state].SetToolTipText(data)

	def OnClickButton(self):
		if self.state == self.STATE_UNSELECTED:
			self.state = self.STATE_SELECTED
		else:
			self.state = self.STATE_UNSELECTED

		self.__Refresh()

		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)

	def SetChecked(self, state):
		self.state = state
		self.__Refresh()

	def IsChecked(self):
		return self.state != self.STATE_UNSELECTED

	def SetText(self, text):
		self.text.SetText(text)
		self.__UpdateRect()

	def SetTextColor(self, color):
		self.text.SetPackedFontColor(color)

	def SetEvent(self, event, *args):
		self.eventFunc = event
		self.eventArgs = args

	def SAFE_SetEvent(self, event, *args):
		self.eventFunc = __mem_func__(event)
		self.eventArgs = args

	def Disable(self):
		self.btnBox[self.STATE_UNSELECTED].Disable()
		self.btnBox[self.STATE_SELECTED].Disable()

	def Enable(self):
		self.btnBox[self.STATE_UNSELECTED].Enable()
		self.btnBox[self.STATE_SELECTED].Enable()

class ListBoxEx(Window):
	class Item(Window):
		def __init__(self):
			Window.__init__(self)

			self.SetWindowName("NONAME_ListBoxEx_Item")

		def __del__(self):
			Window.__del__(self)

		def SetParent(self, parent):
			Window.SetParent(self, parent)
			self.parent=proxy(parent)

		def OnMouseLeftButtonDown(self):
			self.parent.SelectItem(self)

		def OnRender(self):
			if self.parent.GetSelectedItem()==self:
				self.OnSelectedRender()

		def OnSelectedRender(self):
			x, y = self.GetGlobalPosition()
			grp.SetColor(grp.GenerateColor(0.0, 0.0, 0.7, 0.7))
			grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())

	def __init__(self):
		Window.__init__(self)

		self.viewItemCount=10
		self.basePos=0
		self.itemHeight=16
		self.itemStep=20
		self.selItem=0
		self.selItemIdx=0
		self.itemList=[]
		self.onSelectItemEvent = lambda *arg: None

		self.itemWidth=100

		self.scrollBar=None
		self.UpdateSize()

		self.SetWindowName("NONAME_ListBoxEx")

	def __del__(self):
		Window.__del__(self)

	def UpdateSize(self):
		height=self.itemStep*self.__GetViewItemCount()

		self.SetSize(self.itemWidth, height)

	def IsEmpty(self):
		if len(self.itemList)==0:
			return 1
		return 0

	def SetItemStep(self, itemStep):
		self.itemStep=itemStep
		self.UpdateSize()

	def SetItemSize(self, itemWidth, itemHeight):
		self.itemWidth=itemWidth
		self.itemHeight=itemHeight
		self.UpdateSize()

	def GetItemHeight(self):
		return self.itemHeight

	def GetItemWidth(self):
		return self.itemWidth

	def SetViewItemCount(self, viewItemCount):
		self.viewItemCount=viewItemCount
		self.UpdateSize()

	def SetSelectEvent(self, event):
		self.onSelectItemEvent = event

	def SetBasePos(self, basePos):
		for oldItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			oldItem.Hide()

		self.basePos=basePos

		pos=basePos
		for newItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x, y)
			newItem.Show()
			pos+=1

	def GetBasePos(self):
		return self.basePos

	def GetItemIndex(self, argItem):
		return self.itemList.index(argItem)

	def GetSelectedItem(self):
		return self.selItem

	def GetSelectedItemIndex(self):
		return self.selItemIdx

	def SelectIndex(self, index):

		if index >= len(self.itemList) or index < 0:
			self.selItem = None
			self.selItemIdx = None
			return

		try:
			self.selItem=self.itemList[index]
			self.selItemIdx = index
			self.onSelectItemEvent(self.selItem)
		except:
			pass

	def ReplaceItemAtIndex(self, index, item):
		item.SetParent(self)
		item.SetSize(self.itemWidth, self.itemHeight)

		if self.__IsInViewRange(index):
			(x,y) = self.GetItemViewCoord(index, item.GetWidth())
			item.SetPosition(x, y)
			item.Show()
		else:
			item.Hide()

		self.itemList[index] = item

	def GetItemAtIndex(self, index):
		if index > (len(self.itemList) - 1):
			return None
		return self.itemList[index]

	def SelectItem(self, selItem):
		self.selItem=selItem
		self.selItemIdx=self.GetItemIndex(selItem)
		self.onSelectItemEvent(selItem)

	def RemoveAllItems(self):
		for i in self.itemList:
			if i.IsShow():
				i.Hide()
		self.selItem=None
		del self.itemList[:]
		self.itemList=[]

		if self.scrollBar:
			self.scrollBar.SetPos(0)

	if app.ENABLE_SWITCHBOT:
		def GetItems(self):
			return self.itemList

	def RemoveItem(self, delItem):
		if delItem==self.selItem:
			self.selItem=None
			self.selItemIdx=None

		self.itemList.remove(delItem)

	def AppendItem(self, newItem, isFront = False, update = True, bSorted = False):
		newItem.SetParent(self)
		newItem.SetSize(self.itemWidth, self.itemHeight)


		pos=len(self.itemList)
		if isFront:
			pos = 0

		if update:
			if self.__IsInViewRange(pos):
				(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
				newItem.SetPosition(x, y)
				newItem.Show()
			else:
				newItem.Hide()


		if isFront:
			self.itemList.insert(0, newItem)

			if update:
				for i in xrange(1, len(self.itemList)):
					curItem = self.itemList[i]
					if self.__IsInViewRange(i):
						(x, y)=self.GetItemViewCoord(i, newItem.GetWidth())
						curItem.SetPosition(x, y)
						curItem.Show()
					else:
						curItem.Hide()

		else:
			self.itemList.append(newItem)
			#dbg.TraceError("after append to list update CLAUSE" + str(newItem) +  " isFront %d update %d" % (isFront, update))
		
		if bSorted:
			## Sorting
			self.itemList.sort(key = lambda rItem : rItem.bDone)

			## Refresh
			self.SetBasePos(0)

	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
		self.scrollBar=scrollBar

	def __OnScroll(self):
		self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()))

	def __GetScrollLen(self):
		scrollLen=self.__GetItemCount()-self.__GetViewItemCount()
		if scrollLen<0:
			return 0

		return scrollLen

	def __GetViewItemCount(self):
		return self.viewItemCount

	def __GetItemCount(self):
		return len(self.itemList)

	def GetScrollLen(self):
		return self.__GetScrollLen()

	def GetViewItemCount(self):
		return self.viewItemCount

	def GetItemCount(self):
		return len(self.itemList)

	def GetItemStep(self):
		return self.itemStep

	def GetItemViewCoord(self, pos, itemWidth):
		return (0, (pos-self.basePos)*self.itemStep)

	def __IsInViewRange(self, pos):
		if pos<self.basePos:
			return 0
		if pos>=self.basePos+self.viewItemCount:
			return 0
		return 1

class ListBoxExNew(Window):
	class Item(Window):
		def __init__(self):
			Window.__init__(self)

			self.realWidth = 0
			self.realHeight = 0

			self.removeTop = 0
			self.removeBottom = 0

			self.SetWindowName("NONAME_ListBoxExNew_Item")

		def __del__(self):
			Window.__del__(self)

		def SetParent(self, parent):
			Window.SetParent(self, parent)
			self.parent=proxy(parent)

		def SetSize(self, width, height):
			self.realWidth = width
			self.realHeight = height
			Window.SetSize(self, width, height)

		def SetRemoveTop(self, height):
			self.removeTop = height
			self.RefreshHeight()

		def SetRemoveBottom(self, height):
			self.removeBottom = height
			self.RefreshHeight()

		def SetCurrentHeight(self, height):
			Window.SetSize(self, self.GetWidth(), height)

		def GetCurrentHeight(self):
			return Window.GetHeight(self)

		def ResetCurrentHeight(self):
			self.removeTop = 0
			self.removeBottom = 0
			self.RefreshHeight()

		def RefreshHeight(self):
			self.SetCurrentHeight(self.GetHeight() - self.removeTop - self.removeBottom)

		def GetHeight(self):
			return self.realHeight

	def __init__(self, stepSize, viewSteps):
		Window.__init__(self)

		self.viewItemCount=10
		self.basePos=0
		self.baseIndex=0
		self.maxSteps=0
		self.viewSteps = viewSteps
		self.stepSize = stepSize
		self.itemList=[]

		self.scrollBar=None

		self.SetWindowName("NONAME_ListBoxEx")

	def __del__(self):
		Window.__del__(self)

	def IsEmpty(self):
		if len(self.itemList)==0:
			return 1
		return 0

	def __CheckBasePos(self, pos):
		self.viewItemCount = 0

		start_pos = pos

		height = 0
		while height < self.GetHeight():
			if pos >= len(self.itemList):
				return start_pos == 0
			height += self.itemList[pos].GetHeight()
			pos += 1
			self.viewItemCount += 1
		return height == self.GetHeight()

	def SetBasePos(self, basePos, forceRefresh = TRUE):
		if forceRefresh == FALSE and self.basePos == basePos:
			return

		for oldItem in self.itemList[self.baseIndex:self.baseIndex+self.viewItemCount]:
			oldItem.ResetCurrentHeight()
			oldItem.Hide()

		self.basePos=basePos

		baseIndex = 0
		while basePos > 0:
			basePos -= self.itemList[baseIndex].GetHeight() / self.stepSize
			if basePos < 0:
				self.itemList[baseIndex].SetRemoveTop(self.stepSize * abs(basePos))
				break
			baseIndex += 1
		self.baseIndex = baseIndex

		stepCount = 0
		self.viewItemCount = 0
		while baseIndex < len(self.itemList):
			stepCount += self.itemList[baseIndex].GetCurrentHeight() / self.stepSize
			self.viewItemCount += 1
			if stepCount > self.viewSteps:
				self.itemList[baseIndex].SetRemoveBottom(self.stepSize * (stepCount - self.viewSteps))
				break
			elif stepCount == self.viewSteps:
				break
			baseIndex += 1

		y = 0
		for newItem in self.itemList[self.baseIndex:self.baseIndex+self.viewItemCount]:
			newItem.SetPosition(0, y)
			newItem.Show()
			y += newItem.GetCurrentHeight()

	def GetItemIndex(self, argItem):
		return self.itemList.index(argItem)

	def GetSelectedItem(self):
		return self.selItem

	def GetSelectedItemIndex(self):
		return self.selItemIdx

	def RemoveAllItems(self):
		self.itemList=[]
		self.maxSteps=0

		if self.scrollBar:
			self.scrollBar.SetPos(0)

	def RemoveItem(self, delItem):
		self.maxSteps -= delItem.GetHeight() / self.stepSize
		self.itemList.remove(delItem)

	def AppendItem(self, newItem):
		if newItem.GetHeight() % self.stepSize != 0:
			import dbg
			dbg.TraceError("Invalid AppendItem height %d stepSize %d" % (newItem.GetHeight(), self.stepSize))
			return

		self.maxSteps += newItem.GetHeight() / self.stepSize
		newItem.SetParent(self)
		self.itemList.append(newItem)

	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
		self.scrollBar=scrollBar

	def OnMouseWheel(self, len):
		if not self.IsInPosition() and (not self.scrollBar or not self.scrollBar.IsInPosition()):
			return FALSE

		basePos = max(0, min(self.__GetScrollLen(), self.basePos + len))
		if basePos == self.basePos:
			return TRUE

		pos = basePos / float(self.__GetScrollLen())
		self.scrollBar.SetPos(pos)
		self.SetBasePos(basePos, FALSE)

	def __OnScroll(self):
		self.SetBasePos(int(self.scrollBar.GetPos()*self.__GetScrollLen()), FALSE)

	def __GetScrollLen(self):
		scrollLen=self.maxSteps-self.viewSteps
		if scrollLen<0:
			return 0

		return scrollLen

	def __GetViewItemCount(self):
		return self.viewItemCount

	def __GetItemCount(self):
		return len(self.itemList)

	def GetViewItemCount(self):
		return self.viewItemCount

	def GetItemCount(self):
		return len(self.itemList)

class CandidateListBox(ListBoxEx):

	HORIZONTAL_MODE = 0
	VERTICAL_MODE = 1

	class Item(ListBoxEx.Item):
		def __init__(self, text):
			ListBoxEx.Item.__init__(self)

			self.textBox=TextLine()
			self.textBox.SetParent(self)
			self.textBox.SetText(text)
			self.textBox.Show()

		def __del__(self):
			ListBoxEx.Item.__del__(self)

	def __init__(self, mode = HORIZONTAL_MODE):
		ListBoxEx.__init__(self)
		self.itemWidth=32
		self.itemHeight=32
		self.mode = mode

	def __del__(self):
		ListBoxEx.__del__(self)

	def SetMode(self, mode):
		self.mode = mode

	def AppendItem(self, newItem):
		ListBoxEx.AppendItem(self, newItem)

	def GetItemViewCoord(self, pos):
		if self.mode == self.HORIZONTAL_MODE:
			return ((pos-self.basePos)*self.itemStep, 0)
		elif self.mode == self.VERTICAL_MODE:
			return (0, (pos-self.basePos)*self.itemStep)

class TextLine(Window):
	def __init__(self):
		Window.__init__(self)
		self.max = 0
		self.SetFontName(localeInfo.UI_DEF_FONT)
		self.secretMode = FALSE

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterTextLine(self, layer)

	if app.INGAME_WIKI:
		def GetRenderPos(self):
			return wndMgr.GetRenderPos(self.hWnd)

		def SetFixedRenderPos(self, startPos, endPos):
			wndMgr.SetFixedRenderPos(self.hWnd, startPos, endPos)

	def SetMax(self, max):
		wndMgr.SetMax(self.hWnd, max)

	def SetLimitWidth(self, width):
		wndMgr.SetLimitWidth(self.hWnd, width)

	def SetMultiLine(self):
		wndMgr.SetMultiLine(self.hWnd, True)

	def SetHorizontalAlignArabic(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_ARABIC)

	def SetHorizontalAlignLeft(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_LEFT)

	def SetHorizontalAlignRight(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_RIGHT)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetHorizontalAlign(self.hWnd, wndMgr.TEXT_HORIZONTAL_ALIGN_CENTER)

	def SetVerticalAlignTop(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_TOP)

	def SetVerticalAlignBottom(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_BOTTOM)

	def SetVerticalAlignCenter(self):
		wndMgr.SetVerticalAlign(self.hWnd, wndMgr.TEXT_VERTICAL_ALIGN_CENTER)

	def SetSecret(self, Value=True):
		wndMgr.SetSecret(self.hWnd, Value)
		self.secretMode = Value

	def IsSecret(self):
		return self.secretMode

	def SetOutline(self, Value=True):
		wndMgr.SetOutline(self.hWnd, Value)

	def SetFeather(self, value=True):
		wndMgr.SetFeather(self.hWnd, value)

	def SetFontName(self, fontName):
		wndMgr.SetFontName(self.hWnd, fontName)

	def SetDefaultFontName(self):
		wndMgr.SetFontName(self.hWnd, localeInfo.UI_DEF_FONT)

	def SetFontColor(self, red, green, blue, alpha = 1.0):
		wndMgr.SetFontColor(self.hWnd, red, green, blue)

	def SetPackedFontColor(self, color):
		wndMgr.SetFontColor(self.hWnd, color)

	def SetText(self, text):
		wndMgr.SetText(self.hWnd, text)

	def SetTextColor(self, color):
		self.SetPackedFontColor(color)
		#now
	def GetText(self):
		return wndMgr.GetText(self.hWnd)

	def GetTextSize(self):
		return wndMgr.GetTextSize(self.hWnd)

	def GetTextWidth(self):
		w, h = self.GetTextSize()
		return w

	def GetTextHeight(self):
		w, h = self.GetTextSize()
		return h

	def AdjustSize(self):
		x, y = self.GetTextSize()
		wndMgr.SetWindowSize(self.hWnd, x, y)

	def GetRight(self):
		return self.GetLeft() + self.GetTextWidth()

	def GetBottom(self):
		return self.GetTop() + self.GetTextHeight()

	def GetSpecificTextWidth(self, text):
		return wndMgr.GetSpecificTextWidth(self.hWnd, text)

	def SetCenter(self):
		wndMgr.SetWindowPosition(self.hWnd, self.GetLeft() - self.GetTextWidth()/2, self.GetTop())

	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

class EmptyCandidateWindow(Window):
	def __init__(self):
		Window.__init__(self)

	def __del__(self):
		Window.__init__(self)

	def Load(self):
		pass

	def SetCandidatePosition(self, x, y, textCount):
		pass

	def Clear(self):
		pass

	def Append(self, text):
		pass

	def Refresh(self):
		pass

	def Select(self):
		pass

class EditLine(TextLine):
	candidateWindowClassDict = {}

	CURSOR_BLINK_SPEED = 0.5
	#SELECTED_COLOR = grp.GenerateColor(0.0, 0.47, 0.38, 1.0)
	SELECTED_COLOR = grp.GenerateColor(0.0549, 0.4235, 0.8627, 1.0)

	def __init__(self):
		TextLine.__init__(self)

		self.eventReturn = Window.NoneMethod
		self.eventUpdate = Window.NoneMethod
		self.eventEscape = Window.NoneMethod
		self.eventTab    = Window.NoneMethod
		self.eventUpdateArgs = None
		self.eventReturnArgs = None
		self.eventEscapeArgs = None
		self.eventTabArgs	= None
		self.inputMode = ime.MODE_STRING
		
		self.backgroundText = TextLine()
		self.backgroundText.SetParent(self)
		self.backgroundText.SetPosition(0, 0)
		self.backgroundText.SetPackedFontColor(WHITE_COLOR)
		self.backgroundText.Hide()
		
		self.numberMode = False
		self.useIME = True

		self.eventOnInput = None

		self.bCodePage = False

		self.candidateWindowClass = None
		self.candidateWindow = None
		self.SetCodePage(app.GetDefaultCodePage())

		self.readingWnd = ReadingWnd()
		self.readingWnd.Hide()

		if app.INGAME_WIKI:
			self.eventUpdate = None

			self.overLay = TextLine()
			self.overLay.SetParent(self)
			self.overLay.SetPosition(0, 0)
			self.overLay.SetPackedFontColor(WHITE_COLOR)
			self.overLay.Hide()

		self.editOverlayTextLine = None
		self.editOverlayText = ""

		self.cursorShowTime = -1

		self.selPosRenderInfo = None
		self.selMouseDown = False
		self.eventUpdate = None

		self.onSetFocusEvent = None
		self.onKillFocusEvent = None

		self.eventUpArrow = None
		self.eventDownArrow = None

	def __del__(self):
		TextLine.__del__(self)

		self.eventReturn = Window.NoneMethod
		self.eventUpdate = Window.NoneMethod
		self.eventEscape = Window.NoneMethod
		self.eventTab    = Window.NoneMethod
		self.eventUpdateArgs = None
		self.eventReturnArgs = None
		self.eventEscapeArgs = None
		self.eventTabArgs = None
		self.backgroundText = None

		self.editOverlayTextLine = None

	def SetCodePage(self, codePage):
		candidateWindowClass=EditLine.candidateWindowClassDict.get(codePage, EmptyCandidateWindow)
		self.__SetCandidateClass(candidateWindowClass)

	def __SetCandidateClass(self, candidateWindowClass):
		if self.candidateWindowClass==candidateWindowClass:
			return

		self.candidateWindowClass = candidateWindowClass
		self.candidateWindow = self.candidateWindowClass()
		self.candidateWindow.Load()
		self.candidateWindow.Hide()

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterTextLine(self, layer)

	def SAFE_SetReturnEvent(self, event):
		self.eventReturn = __mem_func__(event)		
		self.eventReturnArgs = args

	def SetReturnEvent(self, event, *args):
		self.eventReturn = event
		self.eventReturnArgs = args

	def SAFE_SetUpdateEvent(self, event, *args):
		self.eventUpdate = __mem_func__(event)		
		self.eventUpdateArgs = args
		
	def SetUpdateEvent(self, event, *args):
		self.eventUpdate = event
		self.eventUpdateArgs = args

	def SetEscapeEvent(self, event, *args):
		self.eventEscape = event
		self.eventEscapeArgs = args

	def SetTabEvent(self, event, *args):
		self.eventTab = event
		self.eventTabArgs = args
		
	def SetBackgroundText(self, text):
		self.backgroundText.SetPosition(0, 0)
		self.backgroundText.SetText(text)
		
		if not self.backgroundText.IsShow():
			self.backgroundText.Show()

	def SetTipText(self, tipText):
		input = self.GetText()
		(widht, height) = self.GetTextSize()

		tip = tipText[len(input):]
		self.backgroundText.SetPosition(widht, 0)
		self.backgroundText.SetText(tip)

		if not self.backgroundText.IsShow():
			self.backgroundText.Show()
		
	def GetBackgroundText(self):
		return self.backgroundText.GetText()

	def SetOnFocusEvent(self, event):
		self.onSetFocusEvent = event

	def SetKillFocusEvent(self, event):
		self.onKillFocusEvent = event

	def SetUpArrowEvent(self, event):
		self.eventUpArrow = event

	def SetDownArrowEvent(self, event):
		self.eventDownArrow = event

	if app.INGAME_WIKI:
		def SetOverlayText(self, text):
			self.overLay.SetText(text)
			self.__RefreshOverlay()

		def GetOverlayText(self):
			return self.overLay.GetText()

		def SetUpdateEvent(self, event):
			self.eventUpdate = event

		def GetDisplayText(self):
			if len(self.GetText()):
				return self.GetText()
			else:
				return self.overLay.GetText()

		def __RefreshOverlay(self):
			if len(self.GetText()):
				self.overLay.Hide()
			else:
				self.overLay.Show()

		def IsShowCursor(self):
			return wndMgr.IsShowCursor(self.hWnd)

	def GetEditOverlayText(self):
		return self.editOverlayText

	def SetEditOverlayText(self, text):
		self.editOverlayText = text

		if text:
			if not self.editOverlayTextLine:
				line = TextLine()
				line.SetParent(self)
				line.SetFontColor(0.5, 0.5, 0.5)
				line.Show()
				self.editOverlayTextLine = line

		if self.editOverlayTextLine:
			curLen = len(self.GetText())
			if len(text) >= curLen and text[:curLen].lower() == self.GetText().lower():
				text = text[curLen:]
				self.editOverlayTextLine.SetPosition(self.GetTextWidth() + 3, 0)
			else:
				self.editOverlayTextLine.SetPosition(0, 0)
			self.editOverlayTextLine.SetText(text)
			self.__RefreshOverlay()

	def SetMax(self, max):
		self.max = max
		wndMgr.SetMax(self.hWnd, self.max)
		ime.SetMax(self.max)
		self.SetUserMax(self.max)

	def SetUserMax(self, max):
		self.userMax = max
		ime.SetUserMax(self.userMax)

	def SetNumberMode(self):
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.inputMode = ime.MODE_NUMBER
		else:
			self.numberMode = True

	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def SetCurrencyMode(self):
			self.inputMode = ime.MODE_CURRENCY

	def SetIMEFlag(self, flag):
		self.useIME = flag

	def SetText(self, text):
		wndMgr.SetText(self.hWnd, text)

		if self.IsFocus():
			ime.SetText(text)

		if app.INGAME_WIKI:
			self.__RefreshOverlay()

		if self.eventUpdate:
			self.eventUpdate()

	def SetOnInputEvent(self, onInputEvent):
		self.eventOnInput = onInputEvent

	def Enable(self):
		wndMgr.ShowCursor(self.hWnd)
		self.__ResetCursorShowTime()

	def Disable(self):
		wndMgr.HideCursor(self.hWnd)

	def SetEndPosition(self):
		ime.MoveEnd()

	def OnSetFocus(self):
		Text = self.GetText()
		ime.SetText(Text)
		ime.SetMax(self.max)
		ime.SetUserMax(self.userMax)
		ime.SetCursorPosition(-1)
		
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.inputMode == ime.MODE_STRING:
				ime.SetStringMode()

			elif self.inputMode == ime.MODE_NUMBER:
				ime.SetNumberMode()

			elif self.inputMode == ime.MODE_CURRENCY:
				ime.SetCurrencyMode()
		else:
			if self.numberMode:
				ime.SetNumberMode()
			else:
				ime.SetStringMode()
				
		ime.EnableCaptureInput()
		if self.useIME:
			ime.EnableIME()
		else:
			ime.DisableIME()

		self.selMouseCursorPos = -1
		self.selMouseDown = FALSE
		self.__ResetCursorShowTime()

		if self.onSetFocusEvent:
			self.onSetFocusEvent()

		# wndMgr.ShowCursor(self.hWnd, True)

	def OnKillFocus(self):
		self.SetText(ime.GetText(self.bCodePage))
		self.OnIMECloseCandidateList()
		self.OnIMECloseReadingWnd()
		ime.DisableIME()
		ime.DisableCaptureInput()
		wndMgr.HideCursor(self.hWnd)

		self.cursorShowTime = -1

		if self.onKillFocusEvent:
			self.onKillFocusEvent()

	def OnIMEChangeCodePage(self):
		self.SetCodePage(ime.GetCodePage())

	def OnIMEOpenCandidateList(self):
		self.candidateWindow.Show()
		self.candidateWindow.Clear()
		self.candidateWindow.Refresh()

		gx, gy = self.GetGlobalPosition()
		self.candidateWindow.SetCandidatePosition(gx, gy, len(self.GetText()))

		return True

	def OnIMECloseCandidateList(self):
		self.candidateWindow.Hide()
		return True

	def OnIMEOpenReadingWnd(self):
		gx, gy = self.GetGlobalPosition()
		textlen = len(self.GetText())-2
		reading = ime.GetReading()
		readinglen = len(reading)
		self.readingWnd.SetReadingPosition( gx + textlen*6-24-readinglen*6, gy )
		self.readingWnd.SetText(reading)
		if ime.GetReadingError() == 0:
			self.readingWnd.SetTextColor(0xffffffff)
		else:
			self.readingWnd.SetTextColor(0xffff0000)
		self.readingWnd.SetSize(readinglen * 6 + 4, 19)
		self.readingWnd.Show()
		return True

	def OnIMECloseReadingWnd(self):
		self.readingWnd.Hide()
		return True

	def OnIMEUpdate(self):
		snd.PlaySound("sound/ui/type.wav")
		TextLine.SetText(self, ime.GetText(self.bCodePage))

		self.__ResetCursorShowTime()

		if app.INGAME_WIKI:
			self.__RefreshOverlay()

		if self.eventUpdate != None:
			if self.eventUpdateArgs:
				apply(self.eventUpdate, self.eventUpdateArgs)
			else:
				self.eventUpdate()

			if self.eventUpdate != Window.NoneMethod:
				return True
		
		return False

	def OnIMETab(self):
		if self.eventTabArgs:
			apply(self.eventTab, self.eventTabArgs)
		else:
			self.eventTab()
			
		if self.eventTab != Window.NoneMethod:
			return True

		return False

	def OnIMEReturn(self):
		snd.PlaySound("sound/ui/click.wav")
		if self.eventReturnArgs:
			apply(self.eventReturn, self.eventReturnArgs)
		else:
			self.eventReturn()

		if self.eventReturn != Window.NoneMethod:
			return True
		
		return False

	def OnPressEscapeKey(self):
		if self.eventEscapeArgs:
			apply(self.eventEscape, self.eventEscapeArgs)
		else:
			self.eventEscape()

		if self.eventEscape != Window.NoneMethod:
			return True
		
		return False

	def OnKeyDown(self, key):
		ctrlPressed = app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL)

		if key in (app.DIK_F1, app.DIK_F2, app.DIK_F3, app.DIK_F4, app.DIK_F5, app.DIK_F6, app.DIK_F7, app.DIK_F8, app.DIK_F9, app.DIK_F10, app.DIK_F11, app.DIK_LALT, app.DIK_SYSRQ, app.DIK_LCONTROL):
			return False

		if ctrlPressed:
			if app.DIK_C == key:
				if not self.IsSecret():
					ime.CopyTextToClipBoard()
				return TRUE
			if app.DIK_X == key:
				if ime.IsTextSelected():
					if not self.IsSecret():
						ime.CopyTextToClipBoard()
						ime.Delete()
						TextLine.SetText(self, ime.GetText(self.bCodePage))
				return TRUE
			if app.DIK_V == key:
				ime.PasteTextFromClipBoard()
				return TRUE
			if app.DIK_A == key:
				ime.MoveHome()
				ime.SetSelectedText()
				ime.MoveEnd()
				return TRUE

		if self.eventOnInput:
			self.eventOnInput(key)

		return TRUE

	def OnKeyUp(self, key):
		if key in (app.DIK_F1, app.DIK_F2, app.DIK_F3, app.DIK_F4, app.DIK_F5, app.DIK_F6, app.DIK_F7, app.DIK_F8, app.DIK_F9, app.DIK_F10, app.DIK_F11, app.DIK_LALT, app.DIK_SYSRQ, app.DIK_LCONTROL):
			return False

		return True

	def OnIMEKeyDown(self, key):
		shiftPressed = app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT)

		# Left
		if app.VK_LEFT == key:
			if shiftPressed:
				if not ime.IsTextSelected():
					ime.SetSelectedText()
			else:
				self.__ResetCursorShowTime()

			ime.MoveLeft(not shiftPressed)
			return TRUE
		# Right
		if app.VK_RIGHT == key:
			if shiftPressed:
				if not ime.IsTextSelected():
					ime.SetSelectedText()
			else:
				self.__ResetCursorShowTime()

			ime.MoveRight(not shiftPressed)
			return TRUE
		# Up
		if app.VK_UP == key:
			if self.eventUpArrow:
				self.eventUpArrow()
				return TRUE
		# Down
		if app.VK_DOWN == key:
			if self.eventDownArrow:
				self.eventDownArrow()
				return TRUE

		# Home
		if app.VK_HOME == key:
			if shiftPressed:
				if not ime.IsTextSelected():
					ime.SetSelectedText()
			else:
				ime.ResetSelectedText()
			ime.MoveHome()
			return TRUE
		# End
		if app.VK_END == key:
			if shiftPressed:
				if not ime.IsTextSelected():
					ime.SetSelectedText()
			else:
				ime.ResetSelectedText()
			ime.MoveEnd()
			return TRUE

		# Delete
		if app.VK_DELETE == key:
			ime.Delete()
			TextLine.SetText(self, ime.GetText(self.bCodePage))
			return TRUE

		return TRUE

	def __GetCursorPosition(self):
		PixelPosition = wndMgr.GetCursorPosition(self.hWnd)
		if PixelPosition < 0 or PixelPosition > len(self.GetText()):
			return len(self.GetText())

		return PixelPosition

	def OnMouseLeftButtonDown(self):
		if FALSE == self.IsIn():
			return FALSE

		self.SetFocus()
		PixelPosition = self.__GetCursorPosition()
		ime.SetCursorPosition(PixelPosition)

		self.selMouseDown = TRUE
		self.selMouseCursorPos = PixelPosition
		ime.SetSelectedText()

	def OnMouseLeftButtonUp(self):
		self.selMouseDown = FALSE
		if not ime.IsTextSelected():
			ime.ResetSelectedText()

	def __ResetCursorShowTime(self):
		self.cursorShowTime = app.GetTime()
		if not ime.IsTextSelected():
			wndMgr.ShowCursor(self.hWnd, TRUE)

	def OnIMEUpdateSelection(self):
		selPosStart, selPosEnd = ime.GetSelectedText()
		self.selPosRenderInfo = None

		if ime.IsTextSelected():
			## remove (item) links from the selection position (because they won't be counted in the GetCharPositionByCursor function, that function takes only the rendered characters into account)
			realSelPosStart = wndMgr.TextPositionToRenderPosition(self.hWnd, selPosStart)
			realSelPosEnd = wndMgr.TextPositionToRenderPosition(self.hWnd, selPosEnd)

			## get render x position for the current text selection
			renderStartX, renderStartY, renderStartLineHeight = wndMgr.GetCharPositionByCursor(self.hWnd, realSelPosStart)
			renderEndX, renderEndY, renderEndLineHeight = wndMgr.GetCharPositionByCursor(self.hWnd, realSelPosEnd)
			renderInfo = []
			if renderStartY == renderEndY:
				renderInfo.append({
					"sx" : renderStartX,
					"sy" : renderStartY,
					"width" : renderEndX - renderStartX,
					"height" : renderStartLineHeight,
				})
			else:
				renderInfo.append({
					"sx" : renderStartX,
					"sy" : renderStartY,
					"width" : self.GetWidth() - renderStartX,
					"height" : renderStartLineHeight,
				})
				if renderEndY - (renderStartY + renderStartLineHeight) > 0:
					renderInfo.append({
						"sx" : 0,
						"sy" : renderStartY + renderStartLineHeight,
						"width" : self.GetWidth(),
						"height" : renderEndY - (renderStartY + renderStartLineHeight),
					})
				renderInfo.append({
					"sx" : 0,
					"sy" : renderEndY,
					"width" : renderEndX,
					"height" : renderEndLineHeight,
				})

			self.selPosRenderInfo = renderInfo

			wndMgr.HideCursor(self.hWnd)

		else:
			self.__ResetCursorShowTime()

	def OnUpdate(self):
		if self.cursorShowTime >= 0:
			if self.selMouseDown:
				PixelPosition = self.__GetCursorPosition()
				if self.selMouseCursorPos != PixelPosition:
					self.selMouseCursorPos = PixelPosition
					ime.SetCursorPosition(PixelPosition)

			if not self.selPosRenderInfo:
				if (app.GetTime() - self.cursorShowTime) % (self.CURSOR_BLINK_SPEED * 2) < self.CURSOR_BLINK_SPEED:
					wndMgr.ShowCursor(self.hWnd, TRUE)
				else:
					wndMgr.HideCursor(self.hWnd)

	def OnRenderSelected(self):
		if self.selPosRenderInfo:
			(x, y) = self.GetGlobalPosition()

			grp.SetColor(self.SELECTED_COLOR)
			for data in self.selPosRenderInfo:
				grp.RenderBar(x + data["sx"], y + data["sy"], data["width"], data["height"])

class MarkBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterMarkBox(self, layer)

	def Load(self):
		wndMgr.MarkBox_Load(self.hWnd)

	def SetScale(self, scale):
		wndMgr.MarkBox_SetScale(self.hWnd, scale)

	def SetIndex(self, guildID):
		MarkID = guild.GuildIDToMarkID(guildID)
		wndMgr.MarkBox_SetImageFilename(self.hWnd, guild.GetMarkImageFilenameByMarkID(MarkID))
		wndMgr.MarkBox_SetIndex(self.hWnd, guild.GetMarkIndexByMarkID(MarkID))

	def SetAlpha(self, alpha):
		wndMgr.MarkBox_SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

class ImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.eventDict={}
		self.argDict={}

		self.eventFunc = {"mouse_click" : None, "mouse_over_in" : None, "mouse_over_out" : None}
		self.eventArgs = {"mouse_click" : None, "mouse_over_in" : None, "mouse_over_out" : None}

		self.ToolTipText = None
		self.eventOverInItem = None
		self.eventOverOutItem = None
		self.a = 1.0

	def __del__(self):
		Window.__del__(self)
		self.eventFunc = None
		self.eventArgs = None

		self.eventOverInItem = None
		self.eventOverOutItem = None

	def GetAlpha(self):
		return self.a

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterImageBox(self, layer)

	def LoadImage(self, imageName):
		self.name=imageName
		wndMgr.LoadImage(self.hWnd, imageName)

		if len(self.eventDict)!=0:
			print "LOAD IMAGE", self, self.eventDict

	if app.INGAME_WIKI:
		def UnloadImage(self):
			wndMgr.UnloadImage(self.hWnd)

	def SetCoolTime(self, time):
		wndMgr.SetCoolTimeImageBox(self.hWnd, time)

	def SetStartCoolTime(self, curPoint, maxPoint):
		curPoint = min(curPoint, maxPoint)
		wndMgr.SetStartCoolTimeImageBox(self.hWnd, (float(curPoint) / float(maxPoint)))

	def GetTexturePtr(self):
		return wndMgr.GetTexturePtr(self.GetHandle())

	def SetAlpha(self, alpha):
		# self.a = alpha
		# wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)
		wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

	def GetWidth(self):
		return wndMgr.GetWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetHeight(self.hWnd)

	if app.INGAME_WIKI:
		def OnMouseOverIn(self):
			self.__OnMouseOverIn()

		def OnMouseOverOut(self):
			self.__OnMouseOverOut()

		def __OnMouseOverIn(self):
			try:
				apply(self.eventDict["MOUSE_OVER_IN"], self.argDict["MOUSE_OVER_IN"])
			except KeyError:
				pass

		def __OnMouseOverOut(self):
			try:
				apply(self.eventDict["MOUSE_OVER_OUT"], self.argDict["MOUSE_OVER_OUT"])
			except KeyError:
				pass

		def OnMouseLeftButtonDown(self):
			if self.eventDict.has_key("MOUSE_LEFT_DOWN"):
				apply(self.eventDict["MOUSE_LEFT_DOWN"], self.argDict["MOUSE_LEFT_DOWN"])
	else:
		def OnMouseOverIn(self):
			try:
				self.eventDict["MOUSE_OVER_IN"]()
			except KeyError:
				pass

		def OnMouseOverOut(self):
			try:
				self.eventDict["MOUSE_OVER_OUT"]()
			except KeyError:
				pass

	def SAFE_SetStringEvent(self, event, func, safe=False):
		if safe:
			self.eventDict[event] = func
		else:
			self.eventDict[event] = __mem_func__(func)

	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])
		if result :
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else :
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

	def OnMouseLeftButtonUp(self):
		try:
			self.eventDict["MOUSE_LEFT_BUTTON_UP"]()
		except KeyError:
			pass

		if self.eventFunc["mouse_click"]:
			apply(self.eventDict["mouse_click"], self.eventArgs["mouse_click"])

	def OnMouseLeftButtonDown(self):
		try:
			self.eventDict["MOUSE_LEFT_BUTTON_DOWN"]()
		except KeyError:
			pass

	def OnMouseRightButtonUp(self):
		try:
			self.eventDict["MOUSE_RIGHT_BUTTON_UP"]()
		except KeyError:
			pass

	def OnMouseRightButtonDown(self):
		try:
			self.eventDict["MOUSE_RIGHT_BUTTON_DOWN"]()
		except KeyError:
			pass

	# def OnMouseOverIn(self):
	# 	if self.eventFunc["mouse_over_in"] :
	# 		apply(self.eventFunc["mouse_over_in"], self.eventArgs["mouse_over_in"])
	# 	else:
	# 		try:
	# 			self.eventDict["MOUSE_OVER_IN"]()
	# 		except KeyError:
	# 			pass

	def SetOnMouseLeftButtonUpEvent(self, event):
		self.eventDict["MOUSE_LEFT_BUTTON_UP"] = event

	def SetOnMouseLeftButtonDownEvent(self, event):
		self.eventDict["MOUSE_RIGHT_BUTTON_DOWN"] = event

	def OnMouseLeftButtonDown(self):
		if self.eventDict.has_key("MOUSE_LEFT_DOWN"):
			apply(self.eventDict["MOUSE_LEFT_DOWN"], self.argDict["MOUSE_LEFT_DOWN"])

	def OnMouseOverOut(self):
		if self.eventFunc["mouse_over_out"]:
			apply(self.eventFunc["mouse_over_out"], self.eventArgs["mouse_over_out"])
		else :
			try:
				self.eventDict["MOUSE_OVER_OUT"]()
			except KeyError:
				pass

	def SetFormToolTipText(self, type, text, x, y):
		if not self.ToolTipText:
			toolTip=createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetHorizontalAlignCenter()
			if app.WJ_MULTI_TEXTLINE:
				toolTip.DisableEnterToken()
				toolTip.SetMultiLine()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			self.ToolTipText=toolTip

		self.ToolTipText.SetText(text)

	def SetToolTipWindow(self, toolTip):
		self.ToolTipText=toolTip
		self.ToolTipText.SetParentProxy(self)

	def SetToolTipText(self, text, x=0, y = 20):
		self.SetFormToolTipText("TEXT", text, x, y)

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()

	def SetOverInItemEvent(self, event):
		self.eventOverInItem = event

	def SetOverOutItemEvent(self, event):
		self.eventOverOutItem = event

	def SetStringEvent(self, event, func, *args):
		self.eventDict[event]=func
		self.argDict[event]=args

class ImageBoxNew(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.eventDict = {}
		self.argsDict = {}

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterExpandedImageBox(self, layer)

	def LoadImage(self, imageName):
		self.name = imageName
		wndMgr.LoadImage(self.hWnd, imageName)

		if len(self.eventDict)!=0:
			print "LOAD IMAGE", self, self.eventDict

	def SetAlpha(self, alpha):
		wndMgr.SetDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

	def SetDiffuseColor(self, r, g, b, a):
		wndMgr.SetDiffuseColor(self.hWnd, r, g, b, a)

	def GetWidth(self):
		return wndMgr.GetWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetHeight(self.hWnd)

	def GetSize(self):
		return self.GetWidth(), self.GetHeight(),

	def OnMouseOverIn(self):
		self.__CallStringEvent("MOUSE_OVER_IN")

	def OnMouseOverOut(self):
		self.__CallStringEvent("MOUSE_OVER_OUT")

	def OnMouseLeftButtonUp(self):
		self.__CallStringEvent("MOUSE_LEFT_BUTTON_UP")

	def OnMouseRightButtonDown(self):
		self.__CallStringEvent("MOUSE_RIGHT_BUTTON_DOWN")

	def OnMouseLeftButtonDown(self):
		self.__CallStringEvent("MOUSE_LEFT_BUTTON_DOWN")

	def __CallStringEvent(self, event):
		if not event in self.eventDict:
			return

		f = self.eventDict[event]
		if event in self.argsDict:
			f(event, self.argsDict[event])
		else:
			f()

	def SAFE_SetStringEvent(self, event, func,isa=False):
		if not isa:
			self.eventDict[event]=__mem_func__(func)
		else:
			self.eventDict[event]=func

	def SetEvent(self, func, event, args = None):
		self.eventDict[event] = func

		if args != None:
			self.argsDict[event] = args

class ExpandedImageBox(ImageBox):
	def __init__(self, layer = "UI"):
		ImageBox.__init__(self, layer)

	def __del__(self):
		ImageBox.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterExpandedImageBox(self, layer)

	def SetScale(self, xScale, yScale):
		wndMgr.SetScale(self.hWnd, xScale, yScale)

	def SetOrigin(self, x, y):
		wndMgr.SetOrigin(self.hWnd, x, y)

	def SetRotation(self, rotation):
		wndMgr.SetRotation(self.hWnd, rotation)

	def SetRenderingMode(self, mode):
		wndMgr.SetRenderingMode(self.hWnd, mode)

	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	def SetPercentage(self, curValue, maxValue):
		if maxValue:
			self.SetRenderingRect(0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)
		else:
			self.SetRenderingRect(0.0, 0.0, 0.0, 0.0)

	def GetWidth(self):
		return wndMgr.GetWindowWidth(self.hWnd)

	def GetHeight(self):
		return wndMgr.GetWindowHeight(self.hWnd)

	def GetSize(self):
		return (self.GetWidth(), self.GetHeight(), )

	# if app.ENABLE_INGAME_WIKI:
	# 	def SetWikiImage(self, bFlag):
	# 		wndMgr.SetWikiImage(self.hWnd, bFlag)

class AniImageBox(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.endFrameEvent = None
		self.endFrameArgs = None

		self.keyFrameEvent = None

		# self.eventFunc = { "mouse_click" : None, "MOUSE_OVER_IN" : None, "MOUSE_OVER_OUT" : None }
		# self.eventArgs = { "mouse_click" : None, "MOUSE_OVER_IN" : None, "MOUSE_OVER_OUT" : None }

	def __del__(self):
		Window.__del__(self)

		self.endFrameEvent = None
		self.endFrameArgs = None

		self.keyFrameEvent = None

		# self.eventFunc = { "mouse_click" : None, "MOUSE_OVER_IN" : None, "MOUSE_OVER_OUT" : None }
		# self.eventArgs = { "mouse_click" : None, "MOUSE_OVER_IN" : None, "MOUSE_OVER_OUT" : None }

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterAniImageBox(self, layer)

	def SetDelay(self, delay):
		wndMgr.SetDelay(self.hWnd, delay)

	def GetDelay(self):
		return wndMgr.GetDelay(self.hWnd)

	def AppendImage(self, filename):
		wndMgr.AppendImage(self.hWnd, filename)

	def SetPercentage(self, curValue, maxValue):
		if maxValue != 0:
			pct = float(curValue) / float(maxValue)
		else:
			pct = 0.0
		self.SetRenderingRect(0.0, 0.0, -1.0 + pct, 0.0)


	# [0.0, 1.0] Valorile trebuie sa fie cuprinse intre 0.0 si 1.0
	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)

	def ResetFrame(self):
		wndMgr.ResetFrame(self.hWnd)

	def SetEndFrameEvent(self, event, *args):
		self.endFrameEvent = event
		self.endFrameArgs = args

	def OnEndFrame(self):
		if self.endFrameEvent:
			apply(self.endFrameEvent, self.endFrameArgs)

	def SetKeyFrameEvent(self, event):
		self.keyFrameEvent = event

	def OnKeyFrame(self, curFrame):
		if self.keyFrameEvent:
			self.keyFrameEvent(curFrame)

	def SetScale(self, xScale, yScale):
		wndMgr.SetAniImgScale(self.hWnd, xScale, yScale)

	def SetPercentageWithScale(self, curValue, maxValue):
		wndMgr.SetRenderingRectWithScale(self.hWnd, 0.0, 0.0, -1.0 + float(curValue) / float(maxValue), 0.0)

	# def SetEvent(self, func, *args) :
	# 	result = self.eventFunc.has_key(args[0])
	# 	if result :
	# 		self.eventFunc[args[0]] = func
	# 		self.eventArgs[args[0]] = args
	# 	else :
	# 		print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

	# def OnMouseLeftButtonUp(self) :
	# 	if self.eventFunc["mouse_click"] :
	# 		apply(self.eventFunc["mouse_click"], self.eventArgs["mouse_click"])

	# def OnMouseOverIn(self) :
	# 	if self.eventFunc["MOUSE_OVER_IN"] :
	# 		apply(self.eventFunc["MOUSE_OVER_IN"], self.eventArgs["MOUSE_OVER_IN"])

	# def OnMouseOverOut(self) :
	# 	if self.eventFunc["MOUSE_OVER_OUT"] :
	# 		apply(self.eventFunc["MOUSE_OVER_OUT"], self.eventArgs["MOUSE_OVER_OUT"])

	def SetMoveAll(self, flag):
		wndMgr.SetMoveAll(self.hWnd, flag)

	def AppendImageScale(self, filename, scale_x, scale_y):
		wndMgr.AppendImageScale(self.hWnd, filename, scale_x, scale_y)

class Button(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		self.TextChild = []

		self.eventFunc = None
		self.eventArgs = None

		self.downEventFunc = None
		self.downEventArgs = None

		self.overFunc = None
		self.overArgs = None

		self.overOutFunc = None
		self.overOutArgs = None

		self.tooltipShowEventFunc = None
		self.tooltipHideEventFunc = None
		
		self.showtooltipevent = None
		self.showtooltiparg = None
		self.hidetooltipevent = None
		self.hidetooltiparg = None

		self.ButtonText = None
		self.ToolTipText = None
		self.tooltipTextColor = None

		self.isEnabled = True

	def __del__(self):
		Window.__del__(self)

		self.eventFunc = None
		self.eventArgs = None

		self.overOutFunc = None
		self.overOutArgs = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterButton(self, layer)

	def SetUpVisual(self, filename):
		wndMgr.SetUpVisual(self.hWnd, filename)

	def SetOverVisual(self, filename):
		wndMgr.SetOverVisual(self.hWnd, filename)

	def SetDownVisual(self, filename):
		wndMgr.SetDownVisual(self.hWnd, filename)

	def SetDisableVisual(self, filename):
		wndMgr.SetDisableVisual(self.hWnd, filename)

	def LoadAllImages(self, filename):
		wndMgr.SetUpVisual(self.hWnd, filename)
		wndMgr.SetOverVisual(self.hWnd, filename)
		wndMgr.SetDownVisual(self.hWnd, filename)
		wndMgr.SetDisableVisual(self.hWnd, filename)

	def GetUpVisualFileName(self):
		return wndMgr.GetUpVisualFileName(self.hWnd)

	def GetOverVisualFileName(self):
		return wndMgr.GetOverVisualFileName(self.hWnd)

	def GetDownVisualFileName(self):
		return wndMgr.GetDownVisualFileName(self.hWnd)

	def __GetNewFileName(self, oldName, oldString, addPath):
		imageName = oldName[:oldName.rfind(oldString + ".")] + str(addPath) + oldName[oldName.rfind("."):]
		return imageName

	def UpdateVisualFileName(self, oldString, addPath):
		self.SetUpVisual(self.__GetNewFileName(self.GetUpVisualFileName(), oldString, addPath))
		self.SetOverVisual(self.__GetNewFileName(self.GetOverVisualFileName(), oldString, addPath))
		self.SetDownVisual(self.__GetNewFileName(self.GetDownVisualFileName(), oldString, addPath))

	def Flash(self):
		wndMgr.Flash(self.hWnd)

	def Enable(self):
		wndMgr.Enable(self.hWnd)
		self.isEnabled = True

	def Disable(self):
		wndMgr.Disable(self.hWnd)
		self.isEnabled = False

	def SetEnabled(self, isEnabled):
		if isEnabled:
			if not self.IsEnabled():
				self.Enable()
		else:
			if self.IsEnabled():
				self.Disable()

	def IsEnabled(self):
		return self.isEnabled

	def IsDisabled(self):
		return not self.IsEnabled()

	def Down(self):
		wndMgr.Down(self.hWnd)

	def SetUp(self):
		wndMgr.SetUp(self.hWnd)

	def SAFE_SetEvent(self, func, *args):
		self.eventFunc = __mem_func__(func)
		self.eventArgs = args

	def SetEvent(self, func, *args):
		self.eventFunc = func
		self.eventArgs = args

	def SAFE_SetDownEvent(self, func, *args):
		self.downEventFunc = __mem_func__(func)
		self.downEventArgs = args

	def SetDownEvent(self, func, *args):
		self.downEventFunc = func
		self.downEventArgs = args

	def SetTooltipEvent(self, showFunc, hideFunc):
		self.tooltipShowEventFunc = showFunc
		self.tooltipHideEventFunc = hideFunc

	def OnMouseOverIn(self):
		if self.overFunc:
			apply(self.overFunc, self.overArgs)

	def OnMouseOverOut(self):
		if self.overOutFunc:
			apply(self.overOutFunc, self.overOutArgs)

	def SetOverEvent(self, func, *args):
		self.overFunc = func
		self.overArgs = args

	def SetOverOutEvent(self, func, *args):
		self.overOutFunc = func
		self.overOutArgs = args

	def SetTextColor(self, color):
		if not self.ButtonText:
			return
		self.ButtonText.SetPackedFontColor(color)

	def AppendTextLineAllClear(self) :
		self.TextChild = []

	def SetAppendTextChangeText(self, idx, text):
		if not len(self.TextChild) :
			return

		self.TextChild[idx].SetText(text)

	def SetAppendTextColor(self, idx, color) :
		if not len(self.TextChild) :
			return

		self.TextChild[idx].SetPackedFontColor(color)

	def AppendTextLine(self, text, font_size = localeInfo.UI_DEF_FONT, font_color = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0), text_sort = "center", pos_x = None, pos_y = None):
		textLine = TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(font_size)
		textLine.SetPackedFontColor(font_color)
		textLine.SetText(text)
		textLine.Show()

		if not pos_x and not pos_y :
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2)
		else :
			textLine.SetPosition(pos_x, pos_y)

		textLine.SetVerticalAlignCenter()
		if "center" == text_sort :
			textLine.SetHorizontalAlignCenter()
		elif "right" == text_sort :
			textLine.SetHorizontalAlignRight()
		elif "left" == 	text_sort :
			textLine.SetHorizontalAlignLeft()

		self.TextChild.append(textLine)

	def SetTextLeftAligned(self):
		text = ""
		if self.ButtonText:
			text = self.ButtonText.GetText()

			self.ButtonText.Hide()
			del self.ButtonText

		textLine = TextLine()
		textLine.SetParent(self)
		textLine.SetPosition(5, self.GetHeight() / 2)
		textLine.SetVerticalAlignCenter()
		textLine.SetText(text)
		textLine.Show()

		self.ButtonText = textLine

	def SetText(self, text, height = 0):

		if not self.ButtonText:
			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.GetWidth()/2, self.GetHeight()/2 - height)
			textLine.SetVerticalAlignCenter()
			textLine.SetHorizontalAlignCenter()
			textLine.Show()
			self.ButtonText = textLine

		self.ButtonText.SetText(text)

	if app.ENABLE_QUEST_RENEWAL:
		def GetText(self):
			if not self.ButtonText:
				return ""

			return self.ButtonText.GetText()

		def SetTextAlignLeft(self, text, x = 27, height = 4):
			if not self.ButtonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(x, self.GetHeight()/2)
				textLine.SetVerticalAlignCenter()
				textLine.SetHorizontalAlignLeft()
				textLine.Show()
				self.ButtonText = textLine

			self.ButtonText.SetText(text)
			self.ButtonText.SetPosition(x, self.GetHeight()/2)
			self.ButtonText.SetVerticalAlignCenter()
			self.ButtonText.SetHorizontalAlignLeft()

		def SetTextAlignRight(self, text, x = 27, y = 0):
			if not self.ButtonText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(x, y)
				textLine.SetVerticalAlignCenter()
				textLine.Show()
				self.ButtonText = textLine

			self.ButtonText.SetText(text)
			self.ButtonText.SetPosition(x, y)
			self.ButtonText.SetVerticalAlignCenter()

	def SetFormToolTipText(self, type, text, x, y, xalign = 1, yalign = 0):
		if not self.ToolTipText:
			toolTip=createToolTipWindowDict[type]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			if xalign == 1:
				toolTip.SetHorizontalAlignCenter()
			elif xalign == 2:
				toolTip.SetHorizontalAlignRight()
			if yalign == 1:
				toolTip.SetVerticalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(x + self.GetWidth()/2, y)
			if self.tooltipTextColor:
				toolTip.SetPackedFontColor(self.tooltipTextColor)
			self.ToolTipText=toolTip

		self.ToolTipText.SetText(text)

	def SetToolTipTextColor(self, color):
		self.tooltipTextColor = color
		if self.ToolTipText:
			self.ToolTipText.SetPackedFontColor(color)

	def SetToolTipWindow(self, toolTip):
		self.ToolTipText=toolTip
		self.ToolTipText.SetParentProxy(self)

	def SetToolTipText(self, text, x=0, y = -19, xalign = 1, yalign = 0):
		self.SetFormToolTipText("TEXT", text, x, y, xalign, yalign)

	def SetMultiText(self, text):
		if not self.ToolTipText:
			toolTip=createMultiToolTipWindowDict["TEXT"]()
			toolTip.SetParent(self)
			toolTip.SetSize(0, 0)
			toolTip.SetTextHorizontalAlignCenter()
			toolTip.SetOutline()
			toolTip.Hide()
			toolTip.SetPosition(0 + self.GetWidth()/2, -19)

			self.ToolTipText=toolTip

		self.ToolTipText.SetText(text)

	def CallEvent(self):
		snd.PlaySound("sound/ui/click.wav")

		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)

	def DownEvent(self):
		if self.downEventFunc:
			apply(self.downEventFunc, self.downEventArgs)

	def ShowToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Show()
		if self.tooltipShowEventFunc:
			self.tooltipShowEventFunc()
			
		if self.showtooltipevent:
			apply(self.showtooltipevent, self.showtooltiparg)

	def HideToolTip(self):
		if self.ToolTipText:
			self.ToolTipText.Hide()
		if self.tooltipHideEventFunc:
			self.tooltipHideEventFunc()
			
		if self.hidetooltipevent:
			apply(self.hidetooltipevent, self.hidetooltiparg)

	def SetShowToolTipEvent(self, func, *args):
		self.showtooltipevent = func
		self.showtooltiparg = args
		
	def SetHideToolTipEvent(self, func, *args):
		self.hidetooltipevent = func
		self.hidetooltiparg = args

	def IsDown(self):
		return wndMgr.IsDown(self.hWnd)

	def SetRenderingRect(self, left, top, right, bottom):
		wndMgr.SetRenderingRect(self.hWnd, left, top, right, bottom)
		
	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def SetAlpha(self, alpha):
			wndMgr.SetButtonDiffuseColor(self.hWnd, 1.0, 1.0, 1.0, alpha)

		def GetText(self):
			if self.ButtonText:
				return self.ButtonText.GetText()
			else:
				return ""
				
		def IsDisable(self):
			return wndMgr.IsDisable(self.hWnd)
		
		def SetScale(self, scale_x, scale_y):
			wndMgr.SetButtonScale(self.hWnd, scale_x, scale_y)
			
		def SetDiffuseColor(self, r, g, b, a):
			wndMgr.SetButtonDiffuseColor(self.hWnd, r, g, b, a)

class RadioButton(Button):
	def __init__(self):
		Button.__init__(self)

	def __del__(self):
		Button.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterRadioButton(self, layer)

class RadioButtonGroup:
	def __init__(self):
		self.buttonGroup = []
		self.selectedBtnIdx = -1

	def __del__(self):
		for button, ue, de in self.buttonGroup:
			button.__del__()

	def Show(self):
		for (button, selectEvent, unselectEvent) in self.buttonGroup:
			button.Show()

	def Hide(self):
		for (button, selectEvent, unselectEvent) in self.buttonGroup:
			button.Hide()

	def SetText(self, idx, text):
		if idx >= len(self.buttonGroup):
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[idx]
		button.SetText(text)

	def OnClick(self, btnIdx):
		if btnIdx == self.selectedBtnIdx:
			return
		(button, selectEvent, unselectEvent) = self.buttonGroup[self.selectedBtnIdx]
		if unselectEvent:
			unselectEvent()
		button.SetUp()

		self.selectedBtnIdx = btnIdx
		(button, selectEvent, unselectEvent) = self.buttonGroup[btnIdx]
		if selectEvent:
			selectEvent()

		button.Down()

	def AddButton(self, button, selectEvent, unselectEvent):
		i = len(self.buttonGroup)
		button.SetEvent(lambda : self.OnClick(i))
		self.buttonGroup.append([button, selectEvent, unselectEvent])
		button.SetUp()

	def Create(rawButtonGroup):
		radioGroup = RadioButtonGroup()
		for (button, selectEvent, unselectEvent) in rawButtonGroup:
			radioGroup.AddButton(button, selectEvent, unselectEvent)

		radioGroup.OnClick(0)

		return radioGroup

	Create=staticmethod(Create)

class ToggleButton(Button):
	def __init__(self):
		Button.__init__(self)

		self.eventUp = None
		self.eventDown = None

	def __del__(self):
		Button.__del__(self)

		self.eventUp = None
		self.argsUp = None
		self.eventDown = None
		self.argsDown = None

	def SetToggleUpEvent(self, event, *args):
		self.eventUp = event
		self.argsUp = args

	def SetToggleDownEvent(self, event, *args):
		self.eventDown = event
		self.argsDown = args

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterToggleButton(self, layer)

	def OnToggleUp(self):
		if self.eventUp:
			apply(self.eventUp, self.argsUp)

	def OnToggleDown(self):
		if self.eventDown:
			apply(self.eventDown, self.argsDown)

class DragButton(Button):
	def __init__(self):
		Button.__init__(self)
		self.AddFlag("movable")

		self.callbackEnable = True
		self.eventMove = lambda: None

	def __del__(self):
		Button.__del__(self)

		self.eventMove = lambda: None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterDragButton(self, layer)

	def SetMoveEvent(self, event):
		self.eventMove = event

	def SetRestrictMovementArea(self, x, y, width, height):
		wndMgr.SetRestrictMovementArea(self.hWnd, x, y, width, height)

	def TurnOnCallBack(self):
		self.callbackEnable = True

	def TurnOffCallBack(self):
		self.callbackEnable = False

	def OnMove(self):
		if self.callbackEnable:
			self.eventMove()

class NumberLine(Window):

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

	def __del__(self):
		Window.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterNumberLine(self, layer)

	def SetHorizontalAlignCenter(self):
		wndMgr.SetNumberHorizontalAlignCenter(self.hWnd)

	def SetHorizontalAlignRight(self):
		wndMgr.SetNumberHorizontalAlignRight(self.hWnd)

	def SetVerticalAlignCenter(self):
		wndMgr.SetNumberVerticalAlignCenter(self.hWnd)

	def SetPath(self, path):
		wndMgr.SetPath(self.hWnd, path)

	def SetNumber(self, number):
		wndMgr.SetNumber(self.hWnd, str(number))

	def SetDiffuseColor(self, r, g, b, a):
		wndMgr.SetDiffuseColor(self.hWnd, r, g, b, a)

###################################################################################################
## PythonScript Element
###################################################################################################

class Box(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBox(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class Bar(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class Line(Window):

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterLine(self, layer)

	def SetColor(self, color):
		wndMgr.SetColor(self.hWnd, color)

class SlotBar(Window):

	def __init__(self):
		Window.__init__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar3D(self, layer)

## Same with SlotBar
class Bar3D(Window):

	def __init__(self):
		Window.__init__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBar3D(self, layer)

	def SetColor(self, left, right, center):
		wndMgr.SetColor(self.hWnd, left, right, center)

class SlotWindow(Window):

	def __init__(self):
		Window.__init__(self)

		self.slotList = []

		self.StartIndex = 0

		self.eventSelectEmptySlot = None
		self.eventSelectItemSlot = None
		self.eventUnselectEmptySlot = None
		self.eventUnselectItemSlot = None
		self.eventUseSlot = None
		self.eventOverInItem = None
		self.eventOverOutItem = None
		self.eventPressedSlotButton = None

		self.eventOverIn = None
		self.eventOverOut = None

		self.eventSelectEmptySlotWindow = None
		self.eventSelectItemSlotWindow = None
		self.eventUnselectItemSlotWindow = None
		self.eventOverInItemWindow = None

	def __del__(self):
		Window.__del__(self)

		self.eventSelectEmptySlot = None
		self.eventSelectItemSlot = None
		self.eventUnselectEmptySlot = None
		self.eventUnselectItemSlot = None
		self.eventUseSlot = None
		self.eventOverInItem = None
		self.eventOverOutItem = None
		self.eventPressedSlotButton = None

		self.eventOverIn = None
		self.eventOverOut = None

		self.eventSelectEmptySlotWindow = None
		self.eventSelectItemSlotWindow = None
		self.eventUnselectItemSlotWindow = None
		self.eventOverInItemWindow = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterSlotWindow(self, layer)

	def SetSlotStyle(self, style):
		wndMgr.SetSlotStyle(self.hWnd, style)

	def HasSlot(self, slotIndex):
		return wndMgr.HasSlot(self.hWnd, slotIndex)

	def SetSlotBaseImage(self, imageFileName, r, g, b, a):
		wndMgr.SetSlotBaseImage(self.hWnd, imageFileName, r, g, b, a)

	def SetCoverButton(self,\
						slotIndex,\
						upName="d:/ymir work/ui/public/slot_cover_button_01.sub",\
						overName="d:/ymir work/ui/public/slot_cover_button_02.sub",\
						downName="d:/ymir work/ui/public/slot_cover_button_03.sub",\
						disableName="d:/ymir work/ui/public/slot_cover_button_04.sub",\
						LeftButtonEnable = False,\
						RightButtonEnable = True):
		wndMgr.SetCoverButton(self.hWnd, slotIndex, upName, overName, downName, disableName, LeftButtonEnable, RightButtonEnable)

	def EnableCoverButton(self, slotIndex):
		wndMgr.EnableCoverButton(self.hWnd, slotIndex)

	def DisableCoverButton(self, slotIndex):
		wndMgr.DisableCoverButton(self.hWnd, slotIndex)

	def DeleteCoverButton(self, slotIndex):
		wndMgr.DeleteCoverButton(self.hWnd, slotIndex)

	def SetAlwaysRenderCoverButton(self, slotIndex, bAlwaysRender = True):
		wndMgr.SetAlwaysRenderCoverButton(self.hWnd, slotIndex, bAlwaysRender)

	def AppendSlotButton(self, upName, overName, downName):
		wndMgr.AppendSlotButton(self.hWnd, upName, overName, downName)

	def ShowSlotButton(self, slotNumber):
		wndMgr.ShowSlotButton(self.hWnd, slotNumber)

	def HideAllSlotButton(self):
		wndMgr.HideAllSlotButton(self.hWnd)

	def AppendRequirementSignImage(self, filename):
		wndMgr.AppendRequirementSignImage(self.hWnd, filename)

	def ShowRequirementSign(self, slotNumber):
		wndMgr.ShowRequirementSign(self.hWnd, slotNumber)

	def HideRequirementSign(self, slotNumber):
		wndMgr.HideRequirementSign(self.hWnd, slotNumber)

	def ActivateSlot(self, slotNumber, diffuseColour = (0.0, 0.0, 0.0, 0.0)):
		wndMgr.ActivateSlot(self.hWnd, slotNumber, diffuseColour)

	def DeactivateSlot(self, slotNumber):
		wndMgr.DeactivateSlot(self.hWnd, slotNumber)

	def NewActivateSlot(self, slotNumber):
		wndMgr.NewActivateSlot(self.hWnd, slotNumber)

	def NewDeactivateSlot(self, slotNumber):
		wndMgr.NewDeactivateSlot(self.hWnd, slotNumber)

	def ShowSlotBaseImage(self, slotNumber):
		wndMgr.ShowSlotBaseImage(self.hWnd, slotNumber)

	def HideSlotBaseImage(self, slotNumber):
		wndMgr.HideSlotBaseImage(self.hWnd, slotNumber)

	def SAFE_SetButtonEvent(self, button, state, event):
		if "LEFT"==button:
			if "EMPTY"==state:
				self.eventSelectEmptySlot=__mem_func__(event)
			elif "EXIST"==state:
				self.eventSelectItemSlot=__mem_func__(event)
			elif "ALWAYS"==state:
				self.eventSelectEmptySlot=__mem_func__(event)
				self.eventSelectItemSlot=__mem_func__(event)
		elif "RIGHT"==button:
			if "EMPTY"==state:
				self.eventUnselectEmptySlot=__mem_func__(event)
			elif "EXIST"==state:
				self.eventUnselectItemSlot=__mem_func__(event)
			elif "ALWAYS"==state:
				self.eventUnselectEmptySlot=__mem_func__(event)
				self.eventUnselectItemSlot=__mem_func__(event)

	def SetSelectEmptySlotEvent(self, empty, window = None):
		self.eventSelectEmptySlot = empty
		self.eventSelectEmptySlotWindow = window

	def SetSelectItemSlotEvent(self, item, window = None):
		print "SetSelectItemSlotEvent", item, window
		self.eventSelectItemSlot = item
		self.eventSelectItemSlotWindow = window

	def SetUnselectEmptySlotEvent(self, empty):
		self.eventUnselectEmptySlot = empty

	def SetUnselectItemSlotEvent(self, item, window = None):
		self.eventUnselectItemSlot = item
		self.eventUnselectItemSlotWindow = window

	def SetUseSlotEvent(self, use):
		self.eventUseSlot = use

	def SetOverInItemEvent(self, event, window = None):
		self.eventOverInItem = event
		self.eventOverInItemWindow = window

	def SetOverOutItemEvent(self, event):
		self.eventOverOutItem = event

	def SetOverInEvent(self, event):
		self.eventOverIn = event

	def SetOverOutEvent(self, event):
		self.eventOverOut = event

	def OnOverIn(self, slotNumber):
		if self.eventOverIn:
			self.eventOverIn(slotNumber)

	def OnOverOut(self):
		if self.eventOverOut:
			self.eventOverOut()

	def SetPressedSlotButtonEvent(self, event):
		self.eventPressedSlotButton = event

	def GetSlotCount(self):
		return wndMgr.GetSlotCount(self.hWnd)

	def GetPickedSlotNumber(self, focusItem = True):
		return wndMgr.GetPickedSlotNumber(self.hWnd, focusItem)

	def SetUseMode(self, flag):
		"True�϶��� ItemToItem �� �������� �����ش�"
		wndMgr.SetUseMode(self.hWnd, flag)

	def IsUseMode(self):
		return wndMgr.IsUseMode(self.hWnd)

	def SetUsableItem(self, flag):
		"True�� ���� ����Ų �������� ItemToItem ���� �����ϴ�"
		wndMgr.SetUsableItem(self.hWnd, flag)

	def IsUsableItem(self):
		return wndMgr.IsUsableItem(self.hWnd)

	def SetSwitchMode(self, flag):
		"TRUE??? ItemToItem ? ???? ????"
		wndMgr.SetSwitchMode(self.hWnd, flag)

	def IsSwitchMode(self):
		return wndMgr.IsSwitchMode(self.hWnd)

	def SetSwitchableItem(self, flag):
		"TRUE? ?? ??? ???? ItemToItem ?? ????"
		wndMgr.SetSwitchableItem(self.hWnd, flag)

	def IsSwitchableItem(self):
		return wndMgr.IsSwitchableItem(self.hWnd)

	## Slot
	if app.ENABLE_SLOT_WINDOW_EX:
		def IsActivatedSlot(self, slotNumber):
			return wndMgr.IsActivatedSlot(self.hWnd, slotNumber)

		def GetSlotCoolTime(self, slotIndex):
			return wndMgr.GetSlotCoolTime(self.hWnd, slotIndex)

	def SetSlotCoolTime(self, slotIndex, coolTime, elapsedTime = 0.0):
		wndMgr.SetSlotCoolTime(self.hWnd, slotIndex, coolTime, elapsedTime)

	def DisableSlot(self, slotIndex):
		wndMgr.DisableSlot(self.hWnd, slotIndex)

	def EnableSlot(self, slotIndex):
		wndMgr.EnableSlot(self.hWnd, slotIndex)

	if app.ENABLE_RENEWAL_SHOP_SELLING:
		def SetUnusableSlot(self, slotIndex):
			wndMgr.SetUnusableSlot(self.hWnd, slotIndex)

		def SetUsableSlot(self, slotIndex):
			wndMgr.SetUsableSlot(self.hWnd, slotIndex)

	def LockSlot(self, slotIndex, colour = (0.0, 0.0, 0.0, 0.5)):
		wndMgr.LockSlot(self.hWnd, slotIndex, *colour)

	def UnlockSlot(self, slotIndex):
		wndMgr.UnlockSlot(self.hWnd, slotIndex)

	def RefreshSlot(self):
		wndMgr.RefreshSlot(self.hWnd)

	def ClearSlot(self, slotNumber):
		wndMgr.ClearSlot(self.hWnd, slotNumber)

	def ClearAllSlot(self):
		wndMgr.ClearAllSlot(self.hWnd)

	def AppendSlot(self, index, x, y, width, height):
		wndMgr.AppendSlot(self.hWnd, index, x, y, width, height)

	def SetSlot(self, slotIndex, itemIndex, width, height, icon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetSlot(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor)

	def SetSlotScale(self, slotIndex, itemIndex, width, height, icon, sx, sy, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
		wndMgr.SetSlotScale(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor, sx, sy)

	def SetSlotCount(self, slotNumber, count):
		wndMgr.SetSlotCount(self.hWnd, slotNumber, count)

	def SetSlotCountNew(self, slotNumber, grade, count):
		wndMgr.SetSlotCountNew(self.hWnd, slotNumber, grade, count)

	if app.ENABLE_CUBE_RENEWAL:
		def GetItemIndex(self, slotNumber):
			return wndMgr.GetItemIndex(self.hWnd, slotNumber)

	if app.ENABLE_TRANSMUTATION_SYSTEM:
		def SetItemSlot(self, renderingSlotNumber, ItemIndex, ItemCount = 0, diffuseColor = (1.0, 1.0, 1.0, 1.0), is_transmutated = 0):
			if 0 == ItemIndex or None == ItemIndex:
				wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
				return

			item.SelectItem(ItemIndex)
			itemIcon = item.GetIconImage()

			item.SelectItem(ItemIndex)
			(width, height) = item.GetItemSize()

			wndMgr.SetSlot(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, diffuseColor)
			wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, ItemCount)

			if is_transmutated > 0:
				wndMgr.EnableSlotCoverImage(self.hWnd, renderingSlotNumber)
			else:
				wndMgr.DisableSlotCoverImage(self.hWnd, renderingSlotNumber)
	else:
		def SetItemSlot(self, renderingSlotNumber, ItemIndex, ItemCount = 0, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
			if 0 == ItemIndex or None == ItemIndex:
				wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
				return

			item.SelectItem(ItemIndex)
			itemIcon = item.GetIconImage()

			item.SelectItem(ItemIndex)
			(width, height) = item.GetItemSize()

			wndMgr.SetSlot(self.hWnd, renderingSlotNumber, ItemIndex, width, height, itemIcon, diffuseColor)
			wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, ItemCount)

	def SetSkillSlot(self, renderingSlotNumber, skillIndex, skillLevel):

		skillIcon = skill.GetIconImage(skillIndex)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)
		wndMgr.SetSlotCount(self.hWnd, renderingSlotNumber, skillLevel)

	def SetSkillSlotNew(self, renderingSlotNumber, skillIndex, skillGrade, skillLevel):

		skillIcon = skill.GetIconImageNew(skillIndex, skillGrade)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon)

	def SetEmotionSlot(self, renderingSlotNumber, emotionIndex):
		import player
		icon = player.GetEmotionIconImage(emotionIndex)

		if 0 == icon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		wndMgr.SetSlot(self.hWnd, renderingSlotNumber, emotionIndex, 1, 1, icon)

	def SetPetSkillSlot(self, renderingSlotNumber, skillIndex, skillLevel, sx = 1.0, sy = 1.0):
		skillIcon = pet.GetSkillProtoIconImage(skillIndex)

		if 0 == skillIcon:
			wndMgr.ClearSlot(self.hWnd, renderingSlotNumber)
			return

		if sx != 1.0:
			wndMgr.SetSlotScale(self.hWnd, renderingSlotNumber, skillIndex, 1, 1, skillIcon, (1.0, 1.0, 1.0, 1.0), sx, sy)
		else:
			self.SetSlot(renderingSlotNumber, skillIndex, 1, 1, skillIcon)
			self.SetSlotCount(renderingSlotNumber, skillLevel)

	## Event
	def OnSelectEmptySlot(self, slotNumber):
		if self.eventSelectEmptySlot:
			if self.eventSelectEmptySlotWindow:
				self.eventSelectEmptySlot(slotNumber, self.eventSelectEmptySlotWindow)
			else:
				self.eventSelectEmptySlot(slotNumber)

	def OnSelectItemSlot(self, slotNumber):
		if self.eventSelectItemSlot:
			if self.eventSelectItemSlotWindow:
				self.eventSelectItemSlot(slotNumber, self.eventSelectItemSlotWindow)
			else:
				self.eventSelectItemSlot(slotNumber)

	def OnUnselectEmptySlot(self, slotNumber):
		if self.eventUnselectEmptySlot:
			self.eventUnselectEmptySlot(slotNumber)

	def OnUnselectItemSlot(self, slotNumber):
		if self.eventUnselectItemSlot:
			self.eventUnselectItemSlot(slotNumber)

	def OnUseSlot(self, slotNumber):
		if self.eventUseSlot:
			self.eventUseSlot(slotNumber)

	def OnOverInItem(self, slotNumber):
		if self.eventOverInItem:
			self.eventOverInItem(slotNumber)

	def OnOverOutItem(self):
		if self.eventOverOutItem:
			self.eventOverOutItem()

	def OnPressedSlotButton(self, slotNumber):
		if self.eventPressedSlotButton:
			self.eventPressedSlotButton(slotNumber)

	def GetStartIndex(self):
		return 0

	# def RefreshIndices(self):
	# 	self.__indices = wndMgr.GetSlotIndices(self.hWnd)

	def RefreshItems(self, vnumFunction, countFunction = lambda x: 0):
		for index in self.slotList:
			self.SetItemSlot(index, vnumFunction(index), countFunction(index))

		self.RefreshSlot()

	if app.ENABLE_RENEWAL_EXCHANGE:
		def SetSlotHighlightedGreeen(self, slotNumber):
			wndMgr.SetSlotHighlightedGreeen(self.hWnd, slotNumber)

		def DisableSlotHighlightedGreen(self, slotNumber):
			wndMgr.DisableSlotHighlightedGreen(self.hWnd, slotNumber)

	if app.ENABLE_TRANSMUTATION_SYSTEM:
		def EnableSlotCoverImage(self, slotIndex):
			wndMgr.EnableSlotCoverImage(self.hWnd, slotIndex)

		def DisableSlotCoverImage(self, slotIndex):
			wndMgr.DisableSlotCoverImage(self.hWnd, slotIndex)

		def ActivateChangeLookSlot(self, slotIndex, bDiffuseType = 0):
			wndMgr.ActivateChangeLookSlot(self.hWnd, slotIndex, bDiffuseType)

		def DeactivateChangeLookSlot(self, slotIndex):
			wndMgr.DeactivateChangeLookSlot(self.hWnd, slotIndex)

class GridSlotWindow(SlotWindow):

	def __init__(self):
		SlotWindow.__init__(self)

		self.startIndex = 0

	def __del__(self):
		SlotWindow.__del__(self)

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterGridSlotWindow(self, layer)

	def ArrangeSlot(self, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank):

		self.startIndex = StartIndex

		wndMgr.ArrangeSlot(self.hWnd, StartIndex, xCount, yCount, xSize, ySize, xBlank, yBlank)
		self.startIndex = StartIndex

	def GetStartIndex(self):
		return self.startIndex

class TitleBar(Window):
	BLOCK_WIDTH = 32
	BLOCK_HEIGHT = 23
	IS_SCALE = False
	POSITIONS = {
		"Q" : [21, 0],
		"C" : [0, 0]
	}

	IMAGES = {
		'TITLE' : {
			'PATH' : "assets/ui/elements/title/orange",
			'LEFT' : 'left.tga',
			'CENTER' : 'center.tga',
			'RIGHT' : 'right.tga',
			'RIGHT_SPECIAL' : 'right_2.tga'
		},

		'BTN_CLOSE' : {
			'PATH' : "assets/ui/elements/title/buttons",
			'NORMAL' : 'close_norm.tga',
			'OVER' : 'close_hover.tga',
			'DOWN' : 'close_down.tga'
		},

		'BTN_INFO' : {
			'PATH' : "assets/ui/elements/title/buttons",
			'NORMAL' : 'info_norm.tga',
			'OVER' : 'info_hover.tga',
			'DOWN' : 'info_down.tga'
		},

		'BTN_SORT' : {
			'PATH' : "assets/ui/elements/title/buttons",
			'NORMAL' : 'sort_norm.tga',
			'OVER' : 'sort_hover.tga',
			'DOWN' : 'sort_down.tga'
		},
	}

	def __init__(self):
		Window.__init__(self)
		self.Objects = {}
		self.AddFlag("attach")

	def __del__(self):
		Window.__del__(self)
		self.Objects = {}

	def MakeTitleBar(self, width, color):
		width = max(64, width)

		# Build base
		for sType in ["LEFT", "CENTER", "RIGHT"]:
			rElement = ExpandedImageBox() if sType == "CENTER" else ImageBox()
			rElement.AddFlag("not_pick")
			rElement.SetParent(self)
			rElement.LoadImage("{}/{}".format(self.IMAGES['TITLE']['PATH'], self.IMAGES['TITLE'][sType]))
			rElement.Show()
			self.Objects[sType] = rElement

		## Build whole buttons
		eToolTips = {
			"BTN_CLOSE" : localeInfo.UI_CLOSE,
			"BTN_INFO" : localeInfo.TITLE_BAR_INFORMATION,
			"BTN_SORT" : localeInfo.TITLE_BAR_SORT,
		}

		for sType in ["BTN_CLOSE", "BTN_INFO", "BTN_SORT"]:
			rElement = Button()
			rElement.SetParent(self)
			rElement.SetUpVisual("{}/{}".format(self.IMAGES[sType]['PATH'], self.IMAGES[sType]['NORMAL']))
			rElement.SetOverVisual("{}/{}".format(self.IMAGES[sType]['PATH'], self.IMAGES[sType]['OVER']))
			rElement.SetDownVisual("{}/{}".format(self.IMAGES[sType]['PATH'], self.IMAGES[sType]['DOWN']))
			rElement.SetToolTipText(eToolTips.get(sType, ""))
			rElement.Show()
			self.Objects[sType] = rElement

		chBox = CheckBox()
		chBox.SetParent(self)
		chBox.SetPosition(8, 0)
		chBox.Show()

		self.Objects["BTN_CHBOX"] = chBox

		# Lets hide whole btns except close
		for sType in ["BTN_INFO", "BTN_SORT", "BTN_CHBOX"]:
			if not self.Objects.get(sType):
				continue

			self.HandleButtonState(sType, False)

		self.SetWidth(width, self.IS_SCALE)

	def SetWidth(self, width, isScale = False):

		if isScale:
			self.SetSize(width, self.BLOCK_HEIGHT)
			self.Objects["LEFT"].SetPosition(0, 0)
			self.Objects["CENTER"].SetPosition(self.Objects["LEFT"].GetWidth(), 0)
			self.Objects["CENTER"].SetScale(float(self.GetWidth() - (self.Objects["LEFT"].GetWidth() + self.Objects["RIGHT"].GetWidth())) / float(self.Objects["CENTER"].GetWidth()), 1.0)
			self.Objects["RIGHT"].SetPosition(self.Objects["LEFT"].GetWidth() + self.Objects["CENTER"].GetWidth() - 1, 0)
		else:
			self.Objects["CENTER"].SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
			self.Objects["CENTER"].SetPosition(self.BLOCK_WIDTH, 0)
			self.Objects["RIGHT"].SetPosition(width - self.BLOCK_WIDTH, 0)
			self.SetSize(width, self.BLOCK_HEIGHT)

		self.Objects["BTN_CLOSE"].SetPosition(width - self.Objects["BTN_CLOSE"].GetWidth() - self.POSITIONS["C"][0], self.POSITIONS["C"][1])
		self.Objects["BTN_INFO"].SetPosition(width - self.Objects["BTN_INFO"].GetWidth() - self.POSITIONS["Q"][0], self.POSITIONS["Q"][1])
		self.Objects["BTN_SORT"].SetPosition(width - self.Objects["BTN_SORT"].GetWidth() - self.POSITIONS["Q"][0], self.POSITIONS["Q"][1])

	def SetCloseEvent(self, event):
		self.Objects["BTN_CLOSE"].SetEvent(event)

	def SetInfoToolTip(self, tooltipWnd):
		self.Objects["BTN_INFO"].SetToolTipWindow(tooltipWnd)

	def SetSortEvent(self, event):
		self.Objects["BTN_SORT"].SetEvent(event)

	def HandleButtonState(self, sType, bShow = True):
		if not self.Objects.get(sType):
			return

		if sType == "BTN_CLOSE":
			iStates = ('RIGHT_SPECIAL', 'RIGHT')
			self.Objects["RIGHT"].LoadImage("{}/{}".format(self.IMAGES['TITLE']['PATH'], self.IMAGES['TITLE'][iStates[bShow]]))

		if bShow:
			self.Objects[sType].Show()
		else:
			self.Objects[sType].Hide()

	def HandleButtonGetter(self, sType):
		return self.Objects.get(sType, None)

if app.ENABLE_QUEST_RENEWAL:
	class SubTitleBar(Button):
		def __init__(self):
			Button.__init__(self)

		def __del__(self):
			Button.__del__(self)

		def MakeSubTitleBar(self, width, color):
			width = max(64, width)
			self.SetWidth(width)
			self.SetUpVisual("d:/ymir work/ui/quest_re/quest_tab_01.tga")
			self.SetOverVisual("d:/ymir work/ui/quest_re/quest_tab_02.tga")
			self.SetDownVisual("d:/ymir work/ui/quest_re/quest_tab_03.tga")
			self.Show()

			scrollImage = ImageBox()
			scrollImage.SetParent(self)
			scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_down.tga")
			scrollImage.SetPosition(5, 2.5)
			scrollImage.AddFlag("not_pick")
			scrollImage.Show()
			self.scrollImage = scrollImage

		def OpenCategory(self, qcount = 0):
			if qcount > 1:
				self.scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_up.tga")
			else:
				self.scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_down.tga")

		def CloseCategory(self, qcount = 0):
			self.scrollImage.LoadImage("d:/ymir work/ui/quest_re/quest_down.tga")

		def SetQuestLabel(self, filename, qcount):
			tabColor = ImageBox()
			tabColor.SetParent(self)
			tabColor.LoadImage(filename)
			tabColor.AddFlag("not_pick")
			tabColor.SetPosition(188, 12)
			if qcount > 1:
				tabColor.Show()
			else:
				tabColor.Hide()
			self.tabColor = tabColor

		def SetWidth(self, width):
			self.SetPosition(32, 0)
			self.SetSize(width, 23)

	class ListBar(Button):
		def __init__(self):
			Button.__init__(self)

		def __del__(self):
			Button.__del__(self)

		def MakeListBar(self, width, color):
			width = max(64, width)
			self.SetWidth(width)
			self.Show()

			checkbox = ImageBox()
			checkbox.SetParent(self)
			checkbox.LoadImage("d:/ymir work/ui/quest_re/quest_new.tga")
			checkbox.SetPosition(10, 9)
			checkbox.AddFlag("not_pick")
			checkbox.Show()
			self.checkbox = checkbox
			self.isChecked = False

		def SetWidth(self, width):
			self.SetPosition(32, 0)
			self.SetSize(width, 23)

		def CallEvent(self):
			self.OnClickEvent()
			super(ListBar, self).CallEvent()

		def OnClickEvent(self):
			self.checkbox.Hide()
			self.isChecked = True

		def SetSlot(self, slotIndex, itemIndex, width, height, icon, diffuseColor = (1.0, 1.0, 1.0, 1.0)):
			wndMgr.SetSlot(self.hWnd, slotIndex, itemIndex, width, height, icon, diffuseColor)

class HorizontalBar(Window):

	BLOCK_WIDTH = 32
	BLOCK_HEIGHT = 17

	def __init__(self):
		Window.__init__(self)
		self.AddFlag("attach")

	def __del__(self):
		Window.__del__(self)

	def Create(self, width):

		width = max(96, width)

		imgLeft = ImageBox()
		imgLeft.SetParent(self)
		imgLeft.AddFlag("not_pick")
		imgLeft.LoadImage("d:/ymir work/ui/pattern/horizontalbar_left.tga")
		imgLeft.Show()

		imgCenter = ExpandedImageBox()
		imgCenter.SetParent(self)
		imgCenter.AddFlag("not_pick")
		imgCenter.LoadImage("d:/ymir work/ui/pattern/horizontalbar_center.tga")
		imgCenter.Show()

		imgRight = ImageBox()
		imgRight.SetParent(self)
		imgRight.AddFlag("not_pick")
		imgRight.LoadImage("d:/ymir work/ui/pattern/horizontalbar_right.tga")
		imgRight.Show()

		self.imgLeft = imgLeft
		self.imgCenter = imgCenter
		self.imgRight = imgRight
		self.SetWidth(width)

	def SetWidth(self, width):
		self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - self.BLOCK_WIDTH*2) - self.BLOCK_WIDTH) / self.BLOCK_WIDTH, 0.0)
		self.imgCenter.SetPosition(self.BLOCK_WIDTH, 0)
		self.imgRight.SetPosition(width - self.BLOCK_WIDTH, 0)
		self.SetSize(width, self.BLOCK_HEIGHT)

class Gauge(Window):

	SLOT_WIDTH = 16
	SLOT_HEIGHT = 7

	GAUGE_TEMPORARY_PLACE = 12
	GAUGE_WIDTH = 16

	def __init__(self):
		Window.__init__(self)
		self.bg_curValue = 0
		self.bg_targetValue = None
		self.width = 0

	def __del__(self):
		Window.__del__(self)

	def MakeGauge(self, width, color):

		self.width = max(48, width)

		imgSlotLeft = ImageBox()
		imgSlotLeft.SetParent(self)
		imgSlotLeft.LoadImage("d:/ymir work/ui/pattern/gauge_slot_left.tga")
		imgSlotLeft.Show()

		imgSlotRight = ImageBox()
		imgSlotRight.SetParent(self)
		imgSlotRight.LoadImage("d:/ymir work/ui/pattern/gauge_slot_right.tga")
		imgSlotRight.Show()
		imgSlotRight.SetPosition(width - self.SLOT_WIDTH, 0)

		imgSlotCenter = ExpandedImageBox()
		imgSlotCenter.SetParent(self)
		imgSlotCenter.LoadImage("d:/ymir work/ui/pattern/gauge_slot_center.tga")
		imgSlotCenter.Show()
		imgSlotCenter.SetRenderingRect(0.0, 0.0, float((width - self.SLOT_WIDTH*2) - self.SLOT_WIDTH) / self.SLOT_WIDTH, 0.0)
		imgSlotCenter.SetPosition(self.SLOT_WIDTH, 0)

		bg_imgGauge = ExpandedImageBox()
		bg_imgGauge.SetParent(self)
		bg_imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_darkred.tga")
		bg_imgGauge.Show()
		bg_imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		bg_imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)

		imgGauge = ExpandedImageBox()
		imgGauge.SetParent(self)
		imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_" + color + ".tga")
		imgGauge.Show()
		imgGauge.SetRenderingRect(0.0, 0.0, 0.0, 0.0)
		imgGauge.SetPosition(self.GAUGE_TEMPORARY_PLACE, 0)

		imgSlotLeft.AddFlag("attach")
		imgSlotCenter.AddFlag("attach")
		imgSlotRight.AddFlag("attach")

		self.imgLeft = imgSlotLeft
		self.imgCenter = imgSlotCenter
		self.imgRight = imgSlotRight
		self.bg_imgGauge = bg_imgGauge
		self.imgGauge = imgGauge

		self.gaugeSize = 0.0

		self.SetSize(width, self.SLOT_HEIGHT)

	def SetPercentage(self, curValue, maxValue):
		self.curValue = float(curValue)
		self.maxValue = float(maxValue)

		# PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0
		# END_OF_PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR

		self.gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.imgGauge.SetRenderingRect(0.0, 0.0, self.gaugeSize, 0.0)

	def SetBGPercentage(self, curValue, maxValue):
		self.bg_curValue = float(curValue)
		self.bg_maxValue = float(maxValue)

		# PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR
		if maxValue > 0.0:
			percentage = min(1.0, float(curValue)/float(maxValue))
		else:
			percentage = 0.0
		# END_OF_PERCENTAGE_MAX_VALUE_ZERO_DIVISION_ERROR

		gaugeSize = -1.0 + float(self.width - self.GAUGE_TEMPORARY_PLACE*2) * percentage / self.GAUGE_WIDTH
		self.bg_imgGauge.SetRenderingRect(0.0, 0.0, gaugeSize, 0.0)

	def SetEasingPercentage(self, targetValue, maxValue):
		self.bg_targetValue = float(targetValue)
		self.bg_maxValue = float(maxValue)

	def SetColor(self, color):
		self.imgGauge.LoadImage("d:/ymir work/ui/pattern/gauge_" + color + ".tga")
		self.imgGauge.SetRenderingRect(0.0, 0.0, self.gaugeSize, 0.0)

	def OnUpdate(self):
		if self.bg_targetValue == None:
			return

		if self.bg_targetValue == self.bg_curValue:
			self.bg_targetValue = None
			return

		if self.bg_curValue > self.bg_targetValue:
			self.SetBGPercentage(max(self.bg_targetValue, self.bg_curValue - 0.5), self.bg_maxValue)
		else:
			self.SetBGPercentage(min(self.bg_targetValue, self.bg_curValue + 0.5), self.bg_maxValue)

class Board(Window):
	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	BASE_PATH = "d:/ymir work/ui/pattern"

	IMAGES = {
		'CORNER' : {
			0 : "Board_Corner_LeftTop",
			1 : "Board_Corner_LeftBottom",
			2 : "Board_Corner_RightTop",
			3 : "Board_Corner_RightBottom"
		},
		'BAR' : {
			0 : "Board_Line_Left",
			1 : "Board_Line_Right",
			2 : "Board_Line_Top",
			3 : "Board_Line_Bottom"
		},
		'FILL' : "Board_Base"
	}

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.skipMaxCheck = False

		self.MakeBoard()

	def MakeBoard(self):
		CornerFileNames = [ ]
		LineFileNames = [ ]

		for imageDictKey in (['CORNER', 'BAR']):
			for x in xrange(len(self.IMAGES[imageDictKey])):
				if imageDictKey == "CORNER":
					CornerFileNames.append("%s/%s.tga" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))
				elif imageDictKey == "BAR":
					LineFileNames.append("%s/%s.tga" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

		self.Base = ExpandedImageBox()
		self.Base.AddFlag("attach")
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("%s/%s.tga" % (self.BASE_PATH, self.IMAGES['FILL']))
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):
		if not self.skipMaxCheck:
			width = max(self.CORNER_WIDTH*2, width)
			height = max(self.CORNER_HEIGHT*2, height)

		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

class BorderA(Board):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16

	BASE_PATH = "d:/ymir work/ui/pattern/border_a"
	IMAGES = {
		'CORNER' : {
			0 : "border_a_corner_lefttop",
			1 : "border_a_corner_leftbottom",
			2 : "border_a_corner_righttop",
			3 : "border_a_corner_rightbottom"
		},
		'BAR' : {
			0 : "border_a_line_left",
			1 : "border_a_line_right",
			2 : "border_a_line_top",
			3 : "border_a_line_bottom"
		},
		'FILL' : "border_a_base"
	}

	def __init__(self, layer = "UI"):
		Board.__init__(self, layer)

	def __del__(self):
		Board.__del__(self)

	def SetSize(self, width, height):
		Board.SetSize(self, width, height)

class BorderB(Board):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16

	BASE_PATH = "d:/ymir work/ui/pattern"

	IMAGES = {
		'CORNER' : {
			0 : "border_b_left_top",
			1 : "border_b_left_bottom",
			2 : "border_b_right_top",
			3 : "border_b_right_bottom"
		},
		'BAR' : {
			0 : "border_b_left",
			1 : "border_b_right",
			2 : "border_b_top",
			3 : "border_b_bottom"
		},
		'FILL' : "border_b_center"
	}

	def __init__(self):
		Board.__init__(self)

		self.eventFunc = {
			"MOUSE_LEFT_BUTTON_UP" : None,
		}
		self.eventArgs = {
			"MOUSE_LEFT_BUTTON_UP" : None,
		}

	def __del__(self):
		Board.__del__(self)
		self.eventFunc = None
		self.eventArgs = None

	def SetSize(self, width, height):
		Board.SetSize(self, width, height)

	def SetEvent(self, func, *args) :
		result = self.eventFunc.has_key(args[0])
		if result :
			self.eventFunc[args[0]] = func
			self.eventArgs[args[0]] = args
		else :
			print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

class BoardWithTitleBar(Board):
	def __init__(self):
		Board.__init__(self)

		titleBar = TitleBar()
		titleBar.SetParent(self)
		titleBar.MakeTitleBar(0, "red")
		titleBar.SetPosition(8, 7)
		titleBar.Show()

		titleName = TextLine()
		titleName.SetParent(titleBar)
		titleName.SetPosition(0, 4)
		titleName.SetWindowHorizontalAlignCenter()
		titleName.SetHorizontalAlignCenter()
		titleName.Show()

		self.titleBar = titleBar
		self.titleName = titleName

		self.SetCloseEvent(self.Hide)

	def __del__(self):
		Board.__del__(self)
		self.titleBar = None
		self.titleName = None

	def SetSize(self, width, height):
		self.titleBar.SetWidth(width - 15)
		#self.pickRestrictWindow.SetSize(width, height - 30)
		Board.SetSize(self, width, height)
		self.titleName.UpdateRect()

	def SetTitleColor(self, color):
		self.titleName.SetPackedFontColor(color)

	def SetTitleName(self, name):
		self.titleName.SetText(name)

	def SetCloseEvent(self, event):
		self.titleBar.SetCloseEvent(event)

	def SetInfoToolTip(self, info):
		self.titleBar.SetInfoToolTip(info)

	def HandleButtonState(self, sType, bShow = True):
		self.titleBar.HandleButtonState(sType, bShow)

	def HandleButtonGetter(self, sType):
		return self.titleBar.HandleButtonGetter(sType)

class DragonBoard(Window):

	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128

	BASE_WIDTH = 777
	BASE_HEIGHT = 486

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self):
		Window.__init__(self)
		self.MakeBoard("d:/ymir work/ui/pattern/dragonboard/dragonboard_corner_", "d:/ymir work/ui/pattern/dragonboard/dragonboard_line_")
		self.MakeBase()

	def __del__(self):
		Window.__del__(self)

	def MakeBoard(self, cornerPath, linePath):
		CornerFileNames = [ cornerPath+dir+".tga" for dir in ("LeftTop", "LeftBottom", "RightTop", "RightBottom", ) ]
		LineFileNames = [ linePath+dir+".tga" for dir in ("Left", "Right", "Top", "Bottom", ) ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def MakeBase(self):
		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("d:/ymir work/ui/pattern/dragonboard/dragonboard_base.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def HideLine(self, line):
		self.Lines[line].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.BASE_HEIGHT) / self.BASE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.BASE_WIDTH) / self.BASE_WIDTH

		self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

class DragonBoardWithTitleBar(DragonBoard):
	def __init__(self):
		DragonBoard.__init__(self)

		titleBar = TitleBar()
		titleBar.SetParent(self)
		titleBar.MakeTitleBar(0, "red")
		titleBar.SetPosition(8, 4)
		titleBar.Show()

		titleName = TextLine()
		titleName.SetParent(titleBar)
		titleName.SetPosition(0, 4)
		titleName.SetWindowHorizontalAlignCenter()
		titleName.SetHorizontalAlignCenter()
		titleName.Show()

		self.titleBar = titleBar
		self.titleName = titleName

		self.SetCloseEvent(self.Hide)

	def __del__(self):
		DragonBoard.__del__(self)
		self.titleBar = None
		self.titleName = None

	def SetSize(self, width, height):
		self.titleBar.SetWidth(width - 15)
		#self.pickRestrictWindow.SetSize(width, height - 30)
		DragonBoard.SetSize(self, width, height)
		self.titleName.UpdateRect()

	def SetTitleColor(self, color):
		self.titleName.SetPackedFontColor(color)

	def SetTitleName(self, name):
		self.titleName.SetText(name)

	def SetCloseEvent(self, event):
		self.titleBar.SetCloseEvent(event)

class NewBoard(Window):
	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128
	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self):
		Window.__init__(self)

		self.MakeBoard("d:/ymir work/ui/pattern/new_board/Board_Corner_", "d:/ymir work/ui/pattern/new_board/Board_Line_")
		self.MakeBase()

	def MakeBoard(self, cornerPath, linePath):

		CornerFileNames = [ cornerPath+dir+".tga" for dir in ("LeftTop", "LeftBottom", "RightTop", "RightBottom", ) ]
		LineFileNames = [ linePath+dir+".tga" for dir in ("Left", "Right", "Top", "Bottom", ) ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def MakeBase(self):
		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("d:/ymir work/ui/pattern/new_board/Board_Base.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):
		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

class NewBoardWithTitleBar(NewBoard):
	def __init__(self, withButton = False):
		NewBoard.__init__(self)

		self.withButton = withButton
		titleBar = TitleBar()
		if self.withButton is True:
			titleBar = TitleBarWithoutButton()
		titleBar.SetParent(self)
		titleBar.MakeTitleBar(0, "red")
		titleBar.SetPosition(8, 7)
		titleBar.Show()

		titleName = TextLine()
		titleName.SetParent(titleBar)
		titleName.SetPosition(0, 4)
		titleName.SetWindowHorizontalAlignCenter()
		titleName.SetHorizontalAlignCenter()
		titleName.Show()

		self.titleBar = titleBar
		self.titleName = titleName

		if self.withButton is False:
			self.SetCloseEvent(self.Hide)

	def __del__(self):
		NewBoard.__del__(self)
		self.titleBar = None
		self.titleName = None

	def SetSize(self, width, height):
		self.titleBar.SetWidth(width - 15)
		#self.pickRestrictWindow.SetSize(width, height - 30)
		NewBoard.SetSize(self, width, height)
		self.titleName.UpdateRect()

	def SetTitleColor(self, color):
		self.titleName.SetPackedFontColor(color)

	def SetTitleName(self, name):
		self.titleName.SetText(name)

	def SetCloseEvent(self, event):
		if self.withButton is False:
			self.titleBar.SetCloseEvent(event)

class MainBoard(Window):
	CORNER_WIDTH = 32
	CORNER_HEIGHT = 32
	LINE_WIDTH = 128
	LINE_HEIGHT = 128

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	BASE_PATH = "assets/ui/elements/board/gray"

	IMAGES = {
		'CORNER' : {
			0 : "Left_Top",
			1 : "Left_Bottom",
			2 : "Right_Top",
			3 : "Right_Bottom"
		},
		'BAR' : {
			0 : "Line_Left",
			1 : "Line_Right",
			2 : "Line_Top",
			3 : "Line_Bottom"
		},
		'FILL' : "Base"
	}

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.skipMaxCheck = False

		self.MakeBoard()

	def MakeBoard(self):
		CornerFileNames = [ ]
		LineFileNames = [ ]

		for imageDictKey in (['CORNER', 'BAR']):
			for x in xrange(len(self.IMAGES[imageDictKey])):
				if imageDictKey == "CORNER":
					CornerFileNames.append("%s/%s.tga" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))
				elif imageDictKey == "BAR":
					LineFileNames.append("%s/%s.tga" % (self.BASE_PATH, self.IMAGES[imageDictKey][x]))

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

		self.Base = ExpandedImageBox()
		self.Base.AddFlag("attach")
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("%s/%s.tga" % (self.BASE_PATH, self.IMAGES['FILL']))
		self.Base.SetParent(self)
		self.Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Base.Show()

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):
		if not self.skipMaxCheck:
			width = max(self.CORNER_WIDTH*2, width)
			height = max(self.CORNER_HEIGHT*2, height)

		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

class MainBoardWithTitleBar(MainBoard):
	def __init__(self):
		MainBoard.__init__(self)

		titleBar = TitleBar()
		titleBar.SetParent(self)
		titleBar.MakeTitleBar(0, "red")
		titleBar.SetPosition(8, 7)
		titleBar.Show()

		titleName = TextLine()
		titleName.SetParent(titleBar)
		titleName.SetPosition(0, 4)
		titleName.SetWindowHorizontalAlignCenter()
		titleName.SetHorizontalAlignCenter()
		titleName.SetPackedFontColor(0xFFfff5d7)
		titleName.Show()

		self.titleBar = titleBar
		self.titleName = titleName

		self.SetCloseEvent(self.Hide)

	def __del__(self):
		MainBoard.__del__(self)
		self.titleBar = None
		self.titleName = None

	def SetSize(self, width, height):
		self.titleBar.SetWidth(width - 15)
		#self.pickRestrictWindow.SetSize(width, height - 30)
		MainBoard.SetSize(self, width, height)
		self.titleName.UpdateRect()

	def SetTitleColor(self, color):
		self.titleName.SetPackedFontColor(color)

	def SetTitleName(self, name):
		self.titleName.SetText(name)

	def SetCloseEvent(self, event):
		self.titleBar.SetCloseEvent(event)

	def SetSortEvent(self, event):
		self.titleBar.SetSortEvent(event)

	def SetInfoToolTip(self, info):
		self.titleBar.SetInfoToolTip(info)

	def HandleButtonState(self, sType, bShow = True):
		self.titleBar.HandleButtonState(sType, bShow)

	def HandleButtonGetter(self, sType):
		return self.titleBar.HandleButtonGetter(sType)

class MainSubBoard(Window):

	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.1, 0.1, 0.1, 0.68)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, type = "50", layer = "UI"):
		Window.__init__(self, layer)

		ASSETS = "assets/ui/elements/sub_board/{}/".format(type)

		CornerFileNames = [ ASSETS + dir + ".tga" for dir in ["Left_Top","Left_Bottom","Right_Top","Right_Bottom"] ]
		LineFileNames = [ ASSETS + "line_" + dir + ".tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = ExpandedImageBox()
		Base.AddFlag("not_pick")
		Base.LoadImage(ASSETS + "base.tga")
		Base.SetParent(self)
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def ShowCorner(self, corner):
		self.Corners[corner].Show()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def HideCorners(self, corner):
		self.Corners[corner].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def ShowLine(self, line):
		self.Lines[line].Show()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def HideLine(self, line):
		self.Lines[line].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - 1) / 1
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - 1) / 1

		self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ThinBoard(Window):

	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/ThinBoard_Line_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def HideCorners(self, corner):
		self.Corners[corner].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def ShowLine(self, line):
		self.Lines[line].Show()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def HideLine(self, line):
		self.Lines[line].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ThinBoardGold(Window):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardgold/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop_gold", "LeftBottom_gold","RightTop_gold", "RightBottom_gold"]]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardgold/ThinBoard_Line_"+dir+".tga" for dir in ["Left_gold", "Right_gold", "Top_gold", "Bottom_gold"]]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = ExpandedImageBox()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.LoadImage("d:/ymir work/ui/pattern/thinboardgold/thinboard_bg_gold.tga")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		if self.Base:
			self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ThinBoardCircle(Window):
	CORNER_WIDTH = 4
	CORNER_HEIGHT = 4
	LINE_WIDTH = 4
	LINE_HEIGHT = 4
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 1.0)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Corner_"+dir+"_Circle.tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardcircle/ThinBoard_Line_"+dir+"_Circle.tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ThinBoardNew(Window):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboardnew/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboardnew/ThinBoard_Line_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = Bar()
		Base.SetParent(self)
		Base.AddFlag("attach")
		Base.AddFlag("not_pick")
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.SetColor(self.BOARD_COLOR)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Base.SetSize(width - self.CORNER_WIDTH*2, height - self.CORNER_HEIGHT*2)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class Thinboard_Unique(Window):

	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16
	BOARD_COLOR = grp.GenerateColor(0.1, 0.1, 0.1, 0.68)

	LT = 0
	LB = 1
	RT = 2
	RB = 3
	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = [ "d:/ymir work/ui/pattern/thinboard_new/ThinBoard_new_Corner_"+dir+".tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/pattern/thinboard_new/ThinBoard_new_Line_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		Base = ExpandedImageBox()
		Base.AddFlag("not_pick")
		Base.LoadImage("d:/ymir work/ui/pattern/thinboard_new/thinboard_new_base.tga")
		Base.SetParent(self)
		Base.SetPosition(self.CORNER_WIDTH, self.CORNER_HEIGHT)
		Base.Show()
		self.Base = Base

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def ShowCorner(self, corner):
		self.Corners[corner].Show()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def HideCorners(self, corner):
		self.Corners[corner].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def ShowLine(self, line):
		self.Lines[line].Show()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def HideLine(self, line):
		self.Lines[line].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH
		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - 1) / 1
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - 1) / 1

		self.Base.SetRenderingRect(0, 0, horizontalShowingPercentage, verticalShowingPercentage)

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

class ScrollBar(Window):

	SCROLLBAR_WIDTH = 17
	SCROLLBAR_MIDDLE_HEIGHT = 9
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	MIDDLE_BAR_POS = 5
	MIDDLE_BAR_UPPER_PLACE = 3
	MIDDLE_BAR_DOWNER_PLACE = 4
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")
			#self.AddFlag("restrict_x")

		def MakeImage(self):
			top = ImageBox()
			top.SetParent(self)
			top.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Top.tga")
			top.SetPosition(0, 0)
			top.AddFlag("not_pick")
			top.Show()
			bottom = ImageBox()
			bottom.SetParent(self)
			bottom.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/ui/pattern/ScrollBar_Middle.tga")
			middle.SetPosition(0, 4)
			middle.AddFlag("not_pick")
			middle.Show()

			self.top = top
			self.bottom = bottom
			self.middle = middle

		def SetSize(self, height):
			height = max(12, height)
			DragButton.SetSize(self, 10, height)
			self.bottom.SetPosition(0, height-4)

			height -= 4*3
			self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = False
		self.scrollStep = 0.20
		self.scroll_span = 0

		self.CreateScrollBar()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		barSlot = Bar3D()
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_up_button_03.sub")
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_down_button_03.sub")
		downButton.Show()

		self.upButton = upButton
		self.downButton = downButton
		self.middleBar = middleBar
		self.barSlot = barSlot

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()

	def Destroy(self):
		self.middleBar = None
		self.upButton = None
		self.downButton = None
		self.eventScroll = lambda *arg: None

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2
		self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.upButton.SetPosition(0, 0)
		self.downButton.SetPosition(0, height - self.SCROLLBAR_BUTTON_HEIGHT)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlot.SetPosition(0, self.SCROLLBAR_BUTTON_HEIGHT)
		self.barSlot.SetSize(self.GetWidth() - 2, self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2 - 2)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep
		
	def SetSpan(self, span):
		self.scroll_span = span

	def IncreaseSpan(self, span):
		self.scroll_span += span
	
	def GetSpan(self):
		return self.scroll_span

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def OnMove(self):

		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

	## ScrollBar Wheel Support
	def OnWheelMove(self, iLen):
		pos = self.GetPos()

		## Computing mouse move range (by percent)
		iLen = (float(abs(iLen)-100)/100.0)*(iLen/abs(iLen))

		## Mouse Inversion
		iLen *= -1

		pos += iLen
		self.SetPos(pos)
		return True

class NewScrollBar(Window):

	SCROLLBAR_WIDTH = 13
	SCROLLBAR_MIDDLE_HEIGHT = 1
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	SCROLL_BTN_XDIST = 1
	SCROLL_BTN_YDIST = 2

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

			self.SetWindowName("NONAME_ScrollBar_MiddleBar")

		def MakeImage(self):
			top = ImageBox()
			top.SetParent(self)
			top.LoadImage("d:/ymir work/ui/pattern/slimscroll/ScrollBar_Middle_Top_bottom.tga")
			top.AddFlag("not_pick")
			top.SetPosition(0, 0)
			top.Show()
			topScale = ExpandedImageBox()
			topScale.SetParent(self)
			topScale.SetPosition(0, top.GetHeight())
			topScale.LoadImage("d:/ymir work/ui/pattern/slimscroll/ScrollBar_Middle_TopScale.tga")
			topScale.AddFlag("not_pick")
			topScale.Show()

			bottom = ImageBox()
			bottom.SetParent(self)
			bottom.LoadImage("d:/ymir work/ui/pattern/slimscroll/ScrollBar_Middle_Top_bottom.tga")
			bottom.AddFlag("not_pick")
			bottom.Show()
			bottomScale = ExpandedImageBox()
			bottomScale.SetParent(self)
			bottomScale.LoadImage("d:/ymir work/ui/pattern/slimscroll/ScrollBar_Middle_TopScale.tga")
			bottomScale.AddFlag("not_pick")
			bottomScale.Show()

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/ui/pattern/slimscroll/ScrollBar_Middle_Middle.tga")
			middle.AddFlag("not_pick")
			middle.Show()

			self.top = top
			self.topScale = topScale
			self.bottom = bottom
			self.bottomScale = bottomScale
			self.middle = middle

		def SetSize(self, height):
			minHeight = self.top.GetHeight() + self.bottom.GetHeight() + self.middle.GetHeight()
			height = max(minHeight, height)
			DragButton.SetSize(self, 10, height)

			scale = (height - minHeight) / 2
			extraScale = 0
			if (height - minHeight) % 2 == 1:
				extraScale = 1

			self.topScale.SetRenderingRect(0, 0, 0, scale - 1)
			self.middle.SetPosition(0, self.top.GetHeight() + scale)
			self.bottomScale.SetPosition(0, self.middle.GetBottom())
			self.bottomScale.SetRenderingRect(0, 0, 0, scale - 1 + extraScale)
			self.bottom.SetPosition(0, height - self.bottom.GetHeight())

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.eventArgs = None
		self.lockFlag = False

		self.CreateScrollBar()
		self.SetScrollBarSize(0)

		self.scrollStep = 0.20
		self.SetWindowName("NONAME_ScrollBar")

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		middleImage = ExpandedImageBox()
		middleImage.SetParent(self)
		middleImage.AddFlag("not_pick")
		middleImage.SetPosition(0, 1)
		middleImage.LoadImage("d:/ymir work/ui/pattern/slimscroll/SlimScrollBar_Middle.tga")
		middleImage.Show()
		self.middleImage = middleImage

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(0) # set min height
		self.middleBar = middleBar

	def Destroy(self):
		self.eventScroll = None
		self.eventArgs = None

	def SetScrollEvent(self, event, *args):
		self.eventScroll = event
		self.eventArgs = args

	def SetMiddleBarSize(self, pageScale):
		self.middleBar.SetSize(int(pageScale * float(self.GetHeight() - self.SCROLL_BTN_YDIST*2)))
		realHeight = self.GetHeight() - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()
		self.pageSize = realHeight

	def SetScrollBarSize(self, height):
		self.SetSize(self.SCROLLBAR_WIDTH, height)

		self.pageSize = height - self.SCROLL_BTN_YDIST*2 - self.middleBar.GetHeight()

		middleImageScale = float((height - self.SCROLL_BTN_YDIST*2) - self.middleImage.GetHeight()) / float(self.middleImage.GetHeight())
		self.middleImage.SetRenderingRect(0, 0, 0, middleImageScale)

		self.middleBar.SetRestrictMovementArea(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST, \
			self.middleBar.GetWidth(), height - self.SCROLL_BTN_YDIST * 2)
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, self.SCROLL_BTN_YDIST)

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def GetPos(self):
		return self.curPos

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def SetPos(self, pos, moveEvent = True):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.SCROLL_BTN_XDIST, int(newPos) + self.SCROLL_BTN_YDIST)
		if moveEvent == True:
			self.OnMove()

	def OnMove(self):
		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLL_BTN_YDIST) / float(self.pageSize)

		if self.eventScroll:
			apply(self.eventScroll, self.eventArgs)

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		newPos = float(yMouseLocalPosition) / float(self.GetHeight())
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

	## ScrollBar Wheel Support
	def OnWheelMove(self, iLen):
		pos = self.GetPos()

		## Computing mouse move range (by percent)
		iLen = (float(abs(iLen)-100)/100.0)*(iLen/abs(iLen))

		## Mouse Inversion
		iLen *= -1

		pos += iLen
		self.SetPos(pos)
		return True

def MakeNewScrollBar2(parent, x, y, height):
	scrollbar = NewScrollBar()
	scrollbar.SetParent(parent)
	scrollbar.SetPosition(x, y)
	scrollbar.SetScrollBarSize(height)
	scrollbar.Show()
	return scrollbar

class NewScrollBar2(Window):
	SCROLLBAR_WIDTH = 17
	SCROLLBAR_MIDDLE_HEIGHT = 9
	SCROLLBAR_BUTTON_WIDTH = 17
	SCROLLBAR_BUTTON_HEIGHT = 17
	MIDDLE_BAR_POS = 0
	MIDDLE_BAR_UPPER_PLACE = 3
	MIDDLE_BAR_DOWNER_PLACE = 4
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

		def MakeImage(self):

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage("d:/ymir work/ui/pattern/new_scroll/scrollbar_middle.tga")
			middle.SetPosition(0, 0)
			middle.AddFlag("not_pick")
			middle.Show()

			self.middle = middle

		def SetSize(self, height):
			height = max(12, height)
			DragButton.SetSize(self, 10, height)

			height -= 4*3
			self.middle.SetRenderingRect(0, 0, 0, float(height)/4.0)

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = False
		self.scrollStep = 0.20

		self.eventFuncCall = True

		self.CreateScrollBar()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		barSlot = ExpandedImageBox()
		barSlot.SetParent(self)
		barSlot.LoadImage("d:/ymir work/ui/pattern/new_scroll/base_scroll.tga")
		barSlot.AddFlag("not_pick")
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage()
		middleBar.SetSize(12)
		
		self.middleBar = middleBar
		self.barSlot = barSlot

		self.SCROLLBAR_WIDTH = self.middleBar.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.middleBar.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.middleBar.GetHeight()

	def Destroy(self):
		self.middleBar = None
		self.eventScroll = lambda *arg: None

		self.eventFuncCall	= True

	def SetEvnetFuncCall(self, callable):
		self.eventFuncCall = callable

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2
		self.SCROLLBAR_MIDDLE_HEIGHT = int(pageScale * float(realHeight))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlot.SetPosition(0, self.SCROLLBAR_BUTTON_HEIGHT)
		height =  - self.SCROLLBAR_BUTTON_HEIGHT*2 - 2
		new_height = float(self.GetHeight()) / float(self.barSlot.GetHeight())
		self.barSlot.SetRenderingRect(0.0, 0.0, 0.0, new_height - 2.8)

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos, event_callable = True):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)

		self.OnMove(event_callable)

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep, self.eventFuncCall)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep, self.eventFuncCall)

	def OnMove(self, event_callable = True):
		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		if event_callable:
			self.eventScroll()

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

	def RunMouseWheel(self, nLen):
		if nLen > 0:
			self.OnUp()
		else:
			self.OnDown()

class ScrollBarTemplate(Window):

	MIDDLE_BAR_POS = 5
	MIDDLE_BAR_UPPER_PLACE = 2
	MIDDLE_BAR_DOWNER_PLACE = 2
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(DragButton):
		def __init__(self):
			self.middle = None
			DragButton.__init__(self)
			self.AddFlag("movable")

		def MakeImage(self, img):
			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage(img)
			middle.SetPosition(0, 0)
			middle.AddFlag("not_pick")
			middle.Show()
			self.middle = middle
			self.SetSize(self.GetHeight())

		def SetSize(self, height):
			height = max(12, height)
			if self.middle:
				DragButton.SetSize(self, self.middle.GetWidth(), height)
				val = 0
				if self.middle.GetHeight() != 0:
					val = float(height)/self.middle.GetHeight()
				self.middle.SetRenderingRect(0, 0, 0, -1.0 + val)
			else:
				DragButton.SetSize(self, self.GetWidth(), height)

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.eventArgs = None
		self.lockFlag = False

		self.SCROLLBAR_WIDTH = 0
		self.SCROLLBAR_BUTTON_WIDTH = 0
		self.SCROLLBAR_BUTTON_HEIGHT = 0
		self.SCROLLBAR_MIDDLE_HEIGHT = 0

		self.CreateScrollBar()

		self.scrollStep = 0.20

	def SetUpButton(self, upVisual, overVisual, downVisual):
		self.upButton.SetUpVisual(upVisual)
		self.upButton.SetOverVisual(overVisual)
		self.upButton.SetDownVisual(downVisual)
		self.upButton.Show()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight() + 3

	def SetDownButton(self, upVisual, overVisual, downVisual):
		self.downButton.SetUpVisual(upVisual)
		self.downButton.SetOverVisual(overVisual)
		self.downButton.SetDownVisual(downVisual)
		self.downButton.Show()

	def SetMiddleImage(self, img):
		self.middleBar.MakeImage(img)
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.MIDDLE_BAR_POS = (self.SCROLLBAR_WIDTH - self.middleBar.GetWidth()) / 2

	def SetBarPartImages(self, topImg, centerImg, bottomImg):
		self.barTopImage.LoadImage(topImg)
		self.barTopImage.Show()
		self.barCenterImage.LoadImage(centerImg)
		self.barCenterImage.SetPosition(0, self.barTopImage.GetHeight())
		self.barCenterImage.Show()
		self.barBottomImage.LoadImage(bottomImg)
		self.barBottomImage.Show()
		self.SCROLLBAR_WIDTH = max(self.barTopImage.GetWidth(), self.SCROLLBAR_WIDTH)
		self.MIDDLE_BAR_POS = (self.SCROLLBAR_WIDTH - self.middleBar.GetWidth()) / 2

	def SetBarImage(self, img):
		self.barImage.LoadImage(img)
		self.barImage.Show()
		self.SCROLLBAR_WIDTH = max(self.barImage.GetWidth(), self.SCROLLBAR_WIDTH)
		self.MIDDLE_BAR_POS = (self.SCROLLBAR_WIDTH - self.middleBar.GetWidth()) / 2

	def CreateScrollBar(self):
		barImage = ExpandedImageBox()
		barImage.SetParent(self)
		barImage.AddFlag("not_pick")
		barImage.Hide()

		barTopImage = ImageBox()
		barTopImage.SetParent(self)
		barTopImage.AddFlag("not_pick")
		barTopImage.Hide()

		barCenterImage = ExpandedImageBox()
		barCenterImage.SetParent(self)
		barCenterImage.AddFlag("not_pick")
		barCenterImage.Hide()

		barBottomImage = ImageBox()
		barBottomImage.SetParent(self)
		barBottomImage.AddFlag("not_pick")
		barBottomImage.Hide()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.SetSize(12)

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.SetWindowHorizontalAlignCenter()
		upButton.Hide()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.SetWindowHorizontalAlignCenter()
		downButton.Hide()

		self.upButton = upButton
		self.downButton = downButton
		self.middleBar = middleBar
		self.barImage = barImage
		self.barTopImage = barTopImage
		self.barCenterImage = barCenterImage
		self.barBottomImage = barBottomImage

	def Destroy(self):
		self.middleBar = None
		self.upButton = None
		self.downButton = None
		self.barImage = None
		self.barTopImage = None
		self.barCenterImage = None
		self.barBottomImage = None
		self.eventScroll = None
		self.eventArgs = None

	def SetScrollEvent(self, event, *args):
		self.eventScroll = event
		self.eventArgs = args

	# ------------------------------------------------------------------------------------------

	# Important: pageScale must be float! so parse the values to float before you use them.
	# Otherwise it simply won't work or the bar is gonna be very small

	# ------------------------------------------------------------------------------------------

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2
		self.SCROLLBAR_MIDDLE_HEIGHT = max(12, int(pageScale * float(realHeight)))
		self.middleBar.SetSize(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.upButton.SetPosition(0, 3)
		self.downButton.SetPosition(0, height - self.SCROLLBAR_BUTTON_HEIGHT)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.middleBar.GetWidth(), height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

		self.UpdateBarImage()
		self.upButton.UpdateRect()
		self.downButton.UpdateRect()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def UpdateBarImage(self):
		if self.barImage.IsShow():
			val = 0

			if self.barImage.GetHeight() != 0:
				val = self.GetHeight() / float(self.barImage.GetHeight())

			self.barImage.SetRenderingRect(0.0, 0.0, 0.0, -1.0 + val)

		if self.barCenterImage.IsShow():
			centerHeight = self.GetHeight() - (self.barTopImage.GetHeight() + self.barBottomImage.GetHeight())

			val = 0

			if self.barCenterImage.GetHeight() != 0:
				val = (centerHeight / float(self.barCenterImage.GetHeight()))

			self.barCenterImage.SetRenderingRect(0.0, 0.0, 0.0, -1.0 + val)

		if self.barBottomImage.IsShow():
			self.barBottomImage.SetPosition(0, self.GetHeight() - self.barBottomImage.GetHeight())

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos

		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def OnMove(self):

		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()

		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		if self.eventScroll:
			apply(self.eventScroll, self.eventArgs)

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()

		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
		newPos = float(pickedPos) / float(self.pageSize)

		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

	## ScrollBar Wheel Support
	def OnWheelMove(self, iLen):
		pos = self.GetPos()

		## Computing mouse move range (by percent)
		iLen = (float(abs(iLen)-100)/100.0)*(iLen/abs(iLen))

		## Mouse Inversion
		iLen *= -1

		pos += iLen
		self.SetPos(pos)
		return True

class SlimScrollBar(Window):
	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")
			self.barColor = None
			self.barColorOver = None
			self.isDragging = False

			self.baseWidth = 0

		def MakeImage(self, barColor, barColorOver = None):
			middleBar = Bar()
			middleBar.SetParent(self)
			middleBar.AddFlag("not_pick")
			middleBar.SetPosition(0, 0)
			middleBar.SetColor(barColor)
			middleBar.Show()
			self.middleBar = middleBar


			self.barColor = barColor
			self.barColorOver = barColorOver

		def SetSize(self, width, height):
			if not self.baseWidth:
				self.baseWidth = width

			DragButton.SetSize(self, width, height)

			if self.middleBar:
				self.middleBar.SetSize(width, height)

		def DownEvent(self):
			self.isDragging = True

		def CallEvent(self):
			self.isDragging = False
			if not self.IsIn():
				if self.middleBar and self.barColor:
					self.middleBar.SetColor(self.barColor)

		def OnMouseOverIn(self):
			if self.middleBar and self.barColorOver:
				self.middleBar.SetColor(self.barColorOver)

		def OnMouseOverOut(self):
			if self.middleBar and self.barColor and not self.isDragging:
				self.middleBar.SetColor(self.barColor)

	def __init__(self):
		Window.__init__(self)

		self.tHeight = 0
		self.mbHeight = 0
		self.scrollStep = 0.20
		self.curPos = 0.0

		self.scrollBarWidth = 4

		self.eventScroll = lambda *arg: None

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self, bgColor, middleColor, middleColorOver = None):
		barSlot = Bar()
		barSlot.SetParent(self)
		barSlot.AddFlag("not_pick")
		barSlot.SetColor(bgColor)
		barSlot.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.MakeImage(middleColor, middleColorOver)

		self.middleBar = middleBar
		self.barSlot = barSlot

	def Destroy(self):
		self.middleBar = None
		self.barSlot = None

		self.tHeight = 0
		self.mbHeight = 0
		self.scrollStep = 0.20
		self.curPos = 0.0

		self.eventScroll = lambda *arg: None

	def SetScrollWidth(self, width):
		self.scrollBarWidth = width

	def SetBgSize(self, height):
		self.SetSize(self.scrollBarWidth, height)

		if self.barSlot:
			self.barSlot.SetSize(self.scrollBarWidth, height)

		if self.middleBar:
			self.middleBar.SetRestrictMovementArea(0, 0, self.scrollBarWidth, height)

		self.tHeight = height

	def SetMiddleSize(self, height):
		if self.middleBar:
			self.middleBar.SetSize(self.scrollBarWidth, height)

		self.mbHeight = height

	def SetMiddleBlurColor(self, r, g, b, a):
		if self.middleBar:
			self.middleBar.SetOverEffectColor(r, g, b, a)

	def OnMove(self):
		if self.tHeight == self.mbHeight:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal) / float(self.tHeight - self.mbHeight)

		self.curPos = max(0.0, self.curPos)
		self.curPos = min(1.0, self.curPos)

		self.eventScroll()

	def GetPos(self):
		return self.curPos

	def GetBgSize(self):
		return self.tHeight

	def GetMiddleSize(self):
		return self.mbHeight

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		self.middleBar.SetPosition(self.scrollBarWidth, int(pos * int(self.tHeight - self.mbHeight)))
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos - self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos + self.scrollStep)

	## ScrollBar Wheel Support
	def OnWheelMove(self, iLen):
		pos = self.GetPos()

		## Computing mouse move range (by percent)
		iLen = (float(abs(iLen)-100)/100.0)*(iLen/abs(iLen))

		## Mouse Inversion
		iLen *= -1

		pos += iLen
		self.SetPos(pos)
		return True

class ModernScrollBar(Window):
	MIDDLE_BAR_POS = 2
	MIDDLE_BAR_UPPER_PLACE = 1
	MIDDLE_BAR_DOWNER_PLACE = 1
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE

	class MiddleBar(DragButton):
		BUTTON_COLOR = grp.GenerateColor(0.4, 0.4, 0.4, 1.0)
		BUTTON_ACTIVE_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

			self.bar = Bar()

		def MakeImage(self):
			self.bar = Bar()
			self.bar.SetParent(self)
			self.bar.SetPosition(0, 0)
			self.bar.SetSize(10, 0)
			self.bar.SetColor(self.BUTTON_COLOR)
			self.bar.AddFlag("not_pick")
			self.bar.Show()

		def OnMouseOverIn(self):
			self.bar.SetColor(self.BUTTON_ACTIVE_COLOR)

		def OnMouseOverOut(self):
			self.bar.SetColor(self.BUTTON_COLOR)

		def SetSize(self, width, height):
			height = max(12, height)
			DragButton.SetSize(self, width, height)
			self.bar.SetSize(width, height)

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = lambda *arg: None
		self.lockFlag = False
		self.scrollStep = 0.20
		self.contentHeight = 0

		self.CreateScrollBar()

	def __del__(self):
		Window.__del__(self)

	def CreateScrollBar(self):
		self.SetSize(10, 0)

		self.barSlot = BoxedBoard()
		self.barSlot.SetParent(self)
		self.barSlot.AddFlag("not_pick")
		self.barSlot.Show()

		self.middleBar = self.MiddleBar()
		self.middleBar.SetParent(self)
		self.middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		self.middleBar.Show()
		self.middleBar.MakeImage()
		self.middleBar.SetSize(self.GetWidth() - 2, 12)

	def Destroy(self):
		self.barSlot = None
		self.middleBar = None
		self.eventScroll = lambda *arg: None

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def __SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - 2
		self.middleBar.SetSize(self.GetWidth() - 2, int(pageScale * float(realHeight)))
		self.pageSize = self.GetHeight() - self.middleBar.GetHeight() - self.TEMP_SPACE

	# Deprecated, just refresh the middle bar size in case anything changed.
	def SetMiddleBarSize(self, tmp):
		self.SetContentHeight(self.contentHeight)

	def SetContentHeight(self, contentHeight):
		contentHeight = max(contentHeight, self.GetHeight() - self.TEMP_SPACE)
		self.contentHeight = contentHeight
		self.__SetMiddleBarSize(float(self.GetHeight() - 2) / float(contentHeight))

	def SetScrollBarSize(self, height):
		self.pageSize = height - self.middleBar.GetHeight() - self.TEMP_SPACE
		self.SetSize(self.GetWidth(), height)
		self.middleBar.SetRestrictMovementArea(1, self.MIDDLE_BAR_UPPER_PLACE, self.middleBar.GetWidth(), height - self.TEMP_SPACE)
		self.middleBar.SetPosition(1, self.MIDDLE_BAR_UPPER_PLACE)

		self.UpdateBarSlot()

	def UpdateBarSlot(self):
		self.barSlot.SetSize(self.GetWidth(), self.GetHeight())

	def SetWidth(self, width):
		self.SetSize(width, self.GetHeight())
		self.middleBar.SetSize(width - 2, self.middleBar.GetHeight())
		self.SetScrollBarSize(self.GetHeight())

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def OnMove(self):
		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		self.eventScroll(self.curPos)

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - (self.middleBar.GetHeight() / 2)
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = True

	def UnlockScroll(self):
		self.lockFlag = False

	def OnWheelMove(self, len):
		curY = int(self.GetPos() * float(self.contentHeight)) - len
		self.SetPos(float(curY) / float(self.contentHeight))
		return True

class ThinScrollBar(ScrollBar):

	def CreateScrollBar(self):
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_01.sub")
		middleBar.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_02.sub")
		middleBar.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_middle_button_03.sub")

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_up_button_03.sub")
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_thin_down_button_03.sub")
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.Show()

		self.middleBar = middleBar
		self.upButton = upButton
		self.downButton = downButton

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		self.MIDDLE_BAR_POS = 0
		self.MIDDLE_BAR_UPPER_PLACE = 0
		self.MIDDLE_BAR_DOWNER_PLACE = 0
		self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		pass

class SmallThinScrollBar(ScrollBar):

	def CreateScrollBar(self):
		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()
		middleBar.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")
		middleBar.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")
		middleBar.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_middle_button_01.sub")

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_up_button_03.sub")
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetUpVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/scrollbar_small_thin_down_button_03.sub")
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.Show()

		self.middleBar = middleBar
		self.upButton = upButton
		self.downButton = downButton

		self.SCROLLBAR_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()
		self.MIDDLE_BAR_POS = 0
		self.MIDDLE_BAR_UPPER_PLACE = 0
		self.MIDDLE_BAR_DOWNER_PLACE = 0
		self.TEMP_SPACE = 0

	def UpdateBarSlot(self):
		pass

class ExpensiveScrollBar(Window):
	def __init__(self, path, scroll_image, scroll_cursor_image):
		Window.__init__(self)
		self.mPos = 0.0
		self.eventScroll = lambda *arg: None
		self.disable = False
		self.__LoadWindow(path, scroll_image, scroll_cursor_image)

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		self.mPos = 0.0
		self.eventScroll = None
		self.disable = False

	def	__LoadWindow(self, path, scroll_image, scroll_cursor_image):
		## ScrollBarBase
		self.ScrollBarBase = ExpandedImageBox()
		self.ScrollBarBase.SetParent(self)
		self.ScrollBarBase.SetPosition(0, 0)
		self.ScrollBarBase.LoadImage(path+scroll_image)
		self.ScrollBarBase.SetClickEvent(self.__OnMove_Base)
		self.ScrollBarBase.Show()

		## Size
		self.SetSize(self.ScrollBarBase.GetWidth(), self.ScrollBarBase.GetHeight())

		## ScrollCursor
		self.ScrollCursor = DragButton()
		self.ScrollCursor.SetParent(self)
		self.ScrollCursor.SetUpVisual(path+scroll_cursor_image)
		self.ScrollCursor.SetOverVisual(path+scroll_cursor_image)
		self.ScrollCursor.SetDownVisual(path+scroll_cursor_image)
		self.ScrollCursor.SetPosition(0, 0)
		self.ScrollCursor.TurnOnCallBack()
		self.ScrollCursor.SetMoveEvent(__mem_func__(self.__OnMove))
		self.ScrollCursor.SetRestrictMovementArea(0, 0, self.ScrollCursor.GetWidth(), self.GetHeight())
		self.ScrollCursor.Show()

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def	SetPos(self, pos):
		if self.disable:
			return

		self.mPos = pos
		self.__OnMove_Base(0, 0)

	def GetPos(self):
		return self.mPos

	def	Display(self, bShow):
		self.ScrollCursor.Show()

	def	Disable(self):
		self.disable = True
		self.ScrollCursor.SetRestrictMovementArea(0, 0, self.ScrollCursor.GetWidth(), self.ScrollCursor.GetHeight())

	def	Enable(self):
		self.disable = False
		self.ScrollCursor.SetRestrictMovementArea(0, 0, self.ScrollCursor.GetWidth(), self.GetHeight())

	def	__OnMove_Base(self, x_f = -1, y_f = -1):
		if x_f == -1 and y_f == -1:
			(x, y) = self.GetMouseLocalPosition()
		else:
			(x, y) = (x_f, y_f)

		self.__OnMove()
		self.ScrollCursor.SetPosition(0, min(y, self.GetHeight()-self.ScrollCursor.GetHeight()))

	def	__OnMove(self):
		if self.disable:
			return

		(x, y) = self.GetMouseLocalPosition()
		self.mPos = float(min(max(0, y), self.GetHeight()))/float(self.GetHeight())
		self.eventScroll()

	## ScrollBar Wheel Support
	def OnWheelMove(self, iLen):
		if self.disable:
			return

		y = self.ScrollCursor.GetHeight()
		## Computing mouse move range (by percent)
		iLen = (float(abs(iLen)-100)/100.0)*(iLen/abs(iLen))

		## Mouse Inversion
		iLen *= -1

		## Recomputation
		self.mPos += iLen
		self.mPos = float(min(max(0.0, self.mPos), 1.0))

		## Scroll Cursor pos
		self.ScrollCursor.SetPosition(0, max(0, min(self.mPos*(self.GetHeight()-self.ScrollCursor.GetHeight()), self.GetHeight()-self.ScrollCursor.GetHeight())))

		self.eventScroll()
		return True

class SliderBar(Window):

	def __init__(self):
		Window.__init__(self)

		self.curPos = 1.0
		self.pageSize = 1.0
		self.eventChange = None

		self.backGroundImage = None
		self.cursor = None

		self.CreateBackGroundImage()
		self.CreateCursor()

	def __del__(self):
		Window.__del__(self)

	def CreateBackGroundImage(self, image = "d:/ymir work/ui/game/windows/sliderbar.sub"):
		if self.backGroundImage:
			self.backGroundImage.Hide()
			del self.backGroundImage

		img = ImageBox()
		img.SetParent(self)
		img.LoadImage(image)
		img.Show()
		self.backGroundImage = img

		##
		self.SetSize(self.backGroundImage.GetWidth(), self.backGroundImage.GetHeight())

	def CreateCursor(self, image = "d:/ymir work/ui/game/windows/sliderbar_cursor.sub"):
		if self.cursor:
			self.cursor.Hide()
			del self.cursor

		cursor = DragButton()
		cursor.AddFlag("movable")
		cursor.AddFlag("restrict_y")
		cursor.SetParent(self)
		cursor.SetMoveEvent(self.__OnMove)
		cursor.SetUpVisual(image)
		cursor.SetOverVisual(image)
		cursor.SetDownVisual(image)
		cursor.Show()
		self.cursor = cursor

		self.SetSize(self.backGroundImage.GetWidth(), max(self.backGroundImage.GetHeight(), self.cursor.GetHeight()))
		if cursor.GetHeight() > self.backGroundImage.GetHeight():
			self.backGroundImage.SetPosition(0, (cursor.GetHeight() - self.backGroundImage.GetHeight()) / 2)

		##
		self.cursor.SetRestrictMovementArea(0, 0, self.backGroundImage.GetWidth(), 0)
		self.pageSize = self.backGroundImage.GetWidth() - self.cursor.GetWidth()

	def __OnMove(self):
		(xLocal, yLocal) = self.cursor.GetLocalPosition()
		self.curPos = float(xLocal) / float(self.pageSize)

		if self.eventChange:
			self.eventChange()

	def SetSliderPos(self, pos):
		self.curPos = pos
		self.cursor.SetPosition(int(self.pageSize * pos), 0)

	def GetSliderPos(self):
		return self.curPos

	def SetEvent(self, event):
		self.eventChange = event

	def Enable(self):
		self.cursor.Show()

	def Disable(self):
		self.cursor.Hide()

class ListBox(Window):

	def GetSelectedItemText(self):
		return self.textDict.get(self.selectedLine, "")

	TEMPORARY_PLACE = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.overLine = -1
		self.overTempLine = -1
		self.selectedLine = -1
		self.width = 0
		self.height = 0
		self.stepSize = 17
		self.basePos = 0
		self.showLineCount = 0
		self.itemCenterAlign = True
		self.drawBorder = False
		self.itemList = []
		self.keyDict = {}
		self.textDict = {}
		self.event = lambda *arg: None
		self.doubleClickEvent = lambda * arg: None

		self.lastMousePos = (-1, -1)

		self.SetWindowName("NONAME_ListBox")

	def __del__(self):
		Window.__del__(self)

	def GetStepSize(self):
		return self.stepSize

	def SetWidth(self, width):
		self.SetSize(width, self.height)

	def SetDrawBorder(self, flag):
		self.drawBorder = flag

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height

	def SetTextCenterAlign(self, flag):
		self.itemCenterAlign = flag

	def SetBasePos(self, pos):
		self.basePos = pos
		self._LocateItem()

	def GetBasePos(self):
		return self.basePos

	def ClearItem(self):
		self.keyDict = {}
		self.textDict = {}
		self.itemList = []
		self.overLine = -1
		self.overTempLine = -1
		self.selectedLine = -1

	def HasItem(self, number):
		for i in self.keyDict:
			if self.keyDict[i] == number:
				return True

		return False

	def EraseItem(self, number):
		for i in self.keyDict:
			if self.keyDict[i] == number:
				for j in xrange(number, len(self.itemList) - 1):
					self.keyDict[j] = self.keyDict[j + 1]
					self.textDict[j] = self.textDict[j + 1]

				del self.keyDict[len(self.itemList) - 1]
				del self.textDict[len(self.itemList) - 1]
				del self.itemList[i]

				maxBasePos = max(self.GetItemCount() - self.GetViewItemCount(), 0)
				if self.basePos > maxBasePos:
					self.SetBasePos(maxBasePos)
				else:
					self.LocateItem()

				return True

		return False

	def InsertItem(self, number, text):
		self.keyDict[len(self.itemList)] = number
		self.textDict[len(self.itemList)] = text

		textLine = TextLine()
		textLine.SetParent(self)
		textLine.SetText(text)
		textLine.Show()

		if self.itemCenterAlign:
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()

		self.itemList.append(textLine)

		self._LocateItem()

	def ChangeItem(self, number, text):
		for key, value in self.keyDict.items():
			if value == number:
				self.textDict[key] = text

				if number < len(self.itemList):
					self.itemList[key].SetText(text)

				return

	def LocateItem(self):
		self._LocateItem()

	def _LocateItem(self):

		skipCount = self.basePos
		yPos = 0
		self.showLineCount = 0

		for textLine in self.itemList:
			textLine.Hide()

			if skipCount > 0:
				skipCount -= 1
				continue

			textLine.SetPosition(0, yPos + 3)
			yPos += self.stepSize

			if yPos <= self.GetHeight():
				self.showLineCount += 1
				textLine.Show()

	def ArrangeItem(self):
		self.SetSize(self.width, len(self.itemList) * self.stepSize)
		self._LocateItem()

	def GetViewItemCount(self):
		return int(self.GetHeight() / self.stepSize)

	def GetItemCount(self):
		return len(self.itemList)

	def SetEvent(self, event):
		self.event = event

	def SetDoubleClickEvent(self, event):
		self.doubleClickEvent = event

	def SelectItem(self, line):

		if not self.keyDict.has_key(line):
			return

		if line == self.selectedLine:
			return

		self.selectedLine = line
		self.event(self.keyDict.get(line, 0), self.textDict.get(line, "None"))

	def GetSelectedItem(self, defaultVal = 0):
		return self.keyDict.get(self.selectedLine, defaultVal)

	def GetSelectedLine(self):
		return self.selectedLine

	def OnMouseLeftButtonDown(self):
		if self.overLine < 0:
			return

	def ResetSelected(self):
		self.selectedLine = -1

	def OnMouseLeftButtonUp(self):
		if self.overLine >= 0:
			self.SelectItem(self.overLine+self.basePos)

	def OnMouseLeftButtonDoubleClick(self):
		if self.overLine < 0:
			return

		if self.doubleClickEvent:
			try:
				self.doubleClickEvent(self.keyDict.get(self.overLine, 0))
			except TypeError:
				self.doubleClickEvent(self.keyDict.get(self.overLine, 0), self.textDict.get(self.overLine, "None"))

	def IsOverLine(self):
		return self.overLine != -1

	def GetOverLineIdx(self):
		if self.overLine == -1:
			return self.overTempLine

		return self.overLine

	def SetOverLineIdx(self, idx):
		self.overLine = -1
		self.overTempLine = idx

	def GetOverLine(self, defaultVal = 0):
		if self.IsOverLine():
			return self.keyDict.get(self.GetOverLineIdx()+self.basePos, defaultVal)

		return defaultVal

	def OnUpdate(self):
		if self.IsIn():
			x, y = self.GetGlobalPosition()
			height = self.GetHeight()
			xMouse, yMouse = wndMgr.GetMousePosition()

			if self.lastMousePos[0] == xMouse and self.lastMousePos[1] == yMouse:
				return
			self.lastMousePos = (xMouse, yMouse)

			self.overLine = -1
			if yMouse - y < height - 1:
				self.overLine = (yMouse - y) / self.stepSize

				if self.overLine < 0:
					self.overLine = -1
				elif self.overLine >= len(self.itemList):
					self.overLine = -1
				else:
					self.overTempLine = -1

		else:
			self.overLine = -1

	def OnRender(self):
		xRender, yRender = self.GetGlobalPosition()
		yRender -= self.TEMPORARY_PLACE
		widthRender = self.width
		heightRender = self.height + self.TEMPORARY_PLACE*2

		overLine = self.GetOverLineIdx()
		if -1 != overLine:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + overLine*self.stepSize + 4, self.width - 3, self.stepSize)

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(SELECT_COLOR)
					grp.RenderBar(xRender + 2, yRender + (self.selectedLine-self.basePos)*self.stepSize + 4, self.width - 3, self.stepSize)

class ListBox2(ListBox):
	def __init__(self, *args, **kwargs):
		ListBox.__init__(self, *args, **kwargs)
		self.rowCount = 10
		self.barWidth = 0
		self.colCount = 0

	def SetRowCount(self, rowCount):
		self.rowCount = rowCount

	def SetSize(self, width, height):
		ListBox.SetSize(self, width, height)
		self._RefreshForm()

	def ClearItem(self):
		ListBox.ClearItem(self)
		self._RefreshForm()

	def InsertItem(self, *args, **kwargs):
		ListBox.InsertItem(self, *args, **kwargs)
		self._RefreshForm()

	def OnUpdate(self):
		mpos = wndMgr.GetMousePosition()
		self.overLine = self._CalcPointIndex(mpos)

	def OnRender(self):
		x, y = self.GetGlobalPosition()
		pos = (x + 2, y)

		if -1 != self.overLine:
			grp.SetColor(HALF_WHITE_COLOR)
			self._RenderBar(pos, self.overLine)

		if -1 != self.selectedLine:
			if self.selectedLine >= self.basePos:
				if self.selectedLine - self.basePos < self.showLineCount:
					grp.SetColor(SELECT_COLOR)
					self._RenderBar(pos, self.selectedLine-self.basePos)



	def _CalcPointIndex(self, mpos):
		if self.IsIn():
			px, py = mpos
			gx, gy = self.GetGlobalPosition()
			lx, ly = px - gx, py - gy

			col = lx / self.barWidth
			row = ly / self.stepSize
			idx = col * self.rowCount + row
			if col >= 0 and col < self.colCount:
				if row >= 0 and row < self.rowCount:
					if idx >= 0 and idx < len(self.itemList):
						return idx

		return -1

	def _CalcRenderPos(self, pos, idx):
		x, y = pos
		row = idx % self.rowCount
		col = idx / self.rowCount
		return (x + col * self.barWidth, y + row * self.stepSize)

	def _RenderBar(self, basePos, idx):
		x, y = self._CalcRenderPos(basePos, idx)
		grp.RenderBar(x, y, self.barWidth - 3, self.stepSize)

	def _LocateItem(self):
		pos = (0, self.TEMPORARY_PLACE)

		self.showLineCount = 0
		for textLine in self.itemList:
			x, y = self._CalcRenderPos(pos, self.showLineCount)
			textLine.SetPosition(x, y)
			textLine.Show()

			self.showLineCount += 1

	def _RefreshForm(self):
		if len(self.itemList) % self.rowCount:
			self.colCount = len(self.itemList) / self.rowCount + 1
		else:
			self.colCount = len(self.itemList) / self.rowCount

		if self.colCount:
			self.barWidth = self.width / self.colCount
		else:
			self.barWidth = self.width

class CustomScrollBar(Window):



	HORIZONTAL 	= 1
	VERTICAL	= 2

	BOTTOM		= 1
	TOP			= 2
	RIGHT		= 3
	LEFT		= 4


	def __init__(self, template):
		Window.__init__(self)

		self.baseImage = None
		self.button1 = None
		self.button2 = None
		self.middleButton = None

		self.onScroll = None
		self.parent = None
		self.orientation = 0
		self.pos = 0.0
		self.middleScale = 0.1
		self.step = 0.1

		self.baseInfo = {}
		self.mouseOffset = {}


		base	= template.get('base', 			"")
		button1 = template.get('button1', 		{})
		button2 = template.get('button2', 		{})
		middle	= template.get('middle', 		{})
		onscroll= template.get('onscroll', 		None)
		orient	= template.get('orientation',	0)
		align	= template.get('align',			{})
		parent	= template.get('parent',		None)
		position= template.get('position',		{})

		if not base or not button1 or not button2 or not middle or not onscroll or not orient or not parent:
			dbg.TraceError("CustomScrollBar : cannot set template [%s]"%str(template))
			return

		self.__SetParent(parent)
		self.__SetOrientation(orient)
		self.__LoadBaseImage(base)
		# self.__LoadButton1(button1)
		# self.__LoadButton2(button2)
		self.__LoadMiddleButton(middle)

		self.__SetOnScrollEvent(onscroll)
		if template.has_key('align'):
			self.__SetAlign(align)

		elif template.has_key('position'):
			self.__SetPosition(position)

	def __SetParent(self, parent):
		if parent:
			self.parent = parent
			self.SetParent(parent)

	def __SetOrientation(self, orient):
		self.orientation = orient

	def __LoadBaseImage(self, base):
		bg = ExpandedImageBox()
		bg.LoadImage(base)
		bg.SetParent(self)
		bg.SetPosition(0,0)
		bg.Show()

		w , h = (bg.GetWidth() , bg.GetHeight())

		self.baseInfo = {'base' : {'width':w, 'height':h,}}
		self.SetSize(w,h)

		bg.OnMouseLeftButtonDown = self.__OnClickBaseImage
		self.baseImage = bg

	# def __LoadButton1(self, button1):
	# 	button1['event'] = self.__OnClickButton1

	# 	btn = ExpandedButton(button1)
	# 	btn.SetParent(self.baseImage)
	# 	btn.SetPosition(0,0)
	# 	btn.Show()

	# 	self.button1 = btn


	# def __LoadButton2(self, button2):
	# 	button2['event'] = self.__OnClickButton2

	# 	btn = ExpandedButton(button2)
	# 	btn.SetParent(self.baseImage)

	# 	if self.orientation == self.HORIZONTAL:
	# 		leng = btn.GetWidth()
	# 		btn.SetPosition(self.GetWidth() - leng , 0)

	# 	elif self.orientation == self.VERTICAL:
	# 		leng = btn.GetHeight()
	# 		btn.SetPosition(0, self.GetHeight() - leng)
	# 	btn.Show()

	# 	self.button2 = btn

	def __LoadMiddleButton(self, middle):
		middle['downevent'] = self.__OnClickMiddle
		middle['update']	= self.__OnUpdateMiddleBar
		btn = ExpandedButton(middle)
		btn.SetParent(self.baseImage)


		# if self.orientation == self.HORIZONTAL:
		# 	btn.SetPosition(self.button1.GetWidth(), 0)

		# elif self.orientation == self.VERTICAL:
		# 	btn.SetPosition(0, self.button1.GetHeight())
		btn.SetPosition(0, 0)

		btn.Show()
		self.middleButton = btn

	def __SetOnScrollEvent(self, onscroll):
		self.onScroll = onscroll

	def __SetAlign(self, align):
		mode	= align['mode']
		offset1	= align.get('offset1',0)
		offset2	= align.get('offset2',0)

		if not self.parent:
			return

		if self.orientation == self.HORIZONTAL:
			if mode == self.TOP:
				self.SetPosition(offset1, 0)

			if mode == self.BOTTOM:
				self.SetPosition(offset1, self.parent.GetHeight() - self.GetHeight())

			self.SetScrollBarLength(self.parent.GetWidth() - (offset1 + offset2))


		elif self.orientation == self.VERTICAL:
			if mode == self.RIGHT:
				self.SetPosition(self.parent.GetWidth()-self.GetWidth(),  offset1 )

			elif mode == self.LEFT:
				self.SetPosition(0, offset1)

			self.SetScrollBarLength(self.parent.GetHeight() - (offset1 + offset2))

	def __SetPosition(self, position):
		self.SetPosition(position['x'] , position['y'])

	def SetScrollBarLength(self, leng):
		if self.orientation == self.VERTICAL:
			self.SetSize(self.GetWidth(), leng)


			baseScale = float(leng) / float(self.baseInfo['base']['height'])
			self.baseImage.SetScale(1.0, baseScale)

			# scrollsize  = leng - (self.__GetElementLength(self.button1) + self.__GetElementLength(self.button2))
			scrollsize  = leng

			middle_leng = int(self.middleScale * scrollsize)
			init_middle = float(self.middleButton.baseInfo['default']['height'])

			self.middleButton.SetScale(1.0, float(middle_leng)/init_middle)
			# self.middleButton.SetPosition(0,self.__GetElementLength(self.button1) + int((scrollsize - self.__GetElementLength(self.middleButton))* self.pos))
			self.middleButton.SetPosition(0, int((scrollsize - self.__GetElementLength(self.middleButton))* self.pos))

			# self.button2.SetPosition(0, self.GetHeight()-self.button2.GetHeight())

		elif self.orientation == self.HORIZONTAL:
			self.SetSize(leng, self.GetHeight())

			baseScale = float(leng) / float(self.baseInfo['base']['width'])
			self.baseImage.SetScale(baseScale, 1.0)


			# scrollsize = leng - (self.__GetElementLength(self.button1) + self.__GetElementLength(self.button2))
			scrollsize = leng

			middle_leng = int(self.middleScale * scrollsize)
			init_middle = float(self.middleButton.baseInfo['default']['width'])

			self.middleButton.SetScale(float(middle_leng) / init_middle, 1.0)
			# self.middleButton.SetPosition(self.__GetElementLength(self.button1) + int((scrollsize - self.__GetElementLength(self.middleButton)) * self.pos),0)
			self.middleButton.SetPosition(int((scrollsize - self.__GetElementLength(self.middleButton)) * self.pos),0)

			# self.button2.SetPosition(self.GetWidth() - self.button2.GetWidth(), 0)

	def __GetElementLength(self, element):
		if self.orientation == self.VERTICAL:
			return element.GetHeight()

		if self.orientation == self.HORIZONTAL:
			return element.GetWidth()
		return 0

	def __OnUpdateMiddleBar(self):
		if self.middleButton.status != ExpandedButton.STATUS_DOWN:
			return



		x,y 	= wndMgr.GetMousePosition()
		gx,gy	= self.middleButton.GetGlobalPosition()

		gx += self.mouseOffset.get('x',0)
		gy += self.mouseOffset.get('y',0)

		if self.orientation == self.VERTICAL:
			if y == gy:
				return

		elif self.orientation == self.HORIZONTAL:
			if x == gx:
				return

		self.__OnMoveMiddleBar(x,y)

	def __OnClickBaseImage(self):
		x,y 	= wndMgr.GetMousePosition()
		gx,gy	= self.middleButton.GetGlobalPosition()

		offset = self.__GetElementLength(self.middleButton)/2

		gx += offset
		gy += offset

		if self.orientation == self.VERTICAL:
			if y == gy:
				return

		elif self.orientation == self.HORIZONTAL:
			if x == gx:
				return

		self.mouseOffset = {'x' : offset, 'y': offset}
		self.__OnMoveMiddleBar(x,y)

	def __OnClickButton2(self):
		self.mouseOffset={'x' : 0, 'y' :0}
		gx,gy = self.middleButton.GetGlobalPosition()
		if self.orientation == self.VERTICAL:
			gy += self.__GetElementLength(self.middleButton)
		elif self.orientation == self.HORIZONTAL:
			gx += self.__GetElementLength(self.middleButton)

		self.__OnMoveMiddleBar(gx,gy)

	def __OnClickButton1(self):
		self.mouseOffset={'x' : 0, 'y' :0}
		gx, gy = self.middleButton.GetGlobalPosition()
		if self.orientation == self.VERTICAL:
			gy -= self.__GetElementLength(self.middleButton)
		elif self.orientation == self.HORIZONTAL:
			gx -= self.__GetElementLength(self.middleButton)

		self.__OnMoveMiddleBar(gx, gy)

	def __OnMoveMiddleBar(self, x , y):
		gx, gy = self.GetGlobalPosition()
		x -= self.mouseOffset.get('x', 0)
		y -= self.mouseOffset.get('y', 0)


		if self.orientation == self.VERTICAL:
			# min_ = gy  + self.__GetElementLength(self.button1)
			min_ = gy
			# max_ = min_ + (self.GetHeight() - (self.__GetElementLength(self.button1) + self.__GetElementLength(self.button2) + self.__GetElementLength(self.middleButton)))
			max_ = min_ + (self.GetHeight() - self.__GetElementLength(self.middleButton))

			if max_ < y and self.pos == 1.0:
				return

			if min_ > y and self.pos == 0.0:
				return

			realy = max(y, min_)
			realy = min(realy, max_)
			scroll= max_-min_

			if scroll == 0.0:
				return


			self.pos = float(realy-min_) / float(scroll)
			self.middleButton.SetPosition(0, realy-gy)

			self.__OnScroll()

		elif self.orientation == self.HORIZONTAL:
			min_ = gx
			max_ = min_ + (self.GetWidth() - self.__GetElementLength(self.middleButton))

			if max_ < x and self.pos == 1.0:
				return

			if min_ > x and self.pos == 0.0:
				return

			realx = max(x, min_)
			realx = min(realx, max_)
			scroll = max_ - min_

			if scroll == 0.0:
				return

			self.pos = float(realx - min_) / float(scroll)
			self.middleButton.SetPosition(realx-gx, 0)

			self.__OnScroll()

	def __OnScroll(self):
		if self.onScroll:
			self.onScroll()

	def __OnClickMiddle(self):
		x,y 	= wndMgr.GetMousePosition()
		gx,gy	= self.middleButton.GetGlobalPosition()

		x-= gx
		y-= gy

		self.mouseOffset = {"x" : x, "y": y ,}

	def GetPos(self):
		return self.pos

	def GetStep(self):
		return self.step

	def SetScrollStep(self, step):
		step = min(1.0, max(0.1 , step))
		self.middleScale = step
		self.step = step

		self.SetScrollBarLength(self.__GetElementLength(self.baseImage))

class CustomCheckBox(Window):

	def __init__(self, images={}):
		Window.__init__(self)
		self.clear()
		self.__loadCheckBox(images)
		self.SetOnMouseLeftButtonUpEvent(self.__OnClick)
		self.SetWindowName("checkbox")

	def clear(self):
		self.status = "disabled"
		self.bg_image = None
		self.tip_image = None

	def __del__(self):
		self.status = "disabled"
		self.bg_image = None
		self.tip_image = None
		Window.__del__(self)

	def __loadCheckBox(self, images):
		bg = ImageBox()
		bg.SetParent(self)
		bg.SetPosition(0, 0)

		if not images:
			bg.LoadImage("d:/ymir work/ui/pattern/checkbox_bg.png")
		else:
			bg.LoadImage(images['base'])

		bg.SetOnMouseLeftButtonUpEvent(self.__OnClick)
		bg.SetWindowName("checkbox_bg")
		self.SetSize(bg.GetWidth(), bg.GetHeight())
		bg.Show()

		self.bg_image = bg

		# tip image
		tip = ImageBox()
		tip.SetParent(self.bg_image)

		if not images:
			tip.LoadImage("d:/ymir work/ui/pattern/checkbox_tip.png")
		else:
			tip.LoadImage(images['tip'])

		tip.SetPosition(0, 0)
		tip.Show()
		tip.SetWindowName("checkbox_tip")
		tip.SetOnMouseLeftButtonUpEvent(self.__OnClick)

		self.tip_image = tip

		self.__refreshView()

	def __refreshView(self):
		if self.status == "enabled":
			self.tip_image.Show()
		else:
			self.tip_image.Hide()

	def __OnClick(self):
		if self.status == "disabled":
			self.status = "enabled"

		else:
			self.status = "disabled"

		print("clicked!")
		self.__refreshView()

	def IsEnabled(self):
		return self.status == "enabled"

	def Enable(self):
		self.status = "enabled"
		self.__refreshView()

	def Disable(self):
		self.status = "disabled"
		self.__refreshView()

class CheckBoxOfflineShop(Window):
	def __init__(self, images = {}):
		Window.__init__(self)
		self.clear()
		self.__loadCheckBox(images)
		self.SetOnMouseLeftButtonUpEvent(self.__OnClick)
		self.SetWindowName("checkbox")

	def clear(self):
		self.status = "disabled"
		self.bg_image = None
		self.tip_image = None

	def __del__(self):
		self.status		= "disabled"
		self.bg_image	= None
		self.tip_image	= None
		Window.__del__(self)

	def __loadCheckBox(self, images):
		bg = ImageBox()
		bg.SetParent(self)
		bg.SetPosition(0,0)
		if not images:
			bg.LoadImage("d:/ymir work/ui/pattern/checkbox_bg.png")
		else:
			bg.LoadImage(images['base'])
		bg.SetOnMouseLeftButtonUpEvent(self.__OnClick)
		bg.SetWindowName("checkbox_bg")
		self.SetSize(bg.GetWidth(), bg.GetHeight())
		bg.Show()
		self.bg_image = bg
		tip = ImageBox()
		tip.SetParent(self.bg_image)
		if not images:
			tip.LoadImage("d:/ymir work/ui/pattern/checkbox_tip.png")
		else:
			tip.LoadImage(images['tip'])
		tip.SetPosition(0 , 0)
		tip.Show()
		tip.SetWindowName("checkbox_tip")
		tip.SetOnMouseLeftButtonUpEvent(self.__OnClick)
		self.tip_image = tip
		self.__refreshView()

	def __refreshView(self):
		if self.status == "enabled":
			self.tip_image.Show()
		else:
			self.tip_image.Hide()

	def __OnClick(self):
		if self.status == "disabled":
			self.status = "enabled"
		else:
			self.status = "disabled"
		print("clicked!")
		self.__refreshView()

	def IsEnabled(self):
		return self.status == "enabled"

	def Enable(self):
		self.status = "enabled"
		self.__refreshView()

	def Disable(self):
		self.status = "disabled"
		self.__refreshView()

class ComboBoxImage(Window):
	class ListBoxWithBoard(ListBox):

		def __init__(self, layer):
			ListBox.__init__(self, layer)

		def OnRender(self):
			xRender, yRender = self.GetGlobalPosition()
			yRender -= self.TEMPORARY_PLACE
			widthRender = self.width
			heightRender = self.height + self.TEMPORARY_PLACE*2
			grp.SetColor(BACKGROUND_COLOR)
			grp.RenderBar(xRender, yRender, widthRender, heightRender)
			grp.SetColor(DARK_COLOR)
			grp.RenderLine(xRender, yRender, widthRender, 0)
			grp.RenderLine(xRender, yRender, 0, heightRender)
			ListBox.OnRender(self)

	def __init__(self, parent, name, x ,y):
		Window.__init__(self)
		self.isSelected = False
		self.isOver = False
		self.isListOpened = False
		self.event = lambda *arg: None
		self.enable = True
		self.imagebox = None

		## imagebox
		image = ImageBox()
		image.SetParent(parent)
		image.LoadImage(name)
		image.SetPosition(x, y)
		image.Show()
		self.imagebox = image

		## BaseSetting
		self.x = x + 1
		self.y = y + 1
		self.width = self.imagebox.GetWidth() - 3
		self.height = self.imagebox.GetHeight() - 3
		self.SetParent(parent)

		## TextLine
		self.textLine = MakeTextLine(self)
		self.textLine.SetText(localeInfo.UI_ITEM)

		## ListBox
		self.listBox = self.ListBoxWithBoard("TOP_MOST")
		self.listBox.SetPickAlways()
		self.listBox.SetParent(self)
		self.listBox.SetEvent(__mem_func__(self.OnSelectItem))
		self.listBox.Hide()

		Window.SetPosition(self, self.x, self.y)
		Window.SetSize(self, self.width, self.height)
		self.textLine.UpdateRect()
		self.__ArrangeListBox()

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		self.textLine = None
		self.listBox = None
		self.imagebox = None

	def SetPosition(self, x, y):
		Window.SetPosition(self, x, y)
		self.imagebox.SetPosition(x, y)
		self.x = x
		self.y = y
		self.__ArrangeListBox()

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height
		self.textLine.UpdateRect()
		self.__ArrangeListBox()

	def __ArrangeListBox(self):
		self.listBox.SetPosition(0, self.height + 5)
		self.listBox.SetWidth(self.width)

	def Enable(self):
		self.enable = True

	def Disable(self):
		self.enable = False
		self.textLine.SetText("")
		self.CloseListBox()

	def SetEvent(self, event):
		self.event = event

	def ClearItem(self):
		self.CloseListBox()
		self.listBox.ClearItem()

	def InsertItem(self, index, name):
		self.listBox.InsertItem(index, name)
		self.listBox.ArrangeItem()

	def SetCurrentItem(self, text):
		self.textLine.SetText(text)

	def SelectItem(self, key):
		self.listBox.SelectItem(key)

	def OnSelectItem(self, index, name):
		self.CloseListBox()
		self.event(index)

	def CloseListBox(self):
		self.isListOpened = False
		self.listBox.Hide()

	def OnMouseLeftButtonDown(self):

		if not self.enable:
			return

		self.isSelected = True

	def OnMouseLeftButtonUp(self):
		if not self.enable:
			return

		self.isSelected = False

		if self.isListOpened:
			self.CloseListBox()
		else:
			if self.listBox.GetItemCount() > 0:
				self.isListOpened = True
				self.listBox.Show()
				self.__ArrangeListBox()

	def OnUpdate(self):

		if not self.enable:
			return

		if self.IsIn():
			self.isOver = True
		else:
			self.isOver = False

	def OnRender(self):
		self.x, self.y = self.GetGlobalPosition()
		xRender = self.x
		yRender = self.y
		widthRender = self.width
		heightRender = self.height
		if self.isOver:
			grp.SetColor(DARK_COLOR)
			grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)
			if self.isSelected:
				grp.SetColor(DARK_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

class ComboBox(Window):

	class ListBoxWithBoard(ListBox):

		def __init__(self, layer):
			ListBox.__init__(self, layer)

		def OnRender(self):
			xRender, yRender = self.GetGlobalPosition()
			yRender -= self.TEMPORARY_PLACE
			widthRender = self.width
			heightRender = self.height + self.TEMPORARY_PLACE*2
			grp.SetColor(BACKGROUND_COLOR)
			grp.RenderBar(xRender, yRender, widthRender, heightRender)
			grp.SetColor(DARK_COLOR)
			grp.RenderLine(xRender, yRender, widthRender, 0)
			grp.RenderLine(xRender, yRender, 0, heightRender)
			grp.SetColor(BRIGHT_COLOR)
			grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
			grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

			ListBox.OnRender(self)

	def __init__(self):
		Window.__init__(self)
		self.x = 0
		self.y = 0
		self.width = 0
		self.height = 0
		self.isSelected = FALSE
		self.isOver = FALSE
		self.isListOpened = FALSE
		self.event = lambda *arg: None
		self.enable = TRUE

		self.textLine = MakeTextLine(self)
		self.textLine.SetText(localeInfo.UI_ITEM)

		self.listBox = self.ListBoxWithBoard("TOP_MOST")
		self.listBox.SetPickAlways()
		self.listBox.SetParent(self)
		self.listBox.SetEvent(__mem_func__(self.OnSelectItem))
		self.listBox.Hide()

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		self.textLine = None
		self.listBox = None

	def SetPosition(self, x, y):
		Window.SetPosition(self, x, y)
		self.x = x
		self.y = y
		self.__ArrangeListBox()

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height
		self.textLine.UpdateRect()
		self.__ArrangeListBox()

	def __ArrangeListBox(self):
		self.listBox.SetPosition(0, self.height + 5)
		self.listBox.SetWidth(self.width)

	def Enable(self):
		self.enable = TRUE

	def Disable(self):
		self.enable = FALSE
		self.textLine.SetText("")
		self.CloseListBox()

	def SetEvent(self, event):
		self.event = event

	def ClearItem(self):
		self.CloseListBox()
		self.listBox.ClearItem()

	def InsertItem(self, index, name):
		self.listBox.InsertItem(index, name)
		self.listBox.ArrangeItem()

	def SetCurrentItem(self, text):
		self.textLine.SetText(text)

	def ResetSelected(self):
		self.textLine.SetText("")
		self.listBox.ResetSelected()

	def SelectItem(self, key):
		self.listBox.SelectItem(key)

	def OnSelectItem(self, index, name):

		self.CloseListBox()
		self.event(index)

	def CloseListBox(self):
		self.isListOpened = FALSE
		self.listBox.Hide()

	def OnMouseLeftButtonDown(self):

		if not self.enable:
			return

		self.isSelected = TRUE

	def OnMouseLeftButtonUp(self):

		if not self.enable:
			return

		self.isSelected = FALSE

		if self.isListOpened:
			self.CloseListBox()
		else:
			if self.listBox.GetItemCount() > 0:
				self.isListOpened = TRUE
				self.listBox.Show()
				self.__ArrangeListBox()

	def OnUpdate(self):

		if not self.enable:
			return

		if self.IsIn():
			self.isOver = TRUE
		else:
			self.isOver = FALSE

	def OnRender(self):
		self.x, self.y = self.GetGlobalPosition()
		xRender = self.x
		yRender = self.y
		widthRender = self.width
		heightRender = self.height
		grp.SetColor(BACKGROUND_COLOR)
		grp.RenderBar(xRender, yRender, widthRender, heightRender)
		grp.SetColor(DARK_COLOR)
		grp.RenderLine(xRender, yRender, widthRender, 0)
		grp.RenderLine(xRender, yRender, 0, heightRender)
		grp.SetColor(BRIGHT_COLOR)
		grp.RenderLine(xRender, yRender+heightRender, widthRender, 0)
		grp.RenderLine(xRender+widthRender, yRender, 0, heightRender)

		if self.isOver:
			grp.SetColor(HALF_WHITE_COLOR)
			grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

			if self.isSelected:
				grp.SetColor(WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)

class Table(Window):

	ROW_HEIGHT = 18
	HEADER_EXTRA_HEIGHT = 0

	class TableLine(Window):

		def __init__(self, mouseLeftButtonDownEvent, mouseLeftButtonDoubleClickEvent):
			Window.__init__(self)

			self.colSize = []
			self.textLines = []

			self.mouseLeftButtonDownEvent = mouseLeftButtonDownEvent
			self.mouseLeftButtonDoubleClickEvent = mouseLeftButtonDoubleClickEvent

			self.SetSize(0, Table.ROW_HEIGHT)

			self.SetWindowName("NONAME_Table_TableLine")

		def __del__(self):
			Window.__del__(self)

		def __UpdateWidth(self, appendSize):
			self.SetSize(self.GetWidth() + appendSize, self.GetHeight())

		def __CheckLength(self, line, maxWidth):
			if line.GetTextWidth() <= maxWidth:
				return line.GetText()

			text = line.GetText()
			pos = len(text)
			while pos > 1:
				pos = pos - 1

				line.SetText(text[:pos] + "..")
				if line.GetTextWidth() <= maxWidth and text[pos-1] != " ":
					return text[:pos] + ".."

			return ".."

		def AppendCol(self, wnd, width, checkLength):
			lineWnd = Window()
			lineWnd.SetParent(self)
			lineWnd.SetMouseLeftButtonDownEvent(self.mouseLeftButtonDownEvent)
			lineWnd.SetMouseLeftButtonDoubleClickEvent(self.mouseLeftButtonDoubleClickEvent)
			lineWnd.SetSize(width, self.GetHeight())
			lineWnd.SetPosition(self.GetWidth(), 0)
			lineWnd.Show()

			if type(wnd) == type("") or type(wnd) == type(0) or type(wnd) == type(0.0):
				line = TextLine()
				line.SetParent(lineWnd)
				line.SetWindowHorizontalAlignCenter()
				line.SetHorizontalAlignCenter()
				line.SetWindowVerticalAlignCenter()
				line.SetVerticalAlignCenter()
				line.SetText(str(wnd))
				line.Show()
				if checkLength == True:
					line.SetText(self.__CheckLength(line, width))
				lineWnd.wnd = line
			else:
				wnd.SetParent(lineWnd)
				wnd.SetPosition(0, 0)
				wnd.SetWindowHorizontalAlignCenter()
				wnd.SetWindowVerticalAlignCenter()
				wnd.Show()
				lineWnd.wnd = wnd

			self.textLines.append(lineWnd)

			self.__UpdateWidth(width)

		def OnMouseLeftButtonDown(self):
			self.mouseLeftButtonDownEvent()

		def OnMouseLeftButtonDoubleClick(self):
			self.mouseLeftButtonDoubleClickEvent()

	def __init__(self):
		Window.__init__(self)

		self.cols = 0
		self.rows = 0
		self.basePos = 0
		self.viewLineCount = 0

		self.overLine = -1
		self.overHeader = -1
		self.selectedKey = -1
		self.selectedLine = -1

		self.overRender = None
		self.selectRender = None

		self.colSizePct = []
		self.checkLengthIndexes = []
		self.maxColSizePct = 100
		self.headerLine = None
		self.lines = []
		self.keys = []
		self.keyDict = {}

		self.headerClickEvent = lambda *arg: None
		self.doubleClickEvent = lambda *arg: None

		self.SetWindowName("NONAME_Table")

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		self.lines = []

	def SetWidth(self, width):
		self.SetSize(width, self.GetHeight())

	def SetColSizePct(self, colSizeList):
		self.colSizePct = []
		self.maxColSizePct = 0
		for size in colSizeList:
			self.colSizePct.append(size)
			self.maxColSizePct += size
		self.LocateLines()

	def AddCheckLengthIndex(self, index):
		self.checkLengthIndexes.append(index)

	def GetColSize(self, index):
		return int(self.GetWidth() * self.colSizePct[index] / self.maxColSizePct)

	def __BuildLine(self, colList):
		line = self.TableLine(__mem_func__(self.OnMouseLeftButtonDown), __mem_func__(self.OnMouseLeftButtonDoubleClick))
		line.SetParent(self)
		for i in xrange(len(colList)):
			line.AppendCol(colList[i], self.GetColSize(i), i in self.checkLengthIndexes)
		return line

	def SetHeader(self, colList, extraHeight = 0):
		self.headerLine = self.__BuildLine(colList)
		self.HEADER_EXTRA_HEIGHT = extraHeight
		self.LocateLines()

	def ClearHeader(self):
		self.headerLine = None
		self.LocateLines()

	def Clear(self):
		self.lines = []
		self.keys = []
		self.basePos = 0
		self.overLine = -1
		self.overHeader = -1
		self.selectedKey = -1
		self.selectedLine = -1
		self.LocateLines()

	def GetLineCount(self):
		return len(self.lines)

	def GetMaxLineCount(self):
		if self.GetHeight() < self.ROW_HEIGHT:
			return 0

		maxHeight = self.GetHeight()
		if self.headerLine != None:
			maxHeight -= self.ROW_HEIGHT

		return int(maxHeight / self.ROW_HEIGHT)

	def GetViewLineCount(self):
		return self.viewLineCount

	def Append(self, index, colList, refresh = True):
		self.keyDict[index] = len(self.lines)
		self.lines.append(self.__BuildLine(colList))
		self.keys.append(index)
		if refresh == True:
			self.LocateLines()

	def Erase(self, index):
		if not self.keyDict.has_key(index):
			return

		listIndex = self.keyDict[index]

		for i in xrange(listIndex + 1, len(self.lines)):
			self.keyDict[self.keys[i]] -= 1

		del self.lines[listIndex]
		del self.keys[listIndex]
		del self.keyDict[index]

		if self.selectedLine != -1:
			if self.selectedKey == index:
				self.selectedKey = -1
				self.selectedLine = -1
			else:
				self.selectedLine = self.keyDict[self.selectedKey]
			self.__RefreshSelectedLineRender()

		if listIndex >= self.basePos and listIndex < self.basePos + self.viewLineCount:
			if self.basePos > 0 and self.GetLineCount() < self.basePos + self.viewLineCount:
				self.basePos -= 1
			self.LocateLines()

	def LocateLines(self):
		maxHeight = self.GetHeight()
		if maxHeight < self.ROW_HEIGHT:
			maxHeight = 0

		height = 0

		if self.headerLine != None:
			self.headerLine.SetPosition(0, height)
			self.headerLine.Show()
			height += self.ROW_HEIGHT + self.HEADER_EXTRA_HEIGHT

		self.viewLineCount = 0

		for i in xrange(len(self.lines)):
			if i < self.basePos or (maxHeight != 0 and height + self.ROW_HEIGHT >= maxHeight):
				self.lines[i].Hide()
				continue

			self.lines[i].SetPosition(0, height)
			self.lines[i].Show()
			height += self.ROW_HEIGHT

			self.viewLineCount += 1

	def SetBasePos(self, basePos):
		if basePos < 0:
			basePos = 0
		elif basePos + self.GetMaxLineCount() > self.GetLineCount():
			basePos = max(0, self.GetLineCount() - self.GetMaxLineCount())

		self.basePos = basePos
		self.LocateLines()
		self.__RefreshSelectedLineRender()

	def GetBasePos(self):
		return self.basePos

	def SelectLine(self, line):
		if line < 0 or line >= self.GetViewLineCount():
			line = -1
		else:
			line += self.basePos

		self.selectedKey = self.keys[line]
		self.selectedLine = line
		self.__RefreshSelectedLineRender()

	def __RefreshSelectedLineRender(self):
		self.selectRender = None

		if self.selectedLine == -1:
			return

		if self.selectedLine < self.basePos or self.selectedLine >= self.basePos + self.viewLineCount:
			return

		x, y = self.GetGlobalPosition()
		if self.headerLine != None:
			y += self.ROW_HEIGHT + self.HEADER_EXTRA_HEIGHT

		self.selectRender = {
			"x" : x,
			"y":  y + self.ROW_HEIGHT * (self.selectedLine - self.basePos),
			"width" : self.GetWidth(),
			"height" : self.ROW_HEIGHT,
		}

	def OnMouseLeftButtonDown(self):
		if self.overLine != -1:
			self.SelectLine(self.overLine)
		elif self.overHeader != -1:
			self.headerClickEvent(self.overHeader)

	def SetDoubleClickEvent(self, event):
		self.doubleClickEvent = event

	def OnMouseLeftButtonDoubleClick(self):
		if self.selectedLine != -1 and self.overLine == self.selectedLine:
			self.doubleClickEvent(self.selectedKey)

	def SetHeaderClickEvent(self, event):
		self.headerClickEvent = event

	def OnUpdate(self):
		self.__RefreshSelectedLineRender()

		self.overLine = -1
		self.overHeader = -1
		self.overRender = None

		x, y = self.GetGlobalPosition()
		xMouse, yMouse = wndMgr.GetMousePosition()

		if xMouse < x or xMouse > x + self.GetWidth():
			return

		if self.headerLine != None:
			y += self.ROW_HEIGHT + self.HEADER_EXTRA_HEIGHT

		overLine = int((yMouse - y) / self.ROW_HEIGHT)
		if overLine < 0 or overLine >= self.viewLineCount:
			if yMouse >= y - (self.ROW_HEIGHT + self.HEADER_EXTRA_HEIGHT) and yMouse < y - self.HEADER_EXTRA_HEIGHT and self.headerLine != None:
				width = 0
				headerColIndex = 0
				for i in xrange(len(self.colSizePct)):
					width = int(self.GetWidth() * self.colSizePct[i] / self.maxColSizePct)
					if xMouse <= x + width:
						break
					headerColIndex += 1
					x += width
					if headerColIndex >= len(self.colSizePct):
						return

				self.overHeader = headerColIndex
				self.overRender = {
					"x" : x,
					"y" : y - self.ROW_HEIGHT - self.HEADER_EXTRA_HEIGHT,
					"width" : width,
					"height" : self.ROW_HEIGHT,
				}

			return

		self.overLine = overLine
		self.overRender = {
			"x" : x,
			"y" : y + overLine * self.ROW_HEIGHT,
			"width" : self.GetWidth(),
			"height" : self.ROW_HEIGHT,
		}

	def __DrawRender(self, color, render):
		grp.SetColor(color)
		grp.RenderBar(render["x"], render["y"], render["width"], render["height"])

	def OnRender(self):
		if self.overRender:
			self.__DrawRender(HALF_WHITE_COLOR, self.overRender)
		if self.selectRender:
			self.__DrawRender(SELECT_COLOR, self.selectRender)

class UpDownButton(Window):

	BUTTON_HEIGHT = 38

	def __init__(self):
		Window.__init__(self)

		self.cur = 0
		self.min = 0
		self.max = 0

		self.downBtn = None
		self.lastDownTime = 0
		self.isDownUsed = False

		numberField = InputField()
		numberField.SetParent(self)
		numberField.SetSize(20, 38)
		numberField.Show()

		numberLine = NumberLine()
		numberLine.SetParent(numberField)
		numberLine.SetWindowHorizontalAlignCenter()
		numberLine.SetHorizontalAlignCenter()
		numberLine.SetWindowVerticalAlignCenter()
		numberLine.SetVerticalAlignCenter()
		numberLine.Show()
		numberField.numberLine = numberLine

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetPosition(numberField.GetRight()+2, 0)
		upButton.SetUpVisual("d:/ymir work/ui/public/up_button_01.sub")
		upButton.SetOverVisual("d:/ymir work/ui/public/up_button_02.sub")
		upButton.SetDownVisual("d:/ymir work/ui/public/up_button_03.sub")
		upButton.SAFE_SetEvent(self.OnClickUpButton)
		upButton.SAFE_SetDownEvent(self.OnDownUpButton)
		upButton.Show()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetPosition(numberField.GetRight()+2, upButton.GetBottom())
		downButton.SetUpVisual("d:/ymir work/ui/public/down_button_01.sub")
		downButton.SetOverVisual("d:/ymir work/ui/public/down_button_02.sub")
		downButton.SetDownVisual("d:/ymir work/ui/public/down_button_03.sub")
		downButton.SAFE_SetEvent(self.OnClickDownButton)
		downButton.SAFE_SetDownEvent(self.OnDownDownButton)
		downButton.Show()

		self.numberField = numberField
		self.upButton = upButton
		self.downButton = downButton

		self.SetSize(max(upButton.GetRight(), downButton.GetRight()), max(numberField.GetHeight(), downButton.GetBottom()))
		self.Refresh()

		self.SetWindowName("NONAME_UpDownButton")

	def __del__(self):
		Window.__del__(self)

	def SetValue(self, val):
		val = int(val)
		val = max(val, self.min)
		if self.max > self.min:
			val = min(val, self.max)
		self.cur = val

		self.Refresh()

	def GetValue(self):
		return self.cur

	def SetMin(self, val):
		self.min = int(val)
		self.SetValue(self.cur)

	def SetMax(self, val):
		self.max = int(val)
		self.SetValue(self.cur)

	def OnClickUpButton(self):
		if self.isDownUsed:
			return
		self.SetValue(self.cur + 1)

	def OnDownUpButton(self):
		self.downBtn = self.upButton
		self.lastDownTime = app.GetTime()
		self.isDownUsed = False

	def OnClickDownButton(self):
		if self.isDownUsed:
			return
		self.SetValue(self.cur - 1)

	def OnDownDownButton(self):
		self.downBtn = self.downButton
		self.lastDownTime = app.GetTime()
		self.isDownUsed = False

	def Refresh(self):
		self.numberField.numberLine.SetNumber(self.cur)
		self.numberField.numberLine.UpdateRect()

	def OnUpdate(self):
		if self.downBtn != None:
			if not self.downBtn.IsDown():
				self.downBtn = None
				self.isDownUsed = False
				return

			if app.GetTime() - self.lastDownTime >= 0.25 or (app.GetTime() - self.lastDownTime >= 0.15 and self.isDownUsed == False):
				self.lastDownTime = app.GetTime()

				self.isDownUsed = False
				self.downBtn.CallEvent()
				self.isDownUsed = True

class InputField(Window):

	PATH = "d:/ymir work/ui/pattern/input_%s.tga"

	BORDER_SIZE = 1
	BASE_SIZE = 1

	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, basePath = PATH):
		Window.__init__(self)

		self.isButtonStyle = False
		self.isButtonStyleOverOnly = False
		self.isDown = False
		self.renderData = {}

		self.onClickEvent = None
		self.onClickArgs = None

		self.MakeField(basePath)
		self.SetSize(0, 0)

		self.SetWindowName("NONAME_InputField")

	def __del__(self):
		Window.__del__(self)

	def MakeField(self, basePath):
		self.Lines = []
		for i in xrange(4):
			line = ExpandedImageBox()
			line.AddFlag("attach")
			line.AddFlag("not_pick")
			line.SetParent(self)
			line.LoadImage(basePath % "border")
			line.Show()
			self.Lines.append(line)

		self.Lines[self.T].SetPosition(self.BORDER_SIZE, 0)
		self.Lines[self.B].SetPosition(self.BORDER_SIZE, 0)

		self.Base = ExpandedImageBox()
		self.Base.AddFlag("attach")
		self.Base.AddFlag("not_pick")
		self.Base.SetParent(self)
		self.Base.SetPosition(self.BORDER_SIZE, self.BORDER_SIZE)
		self.Base.LoadImage(basePath % "base")
		self.Base.Show()

	def SetSize(self, width, height):
		minSize = self.BORDER_SIZE * 2 + self.BASE_SIZE
		width = max(minSize, width)
		height = max(minSize, height)
		Window.SetSize(self, width, height)

		scaleH = float(width - self.BORDER_SIZE * 2 - self.BORDER_SIZE) / float(self.BORDER_SIZE)
		scaleV = float(height - self.BORDER_SIZE) / float(self.BORDER_SIZE)
		self.Lines[self.L].SetRenderingRect(0, 0, 0, scaleV)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, scaleV)
		self.Lines[self.T].SetRenderingRect(0, 0, scaleH, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, scaleH, 0)
		self.Lines[self.R].SetPosition(width - self.BORDER_SIZE, self.Lines[self.R].GetTop())
		self.Lines[self.B].SetPosition(self.Lines[self.B].GetLeft(), height - self.BORDER_SIZE)

		scaleH = float(width - self.BORDER_SIZE * 2 - self.BASE_SIZE) / float(self.BASE_SIZE)
		scaleV = float(height - self.BORDER_SIZE * 2 - self.BASE_SIZE) / float(self.BASE_SIZE)
		self.Base.SetRenderingRect(0, 0, scaleH, scaleV)

	def SetAlpha(self, alpha):
		for line in self.Lines:
			line.SetAlpha(alpha)
		self.Base.SetAlpha(alpha)

	def SetEvent(self, event, *args):
		self.onClickEvent = event
		self.onClickArgs = args

	def ClearEvent(self):
		self.onClickEvent = None

	def SetButtonStyle(self, isButtonStyle):
		self.isButtonStyle = isButtonStyle

		if self.isButtonStyle == False and (self.isButtonStyleOverOnly == False or not self.IsIn()):
			self.__ResetRenderData()

	def SetButtonStyleOverOnly(self, isButtonStyleOverOnly):
		self.isButtonStyleOverOnly = isButtonStyleOverOnly

		if self.isButtonStyleOverOnly == False:
			if self.isButtonStyle == False:
				self.__ResetRenderData()

	def __ResetRenderData(self):
		self.renderData = {"render" : False}

	def __SetRenderData(self, key, val):
		self.renderData["render"] = True
		self.renderData[key] = val

	def __GetRenderData(self, key):
		return self.renderData.get(key, False)

	def OnMouseOverIn(self):
		if self.isButtonStyle or self.isButtonStyleOverOnly:
			if self.isButtonStyle == False or self.isDown == False:
				self.__SetRenderData("color", HALF_WHITE_COLOR)
			elif self.isButtonStyle:
				self.__SetRenderData("color", SELECT_COLOR)

	def OnMouseOverOut(self):
		if self.isButtonStyle or self.isButtonStyleOverOnly:
			if self.isButtonStyle == False or self.isDown == False:
				self.__ResetRenderData()

	def OnMouseLeftButtonDown(self):
		Window.OnMouseLeftButtonDown(self)

		self.isDown = True
		if self.isButtonStyle:
			self.__SetRenderData("color", SELECT_COLOR)

	def OnMouseLeftButtonUp(self):
		Window.OnMouseLeftButtonUp(self)

		self.isDown = False
		self.__ResetRenderData()

		if self.IsIn():
			if self.isButtonStyle or self.isButtonStyleOverOnly:
				self.__SetRenderData("color", HALF_WHITE_COLOR)
			if self.onClickEvent:
				apply(self.onClickEvent, self.onClickArgs)

	# def OnAfterRender(self):
	# 	if not self.__GetRenderData("render"):
	# 		return

	# 	x, y, width, height = self.GetRect()
	# 	grp.SetColor(self.__GetRenderData("color"))
	# 	grp.RenderBar(x, y, width, height)


class ExtendedTextLine(Window):

	OBJECT_TYPE_IMAGE = 0
	OBJECT_TYPE_TEXT = 1
	OBJECT_TYPE_HEIGHT = 2
	OBJECT_TYPE_WIDTH = 3

	OBJECT_TAGS = {
		OBJECT_TYPE_IMAGE : "IMAGE",
		OBJECT_TYPE_TEXT : "TEXT",
		OBJECT_TYPE_HEIGHT : "HEIGHT",
		OBJECT_TYPE_WIDTH : "WIDTH",
	}

	def __init__(self):
		Window.__init__(self)

		self.inputText = ""
		self.childrenList = []

		self.limitWidth = 0
		self.x = 0
		self.maxHeight = 0
		self.extraHeight = 0

		self.renderingRect = { "left" : 0, "right" : 0, "top" : 0, "bottom" : 0 }

		self.SetWindowName("NONAME_ExtendedTextLine")

	def __del__(self):
		Window.__del__(self)

	def SetLimitWidth(self, width):
		self.limitWidth = width
		if self.inputText != "":
			self.SetText(self.inputText)

	def IsText(self, text):
		return self.inputText == text

	def SetText(self, text):
		self.childrenList = []
		self.x = 0
		self.maxHeight = 0
		self.extraHeight = 0

		charIndex = 0
		currentWord = ""

		textLine = None

		while charIndex < len(text):
			c = text[charIndex:charIndex+1]

			# tags
			if c == "<":
				if textLine:
					self.childrenList.append(textLine)
					self.x += textLine.GetTextWidth()
					self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)
					textLine = None

				tagStart = charIndex
				tagEnd = text[tagStart:].find(">")
				if tagEnd == -1:
					tagEnd = len(text)
				else:
					tagEnd += tagStart

				tagNameStart = charIndex + 1
				tagNameEnd = text[tagNameStart:].find(" ")
				if tagNameEnd == -1 or tagNameEnd > tagEnd:
					tagNameEnd = tagEnd
				else:
					tagNameEnd += tagNameStart
				tag = text[tagNameStart:tagNameEnd]

				content = {}
				tagContentPos = tagNameEnd + 1
				while tagContentPos < tagEnd:
					tagContentStart = -1
					for i in xrange(tagContentPos, tagEnd):
						if text[i:i+1] != " " and text[i:i+1] != "\t":
							tagContentStart = i
							break
					if tagContentStart == -1:
						break

					tagContentPos = text[tagContentStart:].find("=") + tagContentStart
					tagKey = text[tagContentStart:tagContentPos]

					tagContentPos += 1

					tagContentEnd = -1
					isBreakAtSpace = True
					for i in xrange(tagContentPos, tagEnd+1):
						if isBreakAtSpace == True and (text[i:i+1] == " " or text[i:i+1] == "\t" or text[i:i+1] == ">"):
							tagContentEnd = i
							break
						elif text[i:i+1] == "\"":
							if isBreakAtSpace == True:
								isBreakAtSpace = False
								tagContentPos = i + 1
							else:
								tagContentEnd = i
								break
					if tagContentEnd == -1:
						break

					tagValue = text[tagContentPos:tagContentEnd]
					content[tagKey] = tagValue

					tagContentPos = text[tagContentEnd:].find(" ")
					if tagContentPos == -1:
						tagContentPos = tagContentEnd
					else:
						tagContentPos += tagContentEnd

				bRet = True
				for key in self.OBJECT_TAGS:
					if self.OBJECT_TAGS[key] == tag.upper():
						bRet = self.__ComputeTag(key, content)
						break

				if bRet == False:
					break

				charIndex = tagEnd + 1
				continue

			# text
			if not textLine:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(self.x, 0)
				textLine.SetWindowVerticalAlignCenter()
				textLine.SetVerticalAlignCenter()
				textLine.Show()
			subtext = textLine.GetText()
			textLine.SetText(subtext + c)
			if textLine.GetTextWidth() + self.x >= self.limitWidth and self.limitWidth != 0:
				if subtext != "":
					textLine.SetText(subtext)
					self.childrenList.append(textLine)
					self.x += textLine.GetTextWidth()
					self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)
					textLine = None
				else:
					textLine = None
				break

			# increase char index
			charIndex += 1

		if textLine:
			self.childrenList.append(textLine)
			self.x += textLine.GetTextWidth()
			self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)
			textLine = None

		self.inputText = text[:charIndex]
		self.SetSize(self.x, self.maxHeight + self.extraHeight)
		self.UpdateRect()

		return charIndex

	def __ComputeTag(self, index, content):
		# tag <IMAGE []>
		if index == self.OBJECT_TYPE_IMAGE:
			if not content.has_key("path"):
				import dbg
				dbg.TraceError("Cannot read image tag : no path given")
				return False

			image = ImageBox()
			image.SetParent(self)
			image.SetPosition(self.x, 0)
			image.SetWindowVerticalAlignCenter()
			image.LoadImage(content["path"])
			image.Show()

			if content.has_key("y"):
				image.SetPosition(image.GetLeft(), int(content["y"]))

			if content.has_key("align") and content["align"].lower() == "center":
				image.SetPosition(self.limitWidth / 2 - image.GetWidth() / 2, 0)
			else:
				if self.x + image.GetWidth() >= self.limitWidth and self.limitWidth != 0:
					return False
				self.x += image.GetWidth()

			self.childrenList.append(image)
			self.maxHeight = max(self.maxHeight, image.GetHeight())

			return True

		# tag <TEXT []>
		elif index == self.OBJECT_TYPE_TEXT:
			if not content.has_key("text"):
				import dbg
				dbg.TraceError("Cannot read text tag : no text given")
				return False

			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetPosition(self.x, 0)
			textLine.SetWindowVerticalAlignCenter()
			textLine.SetVerticalAlignCenter()
			if content.has_key("r") and content.has_key("g") and content.has_key("b"):
				textLine.SetFontColor(int(content["r"]) / 255.0, int(content["g"]) / 255.0, int(content["b"]) / 255.0)
			elif content.has_key("color"):
				textLine.SetPackedFontColor(int(content["color"], 0))
			isLarge = False
			if content.has_key("font_size"):
				if content["font_size"].lower() == "large":
					isLarge = True
					textLine.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
			if content.has_key("bold"):
				if content["bold"] == "1" or content["bold"].lower() == "true":
					if isLarge:
						textLine.SetFontName(localeInfo.UI_DEF_FONT_LARGE_BOLD)
					else:
						textLine.SetFontName(localeInfo.UI_DEF_FONT_BOLD)
			if content.has_key("outline") and content["outline"] == "1":
				textLine.SetOutline()
			textLine.SetText(content["text"])
			textLine.Show()

			if self.x + textLine.GetTextWidth() >= self.limitWidth and self.limitWidth != 0:
				return False

			self.childrenList.append(textLine)
			self.x += textLine.GetTextWidth()
			self.maxHeight = max(self.maxHeight, textLine.GetTextHeight() + 2)

			return True

		# tag <HEIGHT []>
		elif index == self.OBJECT_TYPE_HEIGHT:
			if not content.has_key("size"):
				import dbg
				dbg.TraceError("Cannot read height tag : no size given")
				return False

			self.extraHeight += int(content["size"])

			return True

		# tag <WIDTH []>
		elif index == self.OBJECT_TYPE_WIDTH:
			if not content.has_key("size"):
				import dbg
				dbg.TraceError("Cannot read width tag : no size given")
				return False

			self.x += int(content["size"])

			return True

		return False

	def SetRenderingRect(self, left, top, right, bottom):
		self.renderingRect = {
			"left" : max(0, min(self.GetWidth(), int(-left * self.GetWidth()))),
			"top" : max(0, min(self.GetHeight(), int(-top * self.GetHeight()))),
			"right" : max(0, min(self.GetWidth(), int(-right * self.GetWidth()))),
			"bottom" : max(0, min(self.GetHeight(), int(-bottom * self.GetHeight()))),
		}

		self.__ApplyRenderingRect()

	def __ApplyRenderingRect(self):
		for child in self.childrenList:
			(x, y) = child.GetLocalPosition()
			childHeight = child.GetHeight()
			if isinstance(child, TextLine):
				childHeight = child.GetTextHeight()
			yEnd = y + childHeight

			renderTop = max(0, self.renderingRect["top"] - y)
			renderBottom = max(0, self.renderingRect["bottom"] - (self.GetHeight() - yEnd))

			child.SetRenderingRect(0, -float(renderTop) / childHeight, 0, -float(renderBottom) / childHeight)

	def GetTextHeight(self):
		tHeight = 0
		for child in self.childrenList:
			if isinstance(child, TextLine):
				if tHeight < child.GetHeight():
					tHeight = child.GetHeight()
			if isinstance(child, ImageBox):
				if tHeight < child.GetHeight():
					tHeight = child.GetHeight()

		return tHeight

	def GetTextWidth(self):
		tWidth = 0
		for child in self.childrenList:
			if isinstance(child, TextLine):
				tWidth += child.GetTextWidth()
			if isinstance(child, ImageBox):
				tWidth += child.GetWidth()

		return tWidth

class CheckBox_admin(Window):
	STATE_UNSELECTED = 0
	STATE_SELECTED = 1
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.state = self.STATE_UNSELECTED
		self.eventFunc = None
		self.eventArgs = None
		self.btnBox = {
			self.STATE_UNSELECTED : self.__init_MakeButton("d:/ymir work/ui/public/checkbox_unselected_%s.sub"),
			self.STATE_SELECTED : self.__init_MakeButton("d:/ymir work/ui/public/checkbox_selected_%s.sub"),
		}
		text = TextLine()
		text.SetParent(self)
		text.SetWindowVerticalAlignCenter()
		text.SetVerticalAlignCenter()
		text.Show()
		self.text = text
		self.__Refresh()
		self.SetWindowName("NONAME_CheckBox")
	def __del__(self):
		Window.__del__(self)
	def __init_MakeButton(self, path):
		btn = Button()
		btn.SetParent(self)
		btn.SetWindowVerticalAlignCenter()
		btn.SetUpVisual(path % "01")
		btn.SetOverVisual(path % "02")
		btn.SetDownVisual(path % "03")
		btn.SetDisableVisual(path % "01")
		btn.SAFE_SetEvent(self.OnClickButton)
		btn.baseWidth = btn.GetWidth()
		return btn
	def __UpdateRect(self):
		if self.text.GetText() != "":
			width = self.btnBox[self.state].baseWidth + 5 + self.text.GetTextWidth()
		else:
			width = self.btnBox[self.state].baseWidth
		height = max(self.btnBox[self.state].GetHeight(), self.text.GetTextHeight())
		self.SetSize(width, height)
		self.btnBox[self.state].SetSize(width, self.btnBox[self.state].GetHeight())
		self.text.SetPosition(self.btnBox[self.state].baseWidth + 5, 0)
		self.text.UpdateRect()
		self.btnBox[self.state].UpdateRect()
		self.UpdateRect()
	def __Refresh(self):
		self.__UpdateRect()
		self.btnBox[self.STATE_UNSELECTED].SetVisible(self.state == self.STATE_UNSELECTED)
		self.btnBox[self.STATE_SELECTED].SetVisible(self.state == self.STATE_SELECTED)
	def OnClickButton(self):
		if self.state == self.STATE_UNSELECTED:
			self.state = self.STATE_SELECTED
		else:
			self.state = self.STATE_UNSELECTED
		self.__Refresh()
		if self.eventFunc:
			apply(self.eventFunc, self.eventArgs)
	def SetChecked(self, state):
		self.state = state
		self.__Refresh()
	def IsChecked(self):
		return self.state != self.STATE_UNSELECTED
	def SetText(self, text):
		self.text.SetText(text)
		self.__UpdateRect()
	def SetEvent(self, event, *args):
		self.eventFunc = event
		self.eventArgs = args
	def SAFE_SetEvent(self, event, *args):
		self.eventFunc = __mem_func__(event)
		self.eventArgs = args
	def Disable(self):
		self.btnBox[self.STATE_UNSELECTED].Disable()
		self.btnBox[self.STATE_SELECTED].Disable()
	def Enable(self):
		self.btnBox[self.STATE_UNSELECTED].Enable()
		self.btnBox[self.STATE_SELECTED].Enable()

class BoxedBoard(Window):
	BORDER_TOP = 0
	BORDER_RIGHT = 1
	BORDER_BOTTOM = 2
	BORDER_LEFT = 3

	DEFAULT_BORDER_COLOR = grp.GenerateColor(0.3, 0.3, 0.3, 0.8)
	DEFAULT_BASE_COLOR = grp.GenerateColor(0, 0, 0, 0.5)

	def __init__(self):
		Window.__init__(self)

		self.borderSize = 1

		# Create Borders
		self.borders = [
			Bar(),
			Bar(),
			Bar(),
			Bar()
		]

		for border in self.borders:
			border.SetParent(self)
			border.AddFlag("not_pick")
			border.Show()

		# Create Base
		self.base = Bar()
		self.base.SetParent(self)
		self.base.AddFlag("not_pick")
		self.base.Show()

		# Set Default Colors
		self.SetBorderColor(self.DEFAULT_BORDER_COLOR)
		self.SetBaseColor(self.DEFAULT_BASE_COLOR)

	def __del__(self):
		self.Destroy()
		Window.__del__(self)

	def Destroy(self):
		del self.borders[:]
		self.base = None

		Window.Destroy(self)

	def SetBorderColor(self, color):
		for border in self.borders:
			border.SetColor(color)

	def SetBorderSize(self, borderSize):
		self.borderSize = borderSize
		self.SetSize(self.GetWidth(), self.GetHeight())

	def SetBaseColor(self, color):
		self.base.SetColor(color)

	def SetSize(self, width, height):
		width = max(width, (2 * self.borderSize) + 1)
		height = max(height, (2 * self.borderSize) + 1)

		Window.SetSize(self, width, height)
		self.UpdateBoard()

	def UpdateBoard(self):
		width = self.GetWidth()
		height = self.GetHeight()

		top, right, bottom, left = self.borders

		# Top Border
		top.SetSize(width - self.borderSize, self.borderSize)

		# Right Border
		right.SetSize(self.borderSize, height - self.borderSize)
		right.SetPosition(width - self.borderSize, 0)

		# Bottom Border
		bottom.SetSize(width - self.borderSize, self.borderSize)
		bottom.SetPosition(self.borderSize, height - self.borderSize)

		# Left Border
		left.SetSize(self.borderSize, height - self.borderSize)
		left.SetPosition(0, self.borderSize)

		# Base
		self.base.SetSize(width - (2 * self.borderSize), height - (2 * self.borderSize))
		self.base.SetPosition(self.borderSize, self.borderSize)

if app.ENABLE_LUCKY_BOX:
	class Input(Window):
		def __init__(self):
			Window.__init__(self)

			self.inputText = None
			self.eventDict={}
			self.eventFunc = {
				"MOUSE_LEFT_BUTTON_UP" : None,
				"MOUSE_LEFT_BUTTON_DOWN" : None,
				"MOUSE_RIGHT_BUTTON_UP" : None,
				"MOUSE_RIGHT_BUTTON_DOWN" : None,
				"MOUSE_OVER_IN" : None,
				"MOUSE_OVER_OUT" : None
			}
			self.eventArgs = {
				"MOUSE_LEFT_BUTTON_UP" : None,
				"MOUSE_LEFT_BUTTON_DOWN" : None,
				"MOUSE_RIGHT_BUTTON_UP" : None,
				"MOUSE_RIGHT_BUTTON_DOWN" : None,
				"MOUSE_OVER_IN" : None,
				"MOUSE_OVER_OUT" : None
			}


		def __del__(self):
			Window.__del__(self)

			self.inputText = None
			self.eventFunc = None
			self.eventArgs = None

		def MakeInput(self, width):
			imgLeft = ImageBox()
			imgCenter = ExpandedImageBox()
			imgRight = ImageBox()
			imgLeft.AddFlag("not_pick")
			imgCenter.AddFlag("not_pick")
			imgRight.AddFlag("not_pick")
			imgLeft.SetParent(self)
			imgCenter.SetParent(self)
			imgRight.SetParent(self)

			imgLeft.LoadImage("d:/ymir work/ui/pattern/border_c_left.tga")
			imgCenter.LoadImage("d:/ymir work/ui/pattern/border_c_middle.tga")
			imgRight.LoadImage("d:/ymir work/ui/pattern/border_c_right.tga")

			imgLeft.Show()
			imgCenter.Show()
			imgRight.Show()

			self.imgLeft = imgLeft
			self.imgCenter = imgCenter
			self.imgRight = imgRight

			self.SetWidth(width)

		def SetWidth(self, width):
			self.imgCenter.SetRenderingRect(0.0, 0.0, float((width - 42) - 21) / 21, 0.0)
			self.imgCenter.SetPosition(21, 0)
			self.imgRight.SetPosition(width - 21, 0)

			self.SetSize(width, 21)

		def GetText(self):
			if not self.inputText:
				return ""

			return self.inputText.GetText()

		def SetTextColor(self, color):
			if not self.inputText:
				return

			self.inputText.SetPackedFontColor(color)

		def SetText(self, text, x = 0, y = 0):
			if not self.inputText:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(self.GetWidth() / 2 - x, self.GetHeight() / 2 - y)
				textLine.SetVerticalAlignCenter()
				textLine.SetHorizontalAlignCenter()
				textLine.Show()
				self.inputText = textLine

			self.inputText.SetText(text)

		def SetEvent(self, func, *args) :
			result = self.eventFunc.has_key(args[0])
			if result :
				self.eventFunc[args[0]] = func
				self.eventArgs[args[0]] = args
			else :
				print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

		def SAFE_SetEvent(self, func, *args):
			result = self.eventFunc.has_key(args[0])
			if result :
				self.eventFunc[args[0]] = __mem_func__(func)
				self.eventArgs[args[0]] = args
			else :
				print "[ERROR] ui.py SAFE_SetEvent, Can`t Find has_key : %s" % args[0]

		def OnMouseLeftButtonUp(self):
			if self.eventFunc["MOUSE_LEFT_BUTTON_UP"] :
				apply(self.eventFunc["MOUSE_LEFT_BUTTON_UP"], self.eventArgs["MOUSE_LEFT_BUTTON_UP"])

		def OnMouseLeftButtonDown(self):
			if self.eventFunc["MOUSE_LEFT_BUTTON_DOWN"] :
				apply(self.eventFunc["MOUSE_LEFT_BUTTON_DOWN"], self.eventArgs["MOUSE_LEFT_BUTTON_DOWN"])

		def OnMouseRightButtonUp(self):
			if self.eventFunc["MOUSE_RIGHT_BUTTON_UP"] :
				apply(self.eventFunc["MOUSE_RIGHT_BUTTON_UP"], self.eventArgs["MOUSE_RIGHT_BUTTON_UP"])

		def OnMouseRightButtonDown(self):
			if self.eventFunc["MOUSE_RIGHT_BUTTON_DOWN"] :
				apply(self.eventFunc["MOUSE_RIGHT_BUTTON_DOWN"], self.eventArgs["MOUSE_RIGHT_BUTTON_DOWN"])

		def OnMouseOverIn(self) :
			if self.eventFunc["MOUSE_OVER_IN"] :
				apply(self.eventFunc["MOUSE_OVER_IN"], self.eventArgs["MOUSE_OVER_IN"])

		def OnMouseOverOut(self) :
			if self.eventFunc["MOUSE_OVER_OUT"] :
				apply(self.eventFunc["MOUSE_OVER_OUT"], self.eventArgs["MOUSE_OVER_OUT"])

class Shortcut(Window):
	IMAGES = {
		app.DIK_LCONTROL: "assets/ui/keyboard/keyboard_ctrl.png",
		app.DIK_LSHIFT: "assets/ui/keyboard/keyboard_shift.png",
		app.DIK_LALT: "assets/ui/keyboard/keyboard_alt.png",
		app.DIK_RCONTROL: "assets/ui/keyboard/keyboard_ctrl.png",
		app.DIK_RSHIFT: "assets/ui/keyboard/keyboard_shift.png",
		app.DIK_RALT: "assets/ui/keyboard/keyboard_alt.png",
		app.DIK_A: "assets/ui/keyboard/keyboard_a.png",
		app.DIK_B: "assets/ui/keyboard/keyboard_b.png",
		app.DIK_C: "assets/ui/keyboard/keyboard_c.png",
		app.DIK_D: "assets/ui/keyboard/keyboard_d.png",
		app.DIK_E: "assets/ui/keyboard/keyboard_e.png",
		app.DIK_F: "assets/ui/keyboard/keyboard_f.png",
		app.DIK_G: "assets/ui/keyboard/keyboard_g.png",
		app.DIK_H: "assets/ui/keyboard/keyboard_h.png",
		app.DIK_I: "assets/ui/keyboard/keyboard_i.png",
		app.DIK_J: "assets/ui/keyboard/keyboard_j.png",
		app.DIK_K: "assets/ui/keyboard/keyboard_k.png",
		app.DIK_L: "assets/ui/keyboard/keyboard_l.png",
		app.DIK_M: "assets/ui/keyboard/keyboard_m.png",
		app.DIK_N: "assets/ui/keyboard/keyboard_n.png",
		app.DIK_O: "assets/ui/keyboard/keyboard_o.png",
		app.DIK_P: "assets/ui/keyboard/keyboard_p.png",
		app.DIK_Q: "assets/ui/keyboard/keyboard_q.png",
		app.DIK_R: "assets/ui/keyboard/keyboard_r.png",
		app.DIK_S: "assets/ui/keyboard/keyboard_s.png",
		app.DIK_T: "assets/ui/keyboard/keyboard_t.png",
		app.DIK_U: "assets/ui/keyboard/keyboard_u.png",
		app.DIK_V: "assets/ui/keyboard/keyboard_v.png",
		app.DIK_W: "assets/ui/keyboard/keyboard_w.png",
		app.DIK_X: "assets/ui/keyboard/keyboard_x.png",
		app.DIK_Y: "assets/ui/keyboard/keyboard_y.png",
		app.DIK_Z: "assets/ui/keyboard/keyboard_z.png",
		app.DIK_F1: "assets/ui/keyboard/keyboard_f1.png",
		app.DIK_F2: "assets/ui/keyboard/keyboard_f2.png",
		app.DIK_F3: "assets/ui/keyboard/keyboard_f3.png",
		app.DIK_F4: "assets/ui/keyboard/keyboard_f4.png",
		app.DIK_F5: "assets/ui/keyboard/keyboard_f5.png",
		app.DIK_F6: "assets/ui/keyboard/keyboard_f6.png",
		app.DIK_F7: "assets/ui/keyboard/keyboard_f7.png",
		app.DIK_F8: "assets/ui/keyboard/keyboard_f8.png",
		app.DIK_F9: "assets/ui/keyboard/keyboard_f9.png",
		app.DIK_RETURN : "assets/ui/keyboard/keyboard_enter.png",
		app.DIK_DELETE : "assets/ui/keyboard/keyboard_delete.png",
		app.DIK_LMBUTTON: "assets/ui/keyboard/keyboard_mouse_left.png",
		app.DIK_RMBUTTON: "assets/ui/keyboard/keyboard_mouse_right.png",
	}

	def __init__(self):
		Window.__init__(self)

		self.outline = False

		self.shortcut = []
		self.elements = []

	def __del__(self):
		Window.__del__(self)

		del self.elements[:]

	def SetOutline(self, outline = True):
		self.outline = outline

	def SetShortcut(self, shortcut):
		self.shortcut = shortcut
		self.Refresh()

	def Refresh(self):
		del self.elements[:]
		self.elements = []

		x = 0
		for shortcut in self.shortcut:
			if x > 0:
				textLine = TextLine()
				textLine.SetParent(self)
				textLine.SetPosition(x, 2)
				if self.outline:
					textLine.SetOutline(True)
				textLine.SetText("+")
				textLine.Show()

				x += 12
				self.elements.append(textLine)

			image = ImageBox()
			image.SetParent(self)
			image.SetPosition(x, 0)
			image.LoadImage(self.IMAGES[shortcut])
			image.Show()

			x += image.GetWidth() + 3
			self.elements.append(image)

		self.SetSize(x - 3, 20)

class MultiTextLine(Window):

	RETURN_STRING = "[ENTER]"
	LINE_HEIGHT = 15

	def __init__(self):
		Window.__init__(self)

		self.isSetFontColor = False
		self.r = 0.0
		self.g = 0.0
		self.b = 0.0
		self.packedFontColor = -1
		self.textColorDict = {}

		self.lines = []
		self.hAlignCenter = False
		self.vAlignCenter = False
		self.windowVAlignCenter = False
		self.isOutline = False
		self.text = ""
		self.basePos = 0
		self.maxTextWidth = 0
		self.realX = 0
		self.realY = 0

		self.SetWindowName("NONAME_MultiTextLine")

	def __del__(self):
		Window.__del__(self)

	def SetWidth(self, width):
		self.SetSize(width, self.GetHeight())
		self.SetText(self.GetText())

	def SetHeight(self, height):
		self.SetSize(self.GetWidth(), height)
		self.SetText(self.GetText())

	def RegisterPackedFontColor(self, name, color):
		self.textColorDict[name] = color

	def SetRegisteredColor(self, name):
		if self.textColorDict.has_key(name):
			self.SetPackedFontColor(self.textColorDict[name])

	def SetAlpha(self, alpha):
		for line in self.lines:
			line.SetAlpha(alpha)

	def NewTextLine(self):
		line = TextLine()
		line.xRect = 0.0
		line.SetParent(self)
		if self.hAlignCenter == True:
			line.SetWindowHorizontalAlignCenter()
			line.SetHorizontalAlignCenter()
		if self.vAlignCenter == True:
			line.SetVerticalAlignCenter()
		if self.isSetFontColor == True:
			if self.packedFontColor != -1:
				line.SetPackedFontColor(self.packedFontColor)
			else:
				line.SetFontColor(self.r, self.g, self.b)
		if self.isOutline == True:
			line.SetOutline()
		line.Show()
		self.lines.append(line)

		return self.lines[len(self.lines) - 1]

	def Clear(self):
		self.text = ""
		self.lines = []

	def SetTextHorizontalAlignCenter(self):
		self.hAlignCenter = True
		self.SetText(self.GetText())

	def SetTextVerticalAlignCenter(self):
		self.vAlignCenter = True
		self.SetText(self.GetText())

	def SetOutline(self):
		self.isOutline = True
		self.SetText(self.GetText())

	def SetFontColor(self, r, g, b):
		self.isSetFontColor = True
		self.r = r
		self.g = g
		self.b = b

	def SetPackedFontColor(self, color, lineIdx=-1):
		if lineIdx == -1:
			self.isSetFontColor = True
			self.packedFontColor = color
			for line in self.lines:
				line.SetPackedFontColor(color)
		else:
			self.lines[lineIdx].SetPackedFontColor(color)

	def SetText(self, text):
		self.Clear()

		self.text = text
		self.maxTextWidth = 0

		line = self.NewTextLine()
		pos = 0
		newStartPos = 0
		while pos < len(text):
			curTextWidth = line.GetSpecificTextWidth(text[:pos+1])
			#line.SetText(text[:pos+1])

			newLine = False
			if len(text) >= pos + len(self.RETURN_STRING):
				if text[pos:pos+len(self.RETURN_STRING)] == self.RETURN_STRING:
					newLine = True
					newStartPos = pos+len(self.RETURN_STRING)
			if newLine == False and pos > 0:
				if curTextWidth > self.GetWidth() and self.GetWidth() > 0:
					newLine = True

					curText = text[:pos+1]
					breakPos = curText.rfind(" ")
					if breakPos == -1:
						if curText.find("|Hlink:") != -1:
							newLine = False
						else:
							breakPos = curText.rfind(".")
							if breakPos == -1:
								breakPos = curText.rfind(",")
								if breakPos == -1:
									breakPos = curText.rfind(";")
									if breakPos == -1:
										breakPos = curText.rfind(":")
							if breakPos != -1:
								breakPos += 1
					if breakPos != -1:
						pos = breakPos
						newStartPos = pos
					else:
						newStartPos = pos

			if newLine == True:
				line.SetText(text[:pos])
				curTextWidth = line.GetTextWidth()
#				if line.GetTextWidth() > self.GetWidth() and self.GetWidth() > 0:
#					line.ShowPercentage(0.0, 1.0 - (line.GetTextWidth() - self.GetWidth()) / float(line.GetTextWidth()))
#					line.xRect = -(line.GetTextWidth() - self.GetWidth()) / float(line.GetTextWidth())

				line = self.NewTextLine()
				text = text[newStartPos:]
				if text[:1] == " ":
					text = text[1:]
				pos = 0
			else:
				pos += 1
				if pos >= len(text):
					pass
#					if line.GetTextWidth() > self.GetWidth() and self.GetWidth() > 0:
#						line.ShowPercentage(0.0, 1.0 - (line.GetTextWidth() - self.GetWidth()) / float(line.GetTextWidth()))
#						line.xRect = -(line.GetTextWidth() - self.GetWidth()) / float(line.GetTextWidth())

			self.maxTextWidth = max(self.maxTextWidth, curTextWidth)
			if self.GetWidth() > 0 and self.maxTextWidth > self.GetWidth():
				self.maxTextWidth = self.GetWidth()

		line.SetText(text)

		self.ShowBetween(self.GetLineCount() - self.GetViewLineCount(), self.GetLineCount() - 1)
		#self.SetSize(self.GetWidth(), len(self.lines) * self.LINE_HEIGHT)

		self.SetPosition(self.realX, self.realY)

	def GetMaxTextWidth(self):
		return self.maxTextWidth

	def GetLine(self, index):
		if index < 0 or index >= len(self.lines):
			return None
		return self.lines[index]

	def GetLastLine(self):
		return self.GetLine(len(self.lines) - 1)

	def GetLineCount(self):
		return len(self.lines)

	def GetViewLineCount(self):
		if self.GetHeight() == 0:
			return self.GetLineCount()
		return self.GetHeight() / self.LINE_HEIGHT

	def SetBasePos(self, basePos):
		self.basePos = basePos

		self.ShowBetween(self.basePos, self.basePos + self.GetViewLineCount() - 1)

	def GetBasePos(self):
		return self.basePos

	def ShowBetween(self, start, end):
		start = max(0, start)
		end = min(self.GetLineCount() - 1, end)

		height = self.GetHeight()
		if height == 0:
			height = self.GetLineCount() * self.LINE_HEIGHT

		for i in xrange(len(self.lines)):
			if i < start or i > end:
				self.lines[i].Hide()
			else:
				self.lines[i].SetPosition(0, (i - start) * self.LINE_HEIGHT)
				self.lines[i].Show()

	def GetRealHeight(self):
		if self.GetHeight() > 0:
			return self.GetHeight()

		return self.GetLineCount() * self.LINE_HEIGHT

	def SetWindowVerticalAlignCenter(self):
		Window.SetWindowVerticalAlignCenter(self)
		self.windowVAlignCenter = True

		if self.GetHeight() == 0:
			self.SetPosition(self.realX, self.realY)

	def SetPosition(self, x, y):
		self.realX = x
		self.realY = y
		if self.windowVAlignCenter and self.GetHeight() == 0:
			Window.SetPosition(self, x, y - self.GetRealHeight() / 2)
		else:
			Window.SetPosition(self, x, y)

	def GetBottom(self):
		return self.GetTop() + self.GetRealHeight()

	def GetText(self):
		return self.text

	def SetYRenderingRect(self, sy, ey):
		sy = max(0, sy)
		ey = min(self.GetRealHeight(), ey)

		for i in xrange(len(self.lines)):
			line = self.lines[i]
			if sy >= line.GetBottom() or ey <= line.GetTop() or ey <= sy:
				line.SetRenderingRect(0.0, 0.0, line.xRect, -1.0)
			elif line.GetTextHeight() > 0:
				line.SetRenderingRect(0.0, -min(1.0, float(max(0, sy - line.GetTop())) / line.GetTextHeight()), line.xRect, max(-1.0, float(min(0, ey - line.GetTop() - line.GetTextHeight())) / line.GetTextHeight()))

class ThinBoardDailyReward(Window):
	CORNER_WIDTH = 16
	CORNER_HEIGHT = 16
	LINE_WIDTH = 16
	LINE_HEIGHT = 16

	LT = 0
	LB = 1
	RT = 2
	RB = 3

	L = 0
	R = 1
	T = 2
	B = 3

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)

		CornerFileNames = ""
		dir = ""

		CornerFileNames = [ "d:/ymir work/ui/game/daily_reward/thinboard/ThinBoard_Corner_"+dir+".tga" for dir in ["LeftTop","LeftBottom","RightTop","RightBottom"] ]
		LineFileNames = [ "d:/ymir work/ui/game/daily_reward/thinboard/ThinBoard_Line_"+dir+".tga" for dir in ["Left","Right","Top","Bottom"] ]

		self.MakeBase()

		self.Corners = []
		for fileName in CornerFileNames:
			Corner = ExpandedImageBox()
			Corner.AddFlag("attach")
			Corner.AddFlag("not_pick")
			Corner.LoadImage(fileName)
			Corner.SetParent(self)
			Corner.SetPosition(0, 0)
			Corner.Show()
			self.Corners.append(Corner)

		self.Lines = []
		for fileName in LineFileNames:
			Line = ExpandedImageBox()
			Line.AddFlag("attach")
			Line.AddFlag("not_pick")
			Line.LoadImage(fileName)
			Line.SetParent(self)
			Line.SetPosition(0, 0)
			Line.Show()
			self.Lines.append(Line)

		self.Lines[self.L].SetPosition(0, self.CORNER_HEIGHT)
		self.Lines[self.T].SetPosition(self.CORNER_WIDTH, 0)

	def __del__(self):
		Window.__del__(self)

	def SetSize(self, width, height):

		width = max(self.CORNER_WIDTH*2, width)
		height = max(self.CORNER_HEIGHT*2, height)
		Window.SetSize(self, width, height)

		self.Corners[self.LB].SetPosition(0, height - self.CORNER_HEIGHT)
		self.Corners[self.RT].SetPosition(width - self.CORNER_WIDTH, 0)
		self.Corners[self.RB].SetPosition(width - self.CORNER_WIDTH, height - self.CORNER_HEIGHT)
		self.Lines[self.R].SetPosition(width - self.CORNER_WIDTH, self.CORNER_HEIGHT)
		self.Lines[self.B].SetPosition(self.CORNER_HEIGHT, height - self.CORNER_HEIGHT)

		verticalShowingPercentage = float((height - self.CORNER_HEIGHT*2) - self.LINE_HEIGHT) / self.LINE_HEIGHT
		horizontalShowingPercentage = float((width - self.CORNER_WIDTH*2) - self.LINE_WIDTH) / self.LINE_WIDTH

		self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
		self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
		self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)

		if self.Base:
			self.Base.SetRenderingRect(0, 0, (float(width)-32)/float(self.Base.GetWidth()) - 1.0, (float(height)-32)/float(self.Base.GetHeight()) - 1.0)

	def MakeBase(self):
		self.Base = ExpandedImageBox()
		self.Base.AddFlag("not_pick")
		self.Base.LoadImage("d:/ymir work/ui/game/daily_reward/thinboard/thinboard_base.tga")
		self.Base.SetParent(self)
		self.Base.SetPosition(16, 16)
		self.Base.SetAlpha(0.9)
		self.Base.Show()

	def ShowInternal(self):
		self.Base.Show()
		for wnd in self.Lines:
			wnd.Show()
		for wnd in self.Corners:
			wnd.Show()

	def HideInternal(self):
		self.Base.Hide()
		for wnd in self.Lines:
			wnd.Hide()
		for wnd in self.Corners:
			wnd.Hide()

	def ColorThinBoard(self, r, g, b, a):
		self.Base.SetColor(r, g, b, a)
		for wnd in self.Lines:
			wnd.SetColor(r, g, b, a)

		for wnd in self.Corners:
			wnd.SetColor(r, g, b, a)

	def ShowCorner(self, corner):
		self.Corners[corner].Show()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def HideCorners(self, corner):
		self.Corners[corner].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def ShowLine(self, line):
		self.Lines[line].Show()
		self.SetSize(self.GetWidth(), self.GetHeight())

	def HideLine(self, line):
		self.Lines[line].Hide()
		self.SetSize(self.GetWidth(), self.GetHeight())

class FineListBox(Window):
	class FineListBoxItem(Window):
		def __init__(self,color = 0xff0099ff, height = 40, bEnableColor = False):
			Window.__init__(self)
			self.SetColor(color)
			self.bEnableColor = bEnableColor

			self.width  = 100
			self.height = height
			self.minh   = 0
			self.maxh   = height

			self.components = []

		def __del__(self):
			Window.__del__(self)

		def Destroy(self):
			Window.Destroy(self)

			self.components = None

		# Set Background Color
		def SetColor(self, color = 0xff0099ff):
			self.color = color

		def SetParent(self, parent):
			Window.SetParent(self, parent)
			self.parent=proxy(parent)

		# Functions for Height and Width
		def SetHeight(self,h):
			self.SetSize(self.width,h)

		def SetWidth(self,w):
			self.SetSize(w,self.height)

		def SetSize(self,w,h):
			self.width  = w
			self.height = h
			self.maxh   = h
			Window.SetSize(self,w,h)

		# Set the minimum y Position for Rendering
		def SetRenderMin(self, minh):
			self.minh = minh
			self.maxh = self.height
			self.RecalculateRenderedComponents()

		def SetRenderMax(self, maxh):
			self.maxh = maxh
			self.minh = 0
			self.RecalculateRenderedComponents()

		def RegisterComponent(self,component):
			mtype       = type(component).__name__
			if mtype == "Bar":
				(x,y, w,h)            = component.GetRect()
				(x,y)                 = component.GetLocalPosition()
				component.__list_data = [x,y,w,h]
			self.components.append(component)

		def UnregisterComponent(self,component):
			self.components.remove(component)
			if component.__list_data:
				component.__list_data = None

		def RecalculateRenderedComponents(self):
			for component in self.components:
				# Get Size and Position
				(xl,yl)    = component.GetLocalPosition()
				(x,y, w,h) = component.GetRect()
				mtype       = type(component).__name__
				if mtype == "TextLine":
					(w,h) = component.GetTextSize()


				if yl + h < self.minh:
					# Komponente ist nicht sichtbar (oben)
					component.Hide()
				elif yl > self.maxh:
					# Komponente ist nicht sichtbar (unten)
					component.Hide()
				else:
					if mtype == "ExpandedImageBox":
						miny = 0
						if self.minh > 0 and yl < self.minh:
							miny = -float(self.minh-yl)/float(h)

						maxy = 0
						if h != 0:
							maxy = float(self.maxh-yl-h)/float(h)

						maxy = min(0,max(-1,maxy))

						component.SetRenderingRect(0.0,miny,0.0, maxy)
						component.Show()
					else:
						if yl < self.minh or yl + h > self.maxh:
							component.Hide()
						else:
							component.Show()

		# Lulz, I got Clicked!
		def OnMouseLeftButtonDown(self):
			self.parent.SelectItem(self)

		def OnRender(self):
			if self.bEnableColor:
				x, y = self.GetGlobalPosition()
				grp.SetColor(self.color)
				grp.RenderBar(x, y+self.minh, self.GetWidth(), self.maxh-self.minh)

	def __init__(self):
		Window.__init__(self)

		self.items     = []         # Itemlist
		self.selected  = None       # Current selected Item
		self.basePos   = 0          # Scroll Position
		self.itemWidth = 100
		self.itemStep  = 4         # Step between 2 items
		self.scrollbar = None

		self.isModernScrollBar = False
		self.selectEvent = None     # Fired when an item gets selected

	def Destroy(self):
		Window.Destroy(self)

		self.items = None

	def SetItemStep(self, itemStep):
		self.itemStep = itemStep

	def SetSize(self,w,h):
		Window.SetSize(self,w,h)
		self.SetItemWidth(w)

		self.UpdateList()

	def SetScrollBar(self, scrollbar, isModernScrollBar = False):
		self.scrollbar = scrollbar
		self.scrollbar.SetScrollEvent(__mem_func__(self.__OnScroll))
		self.scrollbar.SetScrollStep(0.10)

		self.isModernScrollBar = isModernScrollBar

		self.UpdateList()

	def CalcTotalItemHeight(self):
		total_height = 0
		for item in self.items:
			total_height += item.GetHeight()
			total_height += self.itemStep

		# if total_height > self.itemStep:
			# total_height -= 2* self.itemStep
		return total_height

	def ConfigureScrollBar(self):
		if self.scrollbar:
			itemheight = self.CalcTotalItemHeight()
			myheight   = self.GetHeight()- 2 * self.itemStep
			dif = 0.97
			if itemheight > myheight and itemheight != 0:
				dif = 1.0 * myheight / itemheight

			self.scrollbar.SetMiddleBarSize(dif)

	def __OnScroll(self):
		pos   = self.scrollbar.GetPos()
		toscr = self.CalcTotalItemHeight() - self.GetHeight() + 2* self.itemStep
		self.basePos = toscr * pos

		self.UpdateList()

	def SelectItem(self,item):
		self.selected = item

		if self.selectEvent:
			self.selectEvent(item)


	def AppendItem(self,item):
		item.SetParent(self)
		item.SetWidth(self.itemWidth);
		item.Show()
		self.items.append(item)

		self.UpdateList()

	def ClearItems(self):
		map(lambda wnd: wnd.Hide(), self.items)
		del self.items[:]

		self.basePos = 0
		if self.scrollbar:
			self.scrollbar.SetPos(0)
		self.UpdateList()

	def RemoveItem(self,item):
		self.items.remove(item)
		self.UpdateList()

	def UpdateList(self):
		self.ConfigureScrollBar()
		self.RecalcItemPositions()

	def IsEmpty(self):
		if len(self.itemList)==0:
			return 1
		return 0

	def SetItemWidth(self,w):
		self.itemWidth = w
		for item in self.items:
			item.SetWidth(w)

	# Set the Item-Positions
	def RecalcItemPositions(self):
		curbp = self.basePos

		itemheight = self.CalcTotalItemHeight()
		myheight   = self.GetHeight() - 2 * self.itemStep

		if itemheight < myheight:
			curbp = 0
			return




		fromPos = curbp
		curPos  = 0
		toPos   = curbp + self.GetHeight()
		for item in self.items:
			hw = item.GetHeight()
			if curPos+hw < fromPos:
				# Item ist nicht zu sehen (oben)
				# item.SetColor(0xffff0000)
				item.Hide()
			elif curPos < fromPos and curPos+hw> fromPos:
				# Item ist nur teilweise zu sehen (oben)
				# item.SetColor(0xffffcc00)
				item.SetRenderMin(fromPos-curPos)
				item.Show()
			elif curPos < toPos and curPos+hw > toPos:
				# Item ist nur teilweise zu sehen (unten)
				# item.SetColor(0xffffcc00)
				item.SetRenderMax(toPos-curPos)
				item.Show()
			elif curPos > toPos:
				# Item ist nicht zu sehen (unten)
				# item.SetColor(0xffff0000)
				item.Hide()
			else:
				# Item vollstandig sichtbar
				# item.SetColor(0xff00ff00)
				item.SetRenderMin(0)
				item.Show()

			item.SetPosition(0,curPos- fromPos)
			curPos+= hw+self.itemStep

	def OnWheelMove(self, len):
		if not self.scrollBar:
			return False

		if not self.isModernScrollBar:
			return False

		return self.scrollBar.OnWheelMove(len)

class Graph(Window):

	def __init__(self):
		Window.__init__(self)

		self.yMinValue = 0.0
		self.yMaxValue = 100.0
		self.xMinValue = 0.0
		self.xMaxValue = 10.0

		self.renderColor = grp.GenerateColor(1.0, 0.0, 0.0, 1.0)

		self.keyList = []
		self.valueList = []

	def SetYAxisLimitValue(self, minValue, maxValue):
		self.yMinValue = float(minValue)
		self.yMaxValue = float(maxValue)

	def SetXAxisLimitValue(self, minValue, maxValue):
		self.xMinValue = float(minValue)
		self.xMaxValue = float(maxValue)

	def Clear(self):
		self.keyList = []
		self.valueList = []

	def AddValue(self, xAxisPosition, yAxisValue):
		xAxisPosition = float(xAxisPosition)
		yAxisValue = float(yAxisValue)

		if xAxisPosition in self.keyList:
			import dbg
			dbg.TraceError("Cannot add value to bar graph : already existing xAxisPosition (" + str(xAxisPosition) + ", " + str(yAxisValue) + ")")
			return

		self.keyList.append(xAxisPosition)
		self.valueList.append({ "x" : xAxisPosition, "y" : yAxisValue })

	def Refresh(self):
		self.valueList = sorted(self.valueList, key = lambda val: val["x"])

	def SetColor(self, color):
		self.renderColor = color

	def OnRender(self):
		grp.SetColor(self.renderColor)

class LineGraph(Graph):

	def __init__(self):
		Graph.__init__(self)

		self.lineThickness = 1

		self.lastOverPos = -1
		self.overEvent = None
		self.outEvent = None

	def SetLineThickness(self, thickness):
		self.lineThickness = thickness

	def SetOverLineEvent(self, event):
		self.overEvent = event

	def SetOutLineEvent(self, event):
		self.outEvent = event

	def __GetYPosition(self, xPosition):
		if xPosition < 0 or xPosition >= self.GetWidth():
			return -1

		width = float(self.GetWidth())
		height = float(self.GetHeight())
		valueXRange = self.xMaxValue - self.xMinValue
		valueYRange = self.yMaxValue - self.yMinValue

		lastPos = (0, 0)
		for data in self.valueList:
			renderX = int((data["x"] - self.xMinValue) / valueXRange * width)
			renderY = int((data["y"] - self.yMinValue) / valueYRange * height)

			if xPosition >= lastPos[0] and xPosition <= renderX:
				factor = 1.0
				if renderX - lastPos[0] > 0:
					factor = (xPosition - lastPos[0]) / float(renderX - lastPos[0])

				mouseRenderY = int(factor * (renderY - lastPos[1]) + lastPos[1])
				return self.GetHeight() - mouseRenderY

			lastPos = (renderX, renderY)

		return -1

	def __GetValueByXPos(self, xPosition):
		if xPosition < 0 or xPosition >= self.GetWidth():
			return -1

		width = float(self.GetWidth())
		height = float(self.GetHeight())
		valueXRange = self.xMaxValue - self.xMinValue
		valueYRange = self.yMaxValue - self.yMinValue

		lastPos = (0, 0, 0)
		for data in self.valueList:
			renderX = int((data["x"] - self.xMinValue) / valueXRange * width)
			renderY = int((data["y"] - self.yMinValue) / valueYRange * height)

			if xPosition >= lastPos[0] and xPosition <= renderX:
				factor = 1.0
				if renderX - lastPos[0] > 0:
					factor = (xPosition - lastPos[0]) / float(renderX - lastPos[0])

				return self.yMinValue + ((lastPos[2] - self.yMinValue) * (1.0 - factor) + (data["y"] - self.yMinValue) * factor)

			lastPos = (renderX, renderY, data["y"])

		return -1

	def __RenderElem(self, data, lastXPos, lastYPos):
		(x, y) = self.GetGlobalPosition()

		width = float(self.GetWidth())
		height = float(self.GetHeight())
		valueXRange = self.xMaxValue - self.xMinValue
		valueYRange = self.yMaxValue - self.yMinValue

		renderX = lastXPos
		renderY = lastYPos
		renderEndX = int((data["x"] - self.xMinValue) / valueXRange * width)
		renderEndY = int((data["y"] - self.yMinValue) / valueYRange * height)

		if renderX < renderEndX:
			renderWidth = renderEndX - renderX
			renderHeight = renderEndY - renderY

			for i in xrange(self.lineThickness):
				change = (i + 1) / 2
				if i % 2 == 0:
					grp.RenderLine(x + renderX, y + height - renderY - change, renderWidth, -renderHeight)
				else:
					grp.RenderLine(x + renderX, y + height - renderY + change, renderWidth, -renderHeight)

		return (renderEndX, renderEndY)

	def OnRender(self):
		Graph.OnRender(self)

		lastPos = (0, 0)
		for data in self.valueList:
			lastPos = self.__RenderElem(data, lastPos[0], lastPos[1])

	def OnUpdate(self):
		if self.IsIn():
			(xMouse, yMouse) = self.GetMouseLocalPosition()
			for i in xrange(4 + 3 * self.lineThickness):
				xAdjust = (i + 1) / 2
				if i % 2 == 0:
					xAdjust = -xAdjust

				y = self.__GetYPosition(xMouse + xAdjust)
				if abs(yMouse - y) < 10:
					if xMouse != self.lastOverPos:
						self.lastOverPos = xMouse
						if self.overEvent:
							self.overEvent(xMouse, y, self.__GetValueByXPos(xMouse))
					return

		if self.lastOverPos != -1:
			self.lastOverPos = -1
			if self.outEvent:
				self.outEvent()

class BarGraph(Graph):

	def __init__(self):
		Graph.__init__(self)

		self.barSpace = 1

	def SetBarSpace(self, space):
		self.barSpace = int(space)

	def __RenderElem(self, data, endXValue, addSpace = True):
		(x, y) = self.GetGlobalPosition()

		width = self.GetWidth()
		height = self.GetHeight()
		valueXRange = self.xMaxValue - self.xMinValue
		valueYRange = self.yMaxValue - self.yMinValue

		renderX = int((data["x"] - self.xMinValue) / valueXRange * width)
		renderY = 0
		renderWidth = int((endXValue - data["x"]) / valueXRange * width)
		renderHeight = int((data["y"] - self.yMinValue) / valueYRange * height)

		if addSpace:
			renderWidth -= self.barSpace

		if renderWidth > 0.0 and renderHeight > 0.0:
			grp.RenderBar(x + renderX, y + renderY + height - renderHeight, renderWidth, renderHeight)

	def OnRender(self):
		Graph.OnRender(self)

		lastPair = { "x" : self.xMinValue, "y" : self.yMinValue }
		for data in self.valueList:
			self.__RenderElem(lastPair, data["x"])
			lastPair = data

		self.__RenderElem(lastPair, self.xMaxValue, False)

class SelectableTextLine(TextLine):

	STATE_NONE = 0
	STATE_OVER = 1
	STATE_DOWN = 2

	def __init__(self, autoResize = True):
		TextLine.__init__(self)

		self.autoResize = autoResize
		self.state = self.STATE_NONE
		self.clickEvent = lambda: None

		self.sColors = {
			"normal" : 0xFFffffff,
			"over" : 0xFF686863,
			"down" : 0xFF63630E
		}

	def SetEvent(self, event):
		self.clickEvent = event

	def SetColors(self, colors):
		for name, color in colors.items():
			self.sColors[name] = color

		TextLine.SetPackedFontColor(self, self.sColors["normal"])

	def SetText(self, text):
		TextLine.SetText(self, text)

		if self.autoResize:
			self.SetSize(self.GetTextWidth(), self.GetTextHeight())

	def OnMouseOverIn(self):
		TextLine.SetPackedFontColor(self, self.sColors["over"])

	def OnMouseOverOut(self):
		TextLine.SetPackedFontColor(self, self.sColors["normal"])

	def OnMouseLeftButtonDown(self):
		TextLine.SetPackedFontColor(self, self.sColors["down"])

	def OnMouseLeftButtonUp(self):
		# if self.state == self.STATE_DOWN:
		self.clickEvent()

		if self.IsIn():
			TextLine.SetPackedFontColor(self, self.sColors["over"])
		else:
			TextLine.SetPackedFontColor(self, self.sColors["normal"])

class ModernGauge(Window):
	class _Scaleable(Window):
		def __init__(self, leftFile, centerFile, rightFile):
			Window.__init__(self)

			left = ImageBox()
			left.SetParent(self)
			left.LoadImage(leftFile)
			left.Show()

			center = ExpandedImageBox()
			center.SetParent(self)
			center.SetPosition(left.GetWidth(), 0)
			center.LoadImage(centerFile)
			center.Show()

			right = ImageBox()
			right.SetParent(self)
			right.SetWindowHorizontalAlignRight()
			right.LoadImage(rightFile)
			right.SetPosition(right.GetWidth(), 0)
			right.Show()

			self.left = left
			self.center = center
			self.right = right

		def __del__(self):
			Window.__del__(self)

		def Destroy(self):
			Window.Destroy(self)

			self.left.Destroy()
			self.left = None

			self.center.Destroy()
			self.center = None

			self.right.Destroy()
			self.right = None

		def SetSize(self, width, height = 4):
			# Force height
			height = 4

			Window.SetSize(self, width, height)

			self.center.SetRenderingRect(0.0, 0.0, width - self.left.GetWidth() - self.right.GetWidth() - 1.0, 0.0)
			self.right.UpdateRect()

		def SetWidth(self, width):
			self.SetSize(width)

		def SetPercentage(self, percentage, realWidth):
			percentage = min(max(0.0, float(percentage)), 1.0)

			lrWidth = self.left.GetWidth() + self.right.GetWidth()
			centerMaxWidth = float(realWidth - lrWidth)

			self.SetWidth(lrWidth + centerMaxWidth * percentage)

	COLORS = ["green", "yellow", "blue", "red"]

	GREEN = 0
	YELLOW = 1
	BLUE = 2
	RED = 3

	UI_ROOT = "assets/ui/bars/"

	def __init__(self, color):
		Window.__init__(self)

		self.currentPercentage = 0.0
		self.targetPercentage = 0.0

		self.Create(color)

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		Window.Destroy(self)

		self.background.Destroy()
		self.background = None

		self.gauge.Destroy()
		self.gauge = None

	def Create(self, color):
		self.background = self._Scaleable(self.UI_ROOT + "empty-left.png", self.UI_ROOT + "empty-center.png", self.UI_ROOT + "empty-right.png")
		self.background.SetParent(self)
		self.background.Show()

		self.gauge = self._Scaleable(self.UI_ROOT + self.COLORS[color] + "-left.png", self.UI_ROOT + self.COLORS[color] + "-center.png", self.UI_ROOT + self.COLORS[color] + "-right.png")
		self.gauge.SetParent(self)
		self.gauge.Show()

	def SetSize(self, width, height = 4):
		# Force height
		height = 4

		Window.SetSize(self, width, height)
		self.background.SetWidth(width)
		self.gauge.SetWidth(width)

	def SetWidth(self, width):
		self.SetSize(width)

	def SetPercentage(self, percentage):
		self.targetPercentage = percentage

	def OnUpdate(self):
		if self.currentPercentage == self.targetPercentage:
			return

		delta = 0.03
		if self.targetPercentage > self.currentPercentage:
			self.currentPercentage += delta
			if self.currentPercentage > self.targetPercentage:
				self.currentPercentage = self.targetPercentage
		else:
			self.currentPercentage -= delta
			if self.currentPercentage < self.targetPercentage:
				self.currentPercentage = self.targetPercentage

		self.gauge.SetPercentage(self.currentPercentage, self.background.GetWidth())

class PixelScrollListBox(Window):
	class Item(Window):
		def __init__(self, height=0):
			Window.__init__(self)

			self.SetSize(0, height)

			self.removeTopPixel = 0
			self.removeBottomPixel = 0

			self.elems = []

		def Destroy(self):
			Window.Destroy(self)
			self.elems = []

		def AddObj(self, elem, alignVerticalCenter = False):
			return self._AddElement(elem, alignVerticalCenter)

		def _AddElement(self, elem, alignVerticalCenter = False):
			elem.SetParent(self)
			elem.Show()
			if alignVerticalCenter:
				elem.SetWindowVerticalAlignCenter()
			self.elems.append(elem)
			return elem

		def SetRemovePixel(self, top, bottom):
			if self.removeTopPixel == top and self.removeBottomPixel == bottom:
				return

			self.removeTopPixel = top
			self.removeBottomPixel = bottom

			topPct = float(top) / self.GetHeight()
			bottomPct = float(bottom) / self.GetHeight()
			self._OnSetRenderingRect()

		def GetRemovedTopPixel(self):
			return self.removeTopPixel

		def GetRemovedBottomPixel(self):
			return self.removeBottomPixel

		def _OnSetRenderingRect(self):
			# pass
			startY = self.GetRemovedTopPixel()
			endY = self.GetHeight() - self.GetRemovedBottomPixel()

			for elem in self.elems:
				elemPosX, elemPosY = elem.GetLocalPosition(self)

				elemHeight = elem.GetHeight()
				if elemHeight == 0:
					if isinstance(elem, TextLine):
						elemHeight = elem.GetTextHeight()
					else:
						continue

				topPixel = max(0, startY - elemPosY)
				bottomPixel = max(0, (elemPosY + elemHeight) - endY)
				topPct = float(topPixel) / elemHeight
				bottomPct = float(bottomPixel) / elemHeight

				if isinstance(elem, ExpandedImageBox) or\
					isinstance(elem, Button) or\
					isinstance(elem, TextLine) or\
					isinstance(elem, ExtendedTextLine):
					elem.SetRenderingRect(0, -topPct, 0, -bottomPct)

	def __init__(self):
		Window.__init__(self)

		self.items = []
		self.__Initialize()

		self.verticalElementSpace = 0

		self.SetInsideRender(False)

	def __Initialize(self):
		for item in self.items:
			item.Destroy()
		self.items = []

		self.basePixelPos = 0
		self.maxHeight = 0

	def SetVerticalSpace(self, space):
		self.verticalElementSpace = space

	def ClearItem(self):
		self.__Initialize()

	def AppendItem(self, item):
		item.SetParent(self)
		item.SetSize(self.GetWidth(), item.GetHeight())

		self.items.append(item)

		self.maxHeight += item.GetHeight()

	def GetItemCount(self):
		return len(self.items)

	def LocateItem(self):
		curPxPos = -self.basePixelPos
		height = self.GetHeight()

		for item in self.items:
			item.SetPosition(0, curPxPos)

			if curPxPos >= height or curPxPos + item.GetHeight() <= 0:
				item.Hide()

			else:
				topRemovePixel = max(0, -curPxPos)
				bottomRemovePixel = max(0, (curPxPos + item.GetHeight()) - height)
				item.SetRemovePixel(topRemovePixel, bottomRemovePixel)
				item.Show()

			curPxPos += item.GetHeight() + self.verticalElementSpace

	def GetBasePos(self):
		return self.basePixelPos

	def SetBasePos(self, basePos):
		if self.basePixelPos == int(basePos):
			return

		self.basePixelPos = int(basePos)
		self.LocateItem()

	def GetMaxBasePos(self):
		return max(0, self.GetMaxHeight() - self.GetHeight())

	def GetMaxHeight(self):
		return self.maxHeight + self.verticalElementSpace * max(0, len(self.items) - 1)

class ListBoxExSearch(Window):
	class Item(Window):
		def __init__(self):
			Window.__init__(self)
			self.parent = None
			self.selectedRenderColor = grp.GenerateColor(0.0, 0.0, 0.7, 0.7)

		def __del__(self):
			Window.__del__(self)

		def SetParent(self, parent):
			Window.SetParent(self, parent)
			self.parent=proxy(parent)

		def OnMouseLeftButtonDown(self):
			self.parent.SelectItem(self)

		def IsSelected(self):
			if self.parent != None:
				return self.parent.GetSelectedItem()==self
			return False

		def SetSelectedRenderColor(self, color):
			self.selectedRenderColor = color

		def OnSelect(self):
			pass

		def OnUnselect(self):
			pass

		def OnRender(self):
			if self.IsSelected():
				self.OnSelectedRender()

		def OnSelectedRender(self):
			x, y = self.GetGlobalPosition()
			grp.SetColor(self.selectedRenderColor)
			grp.RenderBar(x, y, self.GetWidth(), self.GetHeight())

	def __init__(self):
		Window.__init__(self)

		self.viewItemCount=10
		self.basePos=0
		self.itemHeight=16
		self.itemStep=20
		self.selItem=0
		self.itemList=[]
		self.onSelectItemEvent = lambda *arg: None

		self.itemWidth=100

		self.scrollBar=None
		self.__UpdateSize()

	def __del__(self):
		Window.__del__(self)

	def __UpdateSize(self):
		height=self.itemStep*self.__GetViewItemCount()

		self.SetSize(self.itemWidth, height)

	def IsEmpty(self):
		if len(self.itemList)==0:
			return 1
		return 0

	def SetItemStep(self, itemStep):
		self.itemStep=itemStep
		self.__UpdateSize()

	def SetItemSize(self, itemWidth, itemHeight):
		self.itemWidth=itemWidth
		self.itemHeight=itemHeight
		self.__UpdateSize()

	def SetViewItemCount(self, viewItemCount):
		self.viewItemCount=viewItemCount
		self.__UpdateSize()

	def SetSelectEvent(self, event):
		self.onSelectItemEvent = event

	def GetBasePos(self):
		return self.basePos

	def SetBasePos(self, basePos):
		for oldItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			oldItem.Hide()

		self.basePos=basePos

		pos=basePos
		for newItem in self.itemList[self.basePos:self.basePos+self.viewItemCount]:
			(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x, y)
			newItem.Show()
			pos+=1

	def GetItemIndex(self, argItem):
		return self.itemList.index(argItem)

	def GetSelectedItem(self):
		return self.selItem

	def SelectIndex(self, index):

		if index >= len(self.itemList) or index < 0:
			self.selItem = None
			return

		oldSelItem = self.selItem

		try:
			self.selItem=self.itemList[index]
		except:
			return

		if oldSelItem:
			oldSelItem.OnUnselect()
		self.selItem.OnSelect()

	def SelectItem(self, selItem):
		if self.selItem == selItem:
			return

		if self.selItem:
			self.selItem.OnUnselect()
		self.selItem=selItem
		selItem.OnSelect()
		self.onSelectItemEvent(selItem)

	def RemoveAllItems(self):
		if self.selItem:
			self.selItem.OnUnselect()

		self.selItem=None
		self.itemList=[]

		if self.scrollBar:
			self.scrollBar.SetPos(0)

	def RemoveItem(self, delItem):
		if delItem==self.selItem:
			delItem.OnUnselect()
			self.selItem=None

		self.itemList.remove(delItem)

	def AppendItem(self, newItem):
		newItem.SetParent(self)
		newItem.SetSize(self.itemWidth, self.itemHeight)

		pos=len(self.itemList)
		if self.__IsInViewRange(pos):
			(x, y)=self.GetItemViewCoord(pos, newItem.GetWidth())
			newItem.SetPosition(x, y)
			newItem.Show()
		else:
			newItem.Hide()

		self.itemList.append(newItem)

	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
		self.scrollBar=scrollBar

	def __OnScroll(self):
		self.SetBasePos(int(self.scrollBar.GetPos()*self.GetScrollLen()))

	def GetScrollLen(self):
		scrollLen=self.__GetItemCount()-self.__GetViewItemCount()
		if scrollLen<0:
			return 0

		return scrollLen

	def __GetViewItemCount(self):
		return self.viewItemCount

	def GetViewItemCount(self):
		return self.__GetViewItemCount()

	def __GetItemCount(self):
		return len(self.itemList)

	def GetItemCount(self):
		return self.__GetItemCount()

	def GetItemViewCoord(self, pos, itemWidth):
		return (0, (pos-self.basePos)*self.itemStep)

	def __IsInViewRange(self, pos):
		if pos<self.basePos:
			return 0
		if pos>=self.basePos+self.viewItemCount:
			return 0
		return 1

class ScrollBarSearch(Window):

	MIDDLE_BAR_POS = 0
	MIDDLE_BAR_UPPER_PLACE = 0
	MIDDLE_BAR_DOWNER_PLACE = 0
	TEMP_SPACE = MIDDLE_BAR_UPPER_PLACE + MIDDLE_BAR_DOWNER_PLACE
	SCROLLBAR_BUTTON_HEIGHT = 0

	class MiddleBar(DragButton):
		def __init__(self):
			DragButton.__init__(self)
			self.AddFlag("movable")

		def MakeImage(self, topImage, middleImage, bottomImage):
			top = ImageBox()
			top.SetParent(self)
			top.LoadImage(topImage)
			top.SetPosition(0, 0)
			top.AddFlag("not_pick")
			top.Show()
			bottom = ImageBox()
			bottom.SetParent(self)
			bottom.LoadImage(bottomImage)
			bottom.AddFlag("not_pick")
			bottom.Show()

			middle = ExpandedImageBox()
			middle.SetParent(self)
			middle.LoadImage(middleImage)
			middle.SetPosition(0, top.GetHeight())
			middle.AddFlag("not_pick")
			middle.Show()

			self.top = top
			self.bottom = bottom
			self.middle = middle

			self.SetHeight(0)

		def GetMinHeight(self):
			return self.top.GetHeight()+self.middle.GetHeight()+self.bottom.GetHeight()

		def SetHeight(self, height):
			minHeight = self.GetMinHeight()
			height = max(minHeight, height)
			DragButton.SetSize(self, self.middle.GetWidth(), height)
			self.bottom.SetPosition(0, height-self.bottom.GetHeight())

			height -= minHeight
			self.middle.SetRenderingRect(0, 0, 0, float(height)/float(self.middle.GetHeight()))

	def __init__(self):
		Window.__init__(self)

		self.pageSize = 1
		self.curPos = 0.0
		self.eventScroll = None
		self.eventArgs = None
		self.lockFlag = FALSE

		self.CreateScrollBar()

		self.scrollStep = 0.20

	def SetUpButton(self, upVisual, overVisual, downVisual):
		self.upButton.SetUpVisual(upVisual)
		self.upButton.SetOverVisual(overVisual)
		self.upButton.SetDownVisual(downVisual)
		self.upButton.Show()
		self.SCROLLBAR_BUTTON_WIDTH = self.upButton.GetWidth()
		self.SCROLLBAR_BUTTON_HEIGHT = self.upButton.GetHeight()# + 3

	def SetDownButton(self, upVisual, overVisual, downVisual):
		self.downButton.SetUpVisual(upVisual)
		self.downButton.SetOverVisual(overVisual)
		self.downButton.SetDownVisual(downVisual)
		self.downButton.Show()

	def SetMiddleImages(self, topImage, middleImage, bottomImage):
		self.middleBar.MakeImage(topImage, middleImage, bottomImage)
		self.SCROLLBAR_MIDDLE_HEIGHT = self.middleBar.GetHeight()

	def SetBarImage(self, img):
		self.barImage.LoadImage(img)
		self.SCROLLBAR_WIDTH = self.barImage.GetWidth()

	def SetBarWidth(self, width):
		self.SCROLLBAR_WIDTH = width

	def CreateScrollBar(self):
		barImage = ExpandedImageBox()
		barImage.SetParent(self)
		barImage.AddFlag("not_pick")
		barImage.Show()

		middleBar = self.MiddleBar()
		middleBar.SetParent(self)
		middleBar.SetMoveEvent(__mem_func__(self.OnMove))
		middleBar.Show()

		upButton = Button()
		upButton.SetParent(self)
		upButton.SetEvent(__mem_func__(self.OnUp))
		upButton.SetWindowHorizontalAlignCenter()
		upButton.Hide()

		downButton = Button()
		downButton.SetParent(self)
		downButton.SetEvent(__mem_func__(self.OnDown))
		downButton.SetWindowHorizontalAlignCenter()
		downButton.Hide()

		self.upButton = upButton
		self.downButton = downButton
		self.middleBar = middleBar
		self.barImage = barImage

	def Destroy(self):
		self.middleBar = None
		self.upButton = None
		self.downButton = None
		self.eventScroll = None
		self.eventArgs = None

	def SetScrollEvent(self, event, *args):
		self.eventScroll = event
		self.eventArgs = args

	def GetPageScale(self):
		return self.SCROLLBAR_MIDDLE_HEIGHT / float(self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2)

	def SetMiddleBarSize(self, pageScale):
		realHeight = self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2
		self.SCROLLBAR_MIDDLE_HEIGHT = max(self.middleBar.GetMinHeight(), int(pageScale * float(realHeight)))
		self.middleBar.SetHeight(self.SCROLLBAR_MIDDLE_HEIGHT)
		self.pageSize = (self.GetHeight() - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)

	def SetScrollBarSize(self, height):
		self.pageSize = (height - self.SCROLLBAR_BUTTON_HEIGHT*2) - self.SCROLLBAR_MIDDLE_HEIGHT - (self.TEMP_SPACE)
		self.SetSize(self.SCROLLBAR_WIDTH, height)
		self.upButton.SetPosition(0, 0)
		self.downButton.SetPosition(0, height - self.SCROLLBAR_BUTTON_HEIGHT)
		self.middleBar.SetRestrictMovementArea(self.MIDDLE_BAR_POS, self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE, self.MIDDLE_BAR_POS+2, height - self.SCROLLBAR_BUTTON_HEIGHT*2 - self.TEMP_SPACE)
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, 0)

		self.UpdateBarImage()
		self.upButton.UpdateRect()
		self.downButton.UpdateRect()

	def SetScrollStep(self, step):
		self.scrollStep = step

	def GetScrollStep(self):
		return self.scrollStep

	def UpdateBarImage(self):
		if self.barImage.GetHeight() > 0:
			self.barImage.SetRenderingRect(0.0, 0.0, 0.0, -1.0 + self.GetHeight() / float(self.barImage.GetHeight()))

	def GetPos(self):
		return self.curPos

	def SetPos(self, pos):
		pos = max(0.0, pos)
		pos = min(1.0, pos)

		newPos = float(self.pageSize) * pos
		self.middleBar.SetPosition(self.MIDDLE_BAR_POS, int(newPos) + self.SCROLLBAR_BUTTON_HEIGHT + self.MIDDLE_BAR_UPPER_PLACE)
		self.OnMove()

	def OnUp(self):
		self.SetPos(self.curPos-self.scrollStep)

	def OnDown(self):
		self.SetPos(self.curPos+self.scrollStep)

	def OnMove(self):

		if self.lockFlag:
			return

		if 0 == self.pageSize:
			return

		(xLocal, yLocal) = self.middleBar.GetLocalPosition()
		self.curPos = float(yLocal - self.SCROLLBAR_BUTTON_HEIGHT - self.MIDDLE_BAR_UPPER_PLACE) / float(self.pageSize)

		if self.eventScroll:
			apply(self.eventScroll, self.eventArgs)

	def OnMouseLeftButtonDown(self):
		(xMouseLocalPosition, yMouseLocalPosition) = self.GetMouseLocalPosition()
		pickedPos = yMouseLocalPosition - self.SCROLLBAR_BUTTON_HEIGHT - self.SCROLLBAR_MIDDLE_HEIGHT/2
		newPos = float(pickedPos) / float(self.pageSize)
		self.SetPos(newPos)

	def LockScroll(self):
		self.lockFlag = TRUE

	def UnlockScroll(self):
		self.lockFlag = FALSE

	## ScrollBar Wheel Support
	def OnWheelMove(self, iLen):
		pos = self.GetPos()

		## Computing mouse move range (by percent)
		iLen = (float(abs(iLen)-100)/100.0)*(iLen/abs(iLen))

		## Mouse Inversion
		iLen *= -1

		pos += iLen
		self.SetPos(pos)
		return True

class UnfoldListBox2(Window):

	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.width = 0
		self.height = 0
		self.basePos = 0
		self.xDif = 0
		self.yDif = 0
		self.showObjCount = 0
		self.showLineCount = 0
		self.fullLineCount = 0
		self.scrollPos = 0
		self.objList = []

		self.scrollBar = NewScrollBar()
		self.scrollBar.SetParent(self)
		self.scrollBar.SetScrollEvent(self.OnScroll)
		self.scrollBar.Hide()

	def __del__(self):
		Window.__del__(self)

	def OnScroll(self):
		import math
		if self.fullLineCount <= 0 or self.showLineCount == self.fullLineCount:
			self.scrollPos = 0
			self.SetBasePos(0)
			return
		pos = self.scrollBar.GetPos()
		itempos = math.floor(float(pos) / float(float(1) / float(self.fullLineCount - self.showLineCount)) + 0.001)
		if itempos != self.scrollPos:
			self.scrollPos = itempos
			self.SetBasePos(itempos)

	def SetWidth(self, width):
		self.SetSize(width, self.height)

	def SetSize(self, width, height):
		Window.SetSize(self, width, height)
		self.width = width
		self.height = height
		self.scrollBar.SetScrollBarSize(self.height - 4)
		self.scrollBar.SetPosition(self.width - self.scrollBar.GetWidth(), 0)

	def SetXDif(self, xDif):
		self.xDif = xDif
		self.LocateItem()

	def SetYDif(self, yDif):
		self.yDif = yDif
		self.LocateItem()

	def SetBasePos(self, pos):
		self.basePos = pos
		self.LocateItem(False)

	def ClearItem(self):
		for obj in self.objList:
			obj.Hide()

		self.objList = []
		self.scrollBar.SetPos(0)

	def InsertItem(self, obj, doLocate = True):
		obj.SetParent(self)
		self.objList.append(obj)

		if doLocate:
			self._LocateItem()

	def LocateItem(self, reloadScrollBar=True):
		self._LocateItem(reloadScrollBar)

	def _LocateItem(self, reloadScrollBar=True):
		import math
		skipCount = self.basePos
		yPos = 0
		xPos = 0
		if reloadScrollBar:
			self.showObjCount = 0
			self.showLineCount = 0
			self.fullLineCount = 0

		if len(self.objList) > 0:
			self.objPerLine = int(float(self.width-self.scrollBar.GetWidth()) / (self.objList[0].GetWidth()+self.xDif))
		
		for obj in self.objList:
			obj.Hide()

			if skipCount > 0:
				xPos += obj.GetWidth()+self.xDif
				if xPos-self.xDif > self.width-self.scrollBar.GetWidth():
					xPos = obj.GetWidth()+self.xDif
					skipCount -= 1
					if skipCount > 0:
						continue
					else:
						xPos = 0
				else:
					continue

			xPos += obj.GetWidth()+self.xDif
			if xPos-self.xDif > self.width-self.scrollBar.GetWidth():
				xPos = obj.GetWidth()+self.xDif
				yPos += obj.GetHeight()+self.yDif

			if reloadScrollBar:
				if xPos-obj.GetWidth()-self.xDif == 0:
					self.fullLineCount += 1
					if yPos+obj.GetHeight() <= self.height:
						self.showLineCount += 1

			obj.SetPosition(xPos-obj.GetWidth()-self.xDif, yPos)

			if yPos+obj.GetHeight() <= self.height:
				self.showObjCount += 1
				obj.Show()

		if reloadScrollBar:
			if self.showObjCount < len(self.objList):
				self.scrollBar.SetMiddleBarSize(float(self.showLineCount)/self.fullLineCount)
				self.scrollBar.Show()
			else:
				self.scrollBar.Hide()

	def ArrangeItem(self):
		self.SetSize(self.width, len(self.objList) * self.stepSize)
		self._LocateItem()

	def GetViewObjectCount(self):
		return self.showObjCount

	def GetObjectCount(self):
		return len(self.objList)

class ExpandedButtonIS(ExpandedImageBox):
	def __init__(self):
		ExpandedImageBox.__init__(self)

		self.images = {"UP": "", "OVER": "", "DOWN": ""}
		self.state = "NORMAL"

		self.xScale = 1.0
		self.yScale = 1.0

		self.eventDict = {}
		self.argsDict = {}

	def __del__(self):
		ExpandedImageBox.__del__(self)

		self.eventDict = {}
		self.argsDict = {}

	def SetScale(self, xScale, yScale):
		self.xScale = float(xScale)
		self.yScale = float(yScale)
		ExpandedImageBox.SetScale(self, xScale, yScale)

	def LoadImage(self, imgPath):
		ExpandedImageBox.LoadImage(self, imgPath)
		ExpandedImageBox.SetScale(self, self.xScale, self.yScale)

	def SetUpVisual(self, filename):
		self.images["UP"] = filename
		if self.state == "NORMAL":
			self.LoadImage(filename)

	def SetOverVisual(self, filename):
		self.images["OVER"] = filename
		if self.state == "OVER":
			self.LoadImage(filename)

	def SetDownVisual(self, filename):
		self.images["DOWN"] = filename
		if self.state == "DOWN":
			self.LoadImage(filename)

	def GetUpVisualFileName(self):
		return self.images["UP"]

	def GetOverVisualFileName(self):
		return self.images["OVER"]

	def GetDownVisualFileName(self):
		return self.images["DOWN"]

	def Enable(self):
		try:
			apply(self.eventDict["ENABLE"], self.argsDict["ENABLE"])
		except KeyError:
			pass
		wndMgr.Enable(self.hWnd)

	def SetEnableEvent(self, func, *args):
		self.eventDict["ENABLE"] = __mem_func__(func)
		self.argsDict["ENABLE"] = args

	def Disable(self):
		try:
			apply(self.eventDict["DISABLE"], self.argsDict["DISABLE"])
		except KeyError:
			pass
		wndMgr.Disable(self.hWnd)

	def SetDisableEvent(self, func, *args):
		self.eventDict["DISABLE"] = __mem_func__(func)
		self.argsDict["DISABLE"] = args

	def OnMouseOverIn(self):
		try:
			apply(self.eventDict["MOUSE_OVER_IN"], self.argsDict["MOUSE_OVER_IN"])
		except KeyError:
			pass
		if self.state == "DOWN":
			return
		self.state = "OVER"
		self.LoadImage(self.images["OVER"])

	def SetMouseOverInEvent(self, func, *args):
		self.eventDict["MOUSE_OVER_IN"] = __mem_func__(func)
		self.argsDict["MOUSE_OVER_IN"] = args

	def OnMouseOverOut(self):
		try:
			apply(self.eventDict["MOUSE_OVER_OUT"], self.argsDict["MOUSE_OVER_OUT"])
		except KeyError:
			pass
		if self.state == "DOWN":
			return
		self.state = "NORMAL"
		self.LoadImage(self.images["UP"])

	def SetMouseOverOutEvent(self, func, *args):
		self.eventDict["MOUSE_OVER_OUT"] = __mem_func__(func)
		self.argsDict["MOUSE_OVER_OUT"] = args

	def OnMouseLeftButtonUp(self):
		self.state = "NORMAL"
		if self.IsIn():
			self.LoadImage(self.images["OVER"])
			snd.PlaySound("sound/ui/click.wav")
			try:
				apply(self.eventDict["MOUSE_CLICK"], self.argsDict["MOUSE_CLICK"])
			except KeyError:
				pass
		else:
			self.LoadImage(self.images["UP"])

	def SAFE_SetEvent(self, func, *args):
		self.eventDict["MOUSE_CLICK"] = __mem_func__(func)
		self.argsDict["MOUSE_CLICK"] = args

	def SetEvent(self, func, *args):
		self.eventDict["MOUSE_CLICK"] = func
		self.argsDict["MOUSE_CLICK"] = args

	def GetEvent(self):
		return self.eventFunc, self.eventArgs

	def OnMouseLeftButtonDown(self):
		self.state = "DOWN"
		self.LoadImage(self.images["DOWN"])

	def SetMouseDoubleClickEvent(self, func, *args):
		self.eventDict["MOUSE_DOUBLE_CLICK"] = __mem_func__(func)
		self.argsDict["MOUSE_DOUBLE_CLICK"] = args

	def OnMouseLeftButtonDoubleClick(self):
		try:
			apply(self.eventDict["MOUSE_DOUBLE_CLICK"], self.argsDict["MOUSE_DOUBLE_CLICK"])
		except KeyError:
			pass

class ColourBox(Box):

	BASE_OPACITY = 40 ## %

	def	__init__(self):
		Box.__init__(self)

		self.boxContent = Bar()
		self.boxContent.SetParent(self)
		self.boxContent.SetPosition(1, 1)
		self.boxContent.Show()

	def	__del__(self):
		Box.__del__(self)

		self.boxContent = None

	def RegisterWindow(self, layer):
		self.hWnd = wndMgr.RegisterBox(self, layer)

	def	SetSize(self, iWidth, iHeight):
		Box.SetSize(self, iWidth, iHeight)

		self.boxContent.SetSize(iWidth-2, iHeight-2)

	def SetColor(self, color, cntColor = None):
		Box.SetColor(self, color)

		## We need to set transparency on boxContent (if user did not provide any opacity)
		## Popping up value from const
		try:
			colorText = hex(color)
			color = int(hex(int(255*self.BASE_OPACITY/100)) + colorText[4:len(colorText)-1], 16)
		except Exception as e:
			print "Invalid color value was provided", e

		self.boxContent.SetColor(color if not cntColor else cntColor)

class ChatFilterCheckBoxLanguage(ImageBox):
	STATE_UNSELECTED = 0
	STATE_SELECTED = 1

	def __init__(self, parent, bLanguage, x, y, event):
		ImageBox.__init__(self)
		self.SetParent(parent)
		self.SetPosition(x, y)
		self.LoadImage("d:/ymir work/ui/public/Parameter_Slot_00.sub")
		self.state = self.STATE_UNSELECTED
		self.event = None

		import uiGuild
		self.mouse = uiGuild.MouseReflector(self)
		self.mouse.SetSize(self.GetWidth(), self.GetHeight())

		image = MakeImageBox(self, "d:/ymir work/ui/public/check_image.sub", 0, 0)
		image.AddFlag("not_pick")
		image.SetWindowHorizontalAlignCenter()
		image.SetWindowVerticalAlignCenter()
		image.Hide()
		self.event = MakeEvent(event)
		self.image, self.bLanguage, self.state = image, bLanguage, 0

		self.Show()
		self.mouse.UpdateRect()

	def GetLanguageIndex(self):
		return self.bLanguage

	def IsChecked(self):
		return self.state == self.STATE_SELECTED

	def __SetState(self, state):
		self.SetState(state)

		if self.event:
			self.event(state)

	def SetState(self, state):
		self.state = state
		if state:
			self.image.Show()
		else:
			self.image.Hide()

	def UnSelect(self):
		self.SetState(self.STATE_UNSELECTED)

	def Select(self):
		self.SetState(self.STATE_SELECTED)

	def OnMouseOverIn(self):
		self.mouse.Show()

	def OnMouseOverOut(self):
		self.mouse.Hide()

	def OnMouseLeftButtonDown(self):
		if self.state == self.STATE_UNSELECTED:
			state = self.STATE_SELECTED
		else:
			state = self.STATE_UNSELECTED
		self.__SetState(state)
		self.mouse.Down()
		return True

	def OnMouseLeftButtonUp(self):
		self.mouse.Up()

class ScrollWindow(Window):
	def __init__(self):
		Window.__init__(self)

		self.SetInsideRender(True)
		self.Show()

		self.scrollBoard = None

	def __del__(self):
		Window.__del__(self)

	def SetContentWindow(self, window):
		from _weakref import proxy
		self.scrollBoard = proxy(window)
		self.scrollBoard.SetParent(self)
		self.scrollBoard.AddFlag("attach")
		self.scrollBoard.AddFlag("not_pick")

		self.SetBoardSize(self.scrollBoard.GetHeight())
		self.RegisterScrollBar()

	def RegisterScrollBar(self):
		self.scrollBar = ModernScrollBar()
		self.scrollBar.SetParent(self)
		self.scrollBar.SetPosition(self.GetLocalPosition()[0] + self.GetWidth() - 10, self.GetLocalPosition()[1])
		# self.scrollBar.SetSize(7, self.GetHeight())
		self.scrollBar.SetWidth(8)
		self.scrollBar.SetScrollBarSize(self.GetHeight())
		self.scrollBar.SetScrollEvent(self.__OnScroll)
		self.scrollBar.Show()

		self.ChangeScrollBar()

	def ChangeScrollBar(self):
		if not self.scrollBar:
			return

		if self.scrollBoard.GetHeight() <= self.GetHeight():
			self.scrollBar.Hide()
		else:
			self.scrollBar.SetContentHeight(self.scrollBoard.GetHeight())
			# self.scrollBar.SetScale(self.GetHeight(), self.scrollBoard.GetHeight())
			# self.scrollBar.SetPosScale((float(1) * abs(self.scrollBoard.GetLocalPosition()[1])) / (self.scrollBoard.GetHeight() - self.GetHeight()))
			self.scrollBar.Show()

	def __OnScroll(self, fScale):
		curr = min(0, max(math.ceil((self.scrollBoard.GetHeight() - self.GetHeight()) * fScale * -1.0), -self.scrollBoard.GetHeight() + self.GetHeight()))
		self.scrollBoard.SetPosition(0, curr)

	def SetBoardSize(self, height):
		self.scrollBoard.SetSize(self.GetWidth(), height)

if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	class DynamicListBox(Window):

		def GetSelectedItemText(self):
			return self.textDict.get(self.selectedLine, "")

		TEMPORARY_PLACE = 3

		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)
			self.overLine = -1
			self.selectedLine = -1
			self.width = 0
			self.height = 0
			self.stepSize = 17
			self.basePos = 0
			self.showLineCount = 0
			self.visibleLineCount = 10
			self.currentPosition = 0
			self.itemCenterAlign = TRUE
			self.itemList = []
			self.keyDict = {}
			self.textDict = {}
			self.event = lambda *arg: None
			
		def __del__(self):
			Window.__del__(self)

		def SetWidth(self, width):
			self.SetSize(width, self.height)

		def SetSize(self, width, height):
			Window.SetSize(self, width, height)
			self.width = width
			self.height = height

		def SetTextCenterAlign(self, flag):
			self.itemCenterAlign = flag

		def SetBasePos(self, pos):
			self.basePos = pos
			self._LocateItem()

		def ClearItem(self):
			self.keyDict = {}
			self.textDict = {}
			self.itemList = []
			self.overLine = -1
			self.selectedLine = -1

		def InsertItem(self, number, text):
			self.keyDict[len(self.itemList)] = number
			self.textDict[len(self.itemList)] = text

			textLine = TextLine()
			textLine.SetParent(self)
			textLine.SetText(text)
			textLine.Hide()

			if self.itemCenterAlign:
				textLine.SetWindowHorizontalAlignCenter()
				textLine.SetHorizontalAlignCenter()

			self.itemList.append(textLine)

			self._LocateItem()

		def ChangeItem(self, number, text):
			for key, value in self.keyDict.items():
				if value == number:
					self.textDict[key] = text

					if number < len(self.itemList):
						self.itemList[key].SetText(text)

					return

		def LocateItem(self):
			self._LocateItem()
			
		def SetVisibleLineCount(self, count):
			self.visibleLineCount = count
			
		def GetVisibleLineCount(self):
			return self.visibleLineCount
			
		def GetVisibleHeight(self):
			return self.visibleLineCount * self.stepSize

		def _LocateItem(self):
			yPos = 0
			self.showLineCount = 0

			i = 0
			for textLine in self.itemList:
				if i >= self.currentPosition and i < (self.currentPosition + self.GetVisibleLineCount()):
					textLine.SetPosition(0, yPos + 3)
					
					textLine.Show()
					yPos += self.stepSize
				else:
					textLine.Hide()

				self.showLineCount += 1
				i += 1

		def ArrangeItem(self):
			self.SetSize(self.width, len(self.itemList) * self.stepSize)
			self._LocateItem()

		def GetViewItemCount(self):
			return int(self.GetHeight() / self.stepSize)

		def GetItemCount(self):
			return len(self.itemList)

		def SetEvent(self, event):
			self.event = event

		def SelectItem(self, line):

			if not self.keyDict.has_key(line):
				return

			if line == self.selectedLine:
				return

			self.selectedLine = line + self.currentPosition
			self.event(self.keyDict.get(self.selectedLine, 0), self.textDict.get(self.selectedLine, "None"))

		def GetSelectedItem(self):
			return self.keyDict.get(self.selectedLine, 0)

		def GetSelectedItemText(self):
			return self.itemList[self.selectedLine].GetText()

		def OnMouseLeftButtonDown(self):
			if self.overLine < 0:
				return

		def OnMouseLeftButtonUp(self):
			if self.overLine >= 0:
				self.SelectItem(self.overLine+self.basePos)
				
		def OnDown(self):
			if self.GetItemCount() > self.GetVisibleLineCount():
				self.currentPosition = min(self.GetItemCount() - self.GetVisibleLineCount(), self.currentPosition + 1)

				self._LocateItem()
			
		def OnUp(self):
			if self.GetItemCount() > self.GetVisibleLineCount():
				self.currentPosition = max(0, self.currentPosition - 1)

				self._LocateItem()
			
		def OnUpdate(self):
			self.overLine = -1

			if self.IsIn():
				x, y = self.GetGlobalPosition()
				height = self.GetHeight()
				xMouse, yMouse = wndMgr.GetMousePosition()

				if yMouse - y < height - 1:
					self.overLine = (yMouse - y) / self.stepSize

					if self.overLine < 0:
						self.overLine = -1
					if self.overLine >= len(self.itemList):
						self.overLine = -1

		def OnRender(self):
			xRender, yRender = self.GetGlobalPosition()
			yRender -= self.TEMPORARY_PLACE
			widthRender = self.width
			heightRender = self.height + self.TEMPORARY_PLACE*2
		
			if -1 != self.overLine:
				grp.SetColor(HALF_WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + self.overLine*self.stepSize + 4, self.width - 3, self.stepSize)				

			if -1 != self.selectedLine:
				if self.selectedLine >= self.currentPosition and self.selectedLine < (self.currentPosition + self.GetVisibleLineCount()):
					if self.selectedLine - self.basePos < self.showLineCount:
						grp.SetColor(grp.GenerateColor(255.0 / 255.0, 150.0 / 255.0, 95.0 / 255.0, 0.2))
						grp.RenderBar(xRender + 2, yRender + (self.selectedLine-self.basePos-self.currentPosition) * self.stepSize + 4, self.width - 3, self.stepSize)

			max_count = min(self.GetVisibleLineCount(), self.GetItemCount())
			for i in range(1, max_count):
				grp.SetColor(WHITE_COLOR)
				grp.RenderBar(xRender, yRender + i*self.stepSize + 4, self.width, 1)		

	class DynamicComboBoxImage(Window):
		class ListBoxWithBoard(DynamicListBox):

			BG_COLOR = grp.GenerateColor(33.0 / 255.0, 33.0 / 255.0, 33.0 / 255.0, 1.0)

			def __init__(self, layer):
				DynamicListBox.__init__(self, layer)

			def OnRender(self):
				xRender, yRender = self.GetGlobalPosition()
				yRender -= self.TEMPORARY_PLACE
				widthRender = self.width
				heightRender = self.height + self.TEMPORARY_PLACE*2
				grp.SetColor(BACKGROUND_COLOR)
				grp.RenderBar(xRender, yRender, widthRender, heightRender)
				grp.SetColor(WHITE_COLOR)
				grp.RenderBox(xRender, yRender, widthRender, heightRender)
				# grp.SetColor(DARK_COLOR)
				# grp.RenderLine(xRender, yRender, widthRender, 0)
				# grp.RenderLine(xRender, yRender, 0, heightRender)
				DynamicListBox.OnRender(self)

		def __init__(self, parent, name, x, y):
			self.isSelected = False
			self.isOver = False
			self.isListOpened = False
			self.event = lambda *arg: None
			self.enable = True
			self.imagebox = None
			self.listBox = None
			self.titleText = None

			Window.__init__(self)
			
			## ImageBox
			image = ExpandedImageBox()
			image.SetParent(parent)
			image.LoadImage(name)
			image.SetPosition(x, y)
			image.Hide()
			self.imagebox = image
			
			## BaseSetting
			self.x = x + 1
			self.y = y + 1
			self.width = self.imagebox.GetWidth() - 3
			self.height = self.imagebox.GetHeight() - 3
			self.SetParent(parent)

			## TextLine
			self.textLine = MakeTextLine(self)
			self.textLine.SetText(localeInfo.UI_ITEM)
			
			## ListBox
			self.listBox = self.ListBoxWithBoard("TOP_MOST")
			self.listBox.SetPickAlways()
			self.listBox.SetParent(self)
			self.listBox.SetVisibleLineCount(12)
			self.listBox.SetEvent(__mem_func__(self.OnSelectItem))
			self.listBox.Hide()
			
			Window.SetPosition(self, self.x, self.y)
			Window.SetSize(self, self.width, self.height)
			self.textLine.UpdateRect()
			self.listBox.SetPosition(0, self.height + 5)
			self.__ArrangeListBox()
			
		def __del__(self):
			Window.__del__(self)

		def Hide(self):
			Window.Hide(self)
			
			if self.listBox:
				self.CloseListBox()

			if self.imagebox:
				self.imagebox.Hide()

		def Show(self):
			Window.Show(self)

			if self.imagebox:
				self.imagebox.Show()

		def Destroy(self):
			self.textLine = None
			self.listBox = None
			self.imagebox = None

		def Clear(self):
			self.SelectItem(0)

		def SetPosition(self, x, y):
			Window.SetPosition(self, x, y)
			self.imagebox.SetPosition(x, y)
			self.x = x
			self.y = y
			self.__ArrangeListBox()

		def SetSize(self, width, height):
			Window.SetSize(self, width, height)
			self.width = width
			self.height = height
			self.textLine.UpdateRect()
			self.__ArrangeListBox()
			
		def SetImageScale(self, scale_x, scale_y):
			self.imagebox.SetScale(scale_x, scale_y)
			self.width = self.imagebox.GetWidth() - 3
			self.height = self.imagebox.GetHeight() - 3
			Window.SetSize(self, self.width, self.height)
			self.textLine.UpdateRect()
			self.__ArrangeListBox()
			
		def __ArrangeListBox(self):
			self.listBox.SetPosition(0, self.height + 5)

			if self.listBox.GetItemCount() <= self.listBox.GetVisibleLineCount():
				self.listBox.SetSize(self.width, self.listBox.GetHeight())
			else:
				self.listBox.SetSize(self.width, self.listBox.GetVisibleHeight())

		def Enable(self):
			self.enable = True

		def Disable(self):
			self.enable = False
			self.CloseListBox()

		def SetEvent(self, event):
			self.event = event

		def SetDefaultTitle(self, title):
			self.titleText = title

			self.SetCurrentItem(self.titleText)

		def UseDefaultTitle(self):
			self.SetCurrentItem(self.titleText)
			
		def SetTitle(self, title):
			self.SetCurrentItem(title)

		def GetTitle(self):
			return self.titleText

		def ClearItem(self):
			self.CloseListBox()
			self.listBox.ClearItem()

		def InsertItem(self, index, name):
			self.listBox.InsertItem(index, name)
			self.listBox.ArrangeItem()

		def SetCurrentItem(self, text):
			self.textLine.SetText(text)

		def GetSelectedItemText(self):
			return self.listBox.GetSelectedItemText()

		def SelectItem(self, key):
			self.listBox.SelectItem(key)

		def OnSelectItem(self, index, name):
			self.CloseListBox()
			self.event(index)

		def CloseListBox(self):
			self.isListOpened = False
			self.listBox.Hide()

		def OnMouseLeftButtonDown(self):
			if not self.enable:
				return

			self.isSelected = True

		def OnMouseLeftButtonUp(self):
			if not self.enable:
				return
			
			self.isSelected = False
			
			if self.isListOpened:
				self.CloseListBox()
			else:
				if self.listBox.GetItemCount() > 0:
					self.isListOpened = True
					self.listBox.Show()
					self.listBox.SetTop()
					self.__ArrangeListBox()
					
		def OnMouseWheel(self, nLen):
			if nLen > 0:
				self.listBox.OnUp()
				return True
				
			elif nLen < 0:
				self.listBox.OnDown()
				return True
				
			return False

		def OnUpdate(self):
			if not self.enable:
				return

			if self.IsIn():
				self.isOver = True
			else:
				self.isOver = False

		def OnRender(self):
			self.x, self.y = self.GetGlobalPosition()
			xRender = self.x
			yRender = self.y
			widthRender = self.width
			heightRender = self.height
			
			if self.isOver:
				grp.SetColor(HALF_WHITE_COLOR)
				grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)
				
				if self.isSelected:
					grp.SetColor(WHITE_COLOR)
					grp.RenderBar(xRender + 2, yRender + 3, self.width - 3, heightRender - 5)
					
	class ShopDecoThinboard(Window):
		DEFAULT_VALUE = 16
		CORNER_WIDTH = 48
		CORNER_HEIGHT = 32
		LINE_WIDTH = 16
		LINE_HEIGHT = 32
		
		DEFAULT_CORNER_WIDTH = 16
		DEFAULT_CORNER_HEIGHT = 16
		DEFAULT_LINE_WIDTH = 16
		DEFAULT_LINE_HEIGHT = 16
		DEFAULT_BOARD_COLOR = grp.GenerateColor(0.0, 0.0, 0.0, 0.51)

		LT = 0
		LB = 1
		RT = 2
		RB = 3
		L = 0
		R = 1
		T = 2
		B = 3

		def __init__(self, type = 0, layer = "UI"):
			Window.__init__(self, layer)
			
			self.type = type
			
			base = Bar()
			base.SetParent(self)
			base.AddFlag("attach")
			base.AddFlag("not_pick")
			base.SetPosition(self.DEFAULT_CORNER_WIDTH, self.DEFAULT_CORNER_HEIGHT)
			base.SetColor(self.DEFAULT_BOARD_COLOR)
			base.Hide()
			self.base = base
		
			self.width = 190
			self.height = 32
			
			self.SetStyle(type)
			self.Refresh()
				
		def __del__(self):
			Window.__del__(self)
			
		def GetStyle(self, type):
			import privateShop

			(name, path, text_color) = privateShop.GetTitleDeco(type)
			
			CornerFileNames = [ path + "_"+dir+".tga" for dir in ["left_top","left_bottom","right_top","right_bottom"] ]
			LineFileNames = [ path + "_"+dir+".tga" for dir in ["left","right","top","bottom"] ]
			
			return CornerFileNames, LineFileNames
			
		def SetStyle(self, type):
			self.type = type
			
			CornerFileNames, LineFileNames = self.GetStyle(type)
			
			if CornerFileNames == None or LineFileNames == None :
				return

			self.Corners = []
			for fileName in CornerFileNames:
				Corner = ExpandedImageBox()
				Corner.AddFlag("attach")
				Corner.AddFlag("not_pick")
				Corner.LoadImage(fileName)
				Corner.SetParent(self)
				Corner.SetPosition(0, 0)
				Corner.Show()
				self.Corners.append(Corner)

			self.Lines = []
			for fileName in LineFileNames:
				Line = ExpandedImageBox()
				Line.AddFlag("attach")
				Line.AddFlag("not_pick")
				Line.LoadImage(fileName)
				Line.SetParent(self)
				Line.SetPosition(0, 0)
				Line.Show()
				self.Lines.append(Line)
				
			if self.type == 0:
				self.base.Show()
			else:
				self.base.Hide()
				
			self.Refresh()

		def SetBoardSize(self, width, height):
			if self.type == 0:
				self.width = max(self.DEFAULT_CORNER_WIDTH*2, width)
				self.height = max(self.DEFAULT_CORNER_HEIGHT*2, height)
				
			else:
				self.width = max(self.DEFAULT_VALUE*2, width)
				self.height = max(self.DEFAULT_VALUE*2, height)
				
			Window.SetSize(self, self.width, self.height)
			self.Refresh()

		def Refresh(self):
			if self.type == 0:
		
				self.Corners[self.LB].SetPosition(0, self.height - self.DEFAULT_CORNER_HEIGHT)
				self.Corners[self.RT].SetPosition(self.width - self.DEFAULT_CORNER_WIDTH, 0)
				self.Corners[self.RB].SetPosition(self.width - self.DEFAULT_CORNER_WIDTH, self.height - self.DEFAULT_CORNER_HEIGHT)
				
				self.Lines[self.L].SetPosition(0, self.DEFAULT_CORNER_HEIGHT)
				self.Lines[self.T].SetPosition(self.DEFAULT_CORNER_WIDTH, 0)
				self.Lines[self.R].SetPosition(self.width - self.DEFAULT_CORNER_WIDTH, self.DEFAULT_CORNER_HEIGHT)
				self.Lines[self.B].SetPosition(self.DEFAULT_CORNER_HEIGHT, self.height - self.DEFAULT_CORNER_HEIGHT)

				verticalShowingPercentage = float((self.height - self.DEFAULT_CORNER_HEIGHT*2) - self.DEFAULT_LINE_HEIGHT) / self.DEFAULT_LINE_HEIGHT
				horizontalShowingPercentage = float((self.width - self.DEFAULT_CORNER_WIDTH*2) - self.DEFAULT_LINE_WIDTH) / self.DEFAULT_LINE_WIDTH
				
				self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
				self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
				self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
				self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
				self.base.SetSize(self.width - self.DEFAULT_CORNER_WIDTH*2, self.height - self.DEFAULT_CORNER_HEIGHT*2)
				self.base.Show()
		
			else:
				self.Corners[self.LT].SetPosition(-self.CORNER_WIDTH + self.DEFAULT_VALUE, -self.CORNER_HEIGHT + self.DEFAULT_VALUE)
				self.Corners[self.LB].SetPosition(-self.CORNER_WIDTH + self.DEFAULT_VALUE, self.height - self.CORNER_HEIGHT + self.DEFAULT_VALUE)
				
				self.Corners[self.RT].SetPosition(self.width - self.DEFAULT_VALUE, -self.CORNER_HEIGHT + self.DEFAULT_VALUE)
				self.Corners[self.RB].SetPosition(self.width - self.DEFAULT_VALUE, self.height - self.CORNER_HEIGHT + self.DEFAULT_VALUE)
				
				self.Lines[self.L].SetPosition(0, self.DEFAULT_VALUE)
				self.Lines[self.R].SetPosition(self.width - self.DEFAULT_VALUE, self.DEFAULT_VALUE)
				self.Lines[self.B].SetPosition(self.DEFAULT_VALUE, self.height - self.LINE_HEIGHT + self.DEFAULT_VALUE)
				self.Lines[self.T].SetPosition(self.DEFAULT_VALUE, -self.LINE_HEIGHT + self.DEFAULT_VALUE)
				
				verticalShowingPercentage = float((self.height - self.DEFAULT_VALUE*2) - self.DEFAULT_VALUE) / self.DEFAULT_VALUE
				horizontalShowingPercentage = float((self.width - self.DEFAULT_VALUE*2) - self.DEFAULT_VALUE) / self.DEFAULT_VALUE
				
				self.Lines[self.L].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
				self.Lines[self.R].SetRenderingRect(0, 0, 0, verticalShowingPercentage)
				self.Lines[self.T].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
				self.Lines[self.B].SetRenderingRect(0, 0, horizontalShowingPercentage, 0)
				self.base.Hide()

		def ShowInternal(self):
			for wnd in self.Lines:
				wnd.Show()
			for wnd in self.Corners:
				wnd.Show()

		def HideInternal(self):
			for wnd in self.Lines:
				wnd.Hide()
			for wnd in self.Corners:
				wnd.Hide()

class GridListBox(Window):
	def __init__(self, layer = "UI"):
		super(GridListBox, self).__init__(layer)

	def Initialize(self, itemSize, itemStep, itemCount):
		self.itemList = []
		self.itemlistOriginal = []
		self.itemSize = itemSize
		self.itemStep = itemStep
		self.itemCount = itemCount
		self.scrollBar = None
		self.scrollLen = 0.0
		self.absoluteSize = (0, 0)
		self.absolutePos = dict()

		self.__ComputeSize()
		self.__ComputeItemPos()

	def __del__(self):
		super(GridListBox, self).__del__()
		self.itemList = []
		self.itemlistOriginal = []
		self.itemSize = 0
		self.itemStep = 0
		self.itemCount = 0
		self.scrollBar = None
		self.scrollLen = 0.0
		self.absoluteSize = (0, 0)
		self.absolutePos = dict()

	def AppendItem(self, newItem):
		newItem.SetParent(self)
		newItem.SetSize(*self.itemSize)
		newItem.SetPosition((len(self.itemList) % self.itemCount[0]) * self.itemStep[0], (len(self.itemList) / self.itemCount[0]) * self.itemStep[1])
		newItem.Hide()

		## Save absolute position (quite useful for clipping computation)
		self.absolutePos[newItem] = newItem.GetLocalPosition()
		self.itemList.append(newItem)

		## Compute current pos
		self.__ComputeSize()
		self.__ComputeItemPos()

	def RemoveItem(self, rToRmv):
		for iPos, rItem in enumerate(self.itemList):
			if rItem == rToRmv:
				del self.itemList[iPos]

		self.__ComputeSize()
		self.__ComputeItemPos()

	def RemoveIndex(self, iPos):
		if iPos >= len(self.itemList) or iPos < 0:
			print "Invalid index to remove!", iPos
			return

		del self.itemList[iPos]

		self.__ComputeSize()
		self.__ComputeItemPos()

	def RemoveAllItems(self):
		for rItem in self.itemList:
			rItem.Hide()
			del rItem

		self.itemList = []
		self.scrollLen = 0.0

		## Refresh the ui
		self.__ComputeSize()
		self.__ComputeItemPos()

	def __OnScroll(self):
		## iLen -> Scroll Position
		self.scrollLen = self.scrollBar.GetPos()
		## Update elements size
		self.__ComputeItemPos()

	def SetScrollBar(self, scrollBar):
		scrollBar.SetScrollEvent(__mem_func__(self.__OnScroll))
		self.scrollBar=scrollBar

	def __ComputeSize(self):
		if len(self.itemList) == 0:
			self.absoluteSize = (0, 0)
			self.SetSize(0, 0)
			return

		windowWidth, windowHeight = min(len(self.itemList), self.itemCount[0]) * self.itemStep[0] - (self.itemStep[0] - self.itemSize[0]), self.itemList[-1].GetLocalPosition()[1] + self.itemSize[1]
		## Compute the absolute size in order to keep the clipping
		self.absoluteSize = (windowWidth, windowHeight)
		self.SetSize(self.itemCount[0] * self.itemStep[0] - (self.itemStep[0] - self.itemSize[0]), self.itemCount[1] * self.itemStep[1] - (self.itemStep[1] - self.itemSize[1]))

	def __ComputeItemPos(self):
		if self.absoluteSize[0] < self.GetWidth() or self.absoluteSize[1] < self.GetHeight():
			## Nothing to scroll, set to default positions
			for rItem in self.itemList:
				rItem.SetPosition(*self.absolutePos[rItem])
				rItem.Show()

			return

		## Calculate real tick based on max distance that can be scrolled
		## TODO: Implement horizontal scrolling if needed
		scrollLen = ((self.absoluteSize[1] - self.GetHeight()) * self.scrollLen / self.absoluteSize[1]) if self.absoluteSize[1] > 0 else 0.0
		windowViewStart, windowViewEnd = min(self.absoluteSize[1] * scrollLen, self.absoluteSize[1] - self.GetHeight()), min(self.absoluteSize[1] * scrollLen + self.GetHeight(), self.absoluteSize[1])

		## Move items to match visibility area
		for rItem in self.itemList:
			if self.__IsWithinArea(rItem, {"l_x" : 0, "r_x" : self.GetWidth(), "l_y" : windowViewStart, "r_y" : windowViewEnd}):
				## Set relative position and make the item visible
				## TODO: Add horizontal scrolling if needed
				rItem.SetPosition(self.absolutePos[rItem][0], self.absolutePos[rItem][1] - windowViewStart)
				## Try to clip if supported
				try:
					rItem.SetClippingMaskWindow(self)
				except:
					pass
				rItem.Show()
			else:
				## Hide items out of the range
				rItem.Hide()

	def __IsWithinArea(self, rItem, dArea):
		(itemLX, itemLY, itemRX, itemRY) = (self.absolutePos[rItem][0], self.absolutePos[rItem][1], self.absolutePos[rItem][0] + rItem.GetWidth(), self.absolutePos[rItem][1] + rItem.GetHeight())
		if (itemLX == dArea["l_x"] or itemLY == dArea["l_y"]) and (itemRX == dArea["r_x"] or itemRY == dArea["r_y"]):
			return True

		if itemLX > dArea["r_x"] or dArea["l_x"] > itemRX:
			return False

		if dArea["l_y"] > itemRY or itemLY > dArea["r_y"]:
			return False

		return True

	def ApplyFilter(self, lFilter):
		## If not filter apply, restore original
		if not lFilter:
			self.itemList = list(self.itemlistOriginal)
			self.itemlistOriginal = []
		else:
			## Copy original content
			if len(self.itemlistOriginal) == 0:
				self.itemlistOriginal = list(self.itemList)

			## Clear listbox
			map(lambda rItem : rItem.Hide(), self.itemList)
			self.RemoveAllItems()

			## Filter content
			for sElement in list(filter(lFilter, self.itemlistOriginal)):
				self.AppendItem(sElement)
				
###################################################################################################
## Python Script Loader
###################################################################################################

class ScriptWindow(Window):
	def __init__(self, layer = "UI"):
		Window.__init__(self, layer)
		self.Children = []
		self.ElementDictionary = {}
		self.TypeDict = {}

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		Window.Destroy(self)
		self.ClearDictionary()

	def Show(self):
		Window.Show(self)

		for children in self.GetChildrenByType("titlebar"):
			children.SetTop()

	def ClearDictionary(self):
		self.Children = []
		self.ElementDictionary = {}
		self.TypeDict = {}

	def InsertChild(self, name, child, Type):
		self.ElementDictionary[name] = child
		if Type in self.TypeDict:
			self.TypeDict[Type].append(child)
		else:
			self.TypeDict[Type] = [child]

	def IsChild(self, name):
		return self.ElementDictionary.has_key(name)

	def GetChild(self, name):
		return self.ElementDictionary[name]

	def GetChildrenByType(self, Type):
		return self.TypeDict.get(Type, [])

	def GetChild2(self, name):
		return self.ElementDictionary.get(name, None)

	def GetChildDictionary(self, *args):
		"""
		:param args: Is used to send a non-keyworded variable length argument list to the function.
		:how-to-call-ex:
			* I. childrenDict = self.GetChildDictionary('a1')
				# childrenDict['a1'].SetScale(scale)
			* II. childrenDict = self.GetChildDictionary('b1', 'b2')
				# childrenDict['b1'].SetSize(w, h)
				# childrenDict['b2'].SetPosition(x, y)
			* III. 
				for value in self.GetChildDictionary('c1', 'c2', 'c3', 'c4').values():
					value.SetSize(w, h)
			* IV. 
				def OnToggleDown(self, index):
					print 'OnToggleDown {:d}'.format(index)
				for key, value in enumerate(self.GetChildDictionary('d1', 'd2').values()):
					value.SAFE_SetEvent(self.OnToggleDown, key)
		"""
		if isinstance(args, tuple):
			return {children : self.ElementDictionary.get(children, None) for children in args}

		return dict()

	def SAFE_SetDictionaryEvent(self, childrenDict, eventNameFuncs):
		"""
		:param childrenDict: A dictionary with objects.
		:param eventNameFuncs: A list of events name as function which will be executed for each object.
		:how-to-call-ex:
			* I. 	self.SAFE_SetDictionaryEvent(self.GetChildDictionary('a1', 'a2', 'a3'), ['Show', 'SetCenterPosition'])
			* II. 	self.SAFE_SetDictionaryEvent(self.GetChildDictionary('b1'), ('Hide'))
			* III. 	self.SAFE_SetDictionaryEvent(self.GetChildDictionary('c1'), ('SetWindowVerticalAlignCenter', 'SetTop', 'SetFocus', 'Lock'))
		"""
		def Abort(*args):
			import dbg, exception
			dbg.TraceError("\n".join(args))
			exception.Abort('SAFE_SetDictionaryEvent')
	
		if isinstance(eventNameFuncs, str):
			eventNameFuncs = tuple(eventNameFuncs.split())

		allowedWindowEventsTuple = \
		(
			'SetWindowHorizontalAlignLeft',     'SetWindowHorizontalAlignCenter',
			'SetWindowHorizontalAlignRight',    'SetWindowVerticalAlignTop',
			'SetWindowVerticalAlignCenter',     'SetWindowVerticalAlignBottom',
			'SetPickAlways',                    'SetTop',
			'SetCenterPosition',                'SetFocus',
			'UpdateRect',                       'KillFocus',
			'Show',                             'Hide',
			'Lock',                             'Unlock'
		)

		if not isinstance(childrenDict, dict):
			Abort('Wrong type of argument childrenDict({:s}), must be as dictionary.'.format(type(childrenDict).__name__))

		if not isinstance(eventNameFuncs, (tuple, list)):
			Abort('Wrong type of argument eventNameFuncs({:s}), must be as list or tuple.'.format(type(eventNameFuncs).__name__))
			
		unallowedWindowEvents = (', '.join(event for event in eventNameFuncs if event not in allowedWindowEventsTuple))
		if unallowedWindowEvents:
			Abort('Unallowed eventNameFuncs ({:s}).'.format(unallowedWindowEvents))

		for key, value in childrenDict.iteritems():
			for event in eventNameFuncs:
				try:
					# Smth: eval('childrenDict.get("{:s}").{:s}()'.format(key, event))
					######################################################################
					# Return the value of the named attribute of object. name must be a string.
					# If the string is the name of one of the object�s attributes, the result is the value of that attribute. 
					# For example, getattr(x, 'foobar') is equivalent to x.foobar. 
					# If the named attribute does not exist, default is returned if provided, otherwise AttributeError is raised.
					getattr(value, event)()

				except AttributeError:
					Abort("Can't get attribute.")

	def LoadScript(self, window, filename):
		try:
			PythonScriptLoader().LoadScriptFile(window, filename)
			return True
		except Exception as e:
			dbg.TraceError("Failed to load uiscript file: {}".format(filename))
			dbg.TraceError(str(e))
			return False


class PythonScriptLoader(object):

	BODY_KEY_LIST = ( "x", "y", "width", "height" )

	#####

	DEFAULT_KEY_LIST = ( "type", "x", "y", )
	WINDOW_KEY_LIST = ( "width", "height", )
	IMAGE_KEY_LIST = ( "image", )
	EXPANDED_IMAGE_KEY_LIST = ( "image", )
	ANI_IMAGE_KEY_LIST = ( "images", )
	SLOT_KEY_LIST = ( "width", "height", "slot", )
	CANDIDATE_LIST_KEY_LIST = ( "item_step", "item_xsize", "item_ysize", )
	GRID_TABLE_KEY_LIST = ( "start_index", "x_count", "y_count", "x_step", "y_step", )
	EDIT_LINE_KEY_LIST = ( "width", "height", "input_limit", )
	COMBO_BOX_KEY_LIST = ( "width", "height", "item", )
	TITLE_BAR_KEY_LIST = ( "width", )
	HORIZONTAL_BAR_KEY_LIST = ( "width", )
	BOARD_KEY_LIST = ( "width", "height", )
	BOARD_WITH_TITLEBAR_KEY_LIST = ( "width", "height", "title", )
	BOX_KEY_LIST = ( "width", "height", )
	BAR_KEY_LIST = ( "width", "height", )
	LINE_KEY_LIST = ( "width", "height", )
	SLOTBAR_KEY_LIST = ( "width", "height", )
	GAUGE_KEY_LIST = ( "width", "color", )
	SCROLLBAR_KEY_LIST = ( "size", )
	LIST_BOX_KEY_LIST = ( "width", "height", )
	TABLE_KEY_LIST = ( "width", )
	INPUT_FIELD_KEY_LIST = ("width", "height", )
	MODERN_SCROLLBAR_KEY_LIST = ("size",)
	GRID_LIST_BOX_KEY_LIST = ("itemsize", "itemstep", "viewcount")

	# if app.ENABLE_RENDER_TARGET_EXTENSION:
	# 	RENDER_TARGET_KEY_LIST = ( "index", )

	if app.ENABLE_QUEST_RENEWAL:
		SUB_TITLE_BAR_KEY_LIST = ( "width", )
		LIST_BAR_KEY_LIST = ( "width", )

	SCROLLBAR_TEMPLATE_KEY_LIST = SCROLLBAR_KEY_LIST + ( "middle_image", )
	SHORTCUT_KEY_LIST = ("shortcut",)

	SCROLLBAR_SEARCH_KEY_LIST = SCROLLBAR_KEY_LIST + ( "middle_image_top", "middle_image_center", "middle_image_bottom", )

	def __init__(self):
		self.Clear()

	def Clear(self):
		self.ScriptDictionary = { "SCREEN_WIDTH" : wndMgr.GetScreenWidth(), "SCREEN_HEIGHT" : wndMgr.GetScreenHeight() }
		self.InsertFunction = 0

	def LoadScriptFile(self, window, FileName):
		import exception
		import exceptions
		import os
		import errno
		self.Clear()

		print "===== Load Script File : %s" % (FileName)

		import sys
		from utils import Sandbox
		sandbox = Sandbox(True, ["uiScriptLocale", "localeInfo", "sys", "item", "app", "player","utils", "grp", "ui", "introInterface", "marblemgr"]) #@ikd - added 'utils' to import it in scriptfile (to use GetElementDictByName)

		import chr
		import player
		import app
		self.ScriptDictionary["PLAYER_NAME_MAX_LEN"] = chr.PLAYER_NAME_MAX_LEN
		self.ScriptDictionary["DRAGON_SOUL_EQUIPMENT_SLOT_START"] = player.DRAGON_SOUL_EQUIPMENT_SLOT_START
		self.ScriptDictionary["LOCALE_PATH"] = app.GetLocalePath()

		if __USE_EXTRA_CYTHON__:
			# sub functions
			from os.path import splitext as op_splitext, basename as op_basename, dirname as op_dirname
			def GetModName(filename):
				return op_splitext(op_basename(filename))[0]
			def IsInUiPath(filename):
				def ICmp(s1, s2):
					return s1.lower() == s2.lower()
				return ICmp(op_dirname(filename), "uiscript")
			# module name to import
			modname = GetModName(FileName)
			# lazy loading of uiscriptlib
			import uiscriptlib
			# copy scriptdictionary stuff to builtin scope (otherwise, import will fail)
			tpl2Main = (
				"SCREEN_WIDTH","SCREEN_HEIGHT",
				"PLAYER_NAME_MAX_LEN", "DRAGON_SOUL_EQUIPMENT_SLOT_START","LOCALE_PATH"
			)
			import __builtin__ as bt
			for idx in tpl2Main:
				tmpVal = self.ScriptDictionary[idx]
				exec "bt.%s = tmpVal"%idx in globals(), locals()
			# debug stuff
			# import dbg
			# dbg.TraceError("Loading %s (%s %s)"%(FileName, GetModName(FileName), IsInUiPath(FileName)))
		try:
			if __USE_EXTRA_CYTHON__ and IsInUiPath(FileName) and uiscriptlib.isExist(modname):
				m1 = uiscriptlib.moduleImport(modname)
				self.ScriptDictionary["window"] = m1.window.copy()
				del m1
			else:
				sandbox.execfile(FileName, self.ScriptDictionary)
		except IOError, err:
			import sys
			import dbg
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			dbg.TraceError("error  : %s" % (err))
			exception.Abort("LoadScriptFile1")
		except RuntimeError,err:
			import sys
			import dbg
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			dbg.TraceError("error  : %s" % (err))
			exception.Abort("LoadScriptFile2")
		except:
			import sys
			import dbg
			dbg.TraceError("Failed to load script file : %s" % (FileName))
			exception.Abort("LoadScriptFile!!!!!!!!!!!!!!")

		#####

		Body = self.ScriptDictionary["window"]
		self.CheckKeyList("window", Body, self.BODY_KEY_LIST)

		window.ClearDictionary()
		self.InsertFunction = window.InsertChild

		window.SetPosition(int(Body["x"]), int(Body["y"]))

		window.SetSize(int(Body["width"]), int(Body["height"]))
		if True == Body.has_key("style"):
			for StyleList in Body["style"]:
				window.AddFlag(StyleList)


		self.LoadChildren(window, Body)

	def LoadChildren(self, parent, dicChildren):
		if True == dicChildren.has_key("style"):
			for style in dicChildren["style"]:
				parent.AddFlag(style)

		if False == dicChildren.has_key("children"):
			return False

		Index = 0

		ChildrenList = dicChildren["children"]
		parent.Children = range(len(ChildrenList))
		for ElementValue in ChildrenList:
			try:
				Name = ElementValue["name"]
			except KeyError:
				Name = ElementValue["name"] = "NONAME"

			try:
				Type = ElementValue["type"]
			except KeyError:
				Type = ElementValue["type"] = "window"

			if False == self.CheckKeyList(Name, ElementValue, self.DEFAULT_KEY_LIST):
				del parent.Children[Index]
				continue

			if Type == "window":
				parent.Children[Index] = ScriptWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementWindow(parent.Children[Index], ElementValue, parent)

			elif Type == "scroll_window":
				parent.Children[Index] = ScrollWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementWindow(parent.Children[Index], ElementValue, parent)

			elif Type == "button":
				parent.Children[Index] = Button()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "radio_button":
				parent.Children[Index] = RadioButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "toggle_button":
				parent.Children[Index] = ToggleButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementButton(parent.Children[Index], ElementValue, parent)

			elif Type == "mark":
				parent.Children[Index] = MarkBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementMark(parent.Children[Index], ElementValue, parent)

			elif Type == "image":
				parent.Children[Index] = ImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementImage(parent.Children[Index], ElementValue, parent)

			elif Type == "image_new":
				parent.Children[Index] = ImageBoxNew()
				parent.Children[Index].SetParent(parent)
				self.LoadElementImage(parent.Children[Index], ElementValue, parent)

			elif Type == "expanded_image":
				parent.Children[Index] = ExpandedImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementExpandedImage(parent.Children[Index], ElementValue, parent)

			elif Type == "ani_image":
				parent.Children[Index] = AniImageBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementAniImage(parent.Children[Index], ElementValue, parent)

			elif Type == "slot":
				parent.Children[Index] = SlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlot(parent.Children[Index], ElementValue, parent)

			elif Type == "candidate_list":
				parent.Children[Index] = CandidateListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCandidateList(parent.Children[Index], ElementValue, parent)

			elif Type == "grid_table":
				parent.Children[Index] = GridSlotWindow()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGridTable(parent.Children[Index], ElementValue, parent)

			elif Type == "text":
				parent.Children[Index] = TextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementText(parent.Children[Index], ElementValue, parent)

			elif Type == "editline":
				parent.Children[Index] = EditLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementEditLine(parent.Children[Index], ElementValue, parent)

			elif Type == "titlebar":
				parent.Children[Index] = TitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "horizontalbar":
				parent.Children[Index] = HorizontalBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementHorizontalBar(parent.Children[Index], ElementValue, parent)

			elif Type == "board":
				parent.Children[Index] = Board()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "border_a":
				parent.Children[Index] = BorderA()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "board_with_titlebar":
				parent.Children[Index] = BoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "dragonboard":
				parent.Children[Index] = DragonBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "dragonboard_with_titlebar":
				parent.Children[Index] = DragonBoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "new_board":
				parent.Children[Index] = NewBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "new_board_with_titlebar":
				parent.Children[Index] = NewBoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "main_board":
				parent.Children[Index] = MainBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "main_board_with_titlebar":
				parent.Children[Index] = MainBoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "main_sub_board":
				parent.Children[Index] = MainSubBoard("100" if ElementValue.has_key("full_opacity") else "50")
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard":
				parent.Children[Index] = ThinBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_circle":
				parent.Children[Index] = ThinBoardCircle()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_gold":
				parent.Children[Index] = ThinBoardGold()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_new":
				parent.Children[Index] = ThinBoardNew()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_":
				parent.Children[Index] = Thinboard_Unique()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "box":
				parent.Children[Index] = Box()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBox(parent.Children[Index], ElementValue, parent)

			elif Type == "bar":
				parent.Children[Index] = Bar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBar(parent.Children[Index], ElementValue, parent)

			elif Type == "line":
				parent.Children[Index] = Line()
				parent.Children[Index].SetParent(parent)
				self.LoadElementLine(parent.Children[Index], ElementValue, parent)

			elif Type == "slotbar":
				parent.Children[Index] = SlotBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlotBar(parent.Children[Index], ElementValue, parent)

			elif Type == "gauge":
				parent.Children[Index] = Gauge()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGauge(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar":
				parent.Children[Index] = ScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "slimscrollbar":
				parent.Children[Index] = NewScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "slim_scrollbar":
				parent.Children[Index] = SlimScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSlimScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "thin_scrollbar":
				parent.Children[Index] = ThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "small_thin_scrollbar":
				parent.Children[Index] = SmallThinScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			elif Type == "sliderbar":
				parent.Children[Index] = SliderBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSliderBar(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox":
				parent.Children[Index] = ListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox(parent.Children[Index], ElementValue, parent)

			elif Type == "listbox2":
				parent.Children[Index] = ListBox2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBox2(parent.Children[Index], ElementValue, parent)

			elif Type == "listboxex":
				parent.Children[Index] = ListBoxEx()
				parent.Children[Index].SetParent(parent)
				self.LoadElementListBoxEx(parent.Children[Index], ElementValue, parent)

			elif Type == "checkbox":
				# if ElementValue.has_key("new"):
				# 	parent.Children[Index] = CheckBox("UI", ElementValue["new"])
				# else:
				parent.Children[Index] = CheckBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementCheckBox(parent.Children[Index], ElementValue, parent)

			elif Type == "render_target" and app.ENABLE_RENDER_TARGET_EXTENSION:
				parent.Children[Index] = RenderTarget()
				parent.Children[Index].SetParent(parent)
				self.LoadElementRenderTarget(parent.Children[Index], ElementValue, parent)

			elif Type == "subtitlebar" and app.ENABLE_QUEST_RENEWAL:
				parent.Children[Index] = SubTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementSubTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "table":
				parent.Children[Index] = Table()
				parent.Children[Index].SetParent(parent)
				self.LoadElementTable(parent.Children[Index], ElementValue, parent)

			elif Type == "updownbutton":
				parent.Children[Index] = UpDownButton()
				parent.Children[Index].SetParent(parent)
				self.LoadElementUpDownButton(parent.Children[Index], ElementValue, parent)

			elif Type == "field":
				if ElementValue.has_key("path"):
					parent.Children[Index] = InputField(ElementValue["path"])
				else:
					parent.Children[Index] = InputField()

				parent.Children[Index].SetParent(parent)
				self.LoadElementInputField(parent.Children[Index], ElementValue, parent)

			elif Type == "extended_text":
				parent.Children[Index] = ExtendedTextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementExtendedText(parent.Children[Index], ElementValue, parent)

			elif Type == "boxed_board":
				parent.Children[Index] = BoxedBoard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoxedBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "input" and app.ENABLE_LUCKY_BOX:
				parent.Children[Index] = Input()
				parent.Children[Index].SetParent(parent)
				self.LoadElementInput(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar_template":
				parent.Children[Index] = ScrollBarTemplate()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBarTemplate(parent.Children[Index], ElementValue, parent)

			elif Type == "multi_text":
				parent.Children[Index] = MultiTextLine()
				parent.Children[Index].SetParent(parent)
				self.LoadElementMultiText(parent.Children[Index], ElementValue, parent)

			elif Type == "thinboard_daily":
				parent.Children[Index] = ThinBoardDailyReward()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoardDaily(parent.Children[Index], ElementValue, parent)

			elif Type == "shortcut":
				parent.Children[Index] = Shortcut()
				parent.Children[Index].SetParent(parent)
				self.LoadElementShortcut(parent.Children[Index], ElementValue, parent)

			elif Type == "line_graph":
				parent.Children[Index] = LineGraph()
				parent.Children[Index].SetParent(parent)
				self.LoadElementLineGraph(parent.Children[Index], ElementValue, parent)

			elif Type == "bar_graph":
				parent.Children[Index] = BarGraph()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBarGraph(parent.Children[Index], ElementValue, parent)

			elif Type == "selectable_text":
				parent.Children[Index] = SelectableTextLine(True)
				parent.Children[Index].SetParent(parent)
				self.LoadElementSelectableText(parent.Children[Index], ElementValue, parent)

			elif Type == "scrollbar_search":
				parent.Children[Index] = ScrollBarSearch()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBarSearch(parent.Children[Index], ElementValue, parent)

			elif Type == "pixellistbox":
				parent.Children[Index] = PixelScrollListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementPixelScrollListBox(parent.Children[Index], ElementValue, parent)

			elif Type == "unfoldlistbox":
				parent.Children[Index] = UnfoldListBox2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementUnfoldListBox(parent.Children[Index], ElementValue, parent)

			elif Type == "modern_scrollbar":
				parent.Children[Index] = ModernScrollBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementModernScrollBar(parent.Children[Index], ElementValue, parent)
				
			elif app.ENABLE_PREMIUM_PRIVATE_SHOP and Type == "thinboard_deco":
				parent.Children[Index] = ShopDecoThinboard()
				parent.Children[Index].SetParent(parent)
				self.LoadElementThinBoard(parent.Children[Index], ElementValue, parent)

			elif Type == "grid_listbox":
				parent.Children[Index] = GridListBox()
				parent.Children[Index].SetParent(parent)
				self.LoadElementGridListBox(parent.Children[Index], ElementValue, parent)

			elif Type == "board_with_titlebar_without_button":
				parent.Children[Index] = BoardWithTitleBar()
				parent.Children[Index].SetParent(parent)
				self.LoadElementBoardWithTitleBar(parent.Children[Index], ElementValue, parent)

			elif Type == "new_scrollbar":
				parent.Children[Index] = NewScrollBar2()
				parent.Children[Index].SetParent(parent)
				self.LoadElementScrollBar(parent.Children[Index], ElementValue, parent)

			else:
				Index += 1
				continue

			parent.Children[Index].SetWindowName(Name)
			if 0 != self.InsertFunction:
				self.InsertFunction(Name, parent.Children[Index], Type)

			self.LoadChildren(parent.Children[Index], ElementValue)
			Index += 1

	def CheckKeyList(self, name, value, key_list):

		for DataKey in key_list:
			if False == value.has_key(DataKey):
				print "Failed to find data key", "[" + name + "/" + DataKey + "]"
				return False

		return True

	def LoadDefaultData(self, window, value, parentWindow):
		loc_x = int(value["x"])
		loc_y = int(value["y"])
		if value.has_key("vertical_align"):
			if "center" == value["vertical_align"]:
				window.SetWindowVerticalAlignCenter()
			elif "bottom" == value["vertical_align"]:
				window.SetWindowVerticalAlignBottom()

		if parentWindow.IsRTL():
			loc_x = int(value["x"]) + window.GetWidth()
			if value.has_key("horizontal_align"):
				if "center" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignCenter()
					loc_x = - int(value["x"])
				elif "right" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignLeft()
					loc_x = int(value["x"]) - window.GetWidth()
					## loc_x = parentWindow.GetWidth() - int(value["x"]) + window.GetWidth()
			else:
				window.SetWindowHorizontalAlignRight()

			if value.has_key("all_align"):
				window.SetWindowVerticalAlignCenter()
				window.SetWindowHorizontalAlignCenter()
				loc_x = - int(value["x"])
		else:
			if value.has_key("horizontal_align"):
				if "center" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignCenter()
				elif "right" == value["horizontal_align"]:
					window.SetWindowHorizontalAlignRight()

		window.SetPosition(loc_x, loc_y)
		window.Show()

		if "content_window" in value:
			parentWindow.SetContentWindow(window)

	## Window
	def LoadElementWindow(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.WINDOW_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))

		if True == value.has_key("renderer"):
			window.SetInsideRender(True)

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Button
	def LoadElementButton(self, window, value, parentWindow):

		if value.has_key("width") and value.has_key("height"):
			window.SetSize(int(value["width"]), int(value["height"]))

		if True == value.has_key("default_image"):
			window.SetUpVisual(value["default_image"])
		if True == value.has_key("over_image"):
			window.SetOverVisual(value["over_image"])
		if True == value.has_key("down_image"):
			window.SetDownVisual(value["down_image"])
		if True == value.has_key("disable_image"):
			window.SetDisableVisual(value["disable_image"])

		if value.has_key("text_left_aligned"):
			window.SetTextLeftAligned()

		if True == value.has_key("text"):
			if True == value.has_key("text_height"):
				window.SetText(value["text"], value["text_height"])
			else:
				window.SetText(value["text"])

			if value.has_key("text_color"):
				window.SetTextColor(value["text_color"])

		if True == value.has_key("multi_text"):
			window.SetMultiText(value["multi_text"])

		if True == value.has_key("tooltip_text"):
			if True == value.has_key("tooltip_x") and True == value.has_key("tooltip_y"):
				window.SetToolTipText(value["tooltip_text"], int(value["tooltip_x"]), int(value["tooltip_y"]))
			else:
				window.SetToolTipText(value["tooltip_text"])

		if True == value.has_key("images"):
			images = value["images"]
			window.SetUpVisual(images[0])
			window.SetOverVisual(images[1])
			window.SetDownVisual(images[2])

			if len(images) == 4:
				window.SetDisableVisual(images[3])


		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Mark
	def LoadElementMark(self, window, value, parentWindow):

		#if False == self.CheckKeyList(value["name"], value, self.MARK_KEY_LIST):
		#	return False

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Image
	def LoadElementImage(self, window, value, parentWindow):

		# if False == self.CheckKeyList(value["name"], value, self.IMAGE_KEY_LIST):
		# 	return False

		if value.has_key("image"):
			window.LoadImage(value["image"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## AniImage
	def LoadElementAniImage(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.ANI_IMAGE_KEY_LIST):
			return False

		if True == value.has_key("delay"):
			window.SetDelay(value["delay"])

		for image in value["images"]:
			window.AppendImage(image)

		if value.has_key("width") and value.has_key("height"):
			window.SetSize(value["width"], value["height"])

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Expanded Image
	def LoadElementExpandedImage(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.EXPANDED_IMAGE_KEY_LIST):
			return False

		window.LoadImage(value["image"])

		if True == value.has_key("x_origin") and True == value.has_key("y_origin"):
			window.SetOrigin(float(value["x_origin"]), float(value["y_origin"]))

		if True == value.has_key("x_scale") and True == value.has_key("y_scale"):
			window.SetScale(float(value["x_scale"]), float(value["y_scale"]))

		if True == value.has_key("rect"):
			RenderingRect = value["rect"]
			window.SetRenderingRect(RenderingRect[0], RenderingRect[1], RenderingRect[2], RenderingRect[3])

		if True == value.has_key("mode"):
			mode = value["mode"]
			if "MODULATE" == mode:
				window.SetRenderingMode(wndMgr.RENDERING_MODE_MODULATE)

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Slot
	def LoadElementSlot(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SLOT_KEY_LIST):
			return False

		global_x = int(value["x"])
		global_y = int(value["y"])
		global_width = int(value["width"])
		global_height = int(value["height"])

		window.SetPosition(global_x, global_y)
		window.SetSize(global_width, global_height)
		window.Show()

		r = 1.0
		g = 1.0
		b = 1.0
		a = 1.0

		if True == value.has_key("image_r") and \
			True == value.has_key("image_g") and \
			True == value.has_key("image_b") and \
			True == value.has_key("image_a"):
			r = float(value["image_r"])
			g = float(value["image_g"])
			b = float(value["image_b"])
			a = float(value["image_a"])

		SLOT_ONE_KEY_LIST = ("index", "x", "y", "width", "height")

		for slot in value["slot"]:
			if True == self.CheckKeyList(value["name"] + " - one", slot, SLOT_ONE_KEY_LIST):
				wndMgr.AppendSlot(window.hWnd,
									int(slot["index"]),
									int(slot["x"]),
									int(slot["y"]),
									int(slot["width"]),
									int(slot["height"]))

				window.slotList.append(int(slot["index"]))

		# window.RefreshIndices()

		if True == value.has_key("image"):
			if True == value.has_key("x_scale") and True == value.has_key("y_scale"):
				wndMgr.SetSlotBaseImageScale(window.hWnd, value["image"], r, g, b, a, float(value["x_scale"]), float(value["y_scale"]))
			else:
				wndMgr.SetSlotBaseImage(window.hWnd, value["image"], r, g, b, a)

		return True

	def LoadElementCandidateList(self, window, value, parentWindow):
		if False == self.CheckKeyList(value["name"], value, self.CANDIDATE_LIST_KEY_LIST):
			return False

		window.SetPosition(int(value["x"]), int(value["y"]))
		window.SetItemSize(int(value["item_xsize"]), int(value["item_ysize"]))
		window.SetItemStep(int(value["item_step"]))
		window.Show()

		return True

	## Table
	def LoadElementGridTable(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.GRID_TABLE_KEY_LIST):
			return False

		xBlank = 0
		yBlank = 0
		if True == value.has_key("x_blank"):
			xBlank = int(value["x_blank"])
		if True == value.has_key("y_blank"):
			yBlank = int(value["y_blank"])

		window.SetPosition(int(value["x"]), int(value["y"]))

		window.ArrangeSlot(	int(value["start_index"]),
							int(value["x_count"]),
							int(value["y_count"]),
							int(value["x_step"]),
							int(value["y_step"]),
							xBlank,
							yBlank)
		if True == value.has_key("image"):
			r = 1.0
			g = 1.0
			b = 1.0
			a = 1.0
			if True == value.has_key("image_r") and \
				True == value.has_key("image_g") and \
				True == value.has_key("image_b") and \
				True == value.has_key("image_a"):
				r = float(value["image_r"])
				g = float(value["image_g"])
				b = float(value["image_b"])
				a = float(value["image_a"])
			wndMgr.SetSlotBaseImage(window.hWnd, value["image"], r, g, b, a)

		if True == value.has_key("style"):
			if "select" == value["style"]:
				wndMgr.SetSlotStyle(window.hWnd, wndMgr.SLOT_STYLE_SELECT)

		window.Show()

		return True

	## Text
	def LoadElementText(self, window, value, parentWindow):

		if value.has_key("fontsize"):
			fontSize = value["fontsize"]

			if "LARGE" == fontSize:
				window.SetFontName(localeInfo.UI_DEF_FONT_LARGE)

		elif value.has_key("fontname"):
			fontName = value["fontname"]
			window.SetFontName(fontName)

		if value.has_key("text_horizontal_align"):
			if "left" == value["text_horizontal_align"]:
				window.SetHorizontalAlignLeft()
			elif "center" == value["text_horizontal_align"]:
				window.SetHorizontalAlignCenter()
			elif "right" == value["text_horizontal_align"]:
				window.SetHorizontalAlignRight()

		if value.has_key("text_vertical_align"):
			if "top" == value["text_vertical_align"]:
				window.SetVerticalAlignTop()
			elif "center" == value["text_vertical_align"]:
				window.SetVerticalAlignCenter()
			elif "bottom" == value["text_vertical_align"]:
				window.SetVerticalAlignBottom()

		if value.has_key("all_align"):
			window.SetHorizontalAlignCenter()
			window.SetVerticalAlignCenter()
			window.SetWindowHorizontalAlignCenter()
			window.SetWindowVerticalAlignCenter()

		if value.has_key("r") and value.has_key("g") and value.has_key("b"):
			window.SetFontColor(float(value["r"]), float(value["g"]), float(value["b"]))
		elif value.has_key("color"):
			window.SetPackedFontColor(value["color"])
		else:
			window.SetFontColor(DEFAULT_TEXT_COLOR, DEFAULT_TEXT_COLOR, DEFAULT_TEXT_COLOR)

		if value.has_key("outline"):
			if value["outline"]:
				window.SetOutline()
		if True == value.has_key("text"):
			window.SetText(value["text"])

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## EditLine
	def LoadElementEditLine(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.EDIT_LINE_KEY_LIST):
			return False


		if value.has_key("secret_flag"):
			window.SetSecret(value["secret_flag"])
		if value.has_key("with_codepage"):
			if value["with_codepage"]:
				window.bCodePage = True
		if value.has_key("only_number"):
			if value["only_number"]:
				window.SetNumberMode()
		if value.has_key("enable_codepage"):
			window.SetIMEFlag(value["enable_codepage"])
		if value.has_key("enable_ime"):
			window.SetIMEFlag(value["enable_ime"])
		if value.has_key("limit_width"):
			window.SetLimitWidth(value["limit_width"])
		if value.has_key("multi_line"):
			if value["multi_line"]:
				window.SetMultiLine()
				
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if value.has_key("only_currency"):
				if value["only_currency"]:
					window.SetCurrencyMode()

		if value.has_key("overlay"):
			window.SetOverlayText(value["overlay"])

		window.SetMax(int(value["input_limit"]))
		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadElementText(window, value, parentWindow)

		return True

	## TitleBar
	def LoadElementTitleBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.TITLE_BAR_KEY_LIST):
			return False

		window.MakeTitleBar(int(value["width"]), value.get("color", "red"))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## HorizontalBar
	def LoadElementHorizontalBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.HORIZONTAL_BAR_KEY_LIST):
			return False

		window.Create(int(value["width"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Board
	def LoadElementBoard(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Board With TitleBar
	def LoadElementBoardWithTitleBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_WITH_TITLEBAR_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		window.SetTitleName(value["title"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## ThinBoard
	def LoadElementThinBoard(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Box
	def LoadElementBox(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BOX_KEY_LIST):
			return False

		if True == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Bar
	def LoadElementBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.BAR_KEY_LIST):
			return False

		if True == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Line
	def LoadElementLine(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LINE_KEY_LIST):
			return False

		if True == value.has_key("color"):
			window.SetColor(value["color"])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Slot
	def LoadElementSlotBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SLOTBAR_KEY_LIST):
			return False

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## Gauge
	def LoadElementGauge(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.GAUGE_KEY_LIST):
			return False

		window.MakeGauge(value["width"], value["color"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## ScrollBar
	def LoadElementScrollBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SCROLLBAR_KEY_LIST):
			return False

		window.SetScrollBarSize(value["size"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	def LoadElementSlimScrollBar(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SCROLLBAR_KEY_LIST):
			return False

		if False == value.has_key("create_colors"):
			return False

		window.CreateScrollBar(value["create_colors"][0], value["create_colors"][1])

		window.SetBgSize(value["size"])

		if True == value.has_key("scroll_width"):
			window.SetScrollWidth(value["scroll_width"])

		if True == value.has_key("scroll_mid_size"):
			window.SetMiddleSize(value["scroll_mid_size"])

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## SliderBar
	def LoadElementSliderBar(self, window, value, parentWindow):

		self.LoadDefaultData(window, value, parentWindow)

		return True

	## ListBox
	def LoadElementListBox(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		if value.has_key("item_align"):
			window.SetTextCenterAlign(value["item_align"])

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	## ListBox2
	def LoadElementListBox2(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		window.SetRowCount(value.get("row_count", 10))
		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.has_key("item_align"):
			window.SetTextCenterAlign(value["item_align"])

		return True
	def LoadElementListBoxEx(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.has_key("itemsize_x") and value.has_key("itemsize_y"):
			window.SetItemSize(int(value["itemsize_x"]), int(value["itemsize_y"]))

		if value.has_key("itemstep"):
			window.SetItemStep(int(value["itemstep"]))

		if value.has_key("viewcount"):
			window.SetViewItemCount(int(value["viewcount"]))

		return True

	def LoadElementCheckBox(self, window, value, parentWindow):

		if value.has_key("text"):
			window.SetText(value["text"])

		if value.has_key("text_color"):
			window.SetTextColor(value["text_color"])

		if value.has_key("checked") and value["checked"] == True:
			window.SetChecked(window.STATE_SELECTED)

		if value.has_key("disabled") and value["disabled"] == True:
			window.Disable()
		
		if value.has_key("sPath"):
			window.LoadResources(value["sPath"], value["sUnselected"], value["sSelected"])
		
		# if value.has_key("sUnselected"):
		# 	window.LoadResources(sUnselected = value["sUnselected"], sSelected = value["sSelected"])

		self.LoadDefaultData(window, value, parentWindow)

	if app.ENABLE_RENDER_TARGET_EXTENSION:
		def LoadElementRenderTarget(self, window, value, parentWindow):
			if value.has_key("image"):
				window.LoadImage(value["image"])

			if value.has_key("race"):
				window.SetRenderTarget(value["race"])

			if value.has_key("rotation"):
				window.SetRotationMode(value["rotation"])

			self.LoadDefaultData(window, value, parentWindow)

	if app.ENABLE_QUEST_RENEWAL:
		## SubTitleBar
		def LoadElementSubTitleBar(self, window, value, parentWindow):
			if False == self.CheckKeyList(value["name"], value, self.SUB_TITLE_BAR_KEY_LIST):
				return False

			window.MakeSubTitleBar(int(value["width"]), value.get("color", "red"))
			self.LoadElementButton(window, value, parentWindow)
			window.Show()
			return True

		## ListBar
		def LoadElementListBar(self, window, value, parentWindow):
			if False == self.CheckKeyList(value["name"], value, self.LIST_BAR_KEY_LIST):
				return False

			window.MakeListBar(int(value["width"]), value.get("color", "red"))
			self.LoadElementButton(window, value, parentWindow)

			return True

	def LoadElementInputField(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.INPUT_FIELD_KEY_LIST):
			return False

		if True == value.has_key("alpha"):
			window.SetAlpha(value["alpha"])

		window.SetSize(int(value["width"]), int(value["height"]))

		self.LoadDefaultData(window, value, parentWindow)

		return True

	if app.ENABLE_ADMIN_MANAGER:
		def LoadElementTable(self, window, value, parentWindow):

			if False == self.CheckKeyList(value["name"], value, self.TABLE_KEY_LIST):
				return False

			if value.has_key("height"):
				window.SetSize(value["width"], value["height"])
			else:
				window.SetWidth(value["width"])
			self.LoadDefaultData(window, value, parentWindow)

			if value.has_key("col_length_check"):
				for index in value["col_length_check"]:
					window.AddCheckLengthIndex(index)

			if value.has_key("col_size"):
				window.SetColSizePct(value["col_size"])

				if value.has_key("header"):
					if value.has_key("header_extra"):
						window.SetHeader(value["header"], int(value["header_extra"]))
					else:
						window.SetHeader(value["header"])

				if value.has_key("content"):
					i = 0
					for colList in value["content"]:
						window.Append(i, colList, False)
						i += 1
					window.LocateLines()

			return True

		def LoadElementUpDownButton(self, window, value, parentWindow):

			if value.has_key("value"):
				window.SetValue(value["value"])
			if value.has_key("min"):
				window.SetMin(value["min"])
			if value.has_key("max"):
				window.SetMax(value["max"])

			self.LoadDefaultData(window, value, parentWindow)

			return True

		def LoadElementInputField(self, window, value, parentWindow):

			if False == self.CheckKeyList(value["name"], value, self.INPUT_FIELD_KEY_LIST):
				return False

			if True == value.has_key("alpha"):
				window.SetAlpha(value["alpha"])

			window.SetSize(int(value["width"]), int(value["height"]))

			self.LoadDefaultData(window, value, parentWindow)

			return True

		def LoadElementExtendedText(self, window, value, parentWindow):

			if True == value.has_key("text"):
				window.SetText(value["text"])

			self.LoadDefaultData(window, value, parentWindow)

			return True

	def LoadElementBoxedBoard(self, window, value, parentWindow):
		if not self.CheckKeyList(value["name"], value, self.WINDOW_KEY_LIST):
			return False

		window.SetSize(value["width"], value["height"])

		if value.has_key("border_color"):
			window.SetBorderColor(value["border_color"])

		if value.has_key("border_size"):
			window.SetBorderSize(value["border_size"])

		if value.has_key("base_color"):
			window.SetBaseColor(value["base_color"])

		self.LoadDefaultData(window, value, parentWindow)
		return True

	if app.ENABLE_LUCKY_BOX:
		def LoadElementInput(self, window, value, parentWindow):
			if False == self.CheckKeyList(value["name"], value, self.TITLE_BAR_KEY_LIST):
				return False

			window.MakeInput(int(value["width"]))
			self.LoadDefaultData(window, value, parentWindow)

			return True

	def LoadElementScrollBarTemplate(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.SCROLLBAR_TEMPLATE_KEY_LIST):
			return False

		if value.has_key("bg_image"):
			window.SetBarImage(value["bg_image"])
		if value.has_key("bg_top_image") and value.has_key("bg_center_image") and value.has_key("bg_bottom_image"):
			window.SetBarPartImages(value["bg_top_image"], value["bg_center_image"], value["bg_bottom_image"])
		if value.has_key("top_btn_up_visual") and value.has_key("top_btn_over_visual") and value.has_key("top_btn_down_visual"):
			window.SetUpButton(value["top_btn_up_visual"], value["top_btn_over_visual"], value["top_btn_down_visual"])
		if value.has_key("bot_btn_up_visual") and value.has_key("bot_btn_over_visual") and value.has_key("bot_btn_down_visual"):
			window.SetDownButton(value["bot_btn_up_visual"], value["bot_btn_over_visual"], value["bot_btn_down_visual"])
		window.SetMiddleImage(value["middle_image"])

		self.LoadDefaultData(window, value, parentWindow)
		window.SetScrollBarSize(value["size"])

		return True

	## MultiTextLine
	def LoadElementMultiText(self, window, value, parent):

		if value.has_key("width") and value.has_key("height"):
			window.SetSize(value["width"], value["height"])
		elif value.has_key("width"):
			window.SetWidth(value["width"])

		if value.has_key("text_horizontal_align"):
			if "center" == value["text_horizontal_align"]:
				window.SetTextHorizontalAlignCenter()

		if value.has_key("text_vertical_align"):
			if "center" == value["text_vertical_align"]:
				window.SetTextVerticalAlignCenter()

		if value.has_key("r") and value.has_key("g") and value.has_key("b"):
			window.SetFontColor(float(value["r"]), float(value["g"]), float(value["b"]))
		elif value.has_key("color"):
			window.SetPackedFontColor(value["color"])
		elif value.has_key("register_color"):
			for data in value["register_color"]:
				window.RegisterPackedFontColor(data[0], data[1])
				if len(data) > 2 and data[2] == True:
					window.SetPackedFontColor(data[1])

		if value.has_key("text"):
			window.SetText(value["text"])

		self.LoadDefaultData(window, value, parent)

		return True

	def LoadElementThinBoardDaily(self, window, value, parentWindow):
		if not self.CheckKeyList(value["name"], value, self.BOARD_KEY_LIST):
			return False

		for i in xrange(4):
			if value.has_key("corner_%d" % i):
				window.HideCorners(value["corner_%d" % i])

			if value.has_key("line_%d" % i):
				window.HideLine(value["line_%d" % i])

		window.SetSize(int(value["width"]), int(value["height"]))
		self.LoadDefaultData(window, value, parentWindow)

	def LoadElementShortcut(self, window, value, parentWindow):
		if not self.CheckKeyList(value["name"], value, self.SHORTCUT_KEY_LIST):
			return False

		window.SetShortcut(value["shortcut"])
		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementGraphDefault(self, window, value, parent):
		if value.has_key("width") and value.has_key("height"):
			window.SetSize(value["width"], value["height"])

		if value.has_key("y_axis_limit"):
			window.SetYAxisLimitValue(value["y_axis_limit"][0], value["y_axis_limit"][1])

		if value.has_key("x_axis_limit"):
			window.SetXAxisLimitValue(value["x_axis_limit"][0], value["x_axis_limit"][1])

		if value.has_key("color"):
			window.SetColor(value["color"])

		return True

	def LoadElementLineGraph(self, window, value, parent):
		self.LoadDefaultData(window, value, parent)
		self.LoadElementGraphDefault(window, value, parent)

		if value.has_key("line_thickness"):
			window.SetLineThickness(value["line_thickness"])

		return True

	def LoadElementBarGraph(self, window, value, parent):
		self.LoadDefaultData(window, value, parent)
		self.LoadElementGraphDefault(window, value, parent)

		if value.has_key("bar_space"):
			window.SetBarSpace(value["bar_space"])

		return True

	def LoadElementSelectableText(self, window, value, parent):
		if value.has_key("colors"):
			sColors = {
				"normal" : value["colors"][0],
				"over" : value["colors"][1],
				"down" : value["colors"][2],
			}
			window.SetColors(sColors)

		if value.has_key("text"):
			window.SetText(value["text"])

		# window.SetSize(int(value["width"]), int(value["height"]))

		self.LoadDefaultData(window, value, parent)

		return True

	def LoadElementScrollBarSearch(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.SCROLLBAR_SEARCH_KEY_LIST):
			return FALSE

		if value.has_key("bg_image"):
			window.SetBarImage(value["bg_image"])
		elif value.has_key("bar_width"):
			window.SetBarWidth(value["bar_width"])
		if value.has_key("top_btn_up_visual"):
			window.SetUpButton(value["top_btn_up_visual"], value["top_btn_over_visual"], value["top_btn_down_visual"])
		if value.has_key("bot_btn_up_visual"):
			window.SetDownButton(value["bot_btn_up_visual"], value["bot_btn_over_visual"], value["bot_btn_down_visual"])
		window.SetMiddleImages(value["middle_image_top"], value["middle_image_center"], value["middle_image_bottom"])

		self.LoadDefaultData(window, value, parentWindow)
		window.SetScrollBarSize(value["size"])

		return TRUE

	def LoadElementPixelScrollListBox(self, window, value, parentWindow):

		if FALSE == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return FALSE

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		if value.has_key("vertical_space"):
			window.SetVerticalSpace(int(value["vertical_space"]))

		return True

	def LoadElementUnfoldListBox(self, window, value, parentWindow):

		if False == self.CheckKeyList(value["name"], value, self.LIST_BOX_KEY_LIST):
			return False

		if value.has_key("x_dif"):
			window.SetXDif(value["x_dif"])
		if value.has_key("y_dif"):
			window.SetYDif(value["y_dif"])

		window.SetSize(value["width"], value["height"])
		self.LoadDefaultData(window, value, parentWindow)

		return True

	def LoadElementModernScrollBar(self, window, value, parentWindow):
		if not self.CheckKeyList(value["name"], value, self.MODERN_SCROLLBAR_KEY_LIST):
			return False

		window.SetScrollBarSize(value["size"])

		if value.has_key("content_height"):
			window.SetContentHeight(value["content_height"])

		if value.has_key("width"):
			window.SetWidth(value["width"])

		self.LoadDefaultData(window, value, parentWindow)
		return True

	def LoadElementGridListBox(self, window, value, parentWindow):
		if not self.CheckKeyList(value["name"], value, self.GRID_LIST_BOX_KEY_LIST):
			return False

		window.Initialize(value["itemsize"], value["itemstep"], value["viewcount"])
		self.LoadDefaultData(window, value, parentWindow)
		return True

class ReadingWnd(Bar):

	def __init__(self):
		Bar.__init__(self,"TOP_MOST")

		self.__BuildText()
		self.SetSize(80, 19)
		self.Show()

	def __del__(self):
		Bar.__del__(self)

	def __BuildText(self):
		self.text = TextLine()
		self.text.SetParent(self)
		self.text.SetPosition(4, 3)
		self.text.Show()

	def SetText(self, text):
		self.text.SetText(text)

	def SetReadingPosition(self, x, y):
		xPos = x + 2
		yPos = y  - self.GetHeight() - 2
		self.SetPosition(xPos, yPos)

	def SetTextColor(self, color):
		self.text.SetPackedFontColor(color)

def MakeSlotBar(parent, x, y, width, height):
	slotBar = SlotBar()
	slotBar.SetParent(parent)
	slotBar.SetSize(width, height)
	slotBar.SetPosition(x, y)
	slotBar.Show()
	return slotBar

def MakeImageBox(parent, name, x, y):
	image = ImageBox()
	image.SetParent(parent)
	image.LoadImage(name)
	image.SetPosition(x, y)
	image.Show()
	return image

def MakeExpandedImageBox(parent, name, x, y, flag = ""):
	image = ExpandedImageBox()
	image.SetParent(parent)
	image.LoadImage(name)
	image.SetPosition(x, y)
	if flag != "":
		image.AddFlag(flag)
	image.Show()

	return image

def MakeTextLine(parent, horizontalAlign = True, verticalAlgin = True, x = 0, y = 0, text = ""):
	textLine = TextLine()
	textLine.SetParent(parent)
	
	if horizontalAlign == True:
		textLine.SetWindowHorizontalAlignCenter()
	
	if verticalAlgin == True:
		textLine.SetWindowVerticalAlignCenter()
	
	textLine.SetHorizontalAlignCenter()
	textLine.SetVerticalAlignCenter()
	textLine.SetPosition(x, y)
	textLine.SetText(text)
	textLine.Show()
	
	return textLine

def MakeTextLineNew(parent, x, y, text):
	textLine = TextLine()
	textLine.SetParent(parent)
	textLine.SetPosition(x, y)
	textLine.SetText(text)
	textLine.Show()

	return textLine

def MakeExtendedTextLine(parent, hA = True, vA = True, pos = (0, 0)):
	eTextLine = ExtendedTextLine()
	eTextLine.SetParent(parent)
	eTextLine.SetPosition(*pos)

	if hA == True:
		eTextLine.SetWindowHorizontalAlignCenter()
	
	if vA == True:
		eTextLine.SetWindowVerticalAlignCenter()

	eTextLine.Show()

	return eTextLine

def MakeButton(parent, x, y, tooltipText, path, up, over, down, text = "", height = 0):
	button = Button()
	button.SetParent(parent)
	button.SetPosition(x, y)
	button.SetUpVisual(path + up)
	button.SetOverVisual(path + over)
	button.SetDownVisual(path + down)
	button.SetToolTipText(tooltipText)
	if text != "":
		button.SetText(text, height)
	button.Show()
	return button

def RenderRoundBox(x, y, width, height, color):
	grp.SetColor(color)
	grp.RenderLine(x+2, y, width-3, 0)
	grp.RenderLine(x+2, y+height, width-3, 0)
	grp.RenderLine(x, y+2, 0, height-4)
	grp.RenderLine(x+width, y+1, 0, height-3)
	grp.RenderLine(x, y+2, 2, -2)
	grp.RenderLine(x, y+height-2, 2, 2)
	grp.RenderLine(x+width-2, y, 2, 2)
	grp.RenderLine(x+width-2, y+height, 2, -2)

def MakeThinBoard(parent,  x, y, width, heigh, moveable=False,center=False):
	thin = ThinBoard()
	if parent != None:
		thin.SetParent(parent)
	if moveable == True:
		thin.AddFlag('movable')
		thin.AddFlag('float')
	thin.SetSize(width, heigh)
	thin.SetPosition(x, y)
	if center == True:
		thin.SetCenterPosition()
	thin.Show()
	
	return thin

if app.ENABLE_RENDER_TARGET_EXTENSION:
	def MakeRenderTarget(parent, iModel = -1, lSize = (100, 100), lPos = (0, 0), sBackground = "d:/ymir work/ui/game/myshop_deco/model_view_bg.sub"):
		render = RenderTarget()
		render.SetParent(parent)
		if iModel != -1:
			render.SetRenderTarget(iModel)
		render.SetSize(*lSize)
		render.SetPosition(*lPos)
		render.LoadImage(sBackground)
		render.Show()

		return render

def GenerateColor(r, g, b):
	r = float(r) / 255.0
	g = float(g) / 255.0
	b = float(b) / 255.0
	return grp.GenerateColor(r, g, b, 1.0)

def EnablePaste(flag):
	ime.EnablePaste(flag)

def GetHyperlink():
	return wndMgr.GetHyperlink()

if app.INGAME_WIKI:
	class WikiRenderTarget(Window):
		def __init__(self):
			Window.__init__(self)

		def __del__(self):
			Window.__del__(self)

		def RegisterWindow(self, layer):
			self.hWnd = wndMgr.RegisterWikiRenderTarget(self, layer)

	class InGameWikiCheckBox(Window):
		def __init__(self):
			Window.__init__(self)

			self.backgroundImage = None
			self.checkImage = None

			self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
			self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }

			self.CreateElements()

		def __del__(self):
			Window.__del__(self)

			self.backgroundImage = None
			self.checkImage = None

			self.eventFunc = { "ON_CHECK" : None, "ON_UNCKECK" : None, }
			self.eventArgs = { "ON_CHECK" : None, "ON_UNCKECK" : None, }

		def CreateElements(self):
			self.backgroundImage = ImageBox()
			self.backgroundImage.SetParent(self)
			self.backgroundImage.AddFlag("not_pick")
			self.backgroundImage.LoadImage("d:/ymir work/ui/wiki/wiki_check_box_clean.tga")
			self.backgroundImage.Show()

			self.checkImage = ImageBox()
			self.checkImage.SetParent(self)
			self.checkImage.AddFlag("not_pick")
			self.checkImage.LoadImage("d:/ymir work/ui/wiki/wiki_check_box_checked.tga")
			self.checkImage.Hide()

			self.textInfo = TextLine()
			self.textInfo.SetParent(self)
			self.textInfo.SetPosition(20, 0)
			self.textInfo.Show()

			self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])

		def SetTextInfo(self, info):
			if self.textInfo:
				self.textInfo.SetText(info)

			self.SetSize(self.backgroundImage.GetWidth() + self.textInfo.GetTextSize()[0], self.backgroundImage.GetHeight() + self.textInfo.GetTextSize()[1])

		def SetCheckStatus(self, flag):
			if flag:
				self.checkImage.Show()
			else:
				self.checkImage.Hide()

		def GetCheckStatus(self):
			if self.checkImage:
				return self.checkImage.IsShow()

			return False

		def SetEvent(self, func, *args) :
			result = self.eventFunc.has_key(args[0])
			if result:
				self.eventFunc[args[0]] = func
				self.eventArgs[args[0]] = args
			else:
				print "[ERROR] ui.py SetEvent, Can`t Find has_key : %s" % args[0]

		def SetBaseCheckImage(self, image):
			if not self.backgroundImage:
				return

			self.backgroundImage.LoadImage(image)

		def OnMouseLeftButtonUp(self):
			if self.checkImage:
				if self.checkImage.IsShow():
					self.checkImage.Hide()

					if self.eventFunc["ON_UNCKECK"]:
						apply(self.eventFunc["ON_UNCKECK"], self.eventArgs["ON_UNCKECK"])
				else:
					self.checkImage.Show()

					if self.eventFunc["ON_CHECK"]:
						apply(self.eventFunc["ON_CHECK"], self.eventArgs["ON_CHECK"])

RegisterToolTipWindow("TEXT", TextLine)
RegisterMultiToolTipWindow("TEXT", MultiTextLine)

class SimplyWindow(Window):
	def __init__(self, layer, flags, width, height, initializeMethod = None, destroyMethod = None):
		Window.__init__(self, layer)
		self.children		= {}
		self.windowConfig	= {
			"size"	:	{
				"width"		:	width,
				"height"	:	height
			},
			"flag"	:	flags,
		}

		if destroyMethod:
			self.destroyMethod = __mem_func__(destroyMethod)

		if initializeMethod:
			self.Initialize(__mem_func__(initializeMethod))

	def __del__(self):
		Window.__del__(self)

	def AppendObject(self, key, child, multiply = False):
		parent = self.children.get(key, None)

		if isinstance(parent, (list, tuple)) and parent != None:
			self.children[key].append(child)
		else:
			if multiply == True:
				self.children[key] = [child]
			else:
				self.children[key] = child

	def DeleteObject(self, key):
		if key in self.children:
			del self.children[key]

	def GetObject(self, key, index = -1):
		child = self.children.get(key, None)

		if not child:
			return None

		if isinstance(child, (tuple, list)):
			if index != -1:
				return child[index]
			return child
		elif index != -1:
			return proxy(child[index])
		else:
			return proxy(child)

	def GetCountObject(self, key):
		try:
			return len(self.children.get(key, None))
		except (KeyError, TypeError):
			return 0

	def Initialize(self, initializeMethod):
		self.SetSize(self.windowConfig["size"]["width"], self.windowConfig["size"]["height"])
		map(self.AddFlag, self.windowConfig["flag"])
		self.SetCenterPosition()

		try:
			initializeMethod()
			return True
		except (Exception, ) as error:
			return self.PrintException(error)

	def PrintException(self, error):
		import exception
		exception.Abort(" ")

		self.Destroy()
		self.Close()
		return False

	def GetSize(self):
		return (self.GetWidth(), self.GetHeight(), )

	def Destroy(self):
		if hasattr(self, "destroyMethod"):
			self.destroyMethod()

		self.children = {}
		self.destroyMethod = None

	def Open(self):
		self.SetTop()
		self.Show()

	def Close(self):
		self.Hide()

	def OpenWindow(self):
		self.Close() if self.IsShow() == True else self.Open()

	def OnPressExitKey(self):
		self.Close()
		return True

	OnPressEscapeKey = OnPressExitKey

if app.ENABLE_RENDER_TARGET_EXTENSION:
	class RenderTarget(Window):
		def __init__(self, layer = "UI"):
			Window.__init__(self, layer)

			self.hair = 0
			self.weapon = 0
			self.armor = 0
			self.sash = 0

		def __del__(self):
			Window.__del__(self)

		def Destroy(self):
			wndMgr.RT_DestroyRender(self.hWnd)
			Window.Destroy(self)

		def RegisterWindow(self, layer):
			self.hWnd = wndMgr.RegisterRenderTarget(self, layer)

		def LoadImage(self, imageName):
			wndMgr.RT_LoadImage(self.hWnd, imageName)

		def SetRenderTarget(self, race):
			wndMgr.RT_SetRenderTarget(self.hWnd, race)

		def DestroyRender(self):
			wndMgr.RT_DestroyRender(self.hWnd)

		def SetHair(self, vnum):
			wndMgr.RT_SetRenderHair(self.hWnd, vnum)
			self.hair = vnum

		def GetHair(self):
			return self.hair

		def SetArmor(self, vnum):
			wndMgr.RT_SetRenderArmor(self.hWnd, vnum)
			self.armor = vnum

		def GetArmor(self):
			return self.armor

		def SetWeapon(self, vnum):
			wndMgr.RT_SetRenderWeapon(self.hWnd, vnum)
			self.weapon = vnum

		def GetWeapon(self):
			return self.weapon

		def SetSash(self, vnum):
			wndMgr.RT_SetRenderSash(self.hWnd, vnum)
			self.sash = vnum

		def GetAcce(self):
			return self.sash

		def SetToggleShining(self, *flags):
			wndMgr.RT_SetRenderToggleShining(self.hWnd, *flags)

		def SetMotion(self, vnum):
			wndMgr.RT_SetRenderMotion(self.hWnd, vnum)

		def SetRenderDistance(self, value):
			wndMgr.RT_SetRenderDistance(self.hWnd, value)

		def GetRenderDistance(self):
			return wndMgr.RT_GetRenderDistance(self.hWnd)

		def SetRotation(self, rotation):
			wndMgr.RT_SetRotation(self.hWnd, rotation)

		def GetRotation(self):
			return wndMgr.RT_SetRotation(self.hWnd)

		def SetRotationMode(self, rotation):
			wndMgr.RT_SetRotationMode(self.hWnd, rotation)

		def SetLightPosition(self, x, y, z):
			wndMgr.RT_SetLightPosition(self.hWnd, x, y, z)

		def GetLightPosition(self):
			return wndMgr.RT_GetLightPosition(self.hWnd)

	class RenderTargetManager:

		MAX_TARGET_NUM = 250

		def	__init__(self):
			self.dTargetElements = dict()

		def	__del__(self):
			self.dTargetElements = dict()

		def	AddNewElement(self, parent, lSize = (0, 0), lPosition = (0, 0)):
			iKey = -1
			for i in xrange(1, self.MAX_TARGET_NUM):
				if not i in self.dTargetElements:
					iKey = i
					break

			if iKey < 0:
				print "No more key is to be assigned!"
				return (-1, None)

			if lSize == (0, 0): ## If size is 0, assuming we need to pickup parent size
				lSize = (parent.GetWidth(), parent.GetHeight())

			self.dTargetElements[iKey] = RenderTarget()
			self.dTargetElements[iKey].SetParent(parent)
			self.dTargetElements[iKey].SetSize(*lSize)
			self.dTargetElements[iKey].SetPosition(*lPosition)
			# self.dTargetElements[iKey].SetRenderTarget(iKey)
			# self.dTargetElements[iKey].SetBackground()
			self.dTargetElements[iKey].Show()

			return (iKey, self.dTargetElements[iKey])

		def	DeleteElement(self, iKey):
			if not iKey in self.dTargetElements:
				print "Key not found"
				return

			self.dTargetElements[iKey].Hide()
			del self.dTargetElements[iKey]

class NewScrollBarItemShop(Window):
	def __init__(self, path, scroll_image, scroll_cursor_image):
		Window.__init__(self)
		self.mPos = 0.0
		self.eventScroll = lambda *arg: None
		self.disable = False
		self.__LoadWindow(path, scroll_image, scroll_cursor_image)

	def __del__(self):
		Window.__del__(self)

	def Destroy(self):
		self.mPos = 0.0
		self.eventScroll = None
		self.disable = False

	def	__LoadWindow(self, path, scroll_image, scroll_cursor_image):
		## ScrollBarBase
		self.ScrollBarBase = ExpandedImageBox()
		self.ScrollBarBase.SetParent(self)
		self.ScrollBarBase.SetPosition(0, 0)
		self.ScrollBarBase.LoadImage(path+scroll_image)
		self.ScrollBarBase.SetClickEvent(self.__OnMove_Base)
		self.ScrollBarBase.Show()

		## Size
		self.SetSize(self.ScrollBarBase.GetWidth(), self.ScrollBarBase.GetHeight())

		## ScrollCursor
		self.ScrollCursor = DragButton()
		self.ScrollCursor.SetParent(self)
		self.ScrollCursor.SetPosition(0, 0)
		self.ScrollCursor.SetUpVisual(path+scroll_cursor_image)
		self.ScrollCursor.SetOverVisual(path+scroll_cursor_image)
		self.ScrollCursor.SetDownVisual(path+scroll_cursor_image)
		self.ScrollCursor.TurnOnCallBack()
		self.ScrollCursor.SetMoveEvent(__mem_func__(self.__OnMove))
		self.ScrollCursor.SetRestrictMovementArea(0, 0, self.ScrollCursor.GetWidth(), self.GetHeight())
		self.ScrollCursor.Show()

	def SetScrollEvent(self, event):
		self.eventScroll = event

	def	SetPos(self, pos):
		if self.disable:
			return

		self.mPos = pos
		self.__OnMove_Base(0, 0)

	def GetPos(self):
		return self.mPos

	def	Display(self, bShow):
		self.ScrollCursor.Show()

	def	Disable(self):
		self.disable = True
		self.ScrollCursor.SetRestrictMovementArea(0, 0, self.ScrollCursor.GetWidth(), self.ScrollCursor.GetHeight())

	def	Enable(self):
		self.disable = False
		self.ScrollCursor.SetRestrictMovementArea(0, 0, self.ScrollCursor.GetWidth(), self.GetHeight())

	def	__OnMove_Base(self, x_f = -1, y_f = -1):
		if x_f == -1 and y_f == -1:
			(x, y) = self.GetMouseLocalPosition()
		else:
			(x, y) = (x_f, y_f)

		self.__OnMove()
		self.ScrollCursor.SetPosition(0, min(y, self.GetHeight()-self.ScrollCursor.GetHeight()))

	def	__OnMove(self):
		if self.disable:
			return

		(x, y) = self.GetMouseLocalPosition()
		self.mPos = float(min(max(0, y), self.GetHeight()))/float(self.GetHeight())
		self.eventScroll()

	## ScrollBar Wheel Support
	def OnWheelMove(self, iLen):
		if self.disable:
			return

		y = self.ScrollCursor.GetHeight()
		## Computing mouse move range (by percent)
		iLen = (float(abs(iLen)-100)/100.0)*(iLen/abs(iLen))

		## Mouse Inversion
		iLen *= -1

		## Recomputation
		self.mPos += iLen
		self.mPos = float(min(max(0.0, self.mPos), 1.0))

		## Scroll Cursor pos
		self.ScrollCursor.SetPosition(0, max(0, min(self.mPos*(self.GetHeight()-self.ScrollCursor.GetHeight()), self.GetHeight()-self.ScrollCursor.GetHeight())))

		self.eventScroll()
		return True

