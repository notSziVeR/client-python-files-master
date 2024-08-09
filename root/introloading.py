# -*- coding: iso-8859-1 -*-
import ui
import uiScriptLocale
import net
import app
import dbg
import background
import chrmgr
import colorInfo
import playerSettingModule
import emotion
import localeInfo
import constInfo
import wndMgr

class LoadingWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, self)

		from _weakref import proxy
		self.stream = proxy(stream)

	def __del__(self):
		ui.Window.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_LOAD, None)

	def Open(self):
		net.SendSelectCharacterPacket( self.stream.GetCharacterSlot() )
		app.SetFrameSkip(1)

		if  constInfo.SHOW_INTROLOADING:
			constInfo.SHOW_INTROLOADING = False

		else:
			self.Close()
			return

		pyScrLoader = ui.PythonScriptLoader()
		pyScrLoader.LoadScriptFile(self, "uiscript/LoadingWindow.py")

		self.stream.LoadingImage.SetParent( self )
		self.stream.LoadingImage.SetWindowHorizontalAlignCenter()
		self.stream.LoadingImage.SetWindowVerticalAlignCenter()
		self.stream.LoadingImage.Show()

		if wndMgr.GetScreenHeight() > self.GetChild("background").GetHeight():
			self.GetChild("background").SetScale(
				1.0,
				float(wndMgr.GetScreenHeight()) / float(self.GetChild("background").GetHeight())
			)
			self.GetChild("background").SetSize(
				self.GetChild("background").GetWidth(),
				wndMgr.GetScreenHeight()
			)
			self.GetChild("background").SetWindowVerticalAlignCenter()

		self.Show()

	def Close(self):
		self.ClearDictionary()
		self.Hide()

		app.SetFrameSkip(0)

	@staticmethod
	def RegisterTitleName():
		chrmgr.RegisterTitleName( *localeInfo.TITLE_NAME_LIST )

		chrmgr.RegisterNameColor({
			chrmgr.NAMECOLOR_PC : colorInfo.CHR_NAME_RGB_PC,
			chrmgr.NAMECOLOR_NPC : colorInfo.CHR_NAME_RGB_NPC,
			chrmgr.NAMECOLOR_MOB : colorInfo.CHR_NAME_RGB_MOB,

			chrmgr.NAMECOLOR_PVP : colorInfo.CHR_NAME_RGB_PVP,
			chrmgr.NAMECOLOR_PK : colorInfo.CHR_NAME_RGB_PK,
			chrmgr.NAMECOLOR_PARTY : colorInfo.CHR_NAME_RGB_PARTY,
			chrmgr.NAMECOLOR_WARP : colorInfo.CHR_NAME_RGB_WARP,
			chrmgr.NAMECOLOR_WAYPOINT : colorInfo.CHR_NAME_RGB_WAYPOINT,
			chrmgr.NAMECOLOR_METIN : colorInfo.CHR_NAME_RGB_METIN,

			chrmgr.NAMECOLOR_EMPIRE_MOB : colorInfo.CHR_NAME_RGB_EMPIRE_MOB,
			chrmgr.NAMECOLOR_EMPIRE_NPC : colorInfo.CHR_NAME_RGB_EMPIRE_NPC,
			chrmgr.NAMECOLOR_EMPIRE_PC + 1 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_A,
			chrmgr.NAMECOLOR_EMPIRE_PC + 2 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_B,
			chrmgr.NAMECOLOR_EMPIRE_PC + 3 : colorInfo.CHR_NAME_RGB_EMPIRE_PC_C,
		})

		TITLE_COLOR_DICT = (	
			colorInfo.TITLE_RGB_GOOD_4,
			colorInfo.TITLE_RGB_GOOD_3,
			colorInfo.TITLE_RGB_GOOD_2,
			colorInfo.TITLE_RGB_GOOD_1,
			colorInfo.TITLE_RGB_NORMAL,
			colorInfo.TITLE_RGB_EVIL_1,
			colorInfo.TITLE_RGB_EVIL_2,
			colorInfo.TITLE_RGB_EVIL_3,
			colorInfo.TITLE_RGB_EVIL_4
		)

		chrmgr.RegisterTitleColor(*TITLE_COLOR_DICT)
