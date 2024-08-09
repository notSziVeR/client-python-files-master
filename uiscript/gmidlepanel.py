import uiScriptLocale

window = {
    "name" : "GMIdlePanel",

    "x" : 100,
    "y" : 100,

    "style" : ("movable", "float",),

    "width" : 400,
    "height" : 600,

    "children" :
    (
		## Board
		{
			"name" : "Board",
			"type" : "board_with_titlebar",

			"style" : ("attach", ),

			"x" : 0,
			"y" : 0,

			"width" : 400,
			"height" : 600,

			"title" : uiScriptLocale.GM_IDLE_PANEL_TITLE,

			"children" :
			(
				## Message Sent - Label
				{
					"name" : "MessageSent_Label",
					"type" : "text",

					"x" : 0,
					"y" : 40,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",

					"text" : uiScriptLocale.GM_IDLE_PANEL_MESSAGE_SENT_TEXT,
				},
				## Message Sent - SlotBar
				{
					"name" : "MessageSent_SlotBar",
					"type" : "slotbar",

					"x" : 0,
					"y" : 60,

					"width" : 300,
					"height" : 20,

					"horizontal_align" : "center",
					"children" :
					(
						## Message Sent - Text
						{
							"name" : "MessageSent_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",
							"text" : "-",
						},
					),
				},
				## Player List - Label
				{
					"name" : "PlayerList_Label",
					"type" : "text",

					"x" : 0,
					"y" : 100,

					"horizontal_align" : "center",
					"text_horizontal_align" : "center",

					"text" : uiScriptLocale.GM_IDLE_PANEL_PANEL_LIST_LABEL,
				},
				## Player List - Window
				{
					"name" : "PlayerList_Window",
					"type" : "thinboard",

					"x" : 0,
					"y" : 120,

					"horizontal_align" : "center",

					"width" : 300,
					"height" : 300,

					"children" :
					(
						## Player List - ListBox
						{
							"name" : "PlayerList_ListBox",
							"type" : "listboxex",

							"x" : 10,
							"y" : 10,

							"width" : 270,
							"height" : 290,
						},
						## Player List - ScrollBar
						{
							"name" : "PlayerList_ScrollBar",
							"type" : "scrollbar",

							"x" : 285,
							"y" : 10,

							"size" : 285,
						},
					),
				},
				## Colour Info - Window
				{
					"name" : "ColourInfo_Window",
					"type" : "thinboard",

					"x" : 0,
					"y" : 430,

					"horizontal_align" : "center",

					"width" : 330,
					"height" : 90,

					"children" :
					(
						## Colour Info White - Text
						{
							"name" : "ColourInfoWhite_Text",
							"type" : "text",

							"x" : 0,
							"y" : 7,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"color" : 0xffffffff,
							"text" : uiScriptLocale.GM_IDLE_PANEL_PANEL_WHITE_COLOUR_LABEL,
						},
						## Colour Info Red - Text
						{
							"name" : "ColourInfoRed_Text",
							"type" : "text",

							"x" : 0,
							"y" : 27,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"color" : 0xffFF0000,
							"text" : uiScriptLocale.GM_IDLE_PANEL_PANEL_RED_COLOUR_LABEL,
						},
						## Colour Info Green - Text
						{
							"name" : "ColourInfoGreen_Text",
							"type" : "text",

							"x" : 0,
							"y" : 47,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"color" : 0xff00FF00,
							"text" : uiScriptLocale.GM_IDLE_PANEL_PANEL_GREEN_COLOUR_LABEL,
						},
						## Colour Info Blue - Text
						{
							"name" : "ColourInfoBlue_Text",
							"type" : "text",

							"x" : 0,
							"y" : 67,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"color" : 0xff00FFFF,
							"text" : uiScriptLocale.GM_IDLE_PANEL_PANEL_BLUE_COLOUR_LABEL,
						},
					),
				},
				## Player List - Clear Button
				{
					"name" : "PlayerList_ClearButton",
					"type" : "button",

					"x" : 0,
					"y" : 530,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.GM_IDLE_PANEL_PANEL_BUTTON_REFRESH,
				},
				## Player List - Send Button
				{
					"name" : "PlayerList_SendButton",
					"type" : "button",

					"x" : 0,
					"y" : 560,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.GM_IDLE_PANEL_PANEL_BUTTON_SEND,
				},
			),
		},
	),
}