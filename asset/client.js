import { fetch_board,new_board,move_piece,fetch_moveable,check_win,bot_move } from "./fetch_api.js";
import { last_selected_pos,setPieces,seteLastSelectedPos } from "./info.js";

function init_button_group() {
    document.getElementById('fetch_render').addEventListener('click',fetch_board);
    document.getElementById('new_game').addEventListener('click',new_board);
}
init_button_group();

function handle_win(result) {
    if (result == 'not_end'){
        console.log('Continue');
        return false;
    }
    else if (result == 'up') {
        console.log('Up win');
        return true;
    }
    else if (result == 'down') {
        console.log('Down win');
        return true;
    }
    else if (result == 'tie') {
        console.log('Tie');
        return true;
    }
}

export function init(){
    let result = [];
    for (let x_it=0;x_it<8;x_it++) {
        let inner_arr = [];
        for (let y_it = 0;y_it<8;y_it++) {
            let pos = y_it.toString()+x_it.toString()
            let img_ele = document.getElementById(pos)
            inner_arr.push(img_ele);
            img_ele.addEventListener('click',async function() {
                if (this.src.endsWith('empty.png')) {

                }
                else if (this.src.endsWith('reen.png') || this.src.endsWith('/red.png')) {
                    move_piece(last_selected_pos,this.id);
                    let result = await check_win();
                    let status = handle_win(result);
                    if (status == false) {
                        bot_move();
                    }
                }
                else {
                    fetch_moveable(this.id);
                    seteLastSelectedPos(this.id);
                }

            })
        }
        result.push(inner_arr);
    }
    return result;
}
setPieces(init());