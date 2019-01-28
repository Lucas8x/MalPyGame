from lxml import html
import requests
# import myanimelist.session
import re
import os
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pickle
import locale
locale.setlocale(locale.LC_ALL, '')

options = Options()
options.headless = False
firefox_capabilities = DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True
driver = webdriver.Firefox(options=options, executable_path='./geckodriver.exe', capabilities=firefox_capabilities)

#chrome_options = Options()
#chrome_options.add_argument("user-data-dir=selenium")
#driver = webdriver.Chrome(chrome_options=chrome_options)

#user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
login_url = 'https://myanimelist.net/login.php'
thread = 'https://myanimelist.net/forum/?topicid=1755755&goto=lastpost'

if not (os.path.exists('./cookies.pkl')):
  driver.get(login_url)
  username = ""
  password = ""
  # driver.find_element_by_css_selector('body > div.root > div > div.modal-wrapper > div > button').click()
  # driver.find_element_by_xpath('//button data-v-4e7046d6')
  # driver.find_element_by_xpath('//button[contains("OK")')
  driver.find_element_by_class_name("text").click()
  ActionChains(driver).send_keys(Keys.TAB).perform()
  ActionChains(driver).send_keys(Keys.TAB).perform()
  ActionChains(driver).send_keys(Keys.ENTER).perform()
  driver.find_element_by_id("loginUserName").send_keys(username)
  driver.find_element_by_id("login-password").send_keys(password)
  ActionChains(driver).send_keys(Keys.ENTER).perform()
  time.sleep(5)
  pickle.dump(driver.get_cookies(), open("./cookies.pkl", "wb"))

driver.get(thread)
for cookie in pickle.load(open("./cookies.pkl", "rb")):
  driver.add_cookie(cookie)

def check():
  driver.get(thread)
  driver.refresh()
  tree = html.fromstring(driver.page_source)
  #users = tree.xpath('//*[@style="padding-bottom: 2px;"]/a/strong/text()')
  users = tree.xpath('//*[contains(@id,"messageuser")]/a/strong/text()')
  #post = tree.xpath('//*[@class="clearfix"]/text()')
  post = tree.xpath('//*[contains(@id,"message")]/text()')

  print("Users: ", *users)
  print("Last User: ", str(users[-1]))
  print("\nPosts: ", *post)

  #filt = [ x for x in post if x.isdigit() ]
  #filt = ''.join(filter(lambda x: x in '0123456789', str(post)))
  #filt = [filt[i:i + 3] for i in range(0, len(filt), 3)]
  filt = [re.sub('[^0-9]','', x) for x in post]

  print("Filter:", *filt)
  print("Last Post: ", filt[-1])
  try: calc = int(filt[-1])-1
  except TypeError: return
  print("Calculation:", calc)

  lastuser = str(users[-1])
  print("\nChecking if last user is you...")
  if (lastuser == ""):
      print("Yes, it's you", lastuser, "nothing will happen")
  else:
      print("Itsn't, trying post...\n")
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      driver.find_element_by_id('showQuickReply').click()
      driver.find_element_by_id("messageText").send_keys(calc)
      driver.find_element_by_id('postReply').click()

if __name__ == "__main__":
  repeat = True
  while repeat == True:
    check()
    time.sleep(15)