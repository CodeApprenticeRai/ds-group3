import socket
import threading
import pickle
import time
import sys
import random
from Queue import Queue

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#serv.setblocking(0)
serv.settimeout(1)
serv.bind(('', 5553))
serv.listen(10)
thread_list = []
stop = False

def make_conn(conn, addr, q_rx, q_send):  
    #conn.settimeout(0.01)
    while True and stop == False:
        try:
            conn.setblocking(0)
            data = conn.recv(32000)
            if not data: 
                #break
                pass
            else:
                from_client = pickle.loads(data)
                print str(addr)
                print str(from_client)
                print
                q_send.put(from_client) 
#        except socket.timeout, e:
#            err = e.args[0]
#            if err == 'timed out':
#                pass
#            else:
#                pass
        except socket.error, e:
            pass
        if q_rx.qsize() > 0:
            pickled_data = pickle.dumps(q_rx.get())
            conn.send(pickled_data)
    conn.close()
    print 'client disconnected'

def listen(max_conn):
    while True and stop == False:
        if len(thread_list) < max_conn:
            serv.settimeout(1)
            try: 
                conn, addr = serv.accept()
                q_rx = Queue(maxsize=0)
                q_send = Queue(maxsize=0)
                temp_thread = threading.Thread(target=make_conn, args=(conn, addr, q_rx, q_send))
                thread_list.append([addr, temp_thread, q_rx, q_send])
                temp_thread.start()
            except socket.timeout:
                pass
    serv.close()    
   
listening_thread = threading.Thread(target=listen, args=(10,))         
listening_thread.start()

#while True:
#    try:
#        time.sleep(1)  
#    except (KeyboardInterrupt, SystemExit):
#        stop = True
#        serv.close()
#        print "closing"
#        sys.exit()
