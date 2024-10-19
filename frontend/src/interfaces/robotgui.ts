import {Communicator} from "../services/communicator";
import {GUI} from 'three/examples/jsm/libs/lil-gui.module.min.js'
import {Dimensions} from "./dimensions";

export class RobotGui {
    communicator: Communicator;
    guiInput : {states: any, position: any, org_position: any};

    constructor(communicator: Communicator) {
        this.communicator = communicator;

        // Initialize default GUI inputs
        this.guiInput = {
            states: {d1: 0.5, theta1: 0, theta2: 0, theta3: 0, l6: 0.1},
            position: {x: 0.4, y: 0.4, z: 0.4, phi: 0, doOpenGripper: true},
            org_position: {x: 0.4, y: 0.4, z: 0.2, phi: 0}
        }
    }

    createGui = (dimensions: Dimensions) => {
        let gui = new GUI();

        // Add Reset button
        let resetParams = {Reset: this.resetRobot};
        gui.add(resetParams, 'Reset');

        // Add GUI folders
        this.addMoveActuatorFolder(gui, dimensions);
        this.addMoveEndEffectorFolder(gui);
        this.addMoveOriginFolder(gui);
        this.addMoveOriginControlEndEffectorFolder(gui);
    }

    resetRobot = () => {
        this.communicator.resetRobot()
    }

    moveActuators = () => {
        this.communicator.moveActuators(this.guiInput.states)
    }

    moveEndEffector = () => {
        this.communicator.moveEndEffector(this.guiInput.position)
    }

    moveOrigin = () => {
        this.communicator.moveOrigin(this.guiInput.org_position)
    }

    moveOriginControl = () => {
        this.communicator.moveOriginControlEndEffector(this.guiInput.org_position)
    }

    private addMoveActuatorFolder(gui: GUI, dimensions: Dimensions) {
        let actuatorsFolder = gui.addFolder('Move actuators');
        actuatorsFolder.add(this.guiInput.states, 'd1').min(dimensions.d4).max(dimensions.l1)
        actuatorsFolder.add(this.guiInput.states, 'theta1').min(-360).max(360)
        actuatorsFolder.add(this.guiInput.states, 'theta2').min(-150).max(150)
        actuatorsFolder.add(this.guiInput.states, 'theta3').min(-360).max(360)
        actuatorsFolder.add(this.guiInput.states, 'l6').min(0).max(dimensions.l7)
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
        let moveOriginParams = {
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
        let moveOriginControlParams = {
            Submit: this.moveOriginControl
        };
        moveOriginControlFolder.add(moveOriginControlParams, 'Submit');
        moveOriginControlFolder.close();
    }
}