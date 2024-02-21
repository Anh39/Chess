let pieces = init();
let side = 'down';
let other_side = 'up';
function init(){
    let result = [];
    for (let x_it=0;x_it<8;x_it++) {
        let inner_arr = [];
        for (let y_it = 0;y_it<8;y_it++) {
            let pos = y_it.toString()+x_it.toString()
            let img_ele = document.getElementById(pos)
            inner_arr.push(img_ele);
            img_ele.addEventListener('click',function() {
                if (this.src.endsWith('empty.png')) {

                }
                else if (this.src.endsWith('reen.png') || this.src.endsWith('/red.png')) {
                    move_piece(this.id);
                }
                else {
                    fetch_moveable(this.id);
                }

            })
        }
        result.push(inner_arr);
    }
    return result;
}
function init_button_group() {
    document.getElementById('fetch_render').addEventListener('click',fetch_board);
    document.getElementById('new_game').addEventListener('click',new_board);
}
init_button_group();
function move_piece(pos) {
    fetch('test.ipynb', {
        method: 'POST',
        headers: {
            'Request-Type':'move_piece'
        },
        body: JSON.stringify({'Side':side,'Other-side':other_side,'To':pos})
    })
    .then(response => {
        if (response.ok) {
            let game_state = response.headers.get('Game-state')
            if (game_state == 'continue') {
                return response.json();
            }
            else {
                console.log(game_state);
            }
        }
        else {
            console.log('ERR');
        }
    })
    .then(data => {
        if (data != null) {
            render_board(data);
        }
    })
    .catch(error => {
        console.log('ERROR :',error);
    })
}
function fetch_board(){
    fetch('test.ipynb', {
        method:'POST',
        headers:{
            'Request-Type':'fetch_board'
        },
        body: JSON.stringify({'Side':side})
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
        if (data != null) {
            render_board(data);
        }
    })
    .catch(error => {
        console.log('ERROR :',error);
    }) 
}
function new_board(){
    fetch('test.ipynb', {
        method:'POST',
        headers:{
            'Request-Type':'reset'
        },
        body: JSON.stringify({'Side':side})
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
        if (data != null) {
            render_board(data);
        }
    })
    .catch(error => {
        console.log('ERROR :',error);
    }) 
}
function fetch_moveable(pos) {
    fetch('test.ipynb', {
        method:'POST',
        headers:{
            'Request-Type':'fetch_moveable'
        },
        body: JSON.stringify({'Side':side,'Other-side':other_side,'Position':pos})
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
        if (data != null) {
            render_board(data);
        }
    })
    .catch(error => {
        console.log('ERROR :',error);
    })
}
function render_board(data) {
    let mapping = {
        'ru' : 'black_rook.png','ku' : 'black_knight.png','bu':'black_bishop.png','qu':'black_queen.png','Ku':'black_king.png','pu':'black_pawn.png',
        'rd' : 'white_rook.png','kd' : 'white_knight.png','bd':'white_bishop.png','qd':'white_queen.png','Kd':'white_king.png','pd':'white_pawn.png',
        'e' : 'empty.png','m':'green.png','c':'red.png'
    }
    for (let x_it=0;x_it<8;x_it++) {
        for (let y_it = 0;y_it<8;y_it++) {
            pieces[x_it][y_it].src = mapping[data[x_it][y_it]];
        }
    }
}
