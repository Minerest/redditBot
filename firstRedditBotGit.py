#! python3
import smtplib
import praw
import matplotlib
import pygal
import random
from time import sleep

#email imports. Who knew it would be so complicated?
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


print("Wokring")

try:
	with open ("./usrIds.txt") as file:
		cache = file.readlines()
except:
	print("NO CACHE!")
	cache = []
print(cache)


def main():
	#Reddit object r
	r = praw.Reddit('bot1')
	lim=80
	print("MAIN")
	getComments("all",r)


def sendMeAttach(file):
	#Sends attachments without message string
	#Also file has to be in same dir as this .py program, 
	#else you have to include the file path
	msg = MIMEMultipart()
	msg['Subject'] = "Test case attachment"
	msg['From'] = "eric.diaz13@yahoo.com"
	msg["To"] = "eric.diaz13@yahoo.com"
	msg.preamble = "Preamble? WTF is this?"
	ctype, encoding = mimetypes.guess_type(file) #does not work for .ini files, but .py and .svg are ok
	maintype, subtype = ctype.split('/', 1)#Have no idea what this does

	with open(file, "rb") as f:
		msg2 = MIMEBase(maintype, subtype)
		msg2.set_payload(f.read())
	encoders.encode_base64(msg2)
	msg2.add_header("Content-Disposition", "attachment", filename=file)
	msg.attach(msg2)
	composed = msg.as_string()

	smtpObj = smtplib.SMTP("smtp.mail.yahoo.com", 587)
	smtpObj.starttls()
	smtpObj.login(email, pass)
	smtpObj.sendmail(email,email,composed)
	smtpObj.quit()

def botReply(comment):
	cussWords = ["fuck","shit","dick","bitch","cunt","crap","cock","pussy","asshole","fag","bastard","slut","douche"]
	replies = ["Bro, you really got to watch your mouth.","Did you really just cuss? Geeze, such language!","Woooowwww. Really gotta use that language, son?","Um, excuse me. Children browse this sub.","Hey, seriously. Stop that foul language right now!","Bro. You really gotta use that vocabulanary?"]
	for i in cussWords:
		if i in comment.body.lower() and not comment.id in cache and not comment.author == "botIsBalanced":
			try:
				print("Replied to the comment of: \n"+str(comment.body))
				comment.reply(rount(random.random(len(replies)-1))) #that syntax tho. Ugly af
				with open("./usrIds.txt",'w') as file:
					for item in cache:
						file.write(item+"\n")
					file.write(comment.id)
				cache.append(comment.id)
				sleep(120)
			except:
				print("DID NOT REPLY")
				sleep(120)
	else:
		print("Nothing found yet")
		sleep(5)

def getComments(s,r):
	sub = r.subreddit(s)
	b = True
	for comment in sub.stream.comments():
		try:
			botReply(comment)
		except:
			#Reddit object r
			r = praw.Reddit('bot1')
			lim=80
			botReply(comment)
	print("Sleeping!")
	sleep(20)
	print("Here we go again!")
	getComments(s)
	return


def makeChart():
	#Style and make the chart.
	conf = pygal.Config()

	conf.title_font_size = 24
	conf.label_font_size = 14
	conf.major_label_font_size = 18
	conf.truncate_label = 15
	conf.show_y_guides = False
	conf.width = 1000
	conf.human_readable = True

	chart = pygal.Line(conf)
	chart.title = "Upvoted Graph for rising posts on r/all"
	pCnt = []
	for i in range (0,90):
		pCnt.append(i)
	sCnt = []
	chart.x_labels = pCnt
	
	#This is where the meat of the code begins
	postCnt=0
	for subs in sub.rising(limit=90):
		print(subs.score)
		sCnt.append(subs.score)
	chart.add("score", sCnt)
	chart.render_to_file("redditSVG.svg")


main()