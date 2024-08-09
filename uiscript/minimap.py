#-*- coding: iso-8859-1 -*-a
import localeInfo
ROOT = "d:/ymir work/ui/minimap/"

Main_ButtonGroupCounter = 0
def Main_GetButtonGroup(inc = False):
	global Main_ButtonGroupCounter

	if inc:
		Main_ButtonGroupCounter += 1
	return Main_ButtonGroupCounter

window = {
	"name" : "MiniMap",

	"x" : SCREEN_WIDTH - 136,
	"y" : 0,

	"width" : 136,
	"height" : 137,

	"children" :
	(
		## OpenWindow
		{
			"name" : "OpenWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 136,
			"height" : 137,

			"children" :
			(
				{
					"name" : "OpenWindowBGI",
					"type" : "image",
					"x" : 0,
					"y" : 0,
					"image" : ROOT + "minimap.sub",
				},
				## MiniMapWindow
				{
					"name" : "MiniMapWindow",
					"type" : "window",

					"x" : 4,
					"y" : 5,

					"width" : 128,
					"height" : 128,
				},
				## ScaleUpButton
				{
					"name" : "ScaleUpButton",
					"type" : "button",

					"x" : 101,
					"y" : 116,

					"default_image" : ROOT + "minimap_scaleup_default.sub",
					"over_image" : ROOT + "minimap_scaleup_over.sub",
					"down_image" : ROOT + "minimap_scaleup_down.sub",
				},
				## ScaleDownButton
				{
					"name" : "ScaleDownButton",
					"type" : "button",

					"x" : 115,
					"y" : 103,

					"default_image" : ROOT + "minimap_scaledown_default.sub",
					"over_image" : ROOT + "minimap_scaledown_over.sub",
					"down_image" : ROOT + "minimap_scaledown_down.sub",
				},
				## MiniMapHideButton
				{
					"name" : "MiniMapHideButton",
					"type" : "button",

					"x" : 111,
					"y" : 6,

					"default_image" : ROOT + "minimap_close_default.sub",
					"over_image" : ROOT + "minimap_close_over.sub",
					"down_image" : ROOT + "minimap_close_down.sub",
				},
				## AtlasShowButton
				{
					"name" : "AtlasShowButton",
					"type" : "button",

					"x" : 12,
					"y" : 12,

					"default_image" : ROOT + "atlas_open_default.sub",
					"over_image" : ROOT + "atlas_open_over.sub",
					"down_image" : ROOT + "atlas_open_down.sub",
				},

				{
					"name" : "CH_%d" % Main_GetButtonGroup(True),
					"type" : "button",

					"x" : -5,
					"y" : 46,

					"tooltip_text" : localeInfo.MINIMAP_CHANNEL_TEXT % Main_GetButtonGroup(),
					"tooltip_x" : -35,
					"tooltip_y" : 0,
					"default_image" : "Assets/ui/minimap/ch{}_0.png".format(Main_GetButtonGroup()),
					"over_image" : "Assets/ui/minimap/ch{}_1.png".format(Main_GetButtonGroup()),
					"down_image" : "Assets/ui/minimap/ch{}_2.png".format(Main_GetButtonGroup()),
					"disable_image" : "Assets/ui/minimap/ch{}_3.png".format(Main_GetButtonGroup()),
				},

				{
					"name" : "CH_%d" % Main_GetButtonGroup(True),
					"type" : "button",

					"x" : -3,
					"y" : 46 + 19,

					"tooltip_text" : localeInfo.MINIMAP_CHANNEL_TEXT % Main_GetButtonGroup(),
					"tooltip_x" : -35,
					"tooltip_y" : 0,
					"default_image" : "Assets/ui/minimap/ch{}_0.png".format(Main_GetButtonGroup()),
					"over_image" : "Assets/ui/minimap/ch{}_1.png".format(Main_GetButtonGroup()),
					"down_image" : "Assets/ui/minimap/ch{}_2.png".format(Main_GetButtonGroup()),
					"disable_image" : "Assets/ui/minimap/ch{}_3.png".format(Main_GetButtonGroup()),
				},

				{
					"name" : "CH_%d" % Main_GetButtonGroup(True),
					"type" : "button",

					"x" : 2,
					"y" : 46 + 19 * 2,

					"tooltip_text" : localeInfo.MINIMAP_CHANNEL_TEXT % Main_GetButtonGroup(),
					"tooltip_x" : -35,
					"tooltip_y" : 0,
					"default_image" : "Assets/ui/minimap/ch{}_0.png".format(Main_GetButtonGroup()),
					"over_image" : "Assets/ui/minimap/ch{}_1.png".format(Main_GetButtonGroup()),
					"down_image" : "Assets/ui/minimap/ch{}_2.png".format(Main_GetButtonGroup()),
					"disable_image" : "Assets/ui/minimap/ch{}_3.png".format(Main_GetButtonGroup()),
				},

				{
					"name" : "CH_%d" % Main_GetButtonGroup(True),
					"type" : "button",

					"x" : 12,
					"y" : 48 + 19 * 3 - 3,

					"tooltip_text" : localeInfo.MINIMAP_CHANNEL_TEXT % Main_GetButtonGroup(),
					"tooltip_x" : -35,
					"tooltip_y" : 0,
					"default_image" : "Assets/ui/minimap/ch{}_0.png".format(Main_GetButtonGroup()),
					"over_image" : "Assets/ui/minimap/ch{}_1.png".format(Main_GetButtonGroup()),
					"down_image" : "Assets/ui/minimap/ch{}_2.png".format(Main_GetButtonGroup()),
					"disable_image" : "Assets/ui/minimap/ch{}_3.png".format(Main_GetButtonGroup()),
				},

				{
					"name" : "CH_%d" % Main_GetButtonGroup(True),
					"type" : "button",

					"x" : 13 + 16,
					"y" : 48 + 21 * 3 + 4,

					"tooltip_text" : localeInfo.MINIMAP_CHANNEL_TEXT % Main_GetButtonGroup(),
					"tooltip_x" : -35,
					"tooltip_y" : 3,
					"default_image" : "Assets/ui/minimap/ch{}_0.png".format(Main_GetButtonGroup()),
					"over_image" : "Assets/ui/minimap/ch{}_1.png".format(Main_GetButtonGroup()),
					"down_image" : "Assets/ui/minimap/ch{}_2.png".format(Main_GetButtonGroup()),
					"disable_image" : "Assets/ui/minimap/ch{}_3.png".format(Main_GetButtonGroup()),
				},

				# {
				# 	"name" : "CH_%d" % Main_GetButtonGroup(True),
				# 	"type" : "button",

				# 	"x" : 13 + 16 + 21,
				# 	"y" : 48 + 21 * 3 + 6,

				# 	"tooltip_text" : localeInfo.MINIMAP_CHANNEL_TEXT % Main_GetButtonGroup(),
				# 	"tooltip_x" : 0,
				# 	"tooltip_y" : -15,
					# "default_image" : "Assets/ui/minimap/ch{}_0.png".format(Main_GetButtonGroup()),
					# "over_image" : "Assets/ui/minimap/ch{}_1.png".format(Main_GetButtonGroup()),
					# "down_image" : "Assets/ui/minimap/ch{}_2.png".format(Main_GetButtonGroup()),
					# "disable_image" : "Assets/ui/minimap/ch{}_3.png".format(Main_GetButtonGroup()),
				# },

				## DungeonInfoButton
				{
					"name" : "BiologButton",
					"type" : "button",

					"x" : 13 + 16 + 21,
					"y" : 48 + 21 * 3 + 6,


					"tooltip_text" : localeInfo.BTN_INVENTORY_BIOLOG,

					"default_image" : "Assets/ui/minimap/btn_bio_normal.png",
					"over_image" : "Assets/ui/minimap/btn_bio_hover.png",
					"down_image" : "Assets/ui/minimap/btn_bio_down.png",
				},

				## DungeonInfoButton
				{
					"name" : "DungeonInfoShowButton",
					"type" : "button",

					"x" : -3,
					"y" : 25,

					"default_image" : "Assets/ui/minimap/btn_timer_normal.png",
					"over_image" : "Assets/ui/minimap/btn_timer_hover.png",
					"down_image" : "Assets/ui/minimap/btn_timer_down.png",
				},

				## ServerInfo
				{
					"name" : "ServerInfo",
					"type" : "text",

					"text_horizontal_align" : "center",
					"color" : 0xFFffffff,

					"outline" : 1,

					"x" : 70,
					"y" : 145,

					"text" : "",
				},
				## PositionInfo
				{
					"name" : "PositionInfo",
					"type" : "text",

					"text_horizontal_align" : "center",
					"color" : 0xFFffffff,

					"outline" : 1,

					"x" : 70,
					"y" : 155,

					"text" : "",
				},
				## Day info
				{
					"name" : "dayInfo",
					"type" : "text",

					"text_horizontal_align" : "center",
					"color" : 0xFFffffff,

					"outline" : 1,

					"x" : 70,
					"y" : 170,

					"text" : "",
				},
				## Time info
				{
					"name" : "timeInfo",
					"type" : "text",

					"text_horizontal_align" : "center",
					"color" : 0xFFffffff,

					"outline" : 1,

					"x" : 70,
					"y" : 183,

					"text" : "",
				},
				## Time info
				{
					"name" : "speedInfo",
					"type" : "text",

					"text_horizontal_align" : "center",
					"color" : 0xFFffffff,

					"outline" : 1,

					"x" : 70,
					"y" : 196,

					"text" : "",
				},
				## ObserverCount
				{
					"name" : "ObserverCount",
					"type" : "text",
					"color" : 0xFFffffff,

					"text_horizontal_align" : "center",

					"outline" : 1,

					"x" : 70,
					"y" : 209,

					"text" : "",
				},
			),
		},
		{
			"name" : "CloseWindow",
			"type" : "window",

			"x" : 0,
			"y" : 0,

			"width" : 132,
			"height" : 48,

			"children" :
			(
				## ShowButton
				{
					"name" : "MiniMapShowButton",
					"type" : "button",

					"x" : 100,
					"y" : 4,

					"default_image" : ROOT + "minimap_open_default.sub",
					"over_image" : ROOT + "minimap_open_default.sub",
					"down_image" : ROOT + "minimap_open_default.sub",
				},
			),
		},
	),
}
