let matriz = new Array(100);
for (let i = 0; i<100; i++)
    matriz[i] = new Array(100);

function obtener_posicion(x, y) {
    return x/y;
}
function iniciar(matriz) {
    // body...
    let canvas = document.getElementById("canvas");
    if (canvas.getContext) {
        let ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, 1000, 1000);
        for (i = 0; i < 1000; i+=10) {
            for (j = 0; j < 1000; j+=10) {
                ctx.fillRect(i, j, 10, 10);
                matriz[i/10][j/10] = {"x":i, "y":j, "val": 0};
            }
        }
        ctx.clearRect(0, 0, 10, 10);
    }
}
iniciar(matriz);
let canvas = document.getElementById("canvas");
canvas.addEventListener('click', function(e) {
    debugger;
})