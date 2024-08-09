#-*- coding: iso-8859-1 -*-a
import uiScriptLocale
import introInterface
import ui

UI_ROOT = "assets/ui/login/{}"

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
					"name" : "Wrapper",
					"type" : "expanded_image",
					"style" : ["attach",],

					"x" : 0, "y" : (SCREEN_HEIGHT - WRAPPER_HEIGHT) / 2,
					"horizontal_align" : "center",
					"image" : UI_ROOT.format("wrapper.png"),
					"children" :
					[
						## Channel Space
						{
							"name" : "ChannelSpace",
							"type" : "window",
							"style" : ["attach",],

							"x" : 28, "y" : 63,

							"width" : 278, "height" : 40,
							"color" : 0xFFfffff,
							"children" :
							[

							],
						},

						## Login Space
						{
							"name" : "LoginSpace",
							"type" : "window",
							"style" : ["attach",],

							"x" : 0, "y" : 103,

							"width" : 333, "height" : 310,
							"children" :
							[
								##LInput
								{
									"name" : "LInput",
									"type" : "button",

									"x" : 0, "y" : 40,
									"horizontal_align" : "center",
									"images" : (UI_ROOT.format("login_input_0.png"), UI_ROOT.format("login_input_1.png"), UI_ROOT.format("login_input_1.png")),
									"children" :
									[
										{ "name" : "ID_EditLine", "style": ("not_pick",), "type" : "editline", "x": 10, "y": 15, "width": 218, "height": 42,
											"input_limit": introInterface.GetWindowConfig("lenght_data", "loginid"), "enable_codepage": 0, "color": 0xFFffffff, "fontname" : "Tahoma:14",
										},
									],
								},

								##PInput
								{
									"name" : "PInput",
									"type" : "button",

									"x" : 0, "y" : 106,
									"horizontal_align" : "center",
									"images" : ((UI_ROOT.format("password_input_0.png"), UI_ROOT.format("password_input_1.png"), UI_ROOT.format("password_input_1.png"))),
									"children" :
									[
										{ "name" : "PWD_EditLine", "style": ("not_pick",), "type" : "editline", "x": 10, "y": 15, "width": 218, "height": 42,
											"input_limit": introInterface.GetWindowConfig("lenght_data", "passwd"), "secret_flag": True, "enable_codepage": 0, "color": 0xFFffffff, "fontname" : "Tahoma:14"
										},
									],
								},

								##Remembe
								{
									"name" : "Remember",
									"type" : "checkbox",

									"x" : 19, "y" : 157,

									"new" : True,
									"text" : uiScriptLocale.LOGIN_WINDOW_REMEMBER,
									"text_color" : 0xFFffffff,

									"sPath" : "assets/ui/login/checkbox_{}",
									"sUnselected" : "unselected.tga",
									"sSelected" : "selected.tga",
								},

								{
									"name" : "LoginButton",
									"type" : "button",

									"x" : 27, "y" : 198,

									"images" : ((UI_ROOT.format("sign_in_0.png"), UI_ROOT.format("sign_in_1.png"), UI_ROOT.format("sign_in_2.png"))),
								},

								{
									"name" : "ExitButton",
									"type" : "button",

									"x" : 202, "y" : 255,

									"images" : ((UI_ROOT.format("exit_game_0.png"), UI_ROOT.format("exit_game_1.png"), UI_ROOT.format("exit_game_2.png"))),
								},

								{
									"name" : "RecoveryPassword",
									"type" : "selectable_text",

									"x" : 19, "y" : 270,
									"colors" : (0xFFffffff, 0xFFfb824e, 0xFF885945),

									"text" : uiScriptLocale.LOGIN_WINDOW_RECOVERY,
								},
							],
						},

						## News Space
						{
							"name" : "NewsSpace",
							"type" : "window",
							"style" : ["attach",],

							"x" : 348, "y" : 3,
							"width" : 290, "height" : 40,
 
							"color" : 0xFFf21cff,
							# "horizontal_align" : "right",

							"children" :
							[
								{
									"name" : "NewsHeader",
									"type" : "text",

									"x" : 10, "y" : -2,
									"text_vertical_align" : "center",
									"vertical_align" : "center",
									"fontname" : "Tahoma:12",
									"color" : 0xFFcc7954,
									"text" : "Important news:",
								},

								{
									"name" : "render_window",
									"type" : "window",
									"style" : ("attach",),
									
									"x" : 87, "y" : 0,
									"width" : 220, "height" : 15,
									"vertical_align" : "center",
									
									"children" :
									[
										{
											"name" : "advise_text",
											"type" : "text",
											
											"x" : 0, "y" : -1,
											"text_vertical_align" : "center",
											"vertical_align" : "center",
											"color" : 0xFFffffff,
											"fontname" : "Tahoma:12",

											"text" : "We’re having a issues with the login...",
										}
									],
								}
							],
						},

						# Accounts Space
						{
							"name" : "AccountsSpace",
							"type" : "window",
							"style" : ["attach",],

							"x" : 348,
							"y" : 54,

							"width" : 333,
							"height" : 362,
							"children" :
							[

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
		},

		{
			"name" : "PopUpBar",
			"type" : "bar",

			"x" : 0, "y" : 0,

			"width" : SCREEN_WIDTH, "height" : SCREEN_HEIGHT,

			"color" : 0x70000000,
			"children" :
			[
				{
					"name" : "PopUpLogIn",
					"type" : "image",

					"x" : (SCREEN_WIDTH - POP_WIDTH) / 2, "y" : (SCREEN_HEIGHT - POP_HEIGHT) / 2,

					"image" : UI_ROOT.format("popup/background.png"),
					"children" :
					[
						{
							"name" : "PopUpText",
							"type" : "multi_text",

							"x" : 0, "y" : 35,
							"fontname" : "Tahoma:16b",
							"color" : 0xff7899ad,
							"width" : 260,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",
							"text_vertical_align" : "center",
							"text" : "Incorrect Login/Password",
						},

						{
							"name" : "PopUpAnimation_1",
							"type" : "image",

							"x" : 175, "y" : 73,

							"image" : UI_ROOT.format("popup/state_connecting.png"),
						},

						{
							"name" : "PopUpAnimation_2",
							"type" : "image",

							"x" : 211, "y" : 73,

							"image" : UI_ROOT.format("popup/state_connecting.png"),
						},

						{
							"name" : "PopUpAnimation_3",
							"type" : "image",

							"x" : 246, "y" : 73,

							"image" : UI_ROOT.format("popup/state_connecting.png"),
						},

						{
							"name" : "PopUpButton",
							"type" : "button",

							"x" : 0, "y" : 125,

							"width" : 107,
							"height" : 30,
							"horizontal_align" : "center",
							"images" : ((UI_ROOT.format("popup/button_0.png"), UI_ROOT.format("popup/button_1.png"),  UI_ROOT.format("popup/button_2.png"))),
							"text" : "Ok",
							"text_height" : 2,
						},
					],
				},
			],
		},
	],
}

for i in range(len(introInterface.GetWindowConfig("connection_info", introInterface.DEFAULT_SERVER, "server"))):
	window["children"][0]["children"][0]["children"][0]["children"] += {
		"name": "Channel{}".format(i),
		"type": "radio_button",

		"x": 0 + ((6 + 41) * i), "y" : 0,
		"vertical_align" : "center",

		"images" : ((UI_ROOT.format("channels/button_channel_0.png"), UI_ROOT.format("channels/button_channel_1.png"), UI_ROOT.format("channels/button_channel_2.png"))),
		"children" :
		[
			{
				"name" : "ChannelID",
				"type" : "text",

				"x" : 0, "y" : -3,
				"horizontal_align" : "center",
				"vertical_align" : "center",
				"text_vertical_align" : "center",
				"text_horizontal_align" : "center",

				"fontname" : "Arial:14",
				"text" : "CH{}".format(i + 1),
			},
		],
	},

for i in range(introInterface.GetWindowConfig("lenght_data", "account")):
	y = (i * (12 + 39))
	window["children"][0]["children"][0]["children"][3]["children"] += {
		"name" : "Account{}".format(i),
		"type" : "window",
		"style" : ["float",],

		"x" : 0, "y" : 83 + y,

		"width" : 292, "height" : 39,

		"horizontal_align" : "center",

		"children" :
		[
			{
				"name" : "account_button_{}".format(i), "type" : "image",
				"style" : ["float",],
				"x" : 0, "y" : 0,

				"image" : UI_ROOT.format("accounts/wrapper.png"),
				"children" :
				[
					{
						"name" : "account_id",
						"type" : "text",

						"x" : 13, "y" : 13,
						"fontname" : "Tahoma:11",
						"text" : "F{}".format(i + 1),
					},

					{
						"name" : "account_name_{}".format(i),
						"type" : "text",

						"x" : 52, "y" : 13,
						"fontname" : "Tahoma:11",
						"color" : 0xFFfc9162,
						"text" : "",
					},

					{
						"name" : "account_button_save_{}".format(i), "type" : "button",
						"x" : 4 + 29, "y" : 0,
						"horizontal_align" : "right",
						"vertical_align" : "center",

						"images" : ((UI_ROOT.format("accounts/button_save_0.png"), UI_ROOT.format("accounts/button_save_1.png"), UI_ROOT.format("accounts/button_save_2.png")))
					},

					{
						"name" : "account_button_delete_{}".format(i), "type" : "button",
						"x" : 4 + 29, "y" : 0,
						"horizontal_align" : "right",
						"vertical_align" : "center",

						"images" : ((UI_ROOT.format("accounts/button_delete_0.png"), UI_ROOT.format("accounts/button_delete_1.png"), UI_ROOT.format("accounts/button_delete_2.png")))
					},

					{
						"name" : "account_button_load_{}".format(i), "type" : "button",
						"x" : (4 + 29) * 2, "y" : 0,
						"horizontal_align" : "right",
						"vertical_align" : "center",

						"images" : ((UI_ROOT.format("accounts/button_load_0.png"), UI_ROOT.format("accounts/button_load_1.png"), UI_ROOT.format("accounts/button_load_2.png")))
					},
				],
			},
		],
	},

if SCREEN_HEIGHT >= 900:
	window["children"][0]["children"] += {
		"name" : "Logo",
		"type" : "image",
		"style" : ["not_pick",],

		"x" : -330,
		"y" : window["children"][0]["children"][0]["y"] - 220,

		"horizontal_align" : "center",

		"image" : UI_ROOT.format("logo.png"),
	},

