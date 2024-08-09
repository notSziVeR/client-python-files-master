#-*- coding: iso-8859-1 -*-a

import uiScriptLocale

WINDOW_WIDTH = 470
WINDOW_HEIGHT = 320

ROOT_PATH = "d:/ymir work/ui/game/find_letters/"

window = {
	"name" : "FindLettersWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float", "animate", ),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children":
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : WINDOW_WIDTH - 15,
					"color" : "yellow",

					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",

							"x" : (WINDOW_WIDTH - 15) / 2,
							"y" : 3,

							"text" : uiScriptLocale.LETTERS_WINDOW_TITLE,
							"text_horizontal_align":"center"
						},
					),
				},

				{
					"name" : "LettersBG",
					"type" : "image",

					"x" : 12,
					"y" : 30,

					"image" : ROOT_PATH + "find_letters_bg.tga",

					"children" :
					(
						{
							"name" : "LettersTitleBG",
							"type" : "image",

							"x" : 0,
							"y" : 10,

							"image" : ROOT_PATH + "find_letters_title.tga",
							"horizontal_align":"center",

							"children" :
							(
								{
									"name" : "LettersTitleText",
									"type" : "text",

									"x" : -15,
									"y" : 8,

									"text" : "* ZnajdŸ Literê *",

									"horizontal_align":"center",
									"text_horizontal_align":"center",
									"text_vertical_align":"center",
								},
							),
						},

						{
							"name" : "LettersWindowBack",
							"type" : "window",

							"x" : 2,
							"y" : 70,

							"width" : 446 - 2,
							"height" : 173 - 70,
						},

						{
							"name" : "LettersWindow",
							"type" : "window",

							"x" : 9,
							"y" : 77,

							"width" : 446 - 9,
							"height" : 173 - 77,
						},

						{
							"name" : "score_completion_effect1",
							"type" : "ani_image",

							"x" : 95,
							"y" : 23,

							"delay" : 6,

							"images" :
							(
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff1.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff2.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff3.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff4.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff5.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff6.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff7.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff8.sub",
							),
						},

						{
							"name" : "score_completion_effect2",
							"type" : "ani_image",

							"x" : 138,
							"y" : 23,

							"delay" : 6,

							"images" :
							(
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff1.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff2.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff3.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff4.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff5.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff6.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff7.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff8.sub",
							),
						},

						{
							"name" : "score_completion_effect3",
							"type" : "ani_image",

							"x" : 181,
							"y" : 23,

							"delay" : 6,

							"images" :
							(
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff1.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff2.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff3.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff4.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff5.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff6.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff7.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_eff8.sub",
							),
						},
						{
							"name" : "score_completion_text_effect",
							"type" : "ani_image",

							"x" : 129,
							"y" : 56,

							"delay" : 0,

							"images" :
							(

								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect1.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect5.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect5.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect5.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect5.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect5.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect6.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect6.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect7.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect8.sub",
								"D:/Ymir Work/UI/minigame/rumi/card_completion_effect/card_completion_text_effect9.sub",
							),
						},
					),
				},

				{
					"name" : "RewardLeftImage",
					"type" : "image",

					"x" : 12,
					"y" : 210,

					"image" : ROOT_PATH + "reward_bg_left.tga",

					"children" :
					(
						{
							"name" : "RewardLeftButton",
							"type" : "button",

							"x" : 3,
							"y" : 0,

							"vertical_align" : "center",

							"default_image" : ROOT_PATH + "left_btn_01.tga",
							"over_image" : ROOT_PATH + "left_btn_02.tga",
							"down_image" : ROOT_PATH + "left_btn_03.tga",
						},
					),
				},

				{
					"name" : "RewardImageBG0",
					"type" : "image",

					"x" : 27,
					"y" : 210,

					"image" : ROOT_PATH + "reward_bg.tga",
				},
				{
					"name" : "RewardImageBG1",
					"type" : "image",

					"x" : 27 + 104,
					"y" : 210,

					"image" : ROOT_PATH + "reward_bg.tga",
				},
				{
					"name" : "RewardImageBG2",
					"type" : "image",

					"x" : 27 + 104 + 104,
					"y" : 210,

					"image" : ROOT_PATH + "reward_bg.tga",
				},
				{
					"name" : "RewardImageBG3",
					"type" : "image",

					"x" : 27 + 104 + 104 + 104,
					"y" : 210,

					"image" : ROOT_PATH + "reward_bg.tga",
				},

				{
					"name" : "RewardRightImage",
					"type" : "image",

					"x" : 443,
					"y" : 210,

					"image" : ROOT_PATH + "reward_bg_right.tga",

					"children" :
					(
						{
							"name" : "RewardRightButton",
							"type" : "button",

							"x" : 2,
							"y" : 0,

							"vertical_align" : "center",

							"default_image" : ROOT_PATH + "right_btn_01.tga",
							"over_image" : ROOT_PATH + "right_btn_02.tga",
							"down_image" : ROOT_PATH + "right_btn_03.tga",
						},
					),
				},
			),
		},
	),
}

