# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours//


# IMPORTS
import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
from apscheduler.schedulers.blocking import BlockingScheduler



#----------------from production log
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import selenium.webdriver.chrome.options
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import timedelta
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('Hurley Production-54b7dbd26519.json',scope)
GOOGLE_CHROME_BIN = '/app/.apt/usr/bin/google-chrome'
CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = GOOGLE_CHROME_BIN
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')

gc = gspread.authorize(credentials)
wks = gc.open('Hurley Enterprises Production Log').sheet1
complete_messages = ['Complete. If customer present, dial 611 for test call and give phone','Complete. If customer present make test call and give phone']



browser = webdriver.Chrome()

sched = BlockingScheduler()

'''

######### RID SELF OF XPATH #########

'''




app = Flask(__name__)
bot_id = "0e32f0e6e58f4d035d908b18a1"

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])


def webhook():
    # 'message' is an object that represents a single GroupMe message.
    
    # TODO: Your bot's logic here


    gc = gspread.authorize(credentials)
    wks = gc.open('Hurley Enterprises Production Log').sheet1
    complete_messages = ['Complete. If customer present, dial 611 for test call and give phone','Complete. If customer present make test call and give phone']

    message = request.get_json()
    msgtxt = message['text']


    
    if '/run' in msgtxt:
        sched.start()
#         dundermain()
    if '/set ' in msgtxt:
        msgparts = msgtxt.split(' ')
        emoji = msgparts[-1]
        fullname = ' '.join(msgparts[1:len(msgparts)-1])
        print('##'+fullname+'##')
        temp = wks.cell(1,10).value
        arr_ppl = temp.split('|')
        for i in range(len(arr_ppl)):
            arr_ppl[i] = arr_ppl[i].split('~')
        hlength = '0'
        # TODO: update sheets with emoji
        hcount = int(wks.cell(2,2).value)
        for hname in range(hcount):
            if arr_ppl[hname][1] == fullname:
                arr_ppl[hname][4] = emoji
                hlength = hname

        arr_ppl = [[str(arr_ppl[i][j]) for j in range(len(arr_ppl[i]))] for i in range(len(arr_ppl))]
        temp = '|'.join(['~'.join(x) for x in arr_ppl])
        #print(temp)
        wks.update_cell(1,11, temp)
        reply('Emoji of '+fullname+ ' set to '+emoji)
        
        

    return "ok", 200

################################################################################

# Send a message in the groupchat
def reply(msg):
    print('$#$# Reply ' + str(msg))
    url = 'https://api.groupme.com/v3/bots/post'
    data = {
        'bot_id'        : bot_id,
        'text'            : msg
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()

# Send a message with an image attached in the groupchat
def reply_with_image(msg, imgURL):
    url = 'https://api.groupme.com/v3/bots/post'
    urlOnGroupMeService = upload_image_to_groupme(imgURL)
    data = {
        'bot_id'        : bot_id,
        'text'            : msg,
        'picture_url'        : urlOnGroupMeService
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

def send_to_groupme(name,count):
##    for gmmessage in gmlog.messages.list_all():
##        print(gmmessage.text)
    if int(count) != 0:
        print(name+ ' gm '+str(count))
        reply(name+' is now at '+str(count))
        
def dundermain():
    a=time.time()
##    print('##### before browser startup #####')
##    browser = webdriver.Chrome()#executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
##    print('##### after browser startup #####')


    if 1==0:
        try:
            print('going to solix')
            browser.get('https://solixlifeline.com')
            print('Printing header')
            print(browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_lblHeader').get_attribute('innerText'))
            print('Printed header')
            browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_UserName_text').send_keys('pres0704')
            browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_Password_text').send_keys('Laughter@2')
            print('P entered info')
            print('P sleeping 1 second')
            time.sleep(1)
            print('E sleeping 1 second')
            print(browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_UserName_text').get_attribute('value'))
            print(browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_Password_text').get_attribute('value'))
            print('E entered info')
            browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_LoginButton').click()
            print('P sleeping 2 seconds')
            time.sleep(2)
            print('E sleeping 2 seconds')
            print('P new Header')
            print(browser.find_element_by_id('ctl00_lblModuleheading').get_attribute('innerText'))
            print('E new header')
            print('P set date')
            browser.find_element_by_id('ctl00_MainPlaceHolder_radtbDate_dateInput_text').send_keys('9/6/19')
            print(browser.find_element_by_id('ctl00_MainPlaceHolder_radtbDate_dateInput_text').get_attribute('value'))
            print('E set date')
            print('P search')
            browser.find_element_by_id('ctl00_MainPlaceHolder_btnSearch').click()
            print('E search')
            print('P sleeping 3 seconds')
            time.sleep(3)
            print('E sleeping 3 seconds')
            print('P app count')
            app_count = int(browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00"]/tbody').get_attribute('childElementCount'))
            print(str(app_count))
            print('E app count')
            print('P get complete')
            complete_count = 0
            for each_app in range(int(browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00"]/tbody').get_attribute('childElementCount'))):
                if(browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__'+str(each_app)+'"]/td[7]').get_attribute('innerText') in complete_messages):
                    complete_count = int(complete_count) + 1
            print('E get complete')
            print('P complete count')
            print(complete_count)
            print('E complete count')
            
            print('Next Person')
            print('Next Person')
            print('Next Person')
            
            print('Going to solix')
            browser.get('https://solixlifeline.com')
            print('Printing header')
            print(browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_lblHeader').get_attribute('innerText'))
            print('Printed header')
            browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_UserName_text').send_keys('pres0704')
            browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_Password_text').send_keys('Laughter@2')
            print('P entered info')
            print('P sleeping 1 second')
            time.sleep(1)
            print('E sleeping 1 second')
            print(browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_UserName_text').get_attribute('value'))
            print(browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_Password_text').get_attribute('value'))
            print('E entered info')
            browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_LoginButton').click()
            print('P sleeping 2 seconds')
            time.sleep(2)
            print('E sleeping 2 seconds')
            print('P new Header')
            print(browser.find_element_by_id('ctl00_lblModuleheading').get_attribute('innerText'))
            print('E new header')
            print('P set date')
            browser.find_element_by_id('ctl00_MainPlaceHolder_radtbDate_dateInput_text').send_keys('9/6/19')
            print(browser.find_element_by_id('ctl00_MainPlaceHolder_radtbDate_dateInput_text').get_attribute('value'))
            print('E set date')
            print('P search')
            browser.find_element_by_id('ctl00_MainPlaceHolder_btnSearch').click()
            print('E search')
            print('P sleeping 3 seconds')
            time.sleep(3)
            print('E sleeping 3 seconds')
            print('P app count')
            app_count = int(browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00"]/tbody').get_attribute('childElementCount'))
            print(str(app_count))
            print('E app count')
            print('P get complete')
            complete_count = 0
            for each_app in range(int(browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00"]/tbody').get_attribute('childElementCount'))):
                if(browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__'+str(each_app)+'"]/td[7]').get_attribute('innerText') in complete_messages):
                    if(browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__'+str(each_app)+'"]/td[8]').get_attribute('innerText') == ""):
                        complete_count = int(complete_count) + 1
            print('E get complete')
            print('P complete count')
            print(complete_count)
            print('E complete count')
            
            
            print('P nat quit')
            browser.quit()
            print('E nat quit')
        except:
            print('P unnat quit')
            browser.quit()
            print('E unnat quit')

    temp = wks.cell(3,1).value
    arr_acti_name = temp.split('|')
    quitvar = 0    
    if 1==1:
        #reply('test')
        #try:
        arr_ppl = get_data()
        
##        browser = webdriver.Chrome()
        activation = arr_acti_name[0]
        #wks.update_cell(2,1,'1')
        index = next_person(arr_ppl)
        print(1)
        
        if activation == '1':
            
            employee_count = int(arr_acti_name[1])
            print(3)
        

            print(4)
            print(arr_ppl)
            if arr_ppl[index][0] == '1':
                try:
                    print(2)
                    #browser = webdriver.Chrome()
                    browser.get('https://solixlifeline.com')
                    ##
                    print(2)
                    print('##### Went to solix for ' + arr_ppl[index][1] + ' #####')
                    #time.sleep(3)#-#
                    browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_UserName_text').send_keys(arr_ppl[index][5])
                    browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_Password_text').send_keys(arr_ppl[index][6])
                    #time.sleep(3)#-#
                    browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_LoginButton').click()
                    time.sleep(3)#-#
                    try:
                        if browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_lblFailureInfo').get_attribute('innerText') != "":
                            arr_ppl[index][0] = '0'
                    except:
                        retd = 5
                    ################ set function to curretn date
                    browser.find_element_by_id('ctl00_MainPlaceHolder_radtbDate_dateInput_text').send_keys('9/6/19')
                    #time.sleep(3)#-#
                    browser.find_element_by_id('ctl00_MainPlaceHolder_btnSearch').click()
                    time.sleep(2.5)#-#
                    complete_count = 0
                    ind=0
                    while True:
                        try:   
                            text = browser.find_element_by_css_selector('#ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__'+str(ind)+' > td:nth-child(7)').get_attribute('innerText')
                            denial = browser.find_element_by_css_selector('#ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__'+str(ind)+' > td:nth-child(8)').get_attribute('innerText')
                            if text in complete_messages and denial == '':
                                complete_count+=1
                            ind+=1
                        except:
                            break
                    print(complete_count)
                    arr_ppl[index][2] = complete_count
                except:
                    oid=0
            arr_ppl[index][7] = ('0'+str(time.localtime().tm_hour))[-2:]+'.'+('0'+str(time.localtime().tm_min))[-2:]+'.'+('0'+str(time.localtime().tm_sec))[-2:]
                #wks.update_cell(employee_number+2,5,complete_count)
                #employee_previous = wks.cell(employee_number+2,6).value
                #print(arr_ppl[employee_number][3],arr_ppl[employee_number][2])
                #print('type: '+str(type(arr_ppl[employee_number][3]))+' : '+str(arr_ppl[employee_number][3])+' :type: '+str(type(arr_ppl[employee_number][2]))+' : '+str(arr_ppl[employee_number][2]))
                #print('##### count is at '+str(complete_count)+' #####')
##                            try:
##                                browser.quir()
##                            except:
##                                rpeo = 5
##            except:
##                    rpeo = 6
##            
##            else:
##                time.sleep(10)
##        except:
##            oisdjf=0
    ##t1_ = time.process_time()
    ##print(t1_-t1_s)
        print(5)
##        s=re.sub(r'[^\x00-\x7f]',r'', your-non-ascii-string)
##        print(arr_ppl)
        send_data(arr_ppl)
##        time.sleep(5)
        print(6)
##        time.sleep(5)
        arr_ppl = get_data()
##        print(arr_ppl)
        print(8)
        for person in range(len(arr_ppl)):
            if str(arr_ppl[person][2]) != str(arr_ppl[person][3]):
                arr_ppl[person][3] = arr_ppl[person][2]
                #wks.update_cell(employee_number+2,6,complete_count)
                print((arr_ppl[person][1],arr_ppl[person][2]))
                time.sleep(1)
                send_to_groupme(arr_ppl[person][1],arr_ppl[person][2])
        print(7)
##        print(arr_ppl)
        send_data(arr_ppl)
    print('time: ',time.time()-a)

def next_person(data):
    ### sorts arr_ppl to get the smallest date, returns the arr_ppl[index]
    ### index is smallest date
    sorted_list = sorted(data, key=lambda x:x[7])
    return data.index(sorted_list[0])

def get_data():
    temp = wks.cell(1,11).value
##    print(temp)
##    print(temp.count('|'))
    arr_ppl = temp.split('|')
##    print(len(arr_ppl))
    for i in range(len(arr_ppl)):
        arr_ppl[i] = arr_ppl[i].split('~')
##    print(arr_ppl,'temp')
##    print(len(arr_ppl))
    return arr_ppl

def send_data(arr_ppl):
#    print(arr_ppl)
    arr_ppl = [[str(arr_ppl[i][j]) for j in range(len(arr_ppl[i]))] for i in range(len(arr_ppl))]
    temp = '|'.join(['~'.join(x) for x in arr_ppl])
    wks.update_cell(1,12, temp)

    return


@sched.scheduled_job('interval', seconds=30)
def timed_job():
    dundermain()

