import { GUI } from 'three/examples/jsm/libs/lil-gui.module.min.js';
var RobotGui = /** @class */ (function () {
    function RobotGui(renderer, scene, camera, controls, communicator, robot) {
        var _this = this;
        this.initGui = function () {
            var gui = new GUI();
            var resetParams = {
                Reset: _this.resetRobot
            };
            gui.add(resetParams, 'Reset');
            var actuatorsFolder = gui.addFolder('Move actuators');
            var endEffFolder = gui.addFolder('Move end-effector');
            var moveOriginFolder = gui.addFolder('Move origin');
            var moveOriginControlFolder = gui.addFolder('Move origin control end-effector');
            actuatorsFolder.add(_this.guiInput.states, 'd_1').min(_this.robot.dimensions.d_4).max(_this.robot.dimensions.l_1);
            actuatorsFolder.add(_this.guiInput.states, 'theta_1').min(-360).max(360);
            actuatorsFolder.add(_this.guiInput.states, 'theta_2').min(-150).max(150);
            actuatorsFolder.add(_this.guiInput.states, 'theta_3').min(-360).max(360);
            actuatorsFolder.add(_this.guiInput.states, 'l_6').min(0).max(_this.robot.dimensions.l_7);
            var actuatorParams = {
                Submit: _this.moveActuators
            };
            actuatorsFolder.add(actuatorParams, 'Submit');
            actuatorsFolder.close();
            endEffFolder.add(_this.guiInput.position, 'x');
            endEffFolder.add(_this.guiInput.position, 'y');
            endEffFolder.add(_this.guiInput.position, 'z');
            endEffFolder.add(_this.guiInput.position, 'phi');
            endEffFolder.add(_this.guiInput.position, 'openGripper');
            var endEffParams = {
                Submit: _this.moveEndEffector
            };
            endEffFolder.add(endEffParams, 'Submit');
            endEffFolder.close();
            moveOriginFolder.add(_this.guiInput.org_position, 'x');
            moveOriginFolder.add(_this.guiInput.org_position, 'y');
            moveOriginFolder.add(_this.guiInput.org_position, 'z');
            moveOriginFolder.add(_this.guiInput.org_position, 'phi');
            var moveOriginParams = {
                Submit: _this.moveOrigin
            };
            moveOriginFolder.add(moveOriginParams, 'Submit');
            moveOriginFolder.close();
            moveOriginControlFolder.add(_this.guiInput.org_position, 'x');
            moveOriginControlFolder.add(_this.guiInput.org_position, 'y');
            moveOriginControlFolder.add(_this.guiInput.org_position, 'z');
            moveOriginControlFolder.add(_this.guiInput.org_position, 'phi');
            var moveOriginControlParams = {
                Submit: _this.moveOriginControl
            };
            moveOriginControlFolder.add(moveOriginControlParams, 'Submit');
            moveOriginControlFolder.close();
            return gui;
        };
        this.moveActuators = function () {
            _this.communicator.setActuatorStates(_this.guiInput.states.d_1, _this.guiInput.states.theta_1, _this.guiInput.states.theta_2, _this.guiInput.states.theta_3, _this.guiInput.states.l_6);
            _this.communicator.streamPoses();
            _this.animate();
        };
        this.moveEndEffector = function () {
            _this.communicator.setEndEffectorPosition(_this.guiInput.position.x, _this.guiInput.position.y, _this.guiInput.position.z, _this.guiInput.position.phi, _this.guiInput.position.openGripper);
            _this.communicator.streamPoses();
            _this.animate();
        };
        this.moveOrigin = function () {
            _this.communicator.moveOrigin(_this.guiInput.org_position.x, _this.guiInput.org_position.y, _this.guiInput.org_position.z, _this.guiInput.org_position.phi);
            _this.communicator.streamPosesNewOrg();
            _this.animate();
        };
        this.moveOriginControl = function () {
            _this.communicator.moveOrigin(_this.guiInput.org_position.x, _this.guiInput.org_position.y, _this.guiInput.org_position.z, _this.guiInput.org_position.phi);
            _this.communicator.streamPosesControlNewOrg();
            _this.animate();
        };
        this.resetRobot = function () {
            _this.communicator.resetRobot();
            _this.communicator.nextPose();
            _this.animate();
        };
        this.animate = function () {
            var id = requestAnimationFrame(_this.animate);
            _this.controls.update();
            if (_this.communicator.exception !== "") {
                alert(_this.communicator.exception);
                _this.communicator.exception = "";
                console.log("Cancelling animation because of an Exception");
                cancelAnimationFrame(id);
            }
            if (_this.counter !== _this.communicator.counter) {
                _this.robot.pose = _this.communicator.pose;
                _this.robot.moveToPose();
                _this.counter = _this.communicator.counter;
            }
            // Render
            _this.renderer.render(_this.scene, _this.camera);
        };
        this.renderer = renderer;
        this.scene = scene;
        this.camera = camera;
        this.controls = controls;
        this.communicator = communicator;
        this.robot = robot;
        this.counter = communicator.counter;
        this.guiInput = {
            states: {
                d_1: 0.5,
                theta_1: 0,
                theta_2: 0,
                theta_3: 0,
                l_6: 0.1
            },
            position: {
                x: 0.4,
                y: 0.4,
                z: 0.4,
                phi: 0,
                openGripper: true
            },
            org_position: {
                x: 0.4,
                y: 0.4,
                z: 0.2,
                phi: 0
            }
        };
    }
    return RobotGui;
}());
export { RobotGui };
