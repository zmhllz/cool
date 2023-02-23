import pymysql
import requests
import json
import time
import urllib.request
import datetime
import uuid
import io
import os
import urllib.parse
import base64
import m3u8
from Crypto.Cipher import AES
from Crypto import Random
import glob
from urllib.parse import urljoin

headers = {
    "X-Access-Token": "",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
}
def download(url, path, name): 

    res = requests.get(url)
    print(res)
    ContentType = res.headers['Content-Type']
    print(ContentType)
    if ContentType == 'video/mp4':
        with open('{}\{}'.format(path, '{}.mp4'.format(name)), 'wb') as file:
            file.write(res.content)
    elif ContentType == 'text/html':
        pass
    elif ContentType == 'application/x-mpegurl':
        video = m3u8.load(url)
        segments = video.segments
        with open('{}\{}.mp4'.format(path, name), 'wb') as fw:
            for i in range(len(segments)):
                ts_url = segments[i]
                file_name = ts_url.uri
                file_name = urljoin(url, file_name)
                print(file_name)
                try:
                    response = requests.get(file_name, stream=True, verify=False)
                    fw.write(response.content)
                except Exception as e:
                    print(e)
    else:
        ContentDisposition = res.headers['Content-Disposition']
        # ContentDisposition = res.headers
        print(ContentDisposition)
        ContentDisposition = ContentDisposition.replace('attachment;filename=', '')
        ContentDisposition = urllib.parse.unquote(ContentDisposition)
        print(ContentDisposition)
        with open('{}\{}'.format(path, ContentDisposition), 'wb') as file:
            file.write(res.content)

def cool_api(parentId, pe):
    url1 = " ".format(
        parentId, parentId)
    response = requests.get(url1, headers=headers)
    jsonData = json.loads(response.text)
    jsonLists = jsonData['list']
    # print(jsonLists)
    for i in range(len(jsonLists)):
        resource = jsonLists[i]['resource']
        type = jsonLists[i]['type']
        name = resource['name']
        print(name)
        name = name.replace('/', '-').replace(':', '-')
        if type == 'resource_classify':
            # global path
            path = r'{}\{}'.format(pe, name)
            print(path)
            os.mkdir(path)
            cool_api(resource['id'], path)
        else:
            url = resource['url']
            print(url)
            download(url, pe, name)
            print('成功')
if __name__ == '__main__':
    cool_api(0, r'路径')
    

