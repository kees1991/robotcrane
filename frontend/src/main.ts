import * as THREE from 'three'
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls'
import {Communicator} from "./services/communicator.js";
import {RobotCrane} from "./interfaces/robotcrane.js";
import {RobotGui} from "./interfaces/robotgui.js";

let scene = new THREE.Scene();

// Add a grid
let grid = new THREE.GridHelper(2, 10);
scene.add(grid);

// Camera
let aspect = window.innerWidth / window.innerHeight;
let camera = new THREE.PerspectiveCamera( 60, aspect, 0.1, 1000 );
camera.position.z = 2;
camera.position.x = 3;
camera.position.y = 3;
camera.lookAt(0, 0, 0);
camera.updateProjectionMatrix();

// Light
let light = new THREE.DirectionalLight(0xffffff, 6.0);
light.position.set(10, 5, 10);
camera.add(light);
scene.add(camera);

// Renderer
let renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize( window.innerWidth, window.innerHeight );
document.body.appendChild( renderer.domElement );

const controls = new OrbitControls( camera, renderer.domElement );

let communicator = new Communicator();
communicator.initializeRobot()

const animateInit = () => {
    let id = requestAnimationFrame( animateInit );

    console.log("Robot not initialized yet")

    if (communicator.robot != null) {
        let robotGui = new RobotGui(communicator)
        robotGui.createGui(communicator.robot.dimensions)

        communicator.robot.initScene(scene, light);
        communicator.robot.moveToPose()

        console.log("Initialized robot")

        cancelAnimationFrame(id)
        animate()

    }
    renderer.render( scene, camera );
}

let counter = communicator.counter;
const animate = () => {
    let id = requestAnimationFrame( animate );

    controls.update();

    // Reset robot if there is an Exception from the backend
    if (communicator.exception != null) {
        alert(communicator.exception)
        communicator.exception = undefined

        console.log("Resetting robot")
        communicator.resetRobot()
    }

    if (counter !== communicator.counter) {
        if (communicator.robot != null) {
            communicator.robot.moveToPose()
        }
        counter = communicator.counter
    }

    // Render
    renderer.render( scene, camera );
};

animateInit()
