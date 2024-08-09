import ui
import localeInfo
import chr
import item
import app
import skill
import player
import uiToolTip
import math
from ui_event import Event
from ui_event import MakeEvent
import uiCommon
import net
import colorInfo

from cff import CFF

INFINITE_AFFECT_DURATION = 0x1FFFFFFF

AFFECT_TO_SKILL = {
	chr.AFFECT_JEONGWI: 3,
	chr.AFFECT_GEOMGYEONG: 4,
	chr.AFFECT_CHEONGEUN: 19,
	chr.AFFECT_EUNHYEONG: 34,
	chr.AFFECT_GYEONGGONG: 49,
	chr.AFFECT_GWIGEOM: 63,
	chr.AFFECT_GONGPO: 64,
	chr.AFFECT_JUMAGAP: 65,
	chr.AFFECT_MUYEONG: 78,
	chr.AFFECT_HEUKSIN: 79,
	chr.AFFECT_HOSIN: 94,
	chr.AFFECT_BOHO: 95,
	chr.AFFECT_GICHEON: 96,
	chr.AFFECT_KWAESOK: 110,
	chr.AFFECT_JEUNGRYEOK: 111,
}

class NAffectImage(ui.ExpandedImageBox):
	def __init__(self):
		ui.ExpandedImageBox.__init__(self)

		self.toolTip = uiToolTip.ItemToolTip(100)
		self.toolTip.HideToolTip()

	def OnMouseOverIn(self):
		self.toolTip.ShowToolTip()
		return True

	def OnMouseOverOut(self):
		self.toolTip.HideToolTip()
		return True

class PolyImage(NAffectImage):
	def __init__(self, affectType, image, duration, description):
		NAffectImage.__init__(self)

		if duration != INFINITE_AFFECT_DURATION and 0 < duration < 60 * 60 * 24 * 356 * 10:
			self.endTime = app.GetGlobalTimeStamp() + duration
		else:
			self.endTime = 0

		self.affectType = affectType
		self.polymorphQuestionDialog = None

		self.description = description
		self.LoadImage(image)
		self.SetScale(0.7, 0.7)
		self.Update()

	def GetType(self):
		return self.affectType

	def OnMouseLeftButtonUp(self):
		self.OnPolymorphQuestionDialog()

	def OnPolymorphQuestionDialog(self):
		self.polymorphQuestionDialog = uiCommon.QuestionDialogWithTimeLimit()
		self.polymorphQuestionDialog.SetText1(localeInfo.REMOVE_AFFECT_POLYMORPH_QUESTION)
		self.polymorphQuestionDialog.SetAcceptEvent(Event(self.OnClosePolymorphQuestionDialog, True))
		self.polymorphQuestionDialog.SetCancelEvent(Event(self.OnClosePolymorphQuestionDialog, False))
		self.polymorphQuestionDialog.Open(5)
		self.polymorphQuestionDialog.SetCancelOnTimeOver()

	def OnClosePolymorphQuestionDialog(self, answer):
		if not self.polymorphQuestionDialog:
			return False

		self.polymorphQuestionDialog.Close()
		self.polymorphQuestionDialog = None

		if not answer:
			return False

		net.SendChatPacket("/remove_polymorph")
		return True

	def Update(self):
		if not self.IsIn() or not self.description or not self.toolTip:
			return

		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(self.description)

		if self.endTime != 0:
			leftTime = localeInfo.sec2time(self.endTime - app.GetGlobalTimeStamp(), "DHMS")
			self.toolTip.AppendTextLine("({} : {})".format(colorInfo.Colorize(localeInfo.LEFT_TIME, 0xFF68bcff), leftTime))

class SimpleAffectImage(NAffectImage):
	def __init__(self, affectType, subType, image, duration, description, scale=True, skill_affect = False):
		NAffectImage.__init__(self)

		if subType == 0:
			if duration != INFINITE_AFFECT_DURATION and 0 < duration < 60 * 60 * 24 * 356 * 10:
				self.endTime = app.GetGlobalTimeStamp() + duration
			else:
				self.endTime = 0

		elif subType == 1:
			self.endTime = duration

		self.removeAffectQuestionDialog = None

		self.affectType = affectType

		self.description = description
		self.LoadImage(image)

		# if scale:
		# 	self.SetScale(0.7, 0.7)
		# else:
		# 	self.SetScale(1.0, 1.0)

		self.skill_affect = skill_affect

		self.Update()

	def GetType(self):
		return self.affectType

	def IsSkillAffect(self):
		return self.skill_affect

	def GetSkillIndex(self):
		skillIndex = AFFECT_TO_SKILL.get(self.GetType(), -1)
		return skillIndex

	def OnMouseLeftButtonUp(self):
		if self.GetSkillIndex() == -1:
			return

		self.OnyRemoveAffectQuestionDialog()

	def OnyRemoveAffectQuestionDialog(self):
		self.removeAffectQuestionDialog = uiCommon.QuestionDialogWithTimeLimit()
		self.removeAffectQuestionDialog.SetText1(localeInfo.REMOVE_AFFECT_QUESTION % skill.GetSkillName(self.GetType()))
		self.removeAffectQuestionDialog.SetAcceptEvent(Event(self.OnCloseRemoveAffectDialog, True))
		self.removeAffectQuestionDialog.SetCancelEvent(Event(self.OnCloseRemoveAffectDialog, False))
		self.removeAffectQuestionDialog.Open(5)
		self.removeAffectQuestionDialog.SetCancelOnTimeOver()

	def OnCloseRemoveAffectDialog(self, answer):
		if not self.removeAffectQuestionDialog:
			return False

		self.removeAffectQuestionDialog.Close()
		self.removeAffectQuestionDialog = None

		if not answer:
			return False

		net.SendChatPacket("/remove_affect " + str(self.GetSkillIndex()))
		return True

	def Update(self):
		if not self.IsIn() or not self.description or not self.toolTip:
			return

		self.toolTip.ClearToolTip()
		self.toolTip.AppendTextLine(self.description, self.toolTip.TITLE_COLOR)

		if self.endTime != 0:
			leftTime = localeInfo.sec2time(self.endTime - app.GetGlobalTimeStamp(), "DHMS")
			self.toolTip.AppendTextLine("({} : {})".format(colorInfo.Colorize(localeInfo.LEFT_TIME, 0xFF68bcff), leftTime))

class LovePointImage(NAffectImage):
	FILE_PATH = "d:/ymir work/ui/pattern/LovePoint/"
	FILE_DICT = {
		# TODO: Use .sub images!
		0: FILE_PATH + "01.dds",
		1: FILE_PATH + "02.dds",
		2: FILE_PATH + "02.dds",
		3: FILE_PATH + "03.dds",
		4: FILE_PATH + "04.dds",
		5: FILE_PATH + "05.dds",
	}

	def __init__(self):
		NAffectImage.__init__(self)

		self.loverName = ""
		self.lovePoint = 0

	def SetLoverInfo(self, name, lovePoint):
		self.loverName = name
		self.lovePoint = lovePoint
		self.__Refresh()

	def OnUpdateLovePoint(self, lovePoint):
		self.lovePoint = lovePoint
		self.__Refresh()

	def __Refresh(self):
		self.lovePoint = max(0, self.lovePoint)
		self.lovePoint = min(100, self.lovePoint)

		if 0 == self.lovePoint:
			loveGrade = 0
		else:
			loveGrade = self.lovePoint / 25 + 1

		fileName = self.FILE_DICT.get(loveGrade, self.FILE_PATH + "00.dds")

		try:
			self.LoadImage(fileName)
		except RuntimeError:
			print("Loading failed for lovePoint=%d %s" % (self.lovePoint, fileName))

		# This is necessary because LoadImage() destroys the old
		# CGraphicExpandedImageInstance object...
		self.SetScale(0.7, 0.7)

		self.toolTip.ClearToolTip()
		self.toolTip.SetTitle(self.loverName)
		self.toolTip.AppendTextLine(localeInfo.AFF_LOVE_POINT % (self.lovePoint))

class HorseImage(NAffectImage):
	FILE_PATH = "d:/ymir work/ui/pattern/HorseState/"

	FILE_DICT = {
		# TODO: Use .sub images!
		00: FILE_PATH + "00.dds",
		01: FILE_PATH + "00.dds",
		02: FILE_PATH + "00.dds",
		03: FILE_PATH + "00.dds",
		10: FILE_PATH + "10.dds",
		11: FILE_PATH + "11.dds",
		12: FILE_PATH + "12.dds",
		13: FILE_PATH + "13.dds",
		20: FILE_PATH + "20.dds",
		21: FILE_PATH + "21.dds",
		22: FILE_PATH + "22.dds",
		23: FILE_PATH + "23.dds",
		30: FILE_PATH + "30.dds",
		31: FILE_PATH + "31.dds",
		32: FILE_PATH + "32.dds",
		33: FILE_PATH + "33.dds",
	}

	def __GetHorseGrade(self, level):
		if 0 == level:
			return 0

		return (level - 1) / 10 + 1

	def SetState(self, level, health, battery):
		self.toolTip.ClearToolTip()

		if level == 0:
			return

		grade = self.__GetHorseGrade(level)

		try:
			self.toolTip.AppendTextLine(localeInfo.LEVEL_LIST[grade])
		except IndexError:
			return

		try:
			healthName = localeInfo.HEALTH_LIST[health]
			if healthName:
				self.toolTip.AppendTextLine(healthName)
		except IndexError:
			return

		if health > 0 and battery == 0:
			self.toolTip.AppendTextLine(localeInfo.NEEFD_REST)

		try:
			fileName = self.FILE_DICT[health * 10 + battery]
		except KeyError:
			return

		try:
			self.LoadImage(fileName)
		except:
			return
		self.toolTip.AppendSpace(30)
		# [tim] This is necessary because LoadImage() destroys the old
		# CGraphicExpandedImageInstance object...
		self.SetScale(0.7, 0.7)

class ItemImage(NAffectImage):
	def __init__(self, cell):
		NAffectImage.__init__(self)

		self.cell = cell

	def SetImage(self, filename):
		self.LoadImage(filename)
		self.SetScale(0.7, 0.7)

	def SetCell(self, cell):
		self.cell = cell
		self.__Refresh()

	def __Refresh(self):
		self.toolTip.ClearToolTip()
		self.toolTip.SetInventoryItem(self.cell)
		self.toolTip.HideToolTip()

	def Update(self):
		return

class AffectShower(ui.Window):

	MALL_DESC_IDX_START = 1000
	IMAGE_STEP = 25
	IMAGE_STEP_Y = 25
	IMAGE_PER_ROW = 12
	AFFECT_MAX_NUM = 32

	AFFECT_DATA_DICT =	{
			chr.AFFECT_POISON : (localeInfo.SKILL_TOXICDIE, "d:/ymir work/ui/skill/common/affect/poison.sub"),
			chr.AFFECT_SLOW : (localeInfo.SKILL_SLOW, "d:/ymir work/ui/skill/common/affect/slow.sub"),
			chr.AFFECT_STUN : (localeInfo.SKILL_STUN, "d:/ymir work/ui/skill/common/affect/stun.sub"),

			chr.AFFECT_ATT_SPEED_POTION : (localeInfo.SKILL_INC_ATKSPD, "d:/ymir work/ui/skill/common/affect/Increase_Attack_Speed.sub"),
			chr.AFFECT_MOV_SPEED_POTION : (localeInfo.SKILL_INC_MOVSPD, "d:/ymir work/ui/skill/common/affect/Increase_Move_Speed.sub"),
			chr.AFFECT_FISH_MIND : (localeInfo.SKILL_FISHMIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub"),

			chr.AFFECT_JEONGWI : (localeInfo.SKILL_JEONGWI, "d:/ymir work/ui/skill/warrior/jeongwi_03.sub",),
			chr.AFFECT_GEOMGYEONG : (localeInfo.SKILL_GEOMGYEONG, "d:/ymir work/ui/skill/warrior/geomgyeong_03.sub",),
			chr.AFFECT_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
			chr.AFFECT_GYEONGGONG : (localeInfo.SKILL_GYEONGGONG, "d:/ymir work/ui/skill/assassin/gyeonggong_03.sub",),
			chr.AFFECT_EUNHYEONG : (localeInfo.SKILL_EUNHYEONG, "d:/ymir work/ui/skill/assassin/eunhyeong_03.sub",),
			chr.AFFECT_GWIGEOM : (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/sura/gwigeom_03.sub",),
			chr.AFFECT_GONGPO : (localeInfo.SKILL_GONGPO, "d:/ymir work/ui/skill/sura/gongpo_03.sub",),
			chr.AFFECT_JUMAGAP : (localeInfo.SKILL_JUMAGAP, "d:/ymir work/ui/skill/sura/jumagap_03.sub"),
			chr.AFFECT_HOSIN : (localeInfo.SKILL_HOSIN, "d:/ymir work/ui/skill/shaman/hosin_03.sub",),
			chr.AFFECT_BOHO : (localeInfo.SKILL_BOHO, "d:/ymir work/ui/skill/shaman/boho_03.sub",),
			chr.AFFECT_KWAESOK : (localeInfo.SKILL_KWAESOK, "d:/ymir work/ui/skill/shaman/kwaesok_03.sub",),
			chr.AFFECT_HEUKSIN : (localeInfo.SKILL_HEUKSIN, "d:/ymir work/ui/skill/sura/heuksin_03.sub",),
			chr.AFFECT_MUYEONG : (localeInfo.SKILL_MUYEONG, "d:/ymir work/ui/skill/sura/muyeong_03.sub",),
			chr.AFFECT_GICHEON : (localeInfo.SKILL_GICHEON, "d:/ymir work/ui/skill/shaman/gicheon_03.sub",),
			chr.AFFECT_JEUNGRYEOK : (localeInfo.SKILL_JEUNGRYEOK, "d:/ymir work/ui/skill/shaman/jeungryeok_03.sub",),
			chr.AFFECT_PABEOP : (localeInfo.SKILL_PABEOP, "d:/ymir work/ui/skill/sura/pabeop_03.sub",),
			chr.AFFECT_FALLEN_CHEONGEUN : (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/warrior/cheongeun_03.sub",),
			28 : (localeInfo.SKILL_FIRE, "d:/ymir work/ui/skill/sura/hwayeom_03.sub",),
			chr.AFFECT_CHINA_FIREWORK : (localeInfo.SKILL_POWERFUL_STRIKE, "d:/ymir work/ui/skill/common/affect/powerfulstrike.sub",),

			#64 - END
			chr.NEW_AFFECT_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub",),

			chr.NEW_AFFECT_ITEM_BONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
			chr.NEW_AFFECT_SAFEBOX : (localeInfo.TOOLTIP_MALL_SAFEBOX, "d:/ymir work/ui/skill/common/affect/safebox.sub",),
			chr.NEW_AFFECT_AUTOLOOT : (localeInfo.TOOLTIP_MALL_AUTOLOOT, "d:/ymir work/ui/skill/common/affect/autoloot.sub",),
			chr.NEW_AFFECT_FISH_MIND : (localeInfo.TOOLTIP_MALL_FISH_MIND, "d:/ymir work/ui/skill/common/affect/fishmind.sub",),
			chr.NEW_AFFECT_MARRIAGE_FAST : (localeInfo.TOOLTIP_MALL_MARRIAGE_FAST, "d:/ymir work/ui/skill/common/affect/marriage_fast.sub",),
			chr.NEW_AFFECT_GOLD_BONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),

			chr.NEW_AFFECT_NO_DEATH_PENALTY : (localeInfo.TOOLTIP_APPLY_NO_DEATH_PENALTY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			chr.NEW_AFFECT_SKILL_BOOK_BONUS : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_BONUS, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY : (localeInfo.TOOLTIP_APPLY_SKILL_BOOK_NO_DELAY, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),

			chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/pattern/auto_hpgauge/05.dds"),
			chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/pattern/auto_spgauge/05.dds"),
			#chr.NEW_AFFECT_AUTO_HP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			#chr.NEW_AFFECT_AUTO_SP_RECOVERY : (localeInfo.TOOLTIP_AUTO_POTION_REST, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub"),

			MALL_DESC_IDX_START+player.POINT_MALL_ATTBONUS : (localeInfo.TOOLTIP_MALL_ATTBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/att_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_DEFBONUS : (localeInfo.TOOLTIP_MALL_DEFBONUS_STATIC, "d:/ymir work/ui/skill/common/affect/def_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_EXPBONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS, "d:/ymir work/ui/skill/common/affect/exp_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_ITEMBONUS : (localeInfo.TOOLTIP_MALL_ITEMBONUS, "d:/ymir work/ui/skill/common/affect/item_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_MALL_GOLDBONUS : (localeInfo.TOOLTIP_MALL_GOLDBONUS, "d:/ymir work/ui/skill/common/affect/gold_bonus.sub",),
			MALL_DESC_IDX_START+player.POINT_CRITICAL_PCT : (localeInfo.TOOLTIP_APPLY_CRITICAL_PCT,"d:/ymir work/ui/skill/common/affect/critical.sub"),
			MALL_DESC_IDX_START+player.POINT_PENETRATE_PCT : (localeInfo.TOOLTIP_APPLY_PENETRATE_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			MALL_DESC_IDX_START+player.POINT_MAX_HP_PCT : (localeInfo.TOOLTIP_MAX_HP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),
			MALL_DESC_IDX_START+player.POINT_MAX_SP_PCT : (localeInfo.TOOLTIP_MAX_SP_PCT, "d:/ymir work/ui/skill/common/affect/gold_premium.sub"),

			MALL_DESC_IDX_START+player.POINT_PC_BANG_EXP_BONUS : (localeInfo.TOOLTIP_MALL_EXPBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/EXP_Bonus_p_on.sub",),
			MALL_DESC_IDX_START+player.POINT_PC_BANG_DROP_BONUS: (localeInfo.TOOLTIP_MALL_ITEMBONUS_P_STATIC, "d:/ymir work/ui/skill/common/affect/Item_Bonus_p_on.sub",),
	}

	if app.ENABLE_DRAGON_SOUL_SYSTEM:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK1] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK1, "d:/ymir work/ui/dragonsoul/buff_ds_sky1.tga")
		AFFECT_DATA_DICT[chr.NEW_AFFECT_DRAGON_SOUL_DECK2] = (localeInfo.TOOLTIP_DRAGON_SOUL_DECK2, "d:/ymir work/ui/dragonsoul/buff_ds_land1.tga")

	if app.ENABLE_WOLFMAN_CHARACTER:
		AFFECT_DATA_DICT[chr.AFFECT_BLEEDING] = (localeInfo.SKILL_BLEEDING, "d:/ymir work/ui/skill/common/affect/poison.sub")
		AFFECT_DATA_DICT[chr.AFFECT_RED_POSSESSION] = (localeInfo.SKILL_GWIGEOM, "d:/ymir work/ui/skill/wolfman/red_possession_03.sub")
		AFFECT_DATA_DICT[chr.AFFECT_BLUE_POSSESSION] = (localeInfo.SKILL_CHEONGEUN, "d:/ymir work/ui/skill/wolfman/blue_possession_03.sub")

	AFFECT_DATA_DICT[chr.NEW_AFFECT_POLYMORPH] = (localeInfo.TOOLTIP_AFFECT_POLYMORPH, "assets/ui/affect/polymorph_marble.dds")
	
	if app.ENABLE_DS_SET:
		AFFECT_DATA_DICT[chr.AFFECT_DS_SET] = (localeInfo.TOOLTIP_AFFECT_DS_SET, "d:/ymir work/ui/skill/common/affect/ds_set_bonus.sub")

	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		AFFECT_DATA_DICT[chr.NEW_AFFECT_PREMIUM_PRIVATE_SHOP] = (localeInfo.TOOLTIP_AFFECT_PREMIUM_PRIVATE_SHOP, "d:/ymir work/ui/skill/common/affect/premium_private_shop.sub")
		
	TOGGLE_AFFECT = {
		173017: "assets/ui/affect/173017.dds",
		173018: "assets/ui/affect/173018.dds",

		50821: "assets/ui/affect/50821.dds",
		50822: "assets/ui/affect/50822.dds",
		50823: "assets/ui/affect/50823.dds",
		50825: "assets/ui/affect/50825.dds",
		71027: "assets/ui/affect/71027.dds",
		71028: "assets/ui/affect/71028.dds",
		71030: "assets/ui/affect/71030.dds",
		71044: "assets/ui/affect/71044.dds",
		71045: "assets/ui/affect/71045.dds",

		173001: "assets/ui/affect/173001.dds",
		173002: "assets/ui/affect/173002.dds",
		173003: "assets/ui/affect/173003.dds",
		173004: "assets/ui/affect/173004.dds",
		173006: "assets/ui/affect/173006.dds",
		173011: "assets/ui/affect/173011.dds",
		173012: "assets/ui/affect/173012.dds",
		173013: "assets/ui/affect/173013.dds",
		173015: "assets/ui/affect/173015.dds",

		173051: "assets/ui/affect/173051.dds",
		173052: "assets/ui/affect/173052.dds",
		173053: "assets/ui/affect/173053.dds",
		173054: "assets/ui/affect/173054.dds",
		173056: "assets/ui/affect/173056.dds",
		173061: "assets/ui/affect/173061.dds",
		173062: "assets/ui/affect/173062.dds",
		173063: "assets/ui/affect/173063.dds",
		173065: "assets/ui/affect/173065.dds",
		173066: "assets/ui/affect/173066.dds",
	}

	TOGGLE_DATA = {
		item.TOGGLE_AUTO_RECOVERY_HP: "assets/ui/affect/hp.dds",
		item.TOGGLE_AUTO_RECOVERY_SP: "assets/ui/affect/mp.dds",
		item.TOGGLE_PET: "assets/ui/affect/pet.dds",
		item.TOGGLE_MOUNT: "assets/ui/affect/mount.dds",
		item.TOGGLE_PICKUPER : "assets/ui/affect/pickuper.dds",
	}

	def __init__(self):
		ui.Window.__init__(self)

		self.affectImageDict = {}
		self.toggleImageDict = {}

		if gcGetEnable("ENABLE_AFFECT_TOOLTIP"):
			self.skillAffectDict = {}

		self.horseImage = None
		self.lovePointImage = None

		self.SetPosition(10, 10)
		self.Show()

		self.TOGGLE_CALLBACK = {
			item.TOGGLE_AUTO_RECOVERY_HP: MakeEvent(self.ToggleCallback_Default),
			item.TOGGLE_AUTO_RECOVERY_SP: MakeEvent(self.ToggleCallback_Default),
			item.TOGGLE_AFFECT: MakeEvent(self.ToggleCallback_ItemIcon),
			item.TOGGLE_PET: MakeEvent(self.ToggleCallback_Default),
			item.TOGGLE_MOUNT: MakeEvent(self.ToggleCallback_Default),
			item.TOGGLE_RED_SOUL: MakeEvent(self.ToggleCallback_ItemIcon),
			item.TOGGLE_BLUE_SOUL: MakeEvent(self.ToggleCallback_ItemIcon),
			item.TOGGLE_PICKUPER: MakeEvent(self.ToggleCallback_Default),
			item.TOGGLE_SHAMAN: MakeEvent(self.ToggleCallback_ItemIcon),
		}

	def ToggleCallback_Default(self, cell, itemVnum):
		image = ItemImage(cell)
		image.SetCell(cell)
		image.SetImage(self.TOGGLE_DATA[item.GetItemSubType()])
		return image

	def ToggleCallback_ItemIcon(self, cell, itemVnum):
		image = ItemImage(cell)
		image.SetCell(cell)
		if itemVnum in self.TOGGLE_AFFECT:
			image.SetImage(self.TOGGLE_AFFECT[itemVnum])
		else:
			image.SetImage(item.GetIconImageFileName())
		return image

	def ClearAllAffects(self):
		self.horseImage = None
		self.lovePointImage = None

		self.affectImageDict = {}
		self.toggleImageDict = {}

		if gcGetEnable("ENABLE_AFFECT_TOOLTIP"):
			self.skillAffectDict = {}

		self.__ArrangeImageList()

	def ClearAffects(self):
		self.living_affectImageDict = {}
		for key, image in self.affectImageDict.items():
			if not image.IsSkillAffect():
				self.living_affectImageDict[key] = image

		self.affectImageDict = self.living_affectImageDict
		self.__ArrangeImageList()

	def BINARY_NEW_AddAffect(self, type, pointIdx, value, duration):
		if type < 500 and type != chr.NEW_AFFECT_POLYMORPH:
			if gcGetEnable("ENABLE_AFFECT_TOOLTIP"):
				if type < 120:
					self.skillAffectDict[type] = app.GetGlobalTimeStamp() + duration
			return

		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		else:
			affect = type

		if self.affectImageDict.has_key(affect):
			return

		if not self.AFFECT_DATA_DICT.has_key(affect):
			return

		if affect == chr.NEW_AFFECT_NO_DEATH_PENALTY or\
			affect == chr.NEW_AFFECT_SKILL_BOOK_BONUS or\
			affect == chr.NEW_AFFECT_AUTO_SP_RECOVERY or\
			affect == chr.NEW_AFFECT_AUTO_HP_RECOVERY or\
			affect == chr.NEW_AFFECT_SKILL_BOOK_NO_DELAY:
			duration = 0

		affectData = self.AFFECT_DATA_DICT[affect]

		# TODO: Get rid of these wrappers...
		if callable(affectData[0]):
			description = affectData[0](float(value))
		else:
			try:
				description = affectData[0] % value
			except TypeError:
				description = affectData[0]
			except ValueError:
				description = affectData[0]

		if pointIdx == player.POINT_MALL_ITEMBONUS or\
			pointIdx == player.POINT_MALL_GOLDBONUS:
			value = 1 + float(value) / 100.0

		if affect != chr.NEW_AFFECT_AUTO_SP_RECOVERY and affect != chr.NEW_AFFECT_AUTO_HP_RECOVERY:
			try:
				if app.ENABLE_DS_SET and affect == chr.AFFECT_DS_SET:
					SET_PERCENTS = (10, 20, 20, 30, 40)
					value = float(SET_PERCENTS[value])
					description = description.format(float(value))
				else:
					description = description(float(value))
			except TypeError:
				pass

		if type == chr.NEW_AFFECT_POLYMORPH:
			image = PolyImage(affect, affectData[1], duration, description)
		else:
			image = SimpleAffectImage(affect, 0, affectData[1], duration, description)

		if affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK1 or affect == chr.NEW_AFFECT_DRAGON_SOUL_DECK2:
			image.SetScale(1, 1)
		else:
			image.SetScale(0.7, 0.7)

		image.SetParent(self)
		image.Show()
	
		self.affectImageDict[affect] = image
		self.__ArrangeImageList()

	def BINARY_NEW_RemoveAffect(self, type, pointIdx):
		if type == chr.NEW_AFFECT_MALL:
			affect = self.MALL_DESC_IDX_START + pointIdx
		else:
			affect = type

		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetAffect(self, affect):
		self.__AppendAffect(affect)
		self.__ArrangeImageList()

	def ResetAffect(self, affect):
		self.__RemoveAffect(affect)
		self.__ArrangeImageList()

	def SetLoverInfo(self, name, lovePoint):
		image = LovePointImage()
		image.SetParent(self)
		image.SetLoverInfo(name, lovePoint)
		self.lovePointImage = image
		self.__ArrangeImageList()

	def ShowLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Show()
			self.__ArrangeImageList()

	def HideLoverState(self):
		if self.lovePointImage:
			self.lovePointImage.Hide()
			self.__ArrangeImageList()

	def ClearLoverState(self):
		self.lovePointImage = None
		self.__ArrangeImageList()

	def OnUpdateLovePoint(self, lovePoint):
		if self.lovePointImage:
			self.lovePointImage.OnUpdateLovePoint(lovePoint)

	def SetHorseState(self, level, health, battery):
		if level==0:
			self.horseImage=None
			self.__ArrangeImageList()
		else:
			image = HorseImage()
			image.SetParent(self)
			image.SetState(level, health, battery)
			image.Show()

			self.horseImage=image
			self.__ArrangeImageList()

	def __AppendAffect(self, affect):
		if self.affectImageDict.has_key(affect):
			return

		if not self.AFFECT_DATA_DICT.has_key(affect):
			return

		affectData = self.AFFECT_DATA_DICT[affect]

		skillIndex = player.AffectIndexToSkillIndex(affect)

		iDuration = 0
		if gcGetEnable("ENABLE_AFFECT_TOOLTIP"):
			if self.skillAffectDict.has_key(skillIndex):
				iDuration = self.skillAffectDict[skillIndex] - app.GetGlobalTimeStamp()

		scale = True
		image = SimpleAffectImage(affect, 0, affectData[1], iDuration, affectData[0], scale, True)
		image.SetScale(0.7, 0.7)
		image.SetParent(self)
		image.Show()

		self.affectImageDict[affect] = image

	def __RemoveAffect(self, affect):
		if not self.affectImageDict.has_key(affect):
			return

		del self.affectImageDict[affect]
		self.__ArrangeImageList()

	def __ArrangeImageList(self):
		imageCount = len(self.affectImageDict) + len(self.toggleImageDict)

		if self.lovePointImage:
			imageCount += 1
		if self.horseImage:
			imageCount += 1

		width = min(imageCount, self.IMAGE_PER_ROW)
		height = (max(0, imageCount - 1) / self.IMAGE_PER_ROW)

		self.SetSize(width * self.IMAGE_STEP, 26 + height * self.IMAGE_STEP_Y)

		yPos = 0
		xPos = 0
		xCount = 0

		if self.lovePointImage and self.lovePointImage.IsShow():
			self.lovePointImage.SetPosition(xPos, yPos)
			xPos += self.IMAGE_STEP
			xCount += 1

		if self.horseImage:
			self.horseImage.SetPosition(xPos, yPos)
			xPos += self.IMAGE_STEP
			xCount += 1

		for image in self.affectImageDict.values():
			image.SetPosition(xPos, yPos)
			xPos += self.IMAGE_STEP
			xCount += 1

			if xCount >= self.IMAGE_PER_ROW:
				xPos = 0
				xCount = 0
				yPos += self.IMAGE_STEP_Y

		for image in self.toggleImageDict.values():
			image.SetPosition(xPos, yPos)
			xPos += self.IMAGE_STEP
			xCount += 1

			if xCount >= self.IMAGE_PER_ROW:
				xPos = 0
				xCount = 0
				yPos += self.IMAGE_STEP_Y

	def ArrangeImageList(self):
		self.__ArrangeImageList()

	def __TryDeleteToggleItem(self, cell):
		# We don't have an image for this item...
		# i.e. nothing to do
		if cell not in self.toggleImageDict:
			return

		self.toggleImageDict[cell] = None
		del self.toggleImageDict[cell]

	def RefreshInventory(self):
		# self.toggleImageDict.clear()

		for cell in xrange(player.INVENTORY_SLOT_COUNT):
			itemVnum = player.GetItemIndex(player.INVENTORY, cell)
			if itemVnum == 0:
				self.__TryDeleteToggleItem(cell)
				continue

			item.SelectItem(itemVnum)

			if item.GetItemType() != item.ITEM_TYPE_TOGGLE:
				self.__TryDeleteToggleItem(cell)
				continue

			if 0 != player.GetItemMetinSocket(cell, 3):
				# We already have an image...
				# i.e. nothing to do.
				if cell in self.toggleImageDict:
					continue

				image = self.TOGGLE_CALLBACK[item.GetItemSubType()](cell, itemVnum)
				image.SetParent(self)
				image.Show()

				self.toggleImageDict[cell] = image
			else:
				self.__TryDeleteToggleItem(cell)

		self.__ArrangeImageList()

	def OnUpdate(self):
		for image in self.affectImageDict.values():
			try:
				image.Update()
			except Exception as e:
				print("Error during affect-image update")

		for image in self.toggleImageDict.values():
			try:
				image.Update()
			except Exception as e:
				print("Error during item-image update")
