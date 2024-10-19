import {Communicator} from "../services/communicator";
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
            states: {d1: 0.5, theta1: 0, theta2: 0, theta3: 0, l6: 0.1},
            position: {x: 0.4, y: 0.4, z: 0.4, phi: 0, doOpenGripper: true},
            org_position: {x: 0.4, y: 0.4, z: 0.2, phi: 0}
        }
    }

    createGui = () => {
        let gui = new GUI();

        // Add Reset button
        let resetParams = {Reset: this.resetRobot};
        gui.add(resetParams, 'Reset');

        // Add GUI folders
        this.addMoveActuatorFolder(gui);
        this.addMoveEndEffectorFolder(gui);
        this.addMoveOriginFolder(gui);
        this.addMoveOriginControlEndEffectorFolder(gui);
    }

    resetRobot = () => {
        this.communicator.resetRobot()
        this.communicator.getPose()
        this.animate();
    }

    moveActuators = () => {
        this.communicator.moveActuators(this.guiInput.states)
        this.animate();
    }

    moveEndEffector = () => {
        this.communicator.moveEndEffector(this.guiInput.position)
        this.animate();
    }

    moveOrigin = () => {
        this.communicator.moveOrigin(this.guiInput.org_position)
        this.animate();
    }

    moveOriginControl = () => {
        this.communicator.moveOriginControlEndEffector(this.guiInput.org_position)
        this.animate();
    }

    animate = () => {
        let id = requestAnimationFrame( this.animate );

        this.controls.update();

        // Cancel animation if there is an Exception from the backend
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

    private addMoveActuatorFolder(gui: GUI) {
        let actuatorsFolder = gui.addFolder('Move actuators');
        actuatorsFolder.add(this.guiInput.states, 'd1').min(this.robot.dimensions.d4).max(this.robot.dimensions.l1)
        actuatorsFolder.add(this.guiInput.states, 'theta1').min(-360).max(360)
        actuatorsFolder.add(this.guiInput.states, 'theta2').min(-150).max(150)
        actuatorsFolder.add(this.guiInput.states, 'theta3').min(-360).max(360)
        actuatorsFolder.add(this.guiInput.states, 'l6').min(0).max(this.robot.dimensions.l7)
        let actuatorParams = {
            Submit: this.moveActuators
        };
        actuatorsFolder.add(actuatorParams, 'Submit');
        actuatorsFolder.close();
    }

    private addMoveEndEffectorFolder(gui: GUI) {
        let endEffFolder = gui.addFolder('Move end-effector');
        endEffFolder.add(this.guiInput.position, 'x')
        endEffFolder.add(this.guiInput.position, 'y')
        endEffFolder.add(this.guiInput.position, 'z')
        endEffFolder.add(this.guiInput.position, 'phi')
        endEffFolder.add(this.guiInput.position, 'doOpenGripper')
        let endEffParams = {
            Submit: this.moveEndEffector
        };
        endEffFolder.add(endEffParams, 'Submit');
        endEffFolder.close();
    }

    private addMoveOriginFolder(gui: GUI) {
        let moveOriginFolder = gui.addFolder('Move origin');
        moveOriginFolder.add(this.guiInput.org_position, 'x')
        moveOriginFolder.add(this.guiInput.org_position, 'y')
        moveOriginFolder.add(this.guiInput.org_position, 'z')
        moveOriginFolder.add(this.guiInput.org_position, 'phi')
        var moveOriginParams = {
            Submit: this.moveOrigin
        };
        moveOriginFolder.add(moveOriginParams, 'Submit');
        moveOriginFolder.close();
    }

    private addMoveOriginControlEndEffectorFolder(gui: GUI) {
        let moveOriginControlFolder = gui.addFolder('Move origin and control end-effector')
        moveOriginControlFolder.add(this.guiInput.org_position, 'x')
        moveOriginControlFolder.add(this.guiInput.org_position, 'y')
        moveOriginControlFolder.add(this.guiInput.org_position, 'z')
        moveOriginControlFolder.add(this.guiInput.org_position, 'phi')
        var moveOriginControlParams = {
            Submit: this.moveOriginControl
        };
        moveOriginControlFolder.add(moveOriginControlParams, 'Submit');
        moveOriginControlFolder.close();
    }
}