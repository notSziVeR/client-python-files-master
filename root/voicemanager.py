import pyaudio
import threading
import time
import struct
import chat
import net

class voiceManager:
	MAX_DISTANCE = 200
	DEFAULT_FORMAT = pyaudio.paInt16
	DEFAULT_CHANNELS = 1
	DEFAULT_RATE = 20000
	DEFAULT_CHUNK = 1024

	def __init__(self):
		self.audioPackets = []
		self.audioData = []
		self.recording = False
		self.wait = 0
		self.time = time.clock()
		self.timeDelta = 0
		self.packets = []

		self.p = pyaudio.PyAudio()

		self.recordStream = self.p.open(format=voiceManager.DEFAULT_FORMAT,
			channels=voiceManager.DEFAULT_CHANNELS,
			rate=voiceManager.DEFAULT_RATE,
			input=True,
			frames_per_buffer=voiceManager.DEFAULT_CHUNK
			#stream_callback=self._recordCallback
			)
		self.playStream = self.p.open(format=voiceManager.DEFAULT_FORMAT,
			channels=voiceManager.DEFAULT_CHANNELS,
			rate=voiceManager.DEFAULT_RATE,
			output=True,
			frames_per_buffer=voiceManager.DEFAULT_CHUNK
			#stream_callback=self._playCallback
			)

	def iteration(self):
		try:
			timeTmp = time.clock()
			self.timeDelta = timeTmp - self.time
			self.wait -= self.timeDelta
			self.time = timeTmp

			if self.wait > 0:
				return

			if self.recordStream.get_read_available() >= voiceManager.DEFAULT_CHUNK:
				inData = self.recordStream.read(voiceManager.DEFAULT_CHUNK)

				if self.recording:
					inData = struct.unpack("%dh" % voiceManager.DEFAULT_CHUNK, inData)
					self._sendAudio(inData)

			data = [0] * voiceManager.DEFAULT_CHUNK
			packetsCount = 0

			if len(self.audioPackets) == 0:
				return

			startTime = self.time + 100
			for packet in self.audioPackets:
				if startTime > packet[2]:
					startTime = packet[2]

			if (self.time - startTime) < (0.4 * voiceManager.DEFAULT_CHUNK / voiceManager.DEFAULT_RATE):
				self.wait = 0.1 * voiceManager.DEFAULT_CHUNK / voiceManager.DEFAULT_RATE
				return

			for packet in self.audioPackets:
				if (packet[2] - startTime) >= (0.8 * voiceManager.DEFAULT_CHUNK / voiceManager.DEFAULT_RATE):
					continue

				self.audioPackets.remove(packet)

				packetsCount += 1

				for i in xrange(voiceManager.DEFAULT_CHUNK):
					data[i] += packet[1][i]

			if packetsCount > 1:
				for i in xrange(len(data)):
					data[i] = int(data[i] / max(1, packetsCount))

			data = struct.pack("%dh" % voiceManager.DEFAULT_CHUNK, *data)

			self.playStream.write(data)
		except Exception as e:
			sys_err("Error lol", e)

	def run(self):
		pass

	def Destroy(self):
		pass

	def __del__(self):
		self.audioData = []
		self.audioPackets = []

		self.recordStream.stop_stream()
		self.recordStream.close()

		self.playStream.stop_stream()
		self.playStream.close()

		self.p.terminate()

	def _audioByDistance(self, data, distance):
		volume = 1.0 - distance

		if volume <= 0.1:
			return [[0]] * voiceManager.DEFAULT_CHUNK

		volume = volume ** 2

		return [int(frame * volume) for frame in data]

	def addAudio(self, name, data, distance):
		self.audioPackets.append([name,
			self._audioByDistance(data, distance),
			time.clock()])

	def _sendAudio(self, data):
		# DEBUG
		#self.addAudio('me', data, 0, time.clock())
		net.netSendVoiceStart(data)
