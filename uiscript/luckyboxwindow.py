import localeInfo

WINDOW_WIDTH = 285
WINDOW_HEIGHT = 215

ROOT_PATH = "d:/ymir work/ui/game/lucky_box/"

window = {
	"name" : "DungeonListWindow",

	"x" : 0,
	"y" : 0,

	"style" : ("attach", "float", "animate",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children":
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"children" :
			(
				## Title
				{
					"name" : "TitleBar",
					"type" : "titlebar",
					"style" : ("attach",),

					"x" : 8,
					"y" : 7,

					"width" : WINDOW_WIDTH - 15,
					"color" : "yellow",

					"children" :
					(
						{
							"name" : "TitleName",
							"type" : "text",

							"x" : (WINDOW_WIDTH - 15) / 2,
							"y" : 3,

							"text" : localeInfo.LUCKY_BOX_TITLE,
							"text_horizontal_align":"center"
						},
					),
				},

				{
					"name" : "SlotImage",
					"type" : "image",

					"x" : 20,
					"y" : 45,

					"image" : ROOT_PATH + "lucky_box_slot.tga",

					"children" :
					(
						{
							"name" : "ItemImage",
							"type" : "image",

							"x" : 4,
							"y" : 4,

							"image" : "icon/item/72734.tga",
						},
					),
				},
				{
					"name" : "RefreshButton",
					"type" : "button",

					"x" : 87,
					"y" : 40,

					"text" : localeInfo.REFRESH_PRIZE,

					"default_image" : ROOT_PATH + "lucky_button_01.tga",
					"over_image" : ROOT_PATH + "lucky_button_02.tga",
					"down_image" : ROOT_PATH + "lucky_button_03.tga",
					"disable_image" : ROOT_PATH + "lucky_button_03.tga",
				},
				{
					"name" : "PriceInput",
					"type" : "input",

					"x" : 85,
					"y" : 69,

					"width" : 152,

					"children" :
					(
						{
							"name" : "PriceBox",
							"type" : "bar",

							"x" : 1,
							"y" : 1,

							"width" : 33,
							"height" : 19,

							"color" : 0xFF282828,
						},
						{
							"name" : "PriceName",
							"type" : "text",

							"x" : 5,
							"y" : 4,

							"text" : localeInfo.LUCKY_PRICE,
						},
						{
							"name" : "PriceValue",
							"type" : "text",

							"x" : 5,
							"y" : 4,

							"text_horizontal_align" : "right",
							"horizontal_align" : "right",

							"text" : "999.999.999 Yang",
						},
					),
				},
				{
					"name" : "BorderA",
					"type" : "border_a",

					"x" : 10,
					"y" : 100,

					"width" : 264,
					"height" : 72,

					"children" :
					(
						{
							"name" : "ItemSluts", # =)) =) for who stelling uiscript part
							"type" : "grid_table",

							"x" : 4,
							"y" : 4,

							"start_index" : 0,
							"x_count" : 8,
							"y_count" : 2,
							"x_step" : 32,
							"y_step" : 32,

							"image" : "d:/ymir work/ui/public/Slot_Base.sub",
						},
					),
				},
				{
					"name" : "KeepButton",
					"type" : "button",

					"x" : 75,
					"y" : 180,

					"text" : localeInfo.KEEP_PRIZE,

					"default_image" : ROOT_PATH + "lucky_button_01.tga",
					"over_image" : ROOT_PATH + "lucky_button_02.tga",
					"down_image" : ROOT_PATH + "lucky_button_03.tga",
				},
				{
					"name" : "RewardEffect",
					"type" : "ani_image",

					"style" : ("not_pick",),

					"x" : 14,
					"y" : 104,

					"delay" : 9,

					"images":
					(
						ROOT_PATH + "effect/1.tga",
						ROOT_PATH + "effect/2.tga",
						ROOT_PATH + "effect/3.tga",
						ROOT_PATH + "effect/4.tga",
						ROOT_PATH + "effect/5.tga",
						ROOT_PATH + "effect/6.tga",
					),
				},
			),
		},
	),
}

