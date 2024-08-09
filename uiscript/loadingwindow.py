import uiScriptLocale

window = {

	"x" : 0,
	"y" : 0,

	"width"  : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		{
			"type" : "bar",

			"x" : 0,
			"y" : 0,

			"width" : SCREEN_WIDTH,
			"height" : SCREEN_WIDTH,
		},
		{
			"name" : "background",
			"type" : "expanded_image",

			"x" : 0,
			"y" : 0,

			"image" : "assets/ui/loading/new/" + "bg.png",

			"horizontal_align" : "center",
		},
	),
}
