import cv2
import pyautogui
import numpy as np
import pyaudio
import socket
import pickle
import struct


class Mic_Client:
    def __init__(self, server_ip, PORT=6666, audio_format=pyaudio.paInt16, channels=1, rate=44100, frame_chunk=4096):
        # Initialize instance variables with the given parameters
        self.PORT = PORT
        self.server_ip = server_ip
        self.audio_format = audio_format
        self.channels = channels
        self.rate = rate
        self.frame_chunk = frame_chunk

        # Set send_running flag to False by default
        self.send_running = False

        self.recv_audio = pyaudio.PyAudio()
        self.send_audio = pyaudio.PyAudio()

    def mic_socket(self):
        # Create a new socket and connect it to the server IP and port
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.server_ip, self.PORT))
        # Save the connection socket as an instance variable
        self.connection = client_socket

    def send_mic(self):
        # Start sending audio data to the server
        if not self.send_running:
            # Open a new audio stream for recording and start sending data
            stream = self.send_audio.open(format=self.audio_format, channels=self.channels, rate=self.rate, input=True,
                                          frames_per_buffer=self.frame_chunk)
            # The stream is used to read audio data from the local microphone in chunks of self.frame_chunk frames,
            # which will be sent to the server.

            self.send_running = True
            while self.send_running:
                # Read audio data from the stream and send it to the server
                self.connection.send(stream.read(self.frame_chunk))
        else:
            print("mic already running!")

    def receive_mic(self):
        # Receive audio data from the server and play it back
        stream = self.recv_audio.open(format=self.audio_format, channels=self.channels, rate=self.rate, output=True,
                                      frames_per_buffer=self.frame_chunk)
        # stream is used to play back the received audio data from the server in chunks of self.frame_chunk frames.
        # The received audio data is continuously read from the network connection
        running = True
        while running:
            # Receive audio data from the server and write it to the audio stream for playback
            data = self.connection.recv(self.frame_chunk)
            stream.write(data)

    def stop_sending(self):
        # Stop sending audio data
        self.send_running = False

    def close_con(self):
        # Close the connection socket
        self.connection.close()


class CameraClient:
    # The __init__ method is called when an instance of the class is created
    def __init__(self, server_ip, PORT_cam=8888):
        # Initialize the instance variables with the arguments passed in
        self.PORT_cam = PORT_cam
        self.server_ip = server_ip
        self.running = True
        self.connection = None

    # Establishes a socket connection with the camera server
    def cam_socket(self, ):
        # Create a TCP socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to the camera server using the IP address and port number
        client_socket.connect((self.server_ip, self.PORT_cam))
        # Save the connection object as an instance variable
        self.connection = client_socket

    # Returns the connection object
    def get_con(self):
        return self.connection

    # Receives frames from the camera server and displays them on the screen
    def receive(self):
        # Calculate the size of the payload that contains the frame data
        payload_size = struct.calcsize('>L')
        data = b""
        break_loop = False
        while True:
            # Receive data from the camera server
            while len(data) < payload_size:
                received = self.connection.recv(4096)
                # If the connection is closed, break the loop
                if received == b'':
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            # Extract the size of the frame data from the payload
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]

            # Receive the frame data from the camera server
            while len(data) < msg_size:
                data += self.connection.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Decode the frame data and display it on the screen
            try:
                frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                cv2.imshow("camera", frame)
                # Wait for a key press, and break the loop if the spacebar is pressed
                if cv2.waitKey(1) == 32:
                    break
            except pickle.UnpicklingError as e:
                # Handle the exception here
                print(f"Error unpickling frame data: {e}")

    def send_cam(self):
        # Set the 'running' flag to True to indicate that the camera is currently streaming
        self.running = True
        # Set the encoding parameters for the video stream
        encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        # Set the resolution for the video stream
        x_res = 1024
        y_res = 576
        # Open the camera and set its resolution
        camera = cv2.VideoCapture(0)
        camera.set(3, x_res)
        camera.set(4, y_res)

        # Continuously read frames from the camera and send them to the server
        while self.running:
            # Capture a frame from the camera
            ret, frame = camera.read()
            # Flip the frame horizontally
            frame = cv2.flip(frame, 1)
            # Compress the frame using JPEG encoding
            result, frame = cv2.imencode('.jpg', frame, encoding_parameters)
            # Serialize the compressed frame using pickle
            data = pickle.dumps(frame, 0)
            # Calculate the size of the serialized frame data
            size = len(data)
            # Send the serialized frame data to the server
            try:
                self.connection.sendall(struct.pack('>L', size) + data)
            except ConnectionResetError:
                # If the connection is reset, release the camera and set 'running' to False
                camera.release()
                running = False
            except ConnectionAbortedError:
                # If the connection is aborted, release the camera and set 'running' to False
                camera.release()
                running = False
            except BrokenPipeError:
                # If the connection is broken, release the camera and set 'running' to False
                camera.release()
                running = False

    def stop_sending(self):
        # Set the 'running' flag to False to stop the camera stream
        self.running = False

    def close_con(self):
        # Close the connection to the server
        self.connection.close()


class ScreenClient:
    def __init__(self, server_ip, PORT=7777):
        self.PORT = PORT
        self.server_ip = server_ip
        self.running = True

    def screen_socket(self):
        # Creates a TCP/IP socket object using IPv4 addressing
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connects the socket to the server's IP address and port number
        client_socket.connect((self.server_ip, self.PORT))

        # Stores the socket object in the connection attribute of the class
        self.connection = client_socket

    def get_con(self):
        # Returns the connection attribute
        return self.connection

    def receive_screen(self):
        # Calculates the size of the message header that contains the size of the incoming frame data
        payload_size = struct.calcsize('>L')
        # Initializes an empty bytes object to store the incoming frame data
        data = b""
        break_loop = False

        # Continuously receives frame data until the loop is broken
        while True:
            # Receiving data in chunks of 4096 bytes
            while len(data) < payload_size:
                received = self.connection.recv(4096)
                # Breaks out of the loop if the received data is empty
                if received == b'':
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            # Extracts the message header that contains the size of the incoming frame data
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            # Unpacks the message header to get the size of the incoming frame data
            msg_size = struct.unpack(">L", packed_msg_size)[0]

            # Receiving the rest of the frame data in chunks of 4096 bytes
            while len(data) < msg_size:
                received = self.connection.recv(4096)
                data += received

            # Extracts the frame data from the received data
            frame_data = data[:msg_size]
            data = data[msg_size:]

            # Decodes the frame data using pickle
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

            # Decodes the image data and displays it in a window named "sharescreen"
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow("sharescreen", frame)

            # Breaks out of the loop if the spacebar key is pressed
            if cv2.waitKey(1) == 32:
                break

            # Closes the window and exits the loop if it is closed by the user
            if cv2.getWindowProperty("sharescreen", cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyAllWindows()

    def send_screen(self):
        # Set the encoding parameters for JPEG images
        encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        # Start the screen sharing loop
        self.running = True
        while self.running:
            # Set the resolution of the screen capture
            y_res = 576
            x_res = 1024

            # Capture a screenshot using the PyAutoGUI library
            screen = pyautogui.screenshot()
            frame = np.array(screen)

            # Convert the frame to the correct color space
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Resize the frame to the desired resolution
            frame = cv2.resize(frame, (x_res, y_res), interpolation=cv2.INTER_AREA)

            # Encode the frame as a JPEG image
            result, frame = cv2.imencode('.jpg', frame, encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)

            # Send the frame to the server
            try:
                self.connection.sendall(struct.pack('>L', size) + data)
            except ConnectionResetError:
                # If the connection is reset, set running to False to exit the loop
                self.running = False
            except ConnectionAbortedError:
                # If the connection is aborted, set running to False to exit the loop
                self.running = False
            except BrokenPipeError:
                # If the pipe is broken, set running to False to exit the loop
                self.running = False

    def stop_sending(self):
        # Set the 'running' flag to False to stop the screen stream
        self.running = False

    def close_con(self):
        # Close the connection to the server
        self.connection.close()
