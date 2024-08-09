import uiScriptLocale
import item
import app

import player
EQUIPMENT_START_INDEX = player.EQUIPMENT_SLOT_START

ROOT_PATH = "d:/ymir work/ui/game/inventory/"

SMALL_NAME = "tab_button_large_half_%s.sub"

BOARD_WIDTH = 178
BOARD_HEIGHT = 540

PAGE_LEFT_X_DIST = 4
PAGE_RIGHT_X_DIST = 5
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

BUTTON_TAB_COUNT_PER_LINE = 4
BUTTON_TAB_WIDTH = 38
BUTTON_TAB_GAP = 2

BUTTON_TAB_SPACE = BUTTON_TAB_WIDTH + BUTTON_TAB_GAP

Main_ButtonGroupCounter = -1
def Main_GetButtonGroup(inc = False):
	global Main_ButtonGroupCounter

	if inc:
		Main_ButtonGroupCounter += 1
	return Main_ButtonGroupCounter

window = {
	"name" : "InventoryWindow",

	"x" : SCREEN_WIDTH - BOARD_WIDTH,
	"y" : SCREEN_HEIGHT - (BOARD_HEIGHT) - (37 + 30),

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
		## Inventory, Equipment Slots
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : BOARD_WIDTH - 15,
					"color" : "yellow",

					"children" :
					(
						{ "name":"TitleName", "type":"text", "x":0, "y":-1, "all_align" : True, "text":uiScriptLocale.INVENTORY_TITLE, "text_horizontal_align":"center" },
					),
				},

				{
					"name" : "ThinBoard",
					"type" : "window",

					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST,
					"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),
					"children" :
					[
						{
							"name" : "Equipment_Page",
							"type" : "image",

							"x" : 0,
							"y" : 0,
							
							"horizontal_align" : "center",
							"image" : "assets/ui/inventory/equipment_bg_without_ring.tga",

							"children" :
							(
								{
									"name" : "EquipmentSlot",
									"type" : "slot",

									"x" : 3,
									"y" : 3,

									"width" : 150,
									"height" : 182,

									"slot" : (
												{"index":EQUIPMENT_START_INDEX+0, "x":39, "y":37, "width":32, "height":64},
												{"index":EQUIPMENT_START_INDEX+1, "x":39, "y":2, "width":32, "height":32},
												{"index":EQUIPMENT_START_INDEX+2, "x":39, "y":145, "width":32, "height":32},
												{"index":EQUIPMENT_START_INDEX+3, "x":75, "y":67, "width":32, "height":32},
												{"index":EQUIPMENT_START_INDEX+4, "x":3, "y":3, "width":32, "height":96},
												{"index":EQUIPMENT_START_INDEX+5, "x":114, "y":67, "width":32, "height":32},
												{"index":EQUIPMENT_START_INDEX+6, "x":114, "y":35, "width":32, "height":32},
												{"index":EQUIPMENT_START_INDEX+7, "x":2, "y":145, "width":32, "height":32},
												{"index":EQUIPMENT_START_INDEX+8, "x":75, "y":145, "width":32, "height":32},
												# {"index":EQUIPMENT_START_INDEX+9, "x":114, "y":2, "width":32, "height":32},
												{"index":item.EQUIPMENT_AMULET, "x":114, "y":2, "width":32, "height":32},
												{"index":EQUIPMENT_START_INDEX+10, "x":75, "y":35, "width":32, "height":32},

												{"index":item.EQUIPMENT_BELT, "x":39, "y":106, "width":32, "height":32},

												# {"index":item.EQUIPMENT_PENDANT, "x":3, "y":106, "width":32, "height":32},

												{"index":item.WEAR_UNIQUE3, "x":3, "y":106, "width":32, "height":32},
												{"index":item.WEAR_UNIQUE4, "x":75, "y":106, "width":32, "height":32},
											),
								},

								## Dragon Soul Button
								{
									"name" : "DSSButton",
									"type" : "button",

									"x" : 117,
									"y" : 111,

									# "multi_text" : "Alchemia Smoczych Kamieni [ENTER] |Eemoticons/actions/key_rclick|e - Aktywacja Alchemii",
									"default_image" : "assets/ui/buttons/DS/dss_inventory_off_button_01.tga",
									"over_image" : "assets/ui/buttons/DS/dss_inventory_off_button_02.tga",
									"down_image" : "assets/ui/buttons/DS/dss_inventory_off_button_03.tga",
								},

								## MallButton
								{
									"name" : "MallButton",
									"type" : "button",

									"x" : 117,
									"y" : 146.5,

									"tooltip_text" : uiScriptLocale.INVENTORY_MENU_BTN_TEXT,

									"default_image" : "assets/ui/buttons/INV/BTN_MENU_NORMAL.png",
									"over_image" : "assets/ui/buttons/INV/BTN_MENU_HOVER.png",
									"down_image" : "assets/ui/buttons/INV/BTN_MENU_DOWN.png",
								},

							## CostumeButton
							{
								"name" : "CostumeButton",
								"type" : "button",

								"x" : 77,
								"y" : 5,

								"tooltip_text" : uiScriptLocale.COSTUME_WINDOW_TITLE,

								"default_image" : "d:/ymir work/ui/game/taskbar/costume_Button_01.tga",
								"over_image" : "d:/ymir work/ui/game/taskbar/costume_Button_02.tga",
								"down_image" : "d:/ymir work/ui/game/taskbar/costume_Button_03.tga",
							},

							),
						},

						{
							"name" : "Inventory_Tab_01",
							"type" : "radio_button",

							"x" : -int(float(BUTTON_TAB_COUNT_PER_LINE-1)/2 * BUTTON_TAB_SPACE),
							"y" : PAGE_TOP_DIST + 155,
							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "01"),
							"over_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "02"),
							"down_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "03"),

							"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP % 1,

							"children" :
							(
								{
									"name" : "Equipment_Tab_01_Print",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "I",
								},
							),
						},

						{
							"name" : "Inventory_Tab_02",
							"type" : "radio_button",

							"x" : -int(float(BUTTON_TAB_COUNT_PER_LINE-1)/2 * BUTTON_TAB_SPACE) + BUTTON_TAB_SPACE,
							"y" : PAGE_TOP_DIST + 155,
							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "01"),
							"over_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "02"),
							"down_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "03"),

							"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP % 2,

							"children" :
							(
								{
									"name" : "Equipment_Tab_02_Print",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "II",
								},
							),
						},

						{
							"name" : "Inventory_Tab_03",
							"type" : "radio_button",

							"x" : -int(float(BUTTON_TAB_COUNT_PER_LINE-1)/2 * BUTTON_TAB_SPACE) + BUTTON_TAB_SPACE * 2,
							"y" : PAGE_TOP_DIST + 155,
							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "01"),
							"over_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "02"),
							"down_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "03"),

							"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP % 3,

							"children" :
							(
								{
									"name" : "Equipment_Tab_03_Print",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "III",
								},
							),
						},

						{
							"name" : "Inventory_Tab_04",
							"type" : "radio_button",

							"x" : -int(float(BUTTON_TAB_COUNT_PER_LINE-1)/2 * BUTTON_TAB_SPACE) + BUTTON_TAB_SPACE * 3,
							"y" : PAGE_TOP_DIST + 155,
							"horizontal_align" : "center",

							"default_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "01"),
							"over_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "02"),
							"down_image" : "d:/ymir work/ui/game/windows/" + (SMALL_NAME % "03"),

							"tooltip_text" : uiScriptLocale.INVENTORY_PAGE_BUTTON_TOOLTIP % 4,

							"children" :
							(
								{
									"name" : "Equipment_Tab_04_Print",
									"type" : "text",

									"x" : 0,
									"y" : 0,

									"all_align" : "center",

									"text" : "IV",
								},
							),
						},
						
						## Item Slot
						{
							"name" : "ItemSlot",
							"type" : "grid_table",

							"x" : 5,
							"y" : PAGE_TOP_DIST + 155 + 20,

							"horizontal_align" : "center",

							"start_index" : 0,
							"x_count" : 5,
							"y_count" : 9,
							"x_step" : 32,
							"y_step" : 32,

							"image" : "d:/ymir work/ui/public/Slot_Base.sub"
						},
					],
				},
			),
		},
	),
}
