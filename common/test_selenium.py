#coding=utf-8
__author__ = 'Daemon'

import urllib2,re,os,datetime
from selenium import webdriver

class Spider:
    def __init__(self):
        self.dirName='/3T/girls/mm/'
        #这是一些配置 关闭loadimages可以加快速度 但是第二页的图片就不能获取了打开(默认)
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        #cap["phantomjs.page.settings.loadImages"] = False
        #cap["phantomjs.page.settings.localToRemoteUrlAccessEnabled"] = True
        browserPath = "/home/meitu/TaoGirlDownload/phantomjs"
        self.driver = webdriver.PhantomJS(desired_capabilities=cap, executable_path = browserPath)

    def getContent(self, n):  
        for page in range(n):
            self.getDetailPage()

    def getDetailPage(self):
        url = "https://500px.com/photo/209952665/i-love-bled-by-g%C3%BCrkan-g%C3%BCndo%C4%9Fdu?ctx_page=1&from=popular"
        print "getting... ", url
        self.driver.get(url)
        print "got."
        icon_url=self.driver.find_element_by_xpath('//div[@class="main_container modal_version"]//img')
        print icon_url
        x
        icon_url=icon_url.get_attribute('src')
        dir= os.path.join(self.dirName, name)
        self.mkdir(dir)
        images_url=self.driver.find_element_by_xpath('//ul[@class="mm-p-menu"]//a')
        images_url=images_url.get_attribute('href')
        try:
            self.getAllImage(images_url,name)
        except:
            print images_url
            print("getAllImage error")

    def getAllImage(self,images_url,name):
        self.driver.get(images_url)
        photos=self.driver.find_element_by_xpath('//div[@class="mm-photo-cell-middle"]//h4/a')
        photos_url=photos.get_attribute('href')
        print photos_url

        self.driver.get(photos_url)
        images_all=self.driver.find_elements_by_xpath('//div[@class="mm-photoimg-area"]/a/img')
        print images_all

        self.saveImgs(images_all,name)


    def saveImgs(self,images,name):
        index=1

        for imageUrl in images:
            x = '_290x10000.jpg'
            url = imageUrl.get_attribute('src')
            url = url[:len(url)-len(x)]
            splitPath = url.split('.')
            fTail = splitPath.pop()
            if len(fTail) > 3:
                fTail = "jpg"
            fileName = os.path.join(self.dirName, name, name+ str(index) + "." + fTail)

            self.saveImg(url,fileName)
            index+=1
            self.total += 1
            print "total:", self.total


    def saveIcon(self,url,dir,name):

        splitPath=url.split('.')
        fTail=splitPath.pop()
        fileName= os.path.join(dir, name+'.'+fTail)
        print(fileName)
        self.saveImg(url,fileName)

    def saveImg(self,imageUrl,fileName):
        print 'page:', self.page,  'image url:', imageUrl
        u=urllib2.urlopen(imageUrl)
        data=u.read()
        f=open(fileName,'wb')
        f.write(data)
        f.close()

    def saveBrief(self,content,dir,name,speed_time):
        speed_time=u'当前MM耗时 '+str(speed_time)
        content=content+'\n'+speed_time

        fileName=os.path.join(dir, name+'.txt')
        f=open(fileName,'w+')
        f.write(content.encode('utf-8'))

    def mkdir(self,path):
        path=path.strip()
        if not os.path.exists(path):
            os.makedirs(path)

spider=Spider()
spider.getContent(2)  # 2932 is loaded
