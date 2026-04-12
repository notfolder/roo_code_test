import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 4 * np.pi, 1000)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y, linewidth=2)
plt.xlabel("x")
plt.ylabel("sin(x)")
plt.title("Sine Wave")
plt.grid(True)
plt.axhline(0, color="black", linewidth=1)
plt.axvline(0, color="black", linewidth=1)
plt.show()
