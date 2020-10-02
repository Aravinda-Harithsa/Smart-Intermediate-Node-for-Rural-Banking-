import imaplib, email 
from email.parser import HeaderParser
import re
import base64
import email
import os
import pandas as pd
from datetime import datetime,timedelta

def fetcher():
	details_dict={"UID":[],"From":[],"To":[],"Subject":[],"Date":[],"Time":[],"Content":[],"Attachment":[]}
	username = "athena.primary.node@gmail.com"
	password = "sih2020!"
	host = "imap.gmail.com"

	def get_emails(result_bytes): 
		msgs = []
		for num in result_bytes[0].split(): 
			typ, data = mail.fetch(num, '(RFC822)') 
			msgs.append(data) 
		return msgs 

	def get_from_addrs(data):
		indexstart = data.find("From: ") 
		data2 = data[indexstart + 5: len(data)] 
		indexend = data2.find("Subject:")
		refined_data=data2[0: indexend]
		indexstart = refined_data.find("<") 
		result = refined_data[indexstart + 1: len(refined_data)] 
		indexend = result.find(">")		
		return (result[0: indexend])

	def get_to_addrs(data):
		search_string="X-Forwarded-For: "
		indexstart = data.find(search_string) 
		data2 = data[indexstart + len(search_string): len(data)] 
		indexend = data2.find(".com")
		refined_data=data2[0: indexend+4].replace("\r\n","")
		return refined_data

	def get_subject(data):
		indexstart = data.find("Subject: ") 
		data2 = data[indexstart + 8: len(data)] 
		indexend = data2.find("To: ")
		refined_data=data2[0: indexend].replace("\r\n","")
		return refined_data

	def get_time(data):
		search_string="(Google Transport Security);"
		indexstart = data.find(search_string) 
		data2 = data[indexstart + len(search_string): len(data)] 
		indexend = data2.find("Received-SPF")
		refined_data=data2[0: indexend].replace("\r\n","")
		date=re.sub(' +',' ',refined_data)
		date=date.split("-")[0]
		datetime_object = datetime.strptime(date, ' %a, %d %b %Y %H:%M:%S ')+timedelta(hours=12.5)
		date = datetime_object.strftime("%Y-%m-%d")
		time=datetime_object.strftime("%H:%M:%S")
		return date,time

	def get_mail(data):
		search_string='charset="UTF-8"'
		indexstart = data.find(search_string) 
		data2 = data[indexstart + len(search_string): len(data)] 
		indexend = data2.find("--0")
		refined_data=data2[0: indexend].replace("\r\n","")
		return refined_data

	print("Retrieving emails.....")
	mail = imaplib.IMAP4_SSL(host,993)
	mail.login(username,password)
	mail.select('Inbox')
	typ, data = mail.search(None,'All')
	msgs = get_emails(data)

	details=[]
	#root="C:\\Users\\Adithya\\Documents\\GitHub\\Athena\\Attachments"
	#root="C:\\Users\\Dexter\\Documents\\Projects\\SIH\\Athena\\Attachments"
	root="/home/pi/Desktop/Athena/Attachments"
	
	os.chdir(root)
	i=1
	for msg in msgs:
		
		for sent in msg: 
			if type(sent) is tuple: 
				content = str(sent[1],'utf-8')
				date,time=get_time(content)
				details.append([str(i),get_from_addrs(content),get_to_addrs(content),get_subject(content),date,time,get_mail(content),"No"])
		raw_email = msg[0][1]
		raw_email_string = raw_email.decode('utf-8')
		email_message = email.message_from_string(raw_email_string)
		for part in email_message.walk():
			if part.get_content_maintype() == 'multipart':
				continue
			if part.get('Content-Disposition') is None:
				continue	
			details[-1][-1]="Yes"
			fileName = part.get_filename()
			if bool(fileName):
				dirName = root+"\\"+get_to_addrs(content)
				if not os.path.exists(dirName):
					os.mkdir(dirName)
				os.chdir(dirName)
				filePath = os.path.join(os.getcwd(), f"{get_subject(content)+date}.pdf")
				if not os.path.isfile(filePath) :
					fp = open(filePath, 'wb')
					fp.write(part.get_payload(decode=True))
					fp.close()
		i=i+1
	print("Emails retieved.\n")
	print(10*"*")
	for each in details:
		i=0
		for every in details_dict.keys():
			details_dict[every].append(each[i])
			i=i+1
	df=pd.DataFrame.from_dict(details_dict)
	return df



	 

