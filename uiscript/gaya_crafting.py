import uiScriptLocale

window = {
	"name" : "GemShopWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float", "animate",),

	"width" : 174,
	"height" : 110,

	"children" :
	(
		## Board
		{
			"name" : "board",
			"style" : ("attach",),
			"type" : "board_with_titlebar",

			"x" : 0,
			"y" : 0,

			"width" : 174,
			"height" : 110,

			"title" : uiScriptLocale.GAYA_CRAFTING_TITLE,

			"children" :
			(
				## SlotBase
				{
					"name" : "CraftingItems",
					"type" : "grid_table",

					"x" : 7,
					"y" : 40,

					"start_index" : 0,
					"x_count" : 5,
					"y_count" : 1,
					"x_step" : 32,
					"y_step" : 32,

					"image" : "d:/ymir work/ui/public/Slot_Base.sub"
				},
				## Exit Button
				{
					"name" : "ExitButton",
					"type" : "button",

					"x" : 0,
					"y" : 30,

					"horizontal_align" : "center",
					"vertical_align" : "bottom",

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",

					"text" : uiScriptLocale.GAYA_CRAFTING_LEAVE_BUTTON,
				},
			),
		},
	),
}