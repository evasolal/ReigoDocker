import unittest
import sys, time

import numpy as np
import scipy.interpolate as si

from datetime import datetime
from time import sleep, time
from random import uniform, randint

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException
#from selenium.webdriver.chrome.chrome_binary import ChromeBinary
import numpy as np
import re
import os

#index = int(uniform(0, len(PROXY)))
MIN_RAND        = 0.64
MAX_RAND        = 1.27
LONG_MIN_RAND   = 4.78
LONG_MAX_RAND = 11.1
PREFIX = 'https://www.zillow.com/homes/'
headless = False
options = None
profile = None
capabilities = None
number = None

#Set Chrome Options
options = webdriver.ChromeOptions()
options.headless = False

#Set Chrome Profile
#profile = webdriver.ChromeProfile()
#profile._install_extension("buster_captcha_solver_for_humans-0.7.2-an+fx.xpi", unpack=False)
#profile.set_preference("security.fileuri.strict_origin_policy", False)
#profile.update_preferences()

#Set Capabilities
capabilities = webdriver.DesiredCapabilities.CHROME
capabilities['marionette']=True
options.setcapabilities = capabilities
driver = webdriver.Chrome('chromedriver',options = options)

def log(s,t=None):
            now = datetime.now()
            if t == None :
                    t = "Main"
            print ("%s :: %s -> %s " % (str(now), t, s))

    # Use time.sleep for waiting and uniform for randomizing
def wait_between(self, a, b):
    rand=uniform(a, b)
    sleep(rand)

# Using B-spline for simulate humane like mouse movments
def human_like_mouse_move(self, action, start_element):
    points = [[6, 2], [3, 2],[0, 0], [0, 2]];
    points = np.array(points)
    x = points[:,0]
    y = points[:,1]

    t = range(len(points))
    ipl_t = np.linspace(0.0, len(points) - 1, 100)

    x_tup = si.splrep(t, x, k=1)
    y_tup = si.splrep(t, y, k=1)

    x_list = list(x_tup)
    xl = x.tolist()
    x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

    y_list = list(y_tup)
    yl = y.tolist()
    y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

    x_i = si.splev(ipl_t, x_list)
    y_i = si.splev(ipl_t, y_list)

    startElement = start_element

    action.move_to_element(startElement);
    action.perform();

    c = 5 # change it for more move
    i = 0
    for mouse_x, mouse_y in zip(x_i, y_i):
        action.move_by_offset(mouse_x,mouse_y);
        action.perform();
        self.log("Move mouse to, %s ,%s" % (mouse_x, mouse_y))
        i += 1
        if i == c:
            break;

def do_captcha(self,driver):
    driver.switch_to.default_content()
    self.log("Switch to new frame")
    iframes = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])

    self.log("Wait for recaptcha-anchor")
    check_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID ,"recaptcha-anchor")))

    self.log("Wait")
    self.wait_between(MIN_RAND, MAX_RAND)

    action =  ActionChains(driver);
    self.human_like_mouse_move(action, check_box)

    self.log("Click")
    check_box.click()

    self.log("Wait")
    self.wait_between(MIN_RAND, MAX_RAND)

    self.log("Mouse movements")
    action =  ActionChains(driver);
    self.human_like_mouse_move(action, check_box)

    self.log("Switch Frame")
    driver.switch_to.default_content()
    iframes = driver.find_elements_by_tag_name("iframe")
    driver.switch_to.frame(iframes[2])

    self.log("Wait")
    self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

    self.log("Find solver button")
    capt_btn = WebDriverWait(driver, 50).until(
                EC.element_to_be_clickable((By.XPATH ,'//button[@id="solver-button"]'))
                )

    self.log("Wait")
    self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

    self.log("Click")
    capt_btn.click()

    self.log("Wait")
    self.wait_between(LONG_MIN_RAND, LONG_MAX_RAND)

    try:
        self.log("Alert exists")
        alert_handler = WebDriverWait(driver, 20).until(
                EC.alert_is_present()
                )
        alert = driver.switch_to.alert
        self.log("Wait before accept alert")
        self.wait_between(MIN_RAND, MAX_RAND)

        alert.accept()

        self.wait_between(MIN_RAND, MAX_RAND)
        self.log("Alert accepted, retry captcha solver")

        self.do_captcha(driver)
    except:
        self.log("No alert")


    self.log("Wait")
    driver.implicitly_wait(5)
    self.log("Switch")
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])




#Get an address and return the Zillow url corresponding to this address
def get_address(address):
    address = re.sub('\W+',' ', address )
    url = address.replace(' ','-')
    return PREFIX + url+'_rb'

#Return Number of bedrooms, bathrooms and size of the appartment
def get_bd_ba_size(driver):
    element = driver.find_element_by_class_name("ds-bed-bath-living-area-container")
    infos = element.text.split()
    #print(infos)
    bd = to_decimal(infos[0])
    ba = to_decimal(infos[1][2:])
    size = infos[2][2:]+infos[3]
    size = [c for c in size if c.isdigit()]
    s= int(''.join(size))
    return bd, ba, s

#Return sold date if the appartment is sold, else None
def get_sold_date(driver):
    try : 
        element =  driver.find_element_by_xpath("//*[contains(text(),'Sold on ')]")
        return element.text[-8:]
    except : 
        return None
#Return Zestimate if the appartment is sold, else None
def get_Zestimate(driver):
    element =  driver.find_element_by_xpath(".//p[@class = 'Text-c11n-8-33-0__aiai24-0 StyledParagraph-c11n-8-33-0__sc-18ze78a-0 jfHfpE']")
    res = element.text.split()[-1] 
    return res if '$' in res else None

def get_walk_Score(driver):
    return int(driver.find_element_by_xpath(".//div[@class= 'zsg-content-component']//a").text)
        
def get_transit_Score(driver):
    return int(driver.find_element_by_xpath(".//div[@class= 'zsg-content-component']//li[position()=2]//a").text)

#Return the average of GrateSchools rating
def get_GreateSchools(driver):
    i, grades =1, []
    while True:
        try :
            element = driver.find_element_by_xpath(".//div[@class= 'Spacer-c11n-8-33-0__sc-17suqs2-0 hHqwWf']//li[position()="+str(i)+"]")
            grades.append(int(element.text[0]))
        except:
            break
        i+=1
    return round(np.average(grades),2)

def get_info(address):
    url = get_address(address)
    
    driver.get(url)
    #time.sleep(15)
    #bt_submit = driver.find_element_by_css_selector("[type=submit]")

# wait for the user to click the submit button (check every 1s with a 1000s timeout)
    #WebDriverWait(driver, timeout=15, poll_frequency=1).until(EC.staleness_of(bt_submit))

    lst = []
    lst += get_bd_ba_size(driver)
    lst.append(get_sold_date(driver))
    lst.append(get_Zestimate(driver))
    lst.append(get_walk_Score(driver))
    lst.append(get_transit_Score(driver))
    lst.append(get_GreateSchools(driver))
    return lst

#Convert a float written with a , to a regular float
def to_decimal(x):
    num = x.split(',')
    return int(x) if len(num) <= 1 else float(num[0]+'.'+num[1])

print(get_info('2517 E 13th St, Indianapolis, IN 46201'))
print(get_info('5689 Versailles Ave, Ann Arbor, MI 48103'))
print(get_info('1500 N Lake Shore Dr #4B, Chicago, IL 60610'))

