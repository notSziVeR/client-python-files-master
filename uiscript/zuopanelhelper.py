import uiScriptLocale

window = {
	"name" : "OfflineShop_Searcher",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : 200,
	"height" : 100,

	"children" :
	(
		## Board
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 200,
			"height" : 100,

			"title" : uiScriptLocale.ZUO_PANEL_HELPER_TITLE,

			"children" :
			(
				## Label
				{
					"name" : "title",
					"type" : "text",

					"x" : 0,
					"y" : 40,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",

					"text" : uiScriptLocale.ZUO_PANEL_HELPER_TITLE,
				},

				## Income Slotbar
				{
					"name" : "ItemName_SlotBar",
					"type" : "slotbar",

					"x" : 0,
					"y" : 60,

					"width" : 150,
					"height" : 15,

					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "ItemName",
							"type" : "editline",

							"x" : 0,
							"y" : 2,

							"width" : 150,
							"height" : 15,

							"input_limit" : 30,
							"enable_codepage" : 0,
						},
					),
				},
			),
		},
	),
}
