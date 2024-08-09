import uiScriptLocale
import grp

BOARD_WIDTH = 534
BOARD_HEIGHT = 310 #305

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 31
PAGE_BOT_DIST = 10

ROOT_PATH = "assets/ui/save_location_manager/{}"

window = {
	"name" : "PositionsWindow",
	"style" : ("movable", "float", "animate",),

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	[
		{
			"name" : "PositionsBoard",
			"type" : "main_board_with_titlebar",
			"style" : ("attach", "ltr"),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"title" : uiScriptLocale.POSITION_MANAGER_WINDOW_TITLE,
			"children" :
			[
				{
					"name" : "MainBox",
					"type" : "image",

					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"image" : ROOT_PATH.format("background.png"),
					"children" :
					[
						{
							"name" : "LocationInfo_Space",

							"x" : 0,
							"y" : 0,

							"width" : 254,
							"height" : 23,
							"children" :
							[
								{
									"name" : "LocationInfo_Text",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",
									"text" : uiScriptLocale.POSITION_MANAGER_WINDOW_SAVED_LOCATIONS,
									"color" : 0xFFb19d58,
								},
							],
						},

						{
							"name" : "FunctionInfo_Space",

							"x" : 256,
							"y" : 0,

							"width" : 254,
							"height" : 23,
							"children" :
							[
								{
									"name" : "FunctionInfo_Text",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",
									"text" : uiScriptLocale.POSITION_MANAGER_WINDOW_FUNCTIONS,
									"color" : 0xFFb19d58,
								},
							],
						},

						{
							"name" : "ListBox_Space",

							"x" : 0,
							"y" : 10,

							"horizontal_align" : "center",
							"vertical_align" : "center",

							"width" : 494,
							"height" : 234,
						},
					],
				},
			],
		},
	],
}