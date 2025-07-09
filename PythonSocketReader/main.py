"""
Made by Dhruv

Program Briefing :
This program is used to provide a simple GUI for the user to connect and control the ESP8266 through the Client object.

Program Flow:
1) Setup all variables.
2) prepare UpdateThread.
3) Configure the cwd (ControlWindow).
4) Connect to the Server.
5) start the thread.
6) Display the GUI.
"""

# Imports
import tkinter.simpledialog
from ControlProgram import ControlWindow
from ControlPacket import ControlPacket
from WiFiSocket import WiFiSocket
from threading import Thread
from time import sleep
from os import system
import tkinter
import ctypes

# Initializing ControlWindow
cwd: ControlWindow = ControlWindow("Control Program", "400x480", "lightblue")

# Thank you Copilot ----- Checks if the program is launched as an administrator since without that, I won't allow TextInput because handling String commands is dangerous and can reset the ESP8266 if not done correctly.
if ctypes.windll.shell32.IsUserAnAdmin():
    cwd.enable_text_input()
else:
    cwd.disable_text_input()

# A tracker packet which is responsible for reporting the current status of hardware.
packet: ControlPacket = ControlPacket()

# An update thread which will update all the variables of the program.
UpdateThreadFlag: bool = True
UpdateThread: Thread | None = None

# Initializing WiFiSocket
ip: str | None = tkinter.simpledialog.askstring("Input IP Address", "Enter the IPAddress of your ESP8266")  # Take the IP Address of the Server from the user.
if isinstance(ip, str) is True:
    Client: WiFiSocket = WiFiSocket(ip, 80)
else:
    print("IP Address is not given.")
    exit(0)

# Functions
def generate_control_packet(cl: WiFiSocket) -> None:
    global packet
    data: bytes | None = cl.receive_data(9)
    if data == None:
        return

    temperature: int           = int.from_bytes(data[0:2], byteorder="big", signed=False)
    humidity: int              = int.from_bytes(data[2:4], byteorder="big", signed=False)
    Light: int                 = int.from_bytes(data[4:6], byteorder="big", signed=False)
    RELAY1: bool               = bool(data[6])
    RELAY2: bool               = bool(data[7])
    AUTOMODE: bool             = bool(data[8])

    packet.set(RELAY1, RELAY2, AUTOMODE, temperature, humidity, Light)

def update_packet(event = None) -> None:
    global UpdateThreadFlag, Client, cwd, packet
    while UpdateThreadFlag:
        Client.send_data(b"G00.")
        generate_control_packet(Client)
        cwd.update_variables(packet)
        cwd.update()
        sleep(0.200)
UpdateThread = Thread(target=update_packet, daemon=True)  # Create the Thread object with the update packet function as its Runnable.

# This function will trigger whenever the TextInput event triggers.
def TextInputFunc(event = None) -> None:
    global Client

    send_str = cwd.TextInputVar.get()
    send_str.replace("\n", "")
    send_str += "."

    Client.send_data( b"S" )
    Client.send_data( send_str.encode("ascii") )

    cwd.clear_entry_text()

# This function is responsible for successfully exiting from the program.
def shutdown() -> None:
    global UpdateThreadFlag, Client

    UpdateThreadFlag = False
    Client.close()


# Configuring CWD
cwd.assign_button_command("RELAY1", lambda: Client.send_data(b"R10."))
cwd.assign_button_command("RELAY2", lambda: Client.send_data(b"R20."))
cwd.assign_button_command("AutoMode", lambda: Client.send_data(b"A00."))
cwd.bind_entry_command("<Return>", TextInputFunc)
cwd.set_exit_function(shutdown)

# Main Program Loop
Client.connect()
print("Connected to Server.")
UpdateThread.start()
cwd.start_loop()
