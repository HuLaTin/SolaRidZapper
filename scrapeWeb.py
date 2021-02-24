import requests
import lxml.html
from urllib.request import urlopen
from lxml import etree
loginData = {'mailuid':'rice', 'pwd':'rice','login-submit':''}
r = requests.post('http://69.4.196.7/solarid/includes/login.inc.php', loginData)
html = etree.HTML(r.text)

# find = etree.XPath("//table/tr/*[contains(text(),'42')]/text()")
find = etree.XPath("//table/tr[td/text() = '42']/td/text()")

find(html)

