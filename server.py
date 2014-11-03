import socket
import time 

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP,UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024)
	reception_time = time.time() 
	print reception_time
	print "received message:", data 
	arr = data.split()
	reply = "{} {} {} {}".format(arr[0],arr[1],reception_time,time.time())
	sock.sendto(reply, addr) 
	
