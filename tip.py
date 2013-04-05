#!/usr/bin/env python
#-*- coding:utf-8 -*-
#by@taobao_ip_Library

import httplib2
import sys
import socket
import re


def net_addr():
    #域名解析
    try:
        return socket.getaddrinfo(_addr, None)
    except Exception:
        print '抱歉！地址解析失败。'
        sys.exit()

def St_dic(arg):
    #类型转换.字符串转字典
    return eval(arg)

def get_info(_net_addr):
    #主函数，获取ip信息
    url =  'http://ip.taobao.com/service/getIpInfo.php?ip=' + _net_addr
    Hc =  httplib2.Http('.cache')
    resp, content =  Hc.request(url, 'GET')

    def vul_info(vule):
        #对返回的IP信息作筛选
        return _ip_key['data'][vule]

    if resp['status'] == '200' or '302':
        if St_dic(content)['code'] == 0:
            conn =  content.decode('unicode_escape')
            #字符编码转换
            _ip_key =  St_dic(conn)
            print vul_info('country'),vul_info('region'),vul_info('city'),vul_info('isp'),vul_info('ip')
        else:
            print St_dic(content)['data']
    else:
        print '抱歉！服务不可用.',resp['status']

if __name__ == '__main__':

    try:
        scrpit, _addr =  sys.argv
    except ValueError:
        print '...\n......\n\n没有获取到IP地址  退出程序!!!\n........Done!'
        sys.exit()
        #接受输入的查询地址

    if re.search(r'^([1-2][0-5]?[0-4]?).*(\d)$', _addr):
        get_info(_addr)
        #输入为ip地址，直接GET taobao IP库信息(taobao会做IP合法性判断)
    else:
        if re.search(r'(\w+\.)?(\w+|\d+)\.(\D){2,3}$', _addr):
            get_info(net_addr()[0][4][0])
            #输入为域名，进行解析，在GET
        else:
            print '地址获取失败。'
            sys.exit()
