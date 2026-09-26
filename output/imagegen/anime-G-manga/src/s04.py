from lib import *
from PIL import Image
rows=[[('rider',32,56,rider()),('bike',24,48,bike('own')),('bike_other',24,48,bike('other')),('npc_delivery',32,56,delivery()),('pile',32,40,pile('on'))],
      [('road',64,64,road_tile()),('grass',64,64,grass_tile()),('npc_wrong',32,56,wrongway()),('player',32,32,player())]]
W=1220
b=f'<rect x="0" y="0" width="{W}" height="54" fill="{INK}"/>'
b+=T(24,37,'04 · 实际尺寸精灵预览',24,fill=PAPER)
b+=T(318,36,'G · 日漫网点风 — 左 1×（游戏真实像素）/ 右 4×（最近邻放大）',15,fill=PAPER,weight='400')
b+=f'<rect x="{W-140}" y="14" width="26" height="26" fill="{Y}" stroke="{PAPER}" stroke-width="2"/>'+T(W-106,34,'#FFCC00',15,fill=PAPER)
POS=[]; y=72
for row in rows:
    x=26; mh=max(h for _,_,h,_ in row)
    ch=mh*4+76
    for name,w,h,g in row:
        colw=w*4+w+44
        b+=f'<rect x="{x-10}" y="{y}" width="{colw}" height="{ch}" fill="none" stroke="{INK}" stroke-width="2"/>'
        b+=f'<rect x="{x-10}" y="{y}" width="{colw}" height="28" fill="{INK}"/>'
        b+=T(x-2,y+20,name,14,fill=PAPER,family='Noto Sans Mono CJK SC')
        b+=T(x+colw-18,y+20,f'{w}×{h}',12,fill=Y,anchor='end',family='Noto Sans Mono CJK SC',weight='400')
        gy=y+42
        b+=f'<g transform="translate({x},{gy})">{g}</g>'
        b+=T(x+w/2,gy+h+16,'1×',12,anchor='middle',weight='400')
        px=x+w+20
        b+=f'<rect x="{px-1}" y="{gy-1}" width="{w*4+2}" height="{h*4+2}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 3"/>'
        b+=T(px+w*2,gy+h*4+20,'4×',12,anchor='middle',weight='400')
        POS.append((name,w,h,g,(px,gy)))
        x+=colw+12
    y+=ch+14
H=y+40
b+=T(26,H-16,'读图结论：1× 下黄色主角车在灰网点中一眼可辨；网点在 32px 内只剩 2~3 个点，灰阶靠"点密度"而非颜色，缩小后仍成立。',13,weight='400')
render(svg(W,H,b),'04-sprites.png')
base=Image.open(OUT+'04-sprites.png').convert('RGB')
for name,w,h,g,(px,py) in POS:
    tmp=f'/tmp/g/sp_{name}.png'
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">{defs()}{g}</svg>'
    cairosvg.svg2png(bytestring=s.encode(),write_to=tmp)
    im=Image.open(tmp).convert('RGBA')
    big=im.resize((w*4,h*4),Image.NEAREST)
    bg=Image.new('RGBA',big.size,(245,241,230,255)); bg.alpha_composite(big)
    base.paste(bg.convert('RGB'),(int(px),int(py)))
base.save(OUT+'04-sprites.png'); print(W,H)
