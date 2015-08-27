import re
from os import listdir, getcwd
from scrapy.spiders import Spider
from cl_jobs.items import ChanItem
from scrapy.selector import Selector
from scrapy.http import Request, HtmlResponse

class MySpider(Spider):
    name = "4ch_gomi"
    allowed_domains = ["boards.4chan.org"]

    def __init__(self, combine=False, thread=""):
        self.combine = combine
        self.threadNum = re.search('[0-9]+', thread).group()
        self.header = '"post_num","thread_num","timestamp","time_difference","user_post"\n'

        self.start_urls = ['http://boards.4chan.org/%s' % thread] # HTTP ONLY, NO HTTPS

    def parse(self, response):
        inFile = "userposts.txt"
        outFile = ("output/%s.csv" % self.threadNum)

        item = ChanItem()
        item["title"] = response.url
        item["body"] = response.body

        # read in list of user posts
        with open(inFile, 'r') as f:
            userPosts = f.read().splitlines()
        
        ext = Selector(response=response).xpath( \
              "//html/body/form/div/div/div/div/div[contains(concat(' ',normalize-space(@class),' '),' postInfo desktop ')]").extract()
        self.logger.info("POSTS: %s", len(ext))
        #print ext[0], "\n\n", ext[1], "\n\n"

        postNum = []
        times = []
        for i in range(0, len(ext)):
            matchTime = re.search('data-utc="[0-9]*', ext[i])
            if matchTime:
                times.append( int(matchTime.group()[10:]) )
            else: # error case
                times.append(0)
            matchPost = re.search('name="[0-9]*', ext[i])
            if matchPost:
                postNum.append( int(matchPost.group()[6:]) )
            else: # error case
                postNum.append(0)

        prevTime = times[0]
        with open(outFile, 'wb') as f:
            f.write(self.header)
            for i in range(0, len(ext)):
                diff = times[i] - prevTime
                # check if user post
                if str(postNum[i]) in userPosts:
                    isUserPost = True
                else:
                    isUserPost = False
                f.write(str(postNum[i]) + "," + self.threadNum + "," + str(times[i]) + "," + str(diff) + "," + \
                        str(isUserPost) + "\n")
                prevTime = times[i]

        # combine threads
        if self.combine:
            files = listdir( "%s\output" % getcwd() )
            data = [self.header]
            for file in files:
                with open("output\\" + file, 'r') as f:
                    imp = f.readlines()[1:] # ignore header
                for row in imp:
                    data.append(row)
            with open("output\\combined.csv", 'wb') as f:
                for row in data:
                    f.write(row)

        return item