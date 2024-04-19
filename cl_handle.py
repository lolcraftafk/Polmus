import datetime
import sql_db
import socket
from datetime import datetime
import threading

class client_handle:
    def __init__(self,IP,PORT):
        self.IP = IP  # The IP address of the server
        self.PORT = PORT  # The port number of the server

        self.client_dict = {}  # A dictionary that stores client information
        self.room_dict = {}  # A dictionary that stores information about the room
        self.room_count = 0  # A variable that keeps track of the number of rooms
        self.app_state = ""  # A variable that stores the current state of the app
        self.name_dict = {}  # A dictionary that stores client names
        self.server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # A socket object that uses IPv4 and TCP protocol

        self.server_socket.bind((self.IP, self.PORT))  # Binds the socket to the IP address and port number
        self.server_socket.listen()  # Starts listening for client connections

        self.server_socket_LEAVE = socket.socket(socket.AF_INET,
                                                 socket.SOCK_STREAM)  # A socket object that uses IPv4 and TCP protocol
        self.server_socket_LEAVE.bind(
            (self.IP, self.PORT + 1))  # Binds the socket to the IP address and a different port number
        self.server_socket_LEAVE.listen()  # Starts listening for clients that have left a room

        self.info_lst = []  # A list that stores information about the room
        self.info_dict = {}  # A dictionary that stores the above list for each client

        # Starts a new thread for each new client that connects to the server
        t1 = threading.Thread(target=self.new_client)
        t1.start()

    # Define a function called new_client that takes self as an argument
    def new_client(self):
        # Start an infinite loop
        while True:
            # Accept an incoming client connection and assign the client socket and IP address
            # to self.client_object and self.client_ip, respectively
            self.client_object, self.client_ip = self.server_socket.accept()
            # Create a new thread t1 that runs the log_or_sign function in the background
            t1 = threading.Thread(target=self.log_or_sign)
            t1.start()
            # Add the client socket to the client_dict dictionary and set its value to "name"
            self.client_dict[self.client_object] = "name"

    # Define a function called log_or_sign
    def log_or_sign(self):
        # Assign self.client_object to client_object and initialize some variables
        client_object = self.client_object
        clname = ""
        clpas = ""
        clnewname = ""
        clnewpas = ""
        clMAC = ""

        # Start an infinite loop
        while True:
            # Set end to False
            end = False
            # Receive data from the client socket and decode it into a string
            log_or_sign = client_object.recv(1024).decode()
            # Send the string "v1" back to the client socket after encoding it
            client_object.send("v1".encode())

            # Check if the client has sent a "log" command
            if log_or_sign == "log":
                # Loop over the range 0 to 3
                for i in range(4):
                    # If i equals 0, receive the client's username and send the string "v2" back to the client socket
                    if i == 0:
                        clname = client_object.recv(1024).decode()
                        client_object.send("v2".encode())
                    # If i equals 1, receive the client's password and send the string "v2" back to the client socket
                    elif i == 1:
                        clpas = client_object.recv(1024).decode()
                        client_object.send("v2".encode())
                    # If i equals 2, receive the client's MAC address
                    elif i == 2:
                        clMAC = client_object.recv(1024).decode()
                    # If i equals 3, check the username, password, and MAC address with the SQL database
                    # If they match, send the string "true" back to the client socket, add the client socket
                    # to the name_dict dictionary, call the anonymous_name function, set end to True, and break the loop
                    # If they do not match, send the string "false" back to the client socket
                    else:
                        if sql_db.check_password(clname, clpas, clMAC):
                            client_object.send("true".encode())
                            self.name_dict[client_object] = clname
                            self.anonymous_name(client_object)
                            end = True
                            break
                        else:
                            client_object.send("false".encode())
                if end:
                    break

            # Check if the client has sent a "sign" command
            elif log_or_sign == "sign":
                # Loop over the range 0 to 3
                for i in range(4):
                    # If i equals 0, receive the new username and send the string "v" back to the client socket
                    if i == 0:
                        clnewname = client_object.recv(1024).decode()
                        client_object.send("v".encode())
                    # If i equals 1, receive the new password and send the string "v"
                    elif i == 1:
                        clnewpas = client_object.recv(1024).decode()
                        client_object.send("v".encode())
                    # If i equals 2, receive the new client's MAC address send the string "v"
                    elif i == 2:
                        clMAC = client_object.recv(1024).decode()

                    # If i equals 3, check the username, password, and MAC address with the SQL database
                    # If they match, send the string "true" back to the client socket, add the client socket
                    # to the sql and wait to get a new commend from the client (login or sign in)
                    # If they do not match, send the string "false" back to the client socket
                    else:
                        if sql_db.add_new_user(clnewname, clnewpas, clMAC):
                            client_object.send("true".encode())
                            break
                        else:
                            client_object.send("false".encode())

    def room_state(self, client_object):
        # If the room count is less than 2, the client can join the room
        if self.room_count < 2:
            client_object.send("1".encode())
            return True
        # If the room count is 2 or more, the client cannot join the room
        client_object.send("X".encode())
        return True

    def anonymous_name(self, client_object):
        # Receive the anonymous name from the client
        anonymous_name = client_object.recv(1024).decode()
        # Add the client's socket object and anonymous name to the client dictionary
        self.client_dict[client_object] = anonymous_name
        # Check if the client can join the room
        self.room_state(client_object)
        # Choose whether to call the history or the chatroom for the client
        self.callhis_or_room(client_object)

    def callhis_or_room(self, client_object, s=""):
        # Check if the argument "s" is "state"
        if s == "state":
            # Call the room_state function with client_object as the argument
            self.room_state(client_object)

        # Set con variable to empty string
        con = ""

        # Set the "running" variable to True
        self.running = True

        # Loop until the running variable is False
        while self.running:
            # Set the app_state variable to "home"
            self.app_state = "home"

            # Receive a message from the client and decode it
            con = client_object.recv(1024).decode()

            # If the message is "room", break the loop
            if "room" == con:
                break

            # If the message is "state", call the room_state function with client_object as the argument
            if con == "state":
                self.room_state(client_object)

            # Otherwise, set the app_state variable to "his"
            else:
                self.app_state = "his"

                # If the message is "his", send "v3" to the client and receive a new message
                if con == "his":
                    client_object.send("v3".encode())
                    con = client_object.recv(1024).decode()

                # If the message is "room" or "state", break the loop
                if "room" == con or "state" == con:
                    break

                # If the message contains the word "read", remove it
                if "read" in con:
                    con = con.replace("read", "")

                # Get the last calls from the database for the given number
                top = sql_db.last_calls(con[0], con[1:])

                # If there are any calls in the top variable, send them to the client
                if top is not None:
                    # If there are more than 4 calls, remove the oldest one
                    if len(top) > 4:
                        top.pop()

                    # Join the calls into a string with a comma separator and send it to the client
                    str = ', '.join(top)
                    client_object.send(str.encode())
                # If there are no calls in the top variable, send "x" to the client
                else:
                    client_object.send("x".encode())

        # If "room" is in the message received from the client
        if "room" in con:
            # If there is room for another client in the chat room, call the room function with client_object as the argument
            if not self.room(client_object):
                self.callhis_or_room(client_object, "state")
        # Otherwise, call the room_state function with client_object as the argument
        else:
            self.callhis_or_room(client_object, "state")

    def room(self, client_object):
        # check if the room has less than 2 clients
        if self.room_count < 2:
            # get current time
            today = datetime.now()

            # send a "v" message to client
            client_object.send("v".encode())
            # wait for client response
            client_object.recv(1024)

            # get client name
            name = self.name_dict[client_object]
            # add client to the room dictionary
            self.room_dict[client_object] = name

            # increase room count
            self.room_count += 1

            # create a list of information about the call
            info_lst = [today.strftime("%d/%m/%Y"), today.strftime("%H:%M:%S"), today.strftime("%H:%M:%S"),
                        self.client_dict[client_object]]
            # add the call to the SQL database
            sql_db.add_call(self.room_dict[client_object], info_lst)

            # add the call information to the info dictionary
            self.info_dict[client_object] = info_lst

            # set the app state to "1"
            self.app_state = "1"

            return True
        else:
            # if the room has 2 clients, send an "x" message to the client
            client_object.send("x".encode())
            return False

    def leaving(self):
        # Wait for a client to connect to the LEAVE socket
        self.client_object_L1, self.client_ip = self.server_socket_LEAVE.accept()

    def left(self):
        # Get the current datetime
        today = datetime.now()

        # Get the client objects in the room
        info = list(self.room_dict.keys())

        # Update the end time in the database for each client in the room
        sql_db.update_time(self.room_dict[info[0]], self.info_dict[info[0]], today.strftime("%H:%M:%S"))
        sql_db.update_time(self.room_dict[info[1]], self.info_dict[info[1]], today.strftime("%H:%M:%S"))

        # Close the client connections
        info[0].close()
        info[1].close()

        # Wait for another client to connect to the LEAVE socket
        self.client_object_L2, self.client_ip = self.server_socket_LEAVE.accept()

        # Close the previous LEAVE socket client connections
        self.client_object_L1.close()
        self.client_object_L2.close()

        # Reset the server state
        self.app_state = ""
        self.room_count = 0
        self.room_dict = {}
        self.info_dict = {}






