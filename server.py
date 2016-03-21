from sys import argv
from threading import Timer
import sys
import socket
import time
import select
import threading
socket_var = []
cl_time = {}
portFlag = True
new_port = []
Connected_user = {}
conn_clients = {}
Block_user = {}
script, port_no, filename = argv
port = int(port_no)
Block_time = 60
time_out = 30*60
offline_msg = {}
#Function that checks if client is authorized or not
def authorize (data1,data2):
	flag = 0
	if data1 in user:
		if data2 == user[data1]:
			return True
		else:
			return False
	else:
		return False	

#Timer function that checks for inactive users
def timer():
	c_u = {}
	D = []
	c_u = Connected_user
	while True:
		try:
			time.sleep(3)
			ctime = time.time()
		
			for i in Connected_user:
				if ctime - Connected_user[i] >= (time_out-1):
					print i, "is logged off"
					D.append(i)	#Getiing all the users that are inactive
					
			for i in D:	#Removing the inactive users from the global dictionaries
				if i in Connected_user:
					Connected_user.pop(i)
					conn_clients[i].sendall("You took too long!")
					conn_clients[i].close()
					conn_clients.pop(i)	
		except:
			break			
			

#Client threads that maintains stable socket with client and closes it when interaction is over	
def run_client(conn,cl_name,cl_add,p):
	
	last_seen = time.time()
	for i in offline_msg:
		if cl_name == i:
			m = offline_msg[i]
			conn.sendall("You received some messages when offline:\n")
			conn.sendall(m)
	try:
		flag5 = 1
		while flag5:
			
			inputready, outputready,exceptrdy = select.select([0, conn], [],[])	#selecting either keyboard input or client message
			
		
			for i in inputready:
			    
			    if i == 0:
				msg = sys.stdin.readline().strip()

				if msg: 
					conn.sendall(data)
			    elif i == conn:
				msg = conn.recv(1024)
				print "Received",msg,"from",cl_name	
				Connected_user[cl_name] = time.time()
				#Performing the various commands based on client message
				if msg == "whoelse":
					A = []
					j = 0
					for i in Connected_user:
						if not (i == cl_name):	
				
							A.append(i)
					A = ' '.join(A)
					conn.sendall(A)

				elif msg[:7] == "wholast":
					g = msg.split()
					p = int(g[1])
					h = []
					print len(cl_time)
					print p
					y = time.time()
					for i in cl_time:
						if (not i in cl_name) and (y - cl_time[i] <= p):
							
							h.append(i)
							
					h = ' '.join(h)
					conn.sendall(str(h))

				elif msg[:9] == "broadcast":
	
					b = msg.split()
					if b[1] == "user":
						send_users = []
						m = []
						for i in range(2,len(b)):
			
							if (b[i] in Connected_user) and not(b[i] == cl_name):
								send_users.append(b[i])
							else:
								m.append(b[i])
						m = ' '.join(m)
		
						for i in range(len(send_users)):
							if send_users[i] in Connected_user:	 
								conn_clients[send_users[i]].sendall(cl_name+":"+m)		
					
					else: 
						for i in range(len(socket_var)):
			
			
							if not(p == conn) :
								socket_var[i].sendall(cl_name+":"+msg[17:])
				elif msg[:7] == "message":
					v = msg.split()
					v1 = v[1]
					if (v1 in Connected_user) and not(v1 == cl_name):
						#v2 = v[3:]
						v2 = ' '.join(v[2:])
		
						conn_clients[v1].sendall(cl_name+": "+v2)
					elif (v1 in user) and not(v1 == cl_name):
						conn.sendall("User not online but will receive you message after next log in")
						m = ' '.join(v[2:])						
						v2 = cl_name+ ': ' + m
						offline_msg[v1] = v2

				elif msg == "logout":
					print "logging out ",cl_name
					
					Connected_user.pop(cl_name)
					
					ip = socket_var.index(conn)
					socket_var.pop(ip)
					
		
					flag5 = 0
					break

				else:
					
					conn.sendall("Enter valid command")
					continue
							
			if not msg:

				print 'Shutting down',cl_name,"...."
				Connected_user.pop(cl_name)
				
				ip = socket_var.index(conn)
				socket_var.pop(ip)
					
				break
			else:
				sys.stdout.write(msg + '\n')
				sys.stdout.flush()
	except:							#Taking care of exceptions like keyboard interrupts and errors
		print "Logging off this client"

#Opening text file with list of usernames and passwords		
txt = open(filename)


s = txt.readlines()
txt.close()

user = {}

for i in range(len(s)):
	u = s[i].split()
	user[u[0]] = u[1]	

#Starting a thread to monitor the time for all clients to check for inactivity
z = threading.Thread(target=timer)
z.setDaemon(True)
z.start()


#Creating a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1',port)
print >>sys.stderr, 'starting up on address %s at port number %s' % server_address
sock.bind(server_address)


thread = []
#Listen socket listens for incoming clients
sock.listen(10)
while True:
	try:
	    	
		# Wait for a connection
		print >>sys.stderr, 'waiting for a connection'
		
		connection, client_address = sock.accept()		#Accepting connection from client
		counter = 0
		e = time.time()			#taking down the current time
		
		flag = 0
	
       		print >>sys.stderr, 'connection from', client_address

		#Authoring the incoming client
		for j in range(3):
			connection.sendall("Enter username")
			data1 = connection.recv(1024)
			uname = data1
						
			connection.sendall("Enter password")
			data2 = connection.recv(1024)
			
			#Checking for duplicate user
			if data1 in Connected_user:
				j = j - 1
				connection.sendall("User already logged in\nEnter a different username\n")
				continue
			#Checking if user is blocked
			if (data1 in Block_user) and (e - Block_user[data1] <= Block_time):
				connection.sendall("You are blocked! You have " + str(int(Block_time - e + Block_user[uname])) + " seconds left")
				connection.close()
				break
			elif (data1 in Block_user) and (e-Block_user[data1] > Block_time):
				Block_user.pop(data1)
				
			
			if data1 and data2:
				if authorize(data1,data2):		#User logged in
					Connected_user[data1] = time.time()	#Need to connect him to a new socket for sustained connection
						
					cl_time[data1] = time.time()
					
					flag = 1
					
					s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					ser_add = ('127.0.0.1', 0)
					s1.bind(ser_add)
					
					s1.listen(1)
					p = s1.getsockname()[1]
					
					connection.sendall("Welcome!"+str(p))
					conn, cl_add = s1.accept()
					conn.sendall("*Welcome! Get ready to Chat here* \n Your options are:\n1. whoelse\n2. wholast <number>\n3. broadcast message <message>\n4. broadcast user <user>\n5. message <user> <message>\n6. logout\n")
					socket_var.append(conn)
					conn_clients[data1] = conn
					#Using client thread to handle multiple clients concurrently
					t = threading.Thread(target=run_client, args = (conn,data1,cl_add[0],p,))
					thread.append(t)
					t.start()
			
			
					break
		

		if flag == 0 and (not uname in Connected_user) and (not uname in Block_user):		
			Block_user[uname]= time.time()#if client enters wrong combination, add him to blocked users


	
		

	except socket.error, (value,message):
		print "\nCancelling connection"
	except KeyboardInterrupt:
		print "\nShutting down the server"
		break		
	finally:
		
		# Clean up the connection
		try:	
			if connection:
				connection.close()
		except:
			#print "Noone has connected yet\nClosing"
			k = 1
	
