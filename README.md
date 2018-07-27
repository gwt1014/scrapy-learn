# scrapy爬虫框架应用

#### 0. scrapy在windows环境下的安装，起手劝退！

 1.  lxml

     >  pip install lxml

 2.  zope.interface

     >  pip install zope.interface

 3.  twisted

     > https://www.lfd.uci.edu/~gohlke/pythonlibs/#twisted

     > pip install wheel
     >
     > pip install xxxxxx.whl 这里要跳到下载目录

	4. pyOpenSSL

    > pip install pyOpenSSL

	5. pywin32

    > https://pypi.pyhon.org/pypi/pypiwin32

    > pip install pywin32xxxxxx.whl  这里要跳到下载目录

	6. scrapy

    > pip install scrapy



#### 1. 打开cmd 在要建立爬虫程序的目录下输入

scrapy startproject xxxxx

#### 2. 在工程目录下的spiders文件夹下，输入

scrapy genspider xxx "http://www.xxxx.com"

#### 3. 爬虫核心

3.1 编写items.py  明确需要爬取的内容

3.2 编写spiders/xxx.py 编写爬虫文件，处理请求和响应，提取数据

​	from xxx.items import xxxItem

- yield item
- yield scrapy.Resquest(url,callback = self.parse)

3.3 编写pipelines.py 编写管道文件，处理spider返回的item数据，基本就是存json，在这里改编码.encode("utf-8")


3.4 编写settings.py **启动管道组件**，其他设置。所有header都在这里，User-agent和其他的不在一起

#### 4.  scrapy crawl xxx 直接执行爬虫



# 注意事项

- spider.py 自己的爬虫文件
- pipelines.py 管道文件，负责处理item

## 1. spider.py

1. 生成一个itcast.py的爬虫文件，用来写爬虫的方法，一定要在开始加上

> import scrapy 
>
> from ITcast.items import ItcastItem 

​	否则这里面不知道ITcastItem是什么

2. spider内用xpath获取的内容并不是文本，而是一个一个xpath对象，所以后面要加.extract()进行“剥壳”。剥壳之后是列表，选[0]就可以了
3. 如果是return item，那就直接给管道。如果是return scrapy.Request(xxxxurl)那就给调度器的请求队列
4. 如果start_urls列表中有多个url，那么parse会并发处理每一个响应
5. **selectors选择器** 不管用哪个选择器，都要用extract()进行剥壳
   1. xpath() 返回的是列表
   2. css() 类似BS4
   3. re 这个不用剥壳，直接返回

## 2. pipelines.py

1. pipelines.py中 写json写入的时候 mode 要用wb 、 wb+，如果用w会报错

2. 编码的修改还是在最后pipeline中最后保存的时候进行设置，在腾讯HR的里面报错了

## 3. 下载图片或媒体文件
1. pipelines 
    导入
    import scrapy
    from scrapy.pipelines.images import ImagesPipeline
    from settings import IMAGES_STORE as images_store
    import os #为了重命名用
    保存
    class xxxPipeline(ImagesPipeline)
        #保存
        def get_media_requests(self,item,info):
            image_link = item['imagelink']
            yield scrapy.Request(image_link)
        #文件改名
        def item_completed(self, results,item ,info ):
            #取出图片路径
            image_path = [x['path'] for ok ,x in results if ok]
            #重命名
            os.rename(images_store + image_path[0] ,images_store + item['nickname'] + ".jpg")

2. setings 要增加参数
    IMAGES_STORE = '绝对路径'