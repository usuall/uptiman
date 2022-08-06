import time
import random
from retry import retry
from wrapt_timeout_decorator import *

class Test():

    @retry(TimeoutError, tries=3, delay=1, backoff=2)
    @timeout(5)
    def worker(value):#valueの処理
        print (value),
        #1~10秒待つ.
        sleep_time = random.randrange(1, 10)
        print (":sleep_time", sleep_time)
        time.sleep(sleep_time)
        print(value, ":Done.")

    if __name__ == "__main__":
        values = [1, 2, 3]

        for value in values:
            Time = time.time()
            try:
                worker(value)
            except TimeoutError as e:
                print (e)
            finally:
                print("掛った時間", time.time() - Time)

        print ("Finish")