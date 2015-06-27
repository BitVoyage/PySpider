__author__ = 'ZLS'
import urllib
import urllib2
import re
import thread
import time

class QSBK:
    #Initial
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozila/4.0(compatible;MSIE 5.5;Windows NT)'
        #initial headers
        self.headers = {'User-Agent':self.user_agent }
        #variable stores the stories
        self.stories = []
        #variable controls the exec
        self.enable = False
        #input the page number, get the source code
    def getPage(self,pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/'+str(pageIndex )
            #structe the request
            request = urllib2.Request(url,headers=self.headers )
            #get the source code
            response = urllib2.urlopen(request)
            #transform the code to UTF-8
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError,e:
            if hasattr(e,"reason"):
                print u"Fail to link the page, error info is ",e.reason
                return None


    #post the source code, get the stories in this page
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "failed to load the page"
            return None
        pattern = re.compile('<div class="content">(.*?)<!--(.*?)-->.*?<i class="number">(.*?)</i>',re.S)
        items = re.findall(pattern,pageCode)
        #Store the stories
        pageStories = []
        #traverse the info
        for item in items:
            #""#if have the Image
            # haveImag = re.search('img',item[3])
            # if not haveImag:
            #item[0],item[1],item[2]is: content
                pageStories.append([item[0].strip(),item[1].strip(),item[2].strip()])
        return pageStories

    def loadPage(self):
        if self.enable == True:
            if len(self.stories)<2:
                pageStories = self.getPageItems(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1



    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == "Q":
                self.enable = False
                return
            print u"Page Number:%d\tTime:%s\n%s\nVote:%s\n" %(page,story[1],story[0],story[2])


    def start(self):
        print u"Reading,press ENTER to check new story,press Q to quit"
        self.enable = True
        self.loadPage()
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories,nowPage)


Spider = QSBK()
Spider.start()

