import uiScriptLocale
import item

BOARD_WIDTH = 171
BOARD_HEIGHT = 235

def AppendLockSlot(sKey, iPosX, iPosY):
	return {
		"name" : "CostumeLockSlot_{}".format(sKey),
		"type" : "image",

		"x" : iPosX, "y" : iPosY,
		"image" : "assets/ui/elements/locked_slot/big.dds",
	}

window = {
	"name" : "CostumeWindow",

	"x" : SCREEN_WIDTH - BOARD_WIDTH,
	"y" : SCREEN_HEIGHT - 37 - 565,

	"style" : ("movable", "float",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	(
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
						{ "name":"TitleName", "type":"text", "x":0, "y":-1, "all_align" : True, "text": uiScriptLocale.COSTUME_WINDOW_TITLE, "text_horizontal_align":"center" },
					),
				},

				## Equipment Slot
				{
					"name" : "Costume_Base",
					"type" : "image",

					"x" : 0,
					"y" : 36,

					"image" : "assets/ui/inventory/equipment_costume.png",
					"horizontal_align" : "center",

					"children" :
					(

						{
							"name" : "CostumeSlot",
							"type" : "slot",

							"x" : 3,
							"y" : 3,

							"width" : 150,
							"height" : 182,

							"slot" : (
										{"index":item.COSTUME_SLOT_HAIR, "x":59, "y":37, "width":32, "height":32},
										{"index":item.COSTUME_SLOT_BODY, "x":58, "y":78, "width":32, "height":32},
										{"index":item.COSTUME_SLOT_WEAPON, "x":10, "y":62, "width":32, "height":96},

										{"index":item.COSTUME_SLOT_SASH, "x":10, "y":22, "width":32, "height":32},

										# {"index":item.COSTUME_SLOT_RING_1, 	"x":110,	"y":22, "width":32, "height":32},
										# {"index":item.COSTUME_SLOT_RING_2, 	"x":110,	"y":22 + 37 * 1, "width":32, "height":32},

										{"index":item.COSTUME_SLOT_MOUNT, "x":110, "y":22 + 37 * 2, "width":32, "height":32},
										{"index":item.COSTUME_SLOT_PET, "x":110, "y":22 + 37 * 3, "width":32, "height":32},
									),
						},
						AppendLockSlot("RING_1", 113, 27),
						AppendLockSlot("RING_2", 113, 27 + 37),
					),
				},
			),
		},
	),
}
