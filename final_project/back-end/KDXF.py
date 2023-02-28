# @Author: Dear-xxf
# @School: TongJi University
# With great power, comes great responsibility.

# @Author: Dear-xxf
# @School: TongJi University
# With great power, comes great responsibility.


import base64
import hashlib
import hmac
import json
import logging
import threading
import time
from socket import *
from urllib.parse import quote
import numpy as np
import os
import ffmpy3

import websocket
from websocket import create_connection

# reload(sys)
# sys.setdefaultencoding("utf8")
logging.basicConfig()

base_url = "ws://rtasr.xfyun.cn/v1/ws"
app_id = "85816698"
api_key = "8adbf9b918f500febc806c02c0535182"
file_path = r"myVoice.pcm"

pd = "edu"

end_tag = "{\"end\": true}"


class Client():
    def __init__(self):
        ts = str(int(time.time()))
        tt = (app_id + ts).encode('utf-8')
        md5 = hashlib.md5()
        md5.update(tt)
        baseString = md5.hexdigest()
        baseString = bytes(baseString, encoding='utf-8')

        apiKey = api_key.encode('utf-8')
        signa = hmac.new(apiKey, baseString, hashlib.sha1).digest()
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')

        self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()

    def send(self, file_path):
        file_object = open(file_path, 'rb')
        try:
            index = 1
            while True:
                chunk = file_object.read(1280)
                if not chunk:
                    break
                self.ws.send(chunk)

                index += 1
                time.sleep(0.04)
        finally:
            file_object.close()

        self.ws.send(bytes(end_tag.encode('utf-8')))
        # print("send end tag success")

    def recv(self):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    # print("receive result end")
                    break
                result_dict = json.loads(result)
                if result_dict["action"] == "started":
                    # print("handshake success, result: " + result)
                    pass
                if result_dict["action"] == "result":
                    result_1 = result_dict
                    data = json.loads(result_1["data"])
                    result_str = ''
                    for i in data["cn"]["st"]["rt"][0]["ws"]:
                        for w in i["cw"]:
                            result_str += w["w"]
                    if result_str == '.' or result_str == '。' or result_str == ',' or result_str == '，' :
                        pass
                    else:
                        print("rtasr result: " + result_str)
                        file_handle = open('result.txt', mode='w')
                        file_handle.write(result_str)
                        file_handle.close()

                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return
        except websocket.WebSocketConnectionClosedException:
            # print("receive result end")
            pass

    def close(self):
        self.ws.close()
        print("connection closed")


def wav_to_pcm():
    f = open('speech.wav', "rb")
    f.seek(0)
    f.read(1024)
    data = np.fromfile(f, dtype=np.int16)
    filePath = str('./myVoice.wav').split('/')
    path = ''
    for item in filePath[:-1]:
        path += item + '/'
    path += 'myVoice.pcm'
    data.tofile(path)


def mp3_to_pcm(fls):
    if os.path.splitext(fls)[-1] != '.mp3':
        return
    fname = os.path.splitext(os.path.basename(fls))[0]
    print("开始转换..." + fname)
    # fname = os.path.splitext(fls)[0]
    ff = ffmpy3.FFmpeg(
        inputs={fls: '-y'},
        outputs={
            './send.pcm': '-acodec pcm_s16le -f s16le -ac 1 -ar 16000'}
    )
    ff.run()
