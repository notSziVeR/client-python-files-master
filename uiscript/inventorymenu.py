import uiScriptLocale
import app

ROOT = "assets/ui/special_storage/{}"

BOARD_WIDTH = 188
BOARD_HEIGHT = 140 + 28 * 3

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

window = {
	"name" : "InventoryMenu",

	"style" : ("movable", "float", "animate",),

	"x" : (SCREEN_WIDTH / 2) - (BOARD_WIDTH / 2),
	"y" : (SCREEN_HEIGHT / 2) - (BOARD_HEIGHT / 2),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "main_board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"title" : uiScriptLocale.INVENTORY_MENU_TITLE,

			"children" :
			(
				{
					"name" : "BlackBoard",
					"type" : "main_sub_board",
					"style" : ("attach",),

					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST,
					"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),

					"children" :
					(
						{
							"name" : "SafeBox",
							"type" : "button",

							"x" : 0,
							"y" : 8,

							"horizontal_align" : "center",
							"text" : uiScriptLocale.INVENTORY_MENU_SAFEBOX,
							"text_height" : 2,

							"default_image" : ROOT.format("button_menu_norm.png"),
							"over_image" : ROOT.format("button_menu_hover.png"),
							"down_image" : ROOT.format("button_menu_down.png"),
						},

						{
							"name" : "ItemShop",
							"type" : "button",

							"x" : 0,
							"y" : 8 + 28,

							"horizontal_align" : "center",
							"text" : uiScriptLocale.INVENTORY_MENU_ITEMSHOP,
							"text_height" : 2,

							"default_image" : ROOT.format("button_menu_norm.png"),
							"over_image" : ROOT.format("button_menu_hover.png"),
							"down_image" : ROOT.format("button_menu_down.png"),
						},

						{
							"name" : "INVENTORY_MENU_STORAGE_01",
							"type" : "button",

							"x" : 0,
							"y" : 8 + (28 * 2),

							"horizontal_align" : "center",
							"text" : uiScriptLocale.INVENTORY_MENU_STORAGE_01,
							"text_height" : 2,

							"default_image" : ROOT.format("button_menu_norm.png"),
							"over_image" : ROOT.format("button_menu_hover.png"),
							"down_image" : ROOT.format("button_menu_down.png"),
						},

						{
							"name" : "INVENTORY_MENU_STORAGE_02",
							"type" : "button",

							"x" : 0,
							"y" : 8 + (28 * 3),

							"horizontal_align" : "center",
							"text" : uiScriptLocale.INVENTORY_MENU_STORAGE_03,
							"text_height" : 2,

							"default_image" : ROOT.format("button_menu_norm.png"),
							"over_image" : ROOT.format("button_menu_hover.png"),
							"down_image" : ROOT.format("button_menu_down.png"),
						},

						{
							"name" : "INVENTORY_MENU_STORAGE_03",
							"type" : "button",

							"x" : 0,
							"y" : 8 + (28 * 4),

							"horizontal_align" : "center",
							"text" : uiScriptLocale.INVENTORY_MENU_STORAGE_04,
							"text_height" : 2,

							"default_image" : ROOT.format("button_menu_norm.png"),
							"over_image" : ROOT.format("button_menu_hover.png"),
							"down_image" : ROOT.format("button_menu_down.png"),
						},

						{
							"name" : "INVENTORY_MENU_STORAGE_04",
							"type" : "button",

							"x" : 0,
							"y" : 8 + (28 * 5),

							"horizontal_align" : "center",
							"text" : uiScriptLocale.INVENTORY_MENU_STORAGE_05,
							"text_height" : 2,

							"default_image" : ROOT.format("button_menu_norm.png"),
							"over_image" : ROOT.format("button_menu_hover.png"),
							"down_image" : ROOT.format("button_menu_down.png"),
						},
					)
				},
			),
		},
	)
}
