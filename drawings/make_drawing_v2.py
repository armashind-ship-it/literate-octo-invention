# Чертёж насосной по принятым данным (drawings/accepted_data.md).
# Единицы: мм. Выход: nasosnaya_drawing.svg и .png
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

fig, ax = plt.subplots(figsize=(24, 26))
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-1500, 19500)
ax.set_ylim(-11500, 12500)

LW = 2.2
DIM = "#0044aa"
RED = "#c00000"

def line(x1, y1, x2, y2, lw=LW, c="black", ls="-"):
    ax.plot([x1, x2], [y1, y2], color=c, lw=lw, ls=ls, solid_capstyle="butt")

def dim_h(x1, x2, y, label, off=0):
    """Горизонтальный размер на уровне y (выносные линии вертикальные)."""
    line(x1, y, x2, y, 1.2, DIM)
    for x in (x1, x2):
        ax.plot([x - 60, x + 60], [y - 60, y + 60], color=DIM, lw=1.5)
    ax.text((x1 + x2) / 2, y + 110 + off, label, ha="center", va="bottom", fontsize=15, color=DIM)

def dim_v(y1, y2, x, label, off=0):
    line(x, y1, x, y2, 1.2, DIM)
    for y in (y1, y2):
        ax.plot([x - 60, x + 60], [y - 60, y + 60], color=DIM, lw=1.5)
    ax.text(x - 110 - off, (y1 + y2) / 2, label, ha="right", va="center", fontsize=15, color=DIM, rotation=90)

def wall_elev(x0, y0, W, H, bays, title, area, top_right=None, door=None, roof_left=None):
    """Развёртка стены. x0,y0 — левый нижний угол. bays — ширины секций по X."""
    if top_right is None:
        top_right = H
    if roof_left is None:
        roof_left = H
    pts = [(x0, y0), (x0 + W, y0), (x0 + W, y0 + top_right), (x0, y0 + roof_left)]
    ax.add_patch(Polygon(pts, closed=True, fill=False, ec="black", lw=3))
    # стойки
    xs = [0]
    for b in bays:
        xs.append(xs[-1] + b)
    for xx in xs:
        line(x0 + xx, y0, x0 + xx, y0 + (roof_left + (top_right - roof_left) * xx / W) if xx else y0 + roof_left, 1.6, "#333")
    # размеры
    for i, b in enumerate(bays):
        ax.text(x0 + (xs[i] + xs[i + 1]) / 2, y0 - 330, f"{b}", ha="center", va="top", fontsize=13, color=DIM)
    dim_h(x0, x0 + W, y0 - 1150, f"{W} мм")
    dim_v(y0, y0 + roof_left, x0 - 500, f"{roof_left} мм")
    if top_right != roof_left:
        ax.text(x0 + W + 120, y0 + top_right, f"{top_right} мм", fontsize=14, color=DIM, va="center")
    if door:
        dx, dw, dh = door
        ax.add_patch(Rectangle((x0 + dx, y0), dw, dh, fc="#fbe3e3", ec=RED, lw=2.5))
        ax.text(x0 + dx + dw / 2, y0 + dh / 2, "ДВЕРЬ\n1200×2200", ha="center", va="center", color=RED, fontsize=13)
        ax.text(x0 + dx + dw / 2, y0 + dh + 90, f"{dw}", ha="center", color=RED, fontsize=13)
    ax.text(x0, y0 + max(roof_left, top_right) + 450, title, fontsize=21, weight="bold", va="bottom")
    ax.text(x0, y0 + max(roof_left, top_right) + 200, f"Площадь по эскизу: {area} м²", fontsize=14, color="#333", va="bottom")

# ---------- Заголовок ----------
ax.text(-1200, 11200, "НАСОСНАЯ — чертёж стен, каркаса и спецификация", fontsize=30, weight="bold")
ax.text(-1200, 10700, "Размеры в мм. Исходные данные: drawings/accepted_data.md (приняты пользователем).", fontsize=15, color="#444")

# ---------- План ----------
PX, PY = 0, 0          # левый нижний угол плана
PW, PH = 4000, 2500
ax.add_patch(Rectangle((PX, PY), PW, PH, fc="none", ec="black", lw=3.5))
ax.text(PX + PW / 2, PY + PH / 2, "ПЛАН\nнасосной", ha="center", va="center", fontsize=18, color="#555")
# стойки-колонны (узлы по периметру и по сетке)
for xx in (0, 1000, 2000, 3000, 4000):
    for yy in (0, PH):
        ax.add_patch(Rectangle((PX + xx - 45, PY + yy - 45), 90, 90, fc="black"))
for yy in (830, 1660):
    ax.add_patch(Rectangle((PX - 45, PY + yy - 45), 90, 90, fc="black"))
    ax.add_patch(Rectangle((PX + PW - 45, PY + yy - 45), 90, 90, fc="black"))
ax.text(PX + PW / 2, PY - 300, "A1 (4000×3300)", ha="center", va="top", fontsize=16, weight="bold")
ax.text(PX + PW / 2, PY + PH + 150, "A3 (4000×4500, скат)", ha="center", va="bottom", fontsize=16, weight="bold")
ax.text(PX - 160, PY + PH / 2, "A2", ha="right", va="center", fontsize=16, weight="bold", rotation=90)
ax.text(PX + PW + 160, PY + PH / 2, "A4", ha="left", va="center", fontsize=16, weight="bold", rotation=90)
dim_h(PX, PX + PW, PY - 1200, "4000")
dim_v(PY, PY + PH, PX - 1200, "2500")
ax.text(PX + 2000, PY + PH + 600, "ПЛАН (вид сверху)", ha="center", fontsize=20, weight="bold")

# ---------- Развёртки стен ----------
# A1 — 4000×3300, шаг стоек 1000 (условно)
wall_elev(6000, -1000, 4000, 3300, [1000, 1000, 1000, 1000], "A1 — 4000×3300", "13,2",
          )
# A3 — 4000×4500 со скатом до 3800, дверь 1200 в последней секции
wall_elev(6000, 5000, 4000, 4500, [930, 930, 940, 1200], "A3 — 4000×4500 (скат)", "4,8 (см. прим. 2)",
          top_right=3800, roof_left=4500, door=(2800, 1200, 2200))
# A2 — 2500×3300, шаг 830
wall_elev(11500, -1000, 2500, 3300, [830, 830, 840], "A2 — 2500×3300", "8,25")
# A4 — 2500×4500, шаг 830
wall_elev(11500, 5000, 2500, 4500, [830, 830, 840], "A4 — 2500×4500", "11,25")

# ---------- Дверь 1200×2200 ----------
DX, DY = 15800, -1000
ax.add_patch(Rectangle((DX, DY), 1200, 2200, fc="#fbe3e3", ec=RED, lw=3))
line(DX, DY + 2200, DX + 1200, DY, 1.2, RED)
line(DX, DY, DX + 1200, DY + 2200, 1.2, RED)
ax.text(DX + 600, DY + 1100, "ДВЕРЬ", ha="center", va="center", color=RED, fontsize=16, weight="bold")
dim_h(DX, DX + 1200, DY - 800, "1200")
dim_v(DY, DY + 2200, DX - 600, "2200")
ax.text(DX, DY + 2200 + 300, "Дверь 1200×2200 — 2 шт.", fontsize=18, weight="bold", va="bottom")
ax.text(DX, DY + 2200 + 130, "Каркас 20×60×1,5; петли 2/дв.; замок 1/дв.", fontsize=12, color="#333", va="bottom")

# ---------- Спецификация ----------
SX, SY = -1200, -5600
ax.text(SX, SY + 2000, "СПЕЦИФИКАЦИЯ МАТЕРИАЛОВ", fontsize=22, weight="bold")
rows = [
    ("Труба проф. 40×80×3", "114 стены + 24 стропила A5", "138 м/п"),
    ("Труба проф. 20×40×2", "54 стены + 25 обрешётка", "79 м/п"),
    ("Профлист (стены/кровля)", "по эскизу", "50,7 м²"),
    ("Труба проф. 20×60×1,5 (дверь)", "2 двери", "16 м/п"),
    ("Петля дверная", "2 на дверь × 2", "4 шт."),
    ("Замок врезной", "1 на дверь × 2", "2 шт."),
]
ax.text(SX, SY + 1450, "Наименование", fontsize=14, weight="bold")
ax.text(SX + 6000, SY + 1450, "Расчёт", fontsize=14, weight="bold")
ax.text(SX + 11500, SY + 1450, "Кол-во", fontsize=14, weight="bold")
y = SY + 1150
for name, calc, q in rows:
    ax.text(SX, y, name, fontsize=14)
    ax.text(SX + 6000, y, calc, fontsize=14)
    ax.text(SX + 11500, y, q, fontsize=14, weight="bold", color=RED)
    line(SX, y - 150, SX + 14000, y - 150, 0.6, "#bbb")
    y -= 420

# ---------- Примечания ----------
notes = [
    "Примечания:",
    "1. Шаг стоек A1 (1000 мм) условный — на эскизе не подтверждён.",
    "2. Площадь A3 по эскизу 4,8 м² соответствует полосе 4000×1200, а не полной стене 4000×4500 (18 м²). Требует уточнения.",
    "3. Длина ската A5 «4300» и высота 1200 — не подтверждены; на чертеже не показаны.",
    "4. «10,75 м³» и «31,24 м²» — не проверены, в спецификацию не входят.",
]
ny = -9800
for n in notes:
    ax.text(SX, ny, n, fontsize=13, color="#333")
    ny -= 300

fig.savefig("drawings/nasosnaya_drawing.png", dpi=90, bbox_inches="tight")
fig.savefig("drawings/nasosnaya_drawing.svg", bbox_inches="tight")
print("ok")
