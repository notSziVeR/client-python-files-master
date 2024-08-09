import uiScriptLocale

ROOT_PATH = "assets/ui/preview_window/"
KEY_PATH = "assets/ui/keyboard/"


BOARD_WIDTH = 373
BOARD_HEIGHT = 533

RENDER_WIDTH = 359
RENDER_HEIGHT = 434

window = {
	"name" : "TransmuteWindow",

	"x" : (SCREEN_WIDTH - BOARD_WIDTH) / 2,
	"y" : (SCREEN_HEIGHT - BOARD_HEIGHT) / 2,

	"style" : ("movable", "float"),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "main_board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"title" : uiScriptLocale.PREVIEW_ITEM_WINDOW_TITLE,

			"children" :
			(
				{
					"name" : "renderer",
					"type" : "render_target",

					"x" : 0,
					"y" : 31,

					"horizontal_align" : "center",
					"image" : ROOT_PATH + "background.tga",
					"width" : RENDER_WIDTH,
					"height" : RENDER_HEIGHT,
				},

				{
					"name" : "rotate",
					"type" : "image",

					"x" : 20,
					"y" : 420,

					"image" : KEY_PATH + "keyboard_mouse_left.png",
				},

				{
					"name" : "rotate_text",
					"type" : "text",

					"x" : 40,
					"y" : 420,

					"text" : uiScriptLocale.PREVIEW_ITEM_WINDOW_ROTATE,
				},

				{
					"name" : "zoom",
					"type" : "image",

					"x" : 20,
					"y" : 440,

					"image" : KEY_PATH + "keyboard_mouse_scroll.png",
				},

				{
					"name" : "zoom_text",
					"type" : "text",

					"x" : 40,
					"y" : 440,

					"text" : uiScriptLocale.PREVIEW_ITEM_WINDOW_ZOOM,
				},

				{
					"name" : "bottom_bg",
					"type" : "main_sub_board",

					"x" : 0,
					"y" : 70,

					"horizontal_align" : "center",
					"width" : BOARD_WIDTH - 10,
					"height" : 65,

					"vertical_align" : "bottom",

					"children" :
					(
						{
							"name" : "sex_male",
							"type" : "radio_button",

							"x" : -140,
							"y" : 0,

							"horizontal_align" : "center",
							"vertical_align" : "center",

							"default_image" : ROOT_PATH + "buttons/sex/male_norm.tga",
							"over_image" : ROOT_PATH + "buttons/sex/male_hover.tga",
							"down_image" : ROOT_PATH + "buttons/sex/male_down.tga",
							"disable_image" : ROOT_PATH + "buttons/sex/male_down.tga",
						},
						{
							"name" : "job_warrior",
							"type" : "radio_button",

							"x" : -75,
							"y" : 0,

							"vertical_align" : "center",
							"horizontal_align" : "center",

							"default_image" : ROOT_PATH + "buttons/races/warrior_0_normal.tga",
							"over_image" : ROOT_PATH + "buttons/races/warrior_0_hover.tga",
							"down_image" : ROOT_PATH + "buttons/races/warrior_0_down.tga",
							"disable_image" : ROOT_PATH + "buttons/races/warrior_0_disabled.tga",
						},
						{
							"name" : "job_sura",
							"type" : "radio_button",

							"x" : -23,
							"y" : 0,

							"vertical_align" : "center",
							"horizontal_align" : "center",

							"default_image" : ROOT_PATH + "buttons/races/sura_0_normal.tga",
							"over_image" : ROOT_PATH + "buttons/races/sura_0_hover.tga",
							"down_image" : ROOT_PATH + "buttons/races/sura_0_down.tga",
							"disable_image" : ROOT_PATH + "buttons/races/sura_0_disabled.tga",
						},
						{
							"name" : "job_assassin",
							"type" : "radio_button",

							"x" : -23 + 52,
							"y" : 0,

							"vertical_align" : "center",
							"horizontal_align" : "center",

							"default_image" : ROOT_PATH + "buttons/races/assassin_0_normal.tga",
							"over_image" : ROOT_PATH + "buttons/races/assassin_0_hover.tga",
							"down_image" : ROOT_PATH + "buttons/races/assassin_0_down.tga",
							"disable_image" : ROOT_PATH + "buttons/races/assassin_0_disabled.tga",
						},
						{
							"name" : "job_shaman",
							"type" : "radio_button",

							"x" : -23 + 52 * 2,
							"y" : 0,

							"vertical_align" : "center",
							"horizontal_align" : "center",

							"default_image" : ROOT_PATH + "buttons/races/shaman_0_normal.tga",
							"over_image" : ROOT_PATH + "buttons/races/shaman_0_hover.tga",
							"down_image" : ROOT_PATH + "buttons/races/shaman_0_down.tga",
							"disable_image" : ROOT_PATH + "buttons/races/shaman_0_disabled.tga",
						},
						{
							"name" : "sex_female",
							"type" : "radio_button",

							"x" : 140,
							"y" : 0,

							"horizontal_align" : "center",
							"vertical_align" : "center",

							"default_image" : ROOT_PATH + "buttons/sex/female_norm.tga",
							"over_image" : ROOT_PATH + "buttons/sex/female_hover.tga",
							"down_image" : ROOT_PATH + "buttons/sex/female_down.tga",
							"disable_image" : ROOT_PATH + "buttons/sex/female_down.tga",
						},
					),
				},
			),
		},
	),
}
