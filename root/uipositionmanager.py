import ui
import localeInfo
import exception

import uiToolTip
import uiCommon

from _weakref import proxy
import background

import net
import cfg
import player

class PositionsManagerInterface(ui.ScriptWindow):

	MAX_PAGE_COUNT = 15

	class PositionObject(ui.Window):
		BUTTON_SIZE = (494, 20)

		ROOT_NEW = "assets/ui/save_location_manager/{}"

		def __init__(self, scriptParent, parent, iPos, iMapIndex = 0, iLocalX = 0, iLocalY = 0, iGlobalX = 0, iGlobalY = 0):
			ui.Window.__init__(self)
			self.SetParent(parent)
			self.parent = proxy(parent)
			self.scriptParent = proxy(scriptParent)

			self.id = iPos
			self.Objects = {}

			self.iMapIndex = iMapIndex
			self.iLocalX = iLocalX
			self.iLocalY = iLocalY
			self.iGlobalX = iGlobalX
			self.iGlobalY = iGlobalY

			self.__BuildObject(iPos, iMapIndex, iLocalX, iLocalY, iGlobalX, iGlobalY)

		def __del__(self):
			ui.Window.__del__(self)
			self.id = None
			self.Objects = {}

		def __BuildObject(self, iPos, iMapIndex, iLocalX, iLocalY, iGlobalX, iGlobalY):
			##Size
			self.SetSize(*self.BUTTON_SIZE)

			self.Objects["Location_BG"] = ui.MakeExpandedImageBox(self, self.ROOT_NEW.format("content_background.png"), 0, 0)

			self.Objects["Location_NAME"] = ui.MakeTextLineNew(self.Objects["Location_BG"], 5, -2, "")
			self.Objects["Location_NAME"].SetVerticalAlignCenter()
			self.Objects["Location_NAME"].SetWindowVerticalAlignCenter()
			self.Objects["Location_NAME"].SetHorizontalAlignLeft()
			self.Objects["Location_NAME"].SetWindowHorizontalAlignLeft()
			sName = cfg.Get(cfg.SAVE_GENERAL, "POSITION_MGR_{}_{}".format(player.GetName(), self.id), "-")
			self.Objects["Location_NAME"].SetText("{}".format(sName))

			self.Objects["Location_CORDS"] = ui.MakeTextLineNew(self.Objects["Location_BG"], 23, -2, "")
			self.Objects["Location_CORDS"].SetVerticalAlignCenter()
			self.Objects["Location_CORDS"].SetWindowVerticalAlignCenter()
			self.Objects["Location_CORDS"].SetHorizontalAlignRight()
			self.Objects["Location_CORDS"].SetWindowHorizontalAlignRight()
			self.Objects["Location_CORDS"].SetText("({}, {})".format(iLocalX, iLocalY))

			self.Objects["Location_Info"] = ui.MakeButton(self, self.Objects["Location_BG"].GetWidth() - 20, 0, "", "assets/ui/save_location_manager/",\
				"button_info_0.png", "button_info_1.png", "button_info_1.png")
			
			self.Objects["Location_Info"].SetOverEvent(ui.__mem_func__(self.OnMouseOverInInfo))
			self.Objects["Location_Info"].SetOverOutEvent(ui.__mem_func__(self.OnMouseOverOutInfo))

			self.Objects["SaveButton"] = ui.MakeButton(self, 256, 0, "", "assets/ui/save_location_manager/",\
				"button_save_0.png", "button_save_1.png", "button_save_2.png")
			self.Objects["SaveButton"].SAFE_SetEvent(self.__SavePosition)

			self.Objects["TeleportButton"] = ui.MakeButton(self, 342, -1, "", "assets/ui/save_location_manager/",\
				"button_0.png", "button_1.png", "button_2.png", localeInfo.POSITION_MANAGER_BUTTON_TELEPORT, 1)
			
			self.Objects["TeleportButton"].SetDisableVisual(self.ROOT_NEW.format("button_2.png"))
			self.Objects["TeleportButton"].SAFE_SetEvent(self.__TeleportPosition)

			self.Objects["DeleteButton"] = ui.MakeButton(self, 428, -1, "", "assets/ui/save_location_manager/",\
				"button_0.png", "button_1.png", "button_2.png", localeInfo.POSITION_MANAGER_BUTTON_REMOVE, 1)
			self.Objects["DeleteButton"].SetDisableVisual(self.ROOT_NEW.format("button_2.png"))
			self.Objects["DeleteButton"].SAFE_SetEvent(self.__DeletePosition)

			if iMapIndex:
				self.Objects["TeleportButton"].Enable()
				self.Objects["DeleteButton"].Enable()
			else:
				self.Objects["TeleportButton"].Disable()
				self.Objects["DeleteButton"].Disable()

			self.Show()

		def OnMouseOverInInfo(self):
			if self.iMapIndex == 0:
				return

			(mapName, xBase, yBase) = background.GlobalPositionToMapInfo(self.iGlobalX * 100, self.iGlobalY * 100)
			(name, x, y) = background.GetMapLocaleName(self.iGlobalX * 100, self.iGlobalY * 100)

			toolTip = uiToolTip.GetItemToolTipInstance()
			toolTip.ClearToolTip()
			toolTip.AppendMapImage(mapName, self.iLocalX, self.iLocalY)
			toolTip.AppendTextLine("{} ({},{})".format(getattr(localeInfo, "ATLAS_MAP_{}".format(name), name.replace("_", " ")), self.iLocalX, self.iLocalY))
			toolTip.ShowToolTip()

		def OnMouseOverOutInfo(self):
			if self.iMapIndex == 0:
				return

			uiToolTip.GetItemToolTipInstance().HideToolTip()

		def __SavePosition(self):
			self.scriptParent.TogglePopup(self.id)

		def __TeleportPosition(self):
			self.scriptParent.TeleportPosition(self.id)

		def __DeletePosition(self):
			self.scriptParent.DeletePosition(self.id)

	def __init__(self):
		ui.ScriptWindow.__init__(self)

		self.Objects = {}

		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		self.ClearDictionary()
		self.Objects = {}

	def __LoadWindow(self):
		try:
			pyScrLoader = ui.PythonScriptLoader()
			pyScrLoader.LoadScriptFile(self, "uiscript/positionsmanagerwindow.py")
		except:
			exception.Abort("PositionsManagerInterface.__LoadWindow.LoadObject")

		try:
			self.Objects["MainBox"] = self.GetChild("MainBox")
			self.Objects["ListBox_Space"] = self.GetChild("ListBox_Space")

		except:
			exception.Abort("PositionsManagerInterface.__LoadWindow.BindObject")

		self.Objects["MainListBox"] = ui.ListBoxEx()
		self.Objects["MainListBox"].SetParent(self.Objects["ListBox_Space"])
		self.Objects["MainListBox"].SetPosition(0, 0)
		self.Objects["MainListBox"].SetItemSize(*self.PositionObject.BUTTON_SIZE)
		self.Objects["MainListBox"].SetItemStep(self.PositionObject.BUTTON_SIZE[1] + 4)
		self.Objects["MainListBox"].SetViewItemCount(10)
		self.Objects["MainListBox"].Show()

		self.GetChild("PositionsBoard").SetCloseEvent(self.Close)

		self.SetCenterPosition()
		self.SetTop()

	def ClearInterface(self):
		self.Objects["MainListBox"].RemoveAllItems()

	def AppendData(self, iPos, iMapIndex, iLocalX, iLocalY, iGlobalX, iGlobalY):
		sName = cfg.Get(cfg.SAVE_GENERAL, "POSITION_MGR_{}_{}".format(player.GetName(), iPos), "-")
		if (sName != "-" and iMapIndex == 0):
			cfg.Set(cfg.SAVE_GENERAL, "POSITION_MGR_{}_{}".format(player.GetName(), iPos), "-")

		self.Objects["MainListBox"].AppendItem(self.PositionObject(self, self.Objects["MainListBox"], iPos, iMapIndex, iLocalX, iLocalY, iGlobalX, iGlobalY))

	def ReSavePosition(self, bPos):
		if len(self.Objects["Q_POPUP"].GetText()) < 1:
			return

		cfg.Set(cfg.SAVE_GENERAL, "POSITION_MGR_{}_{}".format(player.GetName(), bPos), self.Objects["Q_POPUP"].GetText())

		net.SendChatPacket("/positions_action save %d" % bPos)
		self.ClosePopup()

	def TeleportPosition(self, bPos):
		net.SendChatPacket("/positions_action teleport %d" % bPos)

	def DeletePosition(self, bPos):
		cfg.Set(cfg.SAVE_GENERAL, "POSITION_MGR_{}_{}".format(player.GetName(), bPos), "-")
		net.SendChatPacket("/positions_action delete %d" % bPos)

	def TogglePopup(self, iPos):
		self.Objects["Q_POPUP"] = uiCommon.InputDialog()
		self.Objects["Q_POPUP"].SetTitle(localeInfo.POSITION_MANAGER_WINDOW_POPUP_TITLE)
		self.Objects["Q_POPUP"].SetAcceptEvent(lambda iPos = iPos : self.ReSavePosition(iPos))
		self.Objects["Q_POPUP"].SetCancelEvent(self.ClosePopup)
		self.Objects["Q_POPUP"].Open()

	def ClosePopup(self):
		if not self.Objects["Q_POPUP"]:
			return

		self.Objects["Q_POPUP"].Close()

	def	UpdateWindow(self):
		if self.IsShow():
			self.Hide()
		else:
			self.Show()

	def Open(self):
		self.Show()

	def Close(self):
		self.Hide()

	def OnPressEscapeKey(self):
		self.Close()
		return True
