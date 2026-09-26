# -*- coding: utf-8 -*-
# 03 夜间充电 · 22:47
import random, sys
sys.path.insert(0, '.')
from lib import *

W, H = 960, 540
rnd = random.Random(5)
o = svg_open(W, H) + defs()

NIGHT = "#2E3470"
NIGHT2 = "#3C4488"
# ---------- 夜空 + 岳麓山剪影 ----------
o += f'<rect width="{W}" height="{H}" fill="{NIGHT}"/>'
for i in range(40):
    sx, sy = rnd.uniform(0, W), rnd.uniform(0, 120)
    r = rnd.choice([1.2, 1.6, 2.2])
    o += f'<circle cx="{sx:.0f}" cy="{sy:.0f}" r="{r}" fill="#FFF3B0" opacity="0.85"/>'
o += f'<g opacity="0.9">{mountain(760, 120, 1.3, face_on=False)}</g>'
o += f'<path d="M660,90 Q760,40 860,100 L960,140 L560,140 Z" fill="{NIGHT2}" opacity="0.55"/>'
o += f'<g transform="translate(120,56)"><path d="M6,-22 A24,24 0 1,0 16,16 A19,19 0 1,1 6,-22 Z" fill="{LEMON}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
o += f'<ellipse cx="-8" cy="4" rx="3" ry="2" fill="{PINK}" opacity="0.8"/><path d="M-12,-4 q3,-3 6,0" stroke="{INK}" stroke-width="2" fill="none" stroke-linecap="round"/></g>'

# ---------- 宿舍楼（窗户亮灯） ----------
def dorm_night(x0, w, top, label=None, trim=SKY):
    s = f'<rect x="{x0+6}" y="{top+6}" width="{w}" height="{200-top}" rx="10" fill="#161A40" opacity="0.5"/>'
    s += f'<rect x="{x0}" y="{top}" width="{w}" height="{200-top}" rx="10" fill="#5A62A8" stroke="{INK}" stroke-width="3"/>'
    s += f'<rect x="{x0-6}" y="{top-6}" width="{w+12}" height="16" rx="8" fill="{trim}" stroke="{INK}" stroke-width="3"/>'
    cols = int((w - 20) // 46)
    rows = int((200 - top - 30) // 34)
    for r in range(rows):
        for c in range(cols):
            wx = x0 + 16 + c * 46
            wy = top + 20 + r * 34
            lit = rnd.random() < 0.62
            col = rnd.choice(["#FFE08A", "#FFD0A0", "#FFF3C4"]) if lit else "#3A407E"
            if lit:
                s += f'<rect x="{wx-4}" y="{wy-4}" width="42" height="32" rx="9" fill="#FFE08A" opacity="0.25"/>'
            s += f'<rect x="{wx}" y="{wy}" width="34" height="24" rx="6" fill="{col}" stroke="{INK}" stroke-width="2"/>'
            if lit and rnd.random() < 0.4:  # 窗里的小人剪影
                s += f'<circle cx="{wx+22}" cy="{wy+12}" r="5" fill="#C98F5E" opacity="0.6"/><rect x="{wx+15}" y="{wy+16}" width="14" height="8" rx="4" fill="#C98F5E" opacity="0.6"/>'
            s += f'<rect x="{wx-2}" y="{wy+17}" width="38" height="8" rx="3" fill="#8C93D6" stroke="{INK}" stroke-width="1.8"/>'
    if label:
        s += f'<rect x="{x0+w/2-80}" y="{top-14}" width="160" height="24" rx="12" fill="{LEMON}" stroke="{INK}" stroke-width="2.4"/>'
        s += text(x0 + w / 2, top + 4, label, 14, INK, None)
    return s

o += dorm_night(-20, 190, 40, trim=PINK)
o += dorm_night(200, 360, 30, label="升华公寓 · 充电区", trim=SKY)
o += dorm_night(590, 120, 70, trim=LEMON)
# ---------- 地面 ----------
o += f'<rect x="0" y="200" width="{W}" height="{H-200}" fill="#4A5196"/>'
for yy in range(214, H, 34):
    o += f'<path d="M0,{yy} L{W},{yy}" stroke="#555DA4" stroke-width="2"/>'
# 路灯光晕
for lx in (90, 870):
    o += f'<ellipse cx="{lx}" cy="330" rx="170" ry="120" fill="url(#glowLamp)"/>'
    o += f'<rect x="{lx-4}" y="206" width="8" height="120" rx="4" fill="#8C93D6" stroke="{INK}" stroke-width="2.5"/>'
    o += f'<ellipse cx="{lx}" cy="206" rx="18" ry="10" fill="#FFE9A8" stroke="{INK}" stroke-width="2.5"/>'
# 樟树
o += tree(40, 470, 1.0, c1="#3E9B72", c2="#5BB98A", c3="#2C7A58", flowers=True, seed=8)
o += tree(925, 470, 1.0, c1="#3E9B72", c2="#5BB98A", c3="#2C7A58", flowers=True, seed=9)

# ---------- 充电桩一排 ----------
PS = 1.55
states = ["occupied", "broken", "occupied", "qr", "plugged", "occupied", "broken", "free"]
px0, pgap, py = 170, 88, 238
for i, st in enumerate(states):
    x = px0 + i * pgap
    o += pile(x, py, PS, st)
    # 桩前的车位
    o += f'<rect x="{x-22}" y="{py+34}" width="44" height="76" rx="10" fill="none" stroke="#8C93D6" stroke-width="2.5" stroke-dasharray="8 6"/>'
    if st == "occupied":
        o += bike_other(x, py + 70, 1.3, i, rot=rnd.uniform(-5, 5))
        o += f'<path d="M{x+12},{py+12} C{x+26},{py+30} {x+18},{py+50} {x+6},{py+58}" stroke="#FF6F8E" stroke-width="3" fill="none" stroke-linecap="round"/>'
    if st == "plugged":
        o += bike(x, py + 70, 1.3, glow=True)
        o += f'<path d="M{x+12},{py+12} C{x+30},{py+30} {x+22},{py+50} {x+8},{py+60}" stroke="#5CF09A" stroke-width="4" fill="none" stroke-linecap="round"/>'
        for dx, dy in ((-30, 30), (30, 90), (-26, 110)):
            o += f'<path d="M{x+dx},{py+dy-6} l-4,7 l4,0 l-3,7 l8,-9 l-4,0 l3,-5 Z" fill="#8CFFB8" stroke="{INK}" stroke-width="1.2"/>'
# 桩状态小标签
tags = {0: ("被占", "#FF6F8E"), 1: ("坏了", "#8A90AA"), 3: ("扫码失败", LEMON_D), 4: ("充电中", "#2BC46E"), 7: ("空闲", "#2BC46E")}
for i, (lab, c) in tags.items():
    x = px0 + i * pgap
    w = 16 * len(lab) + 20
    o += f'<g transform="translate({x},{py-46})"><rect x="{-w/2}" y="-12" width="{w}" height="24" rx="12" fill="{WHITE}" stroke="{INK}" stroke-width="2.2"/>' + text(0, 5, lab, 13, c, None) + '</g>'
# 坏桩 😵 贴纸
o += sticker_dizzy(px0 + pgap + 24, py - 22, 0.7)

# ---------- 主角推车（刚把车推到桩前） ----------
MX, MY = px0 + 4 * pgap, py + 70
PX, PY = MX + 50, 300
o += chibi(PX, PY, 1.3, expr="happy", arms="front", top=SKY)
o += sticker_sparkle(PX + 30, PY - 34, 0.6)

# ---------- 选项弹窗 ----------
o += f'<rect width="{W}" height="{H}" fill="#161A40" opacity="0.28"/>'
# 重新绘制高亮的那组，放在遮罩之上作为焦点
o += pile(MX, py, PS, "plugged")
o += bike(MX, py + 70, 1.3, glow=True)
o += f'<path d="M{MX+12},{py+12} C{MX+30},{py+30} {MX+22},{py+50} {MX+8},{py+60}" stroke="#5CF09A" stroke-width="4" fill="none" stroke-linecap="round"/>'
o += chibi(PX, PY, 1.3, expr="happy", arms="front", top=SKY)

o += bubble(PX + 30, PY - 86, 150, 40, '亮绿灯了！！', PX + 12, PY - 32, 16)
BX, BY, BW, BH = 200, 346, 560, 136
o += card(BX, BY, BW, BH, WHITE, INK, 3.5, 22, sh=7)
o += f'<rect x="{BX+10}" y="{BY+10}" width="{BW-20}" height="{BH-20}" rx="15" fill="none" stroke="{SKY_L}" stroke-width="2.5"/>'
o += slant_tag(BX + 24, BY - 16, 132, 30, "充电桩 No.5", SKY, WHITE, 15)
o += f'<g transform="translate({BX+BW-40},{BY+4})">' + sticker_sparkle(0, 0, 0.8) + '</g>'
o += text(BX + BW / 2, BY + 48, "终于插上了。守着它，还是先回宿舍？", 21, INK, None)
# 两个选项（横排，左边高亮）
b1x, b2x, by, bw, bh = BX + 50, BX + 300, BY + 70, 210, 48
o += f'<rect x="{b1x}" y="{by+6}" width="{bw}" height="{bh}" rx="26" fill="{INK}"/>'
o += f'<rect x="{b1x}" y="{by}" width="{bw}" height="{bh}" rx="26" fill="{LEMON}" stroke="{INK}" stroke-width="3"/>'
o += f'<path d="M{b1x+24},{by+12} q20,-4 50,-2" stroke="{WHITE}" stroke-width="4" stroke-linecap="round" fill="none" opacity="0.8"/>'
o += text(b1x + bw / 2, by + 32, "守着它", 20, INK, None)
o += f'<path d="M{b1x-22},{by+16} l14,10 l-14,10 Z" fill="{PINK}" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
o += f'<rect x="{b2x}" y="{by+6}" width="{bw}" height="{bh}" rx="26" fill="{INK}" opacity="0.35"/>'
o += f'<rect x="{b2x}" y="{by}" width="{bw}" height="{bh}" rx="26" fill="#F1F3FA" stroke="{INK}" stroke-width="3"/>'
o += text(b2x + bw / 2, by + 32, "回宿舍", 20, "#8A87A8", None)
# 选项小注
o += slant_tag(b1x + bw - 70, by + 38, 86, 20, "稳 · +5%/分", MINT, INK, 11, 6)
o += slant_tag(b2x + bw - 70, by + 38, 86, 20, "赌 · 50%满", PINK, WHITE, 11, 6)

# ---------- HUD ----------
o += battery_hud(16, 14, 12, low=True)
o += clock_hud(724, 18, "22:47", "DAY 2", icon="moon")
o += f'<g transform="translate(834,104)"><rect x="-62" y="-14" width="124" height="28" rx="14" fill="#FF6F8E" stroke="{INK}" stroke-width="2.4"/>' + text(0, 6, "门禁 23:00", 15, WHITE, None) + '</g>'
o += f'<g transform="translate(16,84)"><rect width="120" height="28" rx="14" fill="{WHITE}" stroke="{INK}" stroke-width="2.4"/>'
o += f'<circle cx="16" cy="14" r="9" fill="{LEMON}" stroke="{INK}" stroke-width="2"/>' + text(16, 19, "¥", 12, INK, None)
o += text(72, 20, "63", 16, INK, None) + '</g>'

o += hint_bar(480, 488, [("A/D", "切换"), ("F", "确认")])
o += '</svg>'
open('03.svg', 'w').write(o)
render(o, '../03-charge.png')
print('ok')
