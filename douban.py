# 3个字段:
# 1.sort  =         排序方式(T:热度排序,R:时间排序,S:评价排序)
# 2.range =         表示评分区间,默认评分区间是:0-10
# 3.tags  =         标签
# https://movie.douban.com/tag/#/?sort=S&range=0,10&tags=中国大陆,2018
# Request URL: https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=&start=0&countries=%E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86&year_range=2018,2018
# %E4%B8%AD%E5%9B%BD%E5%A4%A7%E9%99%86 解码为 中国大陆
# start =  表示 偏移量  
import random
import json

import requests
from test.settings import User_Agents


class DoubanSpider(object):
    def __init__(self):
        #URL
        self.base_url = "https://movie.douban.com/j/new_search_subjects?sort=S&range=0,10&tags=&start="
        self.base_url2 = "&countries=中国大陆&year_range=2018,2018"
        #Headers
        self.headers = {'User-Agent': random.choice(User_Agents)}
        self.ans = open("D:/ans.json", 'a')

    def down_(self, offset):
        resp = None
        try:
            resp = requests.get(self.base_url+str(offset)+self.base_url2, headers=self.headers)
        except Exception as e:
            print(resp)
        return resp

    def get_(self, resp):
        if resp:
            if resp.status_code == 200:
                # HTTP状态码
                movies = dict(resp.json()).get('data')
                if movies:
                    return movies
                else:
                    return None
        else:
            return None

    def save_(self, movies):
        for movie in movies:
            dict(movie)
            data = [{'影片名称':movie['title'],'图片链接':movie['cover'],'评分':movie['rate']}]
            self.ans.write(json.dumps(data))
            # print(data)

def main():
    spider = DoubanSpider()
    offset = 0
    while offset<=200:
        # print (offset)
        reps = spider.down_(offset)
        movies = spider.get_(reps)
        spider.save_(movies)
        offset += 20
        # time.sleep(5)


if __name__ == '__main__':
    main()