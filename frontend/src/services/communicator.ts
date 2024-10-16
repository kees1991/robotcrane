import * as THREE from 'three'
import {ActuatorStates} from "../interfaces/actuatorstates";
import {Pose} from "../interfaces/pose.js";
import {OriginPosition, Position} from "../interfaces/position";
import {Dimensions} from "../interfaces/dimensions.js";

export class Communicator {
    promise: Promise<any>;
    areDimensionsInitialized: boolean;
    dimensions: Dimensions;
    pose: Pose;
    counter: number;
    exception: string;

    constructor() {
        this.promise = this.newClientPromise;

        this.areDimensionsInitialized = true;
        this.dimensions = {l_1: 1.0, l_2: 0.4, l_3: 0.4, d_4: 0.2, l_5: 0.1, l_7: 0.1};

        this.pose = {
            j_1: new THREE.Vector3(0.0, 0.0, 0.0),
            j_2: new THREE.Vector3(0.0, 0.7, 0.0),
            j_3: new THREE.Vector3(0.4, 0.7, 0.0),
            j_4: new THREE.Vector3(0.8, 0.7, 0.0),
            j_5: new THREE.Vector3(0.8, 0.5, 0.0),
            j_6: new THREE.Vector3(1.0, 0.5, 0.0),
            j_7: new THREE.Vector3(1.1, 0.5, 0.0),
            theta_0: THREE.MathUtils.degToRad(0),
            theta_1: THREE.MathUtils.degToRad(0),
            theta_2: THREE.MathUtils.degToRad(0),
            theta_3: THREE.MathUtils.degToRad(0)
        };

        this.counter = 0;
        this.exception = "";
    }

    get newClientPromise() {
        return new Promise((resolve, reject) => {
            let wsClient = new WebSocket("ws://localhost:8000/robotcrane");

            wsClient.onopen = () => {
                console.log("Connected to websocket");
                resolve(wsClient);
            };

            wsClient.onmessage = (event) => {
                console.log("Message received: " + event.data);
                resolve(wsClient);
                if (event.data.includes("Exception")) {
                    this.exception = event.data
                }
                if (event.data.includes("l_1")) {
                    this.dimensions = new Dimensions(event.data)
                    this.areDimensionsInitialized = true
                }
                if (event.data.includes("j_1")) {
                    this.counter++
                    this.pose = new Pose(event.data)
                }
            };

            wsClient.onerror = error => reject(error);
        })
    }

    private createMessage(action: string) {
        let message: Message = {action: action};
        return "{\"action\": \"" + message.action + "\"}";
    }

    private sendMessage(messageString: string) {
        this.promise
            .then(wsClient => {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch(error => alert("Connection error: " + error))
    }

    resetRobot = () => {
        let messageString = this.createMessage("reset_robot");
        this.sendMessage(messageString);
    }

    setActuatorStates = (d_1:number, theta_1:number, theta_2:number, theta_3:number, l_6:number) => {
        let message: Message = { action: "set_actuator_states"};
        let actuatorStates: ActuatorStates = { d_1: d_1, theta_1: theta_1, theta_2: theta_2, theta_3: theta_3, l_6: l_6};
        let actStatesJson = JSON.stringify(actuatorStates)

        let messageString = "{\"action\": \"" + message.action + "\", \"actuator_states\":" + actStatesJson + "}";

        this.sendMessage(messageString);
    }

    setEndEffectorPosition = (x : number, y: number, z: number, phi: number, doOpenGripper: boolean) => {
        let message: Message = { action: "set_end_effector"};
        let position: Position = { x: x, y: y, z: z, phi: phi, doOpenGripper: doOpenGripper};
        let positionJson = JSON.stringify(position)

        let messageString = "{\"action\": \"" + message.action + "\", \"end_effector_position\":" + positionJson + "}";

        this.sendMessage(messageString);
    }

    moveOrigin = (x : number, y: number, z: number, phi: number) => {
        let message: Message = { action: "set_origin"};
        let position: OriginPosition = { x: x, y: y, z: z, phi: phi};
        let positionJson = JSON.stringify(position)

        let messageString = "{\"action\": \"" + message.action + "\", \"origin_position\":" + positionJson + "}";

        this.sendMessage(messageString);
    }

    nextPose = () => {
        let messageString = this.createMessage("get_pose");
        this.sendMessage(messageString);
    }

    streamPoses = () => {
        let messageString = this.createMessage("stream_poses");
        this.sendMessage(messageString);
    }

    streamPosesNewOrg = () => {
        let messageString = this.createMessage("stream_poses_for_new_origin");
        this.sendMessage(messageString);
    }

    streamPosesControlNewOrg = () => {
        let messageString = this.createMessage("stream_poses_for_new_origin_and_control_end_effector");
        this.sendMessage(messageString);
    }
}

interface Message {
    action: string;
}