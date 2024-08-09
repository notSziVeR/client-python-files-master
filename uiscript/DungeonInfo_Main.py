import uiScriptLocale
import grp

BATTLE_PASS_UI_PATH = "d:/ymir work/ui/game/battle_pass/"
DUNGEON_INFO_UI_PATH = "assets/ui/dungeon_information/{}"

WINDOW_WIDTH = 666
WINDOW_HEIGHT = 449

BAR_COLOUR = 0xffFFAA00
BAR_BREADTH = 19

window = {
	"name" : "DungeonInfo",

	"x" : 0,
	"y" : 0,
	
	"style" : ("movable", "float", "animate",),

	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,

	"children" :
	(
		{
			"name" : "board",
			"type" : "main_board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,
			
			"title" : uiScriptLocale.DUNGEON_INFO_MAIN_TITLE,

			"children" :
			(
				## Dungeon List - Board
				{
					"name" : "DungeonList_Board",
					"type" : "expanded_image",

					"x" : 9,
					"y" : 33,

					"image" : DUNGEON_INFO_UI_PATH.format("LEFT_DATA.png"),

					"children" :
					(
						## Dungeon List - Window
						{
							"name" : "DungeonList_Window",
							"type" : "listboxex",

							"x" : 3,
							"y" : 5,

							"width" : 300 - 4,
							"height" : WINDOW_HEIGHT - 44,
							"children" :
							[

							],
						},


						## Dungeon List Scroll - Window
						{
							"name" : "DungeonListScroll_Window",
							"type" : "modern_scrollbar",

							"x" : 18,
							"y" : 10,

							"width": 10,
							"size": 380,
							"content_height": 440,

							"horizontal_align" : "right",
						},
					),
				},

				## Basic Info - Window
				{
					"name" : "BasicInfo_Window",
					"type" : "expanded_image",

					"x" : 216 + 9,
					"y" : 33,

					"horizontal_align" : "right",
					
					"image" : DUNGEON_INFO_UI_PATH.format("RIGHT_DATA.png"),
					"children" :
					(
						## Dungeon Details - Information Label
						{
							"name" : "DungeonDetails_InformationLabel",
							"type" : "expanded_image",

							"x" : 0,
							"y" : 0,

							"horizontal_align" : "center",

							"image" : DUNGEON_INFO_UI_PATH.format("title_back.png"),
							"children" :
							(
								## Dungeon Details - Information Text
								{
									"name" : "DungeonDetails_InformationText",
									"type" : "text",

									"x" : 0,
									"y" : -2,

									"all_align" : "center",
									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_DETAILS,
									"color" : 0xFFd1c381,
								},
							),
						},

						# ## Dungeon Details - Type Bar
						{
							"name" : "DungeonDetails_TypeBar",
							"type" : "expanded_image",

							"x" : 1,
							"y" : 39,

							"image" : DUNGEON_INFO_UI_PATH.format("bar_0.png"),

							"children" :
							(
								## Dungeon Details - Type Text
								{
									"name" : "DungeonDetails_TypeText",
									"type" : "text",

									"x" : 2,
									"y" : 2,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_TYPE,
								},

								## Dungeon Details - Type Data
								{
									"name" : "DungeonDetails_TypeData",
									"type" : "text",

									"x" : 5, "y" : 2,
									"text_horizontal_align" : "right",
									"horizontal_align" : "right",

									"text" : "-",
								},
							),
						},

						## Dungeon Details - Apply Bar
						{
							"name" : "DungeonDetails_ApplyBar",
							"type" : "expanded_image",

							"x" : 1,
							"y" : 39 + (BAR_BREADTH) * 1,

							"image" : DUNGEON_INFO_UI_PATH.format("bar_1.png"),

							"children" :
							(
								## Dungeon Details - Apply Text
								{
									"name" : "DungeonDetails_ApplyText",
									"type" : "text",

									"x" : 2,
									"y" : 2,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_APPLY_TEXT,
								},

								## Dungeon Details - Apply Data
								{
									"name" : "DungeonDetails_ApplyData",
									"type" : "text",

									"x" : 5, "y" : 2,
									"text_horizontal_align" : "right",
									"horizontal_align" : "right",

									"text" : "-",
								},
							),
						},

						## Dungeon Details - Level Limit Bar
						{
							"name" : "DungeonDetails_LevelLimitBar",
							"type" : "expanded_image",

							"x" : 1,
							"y" : 39 + (BAR_BREADTH) * 2,

							"image" : DUNGEON_INFO_UI_PATH.format("bar_0.png"),

							"children" :
							(
								## Dungeon Details - Level Limit Text
								{
									"name" : "DungeonDetails_LevelLimitText",
									"type" : "text",

									"x" : 2,
									"y" : 2,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_LEVEL_LIMIT,
								},

								## Dungeon Details - Level Limit Data
								{
									"name" : "DungeonDetails_LevelLimitData",
									"type" : "text",

									"x" : 5, "y" : 2,
									"text_horizontal_align" : "right",
									"horizontal_align" : "right",

									"text" : "-",
								},
							),
						},

						## Dungeon Details - Cooldown Bar
						{
							"name" : "DungeonDetails_CooldownBar",
							"type" : "expanded_image",

							"x" : 1,
							"y" : 39 + (BAR_BREADTH) * 3,

							"image" : DUNGEON_INFO_UI_PATH.format("bar_1.png"),

							"children" :
							(
								## Dungeon Details - Cooldown Text
								{
									"name" : "DungeonDetails_CooldownText",
									"type" : "text",

									"x" : 2,
									"y" : 2,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_COOLDOWN,
								},

								## Dungeon Details - Cooldown Data
								{
									"name" : "DungeonDetails_CooldownData",
									"type" : "text",

									"x" : 5, "y" : 2,
									"text_horizontal_align" : "right",
									"horizontal_align" : "right",

									"text" : "-",
								},
							),
						},

						# ## Dungeon Details - Personal Stats Separator
						{
							"name" : "DungeonDetails_PersonalStatsHeader",
							"type" : "expanded_image",

							"x" : 0.5, "y" : 39 + (BAR_BREADTH)*4,
							"horizontal_align" : "center",

							"image" : DUNGEON_INFO_UI_PATH.format("sub_header.png"),
							"children" :
							(
								## Dungeon Details - Personal Stats Header
								{
									"name" : "DungeonDetails_PersonalStatsHeaderText",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"all_align" : "center",
									"text" : "Personal Stats",
									"color" : 0xFFFFEDCA,
								},
							),
						},

						## Dungeon Details - Completion Count Bar
						{
							"name" : "DungeonDetails_CompletionCountBar",
							"type" : "expanded_image",

							"x" : 1,
							"y" : (39 + 27)  + (BAR_BREADTH) * 4,

							"image" : DUNGEON_INFO_UI_PATH.format("bar_0.png"),

							"children" :
							(
								## Dungeon Details - Completion Count Text
								{
									"name" : "DungeonDetails_CompletionCountText",
									"type" : "text",

									"x" : 2,
									"y" : 2,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_COMPLETION_COUNT,
								},

								## Dungeon Details - Completion Count Data
								{
									"name" : "DungeonDetails_CompletionCountData",
									"type" : "text",

									"x" : 5, "y" : 2,
									"text_horizontal_align" : "right",
									"horizontal_align" : "right",

									"text" : "-",
								},
							),
						},

						## Dungeon Details - Fastest Completion Bar
						{
							"name" : "DungeonDetails_FastestCompletionBar",
							"type" : "expanded_image",

							"x" : 1,
							"y" : (39 + 27)  + (BAR_BREADTH) * 5,

							"image" : DUNGEON_INFO_UI_PATH.format("bar_1.png"),

							"children" :
							(
								## Dungeon Details - Fastest Completion Text
								{
									"name" : "DungeonDetails_FastestCompletionText",
									"type" : "text",

									"x" : 2,
									"y" : 2,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_FASTEST_COMPLETION,
								},

								## Dungeon Details - Fastest Completion Data
								{
									"name" : "DungeonDetails_FastestCompletionData",
									"type" : "text",

									"x" : 5, "y" : 2,
									"text_horizontal_align" : "right",
									"horizontal_align" : "right",

									"text" : "-",
								},
							),
						},

						## Dungeon Details - Greatest Damage Bar
						{
							"name" : "DungeonDetails_GreatestDamageBar",
							"type" : "expanded_image",

							"x" : 1,
							"y" : (39 + 27)  + (BAR_BREADTH) * 6,

							"image" : DUNGEON_INFO_UI_PATH.format("bar_0.png"),

							"children" :
							(
								## Dungeon Details - Greatest Damage Text
								{
									"name" : "DungeonDetails_GreatestDamageText",
									"type" : "text",

									"x" : 2,
									"y" : 2,

									"text" : uiScriptLocale.DUNGEON_INFO_MAIN_GREATEST_DAMAGE,
								},

								## Dungeon Details - Fastest Completion Data
								{
									"name" : "DungeonDetails_GreatestDamageData",
									"type" : "text",

									"x" : 5, "y" : 2,
									"text_horizontal_align" : "right",
									"horizontal_align" : "right",

									"text" : "-",
								},
							),
						},

						# ## Dungeon Details - Pass Item Separator
						{
							"name" : "DungeonDetails_PassItemsHeader",
							"type" : "expanded_image",

							"x" : 0.5, "y" : (39 + 27)  + (BAR_BREADTH) * 7,
							"horizontal_align" : "center",

							"image" : DUNGEON_INFO_UI_PATH.format("sub_header.png"),
							"children" :
							(
								## Dungeon Details - Personal Stats Header
								{
									"name" : "DungeonDetails_PassItemHeaderText",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"all_align" : "center",
									"text" : "Pass Item",
									"color" : 0xFFFFEDCA,
								},
							),
						},

						# ## Dungeon Details - Pass Item Background
						{
							"name" : "DungeonDetails_PassItemBackground",
							"type" : "expanded_image",

							"x" : 0, "y" : (39 + 27 * 2)  + (BAR_BREADTH) * 7,
							"horizontal_align" : "center",

							"image" : DUNGEON_INFO_UI_PATH.format("PassItemBackground.png"),
							"children" :
							[
									# ## Dungeon Details - Pass Item
								{
									"name" : "DungeonDetails_PassItem",
									"type" : "slot",

									"x" : 88, "y" : 12,

									"width" : 32, "height" : 32,
									# "image" : DUNGEON_INFO_UI_PATH.format("slot_item.png"),
									"slot" : (
										{"index":0, "x":0, "y":0, "width":32, "height":32},
									),
								},
							],
						},

						# ## Dungeon Details - Action Separator
						{
							"name" : "DungeonDetails_ActionHeader",
							"type" : "expanded_image",

							"x" : 0.5, "y" : (12 + 39 + 27 * 3)  + (BAR_BREADTH) * 8,
							"horizontal_align" : "center",

							"image" : DUNGEON_INFO_UI_PATH.format("sub_header.png"),
							"children" :
							(
								## Dungeon Details - Personal Stats Header
								{
									"name" : "DungeonDetails_ActionHeaderText",
									"type" : "text",

									"x" : 0,
									"y" : -1,

									"all_align" : "center",
									"text" : "Action",
									"color" : 0xFFFFEDCA,
								},
							),
						},

						# ## Dungeon Details - Completion Count Button
						{
							"name" : "DungeonDetails_CompletionCountButton",
							"type" : "button",

							"x" : -70,
							"y" : 55 + (BAR_BREADTH + 10)*9,
							"horizontal_align" : "center",

							"default_image" : DUNGEON_INFO_UI_PATH.format("Buttons/top_count_btn_01.png"),
							"over_image" : DUNGEON_INFO_UI_PATH.format("Buttons/top_count_btn_02.png"),
							"down_image" : DUNGEON_INFO_UI_PATH.format("Buttons/top_count_btn_03.png"),

							"tooltip_text" : uiScriptLocale.DUNGEON_INFO_MAIN_COMPLETION_COUNT_BUTTON,
						},

						# ## Dungeon Details - Fastest Completion Button
						{
							"name" : "DungeonDetails_FastestCompletionButton",
							"type" : "button",

							"x" : 0,
							"y" : 55 + (BAR_BREADTH + 10)*9,
							"horizontal_align" : "center",

							"default_image" : DUNGEON_INFO_UI_PATH.format("Buttons/top_fastest_btn_01.png"),
							"over_image" : DUNGEON_INFO_UI_PATH.format("Buttons/top_fastest_btn_02.png"),
							"down_image" : DUNGEON_INFO_UI_PATH.format("Buttons/top_fastest_btn_03.png"),

							"tooltip_text" : uiScriptLocale.DUNGEON_INFO_MAIN_FASTEST_COMPLETION_BUTTON,
						},

						## Dungeon Details - Greatest Damage Button
						{
							"name" : "DungeonDetails_GreatestDamageButton",
							"type" : "button",

							"x" : 70,
							"y" : 55 + (BAR_BREADTH + 10)*9,
							"horizontal_align" : "center",

							"default_image" : DUNGEON_INFO_UI_PATH.format("Buttons/top_damage_btn_01.png"),
							"over_image" : DUNGEON_INFO_UI_PATH.format("Buttons/top_damage_btn_02.png"),
							"down_image" : DUNGEON_INFO_UI_PATH.format("Buttons/top_damage_btn_03.png"),

							"tooltip_text" : uiScriptLocale.DUNGEON_INFO_MAIN_GREATEST_DAMAGE_BUTTON,
						},

						# ## Dungeon Details - ReJoin Button
						{
							"name" : "DungeonDetails_ReJoinButton",
							"type" : "button",

							"x" : 5,
							"y" : 82 + (BAR_BREADTH + 10)*9,
							"text_height" : 2,

							"horizontal_align" : "left",

							"default_image" : DUNGEON_INFO_UI_PATH.format("Buttons/rejoin_btn_01.png"),
							"over_image" : DUNGEON_INFO_UI_PATH.format("Buttons/rejoin_btn_02.png"),
							"down_image" : DUNGEON_INFO_UI_PATH.format("Buttons/rejoin_btn_03.png"),

							"text" : uiScriptLocale.DUNGEON_INFO_MAIN_REJOIN_BUTTON,
						},

						## Dungeon Details - Join Button
						{
							"name" : "DungeonDetails_JoinButton",
							"type" : "button",

							"x" : 0, "y" : 35,

							"horizontal_align" : "center",
							"vertical_align" : "bottom",

							"default_image" : DUNGEON_INFO_UI_PATH.format("Buttons/teleport_btn_01.png"),
							"over_image" : DUNGEON_INFO_UI_PATH.format("Buttons/teleport_btn_02.png"),
							"down_image" : DUNGEON_INFO_UI_PATH.format("Buttons/teleport_btn_03.png"),

							"text" : "Teleport",
						},
					),
				},
			),
		},
	),
}