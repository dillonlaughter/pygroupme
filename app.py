# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours//


# IMPORTS
import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request

#-----------------from production log
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.chrome.options
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from groupy.client import Client as groupmeClient
gmclient = groupmeClient.from_token('mEd2vWApuNMkbnSAaHHddzoKHLwpecExfZR0E9ql')
for gmgroups in gmclient.groups.list():
	if gmgroups.name == 'AW Production Log':
     		gmlog = gmgroups
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']



credentials = ServiceAccountCredentials.from_json_keyfile_name('Hurley Production-54b7dbd26519.json',scope)
GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = GOOGLE_CHROME_BIN
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)


gc = gspread.authorize(credentials)
wks = gc.open('Hurley Enterprises Production Log').sheet1
complete_messages = ['Complete. If customer present, dial 611 for test call and give phone','Complete. If customer present make test call and give phone']
def send_to_groupme(name,count):
##    for gmmessage in gmlog.messages.list_all():
##        print(gmmessage.text)
	if count != 0:
		gmlog.post(text=name+' is now at '+str(count))
	
if 1==1:
	activation = wks.cell(2,1).value
	#wks.update_cell(2,1,'1'
	if activation == '1':
		employee_count = int(wks.cell(2,3).value)
		for employee_number in range(3):#employee_count):
			browser.get('https://solixlifeline.com')
			time.sleep(1)#-#
			browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_UserName_text').send_keys(wks.cell(employee_number+2,8).value)
			browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_Password_text').send_keys(wks.cell(employee_number+2,9).value)
			time.sleep(1)#-#
			browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_LoginButton').click()
			time.sleep(3)#-#
			browser.find_element_by_id('ctl00_MainPlaceHolder_radtbDate_dateInput_text').send_keys('8/23/19')
			time.sleep(1)#-#
			browser.find_element_by_id('ctl00_MainPlaceHolder_btnSearch').click()
			time.sleep(5)#-#
			complete_count = 0
			app_count = int(browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00"]/tbody').get_attribute('childElementCount'))
			if app_count > 2:
				for each_app in range(int(browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00"]/tbody').get_attribute('childElementCount'))):
					if(browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__'+str(each_app)+'"]/td[7]').get_attribute('innerText') in complete_messages):
						complete_count +=1
	    ##        complete_count = 1
			wks.update_cell(employee_number+2,5,complete_count)
			employee_previous = wks.cell(employee_number+2,6).value
			if employee_previous != wks.cell(employee_number+2,5).value:
				wks.update_cell(employee_number+2,6,complete_count)
				send_to_groupme(wks.cell(employee_number+2,4).value,complete_count)
browser.quit()
		
		
		
		
		









app = Flask(__name__)
bot_id = "3f468516f8449e3c3482999b9b"

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])
def webhook():
	# 'message' is an object that represents a single GroupMe message.
	message = request.get_json()
	msgtxt = message['text']
	# TODO: Your bot's logic here
	if '/set ' in msgtxt:
		msgparts = msgtxt.split(' ')
		emoji = msgparts[-1]
		fullname = ' '.join(msgparts[1:len(msgparts)-1])
		
		# TODO: update sheets with emoji
		
		reply('Emoji of '+fullname+ ' set to '+emoji)
		

	return "ok", 200

################################################################################

# Send a message in the groupchat
def reply(msg):
	url = 'https://api.groupme.com/v3/bots/post'
	data = {
		'bot_id'		: bot_id,
		'text'			: msg
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()

# Send a message with an image attached in the groupchat
def reply_with_image(msg, imgURL):
	url = 'https://api.groupme.com/v3/bots/post'
	urlOnGroupMeService = upload_image_to_groupme(imgURL)
	data = {
		'bot_id'		: bot_id,
		'text'			: msg,
		'picture_url'		: urlOnGroupMeService
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()
	
# Uploads image to GroupMe's services and returns the new URL
def upload_image_to_groupme(imgURL):
	imgRequest = requests.get(imgURL, stream=True)
	filename = 'temp.png'
	postImage = None
	if imgRequest.status_code == 200:
		# Save Image
		with open(filename, 'wb') as image:
			for chunk in imgRequest:
				image.write(chunk)
		# Send Image
		headers = {'content-type': 'application/json'}
		url = 'https://image.groupme.com/pictures'
		files = {'file': open(filename, 'rb')}
		payload = {'access_token': 'eo7JS8SGD49rKodcvUHPyFRnSWH1IVeZyOqUMrxU'}
		r = requests.post(url, files=files, params=payload)
		imageurl = r.json()['payload']['url']
		os.remove(filename)
		return imageurl

# Checks whether the message sender is a bot
def sender_is_bot(message):
	return message['sender_type'] == "bot"
