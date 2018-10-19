import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys

fig = plt.figure("Historia de la hormiga de Langton")
fig.suptitle("Historia de la hormiga de Langton")
fig.add_axes()
ax1 = fig.add_subplot(1, 1, 1)
archivo = sys.argv[1]

def animacion(i, *args):
    info = open(args[0], "r").read()
    lineas = info.split("\n")
    xs = []
    obreras = []
    soldados = []
    reinas = []
    for linea in lineas:
        if len(linea) > 1:
            x, obrera, soldado, reina = linea.split(",")
            xs.append(int(x))
            obreras.append(int(obrera))
            soldados.append(int(soldado))
            reinas.append(int(reina))

    ax1.clear()
    ax1.plot(xs, obreras, label="Obreras")
    ax1.plot(xs, soldados, label="Soldados")
    ax1.plot(xs, reinas, label="Reinas")
    legend = ax1.legend()
    legend.get_frame()
    ax1.set_xlabel('Generación')
    ax1.set_ylabel('Cantidad')


ani = animation.FuncAnimation(fig, animacion, interval=10000, fargs=(archivo,))
plt.show()
