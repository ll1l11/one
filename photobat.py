#coding=utf-8
"""多线程更新数据"""

import threading, Queue, time, json

from httptoolkit import HttpToolkit

domain = "10.0.0.11:9100"

class Producer(threading.Thread):
    def __init__(self, queue):
        super(Producer, self).__init__()
        self.queue = queue
        
    def run(self):
        httptool = HttpToolkit()
        ids_url = "http://%s/photo/get-from-rr-ids" % domain
        
        while True:
            if self.queue.qsize() < 50:
                res = httptool.get(ids_url)
                ids = json.loads(res)["data"]
                print ids
            
                for rr_id in ids:
                    self.queue.put(rr_id)
            time.sleep(1)
            

class Consumer(threading.Thread):
    def __init__(self, queue, thread_name=None):
        super(Consumer, self).__init__(name=thread_name)
        self.daemon = True
        self.queue = queue
    
    def run(self):
        while True:
            rr_id = self.queue.get()
            url = "http://%s/photo/get-from-rr?rr_id=%d" % (domain, rr_id)
            httptool = HttpToolkit()
            res = httptool.get(url)
            print "%s %s %s" % (self.getName(), rr_id, res)
            if '"code": 0' not in res:
                time.sleep(1)
            self.queue.task_done()

def main():
    queue = Queue.Queue()
    Producer(queue).start()
    time.sleep(3)
    for i in range(3):
        thread_name = "thread-%d" % i
        Consumer(queue, thread_name=thread_name).start()

if __name__ == "__main__":
    main()
