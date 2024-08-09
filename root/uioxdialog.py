#-*- coding: iso-8859-1 -*-
import ui
import net
import chat
import item
import uiCommon
import localeInfo
import collections
import ZuoPanelHelper

class OxEventPoolDialog(ui.BoardWithTitleBar):
	class PoolWindow(ui.Window):
		def	__init__(self, parent, my_key):
			ui.Window.__init__(self)
			self.SetParent(parent)
			self.parent = parent
			self.TextLines = []
			self.iCount = 1
			self.iMaxCount = 0
			self.iKey = my_key
			self.__BuildWindow()

		def	__del__(self):
			ui.Window.__del__(self)
			self.TextLines = []

		def	__BuildWindow(self):
			## Size
			self.SetSize(130, 200)

			## Building pattern board
			self.PatternBoard = ui.ThinBoard()
			self.PatternBoard.SetParent(self)
			self.PatternBoard.SetSize(130, 100)
			self.PatternBoard.SetPosition(0, 0)
			self.PatternBoard.SetWindowHorizontalAlignCenter()
			self.PatternBoard.Show()

			## Building pane
			self.PatternWindow = ui.Window()
			self.PatternWindow.SetParent(self.PatternBoard)
			self.PatternWindow.SetSize(82, 60)
			self.PatternWindow.SetWindowHorizontalAlignCenter()
			self.PatternWindow.SetWindowVerticalAlignCenter()
			self.PatternWindow.Show()

			## Drawing pattern
			"""
				\    __________    /
				 \   __________   /
				  \  __________  /
				   \ __________ /
				    \__________/
			"""

			base = 0
			for i in xrange(5):
				txt = ""

				## Left padding
				for x in xrange(base):
					txt += " "

				base += 1

				txt += "\\"
				## Left blank
				for a in xrange(4-i):
					txt += " "

				## Center
				for a in xrange(10):
					txt += "_"

				## Right blank
				for a in xrange(4-i):
					txt += " "

				txt += "/"
				textLine = ui.TextLine()
				textLine.SetParent(self.PatternWindow)
				textLine.SetPosition(0, 12*i)
				textLine.SetText(txt)
				textLine.Show()
				self.TextLines.append(textLine)

			## Name - SlotBar
			self.Name_SlotBar = ui.MakeSlotBar(self, 0, 120, 120, 20)
			self.Name_SlotBar.SetWindowHorizontalAlignCenter()

			## Name - Text
			self.Name_TextLine = ui.MakeTextLine(self.Name_SlotBar)
			self.Name_TextLine.SetText("Nazwa puli: -")

			## Count - SlotBar
			self.Count_SlotBar = ui.MakeSlotBar(self, 0, 150, 120, 20)
			self.Count_SlotBar.SetWindowHorizontalAlignCenter()

			## Count - Text
			self.Count_TextLine = ui.MakeTextLine(self.Count_SlotBar)
			self.Count_TextLine.SetText("Iloœæ pytañ: 0")

			## Choice - SlotBar
			self.Choice_SlotBar = ui.MakeSlotBar(self, 0, 180, 15, 13)
			self.Choice_SlotBar.SetWindowHorizontalAlignCenter()

			## Count - Text
			self.Choice_TextLine = ui.MakeTextLine(self.Choice_SlotBar)
			self.Choice_TextLine.SetText("0")

			## Minus - Button
			self.Minus_Button = ui.MakeButton(self, -17, 181, "", "d:/ymir work/ui/game/windows/", "btn_minus_up.sub", "btn_minus_over.sub", "btn_minus_down.sub")
			self.Minus_Button.SetWindowHorizontalAlignCenter()
			self.Minus_Button.SAFE_SetEvent(self.__UpdateCount, -1)

			## Plus - Button
			self.Plus_Button = ui.MakeButton(self, 18, 181, "", "d:/ymir work/ui/game/windows/", "btn_plus_up.sub", "btn_plus_over.sub", "btn_plus_down.sub")
			self.Plus_Button.SetWindowHorizontalAlignCenter()
			self.Plus_Button.SAFE_SetEvent(self.__UpdateCount, 1)

			self.__UpdateCount()
			self.Show()

		def	UpdateName(self, s_name, i_score):
			self.Name_TextLine.SetText("Nazwa puli: %s" % s_name)
			self.Count_TextLine.SetText("Iloœæ pytañ: %d" % i_score)

			self.iMaxCount = i_score

		def	GetData(self):
			return (self.iKey, self.iCount)

		def	Clear(self):
			self.iMaxCount = 0
			self.__UpdateCount()

		def	__UpdateCount(self, arg = 0):
			self.iCount = max(0, min(self.iCount+arg, self.iMaxCount))
			self.Choice_TextLine.SetText("%d" % self.iCount)
			self.parent.RefreshCount()

	def __init__(self):
		ui.BoardWithTitleBar.__init__(self)
		self.PoolDict = {}
		self.__BuildWindow()

	def __del__(self):
		ui.BoardWithTitleBar.__del__(self)
		self.PoolDict = {}

	def	__BuildWindow(self):
		## Size & Title
		self.SetSize(30+(max(1, min(3, len(self.PoolDict)))*130), 60+30+(max(1, (len(self.PoolDict)/3)+1)*200))
		self.AddFlag("movable")
		self.AddFlag("float")
		self.SetTitleName("Pule pytañ")

		## Whole Count - SlotBar
		self.WholeCount_SlotBar = ui.MakeSlotBar(self, 0, 30+(max(1, (len(self.PoolDict)/3)+1)*200), 130, 20)
		self.WholeCount_SlotBar.SetWindowHorizontalAlignCenter()

		## Whole Count - TextLine
		self.WholeCount_TextLine = ui.MakeTextLine(self.WholeCount_SlotBar)
		self.WholeCount_TextLine.SetText("£¹czna iloœæ pytañ: 0")

		## Accept - Button
		self.Accept_Button = ui.MakeButton(self, 0, 25+30+(max(1, (len(self.PoolDict)/3)+1)*200), "", "d:/ymir work/ui/public/", "large_button_01.sub", "large_button_02.sub", "large_button_03.sub", "Dodaj pytania")
		self.Accept_Button.SetWindowHorizontalAlignCenter()
		self.Accept_Button.SAFE_SetEvent(self.__AcceptCount)
		self.Accept_Button.Show()

	def	AddPool(self, key, name, q_count):
		if key in self.PoolDict:
			self.PoolDict[key].UpdateName(name, q_count)
		else:
			self.PoolDict[key] = self.PoolWindow(self, key)
			self.PoolDict[key].UpdateName(name, q_count)
			self.__RedrawElements()

	def	RefreshCount(self):
		count = 0
		for val in self.PoolDict.values():
			count += val.GetData()[1]

		self.WholeCount_TextLine.SetText("£¹czna iloœæ pytañ: %d" % count)

	def	__RedrawElements(self):
		## Size
		self.SetSize(30+(max(1, min(3, len(self.PoolDict)))*130), 60+30+(max(1, (len(self.PoolDict)/3)+1)*200))

		## Pools' elements
		for key, element in self.PoolDict.items():
			element.SetPosition(15+(130*key if key < 3 else 130*(key%3)), 30+((key/3)*200))

		self.WholeCount_SlotBar.SetPosition(0, 30+(max(1, (len(self.PoolDict)/3)+1)*200))
		self.Accept_Button.SetPosition(0, 25+30+(max(1, (len(self.PoolDict)/3)+1)*200))

	def	__AcceptCount(self):
		for val in self.PoolDict.values():
			net.SendChatPacket("/ox_add_question_to_pool %d %d" % (val.GetData()[0]+1, val.GetData()[1]))
			val.Clear()

		self.RefreshCount()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.SetCenterPosition()
			self.SetTop()
			self.Show()

class OxEventDialog(ZuoPanelHelper.ZuoPanelHelper):

	TEXT_OBJECTS = {}
	BUTTON_OBJECTS = {}
	Item_List = {}
	Thin = None
	GiveRewardDialog = None
	ListBox = None

	MAX_SLOT_SIZE = 10
	BOARD_BASE_X = 300
	BOARD_BASE_Y = 530

	ITEM_VNUM = 0
	ITEM_COUNT = 0

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.poolDialog = OxEventPoolDialog()
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()

		self.TEXT_OBJECTS = {}
		self.BUTTON_OBJECTS = {}
		self.Item_List = {}
		self.Thin = None
		self.GiveRewardDialog = None
		self.ListBox = None
		self.ITEM_VNUM = 0
		self.ITEM_COUNT = 0

		if self.poolDialog:
			self.poolDialog.Hide()
			self.poolDialog = None

	def	__LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/oxdialog.py")
		except:
			import exception
			exception.Abort("OxDialog.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild
			self.board = GetObject("board")

			## Buttons
			self.BUTTON_OBJECTS["StartEvent"] = GetObject("Start_event_button")
			self.BUTTON_OBJECTS["CloseEvent"] = GetObject("Close_event_button")
			self.BUTTON_OBJECTS["CancelEvent"] = GetObject("GiveUp_event_button")
			self.BUTTON_OBJECTS["RewardEvent"] = GetObject("Reward_event_button")
			self.BUTTON_OBJECTS["NormalQuestion"] = GetObject("Normal_question_button")
			self.BUTTON_OBJECTS["TrapQuestion"] = GetObject("Trap_question_button")
			self.BUTTON_OBJECTS["FillPool"] = GetObject("Fill_Pool_Button")
			self.BUTTON_OBJECTS["ResetPool"] = GetObject("Reset_Pool_Button")

			## Texts
			self.TEXT_OBJECTS["OnlineAttenders"] = [GetObject("Online_attenders_text"), 0]
			self.TEXT_OBJECTS["OnlineObservers"] = [GetObject("Online_observs_text"), 0]
			self.TEXT_OBJECTS["PoolCount"] = [GetObject("PoolText"), 0]

			self.ItemName = GetObject("PrizeName")
			self.ItemName_SlotBar = GetObject("Prize_SlotBar")
			self.ItemCount = GetObject("PrizeCount")
			self.ItemTime = GetObject("TimeValue")
		except:
			import exception
			exception.Abort("OxDialog.LoadDialog.BindObject")

		## Binding Events
		self.BUTTON_OBJECTS["StartEvent"].SAFE_SetEvent(self.__SendChatPacket, "/ox_start_event")
		self.BUTTON_OBJECTS["CloseEvent"].SAFE_SetEvent(self.__SendChatPacket, "/ox_close_event")
		self.BUTTON_OBJECTS["CancelEvent"].SAFE_SetEvent(self.__SendChatPacket, "/ox_cancel_event")
		self.BUTTON_OBJECTS["RewardEvent"].SAFE_SetEvent(self.RewardButtonEvent)
		self.BUTTON_OBJECTS["NormalQuestion"].SAFE_SetEvent(self.__SendChatPacket, "/ox_question 0")
		self.BUTTON_OBJECTS["TrapQuestion"].SAFE_SetEvent(self.__SendChatPacket, "/ox_question 1")
		self.BUTTON_OBJECTS["FillPool"].SAFE_SetEvent(self.__OpenPoolDialog)
		self.BUTTON_OBJECTS["ResetPool"].SAFE_SetEvent(self.__SendChatPacket, "/ox_reset_pool")

		## Updating text
		self.TEXT_OBJECTS["OnlineAttenders"][0].SetText("Iloœæ uczestników: 0") ## Translate
		self.TEXT_OBJECTS["OnlineObservers"][0].SetText("Iloœæ obserwatorów: 0") ## Translate
		self.TEXT_OBJECTS["PoolCount"][0].SetText("Iloœæ pytañ w puli: 0") ## Translate

		self.board.SetCloseEvent(ui.__mem_func__(self.Hide))
		self.ItemName.OnIMEUpdate = ui.__mem_func__(self.__OnValueUpdate)

		self.SetCenterPosition()
		self.ItemName.SetFocus()

	def	UpdateAttendersCount(self, key, value):
		value = int(value)
		if key == "OnlineObservers":
			value -= self.TEXT_OBJECTS["OnlineAttenders"][1]

		templ_tab = {"OnlineAttenders" : "Iloœæ uczestników %d", "OnlineObservers" : "Iloœæ obserwatorów: %d", "PoolCount" : "Iloœæ pytañ w puli: %d"}
		if key in self.TEXT_OBJECTS:
			self.TEXT_OBJECTS[key][0].SetText(templ_tab[key] % value)
			self.TEXT_OBJECTS[key][1] = value

	def	CreateListBox(self):
		self.Item_List = {}
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
		self.ListBox.SetSelectEvent(lambda empty_arg: self.Clear(empty_arg))

		## Fetching Items by Name
		if self.ItemName.GetText() != "":
			item.GetItemsByName(self.ItemName.GetText(), "RetOxItems")
		else:
			self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)
			return

		if len(self.Item_List) == 0:
			self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)
			return
		else:
			self.Item_List = collections.OrderedDict(sorted(self.Item_List.items(), key = lambda x: x[1]))

		self.ListBox.SetViewItemCount(min(len(self.Item_List), self.MAX_SLOT_SIZE))
		self.ListBox.UpdateSize()
		self.Thin.SetSize(self.Thin.GetWidth(), self.ListBox.GetHeight())

		## Adding Items to the ListBox
		for i in self.Item_List.iterkeys():
			line = self.ListBoxItem()
			line.SetText(i)
			self.ListBox.AppendItem(line)

		## Reseting Board Size
		self.UpdateSize(self.BOARD_BASE_X, self.BOARD_BASE_Y)

		x, y = self.GetChild("Prize_window").GetLocalPosition()
		y += 17 + 15
		self.Thin.SetPosition(0, y)

		## Creating ScrollBar
		if len(self.Item_List) > self.MAX_SLOT_SIZE:
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
		if len(self.Item_List) > self.MAX_SLOT_SIZE:
			self.ScrollBar.Show()

	def	RewardButtonEvent(self):
		if self.ListBox != None:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Wybra³eœ niepoprawny przedmiot.") ## Translate
			return

		try:
			self.ITEM_COUNT = int(self.ItemCount.GetText())
		except ValueError:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Iloœæ przedmiotów jest nieprawid³owa.") ## Translate
			return

		if self.ITEM_COUNT <= 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Iloœæ przedmiotów jest nieprawid³owa.") ## Translate
			return

		if self.ITEM_VNUM > 0:
			self.AskGiveReward()
		else:
			chat.AppendChat(chat.CHAT_TYPE_INFO, "Wybra³eœ niepoprawny przedmiot.") ## Translate
			return

	def AskGiveReward(self):
		item.SelectItem(self.ITEM_VNUM)
		itemName = item.GetItemName()

		GiveRewardDialog = uiCommon.QuestionDialog()
		GiveRewardDialog.SetWidth(400)

		if self.GetTime():
			GiveRewardDialog.SetText("Czy chcesz podarowaæ %s w iloœci %d na czas %s?" % (itemName, self.ITEM_COUNT, localeInfo.SecondToDHM(self.GetTime()))) ## Translate
		else:
			GiveRewardDialog.SetText("Czy chcesz podarowaæ %s w iloœci %d?" % (itemName, self.ITEM_COUNT)) ## Translate

		GiveRewardDialog.SetAcceptEvent(lambda arg=True: self.AnswerGiveReward(arg))
		GiveRewardDialog.SetCancelEvent(lambda arg=False: self.AnswerGiveReward(arg))
		GiveRewardDialog.Open()
		self.GiveRewardDialog = GiveRewardDialog

	def AnswerGiveReward(self, flag):
		if flag:
			if self.GetTime():
				net.SendChatPacket("/ox_give_reward %d %d %d" % (self.ITEM_VNUM, self.ITEM_COUNT, self.GetTime()))
			else:
				net.SendChatPacket("/ox_give_reward %d %d" % (self.ITEM_VNUM, self.ITEM_COUNT))

		self.GiveRewardDialog.Close()
		self.GiveRewardDialog = None

	def	GetTime(self):
		try:
			int(self.ItemTime.GetText())
		except ValueError:
			return 0

		return int(self.ItemTime.GetText())

	def	Clear(self, empty_arg = None):
		if self.ListBox and self.ListBox.GetSelectedItem():
			self.ItemName.SetText(self.ListBox.GetSelectedItem().GetText())
			self.ITEM_VNUM = self.Item_List[self.ListBox.GetSelectedItem().GetText()]

		self.Item_List = {}
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
		ui.EditLine.OnIMEUpdate(self.ItemName)
		self.CreateListBox()

	def	__OpenPoolDialog(self):
		self.poolDialog.UpdateWindow()

