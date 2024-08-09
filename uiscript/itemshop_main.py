import uiScriptLocale

BASE_PATH = "itemshop/"

window = {
	"name" : "ItemShop",

	"x" : 0,
	"y" : 0,
	
	"style" : ("movable", "float",),

	"width" : 947,
	"height" : 514,

	"children" :
	(
		{
			"name" : "board",
			"type" : "expanded_image",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"image" : BASE_PATH + "board.png",
			"children" :
			(
				## Exit - Button
				{
					"name" : "Exit_Button",
					"type" : "button",

					"x" : 919,
					"y" : 0,

					"default_image" : BASE_PATH + "button_exit_n.png",
					"over_image" : BASE_PATH + "button_exit_h.png",
					"down_image" : BASE_PATH + "button_exit_d.png",
				},
				## Cash - Text
				{
					"name" : "Cash_Text",
					"type" : "text",

					"x" : 48,
					"y" : 30,

					"text" : "",
					"color" : 0xffDCDBD8,
				},
				## Category Name - Text
				{
					"name" : "Category_Name_Text",
					"type" : "text",

					"x" : 204,
					"y" : 97,

					"text" : "",
					"color" : 0xffF8E3AE,
				},
				## Donate - Button
				{
					"name" : "Donate_Button",
					"type" : "button",

					"x" : 173,
					"y" : 27,

					"default_image" : BASE_PATH + "button_donate_n.png",
					"over_image" : BASE_PATH + "button_donate_h.png",
					"down_image" : BASE_PATH + "button_donate_d.png",
				},
				## Categories - ListBox
				{
					"name" : "Category_ListBox",
					"type" : "listboxex",

					"x" : 12,
					"y" : 86,

					"width" : 137,
					"height" : 416,
				},
				## Items - ListBox
				{
					"name" : "Items_ListBox",
					"type" : "grid_listbox",

					"x" : 191,
					"y" : 127,

					"width" : 708,
					"height" : 370,

					"itemsize" : (228, 116),
					"itemstep" : (242, 129),
					"viewcount" : (3, 3),
				},
			),
		},
	),
}