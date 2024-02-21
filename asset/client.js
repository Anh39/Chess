let piece_container = init();
function init(){
    result = [];
    for (let x_it=0;x_it<8;x_it++) {
        let inner_arr = [];
        for (let y_it = 0;y_it<8;y_it++) {
            inner_arr.push(document.getElementById(x_it.toString()+y_it.toString()));
        }
        result.push(inner_arr);
    }
    return result;
}
function init_button_group() {
    document.getElementById('fetch_render').addEventListener('click',fetch_board);
}
function fetch_board(){
    fetch('test.ipynb', {
        method:'POST',
        headers:{
            'Request-Type':'fetch_board'
        },
        body: JSON.stringify({'Side':'up'})
    })
    .then(response => {
        if (response.ok) {
            return response.json;
        }
        else {
            console.log(response.status);
        }
    })
    .then(data => {
        console.log(data);
    })
    .catch(error => {
        console.log('ERROR');
    }) 
}

