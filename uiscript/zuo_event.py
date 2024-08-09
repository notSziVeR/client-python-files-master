import uiScriptLocale

HORIZONTAL_BAR_LENGTH = 200

window = {
    "name" : "ZUO_EVENT",

    "x" : 0,
    "y" : 0,

    "style" : ("movable", "float",),

    "width" : 300,
    "height" : 550,

    "children" :
    (
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"title" : uiScriptLocale.ZUO_PANEL_TITLE, ## UiscriptDialog

			"width" : 300,
			"height" : 550,

			"children" :
			(
				## Basic Options - HorizontalBar
				{
					"name" : "Basic_Options_Horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						{
							"name" : "Basic_Options_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : uiScriptLocale.ZUO_PANEL_OPTIONS_TITLE, ## UiscriptDialog
						},
					),
				},
				## Start Event Button
				{
					"name" : "Start_Event_Button",
					"type" : "button",

					"x" : -44,
					"y" : 40+30,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.ZUO_PANEL_OPTIONS_START, ## UiscriptDialog
				},
				## Close Event Button
				{
					"name" : "Close_Event_Button",
					"type" : "button",

					"x" : 44,
					"y" : 40+30,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.ZUO_PANEL_OPTIONS_STOP, ## UiscriptDialog
				},
				## Boss Count - HorizontalBar
				{
					"name" : "Boss_Count_Dice_Horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40+30+30,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						{
							"name" : "Boss_Count_Dice_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : uiScriptLocale.ZUO_PANEL_BOSS_COUNT_0, ## UiscriptDialog
						},
					),
				},
				## Boss Count - Window
				{
					"name" : "Boss_Count_Window",
					"type" : "window",

					"x" : 0,
					"y" : 40+30+30+30,

					"width" : HORIZONTAL_BAR_LENGTH-10,
					"height" : 40,

					"horizontal_align" : "center",

					"children" :
					(
						## Boss Count - SlotBar
						{
							"name" : "Boss_Count_SlotBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 0,

							"width" : 150,
							"height" : 20,

							"horizontal_align" : "center",

							"children" :
							(
								## Boss Count - Text
								{
									"name" : "Boss_Count_Text",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : uiScriptLocale.ZUO_PANEL_BOSS_COUNT_0,
								},
							),
						},
						## Boss Count Dead - SlotBar
						{
							"name" : "Boss_Count_Dead_SlotBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 20,

							"width" : 150,
							"height" : 20,

							"horizontal_align" : "center",

							"children" :
							(
								## Boss Count Dead - Text
								{
									"name" : "Boss_Count_Dead_Text",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : uiScriptLocale.ZUO_PANEL_BOSS_COUNT_0,
								},
							),
						},
					),
				},
				## Metin Count - HorizontalBar
				{
					"name" : "Metin_Count_Dice_Horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40+30+30+30+50,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						{
							"name" : "Metin_Count_Dice_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : uiScriptLocale.ZUO_PANEL_STONES_COUNT_0, ## UiscriptDialog
						},
					),
				},
				## Metin Count - Window
				{
					"name" : "Metin_Count_Window",
					"type" : "window",

					"x" : 0,
					"y" : 40+30+30+30+50+30,

					"width" : HORIZONTAL_BAR_LENGTH-10,
					"height" : 40,

					"horizontal_align" : "center",

					"children" :
					(
						## Metin Count - SlotBar
						{
							"name" : "Metin_Count_SlotBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 0,

							"width" : 150,
							"height" : 20,

							"horizontal_align" : "center",

							"children" :
							(
								## Metin Count - Text
								{
									"name" : "Metin_Count_Text",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : uiScriptLocale.ZUO_PANEL_STONES_COUNT_0,
								},
							),
						},
						## Metin Count Dead - SlotBar
						{
							"name" : "Metin_Count_Dead_SlotBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 20,

							"width" : 150,
							"height" : 20,

							"horizontal_align" : "center",

							"children" :
							(
								## Metin Count Dead - Text
								{
									"name" : "Metin_Count_Dead_Text",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : uiScriptLocale.ZUO_PANEL_STONES_COUNT_0,
								},
							),
						},
					),
				},
				## Spawner - HorizontalBar
				{
					"name" : "Spawner_Dice_Horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40+30+30+30+50+30+50,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						{
							"name" : "Spawner_Dice_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : uiScriptLocale.ZUO_PANEL_SPAWNER, ## UiscriptDialog
						},
					),
				},
				## Spawner Window
				{
					"name" : "Spawner_Window",
					"type" : "window",

					"x" : 0,
					"y" : 40+30+30+30+50+30+50+30,

					"width" : 150,
					"height" : 105,

					"horizontal_align" : "center",

					"children" :
					(
						## Monster Spawn Text
						{
							"name" : "Monster_Spawn_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : uiScriptLocale.ZUO_PANEL_MONSTER_NAME, ## UiscriptDialog
						},
						## Monster Spawn - Slotbar
						{
							"name" : "Monster_Spawn_SlotBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 20,

							"width" : 150,
							"height" : 15,

							"horizontal_align" : "center",

							"children" :
							(
								## Monster Spawn - EditLine
								{
									"name" : "Monster_Spawn_EditLine",
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
						## Monster Count - Text
						{
							"name" : "Monster_Count_Text",
							"type" : "text",

							"x" : 0,
							"y" : 40,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : uiScriptLocale.ZUO_PANEL_MONSTER_COUNT, ## UiscriptDialog
						},
						## Monster Count - Slotbar
						{
							"name" : "Monster_Count_SlotBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 60,

							"width" : 150,
							"height" : 15,

							"horizontal_align" : "center",

							"children" :
							(
								## Monster Count - EditLine
								{
									"name" : "Monster_Count_EditLine",
									"type" : "editline",

									"x" : 0,
									"y" : 2,

									"width" : 150,
									"height" : 15,

									"input_limit" : 3,
									"enable_codepage" : 0,
									"only_number" : 1,
								},
							),
						},
						## Spawn Monster - Button
						{
							"name" : "Spawn_Monster_Button",
							"type" : "button",

							"x" : 0,
							"y" : 85,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

							"text" : uiScriptLocale.ZUO_PANEL_ACCEPT, ## UiscriptDialog
						},
					),
				},
				## Players Count - HorizontalBar
				{
					"name" : "Players_Count_Horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40+30+30+30+50+30+50+30+115,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						## Players Count - Text
						{
							"name" : "Players_Count_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : uiScriptLocale.ZUO_PANEL_PLAYER_COUNTER, ## UiscriptDialog
						},
					),
				},
				## Online Attenders - Slotbar
				{
					"name" : "Online_Attenders_SlotBar",
					"type" : "slotbar",

					"x" : 0,
					"y" : 40+30+30+30+50+30+50+30+115+30,

					"width" : HORIZONTAL_BAR_LENGTH-10,
					"height" : 20,

					"horizontal_align" : "center",

					"children" :
					(
						## Online Attenders - Text
						{
							"name" : "Online_Attenders_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : uiScriptLocale.ZUO_PANEL_PLAYER_COUNTER_0_1, ## UiscriptDialog
						},
					),
				},
				## Online Max - Slotbar
				{
					"name" : "Online_Max_SlotBar",
					"type" : "slotbar",

					"x" : 0,
					"y" : 40+30+30+30+50+30+50+30+115+30+20,

					"width" : HORIZONTAL_BAR_LENGTH-10,
					"height" : 20,

					"horizontal_align" : "center",

					"children" :
					(
						## Online Max - Text
						{
							"name" : "Online_Max_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : uiScriptLocale.ZUO_PANEL_PLAYER_COUNTER_0_2, ## UiscriptDialog
						},
					),
				},
				## Time Gone - HorizontalBar
				{
					"name" : "Time_Gone_Horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40+30+30+30+50+30+50+30+115+30+20+20+10,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						## Time Gone - Text
						{
							"name" : "Time_Gone_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "Time", ## UiscriptDialog
						},
					),
				},
				## Time Gone - Slotbar
				{
					"name" : "Time_Gone_SlotBar",
					"type" : "slotbar",

					"x" : 0,
					"y" : 40+30+30+30+50+30+50+30+115+30+20+20+10+30,

					"width" : HORIZONTAL_BAR_LENGTH-10,
					"height" : 20,

					"horizontal_align" : "center",

					"children" :
					(
						## Time Gone - Text
						{
							"name" : "Time_Gone_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "0 sec", ## UiscriptDialog
						},
					),
				},
			),
		},
	),
}