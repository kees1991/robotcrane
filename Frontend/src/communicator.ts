import * as THREE from 'three'
import {ActuatorStates} from "./Entities/actuatorstates";
import {Pose} from "./Entities/pose.js";
import {OriginPosition, Position} from "./Entities/position";
import {Dimensions} from "./Entities/dimensions.js";

export class Communicator {
    promise: Promise<any>;
    areDimensionsInitialized: boolean;
    dimensions: Dimensions;
    pose: Pose;
    counter: number;
    exception: string;

    constructor() {
        this.promise = this.newClientPromise;

        this.areDimensionsInitialized = false;
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
            // let wsClient = new WebSocket("ws://ec2-52-45-198-60.compute-1.amazonaws.com:8000/robotcrane");
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

    initRobot = () => {
        // checkSocketConnection(this.socket)
        let message: Message = { action: "initrobot"};
        let messageString = "{\"action\": \"" + message.action + "\"}";

        this.promise
            .then( wsClient =>  {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch( error => alert("Connection error: " + error) )
    }

    resetRobot = () => {
        // checkSocketConnection(this.socket)
        let message: Message = { action: "resetrobot"};
        let messageString = "{\"action\": \"" + message.action + "\"}";

        this.promise
            .then( wsClient =>  {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch( error => alert("Connection error: " + error) )
    }

    setActuatorStates = (d_1:number, theta_1:number, theta_2:number, theta_3:number, l_6:number) => {
        let message: Message = { action: "setactstates"};
        let actuatorStates: ActuatorStates = { d_1: d_1, theta_1: theta_1, theta_2: theta_2, theta_3: theta_3, l_6: l_6};
        let actStatesJson = JSON.stringify(actuatorStates)

        let messageString = "{\"action\": \"" + message.action + "\", \"act_states\":" + actStatesJson + "}";

        this.promise
            .then( wsClient => {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch( error => alert("Connection error: " + error) )
    }

    setEndEffectorPosition = (x : number, y: number, z: number, phi: number, doOpenGripper: boolean) => {
        let message: Message = { action: "setendeffector"};
        let position: Position = { x: x, y: y, z: z, phi: phi, doOpenGripper: doOpenGripper};
        let positionJson = JSON.stringify(position)

        let messageString = "{\"action\": \"" + message.action + "\", \"endeffector_position\":" + positionJson + "}";

        this.promise
            .then( wsClient => {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch( error => alert("Connection error: " + error) )
    }

    moveOrigin = (x : number, y: number, z: number, phi: number) => {
        let message: Message = { action: "moveorigin"};
        let position: OriginPosition = { x: x, y: y, z: z, phi: phi};
        let positionJson = JSON.stringify(position)

        let messageString = "{\"action\": \"" + message.action + "\", \"org_position\":" + positionJson + "}";

        this.promise
            .then( wsClient => {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch( error => alert("Connection error: " + error) )
    }

    nextPose = () => {
        // checkSocketConnection(this.socket)
        let message: Message = { action: "getpose"};
        let messageString = "{\"action\": \"" + message.action + "\"}";

        this.promise
            .then(wsClient => {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch(error => alert("Connection error: " + error))
    }

    streamPoses = () => {
        let message: Message = { action: "streamposes"};
        let messageString = "{\"action\": \"" + message.action + "\"}";

        this.promise
            .then(wsClient => {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch(error => alert("Connection error: " + error))
    }

    streamPosesNewOrg = () => {
        let message: Message = { action: "streamposesneworg"};
        let messageString = "{\"action\": \"" + message.action + "\"}";

        this.promise
            .then(wsClient => {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch(error => alert("Connection error: " + error))
    }

    streamPosesControlNewOrg = () => {
        let message: Message = { action: "streamposescontrolneworg"};
        let messageString = "{\"action\": \"" + message.action + "\"}";

        this.promise
            .then(wsClient => {
                wsClient.send(messageString);
                console.log('Sending message' + messageString)
            })
            .catch(error => alert("Connection error: " + error))
    }
}

interface Message {
    action: string;
}