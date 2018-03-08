#爬取豆瓣电影 Top250
import requests
# lxml  xml 解析
from lxml import html

url = 'http://movie.douban.com/top250?start={}&filter='

# //从匹配选择的当前节点选择文档中的节点，不考虑文职
# / 从根节点选取
# . 当前节点
# .. 当前节点父节点
# @ 选取属性

k=1

for index in range(0, 10):
    con = requests.get(url.format(index * 25))
    sel = html.fromstring(con.content)
    # 选取所有带有class='info'元素的  div 元素
    for i in sel.xpath('//div[@class="info"]'):
        # 选取带 class='hd' 的元素div 元素，筛选 a 然后筛选 class='title'的 span  元素

        # 影片名称
        title = i.xpath('div[@class="hd"]/a/span[@class="title"]/text()')[0]
        # 引用
        quote = i.xpath('div[@class="bd"]/p/span[@class="inq"]/text()')[0]
        # 影片信息，导演，主演
        info = i.xpath('div[@class="bd"]/p/text()')
        directorActor = info[0].strip()
        timeCountry = info[1]
        timeCountry.replace(" ","").replace("\n","")
        timeCountry.strip()
        time = timeCountry.split(r'/')[0]
        time=time.strip()
        country = timeCountry.split(r'/')[1]
        geners = timeCountry.split(r'/')[2]
        # 评论人数
        evaluateNumber = i.xpath('div[@class="bd"]/div[@class="star"]/span[4]/text()')[0]
        # 评分
        evaluate = i.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0]

        with open("top250.txt","a",encoding='utf-8') as f:
            f.write("Top{}\n 影片名称：{}\n 评分：{} {}\n 上映时期：{}\n 上映国家：{}\n 导演、演员：{}\n"
                    .format(str(k),title,evaluate,evaluateNumber,time,country,directorActor))
            f.write("==========\n")

        k=k+1