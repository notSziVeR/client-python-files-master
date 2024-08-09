import uiScriptLocale

BOARD_WIDTH = 310 + 32
BOARD_HEIGHT = 220

PAGE_LEFT_X_DIST = 5
PAGE_RIGHT_X_DIST = 5
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 5

ITEMSLOT_START = 18
ITEMSLOT_WIDTH = 138
ITEMSLOT_HEIGHT = 118

ROOT_PATH = "assets/ui/discard_manager/{}"

window = {
	"name": "DiscardItemWindow",
	"style": ("movable", "float", "animate",),

	"x": 0,
	"y": 0,

	"width": BOARD_WIDTH,
	"height": BOARD_HEIGHT,

	"children":
	[
		{
			"name": "Board",
			"type": "main_board_with_titlebar",
			"style": ("attach",),

			"x": 0,
			"y": 0,

			"width": BOARD_WIDTH,
			"height": BOARD_HEIGHT,

			"title" : uiScriptLocale.DISCARD_ITEM_WINDOW_TITLE,

			"children":
			[
				{
					"name" : "ThinBoard",
					"type" : "main_sub_board",

					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST,
					"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),

					"full_opacity" : True,
					"children" :
					[
						{
							"name": "ItemWindow0",
							"type" : "image",

							"x": PAGE_LEFT_X_DIST * 2,
							"y": PAGE_BOT_DIST * 4,

							"image" : ROOT_PATH.format("item_background.png"),
							"children":
							[
								{
									"name": "ItemWindowTop0",
									"type": "window",

									"x": 0,
									"y": 0,

									"width": ITEMSLOT_WIDTH,
									"height": ITEMSLOT_HEIGHT,

									"children":
									[
										{
											"name": "ItemSlot0",
											"type": "slot",

											"x": 0,
											"y": 0,

											"horizontal_align": "center",
											"vertical_align": "center",

											"width": 32,
											"height": 32,

											"slot": [
												{"index": 0, "x": 0, "y": 0, "width": 32, "height": 96},
											],
										},
									],
								},
							],
						},

						{
							"name": "ItemWindowBottom0",
							"type" : "image",

							"x": PAGE_LEFT_X_DIST * 2,
							"y": 40,

							"image" : ROOT_PATH.format("background_name.png"),

							"vertical_align" : "bottom",
							"children":
							[
								{"name": "ItemNameText0", "type": "text", "x": 0, "y": 5,
								"text": "item_name", "horizontal_align": "center",
								"text_horizontal_align": "center"},
							],
						},

						{
							"name": "CancelBtn",
							"type": "button",

							"x": 132 + PAGE_LEFT_X_DIST * 4,
							"y": 40,

							"horizontal_align" : "right",
							"vertical_align" : "bottom",
							"text": uiScriptLocale.CANCEL,

							"text_height" : 2,

							"default_image": ROOT_PATH.format("button_0.png"),
							"over_image": ROOT_PATH.format("button_1.png"),
							"down_image": ROOT_PATH.format("button_2.png"),
							"disable_image": ROOT_PATH.format("button_2.png"),
						},

						{
							"name": "DropBtn",
							"type": "button",

							"x": 132 + PAGE_LEFT_X_DIST * 4,
							"y": PAGE_BOT_DIST * 4,

							"horizontal_align" : "right",
							"text": uiScriptLocale.DISCARD_ITEM_WINDOW_DROP,

							"text_height" : 2,

							"default_image": ROOT_PATH.format("button_0.png"),
							"over_image": ROOT_PATH.format("button_1.png"),
							"down_image": ROOT_PATH.format("button_2.png"),
							"disable_image": ROOT_PATH.format("button_2.png"),
						},

						{
							"name": "DestroyBtn",
							"type": "button",

							"x": 132 + PAGE_LEFT_X_DIST * 4,
							"y": PAGE_BOT_DIST * 4 + (23 + 5) * 1,

							"horizontal_align" : "right",
							"text": uiScriptLocale.DISCARD_ITEM_WINDOW_DELETE,

							"text_height" : 2,

							"default_image": ROOT_PATH.format("button_0.png"),
							"over_image": ROOT_PATH.format("button_1.png"),
							"down_image": ROOT_PATH.format("button_2.png"),
							"disable_image": ROOT_PATH.format("button_2.png"),
						},
					],
				},
			],
		},
	],
}