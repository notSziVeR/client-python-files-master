import ui, localeInfo, net, uiCommon, chr, app, wndMgr
# import queuemanager
import uiToolTip

CONFIGURATION = {
	"SKILL_NAMES" : {
		0	:	[localeInfo.SKILL_GROUP_WARRIOR_1,	localeInfo.SKILL_GROUP_WARRIOR_2],
		1	:	[localeInfo.SKILL_GROUP_ASSASSIN_1,	localeInfo.SKILL_GROUP_ASSASSIN_2],
		2	:	[localeInfo.SKILL_GROUP_SURA_1,		localeInfo.SKILL_GROUP_SURA_2],
		3	:	[localeInfo.SKILL_GROUP_SHAMAN_1,	localeInfo.SKILL_GROUP_SHAMAN_2],
	},

	"RENDER_SKILLS" : {
		0	:	[3,	19],
		1	:	[33,	48],
		2	:	[62,	77],
		3	:	[93,	106],
	},

	"IMAGES" : {
		0	:	"assets/ui/skill_select_manager/inners/warrior_{}.png",
		1	:	"assets/ui/skill_select_manager/inners/assassin_{}.png",
		2	:	"assets/ui/skill_select_manager/inners/sura_{}.png",
		3	:	"assets/ui/skill_select_manager/inners/shaman_{}.png",
	},
}

class SkillSelectWindow(ui.ScriptWindow):
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.ConfirmDialog = None
		self.Objects = {}
		self.bRace = -1
		self.iDefaultWeapon = 0
		# self.queue = None
		self.ToolTip = uiToolTip.SkillToolTip()
		self.__LoadWindow()
			
	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def Destroy(self):
		if self.ConfirmDialog:
			self.ConfirmDialog.Hide()
			self.ConfirmDialog = None
			
		self.Hide()
		
	def OnPressEscapeKey(self):
		self.Hide()
		return True
		
	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/selectskillwindow.py")
		except:
			import exception
			exception.Abort("LocationsWindow.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild

			GetObject("BOARD").SetCloseEvent(ui.__mem_func__(self.Hide))
			
			self.Objects = {
				"PATHES" : [GetObject("PATH_{}".format(i)) for i in xrange(2)],
				"RENDER" : GetObject("RENDERER"),
				"INNER" : [GetObject("HEADER_INNER_{}".format(i)) for i in xrange(2)],
				"JOB" : [GetObject("HEADER_JOB_{}".format(i)) for i in xrange(2)],
				"SKILL" : [GetObject("SKILLS_{}".format(i)) for i in xrange(2)],
				"BUTTON" : [GetObject("BUTTON_{}".format(i)) for i in xrange(2)],
			}

			for i in xrange(len(self.Objects["BUTTON"])):
				self.Objects["BUTTON"][i].SetEvent(ui.__mem_func__(self.__OpenDialog), i + 1)

		except:
			import exception
			exception.Abort("LocationsWindow.LoadDialog.BindObject")
		
		# self.queue = queuemanager.Queue()
		self.SetCenterPosition()
		
	def AddData(self, byRace):
		byRace = int(byRace)

		for i in xrange(2):
			self.Objects["INNER"][i].LoadImage(CONFIGURATION["IMAGES"][byRace].format(i))
			self.Objects["JOB"][i].SetText(CONFIGURATION["SKILL_NAMES"][byRace][i])

		for i in xrange(6):
			skillIndex = byRace * 30 + 1 + i
			self.Objects["SKILL"][0].SetSkillSlotNew(i, skillIndex, 3, 1)
			self.Objects["SKILL"][0].SetOverInItemEvent(ui.__mem_func__(self.ClickSkillSlot))
			self.Objects["SKILL"][0].SetOverOutItemEvent(ui.__mem_func__(self.ClickOutSkillSlot))

		for i in xrange(6):
			skillIndex = byRace * 30 + 1 + 15 + i
			self.Objects["SKILL"][1].SetSkillSlotNew(i, skillIndex, 3, 1)
			self.Objects["SKILL"][1].SetOverInItemEvent(ui.__mem_func__(self.ClickSkillSlot))
			self.Objects["SKILL"][1].SetOverOutItemEvent(ui.__mem_func__(self.ClickOutSkillSlot))

		self.Objects["RENDER"].SetRenderTarget(net.GetMainActorRace())
		self.Objects["RENDER"].SetHair(chr.GetPart(0, chr.PART_HAIR))
		self.Objects["RENDER"].SetArmor(chr.GetPart(0, chr.PART_MAIN))
		self.iDefaultWeapon = chr.GetPart(0, chr.PART_WEAPON)
		self.Objects["RENDER"].SetWeapon(self.iDefaultWeapon)

		self.bRace = int(byRace)

		self.Show()

	def ClickSkillSlot(self, slotIndex):
		skillIndex = (self.bRace * 30 + 1, self.bRace * 30 + 1 + 15)

		if self.Objects["SKILL"][0].IsIn():
			skillIndex = skillIndex[0] + slotIndex
			if self.iDefaultWeapon != 0 and self.bRace == 1:
				self.Objects["RENDER"].SetWeapon(self.iDefaultWeapon)
		else:
			skillIndex = skillIndex[1] + slotIndex
			if self.bRace == 1:
				self.Objects["RENDER"].SetWeapon(0)
				self.Objects["RENDER"].SetWeapon(2000)

		self.Objects["RENDER"].SetMotion(skillIndex)

		if self.ToolTip:
			self.ToolTip.ClearToolTip()
			self.ToolTip.AppendDefaultData(skillIndex)
			self.ToolTip.AppendSkillConditionData(skillIndex)
			self.ToolTip.ShowToolTip()

	def ClickOutSkillSlot(self):
		if self.bRace == 1:
			self.Objects["RENDER"].SetWeapon(0)
			if self.iDefaultWeapon != 0:
				self.Objects["RENDER"].SetWeapon(self.iDefaultWeapon)

		if self.ToolTip:
			self.ToolTip.HideToolTip()
			
	def __SelectSkill(self, index):
		self.__CloseDialog()

	def ConfirmSkill(self, index):
		net.SendChatPacket("/select_skills %d" %(index))
		self.__CloseDialog()
		self.Hide()

	def __OpenDialog(self, index):
		self.Objects["RENDER"].SetMotion(CONFIGURATION["RENDER_SKILLS"][self.bRace][index - 1])
		# self.queue.AppendEvent("Close", 2, self.ConfirmSkill, index) 

		qDialog = uiCommon.QuestionDialog()
		qDialog.SetText(localeInfo.DO_YOU_WANNA_SELECT_THIS_SKILL)
		qDialog.SetAcceptEvent(lambda arg=index: self.ConfirmSkill(arg))

		qDialog.SetCancelEvent(ui.__mem_func__(self.__CloseDialog))
		qDialog.Open()
		self.ConfirmDialog = qDialog
		
	def __CloseDialog(self):
		if self.ConfirmDialog != None:
			self.ConfirmDialog.Hide()
			self.ConfirmDialog = None

	def OnUpdate(self):
		# self.queue.Process()
		if self.GetLeft() < 0:
			self.SetPosition(0, self.GetTop())
		elif self.GetRight() > wndMgr.GetScreenWidth():
			self.SetPosition(wndMgr.GetScreenWidth() - self.GetWidth(), self.GetTop())

		if self.GetTop() < 0:
			self.SetPosition(self.GetLeft(), 0)
		elif self.GetBottom() > wndMgr.GetScreenHeight():
			self.SetPosition(self.GetLeft(), wndMgr.GetScreenHeight() - self.GetHeight())