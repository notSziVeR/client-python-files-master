import uiScriptLocale

BOARD_SIZE = (250, 190)
TIME_FIELD_SIZE = (20, 30)
BUTTON_PARAMETER_SIZE = (15, 19)
WINDOW_TIME_SIZE = (TIME_FIELD_SIZE[0]*2 + 10, TIME_FIELD_SIZE[1] + BUTTON_PARAMETER_SIZE[1]*2 + 3 + 20)
WINDOW_TIME_PADDING = 20

window = {
	"name" : "TimeWizardDialog",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float",),

	"width" : BOARD_SIZE[0],
	"height" : BOARD_SIZE[1],

	"children" :
	(
		## Board
		{
			"name" : "Board",
			"style" : ("attach",),
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : BOARD_SIZE[0],
			"height" : BOARD_SIZE[1],

			"title" : "Time wizard",

			"children" :
			(
				## Window - Hours
				{
					"name" : "Hours_Window",
					"type" : "window",

					"x" : 10 + WINDOW_TIME_PADDING,
					"y" : 50,

					"width" : WINDOW_TIME_SIZE[0],
					"height" : WINDOW_TIME_SIZE[1],

					"children" :
					(
						## Hours - Label
						{
							"name" : "Hours_Label",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "Hours",
						},
						## Hours - Field 1
						{
							"name" : "Hours_Field_1",
							"type" : "bar",

							"x" : 0,
							"y" : 20 + BUTTON_PARAMETER_SIZE[1],

							"width" : TIME_FIELD_SIZE[0],
							"height" : TIME_FIELD_SIZE[1],

							"color" : 0xff000000,

							"children" :
							(
								## Hours - Text 1
								{
									"name" : "Hours_Text_1",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "0",
								},
							),
						},
						## Hours - Button Up 1
						{
							"name" : "Hours_ButtonUp_1",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2,
							"y" : 20,

							"default_image" : "d:/ymir work/ui/public/scrollbar_up_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_up_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_up_button_03.sub",
						},
						## Hours - Button Down 1
						{
							"name" : "Hours_ButtonDown_1",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2,
							"y" : WINDOW_TIME_SIZE[1]-BUTTON_PARAMETER_SIZE[1],

							"default_image" : "d:/ymir work/ui/public/scrollbar_down_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_down_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_down_button_03.sub",
						},
						## Hours - Field 2
						{
							"name" : "Hours_Field_2",
							"type" : "bar",

							"x" : 0 + TIME_FIELD_SIZE[0] + 10,
							"y" : 20 + BUTTON_PARAMETER_SIZE[1],

							"width" : TIME_FIELD_SIZE[0],
							"height" : TIME_FIELD_SIZE[1],

							"color" : 0xff000000,

							"children" :
							(
								## Hours - Text 2
								{
									"name" : "Hours_Text_2",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "0",
								},
							),
						},
						## Hours - Button Up 2
						{
							"name" : "Hours_ButtonUp_2",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0] + 10) + ((TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2),
							"y" : 20,

							"default_image" : "d:/ymir work/ui/public/scrollbar_up_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_up_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_up_button_03.sub",
						},
						## Hours - Button Down 2
						{
							"name" : "Hours_ButtonDown_2",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0] + 10) + ((TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2),
							"y" : WINDOW_TIME_SIZE[1]-BUTTON_PARAMETER_SIZE[1],

							"default_image" : "d:/ymir work/ui/public/scrollbar_down_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_down_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_down_button_03.sub",
						},
					),
				},
				## Window - Minutes
				{
					"name" : "Minutes_Window",
					"type" : "window",

					"x" : 10 + WINDOW_TIME_SIZE[0] + WINDOW_TIME_PADDING*2,
					"y" : 50,

					"width" : WINDOW_TIME_SIZE[0],
					"height" : WINDOW_TIME_SIZE[1],

					"children" :
					(
						## Minutes - Label
						{
							"name" : "Minutes_Label",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "Minutes",
						},
						## Minutes - Field 1
						{
							"name" : "Minutes_Field_1",
							"type" : "bar",

							"x" : 0,
							"y" : 20 + BUTTON_PARAMETER_SIZE[1],

							"width" : TIME_FIELD_SIZE[0],
							"height" : TIME_FIELD_SIZE[1],

							"color" : 0xff000000,

							"children" :
							(
								## Minutes - Text 1
								{
									"name" : "Minutes_Text_1",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "0",
								},
							),
						},
						## Minutes - Button Up 1
						{
							"name" : "Minutes_ButtonUp_1",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2,
							"y" : 20,

							"default_image" : "d:/ymir work/ui/public/scrollbar_up_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_up_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_up_button_03.sub",
						},
						## Minutes - Button Down 1
						{
							"name" : "Minutes_ButtonDown_1",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2,
							"y" : WINDOW_TIME_SIZE[1]-BUTTON_PARAMETER_SIZE[1],

							"default_image" : "d:/ymir work/ui/public/scrollbar_down_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_down_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_down_button_03.sub",
						},
						## Minutes - Field 2
						{
							"name" : "Minutes_Field_2",
							"type" : "bar",

							"x" : 0 + TIME_FIELD_SIZE[0] + 10,
							"y" : 20 + BUTTON_PARAMETER_SIZE[1],

							"width" : TIME_FIELD_SIZE[0],
							"height" : TIME_FIELD_SIZE[1],

							"color" : 0xff000000,

							"children" :
							(
								## Minutes - Text 2
								{
									"name" : "Minutes_Text_2",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "0",
								},
							),
						},
						## Minutes - Button Up 2
						{
							"name" : "Minutes_ButtonUp_2",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0] + 10) + ((TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2),
							"y" : 20,

							"default_image" : "d:/ymir work/ui/public/scrollbar_up_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_up_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_up_button_03.sub",
						},
						## Minutes - Button Down 2
						{
							"name" : "Minutes_ButtonDown_2",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0] + 10) + ((TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2),
							"y" : WINDOW_TIME_SIZE[1]-BUTTON_PARAMETER_SIZE[1],

							"default_image" : "d:/ymir work/ui/public/scrollbar_down_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_down_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_down_button_03.sub",
						},
					),
				},
				## Window - Seconds
				{
					"name" : "Seconds_Window",
					"type" : "window",

					"x" : 10 + (WINDOW_TIME_SIZE[0] + WINDOW_TIME_PADDING)*2 + WINDOW_TIME_PADDING,
					"y" : 50,

					"width" : WINDOW_TIME_SIZE[0],
					"height" : WINDOW_TIME_SIZE[1],

					"children" :
					(
						## Seconds - Label
						{
							"name" : "Seconds_Label",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "Seconds",
						},
						## Seconds - Field 1
						{
							"name" : "Seconds_Field_1",
							"type" : "bar",

							"x" : 0,
							"y" : 20 + BUTTON_PARAMETER_SIZE[1],

							"width" : TIME_FIELD_SIZE[0],
							"height" : TIME_FIELD_SIZE[1],

							"color" : 0xff000000,

							"children" :
							(
								## Seconds - Text 1
								{
									"name" : "Seconds_Text_1",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "0",
								},
							),
						},
						## Seconds - Button Up 1
						{
							"name" : "Seconds_ButtonUp_1",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2,
							"y" : 20,

							"default_image" : "d:/ymir work/ui/public/scrollbar_up_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_up_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_up_button_03.sub",
						},
						## Seconds - Button Down 1
						{
							"name" : "Seconds_ButtonDown_1",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2,
							"y" : WINDOW_TIME_SIZE[1]-BUTTON_PARAMETER_SIZE[1],

							"default_image" : "d:/ymir work/ui/public/scrollbar_down_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_down_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_down_button_03.sub",
						},
						## Seconds - Field 2
						{
							"name" : "Seconds_Field_2",
							"type" : "bar",

							"x" : 0 + TIME_FIELD_SIZE[0] + 10,
							"y" : 20 + BUTTON_PARAMETER_SIZE[1],

							"width" : TIME_FIELD_SIZE[0],
							"height" : TIME_FIELD_SIZE[1],

							"color" : 0xff000000,

							"children" :
							(
								## Seconds - Text 2
								{
									"name" : "Seconds_Text_2",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "0",
								},
							),
						},
						## Seconds - Button Up 2
						{
							"name" : "Seconds_ButtonUp_2",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0] + 10) + ((TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2),
							"y" : 20,

							"default_image" : "d:/ymir work/ui/public/scrollbar_up_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_up_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_up_button_03.sub",
						},
						## Seconds - Button Down 2
						{
							"name" : "Seconds_ButtonDown_2",
							"type" : "button",

							"x" : (TIME_FIELD_SIZE[0] + 10) + ((TIME_FIELD_SIZE[0]-BUTTON_PARAMETER_SIZE[0])/2),
							"y" : WINDOW_TIME_SIZE[1]-BUTTON_PARAMETER_SIZE[1],

							"default_image" : "d:/ymir work/ui/public/scrollbar_down_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/scrollbar_down_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/scrollbar_down_button_03.sub",
						},
					),
				},
				## Button Accept
				{
					"name" : "Accept_Button",
					"type" : "button",

					"x" : 0,
					"y" : 155,

					"horizontal_align" : "center",

					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
			),
		},
	),
}