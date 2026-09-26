# 场景共用：宿舍楼立面、电线杆、岳麓山、云、地面
from hd import *
from comp import *


def mountain(s, y_base, x0=0, x1=960, h=70, color='#6F9C92', dark='#5B8479', light='#8DB7AA'):
    """岳麓山剪影：多层山脊 + 硬边亮面"""
    pts = [(x0, y_base)]
    n = 22
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        t = k / n
        peak = math.exp(-((t - 0.42) / 0.26) ** 2) * h + math.exp(-((t - 0.8) / 0.12) ** 2) * h * 0.45
        pts.append((x, y_base - peak - R.uniform(0, 6) - h * 0.15))
    pts.append((x1, y_base))
    s.shape(pts, color, 2.2, amp=1.2, step=10)
    # 亮面（左侧受光）
    for k in range(5):
        cx = x0 + (x1 - x0) * R.uniform(0.2, 0.7)
        s.fill(jag(cx, y_base - h * 0.55, h * 0.25, sy=0.5), light, amp=0, opacity=0.7)
    # 山上树丛纹理
    brush_strokes(s, x0 + 10, y_base - h * 0.9, (x1 - x0) - 20, h * 0.8, 70, dark, 3, 7, 1.2, 2.2, opacity=0.5)
    # 山顶电视塔（岳麓山标志物，一个小小的暖色点）
    return pts


def cloud(s, cx, cy, w, fill=CREAM, night=False):
    pts = []
    n = 16
    for k in range(n):
        a = 2 * math.pi * k / n
        rx = w / 2 * (1 + R.uniform(-0.1, 0.15))
        ry = w / 5 * (1 + (0.6 if 0.3 < a < 2.8 else 0) * 0) * (1 + R.uniform(-0.2, 0.3))
        y = cy + ry * math.sin(a) * (0.5 if math.sin(a) > 0 else 1.2)
        pts.append((cx + rx * math.cos(a), y))
    s.shape(pts, fill, 2.0, amp=1.4, step=6)
    s.fill([(cx - w * 0.4, cy + 2), (cx + w * 0.45, cy + 2), (cx + w * 0.38, cy + w * 0.08), (cx - w * 0.35, cy + w * 0.08)],
           shade_color(fill, 0.86), amp=0.5)


def ac_unit(s, x, y, w=22, h=15, night=False):
    body = CREAM2 if not night else '#7C8A84'
    s.shape(rrect(x, y, w, h, 2), body, 1.6, amp=0.3, step=4)
    s.fill(rect(x + w * 0.7, y + 1, w * 0.28, h - 2), shade_color(body, 0.8), amp=0)
    s.shape(ellipse(x + w * 0.38, y + h / 2, h * 0.34, h * 0.34, 10), shade_color(body, 0.7), 1.0, amp=0)
    s.line((x + w * 0.38 - 3, y + h / 2), (x + w * 0.38 + 3, y + h / 2), 0.8, OUT, amp=0)
    # 冷凝水管
    s.line((x + w - 3, y + h), (x + w - 2, y + h + 12), 1.1, OUT, amp=0.3, step=4, opacity=0.8)


def laundry(s, x0, x1, y, night=False):
    s.line((x0, y), (x1, y), 1.1, OUT, amp=0.2, step=6)
    x = x0 + 3
    cols = [RUST, MUSTARD, CREAM, '#7FA9B5', '#D9A28A', TEAL, '#B8C4B0']
    while x < x1 - 8:
        c = R.choice(cols)
        if night:
            c = shade_color(c, 0.55)
        w = R.uniform(6, 11)
        h = R.uniform(9, 17)
        kind = R.random()
        if kind < 0.4:  # T 恤
            pts = [(x, y), (x + w, y), (x + w + 2, y + 4), (x + w - 1, y + 5), (x + w - 1, y + h), (x + 1, y + h), (x + 1, y + 5), (x - 2, y + 4)]
        elif kind < 0.7:  # 裤子
            pts = [(x, y), (x + w, y), (x + w, y + h), (x + w * 0.58, y + h), (x + w * 0.5, y + h * 0.4), (x + w * 0.42, y + h), (x, y + h)]
        else:  # 毛巾
            pts = rect(x, y, w, h * 0.8)
        s.shape(pts, c, 1.1, amp=0.3, step=4)
        s.fill([(x + w * 0.6, y + 1), (x + w, y + 1), (x + w - 1, y + h * 0.8), (x + w * 0.6, y + h * 0.8)], shade_color(c, 0.8), amp=0, opacity=0.8)
        x += w + R.uniform(3, 7)


def dorm_facade(s, x0, x1, y_top, y_bot, floors, wall=CREAM, tile=True, night=False, lit=None):
    """宿舍楼立面（3/4 俯视看到的南立面）。lit: 夜晚亮灯概率"""
    s.shape(rect(x0, y_top, x1 - x0, y_bot - y_top), wall, 2.8, amp=0.6, step=10)
    fh = (y_bot - y_top) / floors
    if tile:  # 白瓷砖格
        for yy in range(int(y_top) + 6, int(y_bot), 7):
            s.add(f'<line x1="{x0}" y1="{yy}" x2="{x1}" y2="{yy}" stroke="{shade_color(wall, 0.9)}" stroke-width="0.6"/>')
    # 楼层腰线（红砖色小面积）
    for f in range(floors + 1):
        yy = y_top + f * fh
        s.fill(rect(x0, yy - 3, x1 - x0, 5), shade_color(wall, 0.84), amp=0.3, step=10)
    unit_w = 92
    n = int((x1 - x0) // unit_w)
    for f in range(floors):
        yy = y_top + f * fh
        for u in range(n):
            ux = x0 + 10 + u * unit_w
            # 窗
            glass = '#557F80' if not night else ('#F4D27A' if R.random() < (lit or 0) else '#2C3E43')
            s.shape(rect(ux + 8, yy + 8, 44, fh - 22), glass, 1.8, amp=0.3, step=6)
            if not night or glass == '#2C3E43':
                s.fill([(ux + 10, yy + 10), (ux + 22, yy + 10), (ux + 14, yy + fh - 16), (ux + 10, yy + fh - 16)], '#7FAAA8', amp=0, opacity=0.5)
            else:
                s.fill(rect(ux + 10, yy + 10, 40, fh - 26), '#FFE8A6', amp=0, opacity=0.5)
                # 窗帘
                s.fill(rect(ux + 10, yy + 10, 10, fh - 26), '#E0A36A', amp=0, opacity=0.8)
            s.line((ux + 30, yy + 8), (ux + 30, yy + fh - 14), 1.2, OUT, amp=0.2)
            # 阳台栏杆
            s.shape(rect(ux + 2, yy + fh - 18, 58, 12), shade_color(wall, 0.92), 1.8, amp=0.3, step=6)
            for bx in range(int(ux + 7), int(ux + 58), 6):
                s.line((bx, yy + fh - 17), (bx, yy + fh - 7), 0.7, OUT, amp=0, opacity=0.5)
            # 晾衣
            if R.random() < 0.8:
                laundry(s, ux + 4, ux + 58, yy + 5, night=night)
            # 空调外机
            ac_unit(s, ux + 64, yy + fh - 30 + R.uniform(-4, 2), night=night)
    # 楼体右侧冷阴影
    s.fill(rect(x1 - 14, y_top, 14, y_bot - y_top), SHADOW, amp=0.3, opacity=0.25)


def pole(s, x, y, h=120, night=False):
    """电线杆（立面，底部在 x,y）"""
    s.fill([(x + 4, y), (x + 60, y + 18), (x + 58, y + 24), (x + 2, y + 6)], SHADOW, amp=0, opacity=0.25)
    s.shape([(x - 4, y), (x - 3, y - h), (x + 3, y - h), (x + 4, y)], CONC if not night else '#5B625E', 2.2, amp=0.4, step=6)
    s.fill([(x, y), (x + 1, y - h), (x + 3, y - h), (x + 4, y)], shade_color(CONC, 0.78), amp=0)
    for k, cw in ((0, 30), (16, 22)):
        s.shape(rect(x - cw / 2, y - h + 8 + k, cw, 4), '#6A6F68', 1.6, amp=0.2)
        for dx in (-cw / 2 + 3, cw / 2 - 3):
            s.shape(rect(x + dx - 1.5, y - h + 3 + k, 3, 5), CREAM2, 1, amp=0)
    # 小广告 & 变压器
    s.shape(rect(x - 12, y - h + 42, 24, 20), '#7C857E', 1.8, amp=0.3)
    s.fill(rect(x - 11, y - h + 43, 7, 18), shade_color('#7C857E', 1.2), amp=0)
    s.shape(rect(x - 4, y - 50, 8, 14), CREAM, 1, amp=0.2)
    s.shape(rect(x - 4, y - 32, 8, 10), MUSTARD, 1, amp=0.2)
    return (x - 12, y - h + 10), (x + 12, y - h + 10), (x - 8, y - h + 26), (x + 8, y - h + 26)


def ground(s, x, y, w, h, base=CONC2, night=False, seed_=3):
    s.fill(rect(x, y, w, h), base, amp=0)
    R2 = random.Random(seed_)
    # 水泥板缝
    for gx in range(int(x), int(x + w), 120):
        s.add(f'<line x1="{gx + R2.uniform(-3, 3):.1f}" y1="{y}" x2="{gx + R2.uniform(-3, 3):.1f}" y2="{y + h}" stroke="{shade_color(base, 0.85)}" stroke-width="1.2"/>')
    # 斑驳笔触
    brush_strokes(s, x, y, w, h, int(w * h / 900), shade_color(base, 0.9), 6, 16, 1.5, 3.5, ang=0.1, opacity=0.5)
    brush_strokes(s, x, y, w, h, int(w * h / 1600), shade_color(base, 1.12), 4, 10, 1.2, 2.5, ang=0.1, opacity=0.6)
    # 裂缝
    for _ in range(int(w * h / 60000) + 1):
        cx, cy = x + R2.uniform(0, w), y + R2.uniform(0, h)
        pts = [(cx, cy)]
        for k in range(5):
            cx += R2.uniform(4, 12); cy += R2.uniform(-5, 5)
            pts.append((cx, cy))
        s.ink(pts, False, 0.9, 0.5, shade_color(base, 0.7), amp=0.4, step=4, opacity=0.7)


def leaves(s, x, y, w, h, n, night=False):
    """落叶 / 桂花"""
    cols = ['#B8A04A', MUSTARD, '#8FA36E', ORANGE, '#C9B26A']
    out = []
    for _ in range(n):
        px, py = R.uniform(x, x + w), R.uniform(y, y + h)
        c = R.choice(cols)
        if night:
            c = shade_color(c, 0.5)
        a = R.uniform(0, 180)
        L = R.uniform(2.2, 4.5)
        out.append(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{L:.1f}" ry="{L * 0.45:.1f}" fill="{c}" transform="rotate({a:.0f} {px:.1f} {py:.1f})" fill-opacity="0.85"/>')
    s.add(''.join(out))
