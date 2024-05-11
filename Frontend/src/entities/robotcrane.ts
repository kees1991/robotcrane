import * as THREE from "three";
import {Dimensions} from "./dimensions";
import {Pose} from "./pose";

// Materials
const liftMaterial = new THREE.MeshLambertMaterial({
      color: 0x48C9B0})
const upperArmMaterial = new THREE.MeshLambertMaterial({
      color: 0xF1C40F})
const lowerArmMaterial = new THREE.MeshLambertMaterial({
      color: 0xC39BD3})
const wristExtMaterial = new THREE.MeshLambertMaterial({
      color: 0xF4F6F7})
const gripperMaterial = new THREE.MeshLambertMaterial({
      color: 0xE74C3C})
const gripperExtMaterial = new THREE.MeshLambertMaterial({
      color: 0x196F3D})

export class RobotCrane {
    group: THREE.Group<THREE.Object3DEventMap>;
    thickness: number;
    jawThickness: number;
    jawLength: number;
    dimensions: Dimensions

    pivot0: THREE.Mesh<any, THREE.MeshLambertMaterial>;
    liftGeo: THREE.BoxGeometry;
    lift: THREE.Mesh<any, THREE.MeshLambertMaterial>;

    pivot: THREE.Mesh<any, THREE.MeshLambertMaterial>;
    upperArmGeo: THREE.BoxGeometry;
    upperArm: THREE.Mesh<any, THREE.MeshLambertMaterial>;

    pivot2: THREE.Mesh<any, THREE.MeshLambertMaterial>;
    lowerArmGeo: THREE.BoxGeometry;
    lowerArm: THREE.Mesh<any, THREE.MeshLambertMaterial>;

    pivot3: THREE.Mesh<any, THREE.MeshLambertMaterial>;
    wristExtGeo: THREE.BoxGeometry;
    wristExt: THREE.Mesh<any, THREE.MeshLambertMaterial>;

    pivot4: THREE.Mesh<any, THREE.MeshLambertMaterial>;
    gripperGeo: THREE.BoxGeometry;
    gripper: THREE.Mesh<any, THREE.MeshLambertMaterial>;

    pivot5: THREE.Object3D;
    fixedJawGeo: THREE.BoxGeometry;
    fixedJaw: THREE.Mesh<any, THREE.MeshLambertMaterial>;

    pivot6: THREE.Object3D;
    gripperExtGeo: THREE.BoxGeometry;
    gripperExt: THREE.Mesh<any, THREE.MeshLambertMaterial>;

    pivot7: THREE.Object3D;
    moveableJawGeo: THREE.BoxGeometry;
    moveableJaw: THREE.Mesh<any, THREE.MeshLambertMaterial>;

    pose : Pose;

    constructor(dimensions : Dimensions, pose : Pose) {
        this.group = new THREE.Group();

        this.thickness = 0.05;
        this.jawThickness = 0.01;
        this.jawLength = 0.05;

        this.dimensions = dimensions;
        this.pose = pose;

        this.pivot0 = new THREE.Mesh(new THREE.CylinderGeometry(this.thickness, this.thickness,this.thickness), liftMaterial);
        this.liftGeo = new THREE.BoxGeometry(this.thickness, this.dimensions.l_1, this.thickness);
        this.lift = new THREE.Mesh(this.liftGeo, liftMaterial);

        this.pivot = new THREE.Mesh(new THREE.CylinderGeometry(this.thickness, this.thickness,this.thickness), liftMaterial);
        this.upperArmGeo = new THREE.BoxGeometry(this.dimensions.l_2, this.thickness, this.thickness);
        this.upperArm = new THREE.Mesh(this.upperArmGeo, upperArmMaterial);

        this.pivot2 = new THREE.Mesh(new THREE.CylinderGeometry(this.thickness, this.thickness,this.thickness), upperArmMaterial);
        this.lowerArmGeo = new THREE.BoxGeometry(this.dimensions.l_3, this.thickness, this.thickness);
        this.lowerArm = new THREE.Mesh(this.lowerArmGeo, lowerArmMaterial);

        this.pivot3 = new THREE.Mesh(new THREE.CylinderGeometry(this.thickness, this.thickness,this.thickness), lowerArmMaterial);
        this.wristExtGeo = new THREE.BoxGeometry(this.thickness, this.dimensions.d_4, this.thickness);
        this.wristExt = new THREE.Mesh(this.wristExtGeo, wristExtMaterial);

        this.pivot4 = new THREE.Mesh(new THREE.CylinderGeometry(this.thickness, this.thickness,this.thickness), wristExtMaterial);
        this.gripperGeo = new THREE.BoxGeometry(this.dimensions.l_5, this.thickness, this.thickness);
        this.gripper = new THREE.Mesh(this.gripperGeo, gripperMaterial);

        this.pivot5 = new THREE.Object3D()
        this.fixedJawGeo = new THREE.BoxGeometry(this.jawThickness, this.jawLength, this.thickness);
        this.fixedJaw = new THREE.Mesh(this.fixedJawGeo, gripperExtMaterial);

        this.pivot6 = new THREE.Object3D()
        this.gripperExtGeo = new THREE.BoxGeometry(this.dimensions.l_7, this.thickness, this.thickness);
        this.gripperExt = new THREE.Mesh(this.gripperExtGeo, gripperExtMaterial);

        this.pivot7 = new THREE.Object3D()
        this.moveableJawGeo = new THREE.BoxGeometry(this.jawThickness, this.jawLength, this.thickness);
        this.moveableJaw = new THREE.Mesh(this.moveableJawGeo, gripperExtMaterial);
    }

    initScene = (scene: THREE.Scene, light : THREE.DirectionalLight) => {
        this.group.add(this.pivot0)
        this.pivot0.add(this.lift)

        this.group.add(this.pivot)
        this.pivot.add(this.upperArm)

        this.group.add(this.pivot2)
        this.pivot2.add(this.lowerArm)

        this.group.add(this.pivot3)
        this.pivot3.add(this.wristExt)

        this.group.add(this.pivot4)
        this.pivot4.add(this.gripper)

        this.group.add(this.pivot5)
        this.pivot5.add(this.fixedJaw)

        this.group.add(this.pivot6)
        this.pivot6.add(this.gripperExt)

        this.group.add(this.pivot7)
        this.pivot7.add(this.moveableJaw)

        scene.add(this.group)
        light.target = this.lift;
    }

    moveToPose = () => {
        this.pivot0.position.set(this.pose.j_1.x, this.pose.j_1.y, this.pose.j_1.z);
        this.pivot0.rotation.y = this.pose.theta_0;
        this.lift.position.y = this.dimensions.l_1 * 0.5;

        this.pivot.position.set(this.pose.j_2.x, this.pose.j_2.y, this.pose.j_2.z);
        this.pivot.rotation.y = this.pose.theta_0 + this.pose.theta_1;
        this.upperArm.position.x = this.dimensions.l_2 * 0.5;

        this.pivot2.position.set(this.pose.j_3.x, this.pose.j_3.y, this.pose.j_3.z);
        this.pivot2.rotation.y = this.pose.theta_0 + this.pose.theta_1 + this.pose.theta_2;
        this.lowerArm.position.x = this.dimensions.l_3 * 0.5;

        this.pivot3.position.set(this.pose.j_4.x, this.pose.j_4.y, this.pose.j_4.z);
        this.pivot3.rotation.y = this.pose.theta_0 + this.pose.theta_1 + this.pose.theta_2 + this.pose.theta_3;
        this.wristExt.position.y = -this.dimensions.d_4 * 0.5;

        this.pivot4.position.set(this.pose.j_5.x, this.pose.j_5.y, this.pose.j_5.z);
        this.pivot4.rotation.y = this.pose.theta_0 + this.pose.theta_1 + this.pose.theta_2 + this.pose.theta_3;
        this.gripper.position.x = this.thickness;

        this.pivot5.position.set(this.pose.j_6.x, this.pose.j_6.y, this.pose.j_6.z);
        this.pivot5.rotation.y = this.pose.theta_0 + this.pose.theta_1 + this.pose.theta_2 + this.pose.theta_3;
        this.fixedJaw.position.x = -this.jawThickness * 0.5;
        this.fixedJaw.position.y = -this.thickness;

        this.pivot6.position.set(this.pose.j_7.x, this.pose.j_7.y, this.pose.j_7.z);
        this.pivot6.rotation.y = this.pose.theta_0 + this.pose.theta_1 + this.pose.theta_2 + this.pose.theta_3;
        this.gripperExt.position.set(-this.dimensions.l_7 / 2, 0, 0);

        this.pivot7.position.set(this.pose.j_7.x, this.pose.j_7.y, this.pose.j_7.z);
        this.pivot7.rotation.y = this.pose.theta_0 + this.pose.theta_1 + this.pose.theta_2 + this.pose.theta_3;
        this.moveableJaw.position.x = -this.jawThickness * 0.5;
        this.moveableJaw.position.y = -this.thickness;
    }
}