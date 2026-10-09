# 3D-визуализация насосной по принятым данным (мм). Кровля не моделируется: на эскизе
# высоты углов стен не совпадают (A2 и A3 не сходятся в одной точке), поэтому стены показаны отдельными панелями.
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure(figsize=(14, 10))
ax = fig.add_subplot(111, projection="3d")
ax.set_box_aspect((4000, 2500, 4500))
ax.view_init(elev=22, azim=-58)

def panel(p, color, alpha=0.85, edge="#222"):
    ax.add_collection3d(Poly3DCollection([p], facecolors=color, edgecolors=edge, linewidths=0.8, alpha=alpha))

def wall_x(x, y0, y1, h, color="#d9d4c7"):      # стена в плоскости X=const
    panel([(x, y0, 0), (x, y1, 0), (x, y1, h), (x, y0, h)], color)
def wall_y(y, x0, x1, h, color="#e6e1d3", door=None):  # стена в плоскости Y=const
    if door is None:
        panel([(x0, y, 0), (x1, y, 0), (x1, y, h), (x0, y, h)], color)
    else:
        dx0, dx1, dh = door
        # нижняя часть проёма, левая и правая тумбы, верхняя перемычка
        panel([(x0, y, 0), (dx0, y, 0), (dx0, y, h), (x0, y, h)], color)
        panel([(dx1, y, 0), (x1, y, 0), (x1, y, h), (dx1, y, h)], color)
        panel([(dx0, y, dh), (dx1, y, dh), (dx1, y, h), (dx0, y, h)], color)
        panel([(dx0, y, 0), (dx1, y, 0), (dx1, y, dh), (dx0, y, dh)], "#f6d5d5", alpha=0.9, edge="#c00")

# A1 — передняя стена y=0, 4000×3300
wall_y(0, 0, 4000, 3300)
# A3 — задняя стена y=2500, 4000 × 4500 (скат к 3800), дверь 1200×2200 справа
wall_y(2500, 0, 4000, 4500, door=(2800, 4000, 2200))
panel([(0, 2500, 4500), (4000, 2500, 3800), (4000, 2500, 4500)], "#d9d4c7", alpha=0.0, edge="#000")  # контур ската
# A2 — левая стена x=0, 2500×3300
wall_x(0, 0, 2500, 3300)
# A4 — правая стена x=4000, 2500×4500
wall_x(4000, 0, 2500, 4500)

# колонны (стойки) по сетке
for xx in (0, 1000, 2000, 3000, 4000):
    for yy in (0, 2500):
        h = 3300 if yy == 0 else 4500
        ax.plot([xx, xx], [yy, yy], [0, h], color="#333", lw=2.2)
for yy in (830, 1660):
    for xx in (0, 4000):
        ax.plot([xx, xx], [yy, yy], [0, 4500 if xx == 4000 else 3300], color="#333", lw=2.2)

# размеры
ax.plot([0, 4000], [-500, -500], [0, 0], color="#0044aa", lw=2)
ax.text(2000, -900, 0, "4000", color="#0044aa", ha="center", fontsize=12)
ax.plot([4500, 4500], [0, 2500], [0, 0], color="#0044aa", lw=2)
ax.text(4800, 1250, 0, "2500", color="#0044aa", fontsize=12)
ax.plot([-500, -500], [0, 0], [0, 3300], color="#0044aa", lw=2)
ax.text(-900, 0, 1650, "3300", color="#0044aa", fontsize=12)
ax.text(-900, 2500, 2250, "4500", color="#0044aa", fontsize=12)

ax.set_xlim(-600, 4800); ax.set_ylim(-1000, 3000); ax.set_zlim(0, 4800)
ax.set_xlabel("X, мм"); ax.set_ylabel("Y, мм"); ax.set_zlabel("Z, мм")
ax.set_title("Насосная — 3D-визуализация по принятым данным\n(кровля не моделируется, см. примечание)", fontsize=14)
ax.text2D(0.02, 0.02, "Стены A1 (3300), A2 (3300), A3 (4500→3800, дверь 1200×2200), A4 (4500)\n"
          "Колонны по сетке 1000 мм (условно). Размеры в мм.", transform=ax.transAxes, fontsize=10)
fig.savefig("visualization_3d.png", dpi=110, bbox_inches="tight")
print("ok")
