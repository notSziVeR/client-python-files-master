import net
import app
import ui
import uiOption

import uiSystemOption
import uiGameOption
import uiScriptLocale
import networkModule
import constInfo
import localeInfo

import musicInfo
import snd
import systemSetting
import background

import playerSettingModule
import chrmgr

import player

import chat

import dbg
import cfg

import uiCommon

MUSIC_FILENAME_MAX_LEN = 25
CAMERA_MAX_DISTANCE_SHORT = 2500.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LONGEST = 5000.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG, CAMERA_MAX_DISTANCE_LONGEST]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_SHORT

cameraDict = [
	'2500.0',
	'3500.0',
	'5000.0'
]

ENVIRONMENT_NIGHT = "d:/ymir work/environment/moonlight04.msenv"
nightDict = [
	uiScriptLocale.GAME_REFACTORED_OPTIONS_DAY,
	uiScriptLocale.GAME_REFACTORED_OPTIONS_NIGHT
]

switchDict = [
	uiScriptLocale.GAME_REFACTORED_OPTIONS_ON,
	uiScriptLocale.GAME_REFACTORED_OPTIONS_OFF
]

switchDict2 = [
	uiScriptLocale.GAME_REFACTORED_OPTIONS_OFF,
	uiScriptLocale.GAME_REFACTORED_OPTIONS_ON
]

pvpModeDict = [
	uiScriptLocale.OPTION_PVPMODE_PEACE,
	uiScriptLocale.OPTION_PVPMODE_REVENGE,
	uiScriptLocale.OPTION_PVPMODE_GUILD,
	uiScriptLocale.OPTION_PVPMODE_FREE
]

blockMode = 0

###################################################################################################
## System
class MainOptions(ui.ScriptWindow):

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__Initialize()

	def __Initialize(self):
		self.ActivePage = 0
		self.Pages = []
		self.SubPages = []
		self.PageButtons = []
		self.ChannelButtons = []

		self.HideEffectsButtons = []
		self.HideObjectsButtons = []

		self.BlockButton = []

		self.wndWiki = None

	def LoadDialog(self):
		self.__LoadWindow()
		self.__CreateSelectors()

	def __LoadWindow(self):
		try:
			ui.PythonScriptLoader().LoadScriptFile(self, "uiscript/RefactoredOptions.py")

		except KeyError, msg:
			dbg.TraceError("MainOptions #1")

		try:
			self.__BindObjects()

		except KeyError, msg:
			dbg.TraceError("MainOptions #2 - %s" % str(msg))

		try:
			self.__BindEvents()

		except KeyError, msg:
			dbg.TraceError("MainOptions #3 - %s" % str(msg))

		self.OpenPage(0)

	def __CreateSelectors(self):
		fileNameList = app.GetFileList("BGM/*."+"mp3")

		self.selectorObjects = {}
		self.selectors       = {
			"MusicButton"            : [5, self.SelectorButtons["MusicButton"].GetWidth(), self.SelectorButtons["MusicButton"].GetHeight(), self.SubPages[0], self.__OnSelectMusicFromList, dict(enumerate(fileNameList))],
			"SelectCameraButton"     : [3, self.SelectorButtons["SelectCameraButton"].GetWidth(), self.SelectorButtons["SelectCameraButton"].GetHeight(), self.SubPages[1], self.__OnSelectCameraDistance, dict(enumerate(cameraDict))],
			"SelectNightButton"      : [2, self.SelectorButtons["SelectNightButton"].GetWidth(), self.SelectorButtons["SelectNightButton"].GetHeight(), self.SubPages[1], self.__OnSelectNightMode, dict(enumerate(nightDict))],
			"SelectFogButton"        : [2, self.SelectorButtons["SelectFogButton"].GetWidth(), self.SelectorButtons["SelectFogButton"].GetHeight(), self.SubPages[1], self.__OnSelectFogMode, dict(enumerate(switchDict))],
			"SelectModelButton"      : [2, self.SelectorButtons["SelectModelButton"].GetWidth(), self.SelectorButtons["SelectModelButton"].GetHeight(), self.SubPages[2], self.__OnSelectModelMode, dict(enumerate(switchDict2))],
			"SelectNoticeButton"     : [2, self.SelectorButtons["SelectNoticeButton"].GetWidth(), self.SelectorButtons["SelectNoticeButton"].GetHeight(), self.SubPages[2], self.__OnSelectNoticeMode, dict(enumerate(switchDict))],
			"SelectChatLineButton"   : [2, self.SelectorButtons["SelectChatLineButton"].GetWidth(), self.SelectorButtons["SelectChatLineButton"].GetHeight(), self.SubPages[3], self.__OnSelectChatLineMode, dict(enumerate(switchDict))],
			"SelectNamesButton"      : [2, self.SelectorButtons["SelectNamesButton"].GetWidth(), self.SelectorButtons["SelectNamesButton"].GetHeight(), self.SubPages[3], self.__OnSelectNameMode, dict(enumerate(switchDict))],
			"SelectAttackInfoButton" : [2, self.SelectorButtons["SelectAttackInfoButton"].GetWidth(), self.SelectorButtons["SelectAttackInfoButton"].GetHeight(), self.SubPages[3], self.__OnSelectAttackInfoMode, dict(enumerate(switchDict))],
			"SelectAnimateWindowButton" : [2, self.SelectorButtons["SelectAnimateWindowButton"].GetWidth(), self.SelectorButtons["SelectAnimateWindowButton"].GetHeight(), self.SubPages[3], self.__OnSelectAnimateMode, dict(enumerate(switchDict2))],
			"SelectPvPButton"        : [4, self.SelectorButtons["SelectPvPButton"].GetWidth(), self.SelectorButtons["SelectPvPButton"].GetHeight(), self.SubPages[4], self.__OnSelectPvPMode, dict(enumerate(pvpModeDict))],
			"SelectWNDPositionButton": [2, self.SelectorButtons["SelectWNDPositionButton"].GetWidth(), self.SelectorButtons["SelectWNDPositionButton"].GetHeight(), self.SubPages[5], self.__OnSelectWNDPositionMode, dict(enumerate(switchDict2))],
		}

		for key in self.selectors:
			val            = self.selectors[key]
			selectorObject = SuggestionSelector(val[0], val[1], val[2])
			selectorObject.SetParent(val[3])
			selectorObject.SetSelectEvent(val[4])
			selectorObject.SetAttributeDict(val[5])
			selectorObject.Hide()

			self.selectorObjects[key] = selectorObject

	def __BindObjects(self):
		GetObject = self.GetChild
		GetObject("board").SetCloseEvent(ui.__mem_func__(self.Close))

		for _ in range(2):
			self.Pages.append(GetObject("Page_{}".format(_)))
			self.PageButtons.append(GetObject("Button_Page_{}".format(_)))

		for _ in range(6):
			self.SubPages.append(GetObject("SubPage_{}".format(_)))

		for _ in range(5):
			self.ChannelButtons.append(GetObject("Channel_{}".format(_ + 1)))

		self.SelectorButtons = {
			"MusicButton"            : GetObject("SelectMusicButton"),
			"SelectCameraButton"     : GetObject("SelectCameraButton"),
			"SelectNightButton"      : GetObject("SelectNightButton"),
			"SelectFogButton"        : GetObject("SelectFogButton"),
			"SelectModelButton"      : GetObject("SelectModelButton"),
			"SelectNoticeButton"     : GetObject("SelectNoticeButton"),
			"SelectChatLineButton"   : GetObject("SelectChatLineButton"),
			"SelectNamesButton"      : GetObject("SelectNamesButton"),
			"SelectAttackInfoButton" : GetObject("SelectAttackInfoButton"),
			"SelectAnimateWindowButton" : GetObject("SelectAnimateWindowButton"),
			"SelectPvPButton"        : GetObject("SelectPvPButton"),
			"SelectWNDPositionButton": GetObject("SelectWNDPositionButton"),
		}

		self.main = {
			"firstPage" : {
				"music" : {
					"MusicVolumeData": GetObject("MusicVolume_Data"),
					"MusicVolumeDown": GetObject("MusicVolumeDown"),
					"MusicVolumeUp"  : GetObject("MusicVolumeUp"),
				},
				"effect" : {
					"EffectsVolumeData": GetObject("EffectVolume_Data"),
					"EffectsVolumeDown": GetObject("EffectVolumeDown"),
					"EffectsVolumeUp"  : GetObject("EffectVolumeUp"),
				},
			},
		}

		for _ in range(3):
			self.HideEffectsButtons.append(GetObject("Hide_Effects_Button_{}".format(_)))
			self.HideObjectsButtons.append(GetObject("Hide_Objects_Button_{}".format(_)))

		for _ in range(6):
			self.BlockButton.append(GetObject("Block_Button_{}".format(_)))

		GetObject("change_button").SAFE_SetEvent(self.__ClickChangeCharacterButton)
		GetObject("logout_button").SAFE_SetEvent(self.__ClickLogOutButton)
		GetObject("exit_button").SAFE_SetEvent(self.__ClickExitButton)

	def __BindEvents(self):
		for _ in range(2):
			self.PageButtons[_].SetEvent(ui.__mem_func__(self.OpenPage), _)

		for _ in range(5):
			self.ChannelButtons[_].SetEvent(ui.__mem_func__(self.ChangeChannel), _)

		self.SelectorButtons["MusicButton"].SAFE_SetEvent(self.__OnClickSelector, "MusicButton")
		self.SelectorButtons["SelectCameraButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectCameraButton")
		self.SelectorButtons["SelectNightButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectNightButton")
		self.SelectorButtons["SelectFogButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectFogButton")
		self.SelectorButtons["SelectModelButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectModelButton")
		self.SelectorButtons["SelectNoticeButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectNoticeButton")
		self.SelectorButtons["SelectChatLineButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectChatLineButton")
		self.SelectorButtons["SelectNamesButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectNamesButton")
		self.SelectorButtons["SelectAttackInfoButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectAttackInfoButton")
		self.SelectorButtons["SelectAnimateWindowButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectAnimateWindowButton")
		self.SelectorButtons["SelectPvPButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectPvPButton")
		self.SelectorButtons["SelectWNDPositionButton"].SAFE_SetEvent(self.__OnClickSelector, "SelectWNDPositionButton")

		wndMusic = self.main["firstPage"]["music"]
		wndMusic["MusicVolumeDown"].SetEvent(ui.__mem_func__(self.SetVolumeMusic), -10)
		wndMusic["MusicVolumeUp"].SetEvent(ui.__mem_func__(self.SetVolumeMusic), 10)

		wndEffect = self.main["firstPage"]["effect"]
		wndEffect["EffectsVolumeDown"].SetEvent(ui.__mem_func__(self.SetVolumeEffects), -1)
		wndEffect["EffectsVolumeUp"].SetEvent(ui.__mem_func__(self.SetVolumeEffects), 1)

		for _ in xrange(3):
			self.HideEffectsButtons[_].SetToggleDownEvent(self.__OnClickHideEffects, True, _)
			self.HideEffectsButtons[_].SetToggleUpEvent(self.__OnClickHideEffects, False, _)

			self.HideObjectsButtons[_].SetToggleDownEvent(self.__OnClickHideButtonSet, _)
			self.HideObjectsButtons[_].SetToggleUpEvent(self.__OnClickHideButtonDel, _)

		for _ in xrange(6):
			self.BlockButton[_].SetToggleUpEvent(ui.__mem_func__(self.__OnClickBlockButton), _)
			self.BlockButton[_].SetToggleDownEvent(ui.__mem_func__(self.__OnClickBlockButton), _)

	def OpenPage(self, idx):
		for i in range(2):
			if i == idx:
				self.PageButtons[i].Disable()
				self.LoadPageData(i)
				self.Pages[i].Show()
			else:
				self.PageButtons[i].Enable()
				self.Pages[i].Hide()

		self.ActivePage = idx

	def LoadPageData(self, idx):
		self.AppendChannel()

		if idx == 0:
			if musicInfo.fieldMusic==musicInfo.METIN2THEMA:
				self.SelectorButtons["MusicButton"].SetText(localeInfo.MUSIC_METIN2_DEFAULT_THEMA)
			else:
				self.SelectorButtons["MusicButton"].SetText(musicInfo.fieldMusic[:MUSIC_FILENAME_MAX_LEN])

			actualCameraDistance = cfg.Get(cfg.SAVE_OPTION, "DISTANCE", str(CAMERA_MAX_DISTANCE))
			self.SelectorButtons["SelectCameraButton"].SetText(str(actualCameraDistance))

			actualTime = cfg.Get(cfg.SAVE_OPTION, "ENV_MODE", "0")
			self.SelectorButtons["SelectNightButton"].SetText(nightDict[int(actualTime)])

			actualFog = cfg.Get(cfg.SAVE_OPTION, "FOG_MODE", "0")
			self.SelectorButtons["SelectFogButton"].SetText(switchDict[int(actualFog)])

			actualModel = cfg.Get(cfg.SAVE_OPTION, "MODEL_MODE", "1")
			self.SelectorButtons["SelectModelButton"].SetText(switchDict2[int(actualModel)])

			actualNotice = cfg.Get(cfg.SAVE_OPTION, "NOTICE_MODE", "0")
			self.SelectorButtons["SelectNoticeButton"].SetText(switchDict[int(actualNotice)])

			self.main["firstPage"]["music"]["MusicVolumeData"].SetText(str(int(float(systemSetting.GetMusicVolume()) * 100 )))
			self.main["firstPage"]["effect"]["EffectsVolumeData"].SetText(str(float(systemSetting.GetSoundVolume())))

			self.RefreshHideEffects()

			for _ in xrange(3):
				if systemSetting.IsHideObjects(self._GetHideObjectByIndex(_)):
					self.HideObjectsButtons[_].Down()

		if idx == 1:
			actualNotice = cfg.Get(cfg.SAVE_OPTION, "CHAT_LINE_MODE", "0")
			self.SelectorButtons["SelectChatLineButton"].SetText(switchDict[int(actualNotice)])

			actualName = cfg.Get(cfg.SAVE_OPTION, "NAME_MODE", "0")
			self.SelectorButtons["SelectNamesButton"].SetText(switchDict[int(actualName)])

			actualAttackInfo = cfg.Get(cfg.SAVE_OPTION, "ATTACK_MODE", "0")
			self.SelectorButtons["SelectAttackInfoButton"].SetText(switchDict[int(actualAttackInfo)])

			actualAnimateInfo = cfg.Get(cfg.SAVE_OPTION, "ANIMATION_MODE", "1")
			self.SelectorButtons["SelectAnimateWindowButton"].SetText(switchDict2[int(actualAnimateInfo)])

			self.__SetPeaceMPKMode()

			self.RefreshBlock()

			actualSavePosition = int(cfg.Get(cfg.SAVE_OPTION, "save_wnd_pos", "0"))
			self.SelectorButtons["SelectWNDPositionButton"].SetText(switchDict2[actualSavePosition])

			# self.__UpdateIgnoring()

	def AppendChannel(self, bCheck = False, Idx = -1):
		if bCheck and Idx != -1:
			for _ in range(5):
				if _ == Idx:
					self.ChannelButtons[_].Disable()
				else:
					self.ChannelButtons[_].Enable()
		else:
			channel = int(cfg.Get(cfg.SAVE_GENERAL, "channel_", 0))

			for _ in range(5):
				if _ == channel:
					self.ChannelButtons[_].Disable()
				else:
					self.ChannelButtons[_].Enable()

	def ChangeChannel(self, idx):
		net.SendChatPacket("/channel {}".format(idx + 1))
		self.AppendChannel(True, idx)
		self.__SaveChannelInfo(idx + 1)
		self.Close()

	def __SaveChannelInfo(self, channel):
		loadRegionID, loadServerID, loadChannelID = self.__LoadChannelInfo()
		try:
			file = open("channel.inf", "w")
			file.write("%d %d %d" % (loadServerID, channel, loadRegionID))
		except:
			print "MoveChannelDialog.__SaveChannelInfo - SaveError"

	def __LoadChannelInfo(self):
		try:
			file = open("channel.inf")
			lines = file.readlines()

			if len(lines) > 0:
				tokens = lines[0].split()

				selServerID = int(tokens[0])
				selChannelID = int(tokens[1])

				if len(tokens) == 3:
					regionID = int(tokens[2])

				return regionID, selServerID, selChannelID
		except:
			print "MoveChannelDialog.__LoadChannelInfo - OpenError"
			return -1, -1, -1

	def __OnClickSelector(self, selector):
		if self.selectorObjects[selector].IsShow():
			self.selectorObjects[selector].Hide()

		else:
			x,y =  self.SelectorButtons[selector].GetLocalPosition()
			y +=  self.SelectorButtons[selector].GetHeight()

			self.selectorObjects[selector].SetPosition(x,y)
			self.selectorObjects[selector].Show()

	def __OnSelectMusicFromList(self, index):
		fileNameList=app.GetFileList("BGM/*."+"mp3")
		fileName = fileNameList[index]
		self.SelectorButtons["MusicButton"].SetText(fileName)

		if musicInfo.fieldMusic != "":
			snd.FadeOutMusic("BGM/"+ musicInfo.fieldMusic)

		if fileName==localeInfo.MUSIC_METIN2_DEFAULT_THEMA:
			musicInfo.fieldMusic=musicInfo.METIN2THEMA
		else:
			musicInfo.fieldMusic=fileName

		musicInfo.SaveLastPlayFieldMusic()

		if musicInfo.fieldMusic != "":
			snd.FadeInMusic("BGM/" + musicInfo.fieldMusic)

		self.selectorObjects["MusicButton"].Hide()

	def SetVolumeMusic(self, diff):
		b = int(float(systemSetting.GetMusicVolume()) * 100)
		volume = b + diff
		volume = min(max(0, volume), 100)

		snd.SetMusicVolume(volume / 100.0)
		systemSetting.SetMusicVolume(volume / 100.0)

		self.main["firstPage"]["music"]["MusicVolumeData"].SetText(str(volume))

	def __map(self, value, min1, max1, min2, max2):
		lm = max1 - min1
		rm = max2 - min2

		factor = float(rm) / float(lm)

		return min2 + factor * (value - min1)

	def SetVolumeEffects(self, diff):
		current_volume = float(systemSetting.GetSoundVolume())

		changed_volume = current_volume + float(diff)
		changed_volume = max(min(changed_volume, 5.0), 0.0)

		target_volume = self.__map(changed_volume, 0.0, 5.0, 0.0, 1.0)

		snd.SetSoundVolumef(target_volume)
		systemSetting.SetSoundVolumef(target_volume)

		self.main["firstPage"]["effect"]["EffectsVolumeData"].SetText(str(changed_volume))

	def __OnSelectCameraDistance(self, index):
		CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_LIST[index]

		cfg.Set(cfg.SAVE_OPTION, "DISTANCE", str(CAMERA_MAX_DISTANCE))
		app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

		self.SelectorButtons["SelectCameraButton"].SetText(str(CAMERA_MAX_DISTANCE))

		self.selectorObjects["SelectCameraButton"].Hide()

	def __OnSelectNightMode(self, index):
		cfg.Set(cfg.SAVE_OPTION, "ENV_MODE", index)

		if index == 0:
			background.SetEnvironmentData(0)
		else:
			background.RegisterEnvironmentData(1, ENVIRONMENT_NIGHT)
			background.SetEnvironmentData(1)

		self.SelectorButtons["SelectNightButton"].SetText(nightDict[index])
		self.selectorObjects["SelectNightButton"].Hide()

	def __OnSelectFogMode(self, index):
		cfg.Set(cfg.SAVE_OPTION, "FOG_MODE", index)

		if index == 0:
			background.SetEnvironmentFog(True)
		else:
			background.SetEnvironmentFog(False)

		self.SelectorButtons["SelectFogButton"].SetText(switchDict[index])
		self.selectorObjects["SelectFogButton"].Hide()

	def __OnSelectModelMode(self, index):
		cfg.Set(cfg.SAVE_OPTION, "MODEL_MODE", index)

		chrmgr.ClearRaceNameCache()
		# import playerLoad
		# playerLoad.ReloadNPC()
		systemSetting.ReloadInstance(index)

		self.SelectorButtons["SelectModelButton"].SetText(switchDict2[index])
		self.selectorObjects["SelectModelButton"].Hide()

	def RefreshHideEffects(self):
		if systemSetting.IsHideEffects(systemSetting.HIDE_EFFECTS_GENERAL):
			self.HideEffectsButtons[0].Down()
			chrmgr.ShowHideEffectById(0, True)
		else:
			self.HideEffectsButtons[0].SetUp()
			chrmgr.ShowHideEffectById(0, False)

		skillId = [ 15, 16, 19, 20, 21, 25, 43, 44 ]
		if systemSetting.IsHideEffects(systemSetting.HIDE_EFFECTS_SKILLS):
			self.HideEffectsButtons[1].Down()
			for id in skillId:
				chrmgr.ShowHideEffectById(id, True)
		else:
			self.HideEffectsButtons[1].SetUp()
			for id in skillId:
				chrmgr.ShowHideEffectById(id, False)

		buffId = [ 22, 23, 29, 30 ]
		if systemSetting.IsHideEffects(systemSetting.HIDE_EFFECTS_BUFFS):
			self.HideEffectsButtons[2].Down()
			for id in buffId:
				chrmgr.ShowHideEffectById(id, True)
		else:
			self.HideEffectsButtons[2].SetUp()
			for id in buffId:
				chrmgr.ShowHideEffectById(id, False)

	def __OnClickHideEffects(self, isHide, effectType):
		flagList = [ systemSetting.HIDE_EFFECTS_GENERAL, systemSetting.HIDE_EFFECTS_SKILLS, systemSetting.HIDE_EFFECTS_BUFFS ]

		if effectType < len(flagList):
			systemSetting.SetHideEffectsFlag(flagList[effectType], isHide)

		self.RefreshHideEffects()

	def __OnClickHideButtonSet(self, index):
		a = self._GetHideObjectByIndex(index)
		systemSetting.SetHideObjectsFlag(a, 1)

	def __OnClickHideButtonDel(self, index):
		a = self._GetHideObjectByIndex(index)
		systemSetting.SetHideObjectsFlag(a, 0)

	def _GetHideObjectByIndex(self, index):
		valData = [systemSetting.HIDE_OBJECTS_MOUNTS, systemSetting.HIDE_OBJECTS_PETS, systemSetting.HIDE_OBJECTS_SHOPS]

		return valData[index]

	def __OnSelectNoticeMode(self, index):
		cfg.Set(cfg.SAVE_OPTION, "NOTICE_MODE", index)

		self.SelectorButtons["SelectNoticeButton"].SetText(switchDict[index])
		self.selectorObjects["SelectNoticeButton"].Hide()

	def __OnSelectChatLineMode(self, index):
		cfg.Set(cfg.SAVE_OPTION, "CHAT_LINE_MODE", index)

		if index == 0:
			systemSetting.SetViewChatFlag(1)
		else:
			systemSetting.SetViewChatFlag(0)

		self.SelectorButtons["SelectChatLineButton"].SetText(switchDict[index])
		self.selectorObjects["SelectChatLineButton"].Hide()

	def __OnSelectNameMode(self, index):
		cfg.Set(cfg.SAVE_OPTION, "NAME_MODE", index)

		if index == 0:
			systemSetting.SetAlwaysShowNameFlag(True)
		else:
			systemSetting.SetAlwaysShowNameFlag(False)

		self.SelectorButtons["SelectNamesButton"].SetText(switchDict[index])
		self.selectorObjects["SelectNamesButton"].Hide()

	def __OnSelectAttackInfoMode(self, index):
		cfg.Set(cfg.SAVE_OPTION, "ATTACK_MODE", index)

		if index == 0:
			systemSetting.SetShowDamageFlag(True)
		else:
			systemSetting.SetShowDamageFlag(False)

		self.SelectorButtons["SelectAttackInfoButton"].SetText(switchDict[index])
		self.selectorObjects["SelectAttackInfoButton"].Hide()

	def __OnSelectAnimateMode(self, index):
		cfg.Set(cfg.SAVE_OPTION, "ANIMATION_MODE", index)

		self.SelectorButtons["SelectAnimateWindowButton"].SetText(switchDict2[index])
		self.selectorObjects["SelectAnimateWindowButton"].Hide()

	def __CheckPvPProtectedLevelPlayer(self):
		if player.GetStatus(player.LEVEL) < constInfo.PVPMODE_PROTECTED_LEVEL:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_PROTECT % (constInfo.PVPMODE_PROTECTED_LEVEL))
			return 1

		return 0

	def __SetPeaceMPKMode(self):
		self.__SetPKMode(player.PK_MODE_PEACE)

	def __SetPKMode(self, index):
		self.SelectorButtons["SelectPvPButton"].SetText(pvpModeDict[index])

	def __OnSelectPvPMode(self, index):
		if self.__CheckPvPProtectedLevelPlayer():
			return

		pvpDict = [
			player.PK_MODE_PEACE,
			player.PK_MODE_REVENGE,
			player.PK_MODE_GUILD,
			player.PK_MODE_FREE
		]

		if pvpDict[index] == player.PK_MODE_GUILD:
			if 0 == player.GetGuildID():
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_CANNOT_SET_GUILD_MODE)
				return

		if constInfo.PVPMODE_ENABLE:
			net.SendChatPacket("/pkmode %i" % pvpDict[index], chat.CHAT_TYPE_TALKING)
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.OPTION_PVPMODE_NOT_SUPPORT)

		self.__SetPKMode(index)
		self.selectorObjects["SelectPvPButton"].Hide()

	def __OnClickBlockButton(self, blockIdx):
		self.RefreshBlock()
		global blockMode
		blockIdxDict = [
			player.BLOCK_EXCHANGE,
			player.BLOCK_PARTY,
			player.BLOCK_GUILD,
			player.BLOCK_WHISPER,
			player.BLOCK_FRIEND,
			player.BLOCK_PARTY_REQUEST
		]

		net.SendChatPacket("/setblockmode " + str(blockMode ^ blockIdxDict[blockIdx]))

	def RefreshBlock(self):
		global blockMode
		for i in xrange(len(self.BlockButton)):
			if 0 != (blockMode & (1 << i)):
				self.BlockButton[i].Down()
			else:
				self.BlockButton[i].SetUp()

	def OnBlockMode(self, mode):
		global blockMode
		blockMode = mode
		self.RefreshBlock()

	def OnCloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog = None

	def __OnSelectWNDPositionMode(self, index):
		cfg.Set(cfg.SAVE_OPTION, "save_wnd_pos", index)

		self.SelectorButtons["SelectWNDPositionButton"].SetText(switchDict2[index])
		self.selectorObjects["SelectWNDPositionButton"].Hide()

	def Destroy(self):
		self.ClearDictionary()

		self.__Initialize()

	def OpenDialog(self):
		self.OpenPage(self.ActivePage)
		self.Show()
		self.SetCenterPosition()
		self.SetTop()

	def __ClickChangeCharacterButton(self):
		self.Close()

		net.ExitGame()

	def __OnClosePopupDialog(self):
		self.popup = None

	def __ClickLogOutButton(self):
		self.Close()
		net.LogOutGame()

	def __ClickExitButton(self):
		self.Close()
		net.ExitApplication()

	def Close(self):
		self.Hide()
		return True

	def RefreshMobile(self):
		pass

	def OnMobileAuthority(self):
		pass

	def OnChangePKMode(self):
		pass

	def OnPressExitKey(self):
		self.Close()
		return True

	def OnPressEscapeKey(self):
		self.Close()
		return True

class SuggestionElement(ui.Button):
	def __init__(self):
		self.clickEvent = None
		self.index = 0

		ui.Button.__init__(self)


	def __del__(self):
		self.clickEvent = None
		ui.Button.__del__(self)

	def SetClickEvent(self, event):
		self.clickEvent = event
		self.SAFE_SetEvent(self.__OnClickMe)

	def __OnClickMe(self):
		if self.clickEvent:
			self.clickEvent(self.index)

	def SetElement(self, index, text):
		self.index = index
		self.SetText(text)

class SuggestionSelector(ui.Window):
	def __init__(self, labels, width, height):
		ui.Window.__init__(self)

		self.scrollbar = None
		self.background = None
		self.attributeDict = {}
		self.onSelectEvent = None

		self.MAX_DATA = labels

		self.width = width
		self.height = height

		self.elements = []

		self.__loadBackground()
		self.__loadElements()
		self.__loadScrollbar()

		if app.ENABLE_MOUSE_WHEEL_EVENT:
			## ScrollBar Wheel Support
			self.SetScrollWheelEvent(self.scrollbar.OnWheelMove)

	def __loadBackground(self):
		WINDOW_HEIGHT = self.MAX_DATA * self.height
		bg = ui.Bar("TOP_MOST")
		bg.SetSize(self.width, WINDOW_HEIGHT)
		bg.SetParent(self)
		bg.SetPosition(0, -1)
		bg.Show()

		self.background = bg
		self.SetSize(bg.GetWidth() , bg.GetHeight())

	def __loadElements(self):
		for x in xrange(self.MAX_DATA):
			element = SuggestionElement()
			element.SetParent(self.background)
			element.SetPosition(0, x * 23)

			path = "d:/ymir work/ui/game/refactored_options/"
			element.SetUpVisual(path + "slot_normal.tga")
			element.SetOverVisual(path + "slot_hover.tga")
			element.SetDownVisual(path +"slot_active.tga")

			element.Show()

			element.SetClickEvent(self.__OnSelectAttribute)
			self.elements.append(element)

	def __loadScrollbar(self):
		scroll = ui.NewScrollBar()
		scroll.SetParent(self.background)
		scroll.SetPosition(self.GetWidth()-5, 0)
		scroll.SetScrollBarSize(self.GetHeight()+2)
		scroll.SetScrollEvent(self.__OnScroll)
		scroll.Show()

		self.scrollbar = scroll

	def __OnSelectAttribute(self, index):
		if self.onSelectEvent:
			self.onSelectEvent(index)

	def __OnScroll(self):
		self.__refreshViewList()

	def __refreshViewList(self):
		pos 		= self.scrollbar.GetPos()
		initIndex	= int(pos * (len(self.attributeDict) - len(self.elements) ))

		for x in xrange(initIndex , initIndex + len(self.elements)):
			index 	= self.attributeDict.keys()[x]
			text	= self.attributeDict[index]

			self.elements[x-initIndex].SetElement(index, text)

	def SetAttributeDict(self, dct):
		if len(dct) <= self.MAX_DATA:
			self.scrollbar.Hide()

		self.attributeDict = dct
		self.__refreshViewList()

	def SetSelectEvent(self, event):
		self.onSelectEvent = event

	def __del__(self):
		self.background 	= None
		self.elements		= []
		self.scrollbar		= None
		self.onSelectEvent	= None

		ui.Window.__del__(self)
