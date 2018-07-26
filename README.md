# scrapy爬虫框架应用

## 1. 打开cmd 在要建立爬虫程序的目录下输入

> scrapy startproject itcast (“爬虫工程名称”)

## 2. 在工程目录下的spiders文件夹下，输入

> scrapy genspider itcast "http://www.itcast.cn"( 爬虫文件名称" “作用域”)



## 3. 在spider文件中输入 scrapy crawl itcst 直接执行爬虫



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

   ​