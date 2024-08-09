import uiScriptLocale

BOARD_WIDTH	= 204
BOARD_HEIGHT	= 215

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

BUTTON_COUNT_PER_LINE = 3
BUTTON_WIDTH = 39
BUTTON_GAP = 15

BUTTON_SPACE = BUTTON_WIDTH + BUTTON_GAP

ROOT_PATH = "d:/ymir work/ui/element_change/"

window = {
	"name" : "RefineElementChangeDialog",
	"style" : ("movable", "float", "animate",),

	"x" : SCREEN_WIDTH / 2 - BOARD_WIDTH / 2,
	"y" : SCREEN_HEIGHT / 2 - BOARD_HEIGHT / 2,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"title" : uiScriptLocale.REFINE_ELEMENT_CHANGE_TITLE,

			"children" :
			(
				{
					"name" : "ThinBoard",
					"type" : "thinboard",

					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST,
					"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),
					"children" :
					[
						{
							"name" : "FireButton",
							"type" : "radio_button",

							"x" : -int(float(BUTTON_COUNT_PER_LINE-1)/2 * BUTTON_SPACE),
							"y" : PAGE_BOT_DIST,

							"horizontal_align" : "center",

							"default_image" : ROOT_PATH + "fire_0.png",
							"over_image" :  ROOT_PATH + "fire_1.png",
							"down_image" :  ROOT_PATH + "fire_2.png",
							"disable_image" :  ROOT_PATH + "fire_3.png",
						},

						{
							"name" : "IceButton",
							"type" : "radio_button",

							"x" : -int(float(BUTTON_COUNT_PER_LINE-1)/2 * BUTTON_SPACE) + BUTTON_SPACE,
							"y" : PAGE_BOT_DIST,

							"horizontal_align" : "center",

							"default_image" : ROOT_PATH + "ice_0.png",
							"over_image" :  ROOT_PATH + "ice_1.png",
							"down_image" :  ROOT_PATH + "ice_2.png",
							"disable_image" :  ROOT_PATH + "ice_3.png",
						},

						{
							"name" : "WindButton",
							"type" : "radio_button",

							"x" : -int(float(BUTTON_COUNT_PER_LINE-1)/2 * BUTTON_SPACE) + BUTTON_SPACE * 2,
							"y" : PAGE_BOT_DIST,

							"horizontal_align" : "center",

							"default_image" : ROOT_PATH + "wind_0.png",
							"over_image" :  ROOT_PATH + "wind_1.png",
							"down_image" :  ROOT_PATH + "wind_2.png",
							"disable_image" :  ROOT_PATH + "wind_3.png",
						},

						{
							"name" : "Separator",
							"style" : ("not_pick", ),
							"type" : "image",

							"x" : 0,
							"y" : PAGE_BOT_DIST + BUTTON_SPACE + 20,

							"horizontal_align" : "center",
							"image" : "d:/ymir work/ui/separator.png",
						},

						{
							"name" : "ElectButton",
							"type" : "radio_button",

							"x" : -int(float(BUTTON_COUNT_PER_LINE-1)/2 * BUTTON_SPACE),
							"y" : PAGE_BOT_DIST + BUTTON_SPACE,

							"horizontal_align" : "center",

							"default_image" : ROOT_PATH + "elect_0.png",
							"over_image" :  ROOT_PATH + "elect_1.png",
							"down_image" :  ROOT_PATH + "elect_2.png",
							"disable_image" :  ROOT_PATH + "elect_3.png",
						},

						{
							"name" : "EarthButton",
							"type" : "radio_button",

							"x" : -int(float(BUTTON_COUNT_PER_LINE-1)/2 * BUTTON_SPACE) + BUTTON_SPACE,
							"y" : PAGE_BOT_DIST + BUTTON_SPACE,

							"horizontal_align" : "center",

							"default_image" : ROOT_PATH + "earth_0.png",
							"over_image" :  ROOT_PATH + "earth_1.png",
							"down_image" :  ROOT_PATH + "earth_2.png",
							"disable_image" :  ROOT_PATH + "earth_3.png",
						},

						{
							"name" : "DarkButton",
							"type" : "radio_button",

							"x" : -int(float(BUTTON_COUNT_PER_LINE-1)/2 * BUTTON_SPACE) + BUTTON_SPACE * 2,
							"y" : PAGE_BOT_DIST + BUTTON_SPACE,

							"horizontal_align" : "center",

							"default_image" : ROOT_PATH + "dark_0.png",
							"over_image" :  ROOT_PATH + "dark_1.png",
							"down_image" :  ROOT_PATH + "dark_2.png",
							"disable_image" :  ROOT_PATH + "dark_3.png",
						},

						{
							"name" : "Field",
							"type" : "field",

							"x" : 0,
							"y" : 55,

							"width" : 120,
							"height" : 18,

							"horizontal_align" : "center",
							"vertical_align" : "bottom",
							"children" :
							[
								{
									"name" : "Cost",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"all_align" : "center",
									"text" : "",
								},
							],
						},

						{
							"name" : "AcceptButton",
							"type" : "button",

							"x" : -40,
							"y" : 30,

							"horizontal_align" : "center",
							"vertical_align" : "bottom",

							"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
							"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
							"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
						},

						{
							"name" : "CancelButton",
							"type" : "button",

							"x" : 40,
							"y" : 30,

							"horizontal_align" : "center",
							"vertical_align" : "bottom",

							"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
							"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
							"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
						},
					],
				},
			),
		},
	),
}