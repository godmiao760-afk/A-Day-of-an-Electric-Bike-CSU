# 01-findcar 找车 · 早上 07:38 · 淡紫晨雾 + 岳麓山剪影
import os, sys
from lib import P, SVG, render, rrect_pts
import sprites as S

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def mountains(s, y0, color, amp, seed_off=0, peaks=None, op=1, lw=0):
    pts = [(0, 540)]
    import math
    peaks = peaks or []
    for x in range(0, 961, 12):
        h = 0
        for (px, ph, pw) in peaks:
            h = max(h, ph * math.exp(-((x - px) / pw) ** 2))
        h += amp * (0.5 + 0.5 * math.sin(x * 0.03 + seed_off)) + s.r.uniform(-1.5, 1.5)
        pts.append((x, y0 - h))
    pts.append((960, 540))
    if lw:
        s.shape(pts, color, lw, 0.6, seg=14, op=op)
    else:
        s.fillj(pts, color, 0.6, 14, op=op)


def dorm(s, x0, y0, cols, floors, fw=44, fh=19, wall=None, name=None, lit=()):
    """3/4 俯视宿舍楼立面：白瓷砖 + 阳台 + 晾衣 + 空调外机"""
    wall = wall or P['cream']
    W = cols * fw
    H = floors * fh
    # 屋顶顶面（俯视能看到一条）
    s.shape([(x0 - 4, y0 - 12), (x0 + W + 4, y0 - 12), (x0 + W + 4, y0), (x0 - 4, y0)], P['lavL'], 2, 0.6)
    s.box(x0 + 30, y0 - 22, 34, 12, P['creamD'], 1.6, 0.5)  # 楼梯间小屋
    s.box(x0 + W - 90, y0 - 19, 18, 9, P['creamD'], 1.4, 0.4)  # 水箱
    # 立面
    s.shape([(x0, y0), (x0 + W, y0), (x0 + W, y0 + H), (x0, y0 + H)], wall, 2.4, 0.7)
    # 瓷砖横缝
    for f in range(floors + 1):
        s.line([(x0 + 2, y0 + f * fh), (x0 + W - 2, y0 + f * fh)], P['creamD'], 1.0, 0.4)
    clothes = [P['pink'], P['lamp'], P['lavL'], '#7A8FA0', P['cream'], P['rust'], P['gL']]
    for f in range(floors):
        for c in range(cols):
            wx = x0 + c * fw
            wy = y0 + f * fh
            if f == floors - 1 and c in (cols // 2 - 1, cols // 2):
                continue  # 底层入口
            # 窗（上半）+ 阳台栏杆（下半）
            lit_on = (f, c) in lit
            s.box(wx + 6, wy + 3, fw - 12, 9, P['goldL'] if lit_on else '#6E6488', 1.1, 0.3)
            if not lit_on:
                s.box(wx + 6, wy + 3, (fw - 12) * 0.45, 9, P['lavL'], 0, 0.2, op=0.5)
            s.box(wx + 3, wy + 11, fw - 6, 7, P['creamD'], 1.3, 0.3)
            for k in range(4):
                s.line([(wx + 8 + k * 9, wy + 12), (wx + 8 + k * 9, wy + 17)], P['ink2'], 0.7, 0.1, op=0.7)
            # 晾衣
            if s.r.random() < 0.55:
                for k in range(s.r.randint(1, 3)):
                    cx = wx + 8 + k * 9 + s.r.uniform(-1, 1)
                    s.box(cx, wy + 5, 6, s.r.uniform(6, 10), s.r.choice(clothes), 0.9, 0.2)
            # 空调外机
            if s.r.random() < 0.45:
                ax = wx + (fw - 13 if s.r.random() < 0.5 else 1)
                s.box(ax, wy + 12, 12, 7, P['cream'], 1.1, 0.2)
                s.ell_fill(ax + 4, wy + 15.5, 2.2, 2.2, P['creamD'])
    # 入口 + 匾
    ex = x0 + (cols // 2 - 1) * fw
    ey = y0 + (floors - 1) * fh
    s.box(ex + 6, ey + 2, fw * 2 - 12, fh - 2, '#5A4E6E', 1.8, 0.4)
    s.box(ex + 14, ey + 6, fw * 2 - 28, fh - 6, P['goldL'], 0, 0.2, op=0.35)
    if name:
        s.rbox(ex + 10, ey - 13, fw * 2 - 20, 13, 2, P['lav'], 1.4, 0.3)
        s.text(ex + fw, ey - 2.5, name, 9.5, P['cream'], anchor='middle')
    # 立面右侧暗阶（硬光影）
    s.fillj([(x0 + W - 10, y0), (x0 + W, y0), (x0 + W, y0 + H), (x0 + W - 10, y0 + H)], P['lav'], 0.3, 10, op=0.35)


def canopy(s, x0, x1, y, depth=26):
    """车棚雨棚边：波纹板 + 立柱，半透明看见下面的车"""
    s.shape([(x0, y - depth), (x1, y - depth), (x1, y), (x0, y)], P['lav'], 2.2, 0.6, op=0.92)
    for x in range(int(x0) + 6, int(x1), 14):
        s.line([(x, y - depth + 3), (x, y - 3)], P['lavL'], 2.2, 0.3, op=0.8)
    s.fillj([(x0, y - 6), (x1, y - 6), (x1, y), (x0, y)], P['ink'], 0.3, 20, op=0.25)
    for x in range(int(x0) + 20, int(x1), 150):
        s.box(x, y - 2, 6, 10, P['ink2'], 1.2, 0.2)


def draw(path_png, seed=11, iter_tag=''):
    s = SVG(960, 540, seed=seed, bg=P['mist'])
    # ---- 天空与岳麓山 ----
    for i, c in enumerate(['#E9DDEA', '#E3D6E6', '#DCCDE2']):
        s.rect(0, i * 18, 960, 18, c)
    s.ell_fill(640, 48, 30, 30, '#F6E3DA', 0.9)  # 晨日（薄）
    s.ell_fill(640, 48, 46, 46, '#F6E3DA', 0.35)
    mountains(s, 150, '#C3B7D5', 8, 0.5, peaks=[(250, 70, 120), (720, 118, 150), (880, 84, 90)], lw=1.8)
    s.strokes(600, 40, 360, 100, 40, '#AFA2C6', 12, 2.2, 30, 0.6)
    mountains(s, 160, '#A99CC2', 5, 2.0, peaks=[(640, 58, 90), (800, 44, 120)], lw=1.2)
    s.text(690, 112, '岳 麓 山', 13, P['cream'], stroke=P['lav'], sw=3)
    # 雾带
    s.fillj([(560, 104), (960, 96), (960, 132), (560, 138)], P['mist'], 3, 40, op=0.7, smooth=True)
    s.fillj([(560, 140), (960, 134), (960, 160), (560, 166)], P['mist'], 3, 40, op=0.6, smooth=True)
    # ---- 宿舍楼 ----
    dorm(s, 70, 62, 11, 6, name='升华公寓·7栋', lit=[(1, 3), (3, 8), (4, 6)])
    # 远处樟树林一线
    for tx in range(560, 980, 38):
        s.tree(tx, 168 + s.r.uniform(-4, 4), 24, pal=('#8F86A6', '#A198B6', '#B3A9C4', '#C2B9D0'), lw=1.4)
    # 右侧远处的楼（雾里更淡）
    s.fillj([(0, 150), (960, 145), (960, 176), (0, 176)], P['mist'], 2, 40, op=0.35)
    # ---- 地面 ----
    s.rect(0, 176, 960, 364, '#CFC5D6')
    s.fillj([(0, 176), (960, 176), (960, 184), (0, 184)], '#B8ADC6', 0.4, 20)
    s.strokes(0, 186, 960, 354, 90, '#BDB2C9', 14, 2.5, 5, 0.6)
    s.specks(0, 186, 960, 354, 160, '#A89DB9', 0.5, 1.4, 0.6)
    # 湿地面水洼（映出天空）
    s.fillj(s.blob_pts(835, 470, 34, 16, 0.05, 0.2, sy=0.35), '#E6DCEB', 1, 20, op=0.8, smooth=True)
    s.fillj(s.blob_pts(828, 468, 18, 12, 0.05, 0.2, sy=0.3), P['cream'], 1, 20, op=0.6, smooth=True)
    # ---- 左右樟树 / 桂花（在地面层下方边缘）----
    # 车位白线
    rows = [214, 316, 418]
    BW, BH, SC = 24, 48, 1.25
    step = 33
    xs = list(range(96, 830, step))
    for ry in rows:
        s.line([(84, ry - 10), (840, ry - 10)], P['creamD'], 1.6, 0.6, op=0.9)
        for x in xs[::1]:
            s.line([(x - 4, ry - 10), (x - 4, ry + 62)], P['creamD'], 1.0, 0.3, op=0.55)
    # 雨棚立柱阴影
    own_row, own_i = 1, 12
    my_x = xs[own_i]
    variant_seq = [0, 1, 2, 3, 4, 1, 0, 2]
    for ri, ry in enumerate(rows):
        for i, x in enumerate(xs):
            # 走道右侧留一个空位 & 一辆歪停
            if ri == 0 and i in (5,):
                continue
            if ri == 2 and i in (19, 20):
                continue
            rot = s.r.uniform(-7, 7)
            jx = s.r.uniform(-2, 2)
            if ri == own_row and i == own_i:
                # 自己的车：刚被认出，变黄 + 光圈
                s.ell_fill(x + BW * SC / 2, ry + BH * SC / 2, 24, 40, P['lamp'], 0.28)
                s.fillj(rrect_pts(x - 5, ry - 7, BW * SC + 10, BH * SC + 12, 10), 'none', 0, 10)
                s.shape(rrect_pts(x - 6, ry - 8, BW * SC + 12, BH * SC + 14, 11), 'none', 2.4, 1.0, ink=P['lamp'])
                S.bike(s, x, ry, SC, rot=0, shadow=(2, 3))
                continue
            # 邻车贴得很近（左右夹住）
            if ri == own_row and i == own_i - 1:
                jx, rot = 5, 6
            if ri == own_row and i == own_i + 1:
                jx, rot = -5, -5
            S.other_bike(s, x + jx, ry, SC, variant=s.r.choice(variant_seq), rot=rot, shadow=(2, 3))
    # 一辆被推歪到走道里的车
    S.other_bike(s, 700, 372, SC, variant=3, rot=62, shadow=(2, 3))
    # ---- 雨棚（上排车前沿）----
    canopy(s, 80, 846, 206, 22)
    # ---- 左右两侧樟树 & 桂花 ----
    s.tree(30, 250, 58, shadow=(18, 10), sh_op=0.3)
    s.tree(20, 430, 64, shadow=(18, 10), sh_op=0.3)
    s.tree(935, 300, 60, osman=True, pal=('#3E5A45', '#5A7852', '#7F9A68', '#A8B584'), shadow=(-14, 10))
    s.tree(945, 470, 52, shadow=(-14, 10))
    # 飘落桂花
    for _ in range(60):
        s.add(f'<circle cx="{s.r.uniform(830, 960):.1f}" cy="{s.r.uniform(230, 530):.1f}" r="{s.r.uniform(0.8, 1.6):.1f}" fill="{P["gold"]}" opacity="0.9"/>')
    for _ in range(25):
        s.add(f'<circle cx="{s.r.uniform(80, 830):.1f}" cy="{s.r.uniform(190, 490):.1f}" r="{s.r.uniform(0.7, 1.3):.1f}" fill="{P["gold"]}" opacity="0.75"/>')
    # ---- 主角（走道里，靠近自己的车）----
    px, py = my_x + 16, 272
    S.player(s, px - 3, py - 4, 1.45)
    # "滴滴"
    bx = my_x + BW * SC / 2
    for (dx, dy) in [(-42, 392), (30, 400)]:
        s.text(bx + dx, dy, '滴', 15, P['lampD'], stroke=P['cream'], sw=4, anchor='middle')
    for r_ in (8, 14, 20):
        s.add(f'<path d="M{bx - r_},{392} a{r_},{r_} 0 0 0 {2 * r_},0" fill="none" stroke="{P["lampD"]}" stroke-width="2.2" stroke-linecap="round" opacity="{1 - r_ / 30:.2f}"/>')
    # F 提示小键帽（在车右上）
    s.keycap(bx + 26, 318, 'F', 26)
    # 还没熄的路灯（暖黄点缀）
    for lx, ly in [(868, 236), (70, 330)]:
        s.ell_fill(lx + 3, ly + 70, 10, 4, P['shadow'], 0.35)
        s.ell_fill(lx, ly, 26, 26, P['lamp'], 0.18)
        s.box(lx - 2, ly, 4, 70, P['ink2'], 1.2, 0.3)
        s.ellipse(lx, ly, 8, 8, P['lamp'], 1.8, 0.3, n=12)
        s.ell_fill(lx - 2, ly - 2, 3, 3, P['goldL'])
    # 告示牌：请有序停放
    s.slab(846, 430, 84, 40, P['cream'], P['lavL'], depth=4, r=4, lw=1.8)
    s.text(888, 446, '请有序停放', 11, P['ink'], anchor='middle')
    s.text(888, 462, '违者锁车', 10, P['red'], anchor='middle')
    s.box(872, 474, 4, 18, P['ink2'], 1, 0.2)
    s.box(900, 474, 4, 18, P['ink2'], 1, 0.2)
    # 垃圾桶
    s.rbox(46, 208, 22, 26, 4, P['gL'], 1.8, 0.4)
    s.box(44, 204, 26, 6, P['gM'], 1.6, 0.3)
    # ---- 晨雾（前景低矮雾团）----
    for (cx, cy, rx) in [(160, 300, 180), (560, 470, 220), (420, 200, 200), (880, 380, 120)]:
        s.fillj(s.blob_pts(cx, cy, rx, 18, 0.03, 0.15, sy=0.18), P['mist'], 1, 30, op=0.28, smooth=True)
    s.specks(0, 0, 960, 540, 140, P['cream'], 0.6, 1.4, 0.5)
    # ---- 气泡 ----
    s.bubble(px + 40, 222, '终于找到你了！', tail_x=px + 30, tail_y=py + 8, size=17, w=160)
    # ---- UI ----
    s.battery(18, 16, 62)
    s.clock(810, 14, '07:38', signal=4)
    s.hint([('F', '查看'), ('E', '背包')], y=496)
    svg = os.path.join(OUT, 'src', 'tmp', f'01{iter_tag}.svg')
    s.save(svg)
    render(svg, path_png)
    return path_png


if __name__ == '__main__':
    tag = sys.argv[1] if len(sys.argv) > 1 else ''
    print(draw(os.path.join(OUT, f'01-findcar{tag}.png'), iter_tag=tag))
