import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from matplotlib.widgets import Button, TextBox


class Gol:
    def __init__(self):
        self.cantidad_unos = 0


gol = Gol()
tam = 10  # tamano de la matriz
poblacion = np.random.randint(0, 2, size=(tam, tam))
pausa = True
intervalo = 500  # Milisegundos
cantidad_unos = 0
tiempo = 0
regla = [2, 3, 3, 3]

for i in range(tam):
    for j in range(tam):
        if poblacion[i, j] == 1:
            cantidad_unos += 1

historia_x = [tiempo]
historia_y = [cantidad_unos]


def onClickPause(event):
    """Pausar la animacion"""
    global pausa
    print(regla)
    pausa ^= True


def actualizar_celulas(frameNum, img, poblacion, tam):
    """Actualizar las celulas"""
    global cantidad_unos
    global tiempo
    global historia_x
    global historia_y
    if not pausa:
        nueva_poblacion = poblacion.copy()
        print(regla)
        for i in range(tam):
            for j in range(tam):
                vecinos = (poblacion[i - 1, j - 1] + poblacion[i - 1, j] + poblacion[i - 1, (j + 1) % tam] + poblacion[
                    i, (j + 1) % tam]
                           + poblacion[(i + 1) % tam, (j + 1) % tam] + poblacion[(i + 1) % tam, j] + poblacion[
                               (i + 1) % tam, j - 1]
                           + poblacion[i, j - 1])

                if poblacion[i, j] == 1:
                    if vecinos < regla[0] or vecinos > regla[1]:
                        nueva_poblacion[i, j] = 0
                        cantidad_unos -= 1
                else:
                    if vecinos >= regla[2] and vecinos <= regla[3]:
                        nueva_poblacion[i, j] = 1
                        cantidad_unos += 1

        img.set_data(nueva_poblacion)
        poblacion[:] = nueva_poblacion[:]
        tiempo += 1
        historia_y.append(cantidad_unos)
        historia_x.append(tiempo)

    return img,


def submit(text):
    texto = text.split(",")
    regla[0] = int(texto[0])
    regla[1] = int(texto[1])
    regla[2] = int(texto[2])
    regla[3] = int(texto[3])

    print(texto)


initial_text = "2, 3, 3, 3"

fig, ax = plt.subplots()
img = ax.imshow(poblacion, interpolation='nearest')
ax.axis('off')
ani = animation.FuncAnimation(fig, actualizar_celulas, fargs=(img, poblacion, tam), frames=30, interval=intervalo,
                              save_count=1, blit=True)
axnext = plt.axes([0.71, 0.03, 0.2, 0.075])
bnext = Button(axnext, 'Pausar/Reanudar')
bnext.on_clicked(onClickPause)

axbox = plt.axes([0.2, 0.9, 0.2, 0.08])
text_box = TextBox(axbox, 'R(x1, x2, y1, y2):', initial=initial_text)
text_box.on_submit(submit)

fig2, ax2 = plt.subplots()


def animacion(i):
    ax2.clear()
    ax2.plot(historia_x, historia_y)


anima = animation.FuncAnimation(fig2, animacion, interval=intervalo)

plt.show()