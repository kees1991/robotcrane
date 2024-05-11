import asyncio
import json

import websockets

from Interface.RobotResource import RobotResource


async def json_handler(websocket, path):
    global resource

    while True:
        try:
            data = await websocket.recv()
        except websockets.ConnectionClosed:
            print(f"Connection terminated")
            break

        if path == "/robotcrane":
            print("Message received from client: {}".format(data))
            jsondata = json.loads(data)

            action = jsondata["action"]
            try:
                match action:
                    case "initconnection":
                        reply = f"Data received as:  {data}!"
                        await websocket.send(reply)

                    case "initrobot":
                        resource = RobotResource()
                        dims = resource.get_robot_dimensions()
                        await websocket.send(dims)

                    case "resetrobot":
                        resource = RobotResource()
                        await websocket.send("True")

                    case "setactstates":
                        isdone = resource.set_actuator_states(jsondata["act_states"])
                        await websocket.send(isdone)

                    case "setendeffector":
                        isdone = resource.set_end_effectors(jsondata["endeffector_position"])
                        await websocket.send(isdone)

                    case "moveorigin":
                        isdone = resource.set_new_origin(jsondata["org_position"])
                        await websocket.send(isdone)

                    case "getpose":
                        pose = resource.get_pose()
                        await websocket.send(pose)

                    case "streamposes":
                        await resource.stream_pose(websocket)

                    case "streamposesneworg":
                        await resource.stream_pose_new_origin(websocket)

                    case "streamposescontrolneworg":
                        await resource.stream_pose_controlled_new_origin(websocket)

                    case _:
                        reply = f"Data received as:  {data}!"
                        await websocket.send(reply)

            except ValueError as e:
                await websocket.send("Exception: {}".format(e))

start_server = websockets.serve(json_handler, "localhost", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
