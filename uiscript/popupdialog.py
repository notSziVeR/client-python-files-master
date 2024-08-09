import uiScriptLocale

window = {
	"name" : "PopupDialog",
	"style" : ("float", "animate",),

	"x" : SCREEN_WIDTH/2 - 250,
	"y" : SCREEN_HEIGHT/2 - 40,

	"width" : 225,
	"height" : 46,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 225,
			"height" : 46,

			"children" :
			(
				{
					"name" : "message",
					"type" : "multi_text",

					"x" : 0,
					"y" : 15,

					"text" : uiScriptLocale.MESSAGE,

					"width" : 280 - 25 * 2,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "accept",
					"type" : "button",

					"x" : 0,
					"y" : 30,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",
					"text" : uiScriptLocale.OK,

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
			),
		},
	),
}