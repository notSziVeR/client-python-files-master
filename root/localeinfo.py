"""
	File: py
	Refactored code date: 12.05.2016
	Changes:
		Removed all the code which isn't used like korean characters < bad encoding(editors problem) and more checks.
		Removed over 500 lines unused.
		Removed function mapping(**kwargs) and use constructor of dict > dict(**kwarg) which is same (**kwarg let you take arbitrary number of keyword arguments).
		Removed function CutMoneyString because is used just when locale is HongKong, CIBN.
		Removed check IsYMIR from function LoadLocaleData which load locale as locale/ymir or locale/we_korea.
		Removed GUILD_MARK_NOT_ENOUGH_LEVEL, GUILD_HEADQUARTER, GUILD_FACILITY, GUILD_OBJECT, MAP_TRENT02, MAP_WL, MAP_NUSLUCK, MAP_TREE2,
			LOGIN_FAILURE_WEB_BLOCK, LOGIN_FAILURE_BLOCK_LOGIN, CHANNEL_NOTIFY_FULL, now they're readed directly from locale_game.txt.
		Removed declared global variables.
		Removed checks for declaring LOCALE_FILE_NAME, FN_GM_MARK and use current path.
		Removed korean functions/lists/dictionaries/characters GetAuxiliaryWordType, JOBINFO_DATA_LIST, dictSingleWord, dictDoubleWord, etc.
		Removed unused things: locale mapping, 'all' list etc.
		Removed IN_GAME_SHOP_ENABLE declaration, should be declared inside of constInfo directly.
		Removed checks (locale path) - 949, 932 == app.GetDefaultCodePage(), IsHONGKONG, IsNEWCIBN() or IsCIBN10() from declaration of functions like (NumberToMoneyString, NumberToSecondaryCoinString, ...),
			now they're declared directly from old style (IsEUROPE() and not IsWE_KOREA() and not IsYMIR()).

		Added custom string format(format_string, *args, **kwargs) instead of %. (old-style).
		Added new checks inside of LoadLocaleFile for security:
			* Check if token3 (token1=original_string, token2=return-string, token3=function) function name exist in our types (SA, SNA, SAA, SAN) then try to call it.
			* Check if string line have no tabs.
"""

import app
import constInfo
import dbg
import colorInfo

APP_GET_LOCALE_PATH					= app.GetLocalePath()
APP_GET_LOCALE_SERVICE_NAME 		= app.GetLocaleServiceName()

APP_TITLE 							= 'Xamia'

BLEND_POTION_NO_TIME 				= 'BLEND_POTION_NO_TIME'
BLEND_POTION_NO_INFO				= 'BLEND_POTION_NO_INFO'

LOGIN_FAILURE_WRONG_SOCIALID 		= 'LOGIN_FAILURE_WRONG_SOCIALID'
LOGIN_FAILURE_SHUTDOWN_TIME 		= 'LOGIN_FAILURE_SHUTDOWN_TIME'

GUILD_MEMBER_COUNT_INFINITY 		= 'INFINITY'
GUILD_MARK_MIN_LEVEL 				= '3'
GUILD_BUILDING_LIST_TXT 			= '{:s}/GuildBuildingList.txt'.format(APP_GET_LOCALE_PATH)
FN_GM_MARK 							= "locale/common/effect/gm.mse"

MAP_TREE2 							= 'MAP_TREE2'

ERROR_MARK_UPLOAD_NEED_RECONNECT	= 'UploadMark: Reconnect to game'
ERROR_MARK_CHECK_NEED_RECONNECT		= 'CheckMark: Reconnect to game'

VIRTUAL_KEY_ALPHABET_LOWERS			= r"[1234567890]/qwertyuiop\=asdfghjkl;`'zxcvbnm.,"
VIRTUAL_KEY_ALPHABET_UPPERS			= r"{1234567890}?QWERTYUIOP|+ASDFGHJKL:~'ZXCVBNM<>"
VIRTUAL_KEY_SYMBOLS    				= "!@#$%^&*()_+|{}:'<>?~"
VIRTUAL_KEY_NUMBERS					= "1234567890-=\[];',./`"
VIRTUAL_KEY_SYMBOLS_BR 				= '!@#$%^&*()_+|{}:"<>?~????????????????'

SHOP_TYPE_MONEY = "|Eemoticons/tooltip/money|e"
SHOP_TYPE_MONEY_SMALL = "|Eemoticons/tooltip/money_small|e"
SHOP_TYPE_CHEQUE = "|Eemoticons/tooltip/won|e"

# Localization
def GetLocalePath():
	return app.GetLocalePath()

def LoadLocaleData():
	app.LoadLocaleData(GetLocalePath())

# Load locale_game.txt
def SNA(text):
	def f(x):
		return text
	return f

def SA(text):
	def f(x):
		if x == None:
			return text
		else:
			return text % x
	return f

def LoadLocaleFile(srcFileName, localeDict):
	funcDict = {"SA":SA, "SNA":SNA}

	lineIndex = 1

	try:
		lines = open(srcFileName, "r").readlines()
	except IOError:
		import dbg
		dbg.LogBox("LoadLocaleError(%(srcFileName)s)" % locals())
		app.Abort()

	for line in lines:
		try:
			if len(line.strip()) == 0:
				continue

			tokens = line[:-1].split("\t")
			if len(tokens) == 2:
				localeDict[tokens[0]] = tokens[1]
			elif len(tokens) >= 3:
				type = tokens[2].strip()
				if type:
					localeDict[tokens[0]] = funcDict[type](tokens[1])
				else:
					localeDict[tokens[0]] = tokens[1]
			else:
				raise RuntimeError, "Unknown TokenSize"

			lineIndex += 1
		except:
			import dbg
			dbg.LogBox("%s: line(%d): %s" % (srcFileName, lineIndex, line), "Error")
			raise

def GetLocals(name):
	return locals()[name]

LoadLocaleFile("{:s}/locale_game.txt".format(APP_GET_LOCALE_PATH), locals())
LoadLocaleFile("{:s}/locale_game_new.txt".format(APP_GET_LOCALE_PATH), locals())

# Option pvp messages
OPTION_PVPMODE_MESSAGE_DICT = {
	0: PVP_MODE_NORMAL,
	1: PVP_MODE_REVENGE,
	2: PVP_MODE_KILL,
	3: PVP_MODE_PROTECT,
	4: PVP_MODE_GUILD,
}

# Whisper messages
if app.OFFLINE_MESSAGE_ENABLE:
	WHISPER_ERROR = {
		1 : CANNOT_WHISPER_NOT_LOGON2,
		2 : CANNOT_WHISPER_DEST_REFUSE,
		3 : CANNOT_WHISPER_SELF_REFUSE,
		6 : WHISPER_MESSAGE_GONE,
		7 : WHISPER_LIMIT_REACHED,
		8 : WHISPER_PLAYER_NOT_EXIST,
	}
else:
	WHISPER_ERROR = {
		1: CANNOT_WHISPER_NOT_LOGON,
		2: CANNOT_WHISPER_DEST_REFUSE,
		3: CANNOT_WHISPER_SELF_REFUSE,
	}

# Exception of graphic device.
error = dict(
	CREATE_WINDOW = GAME_INIT_ERROR_MAIN_WINDOW,
	CREATE_CURSOR = GAME_INIT_ERROR_CURSOR,
	CREATE_NETWORK = GAME_INIT_ERROR_NETWORK,
	CREATE_ITEM_PROTO = GAME_INIT_ERROR_ITEM_PROTO,
	CREATE_MOB_PROTO = GAME_INIT_ERROR_MOB_PROTO,
	CREATE_NO_DIRECTX = GAME_INIT_ERROR_DIRECTX,
	CREATE_DEVICE = GAME_INIT_ERROR_GRAPHICS_NOT_EXIST,
	CREATE_NO_APPROPRIATE_DEVICE = GAME_INIT_ERROR_GRAPHICS_BAD_PERFORMANCE,
	CREATE_FORMAT = GAME_INIT_ERROR_GRAPHICS_NOT_SUPPORT_32BIT,
	NO_ERROR = str()
)

# Job information (none, skill_group1, skill_group2)
JOBINFO_TITLE = [
	[JOB_WARRIOR0, JOB_WARRIOR1, JOB_WARRIOR2,],
	[JOB_ASSASSIN0, JOB_ASSASSIN1, JOB_ASSASSIN2,],
	[JOB_SURA0, JOB_SURA1, JOB_SURA2,],
	[JOB_SHAMAN0, JOB_SHAMAN1, JOB_SHAMAN2,],
]

#if app.ENABLE_WOLFMAN_CHARACTER:
	#JOBINFO_TITLE += [[JOB_WOLFMAN0,JOB_WOLFMAN1,JOB_WOLFMAN2,],]

# Guild war description
GUILDWAR_NORMAL_DESCLIST = 					(GUILD_WAR_USE_NORMAL_MAP, GUILD_WAR_LIMIT_30MIN, GUILD_WAR_WIN_CHECK_SCORE)
# Guild war warp description
GUILDWAR_WARP_DESCLIST = 					(GUILD_WAR_USE_BATTLE_MAP, GUILD_WAR_WIN_WIPE_OUT_GUILD, GUILD_WAR_REWARD_POTION)
# Guild war flag description
GUILDWAR_CTF_DESCLIST = 					(GUILD_WAR_USE_BATTLE_MAP, GUILD_WAR_WIN_TAKE_AWAY_FLAG1, GUILD_WAR_WIN_TAKE_AWAY_FLAG2, GUILD_WAR_REWARD_POTION)

# Mode of pvp options
MODE_NAME_LIST = 							(PVP_OPTION_NORMAL, PVP_OPTION_REVENGE, PVP_OPTION_KILL, PVP_OPTION_PROTECT,)
# Title name of alignment
TITLE_NAME_LIST = 							(PVP_LEVEL0, PVP_LEVEL1, PVP_LEVEL2, PVP_LEVEL3, PVP_LEVEL4, PVP_LEVEL5, PVP_LEVEL6, PVP_LEVEL7, PVP_LEVEL8,)

# Horse levels
LEVEL_LIST = 								(str(), HORSE_LEVEL1, HORSE_LEVEL2, HORSE_LEVEL3)
# Horse health
HEALTH_LIST = 								(HORSE_HEALTH0, HORSE_HEALTH1, HORSE_HEALTH2, HORSE_HEALTH3)

# Use-skill messages
USE_SKILL_ERROR_TAIL_DICT = {
	'IN_SAFE':								CANNOT_SKILL_SELF_IN_SAFE,
	'NEED_TARGET': 							CANNOT_SKILL_NEED_TARGET,
	'NEED_EMPTY_BOTTLE': 					CANNOT_SKILL_NEED_EMPTY_BOTTLE,
	'NEED_POISON_BOTTLE': 					CANNOT_SKILL_NEED_POISON_BOTTLE,
	'REMOVE_FISHING_ROD': 					CANNOT_SKILL_REMOVE_FISHING_ROD,
	'NOT_YET_LEARN': 						CANNOT_SKILL_NOT_YET_LEARN,
	'NOT_MATCHABLE_WEAPON':					CANNOT_SKILL_NOT_MATCHABLE_WEAPON,
	'WAIT_COOLTIME':						CANNOT_SKILL_WAIT_COOLTIME,
	'NOT_ENOUGH_HP':						CANNOT_SKILL_NOT_ENOUGH_HP,
	'NOT_ENOUGH_SP':						CANNOT_SKILL_NOT_ENOUGH_SP,
	'CANNOT_USE_SELF':						CANNOT_SKILL_USE_SELF,
	'ONLY_FOR_ALLIANCE': 					CANNOT_SKILL_ONLY_FOR_ALLIANCE,
	'CANNOT_ATTACK_ENEMY_IN_SAFE_AREA':		CANNOT_SKILL_DEST_IN_SAFE,
	'CANNOT_APPROACH':						CANNOT_SKILL_APPROACH,
	'CANNOT_ATTACK':						CANNOT_SKILL_ATTACK,
	'ONLY_FOR_CORPSE':						CANNOT_SKILL_ONLY_FOR_CORPSE,
	'EQUIP_FISHING_ROD':					CANNOT_SKILL_EQUIP_FISHING_ROD,
	'NOT_HORSE_SKILL':						CANNOT_SKILL_NOT_HORSE_SKILL,
	'HAVE_TO_RIDE':							CANNOT_SKILL_HAVE_TO_RIDE,
}

# Notify messages
NOTIFY_MESSAGE = {
	'CANNOT_EQUIP_SHOP': 					CANNOT_EQUIP_IN_SHOP,
	'CANNOT_EQUIP_EXCHANGE': 				CANNOT_EQUIP_IN_EXCHANGE,
}

# Attack messages
ATTACK_ERROR_TAIL_DICT = {
	'IN_SAFE': 								CANNOT_ATTACK_SELF_IN_SAFE,
	'DEST_IN_SAFE': 						CANNOT_ATTACK_DEST_IN_SAFE,
}

# Shot messages
SHOT_ERROR_TAIL_DICT = {
	'EMPTY_ARROW': 							CANNOT_SHOOT_EMPTY_ARROW,
	'IN_SAFE':								CANNOT_SHOOT_SELF_IN_SAFE,
	'DEST_IN_SAFE':							CANNOT_SHOOT_DEST_IN_SAFE,
}

# Skill messages
USE_SKILL_ERROR_CHAT_DICT = {
	'NEED_EMPTY_BOTTLE': 					SKILL_NEED_EMPTY_BOTTLE,
	'NEED_POISON_BOTTLE': 					SKILL_NEED_POISON_BOTTLE,
	'ONLY_FOR_GUILD_WAR': 					SKILL_ONLY_FOR_GUILD_WAR,
}

# Shop/private-shop messages
SHOP_ERROR_DICT = {
	'NOT_ENOUGH_MONEY': 					SHOP_NOT_ENOUGH_MONEY + " " + SHOP_TYPE_MONEY,
	'SOLDOUT': 								SHOP_SOLDOUT,
	'INVENTORY_FULL': 						SHOP_INVENTORY_FULL,
	'INVALID_POS': 							SHOP_INVALID_POS,
	'NOT_ENOUGH_MONEY_EX': 					SHOP_NOT_ENOUGH_MONEY_EX,
	'NOT_ENOUGH_ITEM_EX':					SHOP_NOT_ENOUGH_ITEM_EX,
}

# Character status description
STAT_MINUS_DESCRIPTION = {
	'HTH-': 								STAT_MINUS_CON,
	'INT-': 								STAT_MINUS_INT,
	'STR-': 								STAT_MINUS_STR,
	'DEX-': 								STAT_MINUS_DEX,
}

STAT_IMAGE_DESCRIPTION = {
	"HTH" : STAT_TOOLTIP_IMG_CON,
	"INT" : STAT_TOOLTIP_IMG_INT,
	"STR" : STAT_TOOLTIP_IMG_STR,
	"DEX" : STAT_TOOLTIP_IMG_DEX,
}

STAT_IMAGE_MAIN_DESCRIPTION = {
	"VIDA" : STAT_TOOLTIP_HP,
	"MANA" : STAT_TOOLTIP_SP,
	"VATAQUE" : STAT_TOOLTIP_ATT,
	"DEFESA" : STAT_TOOLTIP_DEF,
}

STAT_IMAGE_OTHER_DESCRIPTION = {
	"MSPD" : STAT_TOOLTIP_MOVE_SPEED,
	"ASPD" : STAT_TOOLTIP_ATT_SPEED,
	"CSPD" : STAT_TOOLTIP_CAST_SPEED,
	"MATT" : STAT_TOOLTIP_MAG_ATT,
	"MDEF" : STAT_TOOLTIP_MAG_DEF,
	"ER" : STAT_TOOLTIP_DODGE_PER,
}

# SKILL_PAGE_IMAGE_INFO_DESC = {
# 	"ACTIVE_SKILL_POINTS" : ACTIVE_SKILL_POINTS,

# 	"HORSE_SKILL_TOOLTIP" : HORSE_SKILL_TOOLTIP,
# 	"HORSE_SKILL_POINTS" : HORSE_SKILL_POINTS,

# 	"PASSIVE_SKILL_TOOLTIP" : PASSIVE_SKILL_TOOLTIP,

# 	"SUP_SKILL_TOOLTIP" : SUP_SKILL_TOOLTIP,
# }

EMOTICON_PAGE_IMAGE_INFO_DESC = {
	"NORMAL_EMOTION " : STAT_TOOLTIP_STANDARD_ACTION,
	"DUO_EMOTION " : STAT_TOOLTIP_STANDARD_DUO,
	"SPECIAL_EMOTION " : STAT_TOOLTIP_SPECIAL_ACTION,
}

# Map names
MINIMAP_ZONE_NAME_DICT = {
	'city/metin2_map_a1': 						MAP_A1,
	'map_a2': 								MAP_A2,
	'city/metin2_map_a3': 						MAP_A3,
	'metin2_map_b1': 						MAP_B1,
	'map_b2': 								MAP_B2,
	'metin2_map_b3': 						MAP_B3,
	'metin2_map_c1': 						MAP_C1,
	'map_c2': 								MAP_C2,
	'metin2_map_c3': 						MAP_C3,
	'map_n_snowm_01': 						MAP_SNOW,
	'metin2_map_n_flame_01': 				MAP_FLAME,
	'metin2_map_n_desert_01': 				MAP_DESERT,
	'metin2_map_milgyo': 					MAP_TEMPLE,
	'metin2_map_spiderdungeon': 			MAP_SPIDER,
	'metin2_map_deviltower1': 				MAP_SKELTOWER,
	'metin2_map_guild_01': 					MAP_AG,
	'metin2_map_guild_02': 					MAP_BG,
	'metin2_map_guild_03': 					MAP_CG,
	'metin2_map_trent': 					MAP_TREE,
	'metin2_map_trent02': 					MAP_TREE2,
	'season1/metin2_map_WL_01': 			MAP_WL,
	'season1/metin2_map_nusluck01': 		MAP_NUSLUCK,
    'Metin2_map_CapeDragonHead': 			MAP_CAPE,
    'metin2_map_Mt_Thunder': 				MAP_THUNDER,
    'metin2_map_dawnmistwood': 				MAP_DAWN,
    'metin2_map_BayBlackSand': 				MAP_BAY,
}

import item
AFFECT_DICT = {
	item.APPLY_MAX_HP : TOOLTIP_MAX_HP,
	item.APPLY_MAX_SP : TOOLTIP_MAX_SP,
	item.APPLY_CON : TOOLTIP_CON,
	item.APPLY_INT : TOOLTIP_INT,
	item.APPLY_STR : TOOLTIP_STR,
	item.APPLY_DEX : TOOLTIP_DEX,
	item.APPLY_ATT_SPEED : TOOLTIP_ATT_SPEED,
	item.APPLY_MOV_SPEED : TOOLTIP_MOV_SPEED,
	item.APPLY_CAST_SPEED : TOOLTIP_CAST_SPEED,
	item.APPLY_HP_REGEN : TOOLTIP_HP_REGEN,
	item.APPLY_SP_REGEN : TOOLTIP_SP_REGEN,
	item.APPLY_POISON_PCT : TOOLTIP_APPLY_POISON_PCT,
	item.APPLY_STUN_PCT : TOOLTIP_APPLY_STUN_PCT,
	item.APPLY_SLOW_PCT : TOOLTIP_APPLY_SLOW_PCT,
	item.APPLY_CRITICAL_PCT : TOOLTIP_APPLY_CRITICAL_PCT,
	item.APPLY_PENETRATE_PCT : TOOLTIP_APPLY_PENETRATE_PCT,

	item.APPLY_ATTBONUS_WARRIOR : TOOLTIP_APPLY_ATTBONUS_WARRIOR,
	item.APPLY_ATTBONUS_ASSASSIN : TOOLTIP_APPLY_ATTBONUS_ASSASSIN,
	item.APPLY_ATTBONUS_SURA : TOOLTIP_APPLY_ATTBONUS_SURA,
	item.APPLY_ATTBONUS_SHAMAN : TOOLTIP_APPLY_ATTBONUS_SHAMAN,
	item.APPLY_ATTBONUS_MONSTER : TOOLTIP_APPLY_ATTBONUS_MONSTER,

	item.APPLY_ATTBONUS_HUMAN : TOOLTIP_APPLY_ATTBONUS_HUMAN,
	item.APPLY_ATTBONUS_ANIMAL : TOOLTIP_APPLY_ATTBONUS_ANIMAL,
	item.APPLY_ATTBONUS_ORC : TOOLTIP_APPLY_ATTBONUS_ORC,
	item.APPLY_ATTBONUS_MILGYO : TOOLTIP_APPLY_ATTBONUS_MILGYO,
	item.APPLY_ATTBONUS_UNDEAD : TOOLTIP_APPLY_ATTBONUS_UNDEAD,
	item.APPLY_ATTBONUS_DEVIL : TOOLTIP_APPLY_ATTBONUS_DEVIL,
	item.APPLY_STEAL_HP : TOOLTIP_APPLY_STEAL_HP,
	item.APPLY_STEAL_SP : TOOLTIP_APPLY_STEAL_SP,
	item.APPLY_MANA_BURN_PCT : TOOLTIP_APPLY_MANA_BURN_PCT,
	item.APPLY_DAMAGE_SP_RECOVER : TOOLTIP_APPLY_DAMAGE_SP_RECOVER,
	item.APPLY_BLOCK : TOOLTIP_APPLY_BLOCK,
	item.APPLY_DODGE : TOOLTIP_APPLY_DODGE,
	item.APPLY_RESIST_SWORD : TOOLTIP_APPLY_RESIST_SWORD,
	item.APPLY_RESIST_TWOHAND : TOOLTIP_APPLY_RESIST_TWOHAND,
	item.APPLY_RESIST_DAGGER : TOOLTIP_APPLY_RESIST_DAGGER,
	item.APPLY_RESIST_BELL : TOOLTIP_APPLY_RESIST_BELL,
	item.APPLY_RESIST_FAN : TOOLTIP_APPLY_RESIST_FAN,
	item.APPLY_RESIST_BOW : TOOLTIP_RESIST_BOW,
	item.APPLY_RESIST_FIRE : TOOLTIP_RESIST_FIRE,
	item.APPLY_RESIST_ELEC : TOOLTIP_RESIST_ELEC,
	item.APPLY_RESIST_MAGIC : TOOLTIP_RESIST_MAGIC,
	item.APPLY_RESIST_WIND : TOOLTIP_APPLY_RESIST_WIND,
	item.APPLY_REFLECT_MELEE : TOOLTIP_APPLY_REFLECT_MELEE,
	item.APPLY_REFLECT_CURSE : TOOLTIP_APPLY_REFLECT_CURSE,
	item.APPLY_POISON_REDUCE : TOOLTIP_APPLY_POISON_REDUCE,
	item.APPLY_KILL_SP_RECOVER : TOOLTIP_APPLY_KILL_SP_RECOVER,
	item.APPLY_EXP_DOUBLE_BONUS : TOOLTIP_APPLY_EXP_DOUBLE_BONUS,
	item.APPLY_GOLD_DOUBLE_BONUS : TOOLTIP_APPLY_GOLD_DOUBLE_BONUS,
	item.APPLY_ITEM_DROP_BONUS : TOOLTIP_APPLY_ITEM_DROP_BONUS,
	item.APPLY_POTION_BONUS : TOOLTIP_APPLY_POTION_BONUS,
	item.APPLY_KILL_HP_RECOVER : TOOLTIP_APPLY_KILL_HP_RECOVER,
	item.APPLY_IMMUNE_STUN : TOOLTIP_APPLY_IMMUNE_STUN,
	item.APPLY_IMMUNE_SLOW : TOOLTIP_APPLY_IMMUNE_SLOW,
	item.APPLY_IMMUNE_FALL : TOOLTIP_APPLY_IMMUNE_FALL,
	item.APPLY_BOW_DISTANCE : TOOLTIP_BOW_DISTANCE,
	item.APPLY_DEF_GRADE_BONUS : TOOLTIP_DEF_GRADE,
	item.APPLY_ATT_GRADE_BONUS : TOOLTIP_ATT_GRADE,
	item.APPLY_MAGIC_ATT_GRADE : TOOLTIP_MAGIC_ATT_GRADE,
	item.APPLY_MAGIC_DEF_GRADE : TOOLTIP_MAGIC_DEF_GRADE,
	item.APPLY_MAX_STAMINA : TOOLTIP_MAX_STAMINA,
	item.APPLY_MALL_ATTBONUS : TOOLTIP_MALL_ATTBONUS,
	item.APPLY_MALL_DEFBONUS : TOOLTIP_MALL_DEFBONUS,
	item.APPLY_MALL_EXPBONUS : TOOLTIP_MALL_EXPBONUS,
	item.APPLY_MALL_ITEMBONUS : TOOLTIP_MALL_ITEMBONUS,
	item.APPLY_MALL_GOLDBONUS : TOOLTIP_MALL_GOLDBONUS,
	item.APPLY_SKILL_DAMAGE_BONUS : TOOLTIP_SKILL_DAMAGE_BONUS,
	item.APPLY_NORMAL_HIT_DAMAGE_BONUS : TOOLTIP_NORMAL_HIT_DAMAGE_BONUS,
	item.APPLY_SKILL_DEFEND_BONUS : TOOLTIP_SKILL_DEFEND_BONUS,
	item.APPLY_NORMAL_HIT_DEFEND_BONUS : TOOLTIP_NORMAL_HIT_DEFEND_BONUS,
	item.APPLY_PC_BANG_EXP_BONUS : TOOLTIP_MALL_EXPBONUS_P_STATIC,
	item.APPLY_PC_BANG_DROP_BONUS : TOOLTIP_MALL_ITEMBONUS_P_STATIC,
	item.APPLY_RESIST_WARRIOR : TOOLTIP_APPLY_RESIST_WARRIOR,
	item.APPLY_RESIST_ASSASSIN : TOOLTIP_APPLY_RESIST_ASSASSIN,
	item.APPLY_RESIST_SURA : TOOLTIP_APPLY_RESIST_SURA,
	item.APPLY_RESIST_SHAMAN : TOOLTIP_APPLY_RESIST_SHAMAN,
	item.APPLY_MAX_HP_PCT : TOOLTIP_APPLY_MAX_HP_PCT,
	item.APPLY_MAX_SP_PCT : TOOLTIP_APPLY_MAX_SP_PCT,
	item.APPLY_ENERGY : TOOLTIP_ENERGY,
	item.APPLY_COSTUME_ATTR_BONUS : TOOLTIP_COSTUME_ATTR_BONUS,

	item.APPLY_MAGIC_ATTBONUS_PER : TOOLTIP_MAGIC_ATTBONUS_PER,
	item.APPLY_MELEE_MAGIC_ATTBONUS_PER : TOOLTIP_MELEE_MAGIC_ATTBONUS_PER,
	item.APPLY_RESIST_ICE : TOOLTIP_RESIST_ICE,
	item.APPLY_RESIST_EARTH : TOOLTIP_RESIST_EARTH,
	item.APPLY_RESIST_DARK : TOOLTIP_RESIST_DARK,
	item.APPLY_ANTI_CRITICAL_PCT : TOOLTIP_ANTI_CRITICAL_PCT,
	item.APPLY_ANTI_PENETRATE_PCT : TOOLTIP_ANTI_PENETRATE_PCT,

	item.APPLY_DAMAGE_PERCENTAGE : TOOLTIP_DAMAGE_PERCENTAGE_PCT,
}
if app.ENABLE_WOLFMAN_CHARACTER:
	AFFECT_DICT.update({
		item.APPLY_BLEEDING_PCT : TOOLTIP_APPLY_BLEEDING_PCT,
		item.APPLY_BLEEDING_REDUCE : TOOLTIP_APPLY_BLEEDING_REDUCE,
		item.APPLY_ATTBONUS_WOLFMAN : TOOLTIP_APPLY_ATTBONUS_WOLFMAN,
		item.APPLY_RESIST_CLAW : TOOLTIP_APPLY_RESIST_CLAW,
		item.APPLY_RESIST_WOLFMAN : TOOLTIP_APPLY_RESIST_WOLFMAN,
	})

if app.ENABLE_MAGIC_REDUCTION_SYSTEM:
	AFFECT_DICT.update({
		item.APPLY_RESIST_MAGIC_REDUCTION : TOOLTIP_RESIST_MAGIC_REDUCTION,
	})

if app.ENABLE_12ZI_ELEMENT_ADD:
	AFFECT_DICT.update({
		item.APPLY_ENCHANT_ELECT  : TOOLTIP_APPLY_ENCHANT_ELECT,
		item.APPLY_ENCHANT_FIRE   : TOOLTIP_APPLY_ENCHANT_FIRE,
		item.APPLY_ENCHANT_ICE    : TOOLTIP_APPLY_ENCHANT_ICE,
		item.APPLY_ENCHANT_WIND   : TOOLTIP_APPLY_ENCHANT_WIND,
		item.APPLY_ENCHANT_EARTH  : TOOLTIP_APPLY_ENCHANT_EARTH,
		item.APPLY_ENCHANT_DARK   : TOOLTIP_APPLY_ENCHANT_DARK,
		item.APPLY_ATTBONUS_CZ    : TOOLTIP_APPLY_ATTBONUS_CZ,
		item.APPLY_ATTBONUS_INSECT: TOOLTIP_APPLY_ATTBONUS_INSECT,
		item.APPLY_ATTBONUS_DESERT: TOOLTIP_APPLY_ATTBONUS_DESERT,
	})

AFFECT_DICT.update({
	item.APPLY_RESIST_ALL : TOOLTIP_APPLY_RESIST_ALL,
	item.APPLY_ATTBONUS_METIN : TOOLTIP_APPLY_ATTBONUS_METIN,
	item.APPLY_ATTBONUS_BOSS : TOOLTIP_APPLY_ATTBONUS_BOSS,
	item.APPLY_RESIST_MONSTER : TOOLTIP_APPLY_RESIST_MONSTER,
	item.APPLY_RESIST_BOSS : TOOLTIP_APPLY_RESIST_BOSS,
})

AFFECT_DICT.update({
	item.APPLY_PRECISION : TOOLTIP_PRECISION,
		item.APPLY_DUNGEON_DAMAGE_BONUS : TOOLTIP_APPLY_DUNGEON_DAMAGE_BONUS,
		item.APPLY_DUNGEON_RECV_DAMAGE_BONUS : TOOLTIP_APPLY_DUNGEON_RECV_DAMAGE_BONUS,
		item.APPLY_AGGRO_MONSTER_BONUS : TOOLTIP_APPLY_AGGRO_MONSTER_BONUS,
		item.APPLY_DOUBLE_ITEM_DROP_BONUS : TOOLTIP_APPLY_DOUBLE_ITEM_DROP_BONUS,
})

RACE_FLAG_BONUSES = {
	1 << 0	: item.GetApplyPoint(item.APPLY_ATTBONUS_ANIMAL),
	1 << 1	: item.GetApplyPoint(item.APPLY_ATTBONUS_UNDEAD),
	1 << 2	: item.GetApplyPoint(item.APPLY_ATTBONUS_DEVIL),
	1 << 3	: item.GetApplyPoint(item.APPLY_ATTBONUS_HUMAN),
	1 << 4	: item.GetApplyPoint(item.APPLY_ATTBONUS_ORC),
	1 << 5	: item.GetApplyPoint(item.APPLY_ATTBONUS_MILGYO),

	1 << 11 : [item.APPLY_ENCHANT_ELECT, item.APPLY_RESIST_ELEC],
	1 << 12 : [item.APPLY_ENCHANT_FIRE, item.APPLY_RESIST_FIRE],
	1 << 13 : [item.APPLY_ENCHANT_ICE, item.APPLY_RESIST_ICE],
	1 << 14 : [item.APPLY_ENCHANT_WIND, item.APPLY_RESIST_WIND],
	1 << 15 : [item.APPLY_ENCHANT_EARTH, item.APPLY_RESIST_EARTH],
	1 << 16 : [item.APPLY_ENCHANT_DARK, item.APPLY_RESIST_DARK],
}

RACE_FLAG_TO_NAME = {
	1 << 0	: MOB_RACEFLAG_ANIMAL,
	1 << 1	: MOB_RACEFLAG_UNDEAD,
	1 << 2	: MOB_RACEFLAG_DEVIL,
	1 << 3	: MOB_RACEFLAG_HUMAN,
	1 << 4	: MOB_RACEFLAG_ORC,
	1 << 5	: MOB_RACEFLAG_MISTIC,
}

SUB_RACE_FLAG_TO_NAME = {
	1 << 11 : MOB_RACEFLAG_ELEMENT_ELEC,
	1 << 12 : MOB_RACEFLAG_ELEMENT_FIRE,
	1 << 13 : MOB_RACEFLAG_ELEMENT_ICE,
	1 << 14 : MOB_RACEFLAG_ELEMENT_WIND,
	1 << 15 : MOB_RACEFLAG_ELEMENT_EARTH,
	1 << 16 : MOB_RACEFLAG_ELEMENT_DARK,
}


STAT_MINUS_DESCRIPTION = {
	"HTH-" : STAT_MINUS_CON,
	"INT-" : STAT_MINUS_INT,
	"STR-" : STAT_MINUS_STR,
	"DEX-" : STAT_MINUS_DEX,
}

STAT_IMAGE_DESCRIPTION = {
	"HTH" : STAT_TOOLTIP_IMG_CON,
	"INT" : STAT_TOOLTIP_IMG_INT,
	"STR" : STAT_TOOLTIP_IMG_STR,
	"DEX" : STAT_TOOLTIP_IMG_DEX,
}

STAT_IMAGE_MAIN_DESCRIPTION = {
	"VIDA" : STAT_TOOLTIP_HP,
	"MANA" : "STAT_TOOLTIP_MN",
	"VATAQUE" : "STAT_TOOLTIP_VATAQUE",
	"DEFESA" : "STAT_TOOLTIP_DEFESA",
}

STAT_IMAGE_OTHER_DESCRIPTION = {
	"MSPD" : "STAT_TOOLTIP_MSPD",
	"ASPD" : "STAT_TOOLTIP_ASPD",
	"CSPD" : "STAT_TOOLTIP_CSPD",
	"MATT" : "STAT_TOOLTIP_MATT",
	"MDEF" : "STAT_TOOLTIP_MDEF",
	"ER" : "STAT_TOOLTIP_ER",
}

STATE_IMAGE_OTHER_INFO_DESC = {
	"STAT_TITLE" : "STAT_TITLE_TOOLTIP",
	"AVAIBLE_STAT_POINT" : "STAT_AVAIBLE_STAT_POINT_TOOLTIP",
}

SKILL_PAGE_IMAGE_INFO_DESC = {
	"ACTIVE_SKILL_POINTS" : "ACTIVE_SKILL_POINTS",

	"HORSE_SKILL_TOOLTIP" : "HORSE_SKILL_TOOLTIP",
	"HORSE_SKILL_POINTS" : "HORSE_SKILL_POINTS",

	"PASSIVE_SKILL_TOOLTIP" : "PASSIVE_SKILL_TOOLTIP",

	"SUP_SKILL_TOOLTIP" : "SUP_SKILL_TOOLTIP",
}

EMOTICON_PAGE_IMAGE_INFO_DESC = {
	"NORMAL_EMOTION " : "NORMAL_EMOTION_TOOLTIP",
	"DUO_EMOTION " : "DUO_EMOTION_TOOLTIP",
	"SPECIAL_EMOTION " : "SPECIAL_EMOTION_TOOLTIP",
}

# Path of quest icon file
def GetLetterImageName():
	return "season1/icon/scroll_close.tga"

def GetLetterOpenImageName():
	return "season1/icon/scroll_open.tga"

def GetLetterCloseImageName():
	return "season1/icon/scroll_close.tga"

# Sell item question
def DO_YOU_SELL_ITEM(sellItemName, sellItemCount, sellItemPrice):
	if sellItemCount > 1 :
		return SELL_ITEM_02 % ("|cFFf2e8c2" + sellItemName + "|r", sellItemCount, NumberToStringAsType(sellItemPrice, True, ""))
	else:
		return SELL_ITEM_01 % ("|cFFf2e8c2" + sellItemName + "|r", NumberToStringAsType(sellItemPrice, True, ""))

# Buy item question
def DO_YOU_BUY_ITEM(buyItemName, buyItemCount, buyItemPrice):
	if buyItemCount > 1 :
		return BUY_ITEM_02 % ("|cFFf2e8c2" + buyItemName + "|r", buyItemCount, NumberToStringAsType(buyItemPrice, True, ""))
	else:
		return BUY_ITEM_01 % ("|cFFf2e8c2" + buyItemName + "|r", NumberToStringAsType(buyItemPrice, True, ""))

if app.INGAME_ITEMSHOP_ENABLE:
	def DO_YOU_BUY_ITEM_FROM_ITEMSHOP(buyItemName, buyItemCount, buyItemPrice) :
		if buyItemCount > 1 :
			return DO_YOU_BUY_ITEM2_FROM_ITEMSHOP % ( buyItemName, buyItemCount, buyItemPrice )
		else:
			return DO_YOU_BUY_ITEM1_FROM_ITEMSHOP % ( buyItemName, buyItemPrice )

def DO_YOU_BUY_ITEM_FOR_ITEM(buyItemName, buyItemCount, itemVnumPrice, itemVnumPriceName):
	if buyItemCount > 1 :
		return BUY_ITEM_FOR_ITEM_02 % ("|cFFf2e8c2" + buyItemName + "|r", buyItemCount, itemVnumPrice, "|cFFf2e8c2" + itemVnumPriceName + "|r")
	else:
		return BUY_ITEM_FOR_ITEM_01 % ("|cFFf2e8c2" + buyItemName + "|r", itemVnumPrice, "|cFFf2e8c2" + itemVnumPriceName + "|r")

# Notify when you can't attach a specific item.
def REFINE_FAILURE_CAN_NOT_ATTACH(attachedItemName):
	return REFINE_FAILURE_CAN_NOT_ATTACH0 % (attachedItemName)

def REFINE_FAILURE_NO_SOCKET(attachedItemName):
	return REFINE_FAILURE_NO_SOCKET0 % (attachedItemName)

# Drop item question
def REFINE_FAILURE_NO_GOLD_SOCKET(attachedItemName):
	return REFINE_FAILURE_NO_GOLD_SOCKET0 % (attachedItemName)

# Drop item question
def HOW_MANY_ITEM_DO_YOU_DROP(dropItemName, dropItemCount):
	return HOW_MANY_ITEM_DO_YOU_DROP2 % ("|cFFf2e8c2" + dropItemName + "|r", dropItemCount) if (dropItemCount > 1) else HOW_MANY_ITEM_DO_YOU_DROP1 % ("|cFFf2e8c2" + dropItemName + "|r")

# Fishing notify when looks like the fish is hooked.
def FISHING_NOTIFY(isFish, fishName):
	return FISHING_NOTIFY1 % (fishName) if isFish else FISHING_NOTIFY2 % (fishName)

# Fishing notify when you capture a fish.
def FISHING_SUCCESS(isFish, fishName):
	return FISHING_SUCCESS1 % (fishName) if isFish else FISHING_SUCCESS2 % (fishName)

def	TOOLTIP_FISH_LEN(length):
	return FISHING_LENGTH % (int(length/10), length%10)

# Convert a integer amount into a string and add . as separator for money.
def NumberToMoneyString(n, writeText = True) :
	if writeText:
		if n <= 0 :
			return "0 %s" % (MONETARY_UNIT0)

	if writeText:
		return "%s %s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]), MONETARY_UNIT0)
	else:
		return '.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ])

def NumberToMoneyDotStringWithoutMonetary(n):
	if n <= 0 :
		return "0"

	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

def NumberToString(n):
	n = float(n)
	if n.is_integer():
		return '{:,}'.format(int(n))
	else:
		return '{:,.2f}'.format(n)

def NumberToStringAsType(value, color = False, type = SHOP_TYPE_MONEY_SMALL):
	if color:
		return "|cFFf4be00{:0,.0f}".format(value).replace(',', '.') + " %s|r " % MONETARY_UNIT0 + type
	else:
		return "{:0,.0f}".format(value).replace(',', '.') + " %s " % MONETARY_UNIT0 + type

def NumberToMoneyWA(n) :
	if n <= 0 :
		return "0"

	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

def MoneyFormat(n):
	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

# Convert a integer amount into a string and add . as separator for secondary coin.
def NumberToSecondaryCoinString(n):
	return '0 {:s}'.format(MONETARY_UNIT_JUN) if (n <= 0) else '{:s} {:s}'.format('.'.join([(i - 3) < 0 and str(n)[:i] or str(n)[i - 3: i] for i in range(len(str(n)) % 3, len(str(n)) + 1, 3) if i]), MONETARY_UNIT_JUN)

# Return the title of alignment by points.
def GetAlignmentTitleName(alignment):
	if alignment >= 12000:
		return TITLE_NAME_LIST[0]
	elif alignment >= 8000:
		return TITLE_NAME_LIST[1]
	elif alignment >= 4000:
		return TITLE_NAME_LIST[2]
	elif alignment >= 1000:
		return TITLE_NAME_LIST[3]
	elif alignment >= 0:
		return TITLE_NAME_LIST[4]
	elif alignment > -4000:
		return TITLE_NAME_LIST[5]
	elif alignment > -8000:
		return TITLE_NAME_LIST[6]
	elif alignment > -12000:
		return TITLE_NAME_LIST[7]

	return TITLE_NAME_LIST[8]

# Convert seconds to Days-Hours-Minutes
def SecondToDHM(time):
	if time < 60:
		return colorInfo.Colorize('0' + MINUTE, 0xFFffffff)

	minute = int((time / 60) % 60)
	hour = int((time / 60) / 60) % 24
	day = int(int((time / 60) / 60) / 24)

	text = ''
	if day > 0:
		text += str(day) + DAY
		text += ' '

	if hour > 0:
		text += str(hour) + HOUR
		text += ' '

	if minute > 0:
		text += str(minute) + MINUTE
	return colorInfo.Colorize(text, 0xFFffffff)

def TimeToDHMS(time, ignoreSecTime = -1, useShortName = True):
	text = ""
	if time < 0:
		time *= -1
		text = "-"

	second = int(time % 60)
	minute = int((time / 60) % 60)
	hour = int(((time / 60) / 60) % 24)
	day = int(((time / 60) / 60) / 24)

	if ignoreSecTime > 0 and time >= ignoreSecTime:
		second = 0

	if day > 0:
		if day == 1:
			text += str(day) + DAY + " "
		else:
			text += str(day) + DAY + " "

	if hour > 0:
		text += str(hour) + HOUR
		if hour > 0:
			text += " "

	if minute > 0:
		text += str(minute) + MINUTE
		if useShortName == True:
			text += " "
		else:
			if minute == 1:
				text += " "
			else:
				text += " "

	if second > 0 or (day == 0 and hour == 0 and minute == 0):
		text += str(second) + SECOND
		if useShortName == True:
			text += " "
		else:
			if second == 1:
				text += " "
			else:
				text += " "

	return text[:-1]

# Convert seconds to Days-Hours-Minutes-Seconds
def SecondToDHMS(time):
	if time < 60:
		return colorInfo.Colorize("%.2f %s" % (time, SECOND), 0xFFffffff)

	second = int(time % 60)
	minute = int((time / 60) % 60)
	hour = int((time / 60) / 60) % 24
	day = int(int((time / 60) / 60) / 24)

	text = ""

	if day > 0:
		text += str(day) + DAY

	if hour > 0:
		text += " "
		text += str(hour) + HOUR

	if minute > 0:
		text += " "
		text += str(minute) + MINUTE

	if second > 0:
		text += " "
		text += str(second) + SECOND

	return colorInfo.Colorize(text, 0xFFffffff)

# Convert seconds to Hours-Minutes Seconds
def SecondToHMS(time):
	try:
		time = int(time)
	except ValueError:
		return "0 " + SECOND

	if int(time) <= 0:
		return "0 " + SECOND

	second = int(time % 60)
	minute = int((time / 60) % 60)
	hour = int((time / 60) / 60)

	text = ""

	if hour > 0:
		text += str(hour) + HOUR
		if minute > 0:
			text += " "

	if minute > 0:
		text += str(minute) + MINUTE
		if second > 0:
			text += " "

	if second > 0:
		text += str(second) + " " + SECOND

	return text

# Convert seconds to Hours-Minutes
def SecondToHM(time):
	if time < 60:
		if IsARABIC():
			return '%.2f %s' % (time, SECOND)
		else:
			return '0' + MINUTE

	minute = int((time / 60) % 60)
	hour = int((time / 60) / 60)

	text = ''
	if hour > 0:
		text += str(hour) + HOUR
		if hour > 0:
			text += ' '

	if minute > 0:
		text += str(minute) + MINUTE
	return text

def SecondToMS(time):
	if time < 60:
		return "%d%s" % (time, SECOND)

	second = int(time % 60)
	minute = int((time / 60) % 60)

	text = ""

	if minute > 0:
		text += str(minute) + MINUTE
		if minute > 0:
			text += " "

	if second > 0:
		text += str(second) + SECOND

	return text

def SecondToDHMSShort(time):
	days = int(time / (24 * 60 * 60))
	time -= 24 * 60 * 60 * days
	hours = int(time / (60 * 60))
	time -= 60 * 60 * hours
	mins = int(time / 60)
	time -= 60 * mins
	secs = int(time)

	return "%02d:%02d:%02d:%02d" % (days, hours, mins, secs)

if app.ENABLE_ADMIN_MANAGER:
	def GetSkillGroupName(job, skillGroup):
		if skillGroup == 0:
			return "None"

		skillGroupNames = [
			[SKILLGROUP_NAME_WARRIOR_1, SKILLGROUP_NAME_WARRIOR_2],
			[SKILLGROUP_NAME_ASSASSIN_1, SKILLGROUP_NAME_ASSASSIN_2],
			[SKILLGROUP_NAME_SURA_1, SKILLGROUP_NAME_SURA_2],
			[SKILLGROUP_NAME_SHAMAN_1, SKILLGROUP_NAME_SHAMAN_2],
			["Instinct"],
		]

		return skillGroupNames[job][skillGroup - 1]

	def SecondToDHMSAdmin(time, ignoreSecTime = -1, useShortName = True):
		text = ""
		if time < 0:
			time *= -1
			text = "-"

		second = int(time % 60)
		minute = int((time / 60) % 60)
		hour = int(((time / 60) / 60) % 24)
		day = int(((time / 60) / 60) / 24)

		if ignoreSecTime > 0 and time >= ignoreSecTime:
			second = 0

		if day > 0:
			if day == 1:
				text += str(day) + " Tag "
			else:
				text += str(day) + " Tage "

		if hour > 0:
			text += str(hour) + " "
			if useShortName == True:
				text += "Std. "
			else:
				if hour == 1:
					text += "Stunde "
				else:
					text += "Stunden "

		if minute > 0:
			text += str(minute) + " "
			if useShortName == True:
				text += "Min. "
			else:
				if minute == 1:
					text += "Minute "
				else:
					text += "Minuten "

		if second > 0 or (day == 0 and hour == 0 and minute == 0):
			text += str(second) + " "
			if useShortName == True:
				text += "Sek. "
			else:
				if second == 1:
					text += "Sekunde "
				else:
					text += "Sekunden "

		return text[:-1]

def AddPointToNumberString(n) :
	if n <= 0 :
		return "0"

	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

# if app.ENABLE_DUNGEON_INFO:
def MinuteToHM(time):
	minute = int(time % 60)
	hour = int((time / 60) % 60)

	text = ""

	if hour > 0:
		text += str(hour) + HOUR
		text += " "

	if minute > 0:
		text += str(minute) + MINUTE

	return text

def SecondToHMS(time):
	if time < 60:
		return "00:00:%02d" % (time)

	second = int(time % 60)
	minute = int((time / 60) % 60)
	hour = int((time / 60) / 60)

	return "%02d:%02d:%02d" % (hour, minute, second)

def GetVariableValue(varName):
	if globals().has_key(varName):
		return globals()[varName]

	return ""

def GetVariableName(varValue):
	for name, value in globals().items():
		if str(varValue) == value:
			return str(name)

	return ""

def SecondToNiceTime(time):
	second = int(time % 60)
	minute = int((time / 60) % 60)
	hour = int((time / 60) / 60) % 24

	return "%02d:%02d:%02d" % (hour, minute, second)

def AddPointToNumberString(n) :
	if n <= 0 :
		return "0"

	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

# OFFLINE SHOP
def GetFormattedTimeString(time):
	minutes, seconds = divmod(time, 60)
	hours, minutes = divmod(minutes, 60)
	return "%dh %02dm" % (hours, minutes)

def FormatSeconds(seconds):
	timeInfos = [
		["y", "y", 365 * 24 * 60 * 60],
		["d", "d", 24 * 60 * 60],
		["h", "h", 60 * 60],
		["m", "m", 60],
		["s", "s", 1],
	]

	timeStrings = []
	for timeInfo in timeInfos:
		fitCount = seconds / timeInfo[2]

		if fitCount >= 1:
			seconds = seconds - (timeInfo[2] * fitCount)

			if fitCount > 1:
				timeStrings.append(str(fitCount) + "" + timeInfo[1])
			else:
				timeStrings.append(str(fitCount) + "" + timeInfo[0])

	if len(timeStrings) == 0:
		return "-"

	return " ".join(timeStrings)

def FormatShortSeconds(seconds):
	timeInfos = [
		60 * 60,
		60,
		1
	]

	timeStrings = []
	for timeInfo in timeInfos:
		fitCount = seconds / timeInfo
		seconds = seconds - (timeInfo * fitCount)
		timeStrings.append("{:02d}".format(fitCount))

	return ":".join(timeStrings)

def GetFormattedNumberString(number):
	return "{:,}".format(number).replace(",", ".")

def FormatMoney(money, suffix = "Yang"):
	return "{} {}".format(GetFormattedNumberString(money), suffix)

def NumberToDecimalString(n):
	return str('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

def FloatAsString(num, maxPrec=2):
	if maxPrec <= 0:
		return "%d" % int(num)

	s = ("%%.%df" % maxPrec) % num
	while s[len(s)-1] == '0':
		s = s[:len(s)-1]

	if s[len(s)-1] == '.':
		return "%d" % int(num)

	return s

def DottedNumber(n):
	n = float(n)
	if float(n).is_integer():
		return '{:,}'.format(int(n)).replace('.', '_').replace(',', '.').replace('_', '.')
	else:
		return '{:,.2f}'.format(n).replace('.', '_').replace(',', '.').replace('_', '.')

def sec2time(timeSeconds, timeTypes, timeShowAll=False):
	"""
	Convert seconds to specific format time readable.
	:param time: int
	:param timeTypes: str (DMS, DHS, HMS, HM, HS, MS, M, S)
	:param timeShowAll: bool (showing the time name even if the value is 0, otherwise check the value if is > 0)
	:return: string
	"""
	(d, remainder) = divmod(timeSeconds, 86400)
	(h, remainder) = divmod(remainder, 3600)
	(m, s) = divmod(remainder, 60)

	TIME_INFO_DICT = dict(
		d=(d, DAY),
		h=(h, HOUR),
		m=(m, MINUTE),
		s=(s, SECOND)
	)

	timeOutput = str()
	for timeType in timeTypes:
		timeType = timeType.lower()

		if timeType in TIME_INFO_DICT:
			(timeValue, timeLocaleName) = TIME_INFO_DICT[timeType]
			if timeValue > 0 or timeShowAll:
				timeOutput += '{:0.0f} {} '.format(timeValue, timeLocaleName)

	if not timeOutput:
		return "Less than a minute."

	return timeOutput[:-1]

if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	from datetime import datetime
	def GetFullDateFormat(timestamp):
		return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y - %I:%M:%S")
		
	def GetDateFormat(timestamp):
		return datetime.fromtimestamp(timestamp).strftime("%d/%m/%Y")
		
	def NumberToMoneyStringNoUnit(n) :
		if n <= 0 :
			return "0"

		return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ])) 

def NumberWithPoint(n) :
	if n <= 0 :
		return "0"

	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

def NumberToEXPString(n) :
	if n <= 0 :
		return "0"

	return "%s" % ('.'.join([ i-3<0 and str(n)[:i] or str(n)[i-3:i] for i in range(len(str(n))%3, len(str(n))+1, 3) if i ]))

