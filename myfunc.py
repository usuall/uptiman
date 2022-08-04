# mysql 
import pymysql

# DB 접속
def dbconn():
    # DB 환경에 맞게 입력할것
    host = "localhost"
    port = "3306"
    database = "healthmon"
    username = "root"
    password = ""
    charset = "utf8"
    
    # as_dict=True (select시 column명으로 데이터 조회)
    conn = pymysql.connect(host=host, user=username, password=password, db=database, use_unicode=True, charset='utf8')
    #conn.cursor(pymysql.cursors.DictCursor)
    return conn


# 새창 뜨는 경우 닫기 기능
def close_new_tabs(driver):
    tabs = driver.window_handles
    while len(tabs) != 1:
        driver.switch_to.window(tabs[1])
        driver.close()
        tabs = driver.window_handles
    driver.switch_to.window(tabs[0])