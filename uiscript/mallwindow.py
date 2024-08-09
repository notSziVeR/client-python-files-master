import uiScriptLocale

BOARD_WIDTH = 200
BOARD_HEIGHT = 353

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

			"title" : uiScriptLocale.MALL_TITLE,

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
					],
				},
			),
		},
	),
}
