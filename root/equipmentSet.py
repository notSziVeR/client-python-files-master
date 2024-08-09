import xml.dom.minidom as xml
import item
import player

class EquipmentSet:
	def __init__(self, id, name, applies):
		self.id = id
		self.name = name
		self.applies = applies

_sets = dict()

def get(id):
	return _sets.get(id, None)

def getEq():
	EQUIPMENT_ITEMS = [
		item.EQUIPMENT_HEAD,
		item.EQUIPMENT_BODY,
		item.EQUIPMENT_WEAPON,
		item.EQUIPMENT_WRIST,
		item.EQUIPMENT_SHOES,
		item.EQUIPMENT_NECK,
		item.EQUIPMENT_EAR,
		item.EQUIPMENT_SHIELD,
		item.COSTUME_SLOT_BODY,
		item.COSTUME_SLOT_HAIR,
		item.COSTUME_SLOT_WEAPON,
	]
	
	counts = {}
	for pos in EQUIPMENT_ITEMS:
		vnum = player.GetItemIndex(pos)
		if vnum == 0:
			continue
		
		id = item.GetItemEquipmentSetId(vnum)
		if id == 0:
			continue
		
		counts[id] = counts.get(id, 0) + 1
	
	return counts

def load(filename):
	try:
		content = open(filename, "r").read()
		
		dom = xml.parseString(content)
	except Exception as e:
		import dbg
		dbg.TraceError("Failed to parse {}: {}".format(filename, e))
		return
	
	sets = dom.getElementsByTagName("EquipmentSet")
	for set in sets:
		id = int(set.attributes["id"].value)
		name = set.attributes["name"].value
		
		domApplies = set.getElementsByTagName("Apply")
		applies = []
		for domApply in domApplies:
			applyType = 63
			applyValue = 5
			count = 5

			applies.append((applyType, applyValue, count))
		
		_sets[id] = EquipmentSet(id, name, applies)
