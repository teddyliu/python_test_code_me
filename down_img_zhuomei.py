#-*- coding: utf-8 -*-

"""基于版块URL抓图片，脚本仅限于学习，交流
脚本所抓图片版权为卓美摄影公社所有，请勿用于商业.谢谢！！！"""

import urllib
import httplib2
import re, sys
import logging

LOG =  logging.getLogger('Downimg')
logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        datefmt='%m-%d %H:%M',
        filename='debug.log',
        filemode='a+'
        )


zm7_home_url =  'http://bbs.zm7.cn/'
#桌美BBS URL
forum_url =  'http://bbs.zm7.cn/forum-27-1.html'
#板块URL，测试URL为卓美摄影公社，人文纪实板块，修改该URL可抓取相对应的板块图片

imgbbs_pat =  r'http://imgbbs.zm7.cn/\w{1,10}/\w{1,10}/\w{1,10}/\d{6}/\d{2}/\w{22}.jpg'
#re 匹配img URL

def content(url, pat):
    ''' 页面过滤函数(抓取指定的数据)'''
    Hc =  httplib2.Http('.cache')
    resp, con =  Hc.request(url, 'GET')
    content =  list(set(re.findall(pat, con)))
    return content

def loop_page():
    try:
        count_page_num =  int(''.join(content(forum_url, r'<span title.*共 (\d{1,4}) 页.*>.*</span>')))
        #统计该板块页面数量
        forum_url_count =  int(''.join(re.findall(r'.*-(\d{1,4}).html', forum_url)))
        #基于URL查看版块中当前的页数
    except RequestError:
        print '没有抓取到数据!'
        sys.exit()
        
    loop_url_list =  []

    for i in [str(x) for x in range(1,count_page_num + 1)]:
        loop_url_num =  re.sub('1', i, forum_url)
        loop_url_list.append(loop_url_num)
    return loop_url_list
    ##拆分板块，生成页URL

if __name__ == '__main__':
    thread_a_pat =  r'href="(thread-\d{2,7}-\d+-\d+.html)"'
    thread_b_pat =  r'href="(forum.php?.*tid=\d+)"'

    import types

    def Down_img(img):
        img_name =  re.split(r'/', img)[-1]
        urllib.urlretrieve(img, img_name)
        print 'down', img_name , 'Done!'
        ##下载图片
        LOG.info(img)
        return

    for i in loop_page():
        Theme_url = content(i, thread_a_pat) + content(i, thread_b_pat)
        #生成主题链接

        for x in Theme_url:
            i_url =  zm7_home_url + x
            img_url_a_b =  content(i_url, imgbbs_pat)
            #生成图片链接

            for y in img_url_a_b:
                Down_img(y)
    print 'Done'
    sys.exit()
