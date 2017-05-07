from selenium import webdriver 
import threading
import time
import os
import queue
import urllib.request
import urllib
import re

SHARE_Q = queue.Queue()  #構造一個不限制大小的的隊列
_WORKER_THREAD_NUM = 50  #設置線程個數
class_num = 400 #設置下載張數
global i

class MyThread(threading.Thread) :
	def __init__(self, func) :
		super(MyThread, self).__init__()
		self.func = func

	def run(self) :
		self.func()

def main(photos, search_item) : #將每個圖片URL用多工處理
	global SHARE_Q
	threads = []
	print(len(search_item))	
	i = 0
	for task in photos :  #向隊列中放入任務
		if(i>=class_num):
			break
		SHARE_Q.put([search_item, task, i])		
		i = i + 1
	for i in range(_WORKER_THREAD_NUM) :
		thread = MyThread(main_worker)
		thread.start()
		threads.append(thread)
	for thread in threads :
		thread.join()
		
def main_worker() : #多工下載每張圖片
	global SHARE_Q	
	while not SHARE_Q.empty():
		item = SHARE_Q.get() #獲得任務		
		if item != None:			
			try:#下載圖片
				p = urllib.request.urlopen(item[1], timeout = 5).read()				
			except:
				continue
			else:
				f = open('photo\\'+item[0]+'\\'+str(item[2])+'.png', 'wb')
				f.write(p)
				f.close()		

if __name__ == '__main__':
	f = open('search_item.txt', 'r', encoding = 'utf-8-sig')
	search = []
	for line in f.readlines():
		search.append(line.strip('\n'))	
		
	for search_item in search:		
		photos = [] #記錄下載過的圖片地址，避免重複下載
		if not os.path.exists('photo\\'+search_item): #先確認資料夾是否存在
			os.makedirs('photo\\'+search_item)
			#獲得每張圖片的UR
			keyWord = urllib.request.quote(search_item)
			url = 'https://www.google.com.tw/search?q='+keyWord+'&tbm=isch&source=lnt&tbs=itp:photo&sa=X&ved=0ahUKEwjF3N2wgaLOAhXLFpQKHakCAjEQpwUIFA&dpr=1&biw=1452&bih=866'  #入口頁面
			xpath = '//div[@class="rg_meta"]' #目標元素的xpath  	
			driver = webdriver.Firefox() #啟動Firefox瀏覽器				 
			driver.maximize_window() #最大化窗口，因為每一次爬取只能看到視窗內的圖片
			driver.get(url) #瀏覽器打開爬取頁面  				
			pos = 0 
			m = 0 # 圖片編號 
			f = open('photo\\'+search_item+'\\log.txt', 'w')#紀錄圖片位置
			#模擬滾動窗口以瀏覽下載更多圖片
			for i in range(100):  
				pos += i*500 # 每次下滾500  
				js = "document.documentElement.scrollTop=%d" % pos  
				driver.execute_script(js)  
				time.sleep(1)     
				if m >= class_num:
					break
				for element in driver.find_elements_by_xpath(xpath):  
					img_url = element.get_attribute('innerHTML')
					img_url = re.findall(re.compile("ou\":\"(.+?)\""),img_url)[0]
					if m >= class_num:
						break		
					# 保存圖片到指定路徑  
					if img_url != None and img_url not in photos:  							
						photos.append(img_url)  
						f.write(img_url+'\n')#紀錄位置
						m += 1			
						
			driver.quit()				
			f.close()
			main(photos, search_item)#多工下載每張圖片	