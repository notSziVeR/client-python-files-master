import item

class IItem(object):
	def __init__(self):
		pass

	def GetSize(self):
		raise Exception("NotImplementedException")

class SizeItem(IItem):
	def __init__(self, size):
		IItem.__init__(self)

		self.__size = size

	def GetSize(self):
		return self.__size

class Grid:
	class Iterator(object):
		def __init__(self, grid):
			self.__grid = grid

			self.__pos = 0

		def __next__(self):
			if self.__pos >= self.__grid.GetSize():
				raise StopIteration
			else:
				self.__pos += 1
				return self.__grid.GetGlobal(self.__pos - 1)

		# __next__ is a py3 meta function ...
		def next(self):
			return self.__next__()

	def __init__(self, width, height, pages = 1):
		self.__width = width
		self.__height = height
		self.__pages = pages

		self.Initialize()

	def Initialize(self):
		self.__size = self.GetWidth() * self.GetHeight() * self.GetPages()

		self.__items = [None for x in xrange(self.GetSize())]

	def ToGlobalPosition(self, x, y, z):
		return self.GetWidth() * self.GetHeight() * z + \
			self.GetWidth() * y + \
			x

	def ToLocalPosition(self, position):
		page = position / (self.GetWidth() * self.GetHeight())

		position = position % (self.GetWidth() * self.GetHeight())

		row = position / self.GetWidth()
		col = position % self.GetWidth()

		return (col, row, page)

	def Put(self, item, x, y, z):
		return PutGlobal(item, self.ToGlobalPosition(x, y, z))

	def PutGlobal(self, item, position):
		if not self.IsBlankGlobal(item, position):
			return False

		self.__items[position] = item
		return True

	def Get(self, x, y, z):
		return self.GetGlobal(self.ToGlobalPosition(x, y, z))

	def GetGlobal(self, position):
		return self.__items[position]

	def Clear(self, x, y, z):
		return self.ClearGlobal(self.ToGlobalPosition(x, y, z))

	def ClearGlobal(self, position):
		item = self.__items[position]
		self.__items[position]

		return item

	def IsBlank(self, item, x, y, z):
		if (y + item.GetSize()) > self.GetHeight():
			return False

		for size in xrange(item.GetSize()):
			if self.Get(x, y + size, z):
				return False

		if y > 0:
			for row in xrange(y - 1, -1, -1):
				itemAbove = self.Get(x, row, z)
				if itemAbove:
					if (row + itemAbove.GetSize()) > y:
						return False

					break

		return True

	def IsBlankGlobal(self, item, position):
		return self.IsBlank(item, *self.ToLocalPosition(position))

	def FindBlank(self, item):
		extraSpace = item.GetSize() - 1

		for page in xrange(0, self.GetPages()):
			for row in xrange(0, self.GetHeight() - extraSpace):
				for col in xrange(0, self.GetWidth()):
					if self.IsBlank(item, col, row, page):
						return self.ToGlobalPosition(col, row, page)

		return -1

	def GetWidth(self):
		return self.__width

	def GetHeight(self):
		return self.__height

	def GetPages(self):
		return self.__pages

	def GetSize(self):
		return self.__size

	def __iter__(self):
		return self.Iterator(self)
