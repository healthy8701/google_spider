import os
import urllib.request
import urllib
import re

search_item = '周子瑜'
photos = []
if not os.path.exists('photo\\'+search_item): #先確認資料夾是否存在
	os.makedirs('photo\\'+search_item)
	
keyWord = urllib.request.quote(search_item) #將中文轉換編碼方式
url = 'https://www.google.com.tw/search?q='+keyWord+'&hl=zh-TW&biw=1649&bih=872&site=imghp&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiC2o2A1KvMAhWEkJQKHbZ7AocQ_AUIBygC'  #入口頁面
req = urllib.request.Request(url+'/', headers = {
		'Connection': 'Keep-Alive',
		'Host': 'www.google.com.tw',
		'Referer': 'https://www.google.com.tw',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'zh-TW,en-US;q=0.7,en;q=0.3',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:40.0) Gecko/20100101 Firefox/40.0.3 Waterfox/40.0.3'
	})	

web_page = urllib.request.urlopen(req , timeout = 5).read().decode('utf-8')
web_filter = re.compile("http(.+?)\"")		
for image_url in web_filter.findall(web_page):		
	if '.jpg' in image_url.lower() or '.png' in image_url.lower() or '.bmp' in image_url.lower() or '.jpeg' in image_url.lower():
		photos.append('http'+image_url)		

i = 0
for photo in photos:
	try:
		web_page = urllib.request.urlopen(photo, timeout = 5).read()				
	except:
		continue
	else:
		f = open('photo\\'+search_item+'\\'+str(i)+'.jpg', 'wb')
		i += 1
		f.write(web_page)
		f.close()