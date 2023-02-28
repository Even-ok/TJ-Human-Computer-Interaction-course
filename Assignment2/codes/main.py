import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.config import Config
Config.set('graphics', 'width', '960')
Config.set('graphics', 'height', '540')  # 16:9

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader
import wave
import time
# import pyaudio
from XunfeiApi import *
from voiceControl import *
from kivy.clock import Clock
import threading
import os

# Supports Chinese
kivy.resources.resource_add_path('font/')
ft = kivy.resources.resource_find('DroidSansFallback.ttf')

# # Audio configuration
# CHUNK = 1024
# FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "./audio/test.wav"
IS_RECORDED = False
appid = "c974e19e"
apikey = "332e3d815b759a279563d0236f45602f"
apisecret = "OTc2MDExNDBhNGE2ZDYxY2U0NDRjNzUz"


class BoxLayoutWidget(BoxLayout):
	def __init__(self, **kwargs):
		super(BoxLayout,self).__init__(**kwargs)
		self.control = voiceControl ()
		self.ids.Speak.font_name = ft
		self.ids.Speak.text = "开始录音"
		self.ids.Listen.font_name = ft
		self.ids.Listen.text = "播放录音"
		self.ids.Submit.font_name = ft
		self.ids.Submit.text = "提交录音"
		self.ids.bottom_label.font_name = ft
		self.current_text = "请问您需要什么帮助?"
		self.on_start()
		self.last_result=''

	def on_start(self):
		Clock.schedule_interval(self.update_label,0)

	def update_label(self,nap):
		self.ids.bottom_label.text = self.current_text


	'''
	Recording function
	'''
	def StartRecording(self):
		self.current_text = "开始录制,请说话..."
		# threading.Thread(target=self.doRecording).start()

	# def doRecording(self):
	# 	p = pyaudio.PyAudio()
	# 	stream = p.open(format=FORMAT,
    #             channels=CHANNELS,
    #             rate=RATE,
    #             input=True,
    #             frames_per_buffer=CHUNK)

	# 	frames = []
	# 	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
	# 		data = stream.read(CHUNK)
	# 		frames.append(data)
	# 		value = int((i / int(RATE / CHUNK * RECORD_SECONDS)) * 100)
	# 		self.ids.progress_bar.value = value

	# 	self.ids.progress_bar.value = 100
	# 	stream.stop_stream()
	# 	stream.close()
	# 	p.terminate()
	# 	wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	# 	wf.setnchannels(CHANNELS)
	# 	wf.setsampwidth(p.get_sample_size(FORMAT))
	# 	wf.setframerate(RATE)
	# 	wf.writeframes(b''.join(frames))
	# 	wf.close()

	# 	print("录制结束!")
	# 	Clock.schedule_once(self.recordFinished)

	# def recordFinished(self,dt):
	# 	self.current_text = "录制结束!"
			
	'''
	Speech recognition
	'''

	def SubmitRecording(self):
		self.current_text = "正在转写语音..."
		threading.Thread(target=self.doUpload).start()

	def doUpload(self):
		file_path = r"./audio/test.wav"
		self.last_result=''
		# 文件上传
		api = seve_file.SeveFile(app_id=appid, api_key=apikey, api_secret=apisecret, upload_file_path=file_path)
		file_total_size = os.path.getsize(file_path)
		if file_total_size < 31457280:
			print("-----不使用分块上传-----")
			fileurl = api.gene_params('/upload')['data']['url']
		else:
			print("-----使用分块上传-----")
			fileurl = api.gene_params('/mpupload/upload')

		host = "ost-api.xfyun.cn"
		gClass = get_result(host, appid, apikey, apisecret,fileurl)
		# 创建订单
		print("\n------ 创建任务 -------")
		task_id = gClass.task_create()['data']['task_id']
		# 查询任务
		print("\n------ 查询任务 -------")
		print("任务转写中······")
		while True:
			result = gClass.task_query(task_id)
			if isinstance(result, dict) and result['data']['task_status'] != '1' and result['data']['task_status'] != '2':
				print("转写完成···\n")
				split_word_list = result['data']['result']['lattice'][0]['json_1best']['st']['rt'][0]['ws']
				for cw in split_word_list:
					word = cw['cw'][0]['w']
					self.last_result+=word
				print('\n')
				print('最后的结果为:'+self.last_result)

				Clock.schedule_once(self.uploadFinished)
				time.sleep(1)

				self.current_text = voiceControl.judgeOrder(self.control,self.last_result)

				break
			elif isinstance(result, bytes):
				print("发生错误···\n", result)
				break

	def uploadFinished(self,dt):
		self.current_text = "转写完成！您的指令为:"+self.last_result+'\n'+'正在为您处理...'
		
	'''
	Play recording
	'''
	def playAudio(self):
		self.current_text = "正在播放..."
		sound = SoundLoader.load("./audio/test.wav")
		if sound:
			print("Sound found at %s" % sound.source)
			print("Sound is %.3f seconds" % sound.length)
			sound.play()
		self.ids.progress_bar.value = 100
		threading.Thread(target=self.doPlay).start()
		self.update_label(0)

	def doPlay(self):
		Clock.schedule_once(self.playFinished)

	def playFinished(self,dt):
		time.sleep(3)
		self.current_text = "播放结束"



class TalkToMeApp(App):
	
	def build(self):
		return BoxLayoutWidget()
		
		
			
if __name__ == '__main__':
	# The interface is not allowed to change shape
	from kivy.config import Config
	from kivy.core.window import Window
	Window.size = (540, 960)
	Config.set('graphics', 'resizable',False)


	TalkToMeApp().run()
