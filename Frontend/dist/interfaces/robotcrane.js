import * as THREE from "three";
// Materials
var liftMaterial = new THREE.MeshLambertMaterial({
    color: 0x48C9B0
});
var upperArmMaterial = new THREE.MeshLambertMaterial({
    color: 0xF1C40F
});
var lowerArmMaterial = new THREE.MeshLambertMaterial({
    color: 0xC39BD3
});
var wristExtMaterial = new THREE.MeshLambertMaterial({
    color: 0xF4F6F7
});
var gripperMaterial = new THREE.MeshLambertMaterial({
    color: 0xE74C3C
});
var gripperExtMaterial = new THREE.MeshLambertMaterial({
    color: 0x196F3D
});
var RobotCrane = /** @class */ (function () {
    function RobotCrane(dimensions, pose) {
        var _this = this;
        this.initScene = function (scene, light) {
            _this.group.add(_this.pivot0);
            _this.pivot0.add(_this.lift);
            _this.group.add(_this.pivot);
            _this.pivot.add(_this.upperArm);
            _this.group.add(_this.pivot2);
            _this.pivot2.add(_this.lowerArm);
            _this.group.add(_this.pivot3);
            _this.pivot3.add(_this.wristExt);
            _this.group.add(_this.pivot4);
            _this.pivot4.add(_this.gripper);
            _this.group.add(_this.pivot5);
            _this.pivot5.add(_this.fixedJaw);
            _this.group.add(_this.pivot6);
            _this.pivot6.add(_this.gripperExt);
            _this.group.add(_this.pivot7);
            _this.pivot7.add(_this.moveableJaw);
            scene.add(_this.group);
            light.target = _this.lift;
        };
        this.moveToPose = function () {
            _this.pivot0.position.set(_this.pose.j_1.x, _this.pose.j_1.y, _this.pose.j_1.z);
            _this.pivot0.rotation.y = _this.pose.theta_0;
            _this.lift.position.y = _this.dimensions.l_1 * 0.5;
            _this.pivot.position.set(_this.pose.j_2.x, _this.pose.j_2.y, _this.pose.j_2.z);
            _this.pivot.rotation.y = _this.pose.theta_0 + _this.pose.theta_1;
            _this.upperArm.position.x = _this.dimensions.l_2 * 0.5;
            _this.pivot2.position.set(_this.pose.j_3.x, _this.pose.j_3.y, _this.pose.j_3.z);
            _this.pivot2.rotation.y = _this.pose.theta_0 + _this.pose.theta_1 + _this.pose.theta_2;
            _this.lowerArm.position.x = _this.dimensions.l_3 * 0.5;
            _this.pivot3.position.set(_this.pose.j_4.x, _this.pose.j_4.y, _this.pose.j_4.z);
            _this.pivot3.rotation.y = _this.pose.theta_0 + _this.pose.theta_1 + _this.pose.theta_2 + _this.pose.theta_3;
            _this.wristExt.position.y = -_this.dimensions.d_4 * 0.5;
            _this.pivot4.position.set(_this.pose.j_5.x, _this.pose.j_5.y, _this.pose.j_5.z);
            _this.pivot4.rotation.y = _this.pose.theta_0 + _this.pose.theta_1 + _this.pose.theta_2 + _this.pose.theta_3;
            _this.gripper.position.x = _this.thickness;
            _this.pivot5.position.set(_this.pose.j_6.x, _this.pose.j_6.y, _this.pose.j_6.z);
            _this.pivot5.rotation.y = _this.pose.theta_0 + _this.pose.theta_1 + _this.pose.theta_2 + _this.pose.theta_3;
            _this.fixedJaw.position.x = -_this.jawThickness * 0.5;
            _this.fixedJaw.position.y = -_this.thickness;
            _this.pivot6.position.set(_this.pose.j_7.x, _this.pose.j_7.y, _this.pose.j_7.z);
            _this.pivot6.rotation.y = _this.pose.theta_0 + _this.pose.theta_1 + _this.pose.theta_2 + _this.pose.theta_3;
            _this.gripperExt.position.set(-_this.dimensions.l_7 / 2, 0, 0);
            _this.pivot7.position.set(_this.pose.j_7.x, _this.pose.j_7.y, _this.pose.j_7.z);
            _this.pivot7.rotation.y = _this.pose.theta_0 + _this.pose.theta_1 + _this.pose.theta_2 + _this.pose.theta_3;
            _this.moveableJaw.position.x = -_this.jawThickness * 0.5;
            _this.moveableJaw.position.y = -_this.thickness;
        };
        this.group = new THREE.Group();
        this.thickness = 0.05;
        this.jawThickness = 0.01;
        this.jawLength = 0.05;
        this.dimensions = dimensions;
        this.pose = pose;
        this.pivot0 = new THREE.Mesh(new THREE.CylinderGeometry(this.thickness, this.thickness, this.thickness), liftMaterial);
        this.liftGeo = new THREE.BoxGeometry(this.thickness, this.dimensions.l_1, this.thickness);
        this.lift = new THREE.Mesh(this.liftGeo, liftMaterial);
        this.pivot = new THREE.Mesh(new THREE.CylinderGeometry(this.thickness, this.thickness, this.thickness), liftMaterial);
        this.upperArmGeo = new THREE.BoxGeometry(this.dimensions.l_2, this.thickness, this.thickness);
        this.upperArm = new THREE.Mesh(this.upperArmGeo, upperArmMaterial);
        this.pivot2 = new THREE.Mesh(new THREE.CylinderGeometry(this.thickness, this.thickness, this.thickness), upperArmMaterial);
        this.lowerArmGeo = new THREE.BoxGeometry(this.dimensions.l_3, this.thickness, this.thickness);
        this.lowerArm = new THREE.Mesh(this.lowerArmGeo, lowerArmMaterial);
        this.pivot3 = new THREE.Mesh(new THREE.CylinderGeometry(this.thickness, this.thickness, this.thickness), lowerArmMaterial);
        this.wristExtGeo = new THREE.BoxGeometry(this.thickness, this.dimensions.d_4, this.thickness);
        this.wristExt = new THREE.Mesh(this.wristExtGeo, wristExtMaterial);
        this.pivot4 = new THREE.Mesh(new THREE.CylinderGeometry(this.thickness, this.thickness, this.thickness), wristExtMaterial);
        this.gripperGeo = new THREE.BoxGeometry(this.dimensions.l_5, this.thickness, this.thickness);
        this.gripper = new THREE.Mesh(this.gripperGeo, gripperMaterial);
        this.pivot5 = new THREE.Object3D();
        this.fixedJawGeo = new THREE.BoxGeometry(this.jawThickness, this.jawLength, this.thickness);
        this.fixedJaw = new THREE.Mesh(this.fixedJawGeo, gripperExtMaterial);
        this.pivot6 = new THREE.Object3D();
        this.gripperExtGeo = new THREE.BoxGeometry(this.dimensions.l_7, this.thickness, this.thickness);
        this.gripperExt = new THREE.Mesh(this.gripperExtGeo, gripperExtMaterial);
        this.pivot7 = new THREE.Object3D();
        this.moveableJawGeo = new THREE.BoxGeometry(this.jawThickness, this.jawLength, this.thickness);
        this.moveableJaw = new THREE.Mesh(this.moveableJawGeo, gripperExtMaterial);
    }
    return RobotCrane;
}());
export { RobotCrane };
