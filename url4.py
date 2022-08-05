import pymysql
from selenium import webdriver
from PIL import Image
import requests
import urllib3
import time
import os
import myfunc 


# 실행경로
project_path = os.path.abspath(os.getcwd())
lib_path = project_path + '/lib'
img_path = project_path + '/capture/'
img_resize_path = project_path + '/capture_resized/'

# 실행환경
headless = 1 
user_agent ='user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'


# 이미지 리사이즈(100%->50%)
def img_resizer(img_path, img_str):    
    img = Image.open(img_path + img_str)
    img_half_resize = img.resize((int(img.width / 2), int(img.height / 2)))
    img_half_resize.save(img_resize_path + 'resized_' + img_str)
    

# 브라우저 기본 설정
def set_browser_option(options):
    # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # 브라우져 창 최대화
    options.add_argument("--start-maximized")
    
    # 브라우져 창 최소화
    if(headless == 1):
        options.add_argument('--window-size=900,700')
        options.add_argument("--headless")       
    
    # 실행되는 브라우저 크기를 지정할 수 있습니다.        
    
    options.add_argument(user_agent)    
    
    # InsecureRequestWarning  메시지 제거
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)    
    

def main():    
    try:
        # DB접속
        cur = myfunc.dbconn2()
        
        # 크롬 브라우저 오픈
        options = webdriver.ChromeOptions()
        
        # 브라우져 옵션 설정
        set_browser_option(options)
        driver = webdriver.Chrome(lib_path + '/chromedriver.exe', chrome_options=options)
        
        # start_url = 'https://www.google.com'
        driver.implicitly_wait(10)
        driver.set_window_size(1920, 1080)
        # driver.get(start_url)
        
        while 1:
            
            sql = 'select * from tb_url where url_fg = 1'
            cur.execute(sql)
            rows = cur.fetchall()
            for row in rows:
                #print(row[0], row[1], row[2], row[3])
                #print(row)
                web_url = row['url_type']+row['url_addr']
                str1 = str(row['url_no']) + ' : ' + web_url
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
                img_str = str(row['url_no'])+ "__" + row['url_addr'] + ".png"
                #print (img_str)
                driver.save_screenshot(img_path + img_str)
                img_resizer(img_path, img_str)
                
                if requests_code != 200 :
                    print ('URL점검 이벤트 발생 : ' + web_url)  #음성 맨트
                    #break   #주석 풀면 url_list 처음부터 시작
        
                
        
    except Exception as e:
        print('Exception --> '+ str(e))
    finally:
        print('DB & Browser Closed')
        cur.close()
        driver.quit()

   
# MAIN 
if __name__ == '__main__':
	main()