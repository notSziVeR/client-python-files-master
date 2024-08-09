import uiScriptLocale
import grp

BOARD_WIDTH = 200
BOARD_HEIGHT = 90

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

window = {
	"name" : "PickMoneyDialog",

	"x" : 100,
	"y" : 100,

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
			"title" : uiScriptLocale.PICK_MONEY_TITLE,

			"children" :
			(
				## Money Slot
				{
					"name" : "money_window",

					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : 61,
					"height" : 18,

					"children" :
					(
						{
							"name" : "money_slot",
							"type" : "field",

							"x" : 0,
							"y" : 0,

							"width" : 141,
							"height" : 18,

							"children" :
							(
								{
									"name" : "money_value",
									"type" : "editline",

									"x" : 3,
									"y" : 2,

									"width" : 140,
									"height" : 18,

									"input_limit" : 10,
									# "only_number" : 1, # "k"..

									"text" : "",
								},
								{
									"name" : "max_value",
									"type" : "text",

									"x" : 143,
									"y" : 0,

									"text" : "/ 999999",

									"vertical_align" : "center",
									"text_vertical_align" : "center",
								},
							),
						},
					),
				},

				## Button
				{
					"name" : "accept_button",
					"type" : "button",

					"x" : -6 - 61 / 2,
					"y" : 31,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				{
					"name" : "cancel_button",
					"type" : "button",

					"x" : 6 + 61 / 2,
					"y" : 31,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
					"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
					"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
				},
			),
		},
	),
}