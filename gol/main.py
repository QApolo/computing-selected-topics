import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Button, TextBox


class Gol:
    def __init__(self):
        self.cantidad_unos = 0
        self.tiempo = 0
        self.historia_x = list()
        self.historia_y = list()
        self.intervalo = 1000
        self.tam = 100
        self.regla = [2, 3, 3, 3]
        self.pausa = True
        self.poblacion = np.random.randint(0, 2, size=(self.tam, self.tam))


gol = Gol()

for i in range(gol.tam):
    for j in range(gol.tam):
        if gol.poblacion[i, j] == 1:
            gol.cantidad_unos += 1

gol.historia_x = [gol.tiempo]
gol.historia_y = [gol.cantidad_unos]


def onClickPause(event):
    """Pausar la animacion"""
    gol.pausa ^= True


def actualizar_celulas(frameNum, img, gol):
    """Actualizar las celulas"""
    if not gol.pausa:
        nueva_poblacion = gol.poblacion.copy()
        for i in range(gol.tam):
            for j in range(gol.tam):
                vecinos = (gol.poblacion[i-1, j-1] + gol.poblacion[i-1, j] + gol.poblacion[i-1, (j+1) % gol.tam]
                           + gol.poblacion[i, (j+1) % gol.tam]+ gol.poblacion[(i+1) % gol.tam, (j+1) % gol.tam]
                           + gol.poblacion[(i+1) % gol.tam, j] + gol.poblacion[(i+1) % gol.tam, j-1] + gol.poblacion[i, j-1])

                if gol.poblacion[i, j] == 1:
                    if vecinos < gol.regla[0] or vecinos > gol.regla[1]:
                        nueva_poblacion[i, j] = 0
                        gol.cantidad_unos -= 1
                else:
                    if vecinos >= gol.regla[2] and vecinos <= gol.regla[3]:
                        nueva_poblacion[i, j] = 1
                        gol.cantidad_unos += 1

        img.set_data(nueva_poblacion)
        gol.poblacion[:] = nueva_poblacion[:]
        gol.tiempo += 1
        gol.historia_y.append(gol.cantidad_unos)
        gol.historia_x.append(gol.tiempo)

    return img,

def submit(text):
    texto = text.split(",")
    gol.regla[0] = int(texto[0])
    gol.regla[1] = int(texto[1])
    gol.regla[2] = int(texto[2])
    gol.regla[3] = int(texto[3])

    print(texto)


fig, ax = plt.subplots()
img = ax.imshow(gol.poblacion, interpolation='nearest')
ax.axis('off')
ani = animation.FuncAnimation(fig, actualizar_celulas, fargs=(img, gol), frames=30, interval=gol.intervalo,save_count=1, blit=True)
axnext = plt.axes([0.71, 0.03, 0.2, 0.075])
bnext = Button(axnext, 'Pausar/Reanudar')
bnext.on_clicked(onClickPause)

axbox = plt.axes([0.2, 0.9, 0.2, 0.08])
text_box = TextBox(axbox, 'R(x1, x2, y1, y2):', initial="2, 3, 3, 3")
text_box.on_submit(submit)


fig2, ax2 = plt.subplots()
def animacion(i):
    ax2.clear()
    ax2.plot(gol.historia_x, gol.historia_y)


anima = animation.FuncAnimation(fig2, animacion, interval=gol.intervalo)

plt.show()