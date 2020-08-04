#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2020/8/4 21:32 
# @Author : QX
# @use : 
# @File : get_activity_code.py 
# @Software: PyCharm

import requests, json, time
import urllib3
urllib3.disable_warnings()

def get_activity_code(version):
    url = "https://api.m.mi.com/v1/home/activity_page"
    payload = f"phone_type=&phone_name=&forceVersion=&version={version}&bigGallery=true&"
    headers = {
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False).text
    #print(response)
    if 'coupon' not in response:
        return
    sections = json.loads(response)['data']['sections']
    for section in sections:
        if section['view_type'] == 'lucky_coupon_time':
            items = section['body']['items']
            for item in items:
                #print(item)
                start_time = item['start_time']
                start_time_tmp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(start_time)))
                name = item.get('name', section['view_type'])
                activity_code = item['activity_code']
                print(name, start_time_tmp, activity_code)

if __name__ == '__main__':
    get_activity_code(16426)