# scrapy爬虫框架应用

## 1. 打开cmd 在要建立爬虫程序的目录下输入

> scrapy startproject itcast (“爬虫工程名称”)

## 2. 在工程目录下的spiders文件夹下，输入

> scrapy genspider itcast "http://www.itcast.cn"( 爬虫文件名称" “作用域”)

生成一个itcast.py的爬虫文件，用来写爬虫的方法

已经要在开始加上

> import scrapy 
>
> from ITcast.items import ItcastItem 

否则这里面不知道ITcastItem是什么

## 3. 在spider文件中输入 scrapy crawl itcst 直接执行爬虫



# 注意事项

1. pipelines.py中 写json写入的时候 mode 要用wb 、 wb+，如果用w会报错
2. spider内用xpath获取的内容并不是文本，而是一个一个xpath对象，所以后面要加.extract()进行“剥壳”。剥壳之后是列表，选[0]就可以了