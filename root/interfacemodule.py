##
## Interface
##
import constInfo
from introinterface import gcGetEnable
import systemSetting
import wndMgr
import chat
import app
import player
import uiTaskBar
import uiCharacter
import uiInventory
import uiDragonSoul
import uiChat
import uiMessenger
import guild

import ui
import uiHelp
import uiWhisper
import uiPointReset
import uiShop
import uiExchange
import uiRestart
import uiToolTip
import uiMiniMap
import uiParty
import uiSafebox
import uiGuild
import uiQuest
import uiPrivateShopBuilder
import uiCommon
import uiRefine
import uiEquipmentDialog
import uiGameButton
import uiTip
if app.ENABLE_CUBE_RENEWAL:
	import uiCubeRenewal
import miniMap
# ACCESSORY_REFINE_ADD_METIN_STONE
import uiSelectItem
# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE
import uiScriptLocale

import event
import localeInfo

import net

if app.ENABLE_SWITCHBOT:
	import uiSwitchbot

if app.ENABLE_SPECIAL_STORAGE:
	import uiInventoryMenu

if app.ENABLE_VOICE_CHAT:
	import voiceManager

if gcGetEnable("ENABLE_REFACTORED_OPTIONS"):
	import uiRefactoredOptions
else:
	import uiSystem

if app.ENABLE_ADMIN_MANAGER:
	import admin
	import uiAdminManager

if app.ENABLE_MARBLE_CREATOR_SYSTEM:
	import uimarblemanager

if app.BATTLE_PASS_ENABLE:
	import uibattlepass

if app.ENABLE_TRANSMUTATION_SYSTEM:
	import uiTransmutation

if app.ENABLE_FIND_LETTERS_EVENT:
	import uifindletters

if app.ENABLE_REFINE_ELEMENT:
	import item
	import uiRefineElement

if app.ENABLE_LUCKY_BOX:
	import uiLuckyBox

if app.ENABLE_SAVE_POSITIONS_SYSTEM:
	import uipositionmanager

if app.ENABLE_RENDER_TARGET_EXTENSION:
	import uiPreview

if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
	import uiLogsChat
	import logsChat

if gcGetEnable("ENABLE_SKILL_SELECT"):
	import uiSelectSkill

if app.INGAME_ITEMSHOP_ENABLE:
	import uiItemShopDialog

if app.TOMBOLA_EVENT_ENABLE:
	import uiTombola

if gcGetEnable("ENABLE_LEGENDARY_STONES"):
	import uiLegendaryStones

if app.ENABLE_TELEPORT_SYSTEM:
	import uiteleportmanager

if gcGetEnable("ENABLE_DUNGEON_INFORMATION"):
	import uiDungeonInfo

if app.ENABLE_AMULET_SYSTEM:
	import uiAmuletSystem

if app.SASH_ABSORPTION_ENABLE:
	import uisashsystem
	
if app.ENABLE_PREMIUM_PRIVATE_SHOP:
	import uiPrivateShop
	import uiPrivateShopSearch

if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
	import uiBuffNPC

if app.ENABLE_ANTI_MULTIPLE_FARM:
	import uiAntiMultipleFarm
	import anti_multiple_farm

import cfg

from _weakref import proxy

IsQBHide = 0
class Interface(object):
	CHARACTER_STATUS_TAB = 1
	CHARACTER_SKILL_TAB = 2

	class OverLayButtonGroup(ui.Window):

		BASE_PATH = "assets/ui/overlay_buttons/"
		BUTTON_LIST = ("button_itemshop", )

		def	__init__(self, pInterface):
			ui.Window.__init__(self)
			self.Buttons = {}

			self.interface = proxy(pInterface)

			self.__BuildWindow()
			self.__LoadDialogs()

		def	__del__(self):
			ui.Window.__del__(self)
			self.Buttons = {}
			self.interface = None
			if app.TOMBOLA_EVENT_ENABLE:
				self.uiTombola = None

		def	__BuildWindow(self):
			## Buttons
			for sButt in self.BUTTON_LIST:
				self.Buttons[sButt] = ui.Button()
				self.Buttons[sButt].SetParent(self)
				self.Buttons[sButt].SetPosition(self.GetWidth() + 15, 0)
				self.Buttons[sButt].SetUpVisual(self.BASE_PATH + sButt + "_n.tga")
				self.Buttons[sButt].SetOverVisual(self.BASE_PATH + sButt + "_h.tga")
				self.Buttons[sButt].SetDownVisual(self.BASE_PATH + sButt + "_d.tga")
				self.Buttons[sButt].SAFE_SetEvent(self.__ClickButton, sButt)
				self.Buttons[sButt].Show()

				self.SetSize(self.GetWidth() + self.Buttons[sButt].GetWidth(), self.GetHeight() if self.GetHeight() > self.Buttons[sButt].GetHeight() else self.Buttons[sButt].GetHeight())

		def	__LoadDialogs(self):
			if app.TOMBOLA_EVENT_ENABLE:
				self.uiTombola = uiTombola.TombolaWindow()

		def	__ClickButton(self, sKey):
			if sKey == "button_tombola" and app.TOMBOLA_EVENT_ENABLE:
				self.uiTombola.UpdateWindow()

			elif sKey == "button_attendance" and (gcGetEnable("ATTENDANCE_MANAGER")):
				self.interface.interfaceWindowList["attendance_manager"].Open()

			elif sKey == "button_itemshop":
				net.SendChatPacket("/request_itemshop")

		def	ReplaceButtonImage(self, sKey, sNewKey):
			if sKey in self.Buttons:
				self.Buttons[sKey].SetUpVisual(self.BASE_PATH + sNewKey + "_n.tga")
				self.Buttons[sKey].SetOverVisual(self.BASE_PATH + sNewKey + "_h.tga")
				self.Buttons[sKey].SetDownVisual(self.BASE_PATH + sNewKey + "_d.tga")

		def	AddButton(self, sKey):
			if sKey in self.Buttons:
				return

			self.Buttons[sKey] = ui.Button()
			self.Buttons[sKey].SetParent(self)
			self.Buttons[sKey].SetPosition(self.GetWidth() + 20, 0)
			self.Buttons[sKey].SetUpVisual(self.BASE_PATH + sKey + "_n.tga")
			self.Buttons[sKey].SetOverVisual(self.BASE_PATH + sKey + "_h.tga")
			self.Buttons[sKey].SetDownVisual(self.BASE_PATH + sKey + "_d.tga")
			self.Buttons[sKey].SAFE_SetEvent(self.__ClickButton, sKey)
			self.Buttons[sKey].Show()

			self.SetSize(self.GetWidth() + self.Buttons[sKey].GetWidth(), self.GetHeight() if self.GetHeight() > self.Buttons[sKey].GetHeight() else self.Buttons[sKey].GetHeight())
			self.SetPosition(self.GetGlobalPosition()[0] - self.Buttons[sKey].GetWidth(), self.GetGlobalPosition()[1])

		def	RemoveButton(self, sKey):
			if not sKey in self.Buttons:
				return

			self.Buttons[sKey].Hide()

	def __init__(self):
		systemSetting.SetInterfaceHandler(self)
		self.windowOpenPosition = 0
		self.dlgWhisperWithoutTarget = None
		self.inputDialog = None
		if gcGetEnable("ENABLE_WEB_LINK"):
			self.questionDialog = None
		self.tipBoard = None
		self.bigBoard = None
		if gcGetEnable("ENABLE_LEFT_POPUP"):
			self.leftTipBoard = None

		# ITEM_MALL
		self.mallPageDlg = None
		# END_OF_ITEM_MALL

		self.wndWeb = None
		self.wndTaskBar = None
		self.wndCharacter = None
		self.wndInventory = None
		self.wndExpandedTaskBar = None
		self.wndDragonSoul = None
		self.wndDragonSoulRefine = None
		self.wndChat = None
		self.wndMessenger = None
		self.wndMiniMap = None
		self.wndGuild = None
		self.wndGuildBuilding = None

		if app.INGAME_ITEMSHOP_ENABLE:
			self.uiItemShopDialog = None

		if app.ENABLE_TELEPORT_SYSTEM:
			self.uiTeleportManagerDialog = None
			
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.wndPrivateShopPanel		= None
			self.wndPrivateShopSearch		= None
			self.privateShopTitleBoardDict = {}

		self.listGMName = {}
		self.wndQuestWindow = {}
		self.wndQuestWindowNewKey = 0
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}
		event.SetInterfaceWindow(self)

		if app.ENABLE_SPECIAL_STORAGE:
			self.wndInventoryMenu = None

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = None

		if gcGetEnable("ENABLE_INTERFACE_WINDOW_LIST"):
			self.interfaceWindowList = {}

		if app.ENABLE_VOICE_CHAT:
			self.wVoiceChat = None

		if app.ENABLE_ADMIN_MANAGER:
			self.wndAdminManager = None

		if app.ENABLE_MARBLE_CREATOR_SYSTEM:
			self.wndMarbleManager = None

		if app.BATTLE_PASS_ENABLE:
			self.wndBattlePass = None
			self.btnBattlePass = None

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			self.Transmutation_GUI = None

		if app.ENABLE_FIND_LETTERS_EVENT:
			self.wndFindLettersWindow = None
			self.wndFindLettersButton = None

		if app.ENABLE_LUCKY_BOX:
			self.wndLuckyBoxWindow = None

		if app.ENABLE_SAVE_POSITIONS_SYSTEM:
			self.wndPositionManager = None

		if app.ENABLE_RENDER_TARGET_EXTENSION:
			self.wndPreview = None

		if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
			self.wndLogsChatHandler = None
			self.wndLogsChatMain = None

		if gcGetEnable("ENABLE_SKILL_SELECT"):
			self.wndSkillSelect = None

		if gcGetEnable("ENABLE_LEGENDARY_STONES"):
			self.wndLegendaryStones = {}

		if gcGetEnable("ENABLE_DUNGEON_INFORMATION"):
			self.wndDungeonInfo = None

		if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
			self.wndExpandedMoneyBar = None

		if app.ENABLE_AMULET_SYSTEM:
			self.wndAmuletSystem = {}

		self.wndOverLayButtons = None

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow = None
			self.wndBuffNPCCreateWindow = None

		if app.ENABLE_ANTI_MULTIPLE_FARM:
			self.wndAntiMultipleFarm = None

	def __del__(self):
		systemSetting.DestroyInterfaceHandler()
		event.SetInterfaceWindow(None)

	################################
	## Make Windows & Dialogs
	def __MakeUICurtain(self):
		wndUICurtain = ui.Bar("TOP_MOST")
		wndUICurtain.SetSize(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
		wndUICurtain.SetColor(0x77000000)
		wndUICurtain.Hide()
		self.wndUICurtain = wndUICurtain

	def __MakeMessengerWindow(self):
		self.wndMessenger = uiMessenger.MessengerWindow()

		from _weakref import proxy
		self.wndMessenger.SetWhisperButtonEvent(lambda n,i=proxy(self):i.OpenWhisperDialog(n))
		self.wndMessenger.SetGuildButtonEvent(ui.__mem_func__(self.ToggleGuildWindow))

	def __MakeGuildWindow(self):
		self.wndGuild = uiGuild.GuildWindow()

	def __MakeChatWindow(self):
		CHAT_WINDOW_WIDTH = 600

		if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
			CHAT_WINDOW_WIDTH += 20

		wndChat = uiChat.ChatWindow()
		wndChat.SetSize(wndChat.CHAT_WINDOW_WIDTH, 25)
		wndChat.SetPosition(wndMgr.GetScreenWidth()/2 - wndChat.CHAT_WINDOW_WIDTH/2, wndMgr.GetScreenHeight() - wndChat.EDIT_LINE_HEIGHT - 37)
		wndChat.SetHeight(200)
		wndChat.Refresh()
		wndChat.Show()

		self.wndChat = wndChat
		self.wndChat.BindInterface(self)
		self.wndChat.SetSendWhisperEvent(ui.__mem_func__(self.OpenWhisperDialogWithoutTarget))
		self.wndChat.SetOpenChatLogEvent(ui.__mem_func__(self.ToggleChatLogWindow))

		if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
			self.__MakeNewLogsChatWindow()
			if self.wndLogsChatMain:
				self.wndChat.SetMainLogsChatWindowEvent(ui.__mem_func__(self.ToggleMainLogsChatWindow))

	if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
		def __MakeNewLogsChatWindow(self):
			#Build taskbar window
			self.wndLogsChatHandler = uiLogsChat.LogsChatHandler()
			self.wndLogsChatHandler.BindInterface(self)
			if not logsChat.GetLowResolutionSystem():
				self.wndLogsChatHandler.BuildStaticLogsLines() #This method handle the first window state (show/hide)

			#Build main window
			self.wndLogsChatMain = uiLogsChat.MainLogsChat()
			self.wndLogsChatMain.BindInterface(self)
			self.wndLogsChatMain.BindLogsChatHandler(self.wndLogsChatHandler)
			self.wndLogsChatMain.Hide()

			#Setup the system type
			lowResolutionLogs = ((self.wndLogsChatHandler.GetGlobalPosition()[0] + self.wndLogsChatHandler.GetWidth()) > self.wndChat.GetGlobalPosition()[0])\
								if self.wndChat else True
			logsChat.SetLowResolutionSystem(lowResolutionLogs)

		def ToggleMainLogsChatWindow(self):
			if not self.wndLogsChatMain:
				return

			self.wndLogsChatMain.Show() if not self.wndLogsChatMain.IsShow() else self.wndLogsChatMain.Hide()

	def __MakeTaskBar(self):
		if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
			self.wndExpandedMoneyBar = uiInventory.ExpandedMoneyBar()
			self.wndExpandedMoneyBar.SetFlexPosition(wndMgr.GetScreenWidth(), wndMgr.GetScreenHeight())
			self.ToggleCurrencieInformations(bInit = True)

		wndTaskBar = uiTaskBar.TaskBar()
		wndTaskBar.LoadWindow()
		self.wndTaskBar = wndTaskBar
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHARACTER, ui.__mem_func__(self.ToggleCharacterWindowStatusPage))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_INVENTORY, ui.__mem_func__(self.ToggleInventoryWindow))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_MESSENGER, ui.__mem_func__(self.ToggleMessenger))
		self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_SYSTEM, ui.__mem_func__(self.ToggleSystemDialog))
		if uiTaskBar.TaskBar.IS_EXPANDED:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND, ui.__mem_func__(self.ToggleChat))
			self.wndExpandedTaskBar = uiTaskBar.ExpandedTaskBar()
			self.wndExpandedTaskBar.LoadWindow()
			self.wndExpandedTaskBar.SetToggleButtonEvent(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, ui.__mem_func__(self.ToggleDragonSoulWindow))

		else:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_CHAT, ui.__mem_func__(self.ToggleChat))

		if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_EXPAND_MONEY, ui.__mem_func__(self.ToggleCurrencieInformations))
			
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_OFFLINE_SHOP, ui.__mem_func__(self.TogglePrivateShopPanelWindow))

		# if app.ENABLE_ANTI_MULTIPLE_FARM:
			# self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_ANTI_MULTIPLE_FARM, ui.__mem_func__(self.ToggleAntiMultipleFarmWindow))

	def __MakeParty(self):
		wndParty = uiParty.PartyWindow()
		wndParty.Hide()
		self.wndParty = wndParty

	def __MakeGameButtonWindow(self):
		wndGameButton = uiGameButton.GameButtonWindow()
		wndGameButton.SetTop()
		wndGameButton.Show()
		wndGameButton.SetButtonEvent("STATUS", ui.__mem_func__(self.__OnClickStatusPlusButton))
		wndGameButton.SetButtonEvent("SKILL", ui.__mem_func__(self.__OnClickSkillPlusButton))
		wndGameButton.SetButtonEvent("QUEST", ui.__mem_func__(self.__OnClickQuestButton))
		# wndGameButton.SetButtonEvent("HELP", ui.__mem_func__(self.__OnClickHelpButton))
		wndGameButton.SetButtonEvent("BUILD", ui.__mem_func__(self.__OnClickBuildButton))

		self.wndGameButton = wndGameButton

	def __IsChatOpen(self):
		return True

	def __MakeWindows(self):
		wndCharacter = uiCharacter.CharacterWindow()
		wndCharacter.BindInterfaceClass(self)
		wndInventory = uiInventory.InventoryWindow()
		wndInventory.BindInterfaceClass(self)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			wndDragonSoul = uiDragonSoul.DragonSoulWindow()
			wndDragonSoulRefine = uiDragonSoul.DragonSoulRefineWindow()
		else:
			wndDragonSoul = None
			wndDragonSoulRefine = None

		wndMiniMap = uiMiniMap.MiniMap()
		wndSafebox = uiSafebox.SafeboxWindow()
		wndSafebox.BindInterfaceClass(self)

		# ITEM_MALL
		wndMall = uiSafebox.MallWindow()
		self.wndMall = wndMall
		# END_OF_ITEM_MALL

		wndChatLog = uiChat.ChatLogWindow()
		wndChatLog.BindInterface(self)

		self.wndCharacter = wndCharacter
		self.wndInventory = wndInventory
		self.wndDragonSoul = wndDragonSoul
		self.wndDragonSoulRefine = wndDragonSoulRefine
		self.wndMiniMap = wndMiniMap
		self.wndSafebox = wndSafebox
		self.wndChatLog = wndChatLog

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)
			self.wndDragonSoul.BindInterfaceClass(self)
			self.wndDragonSoulRefine.SetInventoryWindows(self.wndInventory, self.wndDragonSoul)
			self.wndInventory.SetDragonSoulRefineWindow(self.wndDragonSoulRefine)

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot = uiSwitchbot.SwitchbotWindow()

		if app.ENABLE_SPECIAL_STORAGE:
			self.wndInventoryMenu = uiInventoryMenu.InventoryMenuWindow()
			self.wndInventoryMenu.BindInterfaceClass(self)

		if app.ENABLE_VOICE_CHAT:
			self.wVoiceChat = voiceManager.voiceManager()

		if app.ENABLE_MARBLE_CREATOR_SYSTEM:
			self.wndMarbleManager = uimarblemanager.MarbleManager()

		if app.BATTLE_PASS_ENABLE:
			self.wndBattlePass = uibattlepass.BattlePassInterface()
			self.btnBattlePass = uibattlepass.CreateBattlePassButton(self.BattlePass_ToggleWindow)

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			self.Transmutation_GUI = uiTransmutation.TransmutationWindow(self.wndInventory)

		if app.ENABLE_FIND_LETTERS_EVENT:
			self.wndFindLettersWindow = uifindletters.FindLettersWindow()
			self.wndFindLettersButton = uifindletters.FindLettersButton()
			self.wndFindLettersButton.BindInterface(self)

		if app.ENABLE_LUCKY_BOX:
			self.wndLuckyBoxWindow = uiLuckyBox.LuckyBoxWindow()
			self.wndLuckyBoxWindow.BindInterface(self)

		if app.ENABLE_SAVE_POSITIONS_SYSTEM:
			self.wndPositionManager = uipositionmanager.PositionsManagerInterface()

		if gcGetEnable("ENABLE_SKILL_SELECT"):
			self.wndSkillSelect = uiSelectSkill.SkillSelectWindow()

		if app.INGAME_ITEMSHOP_ENABLE:
			self.uiItemShopDialog = uiItemShopDialog.ItemShopDialog()

		if app.ENABLE_TELEPORT_SYSTEM:
			self.uiTeleportManagerDialog = uiteleportmanager.TeleportManagerInterface()

		if gcGetEnable("ENABLE_LEGENDARY_STONES"):
			self.wndLegendaryStones["PASSIVE"] = uiLegendaryStones.LegendaryStonesPassiveWindow()
			self.wndLegendaryStones["MINERALS"] = uiLegendaryStones.LegendaryStonesCraftingMinerals()
			self.wndLegendaryStones["SHARDS"] = uiLegendaryStones.LegendaryStonesCraftingShards()
			self.wndLegendaryStones["STONES"] = uiLegendaryStones.LegendaryStonesCraftingStones()
			self.wndLegendaryStones["REFINE"] = uiLegendaryStones.LegendaryStonesRefine()

		if gcGetEnable("ENABLE_DUNGEON_INFORMATION"):
			self.wndDungeonInfo = uiDungeonInfo.DungeonInfo()

		if app.ENABLE_AMULET_SYSTEM:
			self.wndAmuletSystem["INFORMATION"] = uiAmuletSystem.AmuletInformationClass()
			self.wndAmuletSystem["COMBINATION"] = uiAmuletSystem.AmuletCombinationClass()
			self.wndAmuletSystem["CRAFTING"] = uiAmuletSystem.AmuletCraftingClass()
			
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.wndPrivateShopPanel = uiPrivateShop.PrivateShopPanel()
			self.wndPrivateShopPanel.BindInterfaceClass(self)
			self.wndPrivateShopPanel.BindInventoryClass(self.wndInventory)
			self.wndPrivateShopPanel.BindDragonSoulInventoryClass(self.wndDragonSoul)
			
			# if app.ENABLE_SPECIAL_INVENTORY_SYSTEM:
				# self.wndPrivateShopPanel.BindSpecialInventoryClass(self.wndSpecialInventory)
			
			self.wndDragonSoul.BindPrivateShopClass(self.wndPrivateShopPanel)
			self.wndDragonSoul.BindPrivateShopSearchClass(self.wndPrivateShopSearch)
			
			self.wndPrivateShopSearch = uiPrivateShopSearch.PrivateShopSeachWindow()
			self.wndPrivateShopSearch.BindInterfaceClass(self)
			
			# self.wndInventory.BindWindow(self.wndPrivateShopPanel)
			# self.wndInventory.BindPrivateShopClass(self.wndPrivateShopPanel)
			# self.wndInventory.BindPrivateShopSearchClass(self.wndPrivateShopSearch)

		(miniX, miniY) = (wndMgr.GetScreenWidth() - 210, 0)
		self.wndOverLayButtons = self.OverLayButtonGroup(self)
		self.wndOverLayButtons.SetPosition(miniX - self.wndOverLayButtons.GetWidth() - 20, miniY + (148-self.wndOverLayButtons.GetHeight())/2)
		self.wndOverLayButtons.Show()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow = uiBuffNPC.BuffNPCWindow()
			self.wndBuffNPCCreateWindow = uiBuffNPC.BuffNPCCreateWindow()

	def __MakeDialogs(self):
		self.dlgExchange = uiExchange.ExchangeDialog(self.wndInventory)
		self.dlgExchange.BindInterface(self)
		self.dlgExchange.LoadDialog()
		self.dlgExchange.SetCenterPosition()
		self.dlgExchange.Hide()

		self.dlgPointReset = uiPointReset.PointResetDialog()
		self.dlgPointReset.LoadDialog()
		self.dlgPointReset.Hide()

		self.dlgShop = uiShop.ShopDialog()
		self.dlgShop.LoadDialog()
		if app.ENABLE_RENEWAL_SHOP_SELLING:
			self.dlgShop.BindInterface(self)
		self.dlgShop.Hide()

		self.dlgRestart = uiRestart.RestartDialog()
		self.dlgRestart.LoadDialog()
		self.dlgRestart.Hide()

		if gcGetEnable("ENABLE_REFACTORED_OPTIONS"):
			self.dlgSystem = uiRefactoredOptions.MainOptions()
			self.dlgSystem.LoadDialog()
		else:
			self.dlgSystem = uiSystem.SystemDialog()
			self.dlgSystem.LoadDialog()
			self.dlgSystem.SetOpenHelpWindowEvent(ui.__mem_func__(self.OpenHelpWindow))

		self.dlgSystem.Hide()

		self.dlgPassword = uiSafebox.PasswordDialog()
		self.dlgPassword.Hide()

		self.hyperlinkItemTooltip = uiToolTip.HyperlinkItemToolTip()
		self.hyperlinkItemTooltip.Hide()

		self.tooltipItem = uiToolTip.GetItemToolTipInstance()
		self.tooltipItem.BindInterface(self)

		self.tooltipSkill = uiToolTip.SkillToolTip()
		self.tooltipSkill.Hide()

		self.privateShopBuilder = uiPrivateShopBuilder.PrivateShopBuilder()
		self.privateShopBuilder.Hide()

		self.dlgRefineNew = uiRefine.RefineDialogNew()
		self.dlgRefineNew.Hide()

		if app.ENABLE_REFINE_ELEMENT:
			self.dlgRefineElement = uiRefineElement.RefineElementDialog()
			self.dlgRefineElement.LoadWindow()
			self.dlgRefineElement.Hide()

			self.dlgRefineElementChange = uiRefineElement.RefineElementChangeDialog()
			self.dlgRefineElementChange.LoadWindow()
			self.dlgRefineElementChange.Hide()

	def __MakeHelpWindow(self):
		self.wndHelp = uiHelp.HelpWindow()
		self.wndHelp.LoadDialog()
		self.wndHelp.SetCloseEvent(ui.__mem_func__(self.CloseHelpWindow))
		self.wndHelp.Hide()

	def __MakeTipBoard(self):
		self.tipBoard = uiTip.TipBoard()
		self.tipBoard.Hide()

		self.bigBoard = uiTip.BigBoard()
		self.bigBoard.Hide()

		if gcGetEnable("ENABLE_LEFT_POPUP"):
			self.leftTipBoard = uiTip.LeftTipBoard()
			self.leftTipBoard.Hide()

	def __MakeWebWindow(self):
		if constInfo.IN_GAME_SHOP_ENABLE:
			import uiWeb
			self.wndWeb = uiWeb.WebWindow()
			self.wndWeb.LoadWindow()
			self.wndWeb.Hide()

	def __MakeCubeWindow(self):
		if app.ENABLE_CUBE_RENEWAL:
			self.wndCube = uiCubeRenewal.CubeWindow()
			self.wndCube.LoadWindow()
			self.wndCube.BindInterface(self)
			self.wndCube.Hide()

			# self.wndInventory.SetCubeWindow(self.wndCube)

	if app.ENABLE_ANTI_MULTIPLE_FARM:
		def __MakeAntiMultipleFarmWnd(self):
			self.wndAntiMultipleFarm = uiAntiMultipleFarm.AntiMultipleFarmWnd()
			self.wndAntiMultipleFarm.Hide()

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def __MakeItemSelectWindow(self):
		self.wndItemSelect = uiSelectItem.SelectItemWindow()
		self.wndItemSelect.Hide()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	def MakeInterface(self):
		self.__MakeMessengerWindow()
		self.__MakeGuildWindow()
		self.__MakeChatWindow()
		self.__MakeParty()
		self.__MakeWindows()
		self.__MakeDialogs()

		self.__MakeUICurtain()
		self.__MakeTaskBar()
		self.__MakeGameButtonWindow()
		self.__MakeHelpWindow()
		self.__MakeTipBoard()
		self.__MakeWebWindow()
		self.__MakeCubeWindow()

		if app.ENABLE_ANTI_MULTIPLE_FARM:
			self.__MakeAntiMultipleFarmWnd()

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.__MakeItemSelectWindow()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}

		self.wndInventory.SetItemToolTip(self.tooltipItem)
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.SetItemToolTip(self.tooltipItem)
			self.wndDragonSoulRefine.SetItemToolTip(self.tooltipItem)
		self.wndSafebox.SetItemToolTip(self.tooltipItem)
		self.wndCube.SetItemToolTip(self.tooltipItem)

		# ITEM_MALL
		self.wndMall.SetItemToolTip(self.tooltipItem)
		# END_OF_ITEM_MALL

		self.wndCharacter.SetSkillToolTip(self.tooltipSkill)
		self.wndTaskBar.SetItemToolTip(self.tooltipItem)
		self.wndTaskBar.SetSkillToolTip(self.tooltipSkill)
		self.wndGuild.SetSkillToolTip(self.tooltipSkill)

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow.SetSkillToolTip(self.tooltipSkill)

		# ACCESSORY_REFINE_ADD_METIN_STONE
		self.wndItemSelect.SetItemToolTip(self.tooltipItem)
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		self.dlgShop.SetItemToolTip(self.tooltipItem)
		self.dlgExchange.SetItemToolTip(self.tooltipItem)
		self.privateShopBuilder.SetItemToolTip(self.tooltipItem)

		if gcGetEnable("ENABLE_RECOVER_WHISPERS"):
			if GetWindowConfig("system", "whisper", "WHISPERS_STORED_FOR") == "":
				self.__InitWhisper()
		else:
			self.__InitWhisper()

		self.DRAGON_SOUL_IS_QUALIFIED = True

		if gcGetEnable("ENABLE_INTERFACE_WINDOW_LIST"):
			self.__InitializeWindow()

		if app.ENABLE_SWITCHBOT:
			self.wndSwitchbot.SetItemToolTip(self.tooltipItem)

		if app.ENABLE_LUCKY_BOX:
			self.wndLuckyBoxWindow.SetItemToolTip(self.tooltipItem)
			
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.wndPrivateShopPanel.SetItemToolTip(self.tooltipItem)
			self.wndPrivateShopSearch.SetItemToolTip(self.tooltipItem)
			self.privateShopTitleBoardDict = {}

	if gcGetEnable("ENABLE_INTERFACE_WINDOW_LIST"):
		def __InitializeWindow(self):
			if app.ENABLE_TREASURE_BOX_LOOT:
				import uiBoxLoot
				wndBoxLoot = uiBoxLoot.BoxLootWindow()
				wndBoxLoot.SetItemToolTip(self.tooltipItem)
				wndBoxLoot.Close()
				self.AppendInterfaceWindow("box_loot", wndBoxLoot)

			if app.ENABLE_DELETE_SINGLE_STONE:
				import uiRemoveStone
				wndRemoveStone = uiRemoveStone.RemoveStoneWindow()
				wndRemoveStone.SetItemToolTip(self.tooltipItem)
				wndRemoveStone.Close()
				self.AppendInterfaceWindow("remove_stone", wndRemoveStone)

			if (gcGetEnable("ENABLE_SHAMAN_SYSTEM")):
				import uiShamanSystem
				wndShamanSystem = uiShamanSystem.ShamanSystemClass()
				wndShamanSystem.Close()
				self.AppendInterfaceWindow("shaman_system", wndShamanSystem)

			if (gcGetEnable("MISSION_MANAGER")):
				import uiMissionManager
				wndMissionManager = uiMissionManager.MissionManagerClass()
				wndMissionManager.Close()
				self.AppendInterfaceWindow("mission_manager", wndMissionManager)

			if (gcGetEnable("ATTENDANCE_MANAGER")):
				import uiAttendanceReward
				wndAttendanceManager = uiAttendanceReward.AttendanceManagerClass()
				wndAttendanceManager.Close()
				self.AppendInterfaceWindow("attendance_manager", wndAttendanceManager)

			if app.ENABLE_BIOLOG_SYSTEM:
				import uiBiologSystem
				wndBiologMission = uiBiologSystem.BiologMission()
				wndBiologMission.Close()

				wndBiologSelector = uiBiologSystem.BiologSelector()
				wndBiologSelector.Close()

				wndBiologSets = uiBiologSystem.BiologSets()
				wndBiologSets.Close()

				self.AppendInterfaceWindow("MISSION", wndBiologMission)
				self.AppendInterfaceWindow("SELECTOR", wndBiologSelector)
				self.AppendInterfaceWindow("SETS", wndBiologSets)

			if (gcGetEnable("MOB_TRACKER")):
				import uiMobTracker
				wndMobTracker = uiMobTracker.MobTrackerClass()
				wndMobTracker.Close()
				self.AppendInterfaceWindow("mob_tracker", wndMobTracker)

			import uiLoading
			wndLoading = uiLoading.LoadingWindow( self.gamePhaseWindow.stream.LoadingImage )
			wndLoading.SetCloseEvent( self.gamePhaseWindow.stream.SetLoginPhase )
			wndLoading.Close()
			self.AppendInterfaceWindow("loading_window", wndLoading)

		def AppendInterfaceWindow(self, name, window):
			self.interfaceWindowList[name] = window

	if app.ENABLE_TREASURE_BOX_LOOT:
		def OpenBoxLootWindow(self, itemVnum):
			self.interfaceWindowList["box_loot"].RefreshWindow(itemVnum)
			self.interfaceWindowList["box_loot"].Open()

		def CloseBoxLootWindow(self):
			self.interfaceWindowList["box_loot"].Close()

	if app.ENABLE_DELETE_SINGLE_STONE:
		def RemoveStoneSetItem(self, slotIndex):
			self.interfaceWindowList["remove_stone"].RemoveStoneSetItem(slotIndex)
			self.interfaceWindowList["remove_stone"].Open()

		def CloseRemoveStoneWindow(self):
			self.interfaceWindowList["remove_stone"].Close()

	if (gcGetEnable("ENABLE_SHAMAN_SYSTEM")):
		def OpenShamanSystem(self):
			self.interfaceWindowList["shaman_system"].Open()

		def RegisterShamansSlots(self, iCount):
			self.interfaceWindowList["shaman_system"].RegisterShamanSlots(iCount)

		def RegisterShamanSkill(self, iKey, iType, iLevel, fPower):
			self.interfaceWindowList["shaman_system"].RegisterShamanSkill(iKey, iType, iLevel, fPower)

		def RegisterShamanPremium(self, bPremium):
			self.interfaceWindowList["shaman_system"].RegisterShamanPremium(bPremium)

		def UnregisterShamanSystem(self):
			self.interfaceWindowList["shaman_system"].UnregisterShaman()
			self.interfaceWindowList["shaman_system"].Close()

	if (gcGetEnable("MISSION_MANAGER")):
		def OpenMissionManager(self):
			self.interfaceWindowList["mission_manager"].Open()

		def MissionManagerClear(self):
			self.interfaceWindowList["mission_manager"].OnRecvClear()

		def MissionManagerRegisterTask(self, iKey, iTime, iTaskID, iProgress, dwEnemy, iCount):
			self.interfaceWindowList["mission_manager"].OnRecvTask(iKey, iTime, iTaskID, iProgress, dwEnemy, iCount)

		def MissionManagerRefreshTask(self, iKey, iTaskID, iProgress):
			self.interfaceWindowList["mission_manager"].OnRecvTaskRefresh(iKey, iTaskID, iProgress)

		def MissionManagerRegisterReward(self, iKey, iTaskID, iPos, iVnum, iCount):
			self.interfaceWindowList["mission_manager"].OnRecvReward(iKey, iTaskID, iPos, iVnum, iCount)

		def MissionManagerRefresh(self):
			self.interfaceWindowList["mission_manager"].OnRecvRefresh()

	if app.ENABLE_BIOLOG_SYSTEM:
		def BiologManagerRegisterProgress(self, iKey, iCollected, tTime, bReminder):
			self.interfaceWindowList["MISSION"].RegisterMissionProgress(iKey, iCollected, tTime, bReminder)

		def BiologManagerRegisterMission(self, iLevel, iVnum, iCount, iChance):
			self.interfaceWindowList["MISSION"].RegisterMission(iLevel, iVnum, iCount, iChance)

		def BiologManagerRegisterRewardBasic(self, iVnum, iCount, bSelector):
			self.interfaceWindowList["MISSION"].RegisterRewardBasic(iVnum, iCount, bSelector)
		
		def BiologManagerRegisterRewardAffect(self, sKey, iKey, iType, iValue):
			if not self.interfaceWindowList.has_key(sKey):
				return

			self.interfaceWindowList[sKey].RegisterRewardAffect(iKey, iType, iValue)

		def BiologManagerRequestOpen(self, sKey, iKey):
			if not self.interfaceWindowList.has_key(sKey):
				return

			self.interfaceWindowList[sKey].RegisterComponents()

			self.interfaceWindowList[sKey].OpenWindow()

		def BiologManagerRequestClose(self, sKey):
			if not self.interfaceWindowList.has_key(sKey):
				return

			self.interfaceWindowList[sKey].Close()

		def BiologManagerRequestClear(self, sKey):
			if not self.interfaceWindowList.has_key(sKey):
				return

			self.interfaceWindowList[sKey].RequestClear()
			self.interfaceWindowList[sKey].Close()

		def BiologManagerRegisterSet(self, iKey, bFinished, bSelector, iVnum, iLevel):
			self.interfaceWindowList["SETS"].RegisterSet(iKey, bFinished, bSelector, iVnum, iLevel)
		
		def BiologManagerRegisterSetAffect(self, iKey, iApplyKey, bSelected, iApplyType, iApplyValue):
			self.interfaceWindowList["SETS"].RegisterSetApply(iKey, iApplyKey, bSelected, iApplyType, iApplyValue)
		
		def BiologManagerClearSet(self):
			self.interfaceWindowList["SETS"].ClearSet()

		def BiologManagerOpenSet(self):
			self.interfaceWindowList["SETS"].OpenWindow()

	def MakeHyperlinkTooltip(self, hyperlink):
		tokens = hyperlink.split(":")
		if tokens and len(tokens):
			type = tokens[0]
			if "item" == type:
				if app.ENABLE_RENDER_TARGET_EXTENSION:
					if app.IsPressed(app.DIK_LCONTROL) or app.IsPressed(app.DIK_RCONTROL):
						if len(tokens) >= 2:
							minTokenCount = 4 + player.METIN_SOCKET_MAX_NUM
							maxTokenCount = minTokenCount + 2 * player.ATTRIBUTE_SLOT_MAX_NUM
							if tokens and len(tokens) >= minTokenCount and len(tokens) <= maxTokenCount:
								head, vnum, refineElement, flag = tokens[:4]
								if app.ENABLE_TRANSMUTATION_SYSTEM:
									itemVnum = str(vnum)
								else:
									itemVnum = int(vnum, 16)

								metinSlot = [int(metin, 16) for metin in tokens[4:10]]

								if app.ENABLE_TRANSMUTATION_SYSTEM:
									abc = itemVnum.split("|")
									itemVnum = int(abc[0], 16)
									lookvnum = int(abc[1])

								self.OpenPreviewWindow(lookvnum if lookvnum > 0 else itemVnum)
					else:
						self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)
				else:
					self.hyperlinkItemTooltip.SetHyperlinkItem(tokens)

			elif "player" == type:
				self.OpenWhisperDialog(str(tokens[1]))
			elif "link" == type and gcGetEnable("ENABLE_WEB_LINK"):
				self.OpenWebLinkQuestionDialog(hyperlink[5:])

			print "Received msg hyperlink (%s) [Type: %s]" % (hyperlink, type)

	## Make Windows & Dialogs
	################################

	def Close(self):
		if self.dlgWhisperWithoutTarget:
			self.dlgWhisperWithoutTarget.Destroy()
			del self.dlgWhisperWithoutTarget

		if gcGetEnable("ENABLE_RECOVER_WHISPERS"):
			for name in self.whisperDialogDict:
				self.__MakeWhisperButton(name)

		if uiQuest.QuestDialog.__dict__.has_key("QuestCurtain"):
			uiQuest.QuestDialog.QuestCurtain.Close()

		if self.wndQuestWindow:
			for key, eachQuestWindow in self.wndQuestWindow.items():
				eachQuestWindow.nextCurtainMode = -1
				eachQuestWindow.CloseSelf()
				eachQuestWindow = None
		self.wndQuestWindow = {}

		if self.wndChat:
			self.wndChat.Hide()
			self.wndChat.Destroy()

		if self.wndTaskBar:
			self.wndTaskBar.Hide()
			self.wndTaskBar.Destroy()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.Hide()
			self.wndExpandedTaskBar.Destroy()

		if self.wndCharacter:
			self.wndCharacter.Hide()
			self.wndCharacter.Destroy()

		if self.wndInventory:
			self.wndInventory.Hide()
			self.wndInventory.Destroy()

		if self.wndDragonSoul:
			self.wndDragonSoul.Hide()
			self.wndDragonSoul.Destroy()

		if self.wndDragonSoulRefine:
			self.wndDragonSoulRefine.Hide()
			self.wndDragonSoulRefine.Destroy()

		if self.dlgExchange:
			self.dlgExchange.Hide()
			self.dlgExchange.Destroy()

		if self.dlgPointReset:
			self.dlgPointReset.Hide()
			self.dlgPointReset.Destroy()

		if self.dlgShop:
			self.dlgShop.Hide()
			self.dlgShop.Destroy()

		if self.dlgRestart:
			self.dlgRestart.Hide()
			self.dlgRestart.Destroy()

		if self.dlgSystem:
			self.dlgSystem.Hide()
			self.dlgSystem.Destroy()

		if self.dlgPassword:
			self.dlgPassword.Hide()
			self.dlgPassword.Destroy()

		if self.wndMiniMap:
			self.wndMiniMap.Hide()
			self.wndMiniMap.Destroy()

		if self.wndSafebox:
			self.wndSafebox.Hide()
			self.wndSafebox.Destroy()

		if self.wndWeb:
			self.wndWeb.Hide()
			self.wndWeb.Destroy()
			self.wndWeb = None

		if self.wndMall:
			self.wndMall.Hide()
			self.wndMall.Destroy()

		if self.wndParty:
			self.wndParty.Hide()
			self.wndParty.Destroy()

		if self.wndHelp:
			self.wndHelp.Hide()
			self.wndHelp.Destroy()

		if self.wndCube:
			self.wndCube.Hide()
			self.wndCube.Destroy()

		if self.wndMessenger:
			self.wndMessenger.Hide()
			self.wndMessenger.Destroy()

		if self.wndGuild:
			self.wndGuild.Hide()
			self.wndGuild.Destroy()

		if self.privateShopBuilder:
			self.privateShopBuilder.Hide()
			self.privateShopBuilder.Destroy()

		if self.dlgRefineNew:
			self.dlgRefineNew.Hide()
			self.dlgRefineNew.Destroy()

		if self.wndGuildBuilding:
			self.wndGuildBuilding.Hide()
			self.wndGuildBuilding.Destroy()

		if self.wndGameButton:
			self.wndGameButton.Hide()
			self.wndGameButton.Destroy()

		# ITEM_MALL
		if self.mallPageDlg:
			self.mallPageDlg.Hide()
			self.mallPageDlg.Destroy()
		# END_OF_ITEM_MALL

		# ACCESSORY_REFINE_ADD_METIN_STONE
		if self.wndItemSelect:
			self.wndItemSelect.Hide()
			self.wndItemSelect.Destroy()
		# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.Destroy()
			if self.wndBuffNPCCreateWindow:
				self.wndBuffNPCCreateWindow.Destroy()

		self.wndChatLog.Hide()
		self.wndChatLog.Destroy()

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndInventoryMenu:
				self.wndInventoryMenu.Destroy()

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Destroy()

		if app.ENABLE_VOICE_CHAT:
			if self.wVoiceChat:
				self.wVoiceChat.Destroy()

		if app.ENABLE_ADMIN_MANAGER:
			if self.wndAdminManager:
				self.wndAdminManager.Destroy()

		if app.ENABLE_MARBLE_CREATOR_SYSTEM:
			if self.wndMarbleManager:
				self.wndMarbleManager.Destroy()

		if app.BATTLE_PASS_ENABLE:
			if self.wndBattlePass:
				self.wndBattlePass.Destroy()

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			if self.Transmutation_GUI:
				self.Transmutation_GUI.Destroy()

		if app.ENABLE_FIND_LETTERS_EVENT:
			if self.wndFindLettersWindow:
				self.wndFindLettersWindow.Destroy()

			if self.wndFindLettersButton:
				self.wndFindLettersButton.Destroy()

		if app.ENABLE_REFINE_ELEMENT:
			if self.dlgRefineElement:
				self.dlgRefineElement.Destroy()
				del self.dlgRefineElement

			if self.dlgRefineElementChange:
				self.dlgRefineElementChange.Destroy()
				del self.dlgRefineElementChange

		if app.ENABLE_LUCKY_BOX:
			if self.wndLuckyBoxWindow:
				self.wndLuckyBoxWindow.Hide()
				self.wndLuckyBoxWindow.Destroy()

		if app.ENABLE_SAVE_POSITIONS_SYSTEM:
			if self.wndPositionManager:
				self.wndPositionManager.Destroy()

		if app.ENABLE_RENDER_TARGET_EXTENSION:
			if self.wndPreview:
				self.wndPreview.Hide()
				self.wndPreview.Destroy()

		if app.INGAME_ITEMSHOP_ENABLE:
			if self.uiItemShopDialog:
				self.uiItemShopDialog.Hide()

		if app.ENABLE_TELEPORT_SYSTEM:
			if self.uiTeleportManagerDialog:
				self.uiTeleportManagerDialog.Hide()

		if gcGetEnable("ENABLE_DUNGEON_INFORMATION"):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Hide()
				self.wndDungeonInfo.Destroy()

		if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
			if self.wndLogsChatHandler:
				self.wndLogsChatHandler.Hide()
				self.wndLogsChatHandler.Destroy()

			if self.wndLogsChatMain:
				self.wndLogsChatMain.Hide()
				self.wndLogsChatMain.Destroy()

		if gcGetEnable("ENABLE_SKILL_SELECT"):
			if self.wndSkillSelect:
				self.wndSkillSelect.Destroy()

		if gcGetEnable("ENABLE_WEB_LINK"):
			if self.questionDialog:
				self.__CloseQuestionDialog()

		if gcGetEnable("ENABLE_LEGENDARY_STONES"):
			if self.wndLegendaryStones:
				for wnd in self.wndLegendaryStones.values():
					wnd.Destroy()

		if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Hide()
				self.wndExpandedMoneyBar.Destroy()

		if app.ENABLE_AMULET_SYSTEM:
			if self.wndAmuletSystem:
				for wnd in self.wndAmuletSystem.values():
					wnd.Destroy()
					
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Hide()
				self.wndPrivateShopPanel.Destroy()
				
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Hide()
				self.wndPrivateShopSearch.Destroy()

			del self.wndPrivateShopPanel
			del self.wndPrivateShopSearch
			self.privateShopTitleBoardDict = {}

		if app.ENABLE_ANTI_MULTIPLE_FARM:
			if self.wndAntiMultipleFarm:
				self.wndAntiMultipleFarm.Hide()
				self.wndAntiMultipleFarm.Destroy()

		for btn in self.questButtonList:
			btn.SetEvent(0)
		for btn in self.whisperButtonList:
			btn.SetEvent(0)
		for dlg in self.whisperDialogDict.itervalues():
			dlg.Destroy()
		for brd in self.guildScoreBoardDict.itervalues():
			brd.Destroy()
		for dlg in self.equipmentDialogDict.itervalues():
			dlg.Destroy()

		# ITEM_MALL
		del self.mallPageDlg
		# END_OF_ITEM_MALL

		del self.wndGuild
		del self.wndMessenger
		del self.wndUICurtain
		del self.wndChat
		del self.wndTaskBar
		if self.wndExpandedTaskBar:
			del self.wndExpandedTaskBar
		del self.wndCharacter
		del self.wndInventory
		if self.wndDragonSoul:
			del self.wndDragonSoul
		if self.wndDragonSoulRefine:
			del self.wndDragonSoulRefine
		del self.dlgExchange
		del self.dlgPointReset
		del self.dlgShop
		del self.dlgRestart
		del self.dlgSystem
		del self.dlgPassword
		del self.hyperlinkItemTooltip
		del self.tooltipItem
		del self.tooltipSkill
		del self.wndMiniMap
		del self.wndSafebox
		del self.wndMall
		del self.wndParty
		del self.wndHelp
		del self.wndCube
		del self.privateShopBuilder
		del self.inputDialog
		del self.wndChatLog
		del self.dlgRefineNew
		del self.wndGuildBuilding
		del self.wndGameButton
		del self.tipBoard
		del self.bigBoard
		if gcGetEnable("ENABLE_LEFT_POPUP"):
			del self.leftTipBoard

		del self.wndItemSelect

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndInventoryMenu:
				del self.wndInventoryMenu

		if app.ENABLE_SWITCHBOT:
			del self.wndSwitchbot

		if app.ENABLE_VOICE_CHAT:
			del self.wVoiceChat

		if app.ENABLE_ADMIN_MANAGER:
			del self.wndAdminManager

		if gcGetEnable("ENABLE_RECOVER_WHISPERS"):
			if len(self.whisperButtonList) > 0:
				UpdateConfig("whisper", "WHISPERS_STORED_FOR", player.GetName())
				for btn in self.whisperButtonList:
					GetWindowConfig("system", "whisper", "WHISPERS_STORAGE").append(btn.name)

		if app.ENABLE_MARBLE_CREATOR_SYSTEM:
			del self.wndMarbleManager

		if app.BATTLE_PASS_ENABLE:
			if self.wndBattlePass:
				del self.wndBattlePass
				del self.btnBattlePass

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			del self.Transmutation_GUI

		if app.ENABLE_FIND_LETTERS_EVENT:
			if self.wndFindLettersWindow:
				del self.wndFindLettersWindow

			if self.wndFindLettersButton:
				del self.wndFindLettersButton

		if app.ENABLE_LUCKY_BOX:
			if self.wndLuckyBoxWindow:
				del self.wndLuckyBoxWindow

		if app.ENABLE_SAVE_POSITIONS_SYSTEM:
			if self.wndPositionManager:
				del self.wndPositionManager

		if app.ENABLE_RENDER_TARGET_EXTENSION:
			del self.wndPreview

		if app.INGAME_ITEMSHOP_ENABLE:
			del self.uiItemShopDialog

		if app.ENABLE_TELEPORT_SYSTEM:
			del self.uiTeleportManagerDialog

		if gcGetEnable("ENABLE_DUNGEON_INFORMATION"):
			del self.wndDungeonInfo

		if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
			del self.wndLogsChatHandler
			del self.wndLogsChatMain

		if gcGetEnable("ENABLE_SKILL_SELECT"):
			del self.wndSkillSelect

		if gcGetEnable("ENABLE_WEB_LINK"):
			del self.questionDialog

		if gcGetEnable("ENABLE_LEGENDARY_STONES"):
			for wnd in self.wndLegendaryStones.values():
				del wnd

		if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
			del self.wndExpandedMoneyBar

		if app.ENABLE_AMULET_SYSTEM:
			for wnd in self.wndAmuletSystem.values():
				del wnd

		del self.wndOverLayButtons

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			del self.wndBuffNPCWindow
			del self.wndBuffNPCCreateWindow

		if app.ENABLE_ANTI_MULTIPLE_FARM:
			del self.wndAntiMultipleFarm

		self.questButtonList = []
		self.whisperButtonList = []
		self.whisperDialogDict = {}
		self.privateShopAdvertisementBoardDict = {}
		self.guildScoreBoardDict = {}
		self.equipmentDialogDict = {}

		uiChat.DestroyChatInputSetWindow()

		if gcGetEnable("ENABLE_INTERFACE_WINDOW_LIST"):
			map(lambda wnd : wnd[1].Destroy(), self.interfaceWindowList.iteritems())
			self.interfaceWindowList = {}

		self.gamePhaseWindow = None

	def RepositionGroup(self, height):
		self.wndParty.SetPosition(10, 17 + height)
		self.wndParty.ArrangeReposition()

	## Skill
	def OnUseSkill(self, slotIndex, coolTime):
		self.wndCharacter.OnUseSkill(slotIndex, coolTime)
		self.wndTaskBar.OnUseSkill(slotIndex, coolTime)
		self.wndGuild.OnUseSkill(slotIndex, coolTime)

	def OnActivateSkill(self, slotIndex):
		self.wndCharacter.OnActivateSkill(slotIndex)
		self.wndTaskBar.OnActivateSkill(slotIndex)

	def OnDeactivateSkill(self, slotIndex):
		self.wndCharacter.OnDeactivateSkill(slotIndex)
		self.wndTaskBar.OnDeactivateSkill(slotIndex)

	def OnChangeCurrentSkill(self, skillSlotNumber):
		self.wndTaskBar.OnChangeCurrentSkill(skillSlotNumber)

	if app.SKILL_COOLTIME_UPDATE:
		def	SkillClearCoolTime(self, slotIndex):
			self.wndCharacter.SkillClearCoolTime(slotIndex)
			self.wndTaskBar.SkillClearCoolTime(slotIndex)

	def SelectMouseButtonEvent(self, dir, event):
		self.wndTaskBar.SelectMouseButtonEvent(dir, event)

	## Refresh
	def RefreshAlignment(self):
		self.wndCharacter.RefreshAlignment()

	def RefreshStatus(self):
		self.wndTaskBar.RefreshStatus()
		self.wndCharacter.RefreshStatus()
		self.wndInventory.RefreshStatus()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshStatus()
			
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			if self.wndPrivateShopPanel.IsShow():
				self.wndPrivateShopPanel.Refresh()

	def RefreshStamina(self):
		self.wndTaskBar.RefreshStamina()

	def RefreshSkill(self):
		self.wndCharacter.RefreshSkill()
		self.wndTaskBar.RefreshSkill()

	def RefreshInventory(self):
		self.wndTaskBar.RefreshQuickSlot()
		self.wndInventory.RefreshItemSlot()
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.RefreshItemSlot()
		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			self.wndBuffNPCWindow.RefreshEquipSlotWindow()

	def RefreshCharacter(self):
		self.wndCharacter.RefreshCharacter()
		self.wndTaskBar.RefreshQuickSlot()

	def RefreshQuest(self):
		self.wndCharacter.RefreshQuest()

	def RefreshSafebox(self):
		self.wndSafebox.RefreshSafebox()

	# ITEM_MALL
	def RefreshMall(self):
		self.wndMall.RefreshMall()

	def OpenItemMall(self):
		if not self.mallPageDlg:
			self.mallPageDlg = uiShop.MallPageDialog()

		self.mallPageDlg.Open()
	# END_OF_ITEM_MALL

	def RefreshMessenger(self):
		self.wndMessenger.RefreshMessenger()

	def RefreshGuildInfoPage(self):
		self.wndGuild.RefreshGuildInfoPage()

	def RefreshGuildBoardPage(self):
		self.wndGuild.RefreshGuildBoardPage()

	def RefreshGuildMemberPage(self):
		self.wndGuild.RefreshGuildMemberPage()

	def RefreshGuildMemberPageGradeComboBox(self):
		self.wndGuild.RefreshGuildMemberPageGradeComboBox()

	def RefreshGuildSkillPage(self):
		self.wndGuild.RefreshGuildSkillPage()

	def RefreshGuildGradePage(self):
		self.wndGuild.RefreshGuildGradePage()

	def DeleteGuild(self):
		self.wndMessenger.ClearGuildMember()
		self.wndGuild.DeleteGuild()

	def RefreshMobile(self):
		self.dlgSystem.RefreshMobile()

	def OnMobileAuthority(self):
		self.dlgSystem.OnMobileAuthority()

	def OnBlockMode(self, mode):
		self.dlgSystem.OnBlockMode(mode)

	## Calling Functions
	# PointReset
	def OpenPointResetDialog(self):
		self.dlgPointReset.Show()
		self.dlgPointReset.SetTop()

	def ClosePointResetDialog(self):
		self.dlgPointReset.Close()

	# Shop
	def OpenShopDialog(self, vid):
		if not self.wndInventory.IsShow():
			self.wndInventory.Show()
			self.wndInventory.SetTop()
		self.dlgShop.Open(vid)
		self.dlgShop.SetTop()

	def CloseShopDialog(self):
		self.dlgShop.Close()

	def RefreshShopDialog(self):
		self.dlgShop.Refresh()

	## Quest
	def OpenCharacterWindowQuestPage(self):
		self.wndCharacter.Show()
		self.wndCharacter.SetState("QUEST")

	def OpenQuestWindow(self, skin, idx):

		wnds = ()

		q = uiQuest.QuestDialog(skin, idx)
		q.SetWindowName("QuestWindow" + str(idx))

		if gcGetEnable("ENABLE_FIX_LCONTROL_QUEST"):
			self.HideMouseImage()

		q.Show()
		if skin:
			q.Lock()
			wnds = self.__HideWindows()

			# UNKNOWN_UPDATE
			q.AddOnDoneEvent(lambda tmp_self, args=wnds: self.__ShowWindows(args))
			# END_OF_UNKNOWN_UPDATE

		if skin:
			q.AddOnCloseEvent(q.Unlock)
		q.AddOnCloseEvent(lambda key = self.wndQuestWindowNewKey:ui.__mem_func__(self.RemoveQuestDialog)(key))
		self.wndQuestWindow[self.wndQuestWindowNewKey] = q

		self.wndQuestWindowNewKey = self.wndQuestWindowNewKey + 1

		# END_OF_UNKNOWN_UPDATE

	def RemoveQuestDialog(self, key):
		del self.wndQuestWindow[key]

	## Exchange
	def StartExchange(self):
		self.dlgExchange.OpenDialog()
		self.dlgExchange.Refresh()

	def EndExchange(self):
		self.dlgExchange.CloseDialog()

	def RefreshExchange(self):
		self.dlgExchange.Refresh()

	if gcGetEnable("ENABLE_FAST_INTERACTION_EXCHANGE"):
		def GetExchangeWindow(self):
			return self.dlgExchange

	if app.ENABLE_RENEWAL_EXCHANGE:
		def ExchangeInfo(self, unixTime, info, isError):
			self.dlgExchange.AppendInformation(unixTime, info, isError)

	if app.ENABLE_ADMIN_MANAGER:
		def AdminManager_Init(self):
			if not admin.CanOpenWindow():
				return

			# self.wndTaskBar.SetToggleButtonEvent(uiTaskBar.TaskBar.BUTTON_ADMIN, ui.__mem_func__(self.ToggleAdminManagerWindow))
			# self.wndTaskBar.ShowAdminButton()

		def AdminManager_PlayerOnline(self, pid):
			if self.wndAdminManager:
				self.wndAdminManager.OnPlayerOnline(pid)

		def AdminManager_PlayerOffline(self, pid):
			if self.wndAdminManager:
				self.wndAdminManager.OnPlayerOffline(pid)

		def AdminManager_RefreshGMItemTradeOption(self):
			if self.wndAdminManager:
				self.wndAdminManager.GENERAL_RefreshGMItemTradeOption()

		def AdminManager_RefreshMapViewer(self):
			if self.wndAdminManager:
				self.wndAdminManager.MAPVIEWER_RefreshPage()

		def AdminManager_StartObserver(self):
			if self.wndAdminManager:
				self.wndAdminManager.OBSERVER_OnStart()

		def AdminManager_Refresh(self):
			if self.wndAdminManager:
				self.wndAdminManager.OBSERVER_RefreshPage()
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ADMIN_MANAGER_OBSERVER_RESTARTED % self.wndAdminManager.OBSERVER_GetName())

		def AdminManager_RefreshSkill(self):
			if self.wndAdminManager:
				self.wndAdminManager.OBSERVER_RefreshSkill()

		def AdminManager_PointChange(self):
			if self.wndAdminManager:
				self.wndAdminManager.OBSERVER_OnPointChange()

		def AdminManager_RefreshInventory(self, pageIndex):
			if self.wndAdminManager:
				self.wndAdminManager.OBSERVER_RefreshInventory(pageIndex)

		def AdminManager_RefreshEquipment(self):
			if self.wndAdminManager:
				self.wndAdminManager.OBSERVER_RefreshEquipment()

		def AdminManager_RefreshBanChatPlayer(self, pid):
			if self.wndAdminManager:
				self.wndAdminManager.BAN_ChatRefreshPlayer(pid)

		def AdminManager_ChatSearchResult(self, success):
			if self.wndAdminManager:
				self.wndAdminManager.BAN_ChatLoadResult(success)

		def AdminManager_RefreshBanAccount(self, aid):
			if self.wndAdminManager:
				self.wndAdminManager.BAN_AccountRefreshSingle(aid)

		def AdminManager_AccountSearchResult(self, success):
			if self.wndAdminManager:
				self.wndAdminManager.BAN_AccountLoadResult(success)

		def AdminManager_LoadBanLog(self):
			if self.wndAdminManager:
				self.wndAdminManager.BAN_LoadLog()

		def AdminManager_LoadItemResult(self):
			if self.wndAdminManager:
				self.wndAdminManager.ITEM_ShowResult()

		def AdminManager_LoadHackLogResult(self):
			if self.wndAdminManager:
				self.wndAdminManager.LOGS_ShowResult()

		def AdminManager_OnUpdate(self):
			if self.wndAdminManager and not self.wndAdminManager.IsShow():
				self.wndAdminManager.OnUpdate()

		def ToggleAdminManagerWindow(self):
			if self.wndAdminManager and self.wndAdminManager.IsShow():
				self.CloseAdminManagerWindow()
			else:
				self.OpenAdminManagerWindow()

		def OpenAdminManagerWindow(self):
			if not admin.CanOpenWindow():
				return

			if not self.wndAdminManager:
				self.wndAdminManager = uiAdminManager.AdminManagerWindow()
				self.wndAdminManager.Initialize()
			self.wndAdminManager.Open()

		def CloseAdminManagerWindow(self):
			if self.wndAdminManager:
				self.wndAdminManager.Close()

	## Party
	def AddPartyMember(self, pid, name):
		self.wndParty.AddPartyMember(pid, name)

		self.__ArrangeQuestButton()

	def UpdatePartyMemberInfo(self, pid):
		self.wndParty.UpdatePartyMemberInfo(pid)

	def RemovePartyMember(self, pid):
		self.wndParty.RemovePartyMember(pid)

		self.__ArrangeQuestButton()

	def LinkPartyMember(self, pid, vid):
		self.wndParty.LinkPartyMember(pid, vid)

	def UnlinkPartyMember(self, pid):
		self.wndParty.UnlinkPartyMember(pid)

	def UnlinkAllPartyMember(self):
		self.wndParty.UnlinkAllPartyMember()

	def ExitParty(self):
		self.wndParty.ExitParty()

		self.__ArrangeQuestButton()

	def PartyHealReady(self):
		self.wndParty.PartyHealReady()

	def ChangePartyParameter(self, distributionMode):
		self.wndParty.ChangePartyParameter(distributionMode)

	## Safebox
	def AskSafeboxPassword(self):
		if self.wndSafebox.IsShow():
			return

		# SAFEBOX_PASSWORD
		self.dlgPassword.SetTitle(localeInfo.PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/safebox_password ")
		# END_OF_SAFEBOX_PASSWORD

		self.dlgPassword.ShowDialog()

	def OpenSafeboxWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndSafebox.ShowWindow(size)

	def CommandCloseSafebox(self):
		self.wndSafebox.CommandCloseSafebox()

	## SafeBox Support
	if gcGetEnable("ENABLE_FAST_INTERACTION_SAFEBOX"):
		def GetSafeboxWindow(self):
			return self.wndSafebox

	# ITEM_MALL
	def AskMallPassword(self):
		if self.wndMall.IsShow():
			return
		self.dlgPassword.SetTitle(localeInfo.MALL_PASSWORD_TITLE)
		self.dlgPassword.SetSendMessage("/mall_password ")
		self.dlgPassword.ShowDialog()

	def OpenMallWindow(self, size):
		self.dlgPassword.CloseDialog()
		self.wndMall.ShowWindow(size)

	def CommandCloseMall(self):
		self.wndMall.CommandCloseMall()
	# END_OF_ITEM_MALL

	## Guild
	def OnStartGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnStartGuildWar(guildSelf, guildOpp)

		guildWarScoreBoard = uiGuild.GuildWarScoreBoard()
		guildWarScoreBoard.Open(guildSelf, guildOpp)
		guildWarScoreBoard.Show()
		self.guildScoreBoardDict[uiGuild.GetGVGKey(guildSelf, guildOpp)] = guildWarScoreBoard

	def OnEndGuildWar(self, guildSelf, guildOpp):
		self.wndGuild.OnEndGuildWar(guildSelf, guildOpp)

		key = uiGuild.GetGVGKey(guildSelf, guildOpp)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].Destroy()
		del self.guildScoreBoardDict[key]

	# GUILDWAR_MEMBER_COUNT
	def UpdateMemberCount(self, gulidID1, memberCount1, guildID2, memberCount2):
		key = uiGuild.GetGVGKey(gulidID1, guildID2)

		if not self.guildScoreBoardDict.has_key(key):
			return

		self.guildScoreBoardDict[key].UpdateMemberCount(gulidID1, memberCount1, guildID2, memberCount2)
	# END_OF_GUILDWAR_MEMBER_COUNT

	def OnRecvGuildWarPoint(self, gainGuildID, opponentGuildID, point):
		key = uiGuild.GetGVGKey(gainGuildID, opponentGuildID)
		if not self.guildScoreBoardDict.has_key(key):
			return

		guildBoard = self.guildScoreBoardDict[key]
		guildBoard.SetScore(gainGuildID, opponentGuildID, point)

	## PK Mode
	def OnChangePKMode(self):
		self.wndCharacter.RefreshAlignment()
		self.dlgSystem.OnChangePKMode()

	## Refine
	if app.ENABLE_FAST_REFINE_OPTION:
		def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type, can_fast_refine, addPercent, bSashRefine):
			self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type, can_fast_refine, addPercent, bSashRefine)

		def CloseRefinedDialog(self):
			if not self.dlgRefineNew:
				return

			self.dlgRefineNew.Close()
	else:
		def OpenRefineDialog(self, targetItemPos, nextGradeItemVnum, cost, prob, type):
			self.dlgRefineNew.Open(targetItemPos, nextGradeItemVnum, cost, prob, type)

	def AppendMaterialToRefineDialog(self, vnum, count):
		self.dlgRefineNew.AppendMaterial(vnum, count)

	if app.ENABLE_REFINE_ELEMENT:
		def RefineElementProcess(self, refineType, srcCell, dstCell):
			if refineType == item.REFINE_ELEMENT_TYPE_UPGRADE:
				if self.dlgRefineElement:
					self.dlgRefineElement.OpenRefine(srcCell, dstCell, item.REFINE_ELEMENT_TYPE_UPGRADE)
			elif refineType == item.REFINE_ELEMENT_TYPE_DOWNGRADE:
				if self.dlgRefineElement:
					self.dlgRefineElement.OpenRefine(srcCell, dstCell, item.REFINE_ELEMENT_TYPE_DOWNGRADE)
			elif refineType == item.REFINE_ELEMENT_TYPE_CHANGE:
				if self.dlgRefineElementChange:
					self.dlgRefineElementChange.Open(srcCell, dstCell)

	## Show & Hide
	def ShowDefaultWindows(self):
		windows = [
			self.wndTaskBar,
			self.wndMiniMap,
		]

		for window in windows:
			if window:
				window.Show()

		self.wndMiniMap.ShowMiniMap()
		if self.wndOverLayButtons:
			self.wndOverLayButtons.Show()

	def ShowAllWindows(self):
		windows = [
			self.wndTaskBar,
			self.wndCharacter,
			self.wndInventory,
			self.wndDragonSoul,
			self.wndDragonSoulRefine,
			self.wndChat,
			self.wndMiniMap,
			self.wndExpandedTaskBar
		]

		for window in windows:
			if window:
				window.Show()

		if self.wndExpandedTaskBar:
			self.wndExpandedTaskBar.SetTop()

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndInventoryMenu:
				self.wndInventoryMenu.Show()

		if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
			if self.wndLogsChatHandler:
				self.wndLogsChatHandler.Show()

			if self.wndLogsChatMain:
				self.wndLogsChatMain.Show()

		if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Show()

	def HideAllWindows(self):
		windows = [
			self.wndTaskBar,
			self.wndInventory,
			self.wndDragonSoul,
			self.wndDragonSoulRefine,
			self.wndChat,
			self.wndMiniMap,
			self.wndMessenger,
			self.wndGuild,
			self.wndExpandedTaskBar
		]

		for window in windows:
			if window:
				window.Hide()

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndInventoryMenu:
				self.wndInventoryMenu.Hide()

		if app.ENABLE_SWITCHBOT:
			if self.wndSwitchbot:
				self.wndSwitchbot.Hide()

		if app.ENABLE_MARBLE_CREATOR_SYSTEM:
			if self.wndMarbleManager:
				self.wndMarbleManager.Hide()

		if app.BATTLE_PASS_ENABLE:
			self.wndBattlePass.Hide()
			self.btnBattlePass.Hide()

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			self.Transmutation_GUI.Hide()

		if app.ENABLE_SAVE_POSITIONS_SYSTEM:
			if self.wndPositionManager:
				self.wndPositionManager.Hide()

		if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
			if self.wndLogsChatHandler:
				self.wndLogsChatHandler.Hide()

			if self.wndLogsChatMain:
				self.wndLogsChatMain.Hide()

		if gcGetEnable("ENABLE_SKILL_SELECT"):
			if self.wndSkillSelect:
				self.wndSkillSelect.Hide()

		if app.INGAME_ITEMSHOP_ENABLE:
			self.uiItemShopDialog.Hide()

		if app.ENABLE_TELEPORT_SYSTEM:
			self.uiTeleportManagerDialog.Hide()

		if gcGetEnable("ENABLE_DUNGEON_INFORMATION"):
			if self.wndDungeonInfo:
				self.wndDungeonInfo.Hide()

		if gcGetEnable("ENABLE_LEGENDARY_STONES"):
			if self.wndLegendaryStones:
				for wnd in self.wndLegendaryStones.values():
					wnd.Hide()

		if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
			if self.wndExpandedMoneyBar:
				self.wndExpandedMoneyBar.Hide()

		if app.ENABLE_AMULET_SYSTEM:
			if self.wndAmuletSystem:
				for wnd in self.wndAmuletSystem.values():
					wnd.Hide()

		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			self.wndPrivateShopPanel.Hide()
			self.wndPrivateShopSearch.Hide()

		closeWindows = [
			self.wndCharacter,
			self.wndCube
		]

		if app.ENABLE_ANTI_MULTIPLE_FARM:
			if self.wndAntiMultipleFarm:
				self.wndAntiMultipleFarm.Hide()

		for window in closeWindows:
			if window:
				window.Close()

		if gcGetEnable("ENABLE_INTERFACE_WINDOW_LIST"):
			map(lambda wnd : wnd[1].Close(), self.interfaceWindowList.iteritems())

		if self.wndOverLayButtons:
			self.wndOverLayButtons.Hide()

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.Hide()
			if self.wndBuffNPCCreateWindow:
				self.wndBuffNPCCreateWindow.Hide()

	def ShowMouseImage(self):
		self.wndTaskBar.ShowMouseImage()

	def HideMouseImage(self):
		self.wndTaskBar.HideMouseImage()

	def ToggleChat(self):
		if True == self.wndChat.IsEditMode():
			self.wndChat.CloseChat()
		else:
			if self.wndWeb and self.wndWeb.IsShow():
				pass

			if gcGetEnable("ENABLE_HAND_SWITCHER"):
				if self.wndInventory and self.wndInventory.HandSwitcher and\
					self.wndInventory.HandSwitcher.HandleReturnButton():
						return

			if gcGetEnable("ENABLE_REFINE_ENTER_ABLE") and self.dlgRefineNew and self.dlgRefineNew.IsShow() and self.dlgRefineNew.HandleReturnButton():
				return

			if app.SASH_ABSORPTION_ENABLE and uisashsystem.IS_OPEN_COMBINATION and uisashsystem.SashCombination().HandleReturnButton():
				return

			if self.wndDragonSoulRefine and self.wndDragonSoulRefine.IsShow() and self.wndDragonSoulRefine.HandleReturnButton():
				return

			else:
				self.wndChat.OpenChat()

	def IsOpenChat(self):
		return self.wndChat.IsEditMode()

	def SetChatFocus(self):
		self.wndChat.SetChatFocus()

	if app.ENABLE_RENEWAL_DEAD_PACKET:
		def OpenRestartDialog(self, d_time):
			self.dlgRestart.OpenDialog(d_time)
			self.dlgRestart.SetTop()
	else:
		def OpenRestartDialog(self):
			self.dlgRestart.OpenDialog()
			self.dlgRestart.SetTop()

	def CloseRestartDialog(self):
		self.dlgRestart.Close()

	def ToggleSystemDialog(self):
		if False == self.dlgSystem.IsShow():
			self.dlgSystem.OpenDialog()
			self.dlgSystem.SetTop()
		else:
			self.dlgSystem.Close()

	def OpenSystemDialog(self):
		self.dlgSystem.OpenDialog()
		self.dlgSystem.SetTop()

	def ToggleMessenger(self):
		if self.wndMessenger.IsShow():
			self.wndMessenger.Hide()
		else:
			self.wndMessenger.SetTop()
			self.wndMessenger.Show()

	def ToggleMiniMap(self):
		if app.IsPressed(app.DIK_LSHIFT) or app.IsPressed(app.DIK_RSHIFT):
			if False == self.wndMiniMap.isShowMiniMap():
				self.wndMiniMap.ShowMiniMap()
				self.wndMiniMap.SetTop()
			else:
				self.wndMiniMap.HideMiniMap()

		else:
			self.wndMiniMap.ToggleAtlasWindow()

	def PressMKey(self):
		if app.IsPressed(app.DIK_LALT) or app.IsPressed(app.DIK_RALT):
			self.ToggleMessenger()

		else:
			self.ToggleMiniMap()

	def SetMapName(self, mapName):
		self.wndMiniMap.SetMapName(mapName)

	def MiniMapScaleUp(self):
		self.wndMiniMap.ScaleUp()

	def MiniMapScaleDown(self):
		self.wndMiniMap.ScaleDown()

	def ToggleCharacterWindow(self, state):
		if False == player.IsObserverMode():
			if False == self.wndCharacter.IsShow():
				self.OpenCharacterWindowWithState(state)
			else:
				if state == self.wndCharacter.GetState():
					self.wndCharacter.OverOutItem()
					self.wndCharacter.Hide()
				else:
					self.wndCharacter.SetState(state)

	def OpenCharacterWindowWithState(self, state):
		if False == player.IsObserverMode():
			self.wndCharacter.SetState(state)
			self.wndCharacter.Show()
			self.wndCharacter.SetTop()

	def ToggleCharacterWindowStatusPage(self):
		self.ToggleCharacterWindow("STATUS")

	if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
		def BuffNPC_OpenCreateWindow(self):
			if self.wndBuffNPCWindow:
				if False == self.wndBuffNPCCreateWindow.IsShow():
					self.wndBuffNPCCreateWindow.Show()
					self.wndBuffNPCCreateWindow.SetTop()
				
		def BuffNPCOpenWindow(self):
			if self.wndBuffNPCWindow:
				if False == self.wndBuffNPCWindow.IsShow():
					self.wndBuffNPCWindow.Show()
					self.wndBuffNPCWindow.SetTop()
				else:
					self.wndBuffNPCWindow.Close()
				
		def BuffNPC_Summon(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSummon()
				self.wndBuffNPCWindow.Show()
				self.wndBuffNPCWindow.SetTop()
				
		def BuffNPC_Unsummon(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetUnsummon()
				
		def BuffNPC_Clear(self):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetClear()
				
		def BuffNPC_SetBasicInfo(self, name, sex, intvalue):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetBasicInfo(name, sex, intvalue)
				
		def BuffNPC_SetEXPInfo(self, level, cur_exp, exp):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetEXPInfo(level, cur_exp, exp)
				
		def BuffNPC_SetSkillInfo(self, skill1, skill2, skill3, skill4, skill5, skill6, skillpoints):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSkillInfo(skill1, skill2, skill3, skill4, skill5, skill6, skillpoints)
				
		def BuffNPC_SkillUseStatus(self, slot0, slot1, slot2, slot3, slot4, slot5):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSkillUseStatus(slot0, slot1, slot2, slot3, slot4, slot5)
				
		def BuffNPC_SetSkillCooltime(self, slot, timevalue):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.SetSkillCooltime(slot, timevalue)
		
		def BuffNPC_CreatePopup(self, type, value0, value1):
			if self.wndBuffNPCWindow:
				self.wndBuffNPCWindow.CreatePopup(type, value0, value1)

	def ToggleInventoryWindow(self):
		if False == player.IsObserverMode():
			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()
				self.wndInventory.SetTop()
				if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
					self.ToggleCurrencieInformations(True)
			else:
				self.wndInventory.OverOutItem()
				self.wndInventory.Close()
				if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
					self.ToggleCurrencieInformations(True)

	if gcGetEnable("ENABLE_FAST_INTERACTIONS"):
		def GetInventory(self):
			return self.wndInventory

	def ToggleExpandedButton(self):
		if False == player.IsObserverMode():
			if False == self.wndExpandedTaskBar.IsShow():
				self.wndExpandedTaskBar.Show()
				self.wndExpandedTaskBar.SetTop()
			else:
				self.wndExpandedTaskBar.Close()

	def DragonSoulActivate(self, deck):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.ActivateDragonSoulByExtern(deck)

	def CurrentDragonSoul(self):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			return self.wndDragonSoul.isActivated, self.wndDragonSoul.deckPageIndex

	def DragonSoulDeactivate(self):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.DeactivateDragonSoul()

	def DragonSoulActivateByKey(self):
		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			self.wndDragonSoul.ActivateButtonClickByKey()
	
	if app.ENABLE_DS_SET:
		def DragonSoulSetActivate(self, iSetType):
			if not self.wndDragonSoul:
				return

			self.wndDragonSoul.ActivateSet(iSetType)

		def DragonSoulSetDeactivate(self):
			if not self.wndDragonSoul:
				return

			self.wndDragonSoul.DeactivateSet()

	def Highligt_Item(self, inven_type, inven_pos):
		if (gcGetEnable("ENABLE_OPTIONS_HIGHLIGHT_ITEM")):
			if cfg.Get(cfg.SAVE_OPTION, "config_highlight_item", "1") == "0":
				return

		if player.DRAGON_SOUL_INVENTORY == inven_type:
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				self.wndDragonSoul.HighlightSlot(inven_pos)

		elif app.ENABLE_HIGHLIGHT_NEW_ITEM and player.SLOT_TYPE_INVENTORY == inven_type:
			self.wndInventory.HighlightSlot(inven_pos)

	def DragonSoulGiveQuilification(self):
		self.DRAGON_SOUL_IS_QUALIFIED = True
		self.wndExpandedTaskBar.SetToolTipText(uiTaskBar.ExpandedTaskBar.BUTTON_DRAGON_SOUL, uiScriptLocale.TASKBAR_DRAGON_SOUL)

	def ToggleDragonSoulWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					if self.DRAGON_SOUL_IS_QUALIFIED:
						self.wndDragonSoul.Show()
					else:
						try:
							self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
							self.wndPopupDialog.SetAutoClose()
							self.wndPopupDialog.Open()
						except:
							self.wndPopupDialog = uiCommon.PopupDialog()
							self.wndPopupDialog.SetText(localeInfo.DRAGON_SOUL_UNQUALIFIED)
							self.wndPopupDialog.SetAutoClose()
							self.wndPopupDialog.Open()
				else:
					self.wndDragonSoul.Close()

	def ToggleDragonSoulWindowWithNoInfo(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoul.IsShow():
					if self.DRAGON_SOUL_IS_QUALIFIED:
						self.wndDragonSoul.Show()
				else:
					self.wndDragonSoul.Close()

	def FailDragonSoulRefine(self, reason, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineFail(reason, inven_type, inven_pos)

	def SucceedDragonSoulRefine(self, inven_type, inven_pos):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.RefineSucceed(inven_type, inven_pos)

	def OpenDragonSoulRefineWindow(self):
		if app.ENABLE_DS_SET:
			if self.wndDragonSoul.dsIgnoreCallback:
				self.wndDragonSoul.dsIgnoreCallback = False
				return

		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if False == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Show()
					if None != self.wndDragonSoul:
						if False == self.wndDragonSoul.IsShow():
							self.wndDragonSoul.Show()

	def CloseDragonSoulRefineWindow(self):
		if False == player.IsObserverMode():
			if app.ENABLE_DRAGON_SOUL_SYSTEM:
				if True == self.wndDragonSoulRefine.IsShow():
					self.wndDragonSoulRefine.Close()


	def ToggleGuildWindow(self):
		if not self.wndGuild.IsShow():
			if self.wndGuild.CanOpen():
				self.wndGuild.Open()
			else:
				chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.GUILD_YOU_DO_NOT_JOIN)
		else:
			self.wndGuild.OverOutItem()
			self.wndGuild.Hide()

	def ToggleChatLogWindow(self):
		if self.wndChatLog.IsShow():
			self.wndChatLog.Hide()
		else:
			self.wndChatLog.Show()

	if app.ENABLE_SWITCHBOT:
		def ToggleSwitchbotWindow(self):
			if self.wndSwitchbot.IsShow():
				self.wndSwitchbot.Close()
			else:
				self.wndSwitchbot.Open()

		def RefreshSwitchbotWindow(self):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotWindow()

		def RefreshSwitchbotItem(self, slot):
			if self.wndSwitchbot and self.wndSwitchbot.IsShow():
				self.wndSwitchbot.RefreshSwitchbotItem(slot)

	if app.ENABLE_SPECIAL_STORAGE:
		def ToggleInventoryMenuWindow(self):
			if False == player.IsObserverMode():
				if False == self.wndInventoryMenu.IsShow():
					self.wndInventoryMenu.Show()
					self.wndInventoryMenu.SetTop()
				else:
					self.wndInventoryMenu.Close()

	def CheckGameButton(self):
		if self.wndGameButton:
			self.wndGameButton.CheckGameButton()

	def __OnClickStatusPlusButton(self):
		self.ToggleCharacterWindow("STATUS")

	def __OnClickSkillPlusButton(self):
		self.ToggleCharacterWindow("SKILL")

	def __OnClickQuestButton(self):
		self.ToggleCharacterWindow("QUEST")

	# def __OnClickHelpButton(self):
	# 	player.SetPlayTime(1)
	# 	self.CheckGameButton()
	# 	self.OpenHelpWindow()

	def __OnClickBuildButton(self):
		self.BUILD_OpenWindow()

	def OpenHelpWindow(self):
		self.wndUICurtain.Show()
		self.wndHelp.Open()

	def CloseHelpWindow(self):
		self.wndUICurtain.Hide()
		self.wndHelp.Close()

	def OpenWebWindow(self, url):
		self.wndWeb.Open(url)
		self.wndChat.CloseChat()

	# show GIFT
	def ShowGift(self):
		self.wndTaskBar.ShowGift()

	def CloseWbWindow(self):
		self.wndWeb.Close()

	if app.ENABLE_CUBE_RENEWAL:
		def OpenCubeWindow(self, npcVnum):
			self.wndCube.Open(npcVnum)

			if False == self.wndInventory.IsShow():
				self.wndInventory.Show()

		def CloseCubeWindow(self):
			self.wndCube.Close()

		def RefreshCubeWindow(self):
			self.wndCube.Refresh()

		if constInfo.ENABLE_CUBE_MARK_MATERIAL:
			def IsCubeMaterial(self, invenSlot):
				if self.wndCube and self.wndCube.IsMaterial(invenSlot):
					return True

				return False

			def RefreshCubeInventoryBag(self):
				if self.wndInventory:
					self.wndInventory.RefreshBagSlotWindow()

	def __HideWindows(self):
		hideWindows = self.wndTaskBar,\
						self.wndCharacter,\
						self.wndInventory,\
						self.wndMiniMap,\
						self.wndGuild,\
						self.wndMessenger,\
						self.wndChat,\
						self.wndParty,\
						self.wndGameButton,

		if self.wndExpandedTaskBar:
			hideWindows += self.wndExpandedTaskBar,

		if app.ENABLE_DRAGON_SOUL_SYSTEM:
			hideWindows += self.wndDragonSoul,\
						self.wndDragonSoulRefine,

		if gcGetEnable("ENABLE_INTERFACE_WINDOW_LIST"):
			for index, window in enumerate(self.interfaceWindowList):
				hideWindows += self.interfaceWindowList[window],

		if app.ENABLE_SWITCHBOT and self.wndSwitchbot:
			hideWindows += self.wndSwitchbot,
			
		if app.ENABLE_PREMIUM_PRIVATE_SHOP:
			hideWindows += self.wndPrivateShopPanel,\
						self.wndPrivateShopSearch

		if app.ENABLE_SPECIAL_STORAGE:
			if self.wndInventoryMenu:
				hideWindows += self.wndInventoryMenu,

		if app.BATTLE_PASS_ENABLE:
			hideWindows += self.wndBattlePass,\
						self.btnBattlePass,

		if app.ENABLE_TRANSMUTATION_SYSTEM:
			hideWindows += self.Transmutation_GUI,

		if app.ENABLE_FIND_LETTERS_EVENT:
			if self.wndFindLettersWindow and self.wndFindLettersButton:
				hideWindows += self.wndFindLettersWindow,
				hideWindows += self.wndFindLettersButton,

		if app.ENABLE_REFINE_ELEMENT:
			if self.dlgRefineElement:
				hideWindows += self.dlgRefineElement,

			if self.dlgRefineElementChange:
				hideWindows += self.dlgRefineElementChange,

		if app.ENABLE_LUCKY_BOX:
			if self.wndLuckyBoxWindow:
				hideWindows += self.wndLuckyBoxWindow,

		if app.ENABLE_SAVE_POSITIONS_SYSTEM:
			if self.wndPositionManager:
				hideWindows += self.wndPositionManager,

		if (gcGetEnable("ENABLE_NEW_LOGS_CHAT")):
			if self.wndLogsChatHandler:
				hideWindows += self.wndLogsChatHandler,

			if self.wndLogsChatMain:
				hideWindows += self.wndLogsChatMain,

		if gcGetEnable("ENABLE_SKILL_SELECT"):
			if self.wndSkillSelect:
				hideWindows += self.wndSkillSelect,

		if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
			if self.wndExpandedMoneyBar:
				hideWindows += self.wndExpandedMoneyBar,

		hideWindows += self.wndOverLayButtons,

		if app.ENABLE_ASLAN_BUFF_NPC_SYSTEM:
			if self.wndBuffNPCWindow:
				hideWindows += self.wndBuffNPCWindow,
			if self.wndBuffNPCCreateWindow:
				hideWindows += self.wndBuffNPCCreateWindow,

		if app.ENABLE_ANTI_MULTIPLE_FARM and self.wndAntiMultipleFarm:
			hideWindows += self.wndAntiMultipleFarm,

		hideWindows = filter(lambda x:x.IsShow(), hideWindows)
		map(lambda x:x.Hide(), hideWindows)

		self.HideAllQuestButton()
		self.HideAllWhisperButton()

		if self.wndChat.IsEditMode():
			self.wndChat.CloseChat()

		return hideWindows

	def __ShowWindows(self, wnds):
		map(lambda x:x.Show(), wnds)
		global IsQBHide
		if not IsQBHide:
			self.ShowAllQuestButton()
		else:
			self.HideAllQuestButton()

		self.ShowAllWhisperButton()

	def BINARY_OpenAtlasWindow(self):
		if self.wndMiniMap:
			self.wndMiniMap.ShowAtlas()

	def BINARY_SetObserverMode(self, flag):
		self.wndGameButton.SetObserverMode(flag)

	# ACCESSORY_REFINE_ADD_METIN_STONE
	def BINARY_OpenSelectItemWindow(self):
		self.wndItemSelect.Open()
	# END_OF_ACCESSORY_REFINE_ADD_METIN_STONE

	#####################################################################################
	### Private Shop ###

	def OpenPrivateShopInputNameDialog(self):
		#if player.IsInSafeArea():
		#	chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.CANNOT_OPEN_PRIVATE_SHOP_IN_SAFE_AREA)
		#	return

		inputDialog = uiCommon.InputDialog()
		inputDialog.SetTitle(localeInfo.PRIVATE_SHOP_INPUT_NAME_DIALOG_TITLE)
		inputDialog.SetMaxLength(32)
		inputDialog.SetAcceptEvent(ui.__mem_func__(self.OpenPrivateShopBuilder))
		inputDialog.SetCancelEvent(ui.__mem_func__(self.ClosePrivateShopInputNameDialog))
		inputDialog.Open()
		self.inputDialog = inputDialog

	def ClosePrivateShopInputNameDialog(self):
		self.inputDialog = None
		return True

	def OpenPrivateShopBuilder(self):

		if not self.inputDialog:
			return True

		if not len(self.inputDialog.GetText()):
			return True

		self.privateShopBuilder.Open(self.inputDialog.GetText())
		self.ClosePrivateShopInputNameDialog()
		return True

	def AppearPrivateShop(self, vid, text):

		board = uiPrivateShopBuilder.PrivateShopAdvertisementBoard()
		board.Open(vid, text)

		self.privateShopAdvertisementBoardDict[vid] = board

	def DisappearPrivateShop(self, vid):

		if not self.privateShopAdvertisementBoardDict.has_key(vid):
			return

		del self.privateShopAdvertisementBoardDict[vid]
		uiPrivateShopBuilder.DeleteADBoard(vid)

	#####################################################################################
	### Equipment ###

	def OpenEquipmentDialog(self, vid):
		dlg = uiEquipmentDialog.EquipmentDialog()
		dlg.SetItemToolTip(self.tooltipItem)
		dlg.SetCloseEvent(ui.__mem_func__(self.CloseEquipmentDialog))
		dlg.Open(vid)

		self.equipmentDialogDict[vid] = dlg

	def SetEquipmentDialogItem(self, vid, slotIndex, vnum, count):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogItem(slotIndex, vnum, count)

	def SetEquipmentDialogSocket(self, vid, slotIndex, socketIndex, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogSocket(slotIndex, socketIndex, value)

	def SetEquipmentDialogAttr(self, vid, slotIndex, attrIndex, type, value):
		if not vid in self.equipmentDialogDict:
			return
		self.equipmentDialogDict[vid].SetEquipmentDialogAttr(slotIndex, attrIndex, type, value)

	def CloseEquipmentDialog(self, vid):
		if not vid in self.equipmentDialogDict:
			return
		del self.equipmentDialogDict[vid]

	#####################################################################################

	#####################################################################################
	### Quest ###
	def BINARY_ClearQuest(self, index):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

	def RecvQuest(self, index, name):
		# QUEST_LETTER_IMAGE
		self.BINARY_RecvQuest(index, name, "file", localeInfo.GetLetterImageName())
		# END_OF_QUEST_LETTER_IMAGE

	def BINARY_RecvQuest(self, index, name, iconType, iconName):
		btn = self.__FindQuestButton(index)
		if 0 != btn:
			self.__DestroyQuestButton(btn)

		btn = uiWhisper.WhisperButton()

		# QUEST_LETTER_IMAGE
		import item
		if "item"==iconType:
			item.SelectItem(int(iconName))
			buttonImageFileName=item.GetIconImageFileName()
		else:
			buttonImageFileName=iconName

		if iconName and (iconType not in ("item", "file")): # type "ex" implied
			btn.SetUpVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName.replace("open", "close")))
			btn.SetOverVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
			btn.SetDownVisual("d:/ymir work/ui/game/quest/questicon/%s" % (iconName))
		else:
			btn.SetUpVisual(localeInfo.GetLetterCloseImageName())
			btn.SetOverVisual(localeInfo.GetLetterOpenImageName())
			btn.SetDownVisual(localeInfo.GetLetterOpenImageName())
		# END_OF_QUEST_LETTER_IMAGE

		if not app.ENABLE_QUEST_RENEWAL:
			btn.SetToolTipText(name, -20, 35)
			btn.ToolTipText.SetHorizontalAlignLeft()

			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
			btn.Show()
		else:
			btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)

		listOfTypes = iconType.split(",")
		if "blink" in listOfTypes:
			btn.Flash()

		listOfColors = {
			"golden":	0xFFffa200,
			"green":	0xFF00e600,
			"blue":		0xFF0099ff,
			"purple":	0xFFcc33ff,

			"fucsia":	0xFFcc0099,
			"aqua":		0xFF00ffff,
		}
		for k,v in listOfColors.iteritems():
			if k in listOfTypes:
				btn.ToolTipText.SetPackedFontColor(v)

		# btn.SetEvent(ui.__mem_func__(self.__StartQuest), btn)
		# btn.Show()

		btn.index = index
		btn.name = name

		self.questButtonList.insert(0, btn)
		self.__ArrangeQuestButton()

	def __ArrangeQuestButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		if self.wndParty.IsShow():
			xPos = 100 + 50
		else:
			xPos = 40

		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63

		count = 0
		for btn in self.questButtonList:
			if app.ENABLE_QUEST_RENEWAL:
				btn.SetToolTipText(localeInfo.QUEST_RENEWAL_MISSION_COUNT % str(len(self.questButtonList)))
				btn.ToolTipText.SetHorizontalAlignCenter()

			btn.SetPosition(xPos + (int(count/yCount) * 100), yPos + (count%yCount * 63))
			count += 1

			global IsQBHide
			if IsQBHide:
				btn.Hide()
			else:
				if count > 1:
					btn.Hide()
				else:
					btn.Show()

	def __StartQuest(self, btn):
		if app.ENABLE_QUEST_RENEWAL:
			self.__OnClickQuestButton()
			self.HideAllQuestButton()
		else:
			event.QuestButtonClick(btn.index)
			self.__DestroyQuestButton(btn)
	def __FindQuestButton(self, index):
		for btn in self.questButtonList:
			if btn.index == index:
				return btn

		return 0

	def __DestroyQuestButton(self, btn):
		btn.SetEvent(0)
		self.questButtonList.remove(btn)
		self.__ArrangeQuestButton()

	def HideAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Hide()

	def ShowAllQuestButton(self):
		for btn in self.questButtonList:
			btn.Show()
			if app.ENABLE_QUEST_RENEWAL:
				break
	#####################################################################################

	#####################################################################################
	### Whisper ###

	def OpenWebLinkQuestionDialog(self, link):
		dlg = uiCommon.QuestionDialogMultiLine()
		dlg.SetText(localeInfo.OPEN_RANDOM_LINK_QUESTION % constInfo.WEB_LINK_REPLACE(link))
		dlg.SetAcceptEvent(lambda arg=link: self.__OpenWebLink(link))
		dlg.SetCancelEvent(self.__CloseQuestionDialog)
		dlg.Open()

		self.questionDialog = dlg

	def __OpenWebLink(self, link):
		self.__CloseQuestionDialog()

		import webbrowser
		webbrowser.open(link)

	def __CloseQuestionDialog(self):
		self.questionDialog.Close()
		self.questionDialog.SetAcceptEvent(None)

		self.questionDialog = None

	def __InitWhisper(self):
		chat.InitWhisper(self)

	def OpenWhisperDialogWithoutTarget(self):
		if not self.dlgWhisperWithoutTarget:
			dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
			dlgWhisper.BindInterface(self)
			dlgWhisper.LoadDialog()
			dlgWhisper.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)
			dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
			dlgWhisper.Show()
			self.dlgWhisperWithoutTarget = dlgWhisper

			self.windowOpenPosition = (self.windowOpenPosition+1) % 5
		else:
			self.dlgWhisperWithoutTarget.SetTop()
			self.dlgWhisperWithoutTarget.OpenWithoutTarget(self.RegisterTemporaryWhisperDialog)

	def RegisterTemporaryWhisperDialog(self, name):
		if not self.dlgWhisperWithoutTarget:
			return

		btn = self.__FindWhisperButton(name)
		if 0 != btn:
			self.__DestroyWhisperButton(btn)

		elif self.whisperDialogDict.has_key(name):
			oldDialog = self.whisperDialogDict[name]
			oldDialog.Destroy()
			del self.whisperDialogDict[name]

		self.whisperDialogDict[name] = self.dlgWhisperWithoutTarget
		self.dlgWhisperWithoutTarget.OpenWithTarget(name)
		self.dlgWhisperWithoutTarget = None
		self.__CheckGameMaster(name)

	def OpenWhisperDialog(self, name, iLocale = -1):
		if not self.whisperDialogDict.has_key(name):
			dlg = self.__MakeWhisperDialog(name)
			dlg.OpenWithTarget(name, iLocale)
			dlg.chatLine.SetFocus()
			dlg.Show()

			self.__CheckGameMaster(name)
			btn = self.__FindWhisperButton(name)
			if 0 != btn:
				self.__DestroyWhisperButton(btn)

	def RecvWhisper(self, name, iLocale = -1):
		if not self.whisperDialogDict.has_key(name):
			btn = self.__FindWhisperButton(name)
			if 0 == btn:
				btn = self.__MakeWhisperButton(name, iLocale)
				btn.Flash()

				chat.AppendChat(chat.CHAT_TYPE_NOTICE, localeInfo.RECEIVE_MESSAGE % (name))

			else:
				btn.Flash()
		else:
			dlg = self.whisperDialogDict[name]
			if self.IsGameMasterName(name):
				dlg.SetGameMasterLook()
			
			if iLocale != -1:
				dlg.RefreshLanguage(iLocale)

	if app.MULTI_LANGUAGE_SYSTEM_FLAG_VISIBILITY:
		def RecvWhisperLanguage(self, name, iLocale):
			if not self.whisperDialogDict.has_key(name):
				btn = self.__FindWhisperButton(name)
				if btn:
					btn.lang = iLocale

			else:
				dlg = self.whisperDialogDict[name]
				dlg.RefreshLanguage(iLocale)

	def MakeWhisperButton(self, name):
		self.__MakeWhisperButton(name)

	def ShowWhisperDialog(self, btn):
		try:
			self.__MakeWhisperDialog(btn.name)
			dlgWhisper = self.whisperDialogDict[btn.name]
			dlgWhisper.OpenWithTarget(btn.name, btn.lang)
			dlgWhisper.Show()
			self.__CheckGameMaster(btn.name)
		except:
			import dbg
			dbg.TraceError("interface.ShowWhisperDialog - Failed to find key")

		self.__DestroyWhisperButton(btn)

	def MinimizeWhisperDialog(self, name, lang):

		if 0 != name:
			self.__MakeWhisperButton(name, lang)

		self.CloseWhisperDialog(name)

	def CloseWhisperDialog(self, name):

		if 0 == name:

			if self.dlgWhisperWithoutTarget:
				self.dlgWhisperWithoutTarget.Destroy()
				self.dlgWhisperWithoutTarget = None

			return

		try:
			dlgWhisper = self.whisperDialogDict[name]
			dlgWhisper.Destroy()
			del self.whisperDialogDict[name]
		except:
			import dbg
			dbg.TraceError("interface.CloseWhisperDialog - Failed to find key")

	def __ArrangeWhisperButton(self):

		screenWidth = wndMgr.GetScreenWidth()
		screenHeight = wndMgr.GetScreenHeight()

		xPos = screenWidth - 70
		yPos = 170 * screenHeight / 600
		yCount = (screenHeight - 330) / 63
		#yCount = (screenHeight - 285) / 63

		count = 0
		for button in self.whisperButtonList:

			button.SetPosition(xPos + (int(count/yCount) * -50), yPos + (count%yCount * 63))
			count += 1

	def __FindWhisperButton(self, name):
		for button in self.whisperButtonList:
			if button.name == name:
				return button

		return 0

	def __MakeWhisperDialog(self, name):
		dlgWhisper = uiWhisper.WhisperDialog(self.MinimizeWhisperDialog, self.CloseWhisperDialog)
		dlgWhisper.BindInterface(self)
		dlgWhisper.LoadDialog()
		dlgWhisper.SetPosition(self.windowOpenPosition*30,self.windowOpenPosition*30)
		self.whisperDialogDict[name] = dlgWhisper

		self.windowOpenPosition = (self.windowOpenPosition+1) % 5

		return dlgWhisper

	def __MakeWhisperButton(self, name, iLocale = -1):
		if app.ENABLE_RENEWAL_EXCHANGE:
			if "$" in name:
				return

		whisperButton = uiWhisper.WhisperButton()
		whisperButton.SetUpVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetOverVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		whisperButton.SetDownVisual("d:/ymir work/ui/game/windows/btn_mail_up.sub")
		if self.IsGameMasterName(name):
			whisperButton.SetToolTipTextWithColor(name, 0xffffa200)
		else:
			whisperButton.SetToolTipText(name)
		whisperButton.ToolTipText.SetHorizontalAlignCenter()
		whisperButton.SetEvent(ui.__mem_func__(self.ShowWhisperDialog), whisperButton)
		whisperButton.Show()
		whisperButton.name = name

		whisperButton.lang = iLocale

		self.whisperButtonList.insert(0, whisperButton)
		self.__ArrangeWhisperButton()

		return whisperButton

	def __DestroyWhisperButton(self, button):
		button.SetEvent(0)
		self.whisperButtonList.remove(button)
		self.__ArrangeWhisperButton()

	def HideAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Hide()

	def ShowAllWhisperButton(self):
		for btn in self.whisperButtonList:
			btn.Show()

	def __CheckGameMaster(self, name):
		if not self.listGMName.has_key(name):
			return
		if self.whisperDialogDict.has_key(name):
			dlg = self.whisperDialogDict[name]
			dlg.SetGameMasterLook()

	def RegisterGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return
		self.listGMName[name] = "GM"

	def IsGameMasterName(self, name):
		if self.listGMName.has_key(name):
			return True
		else:
			return False

	if gcGetEnable("ENABLE_RECOVER_WHISPERS"):
		def RecoverWhispers(self):
			if GetWindowConfig("system", "whisper", "WHISPERS_STORED_FOR") == player.GetName():
				for playerName in GetWindowConfig("system", "whisper", "WHISPERS_STORAGE"):
					self.__MakeWhisperButton(playerName)

				self.ShowAllWhisperButton()
			else:
				chat.DestroyWhisper()

			# Reset (recovery was ok: already used - recovery was not ok: drop them anyway)
			UpdateConfig("whisper", "WHISPERS_STORAGE", [])
			UpdateConfig("whisper", "WHISPERS_STORED_FOR", "")

	if app.ENABLE_ANTI_MULTIPLE_FARM:
		def ToggleAntiMultipleFarmWindow(self):
			if not self.wndAntiMultipleFarm:
				return
			
			if anti_multiple_farm.GetAntiFarmPlayerCount() <= anti_multiple_farm.MULTIPLE_FARM_MAX_ACCOUNT:
				try:
					self.wndPopupDialog.SetText(localeInfo.ANTI_MULTIPLE_FARM_MESSAGE.format(anti_multiple_farm.MULTIPLE_FARM_MAX_ACCOUNT+1))
					self.wndPopupDialog.Open()
				except:
					self.wndPopupDialog = uiCommon.PopupDialog()
					self.wndPopupDialog.SetText(localeInfo.ANTI_MULTIPLE_FARM_MESSAGE.format(anti_multiple_farm.MULTIPLE_FARM_MAX_ACCOUNT+1))
					self.wndPopupDialog.Open()
				return
			
			isShow = self.wndAntiMultipleFarm.IsShow()
			self.wndAntiMultipleFarm.Close() if isShow else self.wndAntiMultipleFarm.Open()
		
		def SendAntiFarmReload(self):
			if self.wndTaskBar:
				self.wndTaskBar.ReloadAntiMultipleFarmState()
			
			if self.wndAntiMultipleFarm.IsShow():
				self.wndAntiMultipleFarm.OnRefreshData()

				if self.wndAntiMultipleFarm.page_manage_mode != self.wndAntiMultipleFarm.VIEW_MODE:
					chat.AppendChat(chat.CHAT_TYPE_INFO, localeInfo.ANTI_MULTIPLE_FARM_REFRESHED)
		
		def RegistItemGive(self, itemVnum, itemCount):
			if not self.wndGiveItem:
				return
			
			self.wndGiveItem.Open(itemVnum, itemCount)

	#####################################################################################

	#####################################################################################
	### Guild Building ###

	def BUILD_OpenWindow(self):
		self.wndGuildBuilding = uiGuild.BuildGuildBuildingWindow()
		self.wndGuildBuilding.Open()
		self.wndGuildBuilding.wnds = self.__HideWindows()
		self.wndGuildBuilding.SetCloseEvent(ui.__mem_func__(self.BUILD_CloseWindow))

	def BUILD_CloseWindow(self):
		self.__ShowWindows(self.wndGuildBuilding.wnds)
		self.wndGuildBuilding = None

	def BUILD_OnUpdate(self):
		if not self.wndGuildBuilding:
			return

		if self.wndGuildBuilding.IsPositioningMode():
			import background
			x, y, z = background.GetPickingPoint()
			self.wndGuildBuilding.SetBuildingPosition(x, y, z)

	def BUILD_OnMouseLeftButtonDown(self):
		if not self.wndGuildBuilding:
			return

		# GUILD_BUILDING
		if self.wndGuildBuilding.IsPositioningMode():
			self.wndGuildBuilding.SettleCurrentPosition()
			return True
		elif self.wndGuildBuilding.IsPreviewMode():
			pass
		else:
			return True
		# END_OF_GUILD_BUILDING
		return False

	def BUILD_OnMouseLeftButtonUp(self):
		if not self.wndGuildBuilding:
			return

		if not self.wndGuildBuilding.IsPreviewMode():
			return True

		return False

	def BULID_EnterGuildArea(self, areaID):
		# GUILD_BUILDING
		mainCharacterName = player.GetMainCharacterName()
		masterName = guild.GetGuildMasterName()

		if mainCharacterName != masterName:
			return

		if areaID != player.GetGuildID():
			return
		# END_OF_GUILD_BUILDING

		self.wndGameButton.ShowBuildButton()

	def BULID_ExitGuildArea(self, areaID):
		self.wndGameButton.HideBuildButton()

	#####################################################################################

	def IsEditLineFocus(self):
		if self.ChatWindow.chatLine.IsFocus():
			return 1

		if self.ChatWindow.chatToLine.IsFocus():
			return 1

		return 0

	if gcGetEnable("ENABLE_FAST_INTERACTIONS"):
		def GetWindowByType(self, type):
			windows = {
				player.INVENTORY: self.wndInventory,
				player.DRAGON_SOUL_INVENTORY: self.wndDragonSoul
			}

			return windows.get(type, None)

	def EmptyFunction(self):
		pass

	if app.ENABLE_SPECIAL_STORAGE:
		def ToggleSpecialStorageWindow(self, arg = 0):
			self.wndInventory.ClickSpecialStorageButton(arg)

	if app.ENABLE_RENEWAL_SHOP_SELLING:
		def RenewalShopAppendInformation(self, bAdded, *args):
			if self.dlgShop:
				self.dlgShop.AppendInformation(bAdded, args)

		def RenewalShopAccept(self):
			if self.wndInventory:
				self.wndInventory.AskSellingItems()

		def ClearHighlight(self):
			if self.wndInventory:
				self.wndInventory.ClearHighlightSellingItems()

		def RefreshSellingPrice(self):
			if self.dlgShop:
				self.dlgShop.RenewalClean()

	if app.ENABLE_VOICE_CHAT:
		def VoiceInit(self):
			self.wVoiceChat.run()

	if app.ENABLE_CHANGE_CHANNEL:
		def RefreshServerInfo(self):
			if self.wndMiniMap:
				self.wndMiniMap.RefreshServerInfo()

	if app.ENABLE_MARBLE_CREATOR_SYSTEM:
		def ToggleMarbleManager(self):
			if self.wndMarbleManager.IsShow():
				self.wndMarbleManager.Close()
			else:
				self.wndMarbleManager.Open()

		def MarbleManagerUpdate(self):
			if self.wndMarbleManager:
				self.wndMarbleManager.UpdateInformation()

	if app.BATTLE_PASS_ENABLE:
		def	BattlePass_ToggleWindow(self):
			self.wndBattlePass.UpdateWindow()

		def	BattlePass_ShowToggleButton(self):
			self.btnBattlePass.Show()

	if app.ENABLE_TRANSMUTATION_SYSTEM:
		def	Transmutation_UpdateWindow(self):
			if self.Transmutation_GUI:
				self.Transmutation_GUI.UpdateWindow()

		def	Transmutation_UpdateItem(self, id, item):
			if self.Transmutation_GUI:
				self.Transmutation_GUI.Transmutation_UpdateItem(id, item)

	if app.ENABLE_FIND_LETTERS_EVENT:
		def OpenFindLettersEvent(self):
			if False == player.IsObserverMode():
				if not self.wndFindLettersWindow.IsShow():
					self.wndFindLettersWindow.Open()
				else:
					self.wndFindLettersWindow.Close()

		def AddFindLetters(self, iPos, iAsciiChar, iIsFilled):
			if self.wndFindLettersWindow:
				self.wndFindLettersWindow.AddLetter(iPos, iAsciiChar, iIsFilled)

		def FindLettersFinishEvent(self):
			if self.wndFindLettersWindow:
				self.wndFindLettersWindow.FinishEvent()

		def AddFindLettersReward(self, iPos, itemVnum, itemCount):
			if self.wndFindLettersWindow:
				self.wndFindLettersWindow.AddReward(iPos, itemVnum, itemCount)

		def FindLettersIcon(self, isShow):
			if isShow:
				if self.wndFindLettersButton:
					self.wndFindLettersButton.ShowButton()
					self.wndFindLettersButton.Show()
			else:
				if self.wndFindLettersButton:
					self.wndFindLettersButton.HideButton()
					self.wndFindLettersButton.Hide()

				if self.wndFindLettersWindow:
					if self.wndFindLettersWindow.IsShow():
						self.wndFindLettersWindow.Close()

	if app.ENABLE_LUCKY_BOX:
		def OpenLuckyBox(self):
			if False == player.IsObserverMode():
				if not self.wndLuckyBoxWindow.IsShow():
					self.wndLuckyBoxWindow.Open()

		def RefreshLuckyBox(self):
			if self.wndLuckyBoxWindow:
				self.wndLuckyBoxWindow.RefreshInfo()

		def CloseLuckyBox(self):
			if self.wndLuckyBoxWindow:

				self.wndLuckyBoxWindow.Close()

	if app.ENABLE_SAVE_POSITIONS_SYSTEM:
		def	PositionManager_ToggleWindow(self):
			self.wndPositionManager.UpdateWindow()

	if app.ENABLE_RENDER_TARGET_EXTENSION:
		# PREVIEW
		def OpenPreviewWindow(self, itemIndex):
			item.SelectItem(itemIndex)
			if item.GetItemType() == item.ITEM_TYPE_TOGGLE and item.GetItemSubType() in (item.TOGGLE_PET, item.TOGGLE_MOUNT):
				race = item.GetValue(0)
				self.__OpenPreviewWindow(uiPreview.PreviewWindow.TYPE_CHARACTER, race)
			else:
				self.__OpenPreviewWindow(uiPreview.PreviewWindow.TYPE_ITEM, itemIndex)

		def __OpenPreviewWindow(self, type, value):
			if not self.wndPreview:
				self.wndPreview = uiPreview.PreviewWindow()
			self.wndPreview.Open(type, value)
		# END_OF_PREVIEW

	if app.INGAME_WIKI:
		def ToggleWikiNew(self):
			import net
			net.ToggleWikiWindow()

	if gcGetEnable("ENABLE_LEFT_POPUP"):
		def LoadAppLeftTip(self, message, type):
			self.leftTipBoard.SetTip(message, type)

	if app.INGAME_WIKI:
		def wikiExtension_searchVnum(self, iVnum):
			if iVnum:
				if self.dlgSystem.wikiWnd:
					if self.dlgSystem.wikiWnd.IsShow():
						self.dlgSystem.wikiWnd.Hide()
					else:
						self.dlgSystem.wikiWnd.Show()
						self.dlgSystem.wikiWnd.SetTop()

						self.dlgSystem.wikiWnd.CloseBaseWindows()
						self.dlgSystem.wikiWnd.OpenSpecialPage(None, iVnum, False)
	
	if gcGetEnable("ENABLE_EXPANDED_CURRENCIE_INFORMATION"):
		def ToggleCurrencieInformations(self, bInventoryCall = False, bInit = False):
			"""
				The states of this system is;
					-> When you open the client, and the moneyBar is hided, at the first time when you try to open the inventory its will using method .Show()
					-> When you gonna close the inventory its will using method .Hide()
					
					\-> When you gonna have closed inventory, and you gonna press on the button in the taskbar to show it -> its will be always <SHOWED>,
					\-> When you gonna have opened inventory and moneybar after clicking -> Its will deactivate it permamently,
			"""
			
			if not self.wndExpandedMoneyBar:
				return

			isShowing = self.wndExpandedMoneyBar.IsShow()

			if bInventoryCall:
				if constInfo.CURRENCIE_STATE == True:
					return

				elif constInfo.CURRENCIE_STATE == False and constInfo.CURRENCIE_INIT == True and isShowing:
					return
			else:
				## Right now we gonna check if we have the init, and currencie window should be hided
				if bInit:
					if (constInfo.CURRENCIE_INIT == False):
						return

					if (constInfo.CURRENCIE_STATE == True):
						isShowing = True

			if (not bInventoryCall and not bInit):
				## Just in this case we are able to set the currencie state!
				constInfo.CURRENCIE_INIT = True
				constInfo.CURRENCIE_STATE = True if isShowing else False

			self.wndExpandedMoneyBar.Hide() if isShowing\
					else self.wndExpandedMoneyBar.Show()
					
	if app.ENABLE_PREMIUM_PRIVATE_SHOP:
		def OpenPrivateShopPanel(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Open()
				
			if not self.wndInventory.IsShow():
				self.wndInventory.Show()
				
		def ClosePrivateShopPanel(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Close(False)
				
		def RefreshPrivateShopWindow(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.Refresh()
				self.wndPrivateShopPanel.RefreshWindow()
				
		def TogglePrivateShopPanelWindow(self):
			if False == player.IsObserverMode():
				if not self.wndPrivateShopPanel.RequestOpen():
					self.wndPrivateShopPanel.Close()
					
		def OpenPrivateShopSearch(self, mode):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.Open(mode)
				
		def PrivateShopSearchUpdate(self, index, state):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.UpdateResult(index, state)

		def PrivateShopSearchRefresh(self):
			if self.wndPrivateShopSearch:
				self.wndPrivateShopSearch.RefreshPage()
				
		def AppendMarketItemPrice(self, gold, cheque):
			if self.wndPrivateShopPanel and self.wndPrivateShopPanel.IsShow():
				self.wndPrivateShopPanel.AppendMarketItemPrice(gold, cheque)
				
			elif self.self.privateShopBuilder and self.self.privateShopBuilder.IsShow():
				self.privateShopBuilder.AppendMarketItemPrice(gold, cheque)
				
		def AddPrivateShopTitleBoard(self, vid, text, type):

			board = uiPrivateShop.PrivateShopTitleBoard(type)
			board.Open(vid, text)

			self.privateShopAdvertisementBoardDict[vid] = board

		def RemovePrivateShopTitleBoard(self, vid):

			if not self.privateShopAdvertisementBoardDict.has_key(vid):
				return

			del self.privateShopAdvertisementBoardDict[vid]
			uiPrivateShop.DeleteTitleBoard(vid)
			
		def SetPrivateShopPremiumBuild(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.SetPremiumBuildMode()
				self.wndPrivateShopPanel.RefreshWindow()
				
		def PrivateShopStateUpdate(self):
			if self.wndPrivateShopPanel:
				self.wndPrivateShopPanel.OnStateUpdate()

	def BindMainGamePhaseWindow(self, gamePhaseWindow):
		from _weakref import proxy
		self.gamePhaseWindow = proxy( gamePhaseWindow )

# GLOBALS
_instance = None

def GetInstance():
	global _instance
	return _instance

def SetInstance(instance):
	global _instance

	if _instance:
		del _instance

	_instance = instance
