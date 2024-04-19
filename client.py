import cv2
import pyautogui
import numpy as np
import pyaudio
import socket
import pickle
import struct


class MicCamClient:
    def __init__(self, server_ip, PORT=6666, audio_format=pyaudio.paInt16, channels=1, rate=44100, frame_chunk=4096):
        self.PORT = PORT
        self.server_ip = server_ip
        self.audio_format = audio_format
        self.channels = channels
        self.rate = rate
        self.frame_chunk = frame_chunk
        
        self.send_running = False
        
        self.recv_audio = pyaudio.PyAudio()
        self.send_audio = pyaudio.PyAudio()

    def __init__(self, server_ip, PORT_cam=8888):
        
        self.PORT_cam = PORT_cam
        self.server_ip = server_ip
        self.running = True
        self.connection = None

    
    def cam_socket(self, ):
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        client_socket.connect((self.server_ip, self.PORT_cam))
        
        self.connection = client_socket

    
    def get_con(self):
        return self.connection

    
    def receive(self):
        
        payload_size = struct.calcsize('>L')
        data = b""
        break_loop = False
        while True:
            
            while len(data) < payload_size:
                received = self.connection.recv(4096)
                
                if received == b'':
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]

            
            while len(data) < msg_size:
                data += self.connection.recv(4096)
            frame_data = data[:msg_size]
            data = data[msg_size:]

            
            try:
                frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
                frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                cv2.imshow("camera", frame)
                
                if cv2.waitKey(1) == 32:
                    break
            except pickle.UnpicklingError as e:
                
                print(f"Error unpickling frame data: {e}")

    def send_cam(self):
        
        self.running = True
        
        encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        
        x_res = 1024
        y_res = 576
        
        camera = cv2.VideoCapture(0)
        camera.set(3, x_res)
        camera.set(4, y_res)

        
        while self.running:
            
            ret, frame = camera.read()
            
            frame = cv2.flip(frame, 1)
            
            result, frame = cv2.imencode('.jpg', frame, encoding_parameters)
            
            data = pickle.dumps(frame, 0)
            
            size = len(data)
            
            try:
                self.connection.sendall(struct.pack('>L', size) + data)
            except ConnectionResetError:
                
                camera.release()
                running = False
            except ConnectionAbortedError:
                
                camera.release()
                running = False
            except BrokenPipeError:
                
                camera.release()
                running = False

    def stop_sending(self):
        
        self.running = False

    def close_con(self):
        
        self.connection.close()

# class Mic_Client:
#     def __init__(self, server_ip, PORT=6666, audio_format=pyaudio.paInt16, channels=1, rate=44100, frame_chunk=4096):
        
        

#     def mic_socket(self):
        
#         client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         client_socket.connect((self.server_ip, self.PORT))
        
#         self.connection = client_socket

#     def send_mic(self):
        
#         if not self.send_running:
            
#             stream = self.send_audio.open(format=self.audio_format, channels=self.channels, rate=self.rate, input=True,
#                                           frames_per_buffer=self.frame_chunk)
            
            

#             self.send_running = True
#             while self.send_running:
                
#                 self.connection.send(stream.read(self.frame_chunk))
#         else:
#             print("mic already running!")

#     def receive_mic(self):
        
#         stream = self.recv_audio.open(format=self.audio_format, channels=self.channels, rate=self.rate, output=True,
#                                       frames_per_buffer=self.frame_chunk)
        
        
#         running = True
#         while running:
            
#             data = self.connection.recv(self.frame_chunk)
#             stream.write(data)

#     def stop_sending(self):
        
#         self.send_running = False

#     def close_con(self):
        
#         self.connection.close()



class ScreenClient:
    def __init__(self, server_ip, PORT=7777):
        self.PORT = PORT
        self.server_ip = server_ip
        self.running = True

    def screen_socket(self):
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
        client_socket.connect((self.server_ip, self.PORT))

        
        self.connection = client_socket

    def get_con(self):
        
        return self.connection

    def receive_screen(self):
        
        payload_size = struct.calcsize('>L')
        
        data = b""
        break_loop = False

        
        while True:
            
            while len(data) < payload_size:
                received = self.connection.recv(4096)
                
                if received == b'':
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            
            msg_size = struct.unpack(">L", packed_msg_size)[0]

            
            while len(data) < msg_size:
                received = self.connection.recv(4096)
                data += received

            
            frame_data = data[:msg_size]
            data = data[msg_size:]

            
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")

            
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow("sharescreen", frame)

            
            if cv2.waitKey(1) == 32:
                break

            
            if cv2.getWindowProperty("sharescreen", cv2.WND_PROP_VISIBLE) < 1:
                cv2.destroyAllWindows()

    def send_screen(self):
        
        encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

        
        self.running = True
        while self.running:
            
            y_res = 576
            x_res = 1024

            
            screen = pyautogui.screenshot()
            frame = np.array(screen)

            
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            
            frame = cv2.resize(frame, (x_res, y_res), interpolation=cv2.INTER_AREA)

            
            result, frame = cv2.imencode('.jpg', frame, encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)

            
            try:
                self.connection.sendall(struct.pack('>L', size) + data)
            except ConnectionResetError:
                
                self.running = False
            except ConnectionAbortedError:
                
                self.running = False
            except BrokenPipeError:
                
                self.running = False

    def stop_sending(self):
        
        self.running = False

    def close_con(self):
        
        self.connection.close()
