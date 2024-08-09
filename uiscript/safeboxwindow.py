import uiScriptLocale

BOARD_WIDTH = 200
BOARD_HEIGHT = 400

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

window = {
	"name" : "SafeboxWindow",

	"x" : 100,
	"y" : 20,

	"style" : ("movable", "float", "animate",),

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

			"title" : uiScriptLocale.SAFE_TITLE,
			"children" :
			(
				{
					"name" : "ThinBoard",
					"type" : "thinboard",
					"style" : ("attach",),


					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST,
					"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),
					"children" :
					[
						## Button
						{
							"name" : "ChangePasswordButton",
							"type" : "button",

							"x" : 0,
							"y" : PAGE_BOT_DIST + 21,

							"text" : uiScriptLocale.SAFE_CHANGE_PASSWORD,
							"horizontal_align" : "center",
							"vertical_align" : "bottom",

							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
						},
					],
				},
			),
		},
	),
}
