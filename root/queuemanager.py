import app
import ui
class Queue(object):
	EXIT = 0

	def __init__(self):
		self.eventList = []
		self.eventLockedList = []

	def __del__(self):
		del self.eventList
		del self.eventLockedList

	def GetEvent(self, eventName):
		""" Get the event dictionary by specific name. """
		for event in self.eventList:
			if event['name'] == eventName:
				return event
		return None

	def GetIsLockedEvent(self, eventName):
		""" Get a boolean if a specific event is locked. """
		for event in self.eventLockedList:
			if event['name'] == eventName:
				return True
		return False

	def LockEvent(self, eventName):
		""" Lock a specific event by name for being processed. """
		event = self.GetEvent(eventName)
		if event and not event in self.eventLockedList:
			self.eventLockedList.append(event)

	def UnlockEvent(self, eventName):
		""" Unlock a specific event by name for being processed. """
		event = self.GetEvent(eventName)
		if event in self.eventLockedList:
			self.eventLockedList.remove(event)

	def DeleteEvent(self, eventName):
		""" Delete a specific event by name instantly. """
		event = self.GetEvent(eventName)
		if event:
			self.eventList.remove(event)

	def ResetTimeEvent(self, eventName):
		""" Reset time of a specific event by name. """
		event = self.GetEvent(eventName)
		if event:
			index = self.eventList.index(event)
			self.eventList[index] = app.GetGlobalTimeStamp()

	def AppendEvent(self, eventName, eventStartTime, eventFunc, eventFuncArgs = ()):
		""" Append a new event by specific arguments. """
		if not eventName or not isinstance(eventStartTime, int) or not callable(eventFunc):
			return

		if not hasattr(type(eventFuncArgs), '__iter__'):
			eventFuncArgs = tuple([eventFuncArgs])

		if self.GetEvent(eventName):
			self.DeleteEvent(eventName)

		self.eventList.append({'name' : eventName, 'function' : ui.__mem_func__(eventFunc), 'arguments' : eventFuncArgs, 'run_next_time' : app.GetGlobalTimeStamp() + eventStartTime})

	def Process(self):
		""" Processing the events. """
		for index, event in enumerate(self.eventList):
			if event in self.eventLockedList:
				continue

			if app.GetGlobalTimeStamp() > event['run_next_time']:
				result = apply(event['function'], event['arguments'])
				if result in (None, self.EXIT):
					del self.eventList[index]
					continue

				event['run_next_time'] = app.GetGlobalTimeStamp() + result