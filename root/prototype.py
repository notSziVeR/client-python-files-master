import dbg
import app
import localeInfo
import wndMgr
import systemSetting
import mouseModule
import networkModule
import uiCandidate
import constInfo
import musicInfo
import stringCommander

import introInterface

import playerSettingModule, colorInfo, chrmgr, background

#bind_me(locals().values())

if constInfo.ENABLE_PASTE_FEATURE:
	from ui import EnablePaste as ui_EnablePaste
	ui_EnablePaste(True)

def RunApp():
	musicInfo.LoadLastPlayFieldMusic()

	app.SetHairColorEnable(constInfo.HAIR_COLOR_ENABLE)
	app.SetArmorSpecularEnable(constInfo.ARMOR_SPECULAR_ENABLE)
	app.SetWeaponSpecularEnable(constInfo.WEAPON_SPECULAR_ENABLE)

	app.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetMouseHandler(mouseModule.mouseController)
	wndMgr.SetScreenSize(systemSetting.GetWidth(), systemSetting.GetHeight())

	try:
		app.Create(localeInfo.APP_TITLE, systemSetting.GetWidth(), systemSetting.GetHeight(), 1)
	except RuntimeError, msg:
		msg = str(msg)
		if "CREATE_DEVICE" == msg:
			dbg.LogBox("Sorry, Your system does not support 3D graphics,\r\nplease check your hardware and system configeration\r\nthen try again.")
		else:
			dbg.LogBox("Metin2.%s" % msg)
		return

	app.SetCamera(1500.0, 30.0, 0.0, 180.0)

	#Gets and sets the floating-point control word
	#app.SetControlFP()

	import emotion
	emotion.RegisterEmotionIcons()

	import playerSettingModule
	playerSettingModule.LoadGameNPC()
	playerSettingModule.LoadGuildBuildingList(localeInfo.GUILD_BUILDING_LIST_TXT)
	playerSettingModule.LoadEquipmentSets()

	if app.ENABLE_REFINE_ELEMENT:
		playerSettingModule.LoadRefineElementEff()

	if not mouseModule.mouseController.Create():
		return

	import introTest
	if introTest.TEST_ACTIVE:
		test = introTest.IntroTest()
		test.Show()

		app.Loop()
	else:
		mainStream = networkModule.MainStream()
		mainStream.Create()

		mainStream.SetLoginPhase()
		app.Loop()

		# mainStream.Destroy()
		mouseModule.mouseController.Destroy()

	app.SetMouseHandler   ( None )
	wndMgr.SetMouseHandler( None )

RunApp()

