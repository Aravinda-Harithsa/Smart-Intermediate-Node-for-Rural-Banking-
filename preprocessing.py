import pandas as pd 
from numpy import nan,random
import os
from tika import parser
from firebase import firebase

def preprocessing(df):
	print("preprocessing....")

	bank_dict = {'mail': ['athena.bank.node@gmail.com','athena.bank2.node@gmail.com'],'name':['bank','bank2']}
	govt_dict = {'mail': ['athena.govt.node@gmail.com','athena.govt2.node@gmail.com'],'name':['govt','govt2']}

	def getAttachmentData(dst,sub,date):
		#path=f'C:\\Users\\Adithya\\Documents\\GitHub\\Athena\\Attachments\\{dst}\\{sub+date}.pdf'
		#path=f'C:\\Users\\Dexter\\Documents\\Projects\\SIH\\Athena\\Attachments\\{dst}\\{sub+date}.pdf'
		path=f'\\home\\pi\\Desktop\\Athena\\Attachments\\{dst}\\{sub+date}.pdf'

		raw = parser.from_file(path)
		data = str(raw['content']).replace("\n\n","\n")

		info = [0,0,0,0]
		for i in range(len(info)):
			indexstart =  data.find("₹")
			info[i] = data[indexstart:]
			indexend = info[i].find("\n")
			info[i] = info[i][0:indexend]
			data = data[indexstart+1:]
		msg = f'Opening Balance = {info[0]} Total Deposit = {info[1]} Total Withdrawal = {info[2]} Closing balance = {info[3]}'
		return msg


	def getRefinedData(src,msg,date,time):
		if src in bank_dict['mail']:
			bname = bank_dict['name'][bank_dict['mail'].index(src)]
			indexstart = msg.find("Rs ")
			amt = msg[indexstart+3: len(msg)] 
			indexend = amt.find(" ")
			amt = amt[0:indexend]
			if 'towards' in msg:
				indexstart = msg.find("towards")
				receiver = msg[indexstart+8: len(msg)] 
				indexend = receiver.find("on")
				receiver = receiver[0:indexend]
				msg = f'{bname}: Payment of Rs.{amt} to {receiver} on {date} at {time}'
				return msg
			elif 'debited' in msg:
				Indexstart = msg.find("Transfer")
				r_id = msg[indexstart+12: indexstart+39] 
				msg = f'{bname}: Rs.{amt} debited with Transfer ID:{rid} on {date} at {time}'
				return msg
			elif 'credited' in msg:
				Indexstart = msg.find("Transfer")
				r_id = msg[indexstart+12: indexstart+39] 
				msg = f'{bname}: Rs.{amt} credited with Transfer ID:{rid} on {date} at {time}'
				return msg
			else:
				return msg
		if src in govt_dict['mail']:
			gname = govt_dict['name'][govt_dict['mail'].index(src)]
			indexstart = msg.find(",")
			indexend = msg.find(".")
			info = msg[indexstart: indexend]
			msg = f'{gname}: {info}'
		return msg

	i=0
	for uid,src,dest,sub,date,time,msg,atch in df.itertuples(index=False):
		if atch=='Yes':
			msg = getAttachmentData(dest,sub,date)
			df['Content'][i] = msg
			i=i+1
			continue
		if len(msg)<=160:
			df['Content'][i] = src+ ": "+ msg
			i=i+1
			continue
		msg = getRefinedData(src,msg,date,time)
		df['Content'][i] = msg
		i=i+1
		
	print("File updated\n")
	print(df.Content)

	fb=firebase.FirebaseApplication("https://athena-f1dc4.firebaseio.com/")
	result=fb.get('/Maildatabase',None)

	curr_len = len(result.keys())-1 # SEND LENGTH OF FIREBSASE DATABASE HERE
	new_len=len(df)
	#df = df.tail(new_len-curr_len)

	diff = new_len-curr_len
	new=list(range(diff))
	uid = [each+curr_len for each in new]
	df.drop(index =list(range(curr_len)),inplace=True)
	df=df.reset_index(drop=True)
	#print(df) #df is the dataframe of new mails to be uploaded to firebase.


	#print(df['UID'][df.index[-1]])
	for i in range(len(df["UID"])):
		var=int(df['UID'][i])
		path="/Maildatabase"+"/"+str(var)
		fb.put(path,'From',df['From'][i])
		fb.put(path,'To',df['To'][i])
		fb.put(path,'Subject',df['Subject'][i])
		fb.put(path,'Date',df['Date'][i])
		fb.put(path,'Time',df['Time'][i])
		fb.put(path,'Content',df['Content'][i])
		fb.put(path,'Attachment',df['Attachment'][i])
		fb.put(path,'UID',df['UID'][i])

	print(10*"*")
	print("\nReceived "+str(len(df))+" new mails")
	print("Firebase Updated!")
	return df