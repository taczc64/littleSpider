#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# 标准模板文件布局
import urllib2
from bs4 import BeautifulSoup

# 糗事百科爬虫


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6)"
        self.headers = {"User-Agent": self.user_agent}
        # 存放每一页的内容，每个元素是一页。
        self.stories = []
        self.enable = False

    # 根据索引获取某一页的代码
    def getPage(self, pageIndex):
        try:
            url = "http://www.qiushibaike.com/hot/page/" + str(pageIndex)
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode("UTF-8")
            return pageCode

        except urllib2.URLError, e:
            if hasattr(e, "reason"):
                print u"连接糗事百科失败，错误原因:", e.reason
                return None

    # 传入一页的代码，返回这一页的所有段子，不包含带图片的段子
    def getPageItem(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "加载失败.."
            return None
        soup = BeautifulSoup(pageCode)
        divs = soup.find_all("div", class_="article block untagged mb15")
        pageStories = []
        for div in divs:
            writer = div.find_all("h2")[0].string
            content = div.find_all("div", class_="content")[0].find("span").text
            good = div.find_all("span", class_="stats-vote")[0].find("i").string
            comments = div.find_all("span", class_="stats-comments")[0].find("i").string
            # if not content:
            #     continue
            pageStories.append([writer, content, good, comments])
        return pageStories

    # 加载一页的内容
    def loadPage(self):
        if self.enable:
            if len(self.stories) < 2:
                pageStories = self.getPageItem(self.pageIndex)
                if pageStories:
                    self.stories.append(pageStories)
                    self.pageIndex += 1

    # 加载一页的段子，每次回车读出一条
    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            input = raw_input()
            self.loadPage()
            if input == 'Q':
                self.enable = False
                return
            print u"第%d页\t发布人:%s\t赞:%s\t评论:%s\n%s" %(page, story[0], story[2],story[3], story[1])

    def start(self):
        print u"开始阅读糗事百科，按回车查看新段子，Q键退出"
        self.enable = True
        self.loadPage()
        currentPage = 0
        while self.enable:
            print len(self.stories)
            if len(self.stories) == 0:
                return
            if len(self.stories) > 0:
                pageStories = self.stories[0]
                currentPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, currentPage)


spider = QSBK()
spider.start()
