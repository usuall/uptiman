import pymysql
import time

# DB 환경에 맞게 입력할것
host = "localhost"
port = "3306"
database = "healthmon"
username = "root"
password = ""
charset = "utf8"

def with_cursor(original_func):
    def wrapper(*args, **kwargs):
        # conn = sqlite3.connect('blog.db')
        # conn.row_factory = sqlite3.Row
        # c = conn.cursor()
        conn = pymysql.connect(host=host, user=username, password=password, db=database, use_unicode=True, charset='utf8')
        c = conn.cursor(pymysql.cursors.DictCursor)
        rv = original_func(c, *args, **kwargs)
        conn.commit()
        conn.close()            
        return rv
    return wrapper


@with_cursor
def get_url_list(c):
    c.execute("SELECT * FROM tb_url where url_fg = 1")
    return c.fetchall()

@with_cursor
def get_org_list(c):
    c.execute("SELECT * FROM tb_org order by org_title")
    return c.fetchall()

@with_cursor
def get_org_url_list(c, keyword):
    
    #sql = "select * from customer where category=%s and region=%s"
    #curs.execute(sql, (1, '서울'))

    sql = f"select b.* from tb_org as a right outer join tb_url as b on a.org_no = b.org_no"
    if(keyword.get('DISABLED') == True):
        sql += f" where 1=1"
    else:
        sql += f" where b.url_fg=1"

    if(keyword.get('ORG_LIST') != '전 체' and len(keyword.get('ORG_LIST')) > 0):
        sql += f" and a.org_title='{keyword.get('ORG_LIST')}'"
    if(keyword.get('SITE_TITLE')):
        sql += f" and b.url_title like '%{keyword.get('SITE_TITLE')}%'"
    if(keyword.get('SITE_URL')):
        sql += f" and b.url_addr like '%{keyword.get('SITE_URL')}%'"
    
    #sql += f" order by b.url_addr"
    print(sql)
    c.execute(sql)
    
    return c.fetchall()

# def get_org_url_list(c, org_title):
#     print('>>>>>>> '+org_title);
#     c.execute("select b.* from tb_org as a right outer join tb_url as b on a.org_no = b.org_no where b.url_fg = 1 and a.org_title=%s", org_title)
#     return c.fetchall()

# @with_cursor
# def get_org_url_list_all(c):
#     c.execute("select b.* from tb_org as a right outer join tb_url as b on a.org_no = b.org_no where b.url_fg = 1 ")
#     return c.fetchall()


@with_cursor
def add_monitoring(c, url_no, status_code, file_name):
    sql_data = ("INSERT INTO tb_monitor (url_no, status_code, file_name ) VALUES ( %s, %s, %s)")
    sql_val = (url_no, status_code, file_name)
    c.execute(sql_data, sql_val)
    

@with_cursor
def add_blog(c, subject, content):
    c.execute("INSERT INTO blog (subject, content, date) VALUES (?, ?, ?)", 
        (subject, content, time.strftime('%Y%m%d')))


@with_cursor
def read_blog(c, _id):
    c.execute("SELECT * FROM blog WHERE id=?", (_id,))
    return c.fetchone()


@with_cursor
def modify_blog(c, _id, subject, content):
    c.execute("UPDATE blog SET subject=?, content=? WHERE id=?", 
        (subject, content, _id))


@with_cursor
def remove_blog(c, _id):
    c.execute("DELETE FROM blog WHERE id=?", (_id,))