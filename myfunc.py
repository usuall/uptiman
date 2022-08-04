# mysql 
import pymysql

# DB 접속
def dbconn():
    return pymysql.connect(host='localhost', user='root', password='', db='healthmon', charset='utf8')

# 새창 뜨는 경우 닫기 기능
def close_new_tabs(driver):
    tabs = driver.window_handles
    while len(tabs) != 1:
        driver.switch_to.window(tabs[1])
        driver.close()
        tabs = driver.window_handles
    driver.switch_to.window(tabs[0])