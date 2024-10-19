export class Position {
    x: number;
    y: number;
    z: number;
    phi: number;
    doOpenGripper: boolean;

    constructor(x: number, y: number, z: number, phi: number, doOpenGripper: boolean) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.phi = phi;
        this.doOpenGripper = doOpenGripper;
    }

    static fromJson(json: any): Position {
        return new Position(json.x, json.y, json.z, json.phi, json.doOpenGripper);
    }
}