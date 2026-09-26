import random, time
import numpy as np
from PIL import Image
from wc import *
from shapes import *
BG = (0.957, 0.922, 0.816)
# 1) 在 4 倍分辨率上画出所有精灵（逻辑坐标 = 游戏像素），水彩化后缩回 1×
SW, SH = 420, 72
sc = Scene(SW, SH, S=4, bg=BG)
sc.layer('tiles', warp=0.5, edge=0.45, mottle=0.14, lines=0.25, bleed=0.08, glaze=0.1, edge_r=1.2)
sc.layer('spr', warp=0.25, edge=0.45, mottle=0.06, lines=0.85, bleed=0.05, glaze=0.05, edge_r=1.0)
A = sc.add
POS = {}
def place(name, x, y, w, h): POS[name] = (x, y, w, h)
x = 4
place('rider', x, 8, 32, 56); A('spr', rider(x, 8, 1.0, body='#F2C14E', seat='#C8553D', shirt='#E86F4F', helmet='#F4EBD0', bag='#F2C14E')); x += 44
place('bike', x, 12, 24, 48); A('spr', bike(x, 12, 1.0, body='#F2C14E', seat='#C8553D', cargo='bread')); x += 34
place('bike_other', x, 12, 24, 48); A('spr', bike(x, 12, 1.0, body='#EFEDE6', seat='#4a4440')); x += 34
place('npc_delivery', x, 8, 32, 56); A('spr', rider(x, 8, 1.0, body='#F2E5E0', seat='#3b3531', shirt='#F0B642', helmet='#F0B642', box='#F0B642')); x += 44
# 充电桩 32x40（3/4 俯视）
px = x; place('pile', px, 16, 32, 40)
A('spr', f'<g transform="translate({px} 16)"><ellipse cx="17" cy="37" rx="15" ry="3" fill="#3a2e22" opacity=".25"/>'
         '<rect x="3" y="2" width="26" height="35" rx="4" fill="#E8EEF0"/><rect x="3" y="2" width="26" height="7" rx="3.5" fill="#C7D3D8"/>'
         '<rect x="7" y="11" width="18" height="10" rx="2" fill="#2f3a40"/><rect x="9" y="13" width="14" height="6" rx="1" fill="#8BE07A"/>'
         '<rect x="11" y="24" width="10" height="8" rx="1.5" fill="#fff" stroke="#6b7a80" stroke-width="0.8"/>'
         '<path d="M13 26 h2 v2 h-2z M17 26 h2 v2 h-2z M13 30 h6" stroke="#3b3531" stroke-width=".8"/>'
         '<rect x="3" y="33" width="26" height="4" rx="2" fill="#9CB0B8"/><path d="M28 18 q4 6 -1 12" stroke="#3b3531" stroke-width="1.6" fill="none"/></g>')
x += 42
# 地砖 64x64
place('road', x, 4, 64, 64)
A('tiles', f'<rect x="{x}" y="4" width="64" height="64" fill="#8F8A80"/>'
           f'<path d="M{x+32} 4 v24 M{x+32} 44 v24" stroke="#F4EBD0" stroke-width="3"/>'
           f'<circle cx="{x+12}" cy="20" r="1.2" fill="#6f6a62"/><circle cx="{x+50}" cy="52" r="1.4" fill="#a39e94"/><path d="M{x+8} 50 l6 -3 5 3" stroke="#6f6a62" stroke-width="0.8" fill="none"/>')
x += 72
place('grass', x, 4, 64, 64)
gr = random.Random(4)
g = f'<rect x="{x}" y="4" width="64" height="64" fill="#8DB86B"/>'
for _ in range(14):
    gx = x+gr.uniform(4, 60); gy = 4+gr.uniform(4, 60)
    g += f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{gr.uniform(3,7):.1f}" ry="{gr.uniform(1.5,3):.1f}" fill="{gr.choice(["#A9C77E","#76A35A","#9BC274"])}"/>'
for _ in range(5):
    g += f'<path d="M{x+gr.uniform(6,58):.1f} {4+gr.uniform(8,60):.1f} l-2 -4 m2 4 l0 -5 m0 5 l2 -4" stroke="#5E8C4A" stroke-width="1" fill="none"/>'
g += f'<circle cx="{x+20}" cy="46" r="1.6" fill="#FFF6E0"/><circle cx="{x+46}" cy="18" r="1.6" fill="#F2D06B"/>'
A('tiles', g)
x += 72
SPR = sc.build(seed=44, paper_strength=0.0)
spr1 = Image.fromarray((np.clip(SPR, 0, 1)*255+.5).astype(np.uint8)).resize((SW, SH), Image.LANCZOS)
spr_hi = Image.fromarray((np.clip(SPR, 0, 1)*255+.5).astype(np.uint8))
print('sprites', x)

# 2) 预览板背景（纸 + 手账标题）
W, H = 960, 420
bs = Scene(W, H, S=2, bg=BG)
bs.layer('ui', warp=1.2, edge=0.5, mottle=0.08, lines=0.5, bleed=0.15, glaze=0.05)
bs.layer('text', crisp=True)
B = bs.add
B('ui', tape(120, 26, 60, 16, -5, '#B9D3A4'))
B('text', txt(24, 36, '04 · 实际尺寸精灵预览', 20, '#5a3e2b', anchor='start', family=SERIF))
B('text', txt(936, 36, '上排 1×（游戏里真实像素）· 下排 4×（1× 像素最近邻放大，看能否辨认）', 12, '#8a6a4a', anchor='end'))
B('ui', '<path d="M24 50 H936" stroke="#b9a27e" stroke-width="1.5" stroke-dasharray="4 4"/>')
names = ['rider', 'bike', 'bike_other', 'npc_delivery', 'pile', 'road', 'grass']
labels = {'rider': 'rider 32×56', 'bike': 'bike 24×48（黄）', 'bike_other': 'bike_other 24×48', 'npc_delivery': 'npc_delivery 32×56',
          'pile': 'pile 32×40', 'road': 'road 64×64', 'grass': 'grass 64×64'}
# 4× 列宽
colx = []; cx = 24
for n in names:
    w = POS[n][2]*4 if n not in ('road', 'grass') else 64*2   # 地砖 2× 以免撑破版面（另注明）
    colx.append(cx); cx += w + 12
BGIMG = bs.build(seed=5, paper_strength=0.8)
board = Image.fromarray((np.clip(BGIMG, 0, 1)*255+.5).astype(np.uint8)).resize((W, H), Image.LANCZOS)
# 3) 贴 1× 行、4× 行 + 标注
from PIL import ImageDraw, ImageFont
font = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 12, index=2)
fontS = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 11, index=2)
d = ImageDraw.Draw(board)
Y1, Y4 = 66, 150
d.text((24, Y1-2), '1×', font=font, fill=(138, 106, 74))
for n, cx in zip(names, colx):
    x0, y0, w, h = POS[n]
    tile = spr1.crop((x0, y0, x0+w, y0+h))
    board.paste(tile, (cx+30, Y1+4))
    k = 4 if n not in ('road', 'grass') else 2
    big = tile.resize((w*k, h*k), Image.NEAREST)
    board.paste(big, (cx, Y4))
    d.rectangle((cx-1, Y4-1, cx+w*k, Y4+h*k), outline=(185, 162, 126))
    d.text((cx, Y4+h*k+6), labels[n], font=font, fill=(90, 62, 43))
    d.text((cx, Y4+h*k+22), f'下图 {k}×', font=fontS, fill=(138, 106, 74))
# 4) 实际游戏密度小样：1× 的车阵 + 骑手（直接在 1× 贴）
d.text((24, Y1+62), '', font=font)
save_path = '../04-sprites.png'
board.save(save_path)
spr_hi.save('sprites_hi.png')
print('ok', board.size)
