# 精灵 & UI 组件（全部在各自精灵像素坐标系里画，方便 1× 预览）
from hd import *

LINE = 1.25   # 精灵描边基准宽（精灵像素单位）


def G(s, x, y, sc=1.0, rot=0, flipy=False):
    fy = ' scale(1,-1)' if flipy else ''
    s.add(f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f}) scale({sc:.3f}){fy}">')


def E(s):
    s.add('</g>')


def shade_color(hexc, k):
    """k<1 变暗并偏冷（往蓝绿偏），k>1 变亮偏暖"""
    h = hexc.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    if k < 1:
        r = r * k * 0.92; g = g * k * 1.0; b = b * k * 1.08 + 8
    else:
        t = k - 1
        r = r + (255 - r) * t; g = g + (250 - g) * t; b = b + (232 - b) * t
    c = lambda v: max(0, min(255, int(v)))
    return '#%02X%02X%02X' % (c(r), c(g), c(b))


def cast_shadow(s, pts, dx=2.2, dy=2.6, op=0.32, night=False):
    s.fill([(x + dx, y + dy) for x, y in pts], SHADOW if not night else '#0E2224', amp=0, opacity=op if not night else 0.5)


# ---------------- 电动车（24×48，车头朝上） ----------------
def bike_local(s, body=CREAM, seat='#5C6359', lw=LINE, own=False, basket=False, amp=0.22, night=False, shadow=True):
    body_d = shade_color(body, 0.78)
    body_l = shade_color(body, 1.25)
    seat_d = shade_color(seat, 0.72)
    if shadow:
        cast_shadow(s, rrect(4, 3, 16, 44, 6), night=night)
    # 轮子
    s.shape(rrect(9.6, 0.6, 4.8, 10, 2), '#3E4747', lw * 0.8, amp=0.1, step=3)
    s.shape(rrect(9.6, 38, 4.8, 9.6, 2), '#3E4747', lw * 0.8, amp=0.1, step=3)
    # 车身（下层）
    s.shape([(7, 13), (17, 13), (18.6, 20), (18.6, 42), (15.5, 44.5), (8.5, 44.5), (5.4, 42), (5.4, 20)], body, lw, amp=amp, step=3)
    # 车身右侧冷阴影
    s.fill([(15.2, 16), (18.4, 20), (18.4, 42), (15.4, 44.2), (15.2, 44)], body_d, amp=0.1, step=3)
    # 踏板
    s.fill(rrect(7.4, 16, 9.2, 8, 1.5), body_d, amp=0.1, step=3)
    s.line((8, 19.5), (16, 19.5), lw * 0.45, OUT, amp=0.1, step=3, opacity=0.6)
    s.line((8, 22), (16, 22), lw * 0.45, OUT, amp=0.1, step=3, opacity=0.6)
    # 车头
    head = [(8, 4.5), (16, 4.5), (18, 8), (17.4, 14.5), (6.6, 14.5), (6, 8)]
    s.shape(head, body, lw, amp=amp, step=3)
    s.fill([(14.6, 5.2), (16, 5), (17.8, 8), (17.2, 14), (14.6, 14)], body_d, amp=0.1, step=3)
    s.fill([(8.4, 5.4), (10, 5.4), (9, 12), (7.2, 12)], body_l, amp=0.1, step=3)
    # 车灯
    s.shape(rrect(9.8, 3.4, 4.4, 2.6, 1), '#F7F3D2' if not night else '#FFF1B0', lw * 0.6, amp=0, step=3)
    # 车把 + 后视镜
    s.shape(rrect(0.8, 9.2, 22.4, 2.6, 1.2), '#4A5352', lw * 0.8, amp=0.1, step=3)
    s.line((3.2, 9.4), (2.6, 6.2), lw * 0.7, OUT, amp=0, step=3)
    s.line((20.8, 9.4), (21.4, 6.2), lw * 0.7, OUT, amp=0, step=3)
    s.shape(ellipse(2.4, 5.2, 1.9, 1.4, 8), '#8FA3A0', lw * 0.6, amp=0, step=2)
    s.shape(ellipse(21.6, 5.2, 1.9, 1.4, 8), '#8FA3A0', lw * 0.6, amp=0, step=2)
    if basket:
        s.shape(rrect(7.6, 0.2, 8.8, 5.2, 1), '#7F8C86', lw * 0.6, amp=0.1, step=3)
        for xx in (9.8, 12, 14.2):
            s.line((xx, 0.6), (xx, 5), lw * 0.35, OUT, amp=0, step=3, opacity=0.7)
    # 座垫（座套）
    s.shape(rrect(7.2, 24.2, 9.6, 15.6, 4.2), seat, lw, amp=amp, step=3)
    s.fill(rrect(13.6, 25.5, 3, 13, 1.5), seat_d, amp=0.1, step=3)
    s.fill(rrect(8.4, 26.4, 1.8, 7, 0.9), shade_color(seat, 1.3), amp=0.05, step=3)
    if own:  # 座套缝线 + 小挂饰
        s.line((12, 25.6), (12, 38.4), lw * 0.45, shade_color(seat, 0.55), amp=0.15, step=2, opacity=0.8)
    # 尾架 + 尾灯
    s.shape(rrect(8.2, 40.4, 7.6, 3.6, 1), '#56605E', lw * 0.7, amp=0, step=3)
    s.fill(rrect(10, 44.3, 4, 1.4, 0.6), RUST if not night else '#FF6A4A', amp=0)


def bike(s, x, y, sc=1.0, rot=0, **kw):
    """x,y = 车中心"""
    G(s, x, y, sc, rot)
    G(s, -12, -24)
    bike_local(s, **kw)
    E(s); E(s)


# ---------------- 人物 ----------------
def person_top(s, cx, cy, shirt='#6C9AA0', hair='#3A3F3F', bag=RUST, helmet=None, lw=LINE, arms=None, shoulder=18, night=False):
    """俯视人：肩 + 头 + 书包。arms=[(hx,hy),(hx,hy)] 手的目标点"""
    sw = shoulder
    shirt_d = shade_color(shirt, 0.75)
    if arms:
        for (hx, hy), sx in zip(arms, (cx - sw * 0.42, cx + sw * 0.42)):
            s.line((sx, cy), (hx, hy), lw * 2.6, OUT, amp=0.1, step=3)
            s.line((sx, cy), (hx, hy), lw * 1.3, shirt, amp=0.1, step=3)
            s.shape(ellipse(hx, hy, 1.6, 1.6, 8), '#E3C4A0', lw * 0.5, amp=0)
    s.shape(ellipse(cx, cy + 1, sw / 2, 5.2, 14), shirt, lw, amp=0.25, step=3)
    s.fill([(cx + 1, cy - 3.6), (cx + sw / 2 - 0.4, cy), (cx + sw / 2 - 1.5, cy + 4.5), (cx + 1, cy + 6)], shirt_d, amp=0.1, step=3)
    if bag:
        s.shape(rrect(cx - 5.5, cy + 3, 11, 7.5, 2.5), bag, lw, amp=0.2, step=3)
        s.fill(rrect(cx + 1.5, cy + 3.6, 3.4, 6.4, 1.4), shade_color(bag, 0.75), amp=0.1, step=3)
    if helmet:
        s.shape(ellipse(cx, cy - 2.4, 5.4, 5.8, 14), helmet, lw, amp=0.2, step=3)
        s.fill([(cx + 0.5, cy - 7.8), (cx + 5, cy - 4), (cx + 4.8, cy + 1.5), (cx + 0.5, cy + 3)], shade_color(helmet, 0.76), amp=0.1, step=3)
        s.fill(rrect(cx - 1, cy - 8, 2, 11, 1), shade_color(helmet, 1.3), amp=0)
        s.shape(rrect(cx - 3.6, cy - 9.2, 7.2, 2.4, 1), '#4A5A5E', lw * 0.6, amp=0)  # 护目镜
    else:
        s.shape(ellipse(cx, cy - 2.2, 4.8, 5.2, 14), hair, lw, amp=0.25, step=3)
        s.fill(ellipse(cx - 1.6, cy - 4, 1.4, 1.2, 8), shade_color(hair, 1.4), amp=0)


def rider_local(s, bike_body=MUSTARD, seat='#C9962E', shirt='#6C9AA0', helmet=CREAM2, bag='#5C8A86', night=False, delivery=False, lw=LINE):
    G(s, 4, 4)
    bike_local(s, body=bike_body, seat=seat, own=not delivery, night=night)
    E(s)
    if delivery:  # 外卖箱
        cast_shadow(s, rrect(6.5, 34, 19, 18, 2), night=night)
        s.shape(rrect(6, 33, 20, 18, 2), ORANGE, lw, amp=0.25, step=3)
        s.fill(rrect(18.5, 33.6, 7, 17, 1.5), shade_color(ORANGE, 0.76), amp=0.1, step=3)
        s.fill(rrect(7.4, 34.2, 11, 3, 1), shade_color(ORANGE, 1.25), amp=0.05)
        s.shape(rrect(10, 39.5, 12, 5, 1), CREAM, lw * 0.5, amp=0)
        s.line((12, 42), (20, 42), lw * 0.6, ORANGE, amp=0)
    person_top(s, 16, 24, shirt=shirt, helmet=helmet, bag=None if delivery else bag,
               arms=[(6.2, 14.6), (25.8, 14.6)], shoulder=17, night=night)


def rider(s, x, y, sc=1.0, rot=0, flipy=False, **kw):
    G(s, x, y, sc, rot, flipy)
    G(s, -16, -28)
    rider_local(s, **kw)
    E(s); E(s)


def walker_local(s, shirt='#8DA7B5', hair='#3A3F3F', bag=RUST, step_phase=1, lw=LINE, night=False):
    # 28×28
    cast_shadow(s, ellipse(14, 15, 9, 7, 12), night=night)
    # 腿/脚（迈步）
    s.shape(rrect(8.5, 13 - 6 * step_phase, 4, 7, 2), '#4D5A60', lw * 0.7, amp=0.1, step=2)
    s.shape(rrect(15.5, 13 + 3 * step_phase, 4, 7, 2), '#4D5A60', lw * 0.7, amp=0.1, step=2)
    person_top(s, 14, 13, shirt=shirt, hair=hair, bag=bag, lw=lw,
               arms=[(4.5, 13 + 5 * step_phase), (23.5, 13 - 5 * step_phase)], shoulder=16)


def walker(s, x, y, sc=1.0, rot=0, **kw):
    G(s, x, y, sc, rot)
    G(s, -14, -14)
    walker_local(s, **kw)
    E(s); E(s)


def pusher(s, x, y, sc=1.0, night=False):
    """推车：人走在车左侧扶车把（40×56）"""
    G(s, x, y, sc)
    G(s, -20, -28)
    G(s, 14, 4)
    bike_local(s, body=MUSTARD, seat='#C9962E', own=True, night=night)
    E(s)
    cast_shadow(s, ellipse(9, 26, 8, 6, 12), night=night)
    s.shape(rrect(3.5, 26, 4, 7, 2), '#4D5A60', LINE * 0.7, amp=0.1, step=2)
    s.shape(rrect(9.5, 20, 4, 7, 2), '#4D5A60', LINE * 0.7, amp=0.1, step=2)
    person_top(s, 8.5, 23, shirt='#6C9AA0', helmet=None, bag='#5C8A86', arms=[(15.4, 14.6), (19, 17)], shoulder=15)
    E(s); E(s)


# ---------------- 校车 64×140 ----------------
def bus_local(s, lw=LINE * 1.5):
    cast_shadow(s, rrect(3, 4, 60, 136, 10), dx=4, dy=5)
    s.shape(rrect(2, 2, 60, 136, 10), CREAM, lw, amp=0.4, step=5)
    s.fill(rrect(46, 6, 14, 128, 6), shade_color(CREAM, 0.83), amp=0.2, step=5)
    # 前挡风（车头朝上）
    s.shape([(8, 6), (56, 6), (58, 20), (6, 20)], '#4F7C7E', lw * 0.8, amp=0.3, step=4)
    s.fill([(12, 8), (22, 8), (16, 18), (9, 18)], '#8FC2BD', amp=0.1, step=4, opacity=0.7)
    # 顶部青绿腰线 + 锈红细条
    s.fill(rect(4, 26, 56, 8), TEAL, amp=0.2, step=4)
    s.fill(rect(4, 34, 56, 2.5), RUST, amp=0.1, step=4)
    # 空调机
    s.shape(rrect(16, 58, 32, 26, 4), CONC2, lw * 0.8, amp=0.3, step=4)
    s.fill(rrect(36, 59, 11, 24, 3), shade_color(CONC2, 0.8), amp=0.1, step=4)
    for yy in (64, 69, 74, 79):
        s.line((19, yy), (35, yy), lw * 0.4, OUT, amp=0.1, step=4, opacity=0.6)
    # 天窗
    s.shape(rrect(22, 100, 20, 14, 2), '#6D9A9A', lw * 0.6, amp=0.2, step=4)
    # 侧窗（露出一点侧面）
    for yy in range(42, 132, 15):
        s.fill(rect(2.6, yy, 3, 10), '#4F7C7E', amp=0)
        s.fill(rect(58.4, yy, 3, 10), '#3E6264', amp=0)
    s.fill(rect(24, 128, 16, 5), RUST, amp=0.1)


def bus(s, x, y, sc=1.0):
    G(s, x, y, sc); G(s, -32, -70); bus_local(s); E(s); E(s)


# ---------------- 充电桩 32×40（3/4 俯视） ----------------
PILE_SCREEN = {'idle': '#8ED6C8', 'plugged': '#9BF0A6', 'occupied': ORANGE, 'broken': '#2B3131'}


def pile_local(s, state='idle', lw=LINE, night=False):
    body = '#C9D2C6' if not night else '#8C9A94'
    cast_shadow(s, rrect(6, 30, 24, 10, 3), dx=2, dy=0, night=night)
    # 底座
    s.shape(rrect(5, 32, 22, 6, 2), CONC if not night else '#5E6862', lw, amp=0.2, step=3)
    # 柱身
    s.shape(rrect(7, 5, 18, 29, 3), body, lw, amp=0.25, step=3)
    s.fill(rrect(19.5, 6, 5, 27, 2), shade_color(body, 0.75), amp=0.1, step=3)
    # 顶盖（俯视看到的面）
    s.shape(rrect(6, 1.5, 20, 6, 2.5), TEAL if not night else '#3E8E8A', lw, amp=0.2, step=3)
    s.fill(rrect(7.5, 2.4, 8, 2, 1), shade_color(TEAL, 1.3) if not night else '#6BB3AD', amp=0)
    # 屏幕
    scr = PILE_SCREEN[state]
    s.shape(rrect(9.5, 10, 10, 8, 1.4), scr, lw * 0.8, amp=0.1, step=2)
    if state == 'broken':
        s.line((11, 11.5), (15, 15), lw * 0.5, '#6F7A78', amp=0.2, step=2)
        s.line((15, 15), (18, 12.5), lw * 0.5, '#6F7A78', amp=0.2, step=2)
        s.shape(rect(8.5, 20.5, 12, 3.4), MUSTARD, lw * 0.5, amp=0.2, step=2)  # 胶带
        s.line((9.5, 20.8), (11, 23.6), lw * 0.5, OUT, amp=0, step=2)
        s.line((13, 20.8), (14.5, 23.6), lw * 0.5, OUT, amp=0, step=2)
        s.line((16.5, 20.8), (18, 23.6), lw * 0.5, OUT, amp=0, step=2)
    else:
        s.fill(rrect(11, 12, 4, 1.4, 0.6), CREAM, amp=0, opacity=0.8)
        s.fill(rrect(11, 14.6, 6, 1.2, 0.6), CREAM, amp=0, opacity=0.6)
        # 二维码贴纸
        s.shape(rect(10, 21, 6, 6), CREAM, lw * 0.5, amp=0)
        for (qx, qy) in ((10.8, 21.8), (13.6, 21.8), (10.8, 24.6), (13, 24), (14.4, 25)):
            s.fill(rect(qx, qy, 1.4, 1.4), OUT, amp=0)
    # 插头挂钩 + 线
    cable = ORANGE if state != 'broken' else '#7C6A5E'
    if state in ('idle', 'broken'):
        s.add(f'<path d="M24.5 16 q5 5 1.5 12 q-2 3 -4 1" fill="none" stroke="{OUT}" stroke-width="{lw * 2.2}" stroke-linecap="round"/>')
        s.add(f'<path d="M24.5 16 q5 5 1.5 12 q-2 3 -4 1" fill="none" stroke="{cable}" stroke-width="{lw * 1.1}" stroke-linecap="round"/>')
    s.shape(rrect(22.5, 13, 4, 5, 1), '#56605E', lw * 0.6, amp=0)


def pile(s, x, y, state='idle', sc=1.0, night=False):
    G(s, x, y, sc); G(s, -16, -20); pile_local(s, state, night=night); E(s); E(s)


# ---------------- UI（有厚度的实体小物件） ----------------
def slab(s, x, y, w, h, face=CREAM, side=OUT, depth=5, r=8, lw=2.6, amp=0.7):
    """带厚度、描边的块"""
    s.shape(rrect(x + depth * 0.4, y + depth, w, h, r), side, lw, amp=amp * 0.7, step=8)
    return s.shape(rrect(x, y, w, h, r), face, lw, amp=amp, step=8)


def keycap(s, x, y, key, w=None, size=18):
    w = w or max(30, tw(key, size) + 16)
    slab(s, x, y, w, 28, MUSTARD, '#8A6A1E', depth=4, r=5, lw=2.0, amp=0.4)
    s.fill(rrect(x + 4, y + 3, w - 8, 5, 2), shade_color(MUSTARD, 1.25), amp=0.2)
    s.text(x + w / 2, y + 21, key, size, OUT, anchor='middle', family='Noto Sans Mono CJK SC')
    return w


def hint_bar(s, items, cy=512, W=960):
    """底部操作提示：items = [(键, 文字), ...]"""
    gap = 26
    widths = []
    for k, t in items:
        kw = max(30, tw(k, 17) + 16)
        widths.append(kw + 8 + tw(t, 17))
    total = sum(widths) + gap * (len(items) - 1) + 36
    x = (W - total) / 2
    slab(s, x, cy - 20, total, 40, '#3F4A4A', '#232B2B', depth=5, r=12, lw=2.4)
    cx = x + 18
    for (k, t), wd in zip(items, widths):
        kw = keycap(s, cx, cy - 16, k, size=17)
        s.text(cx + kw + 8, cy + 6, t, 17, CREAM)
        cx += wd + gap
        if (k, t) != items[-1]:
            s.add(f'<circle cx="{cx - gap / 2:.1f}" cy="{cy:.1f}" r="2.4" fill="{CONC}"/>')


def battery_hud(s, x, y, pct, hp=None, hp_max=3, low=False):
    w = 238 if hp is None else 238
    h = 60 if hp is None else 92
    slab(s, x, y, w, h, CREAM, OUT, depth=6, r=10)
    # 闪电徽章
    s.shape(ellipse(x + 26, y + 30, 16, 16, 16), TEAL, 2.2, amp=0.5)
    s.shape([(x + 28, y + 18), (x + 19, y + 32), (x + 26, y + 32), (x + 23, y + 43), (x + 34, y + 27), (x + 27, y + 27), (x + 30, y + 18)],
            MUSTARD, 1.6, amp=0.2, step=4)
    # 电池
    bx, by, bw, bh = x + 50, y + 16, 118, 28
    s.shape(rrect(bx + bw, by + 8, 7, 12, 2), CONC, 2, amp=0.2)
    s.shape(rrect(bx, by, bw, bh, 5), '#DCE0D2', 2.4, amp=0.5)
    col = '#7FB59A' if pct >= 40 else (ORANGE if pct >= 20 else RUST)
    fw = (bw - 8) * pct / 100
    s.fill(rrect(bx + 4, by + 4, fw, bh - 8, 3), col, amp=0.3, step=5)
    s.fill(rrect(bx + 4, by + 4, fw, 6, 3), shade_color(col, 1.3), amp=0.2, step=5)
    for k in range(1, 5):
        xx = bx + 4 + (bw - 8) * k / 5
        s.line((xx, by + 5), (xx, by + bh - 5), 1.2, OUT, amp=0.2, step=4, opacity=0.35)
    s.xtext(x + 182, y + 42, f'{pct}%', 26, OUT if not low else RUST, side=CONC, depth=2)
    if hp is not None:
        s.text(x + 18, y + 78, '血量', 15, OUT)
        for k in range(hp_max):
            hx = x + 64 + k * 34
            filled = k < hp
            heart(s, hx, y + 72, filled)
        s.text(x + 172, y + 79, f'{hp}/{hp_max}', 14, '#5C6359', weight='normal')
    return w, h


def heart(s, cx, cy, filled=True, r=11):
    pts = []
    for k in range(40):
        t = 2 * math.pi * k / 40
        px = 16 * math.sin(t) ** 3
        py = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + px * r / 16, cy + py * r / 16))
    s.shape([(x + 1, y + 2.5) for x, y in pts], OUT, 0, amp=0)
    s.shape(pts, RUST if filled else '#DCE0D2', 2, amp=0.3, step=3)
    if filled:
        s.fill(ellipse(cx - r * 0.42, cy - r * 0.3, r * 0.22, r * 0.16, 8), '#E59A83', amp=0)


def clock_hud(s, time_str, signal=None, curfew=None, W=960, night=False):
    w = 150
    x = W - w - 14
    y = 12
    slab(s, x, y, w, 58, CREAM, OUT, depth=6, r=10)
    s.fill(rrect(x + 8, y + 6, w - 16, 6, 3), '#FFFFF4', amp=0.2, opacity=0.8)
    # 小钟表图标
    s.shape(ellipse(x + 24, y + 30, 11, 11, 14), '#DCE0D2', 2, amp=0.3)
    s.line((x + 24, y + 30), (x + 24, y + 23), 2, OUT, amp=0)
    s.line((x + 24, y + 30), (x + 29, y + 32), 2, OUT, amp=0)
    s.xtext(x + 44, y + 42, time_str, 30, OUT, side=CONC, depth=2, family='Noto Sans Mono CJK SC')
    if signal is not None:
        sx = x - 72
        slab(s, sx, y + 6, 60, 46, CREAM, OUT, depth=5, r=8)
        for k in range(4):
            hh = 8 + k * 7
            c = MUSTARD if k < signal else '#DCE0D2'
            s.shape(rrect(sx + 9 + k * 11, y + 44 - hh, 8, hh, 1.5), c, 1.6, amp=0.2, step=3)
        s.otext(sx + 30, y + 72, '滴滴…', 13, CREAM, OUT, 3, anchor='middle')
    if curfew:
        cx = x + 18
        slab(s, cx, y + 70, w - 18, 30, RUST, '#6E2A1E', depth=4, r=7, lw=2.2)
        s.text(cx + (w - 18) / 2, y + 91, curfew, 16, CREAM, anchor='middle')


def bubble(s, x, y, text, tx, ty, size=17, w=None):
    """独白气泡：中心 x，底边 y，尾巴指向 (tx,ty)"""
    w = w or tw(text, size) + 34
    h = size + 24
    bx = x - w / 2
    by = y - h
    # 阴影
    s.fill([(p[0] + 3, p[1] + 4) for p in rrect(bx, by, w, h, 14)], SHADOW, amp=0, opacity=0.25)
    body = rrect(bx, by, w, h, 14)
    tail = [(tx - 4 if tx < x else tx + 4, y - 1), (tx, ty), (tx + (10 if tx < x else -10), y - 1)]
    # 尾巴描边先画
    s.shape(tail, CREAM, 2.4, amp=0.3, step=4)
    s.shape(body, CREAM, 2.6, amp=0.8, step=7)
    s.fill([(tail[0][0] + 1, y - 4), (tail[2][0] - (1 if tx < x else -1), y - 4), (tail[2][0], y + 1), (tail[0][0], y + 1)], CREAM, amp=0)
    s.text(x, by + h / 2 + size * 0.36, text, size, OUT, anchor='middle')


def dialog(s, question, options, sel=0, W=960, H=540, cy=None):
    cy = cy or H / 2 - 10
    w, h = 560, 190
    x, y = (W - w) / 2, cy - h / 2
    slab(s, x, y, w, h, CREAM, OUT, depth=9, r=16, lw=3)
    s.fill(rrect(x + 12, y + 10, w - 24, 8, 4), '#FFFFF4', amp=0.2, opacity=0.9)
    # 顶部小标签
    slab(s, x + 26, y - 18, 108, 32, TEAL, '#2E6A68', depth=4, r=8, lw=2.2)
    s.text(x + 80, y + 4, '充电桩 07', 15, CREAM, anchor='middle')
    s.text(W / 2, y + 66, question, 22, OUT, anchor='middle')
    ow, gap = 200, 40
    ox = W / 2 - ow - gap / 2
    for i, o in enumerate(options):
        xx = ox + i * (ow + gap)
        if i == sel:
            slab(s, xx, y + 102, ow, 54, MUSTARD, '#8A6A1E', depth=6, r=10, lw=2.6)
            s.fill(rrect(xx + 8, y + 107, ow - 16, 8, 4), shade_color(MUSTARD, 1.3), amp=0.2)
            s.xtext(xx + ow / 2, y + 138, o, 22, CREAM, side=OUT, depth=0, anchor='middle', stroke=OUT, sw=4)
            # 选择箭头
            s.shape([(xx - 22, y + 118), (xx - 8, y + 129), (xx - 22, y + 140)], ORANGE, 2.2, amp=0.2, step=4)
        else:
            slab(s, xx, y + 106, ow, 50, '#DCE0D2', '#6D7572', depth=3, r=10, lw=2.2)
            s.text(xx + ow / 2, y + 139, o, 21, '#5C6359', anchor='middle')
