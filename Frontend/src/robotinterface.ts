import * as THREE from 'three'
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls'
import {Communicator} from "./communicator.js";
import {RobotCrane} from "./entities/robotcrane.js";
import {RobotGui} from "./entities/robotgui.js";

let scene = new THREE.Scene();

// Add grid
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

// let robot = new RobotCrane(communicator.dimensions, communicator.pose);
// robot.initScene(scene, light);
//
// let robotGui = new RobotGui(renderer, scene, camera, controls, communicator, robot)
// robotGui.initGui()
//
// function init() {
//     communicator.initRobot();
//
//     robot.initScene(scene, light);
//
//     robot.pose = communicator.pose
//     robot.moveToPose()
//
//     renderer.render( scene, camera );
//
//     robotGui.animate()
// }
//
// init()

communicator.initRobot();
communicator.nextPose()
const animateInit = () => {
    let id = requestAnimationFrame( animateInit );

    if (communicator.areDimensionsInitialized) {
        let robot = new RobotCrane(communicator.dimensions, communicator.pose);
        robot.initScene(scene, light);

        let robotGui = new RobotGui(renderer, scene, camera, controls, communicator, robot)
        robotGui.initGui()

        console.log("Initialized robot dimensions")
        communicator.areDimensionsInitialized = false

        robot.pose = communicator.pose
        robot.moveToPose()

        cancelAnimationFrame(id)
        robotGui.animate()

    }
    renderer.render( scene, camera );
}

animateInit()
