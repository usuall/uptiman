from glob import glob
import pymysql
from pyparsing import null_debug_action
from selenium import webdriver
from PIL import Image
import requests
import urllib3
import time
import os
import myfunc

from retry import retry
from wrapt_timeout_decorator import *
import random

class URL_Health_Check():

    # 실행경로
    
    
    # 실행환경
    headless = 0
    user_agent ='user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
    cur = None
    
    def __init__(self):
        project_path = os.path.abspath(os.getcwd())
        self.lib_path = project_path + '/lib'
        self.img_path = project_path + '/capture/'
        self.img_resize_path = project_path + '/capture_resized/'
        
    def main2():
        global lib_path
        
        # 브라우져 옵션 설정
        
        self.set_browser_option()
        driver = webdriver.Chrome(lib_path + '/chromedriver.exe', chrome_options=options)
        
        # start_url = 'https://www.google.com'
        driver.implicitly_wait(10)
        driver.set_window_size(1920, 1080)
        # driver.get(start_url)
        
        
    def dbconn():
        global cur
        try:
            # DB접속            
            cur =  myfunc.dbconn2()            
        except Exception as e:
            print('DB Connection Exception : '+ str(e))
            
        
    # 이미지 리사이즈(100%->50%)
    def img_resizer(img_path, img_str):
        global img_resize_path
        img = Image.open(img_path + img_str)
        img_half_resize = img.resize((int(img.width / 2), int(img.height / 2)))
        img_half_resize.save(img_resize_path + 'resized_' + img_str)
        
    
    # 브라우저 기본 설정
    def set_browser_option(self):
        # 전역변수 사용하기
        global headless, user_agent        
        options = webdriver.ChromeOptions()
        # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # 브라우져 창 최대화
        options.add_argument("--start-maximized")
        
        # 브라우져 창 최소화
        if(headless == True):
            options.add_argument('--window-size=900,700')
            options.add_argument("--headless")       
        
        #user agent 지정
        options.add_argument(user_agent)    
        
        # InsecureRequestWarning  메시지 제거
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
        
    #@retry(TimeoutError, tries=3, delay=1, backoff=2)
    @timeout(5)
    def worker(value):#valueの処理
        print (value),
        #1~10秒待つ.
        sleep_time = random.randrange(1, 10)
        print (":sleep_time", sleep_time)
        time.sleep(sleep_time)
        print(value, ":Done.")


    if __name__ == "__main__":
        main2()
        
    # if __name__ == "__main__":
    #     values = [1, 2, 3]

    #     for value in values:
    #         Time = time.time()
    #         try:
    #             worker(value)
    #         except TimeoutError as e:
    #             print (e)
    #         finally:
    #             print("掛った時間", time.time() - Time)

    #     print ("Finish")