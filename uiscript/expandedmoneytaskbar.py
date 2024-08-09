import uiScriptLocale
import app

ROOT    = "d:/ymir work/ui/game/"

BOARD_ADD_X = 0

if app.ENABLE_GAYA_SYSTEM:
	BOARD_ADD_X += 60

BOARD_X      = SCREEN_WIDTH - (185 + BOARD_ADD_X)
BOARD_WIDTH  = (185 + BOARD_ADD_X)
BOARD_HEIGHT = 40

window = {
	"name": "ExpandedMoneyTaskbar",

	"x": BOARD_X,
	"y": SCREEN_HEIGHT - 65,

	"width" : BOARD_WIDTH,
	"height": BOARD_HEIGHT,

	"style": ("float", "animate",),

	"children":
	[
		{
			"name": "ExpanedMoneyTaskBar_Board",
			"type": "board",

			"x": 0,
			"y": 0,

			"width" : BOARD_WIDTH,
			"height": BOARD_HEIGHT,

			"children":
			[
				{
					"name": "Money_Slot",
					"type": "field",


					"x": 15 + 120,
					"y": 8,


					"width" : 120,
					"height" : 18,

					"horizontal_align" : "right",
					"children":
					(
						{
							"name": "Money_Icon",
							"type": "button",

							"x": -18,
							"y": 2,

							"default_image": GetAssets().format("buttons/INV/button-money-0.png"),
							"over_image"   : GetAssets().format("buttons/INV/button-money-1.png"),
							"down_image"   : GetAssets().format("buttons/INV/button-money-2.png"),
						},

						{
							"name": "Money",
							"type": "text",

							"x": 4,
							"y": -1,

							"horizontal_align"     : "right",
							"text_horizontal_align": "right",
							"vertical_align"       : "center",
							"text_vertical_align"  : "center",

							"text": "123456789",
						},
					),
				},
			],
		},
	],
}

if app.ENABLE_GAYA_SYSTEM:
	window["children"][0]["children"] = window["children"][0]["children"] + [
					{
						"name": "Gem_Slot",
						"type": "field",


						"x": 15 + 18,
						"y": 8,

						"width" : 50,
						"height" : 18,

						"horizontal_align" : "left",
						"children":
						(
							{
								"name": "Gem_Icon",
								"type": "image",

								"x"    : -18,
								"y"    : 3,
								"image": "d:/ymir work/ui/gemshop/gemshop_gemicon.sub",
							},
							{
								"name": "Gem",
								"type": "text",

								"x": 4,
								"y": -1,

								"horizontal_align"     : "right",
								"text_horizontal_align": "right",
								"vertical_align"       : "center",
								"text_vertical_align"  : "center",

								"r": 12.0 / 12.0,
								"g": 135.0 / 135.0,
								"b": 217.0 / 217.0,

								"text": "123456789",
							},
						),
					},
					]
