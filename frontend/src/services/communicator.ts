import * as THREE from 'three'
import { ActuatorStates } from "../interfaces/actuatorstates";
import { Pose } from "../interfaces/pose.js";
import { Position } from "../interfaces/position";
import { OriginPosition } from "../interfaces/origin-positions";
import { Dimensions } from "../interfaces/dimensions.js";
import {Message} from "../interfaces/message";

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
        // @ts-ignore
        this.dimensions = {l_1: 1.0, l_2: 0.4, l_3: 0.4, d_4: 0.2, l_5: 0.1, l_7: 0.1};
        // TODO fix this?

        this.pose = {
            j_1: new THREE.Vector3(0.0, 0.0, 0.0),
            j_2: new THREE.Vector3(0.0, 0.7, 0.0),
            j_3: new THREE.Vector3(0.4, 0.7, 0.0),
            j_4: new THREE.Vector3(0.8, 0.7, 0.0),
            j_5: new THREE.Vector3(0.8, 0.5, 0.0),
            j_6: new THREE.Vector3(0.9, 0.5, 0.0),
            j_7: new THREE.Vector3(1.0, 0.5, 0.0),
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
            // @ts-ignore
            let wsClient = new WebSocket(import.meta.env.VITE_API_URL);

            wsClient.onopen = () => {
                console.log("Connected to websocket");
                resolve(wsClient);
            };

            wsClient.onmessage = (event) => {
                resolve(wsClient);
                if (event.data.includes("Exception")) {
                    this.exception = event.data
                }
                if (event.data.includes("Invalid")) {
                    this.exception = event.data
                }
                if (event.data.includes("l_1")) {
                    const json = JSON.parse(event.data)
                    this.dimensions = new Dimensions(json['l_1'],json['l_2'],json['l_3'],-json['d_4'], json['l_5'], json['l_7'])
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

    private sendMessage(messageString: string) {
        this.promise
            .then(wsClient => {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch(error => alert("Connection error: " + error))
    }

    resetRobot = () => {
        let message: Message = new Message("reset_robot");
        this.sendMessage(message.toJsonString());
    }

    getPose = () => {
        let message: Message = new Message("get_pose");
        this.sendMessage(message.toJsonString());
    }

    moveActuators = (d1: number, theta1: number, theta2: number, theta3: number, l6: number) => {
        let actuatorStates: ActuatorStates = new ActuatorStates(d1, theta1, theta2, theta3, l6);

        let message: Message = new Message("move_actuators", actuatorStates);
        this.sendMessage(message.toJsonString());
    }

    moveEndEffector = (x : number, y: number, z: number, phi: number, doOpenGripper: boolean) => {
        let position: Position = new Position(x, y, z, phi, doOpenGripper);

        let message: Message = new Message("move_end_effector", position);
        this.sendMessage(message.toJsonString());
    }

    moveOrigin = (x : number, y: number, z: number, phi: number) => {
        let position: OriginPosition = new OriginPosition(x, y, z, phi);

        let message: Message = new Message("move_origin", position);
        this.sendMessage(message.toJsonString());
    }

    moveOriginControlEndEffector = (x : number, y: number, z: number, phi: number) => {
        let position: OriginPosition = new OriginPosition(x, y, z, phi);

        let message: Message = new Message("move_origin_control_end_effector", position);
        this.sendMessage(message.toJsonString());
    }
}