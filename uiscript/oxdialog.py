#-*- coding: iso-8859-1 -*-a
import uiScriptLocale

HORIZONTAL_BAR_LENGTH = 200

window = {
    "name" : "OXWindow",

    "x" : 0,
    "y" : 0,

    "style" : ("movable", "float",),

    "width" : 300,
    "height" : 530,

    "children" :
    (
		{
			"name" : "board",
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"title" : "Panel OX", ## UiscriptDialog

			"width" : 300,
			"height" : 530,

			"children" :
			(
				## Basic Options HorizontalBar
				{
					"name" : "Basic_options_horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						{
							"name" : "Basic_options_text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "Opcje podstawowe", ## UiscriptDialog
						},
					),
				},
				## Start Event Button
				{
					"name" : "Start_event_button",
					"type" : "button",

					"x" : -44,
					"y" : 40+30,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : "Rozpocznij", ## UiscriptDialog
				},
				## Close Event Button
				{
					"name" : "Close_event_button",
					"type" : "button",

					"x" : 44,
					"y" : 40+30,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : "Zamknij dostêp", ## UiscriptDialog
				},
				## GiveUp Event Button
				{
					"name" : "GiveUp_event_button",
					"type" : "button",

					"x" : 0,
					"y" : 40+30+21,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : "Wy³¹cz Event", ## UiscriptDialog
				},
				## Question Pool HorizontalBar
				{
					"name" : "Question_pool_horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40+30+21+30,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						{
							"name" : "Question_pool_text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "Pule pytañ", ## UiscriptDialog
						},
					),
				},
				## Pool Slotbar
				{
					"name" : "Pool_SlotBar",
					"type" : "slotbar",

					"x" : 0,
					"y" : 40+30+21+30+30,

					"width" : 150,
					"height" : 15,

					"horizontal_align" : "center",

					"children" :
					(
						## Pool TextLine
						{
							"name" : "PoolText",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "Iloœæ pytañ w puli: 0",
						},
					),
				},
				## Fill Pool Button
				{
					"name" : "Fill_Pool_Button",
					"type" : "button",

					"x" : -44,
					"y" : 40+30+21+30+30+30,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : "Uzupe³nij pulê", ## UiscriptDialog
				},
				## Reset Pool Button
				{
					"name" : "Reset_Pool_Button",
					"type" : "button",

					"x" : 44,
					"y" : 40+30+21+30+30+30,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : "Resetuj pule", ## UiscriptDialog
				},
				## Question Dice HorizontalBar
				{
					"name" : "Question_dice_horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40+30+21+30+30+21+30+10,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						{
							"name" : "Question_dice_text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "Losuj pytanie", ## UiscriptDialog
						},
					),
				},
				## Normal Question Button
				{
					"name" : "Normal_question_button",
					"type" : "button",

					"x" : -44,
					"y" : 40+30+21+30+30+30+21+30+10,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : "Normalne pytanie", ## UiscriptDialog
				},
				## Trap Question Button
				{
					"name" : "Trap_question_button",
					"type" : "button",

					"x" : 44,
					"y" : 40+30+21+30+30+30+21+30+10,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : "Pytanie pu³apka", ## UiscriptDialog
				},
				## Prize HorizontalBar
				{
					"name" : "Prize_horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40+30+21+30+30+30+30+21+30+10,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						{
							"name" : "Prize_text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "Nagrody", ## UiscriptDialog
						},
					),
				},
				## Prize Window
				{
					"name" : "Prize_window",
					"type" : "window",

					"x" : 0,
					"y" : 40+30+21+30+30+30+30+30+21+30+10,

					"width" : 150,
					"height" : 130,

					"horizontal_align" : "center",
					"children" :
					(
						## Prize Text
						{
							"name" : "Prize_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "Nazwa przedmiotu", ## UiscriptDialog
						},
						## Prize Slotbar
						{
							"name" : "Prize_SlotBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 15,

							"width" : 150,
							"height" : 15,

							"horizontal_align" : "center",

							"children" :
							(
								{
									"name" : "PrizeName",
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
						## Count Text
						{
							"name" : "Count_Text",
							"type" : "text",

							"x" : 0,
							"y" : 35,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "Iloœæ przedmiotów", ## UiscriptDialog
						},
						## Count Slotbar
						{
							"name" : "Count_SlotBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 50,

							"width" : 150,
							"height" : 15,

							"horizontal_align" : "center",

							"children" :
							(
								{
									"name" : "PrizeCount",
									"type" : "editline",

									"x" : 0,
									"y" : 2,

									"width" : 150,
									"height" : 15,

									"input_limit" : 30,
									"enable_codepage" : 0,
									"only_number" : 1,
								},
							),
						},
						## Time Text
						{
							"name" : "Time_Text",
							"type" : "text",

							"x" : 0,
							"y" : 70,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "Czas przedmiotów", ## UiscriptDialog
						},
						## Time Slotbar
						{
							"name" : "Time_SlotBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 85,

							"width" : 150,
							"height" : 15,

							"horizontal_align" : "center",

							"children" :
							(
								{
									"name" : "TimeValue",
									"type" : "editline",

									"x" : 0,
									"y" : 2,

									"width" : 150,
									"height" : 15,

									"input_limit" : 30,
									"enable_codepage" : 0,
									"only_number" : 1,
								},
							),
						},
						## Reward Event Button
						{
							"name" : "Reward_event_button",
							"type" : "button",

							"x" : 0,
							"y" : 75+35,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

							"text" : "Podaruj", ## UiscriptDialog
						},
					),
				},
				## Players Count HorizontalBar
				{
					"name" : "Players_count_horizontal",
					"type" : "horizontalbar",

					"x" : 0,
					"y" : 40+30+21+30+30+30+30+70+20+20+30+30+21+30+10,

					"horizontal_align" : "center",

					"width" : HORIZONTAL_BAR_LENGTH,
					"children" :
					(
						{
							"name" : "Players_count_text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "Licznik graczy", ## UiscriptDialog
						},
					),
				},
				## Online Attenders Slotbar
				{
					"name" : "Online_attenders_SlotBar",
					"type" : "slotbar",

					"x" : 0,
					"y" : 40+30+21+30+30+30+30+70+20+30+20+30+30+21+30+10,

					"width" : 120,
					"height" : 20,

					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "Online_attenders_text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "Iloœæ uczestników: 2137", ## UiscriptDialog
						},
					),
				},
				## Online Observs Slotbar
				{
					"name" : "Online_observs_SlotBar",
					"type" : "slotbar",

					"x" : 0,
					"y" : 40+30+21+30+30+30+30+70+30+20+20+20+30+30+21+30+10,

					"width" : 120,
					"height" : 20,

					"horizontal_align" : "center",

					"children" :
					(
						{
							"name" : "Online_observs_text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"text" : "Iloœæ obser.: 2137", ## UiscriptDialog
						},
					),
				},
			),
		},
	),
}