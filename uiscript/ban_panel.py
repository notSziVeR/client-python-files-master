import uiScriptLocale

window = {
	"name" : "BanPanel",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : 300,
	"height" : 290,

	"children" :
	(
		## Board
		{
			"name" : "Board",
			"style" : ("attach",),
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 300,
			"height" : 290,

			"title" : "Panel do banowania",

			"children" :
			(
				## Options Window
				{
					"name" : "OptionsWindow",
					"type" : "window",

					"x" : 0,
					"y" : 40,

					"width" : 180,
					"height" : 86,

					"horizontal_align" : "center",

					"children" :
					(
						## Options Label
						{
							"name" : "OptionsText",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "Opcje Panelu",
						},
						## Option 1
						{
							"name" : "ButtonOption1",
							"type" : "radio_button",

							"x" : -44,
							"y" : 20,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

							"text" : "Ban permanentny",
						},
						## Option 2
						{
							"name" : "ButtonOption2",
							"type" : "radio_button",

							"x" : 44,
							"y" : 20,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

							"text" : "Ban po IP",
						},
						## Option 3
						{
							"name" : "ButtonOption3",
							"type" : "radio_button",

							"x" : -44,
							"y" : 40,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

							"text" : "Ban Czasowy",
						},
						## Option 4
						{
							"name" : "ButtonOption4",
							"type" : "radio_button",

							"x" : 44,
							"y" : 40,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

							"text" : "Unban",
						},
						## Option 5
						{
							"name" : "ButtonOption5",
							"type" : "radio_button",

							"x" : 0,
							"y" : 60,

							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

							"text" : "Hardware Ban",
						},
					),
				},
				## Nickname Label
				{
					"name" : "NickNameText",
					"type" : "text",

					"x" : 0,
					"y" : 135,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",

					"text" : "Nick gracza",
				},
				## NickName Slotbar
				{
					"name" : "NickNameSlotBar",
					"type" : "slotbar",
							
					"x" : 0,
					"y" : 150,
					
					"width" : 200,
					"height" : 15,
					
					"horizontal_align" : "center",
							
					"children" :
					(
						## NickName Editline
						{
							"name" : "NickNameEditLine", 
							"type" : "editline", 
									
							"x" : 0, 
							"y" : 2, 
							
							"width" : 200,
							"height" : 15,

							"input_limit" : 24,
							"enable_codepage" : 0,
						},
					),
				},
				## BanReason Label
				{
					"name" : "BanReasonText",
					"type" : "text",

					"x" : 0,
					"y" : 175,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",

					"text" : "Powód bana",
				},
				## BanReason Slotbar
				{
					"name" : "BanReasonSlotBar",
					"type" : "slotbar",
							
					"x" : 0,
					"y" : 190,
					
					"width" : 200,
					"height" : 15,
					
					"horizontal_align" : "center",
							
					"children" :
					(
						## BanReason Editline
						{
							"name" : "BanReasonEditLine", 
							"type" : "editline", 
									
							"x" : 0, 
							"y" : 2, 
							
							"width" : 200,
							"height" : 15,

							"input_limit" : 40,
							"enable_codepage" : 0,
						},
					),
				},
				## BanTime Label
				{
					"name" : "BanTimeText",
					"type" : "text",

					"x" : 0,
					"y" : 215,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",

					"text" : "Czas trwania bana (Format: HH:MM:SS)",
				},
				## BanTime Slotbar
				{
					"name" : "BanTimeSlotBar",
					"type" : "slotbar",
							
					"x" : 0,
					"y" : 230,
					
					"width" : 200,
					"height" : 15,
					
					"horizontal_align" : "center",
							
					"children" :
					(
						## BanTime Editline
						{
							"name" : "BanTimeEditLine", 
							"type" : "editline", 
									
							"x" : 0, 
							"y" : 2, 
							
							"width" : 200,
							"height" : 15,

							"input_limit" : 40,
							"enable_codepage" : 0,
						},
					),
				},
				## Button Accept
				{
					"name" : "ButtonAccept",
					"type" : "button",

					"x" : 0,
					"y" : 255,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : "ZatwierdŸ",
				},
			),
		},
	),
}
