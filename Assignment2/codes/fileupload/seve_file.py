#!/usr/bin/python3
# -*- coding:utf-8 -*-

import json
import math
import os
import time
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlparse
import requests
from urllib3 import encode_multipart_formdata

lfasr_host = 'http://upload-ost-api.xfyun.cn/file'
# The name of the requested interface
api_init = '/mpupload/init'
api_upload = '/upload'
api_cut = '/mpupload/upload'
api_cut_complete = '/mpupload/complete'
api_cut_cancel = '/mpupload/cancel'
# The size of a file fragment is 5M
file_piece_sice = 5242880


# Upload
class SeveFile:
    def __init__(self, app_id, api_key, api_secret,upload_file_path):
        self.app_id = app_id
        self.api_key = api_key
        self.api_secret = api_secret
        self.request_id = '0'
        self.upload_file_path = upload_file_path
        self.cloud_id = '0'

    # request_id process
    def get_request_id(self):
        return time.strftime("%Y%m%d%H%M")

    # header process
    def hashlib_256(self, data):
        m = hashlib.sha256(bytes(data.encode(encoding='utf-8'))).digest()
        digest = "SHA-256=" + base64.b64encode(m).decode(encoding='utf-8')
        return digest

    # header process 
    def assemble_auth_header(self, requset_url, file_data_type, method="", api_key="", api_secret="", body=""):
        u = urlparse(requset_url)
        host = u.hostname
        path = u.path
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))
        digest = "SHA256=" + self.hashlib_256('')
        signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1\ndigest: {}".format(host, date, method, path, digest)
        signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
        authorization = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
            api_key, "hmac-sha256", "host date request-line digest", signature_sha)
        headers = {
            "host": host,
            "date": date,
            "authorization": authorization,
            "digest": digest,
            'content-type': file_data_type,
        }
        return headers

    # post api
    def call(self,  url, file_data, file_data_type):
        api_key = self.api_key
        api_secret = self.api_secret
        headerss = self.assemble_auth_header(url, file_data_type, method="POST",
                                             api_key= api_key,api_secret = api_secret, body = file_data)
        try:
            resp = requests.post(url, headers=headerss, data=file_data, timeout=8)
            #print(resp.status_code, resp.text)
            return resp.json()
        except Exception as e:
            print("Exception ：%s" % e)

    # pre-process
    def prepare_request(self):
        return self.gene_params(apiname=api_init)

    # Generate different parameters for different apiname
    def gene_params(self, apiname):
        appid = self.app_id
        request_id = self.get_request_id()
        upload_file_path = self.upload_file_path
        cloud_id = self.cloud_id
        body_dict = {}
        # Upload File API
        if apiname == api_upload:
            try:
                with open(upload_file_path, mode='rb') as f:
                    file = {
                        "data": (upload_file_path, f.read()),
                        "app_id": appid,
                        "request_id": request_id,
                        "cloud_id": cloud_id,
                    }
                    #print('文件：', upload_file_path, ' 文件大小：', os.path.getsize(upload_file_path))
                    encode_data = encode_multipart_formdata(file)
                    file_data = encode_data[0]
                    file_data_type = encode_data[1]
                url = lfasr_host + api_upload
                fileurl = self.call(url, file_data, file_data_type)
                #print("文件上传参数",file_data)
                return fileurl
            except FileNotFoundError:  # 文件不能找到的异常处理
                print("Sorry!The file " + upload_file_path + " can't find.")
            # pre-process api
        elif apiname == api_init:
            body_dict['app_id'] = appid
            body_dict['request_id'] = request_id
            body_dict['cloud_id'] = cloud_id
            url = lfasr_host + api_init
            file_data_type = 'application/json'
            return self.call(url, json.dumps(body_dict), file_data_type)
        elif apiname == api_cut:
            # pre-process
            upload_prepare = self.prepare_request()
            if upload_prepare:
                upload_id = upload_prepare['data']['upload_id']
            # Block to upload
            self.do_upload(upload_file_path, upload_id)
            body_dict['app_id'] = appid
            body_dict['request_id'] = request_id
            body_dict['upload_id'] = upload_id
            # The uploading is complete
            fileurl = self.upload_cut_complete(body_dict)
            return fileurl
            # Block uploading is cancelled
            # self.upload_cut_cancel(body_dict)

    # The uploading is complete
    def upload_cut_complete(self, body_dict):
        file_data_type = 'application/json'
        url = lfasr_host + api_cut_complete
        fileurl = self.call(url, json.dumps(body_dict), file_data_type)
        return fileurl['data']['url']

    # Block uploading is cancelled
    def upload_cut_cancel(self, body_dict):
        file_data_type = 'application/json'
        url = lfasr_host + api_cut_cancel
        return self.call(url, json.dumps(body_dict), file_data_type)

    # Fragment Upload Request
    def upload_request(self, slice_id, file_data_size, upload_id):
        appid = self.app_id
        request_id = self.get_request_id()
        upload_file_path = self.upload_file_path
        while True:
            try:
                with open(upload_file_path, mode='rb') as content:
                    if not content:
                        break
                    file = {
                        "data": (upload_file_path, content.read(file_data_size)),
                        "app_id": appid,
                        "request_id": request_id,
                        "upload_id": upload_id,
                        "slice_id": slice_id,
                    }
                    encode_data = encode_multipart_formdata(file)
                    file_data = encode_data[0]
                    file_data_type = encode_data[1]
                    url = lfasr_host + api_cut
                    response = self.call(url, file_data, file_data_type)
                if response.get('code') != 0:
                    # 上传分片失败
                    print('upload slice fail, response: ' + str(response))
                    return False
            except FileNotFoundError:  # 文件不能找到的异常处理
                print("Sorry!The file " + upload_file_path + " can't find.")
            return True

    # segment upload
    def do_upload(self, file_path, upload_id):
        file_total_size = os.path.getsize(file_path)
        chunk_size = file_piece_sice
        chunks = math.ceil(file_total_size / chunk_size)
        print('文件：', file_path, ' 文件大小：', file_total_size, ' 分块大小：', chunk_size, ' 分块数：', chunks)
        for i in range(chunks):
            print('chunk', i)
            if i + 1 == chunks:
                current_size = file_total_size % chunk_size
            else:
                current_size = chunk_size
            self.upload_request(i+1, current_size, upload_id)


