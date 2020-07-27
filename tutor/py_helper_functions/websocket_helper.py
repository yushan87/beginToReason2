import asyncio
import ssl
import websocket
from websocket import create_connection


def hello():
    print("preparing...")
    ws = websocket.create_connection("wss://resolve.cs.clemson.edu/teaching/Compiler?job=verify2&project=Teaching_Project", sslopt={"cert_reqs": ssl.CERT_NONE})
    print("sending")
    ws.send({"name": "BeginToReason", "pkg": "User", "project": "Teaching_Project", "content": "Facility%20BeginToReason%3B%0A%20%20%20%20uses%20Integer_Ext_Theory%3B%0A%0A%20%20%20%20Operation%20Main()%3B%0A%20%20%20%20Procedure%0A%20%20%20%20Var%20I%2C%20J%2C%20K%3A%20Integer%3B%0A%0A%20%20%20%20I%20%3A%3D%202%3B%0A%20%20%20%20J%20%3A%3D%203%3B%0A%0A%20%20%20%20K%20%3A%3D%20I%3B%0A%20%20%20%20If%20(J%20%3E%20I)%20then%0A%20%20%20%20K%20%3A%3D%20J%3B%0A%20%20%20%20end%3B%0A%0A%20%20%20%20Confirm%20K%20%3D%203%3B%0A%20%20%20%20end%20Main%3B%0Aend%20BeginToReason%3B%0A", "parent": "undefined", "type": "f"})
    print("sent")
    print("receiving")
    result = ws.recv()
    print("Received '%s'" % result)
    ws.close()
