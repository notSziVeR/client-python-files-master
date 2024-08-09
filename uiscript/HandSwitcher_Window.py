import uiScriptLocale

WINDOW_SIZE = (232, 295)
ROOT_PATH = "assets/ui/hand-switcher/{}"

def AppendLabel(iKey):
	sImage = "0" if (iKey % 2) else "1"
	return {
		"name" : "HandSwitcher-ApplySpace_{}".format(iKey),
		"type" : "expanded_image",

		"x" : 0, "y" : 27 + 20 * iKey,
		"image" : ROOT_PATH.format("bar_{}.png".format(sImage)),
		"horizontal_align" : "center",
		"children" :
		(
			{
				"name" : "HandSwitcher-ApplyText_{}".format(iKey),
				"type" : "text",

				"x" : 0, "y" : -2,
				"text" : "Silny przeciwko potworom: 10%",
				"all_align" : "center",
				"color" : 0xFFfee3ae,
			},
		),
	}

window = {
	"name"  : "HandSwitcher-Window",
	"style" : ["movable", "float",],

	"x" : 0, "y" : 0,
	"width" : WINDOW_SIZE[0], "height" : WINDOW_SIZE[1],
	"children" :
	[
		{
			"name" : "HandSwitcher-Board",
			"type" : "main_board_with_titlebar",

			"x" : 0, "y" : 0,
			"width" : WINDOW_SIZE[0], "height" : WINDOW_SIZE[1],
			"title" : uiScriptLocale.HAND_SWITCHER_WINDOW_TITLE,
			"children" :
			[
				# HandSwitcher - Top Space
				{
					"name" : "HandSwitcher-TopSpace",
					"type" : "expanded_image",

					"x" : 0, "y" : 25,
					"horizontal_align" : "center",
					"image" : ROOT_PATH.format("background_top.png"),
					"children" :
					[
						# HandSwitcher - Item Slot
						{
							"name" : "HandSwitcher-ItemSpace",
							"type" : "slot",

							"x" : 235 / 2 - (32 / 2), "y" : 30,
							"width" : 32, "height" : 32,

							"image" : ROOT_PATH.format("slot_item.png"),

							"slot" : (
								{"index": 0, "x": 0, "y": 0, "width": 32, "height": 32},
								{"index": 1, "x": 0, "y": 32, "width": 32, "height": 32},
								{"index": 2, "x": 0, "y": 32 * 2, "width": 32, "height": 32},
							),
						},
					],
				},

				# HandSwitcher - Applys Space
				{
					"name" : "HandSwitcher-ApplySpace",
					"type" : "main_sub_board",

					"x" : 0, "y" : (35 + 27)  + (20 * 5),
					"width" : 218, "height" : 27 + (20 * 5),
					"horizontal_align" : "center",
					"vertical_align" : "bottom",
					"full_opacity" : True,
					"children" :
					[
						# HandSwitcher - Current Count Space
						{
							"name" : "HandSwitcher-CurrentCount",
							"type" : "expanded_image",

							"x" : 0, "y" : 0,
							"horizontal_align" : "center",
							"image" : ROOT_PATH.format("sub_header.png"),
							"children" :
							[
								{
									"name" : "HandSwitcher-CurrentCountText",
									"type" : "text",

									"x" : 0, "y" : -1,
									"all_align" : "center",
									"text" : "Current switchers: 920x",
								},
							],
						},
						AppendLabel(0),
						AppendLabel(1),
						AppendLabel(2),
						AppendLabel(3),
						AppendLabel(4),
					]
				},

				# HandSwitcher - Reroll Button
				{
					"name" : "Reroll",
					"type" : "button",

					"x" : 0, "y" : 32,
					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"default_image" : ROOT_PATH.format("button_0.png"),
					"over_image" : ROOT_PATH.format("button_1.png"),
					"down_image" : ROOT_PATH.format("button_2.png"),

					"text" : uiScriptLocale.HAND_SWITCHER_WINDOW_ACCEPT,
					"text_height" : 2,
				},
			],
		}
	],
}