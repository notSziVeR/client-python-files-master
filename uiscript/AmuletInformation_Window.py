import uiScriptLocale
WINDOW_SIZE = (440, 380)

ROOT_PATH = "assets/ui/amulet_system/information/{}"

def AppendApply(iKey, i):
	return {
		"name" : "AmuletInformation-ApplyWindow_{}".format(iKey),
		"type" : "bar",

		"x" : 0, "y" : 29 + (24 * i),
		"horizontal_align" : "center",
		"width" : 420, "height" : 24,
		"children" :
		[
			## AmuletInformationApply - LeftSpace
			{
				"name" : "AmuletInformation-ApplySpace_{}".format(iKey),
				"type" : "expanded_image",

				"x" : 0, "y" : 0,
				"vertical_align" : "center",
				"image" : ROOT_PATH.format("apply_input_0.png"),
				"children" : 
				[
					{
						"name" : "AmuletInformation-ApplyText_{}".format(iKey),
						"type" : "text",

						"x" : 0, "y" : -2,
						"text" : "",
						"all_align" : "center",
						"color" : 0xFFfee3ae,
					},
				],
			},
		
			## AmuletInformationApply - Right Value
			{
				"name" : "AmuletInformation-ApplyUpgradeSpace_{}".format(iKey),
				"type" : "expanded_image",

				"x" : 275, "y" : 0,
				"vertical_align" : "center",
				"image" : ROOT_PATH.format("apply_input_1.png"),
				"children" : 
				[
					{
						"name" : "AmuletInformation-ApplyUpgradeText_{}".format(iKey),
						"type" : "extended_text",

						"x" : 0, "y" : 0,
						"text" : "",
						"color" : 0xFFfee3ae,
					},
				],
			},

			## AmuletInformationApply - Button Lock
			{
				"name" : "AmuletInformation-ApplyActionUnlock_{}".format(iKey),
				"type" : "button",

				"x" : 38, "y" : 0,
				"horizontal_align" : "right",
				"vertical_align" : "center",

				"default_image" : ROOT_PATH.format("button_unlock_0.png"),
				"over_image" : ROOT_PATH.format("button_unlock_1.png"),
				"down_image" : ROOT_PATH.format("button_unlock_2.png"),
				"disable_image" : ROOT_PATH.format("button_unlock_3.png"),
			},

			## AmuletInformationApply - Button Upgrade
			{
				"name" : "AmuletInformation-ApplyActionUpgrade_{}".format(iKey),
				"type" : "button",

				"x" : 38, "y" : 0,
				"horizontal_align" : "right",
				"vertical_align" : "center",

				"default_image" : ROOT_PATH.format("button_up_0.png"),
				"over_image" : ROOT_PATH.format("button_up_1.png"),
				"down_image" : ROOT_PATH.format("button_up_2.png"),
			},
		],
	}

window = {
	"name" : "AmuletInformation-Window",
	"style" : ["movable", "float", ],

	"x" : 0, "y" : 0,
	"width" : WINDOW_SIZE[0], "height" : WINDOW_SIZE[1],
	"children" :
	[
		{
			"name" : "AmuletInformation-Board",
			"type" : "main_board_with_titlebar",

			"x" : 0, "y" : 0,
			"width" : WINDOW_SIZE[0], "height" : WINDOW_SIZE[1],
			"title" : uiScriptLocale.AMULET_SYSTEM_INFORMATION_TITLE,
			"children" :
			[
				## AmuletInformation - Top Space
				{
					"name" : "AmuletInformation-TopSpace",
					"type" : "expanded_image",

					"x" : 0, "y" : 31,
					"horizontal_align" : "center",
					"image" : ROOT_PATH.format("top_background.png"),
					"children" :
					[
						## AmuletInformation - MainSlot
						{
							"name" : "AmuletInformation-ItemSlot",
							"type" : "slot",

							"x" : 420 / 2 - 32 / 2, "y" : 71.5 / 2 - 32 / 2,
							"width" : 32, "height" : 32,

							"image" : ROOT_PATH.format("slot.png"),
							"slot" : (
								{"index" : 0, "x" : 5, "y" : 2, "width" : 32, "height" : 32},
							),
						},

					],
				},

				## AmuletInformation - Base Applys Space
				{
					"name" : "AmuletInformation-BaseApplysSpace",
					"type" : "expanded_image",

					"x" : 0, "y" : 31 + 76,
					"horizontal_align" : "center",
					"image" : ROOT_PATH.format("base_applys_background.png"),
					"children" :
					[
						## AmuletInformation - Base Header
						{
							"name" : " AmuletInformation-BaseHeader",
							"type" : "expanded_image",

							"x" : 0, "y" : 3,
							"horizontal_align" : "center",
							"image" : ROOT_PATH.format("header.png"),
							"children" :
							[
								## AmuletInformation - Base Header Text
								{
									"name" : "AmuletInformation-BaseHeaderText",
									"type" : "text",

									"x" : 0, "y" : -2,
									"all_align" : True,
									"text" : uiScriptLocale.AMULET_SYSTEM_INFORMATION_HEADER_BASE,
								},
							],
						},

						AppendApply(0, 0),
						AppendApply(1, 1),
					],
				},

				## AmuletInformation - Other Applys Space
				{
					"name" : "AmuletInformation-OtherApplysSpace",
					"type" : "expanded_image",

					"x" : 0, "y" : 31 + 76 + 88,
					"horizontal_align" : "center",
					"image" : ROOT_PATH.format("other_applys_background.png"),
					"children" :
					[
						## AmuletInformation - Other Header
						{
							"name" : " AmuletInformation-OtherHeader",
							"type" : "expanded_image",

							"x" : 0, "y" : 3,
							"horizontal_align" : "center",
							"image" : ROOT_PATH.format("header.png"),
							"children" :
							[
								## AmuletInformation - Other Header Text
								{
									"name" : "AmuletInformation-OtherHeaderText",
									"type" : "text",

									"x" : 0, "y" : -2,
									"all_align" : True,
									"text" : uiScriptLocale.AMULET_SYSTEM_INFORMATION_HEADER_EXTRA,
								},
							],
						},
					
						AppendApply(2, 0),
						AppendApply(3, 1),
						AppendApply(4, 2),
						AppendApply(5, 3),
					],
				},
			
				## AmuletInformation - Reroll Button
				{
					"name" : "Reroll",
					"type" : "button",

					"x" : 0, "y" : 42,
					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"default_image" : ROOT_PATH.format("button_roll_0.png"),
					"over_image" : ROOT_PATH.format("button_roll_1.png"),
					"down_image" : ROOT_PATH.format("button_roll_2.png"),
				},
			],
		}
	],
}