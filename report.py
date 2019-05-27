# -*- coding: utf-8 -*
import urllib.request
import urllib.parse
import os
import socket, fcntl, struct
import sys
import psutil
import cfg


def do_post(url, post_data):
    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "utf-8",
        "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Host": "c.highpin.cn",
        "Referer": "http://c.highpin.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
    }
    request = urllib.request.Request(url, post_data, header)
    html = urllib.request.urlopen(request).read().decode('utf-8')
    return html


def get_id(host_name):
    post_data = urllib.parse.urlencode({
        "hostName": host_name
    }).encode('utf-8')
    url = cfg.server_ip + ':' + cfg.server_port + cfg.get_ID_url + '/' + host_name
    id = do_post(url, post_data)
    return id

def get_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15],'utf-8')))[20:24])

def get_host_name():
    return socket.getfqdn(socket.gethostname())

def get_frp():
    frp_path = os.getcwd()+'/'+'../frp/frpc.ini'
    if os.path.exists(frp_path) :
        frp_conf_file = open(frp_path, mode='r')
        frp_conf_string = frp_conf_file.read()
        frp_conf_file.close()
    else:
        frp_conf_string = '未配置'
    return frp_conf_string

def get_temperature():
    res = str(psutil.sensors_temperatures())
    a = res.find('current')
    a = res.find('=',a)+1
    b = res.find(',',a)
    temp = res[a:b]
    return temp

def main():

    print('report alive...')

    host_name = get_host_name()
    id = get_id(host_name)
    ip = get_ip('')
    frp_conf_file = open(frp_conf_file_path, mode='r')
    frp_conf_string = frp_conf_file.read()
    frp_conf_file.close()

    postdata = urllib.parse.urlencode({
        "id": id,
        "descrb": descrb,
        "ip": ip,
        "frp_config": frp_conf_string,
        "others": others
    }).encode('utf-8')

    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "utf-8",
        "Accept-Language": "zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
        "Connection": "keep-alive",
        "Host": "c.highpin.cn",
        "Referer": "http://c.highpin.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
    }

    request = urllib.request.Request(url, postdata, header)
    html = urllib.request.urlopen(request).read().decode('utf-8')


if __name__ == '__main__':
    main()

