# Генератор чертежа насосной (по эскизу): развёртка стен A1–A4, дверь, спецификация.
# Единицы: мм. Масштаб на листе: 1 мм = 0.1 px.
S = 0.1
out = []
def add(s): out.append(s)
def T(x, y, txt, size=28, anchor="start", weight="normal", color="#000"):
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{color}">{txt}</text>')
def R(x, y, w, h, stroke="#000", sw=2, fill="none", dash=""):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" stroke="{stroke}" stroke-width="{sw}" fill="{fill}"{d}/>')
def L(x1, y1, x2, y2, stroke="#000", sw=2):
    add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"/>')
def dimH(x1, x2, y, label):  # горизонтальный размер
    L(x1, y, x2, y, "#0044aa", 1.5)
    L(x1, y-12, x1, y+12, "#0044aa", 1.5); L(x2, y-12, x2, y+12, "#0044aa", 1.5)
    T((x1+x2)/2, y-8, label, 24, "middle", color="#0044aa")
def dimV(y1, y2, x, label):  # вертикальный размер
    L(x, y1, x, y2, "#0044aa", 1.5)
    L(x-12, y1, x+12, y1, "#0044aa", 1.5); L(x-12, y2, x+12, y2, "#0044aa", 1.5)
    add(f'<text transform="translate({x-14:.1f},{(y1+y2)/2:.1f}) rotate(-90)" font-family="Arial" font-size="24" text-anchor="middle" fill="#0044aa">{label}</text>')

def elevation(x0, y0, W, H, bays, title, sub, top_h=None, door=None):
    """W, H в мм; bays — список ширин проёмов/секций (мм); top_h — высота стойки справа (скат)."""
    w, h = W*S, H*S
    R(x0, y0, w, h, sw=3)
    # стойки
    xs = [0]; acc = 0
    for b in bays:
        acc += b; xs.append(acc)
    for i, xx in enumerate(xs):
        L(x0+xx*S, y0, x0+xx*S, y0+h, "#333", 2)
    # горизонтальные ригели (через ~1100 мм)
    yy = 1100
    while yy < H:
        L(x0, y0+h-yy*S, x0+w, y0+h-yy*S, "#999", 1.2)
        yy += 1100
    # профлист — диагональ сверху (кровля/скат)
    if top_h:
        L(x0, y0+(H-top_h)*S*0+0, x0+w, y0+(H-top_h)*S, "#c00", 3)
    if door:
        dx, dw, dh = door
        R(x0+dx*S, y0+h-dh*S, dw*S, dh*S, "#c00", 2.5, "#fbe9e9")
        T(x0+(dx+dw/2)*S, y0+h-dh*S/2, "Дверь", 26, "middle", color="#c00")
    # номера секций и размеры по звеньям
    for i, b in enumerate(bays):
        T(x0+(xs[i]+b/2)*S, y0+h+44, f"{b}", 24, "middle", color="#0044aa")
    dimH(x0, x0+w, y0+h+80, f"{W} мм")
    dimV(y0, y0+h, x0-40, f"{H} мм")
    T(x0, y0-70, title, 40, "start", "bold")
    T(x0, y0-28, sub, 26, "start", color="#444")

# ---- Лист: заголовок ----
T(60, 90, "Насосная. Чертёж каркаса и стен по эскизу (развёртка A1–A4)", 50, "start", "bold")
T(60, 135, "Размеры в мм. Масштаб 1:50 (на листе условный). Ветка: arena/8a4d4a1f-literate-octo-invention", 28, "start", color="#444")

# A1: 4000 x 3300, пролёты 4 x 1000 (условно)
elevation(150, 300, 4000, 3300, [1000,1000,1000,1000], "A1 — стена 4000×3300", "Площадь ≈ 13,2 м²  |  стойки шаг 1000 (уточнить)")
# A3: 4000 x 4500 со скатом (верх 3800), проём-дверь 1200
elevation(150, 1000, 4000, 4500, [930,930,930,1210], "A3 — стена 4000×4500 (скат)", "Площадь ≈ 4,8 м²  |  шаг 930, 1200 — дверь", top_h=3800, door=(2800,1200,2200))
# A2: 2500 x 3300
elevation(1000, 300, 2500, 3300, [830,830,830], "A2 — стена 2500×3300", "Площадь ≈ 8,25 м²  |  шаг 830")
# A4: 2500 x 4500
elevation(1000, 1000, 2500, 4500, [830,830,830], "A4 — стена 2500×4500", "Площадь ≈ 11,25 м²  |  шаг 830")

# Дверь 1200 x 2200
elevation(1800, 300, 1200, 2200, [600,600], "Дверь 1200×2200 (2 шт.)", "Каркас 20×60×1,5 (16 м/п на 2 шт.), петли 2 шт/дверь, замок врезной 1 шт/дверь")

# Спецификация
sx, sy = 150, 3450
T(sx, sy, "Спецификация материалов (по эскизу)", 40, "start", "bold")
rows = [
 ("Труба проф. 40×80×3", "30+20+28+36 = 114 м/п  + 12×2 (A5 стропила) = 24 м/п", "138 м/п"),
 ("Труба проф. 20×40×2", "10+10+14+20 = 54 м/п  + 25 м/п (обрешётка) = 79 м/п", "79 м/п"),
 ("Профлист (стены/кровля)", "Суммарно по эскизу", "50,7 м²"),
 ("Труба проф. 20×60×1,5 (дверь)", "На 2 двери", "16 м/п"),
 ("Петля дверная", "2 на дверь × 2 двери", "4 шт."),
 ("Замок врезной (дверь)", "1 на дверь × 2 двери", "2 шт."),
]
y = sy + 60
for name, calc, q in rows:
    T(sx, y, name, 28, weight="bold"); T(sx+900, y, calc, 26); T(sx+2300, y, q, 28, weight="bold", color="#c00")
    L(sx, y+14, sx+2500, y+14, "#bbb", 1)
    y += 60
T(sx, y+40, "Примечания: 1) Расшифровка эскиза выполнена вручную, часть цифр неразборчива (A5: «4300 раз.?», высота 1200).", 24, color="#666")
T(sx, y+80, "2) 4300 — длина ската/стропила на A5, уточнить. 3) «10,75 м³» и «31,24 м²» — не проверены, в спецификацию не включены.", 24, color="#666")
T(sx, y+120, "3) Сумма 138 м/п и 79 м/п совпадает с итогами на эскизе — это подтверждает прочтение труб.", 24, color="#666")

H = y + 200
svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="2300" height="{H:.0f}" viewBox="0 0 2300 {H:.0f}"><rect width="100%" height="100%" fill="#fff"/>' + "\n".join(out) + '</svg>'
open("drawings/nasosnaya.svg", "w", encoding="utf-8").write(svg)
print("ok", H)
