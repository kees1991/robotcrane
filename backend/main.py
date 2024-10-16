from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
import json

from backend.app.views.RobotResource import RobotResource
from backend.app.views.RobotTask import RobotTask

app = FastAPI()


class WebSocketAPI:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        robot = app.__getattribute__("robot_resource")
        dimensions = robot.get_robot_dimensions()
        print(f"Connected, initializing robot with dimensions: \n {dimensions}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        print(f"Disconnected, resetting robot")

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)


websocket_api = WebSocketAPI()


@app.websocket("/robotcrane")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_api.connect(websocket)

    try:
        while True:
            try:
                data = await websocket.receive_text()
                print(f"Message received from client: {data}")

                # Convert request to json
                json_data = json.loads(data)

                # Extract action from request
                requested_action = json_data["action"]

                # Map to Enum
                action = RobotTask[requested_action]

                # Get the robot resource object
                robot_resource = app.__getattribute__("robot_resource")

                # Handle action
                match action:
                    case RobotTask.reset_robot:
                        robot_resource = RobotResource()
                        app.__setattr__("robot_resource", robot_resource)
                        await websocket_api.send_message("True", websocket)

                    case RobotTask.set_actuator_states:
                        requested_actuator_states = json_data["actuator_states"]

                        is_done = robot_resource.set_actuator_states(requested_actuator_states)
                        await websocket_api.send_message(is_done, websocket)

                    case RobotTask.set_end_effector:
                        requested_end_effector = json_data["end_effector_position"]

                        is_done = robot_resource.set_end_effectors(requested_end_effector)
                        await websocket_api.send_message(is_done, websocket)

                    case RobotTask.set_origin:
                        requested_origin = json_data["origin_position"]

                        is_done = robot_resource.set_new_origin(requested_origin)
                        await websocket_api.send_message(is_done, websocket)

                    case RobotTask.get_pose:
                        pose = robot_resource.get_pose()
                        await websocket_api.send_message(pose, websocket)

                    case RobotTask.stream_poses:
                        await robot_resource.stream_pose(websocket)

                    case RobotTask.stream_poses_for_new_origin:
                        await robot_resource.stream_pose_new_origin(websocket)

                    case RobotTask.stream_poses_for_new_origin_and_control_end_effector:
                        await robot_resource.stream_pose_controlled_new_origin(websocket)

                    case _:
                        raise ValueError("Invalid action")

            except KeyError as e:
                print(f"KeyError: {e}")
                await websocket.send_text(f"Invalid request")

    except WebSocketDisconnect:
        websocket_api.disconnect(websocket)


@app.on_event("startup")
def on_startup():
    robot_resource = RobotResource()
    app.__setattr__("robot_resource", robot_resource)
