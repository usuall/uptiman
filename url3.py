from selenium import webdriver
import requests
import urllib3
import time
import os

from mysql_config import dbconn # DB설정
cur = dbconn().cursor()

# 실행경로
project_path = os.path.abspath(os.getcwd())
lib_path = project_path + '/lib'



# 크롬 브라우저 오픈
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
options.add_argument("--start-maximized")
driver = webdriver.Chrome(lib_path + '/chromedriver.exe', chrome_options=options)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # InsecureRequestWarning  메시지 제거

# start_url = 'https://www.google.com'
driver.implicitly_wait(10)
# driver.get(start_url)

def close_new_tabs(driver):
    tabs = driver.window_handles
    while len(tabs) != 1:
        driver.switch_to.window(tabs[1])
        driver.close()
        tabs = driver.window_handles
    driver.switch_to.window(tabs[0])
    

while 1:
    
    # URL 리스트 취득
    sql = 'select * from tb_url where url_fg=1'
    cur.execute(sql)

    for row in cur:
        #print(row[0], row[1], row[2], row[3])
        #print(row)
        web_url = row[3]+row[4]
        str1 = str(row[1]) + ' : ' + web_url
        print(str1)
        driver.get(web_url)
        
        # 새창 닫기
        close_new_tabs(driver)        
        
        # response = requests.get(web_url) 
        response = requests.get(web_url, verify=False) # SSLerror 오류 발생 회피 
        requests_code = response.status_code
        print(requests_code)
        time.sleep(2)
        if requests_code != 200 :
            print ('URL점검 이벤트 발생 : ' + web_url)  #음성 맨트
            #break   #주석 풀면 url_list 처음부터 시작
            
