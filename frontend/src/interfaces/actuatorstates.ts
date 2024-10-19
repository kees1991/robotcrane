export class ActuatorStates {
    d1: number;
    theta1: number;
    theta2: number;
    theta3: number;
    l6: number;

    constructor(d1: number, theta1: number, theta2: number, theta3: number, l6: number) {
        this.d1 = d1;
        this.theta1 = theta1;
        this.theta2 = theta2;
        this.theta3 = theta3;
        this.l6 = l6;
    }

   static fromJson(json: any): ActuatorStates {
        return new ActuatorStates(json.d1, json.theta1, json.theta2, json.theta3, json.l6);
    }
}