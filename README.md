# Python 漫画网站爬虫
## 尊重版权，只供爱好者研究使用，禁止商业用途，保留追究法律责任的权利
## 简介
作为二刺猿，漫画是不能断的，一直在追的漫画使用正版软件观看，
也花费不了多少钱，但是对于那些章节多的，
使用正版软件观看需要花费一大笔费用，所以找漫画就需要去其他免费的网站上看了，
原来[动漫之家](http://manhua.dmzj.com/)是有许多漫画和轻小说的，但慢慢的都被正版搬空了，
这里推荐一个漫画网站：[新新漫画](https://www.177mh.net/)，
更新得挺快的，爬就完事儿了，开始整活
## 运行环境
* 开发语言：python3
* 系统：Windows/Linux/MacOS
## 使用说明
### 1.下载脚本
```
git clone https://github.com/MemoryDewey/comic_crawler.git
```
运行上述命令，将本项目下载到当前目录，如果下载成功当前目录会出现一个名为"comic_crawler"的文件夹；
### 2.安装依赖
```
$ pip3 install
```
### 3.程序设置
前往[新新漫画](https://www.177mh.net/)，查询自己想要搜索的漫画，
查看漫画对应的URL，这里拿[租借女友](https://www.177mh.net/colist_240268.html)举例，
URL中有colist_240268，拿到colist后面的数字240268

打开comic.py文件，在**main**代码中，修改**cid**对应的值为上面拿到的数字
```
if __name__ == '__main__':
    # 网站漫画ID，修改这里
    cid = "240268"
    chapters = None
    get_chapter('https://www.177mh.net/colist_%s.html' % cid)
    f = open('./details.json', 'r', encoding='UTF-8')
    chapters = json.load(f)
    for chapter in chapters:
        get_comic(chapter, cid)
    print('done')
```

开始运行，在目录下会有一个downloads文件夹，里面便是下载好的漫画
> 如需更改漫画文件名，则打开rename.py
> 更改old_name为已下载的漫画名，new_name为自定义的漫画名，
> 运行即可

## 说明
> 如果对您有帮助，您可以点右上角 "Star" 支持一下 谢谢！ ^_^
