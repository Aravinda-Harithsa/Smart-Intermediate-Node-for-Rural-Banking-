string ="ಬ್ಯಾಂಕ್: ಎನ್‌ಎಸ್‌ಡಿಎಲ್‌ಗೆ 2020-05-25ರಂದು 15:22:13 ಕ್ಕೆ ರೂ .54,667 ಪಾವತಿ"
convert = lambda x:"".join([str(hex(ord(c))[2:].zfill(4)) for c in x])
msg = convert(string)
msg2 = msg.replace("0ccd200c","0ccd")
print(msg2=="0cac0ccd0caf0cbe0c820c950ccd003a00200c8e0ca80ccd0c8e0cb80ccd0ca10cbf0c8e0cb20ccd0c970cc600200032003000320030002d00300035002d003200350cb00c820ca60cc1002000310035003a00320032003a0031003300200c950ccd0c950cc600200cb00cc20020002e00350034002c00360036003700200caa0cbe0cb50ca40cbf")