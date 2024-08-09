import uiScriptLocale

WINDOW_SIZE = (300, 385)

window = {
	"name" : "MissionManager",
	"style" : ("movable", "float",),

	"x" : 0, "y" : 0,
	"width" : WINDOW_SIZE[0], "height" : WINDOW_SIZE[1],
	"children" :
	[
		{
			"name" : "MissionManager_Board",
			"type" : "main_board_with_titlebar",
			"style" : ("attach",),

			"x" : 0, "y" : 0,
			"width" : WINDOW_SIZE[0], "height" : WINDOW_SIZE[1],

			"title" : "Missions",
			"children" :
			[
				{
					"name" : "MissionManager_Tab_Mission",
					"type" : "bar",

					"x" : 5, "y" : 31,
					"width" : WINDOW_SIZE[0] - 5 * 2, "height" : WINDOW_SIZE[1] - 31 - 5,
					"children" :
					[
						{
							"name" : "MissionManager_Missions_Peek",
							"type" : "window",
							"style" : ("attach",),

							"x" : 0, "y" : 0,
							"width" : WINDOW_SIZE[0] - 5 * 2, "height" : WINDOW_SIZE[1] - 31 - 5,
							"renderer" : True,
							"children" :
							[
								{
									"name" : "MissionManager_Missions_Content",
									"type" : "window",
									"style" : ("attach",),

									"x" : 0, "y" : 0,
									"width" : 0, "height" : 0,
									"children" :
									[
									],
								},
							],
						},
					],
				},
			],
		},
	],
}