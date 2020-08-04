#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/8/3 22:40 
# @Author : QX
# @use : 
# @File : drew_coupon.py.py
# @Software: PyCharm
from datetime import datetime
import time, os
import requests
import concurrent.futures
from loguru import logger
from pusher import qywx_pusher


start_time = '23:00:30'

start_time = time.strftime('%Y-%m-%d', time.localtime(time.time())) + " " + start_time

#提前时间，ms
before_time = 120

#请求间隔时间
step_time = 10

activity_code = "crypt-602bfe2a7bea92d36fec4f64b1b60515f11f3a77035cc0d2fe62d584a83f4d4681c9b0bfd2cb003a0a70318d193bb8d8"

def log(msg):
    now = datetime.now()
    logger.debug(msg)
    msg = f"{now} {msg}"
    #print(msg)
    #R.lpush("xmsc_log", msg)
    
class Task():
    def __init__(self):
        self.all_cookie = {}
        self.file_path = os.path.join(os.getcwd(), 'cookie.txt')
        self.read_cookie()
        log(f"cookie数量:{len(self.all_cookie)},设定时间:{start_time},延迟:{before_time}ms,请求间隔:{step_time}ms")

    def read_cookie(self):
        with open(self.file_path, 'rb') as f:
            lines = f.readlines()
            if not lines:
                return f'文本内容为空或有误.'
            for line in lines:
                try:
                    line = line.decode('gbk').strip('\n').strip('\r')
                    line = line.split('----')
                    if len(line) != 2:
                        continue
                    self.all_cookie[line[0]] = line[1].split(';')[0]
                except Exception as e:
                    print(e)

    def start(self):
        print(len(self.all_cookie), enumerate(list(self.all_cookie.values())))
        with concurrent.futures.ThreadPoolExecutor(len(self.all_cookie)) as executor:
            executor.map(self.drew_coupon, enumerate(list(self.all_cookie.values())))

    def drew_coupon(self, cookies):
        index, cookie = cookies
        time.sleep(index * step_time / 1000)
        print(index, int(time.time()*1000), get_mi_time())
        name = list(self.all_cookie.keys())[index]
        url = "http://api.m.mi.com/v1/activity/prize_draw_lucky"
        payload = f"component=lucky_coupon_time&activity_code={activity_code}&"
        headers = {
           'Cookie': cookie,
           'Mishop-Client-Id': '180100031052',
           'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        log(f'用户名:{name},返回:{response.text}.')
        if "抢到啦" in response.text:
           qywx_pusher(f'用户名:{name},返回:{response.text}.')


def strtime_int(time_sj):
    data_sj = time.strptime(time_sj, "%Y-%m-%d %H:%M:%S")
    time_int = int(time.mktime(data_sj)*1000)
    return time_int

def get_sys_time():
    return int(time.time()*1000)

# def run():
#     print(f"运行时间:{get_sys_time()}")

def get_mi_time():
    last_time = ""
    session = requests.session()
    while True:
        url = "http://tp.hd.mi.com/gettimestamp"
        payload = {}
        headers = {}
        #time1 = get_time()
        response = session.get(url, headers=headers, data=payload)
        #print(get_time() - time1, response.text)
        if last_time == "":
            last_time = response.text
        if last_time != "" and last_time != response.text:
            last_time = response.text
            last_time =int(last_time[15:])*1000
            return last_time


def get_tb_time():
    pass

if __name__ == '__main__':
    new_start_time = strtime_int(start_time)
    first_run_time = get_sys_time()
    task = Task()
    while True:
        now_time = get_sys_time()
        if now_time + before_time > new_start_time - 2000:
            now_time = get_mi_time()
            break
    #if now_time + before_time > new_start_time - 2000:
    sleep_time = (new_start_time - now_time - before_time)/1000
    time.sleep(sleep_time)
    task.start()