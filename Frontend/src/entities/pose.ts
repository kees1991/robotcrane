import * as THREE from "three";

export class Pose {
    j_1: THREE.Vector3;
    j_2: THREE.Vector3;
    j_3: THREE.Vector3;
    j_4: THREE.Vector3;
    j_5: THREE.Vector3;
    j_6: THREE.Vector3;
    j_7: THREE.Vector3;
    theta_0: number;
    theta_1: number;
    theta_2: number;
    theta_3: number;

    constructor(jsonString : string) {
        const json = JSON.parse(jsonString);

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
}