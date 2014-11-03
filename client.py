import socket
import time 
import sys 

seqNum = 1
UDP_IP = sys.argv[1] 
UDP_PORT = 1078 
MESSAGE =  "{} {:.6f}".format(seqNum,time.time())  

print "UDP target IP:", UDP_IP
print "UDP target port:", UDP_PORT
print "message:",MESSAGE

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(MESSAGE,(UDP_IP, UDP_PORT))
data, addr = sock.recvfrom(1024)
print "Server response: ",data 


