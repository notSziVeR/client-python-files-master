ROOT = "d:/ymir work/ui/public/"

window = {
	"name" : "QuestDialog",
	"style" : ("float", "animate",),#"movable",

	"x" : 0,
	"y" : 0,

	"width" : 800,
	"height" : 450,

	"children" :
	(
		{
			"name" : "board",
			"type" : "board",
			"style" : ("attach", "ignore_size",),

			"x" : 0,
			"y" : 0,

			"horizontal_align" : "center",
			"vertical_align" : "center",

			"width" : 350,
			"height" : 300,
		},
	),
}
