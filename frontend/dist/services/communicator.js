import * as THREE from 'three';
import { Pose } from "../interfaces/pose.js";
import { Dimensions } from "../interfaces/dimensions.js";
var Communicator = /** @class */ (function () {
    function Communicator() {
        var _this = this;
        this.resetRobot = function () {
            var messageString = _this.createMessage("reset_robot");
            _this.sendMessage(messageString);
        };
        this.setActuatorStates = function (d_1, theta_1, theta_2, theta_3, l_6) {
            var message = { action: "set_actuator_states" };
            var actuatorStates = { d_1: d_1, theta_1: theta_1, theta_2: theta_2, theta_3: theta_3, l_6: l_6 };
            var actStatesJson = JSON.stringify(actuatorStates);
            var messageString = "{\"action\": \"" + message.action + "\", \"actuator_states\":" + actStatesJson + "}";
            _this.sendMessage(messageString);
        };
        this.setEndEffectorPosition = function (x, y, z, phi, doOpenGripper) {
            var message = { action: "set_end_effector" };
            var position = { x: x, y: y, z: z, phi: phi, doOpenGripper: doOpenGripper };
            var positionJson = JSON.stringify(position);
            var messageString = "{\"action\": \"" + message.action + "\", \"end_effector_position\":" + positionJson + "}";
            _this.sendMessage(messageString);
        };
        this.moveOrigin = function (x, y, z, phi) {
            var message = { action: "set_origin" };
            var position = { x: x, y: y, z: z, phi: phi };
            var positionJson = JSON.stringify(position);
            var messageString = "{\"action\": \"" + message.action + "\", \"origin_position\":" + positionJson + "}";
            _this.sendMessage(messageString);
        };
        this.nextPose = function () {
            var messageString = _this.createMessage("get_pose");
            _this.sendMessage(messageString);
        };
        this.streamPoses = function () {
            var messageString = _this.createMessage("stream_poses");
            _this.sendMessage(messageString);
        };
        this.streamPosesNewOrg = function () {
            var messageString = _this.createMessage("stream_poses_for_new_origin");
            _this.sendMessage(messageString);
        };
        this.streamPosesControlNewOrg = function () {
            var messageString = _this.createMessage("stream_poses_for_new_origin_and_control_end_effector");
            _this.sendMessage(messageString);
        };
        this.promise = this.newClientPromise;
        this.areDimensionsInitialized = true;
        this.dimensions = { l_1: 1.0, l_2: 0.4, l_3: 0.4, d_4: 0.2, l_5: 0.1, l_7: 0.1 };
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
    Object.defineProperty(Communicator.prototype, "newClientPromise", {
        get: function () {
            var _this = this;
            return new Promise(function (resolve, reject) {
                var wsClient = new WebSocket("ws://ec2-52-90-49-194.compute-1.amazonaws.com:80/robotcrane");
                wsClient.onopen = function () {
                    console.log("Connected to websocket");
                    resolve(wsClient);
                };
                wsClient.onmessage = function (event) {
                    console.log("Message received: " + event.data);
                    resolve(wsClient);
                    if (event.data.includes("Exception")) {
                        _this.exception = event.data;
                    }
                    if (event.data.includes("l_1")) {
                        _this.dimensions = new Dimensions(event.data);
                        _this.areDimensionsInitialized = true;
                    }
                    if (event.data.includes("j_1")) {
                        _this.counter++;
                        _this.pose = new Pose(event.data);
                    }
                };
                wsClient.onerror = function (error) { return reject(error); };
            });
        },
        enumerable: false,
        configurable: true
    });
    Communicator.prototype.createMessage = function (action) {
        var message = { action: action };
        return "{\"action\": \"" + message.action + "\"}";
    };
    Communicator.prototype.sendMessage = function (messageString) {
        this.promise
            .then(function (wsClient) {
            wsClient.send(messageString);
            console.log('Sending message' + messageString);
        })
            .catch(function (error) { return alert("Connection error: " + error); });
    };
    return Communicator;
}());
export { Communicator };
