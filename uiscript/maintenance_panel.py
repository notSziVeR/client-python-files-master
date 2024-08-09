import uiScriptLocale

window = {
	"name" : "MaintenancePanel",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float", "animate",),

	"width" : 500,
	"height" : 300,

	"children" :
	(
		## Board
		{
			"name" : "Board",
			"style" : ("attach",),
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 500,
			"height" : 300,

			"title" : uiScriptLocale.MAINTENACE_PANEL_TITLE,

			"children" :
			(
				## Timeout - Window
				{
					"name" : "Timeout_Window",
					"type" : "window",

					"x" : 0,
					"y" : 40,

					"width" : 450,
					"height" : 40,

					"horizontal_align" : "center",

					"children" :
					(
						## Timeout - Label
						{
							"name" : "Timeout_Label",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : uiScriptLocale.MAINTENACE_PANEL_TIMEOUT_LABEL,
							"fontsize" : "LARGE",
						},
						## Timeout - Slotbar
						{
							"name" : "Timeout_SlobBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 25,

							"width" : 450,
							"height" : 20,

							"horizontal_align" : "center",

							"children" :
							(
								## Timeout - TextLine
								{
									"name" : "Timeout_TextLine",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "-",
									"fontsize" : "LARGE",
								},
							),
						},
					),
				},
				## Reason - Window
				{
					"name" : "Reason_Window",
					"type" : "window",

					"x" : 0,
					"y" : 110,

					"width" : 450,
					"height" : 40,

					"horizontal_align" : "center",

					"children" :
					(
						## Reason - Label
						{
							"name" : "Reason_Label",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : uiScriptLocale.MAINTENACE_PANEL_REASON_LABEL,
							"fontsize" : "LARGE",
						},
						## Reason - SlotBar
						{
							"name" : "Reason_SlobBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 25,

							"width" : 450,
							"height" : 20,

							"horizontal_align" : "center",

							"children" :
							(
								## Reason - TextLine
								{
									"name" : "Reason_TextLine",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "",
									"fontsize" : "LARGE",
								},
								## Reason - TextLine
								{
									"name" : "Reason_EditLine",
									"type" : "editline",

									"x" : 2,
									"y" : 3,

									"width" : 450,
									"height" : 15,

									"input_limit" : 127,
									"enable_codepage" : 0,
								},
							),
						},
					),
				},
				## Status - Window
				{
					"name" : "Status_Window",
					"type" : "window",

					"x" : 0,
					"y" : 180,

					"width" : 450,
					"height" : 40,

					"horizontal_align" : "center",

					"children" :
					(
						## Status - Label
						{
							"name" : "Status_Label",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : uiScriptLocale.MAINTENACE_PANEL_STATUS_LABEL,
							"fontsize" : "LARGE",
						},
						## Status - SlotBar
						{
							"name" : "Status_SlobBar",
							"type" : "slotbar",

							"x" : 0,
							"y" : 25,

							"width" : 450,
							"height" : 20,

							"horizontal_align" : "center",

							"children" :
							(
								## Status - TextLine
								{
									"name" : "Status_TextLine",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "",
									"fontsize" : "LARGE",
								},
							),
						},
					),
				},
				## Schedule - Button
				{
					"name" : "Schedule_Button",
					"type" : "button",

					"x" : -88-44-10,
					"y" : 255,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.MAINTENACE_PANEL_BUTTON_SCHEDULE,
				},
				## Cancelation - Button
				{
					"name" : "Cancelation_Button",
					"type" : "button",

					"x" : 0,
					"y" : 255,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.MAINTENACE_PANEL_BUTTON_CANCEL,
				},
				## Postpone - Button
				{
					"name" : "Postpone_Button",
					"type" : "button",

					"x" : 88+44+10,
					"y" : 255,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.MAINTENACE_PANEL_BUTTON_POSTPONE,
				},
			),
		},
	),
}