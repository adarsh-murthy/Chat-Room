# Chat-Room
Instructions to run the chat program using socket:
This program is written in python 2.7.7

1. Run the server program with port number and the file containing authorized users (with password) as an argument. 
2. This sets the server to listen for incoming clients
3. Run the client program on a different terminal with server IP address and port number as arguments
4. The client is prompted to enter the username and password
5. If wrong combination is entered thrice, the client is blocked for time blocked_time(can be changed in the code)
6. If the entered username is already connected, the client is not allowed to connect.
7. If the correct combination is entered, the client is "logged in" and connected to the server through a stable socket.
8. Once logged in, the list of commands appears and the client can send any of those commands to the server.
9. If an incorrect command is entered, the server sends to enter valid command.
10. At the same time, the client will receive messages that other clients send(through the server of course) and displays them.
11. The connection is closed and the program end when the client logs out.
12. You can start up amy number of clients and connect them to the server(Though, only the 10 authorized will actually connect) and perform all the commands.  
#Threads are used to handle all the clients concurrently   
#select function is used to wait for either keyboard input or receive message from the socket(client from server or vice versa)   
#A master timer runs as a parallel thread that keeps checking for inactive clients. CLients are automatically logged out if they are inactive for a time greater than the time out.  
#try blocks are used to catch the exceptions, keyboard interrupts and errors to exit gracefully.  
#Also note that, while using the wholast command, the client has to enter the time in seconds along with the command.  
