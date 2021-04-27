""" This file isn't used as it is not completely working
Use this idea to connect the Python backend to Resolve
Currently the connection is made in tutor/static/javascript/lesson/editorUtils """

import asyncio
import ssl
import websocket
# wss://resolve.cs.clemson.edu/teaching/Compiler?job=verify2&project=Teaching_Project
# {"name": "BeginToReason", "pkg": "User", "project": "Teaching_Project", "content": "Facility%20BeginToReason%3B%0A%20%20%20%20uses%20Integer_Ext_Theory%3B%0A%0A%20%20%20%20Operation%20Main()%3B%0A%20%20%20%20Procedure%0A%20%20%20%20Var%20I%2C%20J%2C%20K%3A%20Integer%3B%0A%0A%20%20%20%20I%20%3A%3D%202%3B%0A%20%20%20%20J%20%3A%3D%203%3B%0A%0A%20%20%20%20K%20%3A%3D%20I%3B%0A%20%20%20%20If%20(J%20%3E%20I)%20then%0A%20%20%20%20K%20%3A%3D%20J%3B%0A%20%20%20%20end%3B%0A%0A%20%20%20%20Confirm%20K%20%3D%203%3B%0A%20%20%20%20end%20Main%3B%0Aend%20BeginToReason%3B%0A", "parent": "undefined", "type": "f"}
try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print("in open func")

    def run(*args):
        ws.send("{'name': 'BeginToReason', 'pkg': 'User', 'project': 'Teaching_Project', 'content': 'Facility%20BeginToReason%3B%0A%20%20%20%20uses%20Integer_Ext_Theory%3B%0A%0A%20%20%20%20Operation%20Main()%3B%0A%20%20%20%20Procedure%0A%20%20%20%20Var%20I%2C%20J%2C%20K%3A%20Integer%3B%0A%0A%20%20%20%20I%20%3A%3D%202%3B%0A%20%20%20%20J%20%3A%3D%203%3B%0A%0A%20%20%20%20K%20%3A%3D%20I%3B%0A%20%20%20%20If%20(J%20%3E%20I)%20then%0A%20%20%20%20K%20%3A%3D%20J%3B%0A%20%20%20%20end%3B%0A%0A%20%20%20%20Confirm%20K%20%3D%203%3B%0A%20%20%20%20end%20Main%3B%0Aend%20BeginToReason%3B%0A', 'parent': 'undefined', 'type': 'f'}")
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())


def run_socket():
    ws = websocket.WebSocketApp("wss://resolve.cs.clemson.edu/teaching/Compiler?job=verify2&project=Teaching_Project",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
