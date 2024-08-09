#-*- coding: iso-8859-1 -*-
from introinterface import gcGetEnable
import os
import app
import dbg
import grp
import item
import background
import chr
import chrmgr
import player
import snd
import chat
import textTail
import snd
import net
import effect
from uiHandSwitcher import HandSwitcherClass
import wndMgr
import fly
import systemSetting
import quest
import guild
import skill
import messenger
import localeInfo
import constInfo
import exchange
import ime

import ui
import uiCommon
import uiPhaseCurtain
import uiMapNameShower
import uiAffectShower
import uiPlayerGauge
import uiCharacter
import uiTarget

# PRIVATE_SHOP_PRICE_LIST
import uiPrivateShopBuilder
# END_OF_PRIVATE_SHOP_PRICE_LIST

import mouseModule
import consoleModule
import localeInfo

import playerSettingModule
import interfaceModule

import musicInfo
import debugInfo
import stringCommander

import uiToolTip

import introInterface

from _weakref import proxy

# SCREENSHOT_CWDSAVE
SCREENSHOT_CWDSAVE = True
SCREENSHOT_DIR = None

cameraDistance = 1550.0
cameraPitch = 27.0
cameraRotation = 0.0
cameraHeight = 100.0

testAlignment = 0
if app.ENABLE_EMOJI_SYSTEM:
	import emoticon

if app.ENABLE_GAYA_SYSTEM:
	import uiGayaSystem

if gcGetEnable("EVENT_MANAGER_ENABLE"):
	import uiEventManager

if gcGetEnable("ENABLE_TECHNICAL_MAINTENANCE"):
	import uitechnicalmaintenance

if gcGetEnable("ENABLE_NOTIFICATON_SENDER"):
	import uigmidleinterface

if gcGetEnable("ENABLE_REFACTORED_OPTIONS"):
	import cfg
	import uiRefactoredOptions

if app.ZUO_PANEL_ENABLE:
	import uizuopaneldialog

if app.SHIP_DEFEND_DUNGEON:
	import uishipdefenddungeon

if app.OX_EVENT_SYSTEM_ENABLE:
	import uioxdialog

if app.SASH_ABSORPTION_ENABLE:
	import uisashsystem

if gcGetEnable("ENABLE_NEW_LOGS_CHAT"):
	import uiLogsChat

if gcGetEnable("ENABLE_ADMIN_BAN_PANEL"):
	import uibanpanel

if gcGetEnable("ENABLE_DUNGEON_TASK_INFORMATION"):
	import uiDungeonTask

if (gcGetEnable("POPUP_SYSTEM_ENABLE")):
	import uiPopupSystem
	
if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	import uiPrivateShop

import uiDiscardItemWindow

import uiexchange
import time

class GameWindow(ui.ScriptWindow):
	def __init__(self, stream):
		ui.ScriptWindow.__init__(self, "GAME")
		self.SetWindowName("game")
		net.SetPhaseWindow(net.PHASE_WINDOW_GAME, self)
		player.SetGameWindow(self)

		self.quickSlotPageIndex = 0
		self.lastPKModeSendedTime = 0
		self.pressNumber = None

		self.guildWarQuestionDialog = None
		self.interface = None
		self.targetBoard = None
		self.console = None
		self.mapNameShower = None
		self.affectShower = None
		self.playerGauge = None

		self.stream=stream

		self.interface = interfaceModule.Interface()
		interfaceModule.SetInstance(self.interface)
		self.interface.BindMainGamePhaseWindow( self )
		self.interface.MakeInterface()
		self.interface.ShowDefaultWindows()

		self.curtain = uiPhaseCurtain.PhaseCurtain()
		self.curtain.speed = 0.03
		self.curtain.Hide()

		self.targetBoard = uiTarget.TargetBoard(self.interface)
		self.targetBoard.SetWhisperEvent(ui.__mem_func__(self.interface.OpenWhisperDialog))
		self.targetBoard.Hide()

		self.console = consoleModule.ConsoleWindow()
		self.console.BindGameClass(self)
		self.console.SetConsoleSize(wndMgr.GetScreenWidth(), 200)
		self.console.Hide()

		self.mapNameShower = uiMapNameShower.MapNameShower()
		self.affectShower = uiAffectShower.AffectShower()

		self.playerGauge = uiPlayerGauge.PlayerGauge(self)
		self.playerGauge.Hide()

		import queueManager
		self.queue = queueManager.Queue()

		self.itemDropQuestionDialog = None

		self.__toggleRidingLastActionTime = 0

		self.__SetQuickSlotMode()

		self.__ServerCommand_Build()
		self.__ProcessPreservedServerCommand()

		if app.ENABLE_EMOJI_SYSTEM:
			emoticon.LoadEmoticonConfig("locale/common/emoticon_settings.txt")

		if app.ENABLE_GAYA_SYSTEM:
			self.uigayasystem = {}
			self.uigayasystem["CRAFTING"] = uiGayaSystem.GayaCrafting()
			self.uigayasystem["MARKET"] = uiGayaSystem.GayaMarket()

		if gcGetEnable("EVENT_MANAGER_ENABLE"):
			self.uieventmanager_panel = uiEventManager.EventManager()
			self.uieventmanager = uiEventManager.EventLayer()

		if app.ENABLE_VOICE_CHAT:
			if self.interface.wVoiceChat:
				self.interface.wVoiceChat.run()

		if gcGetEnable("ENABLE_TECHNICAL_MAINTENANCE"):
			self.uitechnicalmaintenance = {}
			self.uitechnicalmaintenance["PANEL"] = uitechnicalmaintenance.Maintenance_Panel()
			self.uitechnicalmaintenance["ALERT"] = uitechnicalmaintenance.Maintenance_Alert()

		if gcGetEnable("ENABLE_NOTIFICATON_SENDER"):
			self.uigmidleinterface = {}
			self.uigmidleinterface["PANEL"] = uigmidleinterface.GMIdlePanel()
			self.uigmidleinterface["ANSWER"] = uigmidleinterface.IdlePanelAnswer()

		if app.ZUO_PANEL_ENABLE:
			self.uizuopaneldialog = uizuopaneldialog.ZuoEventDialog()

		if app.SHIP_DEFEND_DUNGEON:
			self.uishipdefenddungeon = uishipdefenddungeon.ShipDungeonAllie()

		if gcGetEnable("ENABLE_LOCK_EFFECTS"):
			self.ttExchangeEffect = (0, 0)

		if app.ENABLE_CUBE_RENEWAL:
			self.craftFailPopupDialog = uiCommon.PopupDialog()
			self.craftFailPopupDialog.Hide()

		if app.OX_EVENT_SYSTEM_ENABLE:
			self.uioxdialog = uioxdialog.OxEventDialog()

		if app.SASH_ABSORPTION_ENABLE:
			self.uisashsystem = {}
			self.uisashsystem["COMBINATION"] = uisashsystem.SashCombination()
			self.uisashsystem["ABSORPTION"] = uisashsystem.SashAbsorption()

		if gcGetEnable("ENABLE_ADMIN_BAN_PANEL"):
			self.uibanpanel = uibanpanel.BanPanel()

		if gcGetEnable("ENABLE_DUNGEON_TASK_INFORMATION"):
			self.uiDungeonTask = uiDungeonTask.DungeonTaskWindow()
			self.uiDungeonTask.SetPosition(self.interface.wndMiniMap.GetGlobalPosition()[0] - self.uiDungeonTask.GetWidth() + 25, 12)

		if (gcGetEnable("POPUP_SYSTEM_ENABLE")):
			self.uiPopupSystem = uiPopupSystem.PopupSystemInterface()

	def __del__(self):
		player.ClearGameWindow(self)
		net.ClearPhaseWindow(net.PHASE_WINDOW_GAME, self)
		ui.ScriptWindow.__del__(self)

	def Open(self):
		app.SetFrameSkip(1)

		self.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())

		self.quickSlotPageIndex = 0
		self.PickingCharacterIndex = -1
		self.PickingItemIndex = -1
		self.consoleEnable = False
		self.isShowDebugInfo = False
		self.ShowNameFlag = False

		self.enableXMasBoom = False
		self.startTimeXMasBoom = 0.0
		self.indexXMasBoom = 0

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight

		if gcGetEnable("ENABLE_REFACTORED_OPTIONS"):
			actualCameraDistance = cfg.Get(cfg.SAVE_OPTION, "DISTANCE", str(uiRefactoredOptions.CAMERA_MAX_DISTANCE))
			app.SetCameraMaxDistance(float(actualCameraDistance))
			app.SetCamera(cameraDistance, cameraPitch, cameraRotation, cameraHeight)

			actualEnv = cfg.Get(cfg.SAVE_OPTION, "ENV_MODE", "0")
			if actualEnv == "1":
				background.RegisterEnvironmentData(1, uiRefactoredOptions.ENVIRONMENT_NIGHT)
				background.SetEnvironmentData(1)
			else:
				background.SetEnvironmentData(0)

			actualFog = cfg.Get(cfg.SAVE_OPTION, "FOG_MODE", "0")
			if actualFog == "0":
				background.SetEnvironmentFog(True)
			else:
				background.SetEnvironmentFog(False)

		else:
			constInfo.SET_DEFAULT_CAMERA_MAX_DISTANCE()

		constInfo.SET_DEFAULT_CHRNAME_COLOR()
		constInfo.SET_DEFAULT_FOG_LEVEL()
		constInfo.SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE()
		constInfo.SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS()
		constInfo.SET_DEFAULT_USE_SKILL_EFFECT_ENABLE()

		# TWO_HANDED_WEAPON_ATTACK_SPEED_UP
		constInfo.SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE()
		# END_OF_TWO_HANDED_WEAPON_ATTACK_SPEED_UP

		import event
		event.SetLeftTimeString(localeInfo.UI_LEFT_TIME)

		textTail.EnablePKTitle(constInfo.PVPMODE_ENABLE)

		if constInfo.PVPMODE_TEST_ENABLE:
			self.testPKMode = ui.TextLine()
			self.testPKMode.SetFontName(localeInfo.UI_DEF_FONT)
			self.testPKMode.SetPosition(0, 15)
			self.testPKMode.SetWindowHorizontalAlignCenter()
			self.testPKMode.SetHorizontalAlignCenter()
			self.testPKMode.SetFeather()
			self.testPKMode.SetOutline()
			self.testPKMode.Show()

			self.testAlignment = ui.TextLine()
			self.testAlignment.SetFontName(localeInfo.UI_DEF_FONT)
			self.testAlignment.SetPosition(0, 35)
			self.testAlignment.SetWindowHorizontalAlignCenter()
			self.testAlignment.SetHorizontalAlignCenter()
			self.testAlignment.SetFeather()
			self.testAlignment.SetOutline()
			self.testAlignment.Show()

		self.__BuildKeyDict()
		self.__BuildDebugInfo()

		# PRIVATE_SHOP_PRICE_LIST
		uiPrivateShopBuilder.Clear()
		# END_OF_PRIVATE_SHOP_PRICE_LIST

		# UNKNOWN_UPDATE
		exchange.InitTrading()
		# END_OF_UNKNOWN_UPDATE

		## Sound
		snd.SetMusicVolume(systemSetting.GetMusicVolume()*net.GetFieldMusicVolume())
		snd.SetSoundVolume(systemSetting.GetSoundVolume())

		netFieldMusicFileName = net.GetFieldMusicFileName()
		if netFieldMusicFileName:
			snd.FadeInMusic("BGM/" + netFieldMusicFileName)
		elif musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		self.__SetQuickSlotMode()
		self.__SelectQuickPage(self.quickSlotPageIndex)

		self.SetFocus()
		self.Show()
		app.ShowCursor()

		net.SendEnterGamePacket()

		# START_GAME_ERROR_EXIT
		try:
			self.StartGame()
		except:
			import exception
			exception.Abort("GameWindow.Open")
		# END_OF_START_GAME_ERROR_EXIT

		if gcGetEnable("ENABLE_RECOVER_WHISPERS"):
			self.interface.RecoverWhispers()

		# ex) cubeInformation[20383] = [ {"rewordVNUM": 72723, "rewordCount": 1, "materialInfo": "101,1&102,2", "price": 999 }, ... ]
		self.cubeInformation = {}
		self.currentCubeNPC = 0

		if app.ENABLE_VOICE_CHAT:
			if self.interface.wVoiceChat:
				self.interface.VoiceInit()

		if app.INGAME_WIKI:
			import inGameWiki
			self.wndWiki = inGameWiki.InGameWiki()
			self.interface.dlgSystem.wikiWnd = proxy(self.wndWiki)

		if app.ENABLE_TEAMLER_STATUS:
			if player.GetName() == constInfo.SET_SHOW_TEAMLER:
				net.SendChatPacket("/set_is_show_teamler %d"  % constInfo.IS_SHOW_TEAMLER_VAL)

	def Close(self):
		self.Hide()

		global cameraDistance, cameraPitch, cameraRotation, cameraHeight
		(cameraDistance, cameraPitch, cameraRotation, cameraHeight) = app.GetCamera()

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		self.onPressKeyDict = None
		self.onClickKeyDict = None

		if gcGetEnable("ENABLE_ITEM_HIGHLIGHT_"):
			self.interface.wndInventory.EFFECT_SLOTS = dict()

		chat.Close()
		snd.StopAllSound()
		grp.InitScreenEffect()
		chr.Destroy()
		textTail.Clear()
		quest.Clear()
		background.Destroy()
		guild.Destroy()
		messenger.Destroy()
		skill.ClearSkillData()
		wndMgr.Unlock()
		mouseModule.mouseController.DeattachObject()

		if app.ENABLE_GAYA_SYSTEM:
			for wnd in self.uigayasystem.values():
				wnd.Hide()
				wnd.Destroy()

			self.uigayasystem = None

		if gcGetEnable("ENABLE_TECHNICAL_MAINTENANCE"):
			for wnd in self.uitechnicalmaintenance.values():
				wnd.Hide()
				wnd.Destroy()

		if gcGetEnable("ENABLE_NOTIFICATON_SENDER"):
			for wnd in self.uigmidleinterface.values():
				wnd.Hide()
				wnd.Destroy()

		if gcGetEnable("EVENT_MANAGER_ENABLE"):
			self.uieventmanager_panel.Clear()
			self.uieventmanager_panel.Close()
			self.uieventmanager_panel = None
			self.uieventmanager.Close()
			self.uieventmanager = None

		if app.ZUO_PANEL_ENABLE:
			self.uizuopaneldialog.Destroy()
			self.uizuopaneldialog.Close()
			self.uizuopaneldialog = None

		if app.SHIP_DEFEND_DUNGEON:
			self.uishipdefenddungeon.Hide()
			self.uishipdefenddungeon = None

		#TODO Lets check a problem with clearing slots after warping!
		if app.SASH_ABSORPTION_ENABLE:
			for wnd in self.uisashsystem.values():
				wnd.Clear()
				wnd.Hide()
				wnd.Destroy()

			self.uisashsystem = None

		if gcGetEnable("ENABLE_ADMIN_BAN_PANEL"):
			del self.uibanpanel
			self.uibanpanel = None

		if self.guildWarQuestionDialog:
			self.guildWarQuestionDialog.Close()

		self.guildNameBoard = None
		self.partyRequestQuestionDialog = None
		self.partyInviteQuestionDialog = None
		self.guildInviteQuestionDialog = None
		self.guildWarQuestionDialog = None
		self.messengerAddFriendQuestion = None

		# UNKNOWN_UPDATE
		self.itemDropQuestionDialog = None
		# END_OF_UNKNOWN_UPDATE

		# QUEST_CONFIRM
		self.confirmDialog = None
		# END_OF_QUEST_CONFIRM

		self.PrintCoord = None
		self.FrameRate = None
		self.Pitch = None
		self.Splat = None
		self.TextureNum = None
		self.ObjectNum = None
		self.ViewDistance = None
		self.PrintMousePos = None

		self.ClearDictionary()

		self.playerGauge = None
		self.mapNameShower = None
		self.affectShower = None

		if self.console:
			self.console.BindGameClass(0)
			self.console.Close()
			self.console=None

		if self.targetBoard:
			self.targetBoard.Hide()
			self.targetBoard.Destroy()
			self.targetBoard = None

		if self.interface:
			self.interface.HideAllWindows()
			self.interface.Close()
			del self.interface
			self.interface=None

		if gcGetEnable("ENABLE_LOCK_EFFECTS"):
			self.ttExchangeEffect = (0, 0)

		if app.ENABLE_CUBE_RENEWAL:
			if self.craftFailPopupDialog:
				self.craftFailPopupDialog.Destroy()

		if app.OX_EVENT_SYSTEM_ENABLE:
			self.uioxdialog.Close()
			self.uioxdialog.Destroy()
			self.uioxdialog = None

		if gcGetEnable("ENABLE_DUNGEON_TASK_INFORMATION"):
			if self.uiDungeonTask:
				self.uiDungeonTask.Hide()
				self.uiDungeonTask.Destroy()
				self.uiDungeonTask = None

		interfaceModule.SetInstance(None)

		if self.affectShower:
			self.affectShower.ClearAllAffects()

		player.ClearSkillDict()
		player.ResetCameraRotation()

		if app.INGAME_WIKI:
			if self.wndWiki:
				self.wndWiki.Hide()
				self.wndWiki = None

		self.KillFocus()
		app.HideCursor()

		print "---------------------------------------------------------------------------- CLOSE GAME WINDOW"

	def __BuildKeyDict(self):
		onPressKeyDict = {}


		onPressKeyDict[app.DIK_1]	= lambda : self.__PressNumKey(1)
		onPressKeyDict[app.DIK_2]	= lambda : self.__PressNumKey(2)
		onPressKeyDict[app.DIK_3]	= lambda : self.__PressNumKey(3)
		onPressKeyDict[app.DIK_4]	= lambda : self.__PressNumKey(4)
		onPressKeyDict[app.DIK_5]	= lambda : self.__PressNumKey(5)
		onPressKeyDict[app.DIK_6]	= lambda : self.__PressNumKey(6)
		onPressKeyDict[app.DIK_7]	= lambda : self.__PressNumKey(7)
		onPressKeyDict[app.DIK_8]	= lambda : self.__PressNumKey(8)
		onPressKeyDict[app.DIK_9]	= lambda : self.__PressNumKey(9)
		onPressKeyDict[app.DIK_F1]	= lambda : self.__PressQuickSlot(4)
		onPressKeyDict[app.DIK_F2]	= lambda : self.__PressQuickSlot(5)
		onPressKeyDict[app.DIK_F3]	= lambda : self.__PressQuickSlot(6)
		onPressKeyDict[app.DIK_F4]	= lambda : self.__PressQuickSlot(7)

		if gcGetEnable("ENABLE_DUNGEON_INFORMATION"):
			onPressKeyDict[app.DIK_F5]	= lambda : self.__DUNGEON_INFO__OpenPanel()

		if app.ENABLE_SAVE_POSITIONS_SYSTEM:
			onPressKeyDict[app.DIK_F6]	= lambda : self.interface.PositionManager_ToggleWindow()

		if app.ENABLE_SWITCHBOT:
			onPressKeyDict[app.DIK_F7] = lambda : self.interface.ToggleSwitchbotWindow()

		# onPressKeyDict[app.DIK_F8]	= lambda state = "on": self.Progress(state)
		# onPressKeyDict[app.DIK_F9]	= lambda state = "off": self.Progress(state)

		if app.ENABLE_TELEPORT_SYSTEM:
			onPressKeyDict[app.DIK_TAB]	= lambda : self.__ToggleTeleportSystem()

		onPressKeyDict[app.DIK_LALT]		= lambda : self.ShowName()
		onPressKeyDict[app.DIK_LCONTROL]	= lambda : self.ShowMouseImage()
		onPressKeyDict[app.DIK_SYSRQ]		= lambda : self.SaveScreen()
		onPressKeyDict[app.DIK_SPACE]		= lambda : self.StartAttack()

		onPressKeyDict[app.DIK_UP]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_DOWN]		= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_LEFT]		= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_RIGHT]		= lambda : self.MoveRight()
		onPressKeyDict[app.DIK_W]			= lambda : self.MoveUp()
		onPressKeyDict[app.DIK_S]			= lambda : self.MoveDown()
		onPressKeyDict[app.DIK_A]			= lambda : self.MoveLeft()
		onPressKeyDict[app.DIK_D]			= lambda : self.MoveRight()

		onPressKeyDict[app.DIK_E]			= lambda: app.RotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_R]			= lambda: app.ZoomCamera(app.CAMERA_TO_NEGATIVE)
		#onPressKeyDict[app.DIK_F]			= lambda: app.ZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_T]			= lambda: app.PitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_G]			= self.__PressGKey
		onPressKeyDict[app.DIK_Q]			= self.__PressQKey

		onPressKeyDict[app.DIK_NUMPAD9]		= lambda: app.MovieResetCamera()
		onPressKeyDict[app.DIK_NUMPAD4]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD6]		= lambda: app.MovieRotateCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_PGUP]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_PGDN]		= lambda: app.MovieZoomCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_NUMPAD8]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_NEGATIVE)
		onPressKeyDict[app.DIK_NUMPAD2]		= lambda: app.MoviePitchCamera(app.CAMERA_TO_POSITIVE)
		onPressKeyDict[app.DIK_GRAVE]		= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_Z]			= lambda : self.PickUpItem()
		onPressKeyDict[app.DIK_C]			= lambda state = "STATUS": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_V]			= lambda state = "SKILL": self.interface.ToggleCharacterWindow(state)
		#onPressKeyDict[app.DIK_B]			= lambda state = "EMOTICON": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_N]			= lambda state = "QUEST": self.interface.ToggleCharacterWindow(state)
		onPressKeyDict[app.DIK_I]			= lambda : self.interface.ToggleInventoryWindow()
		onPressKeyDict[app.DIK_O]			= lambda : self.__PressOKey()
		onPressKeyDict[app.DIK_M]			= lambda : self.interface.PressMKey()
		#onPressKeyDict[app.DIK_H]			= lambda : self.interface.OpenHelpWindow()
		onPressKeyDict[app.DIK_ADD]			= lambda : self.interface.MiniMapScaleUp()
		onPressKeyDict[app.DIK_SUBTRACT]	= lambda : self.interface.MiniMapScaleDown()
		onPressKeyDict[app.DIK_L]			= lambda : self.interface.ToggleChatLogWindow()
		# onPressKeyDict[app.DIK_COMMA]		= lambda : self.ShowConsole()		# "`" key
		onPressKeyDict[app.DIK_LSHIFT]		= lambda : self.__SetQuickPageMode()

		onPressKeyDict[app.DIK_J]			= lambda : self.__PressJKey()
		onPressKeyDict[app.DIK_H]			= lambda : self.__PressHKey()
		onPressKeyDict[app.DIK_B]			= lambda : self.__PressBKey()
		onPressKeyDict[app.DIK_F]			= lambda : self.__PressFKey()

		if app.ENABLE_SPECIAL_STORAGE:
			onPressKeyDict[app.DIK_U]		= lambda : self.interface.ToggleSpecialStorageWindow()

		if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
			onPressKeyDict[app.DIK_K]			= lambda : self.interface.ToggleMainLogsChatWindow()
			
		# if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		onPressKeyDict[app.DIK_Y]			= lambda : self.interface.TogglePrivateShopPanelWindow()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			onPressKeyDict[app.DIK_P]		= lambda : self.interface.BuffNPCOpenWindow()

		self.onPressKeyDict = onPressKeyDict

		onClickKeyDict = {}
		onClickKeyDict[app.DIK_UP] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_DOWN] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_LEFT] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_RIGHT] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_SPACE] = lambda : self.EndAttack()

		onClickKeyDict[app.DIK_W] = lambda : self.StopUp()
		onClickKeyDict[app.DIK_S] = lambda : self.StopDown()
		onClickKeyDict[app.DIK_A] = lambda : self.StopLeft()
		onClickKeyDict[app.DIK_D] = lambda : self.StopRight()
		onClickKeyDict[app.DIK_Q] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_E] = lambda: app.RotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_R] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_F] = lambda: app.ZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_T] = lambda: app.PitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_G] = lambda: self.__ReleaseGKey()
		onClickKeyDict[app.DIK_NUMPAD4] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD6] = lambda: app.MovieRotateCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGUP] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_PGDN] = lambda: app.MovieZoomCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD8] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_NUMPAD2] = lambda: app.MoviePitchCamera(app.CAMERA_STOP)
		onClickKeyDict[app.DIK_LALT] = lambda: self.HideName()
		onClickKeyDict[app.DIK_LCONTROL] = lambda: self.HideMouseImage()
		onClickKeyDict[app.DIK_LSHIFT] = lambda: self.__SetQuickSlotMode()

		#if constInfo.PVPMODE_ACCELKEY_ENABLE:
		#	onClickKeyDict[app.DIK_B] = lambda: self.ChangePKMode()

		self.onClickKeyDict=onClickKeyDict

	if app.ENABLE_TELEPORT_SYSTEM:
		def __ToggleTeleportSystem(self):
			net.SendChatPacket("/teleport_open")

	def Progress(self, state):
		# import logsChat
		import uiScalingOption

		if state == "on":
			# self.interface.OpenShamanSystem()
			# net.SendItemUsePacket(0)
			self.interface.OpenMissionManager()
			# self.interface.OpenShamanSystem()

			# if self.scaling.IsShow():
			# 	self.scaling.Close()
			# else:
			# 	self.scaling.Open()

			# if self.interface.wndLegendaryStones["STONES"].IsShow():
			# 	self.interface.wndLegendaryStones["STONES"].Close()
			# else:
			# 	self.interface.wndLegendaryStones["STONES"].Open()
		else:
			if self.interface.interfaceWindowList["mob_tracker"].IsShow():
				net.SendChatPacket("/request_tracker")
			else:
				self.interface.interfaceWindowList["mob_tracker"].Close()
			# self.interface.interfaceWindowList["attendance_manager"].Open()
			# self.interface.RegisterShamanItem(0)
			# text = "|Eaction/angry|e |Eaction/angry|e |Eaction/angry|e"
			# net.SendChatPacket(text, chat.CHAT_TYPE_SHOUT)

	def __PressNumKey(self,num):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):

			if num >= 1 and num <= 9:
				if(chrmgr.IsPossibleEmoticon(-1)):
					chrmgr.SetEmoticon(-1,int(num)-1)
					net.SendEmoticon(int(num)-1)
		else:
			if num >= 1 and num <= 4:
				self.pressNumber(num-1)

	def __PressOKey(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			# Toggle dragon soul
			self.interface.DragonSoulActivateByKey()
		else:
			self.interface.ToggleDragonSoulWindowWithNoInfo()

	def __ClickBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			return
		else:
			if constInfo.PVPMODE_ACCELKEY_ENABLE:
				self.ChangePKMode()

	def	__PressJKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if player.IsMountingHorse():
				if self.__CanToggleRiding():
					net.SendChatPacket("/unmount")
					self.__SetToggleRidingLastActionTime()
			else:
				if not uiPrivateShopBuilder.IsBuildingPrivateShop():
					for i in xrange(player.INVENTORY_PAGE_SIZE):
						if player.GetItemIndex(i) in (52043, 52044, 52045, 71164, 71165, 71166, 71167, 71168, 52091, 52092, 52093, 52094, 52095, 52096, 52097, 52098, 71161, 71131, 52033, 52005, 52019, 71176, 71177, 71173, 71161):
							net.SendItemUsePacket(i)
							break

	def	__PressHKey(self):
		if app.IsPressed(introInterface.GetWindowConfig("shortcust_items", introInterface.ITEM_RIDE_0, "key")):
			if self.__CanToggleRiding():
				net.SendChatPacket("/ride")
				self.__SetToggleRidingLastActionTime()
		else:
			if app.INGAME_WIKI:
				self.interface.ToggleWikiNew()
			else:
				self.interface.OpenHelpWindow()

	def	__PressBKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if self.__CanToggleRiding():
				net.SendChatPacket("/user_horse_back")
				self.__SetToggleRidingLastActionTime()
		else:
			state = "EMOTICON"
			self.interface.ToggleCharacterWindow(state)

	def	__PressFKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			net.SendChatPacket("/user_horse_feed")
		else:
			app.ZoomCamera(app.CAMERA_TO_POSITIVE)

	def __PressGKey(self):
		if app.IsPressed(introInterface.GetWindowConfig("shortcust_items", introInterface.ITEM_RIDE_1, "key")):
			if self.__CanToggleRiding():
				net.SendChatPacket("/ride")
				self.__SetToggleRidingLastActionTime()
		else:
			if self.ShowNameFlag:
				self.interface.ToggleGuildWindow()
			else:
				app.PitchCamera(app.CAMERA_TO_POSITIVE)

	def	__ReleaseGKey(self):
		app.PitchCamera(app.CAMERA_STOP)

	def __PressQKey(self):
		if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
			if 0==interfaceModule.IsQBHide:
				interfaceModule.IsQBHide = 1
				self.interface.HideAllQuestButton()
			else:
				interfaceModule.IsQBHide = 0
				self.interface.ShowAllQuestButton()
		else:
			app.RotateCamera(app.CAMERA_TO_NEGATIVE)

	def __CanToggleRiding(self):
		return self.__toggleRidingLastActionTime < app.GetTime()

	def __SetToggleRidingLastActionTime(self):
		self.__toggleRidingLastActionTime = app.GetTime() + 0.5

	def __SetQuickSlotMode(self):
		self.pressNumber=ui.__mem_func__(self.__PressQuickSlot)

	def __SetQuickPageMode(self):
		self.pressNumber=ui.__mem_func__(self.__SelectQuickPage)

	def __PressQuickSlot(self, localSlotIndex):
		player.RequestUseLocalQuickSlot(localSlotIndex)

	def __SelectQuickPage(self, pageIndex):
		self.quickSlotPageIndex = pageIndex
		player.SetQuickPage(pageIndex)

	def ToggleDebugInfo(self):
		self.isShowDebugInfo = not self.isShowDebugInfo

		if self.isShowDebugInfo:
			self.PrintCoord.Show()
			self.FrameRate.Show()
			self.Pitch.Show()
			self.Splat.Show()
			self.TextureNum.Show()
			self.ObjectNum.Show()
			self.ViewDistance.Show()
			self.PrintMousePos.Show()
		else:
			self.PrintCoord.Hide()
			self.FrameRate.Hide()
			self.Pitch.Hide()
			self.Splat.Hide()
			self.TextureNum.Hide()
			self.ObjectNum.Hide()
			self.ViewDistance.Hide()
			self.PrintMousePos.Hide()

	def __BuildDebugInfo(self):
		## Character Position Coordinate
		self.PrintCoord = ui.TextLine()
		self.PrintCoord.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintCoord.SetPosition(wndMgr.GetScreenWidth() - 270, 0)

		## Frame Rate
		self.FrameRate = ui.TextLine()
		self.FrameRate.SetFontName(localeInfo.UI_DEF_FONT)
		self.FrameRate.SetPosition(wndMgr.GetScreenWidth() - 270, 20)

		## Camera Pitch
		self.Pitch = ui.TextLine()
		self.Pitch.SetFontName(localeInfo.UI_DEF_FONT)
		self.Pitch.SetPosition(wndMgr.GetScreenWidth() - 270, 40)

		## Splat
		self.Splat = ui.TextLine()
		self.Splat.SetFontName(localeInfo.UI_DEF_FONT)
		self.Splat.SetPosition(wndMgr.GetScreenWidth() - 270, 60)

		##
		self.PrintMousePos = ui.TextLine()
		self.PrintMousePos.SetFontName(localeInfo.UI_DEF_FONT)
		self.PrintMousePos.SetPosition(wndMgr.GetScreenWidth() - 270, 80)

		# TextureNum
		self.TextureNum = ui.TextLine()
		self.TextureNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.TextureNum.SetPosition(wndMgr.GetScreenWidth() - 270, 100)

		self.ObjectNum = ui.TextLine()
		self.ObjectNum.SetFontName(localeInfo.UI_DEF_FONT)
		self.ObjectNum.SetPosition(wndMgr.GetScreenWidth() - 270, 120)

		self.ViewDistance = ui.TextLine()
		self.ViewDistance.SetFontName(localeInfo.UI_DEF_FONT)
		self.ViewDistance.SetPosition(0, 0)

	def __NotifyError(self, msg):
		pass
		# chat.AppendChat(chat.CHAT_TYPE_INFO, msg)

	def ChangePKMode(self):

		if not app.IsPressed(app.DIK_LCONTROL):
			return

		if player.GetStatus(player.LEVEL)<constInfo.PVPMODE_PROTECTED_LEVEL:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return

		curTime = app.GetTime()
		if curTime - self.lastPKModeSendedTime < constInfo.PVPMODE_ACCELKEY_DELAY:
			return

		self.lastPKModeSendedTime = curTime

		curPKMode = player.GetPKMode()
		nextPKMode = curPKMode + 1
		if nextPKMode == player.PK_MODE_PROTECT:
			if 0 == player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				nextPKMode = 0
			else:
				nextPKMode = player.PK_MODE_GUILD

		elif nextPKMode == player.PK_MODE_MAX_NUM:
			nextPKMode = 0

		net.SendChatPacket("/PKMode " + str(nextPKMode))
		print "/PKMode " + str(nextPKMode)

	def OnChangePKMode(self):

		self.interface.OnChangePKMode()

		try:
			self.__NotifyError(localeInfo.OPTION_PVPMODE_MESSAGE_DICT[player.GetPKMode()])
		except KeyError:
			print "UNKNOWN PVPMode[%d]" % (player.GetPKMode())

		if constInfo.PVPMODE_TEST_ENABLE:
			curPKMode = player.GetPKMode()
			alignment, grade = chr.testGetPKData()
			self.pkModeNameDict = { 0 : "PEACE", 1 : "REVENGE", 2 : "FREE", 3 : "PROTECT", }
			self.testPKMode.SetText("Current PK Mode : " + self.pkModeNameDict.get(curPKMode, "UNKNOWN"))
			self.testAlignment.SetText("Current Alignment : " + str(alignment) + " (" + localeInfo.TITLE_NAME_LIST[grade] + ")")

	###############################################################################################
	###############################################################################################
	## Game Callback Functions

	# Start
	def StartGame(self):
		self.RefreshInventory()
		self.RefreshEquipment()
		self.RefreshCharacter()
		self.RefreshSkill()

	# Refresh
	def CheckGameButton(self):
		if self.interface:
			self.interface.CheckGameButton()

	def RefreshAlignment(self):
		self.interface.RefreshAlignment()

	def RefreshStatus(self):
		self.CheckGameButton()

		if self.interface:
			self.interface.RefreshStatus()

		if self.playerGauge:
			self.playerGauge.RefreshGauge()

	def RefreshStamina(self):
		self.interface.RefreshStamina()

	def RefreshSkill(self):
		self.CheckGameButton()
		if self.interface:
			self.interface.RefreshSkill()

	def RefreshQuest(self):
		self.interface.RefreshQuest()

	def RefreshMessenger(self):
		self.interface.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.interface.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.interface.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.interface.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.interface.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.interface.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.interface.RefreshGuildGradePage()

	def RefreshMobile(self):
		if self.interface:
			self.interface.RefreshMobile()

	def OnMobileAuthority(self):
		self.interface.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.interface.OnBlockMode(mode)

	def OpenQuestWindow(self, skin, idx):
		self.interface.OpenQuestWindow(skin, idx)

	def AskGuildName(self):
		guildNameBoard = uiCommon.InputDialog()
		guildNameBoard.SetTitle(localeInfo.GUILD_NAME)
		guildNameBoard.SetAcceptEvent(ui.__mem_func__(self.ConfirmGuildName))
		guildNameBoard.SetCancelEvent(ui.__mem_func__(self.CancelGuildName))
		guildNameBoard.Open()

		self.guildNameBoard = guildNameBoard

	def ConfirmGuildName(self):
		guildName = self.guildNameBoard.GetText()
		if not guildName:
			return

		if net.IsInsultIn(guildName):
			self.PopupMessage(localeInfo.GUILD_CREATE_ERROR_INSULT_NAME)
			return

		net.SendAnswerMakeGuildPacket(guildName)
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	def CancelGuildName(self):
		self.guildNameBoard.Close()
		self.guildNameBoard = None
		return True

	## Refine
	def PopupMessage(self, msg):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, 0, localeInfo.UI_OK)

	if app.ENABLE_FAST_REFINE_OPTION:
		def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type = 0, can_fast_refine = False, addPercent = 0, bSashRefine = False):
			self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type, can_fast_refine, addPercent, bSashRefine)
	else:
		def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type=0):
			self.interface.OpenRefineDialog(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.interface.AppendMaterialToRefineDialog(vnum, count)

	def RunUseSkillEvent(self, slotIndex, coolTime):
		self.interface.OnUseSkill(slotIndex, coolTime)

	def ClearAffects(self):
		self.affectShower.ClearAffects()

	def SetAffect(self, affect):
		self.affectShower.SetAffect(affect)

	def ResetAffect(self, affect):
		self.affectShower.ResetAffect(affect)

	# UNKNOWN_UPDATE
	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		self.affectShower.BINARY_NEW_AddAffect(type, pointIdx, value, duration)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulActivate(type - chr.NEW_AFFECT_DRAGON_SOUL_DECK1)
		elif chr.NEW_AFFECT_DRAGON_SOUL_QUALIFIED == type:
			self.BINARY_DragonSoulGiveQuilification()
		elif chr.AFFECT_DS_SET == type and app.ENABLE_DS_SET:
			self.interface.DragonSoulSetActivate(value)

		if gcGetEnable("ENABLE_ANTY_EXP"):
			if type == chr.AFFECT_EXP_CURSE:
				UpdateConfig("anty_exp", "ANTY_EXP_STATUS_{}".format(player.GetName()), 1)
				self.interface.wndTaskBar.LoadNewImages()

		self.interface.RepositionGroup(self.affectShower.GetBottom())

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		self.affectShower.BINARY_NEW_RemoveAffect(type, pointIdx)
		if chr.NEW_AFFECT_DRAGON_SOUL_DECK1 == type or chr.NEW_AFFECT_DRAGON_SOUL_DECK2 == type:
			self.interface.DragonSoulDeactivate()
		elif chr.AFFECT_DS_SET == type and app.ENABLE_DS_SET:
			self.interface.DragonSoulSetDeactivate()

		if gcGetEnable("ENABLE_ANTY_EXP"):
			if type == chr.AFFECT_EXP_CURSE:
				UpdateConfig("anty_exp", "ANTY_EXP_STATUS_{}".format(player.GetName()), 0)
				self.interface.wndTaskBar.LoadNewImages()

		self.interface.RepositionGroup(self.affectShower.GetBottom())
	# END_OF_UNKNOWN_UPDATE

	def ActivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnActivateSkill(slotIndex)

	def DeactivateSkillSlot(self, slotIndex):
		if self.interface:
			self.interface.OnDeactivateSkill(slotIndex)

	def RefreshEquipment(self):
		if self.interface:
			self.interface.RefreshInventory()

	def RefreshInventory(self):
		if self.interface:
			self.interface.RefreshInventory()

		if self.affectShower:
			self.affectShower.RefreshInventory()

		if self.interface:
			self.interface.RepositionGroup(self.affectShower.GetBottom())

	def RefreshCharacter(self):
		if self.interface:
			self.interface.RefreshCharacter()

	if app.ENABLE_RENEWAL_DEAD_PACKET:
		def OnGameOver(self, d_time):
			self.CloseTargetBoard()
			self.OpenRestartDialog(d_time)
	else:
		def OnGameOver(self):
			self.CloseTargetBoard()
			self.OpenRestartDialog()

	if app.ENABLE_RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.interface.OpenRestartDialog(d_time)
	else:
		def OpenRestartDialog(self):
			self.interface.OpenRestartDialog()

	def ChangeCurrentSkill(self, skillSlotNumber):
		self.interface.OnChangeCurrentSkill(skillSlotNumber)

	## TargetBoard
	def SetPCTargetBoard(self, vid, name):
		self.targetBoard.Open(vid, name)

		if app.IsPressed(app.DIK_LCONTROL):

			if not player.IsSameEmpire(vid):
				return

			if player.IsMainCharacterIndex(vid):
				return
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(vid):
				return

			self.interface.OpenWhisperDialog(name)


	def RefreshTargetBoardByVID(self, vid):
		self.targetBoard.RefreshByVID(vid)

	def RefreshTargetBoardByName(self, name):
		self.targetBoard.RefreshByName(name)

	def __RefreshTargetBoard(self):
		self.targetBoard.Refresh()

	def SetHPTargetBoard(self, vid, hp, maxHp, isPoisoned):
		# Do not show the players HP himself
		if player.IsMainCharacterIndex(vid):
			return

		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.ResetTargetBoard()

			if chr.IsEnemy(vid) or chr.IsStone(vid):
				self.targetBoard.SetEnemyVID(vid)
			else:
				self.targetBoard.Open(vid, chr.GetNameByVID(vid))

		self.targetBoard.SetHP(hp, maxHp)
		# if gcGetEnable("ENABLE_POISON_GAUGE"):
		# 	self.targetBoard.SetPoisoned(isPoisoned)
		self.targetBoard.Show()

	def CloseTargetBoardIfDifferent(self, vid):
		if vid != self.targetBoard.GetTargetVID():
			self.targetBoard.Close()

	def CloseTargetBoard(self):
		self.targetBoard.Close()

	## View Equipment
	def OpenEquipmentDialog(self, vid):
		self.interface.OpenEquipmentDialog(vid)

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		self.interface.SetEquipmentDialogItem(vid, slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		self.interface.SetEquipmentDialogSocket(vid, slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		self.interface.SetEquipmentDialogAttr(vid, slotIndex, attrIndex, type, value)

	# SHOW_LOCAL_MAP_NAME
	def ShowMapName(self, mapName, x, y):
		if self.mapNameShower:
			self.mapNameShower.ShowMapName(mapName, x, y)

		if self.interface:
			self.interface.SetMapName(mapName)
	# END_OF_SHOW_LOCAL_MAP_NAME

	def BINARY_OpenAtlasWindow(self):
		self.interface.BINARY_OpenAtlasWindow()

	## Chat
	if app.OFFLINE_MESSAGE_ENABLE:
		def OnRecvWhisper(self, mode, name, iLocale, line, offline_whisper = 0):
			if mode == chat.WHISPER_TYPE_GM:
				self.interface.RegisterGameMasterName(name)
			chat.AppendWhisper(mode, name, line + " " + localeInfo.WHISPER_OFFLINE_EXTRA if offline_whisper > 0 else line)
			self.interface.RecvWhisper(name, iLocale)
	else:
		def OnRecvWhisper(self, mode, name, line):
			if mode == chat.WHISPER_TYPE_GM:
				self.interface.RegisterGameMasterName(name)
			chat.AppendWhisper(mode, name, line)
			self.interface.RecvWhisper(name)

	def OnRecvWhisperSystemMessage(self, mode, name, line):
		chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, line)
		self.interface.RecvWhisper(name)

	def OnRecvWhisperError(self, mode, name, line):
		sys_err("TEST", [mode, name, line])
		if localeInfo.WHISPER_ERROR.has_key(mode):
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, localeInfo.WHISPER_ERROR[mode].format(name))
		else:
			chat.AppendWhisper(chat.WHISPER_TYPE_SYSTEM, name, "Whisper Unknown Error(mode=%d, name=%s)" % (mode, name))
		self.interface.RecvWhisper(name)

	def RecvWhisper(self, name):
		self.interface.RecvWhisper(name)

	if app.MULTI_LANGUAGE_SYSTEM_FLAG_VISIBILITY:
		def BINARY_WhisperLanguageInfo(self, name, iLocale):
			self.interface.RecvWhisperLanguage(name, iLocale)

	def OnPickMoney(self, money):
		if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
			import logsChat
			timestamp = app.GetGlobalTimeStamp()

			logsChat.InsertInformation(logsChat.LOG_TYPE_YANG, int(money), 0, timestamp)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_PICK_MONEY % (int(money)))

	def OnShopError(self, type):
		try:
			self.PopupMessage(localeInfo.SHOP_ERROR_DICT[type])
		except KeyError:
			self.PopupMessage(localeInfo.SHOP_ERROR_UNKNOWN % (type))

	def OnSafeBoxError(self):
		self.PopupMessage(localeInfo.SAFEBOX_ERROR)

	def OnFishingSuccess(self, isFish, fishName, fishLength):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_SUCCESS(isFish, fishName), 2000)
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.TOOLTIP_FISH_LEN(fishLength), 2000)

	# ADD_FISHING_MESSAGE
	def OnFishingNotifyUnknown(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_UNKNOWN)

	def OnFishingWrongPlace(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_WRONG_PLACE)
	# END_OF_ADD_FISHING_MESSAGE

	def OnFishingNotify(self, isFish, fishName):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.FISHING_NOTIFY(isFish, fishName))

	def OnFishingFailure(self):
		chat.AppendChatWithDelay(chat.CHAT_TYPE_INFO, localeInfo.FISHING_FAILURE, 2000)

	def OnCannotPickItem(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_PICK_ITEM)

	# MINING
	def OnCannotMining(self):
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GAME_CANNOT_MINING)
	# END_OF_MINING

	def OnCannotUseSkill(self, vid, type):
		if localeInfo.USE_SKILL_ERROR_TAIL_DICT.has_key(type):
			textTail.RegisterInfoTail(vid, localeInfo.USE_SKILL_ERROR_TAIL_DICT[type])

		if localeInfo.USE_SKILL_ERROR_CHAT_DICT.has_key(type):
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.USE_SKILL_ERROR_CHAT_DICT[type])

	def	OnCannotShotError(self, vid, type):
		textTail.RegisterInfoTail(vid, localeInfo.SHOT_ERROR_TAIL_DICT.get(type, localeInfo.SHOT_ERROR_UNKNOWN % (type)))

	## PointReset
	def StartPointReset(self):
		self.interface.OpenPointResetDialog()

	## Shop
	def StartShop(self, vid):
		self.interface.OpenShopDialog(vid)

	def EndShop(self):
		self.interface.CloseShopDialog()

	def RefreshShop(self):
		self.interface.RefreshShopDialog()

	def SetShopSellingPrice(self, Price):
		pass

	## Exchange
	def StartExchange(self):
		self.interface.StartExchange()

	def EndExchange(self):
		self.interface.EndExchange()

	def RefreshExchange(self):
		self.interface.RefreshExchange()

	## Party
	def RecvPartyInviteQuestion(self, leaderVID, leaderName):
		partyInviteQuestionDialog = uiCommon.QuestionDialogWithTimeLimit()
		partyInviteQuestionDialog.SetText1(leaderName + localeInfo.PARTY_DO_YOU_JOIN)
		partyInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerPartyInvite(arg))
		partyInviteQuestionDialog.Open(5)
		partyInviteQuestionDialog.SetCancelOnTimeOver()

		partyInviteQuestionDialog.partyLeaderVID = leaderVID
		self.partyInviteQuestionDialog = partyInviteQuestionDialog

	def AnswerPartyInvite(self, answer):

		if not self.partyInviteQuestionDialog:
			return

		partyLeaderVID = self.partyInviteQuestionDialog.partyLeaderVID

		distance = player.GetCharacterDistance(partyLeaderVID)
		if distance < 0.0 or distance > 5000:
			answer = False

		net.SendPartyInviteAnswerPacket(partyLeaderVID, answer)

		self.partyInviteQuestionDialog.Close()
		self.partyInviteQuestionDialog = None

	def AddPartyMember(self, pid, name):
		self.interface.AddPartyMember(pid, name)

	def UpdatePartyMemberInfo(self, pid):
		self.interface.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.interface.RemovePartyMember(pid)
		self.__RefreshTargetBoard()

	def LinkPartyMember(self, pid, vid):
		self.interface.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.interface.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.interface.UnlinkAllPartyMember()

	def ExitParty(self):
		self.interface.ExitParty()
		self.RefreshTargetBoardByVID(self.targetBoard.GetTargetVID())

	def ChangePartyParameter(self, distributionMode):
		self.interface.ChangePartyParameter(distributionMode)

	## Messenger
	def OnMessengerAddFriendQuestion(self, name):
		messengerAddFriendQuestion = uiCommon.QuestionDialogWithTimeLimit()
		messengerAddFriendQuestion.SetAcceptEvent(ui.__mem_func__(self.OnAcceptAddFriend))
		messengerAddFriendQuestion.SetCancelEvent(ui.__mem_func__(self.OnDenyAddFriend))
		messengerAddFriendQuestion.SetText1(localeInfo.MESSENGER_DO_YOU_ACCEPT_ADD_FRIEND_1 % (name))
		messengerAddFriendQuestion.Open(10)
		messengerAddFriendQuestion.SetCancelOnTimeOver()
		messengerAddFriendQuestion.name = name
		self.messengerAddFriendQuestion = messengerAddFriendQuestion

	def OnAcceptAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth y " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnDenyAddFriend(self):
		name = self.messengerAddFriendQuestion.name
		net.SendChatPacket("/messenger_auth n " + name)
		self.OnCloseAddFriendQuestionDialog()
		return True

	def OnCloseAddFriendQuestionDialog(self):
		self.messengerAddFriendQuestion.Close()
		self.messengerAddFriendQuestion = None
		return True

	## SafeBox
	def OpenSafeboxWindow(self, size):
		self.interface.OpenSafeboxWindow(size)

	def RefreshSafebox(self):
		self.interface.RefreshSafebox()

	# ITEM_MALL
	def OpenMallWindow(self, size):
		self.interface.OpenMallWindow(size)

	def RefreshMall(self):
		self.interface.RefreshMall()
	# END_OF_ITEM_MALL

	## Guild
	def RecvGuildInviteQuestion(self, guildID, guildName):
		guildInviteQuestionDialog = uiCommon.QuestionDialog()
		guildInviteQuestionDialog.SetText(guildName + localeInfo.GUILD_DO_YOU_JOIN)
		guildInviteQuestionDialog.SetAcceptEvent(lambda arg=True: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.SetCancelEvent(lambda arg=False: self.AnswerGuildInvite(arg))
		guildInviteQuestionDialog.Open()
		guildInviteQuestionDialog.guildID = guildID
		self.guildInviteQuestionDialog = guildInviteQuestionDialog

	def AnswerGuildInvite(self, answer):

		if not self.guildInviteQuestionDialog:
			return

		guildLeaderVID = self.guildInviteQuestionDialog.guildID
		net.SendGuildInviteAnswerPacket(guildLeaderVID, answer)

		self.guildInviteQuestionDialog.Close()
		self.guildInviteQuestionDialog = None


	def DeleteGuild(self):
		self.interface.DeleteGuild()

	## Clock
	def ShowClock(self, second):
		self.interface.ShowClock(second)

	def HideClock(self):
		self.interface.HideClock()

	## Emotion
	def BINARY_ActEmotion(self, emotionIndex):
		if self.interface.wndCharacter:
			self.interface.wndCharacter.ActEmotion(emotionIndex)

	###############################################################################################
	###############################################################################################
	## Keyboard Functions

	def CheckFocus(self):
		if False == self.IsFocus():
			if True == self.interface.IsOpenChat():
				self.interface.ToggleChat()

			self.SetFocus()

	def SaveScreen(self):
		print "save screen"

		# SCREENSHOT_CWDSAVE
		if SCREENSHOT_CWDSAVE:
			if not os.path.exists(os.getcwd()+os.sep+"screenshot"):
				os.mkdir(os.getcwd()+os.sep+"screenshot")

			(succeeded, name) = grp.SaveScreenShotToPath(os.getcwd()+os.sep+"screenshot"+os.sep)
		elif SCREENSHOT_DIR:
			(succeeded, name) = grp.SaveScreenShot(SCREENSHOT_DIR)
		else:
			(succeeded, name) = grp.SaveScreenShot()
		# END_OF_SCREENSHOT_CWDSAVE

		if succeeded:
			pass
			"""
			chat.AppendChat(chat.CHAT_TYPE_INFO, name + localeInfo.SCREENSHOT_SAVE1)
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE2)
			"""
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.SCREENSHOT_SAVE_FAILURE)

	def ShowConsole(self):
		print "TRY TO OPEN"
		if debugInfo.IsDebugMode() or True == self.consoleEnable:
			player.EndKeyWalkingImmediately()
			print "XDDDDDDDDDDD OPEN"
			self.console.OpenWindow()

	def ShowName(self):
		self.ShowNameFlag = True
		self.playerGauge.EnableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex+1)

		uiToolTip.GetItemToolTipInstance().OnKeyDown(app.DIK_LALT)

	# ADD_ALWAYS_SHOW_NAME
	def __IsShowName(self):

		if systemSetting.IsAlwaysShowName():
			return True

		if self.ShowNameFlag:
			return True

		return False
	# END_OF_ADD_ALWAYS_SHOW_NAME

	def HideName(self):
		self.ShowNameFlag = False
		self.playerGauge.DisableShowAlways()
		player.SetQuickPage(self.quickSlotPageIndex)

		uiToolTip.GetItemToolTipInstance().OnKeyUp(app.DIK_LALT)

	def ShowMouseImage(self):
		self.interface.ShowMouseImage()

	def HideMouseImage(self):
		self.interface.HideMouseImage()

	def StartAttack(self):
		player.SetAttackKeyState(True)

	def EndAttack(self):
		player.SetAttackKeyState(False)

	def MoveUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, True)

	def MoveDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, True)

	def MoveLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, True)

	def MoveRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, True)

	def StopUp(self):
		player.SetSingleDIKKeyState(app.DIK_UP, False)

	def StopDown(self):
		player.SetSingleDIKKeyState(app.DIK_DOWN, False)

	def StopLeft(self):
		player.SetSingleDIKKeyState(app.DIK_LEFT, False)

	def StopRight(self):
		player.SetSingleDIKKeyState(app.DIK_RIGHT, False)

	def PickUpItem(self):
		player.PickCloseItem()

	###############################################################################################
	###############################################################################################
	## Event Handler

	def OnKeyDown(self, key):
		if self.interface.wndWeb and self.interface.wndWeb.IsShow():
			return

		if gcGetEnable("ENABLE_REFINE_ENTER_ABLE") and self.interface.dlgRefineNew and self.interface.dlgRefineNew.IsShow() and self.interface.dlgRefineNew.HandleReturnButton() and key == 28:
			return

		if key == app.DIK_ESC:
			self.RequestDropItem(False)
			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

		try:
			self.onPressKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return True

	def OnKeyUp(self, key):
		try:
			self.onClickKeyDict[key]()
		except KeyError:
			pass
		except:
			raise

		return True

	def OnMouseLeftButtonDown(self):
		if self.interface.BUILD_OnMouseLeftButtonDown():
			return
		if mouseModule.mouseController.isAttached():
			self.CheckFocus()
		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				return
			else:
				self.CheckFocus()
				player.SetMouseState(player.MBT_LEFT, player.MBS_PRESS);

		return True

	def OnMouseLeftButtonUp(self):
		if self.interface:
			if self.interface.BUILD_OnMouseLeftButtonUp():
				return

		if mouseModule.mouseController.isAttached():

			attachedType = mouseModule.mouseController.GetAttachedType()
			attachedItemIndex = mouseModule.mouseController.GetAttachedItemIndex()
			attachedItemSlotPos = mouseModule.mouseController.GetAttachedSlotNumber()
			attachedItemCount = mouseModule.mouseController.GetAttachedItemCount()

			## QuickSlot
			if player.SLOT_TYPE_QUICK_SLOT == attachedType:
				player.RequestDeleteGlobalQuickSlot(attachedItemSlotPos)

			## Inventory
			elif player.SLOT_TYPE_INVENTORY == attachedType:

				if player.ITEM_MONEY == attachedItemIndex:
					self.__PutMoney(attachedType, attachedItemCount, self.PickingCharacterIndex)
				else:
					self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			## DragonSoul
			elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				self.__PutItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, self.PickingCharacterIndex)

			mouseModule.mouseController.DeattachObject()

		else:
			hyperlink = ui.GetHyperlink()
			if hyperlink:
				if app.IsPressed(app.DIK_LALT):
					link = chat.GetLinkFromHyperlink(hyperlink)
					ime.PasteString(link)
				else:
					self.interface.MakeHyperlinkTooltip(hyperlink)
				return
			else:
				player.SetMouseState(player.MBT_LEFT, player.MBS_CLICK)

		#player.EndMouseWalking()
		return True

	def __PutItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount, dstChrID):
		if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
			attachedInvenType = player.SlotTypeToInvenType(attachedType)
			if True == chr.HasInstance(self.PickingCharacterIndex) and player.GetMainCharacterIndex() != dstChrID:
				if player.IsEquipmentSlot(attachedItemSlotPos) and player.SLOT_TYPE_DRAGON_SOUL_INVENTORY != attachedType:
					self.stream.popupWindow.Close()
					self.stream.popupWindow.Open(localeInfo.EXCHANGE_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)
				else:
					if chr.IsNPC(dstChrID):
						net.SendGiveItemPacket(dstChrID, attachedInvenType, attachedItemSlotPos, attachedItemCount)
					else:
						net.SendExchangeStartPacket(dstChrID)
						net.SendExchangeItemAddPacket(attachedInvenType, attachedItemSlotPos, 0)

						if gcGetEnable("ENABLE_LOCK_EFFECTS"):
							self.ttExchangeEffect = (app.GetTime() + 1, attachedItemSlotPos)

			else:
				self.__DropItem(attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount)

	def __PutMoney(self, attachedType, attachedMoney, dstChrID):
		if True == chr.HasInstance(dstChrID) and player.GetMainCharacterIndex() != dstChrID:
			net.SendExchangeStartPacket(dstChrID)
			net.SendExchangeElkAddPacket(attachedMoney)
		else:
			self.__DropMoney(attachedType, attachedMoney)

	def __DropMoney(self, attachedType, attachedMoney):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		if attachedMoney>=1000:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_MONEY_FAILURE_1000_OVER, 0, localeInfo.UI_OK)
			return

		itemDropQuestionDialog = uiCommon.QuestionDialog()
		itemDropQuestionDialog.SetText(localeInfo.DO_YOU_DROP_MONEY % (attachedMoney))
		itemDropQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDropItem(arg))
		itemDropQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDropItem(arg))
		itemDropQuestionDialog.Open()
		itemDropQuestionDialog.dropType = attachedType
		itemDropQuestionDialog.dropCount = attachedMoney
		itemDropQuestionDialog.dropNumber = player.ITEM_MONEY
		self.itemDropQuestionDialog = itemDropQuestionDialog

	def __DropItem(self, attachedType, attachedItemIndex, attachedItemSlotPos, attachedItemCount):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return
		# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

		if player.SLOT_TYPE_INVENTORY == attachedType and player.IsEquipmentSlot(attachedItemSlotPos):
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.DROP_ITEM_FAILURE_EQUIP_ITEM, 0, localeInfo.UI_OK)

		else:
			if player.SLOT_TYPE_INVENTORY == attachedType or player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType:
				itemDropQuestionDialog = uiDiscardItemWindow.DiscardItemWindow()
				itemDropQuestionDialog.SetItemSlot(attachedItemSlotPos, player.DRAGON_SOUL_INVENTORY if player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == attachedType else player.INVENTORY)
				itemDropQuestionDialog.SetDropEvent(lambda arg="DROP": self.RequestDropItem(arg))
				itemDropQuestionDialog.SetCloseEvent(lambda arg="": self.RequestDropItem(arg))
				itemDropQuestionDialog.SetDestroyEvent(lambda arg=True: self.RequestDestroyItem(arg))
				itemDropQuestionDialog.Open()
				itemDropQuestionDialog.dropType = attachedType
				itemDropQuestionDialog.dropNumber = attachedItemSlotPos
				itemDropQuestionDialog.dropCount = attachedItemCount
				self.itemDropQuestionDialog = itemDropQuestionDialog
				constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(1)

	def RequestDropItem(self, answer):
		if not self.itemDropQuestionDialog:
			return

		if answer:
			if answer == "DROP":
				dropType = self.itemDropQuestionDialog.dropType
				dropCount = self.itemDropQuestionDialog.dropCount
				dropNumber = self.itemDropQuestionDialog.dropNumber

				if player.SLOT_TYPE_INVENTORY == dropType:
					if dropNumber == player.ITEM_MONEY:
						net.SendGoldDropPacketNew(dropCount)
						snd.PlaySound("sound/ui/money.wav")
					else:
						self.__SendDropItemPacket(dropNumber, dropCount)
				elif player.SLOT_TYPE_DRAGON_SOUL_INVENTORY == dropType:
						self.__SendDropItemPacket(dropNumber, dropCount, player.DRAGON_SOUL_INVENTORY)

			elif answer == "SELL":
				pass

		self.itemDropQuestionDialog.Close()
		self.itemDropQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def RequestDestroyItem(self, argument):
		if not self.itemDropQuestionDialog:
			return

		dropType = self.itemDropQuestionDialog.dropType
		dropNumber = self.itemDropQuestionDialog.dropNumber
		
		if argument:
			self.itemDropQuestionDialog.Close()
			self.itemDropQuestionDialog = None

			itemDestroyQuestionDialog = uiCommon.QuestionDialogWithTimeLimit()
			itemDestroyQuestionDialog.SetAcceptEvent(lambda arg=True: self.RequestDestroyItemFinaly(arg))
			itemDestroyQuestionDialog.SetCancelEvent(lambda arg=False: self.RequestDestroyItemFinaly(arg))
			itemDestroyQuestionDialog.SetText1(localeInfo.DESTROY_DIALOG_CONFIRMATION)
			itemDestroyQuestionDialog.Open(10)
			itemDestroyQuestionDialog.SetCancelOnTimeOver()
			itemDestroyQuestionDialog.dropType = dropType
			itemDestroyQuestionDialog.dropNumber = dropNumber

			self.itemDestroyQuestionDialog = itemDestroyQuestionDialog
		else:
			self.__SendDestroyItemPacket(dropNumber, mouseModule.SlotTypeToWindowType(dropType))
			self.itemDropQuestionDialog.Close()
			self.itemDropQuestionDialog = None

			constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)

	def RequestDestroyItemFinaly(self, answer):
		if not self.itemDestroyQuestionDialog:
			return
		
		if answer:
			dropType = self.itemDestroyQuestionDialog.dropType
			dropNumber = self.itemDestroyQuestionDialog.dropNumber

			self.__SendDestroyItemPacket(dropNumber, mouseModule.SlotTypeToWindowType(dropType))

		self.itemDestroyQuestionDialog.Close()
		self.itemDestroyQuestionDialog = None

		constInfo.SET_ITEM_QUESTION_DIALOG_STATUS(0)
	
	# PRIVATESHOP_DISABLE_ITEM_DROP
	def __SendDropItemPacket(self, itemVNum, itemCount, itemInvenType = player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemDropPacketNew(itemInvenType, itemVNum, itemCount)
	# END_OF_PRIVATESHOP_DISABLE_ITEM_DROP

	def __SendDestroyItemPacket(self, itemVNum, itemInvenType = player.INVENTORY):
		if uiPrivateShopBuilder.IsBuildingPrivateShop():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.DROP_ITEM_FAILURE_PRIVATE_SHOP)
			return

		net.SendItemDestroyPacket(itemInvenType, itemVNum)

	def OnMouseRightButtonDown(self):

		self.CheckFocus()

		if True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			player.SetMouseState(player.MBT_RIGHT, player.MBS_PRESS)

		return True

	def OnMouseRightButtonUp(self):
		if True == mouseModule.mouseController.isAttached():
			return True

		player.SetMouseState(player.MBT_RIGHT, player.MBS_CLICK)
		return True

	def OnMouseMiddleButtonDown(self):
		player.SetMouseMiddleButtonState(player.MBS_PRESS)

	def OnMouseMiddleButtonUp(self):
		player.SetMouseMiddleButtonState(player.MBS_CLICK)

	def OnUpdate(self):
		app.UpdateGame()

		if self.mapNameShower.IsShow():
			self.mapNameShower.Update()

		if self.isShowDebugInfo:
			self.UpdateDebugInfo()

		if self.enableXMasBoom:
			self.__XMasBoom_Update()

		self.interface.BUILD_OnUpdate()

		self.queue.Process()

		if app.ENABLE_VOICE_CHAT:
			if self.interface.wVoiceChat:
				self.interface.wVoiceChat.recording = app.IsPressed(app.DIK_F8)

				self.interface.wVoiceChat.iteration()

		if gcGetEnable("ENABLE_LOCK_EFFECTS"):
			if self.ttExchangeEffect[0] > 0 and app.GetTime() >= self.ttExchangeEffect[0]:
				if self.interface.dlgExchange.IsShow():
					self.interface.wndInventory.RegisterLockColour("EXCHANGE", uiexchange.EXCHANGE_COLOUR)
					self.interface.wndInventory.AppendLockSlot("EXCHANGE", self.ttExchangeEffect[1])
					self.interface.wndInventory.RefreshBagSlotWindow()

				self.ttExchangeEffect = (0, 0)

		if app.ENABLE_ADMIN_MANAGER:
			self.interface.AdminManager_OnUpdate()
			
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			uiPrivateShop.UpdateTitleBoard()

	def UpdateDebugInfo(self):
		#
		(x, y, z) = player.GetMainCharacterPosition()
		nUpdateTime = app.GetUpdateTime()
		nUpdateFPS = app.GetUpdateFPS()
		nRenderFPS = app.GetRenderFPS()
		nFaceCount = app.GetFaceCount()
		fFaceSpeed = app.GetFaceSpeed()
		nST=background.GetRenderShadowTime()
		(fAveRT, nCurRT) =  app.GetRenderTime()
		(iNum, fFogStart, fFogEnd, fFarCilp) = background.GetDistanceSetInfo()
		(iPatch, iSplat, fSplatRatio, sTextureNum) = background.GetRenderedSplatNum()
		if iPatch == 0:
			iPatch = 1

		#(dwRenderedThing, dwRenderedCRC) = background.GetRenderedGraphicThingInstanceNum()

		self.PrintCoord.SetText("Coordinate: %.2f %.2f %.2f ATM: %d" % (x, y, z, app.GetAvailableTextureMemory()/(1024*1024)))
		xMouse, yMouse = wndMgr.GetMousePosition()
		self.PrintMousePos.SetText("MousePosition: %d %d" % (xMouse, yMouse))

		self.FrameRate.SetText("UFPS: %3d UT: %3d FS %.2f" % (nUpdateFPS, nUpdateTime, fFaceSpeed))

		if fAveRT>1.0:
			self.Pitch.SetText("RFPS: %3d RT:%.2f(%3d) FC: %d(%.2f) " % (nRenderFPS, fAveRT, nCurRT, nFaceCount, nFaceCount/fAveRT))

		self.Splat.SetText("PATCH: %d SPLAT: %d BAD(%.2f)" % (iPatch, iSplat, fSplatRatio))
		#self.Pitch.SetText("Pitch: %.2f" % (app.GetCameraPitch())
		#self.TextureNum.SetText("TN : %s" % (sTextureNum))
		#self.ObjectNum.SetText("GTI : %d, CRC : %d" % (dwRenderedThing, dwRenderedCRC))
		self.ViewDistance.SetText("Num : %d, FS : %f, FE : %f, FC : %f" % (iNum, fFogStart, fFogEnd, fFarCilp))

	def OnRender(self):
		app.RenderGame()

		if self.console.Console.collision:
			background.RenderCollision()
			chr.RenderCollision()

		(x, y) = app.GetCursorPosition()

		########################
		# Picking
		########################
		textTail.UpdateAllTextTail()

		if True == wndMgr.IsPickedWindow(self.hWnd):

			self.PickingCharacterIndex = chr.Pick()

			if -1 != self.PickingCharacterIndex:
				textTail.ShowCharacterTextTail(self.PickingCharacterIndex)
			if 0 != self.targetBoard.GetTargetVID():
				textTail.ShowCharacterTextTail(self.targetBoard.GetTargetVID())

			# ADD_ALWAYS_SHOW_NAME
			if not self.__IsShowName():
				self.PickingItemIndex = item.Pick()
				if -1 != self.PickingItemIndex:
					textTail.ShowItemTextTail(self.PickingItemIndex)
			# END_OF_ADD_ALWAYS_SHOW_NAME

		## Show all name in the range

		# ADD_ALWAYS_SHOW_NAME
		if self.__IsShowName():
			textTail.ShowAllTextTail()
			self.PickingItemIndex = textTail.Pick(x, y)
		# END_OF_ADD_ALWAYS_SHOW_NAME

		textTail.UpdateShowingTextTail()
		textTail.ArrangeTextTail()
		if -1 != self.PickingItemIndex:
			textTail.SelectItemName(self.PickingItemIndex)

		grp.PopState()
		grp.SetInterfaceRenderState()

		textTail.Render()
		textTail.HideAllTextTail()

	def OnPressEscapeKey(self):
		if app.TARGET == app.GetCursor():
			app.SetCursor(app.NORMAL)

		elif True == mouseModule.mouseController.isAttached():
			mouseModule.mouseController.DeattachObject()

		else:
			self.interface.OpenSystemDialog()

		return True

	def OnIMEReturn(self):
		if app.IsPressed(app.DIK_LSHIFT):
			self.interface.OpenWhisperDialogWithoutTarget()
		else:
			self.interface.ToggleChat()
		return True

	def OnPressExitKey(self):
		self.interface.ToggleSystemDialog()
		return True

	## BINARY CALLBACK
	######################################################################################

	# WEDDING
	def BINARY_LoverInfo(self, name, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnAddLover(name, lovePoint)
		if self.affectShower:
			self.affectShower.SetLoverInfo(name, lovePoint)

	def BINARY_UpdateLovePoint(self, lovePoint):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnUpdateLovePoint(lovePoint)
		if self.affectShower:
			self.affectShower.OnUpdateLovePoint(lovePoint)
	# END_OF_WEDDING

	# QUEST_CONFIRM
	def BINARY_OnQuestConfirm(self, msg, timeout, pid):
		confirmDialog = uiCommon.QuestionDialogWithTimeLimit()
		confirmDialog.SetText1(msg)
		confirmDialog.Open(timeout)
		confirmDialog.SetAcceptEvent(lambda answer=True, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelEvent(lambda answer=False, pid=pid: net.SendQuestConfirmPacket(answer, pid) or self.confirmDialog.Hide())
		confirmDialog.SetCancelOnTimeOver()
		self.confirmDialog = confirmDialog

	def Gift_Show(self):
		self.interface.ShowGift()

	def BINARY_Highlight_Item(self, inven_type, inven_pos):
		# @fixme003 (+if self.interface:)
		if self.interface:
			self.interface.Highligt_Item(inven_type, inven_pos)

	def BINARY_DragonSoulGiveQuilification(self):
		self.interface.DragonSoulGiveQuilification()

	def BINARY_DragonSoulRefineWindow_Open(self):
		self.interface.OpenDragonSoulRefineWindow()

	def BINARY_DragonSoulRefineWindow_RefineFail(self, reason, inven_type, inven_pos):
		self.interface.FailDragonSoulRefine(reason, inven_type, inven_pos)

	def BINARY_DragonSoulRefineWindow_RefineSucceed(self, inven_type, inven_pos):
		self.interface.SucceedDragonSoulRefine(inven_type, inven_pos)

	# END of DRAGON SOUL REFINE WINDOW

	def BINARY_SetBigMessage(self, message):
		if gcGetEnable("ENABLE_REFACTORED_OPTIONS"):
			if cfg.Get(cfg.SAVE_OPTION, "NOTICE_MODE", "0") == "1":
				return

		self.interface.bigBoard.SetTip(message)

	def BINARY_SetTipMessage(self, message):
		if gcGetEnable("ENABLE_REFACTORED_OPTIONS"):
			if cfg.Get(cfg.SAVE_OPTION, "NOTICE_MODE", "0") == "1":
				return

		self.interface.tipBoard.SetTip(message)

	def BINARY_AppendNotifyMessage(self, type):
		if not type in localeInfo.NOTIFY_MESSAGE:
			return
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.NOTIFY_MESSAGE[type])

	def BINARY_Guild_EnterGuildArea(self, areaID):
		self.interface.BULID_EnterGuildArea(areaID)

	def BINARY_Guild_ExitGuildArea(self, areaID):
		self.interface.BULID_ExitGuildArea(areaID)

	def BINARY_GuildWar_OnSendDeclare(self, guildID):
		pass

	def BINARY_GuildWar_OnRecvDeclare(self, guildID, warType):
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()
		if mainCharacterName == masterName:
			self.__GuildWar_OpenAskDialog(guildID, warType)

	def BINARY_GuildWar_OnRecvPoint(self, gainGuildID, opponentGuildID, point):
		self.interface.OnRecvGuildWarPoint(gainGuildID, opponentGuildID, point)

	def BINARY_GuildWar_OnStart(self, guildSelf, guildOpp):
		self.interface.OnStartGuildWar(guildSelf, guildOpp)

	def BINARY_GuildWar_OnEnd(self, guildSelf, guildOpp):
		self.interface.OnEndGuildWar(guildSelf, guildOpp)

	def BINARY_BettingGuildWar_SetObserverMode(self, isEnable):
		self.interface.BINARY_SetObserverMode(isEnable)

	def BINARY_BettingGuildWar_UpdateObserverCount(self, observerCount):
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_UpdateMemberCount(self, guildID1, memberCount1, guildID2, memberCount2, observerCount):
		guildID1 = int(guildID1)
		guildID2 = int(guildID2)
		memberCount1 = int(memberCount1)
		memberCount2 = int(memberCount2)
		observerCount = int(observerCount)

		self.interface.UpdateMemberCount(guildID1, memberCount1, guildID2, memberCount2)
		self.interface.wndMiniMap.UpdateObserverCount(observerCount)

	def __GuildWar_OpenAskDialog(self, guildID, warType):

		guildName = guild.GetGuildName(guildID)

		# REMOVED_GUILD_BUG_FIX
		if "Noname" == guildName:
			return
		# END_OF_REMOVED_GUILD_BUG_FIX

		import uiGuild
		questionDialog = uiGuild.AcceptGuildWarDialog()
		questionDialog.SAFE_SetAcceptEvent(self.__GuildWar_OnAccept)
		questionDialog.SAFE_SetCancelEvent(self.__GuildWar_OnDecline)
		questionDialog.Open(guildName, warType)

		self.guildWarQuestionDialog = questionDialog

	def __GuildWar_CloseAskDialog(self):
		self.guildWarQuestionDialog.Close()
		self.guildWarQuestionDialog = None

	def __GuildWar_OnAccept(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/war " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1

	def __GuildWar_OnDecline(self):

		guildName = self.guildWarQuestionDialog.GetGuildName()

		net.SendChatPacket("/nowar " + guildName)
		self.__GuildWar_CloseAskDialog()

		return 1
	## BINARY CALLBACK
	######################################################################################

	def __ServerCommand_Build(self):
		serverCommandList={
			"ConsoleEnable"			: self.__Console_Enable,
			"DayMode"				: self.__DayMode_Update,
			"PRESERVE_DayMode"		: self.__PRESERVE_DayMode_Update,
			"CloseRestartWindow"	: self.__RestartDialog_Close,
			"OpenPrivateShop"		: self.__PrivateShop_Open,
			"PartyHealReady"		: self.PartyHealReady,
			"ShowMeSafeboxPassword"	: self.AskSafeboxPassword,
			"CloseSafebox"			: self.CommandCloseSafebox,

			# ITEM_MALL
			"CloseMall"				: self.CommandCloseMall,
			"ShowMeMallPassword"	: self.AskMallPassword,
			"item_mall"				: self.__ItemMall_Open,
			# END_OF_ITEM_MALL

			"RefineSuceeded"		: self.RefineSuceededMessage,
			"RefineFailed"			: self.RefineFailedMessage,
			"xmas_snow"				: self.__XMasSnow_Enable,
			"xmas_boom"				: self.__XMasBoom_Enable,
			"xmas_song"				: self.__XMasSong_Enable,
			"xmas_tree"				: self.__XMasTree_Enable,
			"newyear_boom"			: self.__XMasBoom_Enable,
			"PartyRequest"			: self.__PartyRequestQuestion,
			"PartyRequestDenied"	: self.__PartyRequestDenied,
			"horse_state"			: self.__Horse_UpdateState,
			"hide_horse_state"		: self.__Horse_HideState,
			"WarUC"					: self.__GuildWar_UpdateMemberCount,
			"test_server"			: self.__EnableTestServerFlag,
			"mall"			: self.__InGameShop_Show,

			# WEDDING
			"lover_login"			: self.__LoginLover,
			"lover_logout"			: self.__LogoutLover,
			"lover_near"			: self.__LoverNear,
			"lover_far"				: self.__LoverFar,
			"lover_divorce"			: self.__LoverDivorce,
			"PlayMusic"				: self.__PlayMusic,
			# END_OF_WEDDING

			# PRIVATE_SHOP_PRICE_LIST
			"MyShopPriceList"		: self.__PrivateShop_PriceList,
			# END_OF_PRIVATE_SHOP_PRICE_LIST
		}

		if gcGetEnable("ENABLE_ITEM_HIGHLIGHT_"):
			serverCommandList["Item_HightLight"] = self.__Item_HightLight__

		if app.ENABLE_GAYA_SYSTEM:
			serverCommandList["OpenGayaCrafting"] = self.OpenGayaCrafting
			serverCommandList["GayaAddItem"] = self.GayaAddItem
			serverCommandList["RequestGayaMarket"] = self.RequestGayaMarket
			serverCommandList["GayaRotationTime"] = self.GayaRotationTime
			serverCommandList["GayaEraseDesc"] = self.GayaEraseDesc
			serverCommandList["GayaOpenInterface"] = self.GayaOpenInterface

		if gcGetEnable("EVENT_MANAGER_ENABLE"):
			serverCommandList["EventManagerOpenPanel"] = self.__Event_Manager_OpenPanel__
			serverCommandList["EventManagerBroadcastStatus"] = self.__Event_Manager_BroadcastStatus__
			serverCommandList["EventManagerUpdateEvent"] = self.__Event_Manager_UpdateEvent__

		if app.ENABLE_FAST_REFINE_OPTION:
			serverCommandList["CloseRefine"] = self.CloseRefineDialog

		if app.ENABLE_CHANGE_CHANNEL:
			serverCommandList["UpdateChannelInfo"] = self.UpdateChannelInfo

		if gcGetEnable("ENABLE_TECHNICAL_MAINTENANCE"):
			serverCommandList["TechnicalMaintenanceOpenPanel"] = self.__TechnicalMaintenanceOpenPanel__
			serverCommandList["TechnicalMaintenanceInfo"] = self.__TechnicalMaintenanceInfo__

		if gcGetEnable("ENABLE_NOTIFICATON_SENDER"):
			## Panel
			serverCommandList["GMIdleOpenInterface"] = self.__GMIdleOpenInterface__
			serverCommandList["GMIdleSendCollectionCount"] = self.__GMIdleSendCollectionCount__
			serverCommandList["GMIdleSendPlayerName"] = self.__GMIdleSendPlayerName__
			serverCommandList["GMIdleUpdateAllPlayerStatus"] = self.__GMIdleUpdateAllPlayerStatus__
			serverCommandList["GMIdleErasePlayer"] = self.__GMIdleErasePlayer__
			serverCommandList["GMIdleUpdatePlayerStatus"] = self.__GMIdleUpdatePlayerStatus__
			## Player
			serverCommandList["GMIdleSendNotification"] = self.__GMIdleSendNotification__

		if app.ZUO_PANEL_ENABLE:
			serverCommandList["ZuoMenuDialog"] = self.ZuoMenuDialog
			serverCommandList["UpdateZuoDialogElement"] = self.UpdateZuoDialogElement

		if app.SHIP_DEFEND_DUNGEON:
			serverCommandList["Ship_Defend_Dungeon_Open"] = self.__Ship_Defend_Dungeon_Open__
			serverCommandList["Ship_Defend_Dungeon_Update"] = self.__Ship_Defend_Dungeon_Update__

		if app.BATTLE_PASS_ENABLE:
			serverCommandList["BattlePass_ClearInterface"] = self.__BATTLE_PASS__ClearInterface
			serverCommandList["BattlePass_BasicInfo"] = self.__BATTLE_PASS__BasicInfo
			serverCommandList["BattlePass_MajorReward"] = self.__BATTLE_PASS__MajorReward
			serverCommandList["BattlePass_TaskInfo"] = self.__BATTLE_PASS__TaskInfo
			serverCommandList["BattlePass_TaskReward"] = self.__BATTLE_PASS__TaskReward
			serverCommandList["BattlePass_HighScore"] = self.__BATTLE_PASS__HighScore

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			## Transmutation
			serverCommandList["Transmutation_Open"] = self.Transmutation_Open
			serverCommandList["SetNewTransMutationItem"] = self.SetNewTransMutationItem

		if app.ENABLE_FIND_LETTERS_EVENT:
			serverCommandList["FindLettersIcon"] = self.BINARY_FindLettersIcon
			serverCommandList["FindLettersRefresh"] = self.BINARY_AddFindLetters
			serverCommandList["FindLettersFinish"] = self.BINARY_FindLettersFinishEvent

		if app.ENABLE_SOUL_SYSTEM:
			serverCommandList["RefineSoulSuceeded"] = self.__RefineSoulSuceededMessage
			serverCommandList["RefineSoulFailed"] = self.__RefineSoulFailedMessage

		if app.ENABLE_LUCKY_BOX:
			serverCommandList["CloseLuckyBox"] = self.BINARY_CloseLuckyBox

		## OX PANEL ##
		if app.OX_EVENT_SYSTEM_ENABLE:
			serverCommandList["OxMenuDialog"] = self.OxMenuDialog
			serverCommandList["UpdateAttendersCount"] = self.UpdateAttendersCount
			serverCommandList["UpdateOXQuestionPool"] = self.UpdateOXQuestionPool

		if app.ENABLE_PASSIVE_SKILLS_HELPER:
			serverCommandList["SkillsManager_ClearInterface"] = self.__SKILLS_MANAGER__ClearInterface
			serverCommandList["SkillsManager_RegisterInformation"] = self.__SKILLS_MANAGER__RegisterInformation

		if app.ENABLE_SAVE_POSITIONS_SYSTEM:
			serverCommandList["Positions_Initialize"] = self.Positions_Initialize
			serverCommandList["Positions_AppendData"] = self.Positions_AppendData
			serverCommandList["Positions_ClearInterface"] = self.Positions_ClearInterface

		if app.ENABLE_TELEPORT_SYSTEM:
			serverCommandList["TeleportManager_ClearInterface"] = self.__BINARY__TeleportManager_Clear
			serverCommandList["TeleportManager_RegisterCategory"] = self.__BINARY__TeleportManager_Category
			serverCommandList["TeleportManager_RegisterTeleport"] = self.__BINARY__TeleportManager_Item
			serverCommandList["TeleportManager_Show"] = self.__BINARY__TeleportManager_Show

		if gcGetEnable("ENABLE_SKILL_SELECT"):
			serverCommandList["RECV_SkillSelect"] = self.__RecvSkillSelect

		if app.INGAME_ITEMSHOP_ENABLE:
			serverCommandList["ItemShopClear"] = self.__BINARY__ItemShopClear
			serverCommandList["ItemShopCategory"] = self.__BINARY__ItemShopCategory
			serverCommandList["ItemShopItem"] = self.__BINARY__ItemShopItem
			serverCommandList["ItemShopUpdateCash"] = self.__BINARY__ItemShopUpdateCash
			serverCommandList["ItemShopPromos"] = self.__BINARY__ItemShopPromos
			serverCommandList["ItemShopSpecialOffer"] = self.__BINARY__ItemShopSpecialOffer
			serverCommandList["ItemShopShow"] = self.__BINARY__ItemShopShow

		if app.TOMBOLA_EVENT_ENABLE:
			serverCommandList["TombolaStatus"] = self.__TOMBOLA__TombolaStatus
			serverCommandList["TombolaItem"] = self.__TOMBOLA__TombolaItem
			serverCommandList["TombolaSpin"] = self.__TOMBOLA__TombolaSpin
			serverCommandList["TombolaUserBalance"] = self.__TOMBOLA__TombolaUserBalance
			serverCommandList["TombolaOpenDialog"] = self.__TOMBOLA__TombolaOpenDialog

		if gcGetEnable("ENABLE_ADMIN_BAN_PANEL"):
			serverCommandList["OpenBanPanel"] = self.__OpenBanPanel

		if gcGetEnable("ENABLE_SKILLS_INFORMATION"):
			serverCommandList["SkillInformationExorcism"] = self.__BINARY__SkillInformationExorcism
			serverCommandList["SkillInformationClear"] = self.__BINARY__SkillInformationClear
			serverCommandList["SkillInformation"] = self.__BINARY__SkillInformation

		if gcGetEnable("ENABLE_LEGENDARY_STONES"):
			serverCommandList["LEGENDARY_STONES_OPEN"] = self.__BINARY__LEGENDARY_STONES_OPEN
			serverCommandList["LEGENDARY_STONES_CONFIGURATION"] = self.__BINARY__LEGENDARY_STONES_CONFIGURATION
			serverCommandList["LEGENDARY_STONES_CLEAR"] = self.__BINARY__LEGENDARY_STONES_CLEAR
			serverCommandList["LEGENDARY_STONES_SET_ITEM"] = self.__BINARY__LEGENDARY_STONES_SET_ITEM

		if gcGetEnable("ENABLE_DUNGEON_INFORMATION"):
			serverCommandList["DungeonInfo_OpenPanel"] = self.__DUNGEON_INFO__OpenPanel
			serverCommandList["DungeonInfo_BroadcastGlobal"] = self.__DUNGEON_INFO__BroadcastGlobal
			serverCommandList["DungeonInfo_BroadcastPersonal"] = self.__DUNGEON_INFO__BroadcastPersonal
			serverCommandList["DungeonInfo_BroadcastHighscore"] = self.__DUNGEON_INFO__BroadcastHighscore
			serverCommandList["DungeonInfo_RecvHighscoreDataClear"] = self.__DUNGEON_INFO__RecvHighscoreDataClear

		if gcGetEnable("ENABLE_DUNGEON_TASK_INFORMATION"):
			serverCommandList["DungeonTaskHelper_RegisterDungeon"] = self.DUNGEON_TASK_SetDungeon
			serverCommandList["DungeonTaskHelper_RegisterTask"] = self.DUNGEON_TASK_TaskInfo
			serverCommandList["DungeonTaskHelper_SetGlobalTimer"] = self.DUNGEON_TASK_SetGlobalTimer
			serverCommandList["DungeonTaskHelper_SetCurrentTask"] = self.DUNGEON_TASK_SetCurrentTask
			serverCommandList["DungeonTaskHelper_EndTasks"] = self.DUNGEON_TASK_EndDungeon
			serverCommandList["DungeonTaskHelper_SetLocalTimer"] = self.DUNGEON_TASK_SetLocalTimer
			serverCommandList["DungeonTaskHelper_UpdateCounter"] = self.DUNGEON_TASK_UpdateCounter
			serverCommandList["DungeonTaskHelper_UpdateProgress"] = self.DUNGEON_TASK_UpdateProgress

		if app.SASH_ABSORPTION_ENABLE:
			serverCommandList["Sash_Combination_Open"] = self.__Sash_Combination_Open
			serverCommandList["Sash_Combination_Update_Slot"] = self.__Sash_Combination_Update_Slot
			serverCommandList["Sash_Combination_UpdateCost"] = self.__Sash_Combination_UpdateCost
			serverCommandList["Sash_Combination_Clear"] = self.__Sash_Combination_Clear
			serverCommandList["Sash_Combination_Close"] = self.__Sash_Combination_Close
			serverCommandList["Sash_Absorption_Open"] = self.__Sash_Absorption_Open
			serverCommandList["Sash_Absorption_Update_Slot"] = self.__Sash_Absorption_Update_Slot
			serverCommandList["Sash_Absorption_Clear"] = self.__Sash_Absorption_Clear
			serverCommandList["Sash_Absorption_Close"] = self.__Sash_Absorption_Close
			serverCommandList["Sash_Inventory_Refresh"] = self.__Sash_Inventory_Refresh
			serverCommandList["SashCombination_RequestOpen"] = self.__SashCombination_RequestOpen
			serverCommandList["SashAbsorption_RequestOpen"] = self.__SashAbsorption_RequestOpen

		if gcGetEnable("ENABLE_EQUIPMENT_LOCK_SLOT"):
			serverCommandList["EquipmentLock_Clear"] = self.EQUIPMENT_LOCK_Clear
			serverCommandList["EquipmentLock_Info"] = self.EQUIPMENT_LOCK_Info

		if gcGetEnable("ENABLE_HIDE_COSTUMES"):
			serverCommandList["BroadcastHideCostume_Info"] = self.HCOSTUMES_Info

		if app.ENABLE_AMULET_SYSTEM:
			serverCommandList["AmuletInformation_UpgradeClear"] = self.__AmuletInformation_UpgradeClear
			serverCommandList["AmuletInformation_UpgradeInfo"] = self.__AmuletInformation_UpgradeInfo
			serverCommandList["AmuletCrafting_Open"] = self.__AmuletCrafting_Open
			serverCommandList["AmuletPassive_Info"] = self.__AmuletPassive_Info

			serverCommandList["AmuletCombine_Open"] = self.__AmuletCombine_Open
			serverCommandList["AmuletCombine_RegisterItem"] = self.__AmuletCombine_RegisterItem
			serverCommandList["AmuletCombine_RegisterChance"] = self.__AmuletCombine_RegisterChance
			serverCommandList["AmuletCombine_RegisterGold"] = self.__AmuletCombine_RegisterGold
			serverCommandList["AmuletCombine_Reset"] = self.__AmuletCombine_Reset

		if (gcGetEnable("ENABLE_SHAMAN_SYSTEM")):
			serverCommandList["ShamanSystem_RegisterSkillCount"] = self.__ShamanSystem__RegisterSkillCount
			serverCommandList["ShamanSystem_RegisterSkill"] = self.__ShamanSystem__RegisterSkill
			serverCommandList["ShamanSystem_RegisterPremium"] = self.__ShamanSystem__RegisterPremium
			serverCommandList["ShamanSystem_UnregisterShaman"] = self.__ShamanSystem__UnregisterShaman

		if (gcGetEnable("POPUP_SYSTEM_ENABLE")):
			serverCommandList["PopupMessageAppend"] = self.__RECV__PopupMessageAppend

		if (gcGetEnable("MISSION_MANAGER")):
			serverCommandList["MissionManager_ClearInterface"] = self.__MisionManager__Clear
			serverCommandList["MissionManager_TaskInfo"] = self.__MisionManager__TaskInfo
			serverCommandList["MissionManager_TaskRefresh"] = self.__MisionManager__TaskRefresh
			serverCommandList["MissionManager_RewardInfo"] = self.__MisionManager__RewardInfo
			serverCommandList["MissionManager_Refresh"] = self.__MisionManager__Refresh

		if (gcGetEnable("ATTENDANCE_MANAGER")):
			serverCommandList["Attendance_Status"] = self.__AttendanceManager__Status
			serverCommandList["Attendance_ClearInterface"] = self.__AttendanceManager__Clear
			serverCommandList["Attendance_BasicInfo"] = self.__AttendanceManager__BasicInfo
			serverCommandList["Attendance_Item"] = self.__AttendanceManager_Item
			serverCommandList["Attendance_RefreshItem"] = self.__AttendanceManager_RefreshItem
			serverCommandList["Attendance_Refresh"] = self.__AttendanceManager__Refresh

		if app.ENABLE_BIOLOG_SYSTEM:
			serverCommandList["BiologManager_RegisterProgress"] = self.__BiologManager__RegisterProgress
			serverCommandList["BiologManager_RegisterMission"] = self.__BiologManager__RegisterMission
			serverCommandList["BiologManager_RegisterRewardBasic"] = self.__BiologManager__RegisterRewardBasic
			serverCommandList["BiologManager_RegisterRewardAffect"] = self.__BiologManager__RegisterRewardAffect
			serverCommandList["BiologManager_RequestOpen"] = self.__BiologManager__RequestOpen
			serverCommandList["BiologManager_RequestClose"] = self.__BiologManager__RequestClose
			serverCommandList["BiologManager_RequestClear"] = self.__BiologManager__RequestClear

			serverCommandList["BiologManager_RegisterSet"] = self.__BiologManager__RegisterSet
			serverCommandList["BiologManager_RegisterSetAffect"] = self.__BiologManager__RegisterSetAffect
			serverCommandList["BiologManager_ClearSet"] = self.__BiologManager__ClearSet
			serverCommandList["BiologManager_OpenSet"] = self.__BiologManager__OpenSet

		if (gcGetEnable("MOB_TRACKER")):
			serverCommandList["MobTracker_ClearInterface"] = self.__MobTracker__Clear
			serverCommandList["MobTracker_RegisterInfo"] = self.__MobTracker__Register
			serverCommandList["MobTracker_OpenInterface"] = self.__MobTracker__Open
			
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			serverCommandList["SetPrivateShopPremiumBuild"] = self.SetPrivateShopPremiumBuild

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			serverCommandList["BuffNPCSummon"] = self.__SetBuffNPCSummon
			serverCommandList["BuffNPCUnsummon"] = self.__SetBuffNPCUnsummon
			serverCommandList["BuffNPCClear"] = self.__SetBuffNPCClear
			serverCommandList["BuffNPCBasicInfo"] = self.__SetBuffNPCBasicInfo
			serverCommandList["BuffNPCEXPInfo"] = self.__SetBuffNPCEXPInfo
			serverCommandList["BuffNPCSkillInfo"] = self.__SetBuffNPCSkillInfo
			serverCommandList["BuffNPCSkillUseStatus"] = self.__SetBuffNPCSkillUseStatus
			serverCommandList["BuffNPCSkillCooltime"] = self.__SetBuffNPCSkillSetSkillCooltime
			serverCommandList["BuffNPCCreatePopup"] = self.__SetBuffNPCCreatePopup

		if app.GLOBAL_RANKING_ENABLE:
			serverCommandList["GlobalRankingUpdatePacket"] = self.__Global_Ranking__RecvData
			serverCommandList["GlobalRankingUpdatePacketMyPos"] = self.__Global_Ranking__RecvSelfData

		self.serverCommander=stringCommander.Analyzer()
		for serverCommandItem in serverCommandList.items():
			self.serverCommander.SAFE_RegisterCallBack(
				serverCommandItem[0], serverCommandItem[1]
			)

	def BINARY_ServerCommand_Run(self, line):
		try:
			#print " BINARY_ServerCommand_Run", line
			return self.serverCommander.Run(line)
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def __ProcessPreservedServerCommand(self):
		try:
			command = net.GetPreservedServerCommand()
			while command:
				print " __ProcessPreservedServerCommand", command
				self.serverCommander.Run(command)
				command = net.GetPreservedServerCommand()
		except RuntimeError, msg:
			dbg.TraceError(msg)
			return 0

	def PartyHealReady(self):
		self.interface.PartyHealReady()

	def AskSafeboxPassword(self):
		self.interface.AskSafeboxPassword()

	# ITEM_MALL
	def AskMallPassword(self):
		self.interface.AskMallPassword()

	def __ItemMall_Open(self):
		self.interface.OpenItemMall();

	def CommandCloseMall(self):
		self.interface.CommandCloseMall()
	# END_OF_ITEM_MALL

	def RefineSuceededMessage(self):
		snd.PlaySound("sound/ui/make_soket.wav")
		self.PopupMessage(localeInfo.REFINE_SUCCESS)

	def RefineFailedMessage(self):
		snd.PlaySound("sound/ui/jaeryun_fail.wav")
		self.PopupMessage(localeInfo.REFINE_FAILURE)

	def CommandCloseSafebox(self):
		self.interface.CommandCloseSafebox()

	# PRIVATE_SHOP_PRICE_LIST
	def __PrivateShop_PriceList(self, itemVNum, itemPrice):
		uiPrivateShopBuilder.SetPrivateShopItemPrice(itemVNum, itemPrice)
	# END_OF_PRIVATE_SHOP_PRICE_LIST

	def __Horse_HideState(self):
		self.affectShower.SetHorseState(0, 0, 0)

	def __Horse_UpdateState(self, level, health, battery):
		self.affectShower.SetHorseState(int(level), int(health), int(battery))

		self.interface.RepositionGroup(self.affectShower.GetBottom())

	def __IsXMasMap(self):
		mapDict = ( "metin2_map_n_flame_01",
					"metin2_map_n_desert_01",
					"metin2_map_spiderdungeon",
					"metin2_map_deviltower1", )

		if background.GetCurrentMapName() in mapDict:
			return False

		return True

	def __XMasSnow_Enable(self, mode):

		self.__XMasSong_Enable(mode)

		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_SNOW ON"
			background.EnableSnow(1)

		else:
			print "XMAS_SNOW OFF"
			background.EnableSnow(0)

	def __XMasBoom_Enable(self, mode):
		if "1"==mode:

			if not self.__IsXMasMap():
				return

			print "XMAS_BOOM ON"
			self.__DayMode_Update("dark")
			self.enableXMasBoom = True
			self.startTimeXMasBoom = app.GetTime()
		else:
			print "XMAS_BOOM OFF"
			self.__DayMode_Update("light")
			self.enableXMasBoom = False

	def __XMasTree_Enable(self, grade):

		print "XMAS_TREE ", grade
		background.SetXMasTree(int(grade))

	def __XMasSong_Enable(self, mode):
		if "1"==mode:
			print "XMAS_SONG ON"

			XMAS_BGM = "xmas.mp3"

			if app.IsExistFile("BGM/" + XMAS_BGM)==1:
				if musicInfo.fieldMusic != "":
					snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

				musicInfo.fieldMusic=XMAS_BGM
				snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		else:
			print "XMAS_SONG OFF"

			if musicInfo.fieldMusic != "":
				snd.FadeOutMusic("BGM/" + musicInfo.fieldMusic)

			musicInfo.fieldMusic=musicInfo.METIN2THEMA
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	def __RestartDialog_Close(self):
		self.interface.CloseRestartDialog()

	def __Console_Enable(self):
		constInfo.CONSOLE_ENABLE = True
		self.consoleEnable = True
		app.EnableSpecialCameraMode()
		ui.EnablePaste(True)

	## PrivateShop
	def __PrivateShop_Open(self):
		self.interface.OpenPrivateShopInputNameDialog()

	def BINARY_PrivateShop_Appear(self, vid, text):
		self.interface.AppearPrivateShop(vid, text)

	def BINARY_PrivateShop_Disappear(self, vid):
		self.interface.DisappearPrivateShop(vid)

	## DayMode
	def __PRESERVE_DayMode_Update(self, mode):
		if "light"==mode:
			background.SetEnvironmentData(0)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

	def __DayMode_Update(self, mode):
		if "light"==mode:
			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToLight)
		elif "dark"==mode:

			if not self.__IsXMasMap():
				return

			self.curtain.SAFE_FadeOut(self.__DayMode_OnCompleteChangeToDark)

	def __DayMode_OnCompleteChangeToLight(self):
		background.SetEnvironmentData(0)
		self.curtain.FadeIn()

	def __DayMode_OnCompleteChangeToDark(self):
		background.RegisterEnvironmentData(1, constInfo.ENVIRONMENT_NIGHT)
		background.SetEnvironmentData(1)
		self.curtain.FadeIn()

	## XMasBoom
	def __XMasBoom_Update(self):

		self.BOOM_DATA_LIST = ( (2, 5), (5, 2), (7, 3), (10, 3), (20, 5) )
		if self.indexXMasBoom >= len(self.BOOM_DATA_LIST):
			return

		boomTime = self.BOOM_DATA_LIST[self.indexXMasBoom][0]
		boomCount = self.BOOM_DATA_LIST[self.indexXMasBoom][1]

		if app.GetTime() - self.startTimeXMasBoom > boomTime:

			self.indexXMasBoom += 1

			for i in xrange(boomCount):
				self.__XMasBoom_Boom()

	def __XMasBoom_Boom(self):
		x, y, z = player.GetMainCharacterPosition()
		randX = app.GetRandom(-150, 150)
		randY = app.GetRandom(-150, 150)

		snd.PlaySound3D(x+randX, -y+randY, z, "sound/common/etc/salute.mp3")

	def __PartyRequestQuestion(self, vid):
		vid = int(vid)
		partyRequestQuestionDialog = uiCommon.QuestionDialog()
		partyRequestQuestionDialog.SetText(chr.GetNameByVID(vid) + localeInfo.PARTY_DO_YOU_ACCEPT)
		partyRequestQuestionDialog.SetAcceptText(localeInfo.UI_ACCEPT)
		partyRequestQuestionDialog.SetCancelText(localeInfo.UI_DENY)
		partyRequestQuestionDialog.SetAcceptEvent(lambda arg=True: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.SetCancelEvent(lambda arg=False: self.__AnswerPartyRequest(arg))
		partyRequestQuestionDialog.Open()
		partyRequestQuestionDialog.vid = vid
		self.partyRequestQuestionDialog = partyRequestQuestionDialog

	def __AnswerPartyRequest(self, answer):
		if not self.partyRequestQuestionDialog:
			return

		vid = self.partyRequestQuestionDialog.vid

		if answer:
			net.SendChatPacket("/party_request_accept " + str(vid))
		else:
			net.SendChatPacket("/party_request_deny " + str(vid))

		self.partyRequestQuestionDialog.Close()
		self.partyRequestQuestionDialog = None

	def __PartyRequestDenied(self):
		self.PopupMessage(localeInfo.PARTY_REQUEST_DENIED)

	def __EnableTestServerFlag(self):
		app.EnableTestServerFlag()

	def __InGameShop_Show(self, url):
		if constInfo.IN_GAME_SHOP_ENABLE:
			self.interface.OpenWebWindow(url)

	# WEDDING
	def __LoginLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLoginLover()

	def __LogoutLover(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.OnLogoutLover()

		if self.affectShower:
			self.affectShower.HideLoverState()

		self.interface.RepositionGroup(self.affectShower.GetBottom())

	def __LoverNear(self):
		if self.affectShower:
			self.affectShower.ShowLoverState()

		self.interface.RepositionGroup(self.affectShower.GetBottom())

	def __LoverFar(self):
		if self.affectShower:
			self.affectShower.HideLoverState()

		self.interface.RepositionGroup(self.affectShower.GetBottom())

	def __LoverDivorce(self):
		if self.interface.wndMessenger:
			self.interface.wndMessenger.ClearLoverInfo()
		if self.affectShower:
			self.affectShower.ClearLoverState()

		self.interface.RepositionGroup(self.affectShower.GetBottom())

	def __PlayMusic(self, flag, filename):
		flag = int(flag)
		if flag:
			snd.FadeOutAllMusic()
			musicInfo.SaveLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + filename)
		else:
			snd.FadeOutAllMusic()
			musicInfo.LoadLastPlayFieldMusic()
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

	if app.ENABLE_REFINE_MSG_ADD:
		def BINARY_RefineFailedTypeMessage(self, type, autoReopen):
			REFINE_FAILURE_DICT = {
				player.REFINE_FAIL_GRADE_DOWN: localeInfo.REFINE_FAILURE_GRADE_DOWN,
				player.REFINE_FAIL_DEL_ITEM:   localeInfo.REFINE_FAILURE_DEL_ITEM,
				player.REFINE_FAIL_KEEP_GRADE: localeInfo.REFINE_FAILURE_KEEP_GRADE,
				player.REFINE_FAIL_MAX:        localeInfo.REFINE_FAILURE
			}

			snd.PlaySound("sound/ui/jaeryun_fail.wav")
			if autoReopen:
				chat.AppendChat(chat.CHAT_TYPE_INFO, REFINE_FAILURE_DICT.get(type, player.REFINE_FAIL_MAX))
			else:
				self.PopupMessage(REFINE_FAILURE_DICT.get(type, player.REFINE_FAIL_MAX))

	if app.ENABLE_TREASURE_BOX_LOOT:
		def BINARY_AppendTreasureBoxLoot(self, *args):
			itemVnum = args[0]

			if len(args) == 1:
				GetWindowConfig("system", "treasure_box", "EMPTY_TREASURE_BOX_VNUM").append(itemVnum)
				chat.AppendChat(1, localeInfo.LACK_OF_INFORMATION)
			else:
				GetWindowConfig("system", "treasure_box", "TREASURE_BOX_ITEMS")[itemVnum] = args[1]
				self.interface.OpenBoxLootWindow(itemVnum)

	if app.ENABLE_TARGET_MONSTER_LOOT:
		def BINARY_AddDropInfo(self, race, vnum, count, minLevel, maxLevel, pct):
			if not race in constInfo.DROP_INFO:
				constInfo.DROP_INFO[race] = []

			item.SelectItem(vnum)
			if item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_ARMOR):
				ovnum = vnum
				vnum = vnum - (vnum % 10)

				idx = -1
				i = 0
				for info in constInfo.DROP_INFO[race]:
					if info.has_key('BASE_VNUM') and info['BASE_VNUM'] == vnum:
						idx = i
						break
					i += 1

				if idx == -1:
					constInfo.DROP_INFO[race].append({
						'LEVEL_RANGE': (minLevel, maxLevel),
						'COUNT': count,
						'VNUM': (ovnum, ovnum),
						'BASE_VNUM' : vnum,
						'PCT' : pct / 100
					})
				else:
					constInfo.DROP_INFO[race][idx]['VNUM'] = (
						min(constInfo.DROP_INFO[race][idx]['VNUM'][0], ovnum),
						max(constInfo.DROP_INFO[race][idx]['VNUM'][1], ovnum)
					)
			else:
				constInfo.DROP_INFO[race].append({
					'LEVEL_RANGE': (minLevel, maxLevel),
					'COUNT': count,
					'VNUM': vnum,
					'PCT': pct / 100
				})

		def BINARY_RefreshDropInfo(self):
			self.targetBoard.RefreshTargetInfo()

	if app.ENABLE_DELETE_SINGLE_STONE:
		def BINARY_RemoveStoneSetItem(self, itemCell):
			self.interface.RemoveStoneSetItem(itemCell)

		def BINARY_CloseRemoveStoneWindow(self):
			self.interface.CloseRemoveStoneWindow()

	if gcGetEnable("ENABLE_ITEM_HIGHLIGHT_"):
		def	__Item_HightLight__(self, iSlot, bAdd, bPersisting = 0):
			self.interface.wndInventory.EFFECT_SLOTS[int(iSlot)] = (bool(int(bAdd)), bool(int(bPersisting)))
			self.RefreshInventory()

	if app.ENABLE_SWITCHBOT:
		def RefreshSwitchbotWindow(self):
			self.interface.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			self.interface.RefreshSwitchbotItem(slot)

	if app.ENABLE_RENEWAL_EXCHANGE:
		def OnRecvExchangeInfo(self, unixTime, isError, info):
			if isError == 1:
				error = True
			else:
				error = False

			self.interface.ExchangeInfo(unixTime, info, error)

	if app.ENABLE_GAYA_SYSTEM:
		def	OpenGayaCrafting(self):
			self.uigayasystem["CRAFTING"].Open()

		def	GayaAddItem(self, id, vnum, count, price, status):
			self.uigayasystem["MARKET"].UpdateGayaSlot(int(id), int(vnum), int(count), int(price), int(status))

		def	RequestGayaMarket(self):
			if not self.uigayasystem["MARKET"].IsShow():
				net.SendChatPacket("/open_gaya_shop")

		def	GayaRotationTime(self, tm):
			self.uigayasystem["MARKET"].SetNextRotationTime(int(tm))

		def	GayaEraseDesc(self):
			self.uigayasystem["MARKET"].Clear()

		def	GayaOpenInterface(self):
			self.uigayasystem["MARKET"].Open()

	if app.ENABLE_VOICE_CHAT:
		def OnRecvVoice(self, sender, distance, object):
			if self.interface.wVoiceChat:
				self.interface.wVoiceChat.addAudio(sender, object, distance)

	if app.SKILL_COOLTIME_UPDATE:
		def	SkillClearCoolTime(self, slotIndex):
			self.interface.SkillClearCoolTime(slotIndex)

	if app.ENABLE_FAST_REFINE_OPTION:
		def CloseRefineDialog(self):
			self.interface.CloseRefinedDialog()

	if gcGetEnable("EVENT_MANAGER_ENABLE"):
		def	__Event_Manager_OpenPanel__(self):
			self.uieventmanager_panel.Open()

		def	__Event_Manager_BroadcastStatus__(self, e_key, e_time):
			self.uieventmanager_panel.UpdateEventElement(e_key, int(e_time))

		def	__Event_Manager_UpdateEvent__(self, e_key, e_time, e_status):
			if int(e_status) > 0:
				self.uieventmanager.AddEvent(e_key, e_time.replace("_", " "))
			else:
				self.uieventmanager.RemoveEvent(e_key)

	if app.ENABLE_CHANGE_CHANNEL:
		def UpdateChannelInfo(self, channelID):
			cfg.Set(cfg.SAVE_GENERAL, "channel_", int(channelID) - 1)

			import introInterface
			net.SetServerInfo("|cFFFF8C00{} |cFFFFFFFF- |cFFFFD700CH{}".format(introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "serverinfo")[0], channelID))
			self.interface.wndMiniMap.RefreshServerInfo(channelID)

	if gcGetEnable("ENABLE_TECHNICAL_MAINTENANCE"):
		def	__TechnicalMaintenanceOpenPanel__(self):
			self.uitechnicalmaintenance["PANEL"].Open()

		def __TechnicalMaintenanceInfo__(self, sRsn, sTimeoutFormatted):
			## Panel update
			self.uitechnicalmaintenance["PANEL"].RecvUpdate(sRsn, sTimeoutFormatted)

			## Alert update
			self.uitechnicalmaintenance["ALERT"].RecvUpdate(sRsn, sTimeoutFormatted)

	if app.ENABLE_ADMIN_MANAGER:
		def BINARY_AdminInit(self):
			self.interface.AdminManager_Init()

		def BINARY_AdminPlayerOnline(self, pid):
			self.interface.AdminManager_PlayerOnline(pid)

		def BINARY_AdminPlayerOffline(self, pid):
			self.interface.AdminManager_PlayerOffline(pid)

		def BINARY_AdminPlayerRefreshGMItemTradeOption(self):
			self.interface.AdminManager_RefreshGMItemTradeOption()

		def BINARY_AdminMapViewerStart(self):
			self.interface.AdminManager_RefreshMapViewer()

		def BINARY_AdminObserverStart(self):
			self.interface.AdminManager_StartObserver()

		def BINARY_AdminObserverRefresh(self):
			self.interface.AdminManager_Refresh()

		def BINARY_AdminObserverRefreshSkill(self):
			self.interface.AdminManager_RefreshSkill()

		def BINARY_AdminObserverPointChange(self):
			self.interface.AdminManager_PointChange()

		def BINARY_AdminObserverRefreshInventory(self, pageIndex):
			self.interface.AdminManager_RefreshInventory(pageIndex)

		def BINARY_AdminObserverRefreshEquipment(self):
			self.interface.AdminManager_RefreshEquipment()

		def BINARY_AdminBanChatUpdate(self, pid):
			self.interface.AdminManager_RefreshBanChatPlayer(pid)

		def BINARY_AdminBanChatSearchResult(self, success):
			self.interface.AdminManager_ChatSearchResult(success)

		def BINARY_AdminBanAccountUpdate(self, aid):
			self.interface.AdminManager_RefreshBanAccount(aid)

		def BINARY_AdminBanAccountSearchResult(self, success):
			self.interface.AdminManager_AccountSearchResult(success)

		def BINARY_AdminBanLoadLog(self):
			self.interface.AdminManager_LoadBanLog()

		def BINARY_AdminItemLoadResult(self):
			self.interface.AdminManager_LoadItemResult()

		def BINARY_AdminHackLogsLoadResult(self):
			self.interface.AdminManager_LoadHackLogResult()

	if gcGetEnable("ENABLE_NOTIFICATON_SENDER"):
		## Panel
		def	__GMIdleOpenInterface__(self):
			self.uigmidleinterface["PANEL"].Show()

		def	__GMIdleSendCollectionCount__(self, count):
			self.uigmidleinterface["PANEL"].UpdateCollectionCount(int(count))

		def	__GMIdleSendPlayerName__(self, p_name):
			self.uigmidleinterface["PANEL"].AddNewPlayer(p_name)

		def	__GMIdleUpdateAllPlayerStatus__(self, status):
			self.uigmidleinterface["PANEL"].UpdateAllPlayerStatus(int(status))

		def	__GMIdleErasePlayer__(self, p_name):
			self.uigmidleinterface["PANEL"].ErasePlayer(p_name)

		def	__GMIdleUpdatePlayerStatus__(self, p_name, status):
			self.uigmidleinterface["PANEL"].UpdatePlayerStatus(p_name, int(status))

		## Player
		def	__GMIdleSendNotification__(self):
			self.uigmidleinterface["ANSWER"].Open()

	if app.ZUO_PANEL_ENABLE:
		def	RetZuoMonsters(self, name, vnum):
			self.uizuopaneldialog.AddMonsterName(name, vnum)

		def	UpdateZuoDialogElement(self, key, value):
			self.uizuopaneldialog.UpdateElement(key, value)

		def	ZuoMenuDialog(self):
			self.uizuopaneldialog.UpdateWindow()

	if app.ENABLE_MARBLE_CREATOR_SYSTEM:
		def BINARY_MarbleManagerOpen(self):
			self.interface.ToggleMarbleManager()

		def BINARY_MarbleManagerUpdate(self):
			self.interface.MarbleManagerUpdate()

	if app.SHIP_DEFEND_DUNGEON:
		def	__Ship_Defend_Dungeon_Open__(self):
			self.uishipdefenddungeon.Show()

		def	__Ship_Defend_Dungeon_Update__(self, perc):
			self.uishipdefenddungeon.UpdateGauge(int(perc))

	if app.BATTLE_PASS_ENABLE:
		def	__BATTLE_PASS__ClearInterface(self):
			self.interface.wndBattlePass.ClearInteface()

		def __BATTLE_PASS__BasicInfo(self, iDiff, iCurrentDT, iFinished, iCollected):
			self.interface.wndBattlePass.RegisterBasicInfo(int(iDiff)-1, int(iCurrentDT), int(iFinished), int(iCollected))

			## Data were broadcasted, showing button
			self.interface.BattlePass_ShowToggleButton()

		def __BATTLE_PASS__MajorReward(self, iVnum, iCount):
			self.interface.wndBattlePass.RegisterMajorReward(int(iVnum), int(iCount))

		def __BATTLE_PASS__TaskInfo(self, sTitle, sDesc, iProgress, iTaskID):
			self.interface.wndBattlePass.RegisterTaskData(sTitle, sDesc, int(iProgress), int(iTaskID))

		def __BATTLE_PASS__TaskReward(self, iTaskID, iVnum, iCount):
			self.interface.wndBattlePass.RegisterTaskReward(int(iTaskID), int(iVnum), int(iCount))

		def __BATTLE_PASS__HighScore(self, iID, sName, iDt):
			self.interface.wndBattlePass.RegisterHighScore(int(iID), sName, int(iDt))

	if app.ENABLE_TRANSMUTATION_SYSTEM:
		def	Transmutation_Open(self):
			self.interface.Transmutation_UpdateWindow()

		def	UpdateTransmutationSlot(self, id, item):
			self.interface.Transmutation_UpdateItem(id, item)

		def SetNewTransMutationItem(self, pos):
			self.interface.Transmutation_GUI.Cancel()
			self.interface.wndInventory.New_Trans_Item = pos
			self.interface.wndInventory.RefreshBagSlotWindow()

	if app.ENABLE_CUBE_RENEWAL:
		def BINARY_Cube_Open(self, npcVnum):
			self.interface.OpenCubeWindow(npcVnum)

		def BINARY_Cube_Close(self):
			self.interface.CloseCubeWindow()

		def BINARY_Cube_Make(self, type, arg):
			CUBE_CRAFT_DICT = [
				localeInfo.CUBE_CRAFT_END,
				localeInfo.CUBE_CRAFT_NOT_ENOUGH_MONEY,
				localeInfo.CUBE_CRAFT_NOT_ENOUGH_OBJECT,
				localeInfo.CUBE_CRAFT_CREATE_ITEM,
				localeInfo.CUBE_CRAFT_INVENTORY_FULL,
				localeInfo.CUBE_CRAFT_SUCCES,
			]

			self.interface.RefreshCubeWindow()

			if self.craftFailPopupDialog:
				if self.craftFailPopupDialog.IsShow():
					self.craftFailPopupDialog.Close()

				if (type == 2 or type == 3) and arg:
					item.SelectItem(arg)
					self.craftFailPopupDialog.SetText(CUBE_CRAFT_DICT[type] % item.GetIconImageFileName())
				elif type == 5:
					if arg:
						self.craftFailPopupDialog.SetText(CUBE_CRAFT_DICT[type] % arg)
					else:
						self.craftFailPopupDialog.SetText(localeInfo.CUBE_CRAFT_FAIL)
				else:
					self.craftFailPopupDialog.SetText(CUBE_CRAFT_DICT[type])

				self.craftFailPopupDialog.SetAutoClose()
				#self.craftFailPopupDialog.AutoResize(45)
				self.craftFailPopupDialog.Open()

	if app.ENABLE_FIND_LETTERS_EVENT:
		def BINARY_OpenFindLetters(self):
			if self.interface:
				self.interface.OpenFindLettersEvent()

		def BINARY_AddFindLetters(self, iPos, iAsciiChar, iIsFilled):
			if self.interface:
				self.interface.AddFindLetters(int(iPos), int(iAsciiChar), int(iIsFilled))

		def BINARY_FindLettersIcon(self, isShow):
			if self.interface:
				self.interface.FindLettersIcon(int(isShow))

		def BINARY_FindLettersFinishEvent(self):
			if self.interface:
				self.interface.FindLettersFinishEvent()

		def BINARY_AddFindLettersReward(self, iPos, itemVnum, itemCount):
			if self.interface:
				self.interface.AddFindLettersReward(iPos, itemVnum, itemCount)

	if app.ENABLE_REFINE_ELEMENT:
		def BINARY_RefineElementProcess(self, refineType, srcCell, dstCell):
			if refineType == item.REFINE_ELEMENT_TYPE_UPGRADE_SUCCES:
				self.PopupMessage(localeInfo.REFINE_ELEMENT_UPGRADE_SUCCESS_TEXT)
			elif refineType == item.REFINE_ELEMENT_TYPE_UPGRADE_FAIL:
				self.PopupMessage(localeInfo.REFINE_ELEMENT_UPGRADE_FAIL_TEXT)
			elif refineType == item.REFINE_ELEMENT_TYPE_DOWNGRADE_SUCCES:
				self.PopupMessage(localeInfo.REFINE_ELEMENT_DOWNGRADE_TEXT)
			elif refineType == item.REFINE_ELEMENT_TYPE_CHANGE_SUCCES:
				elementRefine = player.GetItemRefineElement(dstCell)
				dstVnum = player.GetItemIndex(dstCell)
				elementType = -1
				itemName = ""
				if elementRefine:
					elementType = int(elementRefine / 100000000) - 1

				if dstVnum:
					item.SelectItem(dstVnum)
					itemName = item.GetItemName()

				elementNameByType = {
					chrmgr.REFINE_ELEMENT_CATEGORY_ELECT : uiScriptLocale.REFINE_ELEMENT_CHANGE_ELECT,
					chrmgr.REFINE_ELEMENT_CATEGORY_FIRE : uiScriptLocale.REFINE_ELEMENT_CHANGE_FIRE,
					chrmgr.REFINE_ELEMENT_CATEGORY_ICE : uiScriptLocale.REFINE_ELEMENT_CHANGE_ICE,
					chrmgr.REFINE_ELEMENT_CATEGORY_WIND : uiScriptLocale.REFINE_ELEMENT_CHANGE_WIND,
					chrmgr.REFINE_ELEMENT_CATEGORY_EARTH : uiScriptLocale.REFINE_ELEMENT_CHANGE_EARTH,
					chrmgr.REFINE_ELEMENT_CATEGORY_DARK : uiScriptLocale.REFINE_ELEMENT_CHANGE_DARK,
				}

				if itemName != "" and elementType != -1 and elementNameByType.has_key(elementType):
					self.PopupMessage(localeInfo.REFINE_ELEMENT_CHANGE_TEXT % (itemName, elementNameByType[elementType]))
			else:
				if self.interface:
					self.interface.RefineElementProcess(refineType, srcCell, dstCell)

	if app.ENABLE_SOUL_SYSTEM:
		def __RefineSoulSuceededMessage(self):
			snd.PlaySound("sound/ui/make_soket.wav")
			self.PopupMessage(localeInfo.SOUL_REFINE_SUCCESS)

		def __RefineSoulFailedMessage(self):
			snd.PlaySound("sound/ui/jaeryun_fail.wav")
			self.PopupMessage(localeInfo.SOUL_REFINE_FAILURE)

	if app.ENABLE_LUCKY_BOX:
		def BINARY_OpenLuckyBox(self):
			if self.interface:
				self.interface.OpenLuckyBox()

		def BINARY_RefreshLuckyBox(self):
			if self.interface:
				self.interface.RefreshLuckyBox()

		def BINARY_CloseLuckyBox(self):
			if self.interface:
				self.interface.CloseLuckyBox()

	if app.OX_EVENT_SYSTEM_ENABLE:
		def	RetOxItems(self, name, vnum):
			self.uioxdialog.AddItemName(name, vnum)

		def	UpdateAttendersCount(self, key, value):
			self.uioxdialog.UpdateAttendersCount(key, value)

		def	OxMenuDialog(self):
			self.uioxdialog.UpdateWindow()

		def	UpdateOXQuestionPool(self, key, name, q_count):
			print key, name, q_count
			if int(key) == 0:
				return

			if int(key) == -1:
				self.uioxdialog.UpdateAttendersCount("PoolCount", int(q_count))
			else:
				self.uioxdialog.poolDialog.AddPool(int(key)-1, name, int(q_count))

	if app.ENABLE_PASSIVE_SKILLS_HELPER:
		def __SKILLS_MANAGER__ClearInterface(self):
			constInfo.PASSIVE_SKILLS_DATA = {}

		def __SKILLS_MANAGER__RegisterInformation(self, iKey, iMaxLevel, iCurrent, iRequired):
			if int(iKey) not in constInfo.PASSIVE_SKILLS_DATA:
				constInfo.PASSIVE_SKILLS_DATA[int(iKey)] = {}

			constInfo.PASSIVE_SKILLS_DATA[int(iKey)] = { "MaxLv" : int(iMaxLevel), "Curr" : int(iCurrent), "Req" : int(iRequired) }

	if app.ENABLE_SAVE_POSITIONS_SYSTEM:
		def Positions_Initialize(self, bCount):
			self.interface.wndPositionManager.MAX_PAGE_COUNT = int(bCount)

		def Positions_ClearInterface(self):
			self.interface.wndPositionManager.ClearInterface()

		def Positions_AppendData(self, iPos, iMapIndex, iLocalX, iLocalY, iGlobalX, iGlobalY):
			self.interface.wndPositionManager.AppendData(int(iPos), int(iMapIndex), int(iLocalX), int(iLocalY), int(iGlobalX), int(iGlobalY))

	if app.ENABLE_TELEPORT_SYSTEM:
		def __BINARY__TeleportManager_Clear(self):
			self.interface.uiTeleportManagerDialog.OnRecvClear()

		def __BINARY__TeleportManager_Category(self, sHash):
			self.interface.uiTeleportManagerDialog.OnRecvCategory(sHash)

		def __BINARY__TeleportManager_Item(self, bCategoryID, sCategoryName, sHash):
			self.interface.uiTeleportManagerDialog.OnRecvItem(int(bCategoryID), sCategoryName, sHash)

		def __BINARY__TeleportManager_Show(self):
			self.interface.uiTeleportManagerDialog.UpdateWindow()

	if app.INGAME_WIKI:
		def ToggleWikiWindow(self):
			if not self.wndWiki:
				return

			if self.wndWiki.IsShow():
				self.wndWiki.Hide()
			else:
				self.wndWiki.Show()
				self.wndWiki.SetTop()

	if gcGetEnable("ENABLE_SKILL_SELECT"):
		def __RecvSkillSelect(self, byRace):
			if self.interface and self.interface.wndSkillSelect:
				self.interface.wndSkillSelect.AddData(byRace)

	if app.INGAME_ITEMSHOP_ENABLE:
		def	__BINARY__ItemShopClear(self):
			self.interface.uiItemShopDialog.OnRecvClear()

		def	__BINARY__ItemShopCategory(self, sHash, sHasNew):
			self.interface.uiItemShopDialog.OnRecvCategory(sHash, sHasNew)

		def	__BINARY__ItemShopItem(self, bCategoryID, sHashOld, sHashNew):
			self.interface.uiItemShopDialog.OnRecvItem(int(bCategoryID), sHashOld, sHashNew)

		def	__BINARY__ItemShopUpdateCash(self, iCash):
			self.interface.uiItemShopDialog.OnRecvCashUpdate(int(iCash))

		def	__BINARY__ItemShopPromos(self, sHashOld, sHashNew):
			self.interface.uiItemShopDialog.OnRecvSpecialOfferUpdate(sHashOld, sHashNew)

		def	__BINARY__ItemShopSpecialOffer(self, sHashOld, sHashNew):
			self.interface.uiItemShopDialog.OnRecvSpecialOfferUpdate(sHashOld, sHashNew)

		def	__BINARY__ItemShopShow(self):
			self.interface.uiItemShopDialog.UpdateWindow()

	if app.TOMBOLA_EVENT_ENABLE:
		def	__TOMBOLA__TombolaStatus(self, bStatus):
			if int(bStatus) > 0:
				self.interface.wndOverLayButtons.AddButton("button_tombola")
			else:
				self.interface.wndOverLayButtons.RemoveButton("button_tombola")

		def	__TOMBOLA__TombolaItem(self, iSlot, iVnum, iCount):
			self.interface.wndOverLayButtons.uiTombola.RecvTombolaItem(int(iSlot), int(iVnum), int(iCount))

		def	__TOMBOLA__TombolaSpin(self, iReward):
			self.interface.wndOverLayButtons.uiTombola.RecvTombolaStartSpin(int(iReward))

		def	__TOMBOLA__TombolaUserBalance(self, iBalance):
			self.interface.wndOverLayButtons.uiTombola.RecvUpdateBalance(int(iBalance))

		def	__TOMBOLA__TombolaOpenDialog(self):
			pass

	if gcGetEnable("ENABLE_ADMIN_BAN_PANEL"):
		def	__OpenBanPanel(self):
			self.uibanpanel.Open()

	if gcGetEnable("ENABLE_SKILLS_INFORMATION"):
		def __BINARY__SkillInformationExorcism(self, bActive):
			constInfo.SKILL_EXO = int(bActive)

		def __BINARY__SkillInformationClear(self):
			constInfo.SKILL_INFO = {}

		def __BINARY__SkillInformation(self, iNormalSkill, iIndex, iGrade, iReaded, iRequired, iPercent, iPercentAdd, iTime):
			if int(iIndex) not in constInfo.SKILL_INFO:
				constInfo.SKILL_INFO[int(iIndex)] = []

			constInfo.SKILL_INFO[int(iIndex)].append({
				'STANDARD' : int(iNormalSkill),
				'GRADE' : int (iGrade),
				'READED' : int(iReaded),
				'REQUIRED' : int(iRequired),
				'PERCENT' : int(iPercent),
				'APERCENT' : int (iPercentAdd),
				'TIME' : int(iTime) + app.GetTime()
			})

	if gcGetEnable("ENABLE_LEGENDARY_STONES"):
		def __BINARY__LEGENDARY_STONES_OPEN(self, sKey, iValue):
			if self.interface.wndLegendaryStones[sKey]:
				self.interface.wndLegendaryStones[sKey].UpdateWindow(int(iValue))

		def __BINARY__LEGENDARY_STONES_CONFIGURATION(self, sKey, *args):
			if self.interface.wndLegendaryStones[sKey]:
				self.interface.wndLegendaryStones[sKey].SetConfiguration(args)

		def __BINARY__LEGENDARY_STONES_CLEAR(self, sKey):
			if self.interface.wndLegendaryStones[sKey]:
				self.interface.wndLegendaryStones[sKey].Clear()

		def __BINARY__LEGENDARY_STONES_SET_ITEM(self, sKey, *args):
			if self.interface.wndLegendaryStones[sKey]:
				self.interface.wndLegendaryStones[sKey].RegisterData(args)

	if gcGetEnable("ENABLE_DUNGEON_INFORMATION"):
		def	__DUNGEON_INFO__OpenPanel(self):
			self.interface.wndDungeonInfo.UpdateWindow()

		def	__DUNGEON_INFO__BroadcastGlobal(self, sName, sTitle, dwRaceFlag, bPartyCount, wRequiredLevel, wRequiredMaxLevel, dwPassItem, iDelay):
			self.interface.wndDungeonInfo.RecvGlobalData(sName.replace("|", " "), sTitle.replace("|", " "), int(dwRaceFlag), int(bPartyCount), int(wRequiredLevel), int(wRequiredMaxLevel), int(dwPassItem), int(iDelay))

		def	__DUNGEON_INFO__BroadcastPersonal(self, sName, eType, iRes, iDelay):
			self.interface.wndDungeonInfo.RecvPersonalData(sName.replace("|", " "), int(eType), int(iRes), int(iDelay))

		def	__DUNGEON_INFO__BroadcastHighscore(self, sName, iType, wPos, sPlayerName, wLevel, lValue):
			self.interface.wndDungeonInfo.RecvHighscoreData(sName.replace("|", " "), int(iType), int(wPos), sPlayerName, int(wLevel), long(lValue))

		def	__DUNGEON_INFO__RecvHighscoreDataClear(self, sName):
			self.interface.wndDungeonInfo.RecvHighscoreClear(sName)

	if gcGetEnable("ENABLE_DUNGEON_TASK_INFORMATION"):
		def DUNGEON_TASK_SetDungeon(self, iMapIndex):
			self.uiDungeonTask.RecvSetDungeon(int(iMapIndex))

		def	DUNGEON_TASK_TaskInfo(self, iNum, sTitle):
			self.uiDungeonTask.RecvTaskInfo(int(iNum), sTitle)
			self.uiDungeonTask.Show()
			if self.interface:
				self.interface.wndMiniMap.ManageButtonsOnMiniMap()

			if self.targetBoard.IsShow():
				self.targetBoard.UpdatePosition(50)

		def	DUNGEON_TASK_SetGlobalTimer(self, iElapse):
			self.uiDungeonTask.RecvGlobalTimer(int(iElapse))

		def	DUNGEON_TASK_SetCurrentTask(self, iNum, sDesc, iCount, iProgress):
			self.uiDungeonTask.RecvSetCurrentTask(int(iNum), sDesc.replace("|", " "), int(iCount), int(iProgress))

		def	DUNGEON_TASK_EndDungeon(self):
			self.uiDungeonTask.RecvEndDungeon()
			if self.interface:
				self.interface.wndMiniMap.ManageButtonsOnMiniMap(False)

		def	DUNGEON_TASK_SetLocalTimer(self, iElapse):
			self.uiDungeonTask.RecvSetLocalTimer(int(iElapse))

		def	DUNGEON_TASK_UpdateCounter(self, iCount):
			self.uiDungeonTask.RecvUpdateCounter(int(iCount))

		def	DUNGEON_TASK_UpdateProgress(self, iProgress):
			self.uiDungeonTask.RecvUpdateProgress(int(iProgress))

	if app.SASH_ABSORPTION_ENABLE:
		def	__Sash_Combination_Open(self):
			self.uisashsystem["COMBINATION"].Open()

		def	__Sash_Combination_Update_Slot(self, slot_num, vnum, slot_inv):
			self.uisashsystem["COMBINATION"].UpdateSlot(int(slot_num), int(vnum), int(slot_inv))
			self.RefreshInventory()

		def	__Sash_Combination_UpdateCost(self, cost):
			self.uisashsystem["COMBINATION"].UpdateCost(int(cost))

		def	__Sash_Combination_Clear(self):
			self.uisashsystem["COMBINATION"].Clear()
			self.RefreshInventory()

		def	__Sash_Combination_Close(self):
			self.uisashsystem["COMBINATION"].Clear()
			self.uisashsystem["COMBINATION"].Hide()
			self.RefreshInventory()

		def	__Sash_Absorption_Open(self):
			self.uisashsystem["ABSORPTION"].Open()

		def	__Sash_Absorption_Update_Slot(self, slot_num, vnum, slot_inv):
			self.uisashsystem["ABSORPTION"].UpdateSlot(int(slot_num), int(vnum), int(slot_inv))
			self.RefreshInventory()

		def	__Sash_Absorption_Clear(self):
			self.uisashsystem["ABSORPTION"].Clear()
			self.RefreshInventory()

		def	__Sash_Absorption_Close(self):
			self.uisashsystem["ABSORPTION"].Clear()
			self.uisashsystem["ABSORPTION"].Hide()
			self.RefreshInventory()

		def	__Sash_Inventory_Refresh(self):
			self.RefreshInventory()

		### Additional ###
		def	__SashCombination_RequestOpen(self):
			net.SendChatPacket("/open_sash_combination")

		def	__SashAbsorption_RequestOpen(self):
			net.SendChatPacket("/open_sash_absorption")

	if gcGetEnable("ENABLE_EQUIPMENT_LOCK_SLOT"):
		def EQUIPMENT_LOCK_Clear(self):
			constInfo.EQUIPMENT_LOCK_INFO = {}

		def EQUIPMENT_LOCK_Info(self, dwVnum, iSlot, bStatus):
			if int(iSlot) not in constInfo.EQUIPMENT_LOCK_INFO:
				constInfo.EQUIPMENT_LOCK_INFO[int(iSlot)] = {}

			constInfo.EQUIPMENT_LOCK_INFO[int(iSlot)] = {
				"ITEM" : int(dwVnum),
				"SLOT" : int(iSlot),
				"STATUS" : int(bStatus)
				}

	if gcGetEnable("ENABLE_HIDE_COSTUMES"):
		def HCOSTUMES_Info(self, sType, iStatus):
			lInstance = interfaceModule.GetInstance()
			if not lInstance:
				return

			rConfig = lInstance.wndInventory.wndCostume.COSTUME_CONFIGURATION.get(sType, None)
			if not rConfig:
				return

			rConfig["STATUS"] = bool(int(iStatus))

			lInstance.wndInventory.wndCostume.RefreshHButton(sType, False)

	if app.ENABLE_AMULET_SYSTEM:
		def __AmuletInformation_UpgradeClear(self):
			self.interface.wndAmuletSystem["INFORMATION"].OnRecvUpgradeClear()

		def __AmuletInformation_UpgradeInfo(self, iVnum, iCount):
			self.interface.wndAmuletSystem["INFORMATION"].OnRecvUpgradeInfo(int(iVnum), int(iCount))

		def __AmuletCrafting_Open(self, iVnum):
			self.interface.wndAmuletSystem["CRAFTING"].OnRecvRegisterReward(int(iVnum))
			self.interface.wndAmuletSystem["CRAFTING"].Open()

		def __AmuletPassive_Info(self, iLevel, iFirst, iSecond, iThird, iFourth):
			if int(iLevel) not in constInfo.AMULET_PASSIVE:
				constInfo.AMULET_PASSIVE[int(iLevel)] = []

			constInfo.AMULET_PASSIVE[int(iLevel)] = [iFirst, iSecond, iThird, iFourth]

		def __AmuletCombine_Open(self, iRequiredVnum):
			self.interface.wndAmuletSystem["COMBINATION"].RegisterAdditional(int(iRequiredVnum))
			self.interface.wndAmuletSystem["COMBINATION"].Open()

		def __AmuletCombine_RegisterItem(self, iSlotNum, iItemSlot, iVnum = -1):
			self.interface.wndAmuletSystem["COMBINATION"].RegisterItem(int(iSlotNum), int(iItemSlot), int(iVnum))

		def __AmuletCombine_RegisterChance(self, iChance):
			self.interface.wndAmuletSystem["COMBINATION"].RegisterChance(int(iChance))

		def __AmuletCombine_RegisterGold(self, iGold):
			self.interface.wndAmuletSystem["COMBINATION"].RegisterGold(int(iGold))

		def __AmuletCombine_Reset(self):
			self.interface.wndAmuletSystem["COMBINATION"].Reset()

	if (gcGetEnable("ENABLE_SHAMAN_SYSTEM")):
		def __ShamanSystem__RegisterSkillCount(self, iCount):
			self.interface.RegisterShamansSlots(int(iCount))

		def __ShamanSystem__RegisterSkill(self, iKey, iType, iLevel, fPower):
			self.interface.RegisterShamanSkill(int(iKey), int(iType), int(iLevel), float(fPower))

		def __ShamanSystem__RegisterPremium(self, bPremium):
			self.interface.RegisterShamanPremium(bPremium)

		def __ShamanSystem_Open(self):
			pass

		def __ShamanSystem__UnregisterShaman(self):
			self.interface.UnregisterShamanSystem()

	if (gcGetEnable("POPUP_SYSTEM_ENABLE")):
		def __RECV__PopupMessageAppend(self, sHeader, sTxt, sIcon):
			try:
				sIcon = int(sIcon)
			except:
				pass
			
			self.uiPopupSystem.RecvPopupCommand(sHeader, sTxt, sIcon if sIcon != "EMPTY" else "")

	if (gcGetEnable("MISSION_MANAGER")):
		def __MisionManager__Clear(self):
			self.interface.MissionManagerClear()

		def __MisionManager__TaskInfo(self, iKey, iTime, iTaskID, iProgress, dwEnemy, iCount):
			self.interface.MissionManagerRegisterTask(int(iKey), int(iTime), int(iTaskID), int(iProgress), int(dwEnemy), int(iCount))

		def __MisionManager__TaskRefresh(self, iKey, iTaskID, iProgress):
			self.interface.MissionManagerRefreshTask(int(iKey), int(iTaskID), int(iProgress))

		def __MisionManager__RewardInfo(self, iKey, iTaskID, iPos, iVnum, iCount):
			self.interface.MissionManagerRegisterReward(int(iKey), int(iTaskID), int(iPos), int(iVnum), int(iCount))

		def __MisionManager__Refresh(self):
			self.interface.MissionManagerRefresh()


	if (gcGetEnable("ATTENDANCE_MANAGER")):
		def __AttendanceManager__Status(self, bStatus):
			if int(bStatus) > 0:
				self.interface.wndOverLayButtons.AddButton("button_attendance")
			else:
				self.interface.wndOverLayButtons.RemoveButton("button_attendance")

		def __AttendanceManager__Clear(self):
			self.interface.interfaceWindowList["attendance_manager"].OnRecvClear()

		def __AttendanceManager__BasicInfo(self, eMonth, iCurDay):
			self.interface.interfaceWindowList["attendance_manager"].OnRecvBasic(int(eMonth), int(iCurDay))

		def __AttendanceManager_Item(self, iKey, bCollected, iRewardVnum, iRewardCount, eType):
			self.interface.interfaceWindowList["attendance_manager"].OnRecvObject(int(iKey), int(bCollected), int(iRewardVnum), int(iRewardCount), int(eType))

		def __AttendanceManager_RefreshItem(self, iKey, bCollected):
			self.interface.interfaceWindowList["attendance_manager"].OnRecvRefreshObject(int(iKey), int(bCollected))

		def __AttendanceManager__Refresh(self):
			self.interface.interfaceWindowList["attendance_manager"].OnRecvRefresh()

	if app.ENABLE_BIOLOG_SYSTEM:
		def __BiologManager__RegisterProgress(self, iKey, iCollected, tTime, bReminder):
			self.interface.BiologManagerRegisterProgress(int(iKey), int(iCollected), int(tTime), int(bReminder))

		def __BiologManager__RegisterMission(self, iLevel, iVnum, iCount, iChance):
			self.interface.BiologManagerRegisterMission(int(iLevel), int(iVnum), int(iCount), int(iChance))
		
		def __BiologManager__RegisterRewardBasic(self, iVnum, iCount, bSelector):
			self.interface.BiologManagerRegisterRewardBasic(int(iVnum), int(iCount), int(bSelector))
		
		def __BiologManager__RegisterRewardAffect(self, sKey, iKey, iType, iValue):
			self.interface.BiologManagerRegisterRewardAffect(sKey, int(iKey), int(iType), int(iValue))

		def __BiologManager__RequestOpen(self, sKey, iKey):
			self.interface.BiologManagerRequestOpen(sKey, int(iKey))

		def __BiologManager__RequestClose(self, sKey):
			self.interface.BiologManagerRequestClose(sKey)

		def __BiologManager__RequestClear(self, sKey):
			self.interface.BiologManagerRequestClear(sKey)

		def __BiologManager__RegisterSet(self, iKey, bFinished, bSelector, iVnum, iLevel):
			self.interface.BiologManagerRegisterSet(int(iKey), int(bFinished), int(bSelector), int(iVnum), int(iLevel))

		def __BiologManager__RegisterSetAffect(self, iKey, iApplyKey, bSelected, iApplyType, iApplyValue):
			self.interface.BiologManagerRegisterSetAffect(int(iKey), int(iApplyKey), int(bSelected), int(iApplyType), int(iApplyValue))

		def __BiologManager__ClearSet(self):
			self.interface.BiologManagerClearSet()

		def __BiologManager__OpenSet(self):
			self.interface.BiologManagerOpenSet()

	if (gcGetEnable("MOB_TRACKER")):
		def __MobTracker__Clear(self):
			sys_err("Elo")
			self.interface.interfaceWindowList["mob_tracker"].ClearSet()

		def __MobTracker__Register(self, iKey, iID, iCooldown, iDelay, x, y):
			self.interface.interfaceWindowList["mob_tracker"].RegisterSet(int(iKey), int(iID), int(iCooldown), int(iDelay) + app.GetTime(), (int(x), int(y)))

		def __MobTracker__Open(self):
			self.interface.interfaceWindowList["mob_tracker"].Open()
			
	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def OpenPrivateShopPanel(self):
			if self.interface:
				self.interface.OpenPrivateShopPanel()
			
		def ClosePrivateShopPanel(self):
			if self.interface:
				self.interface.ClosePrivateShopPanel()
			
		def RefreshPrivateShopWindow(self):
			if self.interface:
				self.interface.RefreshPrivateShopWindow()
			
		def OpenPrivateShopSearch(self, mode):
			self.interface.OpenPrivateShopSearch(mode)
			
		def PrivateShopSearchRefresh(self):
			if self.interface:
				self.interface.PrivateShopSearchRefresh()

		def PrivateShopSearchUpdate(self, index, state):
			if self.interface:
				self.interface.PrivateShopSearchUpdate(index, state)
			
		def AppendMarketItemPrice(self, gold, cheque):
			if self.interface:
				self.interface.AppendMarketItemPrice(gold, cheque)

		def AddPrivateShopTitleBoard(self, vid, text, type):
			if self.interface:
				self.interface.AddPrivateShopTitleBoard(vid, text, type)

		def RemovePrivateShopTitleBoard(self, vid):
			if self.interface:
				self.interface.RemovePrivateShopTitleBoard(vid)

		def SetPrivateShopPremiumBuild(self):
			if self.interface:
				self.interface.SetPrivateShopPremiumBuild()
				
		def PrivateShopStateUpdate(self):
			if self.interface:
				self.interface.PrivateShopStateUpdate()

	def ShowLoadingImage(self):
		self.interface.interfaceWindowList["loading_window"].Open()

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def __SetBuffNPCSummon(self):
			self.interface.BuffNPC_Summon()
			
		def __SetBuffNPCUnsummon(self):
			self.interface.BuffNPC_Unsummon()
			
		def __SetBuffNPCClear(self):
			self.interface.BuffNPC_Clear()

		def __SetBuffNPCBasicInfo(self, name, sex, intvalue):
			self.interface.BuffNPC_SetBasicInfo(str(name), int(sex), int(intvalue))
			
		def __SetBuffNPCEXPInfo(self, level, cur_exp, exp):
			self.interface.BuffNPC_SetEXPInfo(level, cur_exp, exp)

		def __SetBuffNPCSkillInfo(self, skill1, skill2, skill3, skill4, skill5, skill6, skillpoints):
			self.interface.BuffNPC_SetSkillInfo(skill1, skill2, skill3, skill4, skill5, skill6, int(skillpoints))
			
		def __SetBuffNPCSkillUseStatus(self, slot0, slot1, slot2, slot3, slot4, slot5):
			self.interface.BuffNPC_SkillUseStatus(slot0, slot1, slot2, slot3, slot4, slot5)
			
		def __SetBuffNPCSkillSetSkillCooltime(self, slot, timevalue):
			self.interface.BuffNPC_SetSkillCooltime(slot, timevalue)
			
		def __SetBuffNPCCreatePopup(self, type, value0, value1):
			self.interface.BuffNPC_CreatePopup(int(type), int(value0), int(value1))
			
		def BINARY_OpenCreateBuffWindow(self):
			self.interface.BuffNPC_OpenCreateWindow()

	if app.ENABLE_ANTI_MULTIPLE_FARM:
		def BINARY_RecvAntiFarmReload(self):
			if not self.interface:
				return
			self.interface.SendAntiFarmReload()
	if app.GLOBAL_RANKING_ENABLE:
		def __Global_Ranking__RecvData(self, iCategory, iNum, sName, iEmpire, lScore):
			if lScore.find(".00") != -1:
				lScore = int(float(lScore))
			else:
				lScore = float(lScore)

			self.interface.wndInventory.wndGlobalRankingWindow.UpdateRankingData(int(iCategory), int(iNum), sName, int(iEmpire), lScore)

		def __Global_Ranking__RecvSelfData(self, iCategory, iPos, sName, iEmpire, lScore):
			if lScore.find(".00") != -1:
				lScore = int(float(lScore))
			else:
				lScore = float(lScore)

			self.interface.wndInventory.wndGlobalRankingWindow.UpdateRankingData_Self(int(iCategory), int(iPos), sName, int(iEmpire), lScore)

