import time
import wrapt_timeout_decorator 

start = time.time()
# デコレータでタイムアウトの秒数を設定
@wrapt_timeout_decorator.timeout(dec_timeout=5)
def func():
    while True:
        pass

if __name__ == '__main__':
    try:
        func()
    except:
        pass
    
    print("time :", time.time() - start)