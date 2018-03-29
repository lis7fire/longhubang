#!/usr/bin/python3
# coding: utf-8
# 上面两句注释必须要，防止无法打印中文的

import datetime
import os
import re
from pyquery import PyQuery as pq
import pymysql.cursors
import requests
import algorithm
import json
import traceback
# import urllib,urllib2,re,json
# 来源url：https://pan.baidu.com/disk/home?#list/vmode=list&path=/极客学院-视频2016/极客学院(知识体系图 实战路径图)/知识体系图

'''
COOKIE中变动的字段：
BDCLND=91Mz4PuAQqrrr%%3D;
MCITY=-%3A; 
Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0=1514801279,1514801523,1514807401,1514811465;
PANPSC=298461236142715097%3Acvzr9Jxhf5DlI0a0yYJfmCOAoXNFwReXsg0gWUDJHkjXG9GmBZpeFcD%2BGm5EjO5jLPY%2BF1C2z9fxTJ3v1z1m%2BnR1lPHAQEb1l29mtrQhjoN%2BSJWX9%2F9F%2FCC9yOinRwwiKg6bXhEDmDblx9uR5zc7VkTo8K6GUSXPWZS%2FCparmSwCDm3pOf6hqyxKPKTDDqOPAg5t6Tn%2BoatGYDbXt8Y3lw%3D%3D;
'''
errno=''
VERSION = "1.0.1"
HEAD_COOKIE_BDCLND='=;'
HEAD_COOKIE_MCITY='-131:;'
HEAD_COOKIE_Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0='1514385494,1514386300,1514647712,1514647867;'
HEAD_COOKIE_PANPSC='13679979192454137669:+dKu8WyLCLL4eXStNSa0XHHC63U2dDStAqhcX9Lqc6TJ9cb0aYFml4VWVlWJGg7qeZ9c6xaO4oLgT0Imr6lK+/C+JWDNkK4hUt7m6T14kJ2T2NtiaXV6jA2rsgnNL+LYct9tn9thbnTpv7IiW4JizVaiS3u8yDNz5M='

HEAD_COOKIE_STATIC = "\
yundetect_httpport=10001;\
"
HEAD_COOKIE=HEAD_COOKIE_STATIC+HEAD_COOKIE_BDCLND+HEAD_COOKIE_MCITY+HEAD_COOKIE_Hm_lvt_7a3960b6f067eb0085b7f96ff5e660b0+HEAD_COOKIE_PANPSC
HEAD_ACCEPT = "application/json, text/javascript, */*; q=0.01"
HEAD_ACCEPT_ENCODING = "gzip, deflate, sdch, br"
HEAD_ACCEPT_LANGUAGE = "zh-CN,zh;q=0.8"
HEAD_CONNECTION = "keep-alive"
HEAD_HOST = "pan.baidu.com"
HEAD_REFERER = "https://pan.baidu.com/disk/home?"
HEAD_USER_AGENT = "Mozilla/5.0 (iPad; CPU OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1 "
HEAD_X_Requested_With = "XMLHttpRequest"

req_head = {'Accept': HEAD_ACCEPT, 'Accept-Encoding': HEAD_ACCEPT_ENCODING, 'Accept-Language': HEAD_ACCEPT_LANGUAGE,
            'Cookie': HEAD_COOKIE, 'Host': HEAD_HOST,
            'Referer': HEAD_REFERER, 'User-Agent': HEAD_USER_AGENT, 'X-Requested-With': HEAD_X_Requested_With
            }
'''
==:%3D%3D
[:%5B
]:%5D
'''
down_link_static_PARS2 = '''\
&type=dlink\
&ct=pcygj\
&cv=5.6.3.4\
&channel=chunlei\
&web=1\
&app_id=250528\
&bdstoken=1ed63c7f24fd368f96f7073bd49b89ab\
&clienttype=0\
'''
def initlink(sign3,sign1,timestamp,fidlist):
    global down_link_static_PARS2
    sign = algorithm.base64_baidu(algorithm.sign2(sign3,sign1))
    sign=sign.replace('/','%2F')
    sign=sign.replace('+','%2B')
    sign=sign.replace('=','%3D')
    fidlist = '%5B'+fidlist+'%5D'
    logid = '==' 
    down_link_pars1 = 'sign=' + sign + '&timestamp=' + timestamp + '&fidlist=' + fidlist + '&logid=' + logid
    # print(down_link_pars1) #下载的文件名：02、Cocos2d-x游戏开发.rar
    link = 'https://pan.baidu.com/api/download?' +  down_link_pars1 + down_link_static_PARS2
    return link
    pass

def zhengze( home_html,debug=False):
    if debug:
        home_html='"sign1":"3fce7b5a87d8238bc7619ea3f592b5695dde7e3c","sign2": "q=0;o};",    "sign3":"d76e889b6aafd3087ac3bd56f4d4053a","timestamp":1515054506," '
        pass 
    print(home_html)
    sign1 = re.search(r'(?<=sign1":").+?(?=",)', home_html).group()
    sign3 = re.search(r'(?<=sign3":").+?(?=",)', home_html).group()
    timestamp = re.search(r'(?<=timestamp":).+?(?=,")', home_html).group()
    print(sign1)
    print(sign3)
    print(timestamp)
    return sign3,sign1,timestamp
    pass

'''sign===&timestamp=1515054506'''

# print(req_head)
print('--------------------')
# print("请求头: ", r.request.headers)
# print("响应头: ", r.headers)
print('--------------------')

filein = open('./jieguo.txt', 'w')
print('开始读取in文件：')
filein.write('aaa')
filein.close()

def init_errno():
    global errno
    with open('./canshu.json','r',encoding='utf-8') as jsfile:
        errno=json.load(jsfile)
    # print(type(errno))

def final_url(js):
    print('-------')
    init_errno()
    if js["errno"]==0:
        print('获取成功！文件 {} 的下载链接是：\n {}'.format('916188959762109',js['dlink'][0]['dlink']),)
        pass
    else:
        print('请求id为：{},失败编号：{},错误类型：{} '.format(js['request_id'],js['errno'],errno[str(js['errno'])]))

def home_page(is_connect_web=True):
    if not is_connect_web:
        home_res=('d76e889b6aafd3087ac3bd56f4d4053a','3fce7b5a87d8238bc7619ea3f592b5695dde7e3c','1515054506')
        print('home_page的调试模式！！！')
        return home_res
        pass
    link='https://pan.baidu.com/disk/home?'
    global req_head
    respon_text=requests.get(link, headers=req_head).text
    home_res=zhengze(respon_text)
    print('home_page的联网模式：',home_res)
    return home_res
    pass

def download_page(home_res,is_connect_web=True):
    if not is_connect_web:
        r_json='{"errno":0,"request_id":84267772485035342,"dlink":[{"fs_id":"916188959762109","dlink":"https:\/\/d.pcs.baidu.com\/file\/6b4f39cc4a791ed4700c171a6977cf4a?fid=2433224667-250528-916188959762109&time=1515049922&rt=pr&sign=FDTAERVC-DCb740ccc5511e5e8fedcff06b081203-nTg1faUlM6qrNwYzneQPSZopDR8%3D&expires=8h&chkv=1&chkbd=1&chkpc=&dp-logid=84267772485035342&dp-callid=0&r=794357218"}]}'
        # r_json='{"errno":-6,"request_id":84159854721116628}' 
        return json.loads(r_json) 
        pass
    sig = initlink(home_res[0], home_res[1],home_res[2],"916188959762109")
    print('download_page函数联网模式，Download页面的Link：\n',sig)
    global req_head
    r_json=requests.get(sig,headers=req_head).text
    js=json.loads(r_json)
    return js
tmp_dirs={}
cur_path,father_path,up_path='/','/','/' # 当前目录，父目录，上次操作的目录
def list_page(dir='/'):
    global cur_path,father_path,up_path,tmp_dirs
    link='https://pan.baidu.com/api/list?dir={}&bdstoken=&logid=&num=100&order=name&desc=0&clienttype=0&showempty=0&web=1&page=1&channel=chunlei&web=1&app_id=250528'.format(dir)
    print('链接为：',link)
    r=requests.get(link,headers=req_head)
    filelist=json.loads(r.text)
    # print(filelist)
    if filelist['errno'] ==0:
        tmp_paths=dir.split('/')
        if dir =='/' or len(tmp_paths)==2:
            father_path='/'
            print('当前目录是根目录!!! ')
        else:
            father_path=dir.rstrip(dir.split('/')[-1])
            father_path=father_path.rstrip('/')
        up_path=cur_path
        cur_path=dir
        tmp_dirs={}
        i=1
        print('当前目录：{} ，上一层目录：{} , 上次操作目录：{}'.format(cur_path,father_path,up_path))
        for x in filelist['list']:
            print('{} : {}'.format(i,x['path']))
            tmp_dirs[i]=x['path']
            i+=1
            pass
    else:
        print('请求id为：{},失败编号：{},错误类型：{} '.format(filelist['request_id'],filelist['errno'],errno[str(filelist['errno'])]))
        pass
    
def main():
    print('主函数：')
    home_res=home_page(is_connect_web=False)
    js=download_page(home_res,is_connect_web=False)
    final_url(js)
    list_page()

    global father_path,tmp_dirs
    while True:
        user_in=input('请输入编号：')
        if user_in == '..' :
            list_page(father_path)  
        else:      
            try:
                user_in=int(user_in)
            except Exception as e: 
                print('必须输入一个数字！！！现在退出程序！')   
                traceback.print_exc()
                return
            else:
                print(tmp_dirs)
                list_page(tmp_dirs[user_in]) 

        
if __name__ == '__main__':
    main()
