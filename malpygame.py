from lxml import html
import requests
from requests import session

# import myanimelist.session
import re
#from robobrowser import RoboBrowser

# import urllib, urllib2, cookielib

#from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

# import schedule
import time
# import threading
# import sched, time

# import string
# from BeautifulSoup import  BeautifulSoup

import locale
locale.setlocale(locale.LC_ALL, '')

topic = requests.get('https://myanimelist.net/forum/?topicid=1731980&goto=lastpost')
tree = html.fromstring(topic.content)
users = tree.xpath('//*[@style="padding-bottom: 2px;"]/a/strong/text()')
# post = tree.xpath('//*[@class="clearfix"]/text()')
post = tree.xpath('//*[contains(@id,"message")]/text()')

print("\nUsers: ", users)
print("\nLast User: ", users[-1])
lastuser = users[-1] = str(users[-1])
print("\nPosts: ", post)

# melhorar o filtro #
#filt = [ x for x in post if x.isdigit() ]
filt = ''.join(filter(lambda x: x in '0123456789', str(post)))  #deixa apenas os números
filt = [filt[i:i + 3] for i in range(0, len(filt), 3)]  #organiza em grupos de 3

print("\nFilter:", filt)
print("\nLast Post: ", filt[-1])
calc = filt[-1] = int(filt[-1])-1 #-1 to Female +1 to Male
print("Calculation:", calc)

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

# login_url = 'https://myanimelist.net/login.php?from=%2F'
login_url = 'https://myanimelist.net/login.php'

payload = {'user_name': '',
           'password': '',
           'cookie': '1',
           'sublogin': 'Login',
           'submit': '1',
           'csrf_token': ''}

action_url = 'https://myanimelist.net/forum/?action=message&topic_id=1731980'

print("\nChecking if last user is you...")
if (lastuser == 'username'):
    print("Yes, it's you", lastuser, "nothing will happen")
else:
    print("Itsn't, trying post...\n")
    r = requests.Session()
    r = requests.get("https://myanimelist.net/login.php", data=payload , headers={'User-Agent': user_agent})
    mycookies = r.cookies.get_dict()
    print("GET Response: ", r.status_code, r.reason)
    print("Cookies: ", mycookies)

    calc = str(calc) #transforma inteiro em string

    #

    # msg = {'action': 'message', 'topic_id': '1731980', 'csrf_token': '', 'msg_text': calc , 'submit': 'Submit'}
    #msg = {'msg_text': calc, 'submit': 'Submit', 'board_id':'','subboard_id':'', 'csrf_token': ''}
    msg = {'msg_text': calc}

    msgT2 = {'topicId': '1731980', 'messageText': calc, 'csrf_token': ''}
    quickReply = {'messageText': calc}

    getactionpag = {'action': 'message','topic_id': '1731980'}
    time.sleep(1)

    # r = requests.post('https://myanimelist.net/forum/?topicid=1731980', data=quickReply)
    # r = requests.post('https://myanimelist.net/includes/ajax.inc.php?t=82', data=quickReply)

    #r = requests.get("https://myanimelist.net/forum/?action=message&topic_id=1731980", data=getactionpag , cookies=mycookies , headers={'User-Agent': user_agent})
    r = requests.post("https://myanimelist.net/forum/?action=message&topic_id=1731980", data=msg , cookies=mycookies , headers={'User-Agent': user_agent})

    #r = requests.post("https://myanimelist.net/includes/ajax.inc.php?t=82", data=msgT2)

    print("POST Response:", r.status_code, r.reason)

# print last post again
# topic = requests.get('https://myanimelist.net/forum/?topicid=1731980&goto=lastpost')
# tree = html.fromstring(topic.content)
# post = tree.xpath('//*[contains(@id,"message")]/text()')
# print("\nLast Post: ", post[-1])

# cookie to check = is_logged_in = 1






# dump things

# session = myanimelist.session.Session(username="username", password="mal_password")
# session.login()

# session_requests = requests.session()
# result = session_requests.get(login_url)
# payload = {'user_name': 'myusername','password': 'mypassword'}
# result = session_requests.post(login_url, data=payload, headers={'User-Agent': user_agent})
# print ("\n", result)