from firebase import firebase
import RPi.GPIO as GPIO
import serial
import time,sys
from gtrans import translate_text, translate_html

def getInfo(mail):
	fb=firebase.FirebaseApplication("https://athena-f1dc4.firebaseio.com/")
	userdb=fb.get('/Userdatabase',None)
	mail=mail.split(".")[1]
	number=userdb[mail]["phone"]
	language=userdb[lang]["lang"]
	return number,language

def sendmessage(phno,string):
	#string=str(string,encoding="utf-8")
	convert = lambda x:"0".join([hex(ord(c))[2:].zfill(3) for c in x])
	msg="0"+convert(string)
	msg=msg.replace("0ccd0200c","0ccd")
	SERIAL_PORT="/dev/ttyAMA0"
	ser=serial.Serial(SERIAL_PORT, baudrate=9600,timeout=5)
	ser.write(str.encode("AT+CMGF=1\r"))
	time.sleep(3)
	ser.write(str.encode('AT+CSCS="HEX"\r'))
	time.sleep(10)
	ser.write(str.encode("AT+CSMP=17,167,0,8\r"))
	time.sleep(10)
	#b=str('AT+CMGS="9449191976"\r',encoding='utf-8')
	ser.write(str.encode('AT+CMGS="'+str(phno)+'"\r'))
	time.sleep(3)
	ser.write((str(msg)+chr(26)).encode())
	time.sleep(3)
	print("sentt!")


def changeLang(message,language):
	return (translate_text(message, 'en', language))


	#########################################
	#  Code to be written to interface GSM	#
	#	 module and send the message        #
	#########################################

