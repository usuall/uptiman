# mysql 
import pymysql

def dbconn():
    return pymysql.connect(host='localhost', user='root', password='', db='healthmon', charset='utf8')


