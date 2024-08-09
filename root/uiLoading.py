#!/usr/bin/python
#-*- coding: iso-8859-1 -*-
import ui
import wndMgr
import net
import app
import uiScriptLocale

from _weakref import proxy

class LoadingWindow(ui.SimplyWindow):
	def __init__(self, *args, **kwargs):
		ui.SimplyWindow.__init__(self, "CURTAIN", ("not_pick", ), wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight(), self.__Initialize, self.__Destroy)

		image = args[0]
		image.SetParent( self.GetObject("bar") )
		image.SetPosition(0, 0)
		image.SetWindowHorizontalAlignCenter()
		image.SetWindowVerticalAlignCenter()
		image.Show()

		self.ani = proxy(image)

	def __del__(self, *args, **kwargs):
		ui.SimplyWindow.__del__(self)

	def __Initialize(self):
		self.windowConfig["user-defines"] = {}

		bar = ui.Bar()
		bar.SetParent(self)
		bar.SetPosition(0, 0)
		bar.SetSize(self.GetWidth(), self.GetHeight())
		bar.SetColor(0xCA000000)
		bar.Show()
		
		self.AppendObject("bar", bar)
		self.closeEvent = None

	def __Destroy(self):
		self.closeEvent = None

	def SetCloseEvent(self, event):
		self.closeEvent = event

	def Close(self):
		self.ani.ResetFrame()
		self.Hide()
		return True

	def Close_(self):
		self.closeEvent()
		self.Close()

		return True

	def Open(self):
		self.ani.ResetFrame()

		self.SetTop()
		self.Show()

	OnPressEscapeKey = OnPressExitKey = Close_
