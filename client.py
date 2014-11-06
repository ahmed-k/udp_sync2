import socket
import time 
import sys 
import threading 

SEQNUM = 1
f = open('client_logfile.txt','w',0) 
UDP_IP = sys.argv[1] 
UDP_PORT = 1078 
LIST_INDEX=0
SOCK = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
SOCK.settimeout(10) 
last_eight=[[None,None] for _ in range(8)] 

def smooth_theta(lasteight):
 print lasteight
 smallest_rtt = lasteight[0][0]  
 print "Smallest Rtt:",smallest_rtt
 desired_index = 0  
 for i in lasteight:  
  	if i[0] != None and i[0] < smallest_rtt:
         print "i[0]",i[0]
   	 smallest_rtt = i[0]  
   	 desired_index = lasteight.index(i) 
 return lasteight[desired_index][1] 	 

def calculate(arr,t0):
 global LIST_INDEX 
 global last_eight 
 global f
 t3 = float(arr[1]) 
 t2 = float(arr[2]) 
 t1 = float(arr[3])  
 rtt = (t2-t3)+(t0-t1)
 theta = rtt/2 
 print "Server response: ",arr 
 print "RTT: ", rtt
 print "Theta: ", theta 
 f.write("Successful Interaction:\n")
 f.write("Server response: " + str(arr)+"\n")
 f.write("RTT: " + str(rtt)+"\n")
 f.write("Theta: " + str(theta)+"\n") 
 last_eight[LIST_INDEX] = [rtt,theta] 
 theta = smooth_theta(last_eight)
 corrected = t0 + theta
 f.write("Client Uncorrected Time: " + "{:.6f}".format(t0)+"\n")
 f.write("Client Corrected   Time: " + "{:.6f}".format(corrected)+"\n")    
 f.write("Smoothed Theta: {:.6f}\n".format(theta))
 LIST_INDEX = (LIST_INDEX + 1) % 8
 
def sendRequest(): 
 message  =  "{} {:.6f}".format(SEQNUM,time.time())  
 print "UDP target IP:", UDP_IP
 print "UDP target port:", UDP_PORT
 print "message:",message 
 try:   
  SOCK.sendto(message ,(UDP_IP,UDP_PORT))
  data, addr = SOCK.recvfrom(1024)
  t0 = time.time()
  return (data.split(),addr,t0) 
 except socket.timeout:   
  f.write("Unsuccessful Interaction: " + str(SEQNUM)+"\n") 
  return None, None,None 
  
def timedRequest():
 global SEQNUM 
 threading.Timer(10.0, timedRequest).start()  
 arr, addr,t0 = sendRequest() 
 if (arr != None): 
  serverSeqNum = int(arr[0]) 
  if (serverSeqNum == SEQNUM and arr != None):  
   calculate(arr,t0) 
  else:
   print "rejected out of sync packet"
   f.write("Unsuccessful Interaction: " + str(SEQNUM)+"\n") 
   arr, addr,t0 = sendRequest() 
   if arr != None: 
    calculate(arr,t0) 
 SEQNUM = SEQNUM  + 1

timedRequest() 
