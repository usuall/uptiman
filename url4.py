import pymysql
from selenium import webdriver
import requests
import urllib3
import time
import os
import myfunc 

def main():
    
    try:
        print ('debug 1')
        cur = myfunc.dbconn2()
        # 실행경로
        project_path = os.path.abspath(os.getcwd())
        lib_path = project_path + '/lib'
        img_path = project_path + '/capture/'        
        print ('debug 2')
        # 크롬 브라우저 오픈
        options = webdriver.ChromeOptions()
        # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # 브라우져 창 최대화
        options.add_argument("--start-maximized")
        # 브라우져 창 최소화
        #options.add_argument("--headless") 
        driver = webdriver.Chrome(lib_path + '/chromedriver.exe', chrome_options=options)
        print ('debug 3')
        # InsecureRequestWarning  메시지 제거
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  

        # start_url = 'https://www.google.com'
        driver.implicitly_wait(10)
        # driver.get(start_url)
        
        while 1:
            
            print ('debug 4')
            
            sql = 'select * from tb_url where url_fg = 1'
            cur.execute(sql)
            rows = cur.fetchall()
            print ('debug 5')
            for row in rows:
                print ('debug 5-1')
                #print(row[0], row[1], row[2], row[3])
                #print(row)
                web_url = row['url_type']+row['url_addr']
                print ('debug 5-2')
                str1 = str(row['url_no']) + ' : ' + web_url
                print(str1)
                driver.get(web_url)
                print ('debug 6')
                # 새창 닫기
                myfunc.close_new_tabs(driver)
                
                # response = requests.get(web_url) 
                response = requests.get(web_url, verify=False) # SSLerror 오류 발생 회피 
                requests_code = response.status_code
                print(requests_code)
                time.sleep(2)
                print ('debug 7')
                # 이미지 캡쳐 (브라우져 크기 설정후 캡쳐 사이즈 지정 필요)
                # redirec 된 url로 이미지 캡쳐 필요
                img_str = str(row['url_no'])+ "__" + row['url_addr'] + ".png"
                #print (img_str)
                driver.save_screenshot(img_path + img_str)
                print ('debug 8')
                
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