import * as THREE from "three";
import {Vector3} from "three";

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

    constructor(j_1: Vector3, j_2: Vector3, j_3: Vector3, j_4: Vector3, j_5: Vector3, j_6: Vector3, j_7: Vector3, theta_0: number, theta_1: number, theta_2: number, theta_3: number) {
        this.j_1 = j_1;
        this.j_2 = j_2;
        this.j_3 = j_3;
        this.j_4 = j_4;
        this.j_5 = j_5;
        this.j_6 = j_6;
        this.j_7 = j_7;
        this.theta_0 = theta_0;
        this.theta_1 = theta_1;
        this.theta_2 = theta_2;
        this.theta_3 = theta_3;
    }

    static fromJson(json : any): Pose {
        return new Pose(
            new THREE.Vector3(json['j_1'][0], json['j_1'][2], -json['j_1'][1]),
            new THREE.Vector3(json['j_2'][0], json['j_2'][2], -json['j_2'][1]),
            new THREE.Vector3(json['j_3'][0], json['j_3'][2], -json['j_3'][1]),
            new THREE.Vector3(json['j_4'][0], json['j_4'][2], -json['j_4'][1]),
            new THREE.Vector3(json['j_5'][0], json['j_5'][2], -json['j_5'][1]),
            new THREE.Vector3(json['j_6'][0], json['j_6'][2], -json['j_6'][1]),
            new THREE.Vector3(json['j_7'][0], json['j_7'][2], -json['j_7'][1]),
            json['theta_0'],
            json['theta_1'],
            json['theta_2'],
            json['theta_3']
        )
    }

// TODO add fromjson method
}