import * as THREE from 'three';
import { Pose } from "./Entities/pose.js";
import { Dimensions } from "./Entities/dimensions.js";
var Communicator = /** @class */ (function () {
    function Communicator() {
        var _this = this;
        this.initRobot = function () {
            // checkSocketConnection(this.socket)
            var message = { action: "initrobot" };
            var messageString = "{\"action\": \"" + message.action + "\"}";
            _this.promise
                .then(function (wsClient) {
                wsClient.send(messageString);
                console.log('Sending message' + messageString);
            })
                .catch(function (error) { return alert("Connection error: " + error); });
        };
        this.resetRobot = function () {
            // checkSocketConnection(this.socket)
            var message = { action: "resetrobot" };
            var messageString = "{\"action\": \"" + message.action + "\"}";
            _this.promise
                .then(function (wsClient) {
                wsClient.send(messageString);
                console.log('Sending message' + messageString);
            })
                .catch(function (error) { return alert("Connection error: " + error); });
        };
        this.setActuatorStates = function (d_1, theta_1, theta_2, theta_3, l_6) {
            var message = { action: "setactstates" };
            var actuatorStates = { d_1: d_1, theta_1: theta_1, theta_2: theta_2, theta_3: theta_3, l_6: l_6 };
            var actStatesJson = JSON.stringify(actuatorStates);
            var messageString = "{\"action\": \"" + message.action + "\", \"act_states\":" + actStatesJson + "}";
            _this.promise
                .then(function (wsClient) {
                wsClient.send(messageString);
                console.log('Sending message' + messageString);
            })
                .catch(function (error) { return alert("Connection error: " + error); });
        };
        this.setEndEffectorPosition = function (x, y, z, phi, doOpenGripper) {
            var message = { action: "setendeffector" };
            var position = { x: x, y: y, z: z, phi: phi, doOpenGripper: doOpenGripper };
            var positionJson = JSON.stringify(position);
            var messageString = "{\"action\": \"" + message.action + "\", \"endeffector_position\":" + positionJson + "}";
            _this.promise
                .then(function (wsClient) {
                wsClient.send(messageString);
                console.log('Sending message' + messageString);
            })
                .catch(function (error) { return alert("Connection error: " + error); });
        };
        this.moveOrigin = function (x, y, z, phi) {
            var message = { action: "moveorigin" };
            var position = { x: x, y: y, z: z, phi: phi };
            var positionJson = JSON.stringify(position);
            var messageString = "{\"action\": \"" + message.action + "\", \"org_position\":" + positionJson + "}";
            _this.promise
                .then(function (wsClient) {
                wsClient.send(messageString);
                console.log('Sending message' + messageString);
            })
                .catch(function (error) { return alert("Connection error: " + error); });
        };
        this.nextPose = function () {
            // checkSocketConnection(this.socket)
            var message = { action: "getpose" };
            var messageString = "{\"action\": \"" + message.action + "\"}";
            _this.promise
                .then(function (wsClient) {
                wsClient.send(messageString);
                console.log('Sending message' + messageString);
            })
                .catch(function (error) { return alert("Connection error: " + error); });
        };
        this.streamPoses = function () {
            var message = { action: "streamposes" };
            var messageString = "{\"action\": \"" + message.action + "\"}";
            _this.promise
                .then(function (wsClient) {
                wsClient.send(messageString);
                console.log('Sending message' + messageString);
            })
                .catch(function (error) { return alert("Connection error: " + error); });
        };
        this.streamPosesNewOrg = function () {
            var message = { action: "streamposesneworg" };
            var messageString = "{\"action\": \"" + message.action + "\"}";
            _this.promise
                .then(function (wsClient) {
                wsClient.send(messageString);
                console.log('Sending message' + messageString);
            })
                .catch(function (error) { return alert("Connection error: " + error); });
        };
        this.streamPosesControlNewOrg = function () {
            var message = { action: "streamposescontrolneworg" };
            var messageString = "{\"action\": \"" + message.action + "\"}";
            _this.promise
                .then(function (wsClient) {
                wsClient.send(messageString);
                console.log('Sending message' + messageString);
            })
                .catch(function (error) { return alert("Connection error: " + error); });
        };
        this.promise = this.newClientPromise;
        this.areDimensionsInitialized = false;
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
                // let wsClient = new WebSocket("ws://ec2-52-45-198-60.compute-1.amazonaws.com:8000/robotcrane");
                var wsClient = new WebSocket("ws://localhost:8000/robotcrane");
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
    return Communicator;
}());
export { Communicator };
