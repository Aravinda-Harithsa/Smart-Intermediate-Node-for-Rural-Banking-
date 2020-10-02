import time
import os
from fetcher import fetcher
from preprocessing import preprocessing
from sendmessage import *

while True:
	start = time.time()
	df = fetcher()
	df = preprocessing(df)
	#os.chdir('C:\\Users\\Adithya\\Documents\\GitHub\\Athena')
	#os.chdir('C:\\Users\\Dexter\\Documents\\Projects\\SIH\\Athena')
	os.chdir('/home/pi/Desktop/Athena')
	for dest,msg in zip(df.To,df.Content):
		phno,lang = getInfo(dest)
		msg=changeLang(msg,lang)
		print(phno)
		sendmessage(phno,msg)
	exe_time = time.time() - start
	time.sleep(120-exe_time)