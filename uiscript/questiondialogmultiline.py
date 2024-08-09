import uiScriptLocale

window = {
	"name" : "QuestionDialogMultiLine",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH/2 - 125,
	"y" : SCREEN_HEIGHT/2 - 52,

	"width" : 400,
	"height" : 105,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 400,
			"height" : 105,

			"children" :
			(
				{
					"name" : "message",
					"type" : "multi_text",

					"x" : 0,
					"y" : 38,

					"horizontal_align" : "center",
					"text" : uiScriptLocale.MESSAGE,

					"text_horizontal_align" : "center",

					"width" : 400,
				},
				{
					"name" : "accept",
					"type" : "button",

					"x" : -40,
					"y" : 42,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",
					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				{
					"name" : "cancel",
					"type" : "button",

					"x" : 40,
					"y" : 42,

					"width" : 61,
					"height" : 21,

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