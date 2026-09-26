# -*- coding: utf-8 -*-
# 01 找车 · 07:38
import random, sys
sys.path.insert(0, '.')
from lib import *

W, H = 960, 540
rnd = random.Random(7)
o = svg_open(W, H) + defs()

# ---------- 天空 + 岳麓山（窄条） ----------
o += f'<rect width="{W}" height="{H}" fill="#EAF2FF"/>'
o += f'<rect width="{W}" height="120" fill="{SKY_L}"/>'
o += mountain(590, 118, 1.25)
o += cloud(520, 40, 0.6)
o += cloud(690, 30, 0.5)

# ---------- 宿舍楼（积木感，3/4 俯视立面） ----------
def dorm(x0, w, floors=4, top=10, label=None, base="#FFFFFF", trim=SKY):
    s = ""
    hgt = 118
    s += f'<rect x="{x0+6}" y="{top+6}" width="{w}" height="{hgt}" rx="10" fill="{INK}" opacity="0.25"/>'
    s += f'<rect x="{x0}" y="{top}" width="{w}" height="{hgt}" rx="10" fill="{base}" stroke="{INK}" stroke-width="3"/>'
    # 屋顶沿
    s += f'<rect x="{x0-6}" y="{top-6}" width="{w+12}" height="16" rx="8" fill="{trim}" stroke="{INK}" stroke-width="3"/>'
    # 窗户 + 阳台 + 晾衣
    cols = int((w - 20) // 46)
    for r in range(int((hgt-30)//34)):
        for c in range(cols):
            wx = x0 + 16 + c * 46
            wy = top + 20 + r * 34
            s += f'<rect x="{wx}" y="{wy}" width="34" height="24" rx="6" fill="#CDEBFF" stroke="{INK}" stroke-width="2"/>'
            s += f'<path d="M{wx+5},{wy+5} L{wx+12},{wy+5}" stroke="{WHITE}" stroke-width="3" stroke-linecap="round"/>'
            # 阳台栏
            s += f'<rect x="{wx-2}" y="{wy+17}" width="38" height="8" rx="3" fill="{PINK_L}" stroke="{INK}" stroke-width="1.8"/>'
            k = rnd.random()
            if k < 0.45:  # 晾衣服
                cc = rnd.choice([PINK, LEMON, SKY, MINT, WHITE])
                s += f'<path d="M{wx+4},{wy+6} L{wx+30},{wy+6}" stroke="{INK}" stroke-width="1"/>'
                s += f'<path d="M{wx+8},{wy+6} l-3,4 l3,0 v7 h8 v-7 l3,0 l-3,-4 Z" fill="{cc}" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>'
                if rnd.random() < 0.6:
                    s += f'<rect x="{wx+22}" y="{wy+6}" width="6" height="9" rx="1" fill="{rnd.choice([SKY, PINK, LEMON])}" stroke="{INK}" stroke-width="1.1"/>'
            elif k < 0.7:  # 空调外机
                s += f'<rect x="{wx+36}" y="{wy+8}" width="9" height="12" rx="2" fill="#F4F6FB" stroke="{INK}" stroke-width="1.5"/><circle cx="{wx+40.5}" cy="{wy+14}" r="2.6" fill="none" stroke="{INK}" stroke-width="1"/>'
    if label:
        s += f'<rect x="{x0+w/2-66}" y="{top+hgt-24}" width="132" height="22" rx="11" fill="{LEMON}" stroke="{INK}" stroke-width="2.4"/>'
        s += text(x0 + w / 2, top + hgt - 8, label, 14, INK, None)
    return s

o += dorm(-20, 150, top=36, trim=LEMON, base="#FFF4F0")
o += dorm(170, 310, top=22, label="升华公寓 · 5 栋", trim=SKY)
o += dorm(700, 210, top=36, trim=PINK)
# 樟树 + 桂花
o += tree(150, 134, 0.8, seed=1)
o += tree(505, 130, 0.9, seed=2)
o += tree(672, 136, 0.85, seed=4)
o += tree(930, 140, 0.9, seed=3)

# ---------- 车棚地面 ----------
o += f'<rect x="0" y="146" width="{W}" height="{H-146}" fill="#E6E4F2"/>'
# 地砖小格
for yy in range(150, H, 32):
    o += f'<path d="M0,{yy} L{W},{yy}" stroke="#D8D5EA" stroke-width="1.5"/>'
# 雨棚（半透明天蓝顶边 + 柱子）
o += f'<rect x="0" y="146" width="{W}" height="22" fill="{SKY}" stroke="{INK}" stroke-width="3"/>'
for i in range(0, W, 40):
    o += f'<path d="M{i},168 q20,12 40,0" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'
o += f'<rect x="0" y="146" width="{W}" height="6" fill="{WHITE}" opacity="0.5"/>'

# ---------- 车阵 ----------
S = 1.35
ROWS = [228, 360, 470]     # 每排中心 y
xs = [60 + i * 34 for i in range(26)]
MINE_ROW, MINE_I = 1, 12
checked = {(0, 9), (0, 10), (1, 8), (1, 15)}   # 查看过的"不是我的"
for r, ry in enumerate(ROWS):
    # 车位线
    o += f'<rect x="30" y="{ry-38}" width="{W-60}" height="76" rx="10" fill="#DCD9EC" opacity="0.7"/>'
    for i, x in enumerate(xs):
        if r == 2 and i in (3, 4, 20):
            continue
        rot = rnd.uniform(-7, 7)
        dy = rnd.uniform(-4, 4)
        if (r, i) == (MINE_ROW, MINE_I):
            continue
        o += bike_other(x, ry + dy, S, rnd.randrange(7), rot=rot, basket=rnd.random() < 0.35)
    # 柱子
    o += f'<rect x="14" y="{ry-30}" width="10" height="60" rx="5" fill="{PINK}" stroke="{INK}" stroke-width="2.4"/>'
    o += f'<rect x="{W-24}" y="{ry-30}" width="10" height="60" rx="5" fill="{PINK}" stroke="{INK}" stroke-width="2.4"/>'

# 被夹住的自己的车（变黄 + 发光）
mx, my = xs[MINE_I], ROWS[MINE_ROW]
o += f'<circle cx="{mx}" cy="{my}" r="62" fill="url(#glowY)"/>'
# 左右邻车压得更紧 → 重画在上层
o += bike_other(xs[MINE_I - 1] + 5, my + 2, S, 1, rot=9)
o += bike_other(xs[MINE_I + 1] - 5, my - 1, S, 3, rot=-8)
o += f'<rect x="{mx-19}" y="{my-38}" width="38" height="76" rx="16" fill="none" stroke="{LEMON}" stroke-width="5"/>'
o += f'<rect x="{mx-19}" y="{my-38}" width="38" height="76" rx="16" fill="none" stroke="{INK}" stroke-width="2" stroke-dasharray="6 5"/>'
o += bike(mx, my, S*1.08, glow=False)
# 挤压标记
o += f'<path d="M{mx-30},{my-44} l6,6 M{mx-22},{my-48} l3,8" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
o += f'<path d="M{mx+30},{my-44} l-6,6 M{mx+22},{my-48} l-3,8" stroke="{INK}" stroke-width="2.5" stroke-linecap="round"/>'
o += sticker_sparkle(mx + 26, my - 34, 0.85)

# 查看过的车：小「×」标签
for (r, i) in checked:
    x, y = xs[i], ROWS[r]
    o += f'<g transform="translate({x},{y-40})"><rect x="-17" y="-10" width="34" height="18" rx="9" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>'
    o += text(0, 4, "不是", 11, "#9A97B5", None) + '</g>'

# ---------- 主角 ----------
px, py = mx - 70, 292
o += f'<path d="M{px-160},{py+14} q20,-8 40,0 t40,0 t40,0" stroke="#B9B4D6" stroke-width="3" fill="none" stroke-dasharray="2 9" stroke-linecap="round"/>'
o += chibi(px, py, 1.55, expr="happy", arms="up")
# 情绪符号
o += f'<path d="M{px+26},{py-44} l6,-8 M{px+32},{py-36} l9,-3 M{px+20},{py-50} l1,-10" stroke="{PINK_D}" stroke-width="3" stroke-linecap="round"/>'

# 独白气泡
o += bubble(px - 150, py - 118, 230, 48, "终于找到你了！", px - 8, py - 46, 21)
# 小副气泡（段子）
o += f'<g transform="translate({px-240},{py-40})">'
o += f'<rect x="0" y="0" width="130" height="30" rx="15" fill="{PINK_L}" stroke="{INK}" stroke-width="2"/>'
o += text(65, 20, "已查看 4 辆…", 13, INK, None) + '</g>'

# F 交互提示（车头上方）
o += f'<g transform="translate({mx},{my+50})"><rect x="-32" y="-2" width="64" height="30" rx="15" fill="{INK}" opacity="0.35" transform="translate(0,3)"/>'
o += f'<rect x="-32" y="-2" width="64" height="30" rx="15" fill="{LEMON}" stroke="{INK}" stroke-width="2.5"/>'
o += text(0, 19, "F 挪车", 14, INK, None) + '</g>'

# ---------- HUD ----------
o += battery_hud(16, 14, 38, low=True)
o += clock_hud(724, 18, "07:38", "DAY 2", signal=3, icon="sun")
o += f'<g transform="translate(880,98)"><rect x="-42" y="-12" width="84" height="24" rx="12" fill="{SKY}" stroke="{INK}" stroke-width="2.2"/>' + text(0, 5, "滴滴滴！", 13, WHITE, None) + '</g>'
# 钱/饥饿小胶囊
o += f'<g transform="translate(16,84)"><rect width="120" height="28" rx="14" fill="{WHITE}" stroke="{INK}" stroke-width="2.4"/>'
o += f'<circle cx="16" cy="14" r="9" fill="{LEMON}" stroke="{INK}" stroke-width="2"/>' + text(16, 19, "¥", 12, INK, None)
o += text(72, 20, "118", 16, INK, None) + '</g>'

o += hint_bar(480, 482, [("F", "查看"), ("E", "背包"), ("WASD", "移动")])
o += '</svg>'

open('01.svg', 'w').write(o)
render(o, '../01-findcar.png')
print('ok')
