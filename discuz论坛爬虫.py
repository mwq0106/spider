# -*- coding: utf-8 -*-

import cookielib
from bs4 import BeautifulSoup
import requests
import sys
import os
import time
import multiprocessing
import PyV8

reload(sys)

sys.setdefaultencoding('utf-8')
session=requests.session()
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
           'Referer' : 'https://bbs.zhuankezhijia.com/forum-37-1.html'}
'''class PriorityQueue:

    #q.put(item, priority)
    #权值小的先出

    def __init__(self):
        self._queue = []
    def put(self, item, priority):
        heappush(self._queue, (priority, item))
    def get(self):
        return heappop(self._queue)[-1]
    def empty(self):
        return len(self._queue)==0
    def lenth(self):
        return len(self._queue)'''
def jsHandle(js):
    import PyV8
    ctxt = PyV8.JSContext()
    ctxt.enter()
    def insert(original, new, pos):
        '''Inserts new inside original at pos.'''
        return original[:pos] + new + original[pos:]
    s=js[31:]

    s=s[:(len(s)-9)]
    s='var location={};var window={};'+s
    pos = s.rfind('location')
    try:
        f = ctxt.eval(s)
        location = ctxt.eval('location')
        if (s[pos + 8] == '='):#location=...location直接就是跳转地址
            return location
        attri = location.keys()[0]#location.href=函数，或者location[href]=函数，跳转地址在参数中
        res = eval('location.' + attri)
        return res
    except:
        pos = s.find('(', pos)
        s = insert(s, '=', pos)#location[]();或者location.href();需要加=,跳转地址在参数中
        f = ctxt.eval(s)
        location = ctxt.eval('location')
        attri = location.keys()[0]
        res = eval('location.' + attri)
        return res
def getPageData(mission_page,p,write_data,session):
    #global session
    if(p==1):
        soup = BeautifulSoup(mission_page)
        mission_list = soup.find_all('tbody')
        i=0
        for s in mission_list:
            i += 1
            if 'checkForumnew_btn' in str(s):
                break
        i+=1
        for i in range(i,len(mission_list)):

            write_data.append('------------------------------------------------------------\r\n'.encode('gbk'))
            write_data.append(u'帖子链接：'.encode('gbk'))
            find_a=mission_list[i].find_all('a')
            find_span=mission_list[i].find_all('span')
            write_data.append(('https://bbs.zhuankezhijia.com/'+find_a[2].attrs['href']+'\r\n').encode('gbk'))
            page_url='https://bbs.zhuankezhijia.com/' + find_a[2].attrs['href']
            #time.sleep(2)
            page=session.get(page_url)
            print '-------------------------------'
            #print u'次session:', id(session)
            #print session.cookies.items()
            print u'帖子链接：'+page_url
            text=page.text#帖子内容
            if(text[0:31]=='<script type="text/javascript">'):
                jump=jsHandle(text.encode("utf-8"))
                page_url = 'https://bbs.zhuankezhijia.com/' +jump
                page = session.get(page_url)
                getContent(page.text)
            else:
                getContent(page.text)
            #print u'帖子链接：', 'https://bbs.zhuankezhijia.com/' + find_a[2].attrs['href']
            try:
                write_data.append((find_span[0].string+' '+find_span[1].string+'\r\n').encode('gbk'))
            except:
                write_data.append((u'特殊例子'+'\r\n').encode('gbk'))#帖子格式不正常
            try:
                write_data.append((find_a[2].string+'\r\n').encode('gbk','ignore'))#标题
            except:
                write_data.append(u'发生编码错误\r\n'.encode('gbk'))
                print find_a[2].string
                #file.write((find_a[2].string.replace(u'\xa0',' ')).encode('gbk'))
            for j in range(len(find_a)-1,len(find_a)-5,-1):
                if(j==len(find_a)-1):
                    write_data.append(u'最后回复时间：'.encode('gbk'))
                    write_data.append((find_a[j].string+'\r\n').encode('gbk'))
                if(j==len(find_a)-2):
                    write_data.append(u'最后回复人：'.encode('gbk'))
                    try:
                        write_data.append((find_a[j].string + '\r\n').encode('gbk'))
                    except:
                        write_data.append((u'请手动取提取用户名' + '\r\n').encode('gbk'))
                if(j==len(find_a)-3):
                    write_data.append(u'回复数量： '.encode('gbk'))
                    write_data.append((find_a[j].string + '\r\n').encode('gbk'))
                if(j==len(find_a)-4):
                    write_data.append(u'发帖人：'.encode('gbk'))
                    try:
                        write_data.append((find_a[j].string + '\r\n').encode('gbk'))
                    except:
                        write_data.append((u'请手动取提取用户名' + '\r\n').encode('gbk'))
    else:
        soup = BeautifulSoup(mission_page)
        mission_list = soup.find_all('tbody')
        for i in range(1, len(mission_list)):
            #print len(mission_list)-1
            write_data.append('------------------------------------------------------------\r\n'.encode('gbk'))
            write_data.append(u'帖子链接：'.encode('gbk'))
            find_a=mission_list[i].find_all('a')
            find_span=mission_list[i].find_all('span')
            #print u'帖子链接：', 'https://bbs.zhuankezhijia.com/' + find_a[2].attrs['href']
            page_url='https://bbs.zhuankezhijia.com/' + find_a[2].attrs['href']
            page=session.get(page_url)
            print '-------------------------------'
            print u'帖子链接：'+page_url
            text=page.text#帖子内容
            if(text[0:31]=='<script type="text/javascript">'):
                jump=jsHandle(text.encode("utf-8"))
                page_url = 'https://bbs.zhuankezhijia.com/' +jump
                page = session.get(page_url)
                getContent(page.text)
            else:
                getContent(text)
            write_data.append(('https://bbs.zhuankezhijia.com/' + find_a[2].attrs['href'] + '\r\n').encode('gbk'))
            try:
                write_data.append((find_span[0].string+' '+find_span[1].string+'\r\n').encode('gbk'))
            except:
                write_data.append((u'特殊例子' + '\r\n').encode('gbk'))
            try:
                write_data.append((find_a[2].string+'\r\n').encode('gbk','ignore'))#标题
            except:
                #file.write((find_a[2].string + '\r\n').encode('gbk','ignore'))
                write_data.append(u'发生编码错误\r\n'.encode('gbk'))
                print find_a[2].string
            for j in range(len(find_a)-1,len(find_a)-5,-1):
                if(j==len(find_a)-1):
                    write_data.append(u'最后回复时间：'.encode('gbk'))
                    write_data.append((find_a[j].string+'\r\n').encode('gbk'))
                elif(j==len(find_a)-2):
                    write_data.append(u'最后回复人：'.encode('gbk'))
                    try:
                        write_data.append((find_a[j].string + '\r\n').encode('gbk'))
                    except:
                        write_data.append((u'请手动取提取用户名'+'\r\n').encode('gbk'))
                elif(j==len(find_a)-3):
                    write_data.append(u'回复数量： '.encode('gbk'))
                    write_data.append((find_a[j].string + '\r\n').encode('gbk'))
                elif(j==len(find_a)-4):
                    write_data.append(u'发帖人：'.encode('gbk'))
                    try:
                        write_data.append((find_a[j].string + '\r\n').encode('gbk'))
                    except:
                        write_data.append((u'请手动取提取用户名' + '\r\n').encode('gbk'))
def login():
    mission_url='https://bbs.zhuankezhijia.com/forum-49-1.html'
    load_cookiejar = cookielib.LWPCookieJar()#实例化一个LWPCookieJar对象
    load_cookiejar.load('zhuanjia_cookie.txt', ignore_discard=True, ignore_expires=True)#从文件中加载cookies(LWP格式)
    load_cookies = requests.utils.dict_from_cookiejar(load_cookiejar)#工具方法转换成字典
    session.cookies = requests.utils.cookiejar_from_dict(load_cookies)#工具方法将字典转换成RequestsCookieJar，赋值给session的cookies.
    mission_page=session.get(mission_url,headers=headers)
    if mission_page.text.find(u'请注册')!=-1:
        print u'登陆失败'
        return False
    else:
        print u'登陆成功'
        return True
def init(se,_n):
    global session,n
    n=_n
    session=se
    session.cookies=se.cookies
def getData(url,i):
    write_data=[]
    global session,n
    #print id(session_lock),id(session)
    '''if session_lock.acquire():
        session1=session
        session1.cookies=session.cookies
        session_lock.release()'''
    mission_page = session.get(url)
    #print mission_page.text#帖子列表
    #print u'主session:',id(session)
    getPageData(mission_page.text,i,write_data,session)
    #print write_data
    #write_data(write_data)
    write_data.append(i)
    print n
    return write_data
def stepSaveData(datalist):
    global write_alltime
    i = datalist[len(datalist) - 1]
    write_start_time = time.time()
    with open(os.getcwd()+"\\zhuanjia\\"+str(i)+'.txt','w') as step_file:
        datalist.pop()
        for s in datalist:
            step_file.write(s)
        step_file.close()
    write_finishi_time=time.time()
    write_alltime+=(write_finishi_time-write_start_time)

def fileTogether(path):
    global write_alltime
    write_start_time = time.time()
    list = os.listdir(path)
    list.sort(key= lambda x:int(x[:-4]))
    with open(os.getcwd()+'\\'+'zhuanjia.txt','w') as f:
        for i in list:
            with open(path+'\\'+i,'r') as partfile:
                text=partfile.read()
                f.write(text)
                partfile.close()
        f.close()
    write_finishi_time = time.time()
    write_alltime += (write_finishi_time - write_start_time)
'''def writeData(q):
    global f,write_alltime
    #print id(f),id(file_lock)
    write_start_time=time.time()
    while not q.empty():
        data_list=q.get()
        for s in data_list:
            f.write(s)
    #if file_lock.acquire():
     #   for s in datalist:
      #      f.write(s)
       # file_lock.release()
    #print len(datalist)
    write_finishi_time=time.time()
    write_alltime+=(write_finishi_time-write_start_time)'''
def getContent(page):
    global n
    n+=1
    soup = BeautifulSoup(page,"html.parser")
    content_list=soup.find_all('table')
    #print content_list
    div_list=content_list[7]
    for d in div_list:
        #print d.get_text().split('\n').remove(u'')
        slist=d.get_text().split('\n')
        while u'' in slist:
            slist.remove(u'')
        a='\n'.join(slist)
        a=a.strip()
        print a
    img_list=content_list[7].find_all('ignore_js_op')
    for img in img_list:
        b='https://bbs.zhuankezhijia.com/'+img.find_all('a')[0].attrs['href']
        print b
    #print img_list
    #print n
if __name__=='__main__':
    if login()==True:
        statr_time=time.time()
        write_alltime=0
        #f = open('zhuanjia.txt', 'w')
        #q = PriorityQueue()
        write_data=[]
        #lock = multiprocessing.Lock()
        n=0
        page_pool = multiprocessing.Pool(processes=20, initializer=init, initargs=(session,n))#, initializer=init, initargs=(session_lock,session)
        #test_url='https://bbs.zhuankezhijia.com/forum-49-1.html'
        #html=session.get(test_url,headers=headers)
        #print html.text
        #getData(test_url,1)
        for i in range(1,101):
            print i
            mission_url = 'https://bbs.zhuankezhijia.com/forum-49-'+str(i)+'.html'
            page_pool.apply_async(getData, (mission_url,i),callback=stepSaveData)
        page_pool.close()
        page_pool.join()
        fileTogether('E:\Pythonfile\zhuanjia')
        finish_time=time.time()
        print u'总时间：',finish_time-statr_time
        print u'写入文件时间：',write_alltime
        print u'访问时间：',(finish_time-statr_time)-write_alltime


