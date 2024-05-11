export class Dimensions {
    l_1: number;
    l_2: number;
    l_3: number;
    d_4: number;
    l_5: number;
    l_7: number;

    constructor(jsonString : string) {
        const json = JSON.parse(jsonString);

        this.l_1 = json['l_1'];
        this.l_2 = json['l_2'];
        this.l_3 = json['l_3'];
        this.d_4 = - json['d_4'];
        this.l_5 = json['l_5'];
        this.l_7 = json['l_7'];
    }
}