import uiScriptLocale

WINDOW_WIDTH = 541
WINDOW_HEIGHT = 385

ROOT_PATH = "assets/ui/skill_select_manager/{}"

window = {
	"name" : "SkillSelectWindow",
	"style" : ("movable", "float",),

	"x" : 0,
	"y" : 0,

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "BOARD",
			"type" : "main_board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"title" : uiScriptLocale.SKILL_SELECT_TITLE,
			"children" :
			(
				{
					"name" : "PATH_0",
					"type" : "image",

					"x" : 5,
					"y" : 31,

					"horizontal_align" : "left",
					"image" : ROOT_PATH.format("path_background.png"),
					"children" : 
					[
						## Header
						{
							"name" : "Header_",
							"type" : "image",

							"x" : 4,
							"y" : 4,

							"image" : ROOT_PATH.format("header_background.png"),
							"children" :
							[
								{
									"name" : "Header_Inner",
									"type" : "image",

									"x" : 5,
									"y" : 0,

									"vertical_align" : "center",
									"image" : ROOT_PATH.format("header_inner.png"),
									"children" :
									[
										{
											"name" : "HEADER_INNER_0",
											"type" : "image",

											"x" : 0,
											"y" : 0,

											"horizontal_align" : "center",
											"vertical_align" : "center",

											"image" : ROOT_PATH.format("inners/warrior_0.png"),
										},

										{
											"name" : "HEADER_JOB_0",
											"type" : "text",

											"x" : -2,
											"y" : -8,

											"horizontal_align" : "right",
											"vertical_align" : "center",

											"text" : "Body",
											"color" : 0xFFb19d58,
										},
									],
								},
							],
						},

						{
							"name" : "Skills_",
							"type" : "image",

							"x" : 0,
							"y" : 15,

							"horizontal_align" : "center",
							"vertical_align" : "center",

							"image" : ROOT_PATH.format("skill_background.png"),
							"children" :
							[
								{
									"name" : "SKILLS_0",
									"type" : "grid_table",
									
									"x" : 17,
									"y" : 15,
									
									"start_index" : 0,
									
									"x_count" : 1,
									"y_count" : 6,
									
									"x_step" : 32,
									"y_step" : 35,
									
									"x_blank" : 6,
									"y_blank" : 1,
									
									"image" : "d:/ymir work/ui/public/Slot_Base.sub"
								},
							],
						},

						{
							"name" : "BUTTON_0",
							"type" : "button",

							"x" : 0,
							"y" : 30,

							"horizontal_align" : "center",
							"vertical_align" : "bottom",
							"text" : translate("Select"),
							"text_height" : 2,

							"default_image" : ROOT_PATH.format("button_0.png"),
							"over_image" : ROOT_PATH.format("button_1.png"),
							"down_image" : ROOT_PATH.format("button_2.png"),
						},
					],
				},

				{
					"name" : "RENDERER",
					"type" : "render_target",

					"x" : 0,
					"y" : 31,

					"horizontal_align" : "center",
					"width" : 263,
					"height" : 349,

					"image" : ROOT_PATH.format("render_background.png"),
				},

				{
					"name" : "PATH_1",
					"type" : "image",

					"x" : 5 + 134,
					"y" : 31,

					"horizontal_align" : "right",
					"image" : ROOT_PATH.format("path_background.png"),
					"children" : 
					[
						## Header
						{
							"name" : "Header_",
							"type" : "image",

							"x" : 4,
							"y" : 4,

							"image" : ROOT_PATH.format("header_background.png"),
							"children" :
							[
								{
									"name" : "Header_Inner",
									"type" : "image",

									"x" : 5,
									"y" : 0,

									"vertical_align" : "center",
									"image" : ROOT_PATH.format("header_inner.png"),
									"children" :
									[
										{
											"name" : "HEADER_INNER_1",
											"type" : "image",

											"x" : 0,
											"y" : 0,

											"horizontal_align" : "center",
											"vertical_align" : "center",

											"image" : ROOT_PATH.format("inners/warrior_0.png"),
										},

										{
											"name" : "HEADER_JOB_1",
											"type" : "text",

											"x" : -2,
											"y" : -8,

											"horizontal_align" : "right",
											"vertical_align" : "center",

											"text" : "Body",
											"color" : 0xFFb19d58,
										},
									],
								},
							],
						},

						{
							"name" : "Skills_",
							"type" : "image",
							"x" : 0,
							"y" : 15,

							"horizontal_align" : "center",
							"vertical_align" : "center",

							"image" : ROOT_PATH.format("skill_background.png"),
							"children" :
							[
								{
									"name" : "SKILLS_1",
									"type" : "grid_table",
									
									"x" : 17,
									"y" : 15,
									
									"start_index" : 0,
									
									"x_count" : 1,
									"y_count" : 6,
									
									"x_step" : 32,
									"y_step" : 35,
									
									# "x_blank" : 6,
									# "y_blank" : 1,
									
									"image" : "d:/ymir work/ui/public/Slot_Base.sub"
								},
							],
						},

						{
							"name" : "BUTTON_1",
							"type" : "button",

							"x" : 0,
							"y" : 30,

							"horizontal_align" : "center",
							"vertical_align" : "bottom",
							"text" : translate("Select"),
							"text_height" : 2,

							"default_image" : ROOT_PATH.format("button_0.png"),
							"over_image" : ROOT_PATH.format("button_1.png"),
							"down_image" : ROOT_PATH.format("button_2.png"),
						},
					],
				},
			),
		},
	),
}