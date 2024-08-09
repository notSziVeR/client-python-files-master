import uiScriptLocale

WINDOW_WIDTH	= 360
WINDOW_HEIGHT	= 295

ROOT_PATH = "assets/ui/dungeon_information/Rankings/{}"

window = {
	"name" : "DungeonInfo_Ranking",
	"style" : ("movable", "float", "animate",),
	
	"x" : 0,
	"y" : 0,
	
	"width" : WINDOW_WIDTH,
	"height" : WINDOW_HEIGHT,
	
	"children" :
	(
		{
			"name" : "board",
			"type" : "board_with_titlebar",
			"style" : ("attach",),

			"x" : 0,
			"y" : 0,

			"width" : WINDOW_WIDTH,
			"height" : WINDOW_HEIGHT,

			"title" : uiScriptLocale.DUNGEON_INFO_RANKING_TITLE,

			"children" :
			(
				## main bg
				{
					"name" : "ListBoard",
					"type" : "expanded_image",
					
					"style" : ("attach",),

					"x" : 10,
					"y" : 30,
					# "horizontal_align" : "center",

					"image" : ROOT_PATH.format("background.png"),
					
					"children" :
					(
						## Ranking header
						{
							"name" : "Ranking_Header",
							"type" : "image",
							
							"x" : 0, "y" : 0,
							"horizontal_align" : "center",
							"image" : ROOT_PATH.format("header.png"),

							"children" :
							(
								{ "name" : "Header_Rank", "type" : "text", "x" : 25, "y" : 6, "text" : uiScriptLocale.DUNGEON_INFO_RANKING_HEADER_RANK, "text_horizontal_align" : "center", },
								{ "name" : "Header_Name", "type" : "text", "x" : 114, "y" : 6, "text" : uiScriptLocale.DUNGEON_INFO_RANKING_HEADER_NAME, "text_horizontal_align" : "center", },
								{ "name" : "Header_Level", "type" : "text", "x" : 205, "y" : 6, "text" : uiScriptLocale.DUNGEON_INFO_RANKING_HEADER_LEVEL, "text_horizontal_align" : "center", },
								{ "name" : "Header_Score", "type" : "text", "x" : 271, "y" : 6, "text" : uiScriptLocale.DUNGEON_INFO_RANKING_HEADER_SCORE, "text_horizontal_align" : "center", },
							),
						},
						
						# Buttons clipper
						{
							"name" : "ListClipper",
							"type" : "listboxex",
							
							"x" : 0,
							"y" : 27,
							
							"width" : 327,
							"height" : 254 - 27,
						},
					),
				},
			),
		},
	),	
}
