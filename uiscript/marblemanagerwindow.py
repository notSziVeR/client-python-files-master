#-*- coding: iso-8859-1 -*-a

import uiScriptLocale
import grp

BOARD_WIDTH = 380
BOARD_HEIGHT = 305

ROOT_PATH = "assets/ui/marble/"

window = {
	"name" : "MarbleManagerWindow",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	[
		{
			"name" : "Board",
			"type" : "main_board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"title" : uiScriptLocale.MARBLE_MANAGER_TITLE,

			"children" :
			[
				## Rendering
				{
					"name" : "RenderTarget",
					"type" : "render_target",

					"x" : 5,
					"y" : 30,

					"image" : ROOT_PATH + "background_left.png",
					"race" : 30000,
					"rotation": True,
				},

				# Base
				{
					"name" : "Main",
					"type" : "image",

					"x" : 167 + 5,
					"y" : 30,

					"horizontal_align" : "right",
					"image" : ROOT_PATH + "background_right.png",

					"children" :
					[
						{
							"name" : "MullHeader",
							"type" : "window",
							"style" : ("attach",),
							"x" : 0,
							"y" : 0,

							"width" : 163,
							"height" : 25,

							"children" :
							[
								{
									"name" : "prev_btn",
									"type" : "button",

									"x" : -55,
									"y" : 4.5,

									"horizontal_align" : "center",

									"default_image" : ROOT_PATH + "buttons/button_prev_norm.png",
									"over_image" : ROOT_PATH + "buttons/button_prev_hover.png",
									"down_image" : ROOT_PATH +  "buttons/button_prev_down.png",
								},

								{
									"name" : "HeaderText",
									"type" : "text",

									"x" : 0,
									"y" : 1,

									"horizontal_align" : "center",
									"vertical_align" : "center",
									"text_horizontal_align" : "center",
									"text_vertical_align" : "center",

									"text" : "Dziki Pies",
									"color" : 0xFFb19d58,
								},

								{
									"name" : "next_btn",
									"type" : "button",

									"x" : 55,
									"y" : 4.5,

									"horizontal_align" : "center",

									"default_image" : ROOT_PATH + "buttons/button_next_norm.png",
									"over_image" : ROOT_PATH + "buttons/button_next_hover.png",
									"down_image" : ROOT_PATH +  "buttons/button_next_down.png",
								},
							],
						},

						## Header Count
						{
							"name" : "HeaderMarbleCount",
							"type" : "expanded_image",
							"style" : ("ltr",),

							"x" : 0,
							"y" : 31,

							"horizontal_align" : "center",
							"vertical_align" : "top",

							"image" : ROOT_PATH + "header_image.png",
							"children" :
							[
								{
									"name" : "HeaderMarbleCount",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"horizontal_align" : "center",
									"vertical_align" : "center",
									"text_horizontal_align" : "center",
									"text_vertical_align" : "center",

									"text" : uiScriptLocale.MARBLE_MANAGER_WINDOW_MARBLE_COUNT,
								},
							],
						},

						## Buttons of count
						{
							"name" : "Button_MarbleCount_0",
							"type" : "button",

							"x" : -60,
							"y" : 59.5,

							"horizontal_align" : "center",
							"default_image" : ROOT_PATH + "buttons/button_count_0.png",
							"over_image" : ROOT_PATH + "buttons/button_count_1.png",
							"down_image" : ROOT_PATH + "buttons/button_count_2.png",
							"disable_image" : ROOT_PATH + "buttons/button_count_3.png",
							"children" :
							[
								{
									"name" : "Button_MarbleCountText_0",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",

									"text" : "I",
									"color" : 0xFFF1E6C0,
								},
							],
						},

						{
							"name" : "Button_MarbleCount_1",
							"type" : "button",

							"x" : -30,
							"y" : 59.5,

							"horizontal_align" : "center",
							"default_image" : ROOT_PATH + "buttons/button_count_0.png",
							"over_image" : ROOT_PATH + "buttons/button_count_1.png",
							"down_image" : ROOT_PATH + "buttons/button_count_2.png",
							"disable_image" : ROOT_PATH + "buttons/button_count_3.png",
							"children" :
							[
								{
									"name" : "Button_MarbleCountText_1",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",

									"text" : "II",
									"color" : 0xFFF1E6C0,
								},
							],
						},

						{
							"name" : "Button_MarbleCount_2",
							"type" : "button",

							"x" : 0,
							"y" : 59.5,

							"horizontal_align" : "center",
							"default_image" : ROOT_PATH + "buttons/button_count_0.png",
							"over_image" : ROOT_PATH + "buttons/button_count_1.png",
							"down_image" : ROOT_PATH + "buttons/button_count_2.png",
							"disable_image" : ROOT_PATH + "buttons/button_count_3.png",
							"children" :
							[
								{
									"name" : "Button_MarbleCountText_2",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",

									"text" : "III",
									"color" : 0xFFF1E6C0,
								},
							],
						},

						{
							"name" : "Button_MarbleCount_3",
							"type" : "button",

							"x" : 30,
							"y" : 59.5,

							"horizontal_align" : "center",
							"default_image" : ROOT_PATH + "buttons/button_count_0.png",
							"over_image" : ROOT_PATH + "buttons/button_count_1.png",
							"down_image" : ROOT_PATH + "buttons/button_count_2.png",
							"disable_image" : ROOT_PATH + "buttons/button_count_3.png",
							"children" :
							[
								{
									"name" : "Button_MarbleCountText_3",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",

									"text" : "IV",
									"color" : 0xFFF1E6C0,
								},
							],
						},

						{
							"name" : "Button_MarbleCount_4",
							"type" : "button",

							"x" : 60,
							"y" : 59.5,

							"horizontal_align" : "center",
							"default_image" : ROOT_PATH + "buttons/button_count_0.png",
							"over_image" : ROOT_PATH + "buttons/button_count_1.png",
							"down_image" : ROOT_PATH + "buttons/button_count_2.png",
							"disable_image" : ROOT_PATH + "buttons/button_count_3.png",
							"children" :
							[
								{
									"name" : "Button_MarbleCountText_4",
									"type" : "text",

									"x" : -1,
									"y" : -2,

									"all_align" : "center",

									"text" : "V",
									"color" : 0xFFF1E6C0,
								},
							],
						},

						## Header of Required
						{
							"name" : "HeaderMarbleRequiredCount",
							"type" : "expanded_image",
							"style" : ("ltr",),

							"x" : 0,
							"y" : 88,

							"horizontal_align" : "center",
							"vertical_align" : "top",

							"image" : ROOT_PATH + "header_image.png",
							"children" :
							[
								{
									"name" : "HeaderCount",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"horizontal_align" : "center",
									"vertical_align" : "center",
									"text_horizontal_align" : "center",
									"text_vertical_align" : "center",

									"text" : uiScriptLocale.MARBLE_MANAGER_WINDOW_REQUIRED_COUNT,
								},
							],
						},

						## Data of Required
						{
							"name" : "HeaderMarbleRequiredData",
							"type" : "image",

							"x" : 0,
							"y" : 117,
							
							"horizontal_align" : "center",
							"image" : ROOT_PATH + "progress_empty.png",
							"children" :
							[
								{
									"name" : "DATA_REQUIRED",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"horizontal_align" : "center",
									"vertical_align" : "center",
									"text_horizontal_align" : "center",
									"text_vertical_align" : "center",

									"text" : "",
								},
							],
						},

						## Header of Killed
						{
							"name" : "HeaderMarbleKilledCount",
							"type" : "expanded_image",
							"style" : ("ltr",),

							"x" : 0,
							"y" : 138,

							"horizontal_align" : "center",
							"vertical_align" : "top",

							"image" : ROOT_PATH + "header_image.png",
							"children" :
							[
								{
									"name" : "HeaderKilled",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"horizontal_align" : "center",
									"vertical_align" : "center",
									"text_horizontal_align" : "center",
									"text_vertical_align" : "center",

									"text" : uiScriptLocale.MARBLE_MANAGER_WINDOW_KILLED,
								},
							],
						},

						## Data of Killed
						{
							"name" : "HeaderMarbleKilledData",
							"type" : "image",

							"x" : 0,
							"y" : 138 + 29,
							
							"horizontal_align" : "center",
							"image" : ROOT_PATH + "progress_empty.png",
							"children" :
							[
								{
									"name" : "DATA_KILLED_BAR",
									"type" : "expanded_image",

									"x" : 0,
									"y" : 0,

									"image" : ROOT_PATH + "progress_green.png",
								},
								{
									"name" : "DATA_KILLED",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"horizontal_align" : "center",
									"vertical_align" : "center",
									"text_horizontal_align" : "center",
									"text_vertical_align" : "center",

									"text" : "",
								},
							],
						},

						## Header of Time
						{
							"name" : "HeaderMarbleTime",
							"type" : "expanded_image",
							"style" : ("ltr",),

							"x" : 0,
							"y" : 138 + 50,

							"horizontal_align" : "center",
							"vertical_align" : "top",

							"image" : ROOT_PATH + "header_image.png",
							"children" :
							[
								{
									"name" : "HeaderTime",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"horizontal_align" : "center",
									"vertical_align" : "center",
									"text_horizontal_align" : "center",
									"text_vertical_align" : "center",

									"text" : uiScriptLocale.MARBLE_MANAGER_WINDOW_REQUIRED_TIME,
								},
							],
						},

						## Data of Time
						{
							"name" : "HeaderMarbleTimeData",
							"type" : "image",

							"x" : 0,
							"y" : 138 + 50 + 29,
							
							"horizontal_align" : "center",
							"image" : ROOT_PATH + "progress_empty.png",
							"children" :
							[
								{
									"name" : "DATA_TIME_BAR",
									"type" : "expanded_image",

									"x" : 0,
									"y" : 0,

									"image" : ROOT_PATH + "progress_red.png",
								},
								{
									"name" : "DATA_TIME",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"horizontal_align" : "center",
									"vertical_align" : "center",
									"text_horizontal_align" : "center",
									"text_vertical_align" : "center",

									"text" : "",
								},
							],
						},

						{
							"name" : "AcceptButton",
							"type" : "button",

							"x" : 0,
							"y" : 35,

							"text" : uiScriptLocale.MARBLE_MANAGER_BUTTON_ACCEPT,

							"text_height" : 2,

							"horizontal_align" : "center",
							"vertical_align" : "bottom",
							"default_image" : ROOT_PATH + "buttons/button_accept_norm.png",
							"over_image" : ROOT_PATH + "buttons/button_accept_hover.png",
							"down_image" : ROOT_PATH + "buttons/button_accept_down.png",
						},
					],
				},
			],
		},
	],
}
