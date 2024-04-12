import { init } from "./client.js";

var pieces = null;
let side = 'down';
let last_selected_pos = 0;

export function setPieces(data) {
    pieces = data
}
export function seteLastSelectedPos(data) {
    last_selected_pos = data
}

export{pieces,side,last_selected_pos}



