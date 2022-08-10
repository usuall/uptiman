from selenium import webdriver
import requests
import urllib3
import time
import os
import myfunc 


# from mysql_config import dbconn # DB설정
# cur = dbconn().cursor()
cur = myfunc.dbconn().cursor()

# 실행경로
project_path = os.path.abspath(os.getcwd())
lib_path = project_path + '/lib'
img_path = project_path + '/capture/'

# 크롬 브라우저 오픈
options = webdriver.ChromeOptions()
# '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
options.add_experimental_option("excludeSwitches", ["enable-logging"])

# 브라우져 창 최대화
#options.add_argument("--start-maximized")
# 브라우져 창 최소화
options.add_argument("--headless") 
driver = webdriver.Chrome(lib_path + '/chromedriver.exe', chrome_options=options)

# InsecureRequestWarning  메시지 제거
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

# start_url = 'https://www.google.com'
driver.implicitly_wait(10)
# driver.get(start_url)

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
        myfunc.close_new_tabs(driver)
        
        # response = requests.get(web_url) 
        response = requests.get(web_url, verify=False) # SSLerror 오류 발생 회피 
        requests_code = response.status_code
        print(requests_code)
        time.sleep(2)
        
        # 이미지 캡쳐 (브라우져 크기 설정후 캡쳐 사이즈 지정 필요)
        # redirec 된 url로 이미지 캡쳐 필요
        img_str = str(row[1])+ "__" + row[4] + ".png"
        #print (img_str)
        driver.save_screenshot(img_path + img_str)
        
        
        if requests_code != 200 :
            print ('URL점검 이벤트 발생 : ' + web_url)  #음성 맨트
            #break   #주석 풀면 url_list 처음부터 시작
            
conn.close()