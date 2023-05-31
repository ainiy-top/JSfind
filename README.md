# JSfind

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
  python JSfind.py -u http://example.com    #指定单个url
  python JSfind.py -f url.txt               #批量扫描url.txt内url
  python JSfind.py -u http://example.com -w -s #将提取到的url通过异步编程,快速访问并提取网站标题状态码长度,并保存到resut.txt.
  python JSfind.py -f url.txt -w -s #批量将提取到的url通过异步编程,快速访问并提取网站标题状态码长度,并保存到resut.txt.
```
