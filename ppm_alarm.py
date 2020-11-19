# -*- coding: utf-8 -*-
import os
import requests
import json
from numpy import mean
from pymsfilereader import MSFileReader

#定义发送钉钉报警的函数
def send_msg(text,mobile):
    url = 'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    json_text = {
                "msgtype": "text",
                "text": {
                    "content": text
                },
                "at": {
                    "atMobiles": [
                        mobile
                    ],
                    "isAtAll": False
                }
            }
    requests.post(url, json.dumps(json_text), headers=headers).content

#钉钉联系人
abc = "\"130xxxxxxxx\""

#将STRONGWASH文件按时间进行排序
def get_wash_list(file_path):
    dir_list = os.listdir(file_path)
    wash_list = []
    if not dir_list:
        return
    else:
        # os.path.getmtime() 函数是获取文件最后修改时间
        # os.path.getctime() 函数是获取文件最后创建时间
        dir_list = sorted(dir_list,  key=lambda x: os.path.getmtime(os.path.join(file_path, x)),reverse = True)
        for file in dir_list:
            if "STRONGWASH" in file:
                wash_list.append(file)
        return wash_list

#选择第二个STRONGWASH文件，防止第一个STRONGWASH正在运行而无法读取
def get_wash_path():
    wash = get_wash_list("D:\\raw data")
    washfile = ("D:\\raw data\\" + wash[1])
    print(washfile)
    return(washfile)

#读取质量轴偏离程度ppm，需要设置LockMass=445.12003
def get_ppm():
    rawfile = MSFileReader(get_wash_path())
    ppmlist = []
    for scan_number in range(rawfile.FirstSpectrumNumber, rawfile.LastSpectrumNumber + 1):
        t = rawfile.GetTrailerExtraForScanNum(scan_number)
        ppmlist.append(float(t['LM m/z-Correction (ppm)']))
    ppm = mean(ppmlist)
    print(ppm)
    return(ppm)

P = get_ppm()
text = ("[***WARNING***]\n质量轴偏移过大，需要校正\nppm=%f"%P)
if abs(P) >= 4.5:
    send_msg(text, abc)
