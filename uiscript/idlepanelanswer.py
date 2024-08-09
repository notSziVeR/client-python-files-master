import uiScriptLocale

window = {
    "name" : "IdleAnswerPanel",

    "x" : 100,
    "y" : 100,

    "style" : ("movable", "float",),

    "width" : 250,
    "height" : 80,

    "children" :
    (
		## Board
		{
			"name" : "Board",
			"type" : "board_with_titlebar",

			"style" : ("attach", ),

			"x" : 0,
			"y" : 0,

			"width" : 250,
			"height" : 80,

			"title" : uiScriptLocale.GM_IDLE_ANSWER_TITLE,

			"children" :
			(
				## Accept Button
				{
					"name" : "AcceptButton",
					"type" : "button",

					"x" : 0,
					"y" : 15,

					"horizontal_align" : "center",
					"vertical_align" : "center",

					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
			),
		},
	),
}