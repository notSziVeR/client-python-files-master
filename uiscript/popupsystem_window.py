PATH = "assets/ui/popup/{}"

window = {
    "name" : "PopupSystem",
 
    "x" : 0,
    "y" : -102,
 
    "style" : ("float",),
 
    "width" : 433,
    "height" : 102,
 
    "children" :
    (
		## Board
		{
			"name" : "Board",
			"style" : ("attach", ),
			"type" : "expanded_image",

			"x" : 0,
			"y" : 0,

			"image" : PATH.format("board.png"),
			"children" :
			(
				## Popup Text - Area
				{
					"name" : "Popup_Text_Area",
					"type" : "window",

					"x" : 107,
					"y" : 32,

					"width" : 268,
					"height" : 53,

					"children" :
					(
						## Popup Header - Text
						{
							"name" : "Popup_Header_Text",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",

							"text" : "SOME SAMPLE TEXT",
							"color" : 0xff999999,
						},
					),
				},
				## Popup Icon - Image
				{
					"name" : "Popup_Icon_Image",
					"type" : "expanded_image",

					"x" : 34,
					"y" : -3,
					"vertical_align" : "center",

					"image" : PATH.format("icon_base.png"),
					"children" :
					(
						## Popup Item Icon - Window
						{
							"name" : "Popup_Item_Icon_Window",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,

							"all_align" : "center",

							"width" : 32,
							"height" : 32,
						},
					),
				},
			),
		},
	),
}
