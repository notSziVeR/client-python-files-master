import uiScriptLocale

window = {
	"name" : "Acce_CombineWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 215,
	"height" : 290,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 215,
			"height" : 290,

			"title" : uiScriptLocale.ACCE_COMBINE,

			"children" :
			(
				## Slot
				{
					"name" : "Acce_Combine",
					"type" : "image",

					"x" : 9,
					"y" : 35,

					"image" : uiScriptLocale.LOCALE_UISCRIPT_PATH + "acce/acce_combine.tga",

					"children" :
					(
						{
							"name" : "AcceSlot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 200,
							"height" : 150,

							"slot" : (
								{"index":0, "x":78, "y":5, "width":32, "height":32},
								{"index":1, "x":78, "y":57, "width":32, "height":32},
								{"index":2, "x":78, "y":115, "width":32, "height":32},
							),
						},
						## Help Text
						{
							"name" : "Main", "type" : "text", "text" : uiScriptLocale.ACCE_MAIN, "text_horizontal_align":"center", "x" : 85+12, "y" : 7+36,
						},
						{
							"name" : "serve", "type" : "text", "text" : uiScriptLocale.ACCE_SERVE, "text_horizontal_align":"center", "x" : 85+12, "y" : 60+38,
						},
						{
							"name" : "Result", "type" : "text", "text" : uiScriptLocale.ACCE_RESULT, "text_horizontal_align":"center", "x" : 85+12, "y" : 115+40
						},

					),
				},
				{
					"name" : "Cost",
					"type" : "text",
					"text" : "",
					"text_horizontal_align" : "center",
					"x" : 105,
					"y" : 215,
				},
				{
					"name" : "Percent",
					"type" : "text",
					"text" : "",
					"text_horizontal_align" : "center",
					"x" : 105,
					"y" : 235,
				},
				## Button
				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : -35,
					"y" : 35,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				{
					"name" : "CancelButton",
					"type" : "button",

					"x" : 35,
					"y" : 35,

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

