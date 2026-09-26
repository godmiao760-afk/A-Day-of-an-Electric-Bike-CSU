# 02-ride 骑行 · 07:52 · 低角度斜阳长影子，校内大坡
import os, sys, math
from lib import P, SVG, render, rrect_pts
import sprites as S

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RL, RR = 318, 642          # 路面左右
LANES = [372, 480, 588]    # 三条车道中心
SH = (34, 16)              # 斜阳投影方向（从左上照来 → 影子往右下）


def draw(path_png, seed=23, tag=''):
    s = SVG(960, 540, seed=seed, bg=P['gM'])
    # ---- 草地（两侧）----
    s.rect(0, 0, 960, 540, '#5B7657')
    s.strokes(0, 0, RL - 40, 540, 160, P['gD'], 9, 2.4, -60, 0.6)
    s.strokes(RR + 40, 0, 960 - RR - 40, 540, 160, P['gD'], 9, 2.4, -60, 0.6)
    s.strokes(0, 0, 960, 540, 120, P['gL'], 7, 2, -70, 0.6)
    # 暮粉的斜阳暖光：左侧草地更亮
    s.fillj([(0, 0), (200, 0), (120, 540), (0, 540)], P['pinkL'], 2, 40, op=0.18)
    # ---- 人行道 ----
    for x0 in (RL - 40, RR):
        s.box(x0, -10, 40, 560, '#BFB2C4', 2, 0.8)
        for y in range(-10, 560, 22):
            s.line([(x0 + 2, y), (x0 + 38, y)], '#A79BB2', 1, 0.4, op=0.8)
        s.line([(x0 + 20, -10), (x0 + 20, 550)], '#A79BB2', 0.8, 0.4, op=0.5)
    # ---- 路面 ----
    s.box(RL, -10, RR - RL, 560, P['road'], 2.4, 0.8)
    s.specks(RL, 0, RR - RL, 540, 260, P['roadD'], 0.5, 1.6, 0.8)
    s.specks(RL, 0, RR - RL, 540, 120, P['roadL'], 0.5, 1.2, 0.8)
    s.strokes(RL, 0, RR - RL, 540, 60, P['roadD'], 16, 2, 88, 0.6)
    # ---- 坡道段（y 0~250）：暖灰紫色块 + 纹理 + 上坡箭头 ----
    slope_y0, slope_y1 = -10, 250
    s.fillj([(RL + 2, slope_y0), (RR - 2, slope_y0), (RR - 2, slope_y1), (RL + 2, slope_y1 + 16)], '#8A7390', 1.2, 20)
    s.fillj([(RL + 2, slope_y1 - 10), (RR - 2, slope_y1 - 16), (RR - 2, slope_y1), (RL + 2, slope_y1 + 16)], '#9C8499', 1, 20)
    for y in range(0, 240, 12):  # 防滑横纹
        s.line([(RL + 6, y), (RR - 6, y + 2)], '#7B6583', 1.6, 0.8, op=0.8)
    s.line([(RL + 2, slope_y1 + 16), (RR - 2, slope_y1)], P['ink'], 2.2, 0.8)
    # 路面上的"上坡"字（倒着读也要能看：俯视，字头朝上）
    s.text(480, 214, '上  坡', 34, P['pinkL'], op=0.85, weight='bold', anchor='middle', ls=4)
    for y in (132, 60):
        for lx in LANES:
            s.line([(lx - 14, y + 12), (lx, y), (lx + 14, y + 12)], P['pinkL'], 4, 0.4, op=0.8)
    # 坡顶提示牌（路边）
    s.slab(RR + 50, 150, 70, 58, P['lamp'], P['lampD'], depth=4, r=6, lw=2)
    s.shape([(RR + 60, 196), (RR + 110, 196), (RR + 110, 166)], P['ink'], 1.4, 0.3)
    s.text(RR + 85, 166, '陡坡', 13, P['ink'], anchor='middle')
    s.text(RR + 105, 230, '12%', 11, P['cream'], stroke=P['ink'], sw=3, anchor='middle')
    s.box(RR + 83, 212, 4, 26, P['ink2'], 1.2, 0.2)
    # ---- 车道虚线（坡下）----
    for lx in (426, 534):
        for y in range(340, 540, 56):
            s.rbox(lx - 2, y, 4, 28, 1.5, P['creamD'], 1, 0.3)
    # 路边实线
    s.line([(RL + 8, 262), (RL + 8, 540)], P['creamD'], 2.2, 0.5)
    s.line([(RR - 8, 258), (RR - 8, 540)], P['creamD'], 2.2, 0.5)
    # ---- 樟树长影子（先画影子再画树）----
    trees_l = [(250, 20), (262, 150), (246, 290), (258, 420), (252, 545)]
    trees_r = [(712, 70), (700, 330), (716, 470)]
    for (tx, ty) in trees_l + trees_r:
        for i in range(8):
            t = (i + 1) / 8
            s.fillj(s.blob_pts(tx + SH[0] * 2.4 * t + 20, ty + SH[1] * 2.4 * t, 50, 16, 0.05, 0.12), P['shadow'], 1, 20,
                    op=0.07, smooth=True)
    # ---- 车辆 ----
    SC = 1.45
    # 前方校车（右道，坡上，慢）
    bus_x, bus_y = LANES[2] - 32 * SC * 0.9, 18
    s.fillj([(bus_x + 10, bus_y + 10), (bus_x + 64 * 1.3 + 40, bus_y + 40), (bus_x + 64 * 1.3 + 40, bus_y + 190), (bus_x + 10, bus_y + 180)], P['shadow'], 1, 20, op=0.3)
    S.npc_bus(s, bus_x, bus_y, 1.3)
    # 逆行车（左道，迎面冲下来）
    wx, wy = LANES[0] - 16 * SC, 150
    s.fillj([(wx + 14, wy + 12), (wx + 60, wy + 30), (wx + 60, wy + 100), (wx + 14, wy + 82)], P['shadow'], 1, 20, op=0.3)
    S.npc_wrong(s, wx, wy, SC)
    s.slab(wx - 44, wy + 18, 36, 22, P['red'], P['rustD'], depth=3, r=5, lw=1.6)
    s.text(wx - 26, wy + 34, '逆行', 11, P['cream'], anchor='middle')
    # 行人横穿（坡底，斑马线）
    for k in range(7):
        s.box(RL + 10 + k * 46, 290, 26, 34, P['cream'], 0, 0.6, op=0.75)
    wkx, wky = 500, 293
    s.fillj([(wkx + 6, wky + 18), (wkx + 60, wky + 40), (wkx + 60, wky + 50), (wkx + 6, wky + 30)], P['shadow'], 1, 20, op=0.3)
    S.walker(s, wkx, wky, 1.5, shirt=P['gL'], facing=-90)
    S.walker(s, wkx + 38, wky + 6, 1.5, shirt=P['pinkD'], facing=-90)
    # 主角（中道）
    px, py = LANES[1] - 16 * SC, 366
    s.fillj([(px + 12, py + 12), (px + 72, py + 36), (px + 72, py + 108), (px + 12, py + 82)], P['shadow'], 1, 20, op=0.35)
    S.rider(s, px, py, SC)
    # 后方外卖车冲上来（左道，底部只露一半）
    dx_, dy_ = LANES[0] - 16 * SC, 440
    s.fillj([(dx_ + 12, dy_ + 12), (dx_ + 72, dy_ + 36), (dx_ + 72, dy_ + 108), (dx_ + 12, dy_ + 82)], P['shadow'], 1, 20, op=0.35)
    S.npc_delivery(s, dx_, dy_, SC)
    for k in range(3):
        s.line([(dx_ + 12 + k * 12, dy_ + 90), (dx_ + 12 + k * 12, dy_ + 70)], P['cream'], 2, 0.3, op=0.6)
    # ---- 樟树（投影之后画）----
    for (tx, ty) in trees_l:
        s.tree(tx, ty, 58 + s.r.uniform(-4, 6), lx=-0.7, ly=-0.35)
    for i, (tx, ty) in enumerate(trees_r):
        s.tree(tx, ty, 54 + s.r.uniform(-4, 6), lx=-0.7, ly=-0.35, osman=(i == 1),
               pal=(('#3E5A45', '#5A7852', '#7F9A68', '#A8B584') if i == 1 else None))
    # 左侧远处草地上的长椅/路灯
    for (lx, ly) in [(RL - 58, 230), (RR + 58, 420)]:
        s.ell_fill(lx + 24, ly + 10, 18, 5, P['shadow'], 0.35)
        s.ellipse(lx, ly, 7, 7, P['lamp'], 1.8, 0.3, n=10)
        s.ell_fill(lx - 2, ly - 2, 2.5, 2.5, P['goldL'])
    # 斜阳光斑（暖粉叠加，硬边）
    for (cx, cy, r) in [(430, 400, 70), (560, 250, 40), (380, 60, 50)]:
        s.fillj(s.blob_pts(cx, cy, r, 14, 0.05, 0.25, sy=0.5), P['pinkL'], 1, 20, op=0.16, smooth=True)
    # 飘落的叶子 / 桂花
    for _ in range(50):
        c = s.r.choice([P['gold'], P['goldL'], P['pink']])
        s.add(f'<circle cx="{s.r.uniform(300, 960):.1f}" cy="{s.r.uniform(0, 540):.1f}" r="{s.r.uniform(0.8, 1.7):.1f}" fill="{c}" opacity="0.85"/>')
    # ---- 后方来车警示「！」----
    ex = LANES[0] - 44
    s.slab(ex - 20, 470, 40, 40, P['rust'], P['rustD'], depth=5, r=20, lw=2.4)
    s.text(ex, 500, '！', 26, P['cream'], anchor='middle')
    s.text(ex, 464, '后方来车', 12, P['cream'], stroke=P['rustD'], sw=4, anchor='middle')
    # ---- 气泡 ----
    s.bubble(px + 60, py + 6, '又是这个大坡……电量在哭。', tail_x=px + 38, tail_y=py + 34, size=16, w=236)
    # ---- UI ----
    s.battery(18, 16, 34)
    for i in range(3):
        s.heart(40 + i * 34, 90, 1.0, full=(i < 2))
    s.clock(810, 14, '07:52')
    # 路程进度（右侧竖条）
    s.slab(906, 110, 30, 240, P['cream'], P['lavL'], depth=4, r=12, lw=2)
    s.box(917, 124, 8, 212, P['creamD'], 1.2, 0.3)
    s.box(917, 124 + 212 * 0.45, 8, 212 * 0.55, P['lamp'], 0, 0.2)
    s.box(917, 124 + 212 * 0.2, 8, 212 * 0.25, '#9C8499', 0, 0.2, op=0.9)  # 坡道段
    s.ellipse(921, 124 + 212 * 0.45, 8, 8, P['lamp'], 1.8, 0.3, n=12)
    s.text(921, 104, '教学楼', 11, P['cream'], stroke=P['ink'], sw=3.5, anchor='middle')
    s.text(921, 370, '宿舍', 11, P['cream'], stroke=P['ink'], sw=3.5, anchor='middle')
    s.hint([('W', '前进'), ('S', '刹车'), ('A/D', '换道')], y=496, cx=610)
    svg = os.path.join(OUT, 'src', 'tmp', f'02{tag}.svg')
    s.save(svg)
    render(svg, path_png)
    return path_png


if __name__ == '__main__':
    tag = sys.argv[1] if len(sys.argv) > 1 else ''
    print(draw(os.path.join(OUT, f'02-ride{tag}.png'), tag=tag))
