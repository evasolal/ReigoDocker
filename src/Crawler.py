from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import re
import os

PREFIX = 'https://www.zillow.com/homes/'

print(os.path.dirname(os.path.realpath(__file__)))

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

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

    lst = []
    lst += get_bd_ba_size(driver)
    lst += [get_sold_date(driver), get_Zestimate(driver), get_walk_Score(driver)]
    lst += [get_transit_Score(driver), get_GreateSchools(driver)]
    return lst

#Convert a float written with a , to a regular float
def to_decimal(x):
    num = x.split(',')
    return int(x) if len(num) <= 1 else float(num[0]+'.'+num[1])


