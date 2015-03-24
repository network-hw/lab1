

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
