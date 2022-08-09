#!/usr/bin/env python
from pickle import TRUE
from threading import TIMEOUT_MAX
import PySimpleGUI as sg
import pymysql
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from uptime_model import *
#from wrapt_timeout_decorator import *

from PIL import Image
import requests
import urllib3
import time
import os
import myfunc
import asyncio


'''
    URL healthcheck dashboard intrudoction...
    ....
    .... copyright usuall@korea.kr

'''

# 실행경로
project_path = os.path.abspath(os.getcwd())
lib_path = project_path + '/lib'
img_path = project_path + '/capture/'
img_resize_path = project_path + '/capture_resized/'
mon_status = 0 #모니터링 시작 유무

# 실행환경
headless = 0
user_agent = 'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
# myfont = lib_path + '/font/NanumGothic-Regular.ttf'

# 브라우저 기본 설정
def set_browser_option(bg_exec):
    
    print ('bg_exec ',bg_exec)
    # 크롬 브라우저 오픈
    options = webdriver.ChromeOptions()
    
    # 브라우져 옵션 설정
    driver = webdriver.Chrome(lib_path + '/chromedriver.exe', chrome_options=options)
    
    # start_url = 'https://www.google.com'
    driver.implicitly_wait(10)
    driver.set_window_size(1920, 1080)
    # driver.get(start_url)
    
    # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # 브라우져 창 최대화
    options.add_argument("--start-maximized")

    # 브라우져 창 최소화
    if (bg_exec == 1):
        print ('-------------bg_executed ----')
        options.add_argument('--window-size=900,700')
        options.add_argument("--headless")

    options.add_argument(user_agent)

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
    from datetime import datetime
    sysdate = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return str(sysdate)

#기관단위 모니터링
def get_monitoring(window, keyword):
    
    stime = time.time()
    # 브라우저 환경 설정 취득
    bg_exec = keyword.get('DISABLED') # 백그라운드 실행
    driver = set_browser_option(bg_exec)
        
    cnt = 0
    print(' 모니터링 시작 : ')
    result = get_org_url_list(keyword)
    for row in result:
        cnt += 1
        # 작업시간 출력
        str1 = '[' + get_sysdate() + '] '+ row['url_addr']
        window['-OUTPUT-'].update(value=str1, append=True)
        
        # 브라우져 URL 탐색
        web_url = row['url_type']+row['url_addr']
        driver.get(web_url)
        
        window.refresh() # 작업창 멈추는 현상 해결 및 작업내용 출력 반영
        #selenium.find_element_by_id('body').send_keys(Keys.ESCAPE).perform()
        #webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        
        # 새창 닫기
        myfunc.close_new_tabs(driver)
        window.refresh() # 작업창 멈추는 현상 해결 및 작업내용 출력 반영
        window['-OUTPUT-'].update(value=' → Tab', append=True)
        window['-OUTPUT-'].update(value='\n', append=True)
        window.refresh() # 작업창 멈추는 현상 해결 및 작업내용 출력 반영

    if(cnt > 0):
        window['-OUTPUT-'].update(value='-------------------------------------------\n', append=True)
        window['-OUTPUT-'].update(value='▶ (처리 URL) ' + str(cnt) +'건, (처리시간) '+ str(round(time.time()-stime, 2)) + '초 \n', append=True)
    else:
        window['-OUTPUT-'].update(value='▶ 검색 결과 없음', append=True)
    # 작업 종료후 버튼 활성화
    button_activate(window, 1)

# #전체 기관 모니터링
# def get_monitoring_all(window):    
#     result = get_org_url_list_all()
#     for row in result:
#         #print(row)
#         str1 = '[' + get_sysdate() + '] '+ row['url_addr']+'\n'
#         window['-OUTPUT-'].update(value=str1, append=True)
        
    
def getCondition(window, values):
    str1 = '[' + get_sysdate() + '] '
    print ('condition : '+values['-ORG_LIST-'])
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
   
    window['-OUTPUT-'].update(value='- 실행시간 : ' + str1 + '\n', append=True)
    window['-OUTPUT-'].update(value='<검색조건>' + '\n', append=True)
    window['-OUTPUT-'].update(value='- 기관 선택 : ' + values['-ORG_LIST-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- 사이트명 : ' + values['-SITE_TITLE-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- URL명 : ' + values['-SITE_URL-'] + '\n', append=True)
    window['-OUTPUT-'].update(value='- 반복 점검 : ' + str(values['-REPEAT-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 비활성화 URL포함. : ' + str(values['-DISABLED-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 백그라운드 실행 : ' + str(values['-BG_EXE-']) + '\n', append=True)
    window['-OUTPUT-'].update(value='- 타임아웃 설정 : ' + str(timeout_term) + '초\n', append=True)
    
    window['-OUTPUT-'].update(value='-------------------------------------------\n', append=True)
    
    #검색 조건 저장
    keyword = {'ORG_LIST':      values['-ORG_LIST-'], 
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
    
    obj_list = '-ORG_LIST-', '-TIMEOUT1-', '-TIMEOUT2-', '-TIMEOUT3-', '-TIMEOUT4-', '-TIMEOUT5-', '-TIMEOUT6-', '-DISABLED-', '-SITE_TITLE-', '-SITE_URL-', '-BG_EXE-', '-BUTTON_START-', '-BUTTON_EXIT-'
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
    #org_list = my_org_list()
    org_list = my_org_list_combo()

    # GUI 실행
    sg.theme('TanBlue')

    layout = [
        [sg.Text('URL Health-Check Manager', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('URL 모니터링 툴입니다. 조건을 선택하고 실행하세요')],
        # [sg.InputText('', key='in1')],
        # [sg.Listbox(values=(org_list), size=(30, 1), key='-ORG_LIST-', enable_events=True)],
        [sg.Text('기관 선택'), sg.Combo(values=(org_list), default_value='전 체', size=(30, 1), key='-ORG_LIST-', enable_events=True)],
        [sg.Text(' 사이트명'), sg.InputText('', key='-SITE_TITLE-', size=(30, 1)),
         sg.Text('  URL'), sg.InputText('', key='-SITE_URL-', size=(30, 1))],
        [sg.CBox('반복 점검', key='-REPEAT-', default=True), 
         sg.CBox('비활성화 URL 포함', key='-DISABLED-'), sg.CBox('백그라운드 실행', key='-BG_EXE-')],
        [sg.Text('타임아웃'), sg.Radio('5초',  group_id="RADIO1", key='-TIMEOUT1-'),
                            sg.Radio('10초', group_id="RADIO1", default=True, key='-TIMEOUT2-'),
                            sg.Radio('15초', group_id="RADIO1", key='-TIMEOUT3-'),
                            sg.Radio('20초', group_id="RADIO1", key='-TIMEOUT4-'),
                            sg.Radio('25초', group_id="RADIO1", key='-TIMEOUT5-'),
                            sg.Radio('30초', group_id="RADIO1", key='-TIMEOUT6-')],

        [sg.MLine(default_text='', font='Gothic', size=(80, 20), key='-OUTPUT-', autoscroll=True, disabled=True)],
        # [sg.Combo(('Combobox 1', 'Combobox 2'), key='combo', size=(20, 1)),sg.Slider(range=(1, 100), orientation='h', size=(34, 20), key='slide1', default_value=85)],
        # [sg.Combo(('Combobox 1', 'Combobox 2'), key='combo', size=(20, 1))],
        # [sg.OptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'), key='optionmenu')],

        # [sg.Text('Choose A Folder', size=(35, 1))],
        # [sg.Text('Your Folder', size=(15, 1), justification='right'),
        # sg.InputText('Default Folder', key='folder'), sg.FolderBrowse()],
        [sg.Button('종 료', key='-BUTTON_EXIT-', button_color=('white', 'firebrick3')),
         sg.Text('  ' * 30), sg.Button('     실 행     ', key='-BUTTON_START-'), sg.Button('중 지', key='-BUTTON_STOP-', disabled=True, button_color=('black', 'lightblue'))]
    ]

    
    window = sg.Window('Uptime Manager for NIRS', layout, default_element_size=(40, 1),
                       grab_anywhere=False)

    while True:
        event, values = window.read()

        # 각종 버튼에 대한 이벤트 처리
        if event == '-BUTTON_START-':
            print('시작')
            
            #버튼 비활성화 전환
            button_activate(window, 0)
            # window['-OUTPUT-'].update(value='', append=False)
            
            # # 버튼 활성화 전환
            # window['-BUTTON_STOP-'].update(disabled=False)
            # for key in obj_list:
            #     window[key].update(disabled=True)

            # 조회조건 출력
            keyword = getCondition(window, values)
            
            # 모니터링 중
            mon_status = 1
            
            # 모니터링 작업
            get_monitoring(window, keyword)
            
        elif event == '-BUTTON_STOP-':
            print('중지')
            # 버튼 활성화 전환
            button_activate(window, 1)
            # window['-BUTTON_STOP-'].update(disabled=True)
            # for key in obj_list:
            #     window[key].update(disabled=False)

        elif event in ('-BUTTON_EXIT-', 'Escape:27', sg.WIN_CLOSED):
            # Todo : browser & dbconnection close.
            print('exit....')
            break

    window.close()


if __name__ == '__main__':
    # DB접속
    cur = myfunc.dbconn2()

    main()
