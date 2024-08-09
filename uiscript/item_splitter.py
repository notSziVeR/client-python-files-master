import uiScriptLocale
import grp

WINDOW_WIDTH = 210
WINDOW_HEIGHT = 200

PAGE_LEFT_X_DIST = 5
PAGE_RIGHT_X_DIST = 5
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 31
PAGE_BOT_DIST = 5

ROOT_PATH = "assets/ui/splitter_manager/{}"
window = {
	"name" : "SplitItemDialog",

	"x" : 100,
	"y" : 100,

	"style" : ("movable", "float", "animate",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "main_board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"title" : uiScriptLocale.PICK_MONEY_TITLE,

			"children" :
			(
				{
					"name" : "Sub_Board",
					"type" : "main_sub_board",

					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : WINDOW_WIDTH - PAGE_X_DIST,
					"height" : WINDOW_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),

					"full_opacity" : True,
					"children" :
					[
						# Slot and Inner/Outer
						{
							"name" : "Slot_0",
							"type" : "slot",

							"x" : WINDOW_WIDTH / 2 - (55 / 2),
							"y" : 8,

							"width" : 38,
							"height" : 38,

							"image" : ROOT_PATH.format("slot.png"),
							"slot" : (
								{"index" : 0, "x" : 0, "y" : 0, "width" : 38, "height" : 38},
							),

							"children" :
							[
								{
									"name" : "ValueInner",
									"type" : "text",

									"x" : 45,
									"y" : -5,

									"text" : "x",

									"vertical_align" : "center",
								},

								{
									"name" : "ValueOuter",
									"type" : "text",

									"x" : 60,
									"y" : -5,

									"text" : "500",

									"vertical_align" : "center",

									"color" : 0xFFb19d58,
								},
							],
						},

						{
							"name" : "Line",
							"type" : "image",

							"x" : 0,
							"y" : 60,
							
							"horizontal_align" : "center",

							"image" : ROOT_PATH.format("separator.png"),
						},

						{
							"name" : "Input_0",
							"type" : "image",

							"x" : 0,
							"y" : 75,

							"horizontal_align" : "center",
							"image" : ROOT_PATH.format("input.png"),

							"children" :
							(
								{
									"name" : "HeaderText",
									"type" : "text",

									"x" : 0,
									"y" : -17,
									
									"all_align" : "center",
									"fontname" : "Arial:12",
									"text" : uiScriptLocale.SPLITTER_MANAGER_QUANTITY_COUNT,
								},

								{
									"name" : "Value_0",
									"type" : "editline",

									"x" : 2,
									"y" : 3,

									"width" : 88,
									"height" : 18,

									"input_limit" : 3,
									"only_number" : 1,

									"text" : "",
								},
							),
						},

						{
							"name" : "Input_1",
							"type" : "image",

							"x" : 0,
							"y" : 110,

							"horizontal_align" : "center",
							"image" : ROOT_PATH.format("input.png"),

							"children" :
							(
								{
									"name" : "HeaderText",
									"type" : "text",

									"x" : 0,
									"y" : -17,
									
									"all_align" : "center",
									"fontname" : "Arial:12",
									"text" : uiScriptLocale.SPLITTER_MANAGER_QUANTITY_PACKAGE_COUNT,
								},

								{
									"name" : "Value_1",
									"type" : "editline",

									"x" : 2,
									"y" : 3,

									"width" : 88,
									"height" : 18,

									"input_limit" : 3,
									"only_number" : 1,

									"text" : "",
								},
							),
						},

						## Button
						{
							"name" : "accept_button",
							"type" : "button",

							"x" : -40,
							"y" : 30,

							"vertical_align" : "bottom",
							"horizontal_align" : "center",

							"text" : uiScriptLocale.OK,

							"text_height" : 2,

							"default_image" : ROOT_PATH.format("button_0.png"),
							"over_image" : ROOT_PATH.format("button_1.png"),
							"down_image" : ROOT_PATH.format("button_2.png"),
						},
						{
							"name" : "cancel_button",
							"type" : "button",

							"x" : 40,
							"y" : 30,

							"vertical_align" : "bottom",
							"horizontal_align" : "center",

							"text" : uiScriptLocale.CANCEL,

							"text_height" : 2,

							"default_image" : ROOT_PATH.format("button_0.png"),
							"over_image" : ROOT_PATH.format("button_1.png"),
							"down_image" : ROOT_PATH.format("button_2.png"),
						},
					],
				},
			),
		},
	),
}
