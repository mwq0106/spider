# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import requests
import random
import os
from selenium.webdriver.common.action_chains import ActionChains
import httplib
import sys
import getpass
reload(sys)
sys.setdefaultencoding('utf8')

class taobao_mgj_spider():
    def __init__(self):
        self.session=requests.session()
        self.img_index=0
        self.test=False
        try:
            self.current_time=self.get_webservertimeINT()
        except:
            self.current_time=''
        pass
    def random_int(self,randomlength):
        #0.2377978178969109
        str = ''
        chars = '0123456789'
        length = len(chars) - 1
        random1 = random.Random()
        for i in range(randomlength):
            str += chars[random1.randint(0, length)]
        return str
    def random_str(self,randomlength):
        str = ''
        chars = 'abcdefghijklmnopqrstuvwxyz'
        #chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        rand = random.Random()
        for i in range(randomlength):
            str += chars[rand.randint(0, length)]
        return str
    def get_webservertime(self,host='www.baidu.com'):
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("GET", "/")
            r = conn.getresponse()
            # r.getheaders() #获取所有的http头
            ts = r.getheader('date')  # 获取http头date部分
            #print '============================'
            #print ts
            #print '============================'
            # 将GMT时间转换成北京时间
            ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
            # print(ltime)
            ttime = time.localtime(time.mktime(ltime) + 8 * 60 * 60)
            # print(ttime)
            dat = "date %u-%02u-%02u" % (ttime.tm_year, ttime.tm_mon, ttime.tm_mday)
            tm = "time %02u:%02u:%02u" % (ttime.tm_hour, ttime.tm_min, ttime.tm_sec)
            currenttime = "%u_%02u_%02u_%02u_%02u_%02u" % (
            ttime.tm_year, ttime.tm_mon, ttime.tm_mday, ttime.tm_hour, ttime.tm_min, ttime.tm_sec)
            #print currenttime
            #print (dat, tm)
            return currenttime
        except:
            return ''
    def get_webservertimeINT(self,host='www.baidu.com'):
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("GET", "/")
            r = conn.getresponse()
            # r.getheaders() #获取所有的http头
            ts = r.getheader('date')  # 获取http头date部分
            #print '============================'
            #print ts
            #print '============================'
            # 将GMT时间转换成北京时间
            ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
            # print(ltime)
            ttime = time.localtime(time.mktime(ltime) + 8 * 60 * 60)
            # print(ttime)
            dat = "date %u-%02u-%02u" % (ttime.tm_year, ttime.tm_mon, ttime.tm_mday)
            tm = "time %02u:%02u:%02u" % (ttime.tm_hour, ttime.tm_min, ttime.tm_sec)
            currenttime = "%u%02u%02u" % (
            ttime.tm_year, ttime.tm_mon, ttime.tm_mday)
            #print currenttime
            #print (dat, tm)
            return currenttime
        except:
            return ''
    def getTaobao(self,url):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            '--user-data-dir=C:\Users\\' + getpass.getuser() + '\AppData\Local\Google\Chrome\User Data')
        driver = webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=chrome_options)
        #driver = webdriver.PhantomJS(executable_path='phantomjs.exe',desired_capabilities=dcap)
        #driver.set_page_load_timeout(60)
        #driver.maximize_window()
        try:
            driver.get('https://login.taobao.com/member/login.jhtml')
            print u'登录完成之后按回车'
            raw_input()
        except:
            print u'页面访问失败'
            #driver.quit()
            pass
            return
        try:
            driver.get(url)
            WebDriverWait(driver, 60, 2).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'J_ReviewsCount')))
        except:
            driver.execute_script('if (window.stop) window.stop();else document.execCommand("Stop");')
            try:
                driver.find_elements_by_class_name('J_ReviewsCount')[0]
            except:
                print u'访问链接超时，请重启运行'
                #driver.quit()
                return
        try:
            print u'已经进入页面'
            js = "document.getElementsByClassName('J_ReviewsCount')[0].click()"
            driver.execute_script(js)
            #driver.find_elements_by_class_name('J_ReviewsCount')[0].click()

            WebDriverWait(driver, 60, 2).until(
                ec.presence_of_element_located((By.XPATH, '//*[@class="J_KgRate_ReviewContent tb-tbcr-content "]')))
            time.sleep(5)
        except Exception,e:

            print u'加载评论超时'
            #driver.quit()
            return
        dir_name=self.get_webservertime()
        if(os.path.exists(dir_name)):
            print u'文件夹已经存在'
            return
        os.makedirs(dir_name+'/img')
        f = open('./' + dir_name + '/' + u'评论.txt', 'w')
        f.close()
        f = open('./' + dir_name + '/' + u'图片链接.txt', 'w')
        f.close()
        #soup = BeautifulSoup(driver.page_source, "lxml")
        #print len(soup.find_all("li", class_="item")),soup.find_all("li", class_="item")
        #driver.save_screenshot('aa.png')
        n=1
        while(True):
            print n
            soup = BeautifulSoup(driver.page_source, "lxml")
            item_list=soup.find_all('li',class_='J_KgRate_ReviewItem kg-rate-ct-review-item')
            text=''
            img_text=''
            for item in item_list:
                comment_list=item.find_all('div',class_="J_KgRate_ReviewContent tb-tbcr-content ")

                comment_text=''
                for comment in comment_list:
                    try:
                        tmp_text=comment.string.strip()
                        if(tmp_text==''):
                            print u'没有评论'
                        else:
                            comment_text+=tmp_text+'\n'
                            print tmp_text
                    except:
                        tmp_list=comment.getText().split()

                        while '' in tmp_list:
                            tmp_list.remove('')
                        tmp_text=''
                        for tmp in tmp_list:
                            tmp_text+=tmp
                        comment_text += tmp_text + '\n'
                        print tmp_text


                text+=comment_text+'-----------------------------------------------------'+'\n'
                img_list=item.find_all("img")
                for img in img_list:
                    try:
                        img_url=img.attrs['src']
                        #print img_url
                        if(not img_url=='about:blank' and not img_url=='' and '40x40' in img_url):
                            img_url=img_url.split('jpg')
                            #print img_url
                            a_list=img_url[0].split('/')#为了获取图片名进行切割
                            filename=a_list[len(a_list)-1]
                            img_url='https:'+img_url[0]+'jpg'
                            print img_url
                            if(self.test==False):
                                response = self.session.get(img_url)
                                self.img_index+=1
                                with open('./'+dir_name+'/img/'+str(self.img_index)+'.jpg', 'wb') as f:
                                    f.write(response.content)
                                    f.close()
                            else:
                                img_text+=img_url+'\n'
                    except Exception,e:
                        print Exception,e
                        print u'图片下载失败'
                        pass
            if(self.test==True):
                f = open('./' + dir_name + '/' + u'图片链接.txt', 'a')
                f.write(img_text)
                f.close()
            f = open('./' + dir_name  +'/' +u'评论.txt', 'a')
            f.write(text.encode('gbk','ignore'))
            f.close()
            try:

                element=driver.find_element_by_xpath('//*[@class="kg-pagination2 thm-1 align-r"]/ul/li[last()]')

                #print element.text
                if(not element.get_attribute('class')=='pg-next pg-disabled'):
                    try:
                        js = "document.getElementsByClassName('kg-pagination2 thm-1 align-r')[0].getElementsByTagName('ul')[0].lastElementChild.click()"
                        driver.execute_script(js)
                    except:
                        #print u'点击失败'
                        #raw_input()
                        pass
                    #element.click()
                    time.sleep(5)
                    try:
                        #print driver.find_element_by_xpath('//*[@class="sufei-dialog sufei-dialog-kissy"]').is_displayed()
                        if(driver.find_element_by_xpath('//*[@class="sufei-dialog sufei-dialog-kissy"]').is_displayed()):
                            print u'出现验证码，请输入验证码点击提交之后回车'
                            print u'出错页数', n+1
                            raw_input()
                            #continue
                    except:
                        pass
                else:
                    print u'已经没有下一页'
                    break
            except Exception,e:
                print u'出错页数',Exception,e
                try:
                    if (driver.find_element_by_xpath('//*[@class="sufei-dialog sufei-dialog-kissy"]').is_displayed()):
                        print u'出现验证码，请输入验证码点击提交之后回车'
                        print u'当前页数',n+1
                        raw_input()
                        continue
                except:
                    pass
                try:
                    driver.find_element_by_xpath('//*[@class="kg-pagination2 thm-1 align-r"]/ul/li[last()]')
                except:
                    break
                #raw_input()
                #break
                pass
            n+=1
        print u'结束'
        #driver.save_screenshot('test.png')
        #driver.quit()
    def getTmail(self,url):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        #dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.939 Mobile Safari/537.36")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            '--user-data-dir=C:\Users\\' + getpass.getuser() + '\AppData\Local\Google\Chrome\User Data')
        driver = webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=chrome_options)
        #driver = webdriver.PhantomJS(executable_path='phantomjs.exe',desired_capabilities=dcap)
        #driver.set_page_load_timeout(60)
        #driver.maximize_window()
        try:
            driver.get('https://login.taobao.com/member/login.jhtml')

            print u'登录后按回车'
            raw_input()
        except:
            print u'页面访问失败'
            #driver.quit()
            pass
            return
        try:
            driver.get(url)
            WebDriverWait(driver, 60, 2).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'J_ReviewsCount')))
        except:
            driver.execute_script('if (window.stop) window.stop();else document.execCommand("Stop");')
            try:
                driver.find_elements_by_class_name('J_ReviewsCount')[0]
            except:
                print u'访问链接超时，请重启运行'
                #driver.quit()
                return
        try:
            print u'已经进入页面'
            js = "document.getElementsByClassName('J_ReviewsCount')[0].click()"
            driver.execute_script(js)
            #driver.find_elements_by_class_name('J_ReviewsCount')[0].click()
            WebDriverWait(driver, 60, 2).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'tm-rate-fulltxt')))
            time.sleep(5)
        except:
            print u'加载评论超时'
            #driver.quit()
            return
        dir_name=self.get_webservertime()
        if(os.path.exists(dir_name)):
            print u'文件夹已经存在'
            return
        os.makedirs(dir_name+'/img')
        f = open('./' + dir_name + '/' + u'评论.txt', 'w')
        f.close()
        f = open('./' + dir_name + '/' + u'图片链接.txt', 'w')
        f.close()
        n=1
        while(True):
            print n
            soup = BeautifulSoup(driver.page_source, "lxml")
            tmp=soup.find_all('div',class_='rate-grid')[0]
            tmp_list = tmp.find_all('tbody')
            tbody=tmp_list[0]
            item_list=tbody.find_all('tr')
            text=''
            img_text=''
            for item in item_list:
                comment_list=item.find_all('div',class_="tm-rate-fulltxt")
                comment_text=''
                for comment in comment_list:
                    try:
                        tmp_text=comment.string.strip()
                        if(tmp_text==''):
                            print u'没有评论'
                        else:
                            comment_text+=tmp_text+'\n'
                            print tmp_text
                    except:
                        print u'没有评论2'
                text+=comment_text+'-----------------------------------------------------'+'\n'
                img_list=item.find_all("img")
                for img in img_list:
                    try:
                        img_url=img.attrs['src']
                        #print img_url
                        if(not img_url=='about:blank' and not img_url==''):
                            img_url=img_url.split('jpg')
                            #print img_url
                            a_list=img_url[0].split('/')#为了获取图片名进行切割
                            filename=a_list[len(a_list)-1]
                            img_url='https:'+img_url[0]+'jpg'
                            print img_url
                            if(self.test==False):
                                response = self.session.get(img_url)
                                self.img_index+=1
                                with open('./'+dir_name+'/img/'+str(self.img_index)+'.jpg', 'wb') as f:
                                    f.write(response.content)
                                    f.close()
                            else:
                                img_text+=img_url+'\n'
                    except Exception,e:
                        print Exception,e
                        print u'图片下载失败'
                        pass
            if(self.test==True):
                f = open('./' + dir_name + '/' + u'图片链接.txt', 'a')
                f.write(img_text)
                f.close()
            f = open('./' + dir_name  +'/' +u'评论.txt', 'a')
            f.write(text.encode('gbk','ignore'))
            f.close()
            try:
                element=driver.find_element_by_xpath('//*[@class="rate-paginator"][1]/a[last()]')
                if(element.text==u'下一页>>'):
                    try:
                        js = "document.getElementsByClassName('rate-paginator')[0].lastChild.click()"
                        driver.execute_script(js)
                    except:
                        pass
                    time.sleep(5)
                else:
                    #print element.text
                    print u'已经没有下一页'
                    break
            except Exception,e:
                print u'页面出错',Exception,e
                try:
                    driver.find_element_by_xpath('//*[@class="rate-paginator"][1]/a[last()]')
                except:
                    break
                #raw_input()
                pass
            n+=1
        print u'结束'
        #raw_input()
        #driver.save_screenshot('test.png')
        #driver.quit()
    def getMogujie(self,url):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        #dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Linux; U; Android 7.0; zh-CN; MI 5 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.0.939 Mobile Safari/537.36")
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument(
            '--user-data-dir=C:\Users\\' + getpass.getuser() + '\AppData\Local\Google\Chrome\User Data')
        driver = webdriver.Chrome(executable_path="chromedriver.exe",chrome_options=chrome_options)
        #driver = webdriver.PhantomJS(executable_path='phantomjs.exe',desired_capabilities=dcap)
        #driver.set_page_load_timeout(60)
        #driver.maximize_window()
        try:
            driver.get(url)
            WebDriverWait(driver, 60, 2).until(
                ec.element_to_be_clickable((By.XPATH, '//*[@class="tabbar-list clearfix"]/li[2]/a')))
        except:
            print u'访问链接超时，请重启运行'
            #driver.quit()
            return
        try:
            print u'已经进入页面'
            time.sleep(3)
            js = "document.getElementsByClassName('tabbar-list clearfix')[0].getElementsByTagName('li')[1].click()"
            driver.execute_script(js)
            #driver.find_element_by_xpath('//*[@class="tabbar-list clearfix"]/li[2]/a').click()
            WebDriverWait(driver, 60, 2).until(
                ec.presence_of_element_located((By.CLASS_NAME, 'info-m')))
            #time.sleep(5)
        except Exception,e:
            print Exception,e
            print u'加载评论超时'
            #driver.quit()
            return
        dir_name=self.get_webservertime()
        if(os.path.exists(dir_name)):
            print u'文件夹已经存在'
            return
        os.makedirs(dir_name+'/img')
        f = open('./' + dir_name + '/' + u'评论.txt', 'w')
        f.close()
        f = open('./' + dir_name + '/' + u'图片链接.txt', 'w')
        f.close()
        #soup = BeautifulSoup(driver.page_source, "lxml")
        #print len(soup.find_all("li", class_="item")),soup.find_all("li", class_="item")
        #driver.save_screenshot('aa.png')
        n=1
        while(True):
            print n
            soup = BeautifulSoup(driver.page_source, "lxml")
            tmp_list = soup.find_all('div',id='J_RatesBuyerList')
            item_list=tmp_list[0].find_all('div',class_="item clearfix")
            text=''
            img_text=''
            for item in item_list:
                comment_list = item.find_all('div', class_="info-m")
                comment_text=''
                for comment in comment_list:
                    try:
                        tmp_text=comment.string.strip()
                        if(tmp_text==''):
                            print u'没有评论1'
                        else:
                            comment_text+=tmp_text+'\n'
                            print tmp_text
                    except:
                        print u'没有评论2'
                text+=comment_text+'-----------------------------------------------------'+'\n'
                img_list=item.find_all("img")
                for img in img_list:
                    try:
                        img_url=img.attrs['src']
                        if(not img_url=='about:blank' and not '64x64' in img_url):
                            img_url=img_url.split('jpg')
                            #print img_url
                            a_list=img_url[0].split('/')
                            filename=a_list[len(a_list)-1]
                            img_url=img_url[0]+'jpg'
                            print img_url
                            if(self.test==False):
                                response = self.session.get(img_url)
                                self.img_index+=1
                                with open('./'+dir_name+'/img/'+str(self.img_index)+'.jpg', 'wb') as f:
                                    f.write(response.content)
                                    f.close()
                            else:
                                img_text+=img_url+'\n'
                    except:
                        print u'图片下载失败'
                        pass
            if(self.test==True):
                f = open('./' + dir_name + '/' + u'图片链接.txt', 'a')
                f.write(img_text)
                f.close()
            f = open('./' + dir_name  +'/' +u'评论.txt', 'a')
            f.write(text.encode('gbk','ignore'))
            f.close()
            try:
                element=driver.find_element_by_xpath('//*[@class="pagination"]/a[last()]')
                #print element.text
                if(element.text==u'下一页>'):
                    try:
                        js = "document.getElementsByClassName('pagination')[0].lastChild.click()"
                        driver.execute_script(js)
                    except:
                        pass
                    #element.click()
                    time.sleep(5)
                else:
                    print u'已经没有下一页'
                    break
            except Exception,e:
                print u'页面错误',Exception,e
                try:
                    driver.find_element_by_xpath('//*[@class="pagination"]/a[last()]')
                except:
                    break
                #break
                pass
            n+=1
        print u'结束'
        #driver.quit()



spider=taobao_mgj_spider()
while(True):
    print u'首先把链接放入：链接.txt文本中,然后输入要爬的平台,输入1是淘宝,2是天猫,3是蘑菇街'
    a=raw_input()
    if(a=='1'):
        f=open(u'链接.txt','r')
        url=f.read().strip()
        f.close()
        spider.getTaobao(url)
    elif(a=='2'):
        f = open(u'链接.txt', 'r')
        url = f.read().strip()
        f.close()
        spider.getTmail(url)
    elif(a=='3'):
        f = open(u'链接.txt', 'r')
        url = f.read().strip()
        f.close()
        spider.getMogujie(url)
    else:
        print u'未识别您的输入'
print u'按回车退出'
raw_input()
