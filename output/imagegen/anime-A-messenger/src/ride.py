# 02-ride：校内大坡骑行 · 07:52
import sys
sys.path.insert(0, '.')
from scene_common import *

W, H = 960, 540
seed(33)
s = SVG(W, H)
RL, RR = 330, 630          # 路面左右边界（3 车道，每道 100）
LANES = [380, 480, 580]

# ---- 两侧草地 + 人行道 ----
s.fill(rect(0, 0, W, H), VEG_L, amp=0)
for _ in range(80):
    cx, cy = R.uniform(0, W), R.uniform(0, H)
    s.fill(jag(cx, cy, R.uniform(8, 20), sy=0.6), '#6C9585', amp=0, opacity=0.8)
brush_strokes(s, 0, 0, W, H, 500, VEG_D, 2, 5, 1, 1.8, ang=-1.57, opacity=0.5)
brush_strokes(s, 0, 0, W, H, 200, VEG_LL, 2, 4, 1, 1.6, ang=-1.57, opacity=0.6)
# 坡地等高线（手绘，表达地势起伏）
for k in range(6):
    y0 = 60 + k * 40
    for side in ((0, RL - 70), (RR + 70, W)):
        pts = [(side[0] + (side[1] - side[0]) * j / 8, y0 + 18 * math.sin(j * 0.9 + k) + (j * 3 if side[0] == 0 else -j * 3)) for j in range(9)]
        s.ink(pts, False, 1.2, 0.5, VEG_D, amp=1.0, step=10, opacity=0.5)
# 右侧：石阶 + 宿舍楼顶（太阳能热水器、水箱）
s.shape(rect(760, 380, 210, 170), CONC2, 2.6, amp=0.5, step=10)
s.fill(rect(760, 380, 210, 16), shade_color(CONC2, 1.15), amp=0.3)
for xx in (784, 850):
    s.shape(rect(xx, 420, 50, 30), '#7FA9B5', 1.8, amp=0.3)
    for k in range(5):
        s.line((xx + 5 + k * 10, 420), (xx + 5 + k * 10, 450), 0.8, OUT, amp=0, opacity=0.6)
    s.shape(rrect(xx - 2, 410, 54, 10, 4), CREAM2, 1.6, amp=0.2)
s.shape(ellipse(930, 440, 18, 18, 14), RUST, 2.2, amp=0.3)
s.fill(ellipse(936, 446, 10, 10, 12), shade_color(RUST, 0.75), amp=0)
laundry(s, 780, 950, 478)
s.fill(rect(760, 380, 14, 170), SHADOW, amp=0, opacity=0.25)
for k in range(6):  # 石阶
    s.shape(rect(700, 20 + k * 16, 56, 14), '#C9CBB8', 1.6, amp=0.3)
# 左侧：路牌 + 长椅
s.shape(rect(118, 480, 5, 50), '#6A6F68', 1.6, amp=0.2)
slab(s, 74, 462, 94, 30, '#3F6F6C', '#23403E', depth=3, r=4, lw=2)
s.text(121, 483, '↑ 新校区', 14, CREAM, anchor='middle')
s.shape(rect(30, 420, 70, 16), '#9C7A5C', 2, amp=0.3)
for xx in (38, 54, 70, 86):
    s.line((xx, 421), (xx, 435), 0.8, OUT, amp=0, opacity=0.5)
# 桂花丛
for (bx, by) in ((170, 110), (200, 150), (720, 300), (770, 330)):
    tree(s, bx, by, 26, dark='#5B6B58', mid='#6F8F6A', light='#8FAF84', shadow=True, w=1.6)
    for _ in range(10):
        s.add(f'<circle cx="{bx + R.uniform(-17, 17):.1f}" cy="{by + R.uniform(-17, 17):.1f}" r="1.7" fill="{MUSTARD}"/>')
# 人行道（米黄地砖）
for x0 in (RL - 56, RR):
    s.shape(rect(x0, -10, 56, H + 20), '#C9CBB8', 2.2, amp=0.6, step=10)
    for yy in range(-10, H + 10, 28):
        s.add(f'<line x1="{x0}" y1="{yy}" x2="{x0 + 56}" y2="{yy}" stroke="#AEB1A0" stroke-width="1"/>')
    s.add(f'<line x1="{x0 + 28}" y1="-10" x2="{x0 + 28}" y2="{H + 10}" stroke="#AEB1A0" stroke-width="1"/>')
# 路缘石
for x0 in (RL - 6, RR):
    s.shape(rect(x0, -10, 6, H + 20), CONC, 1.6, amp=0.3, step=10)

# ---- 路面：下半平路，上半坡道（暖一点的色块）----
s.fill(rect(RL, 0, RR - RL, H), '#8E948C', amp=0)
slope_top, slope_bot = 40, 300
s.fill(rect(RL, slope_top, RR - RL, slope_bot - slope_top), '#A39B88', amp=0.5, step=10)
# 坡道起止的硬边阴影带（2 阶光影表达坡面）
s.fill(rect(RL, slope_bot - 14, RR - RL, 14), SHADOW, amp=0.4, opacity=0.18)
s.fill(rect(RL, slope_top, RR - RL, 10), CREAM2, amp=0.4, opacity=0.35)
brush_strokes(s, RL, 0, RR - RL, H, 260, '#7E857E', 5, 12, 1.2, 2.6, ang=-1.57, opacity=0.45)
brush_strokes(s, RL, 0, RR - RL, H, 120, '#A9AFA4', 4, 10, 1, 2, ang=-1.57, opacity=0.5)
# 车道虚线
for lx in (430, 530):
    for yy in range(-20, H, 60):
        s.fill([(lx - 2, yy), (lx + 2, yy + 1), (lx + 2, yy + 34), (lx - 2, yy + 33)], CREAM2, amp=0.2)
# 坡道箭头 + 「上坡」地面字
for lx in LANES:
    for k in range(2):
        yy = 120 + k * 26
        s.add(f'<path d="M{lx - 18} {yy + 10} L{lx} {yy} L{lx + 18} {yy + 10}" fill="none" stroke="{RUST}" stroke-width="4" stroke-linecap="round" stroke-opacity="0.8"/>')
s.text(480, 248, '上 坡', 30, CREAM2, anchor='middle', extra='fill-opacity="0.85" letter-spacing="8"')
s.text(480, 278, '8%', 16, CREAM2, anchor='middle', extra='fill-opacity="0.8"')
# 井盖
s.shape(ellipse(420, 400, 13, 13, 16), '#6F7670', 1.6, amp=0.3)
for k in (-5, 0, 5):
    s.line((412, 400 + k), (428, 400 + k), 0.8, OUT, amp=0, opacity=0.5)

# ---- 樟树行道树（遮一点路面，投影冷色）----
for yy in (-10, 130, 270, 410, 540):
    tree(s, RL - 60 + R.uniform(-8, 8), yy + R.uniform(-10, 10), R.uniform(58, 70))
for yy in (60, 200, 340, 480):
    tree(s, RR + 60 + R.uniform(-8, 8), yy + R.uniform(-10, 10), R.uniform(58, 70))
leaves(s, RL - 56, 0, RR - RL + 112, H, 70)

# ---- 远景：左侧教学楼屋顶一角、右侧坡上的路灯 ----
s.shape(rect(0, 200, 150, 190), CONC2, 2.6, amp=0.5, step=10)
s.fill(rect(0, 200, 150, 22), shade_color(CONC2, 1.15), amp=0.3)
for xx in (14, 60, 106):
    s.shape(rrect(xx, 250, 30, 22, 3), CONC, 1.6, amp=0.3)
ac_unit(s, 30, 320, 26, 18)
ac_unit(s, 80, 330, 26, 18)
s.shape(rect(20, 360, 60, 10), RUST, 1.6, amp=0.3)   # 锈红管道
s.line((80, 365), (150, 365), 5, OUT, amp=0.2)
s.line((80, 365), (150, 365), 3, RUST, amp=0.2)
s.fill(rect(135, 200, 15, 190), SHADOW, amp=0, opacity=0.25)
s.text(75, 240, '民主楼', 14, OUT, anchor='middle')

# ---- 障碍 ----
# 校车：前方中右道，慢
bus(s, 580, 70, 1.05)
# 逆行车：左道迎面（车头朝下）
rider(s, 380, 176, 1.5, 180, bike_body=CREAM, seat='#5C6359', shirt='#B7775F', helmet=None, bag=None)
for k in range(4):
    s.line((362 + k * 12, 120 - (k % 2) * 6), (362 + k * 12, 96 - (k % 2) * 6), 2.2, CREAM, amp=0.2, opacity=0.85)
# 行人横穿：从右人行道走进来
walker(s, 560, 250, 1.5, -90, shirt='#D9A28A', bag=MUSTARD)
walker(s, 612, 236, 1.5, -90, shirt='#7FA9B5', bag=CREAM2)
# 行人运动线
for k in range(3):
    s.line((632 + k * 10, 226 + k * 9), (644 + k * 10, 226 + k * 9), 2, CREAM, amp=0, opacity=0.9)

# 外卖车：后方冲上（左道，只露一半 + 速度线）
rider(s, 380, 470, 1.5, 0, bike_body='#DCE0D2', seat='#5C6359', shirt=ORANGE, helmet=ORANGE, delivery=True)
for k in range(5):
    x = 352 + k * 14
    s.line((x, 520 + (k % 2) * 6), (x, 540), 2.4, CREAM, amp=0.2, opacity=0.9)

# 主角：中道
rider(s, 480, 402, 1.5, 0)
# 主角身后的电量"哭"小汗滴
for (dx, dy) in ((26, -44), (-28, -38)):
    s.shape([(480 + dx, 402 + dy - 6), (480 + dx + 4, 402 + dy + 2), (480 + dx, 402 + dy + 5), (480 + dx - 4, 402 + dy + 2)], '#8FD3CD', 1.2, amp=0)

# 底部「！」警告（外卖车来袭）
slab(s, 344, 356, 46, 46, ORANGE, '#7A3A1E', depth=5, r=10, lw=2.6)
s.shape([(360, 410), (374, 410), (367, 420)], ORANGE, 1.8, amp=0)
s.xtext(367, 394, '！', 34, CREAM, side=OUT, depth=0, anchor='middle', stroke=OUT, sw=4)

# ---- 背景颗粒 ----
speckles(s, 0, 0, W, H, 260, ['#4E6E60', CREAM, '#5B6B58'], 0.5, 1.4, 0.35)

# ---- UI ----
battery_hud(s, 14, 12, 41, hp=2)
clock_hud(s, '07:52')
# 路线小牌
slab(s, 810, 88, 136, 32, TEAL, '#2E6A68', depth=4, r=8, lw=2.2)
s.text(878, 110, '校内 · 大坡', 15, CREAM, anchor='middle')
bubble(s, 590, 346, '又是这个大坡……电量在哭。', 500, 366, size=17)
hint_bar(s, [('W', '前进'), ('S', '刹车'), ('A/D', '换道')])

s.save_png('../02-ride.png')
print('ok')
