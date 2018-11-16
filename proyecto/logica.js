/*
*
* Tau debe de ir de 3 a 8
*
*/
function getRandomArbitrary(min, max) {
    return Math.floor(Math.random() * max) + min
}

function draw_matrix(size, dimension, matrix) {
    console.log("draw_matrix");
    for (let i = 0; i < size; i++)
        for (let j = 0; j < size; j++){
            if (matrix[i][j] == 1)
                ctx.fillStyle = "#000";
            else
                ctx.fillStyle = "#FFF";
            ctx.fillRect(dimension*j, dimension*i, dimension, dimension);
        }
    ctx.stroke();
}

function draw_grid(size, dimension) {
    console.log("draw_grid");
    for (let i = 0; i < size; i++)
        for (let j = 0; j < size; j++){
            ctx.rect(dimension*j, dimension*i, dimension, dimension);
        }
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
                if (vecinos < regla[0] || vecinos > regla[1]){
                    matrix[i][j] = 0;
                    aux_counter--;
                }
            } 
            else if (regla[2] <= vecinos && vecinos <= regla[3]) {
                matrix[i][j] = 1;
                aux_counter++;
            }
        }

    return aux_counter;
}

function copy_matrix(origen, destino) {
    for (let i = 0; i < origen.length; i++)
        for (let j = 0; j < origen.length; j++)
            destino[i][j] = origen[i][j];
}

let CANVAS_SIZE = 1000;
// estas variables se reinician al dar click en Iniciar/Reiniciar
let c = document.getElementById("canvas");
let ctx = c.getContext("2d");
ctx.lineWidth="0.1";
let size = 100;
let dimension = 1;
let regla = [2, 3, 3, 3];
let counter = 0;
let my_time = 0;
let data;
let suma = 0;
var information = document.getElementById("information");
let interval = null;
let ejecutar = false;

while (dimension*size < CANVAS_SIZE) dimension++;

let original = [];
let auxiliar = [];
for(let i=0; i<size; i++){
    original[i] = [];
    auxiliar[i] = [];
    for(let j=0; j<size; j++){
        original[i][j] = getRandomArbitrary(0, 2);
        auxiliar[i][j] = original[i][j];
        if (auxiliar[i][j] == 1) {
            counter++;
        }
    }
}

draw_grid(size, dimension);
draw_matrix(size, dimension, original);

var slider = document.getElementById("distribution");
var output = document.getElementById("distribution_value");
output.innerHTML = slider.value;
slider.oninput = function(e) {
    e.preventDefault();
    output.innerHTML = this.value;
}

var context = document.getElementById("myChart");
var myLineChart = new Chart(context, {
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

function iterate() {
    suma += counter;
    let promedio = suma/(my_time+1);
    promedio = promedio.toFixed(3);
    let densidad = promedio /(size*size);
    densidad = densidad.toFixed(3);
    information.innerHTML = "Promedio: " + promedio + " densidad: " + densidad;
    myLineChart.data.labels.push(my_time);
    myLineChart.data.datasets[0].data.push(counter);
    myLineChart.update();
    my_time++;
    counter += next_population(size, original, auxiliar);
    copy_matrix(original, auxiliar);
    draw_matrix(size, dimension, original);
}

document.getElementById("btn_next").addEventListener("click", function click(e) {
    iterate();
});

document.getElementById("btn_pause").addEventListener("click", function click(e) {
    console.log("PAUSE");
    ejecutar = !ejecutar;
    if (ejecutar)
        interval = setInterval(iterate, 200); // Aqui se hace lo del proyecto
    else{
        clearInterval(interval);
        interval = null;
    }
});