
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 120

window = {
	"name" : "ScalingOptionWindow",
	"type" : "window",
	"style" : ["movable", "float",],

	"x" : 0, "y" : 0,
	"width" : WINDOW_WIDTH, "height" : WINDOW_HEIGHT,


	"children" : 
	[
		{
			"name" : "ScalingOptionBoard",
			"type" : "board_with_titlebar",

			"x" : 0, "y" : 0,
			"width" : WINDOW_WIDTH, "height" : WINDOW_HEIGHT,

			"title" : "ScalingOption",
			"children" : 
			[
				{
					"name" : "SLIDER_STONES",
					"type" : "sliderbar",
					"x" : 0,"y" : 50,
					"horizontal_align" : "center",
					"children":
					[
						{
							"name" : "textline_0",
							"type" : "text",
							"x" : 0,"y" : -20,
							"all_align" : "center",
							"text" : "Scale Stones"
						},
					]
				},

				{
					"name" : "SLIDER_BOSESS",
					"type" : "sliderbar",
					"x" : 0,"y" : 90,
					"horizontal_align" : "center",
					"children":
					[
						{
							"name" : "textline_0",
							"type" : "text",
							"x" : 0,"y" : -20,
							"all_align" : "center",
							"text" : "Scale Bosess"
						},
					]
				},
			],
		}
	],
}