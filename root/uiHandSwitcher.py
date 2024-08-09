import itemWrapper, ui, localeInfo, colorInfo, uiToolTip
import player, item, net, app, wndMgr

#TODO We need to make some calculations and new function to apply new Applys 

class HandSwitcherClass(ui.ScriptWindow):
	MAX_BONUSES = 5
	ITEM_TYPE_SWITCHER, ITEM_TYPE_MAIN = range(0, 2)

	def __init__(self):
		super(HandSwitcherClass, self).__init__()

		self.__Initialize()
		self.__BuildWindow()

	def __del__(self):
		return super(HandSwitcherClass, self).__del__()

	def Destroy(self):
		self.ClearDictionary()
		self.Objects = {}

	def __Initialize(self):
		self.Objects = {}

	def __BuildWindow(self):
		if not self.LoadScript(self, "uiscript/HandSwitcher_Window.py"):
			return

		GetObject = self.GetChild
		self.Objects["Board"] = GetObject("HandSwitcher-Board")
		self.Objects["TopSpace"] = GetObject("HandSwitcher-TopSpace")
		self.Objects["Slots"] = GetObject("HandSwitcher-ItemSpace")
		self.Objects["Applys"] = [GetObject("HandSwitcher-ApplyText_{}".format(i)) for i in xrange(self.MAX_BONUSES)]
		self.Objects["SwitcherEnumeration"] = GetObject("HandSwitcher-CurrentCountText")
		self.Objects["Reroll"] = GetObject("Reroll")

		self.Objects["Configuration"] = itemWrapper.ItemContainer()
		self.Objects["Configuration"].SetOnSetItem(self.__Refresh)

		self.Objects["ToolTip"] = uiToolTip.ToolTip()
		self.Objects["ToolTip"].ClearToolTip()

		return self.__BindActions()

	def __BindActions(self):
		self.Objects["Board"].SetCloseEvent(ui.__mem_func__(self.Close))
		self.Objects["Board"].HandleButtonState("BTN_CHBOX", True)
		if self.Objects["Board"].HandleButtonGetter("BTN_CHBOX"):
			self.Objects["Board"].HandleButtonGetter("BTN_CHBOX").SetOverEvent(ui.__mem_func__(self.__CreateToolTip))
			self.Objects["Board"].HandleButtonGetter("BTN_CHBOX").SetOverOutEvent(ui.__mem_func__(self.__HideToolTip))

		self.Objects["Reroll"].SetEvent(ui.__mem_func__(self.Reroll))

	def __CreateToolTip(self):
		if not self.Objects.get("ToolTip"):
			return

		(pos_x, pos_y) = wndMgr.GetMousePosition()

		self.Objects["ToolTip"].ClearToolTip()
		self.Objects["ToolTip"].AppendShortcut([app.DIK_RETURN], localeInfo.QUICK_ACTION_CHECKBOX_HAND_SWITCHER, bCenter = True, bSpace = False)
		self.Objects["ToolTip"].SetToolTipPosition(pos_x, pos_y - 5)
		self.Objects["ToolTip"].Show()

	def __HideToolTip(self):
		if not self.Objects.get("ToolTip"):
			return

		self.Objects["ToolTip"].HideToolTip()

	#@Public Methods
	def CanChangeItem(self, sType, iSwitcherPos, iMainPos):
		v_Configuration = {
			"USE_CHANGE_ATTRIBUTE" : (
				{ "TYPE" : item.ITEM_TYPE_WEAPON, "BLOCK" : (item.WEAPON_ARROW, ), "EXCEPTIONS" : (71151, 40) },
				{ "TYPE" : item.ITEM_TYPE_ARMOR },
			),

			"USE_ADD_BELT_ATTR" : (
				{ "TYPE" : item.ITEM_TYPE_BELT, },
			),

			"USE_CHANGE_BELT_ATTR" : (
				{ "TYPE" : item.ITEM_TYPE_BELT, },
			),
		}

		item.SelectItem(player.GetItemIndex(player.INVENTORY, iMainPos))
		(ITEM_TYPE, ITEM_SUB_TYPE) = (item.GetItemType(), item.GetItemSubType())
		cHandler = v_Configuration.get(sType, None)

		if not cHandler:
			return False

		for vFit in cHandler:
			if ITEM_TYPE == vFit.get("TYPE", -1):
				if ITEM_SUB_TYPE in vFit.get("BLOCK", ()):
					return False

				# We will not let you pass in the event that the item is at a higher level than the acceptable one.
				if player.GetItemIndex(player.INVENTORY, iSwitcherPos) == vFit.get("EXCEPTIONS", (-1, -1))[0]:
					for i in xrange(item.LIMIT_MAX_NUM):
						(lType, lValue) = item.GetLimit(i)

						if lType == item.LIMIT_LEVEL:
							if lValue > vFit.get("EXCEPTIONS")[1]:
								return False

				return True

		return False

	def CanMoveItem(self, iPos):
		for i in xrange(self.Objects["Configuration"].GetItemCount()):
			pkItem = self.Objects["Configuration"].GetItem(i)

			if pkItem.GetPosition() == iPos:
				return False

		return True

	def HandleReturnButton(self):
		if not self.Objects["Board"].HandleButtonGetter("BTN_CHBOX"):
			return False

		return self.Objects["Board"].HandleButtonGetter("BTN_CHBOX").IsChecked()

	def BroadcastUpdate(self):
		if not self.Objects["Configuration"].GetItem(self.ITEM_TYPE_SWITCHER):
			self.Hide()

		self.__RefreshAmount()
		self.__AppendApplies()

	def SetConfiguration(self, iSwitcherPos, iMainPos):
		self.Objects["Configuration"].Clear()

		iSwitcher = itemWrapper.ItemToolTipWrapper(player.INVENTORY, iSwitcherPos)
		self.Objects["Configuration"].SetItem(self.ITEM_TYPE_SWITCHER, iSwitcher)

		iMainItem = itemWrapper.ItemToolTipWrapper(player.INVENTORY, iMainPos)
		self.Objects["Configuration"].SetItem(self.ITEM_TYPE_MAIN, iMainItem)

	#@Private Methods
	def __FindEqualItem(self, bSetter = False):
		## Gatherings informations
		iSize = player.INVENTORY_PAGE_SIZE * player.INVENTORY_PAGE_COUNT
		if app.ENABLE_SPECIAL_STORAGE:
			iSize += item.SPECIAL_STORAGE_PAGE_SIZE * item.SPECIAL_STORAGE_PAGE_COUNT * item.SPECIAL_STORAGE_COUNT

		## Let's declare the searched item
		pSwitcher = self.Objects["Configuration"].GetItem(self.ITEM_TYPE_SWITCHER)
		if not pSwitcher:
			return

		iTotalCount = 0
		for it in xrange(iSize):
			iVnum = player.GetItemIndex(it)
			if iVnum == 0:
				continue

			if iVnum != pSwitcher.GetVnum():
				continue
			
			if bSetter and it == pSwitcher.GetPosition():
				continue

			if bSetter:
				self.Objects["Configuration"].SetItem(self.ITEM_TYPE_SWITCHER, itemWrapper.ItemToolTipWrapper(player.INVENTORY, it))

			iTotalCount += player.GetItemCount(it)

		return iTotalCount

	def __Refresh(self, iType):
		if iType == self.ITEM_TYPE_SWITCHER:
			self.__RefreshAmount()
		else:
			self.__RerrangeSlots()
			self.__AppendApplies()

	def __RefreshAmount(self):
		if not self.Objects["Configuration"].GetItem(self.ITEM_TYPE_SWITCHER):
			return

		iTotalCount = self.__FindEqualItem()

		## We gonna close the window just in case if we doesn't have enough items!
		if iTotalCount == 0:
			self.Objects["Configuration"].Clear()
			self.Close()
			return

		## Selecting current item and getting the size of it
		iVnum = self.Objects["Configuration"].GetVnum(self.ITEM_TYPE_SWITCHER)
		item.SelectItem(iVnum)

		self.Objects["SwitcherEnumeration"].SetText(item.GetItemName() + ": {}".format(colorInfo.Colorize(iTotalCount, 0xFFffd169)))

	def __RerrangeSlots(self):
		if not self.Objects["Configuration"].GetItem(self.ITEM_TYPE_MAIN):
			return

		## Selecting current item and getting the size of it
		iVnum = self.Objects["Configuration"].GetVnum(self.ITEM_TYPE_MAIN)
		item.SelectItem(iVnum)
		_width, _height = item.GetItemSize()

		## Let's check which slots need to be hided
		for it in xrange(self.Objects["Slots"].GetSlotCount()):
			if it < _height:
				self.Objects["Slots"].ShowSlotBaseImage(it)
			else:
				self.Objects["Slots"].HideSlotBaseImage(it)

		## Setting the slot, and set center!
		self.Objects["Slots"].SetItemSlot(0, iVnum)
		self.Objects["Slots"].SetPosition((self.Objects["TopSpace"].GetWidth() - _width * 32) / 2, (self.Objects["TopSpace"].GetHeight() - _height * 32) / 2)

	def __AppendApplies(self):
		if not self.Objects["Configuration"].GetItem(self.ITEM_TYPE_MAIN):
			return

		pkItem = self.Objects["Configuration"].GetItem(self.ITEM_TYPE_MAIN)
		if not pkItem:
			return
		
		tooltipInstance = pkItem.GetToolTip()
		if not tooltipInstance:
			return

		v_attrs = [player.GetItemAttribute(pkItem.GetPosition(), i) for i in xrange(self.MAX_BONUSES)]
		it = 0
		for (type, value) in v_attrs:
			if type == 0 or value == 0:
				self.Objects["Applys"][it].SetText("-")
				it += 1
				continue

			fValue = localeInfo.DottedNumber(value)

			sApply = tooltipInstance.GetAffectString(type, fValue, False)
			sApplyColor, sApplyValue = tooltipInstance.GetAttributeColor(it, value, type, False)
			self.Objects["Applys"][it].SetText(tooltipInstance.GetFormattedColorString(sApply, fValue, sApplyValue, 1))
			self.Objects["Applys"][it].SetPackedFontColor(sApplyColor)
			
			it += 1

	def Reroll(self):
		if not self.Objects["Configuration"].GetItem(self.ITEM_TYPE_SWITCHER):
			return

		pSwitcher = self.Objects["Configuration"].GetItem(self.ITEM_TYPE_SWITCHER)
		pItem = self.Objects["Configuration"].GetItem(self.ITEM_TYPE_MAIN)

		## Lets try to set new switcher item of the same type in case if we have the count == 1
		if pSwitcher.GetCount() == 1:
			self.__FindEqualItem(True)

		net.SendItemUseToItemPacket(pSwitcher.GetPosition(), pItem.GetPosition())

	def Show(self):
		super(HandSwitcherClass, self).Show()
		self.SetCenterPosition()
		self.SetTop()

	def Close(self):
		super(HandSwitcherClass, self).Hide()

		if self.Objects:
			self.Objects["Configuration"].Clear()

		self.Objects["Board"].HandleButtonGetter("BTN_CHBOX").SetChecked(False)

	def OnPressEscapeKey(self):
		self.Close()
		return True

	def OnPressReturnKey(self):
		if self.HandleReturnButton():
			self.Reroll()
