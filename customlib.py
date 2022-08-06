import pymysql
import urllib3
import time
import os
from selenium import webdriver
from PIL import Image
from wrapt_timeout_decorator import *

class CustomLib:
    
    headless = None
    user_agent = None
    img_resize_path = None
    driver = None
    
    def __init__(self):
        global headless, user_agent, img_resize_path
        #self.org_no = org_no
        # 실행경로
        project_path = os.path.abspath(os.getcwd())
        self.lib_path = project_path + '/lib'
        self.img_path = project_path + '/capture/'
        img_resize_path = project_path + '/capture_resized/'
        headless = 0
        user_agent ='user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    
    # 새창 뜨는 경우 닫기 기능
    def close_new_tabs(self, driver):
        tabs = driver.window_handles
        while len(tabs) != 1:
            driver.switch_to.window(tabs[1])
            driver.close()
            tabs = driver.window_handles
        driver.switch_to.window(tabs[0])
        
    # 브라우저 기본 설정
    def set_browser_option(self, options):
        global headless
        # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # 브라우져 창 최대화
        options.add_argument("--start-maximized")
        
        # 브라우져 창 최소화
        if(headless == True):
            options.add_argument('--window-size=900,700')
            options.add_argument("--headless")       
        
        # 실행되는 브라우저 크기를 지정할 수 있습니다.        
        
        options.add_argument(user_agent)    
        
        # InsecureRequestWarning  메시지 제거
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    
    
    # 이미지 리사이즈(100%->50%)
    def img_resizer(self, img_path, img_str):
        img = Image.open(img_path + img_str)
        img_half_resize = img.resize((int(img.width / 2), int(img.height / 2)))
        img_half_resize.save(img_resize_path + 'resized_' + img_str)
        
    timeout(5)
    def getChromeBrower(self, web_url):
        global driver
        self.driver.get(web_url)
        
        
        
    



    
    
        
        