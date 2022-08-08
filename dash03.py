#!/usr/bin/env python
import PySimpleGUI as sg
import pymysql
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from uptime_model import *
#from wrapt_timeout_decorator import *

from PIL import Image
import requests
import urllib3
import time
import os
import myfunc


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


# 브라우저 기본 설정
def set_browser_option(options):
    # '시스템에 부착된 장치가 작동하지 않습니다' 오류 제거
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    # 브라우져 창 최대화
    options.add_argument("--start-maximized")

    # 브라우져 창 최소화
    if (headless == 1):
        options.add_argument('--window-size=900,700')
        options.add_argument("--headless")

        # 실행되는 브라우저 크기를 지정할 수 있습니다.

    options.add_argument(user_agent)

    # InsecureRequestWarning  메시지 제거
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 기관 리스트 취득
def my_org_list():

    org_list = {'기관 전체': 0}
    result = get_org_list()
    for row in result:
        org_list[row['org_title']] = row['org_no']

    return org_list

def my_org_list_combo():

    org_list = ['기관 전체']
    result = get_org_list()
    for row in result:
        org_list.append(row['org_title'])

    return org_list

def get_monitoring(window, org_name):
    print(' 모니터링 시작 : ' + org_name)
    result = get_org_url_list(org_name)
    for row in result:
        print(row)
        window['-OUTPUT-'].update(value=row['url_addr']+'\n', append=True)

def get_monitoring_all(window):
    result = get_org_url_list_all()
    for row in result:
        print(row)
        window['-OUTPUT-'].update(value=row['url_addr']+'\n', append=True)
        
    


def main():

    #모니터링 실시
    #org_list = my_org_list()
    org_list = my_org_list_combo()

    # GUI 실행
    sg.theme('TanBlue')

    column1 = [
        [sg.Text('Column 1', background_color=sg.DEFAULT_BACKGROUND_COLOR,
                 justification='center', size=(10, 1))],
        [sg.Spin(values=('Spin Box 1', '2', '3'),
                 initial_value='Spin Box 1', key='spin1')],
        [sg.Spin(values=('Spin Box 1', '2', '3'),
                 initial_value='Spin Box 2', key='spin2')],
        [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3', key='spin3')]]

    layout = [
        [sg.Text('Uptime HealthCheck Manager', size=(30, 1), font=("Helvetica", 25))],
        [sg.Text('URL 모니터링 툴입니다. 실행전에 아래 설정부분을 선택하고 실행바랍니다.')],
        # [sg.InputText('', key='in1')],
        # [sg.Listbox(values=(org_list), size=(30, 1), key='-ORG_LIST-', enable_events=True)],
        [sg.Text('기관 선택'), sg.Combo(values=(org_list), size=(30, 1), key='-ORG_LIST-', enable_events=True)],
        [sg.CBox('반복 점검', key='refeat', default=True), sg.CBox('비활성화 URL 포함', key='url_fg')],
        [sg.Text('타임아웃'), sg.Radio('5초', "RADIO1", key='timeout1'),
         sg.Radio('10초', "RADIO1", key='timeout2', default=True),
         sg.Radio('15초', "RADIO1", key='timeout3'),
         sg.Radio('20초', "RADIO1", key='timeout4'),
         sg.Radio('25초', "RADIO1", key='timeout5'),
         sg.Radio('30초', "RADIO1", key='timeout6')],

        [sg.MLine(default_text='monitoring logging area', size=(80, 20), key='-OUTPUT-', autoscroll=True, disabled=True)],
        # [sg.Combo(('Combobox 1', 'Combobox 2'), key='combo', size=(20, 1)),sg.Slider(range=(1, 100), orientation='h', size=(34, 20), key='slide1', default_value=85)],
        # [sg.Combo(('Combobox 1', 'Combobox 2'), key='combo', size=(20, 1))],
        # [sg.OptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'), key='optionmenu')],

        # [sg.Text('Choose A Folder', size=(35, 1))],
        # [sg.Text('Your Folder', size=(15, 1), justification='right'),
        # sg.InputText('Default Folder', key='folder'), sg.FolderBrowse()],
        [sg.Button('Exit'),
         sg.Text(' ' * 40), sg.Button('     시 작     '), sg.Button('중 지')]
    ]

    window = sg.Window('Uptime Health Check Manager for NIRS', layout, default_element_size=(40, 1),
                       grab_anywhere=False)

    while True:
        event, values = window.read()



        if event == '     시 작     ':
            print('시작')
            mon_status = 1
            org_title = values['-ORG_LIST-']
            if org_title == '기관 전체':
                print('전체 점검..... ')
                get_monitoring_all(window)

            else:
                print('기관 검색')
                get_monitoring(window, org_title)






            # filename = sg.popup_get_file('Save Settings', save_as=True, no_window=True)
            # window.SaveToDisk(filename)
            # save(values)
        elif event == '중 지':
            print('중지')
            # filename = sg.popup_get_file('Load Settings', no_window=True)
            # window.LoadFromDisk(filename)
            # load(form)
        elif event in ('Exit', None):
            break

    window.close()


if __name__ == '__main__':
    # DB접속
    cur = myfunc.dbconn2()

    main()
