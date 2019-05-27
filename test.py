import urllib.request
import urllib.parse
import configparser
import os
import socket, fcntl, struct
import sys
import psutil

conf_file_path = os.getcwd() + '\client_cfg.ini'

#configure
server_ip = ''
server_port = ''
get_ID_url = ''
report_url = ''
id = ''
iface = ''
frp_path = ''
report_period_second = ''
conf = configparser.ConfigParser()



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
    url = server_ip + ':' + server_port + get_ID_url + '/' + host_name
    id = do_post(url, post_data)
    return id

def get_ip(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', bytes(ifname[:15],'utf-8')))[20:24])

def get_host_name():
    return socket.getfqdn(socket.gethostname())

def get_frp():
    frp_path = os.getcwd()+'/../frp/frpc.ini'
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

def configure():
    global conf, server_ip, server_port, get_ID_url, report_url, id, iface, frp_path, report_period_second

    server_ip = input('服务器IP：')
    if server_ip == '':
        print("输入不正确！")
        return -1

    server_port = input('服务器端口号：')
    if server_port == '':
        print("输入不正确！")
        return -1

    iface = input('网卡名:(ifconfig)')
    if iface == '':
        print("输入不正确！")
        return -1

    frp_path = input('frpc.ini路径：（默认是../frp/frpc.ini）')
    if frp_path == '':
        print("使用默认路径！")
        frp_path = '../frp/frpc.ini'

    report_period_second = input('上报周期：（单位秒，默认是3）')
    if report_period_second == '':
        print("使用默认时间！")
        report_period_second = '3'

    #获取id
    host_name =  get_host_name()
    id = get_id(host_name)
    print('id=',id)

    conf.set('configure', 'first_run', 'false')
    conf.set('configure', 'server_ip', server_ip)
    conf.set('configure', 'server_port', server_port)
    conf.set('configure', 'iface', iface)
    conf.set('configure', 'frp_path', frp_path)
    conf.set('configure', 'report_period_second', report_period_second)



    print('配置成功')

    with open(conf_file_path,'w') as configfile:
        conf.write(configfile)

def read_conf_from_file():
    global conf, server_ip, server_port, get_ID_url, report_url, id, iface, frp_path, report_period_second
    # get configure from file
    config = conf['configure']

    server_ip = config['server_ip']
    server_port = config['server_port']
    get_ID_url = config['get_ID_url']
    report_url = config['report_url']
    id = config['id']
    iface = config['iface']
    frp_path = config['frp_path']
    report_period_second = config['report_period_second']

def report():
    global conf, server_ip, server_port, get_ID_url, report_url, id, iface, frp_path, report_period_second
    period = int(report_period_second)

    while(True):
        postdata = urllib.parse.urlencode({
            "id": id,
        }).encode('utf-8')

def main():
    global conf, server_ip, server_port, get_ID_url, report_url, id, iface, frp_path, report_period_second

    conf.read(conf_file_path)
    config = conf['configure']
    # print(conf.items('configure'))

    #检查是否是第一次运行
    first_run = config['first_run']
    if first_run == 'true':
        print('首次运行，请先配置！')
        configure()
        return 0
    elif len(sys.argv) > 0 and sys.argv[0] == '-c':
        configure()
        return 1

    read_conf_from_file()



if __name__ == '__main__':
    main()