#-*- coding: iso-8859-1 -*-a
import uiScriptLocale
import introInterface
import ui

UI_ROOT = "d:/ymir work/ui/login/{}"

WRAPPER_MASK_WIDTH = 747
WRAPPER_MASK_HEIGHT = 389

WRAPPER_WIDTH = 681
WRAPPER_HEIGHT = 439

POP_WIDTH = 451
POP_HEIGHT = 172

IMAGE_WIDTH = introInterface.GetGlobalWindowSize("width")
IMAGE_HEIGHT = introInterface.GetGlobalWindowSize("height")

BACKGROUND_SCALE = float(SCREEN_HEIGHT) / float(IMAGE_HEIGHT)

if (BACKGROUND_SCALE * IMAGE_WIDTH) < SCREEN_WIDTH:
	BACKGROUND_SCALE = float(SCREEN_WIDTH) / IMAGE_WIDTH

FOOTER_WIDTH = introInterface.GetGlobalWindowSize("width")
FOOTER_HEIGHT = 217

FOOTER_SCALE = float(SCREEN_HEIGHT) / float(FOOTER_HEIGHT)

if (FOOTER_SCALE * FOOTER_WIDTH) < SCREEN_WIDTH:
	FOOTER_SCALE = float(SCREEN_WIDTH) / FOOTER_WIDTH

def Account(i):
	Y = (i * (31 + 5))

	return {
		"name" : "Account{}".format(i),
		"type" : "window",

		"x" : 0, "y" : 60 + Y,
		"horizontal_align" : "center",
		"width" : 175, "height" : 31,
		"children" : [
			{
				"name": "account_button_load_{}".format(i),
				"type": "button",

				"x": 0, "y": 0,

				"default_image": UI_ROOT.format("accounts/wrapper_0.png"),
				"over_image": UI_ROOT.format("accounts/wrapper_1.png"),
				"down_image": UI_ROOT.format("accounts/wrapper_1.png"),
				"disable_image": UI_ROOT.format("accounts/wrapper_1.png"),
				"children" : [
					{
						"name": "account_name_{}".format(i),
						"type": "text",
						"style": ("not_pick",),

						"x": 30, "y": -3,

						"horizontal_align": "left",
						"text_horizontal_align": "left",
						"vertical_align": "center",
						"text_vertical_align": "center",
					},
					{
						"name": "account_button_save_{}".format(i),
						"type": "button",

						"x": 25, "y": 0,

						"horizontal_align": "right",
						"vertical_align": "center",

						"default_image": UI_ROOT.format("accounts/save_norm.png"),
						"over_image": UI_ROOT.format("accounts/save_hover.png"),
						"down_image": UI_ROOT.format("accounts/save_down.png"),
					},
					{
						"name": "account_button_delete_{}".format(i),
						"type": "button",

						"x": 25, "y": 0,

						"horizontal_align": "right",
						"vertical_align": "center",

						"default_image": UI_ROOT.format("accounts/delete_norm.png"),
						"over_image": UI_ROOT.format("accounts/delete_hover.png"),
						"down_image": UI_ROOT.format("accounts/delete_down.png"),
					},
				],
			}
		],
	}

def Channel(i):
	Y = (i * (31 + 5))

	return {
		"name": "Channel{}".format(i),
		"type": "radio_button",

		"x" : 5, "y" : 60 + Y,
		"horizontal_align" : "center",

		"default_image": UI_ROOT.format("channels/ch{}.png".format(i + 1)),
		"over_image": UI_ROOT.format("channels/ch{}_hover.png".format(i + 1)),
		"down_image": UI_ROOT.format("channels/ch{}_hover.png".format(i + 1)),
		"disable_image": UI_ROOT.format("channels/ch{}_hover.png".format(i + 1)),

		"children": (

		)
	}

window = {
	"name" : "LoginWindow",
	"style" : ("attach", ),

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	[
		{
			"name" : "Background",
			"type" : "expanded_image",
			"style" : ["attach", "ltr",],

			"x" : (SCREEN_WIDTH - (IMAGE_WIDTH * BACKGROUND_SCALE)) / 2, "y" : 0,

			"x_scale" : BACKGROUND_SCALE, "y_scale" : BACKGROUND_SCALE,

			"image" : UI_ROOT.format("background.png"),
			"children" :
			[
				{
					"name" : "WrappersMask",
					"type" : "window",

					"x" : 0, "y" : (SCREEN_HEIGHT - WRAPPER_HEIGHT) / 2,
					"width" : WRAPPER_MASK_WIDTH, "height" : WRAPPER_MASK_HEIGHT,
					"horizontal_align" : "center",
					"children" : [
						## Wrapper Account
						{
							"name" : "WrapperAccount",
							"type" : "expanded_image",

							"x" : 0, "y" : 0,
							"horizontal_align" : "left", "vertical_align" : "center",
							"image" : UI_ROOT.format("wrapper_account.png"),
							"children" :
							[
								Account(0),
								Account(1),
								Account(2),
								Account(3),
								Account(4),
								Account(5),
							],
						},

						## Wrapper Channel
						{
							"name" : "WrapperChannel",
							"type" : "expanded_image",

							"x" : 232, "y" : 0,
							"horizontal_align" : "right", "vertical_align" : "center",
							"image" : UI_ROOT.format("wrapper_channel.png"),
							"children" :
							[
								Channel(0),
								Channel(1),
								Channel(2),
								Channel(3),
								Channel(4),
								Channel(5),
							],
						},

						## Wrapper Main
						{
							"name" : "WrapperMain",
							"type" : "expanded_image",
							"style" : ["attach",],

							"x" : 0, "y" : 0,
							"horizontal_align" : "center", "vertical_align" : "center",
							"image" : UI_ROOT.format("wrapper_main.png"),
							"children" :
							[
								##LInput
								{
									"name" : "LInput",
									"type" : "expanded_image",

									"x" : 0, "y" : 130,
									"horizontal_align" : "center",
									"image" : UI_ROOT.format("input_0.png"),
									"children" :
									[
										{ "name" : "ID_EditLine", "type" : "editline", "x": 40, "y": 10, "width": 218, "height": 42,
											"input_limit": introInterface.GetWindowConfig("lenght_data", "loginid"), "enable_codepage": 0, "color": 0xFFffffff, "fontname" : "Tahoma:14",
										},
									],
								},

								##PInput
								{
									"name" : "PInput",
									"type" : "expanded_image",

									"x" : 0, "y" : 165,
									"horizontal_align" : "center",
									"image" : UI_ROOT.format("input_1.png"),
									"children" :
									[
										{ "name" : "PWD_EditLine", "type" : "editline", "x": 40, "y": 10, "width": 218, "height": 42,
											"input_limit": introInterface.GetWindowConfig("lenght_data", "passwd"), "secret_flag": True, "enable_codepage": 0, "color": 0xFFffffff, "fontname" : "Tahoma:14"
										},
									],
								},

								##PIInput
								{
									"name" : "PIInput",
									"type" : "expanded_image",

									"x" : 0, "y" : 200,
									"horizontal_align" : "center",
									"image" : UI_ROOT.format("input_1.png"),
									"children" :
									[
										{ "name" : "PIN_EditLine", "type" : "editline", "x": 40, "y": 10, "width": 218, "height": 42,
											"input_limit": introInterface.GetWindowConfig("lenght_data", "passwd"), "secret_flag": True, "enable_codepage": 0, "color": 0xFFffffff, "fontname" : "Tahoma:14"
										},
									],
								},

								##Remembe
								{
									"name" : "Remember",
									"type" : "checkbox",

									"x" : 85, "y" : 240,

									"new" : True,
									"text" : "Remember my login details",
									"text_color" : 0xFF3D3938,

									"sPath" : "assets/ui/login/checkbox_{}",
									"sUnselected" : "unselected.tga",
									"sSelected" : "selected.tga",
								},

								{
									"name" : "LoginButton",
									"type" : "button",

									"x" : 0 / 2, "y" : 270,
									"horizontal_align" : "center",

									"images" : ((UI_ROOT.format("sign_in_0.png"), UI_ROOT.format("sign_in_1.png"), UI_ROOT.format("sign_in_1.png"))),
								},

								{
									"name" : "RecoveryPassword",
									"type" : "selectable_text",

									"x" : 0, "y" : 325,
									"horizontal_align" : "center",
									"colors" : (0xFF3D3938, 0xFFfb824e, 0xFF885945),

									"text" : uiScriptLocale.LOGIN_WINDOW_RECOVERY,
								},
							],
						},
					],
				},

				# Language Space
				{
					"name" : "LanguageSpace",
					"type" : "window",
					"style" : ["attach",],

					"x" : 1.5,
					"y" : 424,

					"width" : 680,
					"height" : 66,
					"children" :
					[

					],
				},
			],
		},
	],
}

# if SCREEN_HEIGHT >= 900:
# 	window["children"][0]["children"] += {
# 		"name" : "Logo",
# 		"type" : "image",
# 		"style" : ["not_pick",],

# 		"x" : -330,
# 		"y" : window["children"][0]["children"][0]["y"] - 220,

# 		"horizontal_align" : "center",

# 		"image" : UI_ROOT.format("logo.png"),
# 	},

