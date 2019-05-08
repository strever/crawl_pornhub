# pornhub爬虫

[toc]


[[TOC]]

[TOC]

[[toc]]

## 概述

### 已实现功能

- 随机User-Agent请求头
- 随机代理
- 多来源爬取最新免费代理，数据redis落地
- 代理清洗
- 以分类维度爬取pornhub
- 爬虫日志`/data/logs`下
- 数据mysql落地

### todo

- 突破cookie令牌请求机制
- 突破scrapy无法读取\<noscript\>反爬机制
- 添加代理ip表建立优选机制
- 使用scrapy-redis实现分布式爬取


### contact

- @strever <strever@qq.com>

:smile:


## 部署（Deploy）

### requirement

- Python 2.7+
- scrapy 1.3.3+

### 安装scrapy

```shell

$ pip install scrapy
$ pip install pymysql
$ pip install redis

```

### 拉取项目代码
```git

$ git clone git@git.mysoft.com.cn:mic/gaia-poi-spider.git

```

### 配置

在根目录新建文件`.env`添加mysql，redis配置信息

```

$ mv .env.example .env

```



## 爬虫

### 爬虫当前设置

- 请求同时并发数：32
- 请求间隔：0.5秒
- 下载超时：30秒
- 重试2次
- user-agents池在/data/useragents.txt
- 重定向follow3次


### 爬虫命令

```shell

$ scrapy startproject crawl_pornhub

$ scrapy genspider pornhub pornhub.com

//抓取最新代理
$ scrapy crawl pull_proxy

//清理无用代理
$ scrapy crawl clean_proxy

//爬取pornhub
$ scrapy crawl pornhub -s JOBDIR=data/crawls/poi-1

//根据单个分类抓取
$ scrapy crawl pornhub -a cmd_arg=ht


```

### tor

如果部署在国外节点即可开启tor代理，稳定性高于免费代理或付费代理

- [tor](https://www.torproject.org/download/download.html.en)
- [tor-gui](https://people.torproject.org/~erinn/vidalia-standalone-bundles/)
- [polipo(http->sock5)](http://www.pps.univ-paris-diderot.fr/~jch/software/files/polipo/)

### 数据落地

```sql

CREATE TABLE `pornhub_videos` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `title` varchar(128) NOT NULL DEFAULT '' COMMENT '标题',
  `thumb` varchar(255) NOT NULL DEFAULT '' COMMENT '缩略图',
  `duration` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '时长',
  `video_link` varchar(255) NOT NULL DEFAULT '' COMMENT '视频浏览地址',
  `video_link_480p` varchar(255) NOT NULL DEFAULT '' COMMENT '视频下载链接',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_uniq_title` (`title`)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8 COMMENT='Pornhub视频资源表';

```

#### 代理池

redis-key： 'crawl:proxies'

```shell

host:port> zrange 'crawl:proxies' 0 -1 WITHSCORES

```


### licence

MIT

