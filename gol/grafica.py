import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure('Historial de unos')
fig.suptitle("Historial de unos")
ax1 = fig.add_subplot(1, 1, 1)
def animacion(i):
    info = open("grafica.txt", "r").read()
    lineas = info.split("\n")
    xs = []
    ys = []
    promedio = 0
    for linea in lineas:
        if len(linea) > 1:
            x,y = linea.split(",")
            xs.append(int(x))
            promedio += int(y)
            ys.append(int(y))

    ax1.clear()
    ax1.plot(xs, ys)
    promedio = int(promedio/len(lineas))
    ax1.set_title("Promedio de unos: {} Densidad: {}".format(promedio, promedio/10000))


ani = animation.FuncAnimation(fig, animacion, interval=500)

plt.show()