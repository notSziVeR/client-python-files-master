import uiScriptLocale

BASE_PATH = "assets/ui/tombola/"

window = {
	"name" : "Tombola",

	"x" : 0,
	"y" : 0,
	
	"style" : ("movable", "float", "animate",),

	"width" : 329 + 20,
	"height" : 329 + 40,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : 329 + 20,
			"height" : 329 + 40,

			"title" : uiScriptLocale.TOMBOLA_WINDOW_TITLE,

			"children" :
			(
				## Main Board - Image
				{
					"name" : "main_board",
					"type" : "expanded_image",

					"x" : 10,
					"y" : 30,

					"image" : BASE_PATH + "board.tga",
					"children" :
					(
						{
							"name" : "User_Balance_Board",
							"type" : "boxed_board",

							"x" : 0,
							"y" : 0,

							"width" : 105,
							"height" : 20,
							"children" :
							[
								## User Balance - Text
								{
									"name" : "User_Balance_Text",
									"type" : "text",

									"x" : 0,
									"y" : 1,

									"horizontal_align" : "center",
									"text_horizontal_align" : "center",

									"fontsize" : "LARGE",
									"text" : "",
								},
							],
						},

						## Slot Window
						{
							"name" : "Slots",
							"type" : "slot",

							"x" : 0,
							"y" : 0,

							"width" : 329,
							"height" : 329,

							"slot" : (
										{"index":0, "x":161 - 10, "y":53 - 4 - 30, "width":32, "height":32},
										{"index":1, "x":207 - 10, "y":63 - 4 - 30, "width":32, "height":32},
										{"index":2, "x":248 - 10, "y":93 - 4 - 30, "width":32, "height":32},
										{"index":3, "x":277 - 10, "y":135 - 4 - 30, "width":32, "height":32},
										{"index":4, "x":290 - 10, "y":182 - 4 - 30, "width":32, "height":32},
										{"index":5, "x":277 - 10, "y":228 - 4 - 30, "width":32, "height":32},
										{"index":6, "x":248 - 10, "y":271 - 4 - 30, "width":32, "height":32},
										{"index":7, "x":207 - 10, "y":298 - 4 - 30, "width":32, "height":32},
										{"index":8, "x":160 - 10, "y":307 - 4 - 30, "width":32, "height":32},
										{"index":9, "x":114 - 10, "y":296 - 4 - 30, "width":32, "height":32},
										{"index":10, "x":72 - 10, "y":269 - 4 - 30, "width":32, "height":32},
										{"index":11, "x":44 - 10, "y":229 - 4 - 30, "width":32, "height":32},
										{"index":12, "x":30 - 10, "y":183 - 4 - 30, "width":32, "height":32},
										{"index":13, "x":41 - 10, "y":133 - 4 - 30, "width":32, "height":32},
										{"index":14, "x":70 - 10, "y":92 - 4 - 30, "width":32, "height":32},
										{"index":15, "x":112 - 10, "y":63 - 4 - 30, "width":32, "height":32},
									),
						},
						## Spin - Button
						{
							"name" : "Spin_Button",
							"type" : "button",

							"x" : 125,
							"y" : 125,

							"default_image" : BASE_PATH + "button_normal.tga",
							"over_image" : BASE_PATH + "button_hover.tga",
							"down_image" : BASE_PATH + "button_down.tga",
							"children" :
							[
								{
									"name" : "Spin_Cost",
									"type" : "text",

									"x" : 0,
									"y" : 20,

									"all_align" : "center",

									"color" : 0xFFC19B17,

									"text" : "100 SM",
								},
							],
						},
					),
				},
			),
		},
	),
}