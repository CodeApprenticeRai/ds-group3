import socket
import pickle
import time
import random
import sys
from Queue import Queue
import threading
import finance

stop = False
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))

def make_conn(q_rx, q_send):
    while True and stop == False:
        try:
            client.setblocking(0)
            data = client.recv(4096)
            if not data: 
                #break
                pass
            else:
                from_client = pickle.loads(data)
                print str(from_client)
                print 
                q_send.put(from_client) 
        except socket.error, e:
            pass
        

        if q_rx.qsize() > 0:
            pickled_data = pickle.dumps(q_rx.get())
            client.send(pickled_data)
    client.close()
    print 'client disconnected'


q_rx = Queue(maxsize=0)
q_send = Queue(maxsize=0)
data_thread = threading.Thread(target=make_conn, args=(q_rx, q_send))
data_thread.start()
while True:
   try:
        time.sleep(1)  
        if q_send.qsize() > 0:
            data = q_send.get()
            if data[0] == "calc_betas":
                betas_list = finance.calcAllBetas2(data[1], data[2], data[3])
                print betas_list
                q_rx.put(betas_list)
   except (KeyboardInterrupt, SystemExit):
        stop = True
        client.close()
        print "closing"
        sys.exit()
