import uiScriptLocale

## CHXELO CHANGES BOARD_WIDTH -> +42 ##
BOARD_WIDTH = 183 + 42

## CHXELO CHANGES BOARD_HEIGHT -> +19 ##
BOARD_HEIGHT = 181 + 19

window = {
	"name" : "AntiMultipleFarmWnd",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	[
		## BOARD
		{
			"name" : "board",
			"type" : "board_with_titlebar_without_button",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"title" : uiScriptLocale.ANTI_MULTIPLE_FARM_WND_TITLE,
			"children" :
			[
				{
					"name" : "anti_farm_bg_layer",
					"type" : "expanded_image",
					"style" : ("ltr",),
					
					"x" : 7,
					"y" : 32,
					
					"image" : "d:/ymir work/ui/anti_multiple_farm/anti_farm_bg_layer.png",
					"children" :
					[
						{
							"name" : "base_text_info",
							"type" : "text",
							
							"x" : 0,
							"y" : 3,
							
							"text_horizontal_align" : "center",
							"horizontal_align" : "center",
							
							"text" : uiScriptLocale.ANTI_MULTIPLE_FARM_BASE_TEXT,
						},
					],
				},
				{
					"name" : "scrollbar",
					"type" : "new_scrollbar",

					## CHXELO CHANGES x -> +42 ##
					"x" : 168 + 42,
					
					## CHXELO CHANGES y -> -8 ##
					"y" : 40 - 8,

					## CHXELO CHANGES size -> +11 ##
					"size" : 130 + 11,
				},
				{
					"name" : "view_window",
					"type" : "window",
					"style" : ("attach",),
					
					## CHXELO CHANGES width -> +42 ##
					"width" : 168 + 42,
					"height" : 21,
					
					"x" : 0,
					
					## CHXELO CHANGES y -> +19 ##
					"y" : 153 + 19,
					
					"children" :
					[
						{
							"name" : "edit_button",
							"type" : "button",

							## CHXELO CHANGES x -> -7 -75 ##
							"x" : 15 - 7 - 75,
							"y" : 0,

							"width" : 61,
							"height" : 21,

							"text_horizontal_align" : "center",
							"horizontal_align" : "center",

							"text" : uiScriptLocale.SHOP_EDIT,

							"default_image" : "d:/ymir work/ui/anti_multiple_farm/edit_norm.tga",
							"over_image" : "d:/ymir work/ui/anti_multiple_farm/edit_hover.tga",
							"down_image" : "d:/ymir work/ui/anti_multiple_farm/edit_down.tga",
						},
						{
							"name" : "close_button",
							"type" : "button",

							## CHXELO CHANGES x -> +22 - 75 ##
							"x" : 60 + 22 - 75,
							"y" : 0,

							"width" : 41,
							"height" : 21,

							"text_horizontal_align" : "center",
							"horizontal_align" : "center",

							"text" : uiScriptLocale.CLOSE,

							"default_image" : "d:/ymir work/ui/new_options/close_norm.tga",
							"over_image" : "d:/ymir work/ui/new_options/close_hover.tga",
							"down_image" : "d:/ymir work/ui/new_options/close_down.tga",
						},

						{
							"name" : "refresh_button",
							"type" : "button",

							## CHXELO CHANGES x -> +31 - 75 ##
							"x" : 125 + 31 - 75,
							"y" : 0,

							"width" : 41,
							"height" : 21,

							"text_horizontal_align" : "center",
							"horizontal_align" : "center",

							"text" : uiScriptLocale.MARKLIST_REFRESH,

							"default_image" : "d:/ymir work/ui/new_options/reload_norm.tga",
							"over_image" : "d:/ymir work/ui/new_options/reload_hover.tga",
							"down_image" : "d:/ymir work/ui/new_options/reload_down.tga",
						},
					],
				},
				{
					"name" : "edit_window",
					"type" : "window",
					"style" : ("attach",),
					
					## CHXELO CHANGES width -> +42 ##
					"width" : 168 + 42,

					"height" : 21,
					
					"x" : 0,
					
					## CHXELO CHANGES y -> +19 ##
					"y" : 153 + 19,
					
					"children" :
					[
						{
							"name" : "save_edit_button",
							"type" : "button",

							## CHXELO CHANGES x -> -7 -75 ##
							"x" : 15 - 7 - 75,
							"y" : 0,

							"width" : 61,
							"height" : 21,

							"text_horizontal_align" : "center",
							"horizontal_align" : "center",

							"text" : uiScriptLocale.CHATTING_SETTING_SAVE,

							"default_image" : "d:/ymir work/ui/new_options/ok_norm.tga",
							"over_image" : "d:/ymir work/ui/new_options/ok_hover.tga",
							"down_image" : "d:/ymir work/ui/new_options/ok_down.tga",
						},
						{
							"name" : "close_edit_button",
							"type" : "button",

							## CHXELO CHANGES x -> +31 - 75 ##
							"x" : 125 + 31 - 75,
							"y" : 0,

							"width" : 41,
							"height" : 21,

							"text_horizontal_align" : "center",
							"horizontal_align" : "center",

							"text" : uiScriptLocale.CLOSE,

							"default_image" : "d:/ymir work/ui/new_options/close_norm.tga",
							"over_image" : "d:/ymir work/ui/new_options/close_hover.tga",
							"down_image" : "d:/ymir work/ui/new_options/close_down.tga",
						},
					],
				},
			],
		},
	],
}
