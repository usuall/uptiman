#!/usr/bin/env python
from pickle import TRUE
from socket import timeout
from threading import TIMEOUT_MAX
import PySimpleGUI as sg
import pymysql
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

from uptime_model import *
#from wrapt_timeout_decorator import *
from bs4 import BeautifulSoup
from datetime import datetime

from PIL import Image
import requests
import urllib3
import time
import os
import myfunc
import asyncio

'''
    URL healthcheck dashboard introduction...
    ....
    .... copyright usuall@gmail.com
'''

# 실행경로
project_path = os.path.abspath(os.getcwd()) + '\\'
lib_path = project_path + 'lib\\'
img_path = project_path + 'capture\\'
html_path = project_path + 'html\\'
img_resize_path = project_path + 'capture_resized\\'
mon_status = 0 #모니터링 시작 유무

# 실행환경
user_agent = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
# myfont = lib_path + '/font/NanumGothic-Regular.ttf'

# 브라우저 기본 설정
def set_browser_option(bg_exec):
    
    # print ('bg_exec ',bg_exec)
    # 크롬 브라우저 오픈
    options = webdriver.ChromeOptions()
    # USER_Agent 지정
    options.add_argument(user_agent)
    options.add_argument("disable-gpu")
    # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # 브라우져 창 최소화 유무
    if (bg_exec == True):
        print ('------------- 백그라운드 실행 = true -----------')
        options.add_argument('--window-size=1900,1080')
        options.add_argument("--headless")
        # options.headless = True

    else:
        # driver.set_window_size(1920, 1080)
        options.add_argument("--start-maximized")
    
    # 브라우져 옵션 설정
    # driver = webdriver.Chrome(lib_path + 'chromedriver.exe', options=options) # deprecated option
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # 명시적으로 대기(10초) 
    driver.implicitly_wait(time_to_wait=10)
    
    # InsecureRequestWarning  메시지 제거
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    return driver

# 기관 리스트 취득
def my_org_list():

    org_list = {'기관 전체': 0}
    result = get_org_list()
    for row in result:
        org_list[row['org_title']] = row['org_no']

    return org_list

def my_org_list_combo():

    org_list = ['전 체']
    result = get_org_list()
    for row in result:
        #org_list.append(row['org_title']+'['+row['org_no']+']')
        org_list.append(row['org_title'])

    return org_list

#현재시각
def get_sysdate():
    sysdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(sysdate)

def get_request_code(web_url):
    response = requests.get(web_url, verify=False) # SSLerror 오류 발생 회피 
    requests_code = response.status_code
    return requests_code        

def save_html(url_no, mon_no, src_text):

    sysdate = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    # print(html_path + str(url_no)+'_'+str(sysdate)+'.html')
    file_name = str(url_no)+'_'+str(sysdate)+'.html'
    full_path_name = html_path + file_name
    
    # 저장용 디렉토리 존재 유무 확인 및 생성
    isExist = os.path.exists(html_path)
    if(isExist == False):
        os.makedirs(html_path)
        
    f = open(full_path_name, 'w', encoding='UTF-8')
    # print(type(src_text))
    f.write(str(src_text))
    f.close()

    return file_name
    # DB insert
    


    
#기관단위 모니터링
def get_monitoring(window, keyword):
    
    stime = time.time()
    # 브라우저 환경 설정 취득
    bg_exec = keyword.get('BG_EXE') # 백그라운드 실행
    driver = set_browser_option(bg_exec)
        
    cnt = 0
    print(' 모니터링 시작 : ')
    result = get_org_url_list(keyword)
    # print('resutl ',type(result), len(result))
    total_cnt = len(result) # 조회 건수
    window['-OUTPUT-'].update(value='- 조회건수 : '+ str(total_cnt) +'건\n', append=True)
    window['-OUTPUT-'].update(value='------------------------------\n\n', append=True)

    for row in result:
        cnt += 1
        
        pertime = time.time() # 개별작업시간
        # 작업시간 출력
        str1 = '[' + get_sysdate() + '] ['+ str(cnt) + '/' + str(total_cnt) + ' (' + str(row['url_no']) + ')] ' + row['url_addr'] +'\n'
        window['-OUTPUT-'].update(value=str1, append=True)
        window.refresh() 

        # 브라우져 URL 탐색
        web_url = row['url_type']+row['url_addr']
        
        #브라우져 무한로딩시 timeout 으로 회피(jnpolice.go.kr 사례) / 해결하는데 5일 걸림
        get_url_timout = keyword.get('TIME_OUT') #디폴트 10초
        driver.set_page_load_timeout(get_url_timout)
        print('1111 ' + web_url)
        try:
            driver.get(web_url)
            print('2222')
        except TimeoutException as ex:
            print('3333')
            pass
        
        redirected_url = driver.current_url
        print('3333')
        # 특정 태그
        #element = driver.find_element(By.TAG_NAME, "body")
        window['-OUTPUT-'].update(value=' Redirected → '+redirected_url+'\n', append=True)
        # print('redirected -->', driver.current_url)
        window.refresh() # 작업내용 출력 반영        
        
        # 이미지 캡쳐 (브라우져 크기 설정후 캡쳐 사이즈 지정 필요)
        # redirect 된 url로 이미지 캡쳐 필요
        img_str = str(row['url_no'])+ "__" + row['url_addr'] + ".png"
        time.sleep(2) # 화면캡쳐 전 2초대기
        driver.save_screenshot(img_path + img_str)
        window['-OUTPUT-'].update(value=' → Image captured ('+ str(round(time.time()-pertime, 2))+'s)', append=True)
        
        #html 소스코드 취득
        html_source = driver.page_source # redirected 최종 URL의 소스를 취득
        #window['-OUTPUT-'].update(value=' redirected2 -> '+ driver.current_url, append=True)
        #print(html_source)
        # window['-OUTPUT-'].update(value='11111-------------------------------------------\n', append=True)
        # window['-OUTPUT-'].update(value=html_source, append=True)
        
        html_source = BeautifulSoup(html_source, 'html.parser').prettify
        # window['-OUTPUT-'].update(value='22222-------------------------------------------\n', append=True)
        # window['-OUTPUT-'].update(value=html_source, append=True)
        # window['-OUTPUT-'].update(value='33333-------------------------------------------\n', append=True)
        window.refresh()
        
        #html 저장
        #add_html_source(row['url_no'], row['url_no'], html_source)
        file_name = save_html(row['url_no'], row['url_no'], html_source)
        window['-OUTPUT-'].update(value=' → html saved ('+ str(round(time.time()-pertime, 2))+'s) ', append=True)

        # Request Code 취득 : (200 : ok, 404 : page not found)
        #req_code = get_request_code(web_url)
        req_code = get_request_code(redirected_url)
        
        t_color='Black'
        if(req_code != 200):
            t_color='Red'
        
        window['-OUTPUT-'].update(value='→ (Code ' + str(req_code) +')', append=True, text_color_for_value=t_color)
        window.refresh()

        # 새창 닫기
        myfunc.close_new_tabs(driver)
        window['-OUTPUT-'].update(value=' → Tab', append=True)
        window['-OUTPUT-'].update(value=' ('+str(round(time.time()-pertime, 2)) + 's)', append=True)        
        window['-OUTPUT-'].update(value='\n', append=True)
        window.refresh() # 작업창 멈추는 현상 해결 및 작업내용 출력 반영

        #모니터링 데이터 DB
        add_monitoring(row['url_no'], req_code, file_name)
        
        print('---- url checking ended----')

    if(cnt > 0):
        endtime = time.time()
        window['-OUTPUT-'].update(value='-------------------------------------------\n', append=True)
        window['-OUTPUT-'].update(value='▶ (처리 URL) ' + str(cnt) +'건, (처리시간) '+ str(round(endtime-stime, 2)) + '초, (평균처리 시간) '+ str(round((endtime-stime)/cnt,2)) +'초 \n', append=True)
    else:
        window['-OUTPUT-'].update(value='▶ 검색 결과 없음', append=True)
    
    # 작업 종료후 버튼 활성화
    button_activate(window, 1)

    #처리건수 리턴
    return cnt

# #전체 기관 모니터링
# def get_monitoring_all(window):    
#     result = get_org_url_list_all()
#     for row in result:
#         #print(row)
#         str1 = '[' + get_sysdate() + '] '+ row['url_addr']+'\n'
#         window['-OUTPUT-'].update(value=str1, append=True)
        
    
def getCondition(window, values):
    str1 = '[' + get_sysdate() + '] '
    #print ('condition : '+values['-ORG_LIST-'])
    if(values['-TIMEOUT1-'] == True ):
        timeout_term = 5
    elif(values['-TIMEOUT2-'] == True ):
        timeout_term = 10
    elif(values['-TIMEOUT3-'] == True ):
        timeout_term = 15
    elif(values['-TIMEOUT4-'] == True ):
        timeout_term = 20
    elif(values['-TIMEOUT5-'] == True ):
        timeout_term = 25
    elif(values['-TIMEOUT6-'] == True ):
        timeout_term = 30
    else:
        timeout_term = 12

    # print ('condition : ' + str(timeout_term))
   
    # window['-OUTPUT-'].update(value='- 실행시간 : ' + str1 + '\n', append=True)
    window['-OUTPUT-'].update(value='--------- <검색조건> ---------' + '\n', append=True)
    window['-OUTPUT-'].update(value='- 카테고리 : ' + values['-ORG_LIST-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- 사이트명 : ' + values['-SITE_TITLE-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- URL명 : ' + values['-SITE_URL-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- 반복 점검 : ' + str(values['-REPEAT-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 비활성화 URL포함. : ' + str(values['-DISABLED-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 백그라운드 실행 : ' + str(values['-BG_EXE-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 타임아웃 설정 : ' + str(timeout_term) + '초\n', append=True)
    # window['-OUTPUT-'].update(value='-------------------------------------------\n', append=True)

    #검색 조건 저장
    keyword = { 'ORG_LIST':     values['-ORG_LIST-'], 
                'SITE_TITLE':   values['-SITE_TITLE-'], 
                'SITE_URL':     values['-SITE_URL-'], 
                'REPEAT':       values['-REPEAT-'], 
                'DISABLED':     values['-DISABLED-'], 
                'BG_EXE':       values['-BG_EXE-'], 
                'TIME_OUT':     timeout_term }

    # for k in keyword.values():
    #     print('>>>',k)

    return keyword


def button_activate(window, activate):

    # 화면 요소ID
    obj_list = '-ORG_LIST-', '-TIMEOUT1-', '-TIMEOUT2-', '-TIMEOUT3-', '-TIMEOUT4-', '-TIMEOUT5-', '-TIMEOUT6-', '-DISABLED-', '-SITE_TITLE-', '-SITE_URL-', '-REPEAT-', '-BG_EXE-', '-BUTTON_START-', '-BUTTON_EXIT-'
    
    # 버튼 활성화 전환
    if activate == 0:
        window['-OUTPUT-'].update(value='', append=False)
        window['-BUTTON_STOP-'].update(disabled=False)
        for key in obj_list:
            window[key].update(disabled=True)
    else:
        window['-BUTTON_STOP-'].update(disabled=True)
        for key in obj_list:
            window[key].update(disabled=False)
        
    
def main():

    #모니터링 실시
    
    #카테고리 취득
    org_list = my_org_list_combo()

    # GUI 실행
    sg.theme('TanBlue')
    layout_left = [[sg.Button('종 료', key='-BUTTON_EXIT-', button_color=('white', 'firebrick3'))]]
    layout_right =[[sg.Button('     실 행     ', key='-BUTTON_START-'), sg.Button('중 지', key='-BUTTON_STOP-', disabled=True, button_color=('black', 'lightblue'))]]
    layout = [
        [sg.Text('URL Health-Check Manager', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('URL 모니터링 툴입니다. 조건을 선택하고 실행하세요'),sg.Text('URL 모니터링 툴입니다. 조건을 선택하고 실행하세요')],
        # [sg.InputText('', key='in1')],
        # [sg.Listbox(values=(org_list), size=(30, 1), key='-ORG_LIST-', enable_events=True)],
        [sg.Text('카테고리'), sg.Combo(values=(org_list), default_value='전 체', size=(30, 1), key='-ORG_LIST-', enable_events=False, tooltip='카테고리를 선택해주세요.')],
        [sg.Text('사이트명'), sg.InputText('', key='-SITE_TITLE-', size=(30, 1), tooltip='사이트명을 입력하세요.'),
         sg.Text('  URL명'), sg.InputText('', key='-SITE_URL-', size=(30, 1), tooltip='도메인(URL)을 입력하세요.')],
        [sg.CBox('반복 점검', key='-REPEAT-', default=False, tooltip='체크 대상을 반복하여 점검합니다.'), 
         sg.CBox('비활성화 URL 포함', key='-DISABLED-'), sg.CBox('백그라운드 실행', key='-BG_EXE-', default=True, tooltip='임시 비활성화 URL 대상까지 검색')],
        [sg.CBox('AP작업 포함', key='-AP_WORK-', default=TRUE, tooltip='AP작업중 URL.....'), 
         sg.CBox('추가 항목', key='-ADD1-'), sg.CBox('추가 항목2', key='-ADD2-', default=True)],
        [sg.MLine(default_text='', font='Gothic', size=(80, 20), key='-OUTPUT-', autoscroll=True, disabled=True)],
        [sg.Text('타임아웃'), sg.Radio('5초',  group_id="RADIO1", key='-TIMEOUT1-'),
                            sg.Radio('10초', group_id="RADIO1", default=True, key='-TIMEOUT2-'),
                            sg.Radio('15초', group_id="RADIO1", key='-TIMEOUT3-'),
                            sg.Radio('20초', group_id="RADIO1", key='-TIMEOUT4-'),
                            sg.Radio('25초', group_id="RADIO1", key='-TIMEOUT5-'),
                            sg.Radio('30초', group_id="RADIO1", key='-TIMEOUT6-')],
        # [sg.Combo(('Combobox 1', 'Combobox 2'), key='combo', size=(20, 1)),sg.Slider(range=(1, 100), orientation='h', size=(34, 20), key='slide1', default_value=85)],
        # [sg.Combo(('Combobox 1', 'Combobox 2'), key='combo', size=(20, 1))],
        # [sg.OptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'), key='optionmenu')],

        # [sg.Text('Choose A Folder', size=(35, 1))],
        # [sg.Text('Your Folder', size=(15, 1), justification='right'),
        # sg.InputText('Default Folder', key='folder'), sg.FolderBrowse()],
        # [sg.Col(layout_left, p=0), sg.Col(layout_right, p=0)],
        [sg.Button('종 료', key='-BUTTON_EXIT-', button_color=('white', 'firebrick3')),
         sg.Text('  ' * 30), sg.Button('     실 행     ', key='-BUTTON_START-'), sg.Button('중 지', key='-BUTTON_STOP-', disabled=True, button_color=('black', 'lightblue'))]
    ]

    
    #window = sg.Window('Uptime Manager for NIRS', layout, default_element_size=(40, 1), grab_anywhere=False, location=sg.user_settings_get_entry('-LOCATION-', (None, None)))
    window = sg.Window('Uptime Manager for NIRS', layout, default_element_size=(40, 1), grab_anywhere=True )

    
    while True:
        event, values = window.read()
        # 각종 버튼에 대한 이벤트 처리
        if event == '-BUTTON_START-':
                        
            cnt = 1
            # 버튼 비활성화 전환
            button_activate(window, 0)

            # 조회조건 출력
            keyword = getCondition(window, values)
            
            # 모니터링 중
            mon_status = 1
            
            # 모니터링 작업
            while True:
                # print ('repeat -->', keyword.get('REPEAT'))
                # 반복작업 선택시
                if (keyword.get('REPEAT') == True or cnt == 1):
                    url_cnt = get_monitoring(window, keyword)
                    if(url_cnt == 0):
                        print('--- Working Completed(cnt=0) ---')
                        break
                    cnt += 1

                else:
                    print('--- Working Completed.(REPEAT=False) ---')
                    break
            
        elif event == '-BUTTON_STOP-':
            print('중지')
            # 버튼 활성화 전환
            button_activate(window, 1)

        elif event in ('-BUTTON_EXIT-', 'Escape:27', sg.WIN_CLOSED):
            # 재실행시 종료한 위치에 실행됨
            sg.user_settings_set_entry('-LOCATION-', window.current_location())
            # Todo : browser & dbconnection close.
            print('exit....')
            break

    window.close()


if __name__ == '__main__':
    main()