import localeInfo

window = {
	"name" : "PopupDialog",
	"style" : ("float",),

	"x" : SCREEN_WIDTH/2 - 250,
	"y" : SCREEN_HEIGHT/2 - 40,

	"width" : 280,
	"height" : 105,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 280,
			"height" : 105,

			"children" :
			(
				{
					"name" : "testWindow",
					"type" : "window",

					"x" : -190,
					"y" : 38 - 15,

					"width" : 0,
					"height" : 32,

					"horizontal_align" : "center",

					"children":
					(
						{
							"name" : "firstText",
							"type" : "text",

							"x" : 0,
							"y" : -30,

							"text" : "#",

							"text_vertical_align" : "center",
						},
						{
							"name" : "itemImage",
							"type" : "image",

							"x" : 0,
							"y" : 0,
						},
						{
							"name" : "secondText",
							"type" : "text",

							"x" : -50,
							"y" : 15,

							"text" : "#",

							"text_vertical_align" : "center",
						},
					),
				},
				{
					"name" : "accept",
					"type" : "button",

					"x" : 0,
					"y" : 63,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",

                    "default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
                    "over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
                    "down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
			),
		},
	),
}