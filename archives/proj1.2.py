import finance
import serv
import sys
import numpy as np
from math import ceil

def print_menu():
   print "1) Show workers"
   print "2) Calculate betas"
   print "3) Select Ports"
   print "4) Quit"

def chunk_list(lst, chunk_len): 
    # break list into chunks
    #return [lst[i * num_chunks:(i + 1) * num_chunks] for i in range((len(lst) + num_chunks - 1) // num_chunks )]
 
    for i in range(0, len(lst), chunk_len):  
         yield lst[i:i + chunk_len] 

def calc_betas(chunked_symbols_list, thread_list):
    betas_list = []
    #send lists to workers to calculate beta 
    responses = [0] * len(thread_list) #keep track of which threads have replied
    for idx in range(len(thread_list)):
        thrd = thread_list[idx]
        #thread tuple format: conn, addr, q_rx, q_send
        thrd[2].put(("calc_betas", [2008, 1, 1], [2008, 12, 31], next(chunked_symbols_list)))

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

def beta_cacl_driver():
    pass
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
                num_workers = len(serv.thread_list)
                if num_workers == 0:
                   print "No workers"
                else:
                	chunked_list = chunk_list(finance.symbols, int(ceil(float(len(finance.symbols))/num_workers)))
                	betas_list = calc_betas(chunked_list, serv.thread_list)
            elif int(selection) == 3:
                #everything
                
            elif int(selection) == 4:
                break
    except (KeyboardInterrupt, SystemExit):
        break
serv.serv.close()
serv.stop = True
print "closing\n"
sys.exit(0)
