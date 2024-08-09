#-*- coding: iso-8859-1 -*-a
import localeInfo

window = {
	"name" : "QuestionCopyBonusDialog",
	"style" : ("movable", "float",),

	"x" : SCREEN_WIDTH/2 - 130,
	"y" : SCREEN_HEIGHT/2 - 52,

	"width" : 260,
	"height" : 115,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",

			"x" : 0,
			"y" : 0,

			"width" : 260,
			"height" : 115,

			"children" :
			(
				{
					"name" : "message1",
					"type" : "text",

					"x" : 0,
					"y" : 20,

					"horizontal_align" : "center",
					"text" : "-",

					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "message2",
					"type" : "text",

					"x" : 0,
					"y" : 40,

					"horizontal_align" : "center",
					"text" : "-",

					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},

				{
					"name" : "message3",
					"type" : "text",

					"x" : 0,
					"y" : 60,

					"horizontal_align" : "center",
					"text" : "Czy chcesz kontynowaæ?",

					"text_horizontal_align" : "center",
					"text_vertical_align" : "center",
				},
				{
					"name" : "accept",
					"type" : "button",

					"x" : -40,
					"y" : 80,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					"default_image" : "d:/ymir work/ui/public/acceptbutton00.sub",
					"over_image" : "d:/ymir work/ui/public/acceptbutton01.sub",
					"down_image" : "d:/ymir work/ui/public/acceptbutton02.sub",
				},
				{
					"name" : "cancel",
					"type" : "button",

					"x" : 40,
					"y" : 80,

					"width" : 61,
					"height" : 21,

					"horizontal_align" : "center",
					"default_image" : "d:/ymir work/ui/public/canclebutton00.sub",
					"over_image" : "d:/ymir work/ui/public/canclebutton01.sub",
					"down_image" : "d:/ymir work/ui/public/canclebutton02.sub",
				},
				{
					"name" : "FromSlot",
					"type" : "slot",

					"x" : 8,
					"y" : 9,

					"width" : 32,
					"height" : 200,

					"horizontal_align" : "left",

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",

					"slot" : (
						{"index":0, "x":0, "y":0, "width":32, "height":32},
						{"index":1, "x":0, "y":33, "width":32, "height":32},
						{"index":2, "x":0, "y":66, "width":32, "height":32},
					),
				},

				{
					"name" : "ToSlot",
					"type" : "slot",

					"x" : 32 + 8,
					"y" : 9,

					"width" : 32,
					"height" : 200,

					"horizontal_align" : "right",

					"image" : "d:/ymir work/ui/public/Slot_Base.sub",

					"slot" : (
						{"index":0, "x":0, "y":0, "width":32, "height":32},
						{"index":1, "x":0, "y":33, "width":32, "height":32},
						{"index":2, "x":0, "y":66, "width":32, "height":32},
					),
				},
			),
		},
	),
}