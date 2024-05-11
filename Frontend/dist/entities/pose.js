import * as THREE from "three";
var Pose = /** @class */ (function () {
    function Pose(jsonString) {
        var json = JSON.parse(jsonString);
        this.j_1 = new THREE.Vector3(json['j_1'][0], json['j_1'][2], -json['j_1'][1]);
        this.j_2 = new THREE.Vector3(json['j_2'][0], json['j_2'][2], -json['j_2'][1]);
        this.j_3 = new THREE.Vector3(json['j_3'][0], json['j_3'][2], -json['j_3'][1]);
        this.j_4 = new THREE.Vector3(json['j_4'][0], json['j_4'][2], -json['j_4'][1]);
        this.j_5 = new THREE.Vector3(json['j_5'][0], json['j_5'][2], -json['j_5'][1]);
        this.j_6 = new THREE.Vector3(json['j_6'][0], json['j_6'][2], -json['j_6'][1]);
        this.j_7 = new THREE.Vector3(json['j_7'][0], json['j_7'][2], -json['j_7'][1]);
        this.theta_0 = json['theta_0'];
        this.theta_1 = json['theta_1'];
        this.theta_2 = json['theta_2'];
        this.theta_3 = json['theta_3'];
    }
    return Pose;
}());
export { Pose };
