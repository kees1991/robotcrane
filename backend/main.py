from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import json

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from backend.app.models.RobotCrane import RobotCrane
from backend.app.services.RobotPoseStreamer import RobotPoseStreamer
from backend.app.views.RobotResource import RobotResource
from backend.app.views.RobotTask import RobotTask
from backend.app.views.WebSocketAPI import WebSocketAPI

# Instantiate a webapp
app = FastAPI()

# Frontend
app.mount("/assets", StaticFiles(directory="frontend/static/assets"), name="static")
templates = Jinja2Templates(directory="frontend/static")


@app.get("/", response_class=HTMLResponse)
async def serve_html(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Backend
websocket_api = WebSocketAPI()


@app.websocket("/robotcrane")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_api.connect(websocket)

    robot_resource = RobotResource()

    try:
        while True:
            robot_resource = await process_request(robot_resource, websocket)

    except WebSocketDisconnect:
        websocket_api.disconnect(websocket)


async def process_request(robot_resource: RobotResource, websocket: WebSocket):
    try:
        data = await websocket_api.receive_message(websocket)
        print(f"Message received from client: {data}")

        # Convert request to json
        json_data = json.loads(data)

        # Extract action from request and map to enum
        requested_action = json_data["action"]
        action = RobotTask[requested_action]

        # Handle action
        match action:
            case RobotTask.reset_robot:
                robot_resource = RobotResource()
                await websocket_api.send_message(websocket, "True")

            case RobotTask.set_actuator_states:
                requested_actuator_states = json_data["actuator_states"]

                is_done = robot_resource.set_actuator_states(requested_actuator_states)
                await websocket_api.send_message(websocket, is_done)

            case RobotTask.set_end_effector:
                requested_end_effector = json_data["end_effector_position"]

                is_done = robot_resource.set_end_effectors(requested_end_effector)
                await websocket_api.send_message(websocket, is_done)

            case RobotTask.set_origin:
                requested_origin = json_data["origin_position"]

                is_done = robot_resource.set_new_origin(requested_origin)
                await websocket_api.send_message(websocket, is_done)

            case RobotTask.get_pose:
                pose = robot_resource.get_pose()
                await websocket_api.send_message(websocket, pose)

            case RobotTask.stream_poses:
                streamer = RobotPoseStreamer(websocket, websocket_api)
                await streamer.stream_poses(robot_resource.robot)

            case RobotTask.stream_poses_for_new_origin:
                streamer = RobotPoseStreamer(websocket, websocket_api)
                await streamer.stream_poses_for_new_origin(robot_resource.robot)

            case RobotTask.stream_poses_for_new_origin_and_control_end_effector:
                streamer = RobotPoseStreamer(websocket, websocket_api)
                await streamer.stream_poses_for_new_origin_and_control_end_effector(robot_resource.robot)

            case _:
                raise ValueError("Invalid action")

    except KeyError as e:
        print(f"KeyError: {e}")
        await websocket_api.send_message(f"Invalid request")

    return robot_resource
