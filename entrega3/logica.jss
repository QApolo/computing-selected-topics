/*
* 2 7 4 6 20% 
* 3 6 3 4 20% 
* 1 6 1 6 10% 
* 3 3 1 8 10% 
* 3 3 1 7 5% 
* 23 3 6 10%
*/
let CANVAS_SIZE = 1000;
let TYPE_FUNCTION_DICT = {
    "MODA": 1,
    "MINIMO": 2,
    "PARIDAD": 3
};
let c = document.getElementById("canvas");
let c_aux = document.getElementById("canvas-aux");
let information_output = document.getElementById("information");
let slider_distribution = document.getElementById("distribution");
let slider_output = document.getElementById("distribution_value");
let context = document.getElementById("myChart");
let ctx = c.getContext("2d");
let ctx_aux = c_aux.getContext("2d");
let size = 100;
let total_population = size*size;
let dimension = 10;
let rule = [2, 3, 3, 3];
let counter = 0;
let my_time = 0;
let suma = 0;
let interval = null;
let is_runinng = false;
let is_active = true;
let original = [];
let auxiliar = [];
let ones_distribution = 0.5;
let tau = 3;
let colors = ["#FFFFFF", "#000000"];
let type_function = TYPE_FUNCTION_DICT["MODA"];
let myLineChart = create_chart(context);
let matrices;
let is_auxiliar_showed = false;

ctx.lineWidth = "0.1";
slider_output.innerHTML = slider_distribution.value;
slider_distribution.oninput = function(e) {
    e.preventDefault();
    slider_output.innerHTML = this.value;
}

function create_chart(_context) {
    return new Chart(_context, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: "Cantidad de unos",
                data: [],
                borderColor: "#c45850",
                fill: false,
                lineTension: 0,
                defaultFontSize: 30 
            }]
        },
        options: {
            title: {
                display: true,
                text: 'Historial de unos',
            },
            legends: {
                labels: {
                    defaultFontSize: 30
                }
            },
            defaultFontSize: 30,
        },
    });
}

function get_zero_or_one(dis) {
    if (Math.random() < dis)
        return 1;
    else
        return 0;
}

function draw_matrix(size, dimension, matrix) {
    for (let i = 0; i < size; i++)
        for (let j = 0; j < size; j++){
            if (matrix[i][j] == 1)
                ctx.fillStyle = colors[1];
            else
                ctx.fillStyle = colors[0];
            ctx.fillRect(dimension*j, dimension*i, dimension, dimension);
        }
    ctx.stroke();
}

function draw_aux_matrix(size, dimension, matrix) {
    for (let i = 0; i < size; i++)
        for (let j = 0; j < size; j++){
            if (matrix[i][j] == 1)
                ctx_aux.fillStyle = colors[1];
            else
                ctx_aux.fillStyle = colors[0];
            ctx_aux.fillRect(dimension*j, dimension*i, dimension, dimension);
        }
    ctx_aux.stroke();
}

function draw_grid(size, dimension) {
    for (let i = 0; i < size; i++)
        for (let j = 0; j < size; j++)
            ctx.rect(dimension*j, dimension*i, dimension, dimension);
    ctx.stroke()
}

function check_neighbours(i, j, matrix, m_size) {
    let row = i-1;
    let col = j-1;
    if (row < 0)
        row = m_size-1;
    if (col < 0)
        col = m_size-1;
    let neighbours = matrix[row][col];
    neighbours += matrix[row][j];
    neighbours += matrix[row][(j + 1) % m_size];
    neighbours += matrix[i][(j + 1) % m_size];
    neighbours += matrix[(i + 1) % m_size][(j + 1) % m_size];
    neighbours += matrix[(i + 1) % m_size][j];
    neighbours += matrix[(i + 1) % m_size][col];
    neighbours += matrix[i][col];

    return neighbours;
}

function next_population(size, matrix, aux) {
    let vecinos = 0;
    let aux_counter = 0;
    for (let i = 0; i < size; i++)
        for (let j = 0; j < size; j++) {
            vecinos = check_neighbours(i, j, aux, size);
            if (aux[i][j] == 1) {
                if (vecinos < rule[0] || vecinos > rule[1]){
                    matrix[i][j] = 0;
                    //aux_counter--;
                }
            } 
            else if (rule[2] <= vecinos && vecinos <= rule[3]) {
                matrix[i][j] = 1;
                //aux_counter++;
            }
            if (matrix[i][j] == 1)
                aux_counter++;
        }

    return aux_counter;
}

function copy_matrix(origen, destino) {
    for (let i = 0; i < origen.length; i++)
        for (let j = 0; j < origen.length; j++)
            destino[i][j] = origen[i][j];
}

function init() {
    size = get_size_matrix();
    total_population = size*size;
    dimension = 1;
    rule = get_rule();
    counter = 0;
    my_time = 0;
    suma = 0;
    interval = null;
    is_runinng = false;
    original = [];
    auxiliar = [];
    other_matrix = [];
    tau = get_tau();
    ones_distribution = get_distribution();
    colors = get_colors();
    type_function = get_type_function();
    myLineChart = create_chart(context);
    is_active = get_check_matrix();
    matrices = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[], 8:[]};

    while (dimension*size < CANVAS_SIZE) dimension++;

    for(let i=0; i<size; i++){
        original[i] = [];
        auxiliar[i] = [];
        for (let k = 1; k <= tau; k++)
            matrices[k][i] = [];
        for(let j=0; j<size; j++){
            original[i][j] = get_zero_or_one(ones_distribution);
            auxiliar[i][j] = original[i][j];
            if (auxiliar[i][j] == 1)
                counter++;
            for (let k = 1; k <= tau; k++)
                matrices[k][i][j] = 0;
        }
    }
}

function plot() {
    suma += counter;
    let promedio = suma/(my_time+1);
    promedio = promedio.toFixed(3);
    let densidad = promedio /(total_population);
    densidad = densidad.toFixed(3);
    information_output.innerHTML = "Promedio: " + promedio + ". Densidad: " + densidad;
    myLineChart.data.labels.push(my_time);
    myLineChart.data.datasets[0].data.push(counter);
    myLineChart.update();
}

function iterate() {
    my_time++;
    counter = next_population(size, original, auxiliar);
    copy_matrix(original, auxiliar);
    draw_matrix(size, dimension, original);
    plot();
}

function get_size_matrix() {
    return parseInt(document.getElementById("size").value);
}

function get_rule() {
    let aux_rule = [2, 3, 3, 3];
    aux_rule[0] = parseInt(document.getElementById("b1").value);
    aux_rule[1] = parseInt(document.getElementById("b2").value);
    aux_rule[2] = parseInt(document.getElementById("s1").value);
    aux_rule[3] = parseInt(document.getElementById("s2").value);
    return aux_rule;
}

function get_type_function() {
    return parseInt(document.getElementById("input_function").value);
}

function get_tau() {
    return parseInt(document.getElementById("tau").value);
}

function get_colors() {
    let aux_colors = ["#FFFFFF", "#000000"]
    aux_colors[0] = document.getElementById("color_zeros").value;
    aux_colors[1] = document.getElementById("color_ones").value;
    return aux_colors;
}

function get_distribution() {
    let aux_dis = parseInt(slider_distribution.value)/100;
    aux_dis = aux_dis.toFixed(2);
    return parseFloat(aux_dis);
}

function apply_paridad(temporal) {
    let aux_paridad = 0;
    for (let i = 0; i < tau; i++)
        aux_paridad += temporal[i];
    if (aux_paridad % 2 == 0) return 1
    else return 0
}

function apply_moda(temporal) {
    let aux_moda = - (tau/2);
    for (let i = 0; i < tau; i++)
        aux_moda += temporal[i];
    if (aux_moda > 0) return 1
    else return 0
}

function apply_minimo(temporal) {
    if (apply_moda(temporal) == 0)
        return 1;
    else
        return 0;
}

function get_check_matrix() {
    return document.getElementById("check-matrix").checked;
}

let contador = 1;
function another_iteration() {
     if (is_active) {
        if (contador == 1)
            copy_matrix(original, matrices[1]);
        else if (contador == 2)
            copy_matrix(original, matrices[2]);
        else if (contador == 3)
            copy_matrix(original, matrices[3]);
        else if (contador == 4)
            copy_matrix(original, matrices[4]);
        else if (contador == 5)
            copy_matrix(original, matrices[5]);
        else if (contador == 6)
            copy_matrix(original, matrices[6]);
        else if (contador == 7)
            copy_matrix(original, matrices[7]);
        else if (contador == 8)
            copy_matrix(original, matrices[8]);

        contador++;
        if (contador > tau)
            contador = 1;
    }
    let aux_res = 0;
    if (is_active) {
        if (((my_time+1) % tau) == 0 && my_time > 0) {
            console.log("APLICANDO");
            for (let i = 0; i < size; i++){
                for (let j = 0; j < size; j++){
                    let arreglo = [];
                    for (let k = 1; k <= tau; k++)
                        arreglo.push(matrices[k][i][j])
                    if (type_function == TYPE_FUNCTION_DICT["MODA"])
                        auxiliar[i][j] = apply_moda(arreglo);
                    else if (type_function == TYPE_FUNCTION_DICT["PARIDAD"])
                        auxiliar[i][j] = apply_paridad(arreglo);
                    else
                        auxiliar[i][j] = apply_minimo(arreglo);
                }
            }
            if (is_auxiliar_showed)
                draw_aux_matrix(size, dimension, auxiliar);
        }
    }
    iterate();
}

document.getElementById("btn_start").addEventListener("click", function click(e) {
    e.preventDefault();
    init();
    plot();
    draw_grid(size, dimension);
    draw_matrix(size, dimension, original);
});

document.getElementById("check-matrix").addEventListener("click", function click(e) {
    is_active = get_check_matrix();
});

document.getElementById("btn_show_matrix").addEventListener("click", function click(e) {
    is_auxiliar_showed = !is_auxiliar_showed;
    if (!is_auxiliar_showed)
        ctx_aux.clearRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
});

document.getElementById("btn_next").addEventListener("click", function click(e) {
    e.preventDefault();
    another_iteration();
});

document.getElementById("btn_pause").addEventListener("click", function click(e) {
    e.preventDefault();
    console.log("PAUSE");
    is_runinng = !is_runinng;
    if (is_runinng)
        interval = setInterval(another_iteration, 250); // Aqui se hace lo del proyecto
    else {
        clearInterval(interval);
        interval = null;
    }
});

c.addEventListener("click", function click(e) {
    let my_y = e.pageY;
    let my_x = e.pageX - 15;
    let i = Math.floor(my_y/dimension);
    let j = Math.floor(my_x/dimension);
    if (original[i][j] == 1){
        original[i][j] = 0;
        auxiliar[i][j] = 0;
        ctx.fillStyle = colors[0];
    } else{
        original[i][j] = 1
        auxiliar[i][j] = 1;
        ctx.fillStyle = colors[1];
    }
    ctx.fillRect(dimension*j, dimension*i, dimension, dimension);
});