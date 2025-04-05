import BeautifulSoup

html = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<html>
<head>
<title>Index of /public/projekty</title>
</head>
<body>
<h1>Index of /public/projekty</h1>
<table><tr><th><img src="/icons/blank.gif" alt="[ICO]" /></th><th><a href="?C=N;O=D">Name</a></th><th><a href="?C=M;O=A">Last modified</a></th><th><a href="?C=S;O=A">Size</a></th><th><a href="?C=D;O=A">Description</a></th></tr><tr><th colspan="5"><hr /></th></tr>
<tr><td valign="top"><img src="/icons/back.gif" alt="[DIR]" /></td><td><a href="/public/">Parent Directory</a></td><td>&nbsp;</td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/folder.gif" alt="[DIR]" /></td><td><a href="2014/">2014/</a></td><td align="right">16-Mar-2015 11:20  </td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/folder.gif" alt="[DIR]" /></td><td><a href="2015/">2015/</a></td><td align="right">14-Oct-2016 12:28  </td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><td valign="top"><img src="/icons/folder.gif" alt="[DIR]" /></td><td><a href="2016/">2016/</a></td><td align="right">07-Nov-2016 09:43  </td><td align="right">  - </td><td>&nbsp;</td></tr>
<tr><th colspan="5"><hr /></th></tr>
</table>
<address>Apache/2.2.15 (CentOS) Server at b2b.roscosteel.eu Port 8080</address>
</body></html>'''


if __name__ == '__main__':
    soup = BeautifulSoup.BeautifulSoup(html)
    print(soup.html.title.text)
    print(soup.findAll('a'))