import uiScriptLocale

BATTLE_PASS_UI_PATH = "d:/ymir work/ui/game/battle_pass/"

BAR_COLOUR = 0x0fffffff
BAR_BREADTH = 14

window = {
	"name" : "BattlePass",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float","animate",),

	"width" : 550,
	"height" : 290,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 550,
			"height" : 290,

			"title" : uiScriptLocale.BATTLE_PASS_TITLE,

			"children" :
			(
				## Task List - Board
				{
					"name" : "TaskList_Board",
					"type" : "border_a",

					"x" : 10,
					"y" : 30,

					"width" : 307,
					"height" : 250,

					"children" :
					(
						## Task List - Window
						{
							"name" : "TaskList_Window",
							"type" : "window",

							"x" : 3,
							"y" : 3,

							"width" : 307-6,
							"height" : 250-6,

							"children" :
							(
								## Scroll Area Scroll - Window
								{
									"name" : "TaskListScroll_Window",
									"type" : "window",

									"x" : 301-6,
									"y" : 0,

									"width" : 6,
									"height" : 250-6,
								},
							),
						},
						## Ranking - Window
						{
							"name" : "Ranking_Window",
							"type" : "window",

							"x" : 3,
							"y" : 3,

							"width" : 307-6,
							"height" : 250-6,

							"children" :
							(
								## Ranking - Header
								{
									"name" : "RankingHeader",
									"type" : "expanded_image",

									"x" : 0,
									"y" : 0,

									"image" : BATTLE_PASS_UI_PATH + "ranking_title.tga",
								},
							),
						},
					),
				},
				## Basic Info - Window
				{
					"name" : "BasicInfo_Window",
					"type" : "window",

					"x" : 307 + 10 + 10,
					"y" : 30,

					"width" : 207,
					"height" : 250,

					"children" :
					(
						## Basic Info Options - Radio Button
						{
							"name" : "BasicInfoOptions_RadioButton",
							"type" : "button",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",

							"default_image" : BATTLE_PASS_UI_PATH + "category_btn_1.tga",
							"over_image" : BATTLE_PASS_UI_PATH + "category_btn_2.tga",
							"down_image" : BATTLE_PASS_UI_PATH + "category_btn_2.tga",
						},
						## Basic Info Options - Board
						{
							"name" : "BasicInfoOptions_Board",
							"type" : "border_a",

							"x" : 0,
							"y" : 26,

							"horizontal_align" : "center",

							"width" : 207,
							"height" : 250-26,

							"children" :
							(
								## Basic Info Options - Information Label
								{
									"name" : "BasicInfoOptions_InformationLabel",
									"type" : "expanded_image",

									"x" : 3,
									"y" : 3,

									"image" : BATTLE_PASS_UI_PATH + "title_bar_special.tga",
									"children" :
									(
										## Basic Info Options - Information Text
										{
											"name" : "BasicInfoOptions_InformationText",
											"type" : "text",

											"x" : 0,
											"y" : 0,

											"all_align" : "center",
											"text" : uiScriptLocale.BATTLE_PASS_BASIC_INFORMATION,
										},
									),
								},
								## Basic Info Options - Difficulity Bar
								{
									"name" : "BasicInfoOptions_DifficulityBar",
									"type" : "bar",

									"x" : 10,
									"y" : 30,

									"width" : 250-26-30,
									"height" : BAR_BREADTH,

									"color" : BAR_COLOUR,

									"children" :
									(
										## Basic Info Options - Difficulity Text
										{
											"name" : "BasicInfoOptions_DifficulityText",
											"type" : "text",

											"x" : 2,
											"y" : 0,

											"text" : "",
										},
									),
								},
								## Basic Info Options - Month Bar
								{
									"name" : "BasicInfoOptions_MonthBar",
									"type" : "bar",

									"x" : 10,
									"y" : 30 + BAR_BREADTH + 10,

									"width" : 250-26-30,
									"height" : BAR_BREADTH,

									"color" : BAR_COLOUR,

									"children" :
									(
										## Basic Info Options - Month Text
										{
											"name" : "BasicInfoOptions_MonthText",
											"type" : "text",

											"x" : 2,
											"y" : 0,

											"text" : "",
										},
									),
								},
								## Basic Info Options - Remaining Time Bar
								{
									"name" : "BasicInfoOptions_RemainingTimeBar",
									"type" : "bar",

									"x" : 10,
									"y" : 30 + (BAR_BREADTH + 10)*2,

									"width" : 250-26-30,
									"height" : BAR_BREADTH,

									"color" : BAR_COLOUR,

									"children" :
									(
										## Basic Info Options - Remaining Time Text
										{
											"name" : "BasicInfoOptions_RemainingTimeText",
											"type" : "text",

											"x" : 2,
											"y" : 0,

											"text" : "",
										},
									),
								},
								## Basic Info Options - Finished Bar
								{
									"name" : "BasicInfoOptions_FinishedBar",
									"type" : "bar",

									"x" : 10,
									"y" : 30 + (BAR_BREADTH + 10)*3,

									"width" : 250-26-30,
									"height" : BAR_BREADTH,

									"color" : BAR_COLOUR,

									"children" :
									(
										## Basic Info Options - Finished Text
										{
											"name" : "BasicInfoOptions_FinishedText",
											"type" : "text",

											"x" : 2,
											"y" : 0,

											"text" : "",
										},
									),
								},
								## Basic Info Options - Progress Bar
								{
									"name" : "BasicInfoOptions_ProgressBar",
									"type" : "bar",

									"x" : 10,
									"y" : 30 + (BAR_BREADTH + 10)*4,

									"width" : 250-26-30,
									"height" : BAR_BREADTH,

									"color" : BAR_COLOUR,

									"children" :
									(
										## Basic Info Options - Progress Text
										{
											"name" : "BasicInfoOptions_ProgressText",
											"type" : "text",

											"x" : 2,
											"y" : 0,

											"text" : "",
										},
									),
								},
								## Basic Info Options - Reward Collected Bar
								{
									"name" : "BasicInfoOptions_RewardCollectedBar",
									"type" : "bar",

									"x" : 10,
									"y" : 30 + (BAR_BREADTH + 10)*5,

									"width" : 250-26-30,
									"height" : BAR_BREADTH,

									"color" : BAR_COLOUR,

									"children" :
									(
										## Basic Info Options - Reward Collected Text
										{
											"name" : "BasicInfoOptions_RewardCollectedText",
											"type" : "text",

											"x" : 2,
											"y" : 0,

											"text" : "",
										},
									),
								},
								## Basic Info Options - Collect Button
								{
									"name" : "BasicInfoOptions_CollectButton",
									"type" : "button",

									"x" : -43,
									"y" : 30 + (BAR_BREADTH + 10)*6.5,

									"horizontal_align" : "center",

									"default_image" : BATTLE_PASS_UI_PATH + "reward_normal.tga",
									"over_image" : BATTLE_PASS_UI_PATH + "reward_over.tga",
									"down_image" : BATTLE_PASS_UI_PATH + "reward_down.tga",
								},
								## Basic Info Options - Reward Info Button
								{
									"name" : "BasicInfoOptions_RewardInfoButton",
									"type" : "button",

									"x" : 43 + 10,
									"y" : 30 + (BAR_BREADTH + 10)*6.5,

									"horizontal_align" : "center",

									"default_image" : BATTLE_PASS_UI_PATH + "ranking_normal.tga",
									"over_image" : BATTLE_PASS_UI_PATH + "ranking_over.tga",
									"down_image" : BATTLE_PASS_UI_PATH + "ranking_down.tga",
								},
							),
						},
					),
				},
				## Bar Curtain
				{
					"name" : "BarCurtain",
					"type" : "bar",

					"x" : 10,
					"y" : 30,

					"width" : 534,
					"height" : 250,

					"color" : 0x77000000,
				},
			),
		},
	),
}

