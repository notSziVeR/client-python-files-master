import uiScriptLocale

WINDOW_WIDTH		= 284
WINDOW_HEIGHT		= 452

MAINBOARD_WIDTH = 196 + 20
MAINBOARD_HEIGHT = 269 + 20 + 24

SUBBOARD_WIDTH = 196
SUBBOARD_HEIGHT = 269
SUBBOARD_X = 10
SUBBOARD_Y = 10

window = {
	"name" : "PrivateShopDecorationWindow",

	"x" : (SCREEN_WIDTH / 2) - (WINDOW_WIDTH / 2) - MAINBOARD_WIDTH + 5,
	"y" : (SCREEN_HEIGHT / 2) - (MAINBOARD_WIDTH / 2) - 43,	

	"width" : MAINBOARD_WIDTH,
	"height" : MAINBOARD_HEIGHT,
	
	"children" :
	(
		## MainBoard
		{
			"name" : "Board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : MAINBOARD_WIDTH,
			"height" : MAINBOARD_HEIGHT,

			"children" :
			(
				{
					"name" : "BackgroundBoard",
					"type" : "thinboard_circle",
					
					"x" : SUBBOARD_X, 
					"y" : SUBBOARD_Y, 
					
					"width" : SUBBOARD_WIDTH, 
					"height" : SUBBOARD_HEIGHT,
					
					"children" : 
					(
						## HeaderImage
						{
							"name" : "HeaderImage",
							"type" : "image",
							
							"x" : 3, 
							"y" : 3,
							
							"image" : "d:/ymir work/ui/game/myshop_deco/model_view_title.sub",
							
							"children" :
							(
								{ "name" : "ModeTitleText", "type" : "text", "x" : 0, "y" : 0, "text" : "", "all_align":"center" },
							),
						},
					),
				},
				
				## ScrollBar
				{
					"name"	: "ScrollBar",
					"type"	: "scrollbar",
					
					"x"		: 189,
					"y"		: 40,
					
					"size"	: 235,
				},
				
				## AppearanceButton	
				{
					"name" : "AppearanceButton",
					"type" : "radio_button",

					"x" : 20,
					"y" : 282,
					
					"horizontal_align" : "left",

					"text" : uiScriptLocale.PREMIUM_PRIVATE_SHOP_DECO_APPEARANCE,
					"text_height" : 6,

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
				
				## TitleButton		
				{
					"name" : "TitleButton",
					"type" : "radio_button",

					"x" : 20 + 85,
					"y" : 282,
					
					"horizontal_align" : "right",

					"text" : uiScriptLocale.PREMIUM_PRIVATE_SHOP_DECO_TITLE,
					"text_height" : 6,

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
			),
		}, ## Board
	),
}
