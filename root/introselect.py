import ui, exception, net, app, musicInfo, snd, playerSettingModule, chr,\
 systemSetting, grp, wndMgr, math, uiCommon, localeInfo, chat, dbg, uiScriptLocale,\
 event, uiToolTip, player, colorInfo

# import playerLoad

# playerLoad.Init()

JOB_WARRIOR = 0
JOB_ASSASSIN = 1
JOB_SURA = 2
JOB_SHAMAN = 3

M2_INIT_VALUE = -1
CHARACTER_SLOT_COUNT_MAX = 4

class MyCharacters:
	class MyUnit:
		def __init__(self, const_id, name, level, race, playtime, guildname, form, hair, acce,\
			stat_str, stat_dex, stat_hth, stat_int):
			self.UnitDataDic = {
				"ID"			:	const_id,
				"NAME"			:	name,
				"LEVEL"			:	level,
				"RACE"			:	race,
				"PLAYTIME"		:	playtime,
				"GUILDNAME"		:	guildname,
				"FORM"			:	form,
				"HAIR"			:	hair,
				"ACCE"			:	acce,
				"STR"			:	stat_str,
				"DEX"			:	stat_dex,
				"HTH"			:	stat_hth,
				"INT"			:	stat_int
			}
		
		def __del__(self):
			self.UnitDataDic = None
		
		def GetUnitData(self):
			return self.UnitDataDic
	
	def __init__(self, stream):
		self.MainStream		= stream
		self.PriorityData	= []
		self.myUnitDic		= {}
		self.HowManyChar	= 0
		self.EmptySlot		= []
		self.Race			= [None, None, None, None, None]
		self.Job			= [None, None, None, None, None]
		self.Guild_Name		= [None, None, None, None, None]
		self.Play_Time		= [None, None, None, None, None]
		self.Stat_Point		= { 0 : None, 1 : None, 2 : None, 3 : None, 4 : None }
	
	def __del__(self):
		for i in xrange(self.HowManyChar):
			chr.DeleteInstance(i)
		
		self.MainStream		= None
		self.PriorityData	= None
		self.myUnitDic		= None
		self.HowManyChar	= None
		self.EmptySlot		= None
		self.Race			= None
		self.Job			= None
		self.Guild_Name		= None
		self.Play_Time		= None
		self.Stat_Point		= None
	
	def LoadCharacterData(self):
		self.RefreshData()
		self.MainStream.All_ButtonInfoHide()
		
		for i in xrange(CHARACTER_SLOT_COUNT_MAX):
			pid = net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_ID) 
			if not pid:
				self.EmptySlot.append(i)
				continue
			
			name			= net.GetAccountCharacterSlotDataString(i, net.ACCOUNT_CHARACTER_SLOT_NAME)
			level			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_LEVEL)
			race			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_RACE)
			playtime		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
			guildname		= net.GetAccountCharacterSlotDataString(i, net.ACCOUNT_CHARACTER_SLOT_GUILD_NAME)
			form			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_FORM)
			hair			= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_HAIR)
			stat_str		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_STR)
			stat_dex		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_DEX)
			stat_hth		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_HTH)
			stat_int		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_INT)
			
			if app.ENABLE_SASH_COSTUME_SYSTEM:
				sash		= net.GetAccountCharacterSlotDataInteger(i, net.ACCOUNT_CHARACTER_SLOT_SASH)
			else:
				sash		= 0
			
			self.SetPriorityData(playtime, i)
			self.myUnitDic[i] = self.MyUnit(i, name, level, race, playtime, guildname, form, hair, sash, stat_str, stat_dex, stat_hth, stat_int)
		
		self.PriorityData.sort(reverse = True)
		for i in xrange(len(self.PriorityData)):
			(time, index) = self.PriorityData[i]
			DestDataDic = self.myUnitDic[index].GetUnitData()
			
			self.SetSortingData(i, DestDataDic["RACE"], DestDataDic["GUILDNAME"], DestDataDic["PLAYTIME"], DestDataDic["STR"], DestDataDic["DEX"], DestDataDic["HTH"], DestDataDic["INT"])
			self.MakeCharacter(i, DestDataDic["NAME"], DestDataDic["RACE"], DestDataDic["FORM"], DestDataDic["HAIR"], DestDataDic["ACCE"])
			self.MainStream.InitDataSet(i, DestDataDic["NAME"], DestDataDic["LEVEL"], DestDataDic["ID"])
		
		if self.HowManyChar:
			self.MainStream.SelectButton(0)
		
		return self.HowManyChar;
	
	def SetPriorityData(self, playtime, index):
		self.PriorityData.append([playtime, index])
	
	def MakeCharacter(self, slot, name, race, form, hair, sash):
		chr.CreateInstance(slot)
		chr.SelectInstance(slot)
		chr.SetVirtualID(slot)
		chr.SetNameString(name)
		
		chr.SetRace(race)
		chr.SetArmor(form)
		chr.SetHair(hair)
		if app.ENABLE_SASH_COSTUME_SYSTEM:
			chr.SetSash(sash)
		
		chr.SetMotionMode(chr.MOTION_MODE_GENERAL)
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
		
		chr.SetRotation(0.0)
		chr.Hide()
	
	def SetSortingData(self, slot, race, guildname, playtime, pStr, pDex, pHth, pInt):
		self.HowManyChar += 1
		self.Race[slot] = race
		self.Job[slot] = chr.RaceToJob(race)
		self.Guild_Name[slot] = guildname
		self.Play_Time[slot] = playtime
		self.Stat_Point[slot] = [pHth, pInt, pStr, pDex]
	
	def GetRace(self, slot):
		return self.Race[slot]
	
	def GetJob(self, slot):
		return self.Job[slot]
	
	def GetMyCharacterCount(self):
		return self.HowManyChar
	
	def GetEmptySlot(self):
		if not len(self.EmptySlot):
			return M2_INIT_VALUE
		
		return self.EmptySlot[0]
	
	def GetStatPoint(self, slot):
		return self.Stat_Point[slot]
	
	def GetGuildNamePlayTime(self, slot):
		return self.Guild_Name[slot], self.Play_Time[slot]
	
	def RefreshData(self):
		self.HowManyChar	= 0
		self.EmptySlot		= []
		self.PriorityData	= []
		self.Race			= [None, None, None, None, None]
		self.Guild_Name		= [None, None, None, None, None]
		self.Play_Time		= [None, None, None, None, None]
		self.Stat_Point		= { 0 : None, 1 : None, 2 : None, 3 : None, 4 : None }

class SelectCharacterWindow(ui.Window):
	EMPIRE_NAME = {
		net.EMPIRE_A : localeInfo.EMPIRE_A,
		net.EMPIRE_B : localeInfo.EMPIRE_B,
		net.EMPIRE_C : localeInfo.EMPIRE_C
	}
	
	EMPIRE_NAME_COLOR = {
		net.EMPIRE_A : (0.7450, 0, 0),
		net.EMPIRE_B : (0.8666, 0.6156, 0.1843),
		net.EMPIRE_C : (0.2235, 0.2549, 0.7490)
	}
	
	RACE_FACE_PATH = {
		playerSettingModule.RACE_WARRIOR_M		:	"D:/ymir work/ui/intro/public_intro/face_intro/face_warrior_m_0",
		playerSettingModule.RACE_ASSASSIN_W		:	"D:/ymir work/ui/intro/public_intro/face_intro/face_assassin_w_0",
		playerSettingModule.RACE_SURA_M			:	"D:/ymir work/ui/intro/public_intro/face_intro/face_sura_m_0",
		playerSettingModule.RACE_SHAMAN_W		:	"D:/ymir work/ui/intro/public_intro/face_intro/face_shaman_w_0",
		playerSettingModule.RACE_WARRIOR_W		:	"D:/ymir work/ui/intro/public_intro/face_intro/face_warrior_w_0",
		playerSettingModule.RACE_ASSASSIN_M		:	"D:/ymir work/ui/intro/public_intro/face_intro/face_assassin_m_0",
		playerSettingModule.RACE_SURA_W			:	"D:/ymir work/ui/intro/public_intro/face_intro/face_sura_w_0",
		playerSettingModule.RACE_SHAMAN_M		:	"D:/ymir work/ui/intro/public_intro/face_intro/face_shaman_m_0",
	}
	
	DISC_FACE_PATH = {
		playerSettingModule.RACE_WARRIOR_M		:"d:/ymir work/bin/icon/face/warrior_m.tga",
		playerSettingModule.RACE_ASSASSIN_W		:"d:/ymir work/bin/icon/face/assassin_w.tga",
		playerSettingModule.RACE_SURA_M			:"d:/ymir work/bin/icon/face/sura_m.tga",
		playerSettingModule.RACE_SHAMAN_W		:"d:/ymir work/bin/icon/face/shaman_w.tga",
		playerSettingModule.RACE_WARRIOR_W		:"d:/ymir work/bin/icon/face/warrior_w.tga",
		playerSettingModule.RACE_ASSASSIN_M		:"d:/ymir work/bin/icon/face/assassin_m.tga",
		playerSettingModule.RACE_SURA_W			:"d:/ymir work/bin/icon/face/sura_w.tga",
		playerSettingModule.RACE_SHAMAN_M		:"d:/ymir work/bin/icon/face/shaman_m.tga",
	}
	
	DESCRIPTION_FILE_NAME = (
		uiScriptLocale.JOBDESC_WARRIOR_PATH,
		uiScriptLocale.JOBDESC_ASSASSIN_PATH,
		uiScriptLocale.JOBDESC_SURA_PATH,
		uiScriptLocale.JOBDESC_SHAMAN_PATH,
	)
	
	JOB_LIST = {
		0	:	localeInfo.JOB_WARRIOR,
		1	:	localeInfo.JOB_ASSASSIN,
		2	:	localeInfo.JOB_SURA,
		3	:	localeInfo.JOB_SHAMAN,
	}
	
	EVENT_DESC_MAX_VISIBLE_LINE_COUNT = 15
	
	class DescriptionBox(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.descIndex = 0
		
		def __del__(self):
			ui.Window.__del__(self)
		
		def SetIndex(self, index):
			self.descIndex = index
		
		def OnRender(self):
			event.RenderEventSet(self.descIndex)
	
	class CharacterRenderer(ui.Window):
		def OnRender(self):
			grp.ClearDepthBuffer()
			grp.SetGameRenderState()
			grp.PushState()
			grp.SetOmniLight()
			
			screenWidth = wndMgr.GetScreenWidth()
			screenHeight = wndMgr.GetScreenHeight()
			newScreenWidth = float(screenWidth)
			newScreenHeight = float(screenHeight)
			
			grp.SetViewport(0.0, 0.0, newScreenWidth/screenWidth, newScreenHeight/screenHeight)
			
			app.SetCenterPosition(0.0, 0.0, 0.0)
			app.SetCamera(1550.0, 15.0, 180.0, 95.0)
			grp.SetPerspective(10.0, newScreenWidth/newScreenHeight, 1000.0, 3000.0)
			
			(x, y) = app.GetCursorPosition()
			grp.SetCursorPosition(x, y)
			
			chr.Deform()
			chr.Render()
			
			grp.RestoreViewport()
			grp.PopState()
			grp.SetInterfaceRenderState()
	
	def __init__(self, stream):
		ui.Window.__init__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, self)
		
		self.stream				= stream
		self.SelectSlot			= M2_INIT_VALUE
		self.SelectEmpire		= False
		self.ShowToolTip		= False
		self.select_job			= M2_INIT_VALUE
		self.select_race		= M2_INIT_VALUE
		self.LEN_STATPOINT		= 4
		self.descIndex			= 0
		self.statpoint			= [0, 0, 0, 0]
		self.curGauge			= [0.0, 0.0, 0.0, 0.0]
		self.Name_FontColor_Def	= grp.GenerateColor(0.7215, 0.7215, 0.7215, 1.0)
		self.Name_FontColor		= grp.GenerateColor(197.0/255.0, 134.0/255.0, 101.0/255.0, 1.0)
		self.Level_FontColor	= grp.GenerateColor(250.0/255.0, 211.0/255.0, 136.0/255.0, 1.0)
		self.Not_SelectMotion	= False
		self.MotionStart		= False
		self.MotionTime			= 0.0
		self.RealSlot			= []
		self.Disable			= False
	
	def __del__(self):
		ui.Window.__del__(self)
		net.SetPhaseWindow(net.PHASE_WINDOW_SELECT, 0)
	
	def __BindEvents(self):
		getChild = ui.__mem_func__(self.dlgBoard.GetChild)
		for i in xrange(4):
			object = getChild("CharacterSlot_{}".format(i))
			object.ShowToolTip = lambda arg = i : self.OverInToolTip(arg)
			object.HideToolTip = lambda : self.OverOutToolTip()
		
		getChild("create_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_CREATE : self.OverInToolTipETC(arg)
		getChild("create_button").HideToolTip = lambda : self.OverOutToolTip()
		getChild("delete_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_DELETE : self.OverInToolTipETC(arg)
		getChild("delete_button").HideToolTip = lambda : self.OverOutToolTip()
		getChild("start_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_SELECT : self.OverInToolTipETC(arg)
		getChild("start_button").HideToolTip = lambda : self.OverOutToolTip()
		getChild("exit_button").ShowToolTip = lambda arg = uiScriptLocale.SELECT_EXIT : self.OverInToolTipETC(arg)
		getChild("exit_button").HideToolTip = lambda : self.OverOutToolTip()
		getChild("prev_button").ShowToolTip = lambda arg = uiScriptLocale.CREATE_PREV : self.OverInToolTipETC(arg)
		getChild("prev_button").HideToolTip = lambda : self.OverOutToolTip()
		getChild("next_button").ShowToolTip = lambda arg = uiScriptLocale.CREATE_NEXT : self.OverInToolTipETC(arg)
		getChild("next_button").HideToolTip = lambda : self.OverOutToolTip()
		
		self.btnStart.SetEvent(ui.__mem_func__(self.StartGameButton))
		self.btnCreate.SetEvent(ui.__mem_func__(self.CreateCharacterButton))
		self.btnExit.SetEvent(ui.__mem_func__(self.ExitButton))
		self.btnDelete.SetEvent(ui.__mem_func__(self.InputPrivateCode))
		self.btnPrev.SetEvent(ui.__mem_func__(self.PrevDescriptionPage))
		self.btnNext.SetEvent(ui.__mem_func__(self.NextDescriptionPage))
		
		[self.CharacterButtonList[i].SetEvent(ui.__mem_func__(self.SelectButton), i) for i in xrange(len(self.CharacterButtonList))]
		for event_type in ["MOUSE_LEFT_BUTTON_DOWN", "MOUSE_OVER_IN", "MOUSE_OVER_OUT"]:
			[self.FaceImage[i].SetEvent(ui.__mem_func__(self.EventProgress), event_type, i) for i in xrange(len(self.FaceImage))]

		# self.statImages[0].SetEvent(ui.__mem_func__(self.EventOverStat), "MOUSE_OVER_IN", localeInfo.STAT_TOOLTIP_IMG_CON)
		# self.statImages[0].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.EventOverStat)
		# self.statImages[1].SetEvent(ui.__mem_func__(self.EventOverStat), "MOUSE_OVER_IN", localeInfo.STAT_TOOLTIP_IMG_INT)
		# self.statImages[1].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.EventOverStat)
		# self.statImages[2].SetEvent(ui.__mem_func__(self.EventOverStat), "MOUSE_OVER_IN", localeInfo.STAT_TOOLTIP_IMG_STR)
		# self.statImages[2].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.EventOverStat)
		# self.statImages[3].SetEvent(ui.__mem_func__(self.EventOverStat), "MOUSE_OVER_IN", localeInfo.STAT_TOOLTIP_IMG_DEX)
		# self.statImages[3].SAFE_SetStringEvent("MOUSE_OVER_OUT", self.EventOverStat)

		self.mycharacters = MyCharacters(self);
		self.mycharacters.LoadCharacterData()
		if not self.mycharacters.GetMyCharacterCount():
			self.stream.SetCharacterSlot(self.mycharacters.GetEmptySlot())
			self.SelectEmpire = True
		
		self.chrRenderer = self.CharacterRenderer()
		self.chrRenderer.SetParent(self.backGround)
		self.chrRenderer.Show()
		
		empire_id = net.GetEmpireID()
		if empire_id not in [net.EMPIRE_A, net.EMPIRE_C]:
			empire_id = net.EMPIRE_A
		
		self.SetEmpire(empire_id)
		self.myID.SetText(localeInfo.SELECT_CHARACTER_WINDOW_TITLE)

		if self.mycharacters.GetMyCharacterCount() == CHARACTER_SLOT_COUNT_MAX:
			self.btnCreate.Disable()
	
	def Open(self):
		self.dlgBoard = ui.ScriptWindow()
		try: ui.PythonScriptLoader().LoadScriptFile( self.dlgBoard, "uiscript/SelectCharacterWindow.py")
		except: exception.Abort("SelectCharacterWindow.LoadScriptFile")
		
		self.backGroundDict = {
			net.EMPIRE_B : "d:/ymir work/ui/intro/empire_default/background/empire_jinno.sub",
			net.EMPIRE_C : "d:/ymir work/ui/intro/empire_default/background/empire_jinno.sub",
		}
		
		self.flagDict = {
			net.EMPIRE_B : "assets/ui/empire_flags/red_flag.png",
			net.EMPIRE_C : "assets/ui/empire_flags/blue_flag.png",
		}

		getChild = ui.__mem_func__(self.dlgBoard.GetChild)

		(self.NameList, self.FaceImage, self.CharacterButtonList) = ([], [], [])
		[self.NameList.append(getChild(object_name)) for object_name in ["name_warrior", "name_assassin", "name_sura", "name_shaman"]]
		[self.FaceImage.append(getChild(object_name)) for object_name in ["CharacterFace_0", "CharacterFace_1", "CharacterFace_2", "CharacterFace_3"]]
		[self.CharacterButtonList.append(getChild(object_name)) for object_name in ["CharacterSlot_0", "CharacterSlot_1", "CharacterSlot_2", "CharacterSlot_3"]]

		self.backGround		= getChild("BackGround")
		self.empireName		= getChild("EmpireName")
		self.flag			= getChild("EmpireFlag")
		self.btnStart		= getChild("start_button")
		self.btnCreate		= getChild("create_button")
		self.btnDelete		= getChild("delete_button")
		self.btnExit		= getChild("exit_button")

		(self.statImages, self.statValue, self.GaugeList) = ([], [], [])
		[self.statImages.append(getChild(object_name)) for object_name in ["hth_img", "int_img", "str_img", "dex_img"]]
		[self.statValue.append(getChild(object_name)) for object_name in ["hth_value", "int_value", "str_value", "dex_value"]]
		[self.GaugeList.append(getChild(object_name)) for object_name in ["hth_gauge", "int_gauge", "str_gauge", "dex_gauge"]]

		self.textBoard		= getChild("text_board")
		self.btnPrev		= getChild("prev_button")
		self.btnNext		= getChild("next_button")
		self.discFace		= getChild("DiscFace")
		self.raceNameText	= getChild("raceName_Text")
		self.myID			= getChild("my_id")
		
		self.__BindEvents()
		
		self.descriptionBox = self.DescriptionBox()
		self.descriptionBox.Show()
		
		self.toolTip = uiToolTip.ToolTip()
		self.toolTip.ClearToolTip()
		
		if musicInfo.selectMusic != "":
			snd.SetMusicVolume(systemSetting.GetMusicVolume())
			snd.FadeInMusic("BGM/"+musicInfo.selectMusic)
		
		app.ShowCursor()
		self.dlgBoard.Show()
		self.Show()
	
	def EventProgress(self, event_type, slot):
		if self.Disable:
			return

		if "MOUSE_LEFT_BUTTON_DOWN" == event_type:
			if slot == self.SelectSlot:
				return
			
			snd.PlaySound("sound/ui/click.wav")
			self.SelectButton(slot)

		elif "MOUSE_OVER_IN" == event_type:
			for button in self.CharacterButtonList:
				button.SetUp()
			
			self.CharacterButtonList[self.SelectSlot].Down()
			self.OverInToolTip(slot)

		elif "MOUSE_OVER_OUT" == event_type:
			for button in self.CharacterButtonList:
				button.SetUp()
			
			self.CharacterButtonList[self.SelectSlot].Down()
			self.OverOutToolTip()
	
	def EventOverStat(self, type = "", data = ""):
		if type == "MOUSE_OVER_IN":
			self.OverInToolTipETC(data, 0xFFf4a460)
		else:
			self.OverOutToolTip()

	def SelectButton(self, slot):
		if slot >= self.mycharacters.GetMyCharacterCount() or slot == self.SelectSlot:
			return
		
		if self.Not_SelectMotion or self.MotionTime != 0.0:
			self.CharacterButtonList[slot].SetUp()
			return
		
		for button in self.CharacterButtonList:
			button.SetUp()
		
		self.SelectSlot = slot
		self.CharacterButtonList[self.SelectSlot].Down()
		
		self.stream.SetCharacterSlot(self.RealSlot[self.SelectSlot])
		self.select_job = self.mycharacters.GetJob(self.SelectSlot)
		
		event.ClearEventSet(self.descIndex)
		self.descIndex = event.RegisterEventSet(self.DESCRIPTION_FILE_NAME[self.select_job])
		event.SetVisibleLineCount(self.descIndex, self.EVENT_DESC_MAX_VISIBLE_LINE_COUNT)
		event.SetRestrictedCount(self.descIndex, 35)
		
		if self.EVENT_DESC_MAX_VISIBLE_LINE_COUNT >= event.GetTotalLineCount(self.descIndex):
			self.btnPrev.Hide()
			self.btnNext.Hide()
		else:
			self.btnPrev.Show()
			self.btnNext.Show()
		
		self.ResetStat()
		for i in xrange(len(self.NameList)):
			self.NameList[i].SetAlpha(1 if self.select_job == i else 0)
		
		self.select_race = self.mycharacters.GetRace(self.SelectSlot)
		for i in xrange(self.mycharacters.GetMyCharacterCount()):
			if slot == i:
				self.FaceImage[slot].LoadImage(self.RACE_FACE_PATH[self.select_race] + "1.sub")
				self.CharacterButtonList[slot].SetAppendTextColor(0, self.Name_FontColor)
			else:
				self.FaceImage[i].LoadImage(self.RACE_FACE_PATH[self.mycharacters.GetRace(i)] + "2.sub")
				self.CharacterButtonList[i].SetAppendTextColor(0, self.Name_FontColor_Def)
		
		self.discFace.LoadImage(self.DISC_FACE_PATH[self.select_race])
		self.raceNameText.SetText(self.JOB_LIST[self.select_job])
		
		chr.Hide()
		chr.SelectInstance(self.SelectSlot)
		chr.Show()
	
	def Close(self):
		del self.mycharacters
		
		self.EMPIRE_NAME			= None
		self.EMPIRE_NAME_COLOR		= None
		self.RACE_FACE_PATH			= None
		self.DISC_FACE_PATH			= None
		self.DESCRIPTION_FILE_NAME	= None
		self.JOB_LIST				= None
		
		self.SelectSlot				= None
		self.SelectEmpire			= None
		self.ShowToolTip			= None
		self.LEN_STATPOINT			= None
		self.descIndex				= None
		self.statpoint				= None
		self.curGauge				= None
		self.Name_FontColor_Def		= None
		self.Name_FontColor			= None
		self.Level_FontColor		= None
		self.Not_SelectMotion		= None
		self.MotionStart			= None
		self.MotionTime				= None
		self.RealSlot				= None
		
		self.select_job				= None
		self.select_race			= None
		
		self.dlgBoard				= None
		self.backGround				= None
		self.backGroundDict			= None
		self.NameList				= None
		self.empireName				= None
		self.flag					= None
		self.flagDict				= None
		self.btnStart				= None
		self.btnCreate				= None
		self.btnDelete				= None
		self.btnExit				= None
		self.FaceImage				= None
		self.CharacterButtonList	= None
		self.statImages				= None
		self.statValue				= None
		self.GaugeList				= None
		self.textBoard				= None
		self.btnPrev				= None
		self.btnNext				= None
		self.raceNameText			= None
		self.myID					= None
		
		self.descriptionBox			= None
		self.toolTip				= None
		self.Disable				= None
		
		if musicInfo.selectMusic != "":
			snd.FadeOutMusic("BGM/"+musicInfo.selectMusic)
		
		self.Hide()
		self.KillFocus()
		app.HideCursor()
		event.Destroy()
	
	def SetEmpire(self, empire_id):
		self.empireName.SetText(self.EMPIRE_NAME.get(empire_id, ""))
		rgb = self.EMPIRE_NAME_COLOR[empire_id]
		self.empireName.SetFontColor(rgb[0], rgb[1], rgb[2])
		
		if empire_id != net.EMPIRE_A:
			self.flag.LoadImage(self.flagDict[empire_id])
			self.backGround.LoadImage(self.backGroundDict[empire_id])
			self.backGround.SetScale(float(wndMgr.GetScreenWidth()) / 1024.0, float(wndMgr.GetScreenHeight()) / 768.0)
	
	def CreateCharacterButton(self):
		slotNumber = self.mycharacters.GetEmptySlot()
		if slotNumber == M2_INIT_VALUE:
			self.stream.popupWindow.Close()
			self.stream.popupWindow.Open(localeInfo.CREATE_FULL, 0, localeInfo.UI_OK, True)
			return
		
		pid = self.GetCharacterSlotPID(slotNumber)
		if not pid:
			self.stream.SetCharacterSlot(slotNumber)
			if not self.mycharacters.GetMyCharacterCount():
				self.SelectEmpire = True
			else:
				self.stream.SetCreateCharacterPhase()
				self.Hide()
	
	def ExitButton(self):
		self.stream.SetLoginPhase()
		self.Hide()
	
	def StartGameButton(self):
		if not self.mycharacters.GetMyCharacterCount() or self.MotionTime != 0.0:
			return
		
		self.DisableWindow()
		chr.PushOnceMotion(chr.MOTION_INTRO_SELECTED)
		self.MotionStart = True
		self.MotionTime = app.GetTime()
	
	def OnUpdate(self):
		chr.Update()
		self.ToolTipProgress()
		
		if self.SelectEmpire:
			self.SelectEmpire = False
			self.stream.SetReselectEmpirePhase()
			self.Hide()
		
		if self.MotionStart and app.GetTime() - self.MotionTime >= 2.0:
			self.MotionStart = False
			chrSlot = self.stream.GetCharacterSlot()
			
			if musicInfo.selectMusic != "":
				snd.FadeLimitOutMusic("BGM/"+musicInfo.selectMusic, systemSetting.GetMusicVolume()*0.05)
			
			net.DirectEnter(chrSlot)
			playTime = net.GetAccountCharacterSlotDataInteger(chrSlot, net.ACCOUNT_CHARACTER_SLOT_PLAYTIME)
			
			player.SetPlayTime(playTime)
			chat.Clear()
		
		(xposEventSet, yposEventSet) = self.textBoard.GetGlobalPosition()
		event.UpdateEventSet(self.descIndex, xposEventSet+7, -(yposEventSet+7))
		self.descriptionBox.SetIndex(self.descIndex)
		
		for i in xrange(self.LEN_STATPOINT):
			self.GaugeList[i].SetPercentage(self.curGauge[i], 1.0)
			self.GaugeList[i].SetBGPercentage(self.curGauge[i], 1.0)
	
	def GetCharacterSlotPID(self, slotIndex):
		return net.GetAccountCharacterSlotDataInteger(slotIndex, net.ACCOUNT_CHARACTER_SLOT_ID)
	
	def All_ButtonInfoHide(self):
		for i in xrange(CHARACTER_SLOT_COUNT_MAX):
			self.CharacterButtonList[i].Hide()
			self.FaceImage[i].Hide()
	
	def InitDataSet(self, slot, name, level, real_slot):
		width = self.CharacterButtonList[slot].GetWidth()
		height = self.CharacterButtonList[slot].GetHeight()
		
		self.CharacterButtonList[slot].AppendTextLine(name, localeInfo.UI_DEF_FONT, self.Name_FontColor_Def	, "right", width - 12, height/4 + 2)
		self.CharacterButtonList[slot].AppendTextLine("Lv." + str(level), localeInfo.UI_DEF_FONT, self.Level_FontColor, "left", width - 42, height*3/4)
		
		self.CharacterButtonList[slot].Show()
		self.FaceImage[slot].LoadImage(self.RACE_FACE_PATH[self.mycharacters.GetRace(slot)] + "2.sub")
		self.FaceImage[slot].Show()
		self.RealSlot.append(real_slot)
	
	def InputPrivateCode(self):
		if not self.mycharacters.GetMyCharacterCount():
			return
		
		privateInputBoard = uiCommon.InputDialogWithDescription()
		privateInputBoard.SetTitle(localeInfo.INPUT_PRIVATE_CODE_DIALOG_TITLE)
		privateInputBoard.SetAcceptEvent(ui.__mem_func__(self.AcceptInputPrivateCode))
		privateInputBoard.SetCancelEvent(ui.__mem_func__(self.CancelInputPrivateCode))
		privateInputBoard.SetSecretMode()
		privateInputBoard.SetMaxLength(7)
		privateInputBoard.SetBoardWidth(250)
		privateInputBoard.SetDescription(localeInfo.INPUT_PRIVATE_CODE_DIALOG_DESCRIPTION)
		privateInputBoard.Open()
		self.privateInputBoard = privateInputBoard
		
		self.DisableWindow()
		
		if not self.Not_SelectMotion:
			self.Not_SelectMotion = True
			chr.PushOnceMotion(chr.MOTION_INTRO_NOT_SELECTED, 0.1)
	
	def AcceptInputPrivateCode(self):
		privateCode = self.privateInputBoard.GetText()
		if not privateCode:
			return
		
		pid = net.GetAccountCharacterSlotDataInteger(self.RealSlot[self.SelectSlot], net.ACCOUNT_CHARACTER_SLOT_ID)
		if not pid:
			self.PopupMessage(localeInfo.SELECT_EMPTY_SLOT)
			return
		
		net.SendDestroyCharacterPacket(self.RealSlot[self.SelectSlot], privateCode)
		self.PopupMessage(localeInfo.SELECT_DELEING)
		
		self.CancelInputPrivateCode()
		return True
	
	def CancelInputPrivateCode(self):
		self.privateInputBoard = None
		self.Not_SelectMotion = False
		chr.SetLoopMotion(chr.MOTION_INTRO_WAIT)
		self.EnableWindow()
		return True
	
	def OnDeleteSuccess(self, slot):
		self.PopupMessage(localeInfo.SELECT_DELETED)
		for i in xrange(len(self.RealSlot)):
			chr.DeleteInstance(i)
		
		self.RealSlot = []
		self.SelectSlot = M2_INIT_VALUE
		
		for button in self.CharacterButtonList:
			button.AppendTextLineAllClear()
		
		if not self.mycharacters.LoadCharacterData():
			self.stream.popupWindow.Close()
			self.stream.SetCharacterSlot(self.mycharacters.GetEmptySlot())
			self.SelectEmpire = True
	
	def OnDeleteFailure(self):
		self.PopupMessage(localeInfo.SELECT_CAN_NOT_DELETE)
	
	def EmptyFunc(self):
		pass
	
	def PopupMessage(self, msg, func=0):
		if not func:
			func = self.EmptyFunc
		
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(msg, func, localeInfo.UI_OK)
	
	def RefreshStat(self):
		statSummary = 90.0
		self.curGauge = [
			float(self.statpoint[0])/statSummary,
			float(self.statpoint[1])/statSummary,
			float(self.statpoint[2])/statSummary,
			float(self.statpoint[3])/statSummary,
		]
		
		for i in xrange(self.LEN_STATPOINT):
			self.statValue[i].SetText(str(self.statpoint[i]))
	
	def ResetStat(self):
		myStatPoint = self.mycharacters.GetStatPoint(self.SelectSlot)
		if not myStatPoint:
			return
		
		for i in xrange(self.LEN_STATPOINT):
			self.statpoint[i] = myStatPoint[i]
		
		self.RefreshStat()
	
	def PrevDescriptionPage(self):
		if True == event.IsWait(self.descIndex):
			if event.GetVisibleStartLine(self.descIndex) - self.EVENT_DESC_MAX_VISIBLE_LINE_COUNT >= 0:
				event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) - self.EVENT_DESC_MAX_VISIBLE_LINE_COUNT)
				event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)
	
	def NextDescriptionPage(self):
		if True == event.IsWait(self.descIndex):
			event.SetVisibleStartLine(self.descIndex, event.GetVisibleStartLine(self.descIndex) + self.EVENT_DESC_MAX_VISIBLE_LINE_COUNT)
			event.Skip(self.descIndex)
		else:
			event.Skip(self.descIndex)
	
	def OverInToolTip(self, slot):
		GuildName = colorInfo.Colorize(localeInfo.GUILD_NAME, 0xFF68bcff)
		(myGuildName, myPlayTime) = self.mycharacters.GetGuildNamePlayTime(slot)
		(pos_x, pos_y) = self.CharacterButtonList[slot].GetGlobalPosition()
		
		if not myGuildName:
			myGuildName = localeInfo.SELECT_NOT_JOIN_GUILD
		
		guild_name = GuildName + ": " + myGuildName
		
		play_time = colorInfo.Colorize(uiScriptLocale.SELECT_PLAYTIME, 0xFF68bcff)
		day = myPlayTime / (60 * 24)
		if day:
			play_time = play_time + " " + str(day) + localeInfo.DAY
		
		hour = (myPlayTime - (day * 60 * 24))/60
		if hour:
			play_time = play_time + " " + str(hour) + localeInfo.HOUR
		
		min = myPlayTime - (hour * 60) - (day * 60 * 24)
		play_time = play_time + " " + str(min) + localeInfo.MINUTE
		
		textlen = max(len(guild_name), len(play_time))
		tooltip_width = 6 * textlen + 22
		
		self.toolTip.ClearToolTip()
		self.toolTip.SetThinBoardSize(tooltip_width)
		
		self.toolTip.SetToolTipPosition(pos_x + 173 + tooltip_width/2, pos_y + 34)
		self.toolTip.AppendTextLine(guild_name, 0xFFffffff, False)
		self.toolTip.AppendTextLine(play_time, 0xFFffffff, False)
		self.toolTip.Show()
	
	def OverInToolTipETC(self, arg, color = 0xFFffffff):
		arglen = len(str(arg))
		(pos_x, pos_y) = wndMgr.GetMousePosition()
		
		self.toolTip.ClearToolTip()
		self.toolTip.SetThinBoardSize(11 * arglen)
		self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
		self.toolTip.AppendTextLine(arg, color)
		self.toolTip.Show()
		self.ShowToolTip = True
	
	def OverOutToolTip(self):
		self.toolTip.Hide()
		self.ShowToolTip = False
	
	def ToolTipProgress(self):
		if self.ShowToolTip:
			pos_x, pos_y = wndMgr.GetMousePosition()
			self.toolTip.SetToolTipPosition(pos_x + 50, pos_y + 50)
	
	def SameLoginDisconnect(self):
		self.stream.popupWindow.Close()
		self.stream.popupWindow.Open(localeInfo.LOGIN_FAILURE_SAMELOGIN, self.ExitButton, localeInfo.UI_OK, True)
	
	def OnIMEReturn(self):
		self.StartGameButton()
		return True
	
	def OnPressEscapeKey(self):
		self.ExitButton()
		return True
	
	def OnPressExitKey(self):
		# self.PopupMessage("Gonna exit?")
		# self.ExitButton()
		return True
	
	def OnKeyDown(self, key):
		if self.MotionTime != 0.0:
			return
		
		if 2 == key:
			self.SelectButton(0)
		elif 3 == key:
			self.SelectButton(1)
		elif 4 == key:
			self.SelectButton(2)
		elif 5 == key:
			self.SelectButton(3)
		elif 6 == key:
			self.SelectButton(4)
		elif 203 == key or 205 == key or 200 == key or 208 == key:
			self.KeyInputUpDown(key)
		else:
			return True
		
		return True
	
	def KeyInputUpDown(self, key):
		idx = self.SelectSlot
		maxValue = self.mycharacters.GetMyCharacterCount()
		if 203 == key or 200 == key:
			idx = idx - 1
			if idx < 0:
				idx = maxValue - 1
		elif 205 == key or 208 == key:
			idx = idx + 1
			if idx >= maxValue:
				idx = 0
		else:
			self.SelectButton(0)
		
		self.SelectButton(idx)
	
	def DisableWindow(self):
		self.btnStart.Disable()
		self.btnCreate.Disable()
		self.btnExit.Disable()
		
		self.btnDelete.SetUp()
		self.btnDelete.Disable()
		
		self.btnPrev.Disable()
		self.btnNext.Disable()
		self.toolTip.Hide()
		self.ShowToolTip = False
		self.Disable = True
		# for button in self.CharacterButtonList:
		# 	button.Disable()

	def EnableWindow(self):
		self.btnStart.Enable()
		if self.mycharacters.GetMyCharacterCount() != CHARACTER_SLOT_COUNT_MAX:
			self.btnCreate.Enable()
		self.btnExit.Enable()
		self.btnDelete.Enable()
		self.btnPrev.Enable()
		self.btnNext.Enable()
		self.Disable = False
		
		for buttonIndex in xrange(len(self.CharacterButtonList)):
			button = self.CharacterButtonList[buttonIndex]
			button.Enable()
			button.SetUp() if self.SelectSlot != buttonIndex else button.Down()
	
	def OnCreateFailure(self, type):
		if 0 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_NAME)
		elif 1 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_ALREADY_EXIST_NAME)
		elif 100 == type:
			self.PopupMessage(localeInfo.SELECT_CHANGE_FAILURE_STRANGE_INDEX)
