import { new_board, fetch_moveable, fetch_back } from "./fetch_api.js";
import { setPieces } from "./info.js";

function init_button_group() {
    document.getElementById('new_game').addEventListener('click', () => {
        new_board();
        let end_game_label = document.getElementById('end_game_label');
        let piece_container = document.getElementById('piece_container');
        piece_container.style.display = 'grid';
        let end_game_container = document.getElementById('end_game_container');
        end_game_container.style.display = 'none';
    })
    document.getElementById('back_game').addEventListener('click', () => {
        try {
            fetch_back();
        }
        catch {
            print('BACK ERROR');
        }
    })
}
init_button_group();

function board_init() {
    const piece_container = document.getElementById('piece_container');
    let result = [];
    for (let i = 0; i < 8; i++) {
        let inner_arr = [];
        for (let j = 0; j < 8; j++) {
            let id = i.toString() + j.toString();
            let span_element = document.createElement('span');
            span_element.id = id;
            let img_element = document.createElement('img');
            img_element.src = 'empty.png';
            img_element.classList.add('under');
            span_element.appendChild(img_element);
            if ((i + j) % 2 == 0) {
                span_element.classList.add('black');
            }
            else {
                span_element.classList.add('white');
            }

            piece_container.appendChild(span_element);

            inner_arr.push(span_element);
            span_element.addEventListener('click', async function () {
                if (this.children[0].src.endsWith('empty.png')) {

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

setPieces(board_init());