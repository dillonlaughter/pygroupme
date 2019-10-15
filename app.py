# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/


# IMPORTS
import os
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
from apscheduler.schedulers.blocking import BlockingScheduler
import groupy
from groupy.client import Client as groupmeClient
gmclient = groupmeClient.from_token('vW461v8rqQ8tya2YGf4J6cSWV5MUoVI2tuNHI60R')
for gmgroups in gmclient.groups.list():
    if gmgroups.name == 'AW log (updates only)':
        gmlog = gmgroups



#----------------from production log
from selenium import webdriver
#from selenium.webdriver.common.keys import Keys
import selenium.webdriver.chrome.options
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from datetime import timedelta,datetime
from pytz import timezone
tztime = datetime.now(timezone('America/Los_Angeles'))
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
complete_messages = ['Complete. If customer present, dial 611 for test call and give phone',    'Complete. If customer present make test call and give phone']



browser = webdriver.Chrome()



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
    denials = ['&nbsp;',' ','']

    message = request.get_json()
    msgtxt = message['text']


    if '/help' in msgtxt:
        reply('''
        /`help    ~ displays this help message
        /`start   ~ starts the bot
        /`run     ~ bot use only, used to continue app running
        /`set     ~ (in development) sets the emoji of a rep
        /`update  ~ updates the reps based on the github file
        ''')
    if '/start' in msgtxt:
        sched = BlockingScheduler()
        reply('/run')
    if '/run' in msgtxt:
        #debug777sched.start()
        dundermain()
    if '/update' in msgtxt:
        txt=wks.cell(3,2).value
        len(txt[txt.index('{')+1:txt.index('}')].split('\n'))
        gitsrc=txt[txt.index('{')+1:txt.index('}')].split('\n')
        excelarr = [['' for i in range(8)] for i in range(len(txt[txt.index('{')+1:txt.index('}')].split('\n'))-1)]
        excelarr[0] = ['1','usr_login_fail','0','0','#','pres0703','Ignore@1','2019.10.12.23.25.48']
        for i in range(1,len(txt[txt.index('{')+1:txt.index('}')].split('\n'))-1):
            excelarr[i][5] = gitsrc[i][gitsrc[i].index("'")+1:gitsrc[i].index("'",gitsrc[i].index("'")+1)]
            excelarr[i][6] = gitsrc[i][gitsrc[i].index("'",gitsrc[i].index(",")+1)+1:gitsrc[i].index("'",gitsrc[i].index("'",gitsrc[i].index(",")+1)+1)]
            excelarr[i][1] = gitsrc[i][gitsrc[i].rindex("'",0,gitsrc[i].rindex("'"))+1:gitsrc[i].rindex("'")]
            excelarr[i][0] = '1'
            excelarr[i][2] = '0'
            excelarr[i][3] = '0'
            excelarr[i][7] = '2019.10.12.23.25.48'
            excelarr[i][4] = '#'
        temp=[]
        for i in range(len(excelarr)):temp.append('~'.join(excelarr[i]))
        excelfinal='|'.join(temp)
        wks.update_cell(1,12, excelfinal)
        
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
        gmlog.post(text=name+' is now at '+str(count))
        
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
        print('#1 @indexed next person')
        
        if activation == '1':
            
            employee_count = int(arr_acti_name[1])
            print('#1 #1 @get employee count')
        

            print('#1 #1 @printing arr_ppl')
            print(arr_ppl)
            if arr_ppl[index][0] == '1':
                subroutine_in_middle(browser,arr_ppl,index)
            tztime = datetime.now(timezone('America/Los_Angeles'))
            arr_ppl[index][7] = (str(tztime.year))+'.'+('0'+str(tztime.month))[-2:]+'.'+('0'+str(tztime.day))[-2:]+'.'+('0'+str(tztime.hour))[-2:]+'.'+('0'+str(tztime.minute))[-2:]+'.'+('0'+str(tztime.second))[-2:]
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
        print('#2 @after browser count?')
##        s=re.sub(r'[^\x00-\x7f]',r'', your-non-ascii-string)
##        print(arr_ppl)
        send_data(arr_ppl)
##        time.sleep(5)
        print('#3 @after sent arr_ppl to sheets')
##        time.sleep(5)
        arr_ppl = get_data()
##        print(arr_ppl)
        print('#4 @get new data from sheets')
        for person in range(len(arr_ppl)):
            if str(arr_ppl[person][2]) != str(arr_ppl[person][3]):
                arr_ppl[person][3] = arr_ppl[person][2]
                #wks.update_cell(employee_number+2,6,complete_count)
                print((arr_ppl[person][1],arr_ppl[person][2]))
                time.sleep(1)
                send_to_groupme(arr_ppl[person][1],arr_ppl[person][2])
        print('#5 @sending arr_ppl (new) to sheets')
##        print(arr_ppl)
        send_data(arr_ppl)
    print('time: ',time.time()-a)
    time.sleep((25-(time.time()-a)))
    #reply('/run')
    return 

def subroutine_in_middle(browser,arr_ppl,index):
    complete_messages = ['Complete. If customer present, dial 611 for test call and give phone','Complete. If customer present make test call and give phone']
    denials = ['&nbsp;',' ','']
    print('#1 #1 #0 @prepare for fail')
    if 1==1: #prepare for fail turn from "try:"
        print('#1 #1 #1 @before browser init')
        #browser = webdriver.Chrome()
        browser.get('https://solixlifeline.com')
        ##
        print('#1 #1 #1 @after browser init')
        print('#1 #1 #1 @##### Went to solix for ' + arr_ppl[index][1] + ' #####')
        #time.sleep(3)#-#
        browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_UserName_text').send_keys(arr_ppl[index][5])
        browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_Password_text').send_keys(arr_ppl[index][6])
        #time.sleep(3)#-#
        browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_LoginButton').click()
        time.sleep(3)#-#
        try:
            if browser.find_element_by_id('ctl00_GeneralContentPlaceHolder_Login1_lblFailureInfo').get_attribute('innerText') != "":
                arr_ppl[index][0] = '0'
                print('#1 #1 #1 #1 @login failure')
                gmlog.post(text='Login failed for '+arr_ppl[index][1]+'. Removing them from log.')
                return
        except:
            debug_username = browser.find_element_by_id('ctl00_lblUserName').get_attribute('innerText')
            print('debug_username == ' + debug_username)
        ################ set function to curretn date

        browser.find_element_by_id('ctl00_MainPlaceHolder_radtbDate_dateInput_text').send_keys(('0'+str(tztime.month))[-2:]+'/'+('0'+str(tztime.day))[-2:]+'/'+('0'+str(tztime.year))[-2:])
        #time.sleep(3)#-#
        browser.find_element_by_id('ctl00_MainPlaceHolder_btnSearch').click()
        time.sleep(5)#-#
        print('#1 #1 #1 @getting debug_date')
        debug_date = browser.find_element_by_id('ctl00_MainPlaceHolder_radtbDate_dateInput_text').get_attribute('value')
        complete_count = 0
        print('#1 #1 #1 @debug_date == ' + debug_date)
        ind=0
        while True:
            try:
#                 element_01 = browser.find_element_by_id('ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__0')
#                 text = browser.find_element_by_id('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__0"]/td[7]')
                print('is table there?')
                table = browser.find_element_by_id('ctl00_MainPlaceHolder_radgrdSearchRetailCustomers')
                print('table is there')
#                 text = browser.find_element_by_id('ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__0')
#                 print(text)
                
                text = browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__'+str(ind)+'"]/td[7]').get_attribute('innerText')
                print('text = '+text)
                #text = browser.find_element_by_css_selector('#ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__'+str(ind)+' > td:nth-child(7)').get_attribute('innerText')
                denial = browser.find_element_by_xpath('//*[@id="ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__'+str(ind)+'"]/td[8]').get_attribute('innerText')
                print('denial = "'+denial+'"')
                #denial = browser.find_element_by_css_selector('#ctl00_MainPlaceHolder_radgrdSearchRetailCustomers_ctl00__'+str(ind)+' > td:nth-child(8)').get_attribute('innerText')
                print('print both')
                print(len(denial))
                print(text in complete_messages,denial in denials)
                if text in complete_messages and len(denial)<3:
                    print('add 1 to complete_count')
                    complete_count+=1
                ind+=1
            except:
                print('search table for complete broke')
                break
#         complete_count=3
        print('complete count == ' + str(complete_count))
        arr_ppl[index][2] = complete_count
#                 except:
#                     print('#1 #1 #2 @break 1')

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


@sched.scheduled_job('interval', seconds=25)
def timed_job():
    print('#######################################################################################################################')
    return

