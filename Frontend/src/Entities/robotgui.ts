import {Communicator} from "../communicator";
import * as THREE from "three";
import {OrbitControls} from "three/examples/jsm/controls/OrbitControls";
import {GUI} from 'three/examples/jsm/libs/lil-gui.module.min.js'
import {RobotCrane} from "./robotcrane";

export class RobotGui {
    renderer: THREE.WebGLRenderer;
    scene: THREE.Scene;
    camera: THREE.PerspectiveCamera;
    controls: OrbitControls;
    communicator: Communicator;
    robot: RobotCrane;
    counter: number;
    guiInput : {states: any, position: any, org_position: any};

    constructor(renderer: THREE.WebGLRenderer, scene: THREE.Scene, camera: THREE.PerspectiveCamera, controls: OrbitControls, communicator: Communicator, robot: RobotCrane) {
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
        }
    }

    initGui = () => {
        let gui = new GUI();

        var resetParams = {
            Reset: this.resetRobot
        };
        gui.add(resetParams, 'Reset');
        let actuatorsFolder = gui.addFolder('Move actuators');
        let endEffFolder = gui.addFolder('Move end-effector');
        let moveOriginFolder = gui.addFolder('Move origin');
        let moveOriginControlFolder = gui.addFolder('Move origin control end-effector')

        actuatorsFolder.add(this.guiInput.states, 'd_1').min(this.robot.dimensions.d_4).max(this.robot.dimensions.l_1)
        actuatorsFolder.add(this.guiInput.states, 'theta_1').min(-360).max(360)
        actuatorsFolder.add(this.guiInput.states, 'theta_2').min(-150).max(150)
        actuatorsFolder.add(this.guiInput.states, 'theta_3').min(-360).max(360)
        actuatorsFolder.add(this.guiInput.states, 'l_6').min(0).max(this.robot.dimensions.l_7)

        var actuatorParams = {
            Submit: this.moveActuators
        };
        actuatorsFolder.add(actuatorParams, 'Submit');
        actuatorsFolder.close();

        endEffFolder.add(this.guiInput.position, 'x')
        endEffFolder.add(this.guiInput.position, 'y')
        endEffFolder.add(this.guiInput.position, 'z')
        endEffFolder.add(this.guiInput.position, 'phi')
        endEffFolder.add(this.guiInput.position, 'openGripper')
        var endEffParams = {
            Submit: this.moveEndEffector
        };
        endEffFolder.add(endEffParams, 'Submit');
        endEffFolder.close();

        moveOriginFolder.add(this.guiInput.org_position, 'x')
        moveOriginFolder.add(this.guiInput.org_position, 'y')
        moveOriginFolder.add(this.guiInput.org_position, 'z')
        moveOriginFolder.add(this.guiInput.org_position, 'phi')
        var moveOriginParams = {
            Submit: this.moveOrigin
        };
        moveOriginFolder.add(moveOriginParams, 'Submit');
        moveOriginFolder.close();

        moveOriginControlFolder.add(this.guiInput.org_position, 'x')
        moveOriginControlFolder.add(this.guiInput.org_position, 'y')
        moveOriginControlFolder.add(this.guiInput.org_position, 'z')
        moveOriginControlFolder.add(this.guiInput.org_position, 'phi')
        var moveOriginControlParams = {
            Submit: this.moveOriginControl
        };
        moveOriginControlFolder.add(moveOriginControlParams, 'Submit');
        moveOriginControlFolder.close();

        return gui;
    }

    moveActuators = () => {
        this.communicator.setActuatorStates(this.guiInput.states.d_1, this.guiInput.states.theta_1, this.guiInput.states.theta_2, this.guiInput.states.theta_3, this.guiInput.states.l_6)
        this.communicator.streamPoses()
        this.animate();
    }

    moveEndEffector = () => {
        this.communicator.setEndEffectorPosition(this.guiInput.position.x, this.guiInput.position.y, this.guiInput.position.z, this.guiInput.position.phi, this.guiInput.position.openGripper)
        this.communicator.streamPoses()
        this.animate();
    }

    moveOrigin = () => {
        this.communicator.moveOrigin(this.guiInput.org_position.x, this.guiInput.org_position.y, this.guiInput.org_position.z, this.guiInput.org_position.phi)
        this.communicator.streamPosesNewOrg()
        this.animate();
    }

    moveOriginControl = () => {
        this.communicator.moveOrigin(this.guiInput.org_position.x, this.guiInput.org_position.y, this.guiInput.org_position.z, this.guiInput.org_position.phi)
        this.communicator.streamPosesControlNewOrg()
        this.animate();
    }

    resetRobot = () => {
        this.communicator.resetRobot()
        this.communicator.nextPose()
        this.animate();
    }

    animate = () => {
        let id = requestAnimationFrame( this.animate );

        this.controls.update();
        if (this.communicator.exception !== "") {
            alert(this.communicator.exception)
            this.communicator.exception = ""
            console.log("Cancelling animation because of an Exception")
            cancelAnimationFrame(id)
        }

        if (this.counter !== this.communicator.counter) {
            this.robot.pose = this.communicator.pose
            this.robot.moveToPose()
            this.counter = this.communicator.counter
        }

        // Render
        this.renderer.render( this.scene, this.camera );
    };
}