import uiScriptLocale

ROOT_PATH = "assets/ui/maintenance/{}"

window = {
	"name" : "MaintenanceAlert",

	"x" : 0,
	"y" : SCREEN_HEIGHT - 80,

	"style" : ("float", "animate", ),

	"width" : 349,
	"height" : 46,

	"children" :
	(
		## Board
		{
			"name" : "Board",
			"style" : ("attach",),
			"type" : "expanded_image",

			"x" : 0,
			"y" : 0,

			"image" : ROOT_PATH.format("background.png"),

			"children" :
			(
				## Start Time - Text
				{
					"name" : "Start_Time_Text",
					"type" : "text",

					"x" : 50,
					"y" : 10,

					"text_horizontal_align" : "left",
					"color" : 0xFFb5a676,

					"text" : "",
				},

				## Reason - Text
				{
					"name" : "Reason_Text",
					"type" : "text",

					"x" : 50,
					"y" : 20,

					# "horizontal_align" : "center",
					"text_horizontal_align" : "left",
					"color" : 0xFFb5a676,

					"text" : "",
				},

				## Changelog
				{
					"name" : "Changelog_Space",

					"x" : 80,
					"y" : 10,

					"width" : 80,
					"height" : 20,

					"horizontal_align" : "right",
					"children" :
					[
						{
							"name" : "ChangelogText",
							"type" : "text",

							"x" : 0,
							"y" : 0,

							# "all_align" : "center",

							"text" : uiScriptLocale.TECHNICAL_MAINTENANCE_CHANGELOG,
							"color" : 0xFF968674,
						},

						{
							"name" : "Changelog_Button",
							"type" : "button",

							"x" : 30,
							"y" : 0,

							"horizontal_align" : "right",
							"default_image" : ROOT_PATH.format("button_0.png"),
							"over_image" : ROOT_PATH.format("button_1.png"),
							"down_image" : ROOT_PATH.format("button_2.png"),
						},
					],
				}
			),
		},
	),
}