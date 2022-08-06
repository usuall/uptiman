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