import uiScriptLocale

ROOT_PATH = "assets/ui/passive_system/crafting/{}"

WINDOW_WIDTH = 250
WINDOW_HEIGHT = 295

CRAFTING_ITEMS_WIDTH = 180
CRAFTING_ITEMS_HEIGHT = 150

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

DISTANCE_BETWEEN = 10

window = {
	"name": "LegendaryCraftingStonesWindow",
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

			"title": uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_STONES_WINDOW_TITLE,
			"children" :
			[
				{
					"name" : "BOX_ITEMS",
					"type" : "image",

					"x" : 0,
					"y" : PAGE_TOP_DIST,

					"horizontal_align" : "center",
					"image" : ROOT_PATH.format("stones/background.png"),
					"children" : 
					[
						{
							"name" : "ADDITIONAL_ITEMS",
							"type" : "slot",

							"x" : (239 - 38) / 2.5 + 1,
							"y" : 15,

							"width" : 80,
							"height" :32,

							"image" : ROOT_PATH.format("stones/slot_additional.png"),

							"horizontal_align" : "center",

							"slot" : (
								{"index":0, "x":0, "y":0, "width":32, "height":32},
								{"index":1, "x":32 + 10, "y":0, "width":32, "height":32},
							),
						},

						## SlotBase
						{
							"name" : "ITEMS",
							"type" : "grid_table",

							"x" : 32,
							"y" : 65,

							"start_index" : 0,
							"x_count" : 5,
							"y_count" : 2,
							"x_step" : 35,
							"y_step" : 31,

							"image" : ROOT_PATH.format("slot_item.png"),
						},

						{
							"name" : "REWARD_ITEM",
							"type" : "slot",

							"x" : (239 - 38) / 2 + 2,
							"y" : 152,

							"width" : 32,
							"height" : 32,

							"image" : ROOT_PATH.format("slot_reward.png"),

							"horizontal_align" : "center",

							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
						},
					],
				},

				## Cost Box
				{
					"name" : "BOX_COST",
					"type" : "image",

					"x" : 0,
					"y" : 235,

					"image" : ROOT_PATH.format("stones/input.png"),

					"horizontal_align" : "center",
					"children" :
					[
						{
							"name" : "REWARD_PERCENT",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",
							"text" : "Szansa na wytworzenie: 35%",
						},
					],
				},

				## Exit Button
				{
					"name" : "CRAFT",
					"type" : "button",

					"x" : 0,
					"y" : 30,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"default_image" : ROOT_PATH.format("button_create_norm.png"),
					"over_image" : ROOT_PATH.format("button_create_hover.png"),
					"down_image" : ROOT_PATH.format("button_create_down.png"),
					"disable_image" : ROOT_PATH.format("button_create_down.png"),

					"text" : uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_STONES_WINDOW_ACCEPT,
				},
			],
		},
	],

}