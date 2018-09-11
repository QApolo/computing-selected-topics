import matplotlib.pyplot as plt
import numpy as np

image = np.random.randint(2, size=(1000, 1000))
fig =plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111)
i = ax.imshow(image)

plt.axis('off')
plt.show()