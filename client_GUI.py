import tkinter
import customtkinter
import tkinter.messagebox
import hashlib
import threading
from PIL import Image, ImageTk
import client
from client import *
import uuid


class ClientGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Set appearance mode of custom tkinter to dark
        customtkinter.set_appearance_mode("dark")
        # Set default color theme of custom tkinter to blue
        customtkinter.set_default_color_theme("blue")

        # Set dimensions of GUI window to 600 x 700 pixels
        self.geometry("600x700")
        # Set title of GUI window to "login"
        self.title("login")

        # Initialize self.b as True
        self.b = True
        # Create the main frame of the GUI
        self.Create_frame()
        # Initialize self.name1 and self.name2 as empty strings
        self.name1 = ""
        self.name2 = ""
        # Get the IP address of the local machine
        self.IP = socket.gethostbyname(socket.gethostname())
        # Set the PORT number to 8080
        self.PORT = 8080
        # Initialize self.color as "Dark"
        self.color = "Dark"
        # Initialize self.rooms_available as an empty string
        self.rooms_available = ""
        # Initialize self.already_conn as False
        self.already_conn = False
        # Get the MAC address of the local machine
        self.mac_address = hashlib.md5((':'.join(format(x, '02x') for x in uuid.getnode().to_bytes(6, 'big'))).encode('utf-8')).hexdigest()

    def start_client(self):
        # Get the IP address of the remote machine entered by the user
        self.newsrIP = self.serverIP.get()
        # Create a client socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Attempt to connect to the remote machine using the client socket
            self.client_socket.connect((self.serverIP.get(), self.PORT))
        except OSError as e:
            # If connection fails, return False
            return False

        # If connection succeeds, set self.already_conn as True and return True
        self.already_conn = True
        return True

    def Create_frame(self):
        # Create the main frame of the GUI using custom tkinter
        self.frame = customtkinter.CTkFrame(master=self)

        # Pack the frame with specified padding and fill and expansion options
        self.frame.pack(pady=20, padx=30, fill="both", expand=True)

    def Client_Login(self):
        # This func will show the client the first screen, the login screen.
        # The screen will contain a name and password and the login button.
        # As well as the option to sign up that will take the client to the sign-up page.

        # Create a label for the login page
        label_0 = customtkinter.CTkLabel(master=self.frame, text="Login", font=("calibri", 30, "normal"),
                                         justify=tkinter.LEFT)
        label_0.pack(pady=10, padx=10)

        # Create a label for the username input
        label_name = customtkinter.CTkLabel(master=self.frame, text="Username", font=("calibri", 20, "normal"),
                                            justify=tkinter.LEFT)
        label_name.pack(pady=0, padx=10)

        # Create an entry field for the username input
        self.name_entered = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username",
                                                   font=("calibri", 15, "normal"))
        self.name_entered.pack(pady=0, padx=10)

        # Create a label for the password input
        label_pass = customtkinter.CTkLabel(master=self.frame, text="Password", font=("calibri", 20, "normal"),
                                            justify=tkinter.LEFT)
        label_pass.pack(pady=0, padx=10)

        # Create an entry field for the password input
        self.password_entered = customtkinter.CTkEntry(master=self.frame, show="*", placeholder_text="Password",
                                                       font=("calibri", 15, "normal"))
        self.password_entered.pack(pady=0, padx=10)

        # If the client has not already connected to a server, create a label for the server IP input
        if not self.already_conn:
            self.label_ip = customtkinter.CTkLabel(master=self.frame, text="Server IP", font=("calibri", 20, "normal"),
                                                   justify=tkinter.LEFT)
            self.label_ip.pack(pady=0, padx=10)

            # Create an entry field for the server IP input
            self.serverIP = customtkinter.CTkEntry(master=self.frame, placeholder_text="ServerIP",
                                                   font=("calibri", 15, "normal"))
            self.serverIP.pack(pady=0, padx=10)

        # Create a button for the login action that starts the check_stats command
        button_log = customtkinter.CTkButton(master=self.frame, text="Login", command=self.check_stats,
                                             font=("calibri", 20, "normal"))
        button_log.pack(pady=20, padx=10)

        # Create a label for displaying any warnings
        self.warning_label = customtkinter.CTkLabel(master=self.frame, text="",
                                                    font=("calibri", 15, "normal"), justify=tkinter.LEFT)
        self.warning_label.pack(pady=0, padx=10)

        # Create a label for the sign-up option
        label_sign = customtkinter.CTkLabel(master=self.frame, text="Haven't signed up yet?",
                                            font=("calibri", 20, "normal"),
                                            justify=tkinter.LEFT)
        label_sign.pack(pady=0, padx=10)

        # Create a button for sign up action that starts the sign_up command
        button_sign = customtkinter.CTkButton(master=self.frame, text="Sign up here", command=self.sign_up,
                                              font=("calibri", 20, "normal"))
        button_sign.pack(pady=0, padx=10)

        # Create the logo
        image = Image.open("Logos/logo_black.png")
        self.Logo = ImageTk.PhotoImage(image)
        self.panel = tkinter.Label(self.frame, image=self.Logo, bd=0)
        self.panel.pack()

    def sign_up(self):
        # This func will show the client the sign-up screen.
        # The screen will contain a name and password and the sign-up button.

        # Destroy the previous frame
        self.frame.destroy()

        # Set the title and create a new frame
        self.title("Sign up")
        self.Create_frame()

        # Create and pack the header label
        label_header = customtkinter.CTkLabel(master=self.frame, text="Enter your username and password here:",
                                              font=("calibri", 30, "normal"), justify=tkinter.LEFT)
        label_header.pack(pady=3, padx=10)

        # Create and pack the username label and entry widget
        label_na = customtkinter.CTkLabel(master=self.frame, text="Username", font=("calibri", 20, "normal"),
                                          justify=tkinter.LEFT)
        label_na.pack(pady=3, padx=10)

        self.na_entered = customtkinter.CTkEntry(master=self.frame, placeholder_text="Username",
                                                 font=("calibri", 15, "normal"))
        self.na_entered.pack(pady=2, padx=10)

        # Create and pack the password label and entry widget
        label_pa = customtkinter.CTkLabel(master=self.frame, text="Password", font=("calibri", 20, "normal"),
                                          justify=tkinter.LEFT)
        label_pa.pack(pady=3, padx=10)

        self.pa_entered = customtkinter.CTkEntry(master=self.frame, placeholder_text="Password", show="*",
                                                 font=("calibri", 15, "normal"))
        self.pa_entered.pack(pady=2, padx=10)

        # Create and pack the second password label and entry widget
        label_pa2 = customtkinter.CTkLabel(master=self.frame, text="Password(again)", font=("calibri", 20, "normal"),
                                           justify=tkinter.LEFT)
        label_pa2.pack(pady=3, padx=10)

        self.pa_entered2 = customtkinter.CTkEntry(master=self.frame, show="*", placeholder_text="Password",
                                                  font=("calibri", 15, "normal"))
        self.pa_entered2.pack(pady=2, padx=10)

        # Create and pack the server IP label and entry widget if it's the first time the user signs up
        if not self.already_conn:
            self.label_ip = customtkinter.CTkLabel(master=self.frame, text="Server IP", font=("calibri", 20, "normal"),
                                                   justify=tkinter.LEFT)
            self.label_ip.pack(pady=3, padx=10)

            self.serverIP = customtkinter.CTkEntry(master=self.frame, placeholder_text="Server IP",
                                                   font=("calibri", 15, "normal"))
            self.serverIP.pack(pady=2, padx=10)

        # Create and pack the warning label
        self.label_war = customtkinter.CTkLabel(master=self.frame, text="", font=("calibri", 20, "normal"),
                                                justify=tkinter.LEFT)
        self.label_war.pack(pady=10, padx=10)

        # Create and pack the sign-up button
        self.button_sign = customtkinter.CTkButton(master=self.frame, text="Sign up", command=self.add_user,
                                                   font=("calibri", 20, "normal"))
        self.button_sign.pack(pady=10, padx=10)

        # Create and pack the logo label
        image = Image.open("Logos/logo_black.png")
        self.Logo = ImageTk.PhotoImage(image)
        self.panel = tkinter.Label(self.frame, image=self.Logo, bd=0)
        self.panel.pack()

    def add_user(self):
        # Check if already connected to server
        if not self.already_conn:
            # If not, start client and check if it succeeded
            if not self.start_client():
                # If it didn't succeed, display error message
                self.label_war.configure(text="Something went wrong with the IP address...")
            else:
                # If it succeeded, remove IP address entry fields
                self.label_ip.destroy()
                self.serverIP.destroy()

        # Check if username and password were entered
        if self.na_entered.get() == "" or self.pa_entered.get() == "":
            # If not, display error message
            self.label_war.configure(text="you forgot to enter the username/password")

        # Check if username and password are the same
        if self.na_entered.get() == self.pa_entered.get():
            # If they are, display error message
            self.label_war.configure(text="the username and password must be different")

        # Check if passwords match
        if self.pa_entered.get() != self.pa_entered2.get():
            # If they don't match, display error message
            self.label_war.configure(text="the passwords arent matching:(")

        # If all checks pass, attempt to add user to server
        else:
            # Send "sign" message to server to indicate that a new user is being added
            self.client_socket.send("sign".encode())
            # Wait for acknowledgement from server
            received = self.client_socket.recv(1024).decode()

            # Get username and password entered by user
            self.newname = self.na_entered.get().encode('utf-8')
            self.newpas = self.pa_entered.get().encode('utf-8')

            # Hash username and send to server
            self.client_socket.send(hashlib.md5(self.newname).hexdigest().encode())
            # Wait for acknowledgement from server
            received = self.client_socket.recv(1024).decode()

            # Hash password and send to server
            self.client_socket.send(hashlib.md5(self.newpas).hexdigest().encode())
            # Wait for acknowledgement from server
            received = self.client_socket.recv(1024).decode()

            # Send MAC address to server
            self.client_socket.send(self.mac_address.encode())
            # Wait for acknowledgement from server
            received = self.client_socket.recv(1024).decode()

            # Check if user was added successfully
            if received != "false":
                # If successful, display success message and move to login screen
                self.label_war.configure(text="good job! now try to login,this may take a moment")
                self.frame.destroy()
                self.Create_frame()
                self.Client_Login()
            else:
                # If not successful, display error message
                self.label_war.configure(text="this username is already taken!")

    def check_stats(self):
        # check if the client is already connected to the server
        if not self.already_conn:
            # if not, try to start the client
            if not self.start_client():
                self.warning_label.configure(text="Something went wrong with the IP address...")
            else:
                # if the client is started successfully, remove some elements from the GUI
                self.label_ip.destroy()
                self.serverIP.destroy()

        # check if the user has entered a username or password
        if self.name_entered.get() == "" or self.password_entered.get() == "":
            self.warning_label.configure(text="You have entered a wrong username/password")
        else:
            # if the user has entered a username and password, send a message to the server
            self.client_socket.send("log".encode())
            received = self.client_socket.recv(1024).decode()

            # hash the username and password and send them to the server
            self.name2 = self.name_entered.get()
            self.name = self.name2.encode('utf-8')

            self.pas = self.password_entered.get().encode('utf-8')

            self.client_socket.send(hashlib.md5(self.name).hexdigest().encode())
            received = self.client_socket.recv(1024).decode()

            self.client_socket.send(hashlib.md5(self.pas).hexdigest().encode())
            received = self.client_socket.recv(1024).decode()

            # send the MAC address of the client to the server
            self.client_socket.send(self.mac_address.encode())
            received = self.client_socket.recv(1024).decode()

            # if the username and password are correct, go to the anonymous screen
            if received == "true":
                self.anonymous_screen()
                self.name = (hashlib.md5(self.name).hexdigest().encode()).decode()
            elif self.b:
                # if the username and password are incorrect, show a warning
                self.warning_label.configure(text="You have entered a wrong username/password")
                self.b = False

    def anonymous_screen(self):
        # This func will show the client the anonymous naming screen.
        # The screen will contain a place to write the name and a continue button.

        # set the size of the window and destroy the previous frame
        self.geometry("600x500")
        self.frame.destroy()

        # set the title of the window and create a new frame
        self.title("anonymous naming")
        self.Create_frame()

        # create a header label and pack it into the frame
        label_header = customtkinter.CTkLabel(master=self.frame,
                                              text="first we'll ask you to name yourself anonymously!\n"
                                                   "all for safety measures:)",
                                              font=("calibri", 24, "normal"), justify=tkinter.LEFT)
        label_header.pack(pady=3, padx=10)

        # create a label and an entry widget for entering an anonymous name and pack them into the frame
        label_an = customtkinter.CTkLabel(master=self.frame, text="enter your one time name here:",
                                          font=("calibri", 20, "normal"),
                                          justify=tkinter.LEFT)
        label_an.pack(pady=5, padx=10)

        self.an_name = customtkinter.CTkEntry(master=self.frame, placeholder_text="anonymous name",
                                              font=("calibri", 15, "normal"))
        self.an_name.pack(pady=5, padx=10)

        # create a button widget for continuing and pack it into the frame
        button_name = customtkinter.CTkButton(master=self.frame, text="continue", command=self.naming,
                                              font=("calibri", 15, "normal"))
        button_name.pack(pady=5, padx=10)

        # create a label widget for displaying any warning messages and pack it into the frame
        self.label_wr = customtkinter.CTkLabel(master=self.frame, text="", font=("calibri", 15, "normal"),
                                               justify=tkinter.LEFT)
        self.label_wr.pack(pady=3, padx=10)

        # load an image and display it in a label widget, then pack it into the frame
        image = Image.open("Logos/logo_black.png")
        self.Logo = ImageTk.PhotoImage(image)
        self.panel = tkinter.Label(self.frame, image=self.Logo, bd=0)
        self.panel.pack()

    def naming(self):
        # Checks if the anonymous name contains the user's account name or part of it
        if self.name2 in self.an_name.get():
            self.label_wr.configure(text="The anonymous name must not be your account's name or include it!")
        # Check if the anonymous name is empty, too long, or includes reserved keywords
        elif self.an_name.get() == "" or self.an_name.get() == "x" or self.an_name.get() == "v" or "room" in self.an_name.get() or self.an_name.get() == "state" or self.an_name.get() == "his":
            self.label_wr.configure(text="Sorry but the name you have chosen is unavailable!")
        # Check if the length of the anonymous name is greater than 10 characters
        elif len(self.an_name.get()) > 10:
            self.label_wr.configure(text="The name you have chosen is too long!")
        else:
            # Send the anonymous name to the server and receive the available rooms
            self.client_socket.send(self.an_name.get().encode())
            self.rooms_available = self.client_socket.recv(1024).decode()
            # Navigate to the client home page
            self.Client_Home_Page()

    def refresh(self):
        # Send a state request to the server and receive the available rooms
        self.client_socket.send("state".encode())
        self.rooms_available = self.client_socket.recv(1024).decode()
        # If Room 1 is available, enable the button to access it; otherwise, disable it
        if "1" in self.rooms_available:
            self.button_1.configure(state="normal")
        else:
            self.button_1.configure(state="disabled")

    def Client_Home_Page(self):
        # This func will show the client the home page.
        # The screen will contain a history button, enter a call button, a refresh button and the logo.

        # Change window geometry, destroy previous frame, create new frame and set window title
        self.geometry("600x380")
        self.frame.destroy()
        self.title("Home Page")
        self.Create_frame()

        # Create headline label for the page
        self.label_headline = customtkinter.CTkLabel(master=self.frame, text="welcome back to Polmus!", font=("calibri", 30, "normal"), justify=tkinter.LEFT)
        self.label_headline.place(x=113, y=25)

        # Create button for accessing call history
        self.button_his = customtkinter.CTkButton(master=self.frame, text="Call history", command=self.call_history, font=("calibri", 20, "normal"))
        self.button_his.place(x=90, y=80)

        # Create button for starting a new call
        self.button_1 = customtkinter.CTkButton(master=self.frame, text="start a new call", command=self.start_new_call, font=("calibri", 20, "normal"))
        self.button_1.place(x=300, y=80)

        # If there are no available rooms, disable the new call button
        if "1" not in self.rooms_available:
            self.button_1.configure(state="disabled")

        # Create button for refreshing the room availability status
        self.button_re = customtkinter.CTkButton(master=self.frame, text="refresh", command=self.refresh, font=("calibri", 20, "normal"))
        self.button_re.place(x=197, y=133)

        # Create label for reminding user to refresh before entering a call
        self.label_headline = customtkinter.CTkLabel(master=self.frame, text="don't forget to refresh before entering a call :)", font=("calibri", 15, "normal"),justify=tkinter.LEFT)
        self.label_headline.place(x=125, y=175)

        # Load and display Polmus logo
        image = Image.open("Logos/logo_b.png")
        self.Logo = ImageTk.PhotoImage(image)
        self.panel = tkinter.Label(self.frame, image=self.Logo, bd=0)
        self.panel.place(x=220, y=198)

        # Change the logo image based on the appearance mode
        if self.color == "light":
            image = Image.open("Logos/logo_w.png")
            self.Logo = ImageTk.PhotoImage(image)
            self.panel.configure(image=self.Logo)
            self.color = "light"

        # Create label and option menu for changing appearance mode
        self.appearance_mode_label = customtkinter.CTkLabel(self.frame, text="Appearance Mode:", anchor="w", font=("calibri", 15, "normal"))
        self.appearance_mode_label.place(x=52, y=225)
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.frame, values=["Dark", "light"], command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.place(x=50, y=255)

    def change_appearance_mode_event(self, new_appearance_mode: str):
        # check if the new appearance mode is "Dark"
        if new_appearance_mode == "Dark":
            # load the logo with black background
            image = Image.open("Logos/logo_b.png")
            self.Logo = ImageTk.PhotoImage(image)
            # update the logo panel with the new image
            self.panel.configure(image=self.Logo)
            # set the color mode to "Dark"
            self.color = "Dark"
        else:
            # load the logo with white background
            image = Image.open("Logos/logo_w.png")
            self.Logo = ImageTk.PhotoImage(image)
            # update the logo panel with the new image
            self.panel.configure(image=self.Logo)
            # set the color mode to "light"
            self.color = "light"
        # call the function to set the appearance mode of customtkinter widgets to the new appearance mode
        customtkinter.set_appearance_mode(new_appearance_mode)

    def call_history(self):
        # This func will show the client the call history screen.
        # The screen will contain the 5 latest calls that the client made and a go back screen.

        # set the geometry of the window
        self.geometry("640x500")

        # destroy the current frame and set the title of the window
        self.frame.destroy()
        self.title("call history")

        # create a new frame and set the appearance mode
        self.Create_frame()
        customtkinter.set_appearance_mode(self.color)

        # create a header label to display the title
        label_header = customtkinter.CTkLabel(master=self.frame, text="these are your last five calls:",
                                              font=("calibri", 30, "normal"), justify=tkinter.LEFT)
        label_header.place(x=15, y=5)

        # create a label to display the column headers of the table
        label_header = customtkinter.CTkLabel(master=self.frame,
                                              text="    Date         Started at     Duration     Anonymous name",
                                              font=("calibri", 23, "normal"), justify=tkinter.LEFT)
        label_header.place(x=40, y=60)

        # initialize a variable for the vertical position of the labels in the table
        yp = 1

        # loop through the five most recent calls and display their information in a table
        for i in range(1, 6):
            # send a message to the server to request call history information
            self.client_socket.send("his".encode())

            # receive a message from the server containing the call history information
            received = self.client_socket.recv(1024).decode()

            # if the server sends an "x" message,that means that that's the end of the history. break out of the loop
            if received == "x": break

            # send a message to the server requesting the i-th call history information
            self.client_socket.send((str(i) + self.name).encode())

            # receive a message from the server containing the i-th call history information
            received = self.client_socket.recv(1024).decode()

            # if the server sends an "x" message, break out of the loop
            if received == "x":
                break

            # split the received message into a list of strings
            top = received.split(",")

            # if the list is not empty, create labels to display the information in the table
            if top is not None:
                # initialize a variable for the horizontal position of the labels in the table
                xp = 0
                for j in range(4):
                    if i!= 0:
                        # if the current column is not the second column, create a label with the current text and position it in the table
                        if j != 1:
                            label_call = customtkinter.CTkLabel(master=self.frame, text=top[j],
                                                                font=("calibri", 20, "normal"), justify=tkinter.LEFT)
                            label_call.place(x=xp * 120 + 30, y=60 * yp+50)

                        # if the current column is the second column, create a label with the current text and position it in the table
                        else:
                            label_call = customtkinter.CTkLabel(master=self.frame, text=top[j],
                                                                font=("calibri", 20, "normal"), justify=tkinter.LEFT)
                            label_call.place(x=xp * 140 + 10, y=60 * yp+50)
                    else:
                        # if the current column is not the second column, create a label with the current text and position it in the table
                        if j != 1:
                            label_call = customtkinter.CTkLabel(master=self.frame, text=top[j],
                                                                font=("calibri", 20, "normal"), justify=tkinter.LEFT)
                            label_call.place(x=xp * 120 + 30, y=50 * yp)

                        # if the current column is the second column, create a label with the current text and position it in the table
                        else:
                            label_call = customtkinter.CTkLabel(master=self.frame, text=top[j],
                                                                font=("calibri", 20, "normal"), justify=tkinter.LEFT)
                            label_call.place(x=xp * 140 + 10, y=50 * yp)

                    # increment the horizontal position variable
                    xp += 1
            # increment the vertical position variable
            yp += 1

        # create a "back" button and position it in the window
        button_back = customtkinter.CTkButton(master=self.frame, text="back", command=self.Client_Home_Page, font=("calibri", 20, "normal"))
        button_back.place(x=400, y=410)

    def start_listening(self):
        # Disable the "Start Call" button
        self.startcall.configure(state="disabled")
        # Create camera, screen, and microphone clients
        self.cam = client.CameraClient(self.newsrIP)
        self.scr = client.ScreenClient(self.newsrIP)
        self.mic = client.Mic_Client(self.newsrIP)
        # Create sockets for camera, screen, and microphone
        self.cam.cam_socket()
        self.scr.screen_socket()
        self.mic.mic_socket()
        # Start threads to receive camera, screen, and microphone streams
        receive_cam = threading.Thread(target=self.cam.receive)
        receive_cam.start()
        receive_screen = threading.Thread(target=self.scr.receive_screen)
        receive_screen.start()
        receive_mic = threading.Thread(target=self.mic.receive_mic)
        receive_mic.start()
        # Create an "Exit Call" button and place it on the frame
        exit_button = customtkinter.CTkButton(master=self.frame, text="Exit call",
                                              command=self.last_screen, font=("calibri", 20, "normal"))
        exit_button.place(x=370, y=310)
        # Create a label welcoming the user to the call and place it on the frame
        label_header = customtkinter.CTkLabel(master=self.frame, text="welcome to the call :)",
                                              font=("calibri", 25, "normal"), justify=tkinter.LEFT)
        label_header.place(x=135, y=60)
        # Enable camera, screen, and microphone buttons
        self.button_camera.configure(state="normal")
        self.button_screen.configure(state="normal")
        self.button_mic.configure(state="normal")





    def start_camerastream(self):
        # Create a new thread to run the send_cam method in the background
        send_cam = threading.Thread(target=self.cam.send_cam)
        send_cam.start()

        # Create a new button to stop the camera stream, and place it on the GUI
        self.button_camera = customtkinter.CTkButton(master=self.frame, text="close camera",
                                                     command=self.stopcam, font=("calibri", 20, "normal"))
        self.button_camera.place(x=170, y=190)

    def start_audiostream(self):
        # Create a new thread to run the send_mic method in the background
        send_mic = threading.Thread(target=self.mic.send_mic)
        send_mic.start()


        # Create a new button to stop the audio stream, and place it on the GUI
        self.button_mic = customtkinter.CTkButton(master=self.frame, text="close mic", command=self.stopmic,
                                                  font=("calibri", 20, "normal"))
        self.button_mic.place(x=170, y=130)






    def start_screenshare(self):
        # Create a new thread to run the send_screen method in the background
        send_screen = threading.Thread(target=self.scr.send_screen)
        send_screen.start()
        # Create a new button to stop the screen sharing, and place it on the GUI
        self.button_screen = customtkinter.CTkButton(master=self.frame, text="close share-screen",
                                                     command=self.stopscreen, font=("calibri", 20, "normal"))
        self.button_screen.place(x=160, y=250)

    def stopcam(self):
        # Stop the camera stream
        self.cam.stop_sending()
        # Create a new button to start the camera stream, and place it on the GUI
        self.button_camera = customtkinter.CTkButton(master=self.frame, text="open camera",
                                                     command=self.start_camerastream, font=("calibri", 20, "normal"))
        self.button_camera.place(x=170, y=190)

    def stopscreen(self):
        # Stop the screen sharing
        self.scr.stop_sending()
        # Create a new button to start the screen sharing, and place it on the GUI
        self.button_screen = customtkinter.CTkButton(master=self.frame, text="open share-screen",
                                                     command=self.start_screenshare, font=("calibri", 20, "normal"))
        self.button_screen.place(x=160, y=250)

    def stopmic(self):
        # Stop the mic sharing
        self.mic.stop_sending()
        # Create a new button to start the mic sharing, and place it on the GUI
        self.button_mic = customtkinter.CTkButton(master=self.frame, text="open mic", command=self.start_audiostream,
                                                  font=("calibri", 20, "normal"))
        self.button_mic.place(x=170, y=130)

    def start_new_call(self):
        # Send a message to the server to indicate that the client wants to join a room
        self.client_socket.send("room".encode())
        # Receive the server's response and decode it
        received = self.client_socket.recv(1024).decode()

        # Destroy the current frame and create a new one for the new call
        self.frame.destroy()
        # Set the title of the new frame to "new call"
        self.title("new call")
        # Create the new frame
        self.Create_frame()
        # Set the size of the new frame
        self.geometry("600x410")

        # Create a label for the header of the new frame
        label_header = customtkinter.CTkLabel(master=self.frame, text="First, to start the call press here-->",
                                              font=("calibri", 25, "normal"), justify=tkinter.LEFT)
        # Place the label in the frame
        label_header.place(x=20, y=20)

        # Create a button for starting the call
        self.startcall = customtkinter.CTkButton(master=self.frame, text="start call", command=self.start_listening,
                                                 font=("calibri", 20, "normal"))
        # Place the button in the frame
        self.startcall.place(x=380, y=20)

        # Create a button for opening the microphone
        self.button_mic = customtkinter.CTkButton(master=self.frame, text="open mic", command=self.start_audiostream,
                                                  font=("calibri", 20, "normal"))
        # Place the button in the frame
        self.button_mic.place(x=170, y=130)
        # Disable the button initially
        self.button_mic.configure(state="disabled")

        # Create a button for opening the camera
        self.button_camera = customtkinter.CTkButton(master=self.frame, text="open camera",
                                                     command=self.start_camerastream, font=("calibri", 20, "normal"))
        # Place the button in the frame
        self.button_camera.place(x=170, y=190)
        # Disable the button initially
        self.button_camera.configure(state="disabled")

        # Create a button for opening the screen share
        self.button_screen = customtkinter.CTkButton(master=self.frame, text="open share-screen",
                                                     command=self.start_screenshare, font=("calibri", 20, "normal"))
        # Place the button in the frame
        self.button_screen.place(x=160, y=250)
        # Disable the button initially
        self.button_screen.configure(state="disabled")

        # If the server's response was "x", it means that there are no rooms available
        if received == "x":
            # Clear the rooms_available attribute
            self.rooms_available = ""
            # Return to the client's home page
            self.Client_Home_Page()
        else:
            # If the server's response was not "x", send a message to the server to indicate that the call is starting
            self.client_socket.send("starting".encode())

    def last_screen(self):
        # Set the window size
        self.geometry("600x230")

        # Connect to the server socket for leaving the room
        self.client_socket_leave = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket_leave.connect((self.newsrIP, self.PORT + 1))

        # Wait for 1 second
        self.after(1000)

        # Close the microphone, screen sharing, and camera
        self.mic.close_con()
        self.scr.close_con()
        self.cam.close_con()

        # Destroy the current frame and create a new one
        self.frame.destroy()
        self.title("leaving already:(")
        self.Create_frame()

        # Add a label to the frame to display a message
        label_header = customtkinter.CTkLabel(master=self.frame, text="The call has sadly ended:(",
                                              font=("calibri", 25, "normal"), justify=tkinter.LEFT)
        label_header.place(x=15, y=10)

        # Add another label to the frame to display a message
        label_header = customtkinter.CTkLabel(master=self.frame, text="But we will be happy to see you next time!",
                                              font=("calibri", 25, "normal"), justify=tkinter.LEFT)
        label_header.place(x=15, y=50)

        # Add a button to exit the application
        close_button = customtkinter.CTkButton(master=self.frame, text="Exit POLMUS",
                                               command=self.end_by_cl, font=("calibri", 20, "normal"))
        close_button.place(x=350, y=100)

        # Add the logo to the frame
        image = Image.open("Logos/logo_b_s.png")
        self.Logo = ImageTk.PhotoImage(image)
        self.panel = tkinter.Label(self.frame, image=self.Logo, bd=0)
        self.panel.place(x=10, y=95)

        # Change the color of the logo if the theme is light
        if self.color == "light":
            image = Image.open("Logos/logo_w_s.png")
            self.Logo = ImageTk.PhotoImage(image)
            self.panel.configure(image=self.Logo)
            self.color = "light"

    def end_by_cl(self):
        # Closes the GUI
        self.destroy()
        self.end()

    def end(self):
        # Closes the GUI
        self.mainloop()


client2 = ClientGUI()
client2.Client_Login()
client2.end()
