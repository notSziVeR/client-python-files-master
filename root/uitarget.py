import app
import ui
import player
import net
import wndMgr
import messenger
import guild
import chr
import nonplayer
import localeInfo
import constInfo

import chrmgr
import grp
import item

import uiToolTip
import chat

import random

from _weakref import proxy

import colorInfo

def FormatRarity(pct):
	if pct == 0 or pct == 1:
		return colorInfo.Colorize(localeInfo.TARGET_INFO_TYPE_MYSTIC, 0xffa135e0)
	elif 1 < pct <= 3:
		return colorInfo.Colorize(localeInfo.TARGET_INFO_TYPE_LEGENDARY, 0xffffd700)
	elif 3 < pct <= 10:
		return colorInfo.Colorize(localeInfo.TARGET_INFO_TYPE_EPIC, 0xff25a7db)
	elif 10 < pct <= 25:
		return colorInfo.Colorize(localeInfo.TARGET_INFO_TYPE_RARE, 0xff1e90ff)
	elif 25 < pct <= 50:
		return colorInfo.Colorize(localeInfo.TARGET_INFO_TYPE_UNCOMMON, 0xff1fc113)
	elif 50 < pct <= 99:
		return colorInfo.Colorize(localeInfo.TARGET_INFO_TYPE_COMMON, 0xffffffff)
	elif pct >= 100:
		return colorInfo.Colorize(localeInfo.TARGET_INFO_TYPE_GUARANTEED, 0xff)

def numberFormat(n, char='.'):
	return '{:,}'.format(n).replace(',', char)

MOB_RACEFLAG = {
					-1 : localeInfo.MOB_RACEFLAG_SPECIAL,
					(1 << 0) : localeInfo.MOB_RACEFLAG_ANIMAL,
					(1 << 1) : localeInfo.MOB_RACEFLAG_UNDEAD,
					(1 << 2) : localeInfo.MOB_RACEFLAG_DEVIL,
					(1 << 3) : localeInfo.MOB_RACEFLAG_HUMAN,
					(1 << 4) : localeInfo.MOB_RACEFLAG_ORC,
					(1 << 5) : localeInfo.MOB_RACEFLAG_MISTIC,
					(1 << 6) : localeInfo.MOB_RACEFLAG_INSECT,
					(1 << 7) : localeInfo.MOB_RACEFLAG_FIREOID,
					(1 << 8) : localeInfo.MOB_RACEFLAG_HUMANOID,
					(1 << 9) : localeInfo.MOB_RACEFLAG_DESERTOID,
					(1 << 10) : localeInfo.MOB_RACEFLAG_TREE,
					(1 << 11) : localeInfo.MOB_RACEFLAG_ELEMENT_ELEC,
					(1 << 12) : localeInfo.MOB_RACEFLAG_ELEMENT_FIRE,
					(1 << 13) : localeInfo.MOB_RACEFLAG_ELEMENT_ICE,
					(1 << 14) : localeInfo.MOB_RACEFLAG_ELEMENT_WIND,
					(1 << 15) : localeInfo.MOB_RACEFLAG_ELEMENT_EARTH,
					(1 << 16) : localeInfo.MOB_RACEFLAG_ELEMENT_DARK,
					(1 << 17) : localeInfo.MOB_RACEFLAG_NONE,
				}

if app.ENABLE_12ZI_ELEMENT_ADD:
	class ElementalImage(ui.Window):

		IMAGE_LIST = {
						nonplayer.RACE_FLAG_ATT_ELEC :	"elect",
						nonplayer.RACE_FLAG_ATT_FIRE :	"fire",
						nonplayer.RACE_FLAG_ATT_ICE :	"ice",
						nonplayer.RACE_FLAG_ATT_WIND :	"wind",
						nonplayer.RACE_FLAG_ATT_EARTH : "earth",
						nonplayer.RACE_FLAG_ATT_DARK :	"dark"
					}
		IMAGE_PATH = "d:/ymir work/ui/game/12zi/element/{}.sub"

		def	__init__(self, parentProxy):
			ui.Window.__init__(self)

			self.windowToolTip = uiToolTip.ToolTip()
			self.iElement = len(MOB_RACEFLAG)-1
			self.parent = proxy(parentProxy)

			self.imgElement = ui.ImageBox()
			self.imgElement.SetParent(self)
			self.imgElement.SetWindowHorizontalAlignCenter()
			self.imgElement.SetWindowVerticalAlignCenter()
			self.imgElement.SetStringEvent("MOUSE_OVER_IN", ui.__mem_func__(self.__OnOverToolTip))
			self.imgElement.SetStringEvent("MOUSE_OVER_OUT", ui.__mem_func__(self.__OnOutToolTip))
			self.imgElement.Show()

		def	__del__(self):
			ui.Window.__del__(self)

			self.imgElement = None
			self.windowToolTip = None

		def	LoadElement(self, iVid):
			(iType, sImage) = self.__ExtractElement(iVid, nonplayer.GetRaceFlag(iVid))
			if len(sImage) == 0:
				print "Element not exists"
				return

			self.iElement = iType
			self.imgElement.LoadImage(self.IMAGE_PATH.format(sImage))
			self.SetSize(self.imgElement.GetWidth() + 4, self.imgElement.GetHeight() + 4)
			self.imgElement.SetPosition(0, 0)

			self.Show()
			self.parent.UpdatePosition()

		def	Close(self):
			self.Hide()
			self.parent.UpdatePosition()

		def	__ExtractElement(self, iVid, dwFlag):
			vnum = nonplayer.GetVnumByVID(iVid)
			if vnum == 0:
				return

			for k, v in self.IMAGE_LIST.items():
				if nonplayer.IsMonsterRaceFlag(vnum, k):
					return (k, v)

			return (-1, "")

		def __getApplys(self, flag):
			if flag in localeInfo.RACE_FLAG_BONUSES:
				return localeInfo.RACE_FLAG_BONUSES[flag]

		def	__OnOverToolTip(self):
			if self.windowToolTip:
				self.windowToolTip.ClearToolTip()

				pkInstance = uiToolTip.GetItemToolTipInstance()
				if not pkInstance:
					return

				for i in xrange(2):
					eApply = self.__getApplys(self.iElement)[i]
					fValue = localeInfo.GetFormattedNumberString(player.GetStatus(item.GetApplyPoint(eApply)))

					sApply = pkInstance.GetAffectString(eApply, fValue, False)
					sApplyColor, sApplyValue = pkInstance.GetAttributeColor(0, player.GetStatus(item.GetApplyPoint(eApply)), eApply, False)
					
					self.windowToolTip.AppendTextLine(pkInstance.GetFormattedColorString(sApply, fValue, sApplyValue, 1), sApplyColor)

				self.windowToolTip.ShowToolTip()

		def	__OnOutToolTip(self):
			if self.windowToolTip:
				self.windowToolTip.HideToolTip()

class TargetBoard(ui.ThinBoard):

	EXCHANGE_LIMIT_RANGE = 3000
	infoBoard = None

	GAUGE_WIDTH = 130
	GAUGE_Y = 20

	def __init__(self, interfaceModule):
		ui.ThinBoard.__init__(self)

		self.interface = interfaceModule

		name = ui.TextLine()
		name.SetParent(self)
		name.SetDefaultFontName()
		name.SetOutline()
		name.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		name.Show()

		bonusName = ui.TextLine()
		bonusName.SetParent(self)
		bonusName.SetWindowHorizontalAlignLeft()
		bonusName.SetHorizontalAlignLeft()
		bonusName.SetWindowVerticalAlignBottom()
		bonusName.SetOutline()
		bonusName.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		bonusName.Hide()
		self.bonusName = bonusName

		hpGauge = ui.Gauge()
		hpGauge.SetParent(self)
		hpGauge.SetPosition(184, self.GAUGE_Y)
		hpGauge.MakeGauge(self.GAUGE_WIDTH, "red")
		hpGauge.SetWindowHorizontalAlignRight()
		hpGauge.Show()

		hpInfo = ui.TextLine()
		hpInfo.SetParent(self)
		hpInfo.SetPosition(119, 4)
		hpInfo.SetOutline(True)
		hpInfo.SetHorizontalAlignCenter()
		hpInfo.SetWindowHorizontalAlignRight()
		hpInfo.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		hpInfo.Show()

		# hpPercent = ui.TextLine()
		# hpPercent.SetParent(self)
		# hpPercent.SetPosition(119, 21)
		# hpPercent.SetOutline(True)
		# hpPercent.SetHorizontalAlignCenter()
		# hpPercent.SetWindowHorizontalAlignRight()
		# hpPercent.SetFontName(localeInfo.UI_DEF_FONT_LARGE)
		# hpPercent.Show()

		closeButton = ui.Button()
		closeButton.SetParent(self)
		closeButton.SetUpVisual("assets/ui/elements/title/buttons/close_norm.tga")
		closeButton.SetOverVisual("assets/ui/elements/title/buttons/close_hover.tga")
		closeButton.SetDownVisual("assets/ui/elements/title/buttons/close_down.tga")
		closeButton.SetPosition(30, 10)
		closeButton.SetWindowHorizontalAlignRight()
		closeButton.SetEvent(ui.__mem_func__(self.OnPressedCloseButton))
		closeButton.Show()

		if app.ENABLE_TARGET_MONSTER_LOOT:
			dropButton = ui.Button()
			dropButton.SetParent(self)
			dropButton.SetUpVisual("assets/ui/elements/title/buttons/info_norm.tga")
			dropButton.SetOverVisual("assets/ui/elements/title/buttons/info_hover.tga")
			dropButton.SetDownVisual("assets/ui/elements/title/buttons/info_down.tga")
			dropButton.SetEvent(lambda: self.ToggleInfoBoard())
			dropButton.SetWindowHorizontalAlignRight()
			dropButton.SetPosition(52, 10)

			dropButton.Hide()

			infoBoard = InfoBoard()
			infoBoard.Hide()

			self.dropButton = dropButton
			self.infoBoard = infoBoard

		self.buttonDict = {}
		self.showingButtonList = []
		for buttonName in (localeInfo.TARGET_BUTTON_WHISPER, localeInfo.TARGET_BUTTON_EXCHANGE, localeInfo.TARGET_BUTTON_FIGHT, localeInfo.TARGET_BUTTON_ACCEPT_FIGHT, localeInfo.TARGET_BUTTON_AVENGE, localeInfo.TARGET_BUTTON_FRIEND, localeInfo.TARGET_BUTTON_INVITE_PARTY, localeInfo.TARGET_BUTTON_LEAVE_PARTY, localeInfo.TARGET_BUTTON_EXCLUDE, localeInfo.TARGET_BUTTON_INVITE_GUILD, localeInfo.TARGET_BUTTON_DISMOUNT, localeInfo.TARGET_BUTTON_EXIT_OBSERVER, localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT, localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY, localeInfo.TARGET_BUTTON_BUILDING_DESTROY, localeInfo.TARGET_BUTTON_EMOTION_ALLOW, "VOTE_BLOCK_CHAT", "Kill", "Kick", "Transfer"):
			button = ui.Button()
			button.SetParent(self)
			button.SetUpVisual("d:/ymir work/ui/public/small_thin_button_01.sub")
			button.SetOverVisual("d:/ymir work/ui/public/small_thin_button_02.sub")
			button.SetDownVisual("d:/ymir work/ui/public/small_thin_button_03.sub")
			button.SetWindowHorizontalAlignCenter()
			button.SetText(buttonName)
			button.Hide()
			self.buttonDict[buttonName] = button
			self.showingButtonList.append(button)

		self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER].SetEvent(ui.__mem_func__(self.OnWhisper))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE].SetEvent(ui.__mem_func__(self.OnExchange))
		self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_ACCEPT_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_AVENGE].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyInvite))
		self.buttonDict[localeInfo.TARGET_BUTTON_LEAVE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyExit))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCLUDE].SetEvent(ui.__mem_func__(self.OnPartyRemove))

		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_GUILD].SAFE_SetEvent(self.__OnGuildAddMember)
		self.buttonDict[localeInfo.TARGET_BUTTON_DISMOUNT].SAFE_SetEvent(self.__OnDismount)
		self.buttonDict[localeInfo.TARGET_BUTTON_EXIT_OBSERVER].SAFE_SetEvent(self.__OnExitObserver)
		self.buttonDict[localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT].SAFE_SetEvent(self.__OnViewEquipment)
		self.buttonDict[localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY].SAFE_SetEvent(self.__OnRequestParty)
		self.buttonDict[localeInfo.TARGET_BUTTON_BUILDING_DESTROY].SAFE_SetEvent(self.__OnDestroyBuilding)
		self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW].SAFE_SetEvent(self.__OnEmotionAllow)

		self.buttonDict["VOTE_BLOCK_CHAT"].SetEvent(ui.__mem_func__(self.__OnVoteBlockChat))
		self.buttonDict["Kill"].SetEvent(self.__OnKill)
		self.buttonDict["Kick"].SetEvent(self.__OnKick)
		self.buttonDict["Transfer"].SetEvent(self.__OnTransfer)

		self.name = name
		self.hpGauge = hpGauge
		self.hpInfo = hpInfo
		# self.hpPercent = hpPercent
		self.closeButton = closeButton
		self.nameString = 0
		self.nameLength = 0
		self.vid = 0
		if gcGetEnable("ENABLE_POISON_GAUGE"):
			self.isPoisoned = False
		self.eventWhisper = None
		self.isShowButton = False

		self.initHP = False

		self.__Initialize()

		if app.ENABLE_12ZI_ELEMENT_ADD:
			self.elementInfo = ElementalImage(self)

		self.ResetTargetBoard()

	def __del__(self):
		ui.ThinBoard.__del__(self)

		print "===================================================== DESTROYED TARGET BOARD"

	def __Initialize(self):
		self.nameString = ""
		self.nameLength = 0
		self.vid = 0
		if gcGetEnable("ENABLE_POISON_GAUGE"):
			self.isPoisoned = False
		self.isShowButton = False

		if self.hpGauge:
			self.hpGauge.SetColor("red")

	def Destroy(self):
		self.Hide()
		self.eventWhisper = None
		self.closeButton = None
		self.showingButtonList = None
		self.buttonDict = None
		self.name = None
		self.bonusName = None
		self.hpGauge = None
		self.hpInfo = None
		# self.hpPercent = None

		if app.ENABLE_12ZI_ELEMENT_ADD:
			self.elementInfo.Hide()
			self.elementInfo = None

		if app.ENABLE_TARGET_MONSTER_LOOT:
			self.dropButton = None
			self.infoBoard = None

		self.__Initialize()

	def OnPressedCloseButton(self):
		player.ClearTarget()
		if self.infoBoard:
			self.infoBoard.Close()
		self.Close()

	def Hide(self):
		if self.infoBoard:
			self.infoBoard.Close()
		ui.ThinBoard.Hide(self)

	def Close(self):
		self.__Initialize()
		if app.ENABLE_TARGET_MONSTER_LOOT:
			self.infoBoard.Close()
		if app.ENABLE_12ZI_ELEMENT_ADD:
			self.elementInfo.Hide()
		self.Hide()

	def Open(self, vid, name):
		if vid:
			if not constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
				if not player.IsSameEmpire(vid):
					self.Hide()
					return

			if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
				if nonplayer.GetVnumByVID(vid) == 10 or nonplayer.GetVnumByVID(vid) == 11:
					self.Hide()
					return

			if vid != self.GetTargetVID():
				self.ResetTargetBoard()
				self.SetTargetVID(vid)
				self.SetTargetName(name)

				if gcGetEnable("ENABLE_POISON_GAUGE"):
					self.CheckPoisoned()

			if player.IsMainCharacterIndex(vid):
				self.__ShowMainCharacterMenu()

			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
				self.Hide()
			else:
				self.isShowButton = True
				self.RefreshButton()
				self.Show()
		else:
			self.HideAllButton()
			self.__ShowButton(localeInfo.TARGET_BUTTON_WHISPER)
			self.__ShowButton("VOTE_BLOCK_CHAT")
			self.__ArrangeButtonPosition()
			self.SetTargetName(name)
			self.Show()

	def Refresh(self):
		if self.IsShow():
			if self.IsShowButton():
				self.RefreshButton()

	def RefreshByVID(self, vid):
		if vid == self.GetTargetVID():
			self.Refresh()

	def RefreshByName(self, name):
		if name == self.GetTargetName():
			self.Refresh()

	def __CanShowMainCharacterMenu(self):
		if player.IsMountingHorse():
			return True

		if player.IsObserverMode():
			return True

		return False

	def __ShowMainCharacterMenu(self):
		hasButton = False

		self.HideAllButton()

		if player.IsMountingHorse():
			self.__ShowButton(localeInfo.TARGET_BUTTON_DISMOUNT)
			hasButton = True

		if player.IsObserverMode():
			self.__ShowButton(localeInfo.TARGET_BUTTON_EXIT_OBSERVER)
			hasButton = True

		self.hpInfo.Hide()
		# self.hpPercent.Hide()
		self.hpGauge.Hide()

		if hasButton:
			self.__ArrangeButtonPosition()
		else:
			self.SetSize(200, self.GetHeight())

		self.UpdatePosition()
		self.Show()

	def __ShowNameOnlyMenu(self):
		self.HideAllButton()

	def SetWhisperEvent(self, event):
		self.eventWhisper = event

	def UpdatePosition(self, y = 10):
		if app.ENABLE_12ZI_ELEMENT_ADD:
			if self.elementInfo.IsShow():
				self.SetPosition(wndMgr.GetScreenWidth()/2 - self.GetWidth()/2 + self.elementInfo.GetWidth(), 10)
				self.elementInfo.SetPosition(self.GetGlobalPosition()[0]-self.elementInfo.GetWidth(), 10 + (self.GetHeight()-self.elementInfo.GetHeight())/2)
				return

		self.SetPosition(wndMgr.GetScreenWidth()/2 - self.GetWidth()/2, y)

	def ResetTargetBoard(self):
		for btn in self.buttonDict.values():
			btn.Hide()

		self.__Initialize()

		self.name.SetPosition(0, 13)
		self.name.SetHorizontalAlignCenter()
		self.name.SetWindowHorizontalAlignCenter()

		self.bonusName.Hide()
		self.hpInfo.Hide()
		# self.hpPercent.Hide()
		self.hpGauge.Hide()

		if app.ENABLE_TARGET_MONSTER_LOOT:
			self.dropButton.Hide()
			self.infoBoard.Close()

		if app.ENABLE_12ZI_ELEMENT_ADD:
			self.elementInfo.Close()

		self.SetSize(250, 42)
		self.UpdatePosition()

	def SetTargetVID(self, vid):
		self.vid = vid

	def SetEnemyVID(self, vid):
		if self.GetTargetVID() == vid:
			return

		self.initHP = True

		self.SetTargetVID(vid)
		if app.ENABLE_12ZI_ELEMENT_ADD:
			self.elementInfo.LoadElement(self.vid)

		name = chr.GetNameByVID(vid)
		race = chr.GetRaceByVID(vid)
		level = nonplayer.GetLevelByVID(vid)

		self.__AppendRace(race)

		nameFront = ""
		if -1 != level:
			nameFront += "|cFF98ff33Lv. " + str(level) + " |r"

		name = nameFront + "|cFFeb1609" + name + "|r"
		self.SetTargetName(name)

		self.SetSize(200 + len(name) * 5, self.GetHeight())
		self.UpdatePosition()

		if chr.IsStone(self.GetTargetVID()) or chr.IsEnemy(self.GetTargetVID()) or player.IsPVPInstance(self.GetTargetVID()):
			self.dropButton.Show()

		if app.ENABLE_TARGET_MONSTER_LOOT:
			if chr.GetInstanceType(self.vid) == chr.INSTANCE_TYPE_PLAYER:
				self.dropButton.Hide()
			else:
				self.dropButton.Show()

	def __AppendRace(self, race):
		raceFlag = nonplayer.GetMonsterRaceFlag(race)

		mainrace = ""
		mainraceVal = 0
		subrace = ""
		subraceVal = 0

		for i in xrange(17):
			curFlag = 1 << i
			if (raceFlag & curFlag) == curFlag:
				if localeInfo.RACE_FLAG_TO_NAME.has_key(curFlag):
					mainrace += localeInfo.RACE_FLAG_TO_NAME[curFlag] + ", "
					mainraceVal = player.GetStatus(localeInfo.RACE_FLAG_BONUSES[curFlag])
				elif localeInfo.SUB_RACE_FLAG_TO_NAME.has_key(curFlag):
					subrace += localeInfo.SUB_RACE_FLAG_TO_NAME[curFlag] + ", "
					subraceVal = player.GetStatus(item.GetApplyPoint(localeInfo.RACE_FLAG_BONUSES[curFlag][0]))

		if nonplayer.IsMonsterStone(race):
			mainrace += localeInfo.TARGET_INFO_RACE_METIN + ", "

		if mainrace == "":
			mainrace = ""
		else:
			mainrace = mainrace[:-2]
			if mainraceVal > 0:
				mainrace += " |cFF89b88d(+{}%)|r".format(mainraceVal)

		if subrace == "":
			subrace = ""
		else:
			subrace = subrace[:-2]
			if subraceVal > 0:
				subrace += " |cFF89b88d(+{}%)|r".format(subraceVal)

		bText = "|cFFb0dfb4{}|r {}{}{}".format(localeInfo.TARGET_INFO_BONUSES, mainrace, (", " if mainrace and subrace else ""), subrace)

		if mainrace == "" and subrace == "":
			bText = "|cFFb0dfb4{}|r {}".format(localeInfo.TARGET_INFO_BONUSES, localeInfo.TARGET_INFO_BONUSES_EMPTY)

		self.bonusName.SetText(bText)

		(textWidth, textHeight) = self.bonusName.GetTextSize()

		self.bonusName.SetPosition(23, 6 + textHeight)
		self.bonusName.UpdateRect()
		self.bonusName.Show()

	def GetTargetVID(self):
		return self.vid

	def GetTargetName(self):
		return self.nameString

	def SetTargetName(self, name):
		self.nameString = name
		self.nameLength = len(name)
		self.name.SetText(name)

	def getColorByPercentage(self, percentage):
		percentage = max(1, 100 - float(percentage))
		colors = [
			[0, [255, 0, 0]],
			[20, [255, 0, 0]],
			[50, [220, 50, 0]],
			[100, [0, 255, 0]], #r, g, b
		]

		closestIndex = 0
		for color in colors:
			if percentage <= color[0]:
				closestIndex += 1
			else:
				break

		color0 = colors[closestIndex - 1]
		color1 = colors[closestIndex]

		color0X = color0[0]
		color1X = color1[0] - color0X
		x = percentage - color0X

		ratio = 1.0 * x / color1X

		w = ratio * 2 - 1
		w1 = (w / 1 + 1) / 2
		w2 = 1 - w1

		r, g, b = (color0[1][0] * w1 + color1[1][0] * w2, color0[1][1] * w1 + color1[1][1] * w2, color0[1][2] * w1 + color1[1][2] * w2)

		return grp.GenerateColor(r / 255., g / 255., b / 255., 1.0)

	def percent(self, num1, num2):
		num1 = float(num1)
		num2 = float(num2)
		percentage = '{0:.1f}'.format((num1 / num2 * 100))
		return percentage

	def SetHP(self, hp, maxHp):
		hpPercentage = float(hp) / float(maxHp) * 100.0

		self.hpInfo.SetText("{}/{} ({:.1f}%)".format(localeInfo.DottedNumber(hp), localeInfo.DottedNumber(maxHp), hpPercentage))
		# self.hpPercent.SetText("%s%%" % str(self.percent(hp, maxHp)))

		color = self.getColorByPercentage(hpPercentage)
		self.hpInfo.SetPackedFontColor(color)
		# self.hpPercent.SetPackedFontColor(color)

		self.hpGauge.SetPercentage(hpPercentage, 100)

		self.name.SetWindowHorizontalAlignLeft()
		self.name.SetHorizontalAlignLeft()
		self.name.SetPosition(23, 6)

		if self.initHP:
			self.hpGauge.SetBGPercentage(hpPercentage, 100)
			self.initHP = False
		else:
			self.hpGauge.SetEasingPercentage(hpPercentage, 100)

		self.hpInfo.Show()
		# self.hpPercent.Show()
		self.hpGauge.Show()

	def ShowDefaultButton(self):

		self.isShowButton = True
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW])
		for button in self.showingButtonList:
			button.Show()

	def HideAllButton(self):
		self.isShowButton = False
		for button in self.showingButtonList:
			button.Hide()
		self.showingButtonList = []

	def __ShowButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		self.buttonDict[name].Show()
		self.showingButtonList.append(self.buttonDict[name])

	def __HideButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		button = self.buttonDict[name]
		button.Hide()

		for btnInList in self.showingButtonList:
			if btnInList == button:
				self.showingButtonList.remove(button)
				break

	if app.ENABLE_TARGET_MONSTER_LOOT:
		def ToggleInfoBoard(self):
			if self.infoBoard.IsShow():
				self.infoBoard.Close()
				return

			vnum = chr.GetRaceByVID(self.GetTargetVID())
			if vnum == 0:
				return

			if not vnum in constInfo.DROP_INFO:
				net.SendLoadTargetInfo(self.GetTargetVID())

			self.infoBoard.Open(self, vnum)

		def RefreshTargetInfo(self):
			if self.infoBoard.IsShow():
				self.infoBoard.Refresh()

	def OnWhisper(self):
		if None != self.eventWhisper:
			self.eventWhisper(self.nameString)

	def OnExchange(self):
		net.SendExchangeStartPacket(self.vid)

	def OnPVP(self):
		net.SendChatPacket("/pvp %d" % (self.vid))

	def OnAppendToMessenger(self):
		net.SendMessengerAddByVIDPacket(self.vid)

	def OnPartyInvite(self):
		net.SendPartyInvitePacket(self.vid)

	def OnPartyExit(self):
		net.SendPartyExitPacket()

	def OnPartyRemove(self):
		net.SendPartyRemovePacketVID(self.vid)

	def __OnGuildAddMember(self):
		net.SendGuildAddMemberPacket(self.vid)

	def __OnDismount(self):
		net.SendChatPacket("/ride")

	def __OnExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def __OnViewEquipment(self):
		net.SendChatPacket("/view_equip " + str(self.vid))

	def __OnRequestParty(self):
		net.SendChatPacket("/party_request " + str(self.vid))

	def __OnDestroyBuilding(self):
		net.SendChatPacket("/build d %d" % (self.vid))

	def __OnEmotionAllow(self):
		net.SendChatPacket("/emotion_allow %d" % (self.vid))

	def __OnVoteBlockChat(self):
		cmd = "/vote_block_chat %s" % (self.nameString)
		net.SendChatPacket(cmd)

	def __OnKill(self):
		cmd = "/kill %s" % self.nameString
		net.SendChatPacket(cmd)

	def __OnKick(self):
		cmd = "/dc %s" % self.nameString
		net.SendChatPacket(cmd)

	def __OnTransfer(self):
		cmd = "/transfer %s" % self.nameString
		net.SendChatPacket(cmd)

	def OnPressEscapeKey(self):
		self.OnPressedCloseButton()
		return True

	def IsShowButton(self):
		return self.isShowButton

	def RefreshButton(self):

		self.HideAllButton()

		if chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
			#self.__ShowButton(localeInfo.TARGET_BUTTON_BUILDING_DESTROY)
			#self.__ArrangeButtonPosition()
			return

		if player.IsPVPInstance(self.vid) or player.IsObserverMode():
			# PVP_INFO_SIZE_BUG_FIX
			self.SetSize(200 + 7*self.nameLength, 40)
			self.UpdatePosition()
			# END_OF_PVP_INFO_SIZE_BUG_FIX
			return

		self.ShowDefaultButton()

		if guild.MainPlayerHasAuthority(guild.AUTH_ADD_MEMBER):
			if not guild.IsMemberByName(self.nameString):
				if 0 == chr.GetGuildID(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_GUILD)

		if player.IsGameMaster():
			self.__ShowButton("Kick")
			self.__ShowButton("Kill")
			self.__ShowButton("Transfer")

		if not messenger.IsFriendByName(self.nameString):
			self.__ShowButton(localeInfo.TARGET_BUTTON_FRIEND)

		if player.IsPartyMember(self.vid):

			self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if player.IsPartyLeader(self.vid):
				self.__ShowButton(localeInfo.TARGET_BUTTON_LEAVE_PARTY)
			elif player.IsPartyLeader(player.GetMainCharacterIndex()):
				self.__ShowButton(localeInfo.TARGET_BUTTON_EXCLUDE)

		else:
			if player.IsPartyMember(player.GetMainCharacterIndex()):
				if player.IsPartyLeader(player.GetMainCharacterIndex()):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
			else:
				if chr.IsPartyMember(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY)
				else:
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)

			if player.IsRevengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_AVENGE)
			elif player.IsChallengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_ACCEPT_FIGHT)
			elif player.IsCantFightInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if not player.IsSameEmpire(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
				self.__HideButton(localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY)
				self.__HideButton(localeInfo.TARGET_BUTTON_FRIEND)
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

		distance = player.GetCharacterDistance(self.vid)
		if distance > self.EXCHANGE_LIMIT_RANGE:
			self.__HideButton(localeInfo.TARGET_BUTTON_EXCHANGE)
			self.__ArrangeButtonPosition()

		self.__ArrangeButtonPosition()

	def __ArrangeButtonPosition(self, ypos = 35):
		showingButtonCount = len(self.showingButtonList)

		pos = -(showingButtonCount / 2) * 68
		if 0 == showingButtonCount % 2:
			pos += 34

		for button in self.showingButtonList:
			button.SetPosition(pos, ypos)
			pos += 68

		self.SetSize(max(150, showingButtonCount * 75), ypos + 32)
		self.UpdatePosition()

	if gcGetEnable("ENABLE_POISON_GAUGE"):
		def CheckPoisoned(self):
			if chr.IsStone(self.GetTargetVID()):
				self.SetPoisoned(False)
				return

			if chrmgr.HasAffectByVID(self.GetTargetVID(), chr.AFFECT_POISON):
				if not self.isPoisoned:
					self.SetPoisoned(True)
			else:
				if self.isPoisoned:
					self.SetPoisoned(False)

		def SetPoisoned(self, isPoisoned):
			if self.isPoisoned == isPoisoned:
				return

			self.isPoisoned = isPoisoned

			if isPoisoned:
				self.hpGauge.SetColor("lime")
			else:
				self.hpGauge.SetColor("red")

	def OnUpdate(self):
		if self.isShowButton:

			exchangeButton = self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE]
			distance = player.GetCharacterDistance(self.vid)

			if distance < 0:
				return

			if exchangeButton.IsShow():
				if distance > self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

			else:
				if distance < self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

		if gcGetEnable("ENABLE_POISON_GAUGE"):
			self.CheckPoisoned()

class InfoBoard(ui.ThinBoard):
	class ItemListBoxItem(ui.FineListBox.FineListBoxItem):
		VNUMS = (28030, 28031, 28032, 28033, 28034, 28035, 28036, 28037, 28038, 28039, 28041, 28042, 28043)

		def __init__(self, width):
			ui.FineListBox.FineListBoxItem.__init__(self, 0xFF7F7D7D)

			self.isMetin = False
			self.metinCounter = 30

			icon = ui.ExpandedImageBox()
			icon.AddFlag("not_pick")
			icon.SetParent(self)
			icon.Show()
			self.icon = icon

			nameLine = ui.TextLine()
			nameLine.SetParent(self)
			nameLine.SetPosition(32 + 5, 0)
			nameLine.SetFontName("Verdana:13")
			nameLine.SetPackedFontColor(0xffe6b233)
			nameLine.Show()
			self.nameLine = nameLine

			rareLine = ui.TextLine()
			rareLine.SetParent(self)
			rareLine.SetPosition(32 + 5, 10)
			rareLine.SetFontName("Verdana:13")
			rareLine.SetPackedFontColor(0xffe6b233)
			rareLine.Show()
			self.rareLine = rareLine

			self.RegisterComponent(icon)
			self.RegisterComponent(nameLine)
			self.RegisterComponent(rareLine)

			self.SetSize(width, 32 + 5)

		def Destroy(self):
			ui.FineListBox.FineListBoxItem.Destroy(self)

			self.icon = None
			self.nameLine = None
			self.rareLine = None

		def LoadImage(self, image, name = None):
			self.icon.LoadImage(image)
			self.SetSize(self.GetWidth(), self.icon.GetHeight() + 5 * (self.icon.GetHeight() / 32))

			if name != None:
				self.SetText(name)

		def SetText(self, text):
			self.nameLine.SetText(text)
		
		def SetRareLine(self, text):
			self.rareLine.SetText(text)

		def RefreshHeight(self):
			ui.FineListBox.FineListBoxItem.RefreshHeight(self)
			self.icon.SetRenderingRect(0.0, 0.0 - float(self.removeTop) / float(self.GetHeight()), 0.0, 0.0 - float(self.removeBottom) / float(self.GetHeight()))
			self.icon.SetPosition(0, - self.removeTop)

		def OnUpdate(self):
			if self.isMetin:
				if self.metinCounter == 30:
					self.metinCounter = 0

					item.SelectItem(self.VNUMS[random.randint(0, len(self.VNUMS) - 1)])
					self.icon.LoadImage(item.GetIconImageFileName())

				self.metinCounter += 1

	MAX_ITEM_COUNT = 5

	BOARD_WIDTH = 280

	def __init__(self):
		ui.ThinBoard.__init__(self)

		self.HideCorners(self.LT)
		self.HideCorners(self.RT)
		self.HideLine(self.T)

		self.race = 0

		self.itemTooltip = uiToolTip.ItemToolTip()
		self.itemTooltip.HideToolTip()

		self.SetSize(self.BOARD_WIDTH, 0)

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def __UpdatePosition(self, targetBoard):
		self.SetPosition(targetBoard.GetLeft() + (targetBoard.GetWidth() - self.GetWidth()) / 2, targetBoard.GetBottom() - 17)
		targetBoard.SetTop()

	def Open(self, targetBoard, race):
		self.__LoadInformation(race)

		self.SetSize(self.BOARD_WIDTH, self.yPos + 10)
		self.__UpdatePosition(targetBoard)

		self.Show()

	def Refresh(self):
		self.__LoadInformation(self.race)
		self.SetSize(self.BOARD_WIDTH, self.yPos + 10)

	def Close(self):
		self.itemTooltip.HideToolTip()
		self.Hide()

	def __LoadInformation(self, race):
		self.yPos = 7
		self.children = []
		self.race = race

		self.__AppendDefault(race)
		self.__AppendDrops(race)

	def __AppendDefault(self, race):
		self.AppendSeperator()

		# self.AppendTextLine("|cffBEB47D{}".format("Informacje:"))
		# self.AppendTextLine("")
		# self.AppendTextLine(localeInfo.TARGET_INFO_MAX_HP % str(nonplayer.GetMonsterMaxHP(race)))

		regenCycle, regenPercent = nonplayer.GetMonsterRegen(race)
		self.AppendTextLine(localeInfo.TARGET_INFO_REGEN % (int(regenPercent), int(regenCycle)))

		iDamMin, iDamMax = nonplayer.GetMonsterDamage(race)
		self.AppendTextLine(localeInfo.TARGET_INFO_DAMAGE % (str(iDamMin), str(iDamMax)))

		self.AppendTextLine(localeInfo.TARGET_INFO_EXP % str(nonplayer.GetMonsterExp(race)))

		minGold, maxGold = nonplayer.GetMonsterGold(race)
		self.AppendTextLine(localeInfo.TARGET_INFO_GOLD % (str(minGold), str(maxGold)))

	def __AppendDrops(self, race):
		self.AppendSeperator()

		if race in constInfo.DROP_INFO:
			usableDropInfo = []
			for info in constInfo.DROP_INFO[race]:
				# if info['LEVEL_RANGE'][0] > player.GetStatus(player.LEVEL) or info['LEVEL_RANGE'][1] < player.GetStatus(player.LEVEL):
				# 	continue

				found = False
				for tmp in usableDropInfo:
					if tmp['VNUM'] == info['VNUM']:
						tmp['COUNT'] += info['COUNT']
						found = True
						break

				if not found:
					usableDropInfo.append({'VNUM' : info['VNUM'], 'COUNT' : info['COUNT'], 'PCT' : info['PCT']})

			monsterLevel = nonplayer.GetMonsterLevel(race)
			playerLevel = player.GetStatus(player.LEVEL)
			isStone = nonplayer.IsMonsterStone(race)

			if (playerLevel-monsterLevel > 15):
				self.AppendTextLine("|cffD14646{} {}.".format(localeInfo.TARGET_INFO_LOCKED_DROP_REQUIRED_LEVEL, localeInfo.TARGET_INFO_LOCKED_DROP_STONE if isStone else localeInfo.TARGET_INFO_LOCKED_DROP_MONSTER))
				self.AppendTextLine(localeInfo.TARGET_INFO_LOCKED_DROP_REASON)
				self.AppendTextLine("")

			if len(usableDropInfo) == 0:
				self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)
			else:

				itemListBox = ui.FineListBox()
				itemListBox.SetItemStep(5)
				itemListBox.SetSize(self.GetWidth() - 15 * 2 - ui.ScrollBar.SCROLLBAR_WIDTH, (32 + 5) * self.MAX_ITEM_COUNT)
				itemListBox.SetItemWidth(itemListBox.GetWidth())

				height = 0
				for info in usableDropInfo:

					height += self.AppendItem(itemListBox, info['VNUM'], info['COUNT'], info['PCT'])

				TEMP_BLOCKED_VNUMS = (8024, 8025, 8026, 8027, 8052, 8054, 8059, 8061)
				if nonplayer.IsMonsterStone(race) and not race in TEMP_BLOCKED_VNUMS:
					height += self.AppendMetinStone(itemListBox)

				if height == 0:
					self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)
				else:
					if height < itemListBox.GetHeight():
						itemListBox.SetSize(itemListBox.GetWidth(), height)

						self.AppendWindow(itemListBox, 15)
					else:
						self.AppendWindow(itemListBox, 15)

						itemScrollBar = ui.ModernScrollBar()
						itemScrollBar.SetParent(self)
						itemScrollBar.SetPosition(itemListBox.GetRight() + 5, itemListBox.GetTop())
						itemScrollBar.SetScrollBarSize(32 * self.MAX_ITEM_COUNT + 5 * (self.MAX_ITEM_COUNT - 1))
						itemScrollBar.SetContentHeight(height)
						itemScrollBar.Show()
						itemListBox.SetScrollBar(itemScrollBar, True)

						if app.ENABLE_MOUSE_WHEEL_EVENT:
							## Wheel support
							self.SetScrollWheelEvent(itemScrollBar.OnWheelMove)
		else:
			self.AppendTextLine(localeInfo.TARGET_INFO_NO_ITEM_TEXT)

	def AppendTextLine(self, text):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetWindowHorizontalAlignCenter()
		textLine.SetHorizontalAlignCenter()
		textLine.SetText(text)
		textLine.SetPosition(0, self.yPos)
		textLine.Show()

		self.children.append(textLine)
		self.yPos += 17

	def AppendSeperator(self):
		img = ui.ImageBox()
		img.LoadImage("d:/ymir work/ui/seperator.tga")
		self.AppendWindow(img)
		img.SetPosition(img.GetLeft(), img.GetTop() - 15)
		self.yPos -= 15

	def AppendItem(self, listBox, vnum, count, pct):
		myItem = self.ItemListBoxItem(listBox.GetWidth())

		itemName = ""
		if type(vnum) == int:
			item.SelectItem(vnum)
			itemName = item.GetItemName()

			myItem.SetOverInEvent(self.OnShowItemTooltip, vnum)
		else:
			item.SelectItem(vnum[0])
			itemName = item.GetItemName()
			if vnum[0] != vnum[1]:
				itemName = "{} +{} - +{}".format(itemName[:itemName.find("+")], vnum[0] % 10, vnum[1] % 10)

			myItem.SetOverInEvent(self.OnShowItemTooltip, vnum[0])

		if count > 1:
			itemName = "%dx %s" % (count, itemName)

		myItem.LoadImage(item.GetIconImageFileName())
		myItem.SetText("{}".format(itemName))
		myItem.SetRareLine("{}".format(FormatRarity(pct)))
		myItem.SetOverOutEvent(self.OnHideItemTooltip)
		listBox.AppendItem(myItem)

		return myItem.GetHeight()

	def AppendMetinStone(self, listBox):
		myItem = self.ItemListBoxItem(listBox.GetWidth())
		myItem.isMetin = True
		myItem.SetText("{} +0 - +4".format(localeInfo.TARGET_INFO_STONE_NAME))
		myItem.SetRareLine("{}".format(FormatRarity(100)))
		listBox.AppendItem(myItem)

		return myItem.GetHeight()

	def OnShowItemTooltip(self, vnum):
		item.SelectItem(vnum)
		if vnum in (50026, 50300, 70037, 70055):
			self.itemTooltip.showSpecialToolTip = False

		self.itemTooltip.SetItemToolTip(vnum)

	def OnHideItemTooltip(self):
		self.itemTooltip.HideToolTip()

	def AppendWindow(self, wnd, x = 0, width = 0, height = 0):
		if width == 0:
			width = wnd.GetWidth()
		if height == 0:
			height = wnd.GetHeight()

		wnd.SetParent(self)
		if x == 0:
			wnd.SetPosition((self.GetWidth() - width) / 2, self.yPos)
		else:
			wnd.SetPosition(x, self.yPos)
		wnd.Show()

		self.children.append(wnd)
		self.yPos += height + 5
