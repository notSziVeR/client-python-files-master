import ui
import app
import net
import chat
import uiCommon
import nonplayer
import collections
import ZuoPanelHelper
import localeinfo
import uiScriptLocale

class ZuoEventDialog(ZuoPanelHelper.ZuoPanelHelper):

	TEXT_OBJECTS = {}
	BUTTON_OBJECTS = {}
	Monster_List = {}
	Thin = None
	MonsterSpawnDialog = None
	ListBox = None

	MAX_SLOT_SIZE = 10
	BOARD_BASE_X = 300
	BOARD_BASE_Y = 550

	MONSTER_VNUM = 0
	MONSTER_COUNT = 0

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()

		TEXT_OBJECTS = {}
		BUTTON_OBJECTS = {}
		Monster_List = {}
		Thin = None
		MonsterSpawnDialog = None
		ListBox = None
		MONSTER_VNUM = 0
		MONSTER_COUNT = 0

	def	__LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/zuo_event.py")
		except:
			import exception
			exception.Abort("ZuoEventDialog.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild
			self.board = GetObject("board")

			## Buttons
			self.BUTTON_OBJECTS["StartEvent"] = GetObject("Start_Event_Button")
			self.BUTTON_OBJECTS["CloseEvent"] = GetObject("Close_Event_Button")
			self.BUTTON_OBJECTS["SpawnMonster"] = GetObject("Spawn_Monster_Button")

			## Texts
			self.TEXT_OBJECTS["OnlineAttenders"] = [GetObject("Online_Attenders_Text"), 0]
			self.TEXT_OBJECTS["MaxAttenders"] = [GetObject("Online_Max_Text"), 0]
			self.TEXT_OBJECTS["BossCount"] = [GetObject("Boss_Count_Text"), 0]
			self.TEXT_OBJECTS["BossCountDead"] = [GetObject("Boss_Count_Dead_Text"), 0]
			self.TEXT_OBJECTS["MetinCount"] = [GetObject("Metin_Count_Text"), 0]
			self.TEXT_OBJECTS["MetinCountDead"] = [GetObject("Metin_Count_Dead_Text"), 0]

			## Time Gone
			self.TEXT_OBJECTS["TimeGone"] = [GetObject("Time_Gone_Text"), 0]

			self.MonsterName = GetObject("Monster_Spawn_EditLine")
			self.MonsterCount = GetObject("Monster_Count_EditLine")
		except:
			import exception
			exception.Abort("ZuoEventDialog.LoadDialog.BindObject")

		## Binding Events
		self.BUTTON_OBJECTS["StartEvent"].SAFE_SetEvent(self.__SendChatPacket, "/zuo_event_manage_status 1")
		self.BUTTON_OBJECTS["CloseEvent"].SAFE_SetEvent(self.__SendChatPacket, "/zuo_event_manage_status 0")
		self.BUTTON_OBJECTS["SpawnMonster"].SAFE_SetEvent(self.__SpawnMonster)

		## Updating text
		self.TEXT_OBJECTS["OnlineAttenders"][0].SetText(uiScriptLocale.ZUO_PANEL_PLAYER_COUNTER_1_1 % 0) ## Translate
		self.TEXT_OBJECTS["MaxAttenders"][0].SetText(uiScriptLocale.ZUO_PANEL_PLAYER_COUNTER_1_2 % 0) ## Translate
		self.TEXT_OBJECTS["BossCount"][0].SetText(uiScriptLocale.ZUO_PANEL_BOSS_COUNT_1 % 0) ## Translate
		self.TEXT_OBJECTS["BossCountDead"][0].SetText(uiScriptLocale.ZUO_PANEL_BOSS_COUNT_2 % 0) ## Translate
		self.TEXT_OBJECTS["MetinCount"][0].SetText(uiScriptLocale.ZUO_PANEL_STONES_COUNT_1 % 0) ## Translate
		self.TEXT_OBJECTS["MetinCountDead"][0].SetText(uiScriptLocale.ZUO_PANEL_STONES_COUNT_2 % 0) ## Translate
		self.TEXT_OBJECTS["TimeGone"][0].SetText("Duration: 0 sec")

		self.board.SetCloseEvent(ui.__mem_func__(self.Hide))
		self.MonsterName.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)

		self.SetCenterPosition()
		self.MonsterName.SetFocus()

	def	UpdateElement(self, key, value):
		value = int(value)
		templ_tab = {"OnlineAttenders" : uiScriptLocale.ZUO_PANEL_PLAYER_COUNTER_1_1, "MaxAttenders" : uiScriptLocale.ZUO_PANEL_PLAYER_COUNTER_1_2,
					"BossCount" : uiScriptLocale.ZUO_PANEL_BOSS_COUNT_1, "BossCountDead" : uiScriptLocale.ZUO_PANEL_BOSS_COUNT_2,
					"MetinCount" : uiScriptLocale.ZUO_PANEL_STONES_COUNT_1, "MetinCountDead" : uiScriptLocale.ZUO_PANEL_STONES_COUNT_2,
					"TimeGone" : "Duration: %s"}

		if key == "TimeGone":
			self.TEXT_OBJECTS["TimeGone"][1] = app.GetTime()-value if value > 0 else 0 ## That's the moment in time where we start counting
			self.TEXT_OBJECTS["TimeGone"][0].SetText(localeinfo.SecondToHMS(self.TEXT_OBJECTS["TimeGone"][1]))
		else:
			if key in self.TEXT_OBJECTS:
				self.TEXT_OBJECTS[key][0].SetText(templ_tab[key] % value)
				self.TEXT_OBJECTS[key][1] = value

	def	CreateListBox(self):
		self.Monster_List = {}
		## ListBox
		self.Thin = ui.SlotBar()
		self.Thin.SetParent(self)
		self.Thin.SetWindowHorizontalAlignCenter()
		self.Thin.SetSize(150, 15)

		self.ListBox = ui.ListBoxEx()
		self.ListBox.SetParent(self.Thin)
		self.ListBox.SetPosition(3, 0)
		self.ListBox.SetItemSize(130, 15)
		self.ListBox.SetItemStep(15)
		self.ListBox.SetSelectEvent(lambda empty_arg: self.Clear())

		## Fetching Items by Name
		if self.MonsterName.GetText() != "":
			nonplayer.GetMonstersByName(self.MonsterName.GetText(), "RetZuoMonsters")
		else:
			self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)
			return

		if len(self.Monster_List) == 0:
			self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)
			return
		else:
			self.Monster_List = collections.OrderedDict(sorted(self.Monster_List.items(), key = lambda x: x[1]))

		self.ListBox.SetViewItemCount(min(len(self.Monster_List), self.MAX_SLOT_SIZE))
		self.ListBox.UpdateSize()
		self.Thin.SetSize(self.Thin.GetWidth(), self.ListBox.GetHeight())

		## Adding Items to the ListBox
		for i in self.Monster_List.iterkeys():
			line = self.ListBoxItem()
			line.SetText(i)
			self.ListBox.AppendItem(line)

		## Reseting Board Size
		self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)

		x, y = self.GetChild("Spawner_Window").GetLocalPosition()
		y += 17 + 18
		self.Thin.SetPosition(0, y)

		## Creating ScrollBar
		if len(self.Monster_List) > self.MAX_SLOT_SIZE:
			self.ScrollBar = ui.ScrollBar()
			self.ScrollBar.SetParent(self.Thin)
			self.ScrollBar.SetPosition(self.Thin.GetWidth()-14, 5)
			self.ListBox.SetScrollBar(self.ScrollBar)

			## Setting Size
			self.ScrollBar.SetScrollBarSize(self.ListBox.GetHeight()-10)

		## Resizing board
		if (y+self.ListBox.GetHeight()) > self.BOARD_BASE_Y:
			self.UpdateSize(self.BOARD_BASE_X, y+self.ListBox.GetHeight()+5)

		self.Thin.Show()
		self.ListBox.Show()
		if len(self.Monster_List) > self.MAX_SLOT_SIZE:
			self.ScrollBar.Show()

	def	__SpawnMonster(self):
		if self.ListBox != None:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.ZUO_PANEL_ERROR_1) ## Translate
			return

		try:
			self.MONSTER_COUNT = int(self.MonsterCount.GetText())
		except ValueError:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.ZUO_PANEL_ERROR_2) ## Translate
			return

		if self.MONSTER_COUNT <= 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.ZUO_PANEL_ERROR_2) ## Translate
			return

		if self.MONSTER_VNUM > 0:
			self.AskGiveReward()
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, uiScriptLocale.ZUO_PANEL_ERROR_1) ## Translate
			return

	def AskGiveReward(self):
		monsterName = nonplayer.GetMonsterName(self.MONSTER_VNUM)

		MonsterSpawnDialog = uiCommon.QuestionDialog()
		MonsterSpawnDialog.SetWidth(400)
		MonsterSpawnDialog.SetText(uiScriptLocale.ZUO_PANEL_QUESTION % (monsterName, self.MONSTER_COUNT)) ## Translate

		MonsterSpawnDialog.SetAcceptEvent(lambda arg=True: self.AnswerMonsterSpawn(arg))
		MonsterSpawnDialog.SetCancelEvent(lambda arg=False: self.AnswerMonsterSpawn(arg))
		MonsterSpawnDialog.Open()
		self.MonsterSpawnDialog = MonsterSpawnDialog

	def AnswerMonsterSpawn(self, flag):
		self.MonsterSpawnDialog.Close()
		self.MonsterSpawnDialog = None

		if flag:
			net.SendChatPacket("/zuo_event_spawn_monster %d %d" % (self.MONSTER_VNUM, self.MONSTER_COUNT))

	def	AddMonsterName(self, name, vnum):
		self.Monster_List[name] = vnum

	def	Clear(self, empty_arg = None):
		if self.ListBox:
			self.MonsterName.SetText(self.ListBox.GetSelectedItem().GetText())
			self.MONSTER_VNUM = self.Monster_List[self.ListBox.GetSelectedItem().GetText()]
			self.MonsterCount.SetFocus()

		self.Monster_List = {}
		if self.ListBox != None:
			self.ListBox.Hide()
			self.ListBox = None
		if self.Thin != None:
			self.Thin.Hide()
			self.Thin = None

		self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)

	def	__SendChatPacket(self, packet):
		net.SendChatPacket(packet)

	def __OnValueUpdate(self):
		ui.EditLine.OnIMEUpdate(self.MonsterName)
		self.CreateListBox()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Close()
		else:
			self.Clear()
			self.Show()
			self.MonsterName.SetFocus()

	def	OnUpdate(self):
		if self.TEXT_OBJECTS["TimeGone"][1] != 0:
			self.TEXT_OBJECTS["TimeGone"][0].SetText(localeinfo.SecondToHMS(app.GetTime()-self.TEXT_OBJECTS["TimeGone"][1])) ## Time never moves backward

