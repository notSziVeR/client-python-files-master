import uiScriptLocale
import localeInfo

WINDOW_WIDTH = 535
WINDOW_HEIGHT = 350

CONTENT_LEFT_WIDTH = 345
CONTENT_LEFT_HEIGHT = 314

CONTENT_RIGHT_WIDTH = 174
CONTENT_RIGHT_HEIGHT = 314

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

DISTANCE_BETWEEN = 10

ROOT_PATH = "assets/ui/teleport_manager/{}"

window = {
	"name": "TeleportManagerWindow",
	"style": ("movable", "float"),

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

			"title": uiScriptLocale.TELEPORT_MANAGER_TITLE,
			"children" :
			[
				# CONTENT LEFT
				{
					"name" : "SUB_BOARD_LEFT",
					"type" : "main_sub_board",

					"x" : 5,
					"y" : 31,

					"width" : CONTENT_LEFT_WIDTH,
					"height" : CONTENT_LEFT_HEIGHT,

					"full_opacity" : True,
					"children" :
					[
						{
							"name" : "ITEMS_LIST_BOX",
							"type" : "listboxex",

							"x" : 0,
							"y" : 0.5,

							"width" : CONTENT_LEFT_WIDTH - 10,
							"height" : CONTENT_LEFT_HEIGHT - 10,

							"horizontal_align" : "center",
							"vertical_align" : "center",
						},
					]
				},

				# CONTENT LEFT
				{
					"name" : "SUB_BOARD_RIGHT",
					"type" : "main_sub_board",

					"x" : CONTENT_RIGHT_WIDTH + 5,
					"y" : 31,

					"horizontal_align" : "right",
					"width" : CONTENT_RIGHT_WIDTH,
					"height" : CONTENT_RIGHT_HEIGHT,

					"full_opacity" : True,
					"children" :
					[
						{
							"name" : "Header",
							"type" : "image",

							"x" : 0,
							"y" : 2,

							"image" : ROOT_PATH.format("header.png"),
							"horizontal_align" : "center",
							"children" : 
							[
								{
									"name" : "CATEGORY_HEADER",
									"type" : "text",

									"x" : 0,
									"y" : -2,

									"all_align" : "center",
									"text" : localeInfo.TELEPORT_MANAGER_CATEGORY_HEADER,

									"color" : 0xFFb19d58,
								},
							],
						},

						{
							"name" : "CATEGORIES_LIST_BOX",
							"type" : "listboxex",

							"x" : 0,
							"y" : 23 + 2 + 5,

							"width" : CONTENT_RIGHT_WIDTH - 10,
							"height" : CONTENT_RIGHT_HEIGHT - (15 + 23),

							"horizontal_align" : "center",
						},
					]
				},
			],
		},
	],
}