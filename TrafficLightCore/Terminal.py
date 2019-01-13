import os
import signal
import threading


class Terminal(threading.Thread):

    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.shutdown_flag = threading.Event()

    def run(self):

        print("Starting default traffic light configuration")

        print("Type \"help\" for info about the commands")
        while not self.shutdown_flag.is_set():
            text = input("# ")
            if text == "exit":
                self.stop()
            elif text == "help":
                print("HELP:\nstart\nreset\nstop\nstatus\nmanual\nstopall\nexit")
            elif text == "start":
                self.backend.start()
                print("Traffic lights started")
            elif text == "reset":
                self.backend.reset()
                print("Traffic lights reset")
            elif text == "stop":
                id = input("Id: ")
                self.backend.stop(id)
                print("Traffic light with id {} stopped!".format(id))
            elif text == "status":
                status = self.backend.status()
                print(status)
            elif text == "manual":
                leave = 0
                print("Commands: RED,GREEN,OFF,exit")
                id = input("Id: ")
                while leave == 0:
                    text = input("M# ")
                    if text == "GREEN":
                        self.backend.manualState(id,"GREEN")
                    elif text == "RED":
                        self.backend.manualState(id, "RED")
                    elif text == "OFF":
                        self.backend.manualState(id,"OFF")
                    elif text == "exit":
                        print("Leaving manual mode")
                        leave = 1
            elif text == "stopall":
                print("Stopping all traffic lights")
                self.backend.kill()

    def stop(self):
        self.backend.deleteAll()
        self.shutdown_flag.set()
        os.kill(os.getpid(), signal.SIGUSR1)
