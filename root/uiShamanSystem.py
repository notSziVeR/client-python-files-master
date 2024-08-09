import ui, itemWrapper, uiToolTip, uiScriptLocale

class ShamanSystemClass(ui.SimplyWindow):
	SIZE = (320, 125) # 300
	ROOT_PATH = "d:/ymir work/ui/shaman_system/{}"

	def __init__(self):
		ui.SimplyWindow.__init__(self, "UI", ("movable", "float"), self.SIZE[0], self.SIZE[1], self.__Initialize, self.__Destroy)
	
	def __del__(self):
		ui.SimplyWindow.__del__(self)

	def __Destroy(self):
		self.windowConfig["SKILLS"] = {}

	def __Initialize(self):
		self.sToolTip = uiToolTip.SkillToolTip()
		self.windowConfig["SKILLS"] = {}

		def __CreateHeader(sKey, iPos = (0, 0), sText = ""):
			rImage = ui.ExpandedImageBox()
			rImage.SetParent(self.GetObject("board"))
			rImage.SetPosition(*iPos)
			rImage.LoadImage(self.ROOT_PATH.format("header.png"))
			rImage.SetScale(0.74, 1.0)
			rImage.SetWindowHorizontalAlignCenter()
			rImage.Show()

			rText = ui.TextLine()
			rText.SetParent(rImage)
			rText.SetPosition(0, -1)
			rText.SetHorizontalAlignCenter()
			rText.SetWindowHorizontalAlignCenter()
			rText.SetVerticalAlignCenter()
			rText.SetWindowVerticalAlignCenter()
			rText.SetText(sText)
			rText.Show()

			self.AppendObject(sKey, (rImage, rText))

			return (rImage, rText)

		def __CreateContainer(sKey, iSizes = (0, 0)):
			rContainer = ui.MainSubBoard()
			rContainer.SetParent(self.GetObject("board"))
			rContainer.SetWindowHorizontalAlignCenter()
			rContainer.SetSize(*iSizes)
			rContainer.Show()

			self.AppendObject(sKey, rContainer)

			return rContainer

		## Build Base
		board = ui.MainBoardWithTitleBar()
		board.SetParent(self)
		board.SetPosition(0, 0)
		board.SetTitleName(uiScriptLocale.SHAMAN_SYSTEM_WINDOW_TITLE)
		board.SetCloseEvent(ui.__mem_func__(self.Close))
		board.SetSize(self.GetWidth(), self.GetHeight())
		board.Show()

		self.AppendObject("board", board)

		# __CreateHeader("equipment_header", (0, 32), "Equipment")

		# rContainer = __CreateContainer("equipment_container", (310, 150))
		# rContainer.SetPosition(0, self.GetObject("equipment_header")[0].GetLocalPosition()[1] + self.GetObject("equipment_header")[0].GetHeight())

		# __CreateHeader("skills_header", (0, rContainer.GetLocalPosition()[1] + rContainer.GetHeight()), "Skills")

		__CreateHeader("skills_header", (0, 32), "Skills")

		rContainer = __CreateContainer("skills_container", (310, 65))
		rContainer.SetPosition(0, self.GetObject("skills_header")[0].GetLocalPosition()[1] + self.GetObject("skills_header")[0].GetHeight())

		text = ui.MakeTextLine(self.GetObject("skills_container"))
		text.SetText(uiScriptLocale.SHAMAN_SYSTEM_WINDOW_REGISTER_SHAMAN)

		slot = ui.SlotWindow()
		slot.SetParent(self.GetObject("skills_container"))
		slot.SetPosition(0, 0)
		slot.SetSize(rContainer.GetWidth(), rContainer.GetHeight())
		slot.SetSlotBaseImage("d:/ymir work/ui/public/Slot_Base.sub", 1.0, 1.0, 1.0, 1.0)
		slot.SetOverInItemEvent(ui.__mem_func__(self.__OnOverInSlot))
		slot.SetOverOutItemEvent(ui.__mem_func__(self.__OnOverOutSlot))
		slot.Show()

		self.AppendObject("skills_objects", (text, slot))

		self.GetObject("skills_objects")[1].Hide()

	def __OnOverInSlot(self, slot):
		if not self.sToolTip:
			return

		getter = self.windowConfig["SKILLS"].get(slot, None)
		if getter == None:
			return

		(sType, sLevel, fPower) = getter

		tGrade, tLevel = self.__GetSkillInformations(sLevel)
		self.sToolTip.ClearToolTip()
		self.sToolTip.AppendDefaultData(sType)
		self.sToolTip.AppendSkillConditionData(sType)
		self.sToolTip.ShowToolTip()

	def __OnOverOutSlot(self):
		if self.sToolTip:
			self.sToolTip.HideToolTip()

	def __GetSkillInformations(self, skillLevel):
		if skillLevel < 20:
			return (0, skillLevel)
		elif skillLevel < 30:
			return (1, skillLevel - 19)
		elif skillLevel < 40:
			return (2, skillLevel - 29)
		else:
			return (3, 0)

	def RegisterLabel(self, iKey, iPos = (0, 0)):
		rLabel = ui.Bar()
		rLabel.SetColor(0xFF3A383A)
		rLabel.SetParent(self.GetObject("skills_container"))
		# rLabel.SetWindowHorizontalAlignCenter()
		rLabel.SetSize(32, 10)
		rLabel.SetPosition(*iPos)
		rLabel.Show()

		sText = ui.MakeTextLine(rLabel)
		sText.SetText("0%")

		sKey = "skill_label_{}".format(iKey)
		self.AppendObject(sKey, (rLabel, sText, ))

		return rLabel

	## Recv
	def RegisterShamanSlots(self, iCount):
		self.GetObject("skills_objects")[0].Hide()
		self.GetObject("skills_objects")[1].Show()

		totalWidth = (iCount * (32 + 3))

		entryX = (self.GetObject("skills_container").GetWidth() - totalWidth) / 2

		for i in xrange(iCount):
			self.GetObject("skills_objects")[1].AppendSlot(i, entryX, (self.GetObject("skills_container").GetHeight() - 32) / 2, 32, 32)
			self.RegisterLabel(i, (entryX, ((self.GetObject("skills_container").GetHeight() - 32) / 2) + 32))
			entryX += 32 + 3

	def RegisterShamanSkill(self, iKey, iType, iLevel, fPower):
		self.windowConfig["SKILLS"][iKey] = (iType, iLevel, fPower)

		tGrade, tLevel = self.__GetSkillInformations(iLevel)

		self.GetObject("skills_objects")[1].ClearSlot(iKey)
		self.GetObject("skills_objects")[1].SetCoverButton(iKey)
		self.GetObject("skills_objects")[1].UnlockSlot(iKey)
		self.GetObject("skills_objects")[1].SetSkillSlotNew(iKey, iType, tGrade, tLevel)
		self.GetObject("skills_objects")[1].SetSlotCountNew(iKey, tGrade, tLevel)

		self.GetObject("skills_objects")[1].RefreshSlot()

		getter = self.windowConfig["SKILLS"].get(iKey, None)
		if getter == None:
			return

		(sType, sLevel, fPower) = getter

		self.GetObject("skill_label_{}".format(iKey))[1].SetText("{}%".format(fPower * sLevel))

	def RegisterShamanPremium(self, bPremium):
		self.windowConfig["IS_PREMIUM"] = bPremium

	def UnregisterShaman(self):
		self.windowConfig["IS_PREMIUM"] = False
		self.GetObject("skills_objects")[0].Show()
		self.GetObject("skills_objects")[1].ClearAllSlot()

		for iKey in self.windowConfig["SKILLS"].keys():
			self.GetObject("skill_label_{}".format(iKey))[0].Hide()

	def Close(self):
		self.Hide()
