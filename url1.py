from selenium import webdriver
import requests
import time
import os
from gtts import gTTS
from playsound import playsound

# 실행경로
project_path = os.path.abspath(os.getcwd())
lib_path = project_path + '/lib'

# 크롬 브라우저 오픈/nSIMS접속
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(lib_path + '/chromedriver.exe', chrome_options=options)
start_url = 'https://www.google.com'
driver.implicitly_wait(10)
driver.get(start_url)

# url 접속 및 상태
f = open("./lib/url_list.txt", 'r', encoding='utf-8')
url_list = f.read().splitlines()

#playsound
def speak(text):
    tts = gTTS(text=text, lang='ko')
    filename = "C:/Python37/python_worker/url_event.wav"
    tts.save(filename)
    playsound.playsound(filename)

while 1:
    for web_url in url_list :
        print(web_url)
        driver.get(web_url)
        response = requests.get(web_url)
        requests_code = response.status_code
        print(requests_code)
        time.sleep(2)
        if requests_code != 200 :
            
            speak('URL점검 이벤트 발생')  #음성 맨트
            pyautogui.alert(text=requests_code, title='URL점검이벤트발생')  #알람팝업
            break   #주석 풀면 url_list 처음부터 시작