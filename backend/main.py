from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
import json

from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

from backend.app.models.RobotCrane import RobotCrane
from backend.app.services.RobotPoseStreamer import RobotPoseStreamer
from backend.app.services.RobotUpdateHelper import set_actuator_states, set_end_effectors, set_new_origin, get_pose
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

    robot = RobotCrane()

    try:
        while True:
            robot = await process_request(robot, websocket)

    except WebSocketDisconnect:
        websocket_api.disconnect(websocket)


async def process_request(robot: RobotCrane, websocket: WebSocket):
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
                robot = RobotCrane()
                await websocket_api.send_message(websocket, "True")

            case RobotTask.set_actuator_states:
                is_done = set_actuator_states(robot, json_data["actuator_states"])
                await websocket_api.send_message(websocket, is_done)

            case RobotTask.set_end_effector:
                is_done = set_end_effectors(robot, json_data["end_effector_position"])
                await websocket_api.send_message(websocket, is_done)

            case RobotTask.set_origin:
                is_done = set_new_origin(robot, json_data["origin_position"])
                await websocket_api.send_message(websocket, is_done)

            case RobotTask.get_pose:
                pose = get_pose(robot)
                await websocket_api.send_message(websocket, pose)

            case RobotTask.stream_poses:
                streamer = RobotPoseStreamer(websocket, websocket_api)
                await streamer.stream_poses(robot)

            case RobotTask.stream_poses_for_new_origin:
                streamer = RobotPoseStreamer(websocket, websocket_api)
                await streamer.stream_poses_for_new_origin(robot)

            case RobotTask.stream_poses_for_new_origin_and_control_end_effector:
                streamer = RobotPoseStreamer(websocket, websocket_api)
                await streamer.stream_poses_for_new_origin_and_control_end_effector2(robot)

            case _:
                raise ValueError("Invalid action")

    except KeyError as e:
        print(f"KeyError: {e}")
        await websocket_api.send_message(websocket, f"Invalid request")
    except ValueError as e:
        print(f"ValueError: {e}")
        await websocket_api.send_message(websocket, f"Invalid request: {e}")

    return robot
