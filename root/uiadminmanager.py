import ui
import admin
import chat
import localeInfo
import miniMap
import uiMiniMap
import wndMgr
import background
import playerSettingModule
import player
import net
import app
import item
import uiTaskBar
import uiToolTip
import chr
import skill
import uiCommon
import grp
import os

ENABLE_LOG_PAGES = True

SKILL_INDEX_DICT = {
	playerSettingModule.JOB_WARRIOR : {
		1 : (1, 2, 3, 4, 5, 0, 0, 0, 137, 0, 138, 0, 139, 0,),
		2 : (16, 17, 18, 19, 20, 0, 0, 0, 137, 0, 138, 0, 139, 0,),
		"SUPPORT" : (122, 123, 121, 124, 129, 132, 0, 0, 130, 131, 133, 134),
	},
	playerSettingModule.JOB_ASSASSIN : {
		1 : (31, 32, 33, 34, 35, 0, 0, 0, 137, 0, 138, 0, 139, 0, 140,),
		2 : (46, 47, 48, 49, 50, 0, 0, 0, 137, 0, 138, 0, 139, 0, 140,),
		"SUPPORT" : (122, 123, 121, 124, 129, 132, 0, 0, 130, 131, 133, 134),
	},
	playerSettingModule.JOB_SURA : {
		1 : (61, 62, 63, 64, 65, 66, 0, 0, 137, 0, 138, 0, 139, 0,),
		2 : (76, 77, 78, 79, 80, 81, 0, 0, 137, 0, 138, 0, 139, 0,),
		"SUPPORT" : (122, 123, 121, 124, 129, 132, 0, 0, 130, 131, 133, 134),
	},
	playerSettingModule.JOB_SHAMAN : {
		1 : (91, 92, 93, 94, 95, 96, 0, 0, 137, 0, 138, 0, 139, 0,),
		2 : (106, 107, 108, 109, 110, 111, 0, 0, 137, 0, 138, 0, 139, 0,),
		"SUPPORT" : (122, 123, 121, 124, 129, 132, 0, 0, 130, 131, 133, 134),
	},
}

class AdminManagerWindow(ui.ScriptWindow):
	class MapViewer_AtlasRenderer(ui.Window):
		def __init__(self):
			ui.Window.__init__(self)
			self.AddFlag("not_pick")

		def OnUpdate(self):
			miniMap.UpdateAdminManagerAtlas()

		def OnRender(self):
			(x, y) = self.GetGlobalPosition()
			miniMap.RenderAdminManagerAtlas(float(x), float(y), float(self.GetWidth()), float(self.GetHeight()))

		def HideAtlas(self):
			miniMap.HideAdminManagerAtlas()

		def ShowAtlas(self):
			miniMap.ShowAdminManagerAtlas()

	class TextToolTip(ui.Window):
		def __init__(self):
			ui.Window.__init__(self, "TOP_MOST")
			self.SetWindowName("GiftBox")
			textLine = ui.TextLine()
			textLine.SetParent(self)
			textLine.SetHorizontalAlignCenter()
			textLine.SetOutline()
			textLine.Show()
			self.textLine = textLine

		def __del__(self):
			ui.Window.__del__(self)

		def SetText(self, text):
			self.textLine.SetText(text)

		def OnRender(self):
			(mouseX, mouseY) = wndMgr.GetMousePosition()
			self.textLine.SetPosition(mouseX, mouseY - 15)

	DISABLE_COLOR = grp.GenerateColor(0.33, 0.33, 0.33, 0.3)

	PAGE_GENERAL = 0
	PAGE_MAPVIEWER = 1
	PAGE_OBSERVER = 2
	PAGE_BAN = 3
	PAGE_ITEM = 4
	if ENABLE_LOG_PAGES:
		PAGE_LOGS = 5
		PAGE_MAX_NUM = 6
	else:
		PAGE_MAX_NUM = 5

	FACE_IMAGE_DICT = {
		playerSettingModule.RACE_WARRIOR_M	: "d:/ymir work/ui/game/admin/face/warrior_m%s.tga",
		playerSettingModule.RACE_WARRIOR_W	: "d:/ymir work/ui/game/admin/face/warrior_w%s.tga",
		playerSettingModule.RACE_ASSASSIN_M	: "d:/ymir work/ui/game/admin/face/assassin_m%s.tga",
		playerSettingModule.RACE_ASSASSIN_W	: "d:/ymir work/ui/game/admin/face/assassin_w%s.tga",
		playerSettingModule.RACE_SURA_M		: "d:/ymir work/ui/game/admin/face/sura_m%s.tga",
		playerSettingModule.RACE_SURA_W		: "d:/ymir work/ui/game/admin/face/sura_w%s.tga",
		playerSettingModule.RACE_SHAMAN_M	: "d:/ymir work/ui/game/admin/face/shaman_m%s.tga",
		playerSettingModule.RACE_SHAMAN_W	: "d:/ymir work/ui/game/admin/face/shaman_w%s.tga",
		# playerSettingModule.RACE_WOLFMAN_M	: "d:/ymir work/ui/game/admin/face/wolfman_m%s.tga",
	}

	OBSERVER_NAVI_GENERAL = 0
	OBSERVER_NAVI_ITEM = 1
	OBSERVER_NAVI_BAN = 2
	OBSERVER_NAVI_MAX_NUM = 3

	OBSERVER_EMPIRE_IMAGE_DICT = {
		net.EMPIRE_A : "d:/ymir work/ui/game/admin/empireflag_a.tga",
		net.EMPIRE_B : "d:/ymir work/ui/game/admin/empireflag_b.tga",
		net.EMPIRE_C : "d:/ymir work/ui/game/admin/empireflag_c.tga",
	}

	BAN_CHAT_STATE_NONE = 0
	BAN_CHAT_STATE_SEARCHING = 1
	BAN_CHAT_STATE_SEARCH_FAIL = 2
	BAN_CHAT_STATE_SEARCH_RESULT = 3
	BAN_CHAT_STATE_MAX_NUM = 4
	BAN_ACCOUNT_STATE_NONE = 0
	BAN_ACCOUNT_STATE_SEARCHING = 1
	BAN_ACCOUNT_STATE_SEARCH_FAIL = 2
	BAN_ACCOUNT_STATE_SEARCH_RESULT = 3
	BAN_ACCOUNT_STATE_MAX_NUM = 4

	BAN_ACTIVE_COLOR = grp.GenerateColor(1.0, 110.0/255.0, 110.0/255.0, 1.0)
	BAN_INACTIVE_COLOR = grp.GenerateColor(110.0/255.0, 1.0, 110.0/255.0, 1.0)

	#################################################
	## MAIN FUNCTIONS
	#################################################

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.currentPageIndex = -1

		self.pageNeedRefresh = []
		self.pageData = []
		for i in xrange(self.PAGE_MAX_NUM):
			self.pageNeedRefresh.append(True)
			self.pageData.append({})

		self.LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "UIScript/AdminManagerWindow.py")
		except:
			import exception
			exception.Abort("AdminManagerWindow.LoadDialog.LoadScript")

		try:
			GetObject=self.GetChild
			self.board = GetObject("board")

			self.pages = {
				# page general
				self.PAGE_GENERAL : {
					"wnd" : GetObject("page_general"),
					"online_list" : GetObject("general_online_player_table"),
					"online_scroll" : GetObject("general_online_player_scrollbar"),
					"dividing_line" : GetObject("general_online_player_dividing_line"),
					"online_search" : GetObject("general_online_player_search"),
					"online_search_edit" : GetObject("general_online_player_search_edit"),
					"online_search_btn" : GetObject("general_online_player_search_button"),
					"main_info" : GetObject("general_main_information_window"),
					"user_count" : GetObject("general_current_user_count"),
					"gm_item_trade" : GetObject("general_gm_item_trade_checkbox"),
				},
				# page mapviewer
				self.PAGE_MAPVIEWER : {
					"wnd" : GetObject("page_mapviewer"),
					"atlas" : GetObject("mapviewer_atlas"),
					"no_select_wnd" : GetObject("mapviewer_no_map_selected"),
					"select_list" : GetObject("mapviewer_select_list"),
					"select_scroll" : GetObject("mapviewer_select_scrollbar"),
					"select_btn" : GetObject("mapviewer_select_button"),
					"select_line" : GetObject("mapviewer_dividing_line2"),
					"option_%d" % miniMap.ADMIN_SHOW_PC : GetObject("mapviewer_option_player"),
					"option_%d" % miniMap.ADMIN_SHOW_MOB : GetObject("mapviewer_option_mob"),
					"option_%d" % miniMap.ADMIN_SHOW_STONE : GetObject("mapviewer_option_stone"),
					"option_%d" % miniMap.ADMIN_SHOW_NPC : GetObject("mapviewer_option_npc"),
					"stop_btn" : GetObject("mapviewer_stop_button"),
				},
				# page observer
				self.PAGE_OBSERVER : {
					"wnd" : GetObject("page_observer"),
					"stopped_wnd" : GetObject("observer_stopped_wnd"),
					"stopped_edit" : GetObject("observer_stopped_name_edit"),
					"stopped_btn" : GetObject("observer_stopped_button"),
					"running_wnd" : GetObject("observer_running_wnd"),
					"navi_buttons" : [GetObject("observer_navi_button_%d" % (i + 1)) for i in xrange(self.OBSERVER_NAVI_MAX_NUM)],
					"stop_button" : GetObject("observer_stop_button"),
					"subpage_%d" % self.OBSERVER_NAVI_GENERAL : {
						"wnd" : GetObject("observer_subpage_general"),
						"face" : GetObject("observer_general_face"),
						"pid" : GetObject("observer_general_pid"),
						"name" : GetObject("observer_general_name"),
						"level" : GetObject("observer_general_level"),
						"hpbar" : GetObject("observer_general_hpgauge"),
						"hptext" : GetObject("observer_general_hptext"),
						"spbar" : GetObject("observer_general_spgauge"),
						"sptext" : GetObject("observer_general_sptext"),
						"exp_point_bg" : GetObject("observer_general_exp_bg"),
						"exp_points" : [GetObject("observer_general_exp_%d" % (i + 1)) for i in xrange(4)],
						"empire" : GetObject("observer_general_empire"),
						"account" : GetObject("observer_general_account"),
						"channel" : GetObject("observer_general_channel"),
						"map_info" : GetObject("observer_general_map_info"),
						"gold" : GetObject("observer_general_gold"),
						"skillgroup" : GetObject("observer_general_skillgroup"),
						"skill_wnd" : GetObject("observer_general_skill_bg"),
						"skill" : GetObject("observer_general_skill_slot"),
					},
					"subpage_%d" % self.OBSERVER_NAVI_ITEM : {
						"wnd" : GetObject("observer_subpage_item"),
						"equipment" : GetObject("observer_item_equipment_slot"),
						"inventory" : GetObject("observer_item_inventory_slot"),
						"inventory_page_1" : GetObject("observer_item_inventory_tab_01"),
						"inventory_page_2" : GetObject("observer_item_inventory_tab_02"),
						"inventory_page_3" : GetObject("observer_item_inventory_tab_03"),
						"inventory_page_4" : GetObject("observer_item_inventory_tab_04"),
						"inventory_page_5" : GetObject("observer_item_inventory_tab_05"),
						"money" : GetObject("observer_item_money_text"),
					},
					"subpage_%d" % self.OBSERVER_NAVI_BAN : {
						"wnd" : GetObject("observer_subpage_ban"),
						"chat_state" : GetObject("observer_chatban_state"),
						"chat_day" : GetObject("observer_chatban_day"),
						"chat_hour" : GetObject("observer_chatban_hour"),
						"chat_minute" : GetObject("observer_chatban_minute"),
						"chat_activate" : GetObject("observer_chatban_activate"),
						"chat_deactivate" : GetObject("observer_chatban_deactivate"),
						"account_state" : GetObject("observer_accountban_state"),
						"account_day" : GetObject("observer_accountban_day"),
						"account_hour" : GetObject("observer_accountban_hour"),
						"account_minute" : GetObject("observer_accountban_minute"),
						"account_activate" : GetObject("observer_accountban_activate"),
					},
				},
				# page ban
				self.PAGE_BAN : {
					"wnd" : GetObject("page_ban"),
					"chat_wnd" : GetObject("ban_chat"),
					"chat_search_wnd" : GetObject("ban_chat_search"),
					"chat_search_edit" : GetObject("ban_chat_search_edit"),
					"chat_search_btn" : GetObject("ban_chat_search_button"),
					"chat_state_%d" % self.BAN_CHAT_STATE_NONE : {
						"wnd" : GetObject("ban_chat_normal_wnd"),
						"chat_list" : GetObject("ban_chat_list"),
						"chat_scroll" : GetObject("ban_chat_scrollbar"),
						"chat_unban_btn" : GetObject("ban_chat_unban_button"),
					},
					"chat_state_%d" % self.BAN_CHAT_STATE_SEARCHING : {
						"wnd" : GetObject("ban_chat_search_result_fail_wnd"),
					},
					"chat_state_%d" % self.BAN_CHAT_STATE_SEARCH_FAIL : {
						"wnd" : GetObject("ban_chat_search_result_fail_wnd"),
						"btn_back" : GetObject("ban_chat_search_fail_button"),
					},
					"chat_state_%d" % self.BAN_CHAT_STATE_SEARCH_RESULT : {
						"wnd" : GetObject("ban_chat_search_result_success_wnd"),
						"pid" : GetObject("ban_chat_result_pid"),
						"name" : GetObject("ban_chat_result_name"),
						"face" : GetObject("ban_chat_result_face"),
						"chatban" : GetObject("ban_chat_result_chatban"),
						"accountban" : GetObject("ban_chat_result_accountban"),
						"ban_state" : GetObject("ban_chat_result_ban_state"),
						"time_wnd" : GetObject("ban_chat_result_time_wnd"),
						"box_day" : GetObject("ban_chat_result_day"),
						"box_hour" : GetObject("ban_chat_result_hour"),
						"box_min" : GetObject("ban_chat_result_minute"),
						"desc_min" : GetObject("ban_chat_result_minute_desc"),
						"online_state" : GetObject("ban_chat_result_online_state"),
						"btn_ban" : GetObject("ban_chat_result_ban_button"),
						"btn_unban" : GetObject("ban_chat_result_unban_button"),
						"btn_back" : GetObject("ban_chat_result_back_button"),
					},
					"account_wnd" : GetObject("ban_account"),
					"account_search_wnd" : GetObject("ban_account_search"),
					"account_search_edit" : GetObject("ban_account_search_edit"),
					"account_search_type_btn" : GetObject("ban_account_search_type_button"),
					"account_search_btn" : GetObject("ban_account_search_button"),
					"account_state_%d" % self.BAN_ACCOUNT_STATE_NONE : {
						"wnd" : GetObject("ban_account_normal_wnd"),
						"account_list" : GetObject("ban_account_list"),
						"account_scroll" : GetObject("ban_account_scrollbar"),
						"account_unban_btn" : GetObject("ban_account_unban_button"),
					},
					"account_state_%d" % self.BAN_ACCOUNT_STATE_SEARCHING : {
						"wnd" : GetObject("ban_account_search_result_fail_wnd"),
					},
					"account_state_%d" % self.BAN_ACCOUNT_STATE_SEARCH_FAIL : {
						"wnd" : GetObject("ban_account_search_result_fail_wnd"),
						"text_%d" % admin.BAN_ACCOUNT_SEARCH_ACCOUNT : GetObject("ban_account_search_fail_account"),
						"text_%d" % admin.BAN_ACCOUNT_SEARCH_PLAYER : GetObject("ban_account_search_fail_player"),
						"btn_back" : GetObject("ban_account_search_fail_button"),
					},
					"account_state_%d" % self.BAN_ACCOUNT_STATE_SEARCH_RESULT : {
						"wnd" : GetObject("ban_account_search_result_success_wnd"),
						"btn_select" : [GetObject("ban_account_result_select%d_btn" % (i + 1)) for i in xrange(net.PLAYER_PER_ACCOUNT5)],
						"account" : GetObject("ban_account_result_account"),
						"player" : GetObject("ban_account_result_player"),
						"face" : GetObject("ban_account_result_face"),
						"chatban" : GetObject("ban_account_result_chatban"),
						"accountban" : GetObject("ban_account_result_accountban"),
						"ban_state" : GetObject("ban_account_result_ban_state"),
						"time_wnd" : GetObject("ban_account_result_time_wnd"),
						"box_day" : GetObject("ban_account_result_day"),
						"box_hour" : GetObject("ban_account_result_hour"),
						"box_min" : GetObject("ban_account_result_minute"),
						"desc_min" : GetObject("ban_account_result_minute_desc"),
						"online_state" : GetObject("ban_account_result_online_state"),
						"btn_ban" : GetObject("ban_account_result_ban_button"),
						"btn_unban" : GetObject("ban_account_result_unban_button"),
						"btn_back" : GetObject("ban_account_result_back_button"),
					},
					"line" : GetObject("ban_line"),
					"log_wnd" : GetObject("ban_log"),
					"log_title" : GetObject("ban_log_title"),
					"log_nodata" : GetObject("ban_log_nodata"),
					"log_data" : GetObject("ban_log_data"),
					"log_scroll" : GetObject("ban_log_data_scroll"),
					"log_button" : GetObject("ban_log_button"),
				},
				# page item
				self.PAGE_ITEM : {
					"wnd" : GetObject("page_item"),
					"main_wnd" : GetObject("item_main"),
					"main_search_wnd" : GetObject("item_main_search"),
					"main_search_edit" : GetObject("item_main_search_edit"),
					"main_search_type_btn" : GetObject("item_main_search_type_button"),
					"main_search_btn" : GetObject("item_main_search_button"),
					"main_table" : GetObject("item_main_table"),
					"main_scroll" : GetObject("item_main_scroll"),
				},


				self.PAGE_LOGS : {
					"wnd" : GetObject("page_logs"),
					"main_wnd" : GetObject("hack_log_main"),
					"main_table" : GetObject("hack_log_main_table"),
					"main_scroll" : GetObject("hack_log_main_scroll"),
				},
			}

			self.naviBtnList = [GetObject("navi_button_%d" % (i + 1)) for i in xrange(self.PAGE_MAX_NUM)]

		except:
			import exception
			exception.Abort("AdminManagerWindow.LoadDialog.BindObject")

		self.board.SetCloseEvent(ui.__mem_func__(self.Close))

		# PAGE_GENERAL
		self.GENERAL_BuildPage()
		page = self.pages[self.PAGE_GENERAL]
		page["online_list"].SetHeaderClickEvent(ui.__mem_func__(self.GENERAL_OnListHeaderClick))
		page["online_list"].SetDoubleClickEvent(ui.__mem_func__(self.GENERAL_OnListDoubleClick))
		page["online_scroll"].SetScrollEvent(ui.__mem_func__(self.GENERAL_OnOnlineScroll))
		page["online_search_edit"].SetEscapeEvent(ui.__mem_func__(self.OnPressEscapeKey))
		page["online_search_edit"].SetReturnEvent(ui.__mem_func__(self.GENERAL_OnlineSearchPlayer))
		page["online_search_btn"].SAFE_SetEvent(self.GENERAL_OnlineSearchPlayer)
		page["gm_item_trade"].SAFE_SetEvent(self.GENERAL_OnClickGMItemTradeOption)

		# PAGE_MAPVIEWER
		self.MAPVIEWER_Build()
		page = self.pages[self.PAGE_MAPVIEWER]
		page["atlas"].SetMouseLeftButtonDownEvent(ui.__mem_func__(self.MAPVIEWER_OnClickAtlas))
		page["select_scroll"].SetScrollEvent(ui.__mem_func__(self.MAPVIEWER_OnSelectScroll))
		page["select_btn"].SAFE_SetEvent(self.MAPVIEWER_SelectMap)
		page["option_%d" % miniMap.ADMIN_SHOW_PC].SAFE_SetEvent(self.MAPVIEWER_OnClickOptionButton, miniMap.ADMIN_SHOW_PC)
		page["option_%d" % miniMap.ADMIN_SHOW_MOB].SAFE_SetEvent(self.MAPVIEWER_OnClickOptionButton, miniMap.ADMIN_SHOW_MOB)
		page["option_%d" % miniMap.ADMIN_SHOW_STONE].SAFE_SetEvent(self.MAPVIEWER_OnClickOptionButton, miniMap.ADMIN_SHOW_STONE)
		page["option_%d" % miniMap.ADMIN_SHOW_NPC].SAFE_SetEvent(self.MAPVIEWER_OnClickOptionButton, miniMap.ADMIN_SHOW_NPC)
		page["stop_btn"].SAFE_SetEvent(self.MAPVIEWER_Stop)

		# PAGE_OBSERVER
		self.OBSERVER_Build()
		page = self.pages[self.PAGE_OBSERVER]
		page["stopped_edit"].SetEscapeEvent(ui.__mem_func__(self.OnPressEscapeKey))
		page["stopped_edit"].SetReturnEvent(ui.__mem_func__(self.OBSERVER_StartObservation))
		page["stopped_btn"].SAFE_SetEvent(self.OBSERVER_StartObservation)
		for i in xrange(self.OBSERVER_NAVI_MAX_NUM):
			btn = page["navi_buttons"][i]
			btn.SAFE_SetEvent(self.OBSERVER_OnClickNaviButton, i)
		page["stop_button"].SAFE_SetEvent(self.OBSERVER_StopObservation)
		# SUB_PAGE_ITEM
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]
		subPage["equipment"].SetOverInItemEvent(ui.__mem_func__(self.OBSERVER_OnOverInItemSlot))
		subPage["equipment"].SetOverOutItemEvent(ui.__mem_func__(self.OBSERVER_OnOverOutItemSlot))
		subPage["equipment"].SetUseSlotEvent(ui.__mem_func__(self.OBSERVER_OnDoubleClickItemSlot))
		subPage["inventory"].SetOverInItemEvent(ui.__mem_func__(self.OBSERVER_OnOverInItemSlot))
		subPage["inventory"].SetOverOutItemEvent(ui.__mem_func__(self.OBSERVER_OnOverOutItemSlot))
		subPage["inventory"].SetUseSlotEvent(ui.__mem_func__(self.OBSERVER_OnDoubleClickItemSlot))
		for i in xrange(player.INVENTORY_PAGE_COUNT):
			subPage["inventory_page_%d" % (i + 1)].SAFE_SetEvent(self.OBSERVER_OnClickInventoryPageButton, i)
		# SUB_PAGE_BAN
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_BAN]
		subPage["chat_activate"].SAFE_SetEvent(self.OBSERVER_OnClickChatBanActivate)
		subPage["chat_deactivate"].SAFE_SetEvent(self.OBSERVER_OnClickChatBanDeactivate)
		subPage["account_activate"].SAFE_SetEvent(self.OBSERVER_OnClickAccountBanActivate)

		# PAGE_BAN
		self.BAN_Build()
		page = self.pages[self.PAGE_BAN]
		# CHAT_BEGIN #
		page["chat_search_edit"].SetEscapeEvent(ui.__mem_func__(self.OnPressEscapeKey))
		page["chat_search_edit"].SetReturnEvent(ui.__mem_func__(self.BAN_OnClickChatSearch))
		page["chat_search_btn"].SAFE_SetEvent(self.BAN_OnClickChatSearch)
		# STATE_NONE
		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_NONE]
		subPage["chat_list"].SetDoubleClickEvent(ui.__mem_func__(self.BAN_OnClickChatList))
		subPage["chat_scroll"].SetScrollEvent(ui.__mem_func__(self.BAN_OnChatScroll))
		subPage["chat_unban_btn"].SAFE_SetEvent(self.BAN_OnClickChatUnban)
		# STATE_SEARCH_FAIL
		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_SEARCH_FAIL]
		subPage["btn_back"].SAFE_SetEvent(self.BAN_OnClickChatBack)
		# STATE_SEARCH_RESULT
		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_SEARCH_RESULT]
		subPage["face"].SAFE_SetEvent(self.BAN_OnClickChatLogShowButton)
		subPage["btn_ban"].SAFE_SetEvent(self.BAN_OnClickChatResultBan)
		subPage["btn_unban"].SAFE_SetEvent(self.BAN_OnClickChatResultUnban)
		subPage["btn_back"].SAFE_SetEvent(self.BAN_OnClickChatBack)
		# CHAT_END #
		# ACCOUNT_BEGIN #
		page["account_search_edit"].SetEscapeEvent(ui.__mem_func__(self.OnPressEscapeKey))
		page["account_search_edit"].SetReturnEvent(ui.__mem_func__(self.BAN_OnClickAccountSearch))
		page["account_search_type_btn"].SAFE_SetEvent(self.BAN_OnClickAccountSearchType)
		page["account_search_btn"].SAFE_SetEvent(self.BAN_OnClickAccountSearch)
		# STATE_NONE
		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_NONE]
		subPage["account_list"].SetDoubleClickEvent(ui.__mem_func__(self.BAN_OnClickAccountList))
		subPage["account_scroll"].SetScrollEvent(ui.__mem_func__(self.BAN_OnAccountScroll))
		subPage["account_unban_btn"].SAFE_SetEvent(self.BAN_OnClickAccountUnban)
		# STATE_SEARCH_FAIL
		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_SEARCH_FAIL]
		subPage["btn_back"].SAFE_SetEvent(self.BAN_OnClickAccountBack)
		# STATE_SEARCH_RESULT
		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_SEARCH_RESULT]
		for i in xrange(net.PLAYER_PER_ACCOUNT5):
			subPage["btn_select"][i].SAFE_SetEvent(self.BAN_OnClickAccountSelectPlayer, i + 1)
		subPage["face"].SAFE_SetEvent(self.BAN_OnClickAccountLogShowButton)
		subPage["btn_ban"].SAFE_SetEvent(self.BAN_OnClickAccountResultBan)
		subPage["btn_unban"].SAFE_SetEvent(self.BAN_OnClickAccountResultUnban)
		subPage["btn_back"].SAFE_SetEvent(self.BAN_OnClickAccountBack)
		# ACCOUNT_END #
		page["log_data"].SetDoubleClickEvent(ui.__mem_func__(self.BAN_OnClickLogTable))
		page["log_scroll"].SetScrollEvent(ui.__mem_func__(self.BAN_OnLogScroll))
		page["log_button"].SAFE_SetEvent(self.BAN_OnClickLogHideButton)

		# PAGE_ITEM
		self.ITEM_Build()
		page = self.pages[self.PAGE_ITEM]
		page["main_search_edit"].SetEscapeEvent(ui.__mem_func__(self.OnPressEscapeKey))
		page["main_search_edit"].SetReturnEvent(ui.__mem_func__(self.ITEM_OnClickMainSearch))
		page["main_search_type_btn"].SAFE_SetEvent(self.ITEM_OnClickMainSearchType)
		page["main_search_btn"].SAFE_SetEvent(self.ITEM_OnClickMainSearch)
		page["main_scroll"].SetScrollEvent(ui.__mem_func__(self.ITEM_OnMainScroll))

		# LOGS_START
		self.LOGS_Build()
		page = self.pages[self.PAGE_LOGS]
		page["main_scroll"].SetScrollEvent(ui.__mem_func__(self.LOGS_OnMainScroll))
		page["main_table"].SetDoubleClickEvent(ui.__mem_func__(self.LOGS_OnListDoubleClick))

		# Navi
		for i in xrange(self.PAGE_MAX_NUM):
			btn = self.naviBtnList[i]
			btn.SAFE_SetEvent(self.OnClickNaviButton, i)
		self.OnClickNaviButton(self.PAGE_GENERAL)

		# refresh rect
		self.UpdateRect()

	def Destroy(self):
		self.Close()

	def Open(self):
		self.OnOpenPage()
		self.Show()
		self.SetTop()

	def Close(self):
		self.OnClosePage()
		self.Hide()

	def OnUpdate(self):
		self.MAPVIEWER_OnUpdate()
		self.OBSERVER_OnUpdate()
		self.BAN_OnUpdate()

	def OnAfterRender(self):
		if self.currentPageIndex == self.PAGE_GENERAL:
			self.GENERAL_OnAfterRender()
		elif self.currentPageIndex == self.PAGE_OBSERVER:
			self.OBSERVER_OnAfterRender()

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def Initialize(self):
		self.InitializePages()

		self.GENERAL_Initialize()
		self.OBSERVER_Initialize()
		self.BAN_Initialize()

	def DrawNotVisible(self, sx, sy, ex, ey):
		grp.SetColor(ui.BRIGHT_COLOR)
		grp.RenderLine(sx, sy, ex - sx, ey - sy)
		grp.RenderLine(sx, ey, ex - sx, sy - ey)

	#################################################
	## PAGE FUNCTIONS
	#################################################

	def InitializePages(self):
		# GENERAL
		if not admin.HasAllow(admin.ALLOW_VIEW_ONLINE_LIST) and not admin.HasAllow(admin.ALLOW_VIEW_ONLINE_COUNT):
			self.DisablePage(self.PAGE_GENERAL)
		if not admin.HasAllow(admin.ALLOW_MAPVIEWER):
			self.DisablePage(self.PAGE_MAPVIEWER)
		if not admin.HasAllow(admin.ALLOW_OBSERVER):
			self.DisablePage(self.PAGE_OBSERVER)
		if not admin.HasAllow(admin.ALLOW_BAN):
			self.DisablePage(self.PAGE_BAN)

	def DisablePage(self, pageIndex):
		self.naviBtnList[pageIndex].Hide()

		btnList = []
		for i in xrange(self.PAGE_MAX_NUM):
			btn = self.naviBtnList[i]
			if btn.IsShow():
				btnList.append(btn)

		for i in xrange(len(btnList)):
			btnList[i].SetPosition(self.GetWidth() / (len(btnList) + 1) * (i + 1) - btnList[i].GetWidth() / 2, btnList[i].GetTop())

		if len(btnList) == 0:
			self.Close()
			return

		if self.currentPageIndex == pageIndex:
			btnList[0].CallEvent()

	def LoadPage(self, pageIndex):
		if self.currentPageIndex == pageIndex:
			return

		self.OnClosePage()

		self.currentPageIndex = pageIndex

		# refresh if needed
		if self.pageNeedRefresh[pageIndex] == True:
			if pageIndex == self.PAGE_GENERAL:
				self.GENERAL_RefreshPage()
			elif pageIndex == self.PAGE_MAPVIEWER:
				self.MAPVIEWER_RefreshPage()
			elif pageIndex == self.PAGE_OBSERVER:
				self.OBSERVER_RefreshPage()
			elif pageIndex == self.PAGE_LOGS:
				self.LOGS_Build()
		self.OnOpenPage()

		# show selected pages
		for i in xrange(self.PAGE_MAX_NUM):
			page = self.pages[i]["wnd"]
			if i == pageIndex:
				page.Show()
			else:
				page.Hide()

	def OnClosePage(self):
		if self.currentPageIndex == self.PAGE_GENERAL:
			self.GENERAL_OnClosePage()
		elif self.currentPageIndex == self.PAGE_MAPVIEWER:
			self.MAPVIEWER_OnClosePage()
		elif self.currentPageIndex == self.PAGE_OBSERVER:
			self.OBSERVER_OnClosePage()
		elif self.currentPageIndex == self.PAGE_BAN:
			self.BAN_OnClosePage()
		elif self.currentPageIndex == self.PAGE_ITEM:
			self.ITEM_OnClosePage()

		elif self.currentPageIndex == self.PAGE_LOGS:
			self.LOGS_OnClosePage()

	def OnOpenPage(self):
		if self.currentPageIndex == self.PAGE_MAPVIEWER:
			self.MAPVIEWER_OnOpenPage()
		elif self.currentPageIndex == self.PAGE_OBSERVER:
			self.OBSERVER_OnOpenPage()
		elif self.currentPageIndex == self.PAGE_BAN:
			self.BAN_ChatRefreshList()
			self.BAN_AccountRefreshList()

	#################################################
	## PAGE: GENERAL FUNCTIONS
	#################################################

	def GENERAL_BuildPage(self):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		pageData["question_wnd"] = uiCommon.QuestionDialogAdmin()
		pageData["question_wnd"].SetAccept2Text(localeInfo.ADMIN_MANAGER_GENERAL_QUESTION_ACCEPT_WARP)
		pageData["question_wnd"].SAFE_SetCancelEvent(pageData["question_wnd"].Close)
		pageData["question_wnd"].Close()

	def GENERAL_Initialize(self):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		if not admin.HasAllow(admin.ALLOW_VIEW_ONLINE_LIST):
			page["online_list"].Hide()
			page["online_search"].Hide()
		if not admin.HasAllow(admin.ALLOW_VIEW_ONLINE_COUNT):
			page["user_count"].Hide()
		if not admin.HasAllow(admin.ALLOW_GM_TRADE_BLOCK_OPTION):
			page["gm_item_trade"].Hide()

	def GENERAL_RefreshPage(self):
		self.GENERAL_RefreshOnlineList()
		self.GENERAL_RefreshOnlineScrollBar()
		self.GENERAL_RefreshUserCount()
		self.GENERAL_RefreshGMItemTradeOption()

		self.pageNeedRefresh[self.PAGE_GENERAL] = False

	def GENERAL_OnClosePage(self):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		page["online_search_edit"].KillFocus()
		pageData["question_wnd"].Close()

	def GENERAL_RefreshOnlineList(self):
		page = self.pages[self.PAGE_GENERAL]

		basePos = page["online_list"].GetBasePos()
		page["online_list"].Clear()

		for i in xrange(admin.GetOnlinePlayerCount()):
			if admin.IsOnlinePlayerSorted():
				(pid, name, map_index, channel, empire) = admin.GetSortOnlinePlayerByIndex(i)
			else:
				(pid, name, map_index, channel, empire) = admin.GetOnlinePlayerByIndex(i)
			page["online_list"].Append(pid, [pid, name, map_index, channel, empire], False)
		page["online_list"].SetBasePos(basePos)

	def GENERAL_RefreshOnlineScrollBar(self):
		page = self.pages[self.PAGE_GENERAL]

		if page["online_list"].GetMaxLineCount() > page["online_list"].GetViewLineCount():
			page["online_scroll"].Hide()
			page["dividing_line"].Show()
		else:
			page["online_scroll"].SetMiddleBarSize(float(page["online_list"].GetMaxLineCount()) / float(page["online_list"].GetLineCount()))
			page["online_scroll"].Show()
			page["dividing_line"].Hide()

	def GENERAL_RefreshUserCount(self):
		page = self.pages[self.PAGE_GENERAL]

		page["user_count"].SetText(localeInfo.ADMIN_MANAGER_GENERAL_USER_COUNT % localeInfo.NumberToString(admin.GetOnlinePlayerCount()))

	def GENERAL_AddOnlinePlayer(self, pid):
		page = self.pages[self.PAGE_GENERAL]

		if admin.IsOnlinePlayerSorted():
			self.GENERAL_RefreshPage()

		else:
			(pid, name, map_index, channel, empire) = admin.GetOnlinePlayerByPID(pid)
			page["online_list"].Append(pid, [pid, name, map_index, channel, empire])

			self.GENERAL_RefreshUserCount()

	def GENERAL_EraseOnlinePlayer(self, pid):
		page = self.pages[self.PAGE_GENERAL]

		page["online_list"].Erase(pid)

		self.GENERAL_RefreshUserCount()

	def GENERAL_OnOnlineScroll(self):
		page = self.pages[self.PAGE_GENERAL]

		pos = page["online_scroll"].GetPos()
		basePos = int(float(page["online_list"].GetLineCount() - page["online_list"].GetViewLineCount()) * pos)
		if basePos != page["online_list"].GetBasePos():
			page["online_list"].SetBasePos(basePos)

	def GENERAL_OnlineSearchPlayer(self):
		page = self.pages[self.PAGE_GENERAL]

		playerName = page["online_search_edit"].GetText()
		if playerName == "":
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_UPDATE_2020_YO_DO_NOT_ENTER_A_NAME)
			return

	def GENERAL_OnClickGMItemTradeOption(self):
		page = self.pages[self.PAGE_GENERAL]

		if page["gm_item_trade"].IsChecked():
			net.SendChatPacket("/eventflag gm_item_trade_block 1 n")
		else:
			net.SendChatPacket("/eventflag gm_item_trade_block 0 n")

	def GENERAL_RefreshGMItemTradeOption(self):
		page = self.pages[self.PAGE_GENERAL]

		if admin.IsGMItemTradeBlock():
			page["gm_item_trade"].SetChecked(ui.CheckBox_admin.STATE_SELECTED)
		else:
			page["gm_item_trade"].SetChecked(ui.CheckBox_admin.STATE_UNSELECTED)

	def GENERAL_OnListHeaderClick(self, colIndex):
		sortDir = 0
		if admin.GetOnlinePlayerSortType() == colIndex and admin.GetOnlinePlayerSortDir() == 0:
			sortDir = 1
		admin.SortOnlinePlayer(colIndex, sortDir)

		self.GENERAL_RefreshOnlineList()

	def GENERAL_OnListDoubleClick(self, pid):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		if pid == 0:
			return

		if admin.IsObserverRunning() and admin.GetObserverPID() == pid:
			self.OnClickNaviButton(self.PAGE_OBSERVER)
			return

		(pid, name, map_index, channel, empire) = admin.GetOnlinePlayerByPID(pid)
		if name == player.GetName():
			return

		pageData["question_wnd"].SetText(localeInfo.ADMIN_MANAGER_GENERAL_QUESTION_TEXT % name)
		pageData["question_wnd"].SAFE_SetAccept1Event(self.GENERAL_OnQuestionDlgAccept1, name)
		pageData["question_wnd"].SAFE_SetAccept2Event(self.GENERAL_OnQuestionDlgAccept2, name)
		pageData["question_wnd"].Open()

	def GENERAL_OnQuestionDlgAccept1(self, name):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		pageData["question_wnd"].Close()
		self.OBSERVER_StartObservation(name)

	def GENERAL_OnQuestionDlgAccept2(self, name):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		pageData["question_wnd"].Close()
		net.SendChatPacket("/warp \"" + str(name) + "\" INVISIBLE")

	def GENERAL_OnAfterRender(self):
		page = self.pages[self.PAGE_GENERAL]
		pageData = self.pageData[self.PAGE_GENERAL]

		if not admin.HasAllow(admin.ALLOW_VIEW_ONLINE_LIST):
			x, y = page["online_list"].GetGlobalPosition()
			x += 10
			x_end = x + page["online_list"].GetWidth()
			y_end = page["online_search"].GetY() + page["online_search"].GetHeight()

			self.DrawNotVisible(x, y, x_end, y_end)

		if not admin.HasAllow(admin.ALLOW_VIEW_ONLINE_COUNT):
			x = page["main_info"].GetX() + 10
			y = page["user_count"].GetY()
			x_end = x + page["main_info"].GetWidth() - 10 * 2
			y_end = y + ui.DEFAULT_TEXT_HEIGHT

			self.DrawNotVisible(x, y, x_end, y_end)

	#################################################
	## PAGE: MAPVIEWER FUNCTIONS
	#################################################

	def MAPVIEWER_Build(self):
		page = self.pages[self.PAGE_MAPVIEWER]

		wndAtlas = self.MapViewer_AtlasRenderer()
		wndAtlas.SetParent(page["atlas"])
		wndAtlas.SetPosition(0, 0)
		wndAtlas.SetSize(page["atlas"].GetWidth(), page["atlas"].GetHeight())
		wndAtlas.HideAtlas()
		wndAtlas.Show()
		page["atlas_wnd"] = wndAtlas

		wndAtlasToolTip = uiMiniMap.MapTextToolTip()
		wndAtlasToolTip.SetParent(wndAtlas)
		wndAtlasToolTip.Hide()
		page["atlas_tooltip"] = wndAtlasToolTip
		wndAtlasStoneToolTip = uiToolTip.ToolTip()
		wndAtlasStoneToolTip.Hide()
		page["atlas_stone_tooltip"] = wndAtlasStoneToolTip

		page["question_wnd"] = uiCommon.QuestionDialog()
		page["question_wnd"].SAFE_SetCancelEvent(page["question_wnd"].Close)
		page["question_wnd"].Close()

	def MAPVIEWER_OnClosePage(self):
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		if self.MAPVIEWER_IsRunning():
			pageData["stop_timer"] = app.GetTime() + 30

	def MAPVIEWER_OnOpenPage(self):
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		if self.MAPVIEWER_IsRunning():
			if pageData.has_key("is_paused") and pageData["is_paused"] == True:
				pageData["is_paused"] = False
				admin.StartMapViewer(pageData["map_x"], pageData["map_y"])
			elif pageData.has_key("stop_timer") and pageData["stop_timer"] != 0:
				pageData["stop_timer"] = 0

	def MAPVIEWER_RefreshPage(self):
		self.MAPVIEWER_RefreshAtlasWindow()
		self.MAPVIEWER_RefreshMapSelection()
		self.MAPVIEWER_RefreshOptionButton(miniMap.ADMIN_SHOW_PC)
		self.MAPVIEWER_RefreshOptionButton(miniMap.ADMIN_SHOW_MOB)
		self.MAPVIEWER_RefreshOptionButton(miniMap.ADMIN_SHOW_STONE)
		self.MAPVIEWER_RefreshOptionButton(miniMap.ADMIN_SHOW_NPC)
		self.MAPVIEWER_RefreshStopButton()

		self.pageNeedRefresh[self.PAGE_MAPVIEWER] = False

	def MAPVIEWER_RefreshAtlasWindow(self):
		page = self.pages[self.PAGE_MAPVIEWER]
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		if self.MAPVIEWER_IsRunning():
			page["atlas_wnd"].ShowAtlas()
			page["no_select_wnd"].Hide()
		else:
			page["atlas_wnd"].HideAtlas()
			page["no_select_wnd"].Show()

	def MAPVIEWER_RefreshMapSelection(self):
		page = self.pages[self.PAGE_MAPVIEWER]

		oldSelection = page["select_list"].GetSelectedLine()
		oldScrollPos = page["select_scroll"].GetPos()

		page["select_list"].ClearItem()

		if self.MAPVIEWER_IsRunning():
			page["select_list"].SetSize(page["select_list"].GetWidth(), page["select_list"].GetStepSize() * 5)
			page["select_btn"].SetPosition(page["select_btn"].GetLeft(), page["select_list"].GetBottom() + 5)
			page["select_line"].Show()
		else:
			page["select_list"].SetSize(page["select_list"].GetWidth(), page["select_list"].GetStepSize() * 14)
			page["select_btn"].SetPosition(page["select_btn"].GetLeft(), page["stop_btn"].GetTop())
			page["select_line"].Hide()
		page["select_line"].SetPosition(page["select_line"].GetLeft(), page["select_btn"].GetBottom() + 6)
		page["select_scroll"].SetScrollBarSize(page["select_btn"].GetBottom() - page["select_scroll"].GetTop())

		for i in xrange(background.GetMapInfoCount()):
			if not self.MAPVIEWER_IsAvailableMap(i):
				continue

			name, x, y = background.GetMapInfoByIndex(i)
			page["select_list"].InsertItem(i, name.replace("_", " "))

		if oldSelection != -1:
			page["select_list"].SelectItem(oldSelection)

		self.MAPVIEWER_RefreshMapScrollBar(oldScrollPos)

	def MAPVIEWER_RefreshMapScrollBar(self, scrollPos):
		page = self.pages[self.PAGE_MAPVIEWER]

		if page["select_list"].GetItemCount() <= page["select_list"].GetViewItemCount():
			page["select_scroll"].Hide()
		else:
			page["select_scroll"].SetMiddleBarSize(float(page["select_list"].GetViewItemCount()) / float(page["select_list"].GetItemCount()))
			page["select_scroll"].SetPos(scrollPos)
			page["select_scroll"].Show()

	def MAPVIEWER_RefreshOptionButton(self, flag):
		page = self.pages[self.PAGE_MAPVIEWER]

		if self.MAPVIEWER_IsRunning():
			self.MAPVIEWER_RefreshOptionButtonState(flag)
			page["option_%d" % flag].Show()
		else:
			page["option_%d" % flag].Hide()

	def MAPVIEWER_RefreshOptionButtonState(self, flag):
		page = self.pages[self.PAGE_MAPVIEWER]

		if miniMap.IsAdminManagerAtlasFlagShown(flag):
			page["option_%d" % flag].SetChecked(ui.CheckBox_admin.STATE_SELECTED)
		else:
			page["option_%d" % flag].SetChecked(ui.CheckBox_admin.STATE_UNSELECTED)

	def MAPVIEWER_RefreshStopButton(self):
		page = self.pages[self.PAGE_MAPVIEWER]

		if self.MAPVIEWER_IsRunning():
			page["stop_btn"].Show()
		else:
			page["stop_btn"].Hide()

	def MAPVIEWER_IsRunning(self):
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		return pageData.has_key("map_name") and pageData["map_name"] != ""

	def MAPVIEWER_OnUpdate(self):
		page = self.pages[self.PAGE_MAPVIEWER]
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		if self.IsShow() and self.currentPageIndex == self.PAGE_MAPVIEWER:
			page["atlas_tooltip"].Hide()
			page["atlas_stone_tooltip"].Hide()

			if not miniMap.isShowAdminManagerAtlas():
				return

			(mouseX, mouseY) = wndMgr.GetMousePosition()
			(bFind, sName, fPosX, fPosY, dwTextColor, dwStoneDropVnum) = miniMap.GetAdminManagerAtlasInfo(mouseX, mouseY)

			if False == bFind:
				return

			if dwStoneDropVnum != 0:
				page["atlas_stone_tooltip"].ClearToolTip()
				page["atlas_stone_tooltip"].AppendTextLine("%s (%d, %d)" % (sName, int(fPosX), int(fPosY)), dwTextColor)

				item.SelectItem(dwStoneDropVnum)
				page["atlas_stone_tooltip"].AppendSpace(5)
				page["atlas_stone_tooltip"].AppendTextLine(item.GetItemName())
				page["atlas_stone_tooltip"].AppendImage(item.GetIconImageFileName())

				page["atlas_stone_tooltip"].ShowToolTip()

			else:
				page["atlas_tooltip"].SetTextColor(dwTextColor)
				page["atlas_tooltip"].SetText("%s (%d, %d)" % (sName, int(fPosX), int(fPosY)))

				(x, y) = page["atlas"].GetGlobalPosition()
				page["atlas_tooltip"].SetTooltipPosition(mouseX - x, mouseY - y)

				page["atlas_tooltip"].Show()
				page["atlas_tooltip"].SetTop()

		else:
			if pageData.has_key("stop_timer") and pageData["stop_timer"] != 0 and app.GetTime() >= pageData["stop_timer"]:
				pageData["stop_timer"] = 0
				pageData["is_paused"] = True
				admin.StopMapViewer()

	def MAPVIEWER_IsAvailableMap(self, index):
		nonAvailList = ["metin2_map_wedding", "metin2_map_deviltower", "metin2_map_skipia_dungeon_boss", "metin2_map_guildwar", "metin2_map_guildflagwar", "metin2_map_oxevent"]

		path = background.GetMapPathByIndex(index)
		splitPath = path.split("/")
		folderName = splitPath[len(splitPath) - 1]

		if folderName in nonAvailList:
			return False

		return True

	def MAPVIEWER_OnClickAtlas(self):
		page = self.pages[self.PAGE_MAPVIEWER]

		if not miniMap.isShowAdminManagerAtlas():
			return

		(mouseX, mouseY) = wndMgr.GetMousePosition()
		(bFind, sName, fPosX, fPosY, dwTextColor, dwStoneDropVnum) = miniMap.GetAdminManagerAtlasInfo(mouseX, mouseY)

		if False == bFind:
			(bFindPos, fPosX, fPosY) = miniMap.GetAdminManagerAtlasInfoNew(mouseX, mouseY)

			if bFindPos == False:
				return

		page["question_wnd"].SetText(localeInfo.ADMIN_MANAGER_MAPVIEWER_WARP_TEXT % (int(fPosX), int(fPosY)))
		page["question_wnd"].SAFE_SetAcceptEvent(self.MAPVIEWER_OnAcceptAtlasWarp, admin.GetMapViewerBaseX() / 100 + int(fPosX), admin.GetMapViewerBaseY() / 100 + int(fPosY))
		page["question_wnd"].Open()

	def MAPVIEWER_OnAcceptAtlasWarp(self, x, y):
		page = self.pages[self.PAGE_MAPVIEWER]

		page["question_wnd"].Close()
		net.SendChatPacket("/warp " + str(x) + " " + str(y))

	def MAPVIEWER_OnSelectScroll(self):
		page = self.pages[self.PAGE_MAPVIEWER]

		pos = page["select_scroll"].GetPos()
		basePos = int(float(page["select_list"].GetItemCount() - page["select_list"].GetViewItemCount()) * pos)
		if basePos != page["select_list"].GetBasePos():
			page["select_list"].SetBasePos(basePos)

	def MAPVIEWER_SelectMap(self):
		page = self.pages[self.PAGE_MAPVIEWER]
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		index = page["select_list"].GetSelectedItem(-1)
		if index == -1:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_UPDATE_2020_FIRST_CHOOSE_A_MAP)
			return

		name, x, y = background.GetMapInfoByIndex(index)
		pageData["map_name"] = name
		pageData["map_x"] = x
		pageData["map_y"] = y
		admin.StartMapViewer(x, y)

	def MAPVIEWER_Stop(self):
		page = self.pages[self.PAGE_MAPVIEWER]
		pageData = self.pageData[self.PAGE_MAPVIEWER]

		if not self.MAPVIEWER_IsRunning():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_UPDATE_2020_THE_MAP_VIEW_IS_NOT_RUNING)
			return

		pageData["map_name"] = ""
		self.MAPVIEWER_RefreshPage()
		admin.StopMapViewer()

	def MAPVIEWER_OnClickOptionButton(self, flag):
		if miniMap.IsAdminManagerAtlasFlagShown(flag):
			miniMap.HideAdminManagerAtlasFlag(flag)
		else:
			miniMap.ShowAdminManagerAtlasFlag(flag)
		self.MAPVIEWER_RefreshOptionButtonState(flag)

	def MAPVIEWER_OnStart(self):
		if not miniMap.canRenderAdminManagerAtlas():
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_UPDATE_2020_THERE_IS_NO_LARGE_MAP_AVL)
			self.MAPVIEWER_Stop()
		else:
			self.MAPVIEWER_RefreshPage()

	#################################################
	## PAGE: OBSERVER FUNCTIONS
	#################################################

	def OBSERVER_Build(self):
		page = self.pages[self.PAGE_OBSERVER]

		subPage = page["subpage_%d" % self.OBSERVER_NAVI_GENERAL]
		subPage["exp_tooltip"] = self.TextToolTip()
		subPage["exp_tooltip"].Hide()

		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]
		subPage["item_tooltip"] = uiToolTip.ItemToolTip()
		subPage["item_tooltip"].HideToolTip()

		dlgReasonInputBan = uiCommon.DoubleInputDialogWithDescription()
		dlgReasonInputBan.SetTitle(localeInfo.ADMIN_MANAGER_OBSERVER_REASON_INPUT_TITLE_BAN)
		dlgReasonInputBan.SetDescription(localeInfo.ADMIN_MANAGER_OBSERVER_REASON_INPUT_BAN1, 0)
		dlgReasonInputBan.SetDescription(localeInfo.ADMIN_MANAGER_OBSERVER_REASON_INPUT_BAN2, 1)
		dlgReasonInputBan.SetAcceptEvent(self.OBSERVER_OnClickReasonBanButton)
		dlgReasonInputBan.SetCancelEvent(dlgReasonInputBan.Hide)
		dlgReasonInputBan.SetMaxLength(50, 0)
		dlgReasonInputBan.SetMaxLength(200, 1)
		dlgReasonInputBan.SetDisplayWidth(dlgReasonInputBan.GetDisplayWidth(0), 1)
		page["reason_input_ban"] = dlgReasonInputBan
		dlgReasonInputUnban = uiCommon.DoubleInputDialogWithDescription()
		dlgReasonInputUnban.SetTitle(localeInfo.ADMIN_MANAGER_OBSERVER_REASON_INPUT_TITLE_UNBAN)
		dlgReasonInputUnban.SetDescription(localeInfo.ADMIN_MANAGER_OBSERVER_REASON_INPUT_UNBAN1, 0)
		dlgReasonInputUnban.SetDescription(localeInfo.ADMIN_MANAGER_OBSERVER_REASON_INPUT_UNBAN2, 1)
		dlgReasonInputUnban.SetAcceptEvent(self.OBSERVER_OnClickReasonUnbanButton)
		dlgReasonInputUnban.SetCancelEvent(dlgReasonInputUnban.Hide)
		dlgReasonInputUnban.SetMaxLength(50, 0)
		dlgReasonInputUnban.SetMaxLength(200, 1)
		dlgReasonInputUnban.SetDisplayWidth(dlgReasonInputUnban.GetDisplayWidth(0), 1)
		page["reason_input_unban"] = dlgReasonInputUnban

	def OBSERVER_Initialize(self):
		page = self.pages[self.PAGE_OBSERVER]

		if not admin.HasAllow(admin.ALLOW_VIEW_OBSERVER_GOLD):
			subPage = page["subpage_%d" % self.OBSERVER_NAVI_GENERAL]
			subPage["gold"].Hide()
			subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]
			subPage["money"].Hide()

	def OBSERVER_GetSubPageIndex(self):
		pageData = self.pageData[self.PAGE_OBSERVER]

		index = 0
		if admin.IsObserverRunning() or admin.IsObserverStopForced():
			if pageData.has_key("sub_page_index"):
				index = pageData["sub_page_index"]
		else:
			index = -1

		return index

	def OBSERVER_SetSubPageIndex(self, index):
		pageData = self.pageData[self.PAGE_OBSERVER]

		pageData["sub_page_index"] = index
		self.OBSERVER_Refresh()

	def OBSERVER_GetName(self):
		pageData = self.pageData[self.PAGE_OBSERVER]

		return pageData["observer_name"]

	def OBSERVER_OnStart(self):
		self.OBSERVER_OnClickNaviButton(self.OBSERVER_NAVI_GENERAL)
		self.OBSERVER_RefreshPage()
		self.OnClickNaviButton(self.PAGE_OBSERVER)

	def OBSERVER_RefreshPage(self):
		page = self.pages[self.PAGE_OBSERVER]

		self.OBSERVER_Refresh()

		if self.OBSERVER_GetSubPageIndex() != -1:
			self.OBSERVER_RefreshSubPage(self.OBSERVER_NAVI_GENERAL)
			self.OBSERVER_RefreshSubPage(self.OBSERVER_NAVI_ITEM)

		self.pageNeedRefresh[self.PAGE_OBSERVER] = False

	def OBSERVER_Refresh(self):
		page = self.pages[self.PAGE_OBSERVER]

		subPageIndex = self.OBSERVER_GetSubPageIndex()
		if subPageIndex == -1:
			page["running_wnd"].Hide()
			page["stopped_wnd"].Show()
		else:
			page["stopped_edit"].KillFocus()
			page["stopped_edit"].SetText("")
			page["stopped_wnd"].Hide()
			page["running_wnd"].Show()

			for i in xrange(self.OBSERVER_NAVI_MAX_NUM):
				wnd = page["subpage_%d" % i]["wnd"]
				if i == subPageIndex:
					wnd.Show()
				else:
					wnd.Hide()

	def OBSERVER_RefreshSubPage(self, subPageIndex):
		if subPageIndex == self.OBSERVER_NAVI_GENERAL:
			self.OBSERVER_RefreshSubPageGeneral()
		elif subPageIndex == self.OBSERVER_NAVI_ITEM:
			self.OBSERVER_RefreshSubPageItem()

	def OBSERVER_RefreshSubPageGeneral(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_GENERAL]

		pid = admin.GetObserverPID()
		try:
			(tmp_pid, name, map_index, channel, empire) = admin.GetOnlinePlayerByPID(pid)
		except:
			name = "[unknown]"
			map_index = 0
			channel = 0
			empire = 0

		pageData["observer_name"] = name

		faceImageName = self.FACE_IMAGE_DICT[admin.GetObserverRaceNum()] % ""

		subPage["face"].LoadImage(faceImageName)
		subPage["face"].Show()

		subPage["pid"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_PID % pid)
		subPage["name"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_NAME % name)
		if empire != 0:
			subPage["empire"].LoadImage(self.OBSERVER_EMPIRE_IMAGE_DICT[empire])
			subPage["empire"].Hide()
		else:
			subPage["empire"].Hide()
		subPage["account"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_ACCOUNT % (admin.GetObserverLoginName(), admin.GetObserverAID()))
		subPage["channel"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_CHANNEL % channel)
		subPage["map_info"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_MAP_INFO % (admin.GetObserverMapName(), map_index))

		self.OBSERVER_OnPointChange()
		self.OBSERVER_RefreshSkill()

	def OBSERVER_RefreshSubPageItem(self):
		self.OBSERVER_OnClickInventoryPageButton(0) # refresh inventory
		self.OBSERVER_RefreshEquipment() # refresh equipment

	def OBSERVER_OnClosePage(self):
		page = self.pages[self.PAGE_OBSERVER]

		page["stopped_edit"].KillFocus()
		page["reason_input_ban"].SoftClose()
		page["reason_input_unban"].SoftClose()

	def OBSERVER_OnOpenPage(self):
		page = self.pages[self.PAGE_OBSERVER]

		if self.OBSERVER_GetSubPageIndex() == -1:
			page["stopped_edit"].SetFocus()

	def OBSERVER_StartObservation(self, name = ""):
		page = self.pages[self.PAGE_OBSERVER]

		if name == "":
			name = page["stopped_edit"].GetText()
			if name == "":
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_UPDATE_2020_A_NAME_MUST_BE_SPECIFIED)
				return

		admin.StartObserver(name)

	def OBSERVER_StopObservation(self):
		admin.StopObserver()
		self.OBSERVER_Refresh()

	def __OBSERVER_GetRealSkillSlot(self, slotIndex, skillGrade):
		return slotIndex + min(skill.SKILL_GRADE_COUNT-1, skillGrade) * skill.SKILL_GRADE_STEP_COUNT

	def OBSERVER_RefreshSkill(self):
		page = self.pages[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_GENERAL]

		job = chr.RaceToJob(admin.GetObserverRaceNum())
		skillGroup = admin.GetObserverSkillGroup()
		subPage["skillgroup"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_SKILLGROUP % localeInfo.GetSkillGroupName(job, skillGroup))

		if skillGroup == 0:
			subPage["skill_wnd"].Hide()
		else:
			skillVnumList = SKILL_INDEX_DICT[job][skillGroup]

			for i in xrange(8):
				skillVnum = skillVnumList[i]
				skillLevel = admin.GetObserverSkillLevel(skillVnum)
				skillGrade = admin.GetObserverSkillMasterType(skillVnum)
				skillCoolTime = admin.GetObserverSkillCoolTime(skillVnum)
				skillElapsedCoolTime = admin.GetObserverESkillCoolTime(skillVnum)

				if skillGrade >= 1:
					skillLevel -= 20 - 1
					if skillGrade >= 2:
						skillLevel -= 10

				for j in xrange(skill.SKILL_GRADE_COUNT):
					slotIndex = self.__OBSERVER_GetRealSkillSlot(i + 1, j)

					subPage["skill"].ClearSlot(slotIndex)

					if skillVnum != 0:
						subPage["skill"].SetSkillSlotNew(slotIndex, skillVnum, j, skillLevel)
						subPage["skill"].SetCoverButton(slotIndex)

						if ((skillGrade == skill.SKILL_GRADE_COUNT) and j == (skill.SKILL_GRADE_COUNT - 1)) or (skillGrade == j):
							subPage["skill"].SetSlotCountNew(slotIndex, skillGrade, skillLevel)
							if skillCoolTime != 0 and skillElapsedCoolTime < skillCoolTime:
								subPage["skill"].SetSlotCoolTime(slotIndex, float(skillCoolTime) / 1000.0, float(skillElapsedCoolTime) / 1000.0)
						else:
							subPage["skill"].SetSlotCount(slotIndex, 0)
							subPage["skill"].DisableCoverButton(slotIndex)

			subPage["skill_wnd"].Show()

	def OBSERVER_OnOverInItemSlot(self, slotPos):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		if slotPos < player.INVENTORY_PAGE_SIZE:
			slotPos += pageData["inventory_page"] * player.INVENTORY_PAGE_SIZE
		(itemID, itemVnum, itemCount, isGMItem) = admin.GetObserverItem(slotPos)
		itemSocket = admin.GetObserverItemSocket(slotPos)
		itemAttr = admin.GetObserverItemAttr(slotPos)

		subPage["item_tooltip"].ClearToolTip()
		subPage["item_tooltip"].AddItemData(itemVnum, itemSocket, itemAttr)
		subPage["item_tooltip"].AppendSpace(5)
		subPage["item_tooltip"].AppendTextLine(localeInfo.ADMIN_MANAGER_OBSERVER_ITEM_TOOLTIP_ID % itemID)
		subPage["item_tooltip"].AppendTextLine(localeInfo.ADMIN_MANAGER_OBSERVER_DOUBLECLICK_INFO)
		subPage["item_tooltip"].ShowToolTip()

	def OBSERVER_OnOverOutItemSlot(self):
		page = self.pages[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		subPage["item_tooltip"].HideToolTip()

	def OBSERVER_OnDoubleClickItemSlot(self, slotPos):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		if slotPos < player.INVENTORY_PAGE_SIZE:
			slotPos += pageData["inventory_page"] * player.INVENTORY_PAGE_SIZE
		(itemID, itemVnum, itemCount, isGMItem) = admin.GetObserverItem(slotPos)

		itemName = "#" + str(itemVnum)
		if item.SelectItem(itemVnum):
			itemName = item.GetItemName()

		os.system('echo %d|clip' % itemID)
		chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_OBSERVER_ITEM_ID_COPIED % (itemID, itemName))

	def OBSERVER_OnClickInventoryPageButton(self, inventoryPageIndex):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		pageData["inventory_page"] = inventoryPageIndex

		for i in xrange(player.INVENTORY_PAGE_COUNT):
			btn = subPage["inventory_page_%d" % (i + 1)]
			if i == inventoryPageIndex:
				btn.Down()
			else:
				btn.SetUp()

		self.OBSERVER_RefreshInventory()

	def OBSERVER_RefreshInventory(self, pageIndex = -1):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		if pageIndex != -1 and pageIndex != pageData["inventory_page"]:
			return

		for i in xrange(player.INVENTORY_PAGE_SIZE):
			(itemID, itemVnum, itemCount, isGMItem) = admin.GetObserverItem(pageData["inventory_page"] * player.INVENTORY_PAGE_SIZE + i)
			if itemCount <= 1:
				itemCount = 0
			subPage["inventory"].SetItemSlot(i, itemVnum, itemCount)


	def OBSERVER_RefreshEquipment(self):
		page = self.pages[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		for i in xrange(player.EQUIPMENT_PAGE_COUNT):
			slotNumber = player.EQUIPMENT_SLOT_START + i
			(itemID, itemVnum, itemCount, isGMItem) = admin.GetObserverItem(slotNumber)
			if itemCount <= 1:
				itemCount = 0
			subPage["equipment"].SetItemSlot(slotNumber, itemVnum, itemCount)

	def OBSERVER_OnClickChatBanActivate(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_BAN]

		sec = subPage["chat_day"].GetValue() * 24 * 60 * 60 + subPage["chat_hour"].GetValue() * 60 * 60 + subPage["chat_minute"].GetValue() * 60
		if sec == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_OBSERVER_BAN_ACTIVATE_INVALID)
			return

		self.OBSERVER_RequestBan(admin.BAN_TYPE_CHAT, sec, 1)

	def OBSERVER_OnClickChatBanDeactivate(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_BAN]

		self.OBSERVER_RequestBan(admin.BAN_TYPE_CHAT, 0, 0)

	def OBSERVER_OnClickAccountBanActivate(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_BAN]

		sec = subPage["account_day"].GetValue() * 24 * 60 * 60 + subPage["account_hour"].GetValue() * 60 * 60 + subPage["account_minute"].GetValue() * 60
		if sec == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_OBSERVER_BAN_ACTIVATE_INVALID)
			return

		self.OBSERVER_RequestBan(admin.BAN_TYPE_ACCOUNT, sec, 1)

	def OBSERVER_RequestBan(self, banType, duration, inccounter):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]

		pageData["current_ban_type"] = banType
		pageData["current_ban_duration"] = duration
		pageData["current_ban_inccounter"] = inccounter

		page["reason_input_ban"].Hide()
		page["reason_input_unban"].Hide()
		if int(duration) > 0:
			page["reason_input_ban"].Open()
		else:
			page["reason_input_unban"].Open()

	def OBSERVER_OnClickReasonBanButton(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]

		if pageData["current_ban_type"] == admin.BAN_TYPE_CHAT:
			net.SendChatPacket("/block_chat \"" + pageData["observer_name"] + "\" " + str(pageData["current_ban_duration"]) + \
				" " + str(pageData["current_ban_inccounter"]) + " \"" + page["reason_input_ban"].GetText(0) + "\"" + \
				" \"" + page["reason_input_ban"].GetText(1) + "\"")
		elif pageData["current_ban_type"] == admin.BAN_TYPE_ACCOUNT:
			aid = admin.GetObserverAID()
			playerid = admin.GetObserverPID()
			admin.BanAccount(aid, playerid, int(pageData["current_ban_duration"]), pageData["current_ban_inccounter"],\
				page["reason_input_ban"].GetText(0), page["reason_input_ban"].GetText(1))

		page["reason_input_ban"].SoftClose()

	def OBSERVER_OnClickReasonUnbanButton(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]

		if pageData["current_ban_name"] != "":
			if pageData["current_ban_type"] == admin.BAN_TYPE_CHAT:
				net.SendChatPacket("/block_chat \"" + pageData["observer_name"] + "\" " + str(pageData["current_ban_duration"]) + \
					" " + str(pageData["current_ban_inccounter"]) + " \"" + page["reason_input_unban"].GetText(0) + "\"" + \
					" \"" + pageData["reason_input_unban"].GetText(1) + "\"")

		page["reason_input_unban"].SoftClose()

	def OBSERVER_OnClickNaviButton(self, index):
		page = self.pages[self.PAGE_OBSERVER]

		# set other buttons up
		for i in xrange(self.OBSERVER_NAVI_MAX_NUM):
			btn = page["navi_buttons"][i]
			if i == index:
				btn.Down()
			else:
				btn.SetUp()

		# set sub page
		self.OBSERVER_SetSubPageIndex(index)

	def OBSERVER_OnPointChange(self):
		page = self.pages[self.PAGE_OBSERVER]

		# GENERAL subpage
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_GENERAL]

		subPage["level"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_LEVEL % admin.GetObserverPoint(player.LEVEL))

		curVal = admin.GetObserverPoint(player.HP)
		maxVal = max(1, admin.GetObserverPoint(player.MAX_HP))
		subPage["hpbar"].SetPercentage(min(curVal, maxVal), maxVal)
		subPage["hptext"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_HP % (curVal, maxVal))

		curVal = admin.GetObserverPoint(player.SP)
		maxVal = max(1, admin.GetObserverPoint(player.MAX_SP))
		subPage["spbar"].SetPercentage(min(curVal, maxVal), maxVal)
		subPage["sptext"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_SP % (curVal, maxVal))

		curVal = admin.GetObserverPoint(player.EXP)
		maxVal = max(1, admin.GetObserverPoint(player.NEXT_EXP))
		for i in xrange(len(subPage["exp_points"])):
			subPage["exp_points"][i].Hide()
		expPerc = float(curVal) / float(maxVal)
		i = 0
		while expPerc >= 1.0 / float(len(subPage["exp_points"])) and i < len(subPage["exp_points"]):
			subPage["exp_points"][i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
			subPage["exp_points"][i].Show()
			expPerc -= 1.0 / float(len(subPage["exp_points"]))
			i += 1
		if i < len(subPage["exp_points"]):
			subPage["exp_points"][i].SetRenderingRect(0.0, expPerc / (1.0 / float(len(subPage["exp_points"]))) - 1.0, 0.0, 0.0)
			subPage["exp_points"][i].Show()
		subPage["exp_tooltip"].SetText("%s : %.2f%%" % (localeInfo.TASKBAR_EXP, float(curVal) / max(1, float(maxVal)) * 100))

		curVal = admin.GetObserverPoint(player.ELK)
		subPage["gold"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_GENERAL_GOLD % localeInfo.NumberToString(curVal))

		# ITEM subpage
		subPage = page["subpage_%d" % self.OBSERVER_NAVI_ITEM]

		curVal = admin.GetObserverPoint(player.ELK)
		subPage["money"].SetText(localeInfo.NumberToMoneyString(curVal))

	def OBSERVER_OnUpdate(self):
		page = self.pages[self.PAGE_OBSERVER]
		pageData = self.pageData[self.PAGE_OBSERVER]
		subPageIndex = self.OBSERVER_GetSubPageIndex()
		if subPageIndex != -1:
			subPage = page["subpage_%d" % subPageIndex]

		if self.currentPageIndex == self.PAGE_OBSERVER:
			if subPageIndex == self.OBSERVER_NAVI_GENERAL:
				if self.IsShow() and subPage["exp_point_bg"].IsInPosition():
					subPage["exp_tooltip"].Show()
				else:
					subPage["exp_tooltip"].Hide()
			elif subPageIndex == self.OBSERVER_NAVI_BAN:
				# chatban
				timeLeft = admin.GetObserverChatBanTimeLeft()
				if timeLeft == 0:
					subPage["chat_state"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_BAN_STATUS_NONE)
					subPage["chat_deactivate"].Disable()
				elif not admin.IsObserverStopForced():
					subPage["chat_state"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_BAN_STATUS_RUNNING % localeInfo.SecondToDHMS(timeLeft))
					if not subPage["chat_deactivate"].IsEnabled():
						subPage["chat_deactivate"].Enable()
				# accountban
				timeLeft = admin.GetObserverAccountBanTimeLeft()
				if timeLeft == 0:
					subPage["account_state"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_BAN_STATUS_NONE)
				else:
					subPage["account_state"].SetText(localeInfo.ADMIN_MANAGER_OBSERVER_BAN_STATUS_RUNNING % localeInfo.SecondToDHMS(timeLeft))

			if admin.IsObserverStopForced():
				if not pageData.has_key("last_retry"):
					pageData["last_retry"] = app.GetTime()
				if pageData["last_retry"] + 10 < app.GetTime():
					pageData["last_retry"] = app.GetTime()
					admin.StartObserver(self.OBSERVER_GetName(), False)

	def OBSERVER_OnAfterRender(self):
		page = self.pages[self.PAGE_OBSERVER]
		subPageIndex = self.OBSERVER_GetSubPageIndex()

		if admin.IsObserverStopForced():
			subPageWnd = page["subpage_%d" % subPageIndex]["wnd"]

			x, y = subPageWnd.GetGlobalPosition()
			w = subPageWnd.GetWidth()
			h = subPageWnd.GetHeight()

			grp.SetColor(self.DISABLE_COLOR)
			grp.RenderBar(x - 5, y - 5, w + 5 * 2, h + 5 * 2)

	#################################################
	## PAGE: BAN FUNCTIONS
	#################################################

	def BAN_Build(self):
		page = self.pages[self.PAGE_BAN]

		wndPlayerToolTip = uiToolTip.ToolTip()
		wndPlayerToolTip.HideToolTip()
		page["player_tooltip"] = wndPlayerToolTip

		wndAccountToolTip = uiToolTip.ToolTip()
		wndAccountToolTip.HideToolTip()
		page["account_tooltip"] = wndAccountToolTip

		dlgReasonInputBan = uiCommon.DoubleInputDialogWithDescription()
		dlgReasonInputBan.SetTitle(localeInfo.ADMIN_MANAGER_BAN_CHAT_REASON_INPUT_TITLE_BAN)
		dlgReasonInputBan.SetDescription(localeInfo.ADMIN_MANAGER_BAN_CHAT_REASON_INPUT_BAN1, 0)
		dlgReasonInputBan.SetDescription(localeInfo.ADMIN_MANAGER_BAN_CHAT_REASON_INPUT_BAN2, 1)
		dlgReasonInputBan.SetAcceptEvent(self.BAN_OnClickReasonBanButton)
		dlgReasonInputBan.SetCancelEvent(dlgReasonInputBan.Hide)
		dlgReasonInputBan.SetMaxLength(50, 0)
		dlgReasonInputBan.SetMaxLength(200, 1)
		dlgReasonInputBan.SetDisplayWidth(dlgReasonInputBan.GetDisplayWidth(0), 1)
		page["reason_input_ban"] = dlgReasonInputBan
		dlgReasonInputUnban = uiCommon.DoubleInputDialogWithDescription()
		dlgReasonInputUnban.SetTitle(localeInfo.ADMIN_MANAGER_BAN_CHAT_REASON_INPUT_TITLE_UNBAN)
		dlgReasonInputUnban.SetDescription(localeInfo.ADMIN_MANAGER_BAN_CHAT_REASON_INPUT_UNBAN1, 0)
		dlgReasonInputUnban.SetDescription(localeInfo.ADMIN_MANAGER_BAN_CHAT_REASON_INPUT_UNBAN2, 1)
		dlgReasonInputUnban.SetAcceptEvent(self.BAN_OnClickReasonUnbanButton)
		dlgReasonInputUnban.SetCancelEvent(dlgReasonInputUnban.Hide)
		dlgReasonInputUnban.SetMaxLength(50, 0)
		dlgReasonInputUnban.SetMaxLength(50, 1)
		dlgReasonInputUnban.SetDisplayWidth(dlgReasonInputUnban.GetDisplayWidth(0), 1)
		page["reason_input_unban"] = dlgReasonInputUnban

		self.BAN_ChatSetState(self.BAN_CHAT_STATE_NONE)
		self.BAN_AccountSetState(self.BAN_ACCOUNT_STATE_NONE)
		self.BAN_SetAccountSearchType(admin.BAN_ACCOUNT_SEARCH_ACCOUNT)

	def BAN_Initialize(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		page["log_wnd"].Hide()

		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_SEARCH_RESULT]
		subPage["time_wnd"].SetSize(subPage["desc_min"].GetRight(), subPage["time_wnd"].GetHeight())
		subPage["time_wnd"].UpdateRect()

		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_SEARCH_RESULT]
		subPage["time_wnd"].SetSize(subPage["desc_min"].GetRight(), subPage["time_wnd"].GetHeight())
		subPage["time_wnd"].UpdateRect()

		pageData["account_search_result"] = 0

		if not admin.HasAllow(admin.ALLOW_VIEW_BAN_CHAT):
			page["chat_wnd"].Hide()
		if not admin.HasAllow(admin.ALLOW_VIEW_BAN_CHAT_LOG):
			subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_SEARCH_RESULT]
			subPage["face"].Disable()
		if not admin.HasAllow(admin.ALLOW_BAN_CHAT):
			subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_NONE]
			subPage["chat_unban_btn"].Hide()
			subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_SEARCH_RESULT]
			subPage["btn_ban"].Hide()
			subPage["btn_unban"].Hide()

	def BAN_SetPlayerToolTip(self, pid, name, race, level, chatban_count, accountban_count, timeout, is_online):
		page = self.pages[self.PAGE_BAN]

		toolTip = page["player_tooltip"]
		toolTip.ClearToolTip()

		toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_PID % (pid))
		toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_NAME % (name, level))
		toolTip.AppendSpace(3)
		toolTip.AppendImage(self.FACE_IMAGE_DICT[race] % "")
		toolTip.AppendSpace(3)
		toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_CHATBAN % (chatban_count))
		toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_ACCOUNTBAN % (accountban_count))
		toolTip.AppendSpace(5)
		if timeout == 0:
			toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_NO_TIMEOUT, grp.GenerateColor(110.0/255.0, 1.0, 110.0/255.0, 1.0))
		else:
			toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_TIMEOUT % (localeInfo.SecondToDHMS(timeout)), grp.GenerateColor(1.0, 110.0/255.0, 110.0/255.0, 1.0))
		toolTip.AppendSpace(3)
		if is_online:
			toolTip.AppendExtendedTextLine(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_ONLINE)
		else:
			toolTip.AppendExtendedTextLine(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_OFFLINE)

		toolTip.ShowToolTip()

	def BAN_SetAccountToolTip(self, accid, accname, accban_count, accban_duration, accinfo):
		page = self.pages[self.PAGE_BAN]

		toolTip = page["account_tooltip"]
		toolTip.ClearToolTip()

		toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_TOOLTIP_ACCID % (accid))
		toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_TOOLTIP_ACCNAME % (accname))
		toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_TOOLTIP_ACCBAN_COUNT % (accban_count))
		toolTip.AppendSpace(3)
		if accban_duration == 0:
			toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_TOOLTIP_NO_TIMEOUT, grp.GenerateColor(110.0/255.0, 1.0, 110.0/255.0, 1.0))
		else:
			toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_TOOLTIP_TIMEOUT % (localeInfo.SecondToDHMS(accban_duration)),\
				grp.GenerateColor(1.0, 110.0/255.0, 110.0/255.0, 1.0))
		# add player short info
		for i in xrange(net.PLAYER_PER_ACCOUNT5):
			pid, pname, race, level, ban_count, is_online = admin.GetBanAccountPlayer(accinfo, i)
			if pid != 0:
				toolTip.AppendSpace(5)
				toolTip.AppendTextLine(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_TOOLTIP_PLAYER_TEXT % (pname, pid))
				toolTip.AppendSpace(3)
				toolTip.AppendImage(self.FACE_IMAGE_DICT[race] % "")

		toolTip.ShowToolTip()

	def BAN_ChatRefresh(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		for i in xrange(self.BAN_CHAT_STATE_MAX_NUM):
			subPage = page["chat_state_%d" % i]
			if i == pageData["chat_state"]:
				subPage["wnd"].Show()
			else:
				subPage["wnd"].Hide()

	def BAN_AccountRefresh(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		for i in xrange(self.BAN_ACCOUNT_STATE_MAX_NUM):
			subPage = page["account_state_%d" % i]
			if i == pageData["account_state"]:
				subPage["wnd"].Show()
			else:
				subPage["wnd"].Hide()

	def BAN_ChatSetState(self, state):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		pageData["chat_state"] = state
		self.BAN_ChatRefresh()

	def BAN_AccountSetState(self, state):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		pageData["account_state"] = state
		self.BAN_AccountRefresh()

	def BAN_SetAccountSearchType(self, type):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		pageData["account_search_type"] = type

		btn = page["account_search_type_btn"]
		if type == admin.BAN_ACCOUNT_SEARCH_ACCOUNT:
			btn.SetToolTipText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_SEARCH_TYPE_ACCOUNT_TOOLTIP)
			btn.SetText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_SEARCH_TYPE_ACCOUNT)
		elif type == admin.BAN_ACCOUNT_SEARCH_PLAYER:
			btn.SetToolTipText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_SEARCH_TYPE_PLAYER_TOOLTIP)
			btn.SetText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_SEARCH_TYPE_PLAYER)

	def BAN_ChatRefreshScroll(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_NONE]

		if subPage["chat_list"].GetItemCount() <= subPage["chat_list"].GetViewItemCount():
			subPage["chat_scroll"].Hide()
		else:
			subPage["chat_scroll"].SetMiddleBarSize(float(subPage["chat_list"].GetViewItemCount()) / float(subPage["chat_list"].GetItemCount()))
			subPage["chat_scroll"].Show()

	def BAN_AccountRefreshScroll(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_NONE]

		if subPage["account_list"].GetItemCount() <= subPage["account_list"].GetViewItemCount():
			subPage["account_scroll"].Hide()
		else:
			subPage["account_scroll"].SetMiddleBarSize(float(subPage["account_list"].GetViewItemCount()) / float(subPage["account_list"].GetItemCount()))
			subPage["account_scroll"].Show()

	def BAN_ChatRefreshList(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_NONE]

		selectedPID = subPage["chat_list"].GetSelectedItem()

		subPage["chat_list"].ClearItem()
		for i in xrange(admin.GetBanChatPlayerCount()):
			pid, name, race, level, chatban_count, accban_count, timeout, is_online = admin.GetBanChatPlayerByIndex(i)
			subPage["chat_list"].InsertItem(pid, name)
			if selectedPID == pid:
				subPage["chat_list"].SelectItem(i)

		self.BAN_ChatRefreshScroll()

	def BAN_AccountRefreshList(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_NONE]

		selectedAID = subPage["account_list"].GetSelectedItem()

		subPage["account_list"].ClearItem()
		for i in xrange(admin.GetBanAccountCount()):
			aid, name, ban_count, duration, pinfo = admin.GetBanAccountByIndex(i)
			subPage["account_list"].InsertItem(aid, name)
			if selectedAID == aid:
				subPage["account_list"].SelectItem(i)

		self.BAN_AccountRefreshScroll()

	def BAN_ChatRefreshPlayer(self, pid):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]
		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_NONE]

		rpid, name, race, level, chatban_count, accban_count, timeout, is_online = admin.GetBanChatPlayerByPID(pid)
		if rpid == 0 or timeout == 0:
			if subPage["chat_list"].EraseItem(pid):
				self.BAN_ChatRefreshScroll()
		else:
			if not subPage["chat_list"].HasItem(pid):
				subPage["chat_list"].InsertItem(pid, name)
				self.BAN_ChatRefreshScroll()

		if rpid != 0 and pageData["chat_state"] == self.BAN_CHAT_STATE_SEARCH_RESULT:
			self.BAN_ChatShowResult(pageData["chat_search_result"])

	def BAN_AccountRefreshSingle(self, aid):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]
		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_NONE]

		raid, name, ban_count, duration, pinfo = admin.GetBanAccountByAID(aid)
		if raid == 0 or duration == 0:
			if subPage["account_list"].EraseItem(aid):
				self.BAN_AccountRefreshScroll()
		else:
			if not subPage["account_list"].HasItem(aid):
				subPage["account_list"].InsertItem(aid, name)
				self.BAN_AccountRefreshScroll()

		if raid != 0 and pageData["account_state"] == self.BAN_ACCOUNT_STATE_SEARCH_RESULT:
			self.BAN_AccountShowResult(pageData["account_search_result"])

	def BAN_ChatLoadResult(self, success):
		if success:
			self.BAN_ChatShowResult(admin.GetBanChatSearchResultPID())
		else:
			self.BAN_ChatShowResult(0)

	def BAN_AccountLoadResult(self, success):
		if success:
			self.BAN_AccountShowResult(admin.GetBanAccountSearchResultAID())
		else:
			self.BAN_AccountShowResult(0)

	def BAN_ChatShowResult(self, pid=-1):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		reloadTimeout = False
		if pid == -1:
			pid = pageData["chat_search_result"]
			reloadTimeout = True

		if pid == 0:
			self.BAN_ChatSetState(self.BAN_CHAT_STATE_SEARCH_FAIL)

		else:
			subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_SEARCH_RESULT]
			try:
				pid, name, race, level, chatban_count, accountban_count, timeout, is_online = admin.GetBanChatPlayerByPID(pid)
			except:
				timeout = 0

			if reloadTimeout == False:
				subPage["pid"].SetText(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_PID % (pid))
				subPage["name"].SetText(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_NAME % (name, level))
				subPage["face"].SetUpVisual(self.FACE_IMAGE_DICT[race] % "")
				subPage["face"].SetOverVisual(self.FACE_IMAGE_DICT[race] % "_over")
				subPage["face"].SetDownVisual(self.FACE_IMAGE_DICT[race] % "_down")
				subPage["face"].SetDisableVisual(self.FACE_IMAGE_DICT[race] % "")
				subPage["face"].UpdateRect()
				subPage["chatban"].SetText(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_CHATBAN % (chatban_count))
				subPage["accountban"].SetText(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_ACCOUNTBAN % (accountban_count))
			if timeout == 0:
				subPage["ban_state"].SetText(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_NO_TIMEOUT)
				subPage["ban_state"].SetPackedFontColor(self.BAN_INACTIVE_COLOR)
				if subPage["btn_unban"].IsEnabled():
					subPage["btn_unban"].Disable()
			else:
				subPage["ban_state"].SetText(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_TIMEOUT % (localeInfo.SecondToDHMS(timeout)))
				subPage["ban_state"].SetPackedFontColor(self.BAN_ACTIVE_COLOR)
				if not subPage["btn_unban"].IsEnabled():
					subPage["btn_unban"].Enable()
			if reloadTimeout == False:
				if is_online:
					subPage["online_state"].SetText(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_ONLINE)
				else:
					subPage["online_state"].SetText(localeInfo.ADMIN_MANAGER_BAN_PLAYER_TOOLTIP_OFFLINE)

			pageData["chat_search_result"] = pid
			self.BAN_ChatSetState(self.BAN_CHAT_STATE_SEARCH_RESULT)

	def BAN_AccountShowResult(self, aid=-1):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		reloadTimeout = False
		if aid == -1:
			aid = pageData["account_search_result"]
			reloadTimeout = True
		elif aid != pageData["account_search_result"]:
			pageData["account_search_result_pcount"] = 1

		if aid == 0:
			subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_SEARCH_FAIL]
			for i in xrange(admin.BAN_ACCOUNT_SEARCH_MAX_NUM):
				subPage["text_%d" % i].Hide()
			subPage["text_%d" % pageData["account_search_type"]].Show()

			self.BAN_AccountSetState(self.BAN_ACCOUNT_STATE_SEARCH_FAIL)

		else:
			subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_SEARCH_RESULT]
			try:
				aid, login, accban_count, timeout, pinfo = admin.GetBanAccountByAID(aid)
			except:
				timeout = 0

			playerIndex = 0
			playerCount = 0
			playerFound = False
			for i in xrange(net.PLAYER_PER_ACCOUNT5):
				pid, pname, prace, plevel, pchatban_count, pis_online = admin.GetBanAccountPlayer(pinfo, i)
				if pid != 0:
					playerCount += 1
					if playerFound == False:
						playerIndex = i
						if playerCount == pageData["account_search_result_pcount"]:
							playerFound = True
			if playerCount < pageData["account_search_result_pcount"]:
				pageData["account_search_result_pcount"] = playerCount
			pageData["account_search_result_pindex"] = playerIndex

			if playerCount > 0:
				pid, pname, prace, plevel, pchatban_count, pis_online = admin.GetBanAccountPlayer(pinfo, playerIndex)

			for i in xrange(net.PLAYER_PER_ACCOUNT5):
				if i < playerCount:
					if not subPage["btn_select"][i].IsEnabled():
						subPage["btn_select"][i].Enable()
				else:
					if subPage["btn_select"][i].IsEnabled():
						subPage["btn_select"][i].Disable()

			## hide player data
			if reloadTimeout == False:
				subPage["player"].Hide()
				subPage["face"].Hide()
				subPage["chatban"].Hide()
				subPage["online_state"].Hide()

				subPage["account"].SetText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_RESULT_ACCOUNT % (login, aid))
				subPage["player"].SetText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_RESULT_PLAYER % (pname, plevel, pid))
				subPage["face"].SetUpVisual(self.FACE_IMAGE_DICT[prace] % "")
				subPage["face"].SetOverVisual(self.FACE_IMAGE_DICT[prace] % "_over")
				subPage["face"].SetDownVisual(self.FACE_IMAGE_DICT[prace] % "_down")
				subPage["face"].SetDisableVisual(self.FACE_IMAGE_DICT[prace] % "")
				subPage["face"].UpdateRect()
				subPage["chatban"].SetText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_RESULT_CHATBAN % (pchatban_count))
				subPage["accountban"].SetText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_RESULT_ACCOUNTBAN % (accban_count))
				if pis_online:
					subPage["online_state"].SetText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_RESULT_ONLINE)
				else:
					subPage["online_state"].SetText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_RESULT_OFFLINE)

				if pid != 0:
					subPage["player"].Show()
					subPage["face"].Show()
					subPage["chatban"].Show()
					subPage["online_state"].Show()
			if timeout == 0:
				subPage["ban_state"].SetText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_RESULT_NO_TIMEOUT)
				subPage["ban_state"].SetPackedFontColor(self.BAN_INACTIVE_COLOR)
				if subPage["btn_unban"].IsEnabled():
					subPage["btn_unban"].Disable()
			else:
				subPage["ban_state"].SetText(localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_RESULT_TIMEOUT % (localeInfo.SecondToDHMS(timeout)))
				subPage["ban_state"].SetPackedFontColor(self.BAN_ACTIVE_COLOR)
				if not subPage["btn_unban"].IsEnabled():
					subPage["btn_unban"].Enable()

			pageData["account_search_result"] = aid
			self.BAN_AccountSetState(self.BAN_ACCOUNT_STATE_SEARCH_RESULT)

	def BAN_RequestBan(self, banType, name, duration, inccounter):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		pageData["current_ban_type"] = banType
		pageData["current_ban_name"] = name
		pageData["current_ban_duration"] = duration
		pageData["current_ban_inccounter"] = inccounter

		page["reason_input_ban"].SoftClose()
		page["reason_input_unban"].SoftClose()
		if int(duration) > 0:
			page["reason_input_ban"].Open()
		else:
			page["reason_input_unban"].Open()

	def BAN_LoadLog(self):
		page = self.pages[self.PAGE_BAN]

		if admin.GetBanLogInfoCount() == 0:
			page["log_nodata"].Show()
			page["log_data"].Hide()
			page["log_scroll"].Hide()

		else:
			page["log_nodata"].Hide()
			page["log_data"].Show()

			page["log_data"].Clear()
			for i in xrange(admin.GetBanLogInfoCount()):
				pid, name, gmPid, gmName, banType, durNew, reason, proof, date = admin.GetBanLogInfo(i)
				banTypeName = "?"
				if banType == admin.BAN_TYPE_CHAT:
					banTypeName = localeInfo.ADMIN_MANAGER_BAN_TYPE_CHAT
				elif banType == admin.BAN_TYPE_ACCOUNT:
					banTypeName = localeInfo.ADMIN_MANAGER_BAN_TYPE_ACCOUNT
				colList = [name, gmName, banTypeName, localeInfo.SecondToDHMSAdmin(durNew, 60*60*24), reason, proof, date]
				page["log_data"].Append(i, colList, False)
			page["log_data"].LocateLines()

			if page["log_data"].GetLineCount() <= page["log_data"].GetViewLineCount():
				page["log_scroll"].Hide()

			else:
				page["log_scroll"].SetMiddleBarSize(float(page["log_data"].GetViewLineCount()) / float(page["log_data"].GetLineCount()))
				page["log_scroll"].SetPos(0.0)
				page["log_scroll"].Show()

	def BAN_OnClickChatSearch(self):
		page = self.pages[self.PAGE_BAN]

		name = page["chat_search_edit"].GetText()
		if name == "":
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_BAN_CHAT_SEARCH_NO_PLAYER)
			return

		self.BAN_ChatSetState(self.BAN_CHAT_STATE_SEARCHING)

		pid = admin.GetBanChatPlayerPIDByName(name)
		if pid != 0:
			admin.SetBanChatSearchResultPID(pid)
			self.BAN_ChatShowResult(pid)

		else:
			admin.SearchBanChatPlayer(name)

	def BAN_OnClickAccountSearchType(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		curType = pageData["account_search_type"]
		if curType == admin.BAN_ACCOUNT_SEARCH_ACCOUNT:
			curType = admin.BAN_ACCOUNT_SEARCH_PLAYER
		elif curType == admin.BAN_ACCOUNT_SEARCH_PLAYER:
			curType = admin.BAN_ACCOUNT_SEARCH_ACCOUNT

		self.BAN_SetAccountSearchType(curType)

	def BAN_OnClickAccountSearch(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		name = page["account_search_edit"].GetText()
		if name == "":
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_SEARCH_NO_NAME)
			return

		self.BAN_AccountSetState(self.BAN_ACCOUNT_STATE_SEARCHING)

		if pageData["account_search_type"] == admin.BAN_ACCOUNT_SEARCH_ACCOUNT:
			aid = admin.GetBanAccountAIDByName(name)
			if aid != 0:
				admin.SetBanAccountSearchResultAID(aid)
				self.BAN_AccountShowResult(aid)
				return
		elif pageData["account_search_type"] == admin.BAN_ACCOUNT_SEARCH_PLAYER:
			aid = admin.GetBanAccountAIDByPlayerName(name)
			if aid != 0:
				admin.SetBanAccountSearchResultAID(aid)
				self.BAN_AccountShowResult(aid)
				return

		admin.SearchBanAccount(pageData["account_search_type"], name)

	def BAN_OnClickChatList(self, pid):
		page = self.pages[self.PAGE_BAN]

		admin.SetBanChatSearchResultPID(pid)
		self.BAN_ChatShowResult(pid)

	def BAN_OnClickAccountList(self, aid):
		page = self.pages[self.PAGE_BAN]

		admin.SetBanAccountSearchResultAID(aid)
		self.BAN_AccountShowResult(aid)

	def BAN_OnChatScroll(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_NONE]

		pos = subPage["chat_scroll"].GetPos()
		basePos = int(float(subPage["chat_list"].GetItemCount() - subPage["chat_list"].GetViewItemCount()) * pos)
		if basePos != subPage["chat_list"].GetBasePos():
			subPage["chat_list"].SetBasePos(basePos)

	def BAN_OnAccountScroll(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_NONE]

		pos = subPage["account_scroll"].GetPos()
		basePos = int(float(subPage["account_list"].GetItemCount() - subPage["account_list"].GetViewItemCount()) * pos)
		if basePos != subPage["account_list"].GetBasePos():
			subPage["account_list"].SetBasePos(basePos)

	def BAN_OnClickLogTable(self, index):
		page = self.pages[self.PAGE_BAN]

		pid, name, gmPid, gmName, banType, durNew, reason, proof, date = admin.GetBanLogInfo(index)
		if proof:
			# just make sure it cannot start a file on your system but only open your browser
			startString = "http://"
			if proof[:len(startString) - 1].lower() != startString:
				proof = startString + proof
			os.startfile(proof)

	def BAN_OnLogScroll(self):
		page = self.pages[self.PAGE_BAN]

		pos = page["log_scroll"].GetPos()
		basePos = int(float(page["log_data"].GetLineCount() - page["log_data"].GetViewLineCount()) * pos)
		if basePos != page["log_data"].GetBasePos():
			page["log_data"].SetBasePos(basePos)

	def BAN_OnClickChatUnban(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_NONE]

		playerName = subPage["chat_list"].GetSelectedItemText()
		if playerName == "":
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_BAN_CHAT_UNBAN_NO_SELECTED)
			return

		self.BAN_RequestBan(admin.BAN_TYPE_CHAT, playerName, 0, 0)

	def BAN_OnClickAccountUnban(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_NONE]

		accountName = subPage["account_list"].GetSelectedItemText()
		if accountName == "":
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_BAN_ACCOUNT_UNBAN_NO_SELECTED)
			return

		bPid = admin.GetBanAccountAIDByName(accountName)

		self.BAN_RequestBan(admin.BAN_TYPE_ACCOUNT, accountName+"#"+str(bPid), 0, 0)

	def BAN_OnClickChatResultBan(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_SEARCH_RESULT]
		pageData = self.pageData[self.PAGE_BAN]

		sec = subPage["box_day"].GetValue() * 24 * 60 * 60 + subPage["box_hour"].GetValue() * 60 * 60 + subPage["box_min"].GetValue() * 60
		if sec == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_BAN_RESULT_BAN_TIME_INVALID)
			return

		pid, name, race, level, chatban_count, accban_count, timeout, is_online = admin.GetBanChatPlayerByPID(pageData["chat_search_result"])
		if pid == 0:
			return

		self.BAN_RequestBan(admin.BAN_TYPE_CHAT, name, sec, 1)

	def BAN_OnClickAccountResultBan(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_SEARCH_RESULT]
		pageData = self.pageData[self.PAGE_BAN]

		sec = subPage["box_day"].GetValue() * 24 * 60 * 60 + subPage["box_hour"].GetValue() * 60 * 60 + subPage["box_min"].GetValue() * 60
		if sec == 0:
			chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_BAN_RESULT_BAN_TIME_INVALID)
			return

		aid, name, ban_count, dur, pinfo = admin.GetBanAccountByAID(pageData["account_search_result"])
		if aid == 0:
			return

		pid, pname, race, level, ban_count, is_online = admin.GetBanAccountPlayer(pinfo, pageData["account_search_result_pindex"])

		self.BAN_RequestBan(admin.BAN_TYPE_ACCOUNT, name+"#"+str(pid), sec, 1)

	def BAN_OnClickChatResultUnban(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["chat_state_%d" % self.BAN_CHAT_STATE_SEARCH_RESULT]
		pageData = self.pageData[self.PAGE_BAN]

		pid, name, race, level, chatban_count, accban_count, timeout, is_online = admin.GetBanChatPlayerByPID(pageData["chat_search_result"])
		if pid == 0:
			return

		self.BAN_RequestBan(admin.BAN_TYPE_CHAT, name, 0, 0)

	def BAN_OnClickAccountResultUnban(self):
		page = self.pages[self.PAGE_BAN]
		subPage = page["account_state_%d" % self.BAN_ACCOUNT_STATE_SEARCH_RESULT]
		pageData = self.pageData[self.PAGE_BAN]

		aid, name, ban_count, dur, pinfo = admin.GetBanAccountByAID(pageData["account_search_result"])
		if aid == 0:
			return

		pid, pname, race, level, ban_count, is_online = admin.GetBanAccountPlayer(pinfo, pageData["account_search_result_pindex"])

		self.BAN_RequestBan(admin.BAN_TYPE_ACCOUNT, name+"#"+str(pid), 0, 0)

	def BAN_OnClickChatBack(self):
		self.BAN_ChatSetState(self.BAN_CHAT_STATE_NONE)

	def BAN_OnClickAccountBack(self):
		self.BAN_AccountSetState(self.BAN_ACCOUNT_STATE_NONE)
		admin.SetBanAccountSearchResultAID(0)

	def BAN_OnClickChatLogShowButton(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		pid = pageData["chat_search_result"]
		try:
			pid, name, race, level, chatban_count, accountban_count, timeout, is_online = admin.GetBanChatPlayerByPID(pid)
			page["log_title"].SetText(localeInfo.ADMIN_MANAGER_BAN_LOG_TITLE % (name, pid))
		except:
			pass

		self.BAN_OnClickLogShowButton()

		admin.RequestBanLogInfo(admin.BAN_TYPE_CHAT, pid)

	def BAN_OnClickAccountSelectPlayer(self, playerCount):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		pageData["account_search_result_pcount"] = playerCount
		self.BAN_AccountShowResult(pageData["account_search_result"])

	def BAN_OnClickAccountLogShowButton(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		aid = pageData["account_search_result"]
		index = pageData["account_search_result_pindex"]
		try:
			aid, login, ban_count, dur, pinfo = admin.GetBanAccountByAID(aid)
			page["log_title"].SetText(localeInfo.ADMIN_MANAGER_BAN_LOG_ACCOUNT_TITLE % (login, aid))
		except:
			pass

		self.BAN_OnClickLogShowButton()

		admin.RequestBanLogInfo(admin.BAN_TYPE_ACCOUNT, aid)

	def BAN_OnClickLogShowButton(self):
		page = self.pages[self.PAGE_BAN]

		page["chat_wnd"].Hide()
		page["line"].Hide()
		page["account_wnd"].Hide()
		page["log_wnd"].Show()

		page["log_nodata"].Hide()
		page["log_data"].Hide()

	def BAN_OnClickLogHideButton(self):
		page = self.pages[self.PAGE_BAN]

		page["log_wnd"].Hide()
		page["chat_wnd"].Show()
		page["line"].Show()
		page["account_wnd"].Show()

	def BAN_OnClickReasonBanButton(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		if pageData["current_ban_name"] != "":
			if pageData["current_ban_type"] == admin.BAN_TYPE_CHAT:
				net.SendChatPacket("/block_chat \"" + pageData["current_ban_name"] + "\" " + str(pageData["current_ban_duration"]) + \
					" " + str(pageData["current_ban_inccounter"]) + " \"" + page["reason_input_ban"].GetText(0) + "\"" + \
					" \"" + page["reason_input_ban"].GetText(1) + "\"")
			elif pageData["current_ban_type"] == admin.BAN_TYPE_ACCOUNT:
				name = pageData["current_ban_name"]

				accname = name[:name.find("#")]
				playerid = int(name[name.find("#")+1:])
				aid = admin.GetBanAccountAIDByName(accname)
				if aid != 0:
					admin.BanAccount(aid, playerid, int(pageData["current_ban_duration"]), pageData["current_ban_inccounter"],\
						page["reason_input_ban"].GetText(0), page["reason_input_ban"].GetText(1))

		page["reason_input_ban"].SoftClose()

	def BAN_OnClickReasonUnbanButton(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		if pageData["current_ban_name"] != "":
			if pageData["current_ban_type"] == admin.BAN_TYPE_CHAT:
				net.SendChatPacket("/block_chat \"" + pageData["current_ban_name"] + "\" " + str(pageData["current_ban_duration"]) + \
					" " + str(pageData["current_ban_inccounter"]) + " \"" + page["reason_input_unban"].GetText(0) + "\"" + \
					" \"" + page["reason_input_unban"].GetText(1) + "\"")
			elif pageData["current_ban_type"] == admin.BAN_TYPE_ACCOUNT:
				name = pageData["current_ban_name"]
				accname = name[:name.find("#")]
				playerid = name[name.find("#")+1:]
				aid = admin.GetBanAccountAIDByName(accname)
				if aid != 0:
					admin.BanAccount(aid, playerid, int(pageData["current_ban_duration"]), pageData["current_ban_inccounter"],\
						page["reason_input_unban"].GetText(0), page["reason_input_unban"].GetText(1))

		page["reason_input_unban"].SoftClose()

	def BAN_OnClosePage(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		page["chat_search_edit"].KillFocus()
		page["account_search_edit"].KillFocus()
		page["reason_input_ban"].SoftClose()
		page["reason_input_unban"].SoftClose()

	def BAN_OnUpdate(self):
		page = self.pages[self.PAGE_BAN]
		pageData = self.pageData[self.PAGE_BAN]

		subPage = page["chat_state_%d" % pageData["chat_state"]]
		page["player_tooltip"].HideToolTip()
		if self.IsShow() and self.currentPageIndex == self.PAGE_BAN:
			if pageData["chat_state"] == self.BAN_CHAT_STATE_NONE:
				if subPage["chat_list"].IsOverLine():
					apply(self.BAN_SetPlayerToolTip, (admin.GetBanChatPlayerByPID(subPage["chat_list"].GetOverLine())))

			elif pageData["chat_state"] == self.BAN_CHAT_STATE_SEARCH_RESULT:
				self.BAN_ChatShowResult()

		subPage = page["account_state_%d" % pageData["account_state"]]
		page["account_tooltip"].HideToolTip()
		if self.IsShow() and self.currentPageIndex == self.PAGE_BAN:
			if pageData["account_state"] == self.BAN_ACCOUNT_STATE_NONE:
				if subPage["account_list"].IsOverLine():
					apply(self.BAN_SetAccountToolTip, (admin.GetBanAccountByAID(subPage["account_list"].GetOverLine())))

			elif pageData["account_state"] == self.BAN_ACCOUNT_STATE_SEARCH_RESULT:
				self.BAN_AccountShowResult()

	#################################################
	## PAGE: ITEM FUNCTIONS
	#################################################

	def ITEM_Build(self):
		page = self.pages[self.PAGE_ITEM]

		self.ITEM_SetMainSearchType(admin.ITEM_SEARCH_IID)

	def ITEM_GetItemInfo(self, pInfo, itemID):
		windowNames = {
			player.INVENTORY : localeInfo.ADMIN_MANAGER_ITEM_MAIN_RESULT_WINDOW_INVENTORY,
			player.EQUIPMENT : localeInfo.ADMIN_MANAGER_ITEM_MAIN_RESULT_WINDOW_EQUIPMENT,
			player.SAFEBOX : localeInfo.ADMIN_MANAGER_ITEM_MAIN_RESULT_WINDOW_SAFEBOX,
			player.MALL : localeInfo.ADMIN_MANAGER_ITEM_MAIN_RESULT_WINDOW_MALL,
			player.GROUND : localeInfo.ADMIN_MANAGER_ITEM_MAIN_RESULT_WINDOW_GROUND,
		}

		ownerType, ownerID, ownerName, windowType, cell, itemVnum, itemCount, isGMItem = admin.GetItemMainInfo(pInfo)
		sockets = [admin.GetItemSocket(pInfo, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrs = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrType, attrValue = player.GetItemAttribute(pInfo, i)
			attrs.append([attrType, attrValue])

		ownerTypeName = "?"
		if ownerType == admin.ITEM_OWNER_PLAYER:
			ownerTypeName = localeInfo.ADMIN_MANAGER_ITEM_MAIN_RESULT_OWNER_TYPE_PLAYER
		elif ownerType == admin.ITEM_OWNER_ACCOUNT:
			ownerTypeName = localeInfo.ADMIN_MANAGER_ITEM_MAIN_RESULT_OWNER_TYPE_ACCOUNT

		windowName = localeInfo.ADMIN_MANAGER_ITEM_MAIN_RESULT_WINDOW_UNKNOWN % windowType
		if windowType in windowNames:
			windowName = windowNames[windowType]

		itemName = "#" + str(itemVnum)
		if item.SelectItem(itemVnum):
			itemName = item.GetItemName()

		if isGMItem:
			isGMItemName = "YES"
		else:
			isGMItemName = "NO"

		return {
			"id" : itemID,
			"owner_type" : ownerType,
			"owner_type_name" : ownerTypeName,
			"owner_id" : ownerID,
			"owner_name" : ownerName,
			"window" : windowType,
			"window_name" : windowName,
			"cell" : cell,
			"vnum" : itemVnum,
			"name" : itemName,
			"count" : itemCount,
			"gm_item" : isGMItem,
			"gm_item_name" : isGMItemName,
			"socket" : sockets,
			"attr" : attrs,
		}

	def ITEM_SetMainSearchType(self, type):
		page = self.pages[self.PAGE_ITEM]
		pageData = self.pageData[self.PAGE_ITEM]

		pageData["main_search_type"] = type

		btn = page["main_search_type_btn"]
		if type == admin.ITEM_SEARCH_IID:
			btn.SetToolTipText(localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_TYPE_IID_TOOLTIP)
			btn.SetText(localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_TYPE_IID)
		elif type == admin.ITEM_SEARCH_INAME:
			btn.SetToolTipText(localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_TYPE_INAME_TOOLTIP)
			btn.SetText(localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_TYPE_INAME)
		elif type == admin.ITEM_SEARCH_PID:
			btn.SetToolTipText(localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_TYPE_PID_TOOLTIP)
			btn.SetText(localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_TYPE_PID)
		elif type == admin.ITEM_SEARCH_PNAME:
			btn.SetToolTipText(localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_TYPE_PNAME_TOOLTIP)
			btn.SetText(localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_TYPE_PNAME)
		elif type == admin.ITEM_SEARCH_GM_ITEM:
			btn.SetToolTipText(localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_TYPE_GM_ITEM_TOOLTIP)
			btn.SetText(localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_TYPE_GM_ITEM)

	def ITEM_ShowResult(self):
		page = self.pages[self.PAGE_ITEM]

		page["main_table"].Clear()
		for i in xrange(admin.GetItemInfoCount()):
			pInfo, itemID = admin.GetItemInfoByIndex(i)
			itemInfo = self.ITEM_GetItemInfo(pInfo, itemID)

			colList = [itemInfo["owner_type_name"], itemInfo["owner_id"], itemInfo["owner_name"], itemInfo["id"], itemInfo["name"], itemInfo["window_name"],\
				itemInfo["cell"], itemInfo["gm_item_name"]]
			page["main_table"].Append(itemID, colList, False)
		page["main_table"].LocateLines()

		if page["main_table"].GetLineCount() <= page["main_table"].GetViewLineCount():
			page["main_scroll"].Hide()

		else:
			page["main_scroll"].SetMiddleBarSize(float(page["main_table"].GetViewLineCount()) / float(page["main_table"].GetLineCount()))
			page["main_scroll"].SetPos(0.0)
			page["main_scroll"].Show()

	def ITEM_OnClickMainSearchType(self):
		page = self.pages[self.PAGE_ITEM]
		pageData = self.pageData[self.PAGE_ITEM]

		curType = pageData["main_search_type"]
		if curType == admin.ITEM_SEARCH_IID:
			curType = admin.ITEM_SEARCH_INAME
		elif curType == admin.ITEM_SEARCH_INAME:
			curType = admin.ITEM_SEARCH_PID
		elif curType == admin.ITEM_SEARCH_PID:
			curType = admin.ITEM_SEARCH_PNAME
		elif curType == admin.ITEM_SEARCH_PNAME:
			curType = admin.ITEM_SEARCH_GM_ITEM
		elif curType == admin.ITEM_SEARCH_GM_ITEM:
			curType = admin.ITEM_SEARCH_IID

		self.ITEM_SetMainSearchType(curType)

	def ITEM_OnClickMainSearch(self):
		page = self.pages[self.PAGE_ITEM]
		pageData = self.pageData[self.PAGE_ITEM]

		data = page["main_search_edit"].GetText()
		if data == "":
			if pageData["main_search_type"] != admin.ITEM_SEARCH_GM_ITEM:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_ITEM_MAIN_SEARCH_NO_TEXT)
				return

		admin.SearchItemInfo(pageData["main_search_type"], data)

	def ITEM_OnMainScroll(self):
		page = self.pages[self.PAGE_ITEM]

		pos = page["main_scroll"].GetPos()
		basePos = int(float(page["main_table"].GetLineCount() - page["main_table"].GetViewLineCount()) * pos)
		if basePos != page["main_table"].GetBasePos():
			page["main_table"].SetBasePos(basePos)

	def ITEM_OnClosePage(self):
		page = self.pages[self.PAGE_ITEM]
		pageData = self.pageData[self.PAGE_ITEM]

		page["main_search_edit"].KillFocus()

	#################################################
	## PAGE: LOGS
	#################################################
	def LOGS_Build(self):
		page = self.pages[self.PAGE_LOGS]
		pageData = self.pageData[self.PAGE_LOGS]

		pageData["question_wnd"] = uiCommon.QuestionDialogAdmin()
		pageData["question_wnd"].SetAccept2Text(localeInfo.ADMIN_MANAGER_GENERAL_QUESTION_ACCEPT_WARP)
		pageData["question_wnd"].SAFE_SetCancelEvent(pageData["question_wnd"].Close)
		pageData["question_wnd"].Close()

		admin.GetLogs()

	def LOGS_OnClosePage(self):
		page = self.pages[self.PAGE_LOGS]
		pageData = self.pageData[self.PAGE_LOGS]

	def LOGS_ShowResult(self):
		page = self.pages[self.PAGE_LOGS]

		page["main_table"].Clear()

		for i in xrange(admin.GetHackInfoCount()):
			dwHackerName, dwReason, dwCount, dwTime = admin.GetHackMainInfo(i)

			colList = [dwHackerName, dwReason, dwCount, dwTime]

			page["main_table"].Append(i, colList, False)

		page["main_table"].LocateLines()

		if page["main_table"].GetLineCount() <= page["main_table"].GetViewLineCount():
			page["main_scroll"].Hide()

		else:
			page["main_scroll"].SetMiddleBarSize(float(page["main_table"].GetViewLineCount()) / float(page["main_table"].GetLineCount()))
			page["main_scroll"].SetPos(0.0)
			page["main_scroll"].Show()

	def LOGS_OnMainScroll(self):
		page = self.pages[self.PAGE_LOGS]

		pos = page["main_scroll"].GetPos()
		basePos = int(float(page["main_table"].GetLineCount() - page["main_table"].GetViewLineCount()) * pos)
		if basePos != page["main_table"].GetBasePos():
			page["main_table"].SetBasePos(basePos)

	def LOGS_OnListDoubleClick(self, idx):
		page = self.pages[self.PAGE_LOGS]
		pageData = self.pageData[self.PAGE_LOGS]

		if admin.IsObserverRunning():
			self.OnClickNaviButton(self.PAGE_OBSERVER)
			return

		dwHackerName, dwReason, dwCount, dwTime = admin.GetHackMainInfo(idx)

		if dwHackerName == player.GetName():
			return

		pageData["question_wnd"].SetText(localeInfo.ADMIN_MANAGER_GENERAL_QUESTION_TEXT % dwHackerName)
		pageData["question_wnd"].SAFE_SetAccept1Event(self.LOGS_OnQuestionDlgAccept1, dwHackerName)
		pageData["question_wnd"].SAFE_SetAccept2Event(self.LOGS_OnQuestionDlgAccept2, dwHackerName)
		pageData["question_wnd"].Open()

	def LOGS_OnQuestionDlgAccept1(self, name):
		page = self.pages[self.PAGE_LOGS]
		pageData = self.pageData[self.PAGE_LOGS]

		pageData["question_wnd"].Close()
		self.OBSERVER_StartObservation(name)

	def LOGS_OnQuestionDlgAccept2(self, name):
		page = self.pages[self.PAGE_LOGS]
		pageData = self.pageData[self.PAGE_LOGS]

		pageData["question_wnd"].Close()
		net.SendChatPacket("/warp \"" + str(name) + "\" INVISIBLE")

	#################################################
	## NAVIGATION FUNCTIONS
	#################################################

	def OnClickNaviButton(self, index):
		# set other buttons up
		for i in xrange(self.PAGE_MAX_NUM):
			btn = self.naviBtnList[i]
			if i == index:
				btn.Down()
			else:
				btn.SetUp()

		# load page
		self.LoadPage(index)

	#################################################
	## EVENT FUNCTIONS
	#################################################

	def OnPlayerOnline(self, pid):
		self.GENERAL_AddOnlinePlayer(pid)

	def OnPlayerOffline(self, pid):
		self.GENERAL_EraseOnlinePlayer(pid)