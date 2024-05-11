var Dimensions = /** @class */ (function () {
    function Dimensions(jsonString) {
        var json = JSON.parse(jsonString);
        this.l_1 = json['l_1'];
        this.l_2 = json['l_2'];
        this.l_3 = json['l_3'];
        this.d_4 = -json['d_4'];
        this.l_5 = json['l_5'];
        this.l_7 = json['l_7'];
    }
    return Dimensions;
}());
export { Dimensions };
