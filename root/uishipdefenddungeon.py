import ui
import wndMgr
import uiScriptLocale

class ShipDungeonAllie(ui.ThinBoard):
	def	__init__(self):
		ui.ThinBoard.__init__(self)
		self.__BuildWindow()

	def __del__(self):
		ui.ThinBoard.__del__(self)
		self.allie_name = None
		self.allie_hp_gauge = None

	def	__BuildWindow(self):
		## Window
		self.SetSize(100, 50)

		## Allie Name
		self.allie_name = ui.TextLine()
		self.allie_name.SetParent(self)
		self.allie_name.SetPosition(0, 10)
		self.allie_name.SetWindowHorizontalAlignCenter()
		self.allie_name.SetHorizontalAlignCenter()
		self.allie_name.SetText(uiScriptLocale.SHIP_DEFEND_TITLE)
		self.allie_name.Show()

		## Allie Gauge
		self.allie_hp_gauge = ui.Gauge()
		self.allie_hp_gauge.SetParent(self)
		self.allie_hp_gauge.MakeGauge(90, "red")
		self.allie_hp_gauge.SetPosition(0, 30)
		self.allie_hp_gauge.SetWindowHorizontalAlignCenter()
		self.allie_hp_gauge.SetPercentage(100, 100)
		self.allie_hp_gauge.Show()

		self.SetPosition((wndMgr.GetScreenWidth() - self.GetWidth()), (wndMgr.GetScreenHeight() - self.GetHeight()) / 2)
		self.SetTop()
		self.Hide()

	def	UpdateGauge(self, perc):
		self.allie_hp_gauge.SetPercentage(perc, 100)

