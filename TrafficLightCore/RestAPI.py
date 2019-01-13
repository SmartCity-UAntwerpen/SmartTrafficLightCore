from flask import Flask, request
import multiprocessing, json, threading

app = Flask("DroneBackend")

global_backend = None


class RestApi:

    def __init__(self, backend):
        if backend is not None:
            global  global_backend
            global_backend = backend
            app.run()
        else:
            print("REST API not able to start correctly (backend is NoneType)")


@app.route("/getStatus/<tid>")
def getStatus(tid):
    return global_backend.get(tid)


@app.route("/start")
def start():
    global_backend.start()
    return "True"


@app.route("/reset")
def reset():
    global_backend.reset()
    return "True"


@app.route("/")
def test():
    return ""
