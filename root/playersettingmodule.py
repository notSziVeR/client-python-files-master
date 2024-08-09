#! /usr/bin/env python
__author__		= 'VegaS'
__date__		= '2020.01.19'
__name__		= 'PlayerSettingsModule - Renewal'
__version__		= '2.0'

import app, chrmgr, uiGuild, dbg, chr, player
import equipmentSet, localeInfo

if gcGetEnable("ENABLE_SHORTCUT_SYSTEM"):
	import shortcutsConfig

JOB_WARRIOR, JOB_ASSASSIN, JOB_SURA, JOB_SHAMAN = range(4)
JOB_MAX_NUM = 4

RACE_WARRIOR_M, RACE_ASSASSIN_W, RACE_SURA_M, RACE_SHAMAN_W, RACE_WARRIOR_W, RACE_ASSASSIN_M, RACE_SURA_W, RACE_SHAMAN_M = range(8)

PASSIVE_GUILD_SKILL_INDEX_LIST = ( 151, )
ACTIVE_GUILD_SKILL_INDEX_LIST = ( 152, 153, 154, 155, 156, 157, )

FACE_IMAGE_DICT = {
	RACE_WARRIOR_M :	"d:/ymir work/ui/game/windows/face_warrior.sub",
	RACE_ASSASSIN_W :	"d:/ymir work/ui/game/windows/face_assassin.sub",
	RACE_SURA_M :		"d:/ymir work/ui/game/windows/face_sura.sub",
	RACE_SHAMAN_W :		"d:/ymir work/ui/game/windows/face_shaman.sub",
}

SKILL_INDEX_DICT = []

def DefineSkillIndexDict():
	global SKILL_INDEX_DICT

	SKILL_INDEX_DICT = {
		JOB_WARRIOR : { 
			1 : (1, 2, 3, 4, 5, 6, 0, 0, 137, 0, 138, 0, 139, 0,), 
			2 : (16, 17, 18, 19, 20, 21, 0, 0, 137, 0, 138, 0, 139, 0,), 
			"SUPPORT" : (122, 130, 131, 121, 129, 123, 124, 143, 144, 145, 146, 147,),
		},
		JOB_ASSASSIN : { 
			1 : (31, 32, 33, 34, 35, 36, 0, 0, 137, 0, 138, 0, 139, 0, 140,), 
			2 : (46, 47, 48, 49, 50, 51, 0, 0, 137, 0, 138, 0, 139, 0, 140,), 
			"SUPPORT" : (122, 130, 131, 121, 129, 123, 124, 143, 144, 145, 146, 147,),
		},
		JOB_SURA : { 
			1 : (61, 62, 63, 64, 65, 66, 0, 0, 137, 0, 138, 0, 139, 0,),
			2 : (76, 77, 78, 79, 80, 81, 0, 0, 137, 0, 138, 0, 139, 0,),
			"SUPPORT" : (122, 130, 131, 121, 129, 123, 124, 143, 144, 145, 146, 147,),
		},
		JOB_SHAMAN : { 
			1 : (91, 92, 93, 94, 95, 96, 0, 0, 137, 0, 138, 0, 139, 0,),
			2 : (106, 107, 108, 109, 110, 111, 0, 0, 137, 0, 138, 0, 139, 0,),
			"SUPPORT" : (122, 130, 131, 121, 129, 123, 124, 143, 144, 145, 146, 147,),
		},
	}

def LoadRaceHeight():
	try:
		lines = open("race_height.txt", "r").readlines()
	except IOError:
		dbg.TraceError("Failed to load race_height.txt")
		return

	for line in lines:
		tokens = line[:-1].split("\t")
		if len(tokens) == 0 or not tokens[0]:
			continue

		chrmgr.SetRaceHeight(int(tokens[0]), float(tokens[1]))


if gcGetEnable("ENABLE_SHORTCUT_SYSTEM"):
	def LoadShortcutSets():
		shortcutsConfig.load("game/shortcutsets.xml")

def LoadEquipmentSets():
	equipmentSet.load("game/equipmentsets.xml")

def LoadRefineElementEff():
	if app.ENABLE_REFINE_ELEMENT:
		## If you don't have wolfman just delete "w" and "w_l"
		for i, elementName in enumerate(("electric", "fire", "ice", "wind", "daeji", "dark")):
			for j, weaponType in enumerate(("", "b", "f", "s", "s_l", "w", "w_l")):
				effectName = "element%02d_%s" % (i + 1, elementName)
				effectName += (".mse") if weaponType == "" else (("_%s.mse" % weaponType[:1]) if weaponType in ("s_l", "w_l") else ("_%s.mse" % weaponType))
				
				effectNumber = (i * chrmgr.EFFECT_REFINE_ELEMENT_WEAPON_MAX) + j
				if weaponType in ("b", "s_l", "w_l"):
					chrmgr.RegisterEffect(chrmgr.EFFECT_REFINE_ELEMENT + effectNumber, "PART_WEAPON_LEFT", "d:/ymir work/pc/common/effect/sword/" + effectName)
				else:
					chrmgr.RegisterEffect(chrmgr.EFFECT_REFINE_ELEMENT + effectNumber, "PART_WEAPON", "d:/ymir work/pc/common/effect/sword/" + effectName)

def LoadGameNPC():
	fHandle = app.OpenTextFile("game/settings/npclist.txt")

	for i in range( app.GetTextFileLineCount(fHandle) ):
		tokens = app.GetTextFileLine(fHandle, i)
		tokens = tokens.split("\t")

		map(lambda token: token.strip(), tokens)

		if tokens[0] == '' or tokens[0][0] == '#':
			continue

		vnum = int(tokens[0])
		if vnum:
			chrmgr.RegisterRaceName(vnum, tokens[1].strip())
		else:
			chrmgr.RegisterRaceSrcName(tokens[1].strip(), tokens[2].strip())

	app.CloseTextFile(fHandle)

def RegisterSkill(race, group, empire=0):
	DefineSkillIndexDict()

	job = chr.RaceToJob(race)

	if SKILL_INDEX_DICT.has_key(job):
		if SKILL_INDEX_DICT[job].has_key(group):
			activeSkillList = SKILL_INDEX_DICT[job][group]

			for i in xrange(len(activeSkillList)):
				skillIndex = activeSkillList[i]

				if i != 6 and i != 7:
					player.SetSkill(i+1, skillIndex)

		supportSkillList = SKILL_INDEX_DICT[job]["SUPPORT"]

		for i in xrange(len(supportSkillList)):
			player.SetSkill(i+100+1, supportSkillList[i])

	## Guild Skill
	for i in range(len(PASSIVE_GUILD_SKILL_INDEX_LIST)):
		player.SetSkill(200 + i, PASSIVE_GUILD_SKILL_INDEX_LIST[i] )

	for i in range(len(ACTIVE_GUILD_SKILL_INDEX_LIST)):
		player.SetSkill(210 + i, ACTIVE_GUILD_SKILL_INDEX_LIST[i] )

# GUILD_BUILDING
def LoadGuildBuildingList(filename):
	uiGuild.BUILDING_DATA_LIST = []

	handle = app.OpenTextFile(filename)
	count = app.GetTextFileLineCount(handle)
	for i in xrange(count):
		line = app.GetTextFileLine(handle, i)
		tokens = line.split("\t")

		TOKEN_VNUM = 0
		TOKEN_TYPE = 1
		TOKEN_NAME = 2
		TOKEN_LOCAL_NAME = 3
		NO_USE_TOKEN_SIZE_1 = 4
		NO_USE_TOKEN_SIZE_2 = 5
		NO_USE_TOKEN_SIZE_3 = 6
		NO_USE_TOKEN_SIZE_4 = 7
		TOKEN_X_ROT_LIMIT = 8
		TOKEN_Y_ROT_LIMIT = 9
		TOKEN_Z_ROT_LIMIT = 10
		TOKEN_PRICE = 11
		TOKEN_MATERIAL = 12
		TOKEN_NPC = 13
		TOKEN_GROUP = 14
		TOKEN_DEPEND_GROUP = 15
		TOKEN_ENABLE_FLAG = 16
		LIMIT_TOKEN_COUNT = 17

		if not tokens[TOKEN_VNUM].isdigit():
			continue

		if len(tokens) < LIMIT_TOKEN_COUNT:
			dbg.TraceError("Strange token count [%d/%d] [%s]" % (len(tokens), LIMIT_TOKEN_COUNT, line))
			continue

		ENABLE_FLAG_TYPE_NOT_USE = False
		ENABLE_FLAG_TYPE_USE = True
		ENABLE_FLAG_TYPE_USE_BUT_HIDE = 2

		if ENABLE_FLAG_TYPE_NOT_USE == int(tokens[TOKEN_ENABLE_FLAG]):
			continue

		vnum = int(tokens[TOKEN_VNUM])
		type = tokens[TOKEN_TYPE]
		name = tokens[TOKEN_NAME]
		localName = tokens[TOKEN_LOCAL_NAME]
		xRotLimit = int(tokens[TOKEN_X_ROT_LIMIT])
		yRotLimit = int(tokens[TOKEN_Y_ROT_LIMIT])
		zRotLimit = int(tokens[TOKEN_Z_ROT_LIMIT])
		price = tokens[TOKEN_PRICE]
		material = tokens[TOKEN_MATERIAL]

		folderName = ""
		if "HEADQUARTER" == type:
			folderName = "headquarter"
		elif "FACILITY" == type:
			folderName = "facility"
		elif "OBJECT" == type:
			folderName = "object"
		elif "WALL" == type:
			folderName = "fence"

		materialList = ["0", "0", "0"]
		if material:
			if material[0] == "\"":
				material = material[1:]
			if material[-1] == "\"":
				material = material[:-1]
			for one in material.split("/"):
				data = one.split(",")
				if 2 != len(data):
					continue
				itemID = int(data[0])
				count = data[1]

				if itemID == uiGuild.MATERIAL_STONE_ID:
					materialList[uiGuild.MATERIAL_STONE_INDEX] = count
				elif itemID == uiGuild.MATERIAL_LOG_ID:
					materialList[uiGuild.MATERIAL_LOG_INDEX] = count
				elif itemID == uiGuild.MATERIAL_PLYWOOD_ID:
					materialList[uiGuild.MATERIAL_PLYWOOD_INDEX] = count

		## GuildSymbol
		chrmgr.RegisterRaceSrcName(name, folderName)
		chrmgr.RegisterRaceName(vnum, name)

		appendingData = {
			"VNUM"			:	vnum,
			"TYPE"			:	type,
			"NAME"			:	name,
			"LOCAL_NAME"	:	localName,
			"X_ROT_LIMIT"	:	xRotLimit,
			"Y_ROT_LIMIT"	:	yRotLimit,
			"Z_ROT_LIMIT"	:	zRotLimit,
			"PRICE"			:	price,
			"MATERIAL"		:	materialList,
			"SHOW"			:	True
		}

		if ENABLE_FLAG_TYPE_USE_BUT_HIDE == int(tokens[TOKEN_ENABLE_FLAG]):
			appendingData["SHOW"] = False

		uiGuild.BUILDING_DATA_LIST.append(appendingData)

	app.CloseTextFile(handle)

def LoadGameEffect():
	chrmgr.RegisterEffect_(\
		(chrmgr.EFFECT_SPAWN_APPEAR, "Bip01", "d:/ymir work/effect/etc/appear_die/monster_appear.mse"),
		(chrmgr.EFFECT_SPAWN_DISAPPEAR, "Bip01", "d:/ymir work/effect/etc/appear_die/monster_die.mse"),
		(chrmgr.EFFECT_FLAME_ATTACK, "equip_right_hand", "d:/ymir work/effect/hit/blow_flame/flame_3_weapon.mse"),
		(chrmgr.EFFECT_FLAME_HIT, "", "d:/ymir work/effect/hit/blow_flame/flame_3_blow.mse"),
		(chrmgr.EFFECT_FLAME_ATTACH, "", "d:/ymir work/effect/hit/blow_flame/flame_3_body.mse"),
		(chrmgr.EFFECT_ELECTRIC_ATTACK, "equip_right", "d:/ymir work/effect/hit/blow_electric/light_1_weapon.mse"),
		(chrmgr.EFFECT_ELECTRIC_HIT, "", "d:/ymir work/effect/hit/blow_electric/light_1_blow.mse"),
		(chrmgr.EFFECT_ELECTRIC_ATTACH, "", "d:/ymir work/effect/hit/blow_electric/light_1_body.mse"),
		(chrmgr.EFFECT_LEVELUP, "", "d:/ymir work/effect/etc/levelup_1/level_up.mse"),
		(chrmgr.EFFECT_SKILLUP, "", "d:/ymir work/effect/etc/skillup/skillup_1.mse"),
		(chrmgr.EFFECT_EMPIRE+1, "Bip01", "d:/ymir work/effect/etc/empire/empire_A.mse"),
		(chrmgr.EFFECT_EMPIRE+2, "Bip01", "d:/ymir work/effect/etc/empire/empire_B.mse"),
		(chrmgr.EFFECT_EMPIRE+3, "Bip01", "d:/ymir work/effect/etc/empire/empire_C.mse"),
		(chrmgr.EFFECT_WEAPON+1, "equip_right_hand", "d:/ymir work/pc/warrior/effect/geom_sword_loop.mse"),
		(chrmgr.EFFECT_WEAPON+2, "equip_right_hand", "d:/ymir work/pc/warrior/effect/geom_spear_loop.mse"),
		(chrmgr.EFFECT_AFFECT+0, "Bip01", localeInfo.FN_GM_MARK),
		(chrmgr.EFFECT_AFFECT+3, "Bip01", "d:/ymir work/effect/hit/blow_poison/poison_loop.mse"),
		(chrmgr.EFFECT_AFFECT+4, "", "d:/ymir work/effect/affect/slow.mse"),
		(chrmgr.EFFECT_AFFECT+5, "Bip01 Head", "d:/ymir work/effect/etc/stun/stun_loop.mse"),
		(chrmgr.EFFECT_AFFECT+6, "", "d:/ymir work/effect/etc/ready/ready.mse"),
		(chrmgr.EFFECT_AFFECT+16, "", "d:/ymir work/pc/warrior/effect/gyeokgongjang_loop.mse"),
		(chrmgr.EFFECT_AFFECT+17, "", "d:/ymir work/pc/assassin/effect/gyeonggong_loop.mse"),
		(chrmgr.EFFECT_AFFECT+19, "Bip01 R Finger2", "d:/ymir work/pc/sura/effect/gwigeom_loop.mse"),
		(chrmgr.EFFECT_AFFECT+20, "", "d:/ymir work/pc/sura/effect/fear_loop.mse"),
		(chrmgr.EFFECT_AFFECT+21, "", "d:/ymir work/pc/sura/effect/jumagap_loop.mse"),
		(chrmgr.EFFECT_AFFECT+22, "", "d:/ymir work/pc/shaman/effect/3hosin_loop.mse"),
		(chrmgr.EFFECT_AFFECT+23, "", "d:/ymir work/pc/shaman/effect/boho_loop.mse"),
		(chrmgr.EFFECT_AFFECT+24, "", "d:/ymir work/pc/shaman/effect/10kwaesok_loop.mse"),
		(chrmgr.EFFECT_AFFECT+25, "", "d:/ymir work/pc/sura/effect/heuksin_loop.mse"),
		(chrmgr.EFFECT_AFFECT+26, "", "d:/ymir work/pc/sura/effect/muyeong_loop.mse"),
		(chrmgr.EFFECT_AFFECT+28, "Bip01", "d:/ymir work/effect/hit/blow_flame/flame_loop.mse"),
		(chrmgr.EFFECT_AFFECT+29, "Bip01 R Hand", "d:/ymir work/pc/shaman/effect/6gicheon_hand.mse"),
		(chrmgr.EFFECT_AFFECT+30, "Bip01 L Hand", "d:/ymir work/pc/shaman/effect/jeungryeok_hand.mse"),
		(chrmgr.EFFECT_AFFECT+32, "Bip01 Head", "d:/ymir work/pc/sura/effect/pabeop_loop.mse"),
		(chrmgr.EFFECT_AFFECT+33, "", "d:/ymir work/pc/warrior/effect/gyeokgongjang_loop.mse"),
		(chrmgr.EFFECT_AFFECT+35, "", "d:/ymir work/effect/etc/guild_war_flag/flag_red.mse"),
		(chrmgr.EFFECT_AFFECT+36, "", "d:/ymir work/effect/etc/guild_war_flag/flag_blue.mse"),
		(chrmgr.EFFECT_AFFECT+37, "", "d:/ymir work/effect/etc/guild_war_flag/flag_yellow.mse"),
		(chrmgr.EFFECT_DUST, "", "d:/ymir work/effect/etc/dust/dust.mse", True),
		(chrmgr.EFFECT_HORSE_DUST, "", "d:/ymir work/effect/etc/dust/running_dust.mse", True),
		(chrmgr.EFFECT_HIT, "", "d:/ymir work/effect/hit/blow_1/blow_1_low.mse", True),
		(chrmgr.EFFECT_HPUP_RED, "", "d:/ymir work/effect/etc/recuperation/drugup_red.mse", True),
		(chrmgr.EFFECT_SPUP_BLUE, "", "d:/ymir work/effect/etc/recuperation/drugup_blue.mse", True),
		(chrmgr.EFFECT_SPEEDUP_GREEN, "", "d:/ymir work/effect/etc/recuperation/drugup_green.mse", True),
		(chrmgr.EFFECT_DXUP_PURPLE, "", "d:/ymir work/effect/etc/recuperation/drugup_purple.mse", True),
		(chrmgr.EFFECT_AUTO_HPUP, "", "d:/ymir work/effect/etc/recuperation/autodrugup_red.mse", True),
		(chrmgr.EFFECT_AUTO_SPUP, "", "d:/ymir work/effect/etc/recuperation/autodrugup_blue.mse", True),
		(chrmgr.EFFECT_RAMADAN_RING_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item1.mse", True),
		(chrmgr.EFFECT_HALLOWEEN_CANDY_EQUIP, "", "d:/ymir work/effect/etc/buff/buff_item2.mse", True),
		(chrmgr.EFFECT_PENETRATE, "Bip01", "d:/ymir work/effect/hit/gwantong.mse", True),
		(chrmgr.EFFECT_FIRECRACKER, "", "d:/ymir work/effect/etc/firecracker/newyear_firecracker.mse", True),
		(chrmgr.EFFECT_SPIN_TOP, "", "d:/ymir work/effect/etc/firecracker/paing_i.mse", True),
		(chrmgr.EFFECT_SELECT, "", "d:/ymir work/effect/etc/click/click_select.mse", True),
		(chrmgr.EFFECT_TARGET, "", "d:/ymir work/effect/etc/click/click_glow_select.mse", True),
		(chrmgr.EFFECT_STUN, "Bip01 Head", "d:/ymir work/effect/etc/stun/stun.mse", True),
		(chrmgr.EFFECT_CRITICAL, "Bip01 R Hand", "d:/ymir work/effect/hit/critical.mse", True),
		(player.EFFECT_PICK, "", "d:/ymir work/effect/etc/click/click.mse", True),
		(chrmgr.EFFECT_DAMAGE_TARGET, "", "d:/ymir work/effect/affect/damagevalue/target.mse", True),
		(chrmgr.EFFECT_DAMAGE_NOT_TARGET, "", "d:/ymir work/effect/affect/damagevalue/nontarget.mse", True),
		(chrmgr.EFFECT_DAMAGE_SELFDAMAGE, "", "d:/ymir work/effect/affect/damagevalue/damage.mse", True),
		(chrmgr.EFFECT_DAMAGE_SELFDAMAGE2, "", "d:/ymir work/effect/affect/damagevalue/damage_1.mse", True),
		(chrmgr.EFFECT_DAMAGE_POISON, "", "d:/ymir work/effect/affect/damagevalue/poison_new.mse", True),
		(chrmgr.EFFECT_DAMAGE_MISS, "", "d:/ymir work/effect/affect/damagevalue/miss.mse", True),
		(chrmgr.EFFECT_DAMAGE_TARGETMISS, "", "d:/ymir work/effect/affect/damagevalue/target_miss.mse", True),
		(chrmgr.EFFECT_DAMAGE_CRITICAL, "", "d:/ymir work/effect/affect/damagevalue/critical.mse", True),
		(chrmgr.EFFECT_PERCENT_DAMAGE1, "", "d:/ymir work/effect/hit/percent_damage1.mse", True),
		(chrmgr.EFFECT_PERCENT_DAMAGE2, "", "d:/ymir work/effect/hit/percent_damage2.mse", True),
		(chrmgr.EFFECT_PERCENT_DAMAGE3, "", "d:/ymir work/effect/hit/percent_damage3.mse", True),

	)
