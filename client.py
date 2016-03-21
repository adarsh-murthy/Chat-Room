import socket
import sys
from sys import argv
import time
import threading
import select

script, server_IP_address, server_port_no = argv

serverport = int(server_port_no)

#Creating socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



server_address = (server_IP_address, serverport)
print >>sys.stderr, 'connecting to %s at port number %s' % server_address
#Connecting to listening socket of server
sock.connect(server_address)
data = ""
data1 = ""
data2 = ""
port = ""
port_no = ""
try:
    	count = 0
	#Getting Authorized by server
    	data1 = sock.recv(1024)	    	
	if data1 != "Enter username":
		#you are in the blocked list
		print data1
	else:
		#not in blocked list, general authentication
		while data1[:8] != "Welcome!":
			count = count + 1
			if count == 4:
				print """You have entered the wrong combination thrice
	Please try again in 60 seconds"""
				sock.close()
				break		
			message1 = raw_input(data1+" : ")
		    	#print >>sys.stderr, 'sending "%s"' % message
		    	sock.sendall(message1)
			data2 = sock.recv(1024)
			message2 = raw_input(data2+" : ")
			sock.sendall(message2)	
			data1 = sock.recv(1024)
			#Duplicate user
			if data1 =="User already logged in\nEnter a different username":
				print "This username is already in use\nExiting now!"
				count = count - 1
				continue

			if data1[:15] == "You are blocked":
				print data1
				sock.close()
				break
		#Check for successful authentication
		
		try:
			if data1[:8] == "Welcome!":		    	
				#Getting new port and connecting to that for sustained connection
				print "---------------------------logged in--------------------------------"
				p=data1[8:8+5]
				if p == "":
					p = int(sock.recv(1024))
				
				sock.close()
				newsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				server_address = (server_IP_address, int(p))
						
				newsock.connect(server_address)
				r = newsock.recv(1024)
				print r
				flag5 = 1
				#Giving the various commands to the server
				while flag5:
					inputready, outputready,exceptrdy = select.select([0, newsock], [],[])
				
					for i in inputready:
					    if i == 0:
						data = sys.stdin.readline().strip()
						if data == "logout":
							print "logging out"
							newsock.close()
							flag5 = 0
							break
						if data: 
							newsock.sendall(data)
					    elif i == newsock:
						data = newsock.recv(1024)
						
						if not data:
						    print 'Shutting down.'
						    
						    break
						#If inactive till time out
						elif data == "You took too long":
							print "Inactive for too long, logging out"
							newsock.close()
							flag5 = 0
							break
						else:
						    sys.stdout.write(data + '\n')
						    sys.stdout.flush()
			
		#Catching exceptions within stable socket			    
		except KeyboardInterrupt:
			print '\nInterrupted.'
			newsock.close()
			
#Catching exception in intitial connection			
except KeyboardInterrupt:
	print "\nClosing now"			
				
finally:
	
	sock.close()
