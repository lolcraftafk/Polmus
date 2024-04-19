import cl_handle
import socket
import threading


class Server_Handle:
    def __init__(self):
        self.SERVER_IP = "0.0.0.0"
        print(self.SERVER_IP)
        self.SERVER_PORT = 8080
        self.cl = cl_handle.client_handle(self.SERVER_IP, self.SERVER_PORT)
        self.running = True
        self.conn()

    # Initialize server sockets
    def socket_init(self, PORT):
        # Create a TCP socket object
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the server socket to the server IP address and specified port number
        server_socket.bind((self.SERVER_IP, PORT))
        # Set the server socket to listen for incoming connections
        server_socket.listen()
        return server_socket

    # Connect the server to clients
    def conn(self):
        # Set up server sockets for camera, screen, and microphone data
        self.server_socket_cam = self.socket_init(8888)  # return of socket object
        self.server_socket_screen = self.socket_init(7777)
        self.server_socket_mic = self.socket_init(6666)

        # Start the server
        self.start()

    # Finish a call and close the sockets
    def finish_call(self):
        # Start the wait for leaving protocol
        self.cl.leaving()
        # Set the server state to not running
        self.running = False
        # Close the server sockets
        self.server_socket_screen.close()
        self.server_socket_cam.close()
        self.server_socket_mic.close()
        # Send a left message to clients using the client_handle object
        self.cl.left()
        # Reconnect the camera, screen, and microphone servers
        self.conn()
        # Restart the process
        self.start()

    # Receive and send data between clients
    def receive_and_send(self, client_get, client_send):
        # Continuously receive and send data while the server is running
        while self.running:
            # Receive data from the client
            data_receive = client_get.recv(4096)
            # Send data to the other client
            client_send.send(data_receive)

    # Start the server
    def start(self):
        # Set the server state to running
        self.running = True
        # Continuously accept incoming connections and set up threads to receive and send data between clients
        while True:
            # Accept incoming camera, screen, and microphone connections from client 1 and client 2
            self.client_cam_object1, client_ip = self.server_socket_cam.accept()
            self.client_screen_object1, client_ip = self.server_socket_screen.accept()
            self.client_mic_object1, client_ip = self.server_socket_mic.accept()

            self.client_cam_object2, client_ip = self.server_socket_cam.accept()
            self.client_screen_object2, client_ip = self.server_socket_screen.accept()
            self.client_mic_object2, client_ip = self.server_socket_mic.accept()

            # Set up threads to receive and send data between clients
            t1 = threading.Thread(target=self.receive_and_send, args=(self.client_cam_object1, self.client_cam_object2))
            t1.start()
            t2 = threading.Thread(target=self.receive_and_send, args=(self.client_screen_object1, self.client_screen_object2))
            t2.start()
            t3 = threading.Thread(target=self.receive_and_send, args=(self.client_mic_object1, self.client_mic_object2))
            t3.start()

            t4 = threading.Thread(target=self.receive_and_send, args=(self.client_cam_object2, self.client_cam_object1))
            t4.start()
            t5 = threading.Thread(target=self.receive_and_send, args=(self.client_screen_object2, self.client_screen_object1))
            t5.start()
            t6 = threading.Thread(target=self.receive_and_send, args=(self.client_mic_object2, self.client_mic_object1))
            t6.start()

            self.finish_call()


server = Server_Handle()
# Start the server
