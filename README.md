# Usage
安装依赖：
    
    sudo apt-get install pip
    pip install requests
    pip install rsa
    pip install cherrpy
    pip install pyquery
   
运行`server.py`运行服务器

    cd lab1/
    python server.py

然后在浏览器中查看网页`127.0.0.1:8080`即可查看demo

# 微博的爬虫设计

## 基本架构

`WeiboCrawler`对象中保存了和微博爬虫相关的所有信息。基本的工作原理是：

在对象初始化之后，首先模拟浏览器登录微博，登录的方法参考的是[Python 微博登录原理](https://gist.github.com/mrluanma/3621775)。
登录之后，每次对保存在`weibo_fun_feeds`的链接执行GET，对获取的结果执行parse，得到每一条微博的信息。
保存的信息主要包括：用户名，文本内容，图片链接，以及赞数、转发数和评论数。
当parse出来图片链接以后，要对图片内容进行下载，同时把在本地的图片文件地址保存到对应的Feed对象中。
考虑到上层的接口，`WeiboCrawler`首先执行init run，获得所有在feed列表中的feed的数据，保存在自己的`feed_list`中。
server每次执行run，`WeiboCrawler`就会返回十条数据。

所用到的对象：

1. `feed_list`: 用来保存所有已经爬取的数据，数据的格式为`WeiboFeedData`
2. `curr_pace`: 用来保存当前已经显示的数据的位置

## 解析HTML的方法

### 数据源

考虑到微博的网页版主页上HTML的结构太过复杂，很难解析，我们对微博的数据源进行了选择:

1. 为了使HTML相对简单，我们选择在[微博手机版](http://weibo.cn)上进行数据抓取
2. 为了获取更集中的搞笑信息，我们在微博手机版上的广场条目中找到了[笑话](http://weibo.cn/pub/category?cat=1899)专题

### 解析方法

对于一条微博，基本的信息结构如下(表达式使用PyQuery)：

    用户id:     d('div.c div a.nk')
    文本内容:   d('div.c div span.ctt')
    缩略图信息: d('div.c div a img')
    原图信息:   d('div.c div a').filter(lambda i, this: pq(this).text() == u'原图')
    赞信息:     d('div.c div a').filter(lambda i, this: pq(this).text().encode('utf-8').find(u'赞'.encode('utf-8')) != -1)
    转发信息:   d('div.c div a').filter(lambda i, this: pq(this).text().encode('utf-8').find(u'转发'.encode('utf-8')) != -1)
    评论信息:   d('div.c div a').filter(lambda i, this: pq(this).text().encode('utf-8').find(u'评论'.encode('utf-8')) != -1)
    日期信息:   d('div.c div span.ct')

之后解析直接使用`text`方法就可以获取对应HTML标签中的内容了。

## 有关排序策略

在这里我们使用非常简单的排序方法，基于以下假设：

1. 一条微博越重要，赞数，评论数，转发数应该都相对高；
2. 对于搞笑微博来说，赞数和转发数应该比评论数更重要，因为对于这种信息量小的内容，用户往往不愿意花费时间去评论一些废话；
3. 微博越搞笑，大家越喜欢转发给朋友的次数越多；


因此最后的权值计算是:

    赞数 * 0.35 + 转发数 * 0.45 + 评论数 * 0.2

# 蛋花网爬虫策略

+ 建立scrapy项目：scrapy startproject danhuaer

+ 定义Item：在items.py中定义要爬取的数据。因为只爬取了图片所以只有url = scrapy.Field()

+ 实现spider：在项目文件夹下的spiders文件夹中新建一个python文件，danhuaerspider.py。Spider是一个继承自scrapy.contrib.spiders.CrawlSpider的python类。有三个必须定义的成员：

		name：spider的标示；
		start_urls：spider开始抓取的网页；
		parse(): 负责解析并匹配抓取的数据，解析为item
	

在danhuaerspider.py中，爬虫允许的领域allowed\_domains限制在danhuaer.com中。

爬虫的起始位置为http://danhuaer.com/?o=top 在这个网页上有很多图片的链接，每个链接都为http://danhuaer.com/t/xxxxxx格式，所以利用正则表达式，设定规则

	rules = (Rule(SgmlLinkExtractor(allow=('/t/\d*'),callback = 'parse_img',follow=True),) 
	
即会对所有符合规则的网页进行爬取，调用parse_img处理。

+ parse\_img是要将所需要的内容提取出来。查看蛋花儿网页面源代码可知需要提取的图片在<div class = “post-container”> 中，图片链接在src=”http://xxxxxx.jpg”中。所以用xpath将src=的链接提取出来，结果存储到urlItem中。

+ pipelines.py文件是关于爬取的内容存储的。item['url']是爬取出的图片的链接。

# 知乎日报爬虫策略

利用Chrome的开发者工具获知乎日报的API为，且没有加密验证

	http://news.at.zhihu.com/api/1.2/news/before/date
	
于是直接利用python的`requests`包，模拟浏览器发送请求，获取`json`格式结果即可。

# 煎蛋爬虫策略

与知乎日报类似，使用`requests`包模拟浏览器请求，然后对结果进行正则表达式匹配即可

# Demo展示

使用`cherrpy`工具搭建了一个简易的服务器，然后前端使用`wookmark`框架，以及`handlebars`模板生成工具，将所有内容以瀑布流的方式展现给用户。每次刷新到页底的，向服务器获取数据，即时爬取新的数据即可。
