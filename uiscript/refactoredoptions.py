import uiScriptLocale

ROOT = "d:/ymir work/ui/public/"

MAIN = "d:/ymir work/ui/game/refactored_options/"

PAGINATION = "d:/ymir work/ui/pagination/"

ROOT_PATH = "assets/ui/options_window/{}"

Channel_ButtonGroupCounter = 0
def Channel_GetButtonGroup(inc = False):
	global Channel_ButtonGroupCounter

	if inc:
		Channel_ButtonGroupCounter += 1
	return Channel_ButtonGroupCounter

BOARD_WIDTH = 570
BOARD_HEIGHT = 370

THINBOARD_HEIGHT = 302
THINBOARD_MAIN_HEIGHT = 282 - 20

def AppendHeader(sKey, iFillY = 0):
	return {
		"name" : "OptionHeader-Image_{}".format(sKey),
		"type" : "expanded_image",

		"x" : 0, "y" : iFillY,
		"all_align" : True,

		"image" : ROOT_PATH.format("header_image.png"),
		"children" : (
			{
				"name" : "OptionHedaer-Text_{}".format(sKey),
				"type" : "text",

				"x" : 0, "y" : -1,
				"all_align" : True,
				"text" : sKey,
			},
		),
	}

window = {
	"name" : "MainOptions",
	# "style" : ("movable", "float", "animate",),
	"style" : ("movable", "float", ),

	"x" : (SCREEN_WIDTH  - BOARD_WIDTH) /2,
	"y" : (SCREEN_HEIGHT - BOARD_HEIGHT) /2,

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

			"title" : uiScriptLocale.GAME_REFACTORED_OPTIONS_TITLE,

			"children" :
			(
				{
					"name" : "MullChannels",
					"x" : 403,
					"y" : 38,

					"width" : 155,
					"height" : 23,
					"children" : [
						{
							"name" : "Channel_Text",
							"type" : "text",

							"x" : -80,
							"y" : 3,

							"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_CHANNELS,

							"horizontal_align" : "center",
							"text_horizontal_align" : "center",
						},

						{
							"name" : "Channel_%d" % Channel_GetButtonGroup(True),
							"type" : "button",

							"x" : 25,
							"y" : 0,

							"text" : "%d" % Channel_GetButtonGroup(),
							"default_image" :  ROOT_PATH.format("btn_channel_0.png"),
							"over_image" 	:  ROOT_PATH.format("btn_channel_1.png"),
							"down_image" 	:  ROOT_PATH.format("btn_channel_2.png"),
							"disable_image" :  ROOT_PATH.format("btn_channel_2.png"),
						},

						{
							"name" : "Channel_%d" % Channel_GetButtonGroup(True),
							"type" : "button",

							"x" : 25 + 26,
							"y" : 0,

							"text" : "%d" % Channel_GetButtonGroup(),
							"default_image" :  ROOT_PATH.format("btn_channel_0.png"),
							"over_image" 	:  ROOT_PATH.format("btn_channel_1.png"),
							"down_image" 	:  ROOT_PATH.format("btn_channel_2.png"),
							"disable_image" :  ROOT_PATH.format("btn_channel_2.png"),
						},

						{
							"name" : "Channel_%d" % Channel_GetButtonGroup(True),
							"type" : "button",

							"x" : 25 + 26 * 2,
							"y" : 0,

							"text" : "%d" % Channel_GetButtonGroup(),
							"default_image" :  ROOT_PATH.format("btn_channel_0.png"),
							"over_image" 	:  ROOT_PATH.format("btn_channel_1.png"),
							"down_image" 	:  ROOT_PATH.format("btn_channel_2.png"),
							"disable_image" :  ROOT_PATH.format("btn_channel_2.png"),
						},

						{
							"name" : "Channel_%d" % Channel_GetButtonGroup(True),
							"type" : "button",

							"x" : 25 + 26 * 3,
							"y" : 0,

							"text" : "%d" % Channel_GetButtonGroup(),
							"default_image" :  ROOT_PATH.format("btn_channel_0.png"),
							"over_image" 	:  ROOT_PATH.format("btn_channel_1.png"),
							"down_image" 	:  ROOT_PATH.format("btn_channel_2.png"),
							"disable_image" :  ROOT_PATH.format("btn_channel_2.png"),
						},

						{
							"name" : "Channel_%d" % Channel_GetButtonGroup(True),
							"type" : "button",

							"x" : 25 + 26 * 4,
							"y" : 0,

							"text" : "%d" % Channel_GetButtonGroup(),
							"default_image" :  ROOT_PATH.format("btn_channel_0.png"),
							"over_image" 	:  ROOT_PATH.format("btn_channel_1.png"),
							"down_image" 	:  ROOT_PATH.format("btn_channel_2.png"),
							"disable_image" :  ROOT_PATH.format("btn_channel_2.png"),
						},
					],
				},

				{
					"name" : "Button_Page_0",
					"type" : "button",

					"x" : 22,
					"y" : 38,

					"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_PAGE_00,
					"default_image" :  ROOT_PATH.format("cattegory_button_0.png"),
					"over_image" 	:  ROOT_PATH.format("cattegory_button_1.png"),
					"down_image" 	:  ROOT_PATH.format("cattegory_button_1.png"),
					"disable_image" :  ROOT_PATH.format("cattegory_button_1.png"),
				},

				{
					"name" : "Button_Page_1",
					"type" : "button",

					"x" : 22 + 122,
					"y" : 38,

					"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_PAGE_01,
					"default_image" :  ROOT_PATH.format("cattegory_button_0.png"),
					"over_image" 	:  ROOT_PATH.format("cattegory_button_1.png"),
					"down_image" 	:  ROOT_PATH.format("cattegory_button_1.png"),
					"disable_image" :  ROOT_PATH.format("cattegory_button_1.png"),
				},

				{
					"name" : "Page_0",
					"type" : "main_sub_board",

					"x" : 10,
					"y" : 60,

					"width" : 548,
					"height" : THINBOARD_HEIGHT,

					"full_opacity" : True,
					"children" : (
						{
							"name" : "SubPage_0",
							"type" : "expanded_image",

							"x" : 10,
							"y" : 10,

							"image" : ROOT_PATH.format("content_bg.png"),
							"children" : [
								{
									"name" : "AudioSettings_Text",
									"type" : "text",

									"x" : 0,
									"y" : 7,

									"text_horizontal_align" : "center",
									"horizontal_align" : "center",

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SUB_TITLE_00,
									"color" : 0xFFb19d58,
								},

								{
									"name" : "SeparateLine",
									"type" : "line",

									"x" : 1,
									"y" : 27,

									"width" : 163,
									"height" : 0,

									"color" : 0xff545454,
								},

								{
									"name" : "SelectMusicButton",
									"type" : "button",

									"x" : 0, "y" : 45,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectMusic_Text",
											"type" : "text",

											"x" : 0,
											"y" : -18,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_MUSIC,
										},
										# AppendHeader(uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_MUSIC, -23),
									],
								},

								{
									"name" : "MusicVolumeDown",
									"type" : "button",

									"x" : 36.5,
									"y" : 46.5 + 40,

									"default_image" : MAIN + "btn_prev_default.dds",
									"over_image" 	: MAIN + "btn_prev_hover.dds",
									"down_image" 	: MAIN + "btn_prev_down.dds",
								},

								{
									"name" : "MusicVolumeUp",
									"type" : "button",

									"x" : 116.5,
									"y" : 46.5 + 40,

									"default_image" : MAIN + "btn_next_default.dds",
									"over_image" 	: MAIN + "btn_next_hover.dds",
									"down_image" 	: MAIN + "btn_next_down.dds",
								},

								{
									"name" : "MusicVolume",
									"type" : "image",

									"x" : 66.5,
									"y" : 45 + 40,

									"image" : MAIN + "pagenumber_default.tga",
									"children" : [
										{
											"name" : "MusicVolume_Data",
											"type" : "text",
											"x" : 0,
											"y" : 0,
											"text" : "0",
											"all_align" : "center",
										},
										{
											"name" : "AudioSettingsVolumeMusic_Text",
											"type" : "text",

											"x" : 0,
											"y" : -18,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_MUSIC_VOLUME,
										},
									],
								},

								{
									"name" : "EffectVolumeDown",
									"type" : "button",

									"x" : 36.5,
									"y" : 46.5 + 40 * 2,

									"default_image" : MAIN + "btn_prev_default.dds",
									"over_image" 	: MAIN + "btn_prev_hover.dds",
									"down_image" 	: MAIN + "btn_prev_down.dds",
								},

								{
									"name" : "EffectVolumeUp",
									"type" : "button",

									"x" : 116.5,
									"y" : 46.5 + 40 * 2,

									"default_image" : MAIN + "btn_next_default.dds",
									"over_image" 	: MAIN + "btn_next_hover.dds",
									"down_image" 	: MAIN + "btn_next_down.dds",
								},

								{
									"name" : "EffectVolume",
									"type" : "image",

									"x" : 66.5,
									"y" : 45 + 40 * 2,

									"image" : MAIN + "pagenumber_default.tga",
									"children" : [
										{
											"name" : "EffectVolume_Data",
											"type" : "text",
											"x" : 0,
											"y" : 0,
											"text" : "0",
											"all_align" : "center",
										},
										{
											"name" : "AudioSettingsVolumeMusic_Text",
											"type" : "text",

											"x" : 0,
											"y" : -17,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_EFFECT_VOLUME,
										},
									],
								},
							],
						},

						{
							"name" : "SubPage_1",
							"type" : "expanded_image",
							"x" : 10 + 181.5,
							"y" : 10,

							"image" : ROOT_PATH.format("content_bg.png"),
							"children" : [
								{
									"name" : "VideoSettings_Text",
									"type" : "text",

									"x" : 0,
									"y" : 7,

									"text_horizontal_align" : "center",
									"horizontal_align" : "center",

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SUB_TITLE_01,
									"color" : 0xFFb19d58,
								},

								{
									"name" : "SeparateLine",
									"type" : "line",

									"x" : 1,
									"y" : 27,

									"width" : 163,
									"height" : 0,

									"color" : 0xff545454,
								},

								{
									"name" : "SelectCameraButton",
									"type" : "button",

									"x" : 0, "y" : 45,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectCamera_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_CAMERA,
										},
									],
								},

								{
									"name" : "SelectNightButton",
									"type" : "button",

									"x" : 0, "y" : 45 + 40,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectNight_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_NIGHT,
										},
									],
								},

								{
									"name" : "SelectFogButton",
									"type" : "button",

									"x" : 0, "y" : 45 + 40 * 2,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectFog_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_FOG,
										},
									],
								},
							],
						},

						{
							"name" : "SubPage_2",
							"type" : "expanded_image",

							"x" : 373,
							"y" : 10,

							"image" : ROOT_PATH.format("content_bg.png"),
							"children" : [
								{
									"name" : "PerformanceSettings_Text",
									"type" : "text",

									"x" : 0,
									"y" : 7,

									"text_horizontal_align" : "center",
									"horizontal_align" : "center",

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SUB_TITLE_02,
									"color" : 0xFFb19d58,
								},

								{
									"name" : "SeparateLine",
									"type" : "line",

									"x" : 1,
									"y" : 27,

									"width" : 163,
									"height" : 0,

									"color" : 0xff545454,
								},

								{
									"name" : "SelectModelButton",
									"type" : "button",

									"x" : 0, "y" : 45,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectModel_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_MODEL,
										},
									],
								},

								{
									"name" : "Hide_Effects_Button_0",
									"type" : "toggle_button",

									"x" : 4, "y" : 45 + 40,

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_HIDE_EFFECTS_GENERAL,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
								},

								{
									"name" : "Hide_Effects_Button_1",
									"type" : "toggle_button",

									"x" : 4 + 50 + 3.5, "y" : 45 + 40,

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_HIDE_EFFECTS_SKILLS,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
									"children" : [
										{
											"name" : "Hide_Effects_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_HIDE_EFFECTS,
										},
									],
								},

								{
									"name" : "Hide_Effects_Button_2",
									"type" : "toggle_button",

									"x" : 4 + 50 * 2 + 3.5 * 2, "y" : 45 + 40,

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_HIDE_EFFECTS_BUFFS,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
								},

								{
									"name" : "Hide_Objects_Button_0",
									"type" : "toggle_button",

									"x" : 4, "y" : 45 + 40 * 2,

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_HIDE_OBJECTS_MOUNTS,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
								},

								{
									"name" : "Hide_Objects_Button_1",
									"type" : "toggle_button",

									"x" : 4 + 50 + 3.5, "y" : 45 + 40 * 2,

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_HIDE_OBJECTS_PETS,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
									"children" : [
										{
											"name" : "Hide_Objects_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_HIDE_OBJECTS,
										},
									],
								},

								{
									"name" : "Hide_Objects_Button_2",
									"type" : "toggle_button",

									"x" : 4 + 50 * 2 + 3.5 * 2, "y" : 45 + 40 * 2,

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_HIDE_OBJECTS_SHOPS,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
								},

								{
									"name" : "SelectNoticeButton",
									"type" : "button",

									"x" : 0, "y" : 45 + 40 * 3,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectNotice_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_NOTICE,
										},
									],
								},
							],
						},
					),
				},

				{
					"name" : "Page_1",
					"type" : "main_sub_board",

					"x" : 10,
					"y" : 60,

					"width" : 548,
					"height" : THINBOARD_HEIGHT,
					"full_opacity" : True,
					"children" : [
						{
							"name" : "SubPage_3",
							"type" : "expanded_image",

							"x" : 10,
							"y" : 10,

							"image" : ROOT_PATH.format("content_bg.png"),
							"children" : [
								{
									"name" : "DisplaySettings_Text",
									"type" : "text",

									"x" : 0,
									"y" : 7,

									"text_horizontal_align" : "center",
									"horizontal_align" : "center",

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SUB_TITLE_03,
									"color" : 0xFFb19d58,
								},

								{
									"name" : "SeparateLine",
									"type" : "line",

									"x" : 1,
									"y" : 27,

									"width" : 163,
									"height" : 0,

									"color" : 0xff545454,
								},

								{
									"name" : "SelectChatLineButton",
									"type" : "button",

									"x" : 0, "y" : 45,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectChatLine_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_CHAT_LINE,
										},
									],
								},

								{
									"name" : "SelectNamesButton",
									"type" : "button",

									"x" : 0, "y" : 45 + 40,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectNames_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_NAME_VISIBILITY,
										},
									],
								},

								{
									"name" : "SelectAttackInfoButton",
									"type" : "button",

									"x" : 0, "y" : 45 + 40 * 2,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectAttack_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_ATTACK_INFO,
										},
									],
								},

								{
									"name" : "SelectAnimateWindowButton",
									"type" : "button",

									"x" : 0, "y" : 45 + 40 * 3,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectAnimate_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : "Animacja okien",
										},
									],
								},
							],
						},

						{
							"name" : "SubPage_4",
							"type" : "expanded_image",

							"x" : 10 + 181.5,
							"y" : 10,

							"image" : ROOT_PATH.format("content_bg.png"),
							"children" : [
								{
									"name" : "SocialSettings_Text",
									"type" : "text",

									"x" : 0,
									"y" : 7,

									"text_horizontal_align" : "center",
									"horizontal_align" : "center",

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SUB_TITLE_04,
									"color" : 0xFFb19d58,
								},

								{
									"name" : "SeparateLine",
									"type" : "line",

									"x" : 1,
									"y" : 27,

									"width" : 163,
									"height" : 0,

									"color" : 0xff545454,
								},

								{
									"name" : "SelectPvPButton",
									"type" : "button",

									"x" : 0, "y" : 45,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectPvP_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_PVP_MODE,
										},
									],
								},

								{
									"name" : "Block_Button_0",
									"type" : "toggle_button",

									"x" : 4, "y" : 45 + 40,

									"text" : uiScriptLocale.OPTION_BLOCK_EXCHANGE,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
								},

								{
									"name" : "Block_Button_1",
									"type" : "toggle_button",

									"x" : 4 + 50 + 3.5, "y" : 45 + 40,

									"text" : uiScriptLocale.OPTION_BLOCK_PARTY,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
									"children" : [
										{
											"name" : "Blocks_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_BLOCKS,
										},
									],
								},

								{
									"name" : "Block_Button_2",
									"type" : "toggle_button",

									"x" : 4 + 50 * 2 + 3.5 * 2, "y" : 45 + 40,

									"text" : uiScriptLocale.OPTION_BLOCK_GUILD,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
								},

								{
									"name" : "Block_Button_3",
									"type" : "toggle_button",

									"x" : 4, "y" : 45 + 35 * 2,

									"text" : uiScriptLocale.OPTION_BLOCK_WHISPER,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
								},

								{
									"name" : "Block_Button_4",
									"type" : "toggle_button",

									"x" : 4 + 50 + 3.5, "y" : 45 + 35 * 2,

									"text" : uiScriptLocale.OPTION_BLOCK_FRIEND,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
								},

								{
									"name" : "Block_Button_5",
									"type" : "toggle_button",

									"x" : 4 + 50 * 2 + 3.5 * 2, "y" : 45 + 35 * 2,

									"text" : uiScriptLocale.OPTION_BLOCK_PARTY_REQUEST,

									"default_image" :  MAIN + "slot_50x23_normal.tga",
									"over_image" 	:  MAIN + "slot_50x23_hover.tga",
									"down_image" 	:  MAIN + "slot_50x23_active.tga",
								},


							],
						},

						{
							"name" : "SubPage_5",
							"type" : "expanded_image",

							"x" : 373,
							"y" : 10,

							"image" : ROOT_PATH.format("content_bg.png"),
							"children" : [
								{
									"name" : "OtherSettings_Text",
									"type" : "text",

									"x" : 0,
									"y" : 7,

									"text_horizontal_align" : "center",
									"horizontal_align" : "center",

									"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SUB_TITLE_05,
									"color" : 0xFFb19d58,
								},

								{
									"name" : "SeparateLine",
									"type" : "line",

									"x" : 1,
									"y" : 27,

									"width" : 163,
									"height" : 0,

									"color" : 0xff545454,
								},

								{
									"name" : "SelectWNDPositionButton",
									"type" : "button",

									"x" : 0, "y" : 45,
									"horizontal_align" : "center",

									"default_image" :  MAIN + "slot_normal.tga",
									"over_image" 	:  MAIN + "slot_hover.tga",
									"down_image" 	:  MAIN + "slot_active.tga",
									"children" : [
										{
											"name" : "SelectWNDPosition_Text",
											"type" : "text",

											"x" : 0,
											"y" : -19,

											"all_align" : "center",
											"text" : uiScriptLocale.GAME_REFACTORED_OPTIONS_SELECT_WND_POS,
										},
									],
								},

							],
						},
					],
				},

				{
					"name" : "change_button",
					"type" : "button",

					"x" : 25,
					"y" : 33,

					"text" : uiScriptLocale.SYSTEM_CHANGE,
					"text_height" : 2,

					"horizontal_align" : "bottom",
					"vertical_align" : "bottom",

					"default_image" :  ROOT_PATH.format("btn_bottom_0.png"),
					"over_image" 	:  ROOT_PATH.format("btn_bottom_1.png"),
					"down_image" 	:  ROOT_PATH.format("btn_bottom_2.png"),
					"disable_image" :  ROOT_PATH.format("btn_bottom_2.png"),
				},
				{
					"name" : "logout_button",
					"type" : "button",

					"x" : 206,
					"y" : 33,

					"text" : uiScriptLocale.SYSTEM_LOGOUT,
					"text_height" : 2,

					"horizontal_align" : "bottom",
					"vertical_align" : "bottom",

					"default_image" :  ROOT_PATH.format("btn_bottom_0.png"),
					"over_image" 	:  ROOT_PATH.format("btn_bottom_1.png"),
					"down_image" 	:  ROOT_PATH.format("btn_bottom_2.png"),
					"disable_image" :  ROOT_PATH.format("btn_bottom_2.png"),
				},
				{
					"name" : "exit_button",
					"type" : "button",

					"x" : 387,
					"y" : 33,

					"text" : uiScriptLocale.SYSTEM_EXIT,
					"text_height" : 2,

					"horizontal_align" : "bottom",
					"vertical_align" : "bottom",

					"default_image" :  ROOT_PATH.format("btn_bottom_0.png"),
					"over_image" 	:  ROOT_PATH.format("btn_bottom_1.png"),
					"down_image" 	:  ROOT_PATH.format("btn_bottom_2.png"),
					"disable_image" :  ROOT_PATH.format("btn_bottom_2.png"),
				},
			),
		},
	),
}
