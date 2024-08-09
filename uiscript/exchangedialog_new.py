import uiScriptLocale
import app

BOARD_WIDTH = 480
BOARD_HEIGHT = 375

LOGS_WIDTH = 392
LOGS_HEIGHT = 90

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

ValueCounter = -1
def GetCounter(inc = False):
	global ValueCounter

	if inc:
		ValueCounter += 1
	return ValueCounter

ROOT = "d:/ymir work/ui/game/"
FACE_SLOT_FILE = "d:/ymir work/ui/game/windows/box_face.sub"


window = {
	"name" : "ExchangeDialog",
	"x" : 0,
	"y" : 0,
	"style" : ("movable", "float", "animate",),
	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,
	"children" :
	[
		{
			"name" : "ExchangeLogs",
			"type" : "thinboard",
			"style" : ("attach",),
			"x" : 0,
			"y" : BOARD_HEIGHT - LOGS_HEIGHT - 11,
			"width" : 392,
			"height" : 100,
			"horizontal_align" : "center",
			"children" :
			(
				## ScrollBar
				{
					"name" : "scrollbar",
					"type" : "slimscrollbar",

					"x" : 376,
					"y" : 8,

					"size" : 90,
				},
			),
		},

		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT - LOGS_HEIGHT,

			"title" : uiScriptLocale.EXCHANGE_TITLE,

			"children" :
			[
				{
					"name" : "ThinBoard",
					"type" : "thinboard",

					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST,
					"height" : (BOARD_HEIGHT - LOGS_HEIGHT) - (PAGE_TOP_DIST + PAGE_BOT_DIST),
					"children" :
					[
						{
							"name" : "TargetMain",
							"type" : "thinboard",

							"x" : PAGE_LEFT_X_DIST,
							"y" : PAGE_BOT_DIST,

							"width" : (BOARD_WIDTH - PAGE_X_DIST - 10 * 2) / 2 - 5,
							"height" : (BOARD_HEIGHT - LOGS_HEIGHT) - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,
							"children" :
							[
								{
									"name" : "FaceTarget_Slot",
									"type" : "thinboard_new",

									"x" : PAGE_LEFT_X_DIST,
									"y" : PAGE_BOT_DIST - 5,

									"width" : 60,
									"height" : 70,
									"children" :
									[
										{
											"name" : "FaceTarget_Image",
											"type" : "render_target",

											"x" : 0,
											"y" : 0,

											"horizontal_align" : "center",
											"vertical_align" : "center",
											"width" : 60,
											"height" : 80,
											"image" : "game/exchange_bg_target.png"
										},
									],
								},
								{
									"name" : "TargetText",
									"type" : "text",

									"x" : PAGE_LEFT_X_DIST + 60 + 5,
									"y" : PAGE_BOT_DIST * 2,

									"text" : "|cFF04DD04120Lv|r TargetName",
								},
								{
									"name" : "Input_0",
									"type" : "field",

									"x" : PAGE_LEFT_X_DIST + 60 + 5,
									"y" : PAGE_BOT_DIST * 4,

									"width" : 80,
									"height" : 20,
									"children" :
									[
										{
											"name" : "Target_Money_Value",
											"type" : "text",

											"x" : 80 - 4,
											"y" : 2,

											"text" : "123456789",

											"text_horizontal_align" : "right",
										},
									],
								},

								{
									"name" : "Target_Slot",
									"type" : "grid_table",

									"start_index" : 0,
									"x" : PAGE_LEFT_X_DIST,
									"y" : PAGE_BOT_DIST * 2 + 60,
									"x_count" : 6,
									"y_count" : 4,
									"x_step" : 32,
									"y_step" : 32,
									"x_blank" : 0,
									"y_blank" : 0,
									"image" : "d:/ymir work/ui/public/slot_base.sub",
								},

								{
									"name" : "Target_Accept_Button",
									"type" : "toggle_button",

									"x" : PAGE_LEFT_X_DIST + 28,
									"y" : PAGE_BOT_DIST * 3,

									"horizontal_align" : "right",
									"default_image" : "d:/ymir work/ui/game/exchange/target_arrow_01.tga",
									"over_image" : "d:/ymir work/ui/game/exchange/target_arrow_02.tga",
									"down_image" : "d:/ymir work/ui/game/exchange/target_arrow_03.tga",
								},
							],
						},

						{
							"name" : "OwnerMain",
							"type" : "thinboard",

							"x" : PAGE_LEFT_X_DIST + (BOARD_WIDTH - PAGE_X_DIST - 10 * 2) / 2 + 5,
							"y" : PAGE_BOT_DIST,

							"width" : (BOARD_WIDTH - PAGE_X_DIST - 10 * 2) / 2 - 5,
							"height" : (BOARD_HEIGHT - LOGS_HEIGHT) - (PAGE_TOP_DIST + PAGE_BOT_DIST) - 10 * 2,
							"children" :
							[
								{
									"name" : "FaceOwner_Slot",
									"type" : "thinboard_new",

									"x" : PAGE_LEFT_X_DIST + 60,
									"y" : PAGE_BOT_DIST,

									"width" : 60,
									"height" : 60,
									"horizontal_align" : "right",

									"children" :
									[
										{
											"name" : "FaceOwner_Image",
											"type" : "render_target",

											"x" : 0,
											"y" : 0,

											"horizontal_align" : "center",
											"vertical_align" : "center",
											"width" : 60,
											"height" : 80,
											"image" : "game/exchange_bg_target.png"
										},
									],
								},
								{
									"name" : "OwnerText",
									"type" : "text",

									"x" : PAGE_LEFT_X_DIST + 60 + 5,
									"y" : PAGE_BOT_DIST * 2,

									"text" : "|cFF04DD04120Lv|r OwnerName",
									"horizontal_align" : "right",
									"text_horizontal_align" : "right",
								},

								{
									"name" : "Input_1",
									"type" : "field",

									"x" : PAGE_LEFT_X_DIST + 60 + 80 + 5,
									"y" : PAGE_BOT_DIST * 4,

									"width" : 80,
									"height" : 20,
									"horizontal_align" : "right",
									"children" :
									[
										{
											"name" : "Owner_Money_Value",
											"type" : "text",

											"x" : 80 - 4,
											"y" : 2,

											"text" : "123456789",

											"text_horizontal_align" : "right",
										},
									],
								},

								{
									"name" : "Owner_Accept_Button",
									"type" : "toggle_button",

									"x" : PAGE_LEFT_X_DIST,
									"y" : PAGE_BOT_DIST * 3,

									"default_image" : "d:/ymir work/ui/game/exchange/own_arrow_01.tga",
									"over_image" : "d:/ymir work/ui/game/exchange/own_arrow_02.tga",
									"down_image" : "d:/ymir work/ui/game/exchange/own_arrow_03.tga",
								},

								{
									"name" : "Owner_Slot",
									"type" : "grid_table",

									"start_index" : 0,
									"x" : PAGE_LEFT_X_DIST,
									"y" : PAGE_BOT_DIST * 2 + 60,
									"x_count" : 6,
									"y_count" : 4,
									"x_step" : 32,
									"y_step" : 32,
									"x_blank" : 0,
									"y_blank" : 0,
									"image" : "d:/ymir work/ui/public/slot_base.sub",
								},
							],
						},
					],
				},
			],
		},
	],
}
