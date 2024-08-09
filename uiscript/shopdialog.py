import uiScriptLocale
import app

BOARD_WIDTH = 200
BOARD_HEIGHT = 380

PAGE_LEFT_X_DIST = 10
PAGE_RIGHT_X_DIST = 10
PAGE_X_DIST = PAGE_LEFT_X_DIST + PAGE_RIGHT_X_DIST

PAGE_TOP_DIST = 33
PAGE_BOT_DIST = 10

window = {
	"name" : "ShopDialog",

	"x" : SCREEN_WIDTH - 400,
	"y" : 10,

	"style" : ("movable", "float", "animate",),

	"width" : BOARD_WIDTH,
	"height" : BOARD_HEIGHT,

	"children" :
	[
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : BOARD_WIDTH,
			"height" : BOARD_HEIGHT,

			"title" : uiScriptLocale.SHOP_TITLE,

			"children" :
			[
				{
					"name" : "ThinBoard",
					"type" : "thinboard",

					"x" : PAGE_LEFT_X_DIST,
					"y" : PAGE_TOP_DIST,

					"width" : BOARD_WIDTH - PAGE_X_DIST,
					"height" : BOARD_HEIGHT - (PAGE_TOP_DIST + PAGE_BOT_DIST),
					"children" :
					[
						## Item Slot
						{
							"name" : "ItemSlot",
							"type" : "grid_table",

							"x" : PAGE_LEFT_X_DIST,
							"y" : PAGE_BOT_DIST + 30,

							"start_index" : 0,
							"x_count" : 5,
							"y_count" : 8,
							"x_step" : 32,
							"y_step" : 32,

							"image" : "d:/ymir work/ui/public/Slot_Base.sub",
						},

						## Buy
						{
							"name" : "BuyButton",
							"type" : "toggle_button",

							"x" : PAGE_LEFT_X_DIST,
							"y" : PAGE_BOT_DIST + 32 * 8 + PAGE_BOT_DIST + 30,

							"horizontal_align" : "left",

							"text" : uiScriptLocale.SHOP_BUY,

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},

						## Sell
						{
							"name" : "SellButton",
							"type" : "toggle_button",

							"x" : 94,
							"y" : 295,

							"x" : PAGE_LEFT_X_DIST + 61,
							"y" : PAGE_BOT_DIST + 32 * 8 + PAGE_BOT_DIST + 30,

							"horizontal_align" : "right",

							"text" : uiScriptLocale.SHOP_SELL,

							"default_image" : "d:/ymir work/ui/public/middle_button_01.sub",
							"over_image" : "d:/ymir work/ui/public/middle_button_02.sub",
							"down_image" : "d:/ymir work/ui/public/middle_button_03.sub",
						},
					],
				},

				## Close
				{
					"name" : "CloseButton",
					"type" : "button",

					"x" : 0,
					"y" : 295,

					"horizontal_align" : "center",

					"text" : uiScriptLocale.PRIVATE_SHOP_CLOSE_BUTTON,

					"default_image" : "d:/ymir work/ui/public/large_button_01.sub",
					"over_image" : "d:/ymir work/ui/public/large_button_02.sub",
					"down_image" : "d:/ymir work/ui/public/large_button_03.sub",
				},
			],
		},
	],
}
if app.ENABLE_RENEWAL_SHOP_SELLING:
	RENEWAL_HEIGHT = 80
	RENEWAL_SPACE_HEIGHT = 20

	window["height"] = window["height"] + RENEWAL_HEIGHT
	window["children"][0]["height"] = window["children"][0]["height"] + RENEWAL_HEIGHT
	window["children"][0]["children"][0]["height"] = window["children"][0]["children"][0]["height"] + RENEWAL_HEIGHT
	window["children"][0]["children"][0]["children"] += [
		{
			"name" : "InformationItems",
			"type" : "field",


			"x" : 0,
			"y" : RENEWAL_HEIGHT,

			"width" : 168,
			"height" : 18,

			"horizontal_align" : "center",
			"vertical_align" : "bottom",

			"children" :
			(
				{
					"name" : "selected_text",
					"type" : "text",

					"x" : 0,
					"y" : -1,

					"text" : "0",
					"all_align" : True,
				},
			),
		},

		{
			"name" : "SellingInformation",
			"type" : "field",


			"x" : 0,
			"y" : RENEWAL_HEIGHT - RENEWAL_SPACE_HEIGHT,

			"width" : 168,
			"height" : 18,

			"horizontal_align" : "center",
			"vertical_align" : "bottom",

			"children" :
			(
				{
					"name" : "total_money_text",
					"type" : "text",

					"x" : 0,
					"y" : -1,

					"text" : "0",
					"all_align" : True,
				},
			),
		},

		{
			"name" : "sell_button",
			"type" : "button",

			"x" : PAGE_LEFT_X_DIST,
			"y" : (RENEWAL_HEIGHT - RENEWAL_SPACE_HEIGHT) / 2,

			"vertical_align" : "bottom",

			"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
			"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
			"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
		},

		{
			"name" : "cancel_button",
			"type" : "button",

			"x" : PAGE_LEFT_X_DIST + 61,
			"y" : (RENEWAL_HEIGHT - RENEWAL_SPACE_HEIGHT) / 2,

			"horizontal_align" : "right",
			"vertical_align" : "bottom",

			"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
			"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
			"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
		},
	]