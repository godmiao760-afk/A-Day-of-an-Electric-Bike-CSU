# 01-findcar：宿舍楼下车棚找车 · 07:38
import sys
sys.path.insert(0, '.')
from scene_common import *

W, H = 960, 540
seed(21)
s = SVG(W, H)

# ---- 天空 + 岳麓山 ----
s.fill(rect(0, 0, W, 190), TEAL, amp=0)
speckles(s, 0, 0, W, 190, 160, ['#4E9E9B', '#8FD3CD', CREAM], 0.6, 1.5, 0.5)
mountain(s, 150, -20, 520, 110)
# 山顶电视塔（小小的锈红点缀）
s.shape(rect(150, 36, 5, 34), CREAM2, 1.4, amp=0.2)
s.shape(rect(146, 30, 13, 8), RUST, 1.4, amp=0.2)
cloud(s, 60, 28, 80)
cloud(s, 225, 70, 50)

# ---- 宿舍楼立面 ----
dorm_facade(s, 250, 772, -60, 184, 4, wall=CREAM)
# 楼顶以上出画：暗示 6~7 层高楼
# 楼号牌
slab(s, 450, 124, 120, 26, RUST, '#6E2A1E', depth=3, r=4, lw=2)
s.text(510, 143, '升华公寓 7 舍', 15, CREAM, anchor='middle')
# 右侧另一栋红砖楼（侧面）
s.shape(rect(760, 44, 220, 140), '#B7775F', 2.8, amp=0.6, step=10)
for yy in range(50, 184, 8):
    s.add(f'<line x1="760" y1="{yy}" x2="980" y2="{yy}" stroke="#A0644F" stroke-width="0.8"/>')
for fx in (790, 860, 930):
    for fy in (56, 118):
        s.shape(rect(fx, fy, 36, 48), '#557F80', 1.8, amp=0.3)
        s.fill(rect(fx + 2, fy + 2, 10, 44), '#7FAAA8', amp=0, opacity=0.5)
        ac_unit(s, fx + 4, fy + 52)
s.fill(rect(760, 44, 16, 140), SHADOW, amp=0, opacity=0.25)

# ---- 地面 ----
ground(s, 0, 176, W, H - 176, '#A9B5AA', seed_=4)
# 晨露积水：倒映青绿天空
for (qx, qy, qr) in ((180, 322, 30), (640, 440, 38), (820, 318, 22)):
    s.shape(jag(qx, qy, qr, rough=0.2, sy=0.45), MIST, 1.6, amp=0.6)
    s.fill(jag(qx - qr * 0.2, qy - 2, qr * 0.45, rough=0.2, sy=0.3), '#B7E0D8', amp=0.3)
# 楼前冷色阴影带
s.fill(rect(0, 176, W, 26), SHADOW, amp=0.5, opacity=0.2)
# 地面停车线
for yy in (196, 318, 428):
    s.line((20, yy), (940, yy), 1.6, CREAM2, amp=0.5, step=12, opacity=0.8)
leaves(s, 0, 180, W, 360, 90)

# ---- 电线杆 + 电线 ----
tops = pole(s, 905, 250, 200)
# 左侧远处电线杆
s.shape(rect(120, 40, 5, 146), CONC, 1.8, amp=0.3)
s.shape(rect(106, 48, 32, 4), '#6A6F68', 1.4, amp=0.2)
s.sag((-10, 70), (110, 50), 10, 1.2)
s.sag((136, 50), tops[0], 34, 1.3)
s.sag((125, 60), tops[2], 40, 1.1)
s.sag(tops[1], (980, 40), 6, 1.3)

# ---- 车阵 ----
SC = 1.3
PITCH = 33
own_col, own_row = 14, 1
rows_y = [252, 372, 482]
others_body = [CREAM, CREAM, '#E4EAE0', '#D8E4E2', '#EDE7D6', '#CFD9D6', '#E9E8CE']
others_seat = ['#5C6359', '#6E7A74', '#3F4747', '#7C6A5E', '#586C74', '#8A8F86']
Rb = random.Random(8)
for ri, ry in enumerate(rows_y):
    for ci in range(27):
        x = 36 + ci * PITCH + (8 if ri == 1 else 0)
        if ri == 0 and ci in (5,):
            continue  # 一处空位（其实有辆共享单车倒着）
        if ri == 2 and 11 <= ci <= 17:
            continue  # 底排中间被提示栏盖住，不画
        if x > 885 and ri < 2:
            continue
        rot = Rb.uniform(-5, 5)
        y = ry + Rb.uniform(-3, 3)
        if ri == own_row and ci == own_col:
            # 自己的车：被认出后变黄，外发光
            for k, op in ((16, 0.18), (11, 0.28), (7, 0.4)):
                s.fill(rrect(x - 12 * SC - k, y - 24 * SC - k, 24 * SC + 2 * k, 48 * SC + 2 * k, 10 + k), MUSTARD, amp=0.4, opacity=op)
            bike(s, x, y, SC, 0, body=MUSTARD, seat='#C9962E', own=True, basket=True)
            own_xy = (x, y)
            continue
        bike(s, x, y, SC, rot, body=Rb.choice(others_body), seat=Rb.choice(others_seat), basket=Rb.random() < 0.35)
        if Rb.random() < 0.18:  # 座上挂着的头盔
            hc = Rb.choice([CREAM2, RUST, TEAL, '#7FA9B5'])
            s.shape(ellipse(x + 1, y + 6, 7, 7.5, 12), hc, 1.6, amp=0.3, step=3)
            s.fill(ellipse(x + 3, y + 8, 4, 4, 10), shade_color(hc, 0.75), amp=0)
# 雨棚：上排车在雨棚下（冷色投影 + 前檐）
s.fill(rect(0, 186, 890, 112), SHADOW, amp=0.5, opacity=0.2)
for px in (60, 330, 600, 870):
    s.shape(rect(px - 5, 290, 10, 12), '#6A6F68', 1.8, amp=0.2)
s.shape(rect(0, 176, 895, 14), '#6F9C92', 2.4, amp=0.6, step=8)
for xx in range(6, 890, 12):
    s.line((xx, 178), (xx, 189), 1.0, '#4E7A70', amp=0, opacity=0.8)
s.shape(rect(0, 286, 895, 8), '#6F9C92', 2.2, amp=0.5, step=8)

# 被夹住提示：左右邻车的小箭头
ox, oy = own_xy
for dx in (-PITCH, PITCH):
    s.shape([(ox + dx * 0.5 - 4, oy - 44), (ox + dx * 0.5 + 4, oy - 44), (ox + dx * 0.5, oy - 36)], ORANGE, 1.6, amp=0.1)
# 闪光
for (sx, sy, r) in ((ox + 24, oy - 40, 7), (ox - 26, oy - 26, 5), (ox + 22, oy + 12, 4)):
    s.shape([(sx, sy - r), (sx + r * 0.28, sy - r * 0.28), (sx + r, sy), (sx + r * 0.28, sy + r * 0.28), (sx, sy + r), (sx - r * 0.28, sy + r * 0.28), (sx - r, sy), (sx - r * 0.28, sy - r * 0.28)],
            CREAM, 1.4, amp=0)

# ---- 樟树（左下角、右侧）----
tree(s, 30, 440, 70)
tree(s, 930, 400, 62)
# 花坛 + 桂花丛
s.shape(rrect(850, 460, 120, 90, 8), '#8F9A8A', 2.4, amp=0.5)
for (bx, by) in ((880, 490), (930, 500), (905, 530)):
    tree(s, bx, by, 24, dark='#5B6B58', mid='#6F8F6A', light='#8FAF84', shadow=False, w=1.6)
    for _ in range(8):
        s.add(f'<circle cx="{bx + R.uniform(-15, 15):.1f}" cy="{by + R.uniform(-15, 15):.1f}" r="1.6" fill="{MUSTARD}"/>')

# ---- 主角（走道里，面向自己的车）----
px, py = ox - 6, 318
walker(s, px, py, 1.7, rot=180, shirt='#6C9AA0', bag='#5C8A86')
# 地上的小脚印/尘土
for k in range(4):
    s.fill(ellipse(px - 60 - k * 26, py + 6 - (k % 2) * 8, 3, 2, 8), shade_color(CONC2, 0.85), amp=0, opacity=0.8)

# ---- 背景纸点 ----
speckles(s, 0, 176, W, 364, 200, ['#6F7670', CREAM, '#5B6B58'], 0.5, 1.4, 0.35)

# ---- UI ----
battery_hud(s, 14, 12, 62)
clock_hud(s, '07:38', signal=4)
bubble(s, px + 40, py - 32, '终于找到你了！', px + 8, py - 14, size=18)
hint_bar(s, [('F', '查看'), ('E', '背包')])

s.save_png('../01-findcar.png')
print('ok')
