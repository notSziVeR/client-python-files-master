import uiScriptLocale

ROOT_PATH = "assets/ui/passive_system/refine/{}"
WINDOW_WIDTH = 220
WINDOW_HEIGHT = 280

CRAFTING_ITEMS_WIDTH = 239
CRAFTING_ITEMS_HEIGHT = 182

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

DISTANCE_BETWEEN = 10

window = {
	"name": "LegendaryStonesRefine",
	"style": ("movable", "float", "animate",),

	"x": 0,
	"y": 0,

	"width": WINDOW_WIDTH,
	"height": WINDOW_HEIGHT,

	"children":
	[
		{
			"name": "BOARD",
			"type": "main_board_with_titlebar",
			"style": ("attach",),

			"x": 0,
			"y": 0,

			"width": WINDOW_WIDTH,
			"height": WINDOW_HEIGHT,

			"title": uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_REFINE_STONES_WINDOW_TITLE,
			"children" :
			[
				## Items Box
				{
					"name" : "BOX_ITEMS",
					"type" : "image",

					"x" : 0,
					"y" : PAGE_TOP_DIST,

					"horizontal_align" : "center",
					"image" : ROOT_PATH.format("background.png"),
					"children" :
					[
						# SlotBase
						{
							"name" : "ITEMS",
							"type" : "slot",

							"x" : (207 - (34)) / 2 + 1,
							"y" : 25,

							"width" : 38,
							"height" : 120,
							# "start_index" : 0,
							# "x_count" : 1,
							# "y_count" : 2,
							# "x_step" : 32,
							# "y_step" : 38,

							"image" : ROOT_PATH.format("slot_additional.png"),

							"slot" : (
								{"index":0, "x":0, "y":0, "width":32, "height":32},
								{"index":1, "x":0, "y":38, "width":32, "height":32},
								{"index":2, "x":0, "y":100, "width":32, "height":32},
								
							),
						},

						{
							"name" : "ADDITIONAL_ITEM",
							"type" : "slot",

							"x" : 150,
							"y" : 25 + 38,

							"width" : 32,
							"height" : 32,

							"image" : ROOT_PATH.format("slot_additional.png"),

							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
						},

						# {
						# 	"name" : "REWARD_ITEM",
						# 	"type" : "slot",

						# 	"x" : (207 - (34)) / 2 + 1,
						# 	"y" : CRAFTING_ITEMS_HEIGHT - (32 * 2 - 5),

						# 	"width" : 32,
						# 	"height" : 32,

						# 	"image" : ROOT_PATH.format("slot_reward.png"),

						# 	"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
						# },
					],
				},

				{
					"name" : "COST",
					"type" : "text",

					"x" : 0,
					"y" : 90,

					"all_align" : 1,

					"text" : "Upgrade cost: 500k",
				},

				{
					"name" : "CRAFT",
					"type" : "button",

					"x" : -40,
					"y" : 35,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",
					"default_image" : ROOT_PATH.format("button_refine_norm.png"),
					"over_image" : ROOT_PATH.format("button_refine_hover.png"),
					"down_image" : ROOT_PATH.format("button_refine_down.png"),

					"text" : uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_REFINE_STONES_WINDOW_ACCEPT,
				},

				{
					"name" : "CANCEL",
					"type" : "button",

					"x" : 40,
					"y" : 35,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",
					"default_image" : ROOT_PATH.format("button_cancel_norm.png"),
					"over_image" : ROOT_PATH.format("button_cancel_hover.png"),
					"down_image" : ROOT_PATH.format("button_cancel_down.png"),

					"text" : uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_REFINE_STONES_WINDOW_CANCEL,
				},
			],
		},
	],

}