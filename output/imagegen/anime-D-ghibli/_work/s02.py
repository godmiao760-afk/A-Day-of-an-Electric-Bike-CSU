import random, math, time
from wc import *
from shapes import *
W, H = 960, 540
rng = random.Random(21)
sc = Scene(W, H, S=2)
sc.layer('ground', warp=3, edge=0.35, mottle=0.14, lines=0, bleed=0.1, glaze=0.1)
sc.layer('ground2', warp=2.2, edge=0.55, mottle=0.12, lines=0.3, bleed=0.2, glaze=0.25)
sc.layer('shadow', warp=3, edge=0.2, mottle=0.2, lines=0, bleed=0.3, glaze=0.9, opacity=0.9)
sc.layer('props', warp=1.0, edge=0.5, mottle=0.08, lines=0.6, bleed=0.1, glaze=0.1)
sc.layer('vehicles', warp=0.7, edge=0.45, mottle=0.06, lines=0.6, bleed=0.08, glaze=0.08)
sc.layer('trees', warp=2.5, edge=0.6, mottle=0.14, lines=0.45, bleed=0.25, glaze=0.2)
sc.layer('glow', blend='screen', opacity=0.8)
sc.layer('ui', warp=1.2, edge=0.5, mottle=0.08, lines=0.5, bleed=0.15, glaze=0.05)
sc.layer('text', crisp=True)
A = sc.add
RL, RR = 336, 624          # 路面左右边界（3 车道，每道 96）
LANE = [384, 480, 576]

# ---------- 地面 ----------
A('ground', f'<rect width="{W}" height="{H}" fill="#8DB86B"/>')
A('ground', f'<rect x="{RL-28}" y="0" width="28" height="{H}" fill="#D8CDB2"/><rect x="{RR}" y="0" width="28" height="{H}" fill="#D8CDB2"/>')   # 人行道
A('ground', f'<rect x="{RL}" y="0" width="{RR-RL}" height="{H}" fill="#8F8A80"/>')
# 坡道段：路面变暖棕色（上坡）
A('ground2', f'<rect x="{RL}" y="40" width="{RR-RL}" height="200" fill="#A8845E" opacity=".75"/>')
for y in range(52, 236, 22):
    A('ground2', f'<path d="M{RL+8} {y+10} L{(RL+RR)/2} {y} L{RR-8} {y+10}" stroke="#7E5E3E" stroke-width="3" fill="none" opacity=".45"/>')
# 人行道砖
for y in range(0, H, 18):
    A('ground2', f'<path d="M{RL-28} {y} h28 M{RR} {y} h28" stroke="#B9AD92" stroke-width="1"/>')
# 车道虚线
for x in (432, 528):
    A('ground2', f'<path d="M{x} 0 V{H}" stroke="#F4EBD0" stroke-width="3.5" stroke-dasharray="26 22"/>')
A('ground2', f'<path d="M{RL+4} 0 V{H} M{RR-4} 0 V{H}" stroke="#F4EBD0" stroke-width="2.5"/>')
# 路面裂缝、补丁、井盖
A('ground2', '<rect x="440" y="300" width="60" height="30" rx="4" fill="#7E7970"/><circle cx="600" cy="420" r="11" fill="#6f6a62"/><circle cx="600" cy="420" r="7" fill="none" stroke="#8f8a80" stroke-width="1.5"/>')
A('ground2', '<path d="M360 470 l12 -6 8 5 14 -9" stroke="#6b665e" stroke-width="1.2" fill="none"/>')
# 斑马线
for i in range(9):
    A('ground2', f'<rect x="{RL+6+i*32}" y="278" width="18" height="46" fill="#F4EBD0" opacity=".92"/>')
# “上坡”地面文字
A('ground2', f'<rect x="{LANE[0]-30}" y="176" width="60" height="30" fill="none"/>')
# 草地斑点 & 花
for _ in range(120):
    x = rng.choice([rng.uniform(0, RL-30), rng.uniform(RR+30, W)]); y = rng.uniform(0, H)
    A('ground2', f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rng.uniform(4,12):.0f}" ry="{rng.uniform(2,5):.0f}" fill="{rng.choice(["#A9C77E","#76A35A","#9BC274"])}"/>')
for _ in range(40):
    x = rng.choice([rng.uniform(10, RL-40), rng.uniform(RR+40, W-10)]); y = rng.uniform(0, H)
    A('ground2', f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2.2" fill="{rng.choice(["#FFF6E0","#F2D06B","#E9A3A0"])}"/>')

# ---------- 路边：左侧 看台/小路/公告栏，右侧 教学楼一角 ----------
# 左：石阶小路 + 长椅 + 公告栏
A('props', '<path d="M0 360 Q120 350 180 380 T308 400" stroke="#D8CDB2" stroke-width="22" fill="none"/>')
A('props', '<rect x="150" y="430" width="60" height="14" rx="3" fill="#9A6B43"/><rect x="150" y="446" width="60" height="5" rx="2" fill="#6E4A2E"/>')
A('props', '<rect x="60" y="252" width="92" height="56" rx="4" fill="#B07D4F"/><rect x="66" y="258" width="80" height="44" fill="#F4EBD0"/>'
           '<rect x="70" y="262" width="30" height="20" fill="#9CC9E0"/><rect x="104" y="262" width="38" height="12" fill="#E9A3A0"/><rect x="104" y="278" width="38" height="20" fill="#F2D06B"/><rect x="70" y="286" width="30" height="12" fill="#B9D3A4"/>'
           '<rect x="72" y="308" width="6" height="14" fill="#6E4A2E"/><rect x="134" y="308" width="6" height="14" fill="#6E4A2E"/>')
A('text', txt(106, 249, '社团招新', 10, '#5a3e2b'))
# 右：图书馆灰白立面（3/4 俯视）
A('props', '<rect x="760" y="-10" width="220" height="150" fill="#E3E0D8"/><rect x="760" y="130" width="220" height="16" fill="#BEB9AE"/>')
for yy in (6, 50, 94):
    for xx in range(772, 960, 34):
        A('props', f'<rect x="{xx}" y="{yy}" width="24" height="30" fill="#9FB6C2"/><path d="M{xx+3} {yy+4} l10 -2" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>')
A('props', '<rect x="780" y="146" width="120" height="8" fill="#D8CDB2"/>')
A('text', txt(860, 166, '新校区 · 图书馆', 11, '#5a3e2b'))
# 右下：自行车架与桂花
A('props', '<rect x="700" y="420" width="120" height="8" rx="3" fill="#7d7466"/>')
for k in range(4):
    A('vehicles', f'<g transform="translate({706+k*28} 400)">' + bike(0, 0, 0.8, body=['#F7F3EA','#E6EEF0','#F2E5E0','#DCE3E8'][k], seat='#4a4440') + '</g>')
# 左：坡顶路牌
A('props', '<rect x="197" y="196" width="6" height="40" fill="#6E4A2E"/><rect x="160" y="170" width="80" height="30" rx="4" fill="#F4EBD0" stroke="#6E4A2E" stroke-width="2"/>')
A('text', txt(200, 191, '前方大坡', 13, '#B5553C'))
# 上坡地面字
A('text', f'<g transform="translate({LANE[1]} 96)" opacity=".85">' + txt(0, 0, '上', 30, '#F4EBD0') + txt(0, 34, '坡', 30, '#F4EBD0') + '</g>')

# ---------- 车辆 / 行人 ----------
# 校车（慢、大）在左道前方
bx, by = LANE[0]-32, 26
A('shadow', f'<rect x="{bx+6}" y="{by+8}" width="64" height="140" rx="12" fill="#2d3a24" opacity=".35"/>')
A('vehicles', f'<g transform="translate({bx} {by})">'
    '<rect x="0" y="0" width="64" height="140" rx="12" fill="#6E9E4A"/>'
    '<rect x="4" y="6" width="56" height="20" rx="8" fill="#BFD7E2"/><path d="M10 10 l18 -2" stroke="#fff" stroke-opacity=".7" stroke-width="3"/>'
    '<rect x="6" y="30" width="52" height="104" rx="6" fill="#F4EBD0"/>'
    '<rect x="6" y="30" width="52" height="10" fill="#E9DFC4"/>'
    '<rect x="12" y="50" width="16" height="12" rx="2" fill="#8FA7A8"/><rect x="36" y="50" width="16" height="12" rx="2" fill="#8FA7A8"/>'
    '<rect x="22" y="80" width="20" height="30" rx="3" fill="#D8CDB2"/>'
    '<rect x="0" y="130" width="64" height="10" rx="5" fill="#4F7A3A"/>'
    '<rect x="6" y="132" width="10" height="4" fill="#C8553D"/><rect x="48" y="132" width="10" height="4" fill="#C8553D"/></g>')
A('text', txt(bx+32, by+100, '校园巴士', 9, '#3F6B3A'))
# 逆行车：右道迎面（车头朝下）
wx, wy = LANE[2]-16, 150
A('vehicles', f'<g transform="translate({wx+32} {wy+56}) rotate(180)">' + rider(0, 0, 1.0, body='#E6EEF0', seat='#3f4a52', shirt='#C8553D', helmet=None) + '</g>')
A('ui', f'<path d="M{wx+16} {wy+70} v20 m-8 -8 l8 8 8 -8" stroke="#C8553D" stroke-width="3" fill="none" stroke-linecap="round"/>')
# 行人横穿斑马线
A('vehicles', walker(RL+8, 286, 1.1, shirt='#9CC9E0', dirx=1, step=2, bag='#F2C14E'))
A('vehicles', walker(RL+44, 292, 1.05, shirt='#F7F3EA', dirx=1, step=-2, bag='#B5553C', hair='#5a3e2b'))
# 主角：中间车道
px, py = LANE[1]-16, 356
A('shadow', f'<ellipse cx="{px+20}" cy="{py+32}" rx="16" ry="28" fill="#2d3a24" opacity=".25"/>')
A('vehicles', rider(px, py, 1.0, body='#F2C14E', seat='#C8553D', shirt='#E86F4F', helmet='#F4EBD0', bag='#F2C14E', cargo='bread'))
# 汗滴 + 速度线（吃力）
A('ui', f'<path d="M{px+36} {py+18} q4 6 0 9 q-4 -3 0 -9z" fill="#9CC9E0" stroke="#5B8DB8" stroke-width="1"/>')
# 外卖车：从后方冲上（左道底部，部分出屏）
dx_, dy_ = LANE[0]-16, 420
A('vehicles', rider(dx_, dy_, 1.0, body='#F2E5E0', seat='#3b3531', shirt='#F0B642', helmet='#F0B642', box='#F0B642'))
A('ui', f'<path d="M{dx_+4} {dy_+60} v-26 M{dx_+28} {dy_+60} v-30 M{dx_+16} {dy_+62} v-20" stroke="#F4EBD0" stroke-width="2" opacity=".8" stroke-linecap="round"/>')
# 底部「！」预警
A('glow', f'<ellipse cx="{LANE[0]}" cy="532" rx="70" ry="30" fill="#FF8A4A" opacity=".75"/>')
A('ui', f'<path d="M{LANE[0]} 490 L{LANE[0]+22} 528 L{LANE[0]-22} 528 Z" fill="#F0B642" stroke="#8a4a2a" stroke-width="2.4" stroke-linejoin="round"/>')
A('text', txt(LANE[0], 524, '!', 24, '#7a3a1e'))

# ---------- 樟树（两侧行道树，大团） ----------
tr = random.Random(9)
for k, y in enumerate((-20, 115, 262, 400, 545)):
    A('trees', camphor(RL-54-(k%2)*10, y, 52+(k%3)*8, tr))
    A('trees', camphor(RR+58+(k%2)*8, y+70, 62-(k%3)*7, tr))
A('trees', camphor(60, 470, 50, tr)); A('trees', camphor(40, 110, 46, tr))
A('trees', camphor(900, 330, 44, tr, dark='#4B6B34', mid='#6E8F45', light='#9BB866', hl='#C7D98E', osm=True))
# 树影落在路上
for y in range(-20, 560, 70):
    A('shadow', f'<ellipse cx="{RL+14}" cy="{y}" rx="28" ry="40" fill="#4a4a3a" opacity=".25"/><ellipse cx="{RR-12}" cy="{y+40}" rx="26" ry="38" fill="#4a4a3a" opacity=".25"/>')
# 光斑
for _ in range(26):
    A('glow', f'<ellipse cx="{tr.uniform(RL,RR):.0f}" cy="{tr.uniform(0,H):.0f}" rx="{tr.uniform(4,12):.0f}" ry="{tr.uniform(3,7):.0f}" fill="#FFE7A8" opacity=".2"/>')

# ---------- UI ----------
A('ui', note(14, 12, 206, 84, fill='#FBF3DC', rot=-1.2))
A('ui', tape(44, 14, 38, 12, -8))
A('ui', '<path d="M30 30 l-6 11 h6 l-3 10 10 -14 h-6 l4 -7 z" fill="#F2C14E" stroke="#6b4f3a" stroke-width="1.4" stroke-linejoin="round"/>')
A('ui', battery_bar(62, 32, 41, w=112, h=20, col='#E0A33A'))
A('text', txt(184, 48, '41%', 15, '#5a3e2b', anchor='start'))
for k in range(3):
    A('ui', heart(74+k*28, 74, 1.25, empty=(k == 2)))
A('text', txt(36, 80, '血', 12, '#8a5a44'))
A('ui', woodboard(806, 12, 140, 54))
A('ui', f'<circle cx="834" cy="39" r="11" fill="#FFF8E8" stroke="#5a3e2b" stroke-width="1.6"/><path d="M834 32 V39 L839 42" stroke="#5a3e2b" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
A('text', txt(892, 47, '07:52', 20, '#FFF6E2'))
# 气泡
bxx, byy = px+44, py-44
A('ui', bubble(bxx, byy, 234, 38, px+26, py+6))
A('text', txt(bxx+117, byy+25, '又是这个大坡……电量在哭。', 14.5, '#5a3e2b'))
# 底部提示
A('ui', note(560, 494, 386, 34, fill='#FFF7E4', rot=-0.5, lines=False))
A('ui', tape(566, 497, 30, 11, -30, '#B9D3A4')); A('ui', tape(940, 497, 30, 11, 30, '#B9D3A4'))
A('ui', keycap(584, 499, 'W') + keycap(672, 499, 'S') + keycap(760, 499, 'A') + keycap(806, 499, 'D'))
A('text', txt(630, 517, '前进', 14, '#5a3e2b') + txt(656, 517, '·', 14, '#8a6a4a') + txt(718, 517, '刹车', 14, '#5a3e2b')
      + txt(744, 517, '·', 14, '#8a6a4a') + txt(795, 517, '/', 13, '#8a6a4a') + txt(868, 517, '换道', 14, '#5a3e2b'))

t = time.time()
cv = sc.build(seed=22)
save(cv, '../02-ride.png', (W, H))
print('done', time.time()-t)
