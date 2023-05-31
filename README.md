# JSfind
python环境：3.8+

JSfind是一款用作快速在网站的js文件中提取URL，接口的工具。该工具在JSFinder上进行了增强，主要有：

- 对提取的url,通过异步编程,快速访问并提取网站标题状态码长度,并保存到resut.txt.
- 提供参数对提取的url进行去除处理.

# usage



```
PS D:\python\JSfinder> python JSFinderPlus.py -h

usage: Jsfind.py [-h] [-u URL] [-f FILE] [-w] [-s]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     The website
  -f FILE, --file FILE  The file contains url or js
  -w, --web             web.
  -s, --screenweb       screenweb
  
  examples:
  python JSfind.py -u http://example.com    #指定单个url,扫描结果保存到resut.txt.
  python JSfind.py -f url.txt               #批量扫描url.txt内url,扫描结果保存到resut.txt.
  python JSfind.py -u http://example.com -w #将提取到的url通过异步编程,快速访问并提取网站标题状态码长度,并保存到web.txt.
  python JSfind.py -u http://example.com -w -s #将提取到的url通过异步编程,快速访问并提取网站标题状态码长度,并保存到resut.txt,并对resut.txt内url去重.
  python JSfind.py -f url.txt -w -s #同上
```

# example
python38 Jsfind.py -u https://xxx.xx.33.235:8001/
![YPMZZNDW92BWIFFSP`ZNEHB](https://github.com/ainiy-top/JSfind/assets/81848507/c8827fb1-af86-4429-82e1-34f8ce064a0b)

添加 -w -s参数查看结果

![52NG)F3N05FT QJVUQ5{5X](https://github.com/ainiy-top/JSfind/assets/81848507/cdf846d1-3c56-49b5-85f0-c4052f6f7911)

本程序在对接口url进行请求,采用了python的异步编程,在运行可能会存在不同程度报错,但是不会影响输出结果.

