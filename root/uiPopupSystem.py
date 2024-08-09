import ui
import app
import item
import Queue
import wndMgr
import uiToolTip

from _weakref import proxy

class PopupSystemInterface(ui.ScriptWindow):

	UPDATE_FREQUENCY = 0.1
	TEXTLINE_BASEPOS = (0, 22)
	TEXTLINE_COLOUR = 0xffB5A676
	TEXTLINE_LEN_LIMIT = 60

	class PopupEvent:

		EVENT_LENGTH = 3 ## in seconds
		PIXS_BY_FRAME = 1
		STATUS_DICT = {"WORKING" : -1, "PENDING" : 0, "DONE" : 1}

		def __init__(self, hParent, sHeader, sText, sIcon):
			self.hParent = proxy(hParent)
			self.sHeader = sHeader
			self.sText = sText
			self.sIcon = sIcon
			self.bIsProcessing = False
			self.ttTimer = 0
			self.iStatus = self.STATUS_DICT["WORKING"] ## Working -> Pending -> Done

		def StartProcessing(self):
			## Prepare main frame
			self.hParent.PrepareInterface(self.sHeader, self.sText, self.sIcon)

			## Set y startup coords
			self.hParent.SetPosition((wndMgr.GetScreenWidth() - self.hParent.GetWidth())/2, -self.hParent.GetHeight())

		def SetTimer(self):
			self.ttTimer = app.GetTime() + self.EVENT_LENGTH

		def IsPending(self):
			return self.ttTimer >= app.GetTime()

		def ProcessTick(self):
			wndY = self.hParent.GetGlobalPosition()[1]
			wndYNew = wndY + (self.PIXS_BY_FRAME if self.GetStatus() == self.STATUS_DICT["WORKING"] else -self.PIXS_BY_FRAME)

			self.hParent.SetPosition(0, wndYNew)
			return (wndYNew == -self.hParent.GetHeight() or wndYNew == 0)

		def UpdateStatus(self):
			self.iStatus += 1

		def GetStatus(self):
			return self.iStatus

	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.qPopupEvents = Queue.Queue()
		self.rCurrentEvent = None
		self.iNextUpdate = 0
		self.__LoadWindow()

	def __del__(self):
		ui.ScriptWindow.__del__(self)

	def	Destroy(self):
		self.ClearDictionary()
		self.qPopupEvents = None
		self.rCurrentEvent = None
		self.iNextUpdate = 0
		self.Objects = {}
		
	def __LoadWindow(self):
		try:
			PythonScriptLoader = ui.PythonScriptLoader()
			PythonScriptLoader.LoadScriptFile(self, "uiscript/popupsystem_window.py")
		except:
			import exception
			exception.Abort("PopupSystemInterface.LoadDialog.LoadObject")

		try:
			GetObject = self.GetChild
			self.Objects = {}
			self.Objects["Board"] = GetObject("Board")
			self.Objects["Popup_Icon"] = GetObject("Popup_Icon_Image")
			self.Objects["Popup_Item_Icon"] = GetObject("Popup_Item_Icon_Window")
			self.Objects["Popup_Header"] = GetObject("Popup_Header_Text")
			self.Objects["Popup_Text"] = GetObject("Popup_Text_Area")

			self.Objects["Popup_Lines"] = []
		except:
			import exception
			exception.Abort("PopupSystemInterface.LoadDialog.BindObject")

		self.Show()

	def PrepareInterface(self, sHeader, sTxt, sIcon):
		## Remove old texts
		for rLine in self.Objects["Popup_Lines"]:
			rLine.Hide()
			del rLine

		## Replace header
		self.Objects["Popup_Header"].SetText(sHeader)

		## Fill with desc
		for iNum, sLine in enumerate(uiToolTip.SplitDescription(sTxt, self.TEXTLINE_LEN_LIMIT)):
			self.__MakeTextLine(iNum, sLine)

		## Load new icon if exits, otherwise remove old one
		if type(sIcon) is str:
			self.Objects["Popup_Icon"].Hide()
			self.Objects["Popup_Item_Icon"].Hide()
			if len(sIcon) > 0:
				self.Objects["Popup_Icon"].LoadImage(sIcon)
				self.Objects["Popup_Icon"].Show()
		else:
			# self.Objects["Popup_Icon"].Hide()
			## New load item image
			item.SelectItem(sIcon)
			(width, height) = item.GetItemSize()
			self.Objects["Popup_Item_Icon"].LoadImage(item.GetIconImageFileName())
			self.Objects["Popup_Item_Icon"].SetPosition((32 - width * 32) / 2, (32 - height * 32) / 2)
			self.Objects["Popup_Item_Icon"].LoadImage(item.GetIconImage())
			# self.Objects["Popup_Item_Icon"].SetScale(32.0 / width*32, 32.0 / height*32)
			self.Objects["Popup_Item_Icon"].Show()

	""" Remote """
	def RecvPopupCommand(self, sHeader, sTxt, sIcon):
		self.qPopupEvents.put(self.PopupEvent(self, sHeader.replace("|", " "), sTxt.replace("|", " "), sIcon))
	""" """

	def __MakeTextLine(self, iNum, sTxt):
		textLine = ui.TextLine()
		textLine.SetParent(self.Objects["Popup_Text"])
		textLine.SetPosition(self.TEXTLINE_BASEPOS[0], self.TEXTLINE_BASEPOS[1] + (iNum*14))
		textLine.SetWindowHorizontalAlignCenter()
		textLine.SetHorizontalAlignCenter()
		textLine.SetText(sTxt)
		textLine.SetPackedFontColor(self.TEXTLINE_COLOUR)
		textLine.Show()
		self.Objects["Popup_Lines"].append(textLine)

	def OnUpdate(self):
		if self.iNextUpdate >= app.GetTime():
			if self.rCurrentEvent == None:
				if self.qPopupEvents.empty():
					return

				## Chuck new event and start processing it
				print "Processing next element.."
				self.rCurrentEvent = self.qPopupEvents.get()
				self.rCurrentEvent.StartProcessing()

			if not self.rCurrentEvent.IsPending():
				if self.rCurrentEvent.ProcessTick():
					self.rCurrentEvent.UpdateStatus()
					if self.rCurrentEvent.GetStatus() == self.PopupEvent.STATUS_DICT["PENDING"]:
						self.rCurrentEvent.SetTimer()

				## Check if process is over
				if self.rCurrentEvent.GetStatus() == self.PopupEvent.STATUS_DICT["DONE"]:
					print "Task is over. Waiting for next schedule.."
					self.rCurrentEvent = None

		else:
			self.iNextUpdate = app.GetTime()+self.UPDATE_FREQUENCY
