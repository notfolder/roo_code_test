import matplotlib.pyplot as plt
import numpy as np

# 時間軸の生成 (0-10 秒)
t = np.linspace(0, 10, 400)

# サインカーブの生成 (振幅 5, 周波数 1 Hz)
y = np.sin(2 * np.pi * t / 10)

# グラフの描画
plt.figure(figsize=(10, 6))
plt.plot(t, y)

# グラフの装飾
plt.title("Sine Wave")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.grid(True, alpha=0.3)

# グラフの表示
plt.show()
