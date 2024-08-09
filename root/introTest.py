from weakref import proxy
from introinterface import GetAssets
import ui
import app
import wndMgr
import grp
import localeInfo
import item
import dbg
import nonplayer
import re

import uiToolTip

import utility
import math
import colorInfo

import uiScriptLocale

import nonplayer

from ui_event import MakeEvent, Event, MakeCallback

import ItemWrapper

TEST_ACTIVE = False
ENABLE_RELOADING = True
SHOW_OUTLINE = False
NEED_LOCALE_DATA = True

# UISCRIPT_FILE = "pack/uiscript/uiscript/legendary_stones_crafting_stones.py"
# UISCRIPT_FILE = "uiscript/loginwindow.py"
# UISCRIPT_FILE = "locale/common/ui/dragonsoulwindow.py"
UISCRIPT_FILE = "work/loginwindow.py"
INTERVAL = 0.5

class IntroTest(ui.Bar):
	__lastUpdate = 0
	__testWindow = None

	def __init__(self):
		ui.Bar.__init__(self)

		import wndMgr
		wndMgr.SetOutlineFlag(SHOW_OUTLINE)

		if NEED_LOCALE_DATA:
			localeInfo.LoadLocaleData()

		self.SetPosition(0, 0)
		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		self.SetColor(0xff333333)

		# import uiMobTracker
		# self.__testWindow = uiMobTracker.MobTrackerClass()
		# self.__testWindow.Show()

		self.__testWindow = ScriptManager()
		self.__testWindow.Show()

	def __del__(self):
		ui.Bar.__del__(self)

	def OnUpdate(self):
		if not ENABLE_RELOADING:
			return

		if app.GetTime() < (self.__lastUpdate + INTERVAL):
			return

		self.__lastUpdate = app.GetTime()

		if self.__testWindow:
			del self.__testWindow

		# import uiLegendaryStones
		# import uiBiologSystem
		# self.__testWindow = uiBiologSystem.BiologSets()
		# self.__testWindow.Show()

		self.__testWindow = ScriptManager()

	def OnPressEscapeKey(self):
		app.Exit()


class ScriptManager(ui.ScriptWindow):
	CONFIGURATION = dict()

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Objects = {}

		ui.PythonScriptLoader().LoadScriptFile(self, UISCRIPT_FILE)

		self.Objects["ToolTip"] = uiToolTip.ToolTip()

		# self.GetChild("HandSwitcher-ItemSpace").HideSlotBaseImage(1)
		# self.GetChild("HandSwitcher-ItemSpace").HideSlotBaseImage(2)

		self.Show()
