import random, math, sys, time
from wc import *
from shapes import *
W, H = 960, 540
rng = random.Random(7)
sc = Scene(W, H, S=2)
sc.layer('ground', warp=3, edge=0.35, mottle=0.14, lines=0, bleed=0.1, glaze=0.1)
sc.layer('ground2', warp=2.5, edge=0.6, mottle=0.12, lines=0.35, bleed=0.2, glaze=0.25)
sc.layer('shadow', warp=3, edge=0.2, mottle=0.2, lines=0, bleed=0.3, glaze=0.9, opacity=0.9)
sc.layer('build', warp=1.2, edge=0.5, mottle=0.1, lines=0.7, bleed=0.12, glaze=0.15)
sc.layer('build2', warp=1.0, edge=0.5, mottle=0.08, lines=0.6, bleed=0.1, glaze=0.1)
sc.layer('bikes', warp=0.7, edge=0.45, mottle=0.06, lines=0.55, bleed=0.08, glaze=0.1)
sc.layer('canopy', warp=1.5, edge=0.4, mottle=0.12, lines=0.5, bleed=0.1, glaze=0.35, opacity=0.9)
sc.layer('trees', warp=2.5, edge=0.6, mottle=0.14, lines=0.45, bleed=0.25, glaze=0.2)
sc.layer('chars', warp=0.6, edge=0.45, mottle=0.05, lines=0.8, bleed=0.08, glaze=0.05)
sc.layer('glow', blend='screen', opacity=0.8)
sc.layer('ui', warp=1.2, edge=0.5, mottle=0.08, lines=0.5, bleed=0.15, glaze=0.05)
sc.layer('text', crisp=True)
A = sc.add

# ---------- 地面 ----------
A('ground', f'<rect width="{W}" height="{H}" fill="#C9C0AA"/>')            # 水泥地
A('ground', f'<rect x="0" y="118" width="{W}" height="22" fill="#B7AE98"/>')  # 楼前台阶/散水
A('ground', f'<rect x="0" y="0" width="112" height="{H}" fill="#8DB86B"/>')  # 左侧草坪
A('ground', f'<rect x="868" y="0" width="92" height="{H}" fill="#8DB86B"/>')  # 右侧草坪
# 地砖缝
for y in range(150, 540, 34):
    A('ground2', f'<path d="M112 {y} H868" stroke="#A89F8A" stroke-width="1" opacity=".55"/>')
for x in range(112, 868, 48):
    A('ground2', f'<path d="M{x} 140 V540" stroke="#A89F8A" stroke-width="0.8" opacity=".35"/>')
# 草地斑点 / 小花
for _ in range(90):
    x = rng.choice([rng.uniform(4, 108), rng.uniform(872, 956)]); y = rng.uniform(0, 540)
    A('ground2', f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rng.uniform(4,12):.0f}" ry="{rng.uniform(2,5):.0f}" fill="{rng.choice(["#A9C77E","#76A35A","#9BC274"])}"/>')
for _ in range(26):
    x = rng.choice([rng.uniform(10, 100), rng.uniform(880, 950)]); y = rng.uniform(150, 530)
    A('ground2', f'<circle cx="{x:.0f}" cy="{y:.0f}" r="2" fill="{rng.choice(["#FFF6E0","#F2D06B","#E9A3A0"])}"/>')
# 路缘石
A('ground2', '<rect x="108" y="140" width="6" height="400" fill="#D8D0BC"/><rect x="866" y="140" width="6" height="400" fill="#D8D0BC"/>')
# 小水洼（前夜的雨）
A('ground2', '<ellipse cx="560" cy="505" rx="46" ry="12" fill="#A8C6D4" opacity=".8"/><ellipse cx="548" cy="502" rx="20" ry="4" fill="#E6F1F4" opacity=".7"/>')
# 走道箭头 / 地面标线
A('ground2', '<path d="M140 262 H840" stroke="#EDE3C8" stroke-width="3" stroke-dasharray="16 12" opacity=".8"/>')
A('ground2', '<path d="M140 386 H840" stroke="#EDE3C8" stroke-width="3" stroke-dasharray="16 12" opacity=".8"/>')

# ---------- 宿舍楼（3/4 立面，占顶部） ----------
A('build', f'<rect x="0" y="-10" width="{W}" height="130" fill="#EFE6D2"/>')    # 白瓷砖
A('build', f'<rect x="0" y="100" width="{W}" height="20" fill="#B5553C"/>')     # 一层红砖裙
for x in range(0, W, 16):
    A('build2', f'<path d="M{x} 100 V120" stroke="#8f3f2c" stroke-width="0.6" opacity=".5"/>')
A('build2', f'<path d="M0 110 H{W}" stroke="#8f3f2c" stroke-width="0.6" opacity=".5"/>')
# 瓷砖格
for y in range(-10, 100, 10):
    A('build2', f'<path d="M0 {y} H{W}" stroke="#D9CFB8" stroke-width="0.5" opacity=".6"/>')
# 阳台单元
quilts = ['#E9A3A0', '#9CC9E0', '#F2D06B', '#F7F3EA', '#B9D3A4', '#E8B98A', '#C9B6DB']
for i, x in enumerate(range(18, W, 96)):
    for row, y in enumerate([-6, 48]):
        A('build2', f'<rect x="{x}" y="{y}" width="80" height="44" fill="#8A9AA4"/>')        # 窗/阳台内
        A('build2', f'<rect x="{x+4}" y="{y+4}" width="34" height="26" fill="#B8CCD6"/><rect x="{x+42}" y="{y+4}" width="34" height="26" fill="#A9BFCB"/>')
        A('build2', f'<path d="M{x+4} {y+8} l14 -4" stroke="#fff" stroke-opacity=".6" stroke-width="2"/>')
        A('build2', f'<rect x="{x-2}" y="{y+30}" width="84" height="16" fill="#E4D9C2"/>')     # 阳台栏板
        A('build2', f'<path d="M{x} {y+6} H{x+80}" stroke="#6b5a4a" stroke-width="1"/>')      # 晾衣杆
        # 晾的被子/衣服
        k = (i*3+row) % 5
        if k in (0, 2, 3):
            q = rng.choice(quilts)
            A('build2', f'<rect x="{x+6}" y="{y+6}" width="30" height="36" fill="{q}"/>'
                        f'<path d="M{x+6} {y+18} H{x+36} M{x+6} {y+30} H{x+36}" stroke="#fff" stroke-opacity=".5" stroke-width="1.5"/>')
        if k in (1, 2, 4):
            for j in range(rng.randint(2, 3)):
                cx = x+44+j*12; col = rng.choice(['#FFFFFF', '#5B8DB8', '#C8553D', '#F2C14E', '#7FA36A', '#3b3531'])
                A('build2', f'<path d="M{cx} {y+7} l-5 3 v4 h3 v11 h10 v-11 h3 v-4 l-5 -3 q-3 3 -6 0 z" fill="{col}"/>')
        # 空调外机
        if (i+row) % 2 == 0:
            A('build2', f'<rect x="{x+58}" y="{y+32}" width="20" height="12" rx="1" fill="#F4F1E8"/><circle cx="{x+64}" cy="{y+38}" r="4" fill="none" stroke="#9a9488" stroke-width="1"/>')
        # 盆栽
        if (i+row) % 3 == 1:
            A('build2', f'<rect x="{x+10}" y="{y+26}" width="8" height="6" fill="#B5553C"/><circle cx="{x+14}" cy="{y+23}" r="6" fill="#6E9E4A"/>')
# 楼门入口
A('build2', '<rect x="436" y="78" width="88" height="42" fill="#6b5a4a"/><rect x="442" y="84" width="36" height="36" fill="#9DB4BF"/><rect x="482" y="84" width="36" height="36" fill="#9DB4BF"/>'
            '<rect x="420" y="70" width="120" height="10" fill="#D8CDB5"/>')
A('build2', '<rect x="444" y="56" width="72" height="14" rx="2" fill="#B5553C"/>')
A('text', txt(480, 67, '升华公寓 · 7栋', 10, '#FFF4DE'))
# 楼下小卖部
A('build2', '<rect x="760" y="76" width="96" height="44" fill="#D6C3A0"/><rect x="760" y="70" width="96" height="14" rx="2" fill="#3F6B3A"/>'
            '<rect x="770" y="90" width="76" height="30" fill="#8FA7A8"/>'
            '<path d="M760 84 l8 8 8 -8 8 8 8 -8 8 8 8 -8 8 8 8 -8 8 8 8 -8 8 8 8 -8" fill="#F4EBD0" stroke="#C8553D" stroke-width="1"/>')
A('text', txt(808, 81, '小卖部 · 冰饮', 9.5, '#FFF4DE'))
# 小卖部门口的冰柜与塑料凳
A('build2', '<rect x="770" y="124" width="34" height="18" rx="2" fill="#F7F3EA"/><rect x="773" y="127" width="28" height="10" fill="#BFD9E3"/>'
            '<circle cx="826" cy="132" r="7" fill="#C8553D"/><circle cx="844" cy="134" r="7" fill="#5B8DB8"/>')

# ---------- 停车区 ----------
pale = ['#F7F3EA', '#EFEDE6', '#E6EEF0', '#F2E5E0', '#E7E9DE', '#DCE3E8', '#F4F0E4', '#E9E2D2']
seats = ['#4a4440', '#5a524b', '#6d5a4c', '#3f4a52', '#7a6a5c']
rows = [150, 272, 398]          # 每排车身顶端 y
x0, dx = 128, 27.5
MY_ROW, MY_I = 1, 12
ncol = int((860-x0)/dx)
for r, ry in enumerate(rows):
    for i in range(ncol):
        if r == 2 and 17 <= i <= 19: continue    # 一个空位缺口
        x = x0+i*dx + rng.uniform(-1.5, 1.5)
        y = ry + rng.uniform(-3, 5)
        rot = rng.uniform(-6, 6)
        if r == MY_ROW and i == MY_I:
            continue
        cargo = rng.choice([None, None, None, 'leaf', 'bread'])
        A('bikes', bike(x, y, 1.0, body=rng.choice(pale), seat=rng.choice(seats), rot=rot, cargo=cargo))
        # 有些车座上放头盔 / 坐垫套
        if rng.random() < 0.18:
            A('bikes', f'<circle cx="{x+12}" cy="{y+36}" r="5.5" fill="{rng.choice(["#E86F4F","#5B8DB8","#F7F3EA","#7FA36A"])}"/>')
# 自己的车：被左右夹紧（邻车更靠近），刚被认出 → 黄色
mx, my = x0+MY_I*dx, rows[MY_ROW]+1
A('glow', f'<ellipse cx="{mx+12}" cy="{my+24}" rx="20" ry="32" fill="#FFD66B" opacity=".45"/>')
A('ui', f'<ellipse cx="{mx+12}" cy="{my+24}" rx="19" ry="31" fill="none" stroke="#E8A93A" stroke-width="2.2" stroke-dasharray="5 4"/>')
# 邻车挤近（再画一遍稍偏向自己）
A('bikes', bike(mx-20, my+2, 1.0, body='#EFEDE6', seat='#4a4440', rot=5))
A('bikes', bike(mx+20, my+1, 1.0, body='#E6EEF0', seat='#3f4a52', rot=-6))
A('bikes', bike(mx, my, 1.0, body='#F2C14E', seat='#C8553D', rot=0, cargo='bread'))

# 认出标记：闪光 + 小星
for (sx, sy, rr) in [(mx-6, my-8, 5), (mx+30, my+4, 4), (mx+28, my+48, 3.5)]:
    A('ui', f'<path d="M{sx} {sy-rr*1.6} L{sx+rr*0.4} {sy-rr*0.4} L{sx+rr*1.6} {sy} L{sx+rr*0.4} {sy+rr*0.4} L{sx} {sy+rr*1.6} L{sx-rr*0.4} {sy+rr*0.4} L{sx-rr*1.6} {sy} L{sx-rr*0.4} {sy-rr*0.4} Z" fill="#FFE08A" stroke="#C98A2B" stroke-width="1"/>')

# 雨棚：地面投影 + 后梁/立柱（顶棚本身不遮车）
for ry in rows:
    A('shadow', f'<rect x="118" y="{ry-10}" width="744" height="66" rx="6" fill="#8a7f68" opacity=".32"/>')
    A('canopy', f'<rect x="116" y="{ry-12}" width="748" height="5" rx="2" fill="#6E9E8E"/>')
    for x in range(118, 870, 93):
        A('canopy', f'<rect x="{x-3}" y="{ry-14}" width="7" height="9" rx="1.5" fill="#5f4a38"/>')
# 树影斑驳（komorebi）：左右树冠投下的影与光斑
sh = random.Random(5)
for (cx, cy, r) in [(150, 200, 70), (130, 360, 60), (150, 500, 70), (860, 280, 60), (850, 470, 70)]:
    for _ in range(7):
        A('shadow', f'<circle cx="{cx+sh.uniform(-r,r):.0f}" cy="{cy+sh.uniform(-r,r)*0.8:.0f}" r="{sh.uniform(r*0.3,r*0.55):.0f}" fill="#6f7d5a" opacity=".22"/>')
for _ in range(30):
    x = sh.uniform(120, 860); y = sh.uniform(140, 540)
    A('glow', f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{sh.uniform(5,14):.0f}" ry="{sh.uniform(3,8):.0f}" fill="#FFE7A8" opacity=".22"/>')
# 地上的落叶
for _ in range(60):
    x = sh.uniform(115, 865); y = sh.uniform(140, 540)
    A('ground2', f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="3" ry="1.6" fill="{sh.choice(["#C9853F","#A5703A","#8DB86B","#D9A650"])}" transform="rotate({sh.uniform(0,180):.0f} {x:.0f} {y:.0f})"/>')
# 车棚尽头的充电桩（白天不亮）
for k in range(3):
    A('bikes', f'<rect x="{826+k*0}" y="{408+k*0}" width="0" height="0"/>')

# ---------- 树 ----------
tr = random.Random(3)
for (cx, cy, r) in [(40, 190, 56), (70, 330, 50), (30, 470, 58), (90, 120, 34)]:
    A('trees', camphor(cx, cy, r, tr))
A('trees', camphor(915, 250, 50, tr, dark='#4B6B34', mid='#6E8F45', light='#9BB866', hl='#C7D98E', osm=True))   # 桂花树
A('trees', camphor(925, 440, 52, tr))
# 飘落的桂花
for _ in range(40):
    A('trees', f'<circle cx="{tr.uniform(860,960):.0f}" cy="{tr.uniform(200,540):.0f}" r="1.3" fill="#F0B642"/>')

# ---------- 人物 / 猫 ----------
# 主角：在走道里，站在自己车前
px, py = mx-8, 222
A('chars', walker(px, py, 1.35, shirt='#E86F4F', hair='#3a2a22', dirx=2, bag='#F2C14E', pants='#4F6480'))
# 猫：趴在一辆车的座垫上
cx_, cy_ = x0+4*dx+12, rows[2]+34
A('chars', f'<ellipse cx="{cx_}" cy="{cy_}" rx="9" ry="7" fill="#E39B52"/><circle cx="{cx_}" cy="{cy_-8}" r="5.2" fill="#E39B52"/>'
           f'<path d="M{cx_-5} {cy_-11} l1 -5 3 3 z M{cx_+5} {cy_-11} l-1 -5 -3 3 z" fill="#E39B52"/>'
           f'<path d="M{cx_-6} {cy_-2} q6 3 12 0 M{cx_-7} {cy_+2} q7 3 14 0" stroke="#B8682E" stroke-width="1.4" fill="none"/>'
           f'<path d="M{cx_+8} {cy_+3} q10 2 8 -8" stroke="#E39B52" stroke-width="3" fill="none" stroke-linecap="round"/>')
# 另一个同学在远处找车
A('chars', walker(610, 350, 1.1, shirt='#9CC9E0', hair='#2b2320', dirx=1, step=2, bag='#C8553D'))

# 车把上搭着的雨衣 / 快递箱 / 共享单车
A('bikes', f'<path d="M{x0+7*dx+2} {rows[0]+12} q10 10 22 0 l-2 14 q-9 5 -18 0 z" fill="#7FB0C8" opacity=".9"/>')
A('bikes', '<rect x="640" y="470" width="30" height="22" rx="2" fill="#C9A06A"/><path d="M640 481 H670 M655 470 V492" stroke="#8a6a44" stroke-width="1.4"/>')
A('text', txt(655, 486, '快递', 7, '#5a3e2b'))
A('bikes', '<g transform="translate(700 470) rotate(-70)"><rect x="-4" y="0" width="8" height="40" rx="3" fill="#E6C75A"/><circle cx="0" cy="3" r="5" fill="none" stroke="#3b3531" stroke-width="2"/><circle cx="0" cy="37" r="5" fill="none" stroke="#3b3531" stroke-width="2"/></g>')
# ---------- UI ----------
# 左上：手账便签 电量
A('ui', note(14, 12, 196, 58, fill='#FBF3DC', rot=-1.2))
A('ui', tape(40, 14, 38, 12, -8))
A('ui', battery_bar(62, 34, 62, w=112, h=20))
A('ui', '<path d="M30 30 l-6 11 h6 l-3 10 10 -14 h-6 l4 -7 z" fill="#F2C14E" stroke="#6b4f3a" stroke-width="1.4" stroke-linejoin="round"/>')
A('text', txt(118, 30, '电量', 11, '#8a6a4a'))
A('text', txt(192, 50, '62%', 15, '#5a3e2b', anchor='start', extra='transform="translate(-8 0)"'))
# 右上：木牌 时钟 + 信号格
A('ui', woodboard(790, 12, 156, 54))
A('ui', signal(804, 52, 4, 3, '#7FB35A'))
A('ui', f'<circle cx="857" cy="39" r="11" fill="#FFF8E8" stroke="#5a3e2b" stroke-width="1.6"/><path d="M857 32 V39 L862 42" stroke="#5a3e2b" stroke-width="1.8" fill="none" stroke-linecap="round"/>')
A('text', txt(906, 47, '07:38', 20, '#FFF6E2', family=SANS))
A('text', txt(818, 62, '滴滴·近了', 8.5, '#FFE9B8'))
# 气泡
bx, by = px-150, py-50
A('ui', bubble(bx, by, 190, 38, px+8, py+8))
A('text', txt(bx+95, by+25, '终于找到你了！', 16, '#5a3e2b'))
# 底部操作提示：便签条
A('ui', note(330, 494, 300, 34, fill='#FFF7E4', rot=0.6, lines=False))
A('ui', tape(336, 498, 30, 11, -30, '#B9D3A4')); A('ui', tape(624, 498, 30, 11, 30, '#B9D3A4'))
A('ui', keycap(372, 499, 'F')+keycap(488, 499, 'E'))
A('text', txt(424, 517, '查看', 15, '#5a3e2b') + txt(466, 517, '·', 15, '#8a6a4a') + txt(540, 517, '背包', 15, '#5a3e2b'))

t = time.time()
cv = sc.build(seed=11)
save(cv, '../01-findcar.png', (W, H))
print('done', time.time()-t)
