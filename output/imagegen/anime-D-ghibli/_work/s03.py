import random, math, time
import numpy as np
from wc import *
from shapes import *
W, H = 960, 540
rng = random.Random(33)
sc = Scene(W, H, S=2, bg=(0.93, 0.90, 0.82))
sc.layer('ground', warp=3, edge=0.35, mottle=0.16, lines=0, bleed=0.1, glaze=0.1)
sc.layer('ground2', warp=2.2, edge=0.55, mottle=0.12, lines=0.3, bleed=0.2, glaze=0.25)
sc.layer('build', warp=1.2, edge=0.5, mottle=0.1, lines=0.6, bleed=0.12, glaze=0.15)
sc.layer('build2', warp=1.0, edge=0.5, mottle=0.08, lines=0.5, bleed=0.1, glaze=0.1)
sc.layer('props', warp=0.8, edge=0.5, mottle=0.08, lines=0.6, bleed=0.1, glaze=0.1)
sc.layer('trees', warp=2.5, edge=0.6, mottle=0.14, lines=0.4, bleed=0.25, glaze=0.2)
sc.layer('night', warp=4, edge=0.1, mottle=0.18, lines=0, bleed=0, glaze=1.0, opacity=1.0)   # 夜色：正片叠底
sc.layer('glow', blend='screen', opacity=0.95)
sc.layer('dim', warp=1, edge=0, mottle=0.05, lines=0, bleed=0.3, glaze=0.2, opacity=0.9)
sc.layer('ui', warp=1.2, edge=0.5, mottle=0.08, lines=0.5, bleed=0.15, glaze=0.05)
sc.layer('text', crisp=True)
A = sc.add
sc.defs = ('<radialGradient id="lamp"><stop offset="0" stop-color="#FFD98A" stop-opacity=".9"/><stop offset=".45" stop-color="#C98A3A" stop-opacity=".45"/><stop offset="1" stop-color="#6a4a2a" stop-opacity="0"/></radialGradient>'
           '<radialGradient id="green"><stop offset="0" stop-color="#B6FF9A" stop-opacity=".95"/><stop offset=".5" stop-color="#5FC45A" stop-opacity=".45"/><stop offset="1" stop-color="#2a6a2a" stop-opacity="0"/></radialGradient>'
           '<radialGradient id="win"><stop offset="0" stop-color="#F6C66A" stop-opacity=".55"/><stop offset="1" stop-color="#F6C66A" stop-opacity="0"/></radialGradient>'
           '<radialGradient id="scr"><stop offset="0" stop-color="#ffffff" stop-opacity=".8"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>')

# ---------- 地面 ----------
A('ground', f'<rect width="{W}" height="{H}" fill="#C9C0AA"/>')
A('ground', f'<rect x="0" y="150" width="{W}" height="18" fill="#B7AE98"/>')
A('ground', f'<rect x="0" y="440" width="{W}" height="100" fill="#8DB86B"/>')
A('ground', f'<rect x="0" y="432" width="{W}" height="8" fill="#D8D0BC"/>')
for y in range(180, 432, 34):
    A('ground2', f'<path d="M0 {y} H{W}" stroke="#A89F8A" stroke-width="1" opacity=".55"/>')
for x in range(0, W, 48):
    A('ground2', f'<path d="M{x} 168 V432" stroke="#A89F8A" stroke-width="0.8" opacity=".35"/>')
for _ in range(60):
    x = rng.uniform(0, W); y = rng.uniform(444, 540)
    A('ground2', f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rng.uniform(4,12):.0f}" ry="{rng.uniform(2,5):.0f}" fill="{rng.choice(["#A9C77E","#76A35A","#9BC274"])}"/>')

# ---------- 宿舍楼 ----------
A('build', f'<rect x="0" y="-10" width="{W}" height="160" fill="#EFE6D2"/><rect x="0" y="130" width="{W}" height="22" fill="#B5553C"/>')
lit = []
for i, x in enumerate(range(18, W, 96)):
    for row, y in enumerate([-18, 38, 86]):
        if row == 2 and 400 < x < 560: continue
        A('build2', f'<rect x="{x}" y="{y}" width="80" height="40" fill="#8A9AA4"/>')
        on = rng.random() < 0.7
        if on: lit.append((x, y))
        wcol = '#F6D98A' if on else '#6F8290'
        A('build2', f'<rect x="{x+4}" y="{y+4}" width="34" height="24" fill="{wcol}"/><rect x="{x+42}" y="{y+4}" width="34" height="24" fill="{wcol if rng.random()<.8 else "#6F8290"}"/>')
        A('build2', f'<rect x="{x-2}" y="{y+28}" width="84" height="14" fill="#E4D9C2"/><path d="M{x} {y+6} H{x+80}" stroke="#6b5a4a" stroke-width="1"/>')
        if rng.random() < 0.6:
            for j in range(rng.randint(1, 3)):
                cx = x+8+j*14; col = rng.choice(['#FFFFFF', '#5B8DB8', '#C8553D', '#F2C14E', '#7FA36A'])
                A('build2', f'<path d="M{cx} {y+7} l-5 3 v4 h3 v10 h10 v-10 h3 v-4 l-5 -3 q-3 3 -6 0 z" fill="{col}"/>')
        if (i+row) % 2 == 0:
            A('build2', f'<rect x="{x+58}" y="{y+30}" width="20" height="11" rx="1" fill="#F4F1E8"/>')
# 楼门 + 门禁牌
A('build2', '<rect x="436" y="96" width="88" height="56" fill="#6b5a4a"/><rect x="442" y="102" width="36" height="50" fill="#E9C77A"/><rect x="482" y="102" width="36" height="50" fill="#E9C77A"/>'
            '<rect x="420" y="88" width="120" height="10" fill="#D8CDB5"/>')
A('build2', '<rect x="548" y="100" width="60" height="40" rx="3" fill="#F4EBD0" stroke="#6E4A2E" stroke-width="2"/>')
A('text', txt(578, 116, '门禁', 11, '#B5553C') + txt(578, 133, '23:00', 13, '#5a3e2b'))

# ---------- 充电桩一排（带雨棚） ----------
A('props', '<rect x="110" y="170" width="740" height="10" rx="3" fill="#6E9E8E"/>')
for x in range(116, 860, 148):
    A('props', f'<rect x="{x-3}" y="166" width="7" height="12" fill="#5f4a38"/>')
piles = []   # (x, 状态)
states = ['busy', 'free', 'plugged', 'broken', 'busy', 'fail', 'busy', 'free', 'busy', 'broken', 'busy']
xs = [140+i*66 for i in range(len(states))]
for x, st in zip(xs, states):
    # 桩体 32x40（3/4 俯视：顶 + 正面）
    A('props', f'<rect x="{x-16}" y="186" width="32" height="40" rx="5" fill="#E8EEF0"/><rect x="{x-16}" y="186" width="32" height="8" rx="4" fill="#C7D3D8"/>'
               f'<rect x="{x-11}" y="197" width="22" height="12" rx="2" fill="#2f3a40"/><rect x="{x-6}" y="213" width="12" height="9" rx="2" fill="#fff" stroke="#6b7a80" stroke-width="1"/>'
               f'<path d="M{x-4} 215 h3 v3 h-3z M{x+1} 215 h3 v3 h-3z M{x-4} 219 h8" stroke="#3b3531" stroke-width="1"/>')
    scr = {'busy': '#E9A94A', 'broken': '#2f3a40', 'free': '#8ED0E8', 'plugged': '#8BE07A', 'fail': '#E86F4F'}[st]
    A('props', f'<rect x="{x-9}" y="199" width="18" height="8" rx="1.5" fill="{scr}"/>')
    if st != 'broken':
        A('glow', f'<ellipse cx="{x}" cy="203" rx="22" ry="16" fill="url(#scr)" opacity=".5"/><rect x="{x-9}" y="199" width="18" height="8" rx="1.5" fill="{scr}" opacity=".7"/>')
    # 车位线
    A('ground2', f'<path d="M{x-30} 236 V330 M{x+30} 236 V330" stroke="#EDE3C8" stroke-width="2" opacity=".75"/>')
    if st in ('busy', 'broken'):
        if st == 'busy' or rng.random() < .5:
            A('props', bike(x-12, 240, 1.0, body=rng.choice(['#F7F3EA', '#E6EEF0', '#F2E5E0', '#DCE3E8']), seat=rng.choice(['#4a4440', '#3f4a52', '#6d5a4c']), rot=rng.uniform(-4, 4)))
            if st == 'busy':
                A('props', f'<path d="M{x+6} 222 q10 14 -4 26" stroke="#3b3531" stroke-width="2" fill="none"/>')
    if st == 'plugged':
        pass
# 状态小标签（手账便签）
labels = {'busy': ('被占', '#E9A94A'), 'broken': ('坏了', '#8a8a8a'), 'free': ('空闲', '#6FB7D0'), 'plugged': ('充电中', '#6FB35A'), 'fail': ('扫码失败', '#E86F4F')}
shown = set()
for x, st in zip(xs, states):
    if st in shown and st not in ('free',): continue
    shown.add(st)
    lb, col = labels[st]
    w = 18+len(lb)*12
    A('ui', f'<rect x="{x-w/2}" y="{158}" width="{w}" height="18" rx="9" fill="#FFF8E8" stroke="{col}" stroke-width="2"/>')
    A('text', txt(x, 171, lb, 11, '#5a3e2b'))
# 坏桩：裂纹 + 小红叉
bxk = xs[2]
A('ui', f'<path d="M{bxk-6} 200 l4 3 -2 3 5 2" stroke="#9aa6aa" stroke-width="1" fill="none"/>')

# 主角的车：插在第 6 个桩（plugged），主角在旁边推 / 站
PX = xs[2]
A('glow', f'<ellipse cx="{PX}" cy="215" rx="40" ry="40" fill="url(#green)" opacity=".8"/><ellipse cx="{PX}" cy="266" rx="30" ry="40" fill="url(#lamp)" opacity=".6"/>')
A('props', bike(PX-12, 242, 1.0, body='#F2C14E', seat='#C8553D', cargo='bread'))
A('props', f'<path d="M{PX+6} 222 q14 16 0 30" stroke="#3b3531" stroke-width="2.4" fill="none"/>')
A('glow', f'<path d="M{PX+6} 222 q14 16 0 30" stroke="#A8FF9A" stroke-width="5" fill="none" opacity=".6"/>')
# 主角（推车后站着）
A('props', person_top(PX+28, 262, 1.5, shirt='#E86F4F', hair='#3a2a22', bag='#F2C14E', arms_to=((PX+11, 254), (PX+14, 272))))
# 另一个同学推车找桩
A('props', f'<g transform="translate({xs[10]+40} 350) rotate(90)">' + bike(0, 0, 1.0, body='#E6EEF0', seat='#3f4a52') + '</g>')
A('props', walker(xs[10]-10, 364, 1.05, shirt='#9CC9E0', dirx=1, bag=None))
# 猫在草地
cx_, cy_ = 120, 470
A('props', f'<ellipse cx="{cx_}" cy="{cy_}" rx="10" ry="7" fill="#3b3531"/><circle cx="{cx_+9}" cy="{cy_-5}" r="5" fill="#3b3531"/>'
           f'<path d="M{cx_+6} {cy_-9} l1 -5 3 3z M{cx_+12} {cy_-9} l0 -5 -3 3z" fill="#3b3531"/><circle cx="{cx_+8}" cy="{cy_-6}" r="1.1" fill="#F2D06B"/><circle cx="{cx_+11}" cy="{cy_-6}" r="1.1" fill="#F2D06B"/>')

# 路灯
LAMPS = [(90, 420), (560, 290), (880, 300)]
for lx, ly in LAMPS:
    A('props', f'<rect x="{lx-3}" y="{ly-50}" width="6" height="56" fill="#4a4440"/><ellipse cx="{lx}" cy="{ly-54}" rx="12" ry="7" fill="#6b5a4a"/><ellipse cx="{lx}" cy="{ly-52}" rx="7" ry="4" fill="#FFE7A0"/>')

# 樟树 / 桂花
tr = random.Random(12)
for (cx, cy, r) in [(230, 490, 48), (720, 500, 54), (380, 530, 40), (930, 470, 44)]:
    A('trees', camphor(cx, cy, r, tr, osm=(cx == 720)))

# ---------- 夜色（整体正片叠底）----------
A('night', f'<rect width="{W}" height="{H}" fill="#5C6AA0"/>')
# ---------- 灯光（screen）----------
for (x, y) in lit:
    A('glow', f'<rect x="{x+4}" y="{y+4}" width="72" height="24" fill="#F6C66A" opacity=".8"/><ellipse cx="{x+40}" cy="{y+20}" rx="64" ry="34" fill="url(#win)"/>')
A('glow', '<rect x="440" y="100" width="80" height="54" fill="#F6C66A" opacity=".8"/><ellipse cx="480" cy="170" rx="120" ry="50" fill="url(#lamp)"/>')
for lx, ly in LAMPS:
    A('glow', f'<ellipse cx="{lx}" cy="{ly-10}" rx="190" ry="150" fill="url(#lamp)"/><ellipse cx="{lx}" cy="{ly-52}" rx="30" ry="22" fill="url(#lamp)"/>')
A('glow', '<rect x="548" y="100" width="60" height="40" fill="#E9D6A6" opacity=".6"/>')
# 萤火虫 / 桂花香点
for _ in range(18):
    A('glow', f'<circle cx="{tr.uniform(0,W):.0f}" cy="{tr.uniform(440,540):.0f}" r="{tr.uniform(1.5,3):.1f}" fill="#FFE08A" opacity=".8"/>')

# ---------- 弹窗前的暗化 ----------


# ---------- UI ----------
A('ui', note(14, 12, 196, 58, fill='#FBF3DC', rot=-1.2))
A('ui', tape(40, 14, 38, 12, -8))
A('ui', '<path d="M30 30 l-6 11 h6 l-3 10 10 -14 h-6 l4 -7 z" fill="#F2C14E" stroke="#6b4f3a" stroke-width="1.4" stroke-linejoin="round"/>')
A('ui', battery_bar(62, 32, 18, w=112, h=20, col='#D9574A'))
A('text', txt(184, 48, '18%', 15, '#5a3e2b', anchor='start'))
A('ui', woodboard(760, 12, 186, 60))
A('ui', f'<circle cx="788" cy="36" r="11" fill="#FFF8E8" stroke="#5a3e2b" stroke-width="1.6"/><path d="M788 29 V36 L793 39" stroke="#5a3e2b" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
A('text', txt(852, 44, '22:47', 22, '#FFF6E2') + txt(852, 63, '门禁 23:00 · 还剩13分', 10, '#FFE0A0'))
# 月亮贴纸
A('ui', '<circle cx="732" cy="36" r="16" fill="#FBE7A6"/><circle cx="740" cy="30" r="14" fill="#EFE6D2" opacity="0"/>')
A('ui', '<path d="M724 24 a16 16 0 1 0 18 24 a13 13 0 1 1 -18 -24z" fill="#F7D774" stroke="#8a6a3a" stroke-width="1.2"/>')

# 弹窗：手账页
DX, DY, DW, DH = 340, 300, 440, 182
A('ui', note(DX, DY, DW, DH, fill='#FBF3DC', rot=0, lines=True))
A('ui', f'<rect x="{DX}" y="{DY}" width="{DW}" height="{DH}" rx="4" fill="none" stroke="#8a6a4a" stroke-width="2"/>')
A('ui', tape(DX+40, DY+2, 60, 16, -6, '#E7B7A3') + tape(DX+DW-40, DY+2, 60, 16, 6, '#9CC9E0'))
for k in range(7):   # 装订孔
    A('ui', f'<circle cx="{DX+14}" cy="{DY+26+k*22}" r="4" fill="#E0D2B4" stroke="#b9a27e" stroke-width="1"/>')
# 小插图：插头 + 桂花
A('ui', f'<g transform="translate({DX+DW-66} {DY+34})"><rect x="0" y="6" width="26" height="30" rx="5" fill="#E8EEF0" stroke="#6b7a80" stroke-width="1.5"/><rect x="5" y="11" width="16" height="8" rx="1" fill="#8BE07A"/>'
       f'<path d="M13 36 q0 16 16 16" stroke="#3b3531" stroke-width="2.4" fill="none"/><path d="M8 -2 l3 5 M18 -2 l-3 5" stroke="#F2C14E" stroke-width="2" stroke-linecap="round"/></g>')
A('text', txt(DX+DW/2-10, DY+56, '终于插上了。', 22, '#5a3e2b', family=SERIF))
A('text', txt(DX+DW/2-10, DY+88, '守着它，还是先回宿舍？', 19, '#5a3e2b', family=SERIF))
# 两个选项横排（左高亮）
bw, bh = 150, 46
L_X, R_X, BY = DX+DW/2-bw-18, DX+DW/2+18, DY+112
A('ui', f'<rect x="{L_X+3}" y="{BY+4}" width="{bw}" height="{bh}" rx="10" fill="#3a2a1a" opacity=".25"/><rect x="{L_X}" y="{BY}" width="{bw}" height="{bh}" rx="10" fill="#F2C14E" stroke="#8a5a2a" stroke-width="2.6"/>')
A('ui', f'<rect x="{R_X}" y="{BY}" width="{bw}" height="{bh}" rx="10" fill="#EFE6D2" stroke="#b9a27e" stroke-width="2" stroke-dasharray="6 4"/>')
A('ui', f'<path d="M{L_X-20} {BY+bh/2-8} l12 8 -12 8z" fill="#C8553D"/>')
A('text', txt(L_X+bw/2, BY+30, '守着它', 19, '#4a2e1a') + txt(R_X+bw/2, BY+30, '回宿舍', 19, '#8a7a66'))
# 底部提示
A('ui', note(300, 494, 360, 34, fill='#FFF7E4', rot=0.5, lines=False))
A('ui', tape(306, 497, 30, 11, -30, '#B9D3A4')); A('ui', tape(654, 497, 30, 11, 30, '#B9D3A4'))
A('ui', keycap(330, 499, 'A') + keycap(376, 499, 'D') + keycap(504, 499, 'F'))
A('text', txt(365, 517, '/', 13, '#8a6a4a') + txt(436, 517, '切换', 14, '#5a3e2b') + txt(480, 517, '·', 14, '#8a6a4a') + txt(568, 517, '确认', 14, '#5a3e2b'))
# 独白气泡（主角头顶，弹窗外）
A('ui', bubble(34, 276, 196, 36, PX+10, 272))
A('text', txt(132, 300, '你也熬到这么晚啊……', 14, '#5a3e2b'))

t = time.time()
cv = sc.build(seed=33, paper_strength=0.9)
save(cv, '../03-charge.png', (W, H))
print('done', time.time()-t)
