# -*- coding: utf-8 -*-
# 02 骑行 · 07:52（校内大坡）
import random, sys
sys.path.insert(0, '.')
from lib import *

W, H = 960, 540
rnd = random.Random(11)
o = svg_open(W, H) + defs()

RL, RR = 300, 660            # 道路左右边
LANE = (RR - RL) / 3
lane_x = [RL + LANE * (i + 0.5) for i in range(3)]

# ---------- 草地两侧 ----------
o += f'<rect width="{W}" height="{H}" fill="#9BE3A8"/>'
for i in range(160):
    gx, gy = rnd.uniform(0, W), rnd.uniform(0, H)
    if RL - 40 < gx < RR + 40:
        continue
    o += f'<path d="M{gx:.0f},{gy:.0f} q2,-6 4,0 q2,-5 4,0" stroke="#6CCB86" stroke-width="2" fill="none" stroke-linecap="round"/>'
# 小花
for i in range(40):
    gx, gy = rnd.uniform(0, W), rnd.uniform(0, H)
    if RL - 50 < gx < RR + 50:
        continue
    c = rnd.choice([PINK, WHITE, LEMON])
    o += f'<circle cx="{gx:.0f}" cy="{gy:.0f}" r="3" fill="{c}" stroke="{INK}" stroke-width="1"/>'

# 人行道（樱粉砖）
o += f'<rect x="{RL-44}" y="0" width="44" height="{H}" fill="{PINK_L}" stroke="{INK}" stroke-width="3"/>'
o += f'<rect x="{RR}" y="0" width="44" height="{H}" fill="{PINK_L}" stroke="{INK}" stroke-width="3"/>'
for yy in range(0, H, 22):
    o += f'<path d="M{RL-44},{yy} h44 M{RR},{yy} h44" stroke="#F4B7C9" stroke-width="2"/>'

# ---------- 路面 ----------
o += f'<rect x="{RL}" y="0" width="{RR-RL}" height="{H}" fill="#8C92B5"/>'
# 坡道色块（暖棕紫）+ 上坡箭头
SL0, SL1 = 60, 330
o += f'<rect x="{RL}" y="{SL0}" width="{RR-RL}" height="{SL1-SL0}" fill="#B08CA8"/>'
for yy in range(SL0 + 10, SL1, 26):
    o += f'<path d="M{RL},{yy} h{RR-RL}" stroke="#A07C98" stroke-width="3"/>'
o += f'<path d="M{RL},{SL0} h{RR-RL} M{RL},{SL1} h{RR-RL}" stroke="{LEMON}" stroke-width="6" stroke-dasharray="18 12"/>'
# 车道线
for i in (1, 2):
    x = RL + LANE * i
    o += f'<path d="M{x},0 V{H}" stroke="{WHITE}" stroke-width="5" stroke-dasharray="30 26" stroke-linecap="round"/>'
# 路面「上坡」字 + 箭头
for yy in (120, 240):
    for lx in (lane_x[0], lane_x[2]):
        o += f'<path d="M{lx-18},{yy+10} L{lx},{yy-8} L{lx+18},{yy+10}" stroke="{WHITE}" stroke-width="6" fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0.8"/>'
# 斑马线（行人横穿）
ZY = 150
for i in range(9):
    o += f'<rect x="{RL+10+i*39}" y="{ZY-16}" width="22" height="32" rx="4" fill="{WHITE}" opacity="0.9"/>'
# 路边上坡标牌
o += f'<g transform="translate(880,190)"><rect x="-4" y="0" width="8" height="46" fill="#B8BCD6" stroke="{INK}" stroke-width="2"/>'
o += f'<path d="M0,-34 L32,20 L-32,20 Z" fill="{LEMON}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
o += f'<path d="M-16,12 L14,-6 L14,12 Z" fill="{INK}"/>' + '</g>'
o += f'<g transform="translate(880,252)"><rect x="-46" y="-14" width="92" height="28" rx="14" fill="{WHITE}" stroke="{INK}" stroke-width="2.5"/>' + text(0, 6, "大坡 · 8%", 15, INK, None) + '</g>'

# ---------- 樟树行道树 ----------
for i, yy in enumerate(range(-20, H + 60, 110)):
    o += tree(RL - 88, yy, 1.05, seed=i)
    o += tree(RR + 90, yy + 55, 1.05, seed=i + 20)
# 更外侧的积木楼 / 教学楼
o += f'<g><rect x="16" y="330" width="120" height="150" rx="12" fill="#F3F4FA" stroke="{INK}" stroke-width="3"/>'
for r in range(3):
    for c in range(2):
        o += f'<rect x="{32+c*50}" y="{350+r*40}" width="38" height="26" rx="6" fill="#CDEBFF" stroke="{INK}" stroke-width="2"/>'
o += f'<rect x="8" y="322" width="136" height="16" rx="8" fill="{SKY}" stroke="{INK}" stroke-width="3"/></g>'
o += f'<g transform="translate(76,504)"><rect x="-58" y="-14" width="116" height="26" rx="13" fill="{LEMON}" stroke="{INK}" stroke-width="2.4"/>' + text(0, 5, "→ 新校区教学楼", 13, INK, None) + '</g>'

# ---------- 障碍：校车（前方右车道，慢） ----------
o += bus(lane_x[2], 40, 1.05)
# 逆行车（左车道迎面，车头朝下）
o += wrongway(lane_x[0], 212, 1.55, rot=180)
o += f'<g transform="translate({lane_x[0]-40},250)">' + ''.join(f'<path d="M{d},0 v-22" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" opacity="0.8"/>' for d in (0, 10, 20)) + '</g>'
o += f'<g transform="translate({lane_x[0]+52},188)"><rect x="-34" y="-13" width="68" height="26" rx="13" fill="#FF7A8A" stroke="{INK}" stroke-width="2.4"/>' + text(0, 5, "逆行!", 14, WHITE, None) + '</g>'
# 行人横穿（看手机）
o += walker(RL + 170, ZY - 4, 1.35, hair="#2F2B45", top=MINT, expr="normal")
o += f'<path d="M{RL+140},{ZY+2} h-26 M{RL+140},{ZY+10} h-18" stroke="{WHITE}" stroke-width="3" stroke-linecap="round"/>'
o += f'<g transform="translate({RL+200},{ZY-44})"><rect x="-26" y="-12" width="52" height="24" rx="12" fill="{WHITE}" stroke="{INK}" stroke-width="2"/>' + text(0, 5, "♪~", 14, INK, None) + '</g>'

# ---------- 主角（中间车道） ----------
PX, PY = lane_x[1], 334
# 速度线
for dx in (-16, 0, 16):
    o += f'<path d="M{PX+dx},{PY+56} v30" stroke="{WHITE}" stroke-width="3" stroke-linecap="round" opacity="0.7"/>'
o += rider(PX, PY, 1.7, expr="tired", helmet=True, look_back=True)
o += sticker_sweat(PX - 30, PY - 40, 0.9)
# 独白气泡（放在路左侧空处）
o += bubble(PX + 30, PY - 104, 280, 50, "又是这个大坡……电量在哭。", PX + 14, PY - 40, 18)

# ---------- 后方外卖车冲上（半出屏）+ 底部警示 ----------
DX = lane_x[2]
o += delivery(DX, 432, 1.7)
o += f'<g transform="translate({DX-40},420)">' + ''.join(f'<path d="M{d},0 v-26" stroke="{WHITE}" stroke-width="3" stroke-linecap="round"/>' for d in (0, 10)) + '</g>'
# 底边红色闪烁警示条
o += f'<rect x="{DX-60}" y="{H-10}" width="120" height="10" fill="#FF5A7A"/>'
o += sticker_bang(DX + 90, 500, 1.2, PINK)
o += f'<g transform="translate({DX+92},452)"><rect x="-40" y="-13" width="80" height="26" rx="13" fill="{WHITE}" stroke="{INK}" stroke-width="2.4"/>' + text(0, 5, "外卖来袭", 13, PINK_D, None) + '</g>'

# ---------- HUD ----------
o += battery_hud(16, 14, 46, hearts=(2, 3))
o += clock_hud(724, 18, "07:52", "DAY 2", icon="sun")
o += f'<g transform="translate(832,104)"><rect x="-70" y="-14" width="140" height="28" rx="14" fill="{PINK}" stroke="{INK}" stroke-width="2.4"/>' + text(0, 6, "距教学楼 420m", 14, WHITE, None) + '</g>'
# 路线标签
o += slant_tag(20, 122, 118, 28, "校内路线", SKY, WHITE, 15)
# 耗电飘字
o += text(174, 145, "-1% ↓", 18, "#FF5A7A", WHITE, 5)

o += hint_bar(440, 488, [("W", "前进"), ("S", "刹车"), ("A/D", "换道")])
o += '</svg>'
open('02.svg', 'w').write(o)
render(o, '../02-ride.png')
print('ok')
