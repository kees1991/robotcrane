import {ActuatorStates} from "../interfaces/actuatorstates";
import {Pose} from "../interfaces/pose.js";
import {Position} from "../interfaces/position";
import {OriginPosition} from "../interfaces/origin-positions";
import {Dimensions} from "../interfaces/dimensions.js";
import {Message} from "../interfaces/message";
import {RobotCrane} from "../interfaces/robotcrane";

export class Communicator {
    promise: Promise<any>;

    robot?: RobotCrane;

    private _shouldUpdatePose: boolean;
    private _exception?: string | undefined;

    constructor() {
        this.promise = this.newClientPromise;
        this._shouldUpdatePose = false;
    }


    get exception(): string | undefined {
        return this._exception;
    }

    set exception(value: string | undefined) {
        this._exception = value;
    }


    get shouldUpdatePose(): boolean {
        return this._shouldUpdatePose;
    }

    set shouldUpdatePose(value: boolean) {
        this._shouldUpdatePose = value;
    }

    get newClientPromise() {
        return new Promise((resolve, reject) => {
            // @ts-ignore
            let wsClient = new WebSocket(import.meta.env.VITE_API_URL);

            wsClient.onopen = () => {
                console.log("Connected to websocket");
                resolve(wsClient);
            };

            wsClient.onmessage = (event) => {
                resolve(wsClient);

                if (event.data.includes("Exception")) {
                    this._exception = event.data;
                }
                if (event.data.includes("Invalid")) {
                    this._exception = event.data;
                }
                if (event.data.includes("init_robot_data")) {
                    // Init the robot with the dimensions and a pose
                    const dataJson = JSON.parse(event.data);
                    const initDataJson = dataJson["init_robot_data"];
                    let dimensions = Dimensions.fromJson(initDataJson["dimensions"]);
                    let pose = Pose.fromJson(initDataJson["pose"]);

                    this.robot = new RobotCrane(dimensions, pose);
                    this._shouldUpdatePose = true;
                }

                if (event.data.includes("pose_data")) {
                    const dataJson = JSON.parse(event.data);
                    const poseDataJson = dataJson["pose_data"];

                    this._shouldUpdatePose = true;
                    if (this.robot != null) {
                        this.robot.pose = Pose.fromJson(poseDataJson);
                    }
                }
            };

            wsClient.onerror = error => reject(error);
        })
    }

    private sendMessage(messageString: string) {
        this.promise
            .then(wsClient => {
                wsClient.send(messageString);
                console.log('Sending message' + messageString);
            })
            .catch(error => alert("Connection error: " + error));
    }

    initializeRobot() {
        let message: Message = new Message("initialize_robot");
        this.sendMessage(message.toJsonString());
    }

    resetRobot(){
        let message: Message = new Message("reset_robot");
        this.sendMessage(message.toJsonString());
    }

    moveActuators(actuatorStatesJson: object) {
        let actuatorStates: ActuatorStates = ActuatorStates.fromJson(actuatorStatesJson);

        let message: Message = new Message("move_actuators", actuatorStates);
        this.sendMessage(message.toJsonString());
    }

    moveEndEffector(positionJson: object) {
        let position: Position = Position.fromJson(positionJson);

        let message: Message = new Message("move_end_effector", position);
        this.sendMessage(message.toJsonString());
    }

    moveOrigin(originPositionJson: object){
        let position: OriginPosition = OriginPosition.fromJson(originPositionJson);

        let message: Message = new Message("move_origin", position);
        this.sendMessage(message.toJsonString());
    }

    moveOriginControlEndEffector(originPositionJson: object) {
        let position: OriginPosition = OriginPosition.fromJson(originPositionJson);

        let message: Message = new Message("move_origin_control_end_effector", position);
        this.sendMessage(message.toJsonString());
    }
}