import os
import app
import localeInfo
import debugInfo

CHINA_PORT = 50000

def BuildServerList(orderList):
	retMarkAddrDict = {}
	retAuthAddrDict = {}
	retRegion0 = {}

	ridx = 1
	for region, auth, mark, channels in orderList:
		cidx = 1
		channelDict = {}
		for channel in channels:
			key = ridx * 10 + cidx
			channel["key"] = key
			channelDict[cidx] = channel
			cidx += 1

		region["channel"] = channelDict

		retRegion0[ridx] = region
		retAuthAddrDict[ridx] = auth
		retMarkAddrDict[ridx*10] = mark
		ridx += 1

	return retRegion0, retAuthAddrDict, retMarkAddrDict

app.ServerName = None

if app.ENABLE_SERVER_SELECT_RENEWAL:
	STATE_NONE = localeInfo.CHANNEL_STATUS_OFFLINE
	STATE_DICT = {
		0 : localeInfo.CHANNEL_STATUS_OFFLINE,
		1 : localeInfo.CHANNEL_STATUS_VACANT,
		2 : localeInfo.CHANNEL_STATUS_RECOMMENDED,
		3 : localeInfo.CHANNEL_STATUS_BUSY,
		4 : localeInfo.CHANNEL_STATUS_FULL,
	}

	STATE_REVERSE_DICT = {}
	STATE_COLOR_DICT = { "..." : 0xffdadada} # ?????? channel??? ...? ???? ??? ??? ??.
	STATE_COLOR_LIST = [ 0xffffffff, 0xffdadada, 0xff00ff00, 0xffffc000, 0xffff0000 ]

	idx = 0
	for key, value in STATE_DICT.items():
		STATE_REVERSE_DICT[value] = key
		STATE_COLOR_DICT[value] = STATE_COLOR_LIST[idx%len(STATE_COLOR_LIST)]
		idx += 1

	SERVER_STATE_DICT = {
		"NONE" : 0,
		"NEW" : 1,
		"SPECIAL" : 2,
		"CLOSE" : 3
	}

if not app.ENABLE_SERVER_SELECT_RENEWAL:
	if app.ENABLE_CHANNEL_LIST:
		STATE_NONE = "Offline"
		STATE_DICT = { 0 : "Offline", 1 : "Available", 2 : "Busy", 3 : "Full" }
		STATE_COLOR_DICT = { "Offline" : 0xffdadada, "Available" : 0xff00ff00, "Busy" : 0xffffff00, "Full" : 0xffff0000}
	else:
		STATE_NONE = "..."

		STATE_DICT = {
			0 : "....",
			1 : "NORM",
			2 : "BUSY",
			3 : "FULL"
		}

SERVER01_CHANNEL_DICT = {
	1 : {
		"key" : 11,
		"name" : "Xantios-1   ",
		"ip" : "192.168.0.36",
		"tcp_port" : 30003,
		"udp_port" : 30003,
		"state" : STATE_NONE,
		'count' : 0,
	},
	2 : {
		"key" : 12,
		"name" : "Xantios-2   ",
		"ip" : "192.168.0.36",
		"tcp_port" : 30007,
		"udp_port" : 30007,
		"state" : STATE_NONE,
		'count' : 0,
	},
}

SERVER02_CHANNEL_DICT = {
	1 : {
		"key" : 11,
		"name" : "CH1   ",
		"ip" : "192.168.0.36",
		"tcp_port" : 30003,
		"udp_port" : 30003,
		"state" : STATE_NONE,
		'count' : 0,
	},
	2 : {
		"key" : 12,
		"name" : "CH2   ",
		"ip" : "192.168.0.36",
		"tcp_port" : 30007,
		"udp_port" : 30007,
		"state" : STATE_NONE,
		'count' : 0,
	},
}

SERVER03_CHANNEL_DICT = {
	1 : {
		"key" : 11,
		"name" : "CH1   ",
		"ip" : "176.122.226.5",
		"tcp_port" : 30003,
		"udp_port" : 30003,
		"state" : STATE_NONE,
		'count' : 0,
	},
	2 : {
		"key" : 12,
		"name" : "CH2   ",
		"ip" : "176.122.226.5",
		"tcp_port" : 30007,
		"udp_port" : 30007,
		"state" : STATE_NONE,
		'count' : 0,
	},
}

REGION_NAME_DICT = {
	0 : "Europe",
}

REGION_AUTH_SERVER_DICT = {
	0 : {
		1 : {
			"ip" : "192.168.0.36",
			"port" : 30001,
		},
		2 : {
			"ip" : "192.168.0.36",
			"port" : 30001,
		},
		3 : {
			"ip" : "176.122.226.5",
			"port" : 30001,
		},
	}
}

REGION_DICT = {
	0 : {
		1 : {
			"name" : "Xantios. Win32",
			"channel" : SERVER01_CHANNEL_DICT,
			"state" : "SPECIAL",
		},
		2 : {
			"name" : "Xantios. FreeBSD",
			"channel" : SERVER02_CHANNEL_DICT,
			"state" : "SPECIAL",
		},
		3 : {
			"name" : "Test Server",
			"channel" : SERVER03_CHANNEL_DICT,
			"state" : "NEW",
		},
	},
}

MARKADDR_DICT = {
	10 : {
		"ip" : "192.168.0.36",
		"tcp_port" : 12101,
		"mark" : "10.tga",
		"symbol_path" : "10",
	},
	20 : {
		"ip" : "192.168.1.4",
		"tcp_port" : 12101,
		"mark" : "10.tga",
		"symbol_path" : "10",
	},
	30 : {
		"ip" : "176.122.226.5",
		"tcp_port" : 12101,
		"mark" : "10.tga",
		"symbol_path" : "10",
	},
}

TESTADDR = {
	"ip" : "192.168.0.36",
	"tcp_port" : 50000,
	"udp_port" : 50000,
}
