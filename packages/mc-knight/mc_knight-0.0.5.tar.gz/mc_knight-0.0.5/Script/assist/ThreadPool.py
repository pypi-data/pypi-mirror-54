from concurrent.futures import ThreadPoolExecutor
import threading, time


class WorkThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self) -> None:
        print('start run task')
        time.sleep(2)
        print('task finish\n')
        return '线程类执行完成'

def test(thread_name):
    print(thread_name, threading.current_thread().name)
    time.sleep(5)
    print('任务完成\n')
    return '线程方法执行完成'

if __name__ == '__main__':
    thread_pool = ThreadPoolExecutor(5)
    futures = []
    for i in range(7):
        thraed = WorkThread()
        # sumit(方法名，参数)
        future1 = thread_pool.submit(thraed.run)
        future2 = thread_pool.submit(test, i)
        futures.append(future1)
        futures.append(future2)

    def get_call_back(future):
        # 监听任务执行结果，当前线程一直阻塞知道有结果，但是不阻塞主线程
        print(future.result())

    for future in futures:
        #添加监听
        future.add_done_callback(get_call_back)

    print('main thread')
