import uiScriptLocale

MAIN_PATH = "assets/ui/dungeon_task/"

window = {
	"name" : "DungeonTask",

	"x" : 0,
	"y" : 0,
	
	"style" : ("float",),

	"width" : 277,
	"height" : 122,

	"children" :
	(
		{
			"name" : "Board",
			"type" : "expanded_image",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"image" : MAIN_PATH + "board_2.tga",
			"children" :
			(
				## Task Label - Text
				{
					"name" : "StageLabel",
					"type" : "text",

					"x" : 75,
					"y" : 3,

					"text" : uiScriptLocale.DUNGEON_TASK_STAGE_TITLE,
					"color" : 0xff928E85,
				},

				## Description - Window
				{
					"name" : "DescriptionWindow",
					"type" : "window",

					"x" : 14,
					"y" : 50,

					"width" : 237,
					"height" : 36,

					"children" :
					(
						## Description - Text
						{
							"name" : "StageDescription",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "",
							"color" : 0xff928E85,
						},
						## Stage Time Left - Text
						{
							"name" : "StageTimeLeft",
							"type" : "text",

							"x" : 0,
							"y" : 12,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "",
							"color" : 0xffB19B67,
						},
					),
				},
				## Global Time Left - Window
				{
					"name" : "GlobalTimeLeftWindow",
					"type" : "window",

					"x" : 7,
					"y" : 101,

					"width" : 121,
					"height" : 12,

					"children" :
					(
						## Global Time Left - Text
						{
							"name" : "GlobalTimeLeft",
							"type" : "text",

							"x" : 0,
							"y" : -2,

							"all_align" : "center",

							"text" : "",
							"color" : 0xff928E85,
						},
					),
				},
				## Global Stage Count - Window
				{
					"name" : "GlobalStageCountWindow",
					"type" : "window",

					"x" : 143,
					"y" : 101,

					"width" : 121,
					"height" : 12,

					"children" :
					(
						## Global Stage Count - Text
						{
							"name" : "GlobalStageCount",
							"type" : "text",

							"x" : 0,
							"y" : -2,

							"all_align" : "center",

							"text" : "",
							"color" : 0xff928E85,
						},
					),
				},
			),
		},
	),
}