#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import requests
import json
import time
import datetime as dt
import os

def send_line_message(token,message):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": "Bearer " + token,
    }
    files = {
        "message": (None, message),
    }
    res = requests.post(url, headers=headers, files=files)
    return res

def send_slack_message(token,channel,message):
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": "Bearer " + token,
    }
    data = {
        "channel": channel,
        "text": message
    }
    res = requests.post(url, headers=headers, data=data)
    return res

log_old = ""
while(True):
    # 設定値読み込み
    with open("/home/pi/work/mailbox_notifier/config.json", "r") as f:
        conf = json.loads(f.read())

    filename = conf["logdir"] + "/" + conf["sensor_name"] + "/" + conf["sensor_name"] + "_" + dt.datetime.now().strftime("%Y-%m-%d") + ".csv"
    if os.path.isfile(filename):
        with open(filename,"r") as f:
            # "2022/11/06 21:34:25,::rc=80000000:lq=15:ct=002B:ed=8xxxxxxxx:id=0:ba=3080:bt=0000"
            lines = f.readlines()[-1:][0][:-1]
            print(lines)
            # "bt=0001" or "bt=0000"
            data = lines.split(",")[1].split(":")[-1:][0]
            if log_old != lines:
                # メッセージ送信
                ret = send_line_message(conf["line_token"],"\n荷物が届きました")
                print(f"line notifier response:{ret}")
                log_old = lines

    # 単発動作 or インターバル動作
    if conf["interval"] != 0:
        time.sleep(conf["interval"])
    else:
        break
