# coding=utf-8
txt = 'Paste Source Text Here'

import sys
import uuid
import requests
import hashlib
import time
from imp import reload
from datetime import datetime
reload(sys)

YOUDAO_URL = 'https://openapi.youdao.com/api'
APP_KEY = 'Paste Your Youdao App Key Here'
APP_SECRET = 'Paste Your Youdao App Secret Here'

def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()

def truncate(q):
    if q is None:
        return None
    size = len(q)
    return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)

def translate(line):
    data = {}
    data['from'] = 'auto'
    data['to'] = 'zh-CHS' # Change to Your Targeted Language Here
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())#
    signStr = APP_KEY + truncate(line) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['q'] = line
    data['salt'] = salt
    data['sign'] = sign
    #data['vocabId'] = "" # Specify Your Vocabulary Library When Necessary 

    response = do_request(data)
    content = response.json()
    return content["translation"][0]
    #return content["translation"][0].encode("utf-8").decode("gbk")


if __name__ == '__main__':
    current_time = datetime.now()
    formatted_time = current_time.strftime("%Y-%m-%d-%H-%M-%S")
    
    # Output Saved File Will Be Named Under This Format:
    file_name = "Output-" + formatted_time + "-Youdao.txt"

    #translator = deepl.Translator(api)
    text_file = open (file_name, "w", encoding='utf-8')
    i = 1
    for line in txt.splitlines():
        if line=='':
            text_file.write('\n')
            print('Process:', i, 'Out of ', len(txt.splitlines()))
            i+=1
            continue
        translated_text = translate(line)
        text_file.write(line)
        text_file.write('\n')
        text_file.write(translated_text)
        text_file.write('\n')
        print('Process:', i, 'Out of ', len(txt.splitlines()))
        i += 1
        time.sleep(2)
    text_file.close()
    print("Saved as " + file_name)
    
