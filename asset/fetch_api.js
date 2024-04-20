import { pieces, side } from "./info.js";

export function move_piece(from_pos, to_pos) {
    fetch('/board/move', {
        method: 'POST',
        body: JSON.stringify({
            'Side': side,
            'From': {
                'x': from_pos % 10,
                'y': Math.floor(from_pos / 10)
            },
            'To': {
                'x': to_pos % 10,
                'y': Math.floor(to_pos / 10)
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
            console.log('ERROR :', error);
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
            console.log('ERROR :', error);
        })
}
export async function check_win() {
    let response_data = await fetch('board/check_win', {
        method: 'POST'
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
            console.log('ERR :', error);
        })
    return response_data;
}
export function fetch_board() {
    fetch('board/render', {
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
            console.log('ERROR :', error);
        })
}
export function new_board() {
    fetch('board/new', {
        method: 'POST',
        body: JSON.stringify({ 'Side': "None" })
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
            console.log('ERROR :', error);
        })
}
export function fetch_back() {
    fetch('board/back', {
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
            console.log('ERROR :', error);
        })
}
export function fetch_moveable(pos) {
    fetch('board/get_move', {
        method: 'POST',
        body: JSON.stringify({
            'Side': side,
            'Position': {
                'x': pos % 10,
                'y': Math.floor(pos / 10),
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
            render_move(data, pos);
        })
        .catch(error => {
            console.log('ERROR :', error);
        })
}
function handle_win(result) {
    if (result == 'not_end') {
        console.log('Continue');
        return false;
    } else {
        let end_game_label = document.getElementById('end_game_label');
        let piece_container = document.getElementById('piece_container');
        piece_container.style.display = 'none';
        let end_game_container = document.getElementById('end_game_container');
        end_game_container.style.display = 'flex';

        if (result == 'up') {
            end_game_label.textContent = 'You LOSE';
            console.log('Up win');
        }
        else if (result == 'down') {
            end_game_label.textContent = 'You WIN';
            console.log('Down win');
        }
        else if (result == 'tie') {
            end_game_label.textContent = 'Tie';
            console.log('Tie');
        }
        return true;
    }
}
function render_board(data) {
    let mapping = {
        'ru': 'black_rook.png', 'ku': 'black_knight.png', 'bu': 'black_bishop.png', 'qu': 'black_queen.png', 'Ku': 'black_king.png', 'pu': 'black_pawn.png',
        'rd': 'white_rook.png', 'kd': 'white_knight.png', 'bd': 'white_bishop.png', 'qd': 'white_queen.png', 'Kd': 'white_king.png', 'pd': 'white_pawn.png',
        '-': 'empty.png', 'm': 'green.png', 'c': 'red.png'
    }
    for (let x_it = 0; x_it < 8; x_it++) {
        for (let y_it = 0; y_it < 8; y_it++) {
            let source = mapping[data[y_it][x_it]];
            let element = pieces[x_it][y_it]
            while (element.children.length > 1) {
                element.removeChild(element.children[element.children.length - 1])
            }
            element.children[0].src = source;
        }
    }
}
function render_move(data, from_pos) {
    let mapping = {
        'ru': 'black_rook.png', 'ku': 'black_knight.png', 'bu': 'black_bishop.png', 'qu': 'black_queen.png', 'Ku': 'black_king.png', 'pu': 'black_pawn.png',
        'rd': 'white_rook.png', 'kd': 'white_knight.png', 'bd': 'white_bishop.png', 'qd': 'white_queen.png', 'Kd': 'white_king.png', 'pd': 'white_pawn.png',
        '-': 'empty.png', 'm': 'green.png', 'c': 'red.png'
    }
    for (let x_it = 0; x_it < 8; x_it++) {
        for (let y_it = 0; y_it < 8; y_it++) {
            let source = mapping[data[y_it][x_it]];
            let element = pieces[x_it][y_it]
            while (element.children.length > 1) {
                element.removeChild(element.children[element.children.length - 1])
            }
            if (source == 'green.png' || source == 'red.png') {
                let new_img_element = document.createElement('img');
                new_img_element.src = source;
                new_img_element.classList.add('overlay');
                new_img_element.addEventListener('click', async () => {
                    move_piece(from_pos, element.id);
                    let result = await check_win();
                    let status = handle_win(result);
                    if (status == false) {
                        bot_move();
                    }
                    result = await check_win();
                    status = handle_win(result);
                })
                element.appendChild(new_img_element);
            }
        }
    }
}