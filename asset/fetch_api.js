import { pieces,side } from "./info.js";

export function move_piece(from_pos,to_pos) {
    fetch('/board/move', {
        method: 'POST',
        body: JSON.stringify({
            'Side':side,
            'From' : {
                'y' : from_pos%10,
                'x' : Math.floor(from_pos/10)
            },
            'To': {
                'y' : to_pos%10,
                'x' : Math.floor(to_pos/10)
            }
        })
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        else {
            console.log('ERR');
        }
    })
    .then(data => {
        render_board(data)
    })
    .catch(error => {
        console.log('ERROR :',error);
    })
}
export function bot_move() {
    fetch('/board/bot_move', {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        else {
            console.log('ERR');
        }
    })
    .then(data => {
        render_board(data);
    })
    .catch(error => {
        console.log('ERROR :',error);
    })
}
export async function check_win() {
    let response_data = await fetch('board/check_win', {
        method:'POST'
    })
    .then(async response => {
        if (response.ok) {
            return await response.text();
        }
        else {
            console.log('ERR')
        }
    })
    .then(async data => {
        return data;
    })
    .catch(error => {
        console.log('ERR :',error);
    })
    return response_data;
}
export function fetch_board(){
    fetch('board/render', {
        method:'POST'
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        else {
            console.log('ERR');
        }
    })
    .then(data => {
        render_board(data);
    })
    .catch(error => {
        console.log('ERROR :',error);
    }) 
}
export function new_board(){
    fetch('board/new', {
        method:'POST',
        body: JSON.stringify({'Side':"None"})
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        else {
            console.log('ERR');
        }
    })
    .then(data => {
        render_board(data);
    })
    .catch(error => {
        console.log('ERROR :',error);
    }) 
} 
export function fetch_moveable(pos) {
    fetch('board/get_move', {
        method:'POST',
        body: JSON.stringify({
            'Side':side,
            'Position':{
                'y' : pos%10,
                'x' : Math.floor(pos/10),
            }
        })
    })
    .then(response => {
    if (response.ok && response.status == 200) {
        return response.json();
    }
    else {
        console.log('ERR');
    }
    })
    .then(data => {
        render_board(data);
    })
    .catch(error => {
        console.log('ERROR :',error);
    })
}
function render_board(data) {
    let mapping = {
        'ru' : 'black_rook.png','ku' : 'black_knight.png','bu':'black_bishop.png','qu':'black_queen.png','Ku':'black_king.png','pu':'black_pawn.png',
        'rd' : 'white_rook.png','kd' : 'white_knight.png','bd':'white_bishop.png','qd':'white_queen.png','Kd':'white_king.png','pd':'white_pawn.png',
        '-' : 'empty.png','m':'green.png','c':'red.png'
    }
    for (let x_it=0;x_it<8;x_it++) {
        for (let y_it = 0;y_it<8;y_it++) {
            pieces[x_it][y_it].src = mapping[data[y_it][x_it]];
        }
    }
}
