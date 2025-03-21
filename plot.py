import matplotlib.pyplot as plt

fig, axes = plt.subplots(3, 3, figsize=(12, 12))

axes[0, 0].set_title("Altitude",fontsize=12, fontweight='bold')
axes[0, 1].set_title("Temperature",fontsize=12, fontweight='bold')
axes[0, 2].set_title("Pressure",fontsize=12, fontweight='bold')
axes[1, 0].set_title("Accelerometer",fontsize=12, fontweight='bold')
axes[1, 1].set_title("Gyroscope",fontsize=12, fontweight='bold')
axes[1, 2].set_title("Battery",fontsize=12, fontweight='bold')
axes[2, 0].set_title("GPS",fontsize=12, fontweight='bold')
axes[2, 1].set_title("Velocity",fontsize=12, fontweight='bold')
axes[2, 2].set_title("Energy Consumption",fontsize=12, fontweight='bold')

for ax in axes.flatten():
    ax.set_xlabel("Time (s)", fontsize=12)


for ax in axes.flatten():
    ax.grid(True)

plt.subplots_adjust(hspace=0.5, wspace=0.5)

plt.show()