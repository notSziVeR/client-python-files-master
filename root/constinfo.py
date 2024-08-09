#-*- coding: iso-8859-1 -*-

import app
import re
import localeInfo

VERSION_ID = 1606802431

SHOW_INTROLOADING = True

if app.ENABLE_AMULET_SYSTEM:
	AMULET_PASSIVE = dict()

EQUIPMENT_LOCK_INFO = {}

CURRENCIE_INIT = False
CURRENCIE_STATE = False

if app.ENABLE_TARGET_MONSTER_LOOT:
	DROP_INFO = {}

if app.ENABLE_TEAMLER_STATUS:
	SET_SHOW_TEAMLER = ""
	IS_SHOW_TEAMLER_VAL = False

SHOPNAMES_RANGE = 4000

GOLD_MAX = 2000000000
CHEQUE_MAX = 999

# EXTRA BEGIN
# loads 5 (B,M,G,P,F) skills .mse
ENABLE_NEW_LEVELSKILL_SYSTEM = 0
# don't set a random channel when you open the client
ENABLE_RANDOM_CHANNEL_SEL = 0
# don't remove id&pass if the login attempt fails
ENABLE_CLEAN_DATA_IF_FAIL_LOGIN = 0
# ctrl+v will now work
ENABLE_PASTE_FEATURE = 0
# display all the bonuses added by a stone instead of the first one
ENABLE_FULLSTONE_DETAILS = 1
# enable successfulness % in the refine dialog
ENABLE_REFINE_PCT = 1
# extra ui features
EXTRA_UI_FEATURE = 1
#
NEW_678TH_SKILL_ENABLE = 0
# EXTRA END

# option
IN_GAME_SHOP_ENABLE = 1
CONSOLE_ENABLE = 0

PVPMODE_ENABLE = 1
PVPMODE_TEST_ENABLE = 0
PVPMODE_ACCELKEY_ENABLE = 1
PVPMODE_ACCELKEY_DELAY = 0.5
PVPMODE_PROTECTED_LEVEL = 15

FOG_LEVEL0 = 4800.0
FOG_LEVEL1 = 9600.0
FOG_LEVEL2 = 12800.0
FOG_LEVEL = FOG_LEVEL0
FOG_LEVEL_LIST=[FOG_LEVEL0, FOG_LEVEL1, FOG_LEVEL2]

CAMERA_MAX_DISTANCE_SHORT = 2500.0
CAMERA_MAX_DISTANCE_LONG = 3500.0
CAMERA_MAX_DISTANCE_LIST=[CAMERA_MAX_DISTANCE_SHORT, CAMERA_MAX_DISTANCE_LONG]
CAMERA_MAX_DISTANCE = CAMERA_MAX_DISTANCE_SHORT

CHRNAME_COLOR_INDEX = 0

ENVIRONMENT_NIGHT="d:/ymir work/environment/moonlight04.msenv"

# constant
HIGH_PRICE = 500000
MIDDLE_PRICE = 50000
ERROR_METIN_STONE = 28960
SUB2_LOADING_ENABLE = 1
EXPANDED_COMBO_ENABLE = 1
CONVERT_EMPIRE_LANGUAGE_ENABLE = 0
USE_ITEM_WEAPON_TABLE_ATTACK_BONUS = 0
ADD_DEF_BONUS_ENABLE = 0
LOGIN_COUNT_LIMIT_ENABLE = 0

USE_SKILL_EFFECT_UPGRADE_ENABLE = 1

VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = 1
GUILD_MONEY_PER_GSP = 100
GUILD_WAR_TYPE_SELECT_ENABLE = 1
TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE = 10

HAIR_COLOR_ENABLE = 1
ARMOR_SPECULAR_ENABLE = 1
WEAPON_SPECULAR_ENABLE = 1
SEQUENCE_PACKET_ENABLE = 1
KEEP_ACCOUNT_CONNETION_ENABLE = 1
MINIMAP_POSITIONINFO_ENABLE = 1

isItemQuestionDialog = 0

def GET_ITEM_QUESTION_DIALOG_STATUS():
	global isItemQuestionDialog
	return isItemQuestionDialog

def SET_ITEM_QUESTION_DIALOG_STATUS(flag):
	global isItemQuestionDialog
	isItemQuestionDialog = flag

import app
import net

########################

def SET_DEFAULT_FOG_LEVEL():
	global FOG_LEVEL
	app.SetMinFog(FOG_LEVEL)

def SET_FOG_LEVEL_INDEX(index):
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	try:
		FOG_LEVEL=FOG_LEVEL_LIST[index]
	except IndexError:
		FOG_LEVEL=FOG_LEVEL_LIST[0]
	app.SetMinFog(FOG_LEVEL)

def GET_FOG_LEVEL_INDEX():
	global FOG_LEVEL
	global FOG_LEVEL_LIST
	return FOG_LEVEL_LIST.index(FOG_LEVEL)

########################

def SET_DEFAULT_CAMERA_MAX_DISTANCE():
	global CAMERA_MAX_DISTANCE
	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def SET_CAMERA_MAX_DISTANCE_INDEX(index):
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	try:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[index]
	except:
		CAMERA_MAX_DISTANCE=CAMERA_MAX_DISTANCE_LIST[0]

	app.SetCameraMaxDistance(CAMERA_MAX_DISTANCE)

def GET_CAMERA_MAX_DISTANCE_INDEX():
	global CAMERA_MAX_DISTANCE
	global CAMERA_MAX_DISTANCE_LIST
	return CAMERA_MAX_DISTANCE_LIST.index(CAMERA_MAX_DISTANCE)

########################

import chrmgr
import player
import app

def SET_DEFAULT_CHRNAME_COLOR():
	global CHRNAME_COLOR_INDEX
	chrmgr.SetEmpireNameMode(CHRNAME_COLOR_INDEX)

def SET_CHRNAME_COLOR_INDEX(index):
	global CHRNAME_COLOR_INDEX
	CHRNAME_COLOR_INDEX=index
	chrmgr.SetEmpireNameMode(index)

def GET_CHRNAME_COLOR_INDEX():
	global CHRNAME_COLOR_INDEX
	return CHRNAME_COLOR_INDEX

def SET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD(index):
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD = index

def GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
	global VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD
	return VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD

def SET_DEFAULT_CONVERT_EMPIRE_LANGUAGE_ENABLE():
	global CONVERT_EMPIRE_LANGUAGE_ENABLE
	net.SetEmpireLanguageMode(CONVERT_EMPIRE_LANGUAGE_ENABLE)

def SET_DEFAULT_USE_ITEM_WEAPON_TABLE_ATTACK_BONUS():
	global USE_ITEM_WEAPON_TABLE_ATTACK_BONUS
	player.SetWeaponAttackBonusFlag(USE_ITEM_WEAPON_TABLE_ATTACK_BONUS)

def SET_DEFAULT_USE_SKILL_EFFECT_ENABLE():
	global USE_SKILL_EFFECT_UPGRADE_ENABLE
	app.SetSkillEffectUpgradeEnable(USE_SKILL_EFFECT_UPGRADE_ENABLE)

def SET_TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE():
	global TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE
	app.SetTwoHandedWeaponAttSpeedDecreaseValue(TWO_HANDED_WEAPON_ATT_SPEED_DECREASE_VALUE)

########################
import item

ACCESSORY_MATERIAL_LIST = [50623, 50624, 50625, 50626, 50627, 50628, 50629, 50630, 50631, 50632, 50633, 50634, 50635, 50636, 50637, 50638, 50639, 50640]
JewelAccessoryInfos = [
		# jewel		perm	wrist	neck	ear
		[ 50628,	150628,		14100,	16100,	17100 ],

		[ 50634,	0,		14420,	16220,	17220 ],
		[ 50635,	0,		14500,	16500,	17500 ],
		[ 50636,	0,		14520,	16520,	17520 ],
		[ 50637,	0,		14540,	16540,	17540 ],
		[ 50638,	0,		14560,	16560,	17560 ],
		[ 50639,	0,		14570,	16570,	17570 ],
		[ 50640,	0,		14580,	16580,	17580 ],
	]

def GET_ACCESSORY_MATERIAL_VNUM(vnum, subType):
	ret = vnum
	item_base = (vnum / 10) * 10
	for info in JewelAccessoryInfos:
		if item.ARMOR_WRIST == subType:
			if info[2] == item_base:
				return (info[0], info[1])
		elif item.ARMOR_NECK == subType:
			if info[3] == item_base:
				return (info[0], info[1])
		elif item.ARMOR_EAR == subType:
			if info[4] == item_base:
				return (info[0], info[1])

	# if vnum >= 16210 and vnum <= 16219:
	# 	return 50625

	# if item.ARMOR_WRIST == subType:
	# 	WRIST_ITEM_VNUM_BASE = 14000
	# 	ret -= WRIST_ITEM_VNUM_BASE
	# elif item.ARMOR_NECK == subType:
	# 	NECK_ITEM_VNUM_BASE = 16000
	# 	ret -= NECK_ITEM_VNUM_BASE
	# elif item.ARMOR_EAR == subType:
	# 	EAR_ITEM_VNUM_BASE = 17000
	# 	ret -= EAR_ITEM_VNUM_BASE

	# type = ret/20

	# if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
	# 	type = (ret-170) / 20
	# 	if type<0 or type>=len(ACCESSORY_MATERIAL_LIST):
	# 		return 0

	# return ACCESSORY_MATERIAL_LIST[type]

##################################################################

def GET_BELT_MATERIAL_VNUM(vnum, subType = 0):
	return 18900

##################################################################

def IS_AUTO_POTION(itemVnum):
	return IS_AUTO_POTION_HP(itemVnum) or IS_AUTO_POTION_SP(itemVnum)

def IS_AUTO_POTION_HP(itemVnum):
	if 72723 <= itemVnum and 72726 >= itemVnum:
		return 1
	elif itemVnum >= 76021 and itemVnum <= 76022:
		return 1
	elif itemVnum == 79012:
		return 1

	return 0

def IS_AUTO_POTION_SP(itemVnum):
	if 72727 <= itemVnum and 72730 >= itemVnum:
		return 1
	elif itemVnum >= 76004 and itemVnum <= 76005:
		return 1
	elif itemVnum == 79013:
		return 1

	return 0

if app.ENABLE_CUBE_RENEWAL:
	ENABLE_CUBE_MARK_MATERIAL = True

ALREADY_NOTIFY_LIST = []

if app.ENABLE_PASSIVE_SKILLS_HELPER:
	PASSIVE_SKILLS_DATA = {}

# if gcGetEnable("ENABLE_SKILLS_INFORMATION"):
SKILL_EXO = 0
SKILL_INFO = {}
SKILL_BOOKS = [
	50401, 50402, 50403, 50404, 50405, 50406, 50416, 50417, 50418,
	50419, 50420, 50421, 50431, 50432, 50433, 50434, 50435, 50436,
	50446, 50447, 50448, 50449, 50450, 50451, 50461, 50462, 50463,
	50464, 50465, 50466, 50476, 50477, 50478, 50479, 50480, 50481,
	50491, 50492, 50493, 50494, 50495, 50496, 50506, 50507, 50508,
	50509, 50510, 50511,
]

LEGENDARY_PASSIVE_INFO = {}

mapSizeDict = {
	"city/metin2_map_a1" : [4, 5],
}

SPECIAL_ITEMS = [
]

COLORED_ITEMS = [

]
def GetItemSpecialColor(itemVnum):
	for fromVnum, toVnum, title, color in SPECIAL_ITEMS:
		if itemVnum >= fromVnum and itemVnum <= toVnum:
			return (title, color)

	return (None, None)

def GetItemTitleColor(itemVnum):
	for fromVnum, toVnum, color in COLORED_ITEMS:
		if itemVnum >= fromVnum and itemVnum <= toVnum:
			return color

	return None

WEB_LINK_REGEX = re.compile("(https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|www\\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\\.[^\\s]{2,}|https?:\\/\\/(?:www\\.|(?!www))[a-zA-Z0-9]+\\.[^\\s]{2,}|www\\.[a-zA-Z0-9]+\\.[^\\s]{2,})")
def WEB_LINK_REPLACE(text):
	global WEB_LINK_REGEX
	links = WEB_LINK_REGEX.findall(text)
	startPos = 0
	for link in links:
		pos = text.find(link, startPos)
		if pos < 0:
			continue

		## replace special characters
		formattedLink = link.replace("\\", "\\\\").replace("|", "\\|")
		linkText = "|cffe85010|Hlink:%s|h%s|h|r" % (formattedLink, formattedLink)
		text = text[:pos] + linkText + text[pos + len(link):]
		startPos = pos + len(linkText)

	return text