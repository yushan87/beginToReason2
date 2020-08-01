import asyncio
import ssl
import certifi
import websockets

ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())


async def hello():
    print("in hello")
    uri = "wss://resolve.cs.clemson.edu/teaching/Compiler?job=verify2&project=Teaching_Project"
    async with websockets.connect(
            uri=uri, ssl=ssl_context
    ) as websocket:
        print("sending")
        await websocket.send({"name": "BeginToReason", "pkg": "User", "project": "Teaching_Project", "content": "Facility%20BeginToReason%3B%0A%20%20%20%20uses%20Integer_Ext_Theory%3B%0A%0A%20%20%20%20Operation%20Main()%3B%0A%20%20%20%20Procedure%0A%20%20%20%20Var%20I%2C%20J%2C%20K%3A%20Integer%3B%0A%0A%20%20%20%20I%20%3A%3D%202%3B%0A%20%20%20%20J%20%3A%3D%203%3B%0A%0A%20%20%20%20K%20%3A%3D%20I%3B%0A%20%20%20%20If%20(J%20%3E%20I)%20then%0A%20%20%20%20K%20%3A%3D%20J%3B%0A%20%20%20%20end%3B%0A%0A%20%20%20%20Confirm%20K%20%3D%203%3B%0A%20%20%20%20end%20Main%3B%0Aend%20BeginToReason%3B%0A", "parent": "undefined", "type": "f"})
        print("sent")
        await websocket.recv()
        print("receiving")
