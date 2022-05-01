
import os
import time
from numpy import mean
from pymsfilereader import MSFileReader


# 钉钉机器人加签获取发送的url模板
def dingtalk_url():
    import hmac
    import hashlib
    import base64
    import urllib.parse

    timestamp = str(round(time.time() * 1000))
    # 钉钉机器人加签密钥SEC开头
    secret = 'SECxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # 钉钉机器人Webhook+加签拼接
    url = f'https://oapi.dingtalk.com/robot/send?access_token=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx&timestamp={timestamp}&sign={sign}'
    return url


# 钉钉机器人发送文本消息模板
def send_msg(text, mobile):
    import requests
    import json

    str_mobile = f'"{mobile}"'
    url = dingtalk_url()
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    json_text = {
                "msgtype": "text",
                "text": {
                    "content": text
                },
                "at": {
                    "atMobiles": [
                        str_mobile
                    ],
                    "isAtAll": False
                }
            }
    send = requests.post(url, json.dumps(json_text), headers=headers).content
    pass


#将原始数据文件按时间进行排序，选择第二个文件，防止第一个文件正在运行而无法读取
def get_rawdata(file_path):
    raw_list = list()
    new_list = list()
    for dirpath, dirnames, filenames in os.walk(file_path):
        if filenames:
            for i in filenames:
                # Thermo文件结尾.raw
                if i.endswith('.raw'):
                    file_name = i
                    abs_path = os.path.join(dirpath, i)
                    raw_list.append(abs_path)
    # 按时间顺序排序
    '''
    os.path.getmtime() 函数是获取文件最后修改时间
    os.path.getctime() 函数是获取文件最后创建时间
    '''
    new_list = sorted(raw_list,  key=lambda x: os.path.getctime(x), reverse=True)
    return new_list[1]


# 获取原始数据质量轴误差
def get_rawdata_ppm(file_path):
    rawfile = MSFileReader(file_path)
    ppm_list = list()
    for i in range(1, rawfile.ScanNumFromRT(RT=10.0)):
        # massRange<112ppm进行前十分钟质谱峰提取
        raw_ppm = rawfile.GetMassListRangeFromScanNum(scanNumber=i, massRange="445.07-445.17", centroidResult=True)
        a = raw_ppm[0][0]
        if len(a) >= 1:
            ppm_list.append(a[0])
    rawfile.Close()
    # 计算误差
    ppm = round((mean(ppm_list) - 445.12003) / 445.12003 * 100000, 2)
    return ppm


if __name__ == '__main__':
    QE_file_path = r'D:\DATA'
    data = get_rawdata(QE_file_path)
    ppm = get_rawdata_ppm(data)
    if abs(ppm) >= 5.0:
        warning_text = "质量轴偏移过大：" + str(ppm) + "ppm"
        send_msg(warning_text, 135xxxxxxxx)
