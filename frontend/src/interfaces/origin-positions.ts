export class OriginPosition {
    x: number;
    y: number;
    z: number;
    phi: number;

    constructor(x: number, y: number, z: number, phi: number) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.phi = phi;
    }

    static fromJson(json: any) {
        return new OriginPosition(json.x, json.y, json.z, json.phi);
    }
}