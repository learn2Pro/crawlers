#!/usr/bin/env python3
# -*- coding:utf8 -*-

import urllib.request
from urllib.parse import quote
import json
import time
import socket
import datetime
import threading
import sys

socket.setdefaulttimeout(60)
# global map_rst_list
map_rst_list = []


def request_contect(user_log_acct, address, publickey):
    address = ''.join(address.split())
    province = "-"
    city = "-"
    district = "-"
    address_map = "-"
    address_title = "-"
    address_type = "-"
    address_lat = "-"
    address_lng = "-"
    request_rst_flag = "-"
    request_info = "-"
    conrst = "-"
    global map_rst_list
    try:
        url = 'http://apis.map.qq.com/ws/geocoder/v1/?address=' + quote(address) + '&key=' + publickey
        response = urllib.request.urlopen(url)
        bj = json.loads(response.read().decode("UTF-8"))
    except socket.timeout as e:
        # print("-----socket timout:" , user_log_acct + '\t' + address)
        time.sleep(1)
        response = urllib.request.urlopen(url)
        bj = json.loads(response.read().decode("UTF-8"))
    except Exception as e:
        # print("other e" , user_log_acct + '\t' + address) ;
        time.sleep(1)
        response = urllib.request.urlopen(url)
        bj = json.loads(response.read().decode("UTF-8"))

    stat = bj['status']
    if (stat != 0):
        request_rst_flag = '1#address_error'
    if (stat == 0):
        lng = str(bj['result']['location']['lng'])
        lat = str(bj['result']['location']['lat'])
        rurl = 'http://apis.map.qq.com/ws/geocoder/v1/?location=' + lat + ',' + lng + '&poi_options=radius=2000;page_size=20;category=' + quote(
            '房产小区,购物,超市,教育学校,医院,旅游,机构团体,政府机关') + '&key=' + publickey + '&get_poi=1'
        try:
            rresponse = urllib.request.urlopen(rurl)
            rbj = json.loads(rresponse.read().decode("UTF-8"))
        except socket.timeout as e:
            time.sleep(1)
            rresponse = urllib.request.urlopen(rurl)
            rbj = json.loads(rresponse.read().decode("UTF-8"))
        except Exception as e:
            time.sleep(1)
            rresponse = urllib.request.urlopen(rurl)
            rbj = json.loads(rresponse.read().decode("UTF-8"))
        if (('result' not in rbj.keys()) or ('ad_info' not in rbj['result'].keys()) or (
            'province' not in rbj['result']['ad_info'].keys())):
            request_rst_flag = '2#request_address_error,no province'
        else:
            province = rbj['result']['ad_info']['province']
            city = rbj['result']['ad_info']['city']
            district = rbj['result']['ad_info']['district']
            if ('poi_count' in rbj['result'].keys()):
                poi_count = rbj['result']["poi_count"]
                if (poi_count == 0):
                    address_map = rbj['result']["address"]
                    address_title = rbj['result']["formatted_addresses"]["recommend"]
                    address_type = "其他"
                    address_lat = str(rbj['result']["location"]["lat"])
                    address_lng = str(rbj['result']["location"]["lng"])
                    request_rst_flag = '0#no pois'
                else:
                    request_info = rbj['result']
                    # request_info=""
                    address_map = rbj['result']['pois'][0]['address']
                    address_title = rbj['result']['pois'][0]['title']
                    address_type = rbj['result']['pois'][0]['category']
                    address_lat = str(rbj['result']['pois'][0]['location']['lat'])
                    address_lng = str(rbj['result']['pois'][0]['location']['lng'])
                    request_rst_flag = '0#normal'
    conrst = user_log_acct + '\t' + address + '\t' + province + '\t' + city + '\t' + district + '\t' + \
             address_map + '\t' + address_title + '\t' + address_type + '\t' + address_lat + '\t' + \
             address_lng + '\t' + str(request_info) + '\t' + request_rst_flag + '\n'
    map_rst_list.append(conrst)


def read_request_url(rfile, publickey, wf):
    rf = open(rfile, 'r', encoding="UTF-8");
    fileline = 0
    user_pin_list = []
    user_addr_list = []
    thread_ap_list = []
    global map_rst_list
    for strline in rf.readlines():
        fileline = fileline + 1
        arrlist = strline.split('\t')
        user_log_acct = arrlist[0].strip().lower()
        address = arrlist[1].strip()
        if (len(address) == 0 or address == 'NULL'):
            continue;
        if (len(user_log_acct) > 0 and len(address) > 0):
            user_pin_list.append(user_log_acct)
            user_addr_list.append(address)
            if (fileline % 250 == 0):
                start = time.clock()
                action_th = threading.Thread
                for i in range(len(user_pin_list)):
                    th = action_th(target=request_contect, name=user_pin_list[i],
                                   args=(user_pin_list[i]
                                         , user_addr_list[i]
                                         , publickey))
                    thread_ap_list.append(th)
                for j in range(len(user_pin_list)):
                    thread_ap_list[j].start()
                for f in range(len(user_pin_list)):
                    thread_ap_list[f].join(30)
                end = time.clock()
                if (fileline % 1000 == 0):
                    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(time_now, 'filelineis' + str(fileline));
                wf.writelines(map_rst_list)
                wf.flush()
                map_rst_list = []
                user_pin_list = []
                user_addr_list = []
                thread_ap_list = []
                if ((end - start) < 0.6):
                    # print(end,start)
                    time.sleep(0.6 - (end - start))
    time_now_tail = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(time_now_tail, 'filelineis' + str(fileline));
    thread_ap_list = []
    for i in range(len(user_pin_list)):
        th = threading.Thread(target=request_contect,
                              args=(user_pin_list[i]
                                    , user_addr_list[i]
                                    , publickey))
        thread_ap_list.append(th)
    for j in range(len(user_pin_list)):
        thread_ap_list[j].start()
    for f in range(len(user_pin_list)):
        thread_ap_list[f].join()
    wf.writelines(map_rst_list)
    wf.flush()


if __name__ == '__main__':
    rfile_name = str(sys.argv[1])
    wfile_name = str(sys.argv[2])
    # wfile_name="/data0/bavol/lbs/tmp_data/a.data"
    publickey = 'VYIBZ-'  # 需要补充
    # print("python3 ",rfile_name,wfile_name)
    wf = open(wfile_name, 'w+', encoding="UTF-8")
    read_request_url(rfile_name, publickey, wf)
    wf.close()
