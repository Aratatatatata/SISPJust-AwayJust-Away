import threading
import time
import queue

#self made library 
import LSM9DS1
import GPS

class Sensor_Queue:
    def __init__(self):
        
        self.q = queue.Queue()

    def __send_message(self, message):
        print(message[0])
        time.sleep(1)
        print(message[1])
        self.q.put(message[0])
        self.q.put(message[1])
        
    def test(self):
        t1 = threading.Thread(target=self.__send_message, args=(["test", "1"],))
        t2 = threading.Thread(target=self.__send_message, args=(["test", "2"],))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        print(threading.current_thread().name)
        print(self.q.qsize())
