#!/usr/bin/python
#-*- coding: iso-8859-1 -*-

#TODO
        # if showRefinedVnum and itemRefineVnum:
        #     refinedData = itemManager().GetProto(itemRefineVnum)
        #     if refinedData:
        #         self.AppendTextLine(localeInfo.Get("TOOLTIP_REFINED_TO"))
        #         self.AppendTextLine(refinedData.GetName())  # TODO LOCALE_GAME
        #         self.AppendSpace(5)
#?XD 
#* Siemanko
# strcpy(kCreateData.m_szName, rkNetActorData.m_stName.c_str());
#if( !bChangeMountStatus )
#{
#	//__RemoveAllActors();
#	__RemoveDynamicActors();
#	__RemoveAllGroundItems();
#}
# GetAntiFlagByRace
# CanHaveSpecialName
# PythonNonPlayer structs
# onSkill::SSkillData::GetSkillCoolTime
# ef SetInventoryItem(self, s
# SetExchangeOwnerItem(self, slotIndex
# QUICKSLOT_REGISTER_HOTFIX
# DEBUG_MODE
# EXTENDED_LOADING_GUAGE
# if (AFFECT_REVIVE_INVISIBLE != pkAff->dwType)
# __MOVIE_MODE__
# ns1.domeny.host
# ns2.domeny.host


#TODO -> uiCharacter passive skills buttons, + new passives
#TODO -> Missions System,
#TODO -> Designs for (ItemShop, Options, Shops),
#TODO -> Inventory Expansion,
#TODO -> Language system some things must be  refactored
#TODO -> Extension for RenderTarget shortcuts + open,
#TODO -> Mining System
#TODO -> Fishing System,
#TODO -> Pet System

#TODO -> locale_string translation = {
# BP,
# DUNG_INFO,
# ITEM_SHOP,
# MONSTER_RESPAWNER,
# MonsterSpecialHelper,
# NotificationSender,
# OfflineShops,

# }
#TODO -> ui.txt translation

import app
import chr
import re
import _winreg
import uiScriptLocale
import localeInfo
import __builtin__

import item
import player
import cfg
import os

EXCHANGE_WND, SAFEBOX_WND, STORAGE_WND, SHOP_WND, WIKI_WND = range(0, 5)
ITEM_SPLIITER, ITEM_MULTI_USE, ITEM_CHECK_INFO, ITEM_PREVIEW, ITEM_RIDE_0, ITEM_RIDE_1 = range(0, 6)

data = {
	"directory" : {
		"assets"   : "assets/ui/{}",
		"registry": "server_name_20200610_124",
		"folder"  : "config",
	},

	"window_size" : {
		"width" : 1920,
		"height": 1080,
	},

	"server_count"  : 1,
	"default_server": 0 if os.path.exists("_DEVACCESS") else 1,

	"links" : {
		"recovery" : "https://xamia.bz/remind/password",
		"changelog" : "",
		"donate" : "",
	},

	"connection_info" : {
		0	: {
			  "ip"            : "185.202.223.143",
			  "login"         : 30001,
			  "guildmark_port": 30003,
			  "server"        : (30003, 30007, 30011, 30015, 30019, 30023),
			  "serverinfo"    : ("Dev", uiScriptLocale.INTROLOGIN_SERVERINFO),
		},
		1	: {
			  "ip"            : "game.xamia.bz",
			  "login"         : 30001,
			  "guildmark_port": 30003,
			  "server"        : (30003, 30007, 30011, 30015, 30019, 30023),
			  "serverinfo"    : ("Xamia", uiScriptLocale.INTROLOGIN_SERVERINFO),
		},
	},

	"shortcust_windows" : {
		EXCHANGE_WND : {
			"key" : app.DIK_LCONTROL,
			"window": lambda s : s.interface.dlgExchange.IsShow(),
			"desc"	: ([app.DIK_LCONTROL, app.DIK_RMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_MOVE_TO_TRADE),
		},

		SAFEBOX_WND :
		{
			"key" : app.DIK_LCONTROL,
			"window":lambda s : s.interface.wndSafebox.IsShow(),
			"desc" : ([app.DIK_LCONTROL, app.DIK_RMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_MOVE_TO_WAREHOUSE),
		},

		STORAGE_WND :
		{
			"key" : app.DIK_LCONTROL,
			"window": lambda s : s.interface.wndInventory.wndSpecialStorage.IsShow(),
			"blocked" : SHOP_WND,
			"range_1" : lambda slotIndex: slotIndex < player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT,
			"range_2" : lambda slotIndex: slotIndex > player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT,
			"desc_1" : ([app.DIK_LCONTROL, app.DIK_RMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_MOVE_TO_STORAGE),
			"desc_2" : ([app.DIK_LCONTROL, app.DIK_RMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_MOVE_TO_INVENTORY),
		},

		SHOP_WND :
		{
			"key" : app.DIK_LALT,
			"window": lambda s : s.interface.dlgShop.IsShow(),
			"range_1" : lambda slotIndex: slotIndex < player.INVENTORY_PAGE_SIZE*player.INVENTORY_PAGE_COUNT,
			"desc_1" : (([app.DIK_LALT, app.DIK_RMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_ATTACH_ITEM)),
			"desc_2" : (([app.DIK_LALT, app.DIK_RMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_DETACH_ITEM)),
		},

		WIKI_WND :
		{
			"key" : app.DIK_LSHIFT,
			"desc" : (([app.DIK_LSHIFT, app.DIK_LMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_WIKI_SEARCH)),
		},
	},

	"shortcust_items" : {
		ITEM_MULTI_USE :
		{
			"key" : app.DIK_LCONTROL,
			"check" : lambda slotIndex, itemVnum, item: player.GetItemCount(slotIndex) > 1 and item.GetItemType() == item.ITEM_TYPE_GIFTBOX,
			"desc" : (([app.DIK_LCONTROL, app.DIK_RMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_USE_THEM_ALL)),
		},

		ITEM_SPLIITER :
		{
			"key" : app.DIK_LSHIFT,
			"check" : lambda slotIndex, itemVnum, item: player.GetItemCount(slotIndex) > 1 and item.IsAntiFlag(item.ITEM_ANTIFLAG_STACK) == False,
			"desc" : (([app.DIK_LSHIFT, app.DIK_LMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_SEPARATE)),
		},

		ITEM_CHECK_INFO :
		{
			"key" : app.DIK_LALT,
			"check" : lambda slotIndex, itemVnum, item: item.GetItemType() == item.ITEM_TYPE_GIFTBOX,
			"desc" : (([app.DIK_LALT, app.DIK_RMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_CHECK_CONTENT)),
		},

		ITEM_PREVIEW :
		{
			"key" : app.DIK_LCONTROL,
			"check" : lambda slotIndex, itemType, itemSubType: item.GetItemType() == item.ITEM_TYPE_ARMOR and item.GetItemSubType() == 0 or item.GetItemType() in (item.ITEM_TYPE_WEAPON, item.ITEM_TYPE_COSTUME) or item.GetItemType() == item.ITEM_TYPE_TOGGLE and item.GetItemSubType() in (item.TOGGLE_PET, item.TOGGLE_MOUNT),
			"desc" : (([app.DIK_LCONTROL, app.DIK_LMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_PREVIEW_ITEM)),
		},

		ITEM_RIDE_0 :
		{
			"key" : app.DIK_LCONTROL,
			"check" : lambda slotIndex, itemType, itemSubType: item.GetItemType() == item.ITEM_TYPE_TOGGLE and item.GetItemSubType() == item.TOGGLE_MOUNT,
			"desc" : (([app.DIK_LCONTROL, app.DIK_H], localeInfo.TOOLTIP_FAST_INTERACTION_RIDE)),
		},

		ITEM_RIDE_1 :
		{
			"key" : app.DIK_LCONTROL,
			"check" : lambda slotIndex, itemType, itemSubType: item.GetItemType() == item.ITEM_TYPE_TOGGLE and item.GetItemSubType() == item.TOGGLE_MOUNT,
			"desc" : (([app.DIK_LCONTROL, app.DIK_G], localeInfo.TOOLTIP_FAST_INTERACTION_RIDE)),
		},
	},

	"lenght_data" : {
		"loginid": 32,
		"passwd" : 32,
		"account": 5,
		"name"   : chr.PLAYER_NAME_MAX_LEN,
		"stat"   : 90,
	},

	"save_info" : {
		"account": True,
		"channel": True,
		"slot"   : True,

		"pin" : False,
	},

	"system" :{
		"list" : {
			"ENABLE_FIX_LCONTROL_QUEST" : True,
			"ENABLE_SHORTCUT_SYSTEM" : True,

			"ENABLE_ADMIN_BAN_PANEL" : True,
			"ENABLE_SKILL_SELECT" : True,
			"ENABLE_INTERFACE_WINDOW_LIST"     : True,
			"ENABLE_ACCE_ENTER_ABLE"           : True,
			"ENABLE_FAST_INTERACTIONS"         : True,
			"ENABLE_FAST_INTERACTION_EXCHANGE" : True,
			"ENABLE_FAST_INTERACTION_SAFEBOX"  : True,
			"ENABLE_FAST_INTERACTION_STORAGE"  : True if app.ENABLE_SPECIAL_STORAGE else False,
			"ENABLE_FAST_INTERACTION_STATUS"   : True,
			"ENABLE_FAST_INTERACTION_MULTI_USE": True if app.ENABLE_MULTI_USE_PACKET else False,
			"ENABLE_FAST_INTERACTION_GIFTBOX"  : True if app.ENABLE_TREASURE_BOX_LOOT else False,
			"ENABLE_FAST_INTERACTION_RENDERING": True if app.ENABLE_RENDER_TARGET_EXTENSION else False,

			"ENABLE_POISON_GAUGE"   : True,
			"ENABLE_ANIMATION_GAUGE": True,

			"ENABLE_ITEM_HIGHLIGHT_"         : True,
			"ENABLE_DSS_ACTIVE_EFFECT_BUTTON": True,
			"ENABLE_DS_REFINE_PERCENT"       : True,

			"ENABLE_NEW_SPLIT_ITEM": True,

			"ENABLE_FAST_SELL_ITEMS": True,

			"ENABLE_RECOVER_MESSAGES": True,
			"ENABLE_RECOVER_WHISPERS": False,#True if app.ENABLE_RENEWAL_WHISPER else False,
			"ENABLE_CHAT_TIME_BOX" : False,

			"ENABLE_RIGHT_PANEL_INVENTORY": True,

			"ENABLE_CONVER_MONEY_TEXT": True,

			"ENABLE_ANTY_EXP": True,

			"ENABLE_LOAD_FROM_PROTOTYPE": False,

			"ENABLE_REMOVE_SKILLS_AFFECT": True,
			"ENABLE_AFFECT_TOOLTIP": True,

			"LOGIN_UI_MODIFY": True,

			"DISABLE_TILING_MOD": True,

			"ENABLE_REFINE_MARKING_REQUIRED": True,
			"ENABLE_REFINE_ITEM_DESCRIPTION": True,
			"ENABLE_REFINE_ENTER_ABLE"      : True,

			"EVENT_MANAGER_ENABLE": True,

			"SAVE_WND_POSITION_CHARACTER"  : True,
			"SAVE_WND_POSITION_DRAGON_SOUL": True,
			"SAVE_WND_POSITION_MINIMAP"    : True,
			"SAVE_WND_POSITION_MESSENGER"  : True,

			"ENABLE_REFACTORED_OPTIONS": True,
			"ENABLE_REFACTORED_TARGET" : False,

			"ENABLE_TECHNICAL_MAINTENANCE": True,
			"ENABLE_NOTIFICATON_SENDER"   : True,

			"ENABLE_LOCK_EFFECTS": True,

			"ENABLE_HIDE_COSTUMES": True,
			"ENABLE_REFACTORED_OFFSHOP": True,

			"ENABLE_WEB_LINK" : True,
			"ENABLE_NEW_GF_UI" : True,
			"ENABLE_SELECT_ROTATION" : True,

			"ENABLE_TOOLTIP_ACCESSORY_SOCKET" : False,
			"ENABLE_TOOLTIP_CATEGORIES" : False,

			"ENABLE_OPTIONS_HIGHLIGHT_ITEM" : True,
			"ENABLE_OPTIONS_YANG_MONEY" : True,

			"ENABLE_PREVIEW" : True,

			"ENABLE_SWITCH_ITEMS" : True,

			"ENABLE_LEFT_POPUP" : True,

			"ENABLE_NEW_LOGS_CHAT" : True,
			"ANCIENT_SHOP_MULTIPLE_BUY" : True,

			"ENABLE_SKILLS_INFORMATION" : True,
			"ENABLE_LEGENDARY_STONES" : True,

			"ENABLE_UPDATE_PARTY" : True,

			"ENABLE_DUNGEON_INFORMATION" : True,
			"ENABLE_DUNGEON_TASK_INFORMATION" : True,

			"ENABLE_EXPANDED_CURRENCIE_INFORMATION" : True,

			"ENABLE_HAND_SWITCHER" : True,

			"ENABLE_EQUIPMENT_LOCK_SLOT" : True,

			"ENABLE_SHAMAN_SYSTEM" : True,

			"POPUP_SYSTEM_ENABLE" : True,

			"MISSION_MANAGER" : True,

			"ATTENDANCE_MANAGER" : True,

			"MOB_TRACKER" : True,
		},

		"acce" : {
			"MAX_ABS_CHANCE" : 25,
			0: 75,
			1: 55,
			2: 35,
			3: 25,
		},
		"treasure_box" : {
			"EMPTY_TREASURE_BOX_VNUM" : [],
			"TREASURE_BOX_ITEMS" : {},
		},
		"chat" : {
			"MESSAGES_STORAGE" : []
		},
		"whisper" : {
			"WHISPERS_STORAGE" : [],
			"WHISPERS_STORED_FOR" : "",
		},
		"anty_exp" : {
			"ANTY_EXP_STATUS" : 0,
		},
		"popup" : {
			"DIALOG_REMAINING_TIME_ENABLED" : True,
			"DIALOG_REMAINING_TIME" : 2.5,
		},
	},

	"miscellaneous" : {
		"loginwindow"       : {
			"enable_pin" : True,
			"check_channel" : False
		},
		"selectempirewindow": {
			"over_out": 0.5,
			"over_in" : 0.8,
			"selected": 1.0
		},
		"global" : {
			"default_character_state" : False,
		},
		"selectcharacterwindow" : {
			"select_time"    : 3.0,
			"character_count": 4,
		},
		"createcharacterwindow" : {
			"create_time"    : 3.0,
			"character_count": 4,
		},
		"loadingwindow" : {
			"loading_images": 3,
		},
	},

	"locale" : {
		"full"        : uiScriptLocale.INTROLOGIN_FULL_ACCOUNT,
		"no_input"    : uiScriptLocale.INTROLOGIN_EMPTY_ID_OR_PWD,
		"success"     : uiScriptLocale.INTROLOGIN_SUCCESS,
		"delete"      : uiScriptLocale.INTROLOGIN_DELETE,
		"empty"       : uiScriptLocale.INTROLOGIN_EMPTY,
		"default_text": uiScriptLocale.INTROLOGIN_DEFAULT_TEXT,
	},
}

CHARACTER_IMAGES = (
	"|Eemoticons/tooltip/warrior_color|e" , "|Eemoticons/tooltip/warrior_grey|e",
	"|Eemoticons/tooltip/ninja_color|e" , "|Eemoticons/tooltip/ninja_grey|e",
	"|Eemoticons/tooltip/sura_color|e" , "|Eemoticons/tooltip/sura_grey|e",
	"|Eemoticons/tooltip/shaman_color|e" , "|Eemoticons/tooltip/shaman_grey|e"
)

def GetEmoji(value):
	return str("|Eemoticons/actions/{}|e".format(value))

__builtin__.GetEmoji = GetEmoji

DEFAULT_SERVER = data["default_server"]

def GetWindowConfig(*args):
	try:
		key	= args[0]
		if len(args) == 2:
			value = args[1]
			return data[key][value]
		elif len(args) == 3:
			value = args[1]
			subKey = args[2]
			return data[key][value][subKey]

		return data[key]
	except KeyError:
		return False

__builtin__.GetWindowConfig = GetWindowConfig

def UpdateConfig(key, *args):
	try:
		data["system"][key][args[0]] = args[1]
	except KeyError:
		return False

__builtin__.UpdateConfig = UpdateConfig

def gcGetEnable(key):
	return GetWindowConfig("system", "list", key)

__builtin__.gcGetEnable = gcGetEnable

def LUA_SetValue(value):
	data.update({"last_used_account" : str(value)})

def GetLocaleText(key):
	return GetWindowConfig("locale", key)

def GetRegistryPath():
	return GetWindowConfig("directory", "registry")

def GetConfigPath():
	return GetWindowConfig("directory", "config")

def GetAssets():
	return data["directory"]["assets"]

__builtin__.GetAssets = GetAssets

def GetGlobalWindowSize(key):
	return GetWindowConfig("window_size", key)

if gcGetEnable("ENABLE_CONVER_MONEY_TEXT"):
	def ConvertMoneyText(text, powers=dict(k=10**3, m=10**6, b=10**9)):
		"""
		Format string value in thousands, millions or billions.

		'1k' = 1.000
		'100kk' = 100.000.000
		'100m' = 100.000.000
		'1b' = 1.000.000.000
		'1kmb' = 1.000 (can't use multiple suffixes types)

		:param text: string
		:return: int
		:date: 10.01.2020
		:author: Vegas
		"""

		match = re.search(r'(\d+)({:s}+)?'.format('+|'.join(powers.keys())), text, re.I)
		if match:
			moneyValue, suffixName = match.groups()
			moneyValue = int(moneyValue)
			if not suffixName:
				return moneyValue

			return moneyValue * (powers[suffixName[0]] ** len(suffixName))

		return 0

	__builtin__.ConvertMoneyText = ConvertMoneyText

POS_ID = 0
POS_PWD = 1
POS_PIN = 2

import os
import binascii
REG_PATH = "SOFTWARE\\" + GetRegistryPath()

class Singleton:
	def __init__(self, decorated):
		self._decorated = decorated

	def Instance(self):
		try:
			return self._instance
		except AttributeError:
			self._instance = self._decorated()
			return self._instance

	def __call__(self):
		raise TypeError('Singletons must be accessed through `Instance()`.')

	def __instancecheck__(self, inst):
		return isinstance(inst, self._decorated)

@Singleton
class RegistryHandle:

	@staticmethod
	def GetRegistryHandle(mode = _winreg.KEY_READ):
		try:
			regKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, REG_PATH, 0, mode)
			return regKey
		except WindowsError:
			return False

	@staticmethod
	def SetRegistryValue(key, value, cipher = lambda arg : binascii.b2a_base64(arg)):
		_winreg.CreateKey(_winreg.HKEY_CURRENT_USER, REG_PATH)
		registryHandle = RegistryHandle.Instance().GetRegistryHandle(_winreg.KEY_WRITE)
		if not registryHandle:
			return False

		value = str(value)
		if value == "":
			return RegistryHandle.Instance().DeleteRegistryTree(key)

		value = cipher(value)

		_winreg.SetValueEx(registryHandle, key, 0, _winreg.REG_SZ, value)
		_winreg.CloseKey(registryHandle)
		return True

	@staticmethod
	def GetRegistryValue(key, decipher = lambda arg : binascii.a2b_base64(arg)):
		registryHandle = RegistryHandle.Instance().GetRegistryHandle()
		if not registryHandle:
			return False

		try:
			(value, _) = _winreg.QueryValueEx(registryHandle, key)
			_winreg.CloseKey(registryHandle)
		except WindowsError:
			return False

		if len(value) == 0:
			return False

		value = str(value)
		value = decipher(value)

		return value

	@staticmethod
	def DeleteRegistryTree(name = ""):
		registryHandle = RegistryHandle.Instance().GetRegistryHandle(_winreg.KEY_ALL_ACCESS)
		if not registryHandle:
			return False

		if name != "":
			_winreg.DeleteValue(registryHandle, name)
		else:
			_winreg.DeleteKey(registryHandle, "")

		_winreg.CloseKey(registryHandle)
		return True

	@staticmethod
	def GetRegistryKeys():
		keyList = []

		i = 0
		while True:
			try:
				regKey = RegistryHandle.Instance().GetRegistryHandle()
				if not regKey:
					return tuple(keyList)

				regKey = _winreg.EnumValue(regKey, i)
			except WindowsError:
				return tuple(keyList)

			keyList.append(regKey[0])
			i += 1

		return tuple(keyList)

@Singleton
class AccountHandle:
	def __init__(self):
		self.accountMap = {}
		self.__Initialize()

	def __del__(self):
		self.accountMap = {}

	def __call__(self, index):
		return self.accountMap.get(index)

	def __Initialize(self):
		accountCount = GetWindowConfig("lenght_data", "account")
		for i in range(accountCount):
			value = RegistryHandle.Instance().GetRegistryValue("acc_%d" % i)
			if not value:
				continue

			value = tuple(value.split("|"))

			if GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
				if GetWindowConfig("save_info", "pin"):
					if len(value) != 3:
						continue
			else:
				if len(value) != 2:
					continue

			self.accountMap[i] = value

	def UpdateAccount(self, index, value):
		if len(value) == 0:
			del self.accountMap[index]
			return True

		value = tuple(value.split("|"))
		if GetWindowConfig("miscellaneous", "loginwindow", "enable_pin"):
			if GetWindowConfig("save_info", "pin"):
				if len(value) != 3:
					return False
		else:
			if len(value) != 2:
				return False

		self.accountMap[index] = value
		return True

	def SaveToRegistry(self):
		accountCount = GetWindowConfig("lenght_data", "account")
		for i in range(accountCount):
			regKey = "acc_%d" % i
			oldValue = RegistryHandle.Instance().GetRegistryValue(regKey)
			if not i in self.accountMap:
				if oldValue:
					RegistryHandle.Instance().DeleteRegistryTree(regKey)
				continue

			value = "|".join(self.accountMap[i])
			if oldValue != None:
				if oldValue == value:
					continue

			RegistryHandle.Instance().SetRegistryValue(regKey, value)

	def GetEmptyAccount(self):
		accountCount = GetWindowConfig("lenght_data", "account")
		for i in range(accountCount):
			if not self.accountMap.get(i, None):
				return i

		return -1

@Singleton
class DirectoryHandle:
	MAIN_FOLDER_NAME = "config"
	DIRECTORIES = ("account", "loginwindow", "selectcharacterwindow")

	def Initialize(self):
		if not os.path.exists(self.MAIN_FOLDER_NAME):
			os.makedirs(self.MAIN_FOLDER_NAME)

		for dir in self.DIRECTORIES:
			if not os.path.exists(self.MAIN_FOLDER_NAME + "\\" + dir):
				os.makedirs(self.MAIN_FOLDER_NAME + "\\" + dir)

	def SaveData(self, key, index, value, cipher = None):
		if not key in self.DIRECTORIES:
			return False

		print key,index,value

		value = str(value)

		f = open(self.MAIN_FOLDER_NAME + "\\" + key + "\\" + str(index), "w")
		if cipher:
			value = cipher(value)
		value += '\n'
		f.write(value)
		f.close()
		return True

	def Destroy(self, key, index):
		if not key in self.DIRECTORIES:
			return False

		try:
			os.remove(self.MAIN_FOLDER_NAME + "\\" + key + "\\" + str(index))
			return True
		except WindowsError:
			return False

	def GetEmptyAccount(self):
		accountCount = GetWindowConfig("lenght_data", "account")
		for i in range(accountCount):
			if not os.path.exists(self.MAIN_FOLDER_NAME + "\\" + "account" + "\\" + str(i)):
				break

		return i

	def __call__(self, key, index, cipher = None):
		if not key in self.DIRECTORIES:
			return False

		try:
			fileName = self.MAIN_FOLDER_NAME + "\\" + key + "\\" + str(index)
			f = open(fileName, "r")
			value = f.read()
			if len(value) == 0:
				self.Destroy(key, index)
				return False

			if cipher:
				value = cipher(value)
			value = value.strip()
			f.close()
			return value
		except IOError:
			return False
