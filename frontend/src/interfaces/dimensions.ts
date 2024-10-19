export class Dimensions {
    l1: number;
    l2: number;
    l3: number;
    d4: number;
    l5: number;
    l7: number;

    constructor(l1: number, l2: number, l3: number, d4: number, l5: number, l7: number) {
        this.l1 = l1;
        this.l2 = l2;
        this.l3 = l3;
        this.d4 = d4;
        this.l5 = l5;
        this.l7 = l7;
    }

    static fromJson(json: any): Dimensions {
        return new Dimensions(json.l_1, json.l_2, json.l_3, -json.d_4, json.l_5, json.l_7)
    }
}