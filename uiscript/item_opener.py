import uiScriptLocale

window = {
	"name" : "ItemOpener",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float", "animate",),

	"width" : 180,
	"height" : 150,

	"children" :
	(
		## Board
		{
			"name" : "Board",
			"style" : ("attach",),
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 180,
			"height" : 150,

			"title" : uiScriptLocale.ITEM_OPENER_TITLE,

			"children" :
			(
				## SlotWindow
				{
					"name" : "SlotWindow",
					"type" : "grid_table",

					"x" : (180-32)/2,
					"y" : 40,

					"start_index" : 0,
					"x_count" : 1,
					"y_count" : 1,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub"
				},

				{
					"name" : "Input_0",
					"type" : "field",

					"x" : 0,
					"y" : 80,

					"width" : 160,
					"height" : 18,
					"horizontal_align" : "center",
					"children" :
					(
						{
							"name" : "InputValue",
							"type" : "editline",

							"x" : 2,
							"y" : 3,

							"width" : 160,
							"height" : 18,

							"input_limit" : 4,
							"only_number" : 1,

							"text" : "",
						},
					),
				},

				## Checkbox
				{
					"name" : "CheckBox",
					"type" : "checkbox",

					"x" : 0,
					"y" : 50,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"text" : uiScriptLocale.ITEM_OPENER_CONFORMATION_TEXT,
				},

				## Button Accept
				{
					"name" : "ButtonAccept",
					"type" : "button",

					"x" : -35,
					"y" : 120,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				## Button Decline
				{
					"name" : "ButtonDecline",
					"type" : "button",

					"x" : 35,
					"y" : 120,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
					"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
					"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
				},
			),
		},
	),
}