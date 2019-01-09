
from threading import Thread
import socket  # For Building TCP Connection


scan_result = []
def scanner(ip, ports):
    global scan_result
     # scan_result is a variable stores our scanning result

    for port in ports.split(','):  # remember the ports are separated by a comma in this format 21,22,..

        try:  # we will try to make a connection using socket library for EACH one of these ports

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            output = sock.connect_ex((ip, int(
                port)))  # connect_ex This function returns 0 if the operation succeeded,  and in our case operation succeeded means that
            # the connection happens whihch means the port is open otherwsie the port could be closed or the host is unreachable in the first place.

            if output == 0:
                print (port)
                print (type(port))
                scan_result.append(port) # add open port to list
                print ("done")

            else:
                pass
            sock.close()

        except Exception :
            pass
def get_ports(ip,range_range):
    # function for get all ip,s from ip range
    global scan_result
    start_start = range_range.split("-")[0]
    end_end= range_range.split("-")[1]
    print(start_start)
    print(end_end)
    start=int(float(start_start))
    end=int(float(end_end))
    print ("done")
    print(type(start_start))
    print(type(end_end))
    threads = [] # threads list
    counter1=0
    for i in range(start,end):
        # for loop to add threads to list and start every 10 threads
        counter1=counter1+ 1
        i=str(i)
        t = Thread(target=scanner, args=(ip,i,))
        threads.append(t)
        if counter1 >= 10:
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            del threads[:]
            counter1 = 0

    return scan_result
# return result
#print(scan_result)
