# ustc-webinfo
A collection for labs and projects for web information at ustc, fall 2019.
## Openning Lab
A spider crawling throuth Douban website to extract music information. Based on scrapy.

Student: 许世晨, PB17030846.

Here is the lab requirements https://git.bdaa.pro/yxonic/data-specification/wikis/%E8%B1%86%E7%93%A3%20%E4%B9%90%E8%AF%84.

### 爬取top250音乐信息
将分支切换至`master`.
```shell
$ scrapy crawl douban
```
### 爬取所有音乐URL
将分支切换至`master`.
```shell
$ scrapy crawl allmusic
```
### 分布式爬虫
将分支切换至`distributed`.
主从分布式爬虫. 主爬虫获取需要爬取页面的URL, 从爬虫从URL中获取数据.
首先安装数据库redis和pymongo. 前者用于在不同主机之间进行URL通信, 后者用于保存爬取的数据.
