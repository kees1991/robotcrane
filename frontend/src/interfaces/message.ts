export class Message {
    private readonly _action: string;
    private readonly _data?: object;

    constructor(action: string, data?: object) {
        this._action = action;
        this._data = data;
    }

    get action(): string {
        return this._action;
    }

    get data(): any | undefined {
        return this._data;
    }

    toJSON(): object {
        if (this.data == null) {
            return {action: this.action};
        }

        return {
            action: this.action,
            data: this.data
        };
    }


    toJsonString(): string {
        return JSON.stringify(this.toJSON());
    }
}