import finance
import serv
import sys
import numpy as np
from math import ceil
import threading
import time

import time
import itertools
from Queue import Queue

def port_select1(betas_list, q1):
    a = itertools.combinations(betas_list, 4)
    for _ in xrange(0, int(210)):
        try:
            cand_port = next(a)
        except StopIteration:
            print "combination error"
            break
        beta_sum = sum(n for _, n in cand_port)
        if (beta_sum >= 4):
            while q1.qsize() > 50:            
               time.sleep(1)
            q1.put(cand_port)

def print_menu():
   print "1) Show workers"
   print "2) Calculate betas"
   print "3) Select Portfolios"
   print "4) Quit"

def chunk_list(lst, chunk_len): 
    # break list into chunks
    for i in range(0, len(lst), chunk_len):  
         yield lst[i:i + chunk_len] 

def calc_betas(chunked_symbols_list, thread_list):
    betas_list = []
    #send lists to workers to calculate beta 
    responses = [0] * len(thread_list) #keep track of which threads have replied
    for idx in range(len(thread_list)):
        thrd = thread_list[idx]
        #thread tuple format: conn, addr, q_rx, q_send
        thrd[2].put(("calc_betas", [2010, 1, 1], [2010, 12, 31], next(chunked_symbols_list)))

    #get all responses
    len_thread_list = len(thread_list)
    while sum(responses) < len_thread_list:
        for idx in range(len_thread_list):
            thrd = thread_list[idx]
            #thread tuple format: conn, addr, q_rx, q_send
            if thrd[3].qsize() > 0:
                responses[idx] = 1
                betas_list += thrd[3].get()
    return betas_list

def beta_calc_driver(num_workers):
    #calc betas
    chunked_list = chunk_list(finance.symbols, int(ceil(float(len(finance.symbols))/num_workers)))
    return calc_betas(chunked_list, serv.thread_list)

def distr_backtest(num_workers, betas_list, thread_list, q1):
    continue_iter = True
    num_sent = 0
    #get 50 portfolios and send out to each worker for backtesting
    responses = [0] * num_workers
    port_results_list = []
    fh = open("./testResults.csv", "w")
    while continue_iter:
        #every worker gets a list of 100 portfolios
        for idx in range(num_workers):
            port_test_list = []
            for _ in range(10):   #sets batch size sent to workers
                if q1.qsize() > 0:
                    port_test_list.append(q1.get())
            #backtest_list(start_date_arr, end_date_arr, port_list, sharpe_threshold) format
            
            if len(port_test_list) > 0:
                thread_list[idx][2].put(("backtest", [2012, 1, 1], [2012, 12, 31], port_test_list, 1.5))
                num_sent += 1
            else:
                continue_iter = False   

        #get responses
        while sum(responses) < num_sent:
            for idx in range(num_workers):
                thrd = thread_list[idx]
                #thread tuple format: conn, addr, q_rx, q_send
                if thrd[3].qsize() > 0:
                    responses[idx] = 1
                    port_results_list += thrd[3].get()
        
        print port_results_list
        for line in port_results_list:
            temp = ",".join(line[0]) + "," + str(line[1]) + "," +str(line[2]) + "\n"
            fh.writelines(temp)
        #reset for next loop
        responses = [0] * num_workers
        port_results_list = []
        num_sent = 0
    fh.close()

betas_list = []
while True:
    try:
        print_menu()
        selection = raw_input()
        if selection.isdigit():
            if int(selection) == 1:
                #distribute and calc betas
                #connected workers
                for thrd in serv.thread_list:
                    print "addr: %s" % (thrd[0],)
            elif int(selection) == 2:
                #calc betas
                t1 = int(round(time.time() * 1000))
                num_workers = len(serv.thread_list)
                if num_workers == 0:
                   print "No workers"
                else:
                	betas_list = beta_calc_driver(num_workers)
                t2 = int(round(time.time() * 1000))
                print "Time (S): %f" % int((t2 - t1) / 1000.0)
            elif int(selection) == 3:
                #do everything
                t1 = int(round(time.time() * 1000))
                num_workers = len(serv.thread_list)
                if num_workers == 0:
                   print "No workers"
                else:
                    betas_list = beta_calc_driver(num_workers)
                    q1 = Queue(maxsize=0)
                    t = threading.Thread(target=port_select1, args=(betas_list, q1))
                    t.start()
                    distr_backtest(num_workers, betas_list, serv.thread_list, q1)
                    t2 = int(round(time.time() * 1000))
                    print "Time (S): %f" % int((t2 - t1) / 1000.0)
            elif int(selection) == 4:
                break
    except (KeyboardInterrupt, SystemExit):
        break
serv.serv.close()
serv.stop = True
print "closing\n"
sys.exit(0)
