#-*- coding: iso-8859-1 -*-
import uiScriptLocale
import app
import grp


QUEST_ICON_BACKGROUND = 'd:/ymir work/ui/game/quest/slot_base.sub'

SMALL_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_00.sub"
MIDDLE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_01.sub"
LARGE_VALUE_FILE = "d:/ymir work/ui/public/Parameter_Slot_03.sub"
ICON_SLOT_FILE = "d:/ymir work/ui/public/Slot_Base.sub"
FACE_SLOT_FILE = "d:/ymir work/ui/game/windows/box_face.sub"
ROOT_PATH = "d:/ymir work/ui/game/windows/"

LOCALE_PATH = uiScriptLocale.WINDOWS_PATH

PATTERN_PATH = "d:/ymir work/ui/pattern/"

QUEST_BOARD_WINDOW_WIDTH	= 231
if app.ENABLE_RENEWAL_CHARACTER_WINDOW:
	QUEST_BOARD_WINDOW_HEIGHT	= 340
	QUEST_BOARD_PATTERN_Y_COUNT = 19
else:
	QUEST_BOARD_WINDOW_HEIGHT	= 297
	QUEST_BOARD_PATTERN_Y_COUNT = 16

QUEST_BOARD_PATTERN_X_COUNT = 12

if app.ENABLE_RENEWAL_CHARACTER_WINDOW:
	window = {
		"name" : "CharacterWindow",
		"style" : ("movable", "float", "animate",),

		"x" : 24,
		"y" : (SCREEN_HEIGHT - 37 - 361) / 2,

		"width" : 253,
		"height" : 405,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),

				"x" : 0,
				"y" : 0,

				"width" : 253,
				"height" : 405,

				"children" :
				[
					{
						"name" : "Skill_TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 238,
						"color" : "red",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":0, "y": -1, "text":uiScriptLocale.CHARACTER_SKILL, "all_align":"center" },
						),
					},
					{
						"name" : "Emoticon_TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 238,
						"color" : "red",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":0, "y": -1, "text":uiScriptLocale.CHARACTER_ACTION, "all_align":"center" },
						),
					},
					{
						"name" : "Quest_TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 238,
						"color" : "red",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":0, "y": -1, "text":uiScriptLocale.CHARACTER_QUEST, "all_align":"center" },
						),
					},

					## Tab Area
					{
						"name" : "TabControl",
						"type" : "window",

						"x" : 0,
						"y" : 371,

						"width" : 250,
						"height" : 31,

						"children" :
						(
							## Tab
							{
								"name" : "Tab_01",
								"type" : "image",

								"x" : 0,
								"y" : 0,

								"width" : 250,
								"height" : 31,

								"image" : ROOT_PATH+"char_tab_01.sub",
							},
							{
								"name" : "Tab_02",
								"type" : "image",

								"x" : 0,
								"y" : 0,

								"width" : 250,
								"height" : 31,

								"image" : ROOT_PATH+"char_tab_02.sub",
							},
							{
								"name" : "Tab_03",
								"type" : "image",

								"x" : 0,
								"y" : 0,

								"width" : 250,
								"height" : 31,

								"image" : ROOT_PATH+"char_tab_03.sub",
							},
							{
								"name" : "Tab_04",
								"type" : "image",

								"x" : 0,
								"y" : 0,

								"width" : 250,
								"height" : 31,

								"image" : ROOT_PATH+"char_tab_04.sub",
							},
							## RadioButton
							{
								"name" : "Tab_Button_01",
								"type" : "radio_button",

								"x" : 6,
								"y" : 5,

								"width" : 53,
								"height" : 27,
							},
							{
								"name" : "Tab_Button_02",
								"type" : "radio_button",

								"x" : 61,
								"y" : 5,

								"width" : 67,
								"height" : 27,
							},
							{
								"name" : "Tab_Button_03",
								"type" : "radio_button",

								"x" : 130,
								"y" : 5,

								"width" : 61,
								"height" : 27,
							},
							{
								"name" : "Tab_Button_04",
								"type" : "radio_button",

								"x" : 192,
								"y" : 5,

								"width" : 55,
								"height" : 27,
							},
						),
					},

					## Page Area
					{
						"name" : "Character_Page",
						"type" : "window",
						"style" : ("attach",),

						"x" : 0,
						"y" : 0,

						"width" : 250,
						"height" : 370,

						"children" :
						(

							## Title Area
							{
								"name" : "Character_TitleBar", "type" : "titlebar", "style" : ("attach",), "x" : 61, "y" : 7, "width" : 185, "color" : "red",
								"children" :
								(
									{ "name" : "TitleName", "type":"text", "x":0, "y": -1, "text":uiScriptLocale.CHARACTER_MAIN, "all_align":"center" },
								),
							},

							## Guild Name Slot
							{
								"name" : "Guild_Name_Slot",
								"type" : "image",
								"x" : 60,
								"y" :27+7,
								"image" : LARGE_VALUE_FILE,

								"children" :
								(
									{
										"name" : "Guild_Name",
										"type":"text",
										"text":"NoName",
										"x":0,
										"y":0,
										"r":1.0,
										"g":1.0,
										"b":1.0,
										"a":1.0,
										"all_align" : "center",
									},
								),
							},

							## Character Name Slot
							{
								"name" : "Character_Name_Slot",
								"type" : "image_new",
								"x" : 153,
								"y" :27+7,
								"image" : LARGE_VALUE_FILE,

								"children" :
								(
									{
										"name" : "Character_Name",
										"type":"text",
										"text":"NoName",
										"x":0,
										"y":0,
										"r":1.0,
										"g":1.0,
										"b":1.0,
										"a":1.0,
										"all_align" : "center",
									},
								),
							},

							# Lv_Exp_BackImg
							{
								"name" : "TopBox",
								"type" : "boxed_board",

								"x" : 8,
								"y" : 60,

								"width" : 236,
								"height" : 44,

								"base_color" : 0xff000000,
								"children" :
								[
									{
										"name" : "HorizontalLine",
										"type" : "line",

										"x" : 0,
										"y" : 22,

										"color" : grp.GenerateColor(0.3, 0.3, 0.3, 1.0),
										"width" : 236,
										"height" : 0,
									},

									{
										"name" : "VerticalLine",
										"type" : "line",

										"x" : 60,
										"y" : 0,

										"color" : grp.GenerateColor(0.3, 0.3, 0.3, 1.0),
										"width" : 0,
										"height" : 44,
									},

									{
										"name" : "MullLevelDesc",

										"x" : 0,
										"y" : 0,

										"width" : 60,
										"height" : 22,

										"children" :
										[
											{
												"name" : "Level_Top",
												"type" : "text",

												"x" : 0,
												"y" : -1,

												"all_align" : "center",

												"text" : uiScriptLocale.CHARACTER_WINDOW_RENEWAL_LEVEL,
											},
										],
									},

									{
										"name" : "MullLevelData",

										"x" : 0,
										"y" : 22,

										"width" : 60,
										"height" : 22,

										"children" :
										[
											{
												"name" : "Level_Value",
												"type" : "text",

												"x" : 0,
												"y" : -1,

												"fontsize" : "LARGE",

												"all_align" : "center",

												"r":1.0, "g":1.0, "b":1.0, "a":1.0,

												"text" : "120",
											},
										],
									},

									{
										"name" : "MullExpDesc",

										"x" : 60,
										"y" : 0,

										"width" : 236 - 60,
										"height" : 22,

										"children" :
										[
											{
												"name" : "Exp_Top",
												"type" : "text",

												"x" : 0,
												"y" : -1,

												"all_align" : "center",

												"text" : uiScriptLocale.CHARACTER_WINDOW_EXP,
											},
										],
									},

									{
										"name" : "MullExpData",

										"x" : 60,
										"y" : 22,

										"width" : 236 - 60,
										"height" : 22,

										"children" :
										[
											{
												"name" : "Exp_Data",
												"type" : "text",

												"x" : 0,
												"y" : -1,

												"all_align" : "center",

												"r":1.0, "g":1.0, "b":1.0, "a":1.0,
												"text" : "2500000000 / 2500000000",
											},
										],
									},
								],
							},

							## Face Slot
							{ "name" : "Face_Image", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
							{ "name" : "Face_Slot", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },


							{
								"name" : "Mull",
								"type" : "boxed_board",

								"x" : 8,
								"y" : 107,

								"width" : 236,
								"height" : 265,

								# "base_color" : 0xff000000,
								"children" :
								[
									{
										"name" : "renewal_button_0",
										"type" : "radio_button",

										"x" : 0,
										"y" : 0,

										"default_image" :  "d:/ymir work/ui/game/character_window/slot_normal.tga",
										"over_image" 	:  "d:/ymir work/ui/game/character_window/slot_hover.tga",
										"down_image" 	:  "d:/ymir work/ui/game/character_window/slot_active.tga",
										"disable_image" :  "d:/ymir work/ui/game/character_window/slot_active.tga",
										"children" :
										[
											{
												"name" : "Attributes",
												"type" : "text",

												"x" : 0,
												"y" : 0,

												"all_align" : True,

												"text" : uiScriptLocale.CHARACTER_WINDOW_RENEWAL_BUTTON_0,
											},
										],
									},

									{
										"name" : "renewal_button_1",
										"type" : "radio_button",

										"x" : 118,
										"y" : 0,

										"default_image" :  "d:/ymir work/ui/game/character_window/slot_normal.tga",
										"over_image" 	:  "d:/ymir work/ui/game/character_window/slot_hover.tga",
										"down_image" 	:  "d:/ymir work/ui/game/character_window/slot_active.tga",
										"disable_image" :  "d:/ymir work/ui/game/character_window/slot_active.tga",
										"children" :
										[
											{
												"name" : "Bonuses",
												"type" : "text",

												"x" : 0,
												"y" : 0,

												"all_align" : True,

												"text" : uiScriptLocale.CHARACTER_WINDOW_RENEWAL_BUTTON_1,
											},
										],
									},

									{
										"name" : "HelperLine",
										"type" : "line",

										"x" : 0,
										"y" : 23 - 1,

										"width" : 236,
										"height" : 0,

										"color" : grp.GenerateColor(0.3, 0.3, 0.3, 1.0),
									},

									{
										"name" : "renewal_window_0",

										"x" : 0,
										"y" : 23,

										"width" : 236,
										"height" : 265 - 23,

										"children" :
										[
											{
												"name" : "BoxedBoardPoints",
												"type" : "boxed_board",

												"x" : 0,
												"y" : -1,

												"width" : 236,
												"height" : 15,

												"base_color" : 0xff000000,
												"children" :
												[
													{
														"name" : "Status_Plus_Value",
														"type" : "text",

														"x" : 0,
														"y" : -1,

														"all_align" : True,

														"text" : "Dostêpne punkty (5)",
													},
												],
											},

											{
												"name" : "MullLeft",

												"x" : 0,
												"y" : 15,

												"width" : 236/2,
												"height" : 265 - 23 - 15,
												"children" :
												[
													{ "name":"HTH_IMG", "type":"image_new",	"x":5, "y":5,	"image":ROOT_PATH+"char_info_con.sub" },
													{ "name":"INT_IMG", "type":"image_new",	"x":5, "y":35,	"image":ROOT_PATH+"char_info_int.sub" },
													{ "name":"STR_IMG", "type":"image_new",	"x":5, "y":65,	"image":ROOT_PATH+"char_info_str.sub" },
													{ "name":"DEX_IMG", "type":"image_new",	"x":5, "y":95,	"image":ROOT_PATH+"char_info_dex.sub" },

													{ "name":"HTH_Slot", "type":"boxed_board", "x": 65 + 20, "y":24 - 17, "width" : 65, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "HTH_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"INT_Slot", "type":"boxed_board", "x": 65 + 20, "y":54 - 17, "width" : 65, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "INT_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"STR_Slot", "type":"boxed_board", "x": 65 + 20, "y":84 - 17, "width" : 65, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "STR_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"DEX_Slot", "type":"boxed_board", "x": 65 + 20, "y":114 - 17, "width" : 65, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "DEX_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"HTH_Plus", "type" : "button", "x": 65 + 37, "y": 24 - 15, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },
													{ "name":"INT_Plus", "type" : "button", "x" : 65 + 37, "y" : 54 - 15, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },
													{ "name":"STR_Plus", "type" : "button", "x" : 65 + 37, "y" : 84 - 15, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },
													{ "name":"DEX_Plus", "type" : "button", "x" : 65 + 37, "y" : 114 - 15, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },

													{ "name":"HTH_Minus", "type" : "button", "x":65 + 37, "y":24 - 15, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },
													{ "name":"INT_Minus", "type" : "button", "x":65 + 37, "y":54 - 15, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },
													{ "name":"STR_Minus", "type" : "button", "x":65 + 37, "y":84 - 15, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },
													{ "name":"DEX_Minus", "type" : "button", "x":65 + 37, "y":114 - 15, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },

													{ "name":"MSPD_IMG", "type":"image_new", "x":5, "y":149 - 15, "image":ROOT_PATH+"char_info_movespeed.sub" },
													{ "name":"ASPD_IMG", "type":"image_new", "x":5, "y":149 - 15 + 30, "image":ROOT_PATH+"char_info_attspeed.sub" },
													{ "name":"CSPD_IMG", "type":"image_new", "x":5, "y":149	 - 15 + 30 * 2, "image":ROOT_PATH+"char_info_magspeed.sub" },

													{ "name":"MSPD_Slot", "type":"boxed_board", "x": 80 + 5, "y": 149 - 15 + 2, "width" : 80, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "MSPD_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"ASPD_Slot", "type":"boxed_board", "x": 80 + 5, "y":149 - 15 + 30 + 2, "width" : 80, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "ASPD_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"CSPD_Label", "type":"boxed_board", "x": 80 + 5, "y":149	 - 15 + 30 * 2 + 2, "width" : 80, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "CSPD_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},
												],
											},

											{
												"name" : "VerticalLine#Stats",
												"type" : "line",

												"x" : 0,
												"y" : 15,

												"width" : 0,
												"height" : 265 - 23 - 15,

												"horizontal_align" : "center",

												"color" : grp.GenerateColor(0.3, 0.3, 0.3, 1.0),
											},

											{
												"name" : "MullRight",

												"x" : 236/2,
												"y" : 15,

												"width" : 236/2,
												"height" : 265 - 23 - 15,
												"children" :
												[
													{ "name":"HEL_IMG",		"type":"image_new",	"x":5,	"y":5,	"image":ROOT_PATH+"char_info_hp.sub" },
													{ "name":"SP_IMG",		"type":"image_new",	"x":5,	"y":35,	"image":ROOT_PATH+"char_info_sp.sub" },
													{ "name":"ATT_IMG",		"type":"image_new",	"x":5,	"y":65,	"image":ROOT_PATH+"char_info_att.sub" },
													{ "name":"DEF_IMG",		"type":"image_new",	"x":5,	"y":95,	"image":ROOT_PATH+"char_info_def.sub" },

													{ "name":"HP_Slot", "type":"boxed_board", "x": 80 + 5, "y":24 - 17, "width" : 80, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "HP_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "17.558/17.557",
															},
														],
													},

													{ "name":"SP_Slot", "type":"boxed_board", "x": 80 + 5, "y":54 - 17, "width" : 80, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "SP_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"ATT_Slot", "type":"boxed_board", "x": 80 + 5, "y":84 - 17, "width" : 80, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "ATT_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"DEF_Slot", "type":"boxed_board", "x": 80 + 5, "y":114 - 17, "width" : 80, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "DEF_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"MATT_IMG", "type":"image_new", "x":5, "y":149 - 15, "image":ROOT_PATH+"char_info_magatt.sub" },
													{ "name":"MDEF_IMG", "type":"image_new", "x":5, "y":149 - 15 + 30, "image":ROOT_PATH+"char_info_magdef.sub" },
													{ "name":"ER_IMG", "type":"image_new", "x":5, "y":149	 - 15 + 30 * 2, "image":ROOT_PATH+"char_info_hitpct.sub" },


													{ "name":"MATT_Slot", "type":"boxed_board", "x": 80 + 5, "y": 149 - 15 + 2, "width" : 80, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "MATT_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"MDEF_Slot", "type":"boxed_board", "x": 80 + 5, "y":149 - 15 + 30 + 2, "width" : 80, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "MDEF_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},

													{ "name":"ER_Slot", "type":"boxed_board", "x": 80 + 5, "y":149	 - 15 + 30 * 2 + 2, "width" : 80, "height" : 18, "horizontal_align" : "right", "children" :
														[
															{
																"name" : "ER_Value",
																"type" : "text",

																"x" : 0,
																"y" : -1,

																"all_align" : True,

																"text" : "999",
															},
														],
													},
												],
											},

											{
												"name" : "HorizontalLine#Stats",
												"type" : "line",

												"x" : 0,
												"y" : 140,

												"width" : 236,
												"height" : 0,

												"horizontal_align" : "center",

												"color" : grp.GenerateColor(0.3, 0.3, 0.3, 1.0),
											},
										],
									},

									{
										"name" : "renewal_window_1",

										"x" : 0,
										"y" : 23,

										"width" : 236,
										"height" : 265 - 23,
										"children" :
										[
											{
												"name" : "TAB_OFFENSIVE",
												"type" : "radio_button",

												"x" : 0,
												"y" : -1,

												"default_image" :  "d:/ymir work/ui/game/character_window/slot_normal.tga",
												"over_image" 	:  "d:/ymir work/ui/game/character_window/slot_hover.tga",
												"down_image" 	:  "d:/ymir work/ui/game/character_window/slot_active.tga",
												"disable_image" :  "d:/ymir work/ui/game/character_window/slot_active.tga",
												"children" :
												[
													{
														"name" : "test",
														"type" : "text",

														"x" : 0,
														"y" : -1,

														"all_align" : True,

														"text" : uiScriptLocale.CHARACTER_WINDOW_BONUS_1,
													},
												],
											},

											{
												"name" : "TAB_DEFENSIVE",
												"type" : "radio_button",

												"x" : 118,
												"y" : -1,

												"default_image" :  "d:/ymir work/ui/game/character_window/slot_normal.tga",
												"over_image" 	:  "d:/ymir work/ui/game/character_window/slot_hover.tga",
												"down_image" 	:  "d:/ymir work/ui/game/character_window/slot_active.tga",
												"disable_image" :  "d:/ymir work/ui/game/character_window/slot_active.tga",
												"children" :
												[
													{
														"name" : "test",
														"type" : "text",

														"x" : 0,
														"y" : 0,

														"all_align" : True,

														"text" : uiScriptLocale.CHARACTER_WINDOW_BONUS_2,
													},
												],
											},
											{
												"name" : "ListBox_Bonuses",
												"type" : "listboxex",

												"x" : 0,
												"y" : 25,

												"width" : 199,
												"height" : 45,

												"itemsize_x" : 199,
												"itemsize_y" : 17,

												"itemstep" : 17,
												"viewcount" : 13,
											},
											## ScrollBar
											{
												"name" : "LogsScroll",
												"type" : "scrollbar_template",

												"x" : 9,
												"y" : 21,

												"horizontal_align" : "right",
												"size" : 221,

												"middle_image" : "d:/ymir work/ui/scroll/scrollbar.tga",
												"bg_top_image" : "d:/ymir work/ui/scroll/scroll_top.tga",
												"bg_center_image" : "d:/ymir work/ui/scroll/scroll_center.tga",
												"bg_bottom_image" : "d:/ymir work/ui/scroll/scroll_bottom.tga",
											},
										],
									},
								],
							},
						),
					},
					{
						"name" : "Skill_Page",
						"type" : "window",
						"style" : ("attach",),

						"x" : 0,
						"y" : 24,

						"width" : 250,
						"height" : 350,

						"children" :
						(
							{
								"name":"Skill_Active_Title_Bar", "type":"horizontalbar", "x":15, "y":9, "width":223,

								"children" :
								(
									{
										"name":"Active_Skill_Point_Label",
										"type":"image",
										"x":180,
										"y":3,
										"image":ROOT_PATH+"char_info_status_plus_img.sub",
										"children" :
										(
											{ "name":"Active_Skill_Plus_Img", "type":"image", "x":13, "y":0, "image":ROOT_PATH+"char_info_status_value_img.sub", },
											{ "name":"Active_Skill_Point_Value", "type":"text", "x":25, "y":0, "text":"99", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										),
									},

									## Group Button
									{
										"name" : "Skill_Group_Button_1",
										"type" : "radio_button",

										"x" : 5,
										"y" : 2,

										"text" : "Group1",
										"text_color" : 0xFFFFE3AD,

										"default_image" : "d:/ymir work/ui/game/windows/skill_tab_button_01.sub",
										"over_image" : "d:/ymir work/ui/game/windows/skill_tab_button_02.sub",
										"down_image" : "d:/ymir work/ui/game/windows/skill_tab_button_03.sub",
									},

									{
										"name" : "Skill_Group_Button_2",
										"type" : "radio_button",

										"x" : 50,
										"y" : 2,

										"text" : "Group2",
										"text_color" : 0xFFFFE3AD,

										"default_image" : "d:/ymir work/ui/game/windows/skill_tab_button_01.sub",
										"over_image" : "d:/ymir work/ui/game/windows/skill_tab_button_02.sub",
										"down_image" : "d:/ymir work/ui/game/windows/skill_tab_button_03.sub",
									},

									{
										"name" : "Active_Skill_Group_Name",
										"type" : "text",

										"x" : 7,
										"y" : 1,
										"text" : "Active",

										"vertical_align" : "center",
										"text_vertical_align" : "center",
										"color" : 0xFFFFE3AD,
									},
								),
							},

							{
								"name":"Skill_ETC_Title_Bar", "type":"horizontalbar", "x":15, "y":200+22, "width":223,
								"children" :
								(
									{
										"name" : "passiveText",
										"type" : "text",

										"x" : 0,
										"y" : 0,

										"fontsize" : "LARGE",
										"color" : 0xFFffe3ad,

										"horizontal_align" : "right",
										"text_horizontal_align" : "right",
										"text" : uiScriptLocale.CHARACTER_WINDOW_PASSIVE,
									},
									{
										"name":"Support_Skill_Point_Label",
										"type":"image",
										"x":180,
										"y":3,
										"image":ROOT_PATH+"char_info_status_plus_img.sub",
										"children" :
										(
											{ "name":"Support_Skill_Plus_Img", "type":"image", "x":13, "y":0, "image":ROOT_PATH+"char_info_status_value_img.sub", },
											{ "name":"Support_Skill_Point_Value", "type":"text", "x":25, "y":0, "text":"99", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										),
									},

									{ "name":"Support_Skill_ToolTip", "type":"image", "x":3, "y":3, "image":ROOT_PATH+"support_skill_bar_icon.sub", },
								),
							},

							{ "name":"Skill_Board", "type":"image", "x":13, "y":30, "image":"d:/ymir work/ui/game/windows/skill_board.sub", },
							{ "name":"Skill_Board_expanded", "type":"image", "x":13, "y":179, "image":"d:/ymir work/ui/game/windows/skill_board_expanded.sub", },

							## Active Slot
							{
								"name" : "Skill_Active_Slot",
								"type" : "slot",

								"x" : 0 + 16,
								"y" : 0 + 15 + 15,

								"width" : 223,
								"height" : 190,
								"image" : ICON_SLOT_FILE,

								"slot" :	(
												{"index": 1, "x": 1, "y":  4, "width":32, "height":32},
												{"index":21, "x":38, "y":  4, "width":32, "height":32},
												{"index":41, "x":75, "y":  4, "width":32, "height":32},

												{"index": 3, "x": 1, "y": 40, "width":32, "height":32},
												{"index":23, "x":38, "y": 40, "width":32, "height":32},
												{"index":43, "x":75, "y": 40, "width":32, "height":32},

												{"index": 5, "x": 1, "y": 76, "width":32, "height":32},
												{"index":25, "x":38, "y": 76, "width":32, "height":32},
												{"index":45, "x":75, "y": 76, "width":32, "height":32},

												{"index": 7, "x": 1, "y":112, "width":32, "height":32},
												{"index":27, "x":38, "y":112, "width":32, "height":32},
												{"index":47, "x":75, "y":112, "width":32, "height":32},

												####

												{"index": 2, "x":113, "y":  4, "width":32, "height":32},
												{"index":22, "x":150, "y":  4, "width":32, "height":32},
												{"index":42, "x":187, "y":  4, "width":32, "height":32},

												{"index": 4, "x":113, "y": 40, "width":32, "height":32},
												{"index":24, "x":150, "y": 40, "width":32, "height":32},
												{"index":44, "x":187, "y": 40, "width":32, "height":32},

												{"index": 6, "x":113, "y": 76, "width":32, "height":32},
												{"index":26, "x":150, "y": 76, "width":32, "height":32},
												{"index":46, "x":187, "y": 76, "width":32, "height":32},

												{"index": 8, "x":113, "y":112, "width":32, "height":32},
												{"index":28, "x":150, "y":112, "width":32, "height":32},
												{"index":48, "x":187, "y":112, "width":32, "height":32},
											),
							},

							## ETC Slot
							{
								"name" : "Skill_ETC_Slot",
								"type" : "grid_table",
								"x" : 18,
								"y" : 221 + 22,
								"start_index" : 101,
								"x_count" : 6,
								"y_count" : 3,
								"x_step" : 32,
								"y_step" : 32,
								"x_blank" : 5,
								"y_blank" : 4,
								"image" : ICON_SLOT_FILE,
							},

							
						),
					},
				],
			},
		),
	}
else:
	window = {
		"name" : "CharacterWindow",
		"style" : ("movable", "float",),

		"x" : 24,
		"y" : (SCREEN_HEIGHT - 37 - 361) / 2,

		"width" : 253,
		"height" : 361,

		"children" :
		(
			{
				"name" : "board",
				"type" : "board",
				"style" : ("attach",),

				"x" : 0,
				"y" : 0,

				"width" : 253,
				"height" : 361,

				"children" :
				[
					{
						"name" : "Skill_TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 238,
						"color" : "red",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":0, "y": -1, "text":uiScriptLocale.CHARACTER_SKILL, "all_align":"center" },
							#{ "name":"TitleName", "type":"image", "style" : ("attach",), "x":101, "y" : 1, "image" : LOCALE_PATH+"title_skill.sub", },
						),
					},
					{
						"name" : "Emoticon_TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 238,
						"color" : "red",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":0, "y": -1, "text":uiScriptLocale.CHARACTER_ACTION, "all_align":"center" },
						),
					},
					{
						"name" : "Quest_TitleBar",
						"type" : "titlebar",
						"style" : ("attach",),

						"x" : 8,
						"y" : 7,

						"width" : 238,
						"color" : "red",

						"children" :
						(
							{ "name":"TitleName", "type":"text", "x":0, "y": -1, "text":uiScriptLocale.CHARACTER_QUEST, "all_align":"center" },
						),
					},

					## Tab Area
					{
						"name" : "TabControl",
						"type" : "window",

						"x" : 0,
						"y" : 328,

						"width" : 250,
						"height" : 31,

						"children" :
						(
							## Tab
							{
								"name" : "Tab_01",
								"type" : "image",

								"x" : 0,
								"y" : 0,

								"width" : 250,
								"height" : 31,

								"image" : LOCALE_PATH+"tab_1.sub",
							},
							{
								"name" : "Tab_02",
								"type" : "image",

								"x" : 0,
								"y" : 0,

								"width" : 250,
								"height" : 31,

								"image" : LOCALE_PATH+"tab_2.sub",
							},
							{
								"name" : "Tab_03",
								"type" : "image",

								"x" : 0,
								"y" : 0,

								"width" : 250,
								"height" : 31,

								"image" : LOCALE_PATH+"tab_3.sub",
							},
							{
								"name" : "Tab_04",
								"type" : "image",

								"x" : 0,
								"y" : 0,

								"width" : 250,
								"height" : 31,

								"image" : LOCALE_PATH+"tab_4.sub",
							},
							## RadioButton
							{
								"name" : "Tab_Button_01",
								"type" : "radio_button",

								"x" : 6,
								"y" : 5,

								"width" : 53,
								"height" : 27,
							},
							{
								"name" : "Tab_Button_02",
								"type" : "radio_button",

								"x" : 61,
								"y" : 5,

								"width" : 67,
								"height" : 27,
							},
							{
								"name" : "Tab_Button_03",
								"type" : "radio_button",

								"x" : 130,
								"y" : 5,

								"width" : 61,
								"height" : 27,
							},
							{
								"name" : "Tab_Button_04",
								"type" : "radio_button",

								"x" : 192,
								"y" : 5,

								"width" : 55,
								"height" : 27,
							},
						),
					},

					## Page Area
					{
						"name" : "Character_Page",
						"type" : "window",
						"style" : ("attach",),

						"x" : 0,
						"y" : 0,

						"width" : 250,
						"height" : 304,

						"children" :
						(

							## Title Area
							{
								"name" : "Character_TitleBar", "type" : "titlebar", "style" : ("attach",), "x" : 61, "y" : 7, "width" : 185, "color" : "red",
								"children" :
								(
									#{ "name" : "TitleName", "type" : "image", "style" : ("attach",), "x" : 70, "y" : 1, "image" : LOCALE_PATH+"title_status.sub", },
									{ "name" : "TitleName", "type":"text", "x":0, "y": -1, "text":uiScriptLocale.CHARACTER_MAIN, "all_align":"center" },
								),
							},

							## Guild Name Slot
							{
								"name" : "Guild_Name_Slot",
								"type" : "image",
								"x" : 60,
								"y" :27+7,
								"image" : LARGE_VALUE_FILE,

								"children" :
								(
									{
										"name" : "Guild_Name",
										"type":"text",
										"text":"NoName",
										"x":0,
										"y":0,
										"r":1.0,
										"g":1.0,
										"b":1.0,
										"a":1.0,
										"all_align" : "center",
									},
								),
							},

							## Character Name Slot
							{
								"name" : "Character_Name_Slot",
								"type" : "image",
								"x" : 153,
								"y" :27+7,
								"image" : LARGE_VALUE_FILE,

								"children" :
								(
									{
										"name" : "Character_Name",
										"type":"text",
										"text":"NoName",
										"x":0,
										"y":0,
										"r":1.0,
										"g":1.0,
										"b":1.0,
										"a":1.0,
										"all_align" : "center",
									},
								),
							},

							## Header
							{
								"name":"Status_Header", "type":"window", "x":3, "y":31, "width":0, "height":0,
								"children" :
								(
									## Lv
									{
										"name":"Status_Lv", "type":"window", "x":9, "y":30, "width":37, "height":42,
										"children" :
										(
											{ "name":"Level_Header", "type":"image", "x":0, "y":0, "image":LOCALE_PATH+"label_level.sub" },
											{ "name":"Level_Value", "type":"text", "x":19, "y":19, "fontsize":"LARGE", "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										),
									},

									## EXP
									{
										"name":"Status_CurExp", "type":"window", "x":53, "y":30, "width":87, "height":42,
										"children" :
										(
											{ "name":"Exp_Slot", "type":"image", "x":0, "y":0, "image":LOCALE_PATH+"label_cur_exp.sub" },
											{ "name":"Exp_Value", "type":"text", "x":46, "y":19, "fontsize":"LARGE", "text":"12345678901", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },									),
									},

									## REXP
									{
										"name":"Status_RestExp", "type":"window", "x":150, "y":30, "width":50, "height":20,
										"children" :
										(
											{ "name":"RestExp_Slot", "type":"image", "x":0, "y":0, "image":LOCALE_PATH+"label_last_exp.sub" },
											{ "name":"RestExp_Value", "type":"text", "x":46, "y":19, "fontsize":"LARGE", "text":"12345678901", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										),
									},
								),
							},

							## Face Slot
							{ "name" : "Face_Image", "type" : "image", "x" : 11, "y" : 11, "image" : "d:/ymir work/ui/game/windows/face_warrior.sub" },
							{ "name" : "Face_Slot", "type" : "image", "x" : 7, "y" : 7, "image" : FACE_SLOT_FILE, },

							{
								"name":"Status_Standard", "type":"window", "x":3, "y":100, "width":200, "height":250,
								"children" :
								(
									{ "name":"Character_Bar_01", "type":"horizontalbar", "x":12, "y":8, "width":223, },
									{ "name":"Character_Bar_01_Text", "type" : "image", "x" : 13, "y" : 9, "image" : LOCALE_PATH+"label_std.sub", },

									{
										"name":"Status_Plus_Label",
										"type":"image",
										"x":150, "y":11,
										"image":LOCALE_PATH+"label_uppt.sub",

										"children" :
										(
											{ "name":"Status_Plus_Value",
											"type":"text",
											"x":62,
											"y":0,
											"text":"99",
											"r":1.0,
											"g":1.0,
											"b":1.0,
											"a":1.0,
											"text_horizontal_align":"center"
											},
										),
									},

									{"name":"Status_Standard_ItemList1", "type" : "image", "x":17, "y":31, "image" : LOCALE_PATH+"label_std_item1.sub", },
									{"name":"Status_Standard_ItemList2", "type" : "image", "x":100, "y":30, "image" : LOCALE_PATH+"label_std_item2.sub", },

									## HTH
									{
										"name":"HTH_Label", "type":"window", "x":50, "y":32, "width":60, "height":20,
										"children" :
										(
											{ "name":"HTH_Slot", "type":"image", "x":0, "y":0, "image":SMALL_VALUE_FILE },
											{ "name":"HTH_Value", "type":"text", "x":20, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											{ "name":"HTH_Plus", "type" : "button", "x":41, "y":3, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },
										),
									},
									## INT
									{
										"name":"INT_Label", "type":"window", "x":50, "y":32+23, "width":60, "height":20,
										"children" :
										(
											{ "name":"INT_Slot", "type":"image", "x":0, "y":0, "image":SMALL_VALUE_FILE },
											{ "name":"INT_Value", "type":"text", "x":20, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											{ "name":"INT_Plus", "type" : "button", "x" : 41, "y" : 3, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },
										)
									},
									## STR
									{
										"name":"STR_Label", "type":"window", "x":50, "y":32+23*2, "width":60, "height":20,
										"children" :
										(
											{ "name":"STR_Slot", "type":"image", "x":0, "y":0, "image":SMALL_VALUE_FILE },
											{ "name":"STR_Value", "type":"text", "x":20, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											{ "name":"STR_Plus", "type" : "button", "x" : 41, "y" : 3, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },
										)
									},
									## DEX
									{
										"name":"DEX_Label", "type":"window", "x":50, "y":32+23*3, "width":60, "height":20,
										"children" :
										(
											{ "name":"DEX_Slot", "type":"image", "x":0, "y":0, "image":SMALL_VALUE_FILE },
											{ "name":"DEX_Value", "type":"text", "x":20, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
											{ "name":"DEX_Plus", "type" : "button", "x" : 41, "y" : 3, "default_image" : ROOT_PATH+"btn_plus_up.sub", "over_image" : ROOT_PATH+"btn_plus_over.sub", "down_image" : ROOT_PATH+"btn_plus_down.sub", },
										)
									},

									{ "name":"HTH_Minus", "type" : "button", "x":9, "y":35, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },
									{ "name":"INT_Minus", "type" : "button", "x":9, "y":35+23, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },
									{ "name":"STR_Minus", "type" : "button", "x":9, "y":35+23*2, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },
									{ "name":"DEX_Minus", "type" : "button", "x":9, "y":35+23*3, "default_image" : ROOT_PATH+"btn_minus_up.sub", "over_image" : ROOT_PATH+"btn_minus_over.sub", "down_image" : ROOT_PATH+"btn_minus_down.sub", },

									####

									## HP
									{
										"name":"HEL_Label", "type":"window", "x":145, "y":32, "width":50, "height":20,
										"children" :
										(
											{ "name":"HP_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
											{ "name":"HP_Value", "type":"text", "x":45, "y":3, "text":"9999/9999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										),
									},
									## SP
									{
										"name":"SP_Label", "type":"window", "x":145, "y":32+23, "width":50, "height":20,
										"children" :
										(
											{ "name":"SP_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
											{ "name":"SP_Value", "type":"text", "x":45, "y":3, "text":"9999/9999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										)
									},
									## ATT
									{
										"name":"ATT_Label", "type":"window", "x":145, "y":32+23*2, "width":50, "height":20,
										"children" :
										(
											{ "name":"ATT_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
											{ "name":"ATT_Value", "type":"text", "x":45, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										),
									},
									## DEF
									{
										"name":"DEF_Label", "type":"window", "x":145, "y":32+23*3, "width":50, "height":20,
										"children" :
										(
											{ "name":"DEF_Slot", "type":"image", "x":0, "y":0, "image":LARGE_VALUE_FILE },
											{ "name":"DEF_Value", "type":"text", "x":45, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										)
									},
								),
							},

							{
								"name":"Status_Extent", "type":"window", "x":3, "y":221, "width":200, "height":50,
								"children" :
								(

									{ "name":"Status_Extent_Bar", "type":"horizontalbar", "x":12, "y":6, "width":223, },
									{ "name":"Status_Extent_Label", "type" : "image", "x" : 13, "y" : 8, "image" : LOCALE_PATH+"label_ext.sub", },

									{"name":"Status_Extent_ItemList1", "type" : "image", "x":11, "y":31, "image" : LOCALE_PATH+"label_ext_item1.sub", },
									{"name":"Status_Extent_ItemList2", "type" : "image", "x":128, "y":32, "image" : LOCALE_PATH+"label_ext_item2.sub", },

									{
										"name":"MOV_Label", "type":"window", "x":66, "y":33, "width":50, "height":20,
										"children" :
										(
											{ "name":"MSPD_Slot", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
											{ "name":"MSPD_Value", "type":"text", "x":26, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										)
									},

									{
										"name":"ASPD_Label", "type":"window", "x":66, "y":33+23, "width":50, "height":20,
										"children" :
										(
											{ "name":"ASPD_Slot", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
											{ "name":"ASPD_Value", "type":"text", "x":26, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										)
									},

									{
										"name":"CSPD_Label", "type":"window", "x":66, "y":33+23*2, "width":50, "height":20,
										"children" :
										(
											{ "name":"CSPD_Slot", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
											{ "name":"CSPD_Value", "type":"text", "x":26, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										)
									},

									{
										"name":"MATT_Label", "type":"window", "x":183, "y":33, "width":50, "height":20,
										"children" :
										(
											{ "name":"MATT_Slot", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
											{ "name":"MATT_Value", "type":"text", "x":26, "y":3, "text":"999-999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										)
									},

									{
										"name":"MDEF_Label", "type":"window", "x":183, "y":33+23, "width":50, "height":20,
										"children" :
										(
											{ "name":"MDEF_Slot", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
											{ "name":"MDEF_Value", "type":"text", "x":26, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										)
									},

									{
										"name":"ER_Label", "type":"window", "x":183, "y":33+23*2, "width":50, "height":20,
										"children" :
										(
											{ "name":"ER_Slot", "type":"image", "x":0, "y":0, "image":MIDDLE_VALUE_FILE },
											{ "name":"ER_Value", "type":"text", "x":26, "y":3, "text":"999", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										)
									},

								),
							},
						),
					},
					{
						"name" : "Skill_Page",
						"type" : "window",
						"style" : ("attach",),

						"x" : 0,
						"y" : 24,

						"width" : 250,
						"height" : 304,

						"children" :
						(

							{
								"name":"Skill_Active_Title_Bar", "type":"horizontalbar", "x":15, "y":3, "width":223,

								"children" :
								(
									{
										"name":"Active_Skill_Point_Label", "type":"image", "x":145, "y":3, "image":LOCALE_PATH+"label_uppt.sub",
										"children" :
										(
											{ "name":"Active_Skill_Point_Value", "type":"text", "x":62, "y":0, "text":"99", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										),
									},

									## Group Button
									{
										"name" : "Skill_Group_Button_1",
										"type" : "radio_button",

										"x" : 5,
										"y" : 2,

										"text" : "Group1",
										"text_color" : 0xFFFFE3AD,

										"default_image" : "d:/ymir work/ui/game/windows/skill_tab_button_01.sub",
										"over_image" : "d:/ymir work/ui/game/windows/skill_tab_button_02.sub",
										"down_image" : "d:/ymir work/ui/game/windows/skill_tab_button_03.sub",
									},

									{
										"name" : "Skill_Group_Button_2",
										"type" : "radio_button",

										"x" : 50,
										"y" : 2,

										"text" : "Group2",
										"text_color" : 0xFFFFE3AD,

										"default_image" : "d:/ymir work/ui/game/windows/skill_tab_button_01.sub",
										"over_image" : "d:/ymir work/ui/game/windows/skill_tab_button_02.sub",
										"down_image" : "d:/ymir work/ui/game/windows/skill_tab_button_03.sub",
									},

									{
										"name" : "Active_Skill_Group_Name",
										"type" : "text",

										"x" : 7,
										"y" : 1,
										"text" : "Active",

										"vertical_align" : "center",
										"text_vertical_align" : "center",
										"color" : 0xFFFFE3AD,
									},

								),
							},

							{
								"name":"Skill_ETC_Title_Bar", "type":"horizontalbar", "x":15, "y":200, "width":223,

								"children" :
								(
									{
										"name" : "Support_Skill_Group_Name",
										"type" : "text",

										"x" : 7,
										"y" : 1,
										"text" : uiScriptLocale.SKILL_SUPPORT_TITLE,

										"vertical_align" : "center",
										"text_vertical_align" : "center",
										"color" : 0xFFFFE3AD,
									},

									{
										"name":"Support_Skill_Point_Label", "type":"image", "x":145, "y":3, "image":LOCALE_PATH+"label_uppt.sub",
										"children" :
										(
											{ "name":"Support_Skill_Point_Value", "type":"text", "x":62, "y":0, "text":"99", "r":1.0, "g":1.0, "b":1.0, "a":1.0, "text_horizontal_align":"center" },
										),
									},
								),
							},
							{ "name":"Skill_Board", "type":"image", "x":13, "y":38, "image":"d:/ymir work/ui/game/windows/skill_board.sub", },

							## Active Slot
							{
								"name" : "Skill_Active_Slot",
								"type" : "slot",

								"x" : 0 + 16,
								"y" : 0 + 15 + 23,

								"width" : 223,
								"height" : 223,
								"image" : ICON_SLOT_FILE,

								"slot" :	(
												{"index": 1, "x": 1, "y":  4, "width":32, "height":32},
												{"index":21, "x":38, "y":  4, "width":32, "height":32},
												{"index":41, "x":75, "y":  4, "width":32, "height":32},

												{"index": 3, "x": 1, "y": 40, "width":32, "height":32},
												{"index":23, "x":38, "y": 40, "width":32, "height":32},
												{"index":43, "x":75, "y": 40, "width":32, "height":32},

												{"index": 5, "x": 1, "y": 76, "width":32, "height":32},
												{"index":25, "x":38, "y": 76, "width":32, "height":32},
												{"index":45, "x":75, "y": 76, "width":32, "height":32},

												{"index": 7, "x": 1, "y":112, "width":32, "height":32},
												{"index":27, "x":38, "y":112, "width":32, "height":32},
												{"index":47, "x":75, "y":112, "width":32, "height":32},

												####

												{"index": 2, "x":113, "y":  4, "width":32, "height":32},
												{"index":22, "x":150, "y":  4, "width":32, "height":32},
												{"index":42, "x":187, "y":  4, "width":32, "height":32},

												{"index": 4, "x":113, "y": 40, "width":32, "height":32},
												{"index":24, "x":150, "y": 40, "width":32, "height":32},
												{"index":44, "x":187, "y": 40, "width":32, "height":32},

												{"index": 6, "x":113, "y": 76, "width":32, "height":32},
												{"index":26, "x":150, "y": 76, "width":32, "height":32},
												{"index":46, "x":187, "y": 76, "width":32, "height":32},

												{"index": 8, "x":113, "y":112, "width":32, "height":32},
												{"index":28, "x":150, "y":112, "width":32, "height":32},
												{"index":48, "x":187, "y":112, "width":32, "height":32},
											),
							},

							## ETC Slot
							{
								"name" : "Skill_ETC_Slot",
								"type" : "grid_table",
								"x" : 18,
								"y" : 221,
								"start_index" : 101,
								"x_count" : 6,
								"y_count" : 2,
								"x_step" : 32,
								"y_step" : 32,
								"x_blank" : 5,
								"y_blank" : 4,
								"image" : ICON_SLOT_FILE,
							},

						),
					},
				],
			},
		),
	}

if app.ENABLE_QUEST_RENEWAL:
	window["children"][0]["children"] = window["children"][0]["children"] + [
	{
		"name" : "Quest_Page",
		"type" : "window",
		"style" : ("attach",),

		"x" : 0,
		"y" : 24,

		"width" : 250,
		"height" : QUEST_BOARD_WINDOW_HEIGHT,

		"children" :
		(
			{
				"name" : "quest_page_board_window",
				"type" : "window",
				"style" : ("attach", "ltr",),

				"x" : 10,
				"y" : 7,

				"width" : QUEST_BOARD_WINDOW_WIDTH,
				"height" : QUEST_BOARD_WINDOW_HEIGHT,

				"children" :
				(
					## LeftTop 1
					{
						"name" : "LeftTop",
						"type" : "image",
						"style" : ("ltr",),

						"x" : 0,
						"y" : 0,
						"image" : PATTERN_PATH + "border_A_left_top.tga",
					},
					## RightTop 2
					{
						"name" : "RightTop",
						"type" : "image",
						"style" : ("ltr",),

						"x" : QUEST_BOARD_WINDOW_WIDTH - 16,
						"y" : 0,
						"image" : PATTERN_PATH + "border_A_right_top.tga",
					},
					## LeftBottom 3
					{
						"name" : "LeftBottom",
						"type" : "image",
						"style" : ("ltr",),

						"x" : 0,
						"y" : QUEST_BOARD_WINDOW_HEIGHT - 16,
						"image" : PATTERN_PATH + "border_A_left_bottom.tga",
					},
					## RightBottom 4
					{
						"name" : "RightBottom",
						"type" : "image",
						"style" : ("ltr",),

						"x" : QUEST_BOARD_WINDOW_WIDTH - 16,
						"y" : QUEST_BOARD_WINDOW_HEIGHT - 16,
						"image" : PATTERN_PATH + "border_A_right_bottom.tga",
					},
					## topcenterImg 5
					{
						"name" : "TopCenterImg",
						"type" : "expanded_image",
						"style" : ("ltr",),

						"x" : 16,
						"y" : 0,
						"image" : PATTERN_PATH + "border_A_top.tga",
						"rect" : (0.0, 0.0, QUEST_BOARD_PATTERN_X_COUNT, 0),
					},
					## leftcenterImg 6
					{
						"name" : "LeftCenterImg",
						"type" : "expanded_image",
						"style" : ("ltr",),

						"x" : 0,
						"y" : 16,
						"image" : PATTERN_PATH + "border_A_left.tga",
						"rect" : (0.0, 0.0, 0, QUEST_BOARD_PATTERN_Y_COUNT),
					},
					## rightcenterImg 7
					{
						"name" : "RightCenterImg",
						"type" : "expanded_image",
						"style" : ("ltr",),

						"x" : QUEST_BOARD_WINDOW_WIDTH - 16,
						"y" : 16,
						"image" : PATTERN_PATH + "border_A_right.tga",
						"rect" : (0.0, 0.0, 0, QUEST_BOARD_PATTERN_Y_COUNT),
					},
					## bottomcenterImg 8
					{
						"name" : "BottomCenterImg",
						"type" : "expanded_image",
						"style" : ("ltr",),

						"x" : 16,
						"y" : QUEST_BOARD_WINDOW_HEIGHT - 16,
						"image" : PATTERN_PATH + "border_A_bottom.tga",
						"rect" : (0.0, 0.0, QUEST_BOARD_PATTERN_X_COUNT, 0),
					},
					## centerImg
					{
						"name" : "CenterImg",
						"type" : "expanded_image",
						"style" : ("ltr",),

						"x" : 16,
						"y" : 16,
						"image" : PATTERN_PATH + "border_A_center.tga",
						"rect" : (0.0, 0.0, QUEST_BOARD_PATTERN_X_COUNT, QUEST_BOARD_PATTERN_Y_COUNT),
					},

					{
						"name" : "quest_object_board_window",
						"type" : "window",
						"style" : ("attach", "ltr",),

						"x" : 3,
						"y" : 3,

						"width" : QUEST_BOARD_WINDOW_WIDTH - 3, # 228
						"height" : QUEST_BOARD_WINDOW_HEIGHT - 3, # 294
					},
				),
			},

			### QUEST_CATEGORY
			{
				"name" : "Quest_Category_00",
				"type" : "subtitlebar",
				"text" : uiScriptLocale.QUEST_CATEGORY_00,

				"x" : 13,
				"y" : 0,

				"width" : 210,
				"height" : 16,
			},
			{
				"name" : "Quest_Category_01",
				"type" : "subtitlebar",
				"text" : uiScriptLocale.QUEST_CATEGORY_01,

				"x" : 13,
				"y" : 0,

				"width" : 210,
				"height" : 16,
			},
			{
				"name" : "Quest_Category_02",
				"type" : "subtitlebar",
				"text" : uiScriptLocale.QUEST_CATEGORY_02,

				"x" : 13,
				"y" : 0,

				"width" : 210,
				"height" : 16,
			},
			{
				"name" : "Quest_Category_03",
				"type" : "subtitlebar",
				"text" : uiScriptLocale.QUEST_CATEGORY_03,

				"x" : 13,
				"y" : 0,

				"width" : 210,
				"height" : 16,
			},
			{
				"name" : "Quest_Category_04",
				"type" : "subtitlebar",
				"text" : uiScriptLocale.QUEST_CATEGORY_04,

				"x" : 13,
				"y" : 0,

				"width" : 210,
				"height" : 16,
			},
			{
				"name" : "Quest_Category_05",
				"type" : "subtitlebar",
				"text" : uiScriptLocale.QUEST_CATEGORY_05,

				"x" : 13,
				"y" : 0,

				"width" : 210,
				"height" : 16,
			},
			{
				"name" : "Quest_Category_06",
				"type" : "subtitlebar",
				"text" : uiScriptLocale.QUEST_CATEGORY_06,

				"x" : 13,
				"y" : 0,

				"width" : 210,
				"height" : 16,
			},
			{
				"name" : "Quest_Category_07",
				"type" : "subtitlebar",
				"text" : uiScriptLocale.QUEST_CATEGORY_07,

				"x" : 13,
				"y" : 0,

				"width" : 210,
				"height" : 16,
			},
			### END_OF_QUEST_CATEGORY

			{
				"name" : "Quest_ScrollBar",
				"type" : "scrollbar",

				"x" : 25,
				"y" : 12,
				"size" : QUEST_BOARD_WINDOW_HEIGHT - 10,
				"horizontal_align" : "right",
			},
		),
	},]
else:
	window["children"][0]["children"] = window["children"][0]["children"] + [
	{
		"name" : "Quest_Page",
		"type" : "window",
		"style" : ("attach",),

		"x" : 0,
		"y" : 24,

		"width" : 250,
		"height" : 304,

		"children" :
		(
			{
				"name" : "Quest_Slot",
				"type" : "grid_table",
				"x" : 18,
				"y" : 20,
				"start_index" : 0,
				"x_count" : 1,
				"y_count" : 5,
				"x_step" : 32,
				"y_step" : 32,
				"y_blank" : 28,
				"image" : QUEST_ICON_BACKGROUND,
			},

			{
				"name" : "Quest_ScrollBar",
				"type" : "scrollbar",

				"x" : 25,
				"y" : 12,
				"size" : 290,
				"horizontal_align" : "right",
			},

			{ "name" : "Quest_Name_00", "type" : "text", "text" : "0", "x" : 60, "y" : 14 },
			{ "name" : "Quest_LastTime_00", "type" : "text", "text" : "0", "x" : 60, "y" : 30 },
			{ "name" : "Quest_LastCount_00", "type" : "text", "text" : "0", "x" : 60, "y" : 46 },

			{ "name" : "Quest_Name_01", "type" : "text", "text" : "0", "x" : 60, "y" : 74 },
			{ "name" : "Quest_LastTime_01", "type" : "text", "text" : "0", "x" : 60, "y" : 90 },
			{ "name" : "Quest_LastCount_01", "type" : "text", "text" : "0", "x" : 60, "y" : 106 },

			{ "name" : "Quest_Name_02", "type" : "text", "text" : "0", "x" : 60, "y" : 134 },
			{ "name" : "Quest_LastTime_02", "type" : "text", "text" : "0", "x" : 60, "y" : 150 },
			{ "name" : "Quest_LastCount_02", "type" : "text", "text" : "0", "x" : 60, "y" : 166 },

			{ "name" : "Quest_Name_03", "type" : "text", "text" : "0", "x" : 60, "y" : 194 },
			{ "name" : "Quest_LastTime_03", "type" : "text", "text" : "0", "x" : 60, "y" : 210 },
			{ "name" : "Quest_LastCount_03", "type" : "text", "text" : "0", "x" : 60, "y" : 226 },

			{ "name" : "Quest_Name_04", "type" : "text", "text" : "0", "x" : 60, "y" : 254 },
			{ "name" : "Quest_LastTime_04", "type" : "text", "text" : "0", "x" : 60, "y" : 270 },
			{ "name" : "Quest_LastCount_04", "type" : "text", "text" : "0", "x" : 60, "y" : 286 },
		),
	},]

if app.ENABLE_RENEWAL_CHARACTER_WINDOW:
	window["children"][0]["children"] = window["children"][0]["children"] + [
	{
		"name" : "Emoticon_Page",
		"type" : "window",
		"style" : ("attach",),

		"x" : 0,
		"y" : 24,

		"width" : 250,
		"height" : 304,

		"children" :
		[
			{
				"name":"Action_Bar",
				"type":"horizontalbar",

				"x":12,
				"y":11+7,

				"width":223,
				"children" :
				[
					{
						"name" : "emotionText_0",
						"type" : "text",

						"x" : 0,
						"y" : 0,

						"fontsize" : "LARGE",
						"color" : 0xFFffe3ad,

						"horizontal_align" : "right",
						"text_horizontal_align" : "right",
						"text" : uiScriptLocale.CHARACTER_WINDOW_EMOTION_0,
					},
				],
			},

			{ "name":"Action_Bar_Img", "type":"image_new", "x":15, "y":19, "image":ROOT_PATH+"action_bar_img.sub", },

			## Basis Action Slot
			{
				"name" : "SoloEmotionSlot",
				"type" : "grid_table",
				"x" : 15,
				"y" : 33+7,
				"horizontal_align" : "center",
				"start_index" : 1,
				"x_count" : 6,
				"y_count" : 3,
				"x_step" : 32,
				"y_step" : 32,
				"x_blank" : 5,
				"y_blank" : 10,
				"image" : ICON_SLOT_FILE,
			},

			{
				"name":"Reaction_Bar",
				"type":"horizontalbar",
				"x":12,
				"y":8+130+26,
				"width":223,
				"children" :
				[
					{
						"name" : "emotionText_1",
						"type" : "text",

						"x" : 0,
						"y" : 0,

						"fontsize" : "LARGE",
						"color" : 0xFFffe3ad,

						"horizontal_align" : "right",
						"text_horizontal_align" : "right",
						"text" : uiScriptLocale.CHARACTER_WINDOW_EMOTION_1,
					},
				],
			},

			{ "name":"Reaction_Bar_Img", "type":"image_new", "x":15, "y":10+130+25, "image":ROOT_PATH+"reaction_bar_img.sub", },

			{
				"name" : "DualEmotionSlot",
				"type" : "grid_table",
				"x" : 15,
				"y" : 160+25,
				"start_index" : 51,
				"x_count" : 6,
				"y_count" : 1,
				"x_step" : 32,
				"y_step" : 32,
				"x_blank" : 5,
				"y_blank" : 10,
				"image" : ICON_SLOT_FILE,
			},

			{
				"name":"Special_Action_Bar",
				"type":"horizontalbar",
				"x":12,
				"y":8+190+25,
				"width":223,
				"children" :
				[
					{
						"name" : "emotionText_2",
						"type" : "text",

						"x" : 0,
						"y" : 0,

						"fontsize" : "LARGE",
						"color" : 0xFFffe3ad,

						"horizontal_align" : "right",
						"text_horizontal_align" : "right",
						"text" : uiScriptLocale.CHARACTER_WINDOW_EMOTION_2,
					},
				],
			},
			{ "name":"Special_Action_Bar_Img", "type":"image_new", "x":15, "y":10+190+24, "image":ROOT_PATH+"special_action_bar_img.sub", },

			## Special_Action_Slot
			{
				"name" : "SpecialEmotionSlot",
				"type" : "grid_table",

				"x" : 30,
				"y" : 220+25,
				"start_index" : 60,
				"x_count" : 6,
				"y_count" : 2,
				"x_step" : 32,
				"y_step" : 32,
				"x_blank" : 0,
				"y_blank" : 0,
				"image" : ICON_SLOT_FILE,
			},
		],
	},]
else:
	window["children"][0]["children"] = window["children"][0]["children"] + [
	{
		"name" : "Emoticon_Page",
		"type" : "window",
		"style" : ("attach",),

		"x" : 0,
		"y" : 24,

		"width" : 250,
		"height" : 304,

		"children" :
		(
			{ "name":"Action_Bar", "type":"horizontalbar", "x":12, "y":11, "width":223, },
			{ "name":"Action_Bar_Text", "type":"text", "x":15, "y":13, "text":uiScriptLocale.CHARACTER_NORMAL_ACTION },

			## Basis Action Slot
			{
				"name" : "SoloEmotionSlot",
				"type" : "grid_table",
				"x" : 30,
				"y" : 33,
				"horizontal_align" : "center",
				"start_index" : 1,
				"x_count" : 6,
				"y_count" : 3,
				"x_step" : 32,
				"y_step" : 32,
				"x_blank" : 0,
				"y_blank" : 0,
				"image" : ICON_SLOT_FILE,
			},

			{ "name":"Reaction_Bar", "type":"horizontalbar", "x":12, "y":8+150, "width":223, },
			{ "name":"Reaction_Bar_Text", "type":"text", "x":15, "y":10+150, "text":uiScriptLocale.CHARACTER_MUTUAL_ACTION },

			## Reaction Slot
			{
				"name" : "DualEmotionSlot",
				"type" : "grid_table",
				"x" : 30,
				"y" : 180,
				"start_index" : 51,
				"x_count" : 6,
				"y_count" : 3,
				"x_step" : 32,
				"y_step" : 32,
				"x_blank" : 0,
				"y_blank" : 0,
				"image" : ICON_SLOT_FILE,
			},
		),
	},]