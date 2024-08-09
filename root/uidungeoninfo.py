import ui
import net
import app
import item
import exception
import uiToolTip
import localeInfo
import player

from cff import CFF

from _weakref import proxy
import colorInfo

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

class DungeonInfo(ui.ScriptWindow):

	DUNGEON_CONFIG = {"global" : dict(), "personal" : dict()}
	DUNGEON_RANKINGS = dict()
	DUNGEON_RANKING_TYPES = {
								"CC" : 0,
								"FC" : 1,
								"GD" : 2,
							}

	class DungeonButton(ui.RadioButton):
		
		ROOT_PATH = "assets/ui/dungeon_information/{}"
		BUTTON_IMAGES = ("assets/ui/dungeon_information/item_0.png", "assets/ui/dungeon_information/item_2.png")
		TEXT_COLOURS = (0xFF48b804, 0xFFB3AA14)

		def	__init__(self, sTitle, sKey, dtCoolDown, iRequiredMinLevel, iRequiredMaxLevel):
			ui.RadioButton.__init__(self)
			self.Objects = {}
			self.dtCoolDown = app.GetTime()+dtCoolDown
			self.iRequiredMinLevel = iRequiredMinLevel
			self.iRequiredMaxLevel = iRequiredMaxLevel
			self.sKey = sKey
			self.__BuildObject(sTitle, sKey)

		def	__del__(self):
			ui.RadioButton.__del__(self)
			self.Objects = {}
			self.dtCoolDown = 0
			self.sKey = ""

		def SetParent(self, parent):
			ui.RadioButton.SetParent(self, parent)

			self.parent=proxy(parent)
			self.SAFE_SetEvent(self.parent.SelectItem, self)

		def	GetKey(self):
			return self.sKey

		def	UpdateCooldown(self, iTime):
			self.dtCoolDown = app.GetTime()+iTime

		def	__BuildObject(self, sTitle, sKey):
			## Layer
			self.SetUpVisual(self.BUTTON_IMAGES[0])
			self.SetOverVisual(self.BUTTON_IMAGES[1])
			self.SetDownVisual(self.BUTTON_IMAGES[1])

			## Title
			self.Objects["TITLE"] = ui.TextLine()
			self.Objects["TITLE"].SetParent(self)
			self.Objects["TITLE"].AddFlag("not_pick")
			self.Objects["TITLE"].SetPosition(65, 0)
			self.Objects["TITLE"].SetVerticalAlignCenter()
			self.Objects["TITLE"].SetWindowVerticalAlignCenter()
			self.Objects["TITLE"].SetText(getattr(localeInfo, sTitle, "NOT FOUND"))
			self.Objects["TITLE"].Show()

			self.Objects["STATE_IMAGE"] = ui.ImageBoxNew()
			self.Objects["STATE_IMAGE"].SetParent(self)
			self.Objects["STATE_IMAGE"].AddFlag("not_pick")
			self.Objects["STATE_IMAGE"].LoadImage(self.ROOT_PATH.format("States/state_01.png"))
			self.Objects["STATE_IMAGE"].SetPosition(25 + 122, self.GetHeight() / 2 - self.Objects["STATE_IMAGE"].GetHeight() / 2)
			self.Objects["STATE_IMAGE"].SetWindowHorizontalAlignRight()
			self.Objects["STATE_IMAGE"].Show()

			## State Header
			self.Objects["STATE_HEADER"] = ui.TextLine()
			self.Objects["STATE_HEADER"].SetParent(self.Objects["STATE_IMAGE"])
			self.Objects["STATE_HEADER"].AddFlag("not_pick")
			self.Objects["STATE_HEADER"].SetPosition(5, 12)
			self.Objects["STATE_HEADER"].SetText("")
			self.Objects["STATE_HEADER"].Show()

			## State Data
			self.Objects["STATE_DATA"] = ui.TextLine()
			self.Objects["STATE_DATA"].SetParent(self.Objects["STATE_IMAGE"])
			self.Objects["STATE_DATA"].AddFlag("not_pick")
			self.Objects["STATE_DATA"].SetPosition(5, 20)
			self.Objects["STATE_DATA"].SetText("")
			self.Objects["STATE_DATA"].Show()

			self.__CalculateState()

		def __CalculateState(self):
			lStates = {
				"AC" : [localeInfo.DUNGEON_STATUS_0, 0xFF48b804, "States/state_01.png"],
				"UN" : [localeInfo.DUNGEON_STATUS_1, 0xFFa93130, "States/state_02.png"],
				"CT" : [localeInfo.DUNGEON_STATUS_2, 0xFFc88418, "States/state_03.png"],
			}

			if player.GetStatus(player.LEVEL) < self.iRequiredMinLevel:
				## Setting the image depend by state
				self.Objects["STATE_IMAGE"].LoadImage(self.ROOT_PATH.format(lStates.get("UN")[2]))

				## Setting the text
				self.Objects["STATE_HEADER"].SetText(lStates.get("UN")[0])

				## Setting the color
				self.Objects["STATE_HEADER"].SetPackedFontColor(lStates.get("UN")[1])

				## Setting the data
				self.Objects["STATE_DATA"].SetText(CFF.format(localeInfo.DUNGEON_REQUIRED_LEVEL.format(self.iRequiredMinLevel), "#555555"))

			elif player.GetStatus(player.LEVEL) > self.iRequiredMaxLevel:
				## Setting the image depend by state
				self.Objects["STATE_IMAGE"].LoadImage(self.ROOT_PATH.format(lStates.get("UN")[2]))

				## Setting the text
				self.Objects["STATE_HEADER"].SetText(lStates.get("UN")[0])

				## Setting the color
				self.Objects["STATE_HEADER"].SetPackedFontColor(lStates.get("UN")[1])

				## Setting the data
				self.Objects["STATE_DATA"].SetText(CFF.format(localeInfo.DUNGEON_REQUIRED_MAX_LEVEL.format(self.iRequiredMaxLevel), "#555555"))

			elif self.dtCoolDown > app.GetTime():
				## Setting the image depend by state
				self.Objects["STATE_IMAGE"].LoadImage(self.ROOT_PATH.format(lStates.get("CT")[2]))

				## Setting the text
				self.Objects["STATE_HEADER"].SetText(lStates.get("CT")[0])

				## Setting the color
				self.Objects["STATE_HEADER"].SetPackedFontColor(lStates.get("CT")[1])

				## Setting the data
				self.Objects["STATE_DATA"].SetText(CFF.format("{}".format(localeInfo.SecondToNiceTime(self.dtCoolDown-app.GetTime())), "#555555"))

			else:
				## Setting the image depend by state
				self.Objects["STATE_IMAGE"].LoadImage(self.ROOT_PATH.format(lStates.get("AC")[2]))

				## Setting the text
				self.Objects["STATE_HEADER"].SetText(lStates.get("AC")[0])

				## Setting the color
				self.Objects["STATE_HEADER"].SetPackedFontColor(lStates.get("AC")[1])

				## Reseting the data
				self.Objects["STATE_DATA"].SetText("")

		def	OnUpdate(self):
			self.__CalculateState()

	class DungeonRanking(ui.ScriptWindow):
		class RankingField(ui.ExpandedImageBox):

			WINDOW_SIZE = (325, 34)

			def	__init__(self, iPos, sName, iLevel, lRes):
				ui.ExpandedImageBox.__init__(self)
				self.Objects = {}

				## Self params
				self.SetSize(*self.WINDOW_SIZE)
				self.LoadImage("assets/ui/dungeon_information/Rankings/item_data.png")

				## Pos Field
				self.Objects["Pos"] = self.__GenerateAppendSmallField(self.WINDOW_SIZE[0]*0.1, 2, str(iPos + 1))

				## Name Field
				self.Objects["Name"] = self.__GenerateAppendSmallField(self.WINDOW_SIZE[0]*0.2, 79	, sName)

				## Level Field
				self.Objects["Level"] = self.__GenerateAppendSmallField(self.WINDOW_SIZE[0]*0.1, 185, str(iLevel))

				## lRes Field
				self.Objects["Res"] = self.__GenerateAppendSmallField(self.WINDOW_SIZE[0]*0.25, self.WINDOW_SIZE[0]*0.75-16, str(lRes))

			def	__del__(self):
				ui.ExpandedImageBox.__del__(self)

				self.Objects = {}

			def	__GenerateAppendSmallField(self, iWidth, iX, sTxt):
				newWnd = ui.Window()
				newWnd.SetParent(self)
				newWnd.SetSize(iWidth, self.WINDOW_SIZE[1]*0.8)
				newWnd.SetPosition(iX, 0)
				newWnd.SetWindowVerticalAlignCenter()
				newWnd.Show()

				self.Objects["TXT_%d_%s" % (iX, sTxt)] = ui.MakeTextLine(newWnd)
				self.Objects["TXT_%d_%s" % (iX, sTxt)].SetText(sTxt)

				return newWnd

		def __init__(self):
			ui.ScriptWindow.__init__(self)
			self.Objects = {}
			self.__LoadWindow()

		def __del__(self):
			ui.ScriptWindow.__del__(self)

		def	Destroy(self):
			self.ClearDictionary()
			self.Objects = {}

		def	__LoadWindow(self):
			try:
				pyScrLoader = ui.PythonScriptLoader()
				pyScrLoader.LoadScriptFile(self, "uiscript/DungeonInfo_Ranking.py")
			except:
				exception.Abort("DungeonInfoRanking.__LoadWindow.LoadObject")

			try:
				self.Objects["Board"] = self.GetChild("board")

				self.Objects["ListClipper"] = self.GetChild("ListClipper")
			except:
				exception.Abort("DungeonInfoRanking.__LoadWindow.BindObject")

			self.Objects["Board"].SetCloseEvent(ui.__mem_func__(self.Hide))

			self.Objects["ListClipper"].SetItemSize(*self.RankingField.WINDOW_SIZE)
			self.Objects["ListClipper"].SetItemStep(self.RankingField.WINDOW_SIZE[1])
			self.Objects["ListClipper"].SetViewItemCount(10)

			self.Objects["ListClipper"].SetScrollBar(self.__MakeScrollBar(self.Objects["ListClipper"], "scroll_base.png", "scroll_image.png", xFill = 12, yFill = 2))

			## Simulation
			# self.__Simulate()

			self.SetCenterPosition()
			self.SetTop()
			self.Hide()

		def	__MakeScrollBar(self, nObject, sField, sCursor, xFill = 0, yFill = 0):
			newScroll = ui.ExpensiveScrollBar("assets/ui/dungeon_information/Rankings/", sField, sCursor)
			newScroll.SetParent(self)
			newScroll.SetPosition(nObject.GetLocalPosition()[0] + (nObject.GetWidth() + xFill), nObject.GetLocalPosition()[1] + yFill)
			newScroll.Show()

			return newScroll

		def	__ClearList(self):
			self.Objects["ListClipper"].RemoveAllItems()

		ClearList = __ClearList

		def	__InsertElement(self, iPos, sName, iLevel, lScore):
			self.Objects["ListClipper"].AppendItem(self.RankingField(iPos, sName, iLevel, lScore))

		def	LoadConfig(self, rConf, lInfo = ()):
			self.__ClearList()

			if rConf:
				for wPos, sName, iLevel, lValue in rConf:
					self.__InsertElement(wPos, sName, iLevel, lValue)

			lTypes = (localeInfo.DUNGEON_RANKING_TYPE_0, localeInfo.DUNGEON_RANKING_TYPE_1, localeInfo.DUNGEON_RANKING_TYPE_2)
			self.Objects["Board"].SetTitleName(localeInfo.DUNGEON_RANKING_TITLE.format(colorInfo.Colorize(lInfo[0], 0xFFc5b44a), colorInfo.Colorize(lTypes[lInfo[1]], 0xFFc5b44a)))

		def	__Simulate(self):
			## Clear Box
			self.__ClearList()

			## Generate randoms
			for i in xrange(255):
				self.__InsertElement((i+1), ("TEST_%d" % app.GetRandom(0, 999)), app.GetRandom(1, 99), app.GetRandom(0, 9999999)) ## POS, NAME, LEVEL, SCORE

		def	UpdateWindow(self):
			if self.IsShow():
				self.Hide()
			else:
				self.Show()
				self.SetTop()

	class ToolTipDialog:
		def	__init__(self):
			pass

		def	__del__(self):
			pass

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.Objects = {}
		self.toolTipDialog = self.ToolTipDialog()
		self.tooltipItem = uiToolTip.ItemToolTip()
		self.windowRanking = self.DungeonRanking()
		self.sKey = ""
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.Objects = {}
		self.toolTipDialog = None
		self.tooltipItem = None
		self.windowRanking = None
		self.sKey = ""

	def	__LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/DungeonInfo_Main.py")
		except:
			exception.Abort("DungeonInfo.__LoadWindow.LoadObject")

		try:
			self.Objects["Board"] = self.GetChild("board")

			self.Objects["DungeonList"] = self.GetChild("DungeonList_Window")
			self.Objects["DungeonListScroll"] = self.GetChild("DungeonListScroll_Window")

			self.Objects["DungeonInformation"] = self.GetChild("DungeonDetails_InformationText")
			self.Objects["DungeonType"] = self.GetChild("DungeonDetails_TypeData")
			self.Objects["DungeonApply"] = self.GetChild("DungeonDetails_ApplyData")
			self.Objects["DungeonLevelLimit"] = self.GetChild("DungeonDetails_LevelLimitData")
			self.Objects["DungeonCooldown"] = self.GetChild("DungeonDetails_CooldownData")
			self.Objects["DungeonPassItem"] = self.GetChild("DungeonDetails_PassItem")
			self.Objects["DungeonCompletionCount"] = self.GetChild("DungeonDetails_CompletionCountData")
			self.Objects["DungeonFastestCompletion"] = self.GetChild("DungeonDetails_FastestCompletionData")
			self.Objects["DungeonGreatestDamage"] = self.GetChild("DungeonDetails_GreatestDamageData")

			self.Objects["HighscoresCompletionCount"] = self.GetChild("DungeonDetails_CompletionCountButton")
			self.Objects["HighscoresFastestCompletion"] = self.GetChild("DungeonDetails_FastestCompletionButton")
			self.Objects["HighscoresGreatestDamage"] = self.GetChild("DungeonDetails_GreatestDamageButton")

			self.Objects["DungeonJoinButton"] = self.GetChild("DungeonDetails_JoinButton")
			self.Objects["DungeonReJoinButton"] = self.GetChild("DungeonDetails_ReJoinButton")
		except:
			exception.Abort("DungeonInfo.__LoadWindow.BindObject")

		## Board
		self.Objects["Board"].SetCloseEvent(ui.__mem_func__(self.Hide))

		## ListBox
		tmpBut = self.DungeonButton("", "", 0, 0, 0)
		tmpBut.Hide()

		self.Objects["DungeonList"].SetItemSize(tmpBut.GetWidth(), tmpBut.GetHeight())
		self.Objects["DungeonList"].SetItemStep(tmpBut.GetHeight() - 1)
		self.Objects["DungeonList"].SetViewItemCount(7)
		self.Objects["DungeonList"].SetScrollBar(self.Objects["DungeonListScroll"])
		# self.Objects["DungeonList"].SetScrollBar(self.__MakeScrollBar("scroll_base.png", "scroll_image.png", iY = 33 + 3))
		self.Objects["DungeonList"].SetSelectEvent(ui.__mem_func__(self.__SelectDungeon))
		self.Objects["DungeonList"].SetScrollWheelEvent(self.Objects["DungeonList"].scrollBar.OnWheelMove)

		## ToolTip
		self.Objects["DungeonPassItem"].SetOverInItemEvent(ui.__mem_func__(self.__OnOverItemIn))
		self.Objects["DungeonPassItem"].SetOverOutItemEvent(ui.__mem_func__(self.__OnOverItemOut))

		## Buttons
		self.Objects["HighscoresCompletionCount"].SAFE_SetEvent(self.__HighscoreButton, self.DUNGEON_RANKING_TYPES["CC"])
		self.Objects["HighscoresFastestCompletion"].SAFE_SetEvent(self.__HighscoreButton, self.DUNGEON_RANKING_TYPES["FC"])
		self.Objects["HighscoresGreatestDamage"].SAFE_SetEvent(self.__HighscoreButton, self.DUNGEON_RANKING_TYPES["GD"])
		self.Objects["DungeonJoinButton"].SAFE_SetEvent(self.__JoinDungeon)
		self.Objects["DungeonReJoinButton"].SAFE_SetEvent(self.__ReJoinDungeon)

		## SIMULATION
		# self.__Simulate()

		self.SetCenterPosition()
		self.SetTop()
		self.Hide()

	def	__Simulate(self):
		self.Objects["DungeonList"].AppendItem(self.DungeonButton("Przelecz Dzikusow", "DT", app.GetRandom(0, 30), 80, 120))
		self.Objects["DungeonList"].AppendItem(self.DungeonButton("Orkowa Przystan", "DC", app.GetRandom(0, 30), 80, 120))
		self.Objects["DungeonList"].AppendItem(self.DungeonButton("Wieza Demonow", "MT", app.GetRandom(0, 30), 80, 120))
		self.Objects["DungeonList"].AppendItem(self.DungeonButton("Komnata Pajaka", "DT", app.GetRandom(0, 30), 80, 120))
		self.Objects["DungeonList"].AppendItem(self.DungeonButton("Wyspy Elfow", "DC", app.GetRandom(0, 30), 80, 120))
		self.Objects["DungeonList"].AppendItem(self.DungeonButton("Piekielne Katakumby", "MT", app.GetRandom(0, 30), 80, 120))
		self.Objects["DungeonList"].AppendItem(self.DungeonButton("Komnata Smoka", "DT", app.GetRandom(0, 30), 80, 120))

		for i in xrange(1, 100):
			self.RecvHighscoreData("DT", self.DUNGEON_RANKING_TYPES["CC"], i, "TEST_%d" % app.GetRandom(1, 999), app.GetRandom(1, 99), app.GetRandom(1, 99999999))
			self.RecvHighscoreData("DT", self.DUNGEON_RANKING_TYPES["FC"], i, "TEST_%d" % app.GetRandom(1, 999), app.GetRandom(1, 99), app.GetRandom(1, 99999999))
			self.RecvHighscoreData("DT", self.DUNGEON_RANKING_TYPES["GD"], i, "TEST_%d" % app.GetRandom(1, 999), app.GetRandom(1, 99), app.GetRandom(1, 99999999))

	def	__SelectDungeon(self, selItem):
		for obj in self.Objects["DungeonList"].itemList:
			if obj == selItem:
				obj.Down()
			else:
				obj.SetUp()

		## Loading informations
		self.Objects["DungeonInformation"].SetText(getattr(localeInfo, self.DUNGEON_CONFIG["global"][selItem.GetKey()]["title"], "NOT FOUND"))
		self.Objects["DungeonType"].SetText(self.DUNGEON_CONFIG["global"][selItem.GetKey()]["type"])
		self.Objects["DungeonApply"].SetText(self.DUNGEON_CONFIG["global"][selItem.GetKey()]["apply"])
		self.Objects["DungeonLevelLimit"].SetText("%s - %s" % self.DUNGEON_CONFIG["global"][selItem.GetKey()]["level_limit"])
		self.Objects["DungeonCooldown"].SetText(self.DUNGEON_CONFIG["global"][selItem.GetKey()]["cooldown"])
		self.Objects["DungeonPassItem"].SetItemSlot(0, self.DUNGEON_CONFIG["global"][selItem.GetKey()]["pass_vnum"], 1)
		self.Objects["DungeonCompletionCount"].SetText(localeInfo.DottedNumber(self.DUNGEON_CONFIG["personal"][selItem.GetKey()]["completion_count"]))
		self.Objects["DungeonFastestCompletion"].SetText(self.DUNGEON_CONFIG["personal"][selItem.GetKey()]["fastest_completion"])
		self.Objects["DungeonGreatestDamage"].SetText(localeInfo.DottedNumber(self.DUNGEON_CONFIG["personal"][selItem.GetKey()]["greatest_damage"]))

		## Binding key
		self.sKey = selItem.GetKey()

	""" RECV """
	def	RecvGlobalData(self, sKey, sTitle, dwRaceFlag, bPartyCount, wRequiredLevel, wRequiredMaxLevel, dwPassItem, iDelay):
		## Independent data
		self.DUNGEON_CONFIG["global"][sKey] = {"title" : sTitle, "level_limit" : (str(wRequiredLevel), str(wRequiredMaxLevel))}

		self.DUNGEON_CONFIG["global"][sKey]["type"] = "Solo" if bPartyCount == 0 else "Group"
		self.DUNGEON_CONFIG["global"][sKey]["apply"] = self.__GetRaceFlags(dwRaceFlag)
		self.DUNGEON_CONFIG["global"][sKey]["cooldown"] = localeInfo.SecondToNiceTime(iDelay)

		if dwPassItem > 0:
			item.SelectItem(dwPassItem)
			self.DUNGEON_CONFIG["global"][sKey]["pass_item"] = item.GetItemName()
			self.DUNGEON_CONFIG["global"][sKey]["pass_vnum"] = dwPassItem
		else:
			self.DUNGEON_CONFIG["global"][sKey]["pass_item"] = "Not needed"
			self.DUNGEON_CONFIG["global"][sKey]["pass_vnum"] = 0

		## Adding Button if doesn't exist
		for obj in self.Objects["DungeonList"].itemList:
			if obj.GetKey() == sKey:
				return

		self.Objects["DungeonList"].AppendItem(self.DungeonButton(sTitle, sKey, iDelay, wRequiredLevel, wRequiredMaxLevel))

	def	RecvPersonalData(self, sKey, eType, iRes, iDelay):
		## Independent data
		keysToEnum = ("completion_count", "fastest_completion", "greatest_damage")
		if not sKey in self.DUNGEON_CONFIG["personal"]:
			self.DUNGEON_CONFIG["personal"][sKey] = {"completion_count" : "0", "fastest_completion" : "0", "greatest_damage" : "0"}

		if keysToEnum[eType] == "fastest_completion":
			iRes = localeInfo.SecondToNiceTime(iRes)
		else:
			iRes = str(iRes)

		self.DUNGEON_CONFIG["personal"][sKey][keysToEnum[eType]] = iRes

		## Update button
		for obj in self.Objects["DungeonList"].itemList:
			if obj.GetKey() == sKey:
				obj.UpdateCooldown(iDelay)

	def	RecvHighscoreData(self, sName, iType, wPos, sPlayerName, wLevel, lValue):
		if not sName in self.DUNGEON_RANKINGS:
			self.DUNGEON_RANKINGS[sName] = dict()

		if not iType in self.DUNGEON_RANKINGS[sName]:
			self.DUNGEON_RANKINGS[sName][iType] = []

		if wPos >= len(self.DUNGEON_RANKINGS[sName][iType]):
			self.DUNGEON_RANKINGS[sName][iType].append((wPos, sPlayerName, wLevel, lValue))
		else:
			self.DUNGEON_RANKINGS[sName][iType][wPos] = (wPos, sPlayerName, wLevel, lValue)
	
	def RecvHighscoreClear(self, sName):
		## Clear dictionary
		self.DUNGEON_RANKINGS[sName] = dict()

		## Flush elements
		self.windowRanking.ClearList()
	""" """

	def	__GetRaceFlags(self, dwRaceFlag):
		raceFlags = [v for k, v in MOB_RACEFLAG.items() if k & dwRaceFlag and not k == -1]
		return ", ".join(raceFlags) if len(raceFlags) > 0 else "-"

	def	__HighscoreButton(self, iType):
		self.windowRanking.LoadConfig(self.DUNGEON_RANKINGS[self.sKey].get(iType, None) if self.sKey in self.DUNGEON_RANKINGS else None, (getattr(localeInfo, self.DUNGEON_CONFIG["global"][self.sKey]["title"], "NOT FOUND"), iType))
		self.windowRanking.UpdateWindow()

	def	__JoinDungeon(self):
		net.SendChatPacket("/dungeon_info_join_dungeon %s" % self.sKey)

	def	__ReJoinDungeon(self):
		net.SendChatPacket("/dungeon_info_rejoin_dungeon %s" % self.sKey)

	def	__OnOverItemIn(self):
		if self.DUNGEON_CONFIG["global"][self.sKey]["pass_vnum"] and self.tooltipItem:
			self.tooltipItem.ClearToolTip()
			self.tooltipItem.AddItemData(self.DUNGEON_CONFIG["global"][self.sKey]["pass_vnum"], [0 for i in xrange(player.METIN_SOCKET_MAX_NUM)], bShowIcon = True)
			self.tooltipItem.ShowToolTip()

	def	__OnOverItemOut(self):
		if self.tooltipItem:
			self.tooltipItem.HideToolTip()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.__SelectDungeon(self.Objects["DungeonList"].itemList[0])
			self.Show()

	def	OnUpdate(self):
		## Broadcaster
		for obj in self.Objects["DungeonList"].itemList:
			obj.OnUpdate()

