import uiScriptLocale

window = {
	"name" : "QuestionDialog",
	"style" : ("movable", "float", "animate",),

	"x" : SCREEN_WIDTH/2 - 125,
	"y" : SCREEN_HEIGHT/2 - 52,

	"width" : 340,
	"height" : 105,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 340,
			"height" : 105,

			"children" :
			(
				{
					"name" : "message",
					"type" : "extended_text",

					"x" : 0,
					"y" : 25,

					"horizontal_align" : "center",
					"text" : uiScriptLocale.MESSAGE,

					# "text_horizontal_align" : "center",
					# "text_vertical_align" : "center",
				},
				{
					"name" : "accept",
					"type" : "button",

					"x" : -40,
					"y" : 63,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				{
					"name" : "cancel",
					"type" : "button",

					"x" : 40,
					"y" : 63,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
					"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
					"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
				},
			),
		},
	),
}