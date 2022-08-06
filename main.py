from customlib import *
from uptime_model import *

import requests
import time
from selenium import webdriver
from wrapt_timeout_decorator import *


def getMyURL():
    Time = time.time()
    while 1:
        # url 리스트 취득
        rows = get_url_list()
        for row in rows:
            web_url = row['url_type']+row['url_addr']
            str1 = str(row['url_no']) + ' : ' + web_url
            print(str1)
            #driver.get(web_url)
            try:
                lib.getChromeBrower(web_url)
            except TimeoutError as e:
                print (e)
            finally:
                print("소요 시간 : ", time.time() - Time)            
            
            # todo timeout exception
            
            # 새창 닫기
            lib.close_new_tabs(lib.driver)
            print('new table closed : '+ str1)
            # response = requests.get(web_url) 
            response = requests.get(web_url, verify=False) # SSLerror 오류 발생 회피 
            requests_code = response.status_code
            print(str1 + ' : ' + str(requests_code))
            time.sleep(2)
            # 이미지 캡쳐 (브라우져 크기 설정후 캡쳐 사이즈 지정 필요)
            # redirec 된 url로 이미지 캡쳐 필요
            img_str = str(row['url_no'])+ "__" + row['url_addr'] + ".png"
            #print (img_str)
            lib.driver.save_screenshot(lib.img_path + img_str)
            print('save_screenshot : '+ str1)
            lib.img_resizer(lib.img_path, img_str)
            print('img_resizer : '+ str1)
            if requests_code != 200 :
                print ('URL점검 이벤트 발생 : ' + web_url)  #음성 맨트
                #break   #주석 풀면 url_list 처음부터 시작


if __name__ == '__main__':

    lib = CustomLib()    
    
    #크롬 브라우저 오픈
    options = webdriver.ChromeOptions()
    
    # 브라우져 옵션 설정
    lib.set_browser_option(options)
    lib.driver = webdriver.Chrome(lib.lib_path + '/chromedriver.exe', chrome_options=options)
    lib.driver.implicitly_wait(10)
    lib.driver.set_window_size(1920, 1080)
    
    getMyURL()
