import app
import uiScriptLocale

HELP_STICK_IMAGE_FILE_NAME = "d:/ymir work/ui/pattern/help_stick.tga"

START_HEIGHT = 50
HEIGHT_STEP = 25

def line(i, text, shortcut):
	return {
		"name": "HELP_LINE",
		"type": "window",

		"x": SCREEN_WIDTH * 150 / 800,
		"y": SCREEN_HEIGHT * (START_HEIGHT + HEIGHT_STEP * i) / 600,

		"width": 300,
		"height": 20,

		"children": (
			{
				"name": "HELP_LINE_SHORTCUT",
				"type": "shortcut",

				"x": 0,
				"y": 0,

				"shortcut": shortcut
			},
			{
				"name": "HELP_LINE_TEXT",
				"type": "text",

				"x": 100,
				"y": 0,

				"text": text,
				"outline": True
			}
		)
	}

def GetHotkeys():
	HOTKEYS = [
		("Show / Hide the special storage window.", [app.DIK_U]),
		("Show / Hide the chat protocol window.", [app.DIK_L]),
		("Show / Hide the dragon soul alchemy window.", [app.DIK_O]),
		("Show / Hide the switchbot window.", [app.DIK_F5]),
		("Show / Hide the dungeon overview window.", [app.DIK_F6]),
		("Show / Hide the drop filter settings window.", [app.DIK_F7]),
		("Open your shop (you have to be on the same map in the same channel of the shop).", [app.DIK_F9]),
		("Mount / Unmount mounts.", [app.DIK_LCONTROL, app.DIK_G]),
		("Unsummon your mount.", [app.DIK_LCONTROL, app.DIK_B]),
		("Activate / Deactivate dragon stoul alchemy.", [app.DIK_LSHIFT, app.DIK_O]),
	]

	lines = []
	i = 0
	for hotkey in HOTKEYS:
		lines.append(line(i, hotkey[0], hotkey[1]))
		i += 1

	return {
		"name": "Hotkeys",
		"type": "window",

		"x": 0,
		"y": 0,

		"width": SCREEN_WIDTH,
		"height": SCREEN_HEIGHT,

		"children": tuple(lines)
	}

window = {
	"name" : "HelpWindow",

	"x" : 0,
	"y" : 0,

	"width" : SCREEN_WIDTH,
	"height" : SCREEN_HEIGHT,

	"children" :
	(
		GetHotkeys(),

		## Button
		{
			"name" : "close_button",
			"type" : "button",

			"x" : SCREEN_WIDTH * (55) / 800,
			"y" : SCREEN_HEIGHT * (55) / 600,

			"text" : uiScriptLocale.CLOSE,

			"default_image" : "d:/ymir work/ui/public/xlarge_thin_button_01.sub",
			"over_image" : "d:/ymir work/ui/public/xlarge_thin_button_02.sub",
			"down_image" : "d:/ymir work/ui/public/xlarge_thin_button_03.sub",
		},
	),
}
