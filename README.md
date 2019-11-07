# ustc-webinfo
A collection for labs and projects for web information at ustc, fall 2019.
## Openning Lab
A spider crawling throuth Douban website to extract music information. Based on scrapy.

Student: 许世晨, PB17030846.

### requirements
本爬虫需要以下python包.

为了运行基本功能, 需要:
- `scrapy`
- `requests`
- `fake_useragent`

为了使用代理, 需要:
- `scrapy_proxies`

为了使用分布式爬虫, 需要:
- `scrapy_redis`
- `redis`

为了将爬取结构写入数据库, 需要:
- `pymysql`
- `pymongo`

此外, 分布式爬虫还需搭建redis数据库和mongo数据库.

### 爬取top250音乐信息
将分支切换至`master`.
```shell
$ scrapy crawl douban
```
数据将输出至`top250.json`中.
### 爬取所有音乐URL
将分支切换至`master`.
```shell
$ scrapy crawl allmusic
```
数据将输出至`allmusic.txt`中.
### 分布式爬虫

将分支切换至`distributed`.

#### 结构

这是一个主从分布式爬虫. 主爬虫不断获取新音乐的URL, 从爬虫从URL中获取音乐的结构化数据. 主从爬虫可以运行在不同或相同的主机上,并且可以运行多个主从爬虫. 

主爬虫将获取的URL存入Redis数据库, 为此你需要先搭建一个Redis数据库. 从爬虫从Redis数据库中获取URL, 爬取数据,
你可以选择将这些数据存储在Mongo数据库或本地磁盘中. 这里默认将数据存储在从爬虫所在主机的磁盘中.

#### 使用
首先创建redis数据库作为URL队列. 在本机或服务器上输入:
```shell
$ redis-service --port YourPort(default:6379)
```
在`doubanspider/settings.py`中, 修改`REDIS_SERVER`为redis服务器的IP地址或本机地址(127.0.0.1), 修改`REDIS_PORT`为选定的端口号. 如果你的Redis数据库搭建在和主爬虫相同的主机, 并且端口为`6379`, 则无需更改.

运行主爬虫:
```shell
$ scrapy crawl allmusic
```
此时, 主爬虫不断获得新的URL, 并将其存在Redis数据库中.

打开新的shell或更换主机, 运行从爬虫:
```
$ scrapy crawl douban
```
从爬虫从Redis数据库中获取音乐的URL, 并爬取音乐的详细信息. 这里默认将数据存在从爬虫所在主机的`music_info_distributed.json`文件中.

#### 将数据存在Mongo数据库中
如果你需要将数据存储在数据库中而非本地磁盘中, 你需要首先搭建一个Mongo数据库, 并在`doubanspider/settings.py`中修改MONGODB的URI, IP以及PORT.
然后修改`doubanspider/spiders/douban_spider.py`中的
```python
custom_settings = {
        'ITEM_PIPELINES': {'doubanspider.pipelines.DoubanspiderPipeline': 300}
}
```
为
```
custom_settings = {
        'ITEM_PIPELINES': {'doubanspider.pipelines.MgdbPipeline': 300}
}
```
然后安装相同的方式运行主从爬虫.

### 代码说明

- `doubanspider/spiders/douban_spider.py`: 从豆瓣音乐top250推荐页面获取唱片URL, 并从唱片介绍页面爬取结构化数据.
页面解析通过xpath语法基于scrapy.Selector完成.
- `doubanspider/spiders/allmusic.py`: 从一个音乐介绍页面开始, 通过音乐推荐获取新的URL, 并不断重复这一过程. 
页面解析通过xpath语法基于scrapy.Selector完成.
- `doubanspider/middlewares.py`: 其中的`RandomUserAgentMiddlware`用于添加User-agent头部, 避免爬虫被识别.
- `doubanspider/items.py`: 定义了爬取数据的结构.
- `doubanspider/pipelines.py`: 将爬取的数据存入磁盘或数据库.
- `doubanspider/settings.py`: 定义了一些配置.
- `proxies.py`: 从网上爬取一些IP代理, 避免爬虫被识别. 爬取的代理效果都不怎么地.
整个项目的基本框架由scrapy生成.
