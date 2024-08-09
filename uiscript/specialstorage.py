import uiScriptLocale
import item

ROOT_PATH = "assets/ui/special_storage/{}"

UI_PATH = "d:/ymir work/ui/game/special_storage/"
TAB_SIZE = 32

WINDOW_WIDTH = 190
WINDOW_HEIGHT = 430

BUTTON_WIDTH = 38
BUTTON_HEIGHT = 39

SMIDDLE_NAME = "tab_button_smiddle_%s.sub"
SMALL_NAME = "tab_button_smiddle_%s.sub"

Main_Iterator = 0

def AppendCattegoryButton(sKey):
	global Main_Iterator
	Main_Iterator += 1

	PADDING = 10

	CONTENT_WIDTH = WINDOW_WIDTH - 5 * 2

	WND_PADDING = CONTENT_WIDTH - PADDING * 2

	BTN_SPACE = float(WND_PADDING - 32) / float(4 - 1)

	BTN_ENTRY_X = PADDING + ((Main_Iterator - 1) * BTN_SPACE)

	return {
		"name" : "Storage_Tab_0{}".format(Main_Iterator),
		"type" : "radio_button",

		"x" : BTN_ENTRY_X, "y" : 12,
		"default_image" : ROOT_PATH.format("categories/{}_normal.png".format(sKey)),
		"over_image" : ROOT_PATH.format("categories/{}_hover.png".format(sKey)),
		"down_image" : ROOT_PATH.format("categories/{}_down.png".format(sKey)),
	}

window = {
	"name" : "SpecialStorageWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("movable", "float", "animate",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		## Inventory, Equipment Slots
		{
			"name" : "board",
			"type" : "main_board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"title" : uiScriptLocale.SPECIAL_STORAGE_TITLE,

			"children" :
			(
				{
					"name" : "sub_board_items",
					"type" : "main_sub_board",

					"x" : 5,
					"y" : 31,

					"width" : WINDOW_WIDTH - 5 * 2,
					"height" : 310,

					"full_opacity" : True,
					"children" :
					[
						## Item Slot
						{
							"name" : "ItemSlot",
							"type" : "grid_table",

							"x" : 6,
							"y" : 5,

							"start_index" : item.SPECIAL_STORAGE_START_CELL,
							"x_count" : item.SPECIAL_STORAGE_PAGE_LENGTH,
							"y_count" : item.SPECIAL_STORAGE_PAGE_BREADTH,
							"x_step" : 34,
							"y_step" : 34,

							"image" : "d:/ymir work/ui/public/Slot_Base.sub",
						},
					],
				},

				{
					"name" : "sub_board_menu",
					"type" : "main_sub_board",

					"x" : 5,
					"y" : 31 + 310 + 2,

					"width" : WINDOW_WIDTH - 5 * 2,
					"height" : 80,

					"full_opacity" : True,
					"children" :
					[
						AppendCattegoryButton("stone"),
						AppendCattegoryButton("book"),
						AppendCattegoryButton("material"),
						AppendCattegoryButton("general"),

						## Inventory Tab - 1
						{
							"name" : "Inventory_Tab_01",
							"type" : "radio_button",

							"x" : 5,
							"y" : 30,

							"vertical_align" : "bottom",
							"default_image" : ROOT_PATH.format("btn_page_0.png"),
							"over_image" : ROOT_PATH.format("btn_page_1.png"),
							"down_image" : ROOT_PATH.format("btn_page_2.png"),

							"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP % 1,

							"children" :
							(
								{
									"name" : "Equipment_Tab_01_Print",
									"type" : "text",

									"x" : 0,
									"y" : -2.5,

									"all_align" : "center",

									"text" : "I",
								},
							),
						},
						## Inventory Tab - 2
						{
							"name" : "Inventory_Tab_02",
							"type" : "radio_button",

							"x" : 48,
							"y" : 30,

							"vertical_align" : "bottom",
							"default_image" : ROOT_PATH.format("btn_page_0.png"),
							"over_image" : ROOT_PATH.format("btn_page_1.png"),
							"down_image" : ROOT_PATH.format("btn_page_2.png"),

							"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP % 2,

							"children" :
							(
								{
									"name" : "Equipment_Tab_02_Print",
									"type" : "text",

									"x" : 0,
									"y" : -2.5,

									"all_align" : "center",

									"text" : "II",
								},
							),
						},
						## Inventory Tab - 3
						{
							"name" : "Inventory_Tab_03",
							"type" : "radio_button",

							"x" : 92,
							"y" : 30,

							"vertical_align" : "bottom",
							"default_image" : ROOT_PATH.format("btn_page_0.png"),
							"over_image" : ROOT_PATH.format("btn_page_1.png"),
							"down_image" : ROOT_PATH.format("btn_page_2.png"),

							"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP % 3,

							"children" :
							(
								{
									"name" : "Equipment_Tab_03_Print",
									"type" : "text",

									"x" : 0,
									"y" : -2.5,

									"all_align" : "center",

									"text" : "III",
								},
							),
						},
						## Inventory Tab - 4
						{
							"name" : "Inventory_Tab_04",
							"type" : "radio_button",

							"x" : 135,
							"y" : 30,

							"vertical_align" : "bottom",
							"default_image" : ROOT_PATH.format("btn_page_0.png"),
							"over_image" : ROOT_PATH.format("btn_page_1.png"),
							"down_image" : ROOT_PATH.format("btn_page_2.png"),

							"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP % 4,


							"children" :
							(
								{
									"name" : "Equipment_Tab_04_Print",
									"type" : "text",

									"x" : 0,
									"y" : -2.5,

									"all_align" : "center",

									"text" : "IV",
								},
							),
						},
					],
				},
			),
		},
	),
}