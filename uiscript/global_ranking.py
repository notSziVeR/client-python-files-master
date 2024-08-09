import uiScriptLocale

MAINBOARD_WIDTH = 610
MAINBOARD_HEIGHT = 405

LEFTBOARD_WIDTH = 291
LEFTBOARD_HEIGHT = 270
LEFTBOARD_X = 13
LEFTBOARD_Y = 36

RIGHTBOARD_WIDTH = 305
RIGHTBOARD_HEIGHT = 270
RIGHTBOARD_X = 328 + 6
RIGHTBOARD_Y = 36

window = {
    "name" : "EventInfoWindow",
    "style" : ("movable", "float",),

    "x" : 0,
    "y" : 0,

    "width" : MAINBOARD_WIDTH,
    "height" : MAINBOARD_HEIGHT,

    "children" :
    (
        {
            "name" : "EventBoard",
            "type" : "board_with_titlebar",
            "style" : ("attach",),
            "x" : 0,
            "y" : 0,
            "width" : MAINBOARD_WIDTH,
            "height" : MAINBOARD_HEIGHT,
            "title": "Ranking",
            "children" :
            (

                {
                    "name" : "EventButtonThinBoard",
                    "type" : "thinboard",
                    "x" : LEFTBOARD_X - 4,
                    "y" : LEFTBOARD_Y - 4,
                    "width" : MAINBOARD_WIDTH - 20,
                    "height" : MAINBOARD_HEIGHT - 42,
                    "children" :
                    (
                        {
                            "name" : "LeftThinboard",
                            "type" : "image",
                            "x" : 10,
                            "y" : 10,
                            "image" : "global_ranking/left_thin.tga",
                            "children" :
                            (
                                {
                                    "name" : "RankingCategories",
                                    "type" : "listboxex",
                                    "x" : 10,
                                    "y" : 10,
                                    "width" : 400,
                                    "height" : 42*7,
                                    "viewcount" : 7,
                                },
                            
                            ),
                        },
                        
                        {
                            "name" : "ScrollBar",
                            "type" : "scrollbar",
                            "x" : 180,
                            "y" : 10,
                            "size" : 345,
                        },

                        {
                            "name" : "RightThinboard",
                            "type" : "image",
                            "x" : 180 + 14 + 10,
                            "y" : 10,
                            "image" : "global_ranking/right_thin.tga",
                            "children" :
                            (
                                {
                                    "name" : "RightTitle",
                                    "type" : "image",
                                    "x" : 12,
                                    "y" : 10,
                                    "image" : "global_ranking/right_title.tga",
                                },
                                
                                {
                                    "name" : "RankingRecords",
                                    "type" : "image",
                                    "x" : 12,
                                    "y" : 10+23+10,
                                    "image" : "global_ranking/right_list.tga",
                                },
                            ),
                        },
                    ),
                },

                
            ),
        },
    ),
}
