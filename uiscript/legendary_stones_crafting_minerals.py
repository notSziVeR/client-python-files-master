import uiScriptLocale

ROOT_PATH = "assets/ui/passive_system/crafting/{}"
WINDOW_WIDTH = 262
WINDOW_HEIGHT = 400

CRAFTING_ITEMS_WIDTH = 239
CRAFTING_ITEMS_HEIGHT = 182

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

DISTANCE_BETWEEN = 10

window = {
	"name": "LegendaryCraftingMineralsWindow",
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

			"title": uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_MINERALS_WINDOW_TITLE,
			"children" :
			[
				## Items Box
				{
					"name" : "BOX_ITEMS",
					"type" : "image",

					"x" : 0,
					"y" : PAGE_TOP_DIST,

					"horizontal_align" : "center",
					"image" : ROOT_PATH.format("minerals_shards/background.png"),
					"children" :
					[
						## SlotBase
						{
							"name" : "ITEMS",
							"type" : "grid_table",

							"x" : 22.5,
							"y" : DISTANCE_BETWEEN - 1,

							"start_index" : 0,
							"x_count" : 6,
							"y_count" : 2,
							"x_step" : 32,
							"y_step" : 32,

							"image" : ROOT_PATH.format("slot_item.png"),
						},

						{
							"name" : "REWARD_ITEM",
							"type" : "slot",

							"x" : (239 - (32)) / 2 - 1,
							"y" : CRAFTING_ITEMS_HEIGHT - (32 * 2 - 5),

							"width" : 32,
							"height" : 32,

							"image" : ROOT_PATH.format("slot_reward.png"),

							"slot" : ({"index":0, "x":0, "y":0, "width":32, "height":32},),
						},
					],
				},

				## Cost Box
				{
					"name" : "BOX_COST",
					"type" : "image",

					"x" : 0,
					"y" : 210 + 5,

					"image" : ROOT_PATH.format("minerals_shards/bg_cost.png"),

					"horizontal_align" : "center",
					"children" :
					[
						{
							"name" : "COST",
							"type" : "text",

							"x" : 0,
							"y" : -1,

							"all_align" : 1,

							"text" : "",
						},
					],
				},

				## Exit Button
				{
					"name" : "CRAFT",
					"type" : "button",

					"x" : 0,
					"y" : 245 + 5,

					"horizontal_align" : "center",
					"default_image" : ROOT_PATH.format("button_create_norm.png"),
					"over_image" : ROOT_PATH.format("button_create_hover.png"),
					"down_image" : ROOT_PATH.format("button_create_down.png"),

					"text" : uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_MINERALS_WINDOW_ACCEPT,
				},

				{
					"name" : "INFO_BACKGROUND",
					"type" : "image",

					"x" : 0,
					"y" : 273 + 5,

					"horizontal_align" : "center",
					"image" : ROOT_PATH.format("minerals_shards/info_background.png"),
					"children" :
					[
						{
							"name" : "INFO",
							"type" : "text",

							"x" : 0,
							"y" : -1,

							"all_align" : 1,

							"text" : uiScriptLocale.LEGENDARY_STONES_SYSTEM_C_MINERALS_WINDOW_INFORMATION,
						},
					],
				},

				## Info Box
				{
					"name" : "BOX_INFO",
					"type" : "main_sub_board",

					"x" : PAGE_LEFT_X_DIST,
					"y" : DISTANCE_BETWEEN * 8 + DISTANCE_BETWEEN,

					"width" : WINDOW_WIDTH - PAGE_X_DIST,
					"height" : DISTANCE_BETWEEN * 8,

					"vertical_align" : "bottom",
					"full_opacity" : True,
					"children" :
					[

					],
				},


			],
		},
	],

}