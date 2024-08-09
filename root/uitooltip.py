#-*- coding: iso-8859-1 -*-
from introinterface import gcGetEnable
import dbg
import player
import item
import grp
import wndMgr
import skill
import shop
import exchange
import grpText
import safebox
import localeInfo
import app
import background
import nonplayer
import chr

import ui
import mouseModule
import constInfo

import introInterface

import uiScriptLocale

if app.ENABLE_REFINE_ELEMENT:
	import chrmgr

import localeInfo

from _weakref import proxy

import colorInfo

import equipmentSet

import math

from cff import CFF

import util

if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	import privateShop

WARP_SCROLLS = [22011, 22000, 22010]

DESC_DEFAULT_MAX_COLS = 26
DESC_WESTERN_MAX_COLS = 35
DESC_WESTERN_MAX_WIDTH = 220

def chop(n):
	return round(n - 0.5, 1)

if app.INGAME_WIKI:
	def GET_AFFECT_STRING(affType, affValue):
		if 0 == affType:
			return None

		try:
			affectString = localeInfo.AFFECT_DICT[affType]
			if type(affectString) != str:
				return affectString(affValue)

			if affectString.find("%d") != -1:
				return affectString % affValue
			else:
				return affectString
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affType, affValue)

def SplitDescription(desc, limit):
	total_tokens = desc.split()
	line_tokens = []
	line_len = 0
	lines = []
	for token in total_tokens:
		if "|" in token:
			sep_pos = token.find("|")
			line_tokens.append(token[:sep_pos])

			lines.append(" ".join(line_tokens))
			line_len = len(token) - (sep_pos + 1)
			line_tokens = [token[sep_pos+1:]]
		else:
			line_len += len(token)
			if len(line_tokens) + line_len > limit:
				lines.append(" ".join(line_tokens))
				line_len = len(token)
				line_tokens = [token]
			else:
				line_tokens.append(token)

	if line_tokens:
		lines.append(" ".join(line_tokens))

	return lines

###################################################################################################
## ToolTip
##
##
class ToolTip(ui.ThinBoard):

	TOOL_TIP_WIDTH = 190
	TOOL_TIP_HEIGHT = 10

	TEXT_LINE_HEIGHT = 17

	TITLE_COLOR = grp.GenerateColor(0.9490, 0.9058, 0.7568, 1.0)
	SPECIAL_TITLE_COLOR = grp.GenerateColor(1.0, 0.7843, 0.0, 1.0)
	NORMAL_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	PRICE_COLOR = 0xffFFB96D

	HIGH_PRICE_COLOR = SPECIAL_TITLE_COLOR
	MIDDLE_PRICE_COLOR = grp.GenerateColor(0.85, 0.85, 0.85, 1.0)
	LOW_PRICE_COLOR = grp.GenerateColor(0.7, 0.7, 0.7, 1.0)

	ENABLE_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)
	DISABLE_COLOR = grp.GenerateColor(0.9, 0.4745, 0.4627, 1.0)

	NEGATIVE_COLOR = 0xFFe57875
	POSITIVE_COLOR = grp.GenerateColor(0.5411, 0.7254, 0.5568, 1.0)
	SPECIAL_POSITIVE_COLOR = grp.GenerateColor(0.6911, 0.8754, 0.7068, 1.0)
	SPECIAL_POSITIVE_COLOR2 = grp.GenerateColor(0.8824, 0.9804, 0.8824, 1.0)

	CONDITION_COLOR = 0xffBEB47D
	CAN_LEVEL_UP_COLOR = 0xff8EC292
	CANNOT_LEVEL_UP_COLOR = DISABLE_COLOR
	NEED_SKILL_POINT_COLOR = 0xff9A9CDB

	VNUM_COLOR = 0xffEF0ED5
	SPECIAL_COLOR_GOLD = 0xFFff8800

	if app.ENABLE_SASH_COSTUME_SYSTEM:
		ABSORPTION_TITLE_COLOR = 0xffffcc00

	if app.ENABLE_TRANSMUTATION_SYSTEM:
		TRANSMUTATION_TITLE_COLOR = 0xff8BBDFF
		TRANSMUTATION_ITEMNAME_COLOR = 0xffBCE55C

	if app.ENABLE_REFINE_ELEMENT:
		REFINE_ELEMENT_TITLE_TEXT_GAP = 10

		REFINE_ELEMENT_BONUS_COLOR = 0xFF764773
		REFINE_ELEMENT_COLOR_DICT = {
			chrmgr.REFINE_ELEMENT_CATEGORY_ELECT : 0xFF23B7E8,
			chrmgr.REFINE_ELEMENT_CATEGORY_FIRE : 0xFFDD483B,
			chrmgr.REFINE_ELEMENT_CATEGORY_ICE : 0xFF3D6CDF,
			chrmgr.REFINE_ELEMENT_CATEGORY_WIND : 0xFF37CF21,
			chrmgr.REFINE_ELEMENT_CATEGORY_EARTH : 0xFFF4CA14,
			chrmgr.REFINE_ELEMENT_CATEGORY_DARK : 0xFFB72EEC,
		}

	SET_COLOR = grp.GenerateColor(0.537, 0.941, 0.780, 1.0)

	ACTUAL_POINTS_TITLE = 0xFFffd169
	NEXT_SKILL_LEVEL = 0xff134206

	COLOR_CONFIGURATION = {
		POSITIVE_COLOR : "89ff8d",
		SPECIAL_POSITIVE_COLOR : "89ff8d",
		SPECIAL_COLOR_GOLD : "ffba6b",
		NEGATIVE_COLOR : "ff6460",
		NORMAL_COLOR : "dddddd"
	}


	def __init__(self, width = TOOL_TIP_WIDTH, isPickable=False):
		ui.ThinBoard.__init__(self, "TOP_MOST")

		if isPickable:
			pass
		else:
			self.AddFlag("not_pick")

		self.AddFlag("float")

		self.followFlag = True
		self.toolTipWidth = width
		self.TOOL_TIP_WIDTH = width

		self.xPos = -1
		self.yPos = -1

		self.defFontName = localeInfo.UI_DEF_FONT
		self.ClearToolTip()

	def __del__(self):
		ui.ThinBoard.__del__(self)

	def ClearToolTip(self):
		self.toolTipWidth = self.TOOL_TIP_WIDTH
		self.toolTipHeight = 12
		self.childrenList = []

	def SetFollow(self, flag):
		self.followFlag = flag

	def SetDefaultFontName(self, fontName):
		self.defFontName = fontName

	def AppendSpace(self, size):
		self.toolTipHeight += size
		self.ResizeToolTip()

	def AppendHorizontalLine(self):

		for i in xrange(2):
			horizontalLine = ui.Line()
			horizontalLine.SetParent(self)
			horizontalLine.SetPosition(0, self.toolTipHeight + 3 + i)
			horizontalLine.SetWindowHorizontalAlignCenter()
			horizontalLine.SetSize(150, 0)
			horizontalLine.Show()

			if 0 == i:
				horizontalLine.SetColor(0xff555555)
			else:
				horizontalLine.SetColor(0xff000000)

			self.childrenList.append(horizontalLine)

		self.toolTipHeight += 11
		self.ResizeToolTip()

	def AlignHorizonalCenter(self):
		for child in self.childrenList:
			(x, y) = child.GetLocalPosition()
			child.SetPosition(0, y)
			child.SetWindowHorizontalAlignCenter()

		self.ResizeToolTip()

	def AutoAppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.isCenterAlign = centerAlign
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(0, self.toolTipHeight)
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		(textWidth, textHeight)=textLine.GetTextSize()

		textWidth += 40
		textHeight += 5

		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		self.toolTipHeight += textHeight

		return textLine

	def AutoAppendNewTextLineResize(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()

		(textWidth, textHeight) = textLine.GetTextSize()
		textWidth += 30
		textHeight += 10
		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		if centerAlign:
			textLine.SetPosition(self.toolTipWidth/2, self.toolTipHeight)
			textLine.SetHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.AlignHorizonalCenter()
		return textLine

	def AutoAppendNewTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(False)
		textLine.Show()
		textLine.SetPosition(15, self.toolTipHeight)

		self.childrenList.append(textLine)
		(textWidth, textHeight) = textLine.GetTextSize()
		textWidth += 30
		textHeight += 10
		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		self.toolTipHeight += textHeight
		self.ResizeToolTipText(textWidth, self.toolTipHeight)
		return textLine

	def SetThinBoardSize(self, width, height = 12):
		self.toolTipWidth = width
		self.toolTipHeight = height

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = TRUE):
		textLine = ui.TextLine()
		textLine.SetParent(self)
		textLine.SetFontName(self.defFontName)
		textLine.SetPackedFontColor(color)
		textLine.SetText(text)
		textLine.SetOutline()
		textLine.SetFeather(FALSE)
		textLine.isCenterAlign = centerAlign
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(0, self.toolTipHeight)
			textLine.SetWindowHorizontalAlignCenter()
			textLine.SetHorizontalAlignCenter()

		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		(textWidth, textHeight)=textLine.GetTextSize()

		textWidth += 40

		if self.toolTipWidth < textWidth:
			self.toolTipWidth = textWidth

		self.toolTipHeight += self.TEXT_LINE_HEIGHT
		self.ResizeToolTip()

		return textLine

	def AppendTextLineEx(self, text, centerAlign = False):
		textLine = ui.ExtendedTextLine()
		textLine.SetParent(self)
		textLine.SetText(text)
		textLine.Show()

		if centerAlign:
			textLine.SetPosition(0, self.toolTipHeight)
			textLine.SetWindowHorizontalAlignCenter()
		else:
			textLine.SetPosition(10, self.toolTipHeight)

		self.childrenList.append(textLine)

		self.toolTipHeight += textLine.GetHeight()
		self.ResizeToolTip()

		return textLine

	if app.ENABLE_ADMIN_MANAGER:
		def AppendExtendedTextLine(self, text, centerAlign = True):
			textLine = ui.ExtendedTextLine()
			textLine.SetParent(self)
			textLine.SetText(text)
			textLine.Show()

			if centerAlign:
				textLine.SetPosition(0, self.toolTipHeight)
				textLine.SetWindowHorizontalAlignCenter()

			else:
				textLine.SetPosition(10, self.toolTipHeight)

			self.childrenList.append(textLine)

			self.toolTipHeight += self.TEXT_LINE_HEIGHT
			self.ResizeToolTip()

			return textLine

		def AppendImage(self, image, centerAlign = True, yChange = 0):
			imageBox = ui.ImageBox()
			imageBox.SetParent(self)
			imageBox.LoadImage(image)
			imageBox.Show()

			if centerAlign:
				imageBox.SetPosition(0, self.toolTipHeight + yChange)
				imageBox.SetWindowHorizontalAlignCenter()

			else:
				imageBox.SetPosition(10, self.toolTipHeight + yChange)

			self.childrenList.append(imageBox)

			self.toolTipHeight += imageBox.GetHeight() + 2 + yChange
			self.ResizeToolTip()

			return imageBox

	if gcGetEnable("ENABLE_FAST_INTERACTIONS"):
		def AppendShortcut(self, shortcut, description, bColor = 0xFFffffff, bCenter = False, bSpace = True):
			if bSpace:
				self.AppendSpace(2)

			wrapper = ui.Window()
			wrapper.AddFlag("not_pick")
			wrapper.SetParent(self)
			wrapper.Show()
			wrapper.childrenList = []

			sc = ui.Shortcut()
			sc.SetParent(wrapper)
			sc.SetShortcut(shortcut)
			sc.Show()
			wrapper.childrenList.append(sc)

			desc = ui.TextLine()
			desc.SetParent(wrapper)
			desc.SetPosition(5, 2)
			desc.SetWindowHorizontalAlignRight()
			desc.SetHorizontalAlignRight()
			desc.SetText(" - " + description)
			desc.SetOutline()
			desc.SetPackedFontColor(bColor)
			desc.Show()
			wrapper.childrenList.append(desc)

			wrapper.SetSize(sc.GetWidth() + 5 + desc.GetTextWidth(), sc.GetHeight())

			wrapper.SetPosition(10, self.toolTipHeight)
			
			self.AppendChild(wrapper, bCenter)

			return wrapper

	def AppendTupleImages(self, images, space = 0):
		self.AppendSpace(3)

		wrapper = ui.Window()
		wrapper.SetParent(self)
		wrapper.Show()
		wrapper.childrenList = []

		x = 0
		height = 0
		for image in images:
			mImage = ui.ImageBox()
			mImage.SetParent(wrapper)
			mImage.LoadImage(image)
			mImage.SetPosition(x, 0)
			mImage.Show()

			x += mImage.GetWidth() - space
			if height < mImage.GetHeight():
				height = mImage.GetHeight()

			wrapper.childrenList.append(mImage)

		wrapper.SetSize(x, height)
		wrapper.SetPosition(10, self.toolTipHeight)

		self.AppendChild(wrapper, True)

		return wrapper

	def AppendRenderTarget(self, width = 100, height = 200, data = {}):
		renderTarget = ui.RenderTarget()
		renderTarget.SetParent(self)
		renderTarget.SetWindowHorizontalAlignCenter()
		renderTarget.SetPosition(0, self.toolTipHeight)
		renderTarget.SetSize(width, height)
		renderTarget.LoadImage("d:/ymir work/ui/game/myshop_deco/model_view_bg.sub")
		renderTarget.SetRenderTarget(chr.GetRace())

		iTypes = {
			item.ITEM_TYPE_WEAPON : renderTarget.SetWeapon(data['iValue']),
		}
		
		if not iTypes.has_key(data['iType']):
			return

		renderTarget.Show()


		self.AppendChild(renderTarget)
		
		return renderTarget

	def AppendChild(self, child, bCenter = True):
		child.SetParent(self)

		if bCenter:
			child.SetPosition(0, self.toolTipHeight)
			child.SetWindowHorizontalAlignCenter()

		self.childrenList.append(child)
		
		if (self.toolTipWidth < child.GetWidth()):
			self.toolTipWidth += child.GetWidth() - self.toolTipWidth + 25

		self.toolTipHeight += child.GetHeight()
		self.ResizeToolTip()

	def AppendDescription(self, desc, limit, color = FONT_COLOR):
		self.__AppendDescription_WesternLanguage(desc, color)

	def __AppendDescription_WesternLanguage(self, desc, color=FONT_COLOR):
		lines = SplitDescription(desc, DESC_WESTERN_MAX_COLS)
		if not lines:
			return

		for line in lines:
			self.AppendTextLine(line, color)

	def ResizeToolTip(self):
		self.SetSize(self.toolTipWidth, self.TOOL_TIP_HEIGHT + self.toolTipHeight)

	def ResizeToolTipX(self, x):
		self.SetSize(x, self.TOOL_TIP_HEIGHT + self.toolTipHeight)

	def ResizeToolTipText(self, x, y):
		self.SetSize(x, y)

	def SetTitle(self, name):
		self.AppendTextLine(name, self.TITLE_COLOR)

	def GetLimitTextLineColor(self, curValue, limitValue):
		if curValue < limitValue:
			return self.DISABLE_COLOR

		return self.ENABLE_COLOR

	def GetChangeTextLineColor(self, value, isSpecial=False, type = -1):
		if app.ENABLE_12ZI_ELEMENT_ADD:
			if type in self.TAB_COLOR:
				return self.TAB_COLOR[type]

		if value > 0:
			if isSpecial:
				return self.SPECIAL_POSITIVE_COLOR
			else:
				return self.POSITIVE_COLOR

		if 0 == value:
			return self.NORMAL_COLOR

		return self.NEGATIVE_COLOR

	def SetToolTipPosition(self, x = -1, y = -1):
		self.xPos = x
		self.yPos = y

	def RectSize(self, width, height):
		self.toolTipHeight = int(height)
		self.toolTipWidth = int(width)
		self.ResizeToolTip()
		self.UpdateRect()

	def ShowToolTip(self):
		self.SetTop()
		self.Show()

		self.OnUpdate()

	def HideToolTip(self):
		self.Hide()

	def OnUpdate(self):

		if not self.followFlag:
			return

		x = 0
		y = 0
		width = self.GetWidth()
		height = self.toolTipHeight

		if -1 == self.xPos and -1 == self.yPos:

			(mouseX, mouseY) = wndMgr.GetMousePosition()

			if mouseY < wndMgr.GetScreenHeight() - 300:
				y = mouseY + 40
			else:
				y = mouseY - height - 30

			x = mouseX - width/2

		else:

			x = self.xPos - width/2
			y = self.yPos - height

		x = max(x, 0)
		y = max(y, 0)
		x = min(x + width/2, wndMgr.GetScreenWidth() - width/2) - width/2
		y = min(y + self.GetHeight(), wndMgr.GetScreenHeight()) - self.GetHeight()

		parentWindow = self.GetParentProxy()
		if parentWindow:
			(gx, gy) = parentWindow.GetGlobalPosition()
			x -= gx
			y -= gy

		self.SetPosition(x, y)

class ItemToolTip(ToolTip):
	GENERAL_INFO_COLOR = ToolTip.ENABLE_COLOR

	CHARACTER_NAMES = (
		localeInfo.TOOLTIP_WARRIOR,
		localeInfo.TOOLTIP_ASSASSIN,
		localeInfo.TOOLTIP_SURA,
		localeInfo.TOOLTIP_SHAMAN
	)
	if app.ENABLE_WOLFMAN_CHARACTER:
		CHARACTER_NAMES += (
			localeInfo.TOOLTIP_WOLFMAN,
		)

	CHARACTER_COUNT = len(CHARACTER_NAMES)
	WEAR_NAMES = (
		localeInfo.TOOLTIP_ARMOR,
		localeInfo.TOOLTIP_HELMET,
		localeInfo.TOOLTIP_SHOES,
		localeInfo.TOOLTIP_WRISTLET,
		localeInfo.TOOLTIP_WEAPON,
		localeInfo.TOOLTIP_NECK,
		localeInfo.TOOLTIP_EAR,
		localeInfo.TOOLTIP_UNIQUE,
		localeInfo.TOOLTIP_SHIELD,
		localeInfo.TOOLTIP_ARROW,
	)
	WEAR_COUNT = len(WEAR_NAMES)

	MAX_AFF_DICT = {
		item.APPLY_MAX_HP : 2000,
		item.APPLY_MAX_SP : 80,
		item.APPLY_CON : 12,
		item.APPLY_INT : 12,
		item.APPLY_STR : 12,
		item.APPLY_DEX : 12,
		item.APPLY_ATT_SPEED : 8,
		item.APPLY_MOV_SPEED : 20,
		item.APPLY_CAST_SPEED : 20,
		item.APPLY_HP_REGEN : 30,
		item.APPLY_SP_REGEN : 30,
		item.APPLY_POISON_PCT : 8,
		item.APPLY_STUN_PCT : 8,
		item.APPLY_SLOW_PCT : 8,
		item.APPLY_CRITICAL_PCT : 10,
		item.APPLY_PENETRATE_PCT : 10,
		item.APPLY_ATTBONUS_HUMAN : 10,
		item.APPLY_ATTBONUS_ANIMAL : 20,
		item.APPLY_ATTBONUS_ORC : 20,
		item.APPLY_ATTBONUS_MILGYO : 20,
		item.APPLY_ATTBONUS_UNDEAD : 20,
		item.APPLY_ATTBONUS_DEVIL : 20,
		item.APPLY_STEAL_HP : 10,
		item.APPLY_STEAL_SP : 10,
		item.APPLY_MANA_BURN_PCT : 10,
		item.APPLY_BLOCK : 15,
		item.APPLY_DODGE : 15,
		item.APPLY_RESIST_SWORD : 15,
		item.APPLY_RESIST_TWOHAND : 15,
		item.APPLY_RESIST_DAGGER : 15,
		item.APPLY_RESIST_BELL : 15,
		item.APPLY_RESIST_FAN : 15,
		item.APPLY_RESIST_BOW : 15,
		item.APPLY_RESIST_MAGIC : 15,
		item.APPLY_REFLECT_MELEE : 10,
		item.APPLY_POISON_REDUCE : 5,
		item.APPLY_RESIST_ELEC : 15,
		item.APPLY_RESIST_FIRE : 15,
		item.APPLY_IMMUNE_STUN : 1,
		item.APPLY_IMMUNE_SLOW : 1,
		item.APPLY_ATT_GRADE_BONUS : 50,
		item.APPLY_RESIST_WIND : 15,
		item.APPLY_EXP_DOUBLE_BONUS : 20,
		item.APPLY_GOLD_DOUBLE_BONUS : 20,
		item.APPLY_ITEM_DROP_BONUS : 20,
	}

	ATTRIBUTE_NEED_WIDTH = {
		23 : 230,
		24 : 230,
		25 : 230,
		26 : 220,
		27 : 210,

		35 : 210,
		36 : 210,
		37 : 210,
		38 : 210,
		39 : 210,
		40 : 210,
		41 : 210,

		42 : 220,
		43 : 230,
		45 : 230,
	}

	ANTI_FLAG_DICT = {
		0 : item.ITEM_ANTIFLAG_WARRIOR,
		1 : item.ITEM_ANTIFLAG_ASSASSIN,
		2 : item.ITEM_ANTIFLAG_SURA,
		3 : item.ITEM_ANTIFLAG_SHAMAN,
	}
	if app.ENABLE_WOLFMAN_CHARACTER:
		ANTI_FLAG_DICT.update({
			4 : item.ITEM_ANTIFLAG_WOLFMAN,
		})

	if app.ENABLE_REFINE_ELEMENT:
		REFINE_ELEMENT_TEXT_INFO_INFO = {
			chrmgr.REFINE_ELEMENT_CATEGORY_ELECT : ( localeInfo.REFINE_ELEMENT_TEXT_ELECT, localeInfo.TOOLTIP_APPLY_ENCHANT_ELECT, localeInfo.TOOLTIP_APPLY_ENCHANT_ELECT2 ),
			chrmgr.REFINE_ELEMENT_CATEGORY_FIRE : ( localeInfo.REFINE_ELEMENT_TEXT_FIRE, localeInfo.TOOLTIP_APPLY_ENCHANT_FIRE, localeInfo.TOOLTIP_APPLY_ENCHANT_FIRE2 ),
			chrmgr.REFINE_ELEMENT_CATEGORY_ICE : ( localeInfo.REFINE_ELEMENT_TEXT_ICE, localeInfo.TOOLTIP_APPLY_ENCHANT_ICE, localeInfo.TOOLTIP_APPLY_ENCHANT_ICE2 ),
			chrmgr.REFINE_ELEMENT_CATEGORY_WIND : ( localeInfo.REFINE_ELEMENT_TEXT_WIND, localeInfo.TOOLTIP_APPLY_ENCHANT_WIND, localeInfo.TOOLTIP_APPLY_ENCHANT_WIND2 ),
			chrmgr.REFINE_ELEMENT_CATEGORY_EARTH : ( localeInfo.REFINE_ELEMENT_TEXT_EARTH, localeInfo.TOOLTIP_APPLY_ENCHANT_EARTH, localeInfo.TOOLTIP_APPLY_ENCHANT_EARTH2 ),
			chrmgr.REFINE_ELEMENT_CATEGORY_DARK : ( localeInfo.REFINE_ELEMENT_TEXT_DARK, localeInfo.TOOLTIP_APPLY_ENCHANT_DARK, localeInfo.TOOLTIP_APPLY_ENCHANT_DARK2 ),
		}

	if app.ENABLE_12ZI_ELEMENT_ADD:
		ITEM_ELECT = 0xff33FFFF
		ITEM_FIRE = 0xfffe661b
		ITEM_ICE = 0xff067d8c
		ITEM_WIND = 0xff0fcc08
		ITEM_EARTH = 0xff8c7106
		ITEM_DARK = 0xff8314b7
		ITEM_CZ = 0xffFFFF33
		ITEM_INSECT = 0xffFFD700
		ITEM_DESERT = 0xff00C0F0

		TAB_COLOR = {
			item.APPLY_ENCHANT_ELECT : ITEM_ELECT,
			item.APPLY_RESIST_ELEC : ITEM_ELECT,

			item.APPLY_ENCHANT_FIRE : ITEM_FIRE,
			item.APPLY_RESIST_FIRE : ITEM_FIRE,

			item.APPLY_ENCHANT_ICE : ITEM_ICE,
			item.APPLY_RESIST_ICE : ITEM_ICE,

			item.APPLY_ENCHANT_WIND : ITEM_WIND,
			item.APPLY_RESIST_WIND : ITEM_WIND,

			item.APPLY_ENCHANT_EARTH : ITEM_EARTH,
			item.APPLY_RESIST_EARTH : ITEM_EARTH,

			item.APPLY_ENCHANT_DARK : ITEM_DARK,
			item.APPLY_RESIST_DARK : ITEM_DARK,

			item.APPLY_ATTBONUS_CZ : ITEM_CZ,
			item.APPLY_ATTBONUS_INSECT : ITEM_INSECT,
			item.APPLY_ATTBONUS_DESERT : ITEM_DESERT,
		}

	if gcGetEnable("ENABLE_TOOLTIP_CATEGORIES"):
		CATEGORIES_GENERAL = {
			item.ITEM_TYPE_TOGGLE: "Aktywne",
			item.ITEM_TYPE_USE: "U�yteczne",
			item.ITEM_TYPE_UNIQUE: "Wyj�tkowe",
			item.ITEM_TYPE_QUEST: "Questowe",
			item.ITEM_TYPE_GIFTBOX: "Szkatu�ka",
			item.ITEM_TYPE_COSTUME: "Kostium",
			item.ITEM_TYPE_MATERIAL: "Materia�",
			item.ITEM_TYPE_POLYMORPH: "Polimorfia",
			item.ITEM_TYPE_RING: "Pier�cie�",
			item.ITEM_TYPE_LUCKY_BOX: "Szkatu�ka Losowo�ci",
		}

		CATEGORIES_SPECIFIC = {
			#Toggle Items
			(item.ITEM_TYPE_TOGGLE, item.TOGGLE_AFFECT): "Dzia�aj�ce",
			(item.ITEM_TYPE_TOGGLE, item.TOGGLE_PET): "Pet",
			(item.ITEM_TYPE_TOGGLE, item.TOGGLE_MOUNT): "Mount",

			#Material Items
			(item.ITEM_TYPE_MATERIAL, item.MATERIAL_DS_REFINE_NORMAL): "Alchemia Ulepszanie",
			(item.ITEM_TYPE_MATERIAL, item.MATERIAL_DS_REFINE_BLESSED): "Alchemia Ulepszanie",
			(item.ITEM_TYPE_MATERIAL, item.MATERIAL_DS_REFINE_HOLLY): "Alchemia Ulepszanie",
			#Use Items
			(item.ITEM_TYPE_USE, item.USE_SPECIAL): "Specjalne",
			(item.ITEM_TYPE_USE, item.USE_TUNING): "Polepszenie",
			(item.ITEM_TYPE_USE, item.USE_ADD_ATTRIBUTE): "Dodaj Bonus",
			(item.ITEM_TYPE_USE, item.USE_ADD_ATTRIBUTE2): "Dodaj Bonus",
			(item.ITEM_TYPE_USE, item.USE_CHANGE_ATTRIBUTE): "Zmie� Bonus",
			(item.ITEM_TYPE_USE, item.USE_TIME_CHARGE_PER): "Alchemia Czas",
			(item.ITEM_TYPE_USE, item.USE_TIME_CHARGE_FIX): "Alchemia Czas",
			#Costume Items
			(item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_BODY): "Kostium",
			(item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_WEAPON): "Nak�adka",
			(item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_HAIR): "Fryzura",
			(item.ITEM_TYPE_COSTUME, item.COSTUME_TYPE_SASH): "Szarfa",
		}

	FONT_COLOR = grp.GenerateColor(0.7607, 0.7607, 0.7607, 1.0)

	def __init__(self, *args, **kwargs):
		self.dataToolTip = None

		ToolTip.__init__(self, *args, **kwargs)
		self.itemVnum = 0
		self.isShopItem = False
		
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.isPrivateSearchItem = False
			self.isPrivateShopSaleItem = False

		if app.ENABLE_REFINE_ELEMENT:
			self.isRefineElement = -1
			self.bRefineElementType = -1

		self.dataToolTip = ItemDataToolTip(self)

		self.interface = None

		self.refreshFunc = None
		self.refreshArgs = None
		self.refreshFuncAdd = None
		self.refreshArgsAdd = None
		self.lastRefreshTime = 0

		self.bCannotUseItemForceSetDisableColor = True

	def __del__(self):
		ToolTip.__del__(self)

	def ShowToolTip(self):
		ToolTip.ShowToolTip(self)

		# if app.IsPressed(app.DIK_LALT) and player.IsGameMaster():
		# 	if self.dataToolTip:
		# 		self.dataToolTip.ShowToolTip()

	def HideToolTip(self):
		ToolTip.HideToolTip(self)

		if self.dataToolTip:
			self.dataToolTip.HideToolTip()

	def SetCannotUseItemForceSetDisableColor(self, enable):
		self.bCannotUseItemForceSetDisableColor = enable

	def CanEquip(self):
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.isPrivateSearchItem or self.isPrivateShopSaleItem:
				return True
				
		if not item.IsEquipmentVID(self.itemVnum):
			return True

		race = player.GetRace()
		job = chr.RaceToJob(race)
		if not self.ANTI_FLAG_DICT.has_key(job):
			return False

		if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
			return False

		sex = chr.RaceToSex(race)

		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			return False

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == FEMALE:
			return False

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if item.LIMIT_LEVEL == limitType:
				if player.GetStatus(player.LEVEL) < limitValue:
					return False
			"""
			elif item.LIMIT_STR == limitType:
				if player.GetStatus(player.ST) < limitValue:
					return False
			elif item.LIMIT_DEX == limitType:
				if player.GetStatus(player.DX) < limitValue:
					return False
			elif item.LIMIT_INT == limitType:
				if player.GetStatus(player.IQ) < limitValue:
					return False
			elif item.LIMIT_CON == limitType:
				if player.GetStatus(player.HT) < limitValue:
					return False
			"""

		return True

	def AppendTextLine(self, text, color = FONT_COLOR, centerAlign = True):
		#if not self.CanEquip() and self.bCannotUseItemForceSetDisableColor:
		#	color = self.DISABLE_COLOR

		return ToolTip.AppendTextLine(self, text, color, centerAlign)

	def ClearToolTip(self):
		self.isShopItem = False
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.isPrivateSearchItem = False
			self.isPrivateShopSaleItem = False

		if app.ENABLE_REFINE_ELEMENT:
			self.isRefineElement = -1
			self.bRefineElementType = -1

		self.toolTipWidth = self.TOOL_TIP_WIDTH

		self.__ClearRefreshFunc()
		ToolTip.ClearToolTip(self)

		if self.dataToolTip:
			self.dataToolTip.ClearToolTip()

	def __SetRefreshFunc(self, func, *args):
		self.__ClearRefreshFunc()

		self.refreshFunc = func
		self.refreshArgs = args

	def SetRefreshFunc(self, func, *args):
		apply(self.__SetRefreshFunc, (func,) + args)
	
	"""ENABLE_LEGENDARY_STONES"""
	def SetInventoryItem(self, slotIndex, window_type = player.INVENTORY, bLegendaryStoneRefine = False):
		itemVnum = player.GetItemIndex(window_type, slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = [player.GetItemMetinSocket(window_type, slotIndex, i) for i in xrange(player.METIN_SOCKET_MAX_NUM)]
		attrSlot = [player.GetItemAttribute(window_type, slotIndex, i) for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM)]

		self.__SetRefreshFunc(self.SetInventoryItem, slotIndex, window_type)

		transmutate = player.GetItemTransmutate(window_type, slotIndex)
		refineElement = player.GetItemRefineElement(window_type, slotIndex)
		"""ENABLE_LEGENDARY_STONES"""
		self.AddItemData(itemVnum, metinSlot, attrSlot, 0, trans_id = transmutate, refineElement = refineElement, bLegendaryStoneRefine = bLegendaryStoneRefine, window_type = window_type, slot_index = slotIndex, auxiliaryDict = player.GetAuxiliaryString(window_type, slotIndex))
	
	def InventoryAppendSellingPrice(self, slotIndex):
		itemVnum = player.GetItemIndex(player.INVENTORY, slotIndex)
		if 0 == itemVnum:
			return

		if shop.IsOpen():
			if not shop.IsPrivateShop():
				self.AppendHorizontalLine()
				item.SelectItem(itemVnum)
				self.AppendSellingPrice(player.GetISellItemPrice(player.INVENTORY, slotIndex))

	def BindInterface(self, interface):
		self.interface = interface

	def SetShopItem(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		priceVnum = shop.GetItemPriceVnum(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			transmutate = shop.GetItemTransmutate(slotIndex)
			if app.ENABLE_REFINE_ELEMENT:
				refineElement = shop.GetItemRefineElement(slotIndex)
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, trans_id = transmutate, refineElement = refineElement, shortcustHelper = introInterface.SHOP_WND)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, trans_id = transmutate)
		else:
			if app.ENABLE_REFINE_ELEMENT:
				refineElement = shop.GetItemRefineElement(slotIndex)
				self.AddItemData(itemVnum, metinSlot, attrSlot, refineElement = refineElement)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)

		if gcGetEnable("ANCIENT_SHOP_MULTIPLE_BUY"):
			import uiShop
			if (uiShop.ShopDialog.ToolTipGetter):
				self.AppendShortcut([app.DIK_LCONTROL, app.DIK_LSHIFT, app.DIK_RMBUTTON], localeInfo.TOOLTIP_FAST_INTERACTION_BUY_MULTIPLE)

		self.AppendHorizontalLine()

		if priceVnum != 0:
			self.AppendPriceItem(price, priceVnum)
		else:
			self.AppendPrice(price)

	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def SetPrivateShopItem(self, slotIndex):
			itemVnum = privateShop.GetItemVnum(slotIndex)
			if 0 == itemVnum:
				return

			self.ClearToolTip()
			
			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(privateShop.GetItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(privateShop.GetItemAttribute(slotIndex, i))

			self.AddItemData(itemVnum, metinSlot, attrSlot)
			
			if app.ENABLE_PRIVATE_SHOP_CHEQUE:
				goldPrice = privateShop.GetItemPrice(slotIndex)
				chequePrice = privateShop.GetChequeItemPrice(slotIndex)
				self.AppendSellingPrice(goldPrice, chequePrice, True)
			else:
				self.AppendSellingPrice(privateShop.GetItemPrice(slotIndex))
				
				
		def SetPrivateShopSearchItem(self, slotIndex):
			itemVnum = privateShop.GetSearchItemVnum(slotIndex)
			if 0 == itemVnum:
				return
				
			self.ClearToolTip()
			self.isPrivateSearchItem = True
			
			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(privateShop.GetSearchItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(privateShop.GetSearchItemAttribute(slotIndex, i))

			self.AddItemData(itemVnum, metinSlot, attrSlot)
			
		def SetPrivateShopSaleItem(self, slotIndex):
			itemVnum = privateShop.GetSaleItemVnum(slotIndex)
			if 0 == itemVnum:
				return
			
			self.ClearToolTip()
			self.isPrivateShopSaleItem = True
			
			# Required to fix DISABLE_COLOR being applied to textliens before item information
			self.itemVnum = itemVnum
			
			metinSlot = []
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlot.append(privateShop.GetSaleItemMetinSocket(slotIndex, i))
			attrSlot = []
			for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
				attrSlot.append(privateShop.GetSaleItemAttribute(slotIndex, i))

			self.AddItemData(itemVnum, metinSlot, attrSlot)

			self.AppendHorizontalLine()

			self.AppendTextLine(localeInfo.PREMIUM_PRIVATE_SALE_CUSTOMER % privateShop.GetSaleCustomerName(slotIndex), self.TITLE_COLOR)
			
			timestamp = privateShop.GetSaleTime(slotIndex)

			self.AppendTextLine(localeInfo.PREMIUM_PRIVATE_SALE_TIME % localeInfo.GetFullDateFormat(timestamp), self.TITLE_COLOR)
			self.AppendSpace(2)
			
			if app.ENABLE_PRIVATE_SHOP_CHEQUE:
				goldPrice = privateShop.GetSaleItemPrice(slotIndex)
				chequePrice = privateShop.GetSaleChequeItemPrice(slotIndex)
				self.AppendSellingPrice(goldPrice, chequePrice, True)
			else:
				self.AppendSellingPrice(privateShop.GetSaleItemPrice(slotIndex))

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def GetBuffSkillLevelGrade(self, skillLevel):
			skillLevel = int(skillLevel)
			if skillLevel >= 0 and skillLevel < 20:
				return ("%d" % int(skillLevel))
			if skillLevel >= 20 and skillLevel < 30:
				return ("M%d" % int(skillLevel-19))
			if skillLevel >= 30 and skillLevel < 40: 
				return ("G%d" % int(skillLevel-29))
			if skillLevel == 40: 
				return "P"

		def AppendEXPGauge(self, exp_perc):
			IMG_PATH = "d:/ymir work/ui/aslan/buffnpc/"
			gauge_empty_list = []
			gauge_full_list = []
			x_pos = [35, 17, 1, 19]
			for i in xrange(4):
				gauge_empty = ui.ExpandedImageBox()
				gauge_empty.SetParent(self)
				gauge_empty.LoadImage(IMG_PATH + "exp_empty.sub")
				if i <= 1:
					gauge_empty.SetPosition(self.toolTipWidth/2 - x_pos[i], self.toolTipHeight)
				else:
					gauge_empty.SetPosition(self.toolTipWidth/2 + x_pos[i], self.toolTipHeight)
				gauge_empty.Show()

				gauge_full = ui.ExpandedImageBox()
				gauge_full.SetParent(self)
				gauge_full.LoadImage(IMG_PATH + "exp_full.sub")
				if i <= 1:
					gauge_full.SetPosition(self.toolTipWidth/2 - x_pos[i], self.toolTipHeight)
				else:
					gauge_full.SetPosition(self.toolTipWidth/2 + x_pos[i], self.toolTipHeight)
					
				gauge_empty_list.append(gauge_empty)
				gauge_full_list.append(gauge_full)
		
			exp_perc = float(exp_perc / 100.0)
			exp_bubble_perc = 25.0

			for i in xrange(4):
				if exp_perc > exp_bubble_perc:
					exp_bubble_perc += 25.0
					gauge_full_list[i].SetRenderingRect(0.0, 0.0, 0.0, 0.0)
					gauge_full_list[i].Show()
				else:
					exp_perc = float((exp_perc - exp_bubble_perc) * 4 / 100) 
					gauge_full_list[i].SetRenderingRect(0.0, exp_perc, 0.0, 0.0)
					gauge_full_list[i].Show()
					break

			self.childrenList.append(gauge_empty_list)
			self.childrenList.append(gauge_full_list)
			
			self.toolTipHeight += 18
			self.ResizeToolTip()
				
	def SetShopItemBySecondaryCoin(self, slotIndex):
		itemVnum = shop.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		price = shop.GetItemPrice(slotIndex)
		self.ClearToolTip()
		self.isShopItem = True

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(shop.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(shop.GetItemAttribute(slotIndex, i))

		if app.ENABLE_REFINE_ELEMENT:
			refineElement = shop.GetItemRefineElement(slotIndex)
			self.AddItemData(itemVnum, metinSlot, attrSlot, refineElement = refineElement)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)
		self.AppendPriceBySecondaryCoin(price)

	def SetExchangeOwnerItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromSelf(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromSelf(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromSelf(slotIndex, i))

		self.__SetRefreshFunc(self.SetExchangeOwnerItem, slotIndex)

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			transmutate = exchange.GetItemTransmutateFromSelf(slotIndex)
			if app.ENABLE_REFINE_ELEMENT:
				refineElement = exchange.GetItemRefineElementFromSelf(slotIndex)
				self.AddItemData(itemVnum, metinSlot, attrSlot, trans_id = transmutate, refineElement = refineElement)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, trans_id = transmutate)
		else:
			if app.ENABLE_REFINE_ELEMENT:
				refineElement = exchange.GetItemRefineElementFromSelf(slotIndex)
				self.AddItemData(itemVnum, metinSlot, attrSlot, refineElement = refineElement)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetExchangeTargetItem(self, slotIndex):
		itemVnum = exchange.GetItemVnumFromTarget(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(exchange.GetItemMetinSocketFromTarget(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(exchange.GetItemAttributeFromTarget(slotIndex, i))

		self.__SetRefreshFunc(self.SetExchangeTargetItem, slotIndex)

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			transmutate = exchange.GetItemTransmutateFromTarget(slotIndex)
			if app.ENABLE_REFINE_ELEMENT:
				refineElement = exchange.GetItemRefineElementFromTarget(slotIndex)
				self.AddItemData(itemVnum, metinSlot, attrSlot, trans_id = transmutate, refineElement = refineElement)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, trans_id = transmutate)
		else:
			if app.ENABLE_REFINE_ELEMENT:
				refineElement = exchange.GetItemRefineElementFromTarget(slotIndex)
				self.AddItemData(itemVnum, metinSlot, attrSlot, refineElement = refineElement)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetPrivateShopBuilderItem(self, invenType, invenPos, privateShopSlotIndex):
		itemVnum = player.GetItemIndex(invenType, invenPos)
		if 0 == itemVnum:
			return

		item.SelectItem(itemVnum)
		self.ClearToolTip()
		
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if app.ENABLE_PRIVATE_SHOP_CHEQUE:
				goldPrice = privateShop.GetStockItemPrice(invenType, invenPos)
				chequePrice = privateShop.GetStockChequeItemPrice(invenType, invenPos)
				
				self.AppendSellingPrice(goldPrice, chequePrice, True)
			else:
				self.AppendSellingPrice(privateShop.GetStockItemPrice(invenType, invenPos))
		else:
			self.AppendSellingPrice(shop.GetPrivateShopItemPrice(invenType, invenPos))

		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(player.GetItemMetinSocket(invenPos, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(player.GetItemAttribute(invenPos, i))

		self.__SetRefreshFunc(self.SetPrivateShopBuilderItem, invenType, invenPos, privateShopSlotIndex)

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			transmutate = player.GetItemTransmutate(invenPos)
			if app.ENABLE_REFINE_ELEMENT:
				refineElement = player.GetItemRefineElement(invenType, invenPos)
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, trans_id = transmutate, refineElement = refineElement)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, trans_id = transmutate)
		else:
			if app.ENABLE_REFINE_ELEMENT:
				refineElement = player.GetItemRefineElement(invenType, invenPos)
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0, refineElement = refineElement)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, 0)

	def SetSafeBoxItem(self, slotIndex):
		itemVnum = safebox.GetItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetItemAttribute(slotIndex, i))

		self.__SetRefreshFunc(self.SetSafeBoxItem, slotIndex)

		transmutate = safebox.GetItemTransmutate(slotIndex)
		refineElement = safebox.GetItemRefineElement(slotIndex)
		self.AddItemData(itemVnum, metinSlot, attrSlot, safebox.GetItemFlags(slotIndex), trans_id = transmutate, refineElement = refineElement, window_type = player.SAFEBOX, slot_index = slotIndex, auxiliaryDict = player.GetAuxiliaryString(player.SAFEBOX, slotIndex))
	
	def SetMallItem(self, slotIndex):
		itemVnum = safebox.GetMallItemID(slotIndex)
		if 0 == itemVnum:
			return

		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(safebox.GetMallItemMetinSocket(slotIndex, i))
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append(safebox.GetMallItemAttribute(slotIndex, i))

		if app.ENABLE_REFINE_ELEMENT:
			refineElement = safebox.GetMallItemRefineElement(slotIndex)
			self.AddItemData(itemVnum, metinSlot, attrSlot, refineElement = refineElement, window_type = player.MALL, slot_index = slotIndex)
		else:
			self.AddItemData(itemVnum, metinSlot, attrSlot)

	def SetItemToolTip(self, itemVnum):
		self.ClearToolTip()
		metinSlot = []
		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlot.append(0)
		attrSlot = []
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			attrSlot.append((0, 0))

		self.AddItemData(itemVnum, metinSlot, attrSlot)

	def __AppendAttackSpeedInfo(self, item):
		atkSpd = item.GetValue(0)

		if atkSpd < 80:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_FAST
		elif atkSpd <= 95:
			stSpd = localeInfo.TOOLTIP_ITEM_FAST
		elif atkSpd <= 105:
			stSpd = localeInfo.TOOLTIP_ITEM_NORMAL
		elif atkSpd <= 120:
			stSpd = localeInfo.TOOLTIP_ITEM_SLOW
		else:
			stSpd = localeInfo.TOOLTIP_ITEM_VERY_SLOW

		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_SPEED % stSpd, self.NORMAL_COLOR)

	def __AppendAttackGradeInfo(self):
		atkGrade = item.GetValue(1)
		self.AppendTextLine(localeInfo.TOOLTIP_ITEM_ATT_GRADE % atkGrade, self.GetChangeTextLineColor(atkGrade))

	## Refine Elemental System
	def __AppendAttackPowerInfo(self, refineElement = 0):
		minPower = item.GetValue(3)
		maxPower = item.GetValue(4)
		addPower = item.GetValue(5)

		refineElementAddText = ""
		if app.ENABLE_REFINE_ELEMENT:
			elementAttackValueMin, elementAttackValueMax = -1, -1
			if self.isRefineElement != -1:
				if self.isRefineElement == item.REFINE_ELEMENT_TYPE_UPGRADE:
					if refineElement:
						elementAttackValueMin = int(refineElement / 1000 % 100) + item.REFINE_ELEMENT_RANDOM_BONUS_VALUE_MIN
						elementAttackValueMax = int(refineElement / 1000 % 100) + item.REFINE_ELEMENT_RANDOM_BONUS_VALUE_MAX
					else:
						elementAttackValueMin, elementAttackValueMax = item.REFINE_ELEMENT_RANDOM_BONUS_VALUE_MIN, item.REFINE_ELEMENT_RANDOM_BONUS_VALUE_MAX
				elif self.isRefineElement == item.REFINE_ELEMENT_TYPE_DOWNGRADE:
					if refineElement:
						elementPlus = int(refineElement / 10000000 % 10)
						if elementPlus == 1:
							elementAttackValueMin, elementAttackValueMax = -1, -1
						else:
							elementAttackValueMin = int(refineElement / 1000 % 100) - int(refineElement % 100)
							elementAttackValueMax = int(refineElement / 1000 % 100) - int(refineElement % 100)
			else:
				if refineElement:
					elementAttackValueMin, elementAttackValueMax = int(refineElement / 1000 % 100),  int(refineElement / 1000 % 100)

			if elementAttackValueMin != -1 and elementAttackValueMax != -1:
				if elementAttackValueMin == elementAttackValueMax:
					refineElementAddText = " (+%d)" % elementAttackValueMin
				else:
					refineElementAddText = " (+%d~+%d)" % (elementAttackValueMin, elementAttackValueMax)

		if maxPower > minPower:
			if app.ENABLE_REFINE_ELEMENT and refineElementAddText != "":
				bValue_1, bValue_2 = (minPower+addPower, maxPower+addPower)
				text = (localeInfo.TOOLTIP_ITEM_ATT_POWER % (bValue_1, bValue_2)) + refineElementAddText

				self.AppendTextLine(self.GetFormattedColorString(text, bValue_1, self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)
			else:
				bValue_1, bValue_2 = (minPower+addPower, maxPower+addPower)
				text = (localeInfo.TOOLTIP_ITEM_ATT_POWER % (bValue_1, bValue_2))
				self.AppendTextLine(self.GetFormattedColorString(text, bValue_1, self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)
		else:
			if app.ENABLE_REFINE_ELEMENT and refineElementAddText != "":
				bValue = (minPower+addPower)
				text = (localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % bValue) + refineElementAddText
				self.AppendTextLine(self.GetFormattedColorString(text, bValue, self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)
			else:
				bValue = (minPower+addPower)
				text = (localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % bValue)
				self.AppendTextLine(self.GetFormattedColorString(text, bValue, self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)

	def __AppendMagicAttackInfo(self):
		minMagicAttackPower = item.GetValue(1)
		maxMagicAttackPower = item.GetValue(2)
		addPower 			= item.GetValue(5)

		if minMagicAttackPower > 0 or maxMagicAttackPower > 0:
			if maxMagicAttackPower > minMagicAttackPower:
				bValue_1, bValue_2 = (minMagicAttackPower+addPower, maxMagicAttackPower+addPower)

				self.AppendTextLine(self.GetFormattedColorString(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (bValue_1, bValue_2), bValue_1, self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)
			else:
				bValue = (minMagicAttackPower+addPower)
				self.AppendTextLine(self.GetFormattedColorString(localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % bValue, bValue, self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)

	def __AppendMagicDefenceInfo(self):
		magicDefencePower = item.GetValue(0)

		if magicDefencePower > 0:
			self.AppendTextLine(self.GetFormattedColorString(localeInfo.TOOLTIP_ITEM_MAGIC_DEF_POWER % magicDefencePower, magicDefencePower, self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.GetChangeTextLineColor(magicDefencePower))

	def __AppendAttributeInformation(self, attrSlot, isDragonSoul = False):
		if 0 != attrSlot:
			i = 0
			for (type, value) in attrSlot:
				if 0 == value:
					i += 1
					continue

				fValue = localeInfo.GetFormattedNumberString(value)

				affectString = self.__GetAffectString(type, fValue, False)

				if affectString:
					affectColor, affectValueColor = self.__GetAttributeColor(i, value, type, isDragonSoul)
					self.AppendTextLine(self.GetFormattedColorString(affectString, fValue, affectValueColor, 1), affectColor)

				i += 1

	if app.ENABLE_AMULET_SYSTEM:
		def __AppendAmuletAttributeInformation(self, attrSlot, lSockets):
			AMULET_BASE_BONUS_COUNT = 2
			if 0 != attrSlot:
				i = 0
				for (type, value) in attrSlot:
					blocked = False
					if 0 == value and lSockets[i] != 0:
						blocked = True

					if i == AMULET_BASE_BONUS_COUNT:
						self.AppendHorizontalLine()

					fValue = localeInfo.GetFormattedNumberString(value)

					affectString = self.__GetAffectString(type, fValue, False)
					if affectString:
						affectColor, affectValueColor = self.__GetAttributeColor(i, value, type)
						sText = self.GetFormattedColorString(affectString, fValue, affectValueColor, 1)
						if (blocked):
							sText += "|r " + "|cFFdf80ff" + localeInfo.AMULET_APPLY_LOCKED + "|r"
						else:
							sText += "|r |cFF4da6ff({}/{})|r".format(min(lSockets[i], item.GetValue(1)), item.GetValue(1))

						self.AppendTextLine(sText, affectColor)

					i += 1

	if app.ENABLE_DS_SET:
		def __AppendDragonSoulAttributeInformation(self, attrSlot, iStep = 0, iSetType = 0):
			if 0 != attrSlot:
				it = 0
				S_BONUSES_DS = 3

				POSSIBLE_TO_SET = (iSetType > -1 and self.interface.wndDragonSoul.IsDSPageFull())
				SET_PERCENTS = (20, 20, 20, 20, 25)

				for (type, value) in attrSlot:
					if type == 0 or value == 0:
						it += 1
						continue
					
					if it == S_BONUSES_DS:
						self.AppendHorizontalLine()

					extraValue = max(1, int(math.ceil(float(value) * float(SET_PERCENTS[iStep]) / 100)))

					gValue = value if iSetType == -1 else value + extraValue
					applyString = self.__GetAffectString(type, gValue, False)
					if (applyString):
						affectColor, affectValueColor = self.__GetAttributeColor(0, gValue, type, True)
						fString = self.GetFormattedColorString(applyString, gValue, affectValueColor, 1)
						fString += "|r" + CFF.format(" (+{})".format(extraValue), "#ffff9a" if POSSIBLE_TO_SET else "#ff4f4f")
						self.AppendTextLine(fString, affectColor)

					it += 1

				self.AppendSpace(3)
				self.AppendTextLine(CFF.format("Percent: +{}%".format(SET_PERCENTS[iStep]), "#ffff9a" if POSSIBLE_TO_SET else "#ff4f4f"))

	def __GetAttributeColor(self, index, value, type, bDisableMaxAff = False):
		# if app.ENABLE_12ZI_ELEMENT_ADD:
		# 	if type in self.TAB_COLOR:
		# 		return (self.TAB_COLOR[type], "")

		# value = int(value)

		if not bDisableMaxAff:
			if (type in self.MAX_AFF_DICT and value >= self.MAX_AFF_DICT[type]):
				return (self.SPECIAL_COLOR_GOLD, self.COLOR_CONFIGURATION[self.SPECIAL_COLOR_GOLD])

		if value > 0:
			if index > player.ATTRIBUTE_SLOT_RARE_START and index < player.ATTRIBUTE_SLOT_RARE_END:
				return (self.SPECIAL_POSITIVE_COLOR2, "")
			else:
				return (self.SPECIAL_POSITIVE_COLOR, self.COLOR_CONFIGURATION[self.SPECIAL_POSITIVE_COLOR])

		elif value == 0:
			return (self.NORMAL_COLOR, self.COLOR_CONFIGURATION[self.NORMAL_COLOR])
		else:
			return (self.NEGATIVE_COLOR, self.COLOR_CONFIGURATION[self.NEGATIVE_COLOR])

	def GetAttributeColor(self, index, value, type, bDisableMaxAff = False):
		return self.__GetAttributeColor(index, value, type, bDisableMaxAff)

	def __IsPolymorphItem(self, itemVnum):
		if itemVnum >= 70103 and itemVnum <= 70106:
			return 1
		return 0

	def __SetPolymorphItemTitle(self, monsterVnum):
		itemName =nonplayer.GetMonsterName(monsterVnum)
		itemName+=" "
		itemName+=item.GetItemName()
		self.SetTitle(itemName)

	def __CheckAntiFlag(self):
		race = player.GetRace()
		job = chr.RaceToJob(race)

		if item.IsAntiFlag(self.ANTI_FLAG_DICT[job]):
			return True
		else:
			return False

	def __CheckSex(self):
		sex = chr.RaceToSex(player.GetRace())
		MALE = 1
		FEMALE = 0

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_MALE) and sex == MALE:
			return True

		if item.IsAntiFlag(item.ITEM_ANTIFLAG_FEMALE) and sex == MALE:
			return False

	def __SetNormalItemTitle(self, window_type = player.INVENTORY, slotIndex = -1):
		# self.SetTitle(item.GetItemName())
		itemCount = player.GetItemCount(window_type, slotIndex)
		itemName = item.GetItemName()

		if self.__CheckAntiFlag() == True:
			if itemCount > 1:
				self.AppendTextLine("%s (%s)" % (itemName, itemCount), self.TITLE_COLOR)
			else:
				self.AppendTextLine(item.GetItemName(), self.TITLE_COLOR)
		else:
			if self.__CheckSex() == True:
				if itemCount > 1:
					self.AppendTextLine("%s (%s)" % (itemName, itemCount), self.TITLE_COLOR)
				else:
					self.AppendTextLine(item.GetItemName(), self.TITLE_COLOR)
			else:
				if itemCount > 1:
					self.AppendTextLine("%s (%s)" % (itemName, itemCount), self.TITLE_COLOR)
				else:
					self.AppendTextLine(item.GetItemName(), self.TITLE_COLOR)

	def __SetSpecialItemTitle(self, itemVnum):
		if item.GetItemType() == item.ITEM_TYPE_DS:
			dsColors = [0xFFeaeaea, 0xFFe41b31, 0xFF56b42f, 0xFF00a0e4, 0xFFdf8f28, 0xFF999999]
			colorID = itemVnum / 10000

			self.AppendTextLine(item.GetItemName(), dsColors[colorID % 10 - 1])
			return

		if self.__CheckAntiFlag() == True:
			self.AppendTextLine(item.GetItemName(), self.TITLE_COLOR)
		else:
			if self.__CheckSex() == True:
				self.AppendTextLine(item.GetItemName(), self.TITLE_COLOR)
			else:
				self.AppendTextLine(item.GetItemName(), self.SPECIAL_TITLE_COLOR)

	if app.ENABLE_FIND_LETTERS_EVENT:
		def SetLetterTitle(self, itemVnum):
			letterAscii = self.itemVnum - 90500
			if letterAscii < 48 or (letterAscii > 57 and letterAscii < 65) or letterAscii > 90:
				self.__SetNormalItemTitle()
			else:
				letterName = item.GetItemName() + (" (%c)" % letterAscii)
				self.AppendTextLine(letterName, self.SPECIAL_TITLE_COLOR)

	def __SetItemTitle(self, itemVnum, metinSlot, attrSlot, window_type = player.INVENTORY, slotIndex = -1):
		if self.__IsPolymorphItem(itemVnum):
			self.__SetPolymorphItemTitle(metinSlot[0])
		else:
			if app.ENABLE_FIND_LETTERS_EVENT:
				if itemVnum >= 90500 and itemVnum <= 90600:
					self.SetLetterTitle(itemVnum)
					return

			if self.__IsAttr(attrSlot):
				self.__SetSpecialItemTitle(itemVnum)
				return

			self.__SetNormalItemTitle(window_type, slotIndex)

	def __IsAttr(self, attrSlot):
		if not attrSlot:
			return False

		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			if 0 != type:
				return True

		return False

	if app.ENABLE_REFINE_ELEMENT:
		def __AppendRefineElementText(self, refineElement):
			elementType = -1
			elementPlus = -1
			if self.isRefineElement != -1:
				if self.isRefineElement == item.REFINE_ELEMENT_TYPE_UPGRADE:
					if refineElement:
						elementType = int(refineElement / 100000000) - 1
						elementPlus = int(refineElement / 10000000 % 10) + 1
					else:
						if self.bRefineElementType > 0:
							elementType = self.bRefineElementType - 1
							elementPlus = 1
				elif self.isRefineElement == item.REFINE_ELEMENT_TYPE_DOWNGRADE:
					if refineElement:
						elementType = int(refineElement / 100000000) - 1
						elementPlus = int(refineElement / 10000000 % 10)

						if elementPlus == 1:
							elementType = -1
							elementPlus = -1
						else:
							elementType = int(refineElement / 100000000) - 1
							elementPlus = int(refineElement / 10000000 % 10) - 1
			else:
				if refineElement:
					elementType = int(refineElement / 100000000) - 1
					elementPlus = int(refineElement / 10000000 % 10)

			if elementType != -1 and elementPlus != -1:
				if elementType >= chrmgr.REFINE_ELEMENT_CATEGORY_ELECT and elementType < chrmgr.REFINE_ELEMENT_CATEGORY_MAX:
					if self.REFINE_ELEMENT_TEXT_INFO_INFO.has_key(elementType) and self.REFINE_ELEMENT_COLOR_DICT.has_key(elementType):
						self.AppendSpace(5)
						self.AppendTextLine(self.REFINE_ELEMENT_TEXT_INFO_INFO[elementType][0] % elementPlus, self.REFINE_ELEMENT_COLOR_DICT[elementType])

		def __AppendRefineElementInformation(self, refineElement):
			elementType = -1
			elementBonusValueMin = -1
			elementBonusValueMax = -1

			if self.isRefineElement != -1:
				if self.isRefineElement == item.REFINE_ELEMENT_TYPE_UPGRADE:
					if refineElement:
						elementType = int(refineElement / 100000000) - 1
						elementBonusValueMin = int(refineElement / 100000 % 100) + item.REFINE_ELEMENT_RANDOM_VALUE_MIN
						elementBonusValueMax = int(refineElement / 100000 % 100) + item.REFINE_ELEMENT_RANDOM_VALUE_MAX
					else:
						if self.bRefineElementType > 0:
							elementType = self.bRefineElementType - 1
							elementBonusValueMin = item.REFINE_ELEMENT_RANDOM_VALUE_MIN
							elementBonusValueMax = item.REFINE_ELEMENT_RANDOM_VALUE_MAX
				elif self.isRefineElement == item.REFINE_ELEMENT_TYPE_DOWNGRADE:
					if refineElement:
						elementPlus = int(refineElement / 10000000 % 10)
						if elementPlus == 1:
							elementType = -1
							elementBonusValueMin = -1
							elementBonusValueMax = -1
						else:
							elementType = int(refineElement / 100000000) - 1
							elementBonusValueMin = int(refineElement / 100000 % 100) - int(refineElement / 100 % 10)
							elementBonusValueMax = int(refineElement / 100000 % 100) - int(refineElement / 100 % 10)
			else:
				if refineElement:
					elementType = int(refineElement / 100000000) - 1
					elementBonusValueMin = int(refineElement / 100000 % 100)
					elementBonusValueMax = int(refineElement / 100000 % 100)

			if elementType != -1 and elementBonusValueMin != -1 and elementBonusValueMax != -1:
				if elementType >= chrmgr.REFINE_ELEMENT_CATEGORY_ELECT and elementType < chrmgr.REFINE_ELEMENT_CATEGORY_MAX:
					if self.REFINE_ELEMENT_TEXT_INFO_INFO.has_key(elementType) and self.REFINE_ELEMENT_COLOR_DICT.has_key(elementType):
						if elementBonusValueMin == elementBonusValueMax:
							self.AppendTextLine(self.REFINE_ELEMENT_TEXT_INFO_INFO[elementType][1].format(elementBonusValueMin), self.REFINE_ELEMENT_COLOR_DICT[elementType])
						else:
							self.AppendTextLine(self.REFINE_ELEMENT_TEXT_INFO_INFO[elementType][2] % (elementBonusValueMin, elementBonusValueMax), self.REFINE_ELEMENT_COLOR_DICT[elementType])

	if app.ENABLE_TRANSMUTATION_SYSTEM:
		## Refine Elemental System
		def AddRefineItemData(self, itemVnum, metinSlot, attrSlot = 0, type = 0, trans_id = 0, refineElement = 0, sashRefineItem = -1):
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlotData=metinSlot[i]
				if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
					metinSlot[i]=player.METIN_SOCKET_TYPE_SILVER

			if app.ENABLE_REFINE_ELEMENT:
				self.AddItemData(itemVnum, metinSlot, attrSlot, type, trans_id=trans_id, refineElement = refineElement, sashRefineItem = sashRefineItem)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, type, trans_id=trans_id)
	else:
		def AddRefineItemData(self, itemVnum, metinSlot, attrSlot = 0, type = 0, refineElement = 0):
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				metinSlotData=metinSlot[i]
				if self.GetMetinItemIndex(metinSlotData) == constInfo.ERROR_METIN_STONE:
					metinSlot[i]=player.METIN_SOCKET_TYPE_SILVER

			if app.ENABLE_REFINE_ELEMENT:
				self.AddItemData(itemVnum, metinSlot, attrSlot, type, refineElement = refineElement)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, type)

	def AddItemData_Offline(self, itemVnum, itemDesc, itemSummary, metinSlot, attrSlot):
		self.__AdjustMaxWidth(attrSlot, itemDesc)
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot)

		if self.__IsHair(itemVnum):
			self.__AppendHairIcon(itemVnum)

		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

	def __ClearRefreshFunc(self):
		self.refreshFunc = None
		self.refreshArgs = None
		self.ClearAddRefreshFunc()

	def ClearAddRefreshFunc(self):
		self.refreshFuncAdd = None
		self.refreshArgsAdd = None

	## Refine Elemental System
	"""ENABLE_LEGENDARY_STONES"""
	def AddItemData(self, itemVnum, metinSlot, attrSlot = 0, flags = 0, unbindTime = 0, trans_id = 0, refineElement = 0, **kwargs):
		self.dataToolTip.AddItemData(itemVnum, metinSlot, attrSlot, flags, unbindTime, trans_id, refineElement, **kwargs)
		self.itemVnum = itemVnum
		item.SelectItem(itemVnum)
		itemType = item.GetItemType()
		itemSubType = item.GetItemSubType()

		sAuxiliary = kwargs.get("auxiliaryDict")
		if not sAuxiliary and (kwargs.get("window_type") and kwargs.get("slot_index")):
			sAuxiliary = player.GetAuxiliaryString(kwargs.get("window_type"), kwargs.get("slot_index"))

		minAtk=player.GetStatus(player.ATT_MIN)
		maxAtk=player.GetStatus(player.ATT_MAX)
		atkBonus=player.GetStatus(player.ATT_BONUS)
		attackerBonus=player.GetStatus(player.ATTACKER_BONUS)

		self.lastRefreshTime = app.GetTime()

		if 50026 == itemVnum:
			if 0 != metinSlot:
				name = item.GetItemName()
				if metinSlot[0] > 0:
					name += " "
					name += localeInfo.NumberToMoneyString(metinSlot[0])
				self.SetTitle(name)
				self.ShowToolTip()
			return

		### Skill Book ###
		elif 50300 == itemVnum:
			if 0 != metinSlot:
				self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILLBOOK_NAME, 1)
				self.ShowToolTip()
			return
		elif 70037 == itemVnum:
			if 0 != metinSlot:
				self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
				self.AppendDescription(item.GetItemDescription(), 26)
				self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
				self.ShowToolTip()
			return
		elif 70055 == itemVnum:
			if 0 != metinSlot:
				self.__SetSkillBookToolTip(metinSlot[0], localeInfo.TOOLTIP_SKILL_FORGET_BOOK_NAME, 0)
				self.AppendDescription(item.GetItemDescription(), 26)
				self.AppendDescription(item.GetItemSummary(), 26, self.CONDITION_COLOR)
				self.ShowToolTip()
			return

		###########################################################################################


		itemDesc = item.GetItemDescription()
		itemSummary = item.GetItemSummary()

		isTimed = False

		isCostumeItem = 0
		isCostumeHair = 0
		isCostumeBody = 0

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if itemVnum == 71999:
				self.__AdjustMaxWidth(attrSlot, itemDesc)
				self.__SetItemTitle(itemVnum, 0, 0)
				self.AppendDescription(itemDesc, 26)
				self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)
				# self.AppendSpace(5)
				self.AppendTextLine("_________________", self.TITLE_COLOR)
				
				if metinSlot[0] == 0:
					self.AppendDescription(uiScriptLocale.ASLAN_BUFF_TOOLTIP_WITH_SOCKET_ZERO, 26)
				else:
					sexDesc = [uiScriptLocale.ASLAN_BUFF_TOOLTIP_MALE, uiScriptLocale.ASLAN_BUFF_TOOLTIP_FEMALE]
					self.AppendTextLine(sexDesc[metinSlot[1]], self.NORMAL_COLOR)
					self.AppendTextLine(uiScriptLocale.ASLAN_BUFF_TOOLTIP_LEVEL % str(metinSlot[2]), self.NORMAL_COLOR)
					exp_perc = float(metinSlot[3] / 100.0)
					self.AppendTextLine("%.2f%%" % exp_perc, self.TITLE_COLOR)
					self.AppendEXPGauge(metinSlot[3])
					self.AppendTextLine("_________________", self.TITLE_COLOR)
					self.AppendTextLine(uiScriptLocale.ASLAN_BUFF_TOOLTIP_SKILLPOINTS % str(metinSlot[4]), self.NORMAL_COLOR)
					self.AppendTextLine(uiScriptLocale.ASLAN_BUFF_TOOLTIP_INTELLIGENCE % str(metinSlot[5]), self.NORMAL_COLOR)
					self.AppendTextLine("_________________", self.TITLE_COLOR)
					
					self.AppendTextLine(skill.GetSkillName(94, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[0][0]), self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(skill.GetSkillName(95, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[0][1]), self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(skill.GetSkillName(96, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[1][0]), self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(skill.GetSkillName(109, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[1][1]), self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(skill.GetSkillName(110, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[2][0]), self.SPECIAL_POSITIVE_COLOR)
					self.AppendTextLine(skill.GetSkillName(111, 0)+" : "+self.GetBuffSkillLevelGrade(attrSlot[2][1]), self.SPECIAL_POSITIVE_COLOR)
					
				self.ShowToolTip()
				return

		if app.ENABLE_WEAPON_COSTUME_SYSTEM:
			isCostumeWeapon = 0

		if app.ENABLE_COSTUME_SYSTEM:
			if item.ITEM_TYPE_COSTUME == itemType:
				isCostumeItem = 1
				isCostumeHair = item.COSTUME_TYPE_HAIR == itemSubType
				isCostumeBody = item.COSTUME_TYPE_BODY == itemSubType

				if app.ENABLE_WEAPON_COSTUME_SYSTEM:
					isCostumeWeapon = item.COSTUME_TYPE_WEAPON == itemSubType

				#dbg.TraceError("IS_COSTUME_ITEM! body(%d) hair(%d)" % (isCostumeBody, isCostumeHair))

		self.__AdjustMaxWidth(attrSlot, itemDesc)
		self.__SetItemTitle(itemVnum, metinSlot, attrSlot, kwargs.get("window_type", player.INVENTORY), kwargs.get("slot_index", -1))

		if kwargs.get("bShowIcon", False):
			self.AppendImage(item.GetIconImageFileName())

		if app.ENABLE_REFINE_ELEMENT:
			self.__AppendRefineElementText(refineElement)

		if gcGetEnable("ENABLE_TOOLTIP_CATEGORIES"):
			self.AppendCategoryInfo()

		### Hair Preview Image ###
		# if self.__IsHair(itemVnum):
		# 	self.__AppendHairIcon(itemVnum)
		
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.isPrivateSearchItem or self.isPrivateShopSaleItem:
				if not self.__IsHair(itemVnum):
					self.__AppendPrivateItemIcon(itemVnum)

		### Description ###
		self.AppendDescription(itemDesc, 26)
		self.AppendDescription(itemSummary, 26, self.CONDITION_COLOR)

		### Weapon ###
		if item.ITEM_TYPE_WEAPON == itemType:

			self.__AppendLimitInformation()

			# self.AppendSpace(5)

			if item.WEAPON_FAN == itemSubType:
				self.__AppendMagicAttackInfo()
				if app.ENABLE_REFINE_ELEMENT:
					self.__AppendAttackPowerInfo(refineElement = refineElement)
				else:
					self.__AppendAttackPowerInfo()

			else:
				if app.ENABLE_REFINE_ELEMENT:
					self.__AppendAttackPowerInfo(refineElement = refineElement)
				else:
					self.__AppendAttackPowerInfo()
				self.__AppendMagicAttackInfo()

			self.__AppendAffectInformation()
			if app.ENABLE_REFINE_ELEMENT:
				self.__AppendRefineElementInformation(refineElement)
			self.__AppendAttributeInformation(attrSlot)

			self.__AppendSetInformation(itemVnum)

			#TODO In some time we gonna back there to make something for it with options
			# iData = {'iType' : itemType, 'charType' : chr.GetRace(), 'iValue' : itemVnum}
			# self.AppendRenderTarget(data = iData)

			## Transmutation System
			if app.ENABLE_TRANSMUTATION_SYSTEM:
				if trans_id > 0:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.CHANGE_LOOK_TITLE)

					item.SelectItem(trans_id)
					self.AppendTextLine("%s" % str(item.GetItemName()), self.TRANSMUTATION_ITEMNAME_COLOR)

			self.AppendWearableInformation()
			if app.ENABLE_QUIVER_SYSTEM:
				if itemSubType != item.WEAPON_QUIVER:
					self.__AppendMetinSlotInfo(metinSlot)
					## <!!!> Enable this below if you have the realtimed weapons
					#self.__AppendRealTimeToolTip(itemVnum, metinSlot[0])
					## <!!!>
				elif item.WEAPON_QUIVER == itemSubType:
					bHasRealtimeFlag = 0
					defaultValue = 0
					for i in xrange(item.LIMIT_MAX_NUM):
						(limitType, defaultValue) = item.GetLimit(i)
						if item.LIMIT_REAL_TIME == limitType:
							bHasRealtimeFlag = 1
							break

					if bHasRealtimeFlag == 1:
						self.AppendMallItemLastTime(defaultValue if self.isShopItem else metinSlot[0])
			else:
				self.__AppendMetinSlotInfo(metinSlot)

		### Armor ###
		elif item.ITEM_TYPE_ARMOR == itemType:
			self.__AppendLimitInformation()

			if app.ENABLE_ORE_REFACTOR and itemSubType not in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				defGrade = item.GetValue(1)
				defBonus = item.GetValue(5)*2
				if defGrade > 0:
					self.AppendTextLine(self.GetFormattedColorString(localeInfo.TOOLTIP_ITEM_DEF_GRADE % (defGrade+defBonus), (defGrade+defBonus), self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.GetChangeTextLineColor(defGrade))

				self.__AppendMagicDefenceInfo()

			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			self.__AppendSetInformation(itemVnum)

			## Transmutation System
			if app.ENABLE_TRANSMUTATION_SYSTEM:
				if trans_id > 0:
					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.CHANGE_LOOK_TITLE)

					item.SelectItem(trans_id)
					self.AppendTextLine("%s" % str(item.GetItemName()), self.TRANSMUTATION_ITEMNAME_COLOR)

			self.AppendWearableInformation()

			if itemSubType in (item.ARMOR_WRIST, item.ARMOR_NECK, item.ARMOR_EAR):
				if app.ENABLE_ORE_REFACTOR:
					self.__AppendAccesoryInformation(metinSlot)
				else:
					self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_ACCESSORY_MATERIAL_VNUM(itemVnum, itemSubType))
			else:
				self.__AppendMetinSlotInfo(metinSlot)

		### Ring Slot Item (Not UNIQUE) ###
		elif item.ITEM_TYPE_RING == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)
			self.__AppendSetInformation(itemVnum)
			#self.__AppendAccessoryMetinSlotInfo(metinSlot, 99001)

		### Belt Item ###
		elif item.ITEM_TYPE_BELT == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			if app.ENABLE_ORE_REFACTOR:
				self.__AppendAccessoryMetinSlotInfo(metinSlot)
			else:
				self.__AppendAccessoryMetinSlotInfo(metinSlot, constInfo.GET_BELT_MATERIAL_VNUM(itemVnum))

			self.AppendWearableInformation()

		elif 0 != isCostumeItem:
			if app.ENABLE_SASH_COSTUME_SYSTEM and item.COSTUME_TYPE_SASH == itemSubType:
				self.__AppendLimitInformation()
				self.AppendSpace(5)

				self.__AppendAffectInformation()

				if app.ENABLE_SASH_COSTUME_SYSTEM:
					self.__AppendSashInfo(attrSlot, metinSlot, kwargs.get("sashRefineItem", False))
					item.SelectItem(itemVnum)
				else:
					self.__AppendAttributeInformation(attrSlot)

				## Transmutation System
				if app.ENABLE_TRANSMUTATION_SYSTEM:
					if trans_id > 0:
						self.AppendSpace(5)
						self.AppendTextLine(localeInfo.CHANGE_LOOK_TITLE, self.TRANSMUTATION_TITLE_COLOR)

						item.SelectItem(trans_id)
						self.AppendTextLine("%s" % str(item.GetItemName()), self.TRANSMUTATION_ITEMNAME_COLOR)

				self.__AppendSetInformation(itemVnum)
				self.AppendWearableInformation()
				self.__AppendMetinSlotInfo(metinSlot, True)
			else:
				self.__AppendLimitInformation()

				self.__AppendAffectInformation()
				self.__AppendAttributeInformation(attrSlot)
				self.__AppendSetInformation(itemVnum)
				self.AppendWearableInformation()

		## Rod ##
		elif item.ITEM_TYPE_ROD == itemType:

			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendRodInformation(curLevel, curEXP, maxEXP)

		## Pick ##
		elif item.ITEM_TYPE_PICK == itemType:

			if 0 != metinSlot:
				curLevel = item.GetValue(0) / 10
				curEXP = metinSlot[0]
				maxEXP = item.GetValue(2)
				self.__AppendLimitInformation()
				self.__AppendPickInformation(curLevel, curEXP, maxEXP)

		## Lottery ##
		elif item.ITEM_TYPE_LOTTERY == itemType:
			if 0 != metinSlot:

				ticketNumber = int(metinSlot[0])
				stepNumber = int(metinSlot[1])

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_LOTTERY_STEP_NUMBER % (stepNumber), self.NORMAL_COLOR)
				self.AppendTextLine(localeInfo.TOOLTIP_LOTTO_NUMBER % (ticketNumber), self.NORMAL_COLOR);

		### Metin ###
		elif item.ITEM_TYPE_METIN == itemType:
			if gcGetEnable("ENABLE_LEGENDARY_STONES"):
				self.AppendMetinInformation(metinSlot, kwargs.get("bLegendaryStoneRefine", False))
			else:
				self.AppendMetinInformation()

			self.AppendMetinWearInformation()

		### Fish ###
		elif item.ITEM_TYPE_FISH == itemType:
			if 0 != metinSlot:
				self.__AppendFishInfo(metinSlot[0])

		## item.ITEM_TYPE_BLEND
		elif item.ITEM_TYPE_BLEND == itemType:
			self.__AppendLimitInformation()

			if metinSlot:
				affectType = metinSlot[0]
				affectValue = metinSlot[1]
				time = metinSlot[2]
				self.AppendSpace(5)
				affectText = self.__GetAffectString(affectType, affectValue)

				self.AppendTextLine(affectText, self.NORMAL_COLOR)

				if time > 0:
					minute = (time / 60)
					second = (time % 60)
					timeString = localeInfo.TOOLTIP_POTION_TIME

					if minute > 0:
						timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
					if second > 0:
						timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

					self.AppendTextLine(timeString)

					isTimed = True
				else:
					self.AppendTextLine(localeInfo.BLEND_POTION_NO_TIME)
			else:
				self.AppendTextLine("BLEND_POTION_NO_INFO")

		elif item.ITEM_TYPE_UNIQUE == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()
			self.__AppendAttributeInformation(attrSlot)

			if 0 != metinSlot:
				bHasRealtimeFlag = 0
				bSuppress = False

				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
					elif limitType in (item.LIMIT_REAL_TIME_START_FIRST_USE, item.LIMIT_TIMER_BASED_ON_WEAR):
						bSuppress = True

				# if not bSuppress:
				# 	isTimed = True
				# 	if 1 == bHasRealtimeFlag:
				# 		self.AppendMallItemLastTime(metinSlot[0])
				# 	elif itemSubType != 2: # UNIQUE_SPECIAL_RIDE
				# 		time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

				# 		if 1 == item.GetValue(2):
				# 			self.AppendMallItemLastTime(time)
				# 		else:
				# 			self.AppendUniqueItemLastTime(time)

		elif item.ITEM_TYPE_GIFTBOX == itemType:
			self.AppendSpace(5)
			itemCount = player.GetItemCount(kwargs.get("window_type", player.INVENTORY), kwargs.get("slot_index", -1))

		### Use ###
		elif item.ITEM_TYPE_USE == itemType:
			self.__AppendLimitInformation()

			if item.USE_POTION == itemSubType or item.USE_POTION_NODELAY == itemSubType:
				self.__AppendPotionInformation()

			elif item.USE_ABILITY_UP == itemSubType:
				self.__AppendAbilityPotionInformation()

			TAB_BONUS_ITEM = {
				71027: [['Max. HP +20% (+{} HP)'.format((player.GetStatus(player.MAX_HP) / 100) * 20)],
				['Currently: {} HP'.format(player.GetStatus(player.MAX_HP))],
				['After: {} HP'.format(player.GetStatus(player.MAX_HP)/100 * 20 + player.GetStatus(player.MAX_HP))],],
				71028: ['Max. Atk +20% (+{} - {} value)'.format(int(float(minAtk+atkBonus+attackerBonus)/100* 20),int(float(maxAtk+atkBonus+attackerBonus)/100* 20))],
				71029: ['Max. PE +20% (+{} PE)'.format((player.GetStatus( player.MAX_SP )/100) * 20 )],
				71030: ['Injuries received are reduced by {}%'.format(20)]
			}

			if (itemVnum in TAB_BONUS_ITEM) and (0 != metinSlot):
				self.AppendSpace(5)
				if len(TAB_BONUS_ITEM[itemVnum])==1:self.AppendTextLine(str(TAB_BONUS_ITEM[itemVnum][0]), self.POSITIVE_COLOR)
				else:
					for x in TAB_BONUS_ITEM[itemVnum]:
						self.AppendTextLine(str(x[0]), self.POSITIVE_COLOR)

			if 27989 == itemVnum or 76006 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (6 - useCount), self.NORMAL_COLOR)

			elif 50004 == itemVnum:
				if 0 != metinSlot:
					useCount = int(metinSlot[0])

					self.AppendSpace(5)
					self.AppendTextLine(localeInfo.TOOLTIP_REST_USABLE_COUNT % (10 - useCount), self.NORMAL_COLOR)

			elif constInfo.IS_AUTO_POTION(itemVnum):
				if 0 != metinSlot:
					isActivated = int(metinSlot[0])
					usedAmount = float(metinSlot[1])
					totalAmount = float(metinSlot[2])

					if 0 == totalAmount:
						totalAmount = 1

					self.AppendSpace(5)

					if 0 != isActivated:
						self.AppendTextLine("(%s)" % (localeInfo.TOOLTIP_AUTO_POTION_USING), self.SPECIAL_POSITIVE_COLOR)
						self.AppendSpace(5)

					self.AppendTextLine(localeInfo.TOOLTIP_AUTO_POTION_REST % (100.0 - ((usedAmount / totalAmount) * 100.0)), self.POSITIVE_COLOR)

			elif itemVnum in WARP_SCROLLS:
				if 0 != metinSlot:
					xPos = int(metinSlot[0])
					yPos = int(metinSlot[1])

					if xPos != 0 and yPos != 0:
						(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(xPos, yPos)

						localeMapName = ""
						(localeMapName, x, y) = background.GetMapLocaleName(xPos, yPos)

						self.AppendSpace(5)

						if localeMapName!="":
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION % (getattr(localeInfo, "ATLAS_MAP_{}".format(self.localeMapName), localeMapName.replace("_", " ")), int(xPos-xBase)/100, int(yPos-yBase)/100), self.NORMAL_COLOR)
							try:
								self.AppendMapImage(mapName, int(xPos-xBase)/100, int(yPos-yBase)/100)
							except:
								self.AppendTextLine("COULD NOT LOAD MINIMAP", self.NORMAL_COLOR)
						else:
							self.AppendTextLine(localeInfo.TOOLTIP_MEMORIZED_POSITION_ERROR % (int(xPos)/100, int(yPos)/100), self.NORMAL_COLOR)
							dbg.TraceError("NOT_EXIST_IN_MINIMAP_ZONE_NAME_DICT: %s" % mapName)

			elif itemVnum == 70102:
				self.AppendSpace(4)
				point, grade = player.GetAlignmentData()

				colorList = colorInfo.TITLE_RGB_COLOR_DICT.get(grade, colorInfo.TITLE_RGB_NORMAL)
				gradeColor = ui.GenerateColor(colorList[0], colorList[1], colorList[2])

				self.AppendTextLine(localeInfo.TITLE_NAME_LIST[grade], gradeColor)

				if point < 0:
					value = item.GetValue(0) / 10
					self.AppendTextLine(localeInfo.ALIGNMENT_NAME + " " + colorInfo.Colorize(localeInfo.DottedNumber(point), 0xFFffffff) + " (+{})".format((colorInfo.Colorize(localeInfo.DottedNumber(value), 0xFFffffff)) if abs(point) > value else colorInfo.Colorize(localeInfo.DottedNumber(abs(point)), 0xFFffffff)))
				else:
					self.AppendTextLine(localeInfo.ALIGNMENT_NAME + " " + colorInfo.Colorize(localeInfo.DottedNumber(point), 0xFFffffff))

			#####
			if item.USE_SPECIAL == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					#if item.LIMIT_REAL_TIME == limitType:
					#	bHasRealtimeFlag = 1

				if 1 == bHasRealtimeFlag:
					isTimed = True
					self.AppendMallItemLastTime(metinSlot[0])
				else:
					if 0 != metinSlot:
						time = metinSlot[player.METIN_SOCKET_MAX_NUM-1]

						if 1 == item.GetValue(2):
							isTimed = True
							self.AppendMallItemLastTime(time)

			elif item.USE_TIME_CHARGE_PER == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1

				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER.format(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_PER.format(item.GetValue(0)))

				if 1 == bHasRealtimeFlag:
					isTimed = True
					self.AppendMallItemLastTime(metinSlot[0])

			elif item.USE_TIME_CHARGE_FIX == itemSubType:
				bHasRealtimeFlag = 0
				for i in xrange(item.LIMIT_MAX_NUM):
					(limitType, limitValue) = item.GetLimit(i)

					if item.LIMIT_REAL_TIME == limitType:
						bHasRealtimeFlag = 1
				if metinSlot[2]:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX.format(metinSlot[2]))
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_TIME_CHARGER_FIX.format(item.GetValue(0)))

				if 1 == bHasRealtimeFlag:
					isTimed = True
					self.AppendMallItemLastTime(metinSlot[0])

			elif item.USE_PUT_INTO_ACCESSORY_SOCKET == itemSubType:
				ACC_HEADERS = (localeInfo.TOOLTIP_ACCESSORY_TYPE_0, localeInfo.TOOLTIP_ACCESSORY_TYPE_1, localeInfo.TOOLTIP_ACCESSORY_TYPE_2)

				## Lets define multipler
				iMultipler = 0

				if not item.GetValue(5):
					iMultipler = item.GetValue(3)
					self.AppendTextLine(localeInfo.TOOLTIP_ACCESSORY_GRADE.format(colorInfo.Colorize(util.IntegerToRoman(iMultipler), 0xFFffd169)))

				for it in xrange(len(ACC_HEADERS)):
					## We need select the main item at the beggin
					item.SelectItem(itemVnum)

					## Lets check the value of main item!
					lValue = item.GetValue(it)
					if not lValue:
						continue

					self.AppendSpace(3)

					##Append header
					self.AppendTextLine(ACC_HEADERS[it], 0xFFffd169)

					##Selecting item and set a name
					item.SelectItem(lValue)

					for i in xrange(item.ITEM_APPLY_MAX_NUM):
						(affectType, affectValue) = item.GetAffect(i)

						if (affectType == 0):
							continue
						
						affectString = self.__GetAffectString(affectType, max(1, item.GetValue(i) * iMultipler), True)
						if affectString:
							self.AppendTextLine(affectString, self.POSITIVE_COLOR)

				self.AppendSpace(4)

				self.AppendTextLine(self.__GetAccessoryType(itemVnum, 3600 * 36))

			if app.ENABLE_NEW_COSTUME_BONUS:
				if item.USE_ADD_COSTUME_ATTR_SPECIAL == itemSubType:
					self.__AppendLimitInformation()
					self.__AppendAffectInformation()

					self.__AppendAttributeInformation(attrSlot)

		elif item.ITEM_TYPE_QUEST == itemType:
			if metinSlot[0] != 0 or metinSlot[1] != 1 or metinSlot[2] != 2:
				self.__AppendLimitInformation()
				self.__AppendAffectInformation()
				self.__AppendAttributeInformation(attrSlot)

		elif item.ITEM_TYPE_DS == itemType:
			bText = self.__DragonSoulInfoString(itemVnum).replace(":", ":|cFFf4be00")
			bTextOut = bText[:bText.rfind(",")] + "|r" + bText[bText.rfind(","):]

			self.AppendTextLine(bTextOut)

			if app.ENABLE_DS_SET and kwargs.get("window_type", player.INVENTORY) == player.INVENTORY and self.interface and self.interface.wndDragonSoul:
				self.__AppendDragonSoulAttributeInformation(attrSlot, (itemVnum / 100) % 10, self.interface.wndDragonSoul.GetSetType())
			else:
				self.__AppendAttributeInformation(attrSlot, True)

		elif app.ENABLE_TOGGLE_SYSTEM and item.ITEM_TYPE_TOGGLE == itemType:
			self.__AppendLimitInformation()
			self.__AppendAffectInformation()

			isActivated = int(metinSlot[3])
			if 0 != isActivated:
				self.AppendTextLine("(%s)" % localeInfo.TOOLTIP_TOGGLE_ACTIVE, self.SPECIAL_POSITIVE_COLOR)

			if itemSubType in (item.TOGGLE_AUTO_RECOVERY_HP, item.TOGGLE_AUTO_RECOVERY_SP):
				if metinSlot != 0:
					usedAmount = float(metinSlot[0])
					totalAmount = float(metinSlot[1])
					if 0 == totalAmount:
						totalAmount = 1

					# isPerma = item.GetValue(4)

					# if isPerma:
					# 	self.AppendTextLine(colorInfo.Colorize(localeInfo.TOOLTIP_TIME_HEADER, 0xFF68bcff) + localeInfo.TOOLTIP_TIME_PERMANENT, 0xFFffffff)
					# else:

					# rest = 100.0 - ((usedAmount / totalAmount) * 100.0)

					# gaugeImage = ui.Gauge()
					# gaugeImage.SetWindowName("IMAGE_P")
					# gaugeImage.SetParent(self)
					# gaugeImage.MakeGauge(130, "red" if itemSubType == item.TOGGLE_AUTO_RECOVERY_HP else "blue")
					# gaugeImage.SetPosition(0, self.toolTipHeight)
					# gaugeImage.SetWindowHorizontalAlignCenter()
					# gaugeImage.SetPercentage(int(rest), 100)
					# gaugeImage.Show()
					# self.toolTipHeight += gaugeImage.imgGauge.GetHeight()
					# self.childrenList.append(gaugeImage)

					# rest = 100.0 - ((usedAmount / totalAmount) * 100.0)
					# self.AppendTextLine(localeInfo.TOOLTIP_TOGGLE_POTION_LEFT + " {} / {}".format(localeInfo.DottedNumber(totalAmount - usedAmount), localeInfo.DottedNumber(totalAmount)), self.POSITIVE_COLOR)
					# self.AppendTextLine(localeInfo.TOOLTIP_TOGGLE_POTION_LEFT + " %.2f%%" % (rest), self.POSITIVE_COLOR)

			elif itemSubType in (item.TOGGLE_RED_SOUL, item.TOGGLE_BLUE_SOUL):
				if metinSlot != 0:
					(limit_Type, limit_Value) = item.GetLimit(1)
					max_time = limit_Value

					if 0 != flags:
						metinSlot[2] = item.GetValue(2)

					data = metinSlot[2]
					keep_time = data / 10000
					remain_count = data % 10000

					value_index = 2 + keep_time / 60
					if value_index < 3:
						value_index = 3
					if value_index > 5:
						value_index = 5
					damage_value = float( item.GetValue(value_index) / 10.0 )

					soul_desc = ""
					if item.TOGGLE_RED_SOUL == itemSubType:
						soul_desc = localeInfo.SOUL_ITEM_TOOLTIP_RED1 % (keep_time, max_time)
						soul_desc += localeInfo.SOUL_ITEM_TOOLTIP_RED2 % (damage_value)
					elif item.TOGGLE_BLUE_SOUL == itemSubType:
						soul_desc = localeInfo.SOUL_ITEM_TOOLTIP_BLUE1 % (keep_time, max_time)
						soul_desc += localeInfo.SOUL_ITEM_TOOLTIP_BLUE2 % (damage_value)
						
					self.__AdjustMaxWidth(0, soul_desc)

					if keep_time < 60:
						desc_color = 0xfff15f5f	# RGB(241,95,95)
					else:
						desc_color = 0xff86e57f	# RGB(134,229,127)

					self.AppendDescription( soul_desc, 26, desc_color)

					self.AppendDescription(localeInfo.SOUL_ITEM_TOOLTIP_COMMON, 26, 0xfff15f5f)	# RGB(241,95,95)

					self.AppendSpace(5)

					self.AppendTextLine( localeInfo.SOUL_ITEM_TOOLTIP_REMAIN_COUNT % remain_count )
					self.AppendSpace(5)

		elif app.ENABLE_AMULET_SYSTEM and item.ITEM_TYPE_AMULET == itemType:
			self.AppendSpace(2)

			self.__AppendAmuletAttributeInformation(attrSlot, metinSlot)

		else:
			self.__AppendLimitInformation()

		item.SelectItem(self.itemVnum)

		if itemType != item.ITEM_TYPE_BLEND and itemSubType not in (item.USE_TIME_CHARGE_PER, item.USE_TIME_CHARGE_FIX):
			if self.__AppendTimeLimitInfo(metinSlot, (item.ITEM_TYPE_COSTUME == itemType and itemSubType != item.COSTUME_TYPE_SASH), isToggle = itemType == item.ITEM_TYPE_TOGGLE):
				isTimed = True

		if not isTimed:
			self.__ClearRefreshFunc()

		self.__AppendSealInformation(kwargs.get("window_type", player.INVENTORY), kwargs.get("slot_index", -1)) ## cyh itemseal 2013 11 11

		self.AppendAntiflagInformation()

		if gcGetEnable("ENABLE_FAST_INTERACTIONS") and self.interface:
			self.AppendShortcuts(kwargs.get("slot_index", -1), itemVnum, kwargs.get("shortcustHelper", False))

		self.ShowToolTip()

	# Item expiration time
	def __AppendRemainingTime(self, seconds):
		self.AppendTextLine("|cFF68bcff" + localeInfo.LEFT_TIME + ":|r " + localeInfo.SecondToDHMS(seconds), self.NORMAL_COLOR)

	def __AppendMallItemLastTime(self, endTime, appendSpace = True):
		leftSec = max(0, endTime - app.GetGlobalTimeStamp())
		self.__AppendRemainingTime(leftSec)

	def __AppendRealTimeLastTime(self, metinSlot, limitValue):
		rem = metinSlot[0]
		if rem != 0:
			self.__AppendMallItemLastTime(rem)
		else:
			self.__AppendRemainingTime(limitValue)

	if app.ENABLE_NEW_COSTUME_BONUS:
		def __AppendCostumeRealTime(self, metinSlot):
			if metinSlot[3] > 0:
				self.AppendTextLine(localeInfo.LEFT_BONUS_TIME + ": " + localeInfo.SecondToDHMS(metinSlot[3] - app.GetGlobalTimeStamp()), self.NORMAL_COLOR)

	def __AppendTimerBasedOnWearLastTime(self, metinSlot, limitValue):
		rem = metinSlot[0]
		if 0 == rem:
			item.SelectItem(self.itemVnum)
			if item.GetItemType() != item.ITEM_TYPE_DS:
				rem = limitValue
		self.__AppendRemainingTime(rem)

	def __AppendRealTimeStartFirstUseLastTime(self, metinSlot, limitValue):
		useCount = metinSlot[1]
		remTime = metinSlot[0]

		if 0 == useCount:
			if 0 == remTime:
				remTime = limitValue

			self.__AppendRemainingTime(remTime)
		else:
			self.__AppendMallItemLastTime(remTime)

	def __AppendTimeLimitInfo(self, metinSlot, costume_time = False, isToggle = False):
		ret = False

		if costume_time:
			self.__AppendCostumeRealTime(metinSlot)
			ret = True

		for i in xrange(item.LIMIT_MAX_NUM):
			(limitType, limitValue) = item.GetLimit(i)

			if item.LIMIT_REAL_TIME == limitType:
				self.__AppendRealTimeLastTime(metinSlot, limitValue)
				ret = True

			elif item.LIMIT_REAL_TIME_START_FIRST_USE == limitType:
				self.__AppendRealTimeStartFirstUseLastTime(metinSlot, limitValue)
				ret = True

			elif item.LIMIT_TIMER_BASED_ON_WEAR == limitType:
				if metinSlot[0] != -1:
					self.__AppendTimerBasedOnWearLastTime(metinSlot, limitValue)
					ret = True

		if isToggle and not ret:
			self.AppendTextLine(colorInfo.Colorize(localeInfo.TOOLTIP_TIME_HEADER, 0xFF68bcff) + localeInfo.TOOLTIP_TIME_PERMANENT, 0xFFffffff)

		return ret

	def GetMapImageWidth(self, mapName):
		mapImage = ui.ImageBox()
		mapImage.LoadImage("d:/ymir work/ui/atlas/%s/atlas.sub" % (mapName))
		width = mapImage.GetWidth()
		mapImage = None
		return width

	def AppendMapImage(self, mapName, xPos, yPos, pointShow = True):
		try:
			mapImage = ui.ImageBox()
			mapImage.SetParent(self)
			mapImage.Show()
			mapImage.LoadImage("d:/ymir work/ui/atlas/%s/atlas.sub" % (mapName))
			mapImage.SetPosition(0, self.toolTipHeight)
			mapImage.SetWindowHorizontalAlignCenter()
			mapSizeDict = constInfo.mapSizeDict

			if not mapName in mapSizeDict:
				atlas = open("game/atlasinfo.txt", "r")
				content = atlas.readlines()
				for i in content:
					row = i.split("\t")
					if row[0] == mapName:
						constInfo.mapSizeDict[mapName] = [int(row[4]), int(row[5])]
				atlas.close()
			if pointShow:
				pointImageX = (xPos / float(mapSizeDict[mapName][0] * (128 * 200)) * float(mapImage.GetWidth())) * 100 - 15.0
				pointImageY = (yPos / float(mapSizeDict[mapName][1] * (128 * 200)) * float(mapImage.GetHeight())) * 100 - 15.0

				pointImage = ui.AniImageBox()
				pointImage.SetParent(mapImage)
				pointImage.SetDelay(6)
				for i in xrange(1, 13):
					pointImage.AppendImage("d:/ymir work/ui/minimap/mini_waypoint%02d.sub" % i)
				pointImage.SetPosition(pointImageX, pointImageY)
				pointImage.Show()

			self.toolTipWidth = max(self.toolTipWidth, mapImage.GetWidth() + 20)
			self.toolTipHeight += mapImage.GetHeight()

			self.childrenList.append(mapImage)
			if pointShow:
				self.childrenList.append(pointImage)
			self.ResizeToolTip()
		except:
			pass

	if gcGetEnable("ENABLE_TOOLTIP_CATEGORIES"):
		def AppendCategoryInfo(self):
			itemType = item.GetItemType()
			itemSubType = item.GetItemSubType()

			generalCategory = self.CATEGORIES_GENERAL.get(itemType, None)
			specificCategory = self.CATEGORIES_SPECIFIC.get((itemType, itemSubType), None)

			if generalCategory:
				self.AppendTextLine(localeInfo.TOOLTIP_CATEGORY + "{}".format(generalCategory))

			if specificCategory:
				self.AppendTextLine(localeInfo.TOOLTIP_SUB_CATEGORY + "{}".format(specificCategory))

	def __DragonSoulInfoString (self, dwVnum):
		step = (dwVnum / 100) % 10
		refine = (dwVnum / 10) % 10
		if 0 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL1 + " " + localeInfo.DRAGON_SOUL_STRENGTH.format(refine)
		elif 1 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL2 + " " + localeInfo.DRAGON_SOUL_STRENGTH.format(refine)
		elif 2 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL3 + " " + localeInfo.DRAGON_SOUL_STRENGTH.format(refine)
		elif 3 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL4 + " " + localeInfo.DRAGON_SOUL_STRENGTH.format(refine)
		elif 4 == step:
			return localeInfo.DRAGON_SOUL_STEP_LEVEL5 + " " + localeInfo.DRAGON_SOUL_STRENGTH.format(refine)
		else:
			return ""

	def __IsHair(self, itemVnum):
		return (self.__IsOldHair(itemVnum) or
			self.__IsNewHair(itemVnum) or
			self.__IsNewHair2(itemVnum) or
			self.__IsNewHair3(itemVnum)
		)

	def __IsOldHair(self, itemVnum):
		return itemVnum > 73000 and itemVnum < 74000

	def __IsNewHair(self, itemVnum):
		return itemVnum > 74000 and itemVnum < 75000

	def __IsNewHair2(self, itemVnum):
		return itemVnum > 75000 and itemVnum < 76000

	def __IsNewHair3(self, itemVnum):
		return ((74012 < itemVnum and itemVnum < 74022) or
			(74262 < itemVnum and itemVnum < 74272) or
			(74512 < itemVnum and itemVnum < 74522) or
			(74544 < itemVnum and itemVnum < 74560) or
			(74762 < itemVnum and itemVnum < 74772) or
			(45000 < itemVnum and itemVnum < 47000))

	def __AppendHairIcon(self, itemVnum):
		itemImage = ui.ImageBox()
		itemImage.SetParent(self)
		itemImage.Show()

		if self.__IsOldHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum)+".tga")
		elif self.__IsNewHair3(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))
		elif self.__IsNewHair(itemVnum):
			itemImage.LoadImage("d:/ymir work/item/quest/"+str(itemVnum-1000)+".tga")
		elif self.__IsNewHair2(itemVnum):
			itemImage.LoadImage("icon/hair/%d.sub" % (itemVnum))

		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.isPrivateSearchItem:
				itemImage.SetPosition((self.toolTipWidth/2)-48, self.toolTipHeight)
			else:
				itemImage.SetPosition((self.toolTipWidth/2)-48, self.toolTipHeight)
		else:
			itemImage.SetPosition(itemImage.GetWidth()/2, self.toolTipHeight)
		self.toolTipHeight += itemImage.GetHeight()
		#self.toolTipWidth += itemImage.GetWidth()/2
		self.childrenList.append(itemImage)
		self.ResizeToolTip()
		
	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def __AppendPrivateItemIcon(self, itemVnum):
			itemImage = ui.ImageBox()
			itemImage.SetParent(self)
			itemImage.Show()
			item.SelectItem(itemVnum)
			itemImage.LoadImage(item.GetIconImageFileName())
			itemImage.SetPosition((self.toolTipWidth/2)-16, self.toolTipHeight)
			self.toolTipHeight += itemImage.GetHeight()
			self.childrenList.append(itemImage)
			self.ResizeToolTip()

	def __AdjustMaxWidth(self, attrSlot, desc):
		newToolTipWidth = self.toolTipWidth
		newToolTipWidth = max(self.__AdjustAttrMaxWidth(attrSlot), newToolTipWidth)
		newToolTipWidth = max(self.__AdjustDescMaxWidth(desc), newToolTipWidth)
		if newToolTipWidth > self.toolTipWidth:
			self.toolTipWidth = newToolTipWidth
			self.ResizeToolTip()

	def __AdjustAttrMaxWidth(self, attrSlot):
		if 0 == attrSlot:
			return self.toolTipWidth

		maxWidth = self.toolTipWidth
		for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
			type = attrSlot[i][0]
			value = attrSlot[i][1]
			if self.ATTRIBUTE_NEED_WIDTH.has_key(type):
				if value > 0:
					maxWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], maxWidth)

					# ATTR_CHANGE_TOOLTIP_WIDTH
					#self.toolTipWidth = max(self.ATTRIBUTE_NEED_WIDTH[type], self.toolTipWidth)
					#self.ResizeToolTip()
					# END_OF_ATTR_CHANGE_TOOLTIP_WIDTH

		return maxWidth

	def __AdjustDescMaxWidth(self, desc):
		if len(desc) < DESC_DEFAULT_MAX_COLS:
			return self.toolTipWidth

		return DESC_WESTERN_MAX_WIDTH

	def __SetSkillBookToolTip(self, skillIndex, bookName, skillGrade):
		skillName = skill.GetSkillName(skillIndex)

		if not skillName:
			return

		itemName = skillName + " " + bookName
		self.SetTitle(itemName)

	def __AppendPickInformation(self, curLevel, curEXP, maxEXP):
		pick_configuration = {
			0 : { "chance" : 0, "quantity" : (0, 0)},
			1 : { "chance" : 1, "quantity" : (1, 1)},
			2 : { "chance" : 2, "quantity" : (2, 2)},
			3 : { "chance" : 3, "quantity" : (3, 3)},
			4 : { "chance" : 4, "quantity" : (4, 4)},
			5 : { "chance" : 5, "quantity" : (6, 5)},
			6 : { "chance" : 6, "quantity" : (8, 6)},
			7 : { "chance" : 7, "quantity" : (10, 7)},
			8 : { "chance" : 8, "quantity" : (12, 8)},
			9 : { "chance" : 10, "quantity" : (15, 10)},
		}

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_LEVEL.format(colorInfo.Colorize(curLevel, 0xFFffd169)), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_EXP.format(colorInfo.Colorize(curEXP, 0xFFffd169), colorInfo.Colorize(maxEXP, 0xFFffd169)), self.NORMAL_COLOR)

		text = localeInfo.TOOLTIP_PICK_PERCENT.format(str(pick_configuration[curLevel].get("chance", 0)) + "%")
		self.AppendTextLine(self.GetFormattedColorString(text, pick_configuration[curLevel].get("chance", 0), self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_QUANTITY_NORMAL.format(colorInfo.Colorize("+" + str(pick_configuration[curLevel].get("quantity")[0]), 0xFFffd169)))
		self.AppendTextLine(localeInfo.TOOLTIP_PICK_QUANTITY_SPECIAL.format(colorInfo.Colorize("+" + str(pick_configuration[curLevel].get("quantity")[1]), 0xFFffd169)))

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_PICK_UPGRADE3, self.NORMAL_COLOR)

	def __AppendRodInformation(self, curLevel, curEXP, maxEXP):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_LEVEL % (curLevel), self.NORMAL_COLOR)
		self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_EXP % (curEXP, maxEXP), self.NORMAL_COLOR)

		if curEXP == maxEXP:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE1, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE2, self.NORMAL_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_FISHINGROD_UPGRADE3, self.NORMAL_COLOR)

	def __AppendLimitInformation(self):
		appendSpace = False

		for i in xrange(item.LIMIT_MAX_NUM):

			(limitType, limitValue) = item.GetLimit(i)

			if limitValue > 0:
				if False == appendSpace:
					appendSpace = True

			else:
				if item.LIMIT_LEVEL == limitType:
					self.AppendTextLine(self.GetFormattedColorString(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % 1, 1, self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.ENABLE_COLOR)
				continue

			if item.LIMIT_LEVEL == limitType:
				bColor = self.COLOR_CONFIGURATION[self.POSITIVE_COLOR] if player.GetStatus(player.LEVEL) >= limitValue else self.COLOR_CONFIGURATION[self.NEGATIVE_COLOR] 
				self.AppendTextLine(self.GetFormattedColorString(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % limitValue, limitValue, bColor), self.ENABLE_COLOR)

	## cyh itemseal 2013 11 11
	def __AppendSealInformation(self, window_type, slotIndex):
		if not app.ENABLE_SOULBIND_SYSTEM:
			return

		itemSealDate = player.GetItemSealDate(window_type, slotIndex)
		if itemSealDate == item.GetDefaultSealDate():
			return

		if itemSealDate == item.GetUnlimitedSealDate():
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_SEALED, self.NEGATIVE_COLOR)

		elif itemSealDate > 0:
			self.AppendSpace(5)
			hours, minutes = player.GetItemUnSealLeftTime(window_type, slotIndex)
			self.AppendTextLine(localeInfo.TOOLTIP_UNSEAL_LEFT_TIME % (hours, minutes), self.NEGATIVE_COLOR)

	def __GetAffectString(self, affectType, affectValue, bFormat = True):
		if 0 == affectType:
			return None

		if 0 == affectValue and affectType != item.APPLY_MOV_SPEED:
			return None

		try:
			if (bFormat):
				affectColor, affectValueColor = self.__GetAttributeColor(0, affectValue, affectType, True)
				return self.GetFormattedColorString(localeInfo.AFFECT_DICT[affectType].format(affectValue), affectValue, affectValueColor, 1)
			else:
				return localeInfo.AFFECT_DICT[affectType].format(affectValue)

		except TypeError:
			return "UNKNOWN_VALUE[%s] %s" % (affectType, affectValue)
		except ValueError:
			return "Not found a index"
		except KeyError:
			return "UNKNOWN_TYPE[%s] %s" % (affectType, affectValue)

	def GetAffectString(self, affectType, affectValue, bFormat = True):
		return self.__GetAffectString(affectType, affectValue, bFormat)

	def __AppendSetInformation(self, index):
		id = item.GetItemEquipmentSetId(index)

		if id == 0:
			return
		
		set = equipmentSet.get(id)
		if not set:
			return

		self.AppendSpace(5)
		self.AppendTextLine("{}".format(set.name), self.HIGH_PRICE_COLOR)
		
		eqSet = equipmentSet.getEq()
		for (type, value, count) in set.applies:
			applyString = self.__GetAffectString(type, value, False)
			color = self.__GetAttributeColor(0, value, type, False)
			curColor = color[0]
			
			if count > eqSet.get(id, 0):
				curColor = self.GENERAL_INFO_COLOR

			self.AppendTextLine("[{}] - {}".format(count, applyString), color = curColor)

	def __AppendAffectInformation(self):
		for i in xrange(item.ITEM_APPLY_MAX_NUM):

			(affectType, affectValue) = item.GetAffect(i)

			affectString = self.__GetAffectString(affectType, affectValue)

			if affectString:
				self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue, type = affectType))

	def AppendAntiflagInformation(self):
		antiFlagDict = {
			"assets/ui/tool_tip/anti_flags/cant_drop.png": item.IsAntiFlag(item.ITEM_ANTIFLAG_DROP),
			"assets/ui/tool_tip/anti_flags/cant_sell.png": item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL),
			"assets/ui/tool_tip/anti_flags/cant_exchange.png": item.IsAntiFlag(item.ITEM_ANTIFLAG_GIVE),
			"assets/ui/tool_tip/anti_flags/cant_stack.png": item.IsAntiFlag(item.ITEM_ANTIFLAG_STACK),
			"assets/ui/tool_tip/anti_flags/cant_myshop.png": item.IsAntiFlag(item.ITEM_ANTIFLAG_MYSHOP),
			"assets/ui/tool_tip/anti_flags/cant_safebox.png": item.IsAntiFlag(item.ITEM_ANTIFLAG_SAFEBOX),
		}

		antiFlagNames = [name for name, flag in antiFlagDict.iteritems() if flag]
		if antiFlagNames:
			self.AppendTextLine(localeInfo.ANTIFLAG_INFORMATION_HEADER, self.NORMAL_COLOR)
			self.AppendTupleImages(antiFlagNames)

	if gcGetEnable("ENABLE_FAST_INTERACTIONS"):
		def AppendShortcuts(self, slotIndex, itemVnum, helper = -1):
			shortcuts = []

			item.SelectItem(itemVnum)

			for key, values in introInterface.data["shortcust_windows"].items():
				if "window" in values:
					if player.IsEquipmentSlot(slotIndex):
						continue

					if values["window"](self):
						if "blocked" in values:
							if helper:
								if helper == values["blocked"]:
									return

						if key == introInterface.STORAGE_WND:
							if values["range_1"](slotIndex):
								shortcuts.append(values["desc_1"])
							elif values["range_2"](slotIndex):
								shortcuts.append(values["desc_2"])
						elif key == introInterface.SHOP_WND and helper == introInterface.SHOP_WND:
							return

						else:
							if key == introInterface.SHOP_WND:
								if slotIndex in self.interface.wndInventory.gcGetSellingList:
									shortcuts.append(values["desc_2"])
								else:
									shortcuts.append(values["desc_1"])
							else:
								shortcuts.append(values["desc"])

			for key, values in introInterface.data["shortcust_items"].items():
				if key != introInterface.ITEM_PREVIEW and player.IsEquipmentSlot(slotIndex):
					continue

				if "check" in values:
					check = values["check"](slotIndex, itemVnum, item)
					if check == True:
						shortcuts.append(values["desc"])

			if len(shortcuts) > 0:
				for shortcut in shortcuts:
					self.AppendShortcut(*shortcut)

	def AppendWearableInformation(self):
		if self.__CheckAntiFlag() == True:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.DISABLE_COLOR)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_WEARABLE_JOB, self.NORMAL_COLOR)

		gSex, gRaces, perSex = self.GetRandomCharBasedInItem()
		nRaces = []
		for pRaces in gRaces:
			if perSex:
				nRaces.append(pRaces[gSex[0]] + ".png")
			else:
				for sR in pRaces:
					nRaces.append(sR + ".png")
		
		self.AppendTupleImages(nRaces, 2)

	def GetRandomCharBasedInItem(self):
		ASSASSINS 		= [ "assets/ui/tool_tip/races/enabled/assassin_w", "assets/ui/tool_tip/races/enabled/assassin_m" ]
		WARRIORS 		= [ "assets/ui/tool_tip/races/enabled/warrior_w", "assets/ui/tool_tip/races/enabled/warrior_m" ]
		SURAS 			= [ "assets/ui/tool_tip/races/enabled/sura_w", "assets/ui/tool_tip/races/enabled/sura_m" ]
		SHAMANS 		= [ "assets/ui/tool_tip/races/enabled/shaman_w", "assets/ui/tool_tip/races/enabled/shaman_m" ]
		ITEM_CHARACTERS = [ ASSASSINS, WARRIORS, SURAS, SHAMANS ]

		SEX_FEMALE		= 0
		SEX_MALE		= 1
		ITEM_SEX		= [ SEX_FEMALE, SEX_MALE ]

		if item.IsAntiFlag( item.ITEM_ANTIFLAG_MALE ):
			ITEM_SEX.remove( SEX_MALE )
		if item.IsAntiFlag( item.ITEM_ANTIFLAG_FEMALE ):
			ITEM_SEX.remove( SEX_FEMALE )
		if item.IsAntiFlag( item.ITEM_ANTIFLAG_WARRIOR ):
			ITEM_CHARACTERS.remove( WARRIORS )
		if item.IsAntiFlag( item.ITEM_ANTIFLAG_SURA ):
			ITEM_CHARACTERS.remove( SURAS )
		if item.IsAntiFlag( item.ITEM_ANTIFLAG_ASSASSIN ):
			ITEM_CHARACTERS.remove( ASSASSINS )
		if item.IsAntiFlag( item.ITEM_ANTIFLAG_SHAMAN ):
			ITEM_CHARACTERS.remove( SHAMANS )

		return ITEM_SEX, ITEM_CHARACTERS, len(ITEM_SEX) - 1 == 0

	def __AppendPotionInformation(self):
		self.AppendSpace(5)

		healHP = item.GetValue(0)
		healSP = item.GetValue(1)
		healStatus = item.GetValue(2)
		healPercentageHP = item.GetValue(3)
		healPercentageSP = item.GetValue(4)

		if healHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_POINT % healHP, self.GetChangeTextLineColor(healHP))
		if healSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_POINT % healSP, self.GetChangeTextLineColor(healSP))
		if healStatus != 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_CURE)
		if healPercentageHP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_HP_PERCENT % healPercentageHP, self.GetChangeTextLineColor(healPercentageHP))
		if healPercentageSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_SP_PERCENT % healPercentageSP, self.GetChangeTextLineColor(healPercentageSP))

	def __AppendAbilityPotionInformation(self):

		self.AppendSpace(5)

		abilityType = item.GetValue(0)
		time = item.GetValue(1)
		point = item.GetValue(2)

		if abilityType == item.APPLY_ATT_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_ATTACK_SPEED % point, self.GetChangeTextLineColor(point))
		elif abilityType == item.APPLY_MOV_SPEED:
			self.AppendTextLine(localeInfo.TOOLTIP_POTION_PLUS_MOVING_SPEED % point, self.GetChangeTextLineColor(point))

		if time > 0:
			minute = (time / 60)
			second = (time % 60)
			timeString = localeInfo.TOOLTIP_POTION_TIME

			if minute > 0:
				timeString += str(minute) + localeInfo.TOOLTIP_POTION_MIN
			if second > 0:
				timeString += " " + str(second) + localeInfo.TOOLTIP_POTION_SEC

			self.AppendTextLine(timeString)

	def GetPriceColor(self, price):
		if price>=constInfo.HIGH_PRICE:
			return self.HIGH_PRICE_COLOR
		if price>=constInfo.MIDDLE_PRICE:
			return self.MIDDLE_PRICE_COLOR
		else:
			return self.LOW_PRICE_COLOR

	def AppendPrice(self, price, priceColor = None):
		if priceColor == None:
			priceColor = self.GetPriceColor(price)
		self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToStringAsType(price, True, localeInfo.SHOP_TYPE_MONEY)), priceColor)

		self.refreshFuncAdd = self.AppendPrice
		self.refreshArgsAdd = (price, priceColor)

	def AppendPriceItem(self, price, priceVnum):
		if priceVnum == 0:
			self.AppendPrice(price)
			return

		item.SelectItem(priceVnum)

		baseTextFormatter = "<TEXT color=" + str(self.GetPriceColor(price)) + " outline=1 text=\"%s\">"
		imageText = (baseTextFormatter % localeInfo.NumberToString(price) + "x") + " <IMAGE path=\"" + item.GetIconImageFileName() + "\"> " + (baseTextFormatter % item.GetItemName())
		text = localeInfo.TOOLTIP_BUYPRICE

		splitPos = text.find("%s")
		frontText = baseTextFormatter % text[:splitPos]
		endText = text[splitPos+2:]
		if endText.strip():
			endText = baseTextFormatter % endText

		self.AppendSpace(5)
		self.AppendTextLineEx(frontText + imageText + endText, True)

		self.refreshFuncAdd = self.AppendPriceItem
		self.refreshArgsAdd = (price,priceVnum,)

	def AppendPriceBySecondaryCoin(self, price):
		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_BUYPRICE  % (localeInfo.NumberToSecondaryCoinString(price)), self.GetPriceColor(price))

	def AppendSellingPrice(self, price):
		if item.IsAntiFlag(item.ITEM_ANTIFLAG_SELL):
			self.AutoAppendTextLine(localeInfo.TOOLTIP_ANTI_SELL, self.DISABLE_COLOR)
		else:
			self.AppendTextLine(localeInfo.TOOLTIP_SELLPRICE % (localeInfo.NumberToStringAsType(price, True, localeInfo.SHOP_TYPE_MONEY)), self.GetPriceColor(price))

		self.refreshFuncAdd = self.AppendSellingPrice
		self.refreshArgsAdd = (price,)

	"""ENABLE_LEGENDARY_STONES"""
	def AppendMetinInformation(self, metinSlot = 0, bLegendaryStoneRefine = False):
		if constInfo.ENABLE_FULLSTONE_DETAILS:
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affectType, affectValue) = item.GetAffect(i)

				if gcGetEnable("ENABLE_LEGENDARY_STONES"):
					iLegendaryValue = metinSlot[0]
					if bLegendaryStoneRefine:
						iLegendaryValue = "{} ~ {}".format(iLegendaryValue, item.GetValue(4))

					affectString = self.__GetAffectString(affectType, iLegendaryValue if iLegendaryValue > 0 else affectValue)
				else:
					affectString = self.__GetAffectString(affectType, affectValue)

				if affectString:
					# self.AppendSpace(5)
					self.AppendTextLine(affectString, self.GetChangeTextLineColor(affectValue))

	def AppendMetinWearInformation(self):
		# self.AppendTextLine(localeInfo.TOOLTIP_SOCKET_REFINABLE_ITEM, self.NORMAL_COLOR)

		flagList = (item.IsWearableFlag(item.WEARABLE_BODY),
					item.IsWearableFlag(item.WEARABLE_HEAD),
					item.IsWearableFlag(item.WEARABLE_FOOTS),
					item.IsWearableFlag(item.WEARABLE_WRIST),
					item.IsWearableFlag(item.WEARABLE_WEAPON),
					item.IsWearableFlag(item.WEARABLE_NECK),
					item.IsWearableFlag(item.WEARABLE_EAR),
					item.IsWearableFlag(item.WEARABLE_UNIQUE),
					item.IsWearableFlag(item.WEARABLE_SHIELD),
					item.IsWearableFlag(item.WEARABLE_ARROW))

		wearNames = ""
		for i in xrange(self.WEAR_COUNT):

			name = self.WEAR_NAMES[i]
			flag = flagList[i]

			if flag:
				wearNames += name

		self.AppendTextLine("[{} {}]".format(localeInfo.TOOLTIP_SOUL_STONE, wearNames))
		self.ResizeToolTip()

	def GetMetinSocketType(self, number):
		if player.METIN_SOCKET_TYPE_NONE == number:
			return player.METIN_SOCKET_TYPE_NONE
		elif player.METIN_SOCKET_TYPE_SILVER == number:
			return player.METIN_SOCKET_TYPE_SILVER
		elif player.METIN_SOCKET_TYPE_GOLD == number:
			return player.METIN_SOCKET_TYPE_GOLD
		else:
			item.SelectItem(number)
			if item.METIN_NORMAL == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_SILVER
			elif item.METIN_GOLD == item.GetItemSubType():
				return player.METIN_SOCKET_TYPE_GOLD
			elif "USE_PUT_INTO_ACCESSORY_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_RING_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER
			elif "USE_PUT_INTO_BELT_SOCKET" == item.GetUseType(number):
				return player.METIN_SOCKET_TYPE_SILVER

		return player.METIN_SOCKET_TYPE_NONE

	def GetMetinItemIndex(self, number):
		if player.METIN_SOCKET_TYPE_SILVER == number:
			return 0
		if player.METIN_SOCKET_TYPE_GOLD == number:
			return 0

		return number

	# ENABLE_ORE_REFACTOR mtrlVnum = 0
	def __AppendAccessoryMetinSlotInfo(self, metinSlot, mtrlVnum = 0):
		ACCESSORY_SOCKET_MAX_SIZE = 3

		cur=min(metinSlot[0], ACCESSORY_SOCKET_MAX_SIZE)
		end=min(metinSlot[1], ACCESSORY_SOCKET_MAX_SIZE)

		affectType1, affectValue1 = item.GetAffect(0)
		affectList1=[0, max(1, affectValue1*10/100), max(2, affectValue1*20/100), max(3, affectValue1*40/100)]

		affectType2, affectValue2 = item.GetAffect(1)
		affectList2=[0, max(1, affectValue2*10/100), max(2, affectValue2*20/100), max(3, affectValue2*40/100)]

		affectType3, affectValue3 = item.GetAffect(2)
		affectList3=[0, max(1, affectValue3*10/100), max(2, affectValue3*20/100), max(3, affectValue3*40/100)]

		if gcGetEnable("ENABLE_TOOLTIP_ACCESSORY_SOCKET"):
			################# Position Renewal #########################
			if cur > 0 or end > 0:
				windowBack = ui.Window()
				windowBack.SetParent(self)

				gapWidth = 20
				for i in xrange(end):
					slotImage = ui.ImageBox()
					slotImage.SetParent(windowBack)
					slotImage.SetPosition((36 + gapWidth) * i, 0)
					slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
					slotImage.Show()

					if i < cur:
						item.SelectItem(mtrlVnum)
						itemImage = ui.ImageBox()
						itemImage.SetParent(slotImage)
						itemImage.SetPosition(2, 1)
						itemImage.LoadImage(item.GetIconImageFileName())
						itemImage.Show()

						self.childrenList.append(itemImage)

					self.childrenList.append(slotImage)

				windowBack.SetPosition(0, self.toolTipHeight + 4)
				windowBack.SetSize((36 * end) + (gapWidth * (end - 1)), 36)
				windowBack.SetWindowHorizontalAlignCenter()
				windowBack.Show()

				self.toolTipHeight += 40
				self.childrenList.append(windowBack)

				if cur > 0:
					item.SelectItem(mtrlVnum)
					itemNameTextLine = ui.TextLine()
					itemNameTextLine.SetParent(self)
					itemNameTextLine.SetHorizontalAlignCenter()
					itemNameTextLine.SetPosition(self.toolTipWidth / 2, self.toolTipHeight + 4)
					itemNameTextLine.SetFontName(self.defFontName)
					itemNameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
					itemNameTextLine.SetText(item.GetItemName())
					itemNameTextLine.SetOutline()
					itemNameTextLine.SetFeather()
					itemNameTextLine.Show()

					self.toolTipHeight += 18
					self.childrenList.append(itemNameTextLine)

					affectTotal = [0] * 3
					for aff in xrange(cur):
						affectTotal[0] += affectList1[aff + 1] - affectList1[aff]
						affectTotal[1] += affectList2[aff + 1] - affectList2[aff]
						affectTotal[2] += affectList3[aff + 1] - affectList3[aff]

					affectStrings = [self.__GetAffectString(affectType1, affectTotal[0]),
									self.__GetAffectString(affectType2, affectTotal[1]),
									self.__GetAffectString(affectType3, affectTotal[2])]

					for affectString in affectStrings:
						if affectString:
							affectTextLine = ui.TextLine()
							affectTextLine.SetParent(self)
							affectTextLine.SetHorizontalAlignCenter()
							affectTextLine.SetPosition(self.toolTipWidth / 2, self.toolTipHeight + 4)
							affectTextLine.SetFontName(self.defFontName)
							affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
							affectTextLine.SetOutline()
							affectTextLine.SetFeather()
							affectTextLine.SetText(affectString)
							affectTextLine.Show()

							self.toolTipHeight += 18
							self.childrenList.append(affectTextLine)

					leftTime = metinSlot[2]
					if leftTime:
						timeText = ("|cFF68bcff" + localeInfo.LEFT_TIME + ":|r " + localeInfo.SecondToDHM(leftTime))

						timeTextLine = ui.TextLine()
						timeTextLine.SetParent(self)
						timeTextLine.SetHorizontalAlignCenter()
						timeTextLine.SetPosition(self.toolTipWidth / 2, self.toolTipHeight + 4)
						timeTextLine.SetFontName(self.defFontName)
						timeTextLine.SetPackedFontColor(self.NORMAL_COLOR)
						timeTextLine.SetOutline()
						timeTextLine.SetFeather()
						timeTextLine.Show()
						timeTextLine.SetText(timeText)

						self.toolTipHeight += 18
						self.childrenList.append(timeTextLine)

				self.ResizeToolTip()
			################# Position Renewal #########################
		else:
			mtrlPos=0
			if app.ENABLE_ORE_REFACTOR:
				mtrlList=[]
				for x in range(end):
					mtrlList.append(metinSlot[2+x] if not metinSlot[2+x] == 0 else 1)
			else:
				mtrlList=[mtrlVnum]*cur+[player.METIN_SOCKET_TYPE_SILVER]*(end-cur)

			for mtrl in mtrlList:
			# for rIT in xrange(ACCESSORY_SOCKET_MAX_SIZE):
				affectString1 = self.__GetAffectString(affectType1, affectList1[mtrlPos+1]-affectList1[mtrlPos])
				affectString2 = self.__GetAffectString(affectType2, affectList2[mtrlPos+1]-affectList2[mtrlPos])
				affectString3 = self.__GetAffectString(affectType3, affectList3[mtrlPos+1]-affectList3[mtrlPos])


				leftTime = 0
				if cur == mtrlPos+1:
					leftTime=metinSlot[2]

				self.__AppendMetinSlotInfo_AppendMetinSocketData(mtrlPos, mtrl, affectString1, affectString2, affectString3, leftTime)
				mtrlPos+=1
	
	## ENABLE_SASH_COSTUME_SYSTEM
	def __AppendMetinSlotInfo(self, metinSlot, bIsSash = False):
		if self.__AppendMetinSlotInfo_IsEmptySlotList(metinSlot):
			return

		if gcGetEnable("ENABLE_LEGENDARY_STONES"):
			for i in xrange(len(metinSlot[:6]) / 2):
				## ENABLE_SASH_COSTUME_SYSTEM
				self.__AppendMetinSocketDataRef(i, metinSlot[i], iMetinSlotDataLegendaryValue = metinSlot[i + len(metinSlot[:6]) / 2], bIsSash = bIsSash, iAbsorption = metinSlot[player.SASH_TYPE_SOCKET])
		else:
			for i in xrange(player.METIN_SOCKET_MAX_NUM):
				self.__AppendMetinSlotInfo_AppendMetinSocketData(i, metinSlot[i])

	def __AppendMetinSlotInfo_IsEmptySlotList(self, metinSlot):
		if 0 == metinSlot:
			return 1

		for i in xrange(player.METIN_SOCKET_MAX_NUM):
			metinSlotData=metinSlot[i]
			if app.ENABLE_SASH_COSTUME_SYSTEM:
				if i >= player.SASH_TYPE_SOCKET:
					return 1
			if 0 != self.GetMetinSocketType(metinSlotData):
				if 0 != self.GetMetinItemIndex(metinSlotData):
					return 0

		return 1
	
	if gcGetEnable("ENABLE_LEGENDARY_STONES"):
		def __AppendMetinSocketDataRef(self, iIndex, iMetinSlotData, iMetinSlotDataLegendaryValue, bIsSash, iAbsorption):
			iSlotType = self.GetMetinSocketType(iMetinSlotData)
			iSelectedItem = self.GetMetinItemIndex(iMetinSlotData)

			if iSlotType == 0:
				return

			self.AppendSpace(5)

			slotImage = ui.ImageBox()
			slotImage.SetParent(self)
			slotImage.Show()

			## Name
			nameTextLine = ui.TextLine()
			nameTextLine.SetParent(self)
			nameTextLine.SetFontName(self.defFontName)
			nameTextLine.SetPackedFontColor(0xFFf1e6c0)
			nameTextLine.SetOutline()
			nameTextLine.SetFeather()
			nameTextLine.Show()

			self.childrenList.append(nameTextLine)

			if iMetinSlotDataLegendaryValue != 0:
				slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")
			else:
				slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")

			self.childrenList.append(slotImage)
			slotImage.SetPosition(9, self.toolTipHeight - 1)

			nameTextLine.SetPosition(50, self.toolTipHeight + 2)

			metinImage = ui.ImageBox()
			metinImage.SetParent(self)
			metinImage.Show()
			self.childrenList.append(metinImage)

			if iSelectedItem:
				item.SelectItem(iSelectedItem)

				## Image
				try:
					metinImage.LoadImage(item.GetIconImageFileName())
				except:
					dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" %
						(iSelectedItem, item.GetIconImageFileName())
					)

				nameTextLine.SetText(item.GetItemName())

				## Affect
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()

				metinImage.SetPosition(10, self.toolTipHeight)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

				affectType, affectValue = item.GetAffect(0)
				affectValue = iMetinSlotDataLegendaryValue if iMetinSlotDataLegendaryValue else affectValue

				if (bIsSash and iAbsorption != 0):
					f_abs = lambda val : max(1, int(float(val)*float(iAbsorption)/100.0))
					affectValue = f_abs(affectValue)

				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					affectTextLine.SetText(affectString)
					(textWidth, textHeight) = affectTextLine.GetTextSize()
					textWidth += 60

					if self.toolTipWidth < textWidth:
						self.toolTipWidth = textWidth

				self.childrenList.append(affectTextLine)

			self.toolTipHeight += 35
			self.ResizeToolTip()

	def __AppendMetinSlotInfo_AppendMetinSocketData(self, index, metinSlotData, custumAffectString="", custumAffectString2="", custumAffectString3="", leftTime=0):
		slotType = self.GetMetinSocketType(metinSlotData)
		itemIndex = self.GetMetinItemIndex(metinSlotData)

		if 0 == slotType:
			return

		self.AppendSpace(5)

		slotImage = ui.ImageBox()
		slotImage.SetParent(self)
		slotImage.Show()

		## Name
		nameTextLine = ui.TextLine()
		nameTextLine.SetParent(self)
		nameTextLine.SetFontName(self.defFontName)
		nameTextLine.SetPackedFontColor(self.NORMAL_COLOR)
		nameTextLine.SetOutline()
		nameTextLine.SetFeather()
		nameTextLine.Show()

		self.childrenList.append(nameTextLine)

		if player.METIN_SOCKET_TYPE_SILVER == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_silver.sub")
		elif player.METIN_SOCKET_TYPE_GOLD == slotType:
			slotImage.LoadImage("d:/ymir work/ui/game/windows/metin_slot_gold.sub")

		self.childrenList.append(slotImage)

		slotImage.SetPosition(9, self.toolTipHeight-1)
		nameTextLine.SetPosition(50, self.toolTipHeight + 2)

		metinImage = ui.ImageBox()
		metinImage.SetParent(self)
		metinImage.Show()
		self.childrenList.append(metinImage)

		if itemIndex:

			item.SelectItem(itemIndex)

			## Image
			try:
				metinImage.LoadImage(item.GetIconImageFileName())
			except:
				dbg.TraceError("ItemToolTip.__AppendMetinSocketData() - Failed to find image file %d:%s" %
					(itemIndex, item.GetIconImageFileName())
				)

			nameTextLine.SetText(item.GetItemName())

			## Affect
			affectTextLine = ui.TextLine()
			affectTextLine.SetParent(self)
			affectTextLine.SetFontName(self.defFontName)
			affectTextLine.SetPackedFontColor(0xFFf1e6c0)
			affectTextLine.SetOutline()
			affectTextLine.SetFeather()
			affectTextLine.Show()

			metinImage.SetPosition(10, self.toolTipHeight)
			affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2)

			if custumAffectString:
				affectTextLine.SetText(custumAffectString)
			elif itemIndex!=constInfo.ERROR_METIN_STONE:
				affectType, affectValue = item.GetAffect(0)
				affectString = self.__GetAffectString(affectType, affectValue)
				if affectString:
					affectTextLine.SetText(affectString)
			else:
				affectTextLine.SetText(localeInfo.TOOLTIP_APPLY_NOAFFECT)

			self.childrenList.append(affectTextLine)

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString2) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString2 = self.__GetAffectString(*item.GetAffect(1))

			if custumAffectString2:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString2)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

				if app.ENABLE_ORE_REFACTOR:
					if custumAffectString3 == "":
						self.__AppendAccessoryType(itemIndex)

			if constInfo.ENABLE_FULLSTONE_DETAILS and (not custumAffectString3) and (itemIndex!=constInfo.ERROR_METIN_STONE):
				custumAffectString3 = self.__GetAffectString(*item.GetAffect(2))

			if custumAffectString3:
				affectTextLine = ui.TextLine()
				affectTextLine.SetParent(self)
				affectTextLine.SetFontName(self.defFontName)
				affectTextLine.SetPackedFontColor(self.POSITIVE_COLOR)
				affectTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				affectTextLine.SetOutline()
				affectTextLine.SetFeather()
				affectTextLine.Show()
				affectTextLine.SetText(custumAffectString3)
				self.childrenList.append(affectTextLine)
				self.toolTipHeight += 16 + 2

				if app.ENABLE_ORE_REFACTOR:
					self.__AppendAccessoryType(itemIndex)

			if 0 != leftTime:
				timeText = ("|cFF68bcff" + localeInfo.LEFT_TIME + ":|r " + localeInfo.SecondToNiceTime(leftTime))

				timeTextLine = ui.TextLine()
				timeTextLine.SetParent(self)
				timeTextLine.SetFontName(self.defFontName)
				# timeTextLine.SetPackedFontColor(self.LEFT_TIME)
				timeTextLine.SetPosition(50, self.toolTipHeight + 16 + 2 + 16 + 2)
				timeTextLine.SetOutline()
				timeTextLine.SetFeather()
				timeTextLine.Show()
				timeTextLine.SetText(timeText)
				self.childrenList.append(timeTextLine)
				self.toolTipHeight += 16 + 2

		else:
			nameTextLine.SetText(localeInfo.TOOLTIP_SOCKET_EMPTY)

		self.toolTipHeight += 35
		self.ResizeToolTip()

	if app.ENABLE_ORE_REFACTOR:
		def __AppendAccesoryInformation(self, lMetinSlots):
			ACCESSORY_SOCKET_MAX_SIZE = 3
			H_ADDER = 14

			iCur, iMax = (min(lMetinSlots[i], ACCESSORY_SOCKET_MAX_SIZE) for i in xrange(2))
			
			## Lets store the list of affects
			lAffects = []
			for i in xrange(item.ITEM_APPLY_MAX_NUM):
				(affType, affValue) = item.GetAffect(i)
				if (affType == 0):
					continue

				lAffects.append([item.GetAffect(i)[0], item.GetValue(i)])

			## List of slots
			lSlots = ("metin_slot_gold.sub", "metin_slot_silver.sub")

			## Lets build the slots
			for i in xrange(iMax):
				self.AppendSpace(3)

				pSlotImage = ui.ImageBox()
				pSlotImage.SetPosition(9, self.toolTipHeight - 1)
				pSlotImage.LoadImage("d:/ymir work/ui/game/windows/{}".format(lSlots[1]))
				pSlotImage.Show()

				if i < iCur:
					iVnum = lMetinSlots[2 + i]
					
					item.SelectItem(iVnum)

					## Check if item is normal one
					bIsNormal = item.GetValue(5) == 0
					pSlotImage.LoadImage("d:/ymir work/ui/game/windows/{}".format(lSlots[bIsNormal]))

					pItemImage = ui.ImageBox()
					pItemImage.SetParent(pSlotImage)
					pItemImage.SetPosition(2, 1)
					pItemImage.LoadImage(item.GetIconImageFileName())
					pItemImage.Show()

					self.childrenList.append(pItemImage)

					pItemName = ui.TextLine()
					pItemName.SetParent(self)
					pItemName.SetPosition(50, self.toolTipHeight)
					pItemName.SetFontName(self.defFontName)
					pItemName.SetPackedFontColor(0xFFf1e6c0)
					pItemName.SetOutline()
					pItemName.SetFeather()
					pItemName.SetText(item.GetItemName())
					pItemName.Show()

					self.childrenList.append(pItemName)

					## Append Bonuses
					for key, value in enumerate(lAffects):
						affString = self.__GetAffectString(value[0], value[1] * item.GetValue(3), True)
						if not affString:
							continue

						pAffectString = ui.TextLine()
						pAffectString.SetParent(self)
						pAffectString.SetPosition(50, self.toolTipHeight + H_ADDER)
						pAffectString.SetFontName(self.defFontName)
						pAffectString.SetPackedFontColor(self.POSITIVE_COLOR)
						pAffectString.SetOutline()
						pAffectString.SetFeather()
						pAffectString.SetText(affString)
						pAffectString.Show()

						self.toolTipHeight += H_ADDER
						self.childrenList.append(pAffectString)

					## Append the time text!
					pTimeString = ui.TextLine()
					pTimeString.SetParent(self)
					pTimeString.SetPosition(50, self.toolTipHeight + H_ADDER)
					pTimeString.SetFontName(self.defFontName)
					pTimeString.SetPackedFontColor(self.NORMAL_COLOR)
					pTimeString.SetOutline()
					pTimeString.SetFeather()
					pTimeString.SetText(self.__GetAccessoryType(iVnum, lMetinSlots[5 + i]))
					pTimeString.Show()

					self.childrenList.append(pTimeString)

				self.AppendChild(pSlotImage, bCenter = False)

		def __GetAccessoryType(self, iVnum, iLeftTime = 0):
			item.SelectItem(iVnum)
			
			ITEM_TYPES = (localeInfo.TOOLTIP_ACCESSORY_PERMANENT, "|cFF68bcff" + localeInfo.TIME_LEFT_ORE + ":|r " + colorInfo.Colorize(localeInfo.FormatSeconds(iLeftTime), 0xFFffffff))

			##Checking if the accessory is normal one
			bIsNormal = item.GetValue(5) == 0

			return ITEM_TYPES[bIsNormal]

	def __AppendFishInfo(self, size):
		if size > 0:
			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_FISH_LEN % (float(size) / 100.0), self.NORMAL_COLOR)

	def AppendUniqueItemLastTime(self, restMin):
		restSecond = restMin*60
		self.AppendTextLine(colorInfo.Colorize(localeInfo.TOOLTIP_TIME_HEADER, 0xFF68bcff) + " " + localeInfo.SecondToDHMSShort(restSecond), self.NORMAL_COLOR)

	def AppendLeftTimeSeconds(self, seconds):
		self.AppendTextLine(colorInfo.Colorize(localeInfo.TOOLTIP_TIME_HEADER, 0xFF68bcff) + " " + localeInfo.SecondToDHMSShort(seconds), self.NORMAL_COLOR)

	def AppendMallItemLastTime(self, endTime):
		leftSec = max(0, endTime - app.GetGlobalTimeStamp())
		self.AppendLeftTimeSeconds(leftSec)

	def AppendTimerBasedOnWearLastTime(self, metinSlot):
		if 0 == metinSlot[0]:
			self.AppendTextLine(localeInfo.CANNOT_USE, self.DISABLE_COLOR)
		else:
			endTime = app.GetGlobalTimeStamp() + metinSlot[0]
			self.AppendMallItemLastTime(endTime)

	def AppendRealTimeStartFirstUseLastTime(self, item, metinSlot, limitIndex, defaultValue = 0):
		useCount = metinSlot[1]
		endTime = metinSlot[0]

		if endTime == 0 and defaultValue > 0:
			self.AppendLeftTimeSeconds(defaultValue)
			return

		if 0 == useCount:
			if 0 == endTime:
				(limitType, limitValue) = item.GetLimit(limitIndex)
				endTime = limitValue

			self.AppendLeftTimeSeconds(endTime)
		else:
			self.AppendMallItemLastTime(endTime)

	if app.ENABLE_SASH_COSTUME_SYSTEM:
		def	__AppendSashInfo(self, attrSlot, metinSlot, sashRefineItem = -1):
			if metinSlot != 0:
				f_abs = lambda val : max(1, int(float(val)*float(metinSlot[player.SASH_TYPE_SOCKET])/100.0))

				if metinSlot[player.METIN_SOCKET_MAX_NUM - 1] == 0:
					sText = localeInfo.SASH_SYSTEM_ABSORPTION_TITLE % metinSlot[player.SASH_TYPE_SOCKET]
					self.AppendTextLine(self.GetFormattedColorString(sText, metinSlot[player.SASH_TYPE_SOCKET], self.COLOR_CONFIGURATION[self.SPECIAL_COLOR_GOLD], 1), self.ABSORPTION_TITLE_COLOR)
				else:
					sText = localeInfo.SASH_SYSTEM_ABSORPTION_TITLE_COMBINATION % (metinSlot[player.SASH_TYPE_SOCKET], metinSlot[player.METIN_SOCKET_MAX_NUM - 1])
					self.AppendTextLine(self.GetFormattedColorString(sText, metinSlot[player.SASH_TYPE_SOCKET], self.COLOR_CONFIGURATION[self.SPECIAL_COLOR_GOLD], 1), self.ABSORPTION_TITLE_COLOR)

				self.AppendSpace(5)

				## Base stats
				if metinSlot[player.SASH_ABSORPTION_SOCKET] > 0:
					item.SelectItem(sashRefineItem if sashRefineItem > -1 else metinSlot[player.SASH_ABSORPTION_SOCKET])

					if item.GetItemType() == item.ITEM_TYPE_WEAPON:
						## Att (for weapons)
						if f_abs(item.GetValue(3)+item.GetValue(5)) != f_abs(item.GetValue(4)+item.GetValue(5)):
							sText = localeInfo.TOOLTIP_ITEM_ATT_POWER % (f_abs(item.GetValue(3)+item.GetValue(5)), f_abs(item.GetValue(4)+item.GetValue(5)))
							self.AppendTextLine(self.GetFormattedColorString(sText, f_abs(item.GetValue(3)+item.GetValue(5)), self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)
						else:
							sText = localeInfo.TOOLTIP_ITEM_ATT_POWER_ONE_ARG % f_abs(item.GetValue(3)+item.GetValue(5))
							self.AppendTextLine(self.GetFormattedColorString(sText, f_abs(item.GetValue(3)+item.GetValue(5)), self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)

						item.SelectItem(sashRefineItem if sashRefineItem > -1 else metinSlot[player.SASH_ABSORPTION_SOCKET])

						if f_abs(item.GetValue(1)+item.GetValue(5)) != f_abs(item.GetValue(2)+item.GetValue(5)):
							sText = localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER % (f_abs(item.GetValue(1)+item.GetValue(5)), f_abs(item.GetValue(2)+item.GetValue(5)))
							self.AppendTextLine(self.GetFormattedColorString(sText, (f_abs(item.GetValue(1)+item.GetValue(5)), f_abs(item.GetValue(2)+item.GetValue(5))), self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)
						else:
							sText = localeInfo.TOOLTIP_ITEM_MAGIC_ATT_POWER_ONE_ARG % f_abs(item.GetValue(1)+item.GetValue(5))
							self.AppendTextLine(self.GetFormattedColorString(sText, f_abs(item.GetValue(1)+item.GetValue(5)), self.COLOR_CONFIGURATION[self.POSITIVE_COLOR]), self.POSITIVE_COLOR)

					elif item.GetItemType() == item.ITEM_TYPE_ARMOR:
						## Def (for armors)
						self.AppendTextLine(localeInfo.TOOLTIP_ITEM_DEF_GRADE % f_abs(item.GetValue(1)+(item.GetValue(5)*2)), self.POSITIVE_COLOR)

					## Applies
					for i in xrange(item.ITEM_APPLY_MAX_NUM):

						item.SelectItem(sashRefineItem if sashRefineItem > -1 else metinSlot[player.SASH_ABSORPTION_SOCKET])
						(affectType, affectValue) = item.GetAffect(i)

						if f_abs(affectValue) <= 0:
							continue

						affectString = self.__GetAffectString(affectType, f_abs(affectValue))
						if affectString:
							self.AppendTextLine(affectString, self.POSITIVE_COLOR)

			## Attrs
			if 0 != attrSlot:

				for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
					type = attrSlot[i][0]
					value = f_abs(attrSlot[i][1])

					if 0 >= value:
						continue

					affectString = self.__GetAffectString(type, value)
					if affectString:
						self.AppendTextLine(affectString, self.POSITIVE_COLOR)

			## Absorbed Item
			if metinSlot[player.SASH_ABSORPTION_SOCKET] > 0:
				self.AppendSpace(3)
				self.AppendTextLine(localeInfo.TOOLTIP_ABSORBED_ITEM, self.TRANSMUTATION_TITLE_COLOR)

				self.AppendTextLine(item.GetItemName(), self.TRANSMUTATION_ITEMNAME_COLOR)

				self.AppendSpace(3)

				if 0 != attrSlot:

					for i in xrange(player.ATTRIBUTE_SLOT_MAX_NUM):
						type = attrSlot[i][0]
						value = attrSlot[i][1]

						affectString = self.__GetAffectString(type, value, False)
						if affectString:
							affectColor, affectValueColor = self.__GetAttributeColor(i, value, type)
							self.AppendTextLine(self.GetFormattedColorString(affectString, value, affectValueColor, 1), affectColor)

							# self.AppendTextLine(affectString, self.POSITIVE_COLOR)

	def GetFormattedColorString(self, data, value, color, bSize = 0):
		value = str(value)
		sIndexValue = data.find(str(value))

		#! In case if we doesn't have any value to find!
		if sIndexValue < 0:
			return data

		bColor = ("|cFF" + color) if color else ""
		if sIndexValue == 0:
			sPairFirst, sPairSecond = (data[:len(value) + bSize], data[len(value) + bSize:])
			return (bColor + sPairFirst + "|r" + sPairSecond)
		
		sPairFirst, sPairSecond = (data[:sIndexValue - bSize], data[sIndexValue - bSize:])
		return (sPairFirst + bColor + sPairSecond)

	def GetFormattedStringTuple(self, data, values, color, bSize = 0):
		sIndexValues = (
			data.find(str(values[0])),
			data.find(str(values[1]))
		)

		sPair_First, sPair_Second = (data[:sIndexValues[0] - bSize], data[sIndexValues[0] - bSize:])

		formattedString = (sPair_First + "|cFF{}".format(color) + sPair_Second)

	def OnUpdate(self):
		ToolTip.OnUpdate(self)

		if self.refreshFunc != None and (app.GetTime() - self.lastRefreshTime) > 0.5:
			funcAdd = self.refreshFuncAdd
			argsAdd = self.refreshArgsAdd
			apply(self.refreshFunc, self.refreshArgs)
			if funcAdd != None:
				self.refreshFuncAdd = funcAdd
				self.refreshArgsAdd = argsAdd
				apply(funcAdd, argsAdd)

	def OnKeyDown(self, key):
		if not self.IsShow():
			return
		
		if key == app.DIK_LALT:
			if self.dataToolTip:
				self.dataToolTip.ShowToolTip()

	def OnKeyUp(self, key):
		if not self.IsShow():
			return

		if key == app.DIK_LALT:
			if self.dataToolTip:
				self.dataToolTip.HideToolTip()

class HyperlinkItemToolTip(ItemToolTip):
	def __init__(self):
		ItemToolTip.__init__(self, isPickable=True)

	def SetHyperlinkItem(self, tokens):
		minTokenCount = 4 + player.METIN_SOCKET_MAX_NUM
		maxTokenCount = minTokenCount + 2 * player.ATTRIBUTE_SLOT_MAX_NUM
		if tokens and len(tokens) >= minTokenCount and len(tokens) <= maxTokenCount:
			head, vnum, refineElement, flag = tokens[:4]

			if app.ENABLE_TRANSMUTATION_SYSTEM:
				itemVnum = str(vnum)
			else:
				itemVnum = int(vnum, 16)

			metinSlot = [int(metin, 16) for metin in tokens[4:14]]

			if app.ENABLE_TRANSMUTATION_SYSTEM:
				abc = itemVnum.split("|")
				itemVnum = int(abc[0], 16)
				lookvnum = int(abc[1])

			rests = tokens[14:]
			if rests:
				attrSlot = []

				rests.reverse()

				if rests[0].find("|") != -1:
					rests[0] = rests[0].split("|")[0]
					bDemo = True

				while rests:
					key = int(rests.pop(), 16)
					if rests:
						val = int(rests.pop())
						attrSlot.append((key, val))

				# attrSlot += [(0, 0)] * (player.ATTRIBUTE_SLOT_MAX_NUM - len(attrSlot))
			else:
				attrSlot = [(0, 0)] * player.ATTRIBUTE_SLOT_MAX_NUM

			self.ClearToolTip()
			if app.ENABLE_TRANSMUTATION_SYSTEM:
				self.AddItemData(itemVnum, metinSlot, attrSlot, refineElement = int(refineElement), trans_id=lookvnum, bShowIcon = True)
			else:
				self.AddItemData(itemVnum, metinSlot, attrSlot, bShowIcon = True)

			ItemToolTip.OnUpdate(self)

	def OnUpdate(self):
		pass

	def OnMouseLeftButtonDown(self):
		self.Hide()

class SkillToolTip(ToolTip):

	POINT_NAME_DICT = {
		player.LEVEL : localeInfo.SKILL_TOOLTIP_LEVEL,
		player.IQ : localeInfo.SKILL_TOOLTIP_INT,
	}

	SKILL_TOOL_TIP_WIDTH = 200
	PARTY_SKILL_TOOL_TIP_WIDTH = 340

	PARTY_SKILL_EXPERIENCE_AFFECT_LIST = (	( 2, 2,  10,),
											( 8, 3,  20,),
											(14, 4,  30,),
											(22, 5,  45,),
											(28, 6,  60,),
											(34, 7,  80,),
											(38, 8, 100,), )

	PARTY_SKILL_PLUS_GRADE_AFFECT_LIST = (	( 4, 2, 1, 0,),
											(10, 3, 2, 0,),
											(16, 4, 2, 1,),
											(24, 5, 2, 2,), )

	PARTY_SKILL_ATTACKER_AFFECT_LIST = (	( 36, 3, ),
											( 26, 1, ),
											( 32, 2, ), )

	SKILL_GRADE_NAME = {	player.SKILL_GRADE_MASTER : localeInfo.SKILL_GRADE_NAME_MASTER,
							player.SKILL_GRADE_GRAND_MASTER : localeInfo.SKILL_GRADE_NAME_GRAND_MASTER,
							player.SKILL_GRADE_PERFECT_MASTER : localeInfo.SKILL_GRADE_NAME_PERFECT_MASTER, }

	AFFECT_NAME_DICT =	{
							"HP" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_POWER,
							"ATT_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_GRADE,
							"DEF_GRADE" : localeInfo.TOOLTIP_SKILL_AFFECT_DEF_GRADE,
							"ATT_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_ATT_SPEED,
							"MOV_SPEED" : localeInfo.TOOLTIP_SKILL_AFFECT_MOV_SPEED,
							"DODGE" : localeInfo.TOOLTIP_SKILL_AFFECT_DODGE,
							"RESIST_NORMAL" : localeInfo.TOOLTIP_SKILL_AFFECT_RESIST_NORMAL,
							"REFLECT_MELEE" : localeInfo.TOOLTIP_SKILL_AFFECT_REFLECT_MELEE,
						}
	AFFECT_APPEND_TEXT_DICT =	{
									"DODGE" : "%",
									"RESIST_NORMAL" : "%",
									"REFLECT_MELEE" : "%",
								}

	def __init__(self):
		ToolTip.__init__(self, self.SKILL_TOOL_TIP_WIDTH)

	def __del__(self):
		ToolTip.__del__(self)

	def SetSkill(self, skillIndex, skillLevel = -1):

		if 0 == skillIndex:
			return

		if skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			## NEW
			self.AppendExtraInfoInSkill(skillIndex)

			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillGrade = player.GetSkillGrade(slotIndex)
			skillLevel = player.GetSkillLevel(slotIndex)
			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex)
			## NEW
			self.AppendExtraInfoInSkill(skillIndex)

			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def SetSkillNew(self, slotIndex, skillIndex, skillGrade, skillLevel):

		if 0 == skillIndex:
			return

		if player.SKILL_INDEX_TONGSOL == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillLevel = player.GetSkillLevel(slotIndex)

			self.AppendDefaultData(skillIndex)
			self.AppendPartySkillData(skillGrade, skillLevel)

			if gcGetEnable("ENABLE_SKILLS_INFORMATION"):
				SKILL_DATA = {
					player.SKILL_GRADE_NORMAL : 50301,
					player.SKILL_GRADE_MASTER : 50302,
					player.SKILL_GRADE_GRAND_MASTER : 50303,
					player.SKILL_GRADE_PERFECT_MASTER : 0,
				}

				self.AppendPassiveSkillInformation(skillIndex, SKILL_DATA[skillGrade])

		elif player.SKILL_INDEX_RIDING == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			self.AppendSupportSkillDefaultData(skillIndex, skillGrade, skillLevel, 30)

		elif player.SKILL_INDEX_SUMMON == skillIndex:

			maxLevel = 10

			self.ClearToolTip()
			self.__SetSkillTitle(skillIndex, skillGrade)

			## Description
			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)

			if skillLevel == 10:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				text = localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel*10)
				find = text.find("+")

				self.AppendTextLine(text[:find] + colorInfo.Colorize(text[find:], 0xFFffd169), self.POSITIVE_COLOR)
			else:
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.__AppendSummonDescription(skillLevel, self.POSITIVE_COLOR)

				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel+1), self.NEGATIVE_COLOR)
				self.__AppendSummonDescription(skillLevel+1, self.NEGATIVE_COLOR)

		elif skill.SKILL_TYPE_GUILD == skill.GetSkillType(skillIndex):

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			## NEW
			self.AppendExtraInfoInSkill(skillIndex)

			self.AppendSkillConditionData(skillIndex)
			self.AppendGuildSkillData(skillIndex, skillLevel)

		elif gcGetEnable("ENABLE_SKILLS_INFORMATION") and player.SKILL_INDEX_POLYMORPH == skillIndex:

			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillLevel = player.GetSkillLevel(slotIndex)

			self.AppendDefaultData(skillIndex)

			SKILL_DATA = {
				player.SKILL_GRADE_NORMAL : [5, 5, 50314],
				player.SKILL_GRADE_MASTER : [10, 15, 50315],
				player.SKILL_GRADE_GRAND_MASTER : [15, 25, 50316],
				player.SKILL_GRADE_PERFECT_MASTER : [25, 35, 0],
			}

			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_POLYMORPH_DAMAGE + colorInfo.Colorize(" {}%".format(SKILL_DATA[skillGrade][0]), 0xFFffd169), self.POSITIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_POLYMORPH_DURATION + colorInfo.Colorize(" {}min".format(SKILL_DATA[skillGrade][0]), 0xFFffd169), self.POSITIVE_COLOR)

			self.AppendPassiveSkillInformation(skillIndex, SKILL_DATA[skillGrade][2])

		elif gcGetEnable("ENABLE_LEGENDARY_STONES") and 146 == skillIndex:
			self.ClearToolTip()

			self.__SetSkillTitle(skillIndex, skillGrade)

			## Description
			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)

			self.AppendSpace(5)

			data = constInfo.LEGENDARY_PASSIVE_INFO
			totalGivedStones = 0
			for key in xrange(len(data)):
				(vnum, gived, required) = data[key]

				if gived == required:
					totalGivedStones += 1

			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEGENDARY_STONES_GIVED + " " + CFF.format("{}/{}".format(totalGivedStones, len(data)), "#ffd169"), 0xFF89b88d)
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEGENDARY_SUCCESS_RATE + " " + CFF.format("{}%".format((totalGivedStones * 2) + 9 if totalGivedStones == len(data) else 0), "#ffd169"), 0xFF89b88d)

			self.AppendSpace(4)

			self.AppendTextLine(localeInfo.LEGENDARY_STONES_PASSIVE_USE_INFO, 0xFF66c1ff)
			sText = "<TEXT color=" + str(grp.GenerateColor(102.0 / 255.0, 193.0 / 255.0, 255.0 / 255.0, 1.0)) + " outline=1 text=\"{}\">".format(localeInfo.TOOLTIP_SKILL_LEGENDARY_USE_IT)
			sText += "<IMAGE path=\"{}\">".format("assets/ui/keyboard/keyboard_mouse_right.png")

			self.AppendTextLineEx(sText, True)

			self.AppendSpace(10)

			LINES = [
				localeInfo.TOOLTIP_SKILL_LEGENDARY_LINE_0_0,
				localeInfo.TOOLTIP_SKILL_LEGENDARY_LINE_0_1,
				localeInfo.TOOLTIP_SKILL_LEGENDARY_LINE_0_2,
			]

			for rItem in LINES:
				self.AppendTextLine(rItem)

			self.AppendSpace(6)

			LINES = [
				localeInfo.TOOLTIP_SKILL_LEGENDARY_LINE_1_0,
				localeInfo.TOOLTIP_SKILL_LEGENDARY_LINE_1_1,
			]

			for rItem in LINES:
				self.AppendTextLine(rItem, 0xFFb0dfb4)
		
		elif app.ENABLE_AMULET_SYSTEM and 147 == skillIndex:
			self.ClearToolTip()

			self.__SetSkillTitle(skillIndex, skillGrade)

			## Description
			description = skill.GetSkillDescription(skillIndex)
			self.AppendDescription(description, 25)

			self.AppendSpace(5)

			LINES = [
				localeInfo.AMULET_PASSIVE_TYPE.format("II"),
				localeInfo.AMULET_PASSIVE_TYPE.format("III"),
				localeInfo.AMULET_PASSIVE_TYPE.format("IV"),
				localeInfo.AMULET_PASSIVE_TYPE.format("V")
			]

			if 1 == skillGrade:
				skillLevel += 19
			elif 2 == skillGrade:
				skillLevel += 29
			elif 3 == skillGrade:
				skillLevel = 40

			it = 0
			for rItem in LINES:
				if skillLevel == 0:
					self.AppendTextLine(localeInfo.AMULET_PASSIVE_CHANCE + " " + rItem + ": {}%".format(0), self.NEGATIVE_COLOR)
				else:
					self.AppendTextLine(localeInfo.AMULET_PASSIVE_CHANCE + " " + rItem + ": {}%".format(constInfo.AMULET_PASSIVE.get(skillLevel)[it]), self.POSITIVE_COLOR if int(constInfo.AMULET_PASSIVE.get(skillLevel)[it]) > 0 else self.NEGATIVE_COLOR)
				it += 1

			if gcGetEnable("ENABLE_SKILLS_INFORMATION"):
				SKILL_DATA = {
					player.SKILL_GRADE_NORMAL : 178107,
					player.SKILL_GRADE_MASTER : 178108,
					player.SKILL_GRADE_GRAND_MASTER : 178109,
				}

				self.AppendPassiveSkillInformation(skillIndex, SKILL_DATA.get(skillGrade, 0))

		else:

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			slotIndex = player.GetSkillSlotIndex(skillIndex)

			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)
			skillNextPercentage = player.GetSkillNextEfficientPercentage(slotIndex)

			self.AppendDefaultData(skillIndex, skillGrade)


			## NEW
			self.AppendExtraInfoInSkill(skillIndex)

			self.AppendSkillConditionData(skillIndex)

			if gcGetEnable("ENABLE_SKILLS_INFORMATION"):
				self.AppendNormalSkillInformation(skillIndex, skillGrade)

			self.AppendSkillDataNew(slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage)
			self.AppendSkillRequirement(skillIndex, skillLevel)

		self.ShowToolTip()

	def __SetSkillTitle(self, skillIndex, skillGrade):
		if chr.IsGameMaster(player.GetMainCharacterIndex()):
			self.SetTitle(skill.GetSkillName(skillIndex, skillGrade) + " ({})".format(skillIndex))
		else:
			self.SetTitle(skill.GetSkillName(skillIndex, skillGrade))
		self.__AppendSkillGradeName(skillIndex, skillGrade)

	def __AppendSkillGradeName(self, skillIndex, skillGrade):
		if self.SKILL_GRADE_NAME.has_key(skillGrade):
			self.AppendSpace(5)
			self.AppendTextLine(self.SKILL_GRADE_NAME[skillGrade] % (skill.GetSkillName(skillIndex, 0)), self.CAN_LEVEL_UP_COLOR)

	def SetSkillOnlyName(self, slotIndex, skillIndex, skillGrade):
		if 0 == skillIndex:
			return

		slotIndex = player.GetSkillSlotIndex(skillIndex)

		self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
		self.ResizeToolTip()

		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)
		self.AppendDefaultData(skillIndex, skillGrade)
		## NEW
		self.AppendExtraInfoInSkill(skillIndex)
		self.AppendSkillConditionData(skillIndex)
		self.ShowToolTip()

	def AppendDefaultData(self, skillIndex, skillGrade = 0):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Level Limit
		levelLimit = skill.GetSkillLevelLimit(skillIndex)
		if levelLimit > 0:

			color = self.NORMAL_COLOR
			if player.GetStatus(player.LEVEL) < levelLimit:
				color = self.NEGATIVE_COLOR

			self.AppendSpace(5)
			self.AppendTextLine(localeInfo.TOOLTIP_ITEM_LIMIT_LEVEL % (levelLimit), color)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

	def AppendSupportSkillDefaultData(self, skillIndex, skillGrade, skillLevel, maxLevel):
		self.ClearToolTip()
		self.__SetSkillTitle(skillIndex, skillGrade)

		## Description
		description = skill.GetSkillDescription(skillIndex)
		self.AppendDescription(description, 25)

		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel = 40

		self.AppendSpace(5)
		self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_WITH_MAX % (skillLevel, maxLevel), self.NORMAL_COLOR)

	def AppendSkillConditionData(self, skillIndex):
		conditionDataCount = skill.GetSkillConditionDescriptionCount(skillIndex)
		if conditionDataCount > 0:
			self.AppendSpace(5)
			for i in xrange(conditionDataCount):
				self.AppendTextLine(skill.GetSkillConditionDescription(skillIndex, i), self.CONDITION_COLOR)

	if gcGetEnable("ENABLE_SKILLS_INFORMATION"):
		def AppendNormalSkillInformation(self, skillIndex, skillGrade):
			if skillIndex in constInfo.SKILL_INFO:
				if skillGrade in (player.SKILL_GRADE_MASTER, player.SKILL_GRADE_GRAND_MASTER):
					self.AppendHorizontalLine()
					data = constInfo.SKILL_INFO[skillIndex][0]
					
					if (data.get("GRADE") == player.SKILL_GRADE_MASTER):
						self.AppendReaded(data.get("READED"), data.get("REQUIRED") + 1)

					""" Append percent text"""
					self.AppendChance(data.get("PERCENT"), data.get("APERCENT"), data.get("GRADE") == player.SKILL_GRADE_GRAND_MASTER)

					""" Append info about APercent active """
					if (data.get("APERCENT")):
						self.AppendTextLine(localeInfo.TOOLTIP_SKILL_ADDITIONAL_INFORMATION_ADDED_PERCENT, 0xFFffd169)

					""" Check time condination """
					self.AppendTime(data.get("TIME"))

					""" Append required item """
					lNames = []
					if (data.get("STANDARD")):
						if (data.get("GRADE") == player.SKILL_GRADE_MASTER):
							skillBook = 0
							for itemVnum in constInfo.SKILL_BOOKS:
								item.SelectItem(itemVnum)

								if skillIndex == item.GetValue(0):
									skillBook = itemVnum

							lNames.append(skillBook)
						else:
							lNames = [50513, 50569]

						self.AppendTextLine(localeInfo.TOOLTIP_SKILL_ADDITIONAL_INFORMATION_REQUIRED_ITEM, 0xFF11B4E3)
						for rElement in lNames:
							item.SelectItem(rElement)

							self.AppendTextLine(CFF.format(item.GetItemName(), "#ffd169"))
							# self.AppendTextLineEx(self.AppendRequiredItemLine(), True)

					self.AppendHorizontalLine()

		def AppendRequiredItemLine(self):
			return "<TEXT color=" + str(grp.GenerateColor(0.85, 0.85, 0.85, 1.0)) + " outline=1 text=\"%s\">" % item.GetItemName() + " <IMAGE path=\"" + item.GetIconImageFileName() + "\"> "

		def AppendPassiveSkillInformation(self, skillIndex, skillBook):
			if skillIndex in constInfo.SKILL_INFO:
				data = constInfo.SKILL_INFO[skillIndex][0]
				if (data.get("GRADE") != player.SKILL_GRADE_PERFECT_MASTER):
					self.AppendHorizontalLine()

					""" Append required count """
					if (data.get("GRADE") in (player.SKILL_GRADE_MASTER, player.SKILL_GRADE_GRAND_MASTER)):
						self.AppendReaded(data.get("READED"), data.get("REQUIRED") + 1)

					""" Append percent text"""
					self.AppendChance(data.get("PERCENT"), data.get("APERCENT"))

					""" Append info about APercent active """
					if (data.get("APERCENT")):
						self.AppendTextLine(localeInfo.TOOLTIP_SKILL_ADDITIONAL_INFORMATION_ADDED_PERCENT, 0xFFffd169)

					""" Check time condination """
					self.AppendTime(data.get("TIME"))

					if skillBook != 0:
						item.SelectItem(skillBook)
						self.AppendTextLine(localeInfo.TOOLTIP_SKILL_ADDITIONAL_INFORMATION_REQUIRED_ITEM, 0xFF11B4E3)
						self.AppendTextLine(CFF.format(item.GetItemName(), "#ffd169"))

					self.AppendHorizontalLine()

		def AppendReaded(self, iReaded, iRequired):
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_ADDITIONAL_INFORMATION_AMOUNT + CFF.format(" {}/{}".format(iReaded, iRequired), '#ffd169'), 0xFF11B4E3)

		def AppendChance(self, iChance, iAddChance, bGrandMaster = False):
			sGreater = ""
			if (bGrandMaster):
				sGreater = "/{}%".format(iChance * 2 - 5)

			chanceTx = localeInfo.TOOLTIP_SKILL_ADDITIONAL_INFORMATION_CHANCE +  CFF.format(" {}%{}".format(iChance, sGreater), '#ffd169')
			if (iAddChance):
				chanceTx += CFF.format(" (+{}%)".format(iAddChance), '#ffd169')

			self.AppendTextLine(chanceTx, 0xFF11B4E3)

		def AppendTime(self, iTime):
			if app.GetTime() >= iTime:
				bText = localeInfo.TOOLTIP_SKILL_ADDITIONAL_INFORMATION_POSSIBLE_LEARN
			elif constInfo.SKILL_EXO:
				bText = localeInfo.TOOLTIP_SKILL_ADDITIONAL_INFORMATION_EXO_ACTIVE
			else:
				timeNew = iTime - app.GetTime()
				bText = CFF.format(localeInfo.TOOLTIP_SKILL_ADDITIONAL_INFORMATION_REMAINING, '#11B4E3') + " {}".format(localeInfo.SecondToHMS(timeNew))

			self.AppendTextLine("{}".format(bText), 0xFFffd169)

			self.AppendSpace(5)

	def AppendExtraInfoInSkill(self, skillIndex):
		if skillIndex == 66:
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_SURA_INFORMATION_0, self.NEGATIVE_COLOR)
			self.AppendTextLine(localeInfo.TOOLTIP_SKILL_SURA_INFORMATION_1, self.NEGATIVE_COLOR)

	def AppendGuildSkillData(self, skillIndex, skillLevel):
		skillMaxLevel = 7
		skillCurrentPercentage = float(skillLevel) / float(skillMaxLevel)
		skillNextPercentage = float(skillLevel+1) / float(skillMaxLevel)
		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillLevel == skillMaxLevel:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)

				#####

				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillCurrentPercentage), self.ENABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillCurrentPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.ENABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillCurrentPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.ENABLE_COLOR)

		## Next Level
		if skillLevel < skillMaxLevel:
			if self.HasSkillLevelDescription(skillIndex, skillLevel+1):
				self.AppendSpace(5)
				self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevel), self.DISABLE_COLOR)

				#####

				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillNextPercentage), self.DISABLE_COLOR)

				## Cooltime
				coolTime = skill.GetSkillCoolTime(skillIndex, skillNextPercentage)
				if coolTime > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), self.DISABLE_COLOR)

				## SP
				needGSP = skill.GetSkillNeedSP(skillIndex, skillNextPercentage)
				if needGSP > 0:
					self.AppendTextLine(localeInfo.TOOLTIP_NEED_GSP % (needGSP), self.DISABLE_COLOR)

	def AppendSkillDataNew(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage):

		self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
		self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

		skillLevelUpPoint = 1
		realSkillGrade = player.GetSkillGrade(slotIndex)
		skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
		skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

		## Current Level
		if skillLevel > 0:
			if self.HasSkillLevelDescription(skillIndex, skillLevel):
				self.AppendSpace(5)
				if skillGrade == skill.SKILL_GRADE_COUNT:
					pass
				elif skillLevel == skillMaxLevelEnd:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
				else:
					self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
				self.AppendSkillLevelDescriptionNew("current", skillGrade, skillIndex, skillCurrentPercentage, self.ENABLE_COLOR)

		## Next Level
		if skillGrade != skill.SKILL_GRADE_COUNT:
			if skillLevel < skillMaxLevelEnd:
				if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
					self.AppendSpace(5)
					if skillIndex == 141 or skillIndex == 142:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_3 % (skillLevel+1), self.DISABLE_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)
					self.AppendSkillLevelDescriptionNew("next", skillGrade, skillIndex, skillNextPercentage, self.DISABLE_COLOR)

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def SetSkillBuffNPC(self, slotIndex, skillIndex, skillGrade, skillLevel, curSkillPower, nextSkillPower, intPoints):

			if 0 == skillIndex:
				return

			self.AppendDefaultData(skillIndex, skillGrade)
			self.AppendSkillConditionData(skillIndex)
			self.AppendSkillDataBuffNPC(slotIndex, skillIndex, skillGrade, skillLevel, curSkillPower, nextSkillPower, intPoints)
			self.AppendSkillRequirement(skillIndex, skillLevel)

			self.ShowToolTip()
			
		def AppendSkillDataBuffNPC(self, slotIndex, skillIndex, skillGrade, skillLevel, skillCurrentPercentage, skillNextPercentage, intPoints):
			self.skillMaxLevelStartDict = { 0 : 17, 1 : 7, 2 : 10, }
			self.skillMaxLevelEndDict = { 0 : 20, 1 : 10, 2 : 10, }

			skillLevelUpPoint = 1
			realSkillGrade = player.GetSkillGrade(slotIndex)
			skillMaxLevelStart = self.skillMaxLevelStartDict.get(realSkillGrade, 15)
			skillMaxLevelEnd = self.skillMaxLevelEndDict.get(realSkillGrade, 20)

			## Current Level
			if skillLevel > 0:
				if self.HasSkillLevelDescription(skillIndex, skillLevel):
					self.AppendSpace(5)
					if skillGrade == skill.SKILL_GRADE_COUNT:
						pass
					elif skillLevel == skillMaxLevelEnd:
						self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.NORMAL_COLOR)
					else:
						self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.NORMAL_COLOR)
					self.AppendSkillLevelDescriptionBuffNPC(skillIndex, skillCurrentPercentage, self.ENABLE_COLOR, intPoints)

			## Next Level
			if skillGrade != skill.SKILL_GRADE_COUNT:
				if skillLevel < skillMaxLevelEnd:
					if self.HasSkillLevelDescription(skillIndex, skillLevel+skillLevelUpPoint):
						self.AppendSpace(5)
						if skillIndex == 141 or skillIndex == 142:
							self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_3 % (skillLevel+1), self.DISABLE_COLOR)
						else:
							self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skillMaxLevelEnd), self.DISABLE_COLOR)
						self.AppendSkillLevelDescriptionBuffNPC(skillIndex, skillNextPercentage, self.DISABLE_COLOR, intPoints)
					
		def AppendSkillLevelDescriptionBuffNPC(self, skillIndex, skillPercentage, color, intPoints):

			affectDataCount = skill.GetNewAffectDataCount(skillIndex)
			
			for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
				self.AppendTextLine(skill.GetBuffNPCSkillAffectDescription(skillIndex, i, skillPercentage, intPoints), color)

			duration = skill.GetDuration(skillIndex, skillPercentage)
			if duration > 0:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)

			coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
			if coolTime > 0:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)

	if app.ENABLE_PASSIVE_SKILLS_HELPER:
		def SetPassiveSkill(self, skillIndex, skillGrade, skillLevel):
			slotIndex = player.GetSkillSlotIndex(skillIndex)
			skillLevel = player.GetSkillLevel(slotIndex)
			skillCurrentPercentage = player.GetSkillCurrentEfficientPercentage(slotIndex)

			SkillHandler = constInfo.PASSIVE_SKILLS_DATA.get(skillIndex, None)
			if not slotIndex:
				return

			if self.SKILL_TOOL_TIP_WIDTH != self.toolTipWidth:
				self.toolTipWidth = self.SKILL_TOOL_TIP_WIDTH
				self.ResizeToolTip()

			self.AppendDefaultData(skillIndex)
			self.AppendSkillConditionData(skillIndex)

			if skillLevel == skill.GetSkillMaxLevel(skillIndex):
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL_MASTER % (skillLevel), self.CONDITION_COLOR)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_LEVEL % (skillLevel), self.POSITIVE_COLOR)

			# Actual Bonuses
			for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
				text = skill.GetSkillAffectDescription(skillIndex, i, skillLevel)
				splitText = text.find("+")

				self.AppendTextLine(text[:splitText] + colorInfo.Colorize(text[splitText:], 0xFF89ff8d), self.POSITIVE_COLOR)

			## Space for Mining System
			# self.AppendTextLine("Amount of Mining (normal) {} - {}".format())
			# self.AppendTextLine("Amount of Mining (special) {} - {}".format())

			# self.AppendTextLine("Chance of successful mining (normal) {} - {}".format())
			# self.AppendTextLine("Chance of successful mining (special) {} - {}".format())

			# Next Level Bonuses
			if skillLevel != skill.GetSkillMaxLevel(skillIndex):
				self.AppendTextLine(localeInfo.TOOLTIP_NEXT_SKILL_LEVEL_1 % (skillLevel+1, skill.GetSkillMaxLevel(skillIndex)), self.NEGATIVE_COLOR)
				for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
					text = skill.GetSkillAffectDescription(skillIndex, i, skillLevel+1)
					splitText = text.find("+")

					self.AppendTextLine(text[:splitText] + colorInfo.Colorize(text[splitText:], 0xFFff6460), self.NEGATIVE_COLOR)

			self.AppendSpace(5)

			self.ShowToolTip()

	def AppendSkillLevelDescriptionNew(self, skillEv, skillGrade, skillIndex, skillPercentage, color):

		affectDataCount = skill.GetNewAffectDataCount(skillIndex)

		if affectDataCount > 0:
			for i in xrange(affectDataCount):
				type, minValue, maxValue = skill.GetNewAffectData(skillIndex, i, skillPercentage)

				if not self.AFFECT_NAME_DICT.has_key(type):
					continue

				minValue = int(minValue)
				maxValue = int(maxValue)
				affectText = self.AFFECT_NAME_DICT[type]

				if "HP" == type:
					if minValue < 0 and maxValue < 0:
						minValue *= -1
						maxValue *= -1

					else:
						affectText = localeInfo.TOOLTIP_SKILL_AFFECT_HEAL

				affectText += str(minValue)
				if minValue != maxValue:
					affectText += " - " + str(maxValue)
				affectText += self.AFFECT_APPEND_TEXT_DICT.get(type, "")

				#import debugInfo
				#if debugInfo.IsDebugMode():
				#	affectText = "!!" + affectText

				self.AppendTextLine(affectText, color)

		else:
			for i in xrange(skill.GetSkillAffectDescriptionCount(skillIndex)):
				bSkill = skill.GetSkillAffectDescription(skillIndex, i, skillPercentage)

				bSplited = bSkill.split(":")
				if bSplited and skillEv == "current":
					type = bSplited[0]

					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillPercentage), self.SPECIAL_POSITIVE_COLOR)
				else:
					self.AppendTextLine(skill.GetSkillAffectDescription(skillIndex, i, skillPercentage), color)

			#TODO Translation
			NEW_BONUSES_FOR_SKILLS = {
				3 : "Silny przeciwko potworom: +%d%%",
				49 : "Silny przeciwko ludziom: +%d%%",
				110 : "Silny przeciwko ludziom: +%d%%",
				64 : "Silny przeciwko potworom: +%d%%",
			}

			bValue = 5
			if skillIndex in NEW_BONUSES_FOR_SKILLS:
				if skillGrade == 3 and skillEv == "current":
					self.AppendTextLine(NEW_BONUSES_FOR_SKILLS[skillIndex] % bValue, self.SPECIAL_POSITIVE_COLOR)
				elif skillGrade == 2 and skillEv == "next":
					self.AppendTextLine(NEW_BONUSES_FOR_SKILLS[skillIndex] % bValue, self.DISABLE_COLOR)

		## Duration
		duration = skill.GetDuration(skillIndex, skillPercentage)
		if duration > 0:
			if skillEv == "current":
				self.AppendTextLine("|cffffc49e" + localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_DURATION % (duration), color)

		## Cooltime
		coolTime = skill.GetSkillCoolTime(skillIndex, skillPercentage)
		if coolTime > 0:
			if skillEv == "current":
				self.AppendTextLine("|cffffffaa" + localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_SKILL_COOL_TIME + str(coolTime), color)

		## SP
		needSP = skill.GetSkillNeedSP(skillIndex, skillPercentage)
		if needSP != 0:
			continuationSP = skill.GetSkillContinuationSP(skillIndex, skillPercentage)

			if skill.IsUseHPSkill(skillIndex):
				self.AppendNeedHP(needSP, continuationSP, color)
			else:
				self.AppendNeedSP(skillEv, needSP, continuationSP, color)

	def AppendSkillRequirement(self, skillIndex, skillLevel):

		skillMaxLevel = skill.GetSkillMaxLevel(skillIndex)

		if skillLevel >= skillMaxLevel:
			return

		isAppendHorizontalLine = False

		## Requirement
		if skill.IsSkillRequirement(skillIndex):

			if not isAppendHorizontalLine:
				isAppendHorizontalLine = True
				self.AppendHorizontalLine()

			requireSkillName, requireSkillLevel = skill.GetSkillRequirementData(skillIndex)

			color = self.CANNOT_LEVEL_UP_COLOR
			if skill.CheckRequirementSueccess(skillIndex):
				color = self.CAN_LEVEL_UP_COLOR
			self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_SKILL_LEVEL % (requireSkillName, requireSkillLevel), color)

		## Require Stat
		requireStatCount = skill.GetSkillRequireStatCount(skillIndex)
		if requireStatCount > 0:

			for i in xrange(requireStatCount):
				type, level = skill.GetSkillRequireStatData(skillIndex, i)
				if self.POINT_NAME_DICT.has_key(type):

					if not isAppendHorizontalLine:
						isAppendHorizontalLine = True
						self.AppendHorizontalLine()

					name = self.POINT_NAME_DICT[type]
					color = self.CANNOT_LEVEL_UP_COLOR
					if player.GetStatus(type) >= level:
						color = self.CAN_LEVEL_UP_COLOR
					self.AppendTextLine(localeInfo.TOOLTIP_REQUIREMENT_STAT_LEVEL % (name, level), color)

	def HasSkillLevelDescription(self, skillIndex, skillLevel):
		if skill.GetSkillAffectDescriptionCount(skillIndex) > 0:
			return True
		if skill.GetSkillCoolTime(skillIndex, skillLevel) > 0:
			return True
		if skill.GetSkillNeedSP(skillIndex, skillLevel) > 0:
			return True

		return False

	def AppendMasterAffectDescription(self, index, desc, color):
		self.AppendTextLine(desc, color)

	def AppendNextAffectDescription(self, index, desc):
		self.AppendTextLine(desc, self.DISABLE_COLOR)

	def AppendNeedHP(self, needSP, continuationSP, color):

		self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP % (needSP), color)

		if continuationSP > 0:
			self.AppendTextLine(localeInfo.TOOLTIP_NEED_HP_PER_SEC % (continuationSP), color)

	def AppendNeedSP(self,skillEv, needSP, continuationSP, color):

		if -1 == needSP:
			if skillEv == "current":
				self.AppendTextLine("|cff4f92ff" + localeInfo.TOOLTIP_NEED_ALL_SP, color)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_NEED_ALL_SP, color)

		else:
			if skillEv == "current":
				self.AppendTextLine("|cff4f92ff" + localeInfo.TOOLTIP_NEED_SP % (needSP), color)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP % (needSP), color)

		if continuationSP > 0:
			if skillEv == "current":
				self.AppendTextLine("|cff4f92ff" + localeInfo.TOOLTIP_NEED_SP_PER_SEC % (continuationSP), color)
			else:
				self.AppendTextLine(localeInfo.TOOLTIP_NEED_SP_PER_SEC % (continuationSP), color)

	def AppendPartySkillData(self, skillGrade, skillLevel):
		if 1 == skillGrade:
			skillLevel += 19
		elif 2 == skillGrade:
			skillLevel += 29
		elif 3 == skillGrade:
			skillLevel = 40

		if skillLevel <= 0:
			return

		skillIndex = player.SKILL_INDEX_TONGSOL
		slotIndex = player.GetSkillSlotIndex(skillIndex)
		skillPower = player.GetSkillCurrentEfficientPercentage(slotIndex)
		k = skillLevel / 100.0
		self.AppendSpace(5)
		self.AutoAppendTextLine(localeInfo.TOOLTIP_PARTY_SKILL_LEVEL % skillLevel, self.NORMAL_COLOR)

		can_add_extras = bool(skillLevel == 40)

		if skillLevel>=10:
			attacker_calc = chop(20 + (200 * k))
			self.AutoAppendTextLine("{} {}".format((localeInfo.PARTY_SKILL_ATTACKER % attacker_calc), ["", "|cffd1a400(+%.1f)" % math.ceil(attacker_calc*0.1)][can_add_extras]))

		if skillLevel>=20:
			berserker_calc = chop(2 + (15 * k))
			self.AutoAppendTextLine("{} {}".format((localeInfo.PARTY_SKILL_BERSERKER % berserker_calc), ["", "|cffd1a400(+%.1f)" % math.ceil(berserker_calc*0.1)][can_add_extras]))
			tanker_calc = chop(500 + (3750 * k))
			self.AutoAppendTextLine("{} {}".format((localeInfo.PARTY_SKILL_TANKER % tanker_calc), ["", "|cffd1a400(+%.1f)" % math.ceil(tanker_calc*0.1)][can_add_extras]))

		if skillLevel>=25:
			buffer_calc = chop(6 + (60 * k))
			self.AutoAppendTextLine("{} {}".format((localeInfo.PARTY_SKILL_BUFFER % buffer_calc), ["", "|cffd1a400(+%.1f)" % math.ceil(buffer_calc*0.1)][can_add_extras]))

		if skillLevel>=35:
			skillmaster_calc = chop(10 + (100 * k))
			self.AutoAppendTextLine("{} {}".format((localeInfo.PARTY_SKILL_SKILL_MASTER % skillmaster_calc), ["", "|cffd1a400(+%.1f)" % math.ceil(skillmaster_calc*0.1)][can_add_extras]))

		if skillLevel>=40:
			defender_calc = chop(3.5 + (30 * k))
			self.AutoAppendTextLine("{} {}".format((localeInfo.PARTY_SKILL_DEFENDER % defender_calc), ["", "|cffd1a400(+%.1f)" % math.ceil(defender_calc*0.1)][can_add_extras]))

		if can_add_extras:
			self.AutoAppendTextLine("|cFFffcc99%s"%localeInfo.PARTY_PASSIVE_BONUS_1)
			self.AutoAppendTextLine("|cFFffcc99%s"%localeInfo.PARTY_PASSIVE_BONUS_2)
		else:
			self.AutoAppendTextLine("|cFFffcc99%s"%localeInfo.PARTY_PASSIVE_BONUS_3)
			self.AutoAppendTextLine("|cFFffcc99%s"%localeInfo.PARTY_PASSIVE_BONUS_4)

		self.AlignHorizonalCenter()

	def __AppendSummonDescription(self, skillLevel, color):
		if skillLevel > 1:
			text = localeInfo.SKILL_SUMMON_DESCRIPTION % (skillLevel*10)
			find = text.find("+")

			self.AppendTextLine(text[:find] + colorInfo.Colorize(text[find:], 0xFFffd169), color)
		elif 1 == skillLevel:
			text = localeInfo.SKILL_SUMMON_DESCRIPTION % 15
			find = text.find("+")

			self.AppendTextLine(text[:find] + colorInfo.Colorize(text[find:], 0xFFffd169), color)
		elif 0 == skillLevel:
			text = localeInfo.SKILL_SUMMON_DESCRIPTION % 10
			find = text.find("+")

			self.AppendTextLine(text[:find] + colorInfo.Colorize(text[find:], 0xFFffd169), color)

class ItemDataToolTip(ToolTip):
	def __init__(self, mainInstance):
		ToolTip.__init__(self)

		self.mainInstance = proxy(mainInstance)

		self.SetFollow(False)

	def __del__(self):
		ToolTip.__del__(self)

	def AppendTextLine(self, text, color = ToolTip.SPECIAL_POSITIVE_COLOR2):
		ToolTip.AppendTextLine(self, text, color)

	def AddItemData(self, itemVnum, metinSlot, attrSlot = 0, flags = 0, unbindTime = 0, trans_id = -1, refineElement = 1, **kwargs):
		if not player.IsGameMaster():
			return

		self.ClearToolTip()

		item.SelectItem(itemVnum)

		values = [item.GetValue(i) for i in xrange(6)]

		self.AppendTextLine("Proto Data:", self.TITLE_COLOR)
		self.AppendTextLine("vnum: {}".format(itemVnum))
		self.AppendTextLine("type: {}, subType: {}".format(item.GetItemType(), item.GetItemSubType()))
		self.AppendTextLine("values: {}".format(values))
		self.AppendSpace(5)
		self.AppendTextLine("Item Data:", self.SPECIAL_TITLE_COLOR)
		self.AppendTextLine("sockets: {}".format(metinSlot))

		if kwargs.get("auxiliaryDict"):
			self.AppendTextLine("Auxs: ")
			for _, val in kwargs.get("auxiliaryDict").items():
				self.AppendTextLine("Key: [{}] Value: [{}]".format(_, val))

	def OnUpdate(self):
		(x, y) = self.mainInstance.GetGlobalPosition()
		self.SetPosition(x, y - self.GetHeight())

# GLOBALS
_instanceItemToolTip = None

def GetItemToolTipInstance():
	global _instanceItemToolTip

	if not _instanceItemToolTip:
		SetItemToolTipInstance(ItemToolTip())

	return _instanceItemToolTip

def SetItemToolTipInstance(instance):
	global _instanceItemToolTip

	if _instanceItemToolTip:
		del _instanceItemToolTip

	_instanceItemToolTip = instance


