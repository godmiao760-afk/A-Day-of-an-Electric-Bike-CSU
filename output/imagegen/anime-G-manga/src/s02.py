from lib import *
random.seed(21)
b=''
RL,RR=300,660   # 路面
LW=(RR-RL)/3
lane=lambda i: RL+LW*(i+0.5)
# 两侧人行道 + 草地
b+=f'<rect x="0" y="0" width="{RL-36}" height="540" fill="url(#t10)"/>'
b+=f'<rect x="{RR+36}" y="0" width="{960-RR-36}" height="540" fill="url(#t10)"/>'
for x0 in (RL-36,RR):
    b+=f'<rect x="{x0}" y="0" width="36" height="540" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    for yy in range(0,540,18): b+=f'<line x1="{x0}" y1="{yy}" x2="{x0+36}" y2="{yy}" stroke="{INK}" stroke-width="0.8"/>'
    b+=f'<line x1="{x0+18}" y1="0" x2="{x0+18}" y2="540" stroke="{INK}" stroke-width="0.5"/>'
# 路面
b+=f'<rect x="{RL}" y="0" width="{RR-RL}" height="540" fill="{PAPER}"/>'
# 坡道区（交叉斜线网点）y 60~260
b+=f'<rect x="{RL}" y="40" width="{RR-RL}" height="230" fill="url(#hx)"/>'
b+=f'<rect x="{RL}" y="40" width="{RR-RL}" height="230" fill="none" stroke="{INK}" stroke-width="0"/>'
for yy in (40,270): b+=f'<line x1="{RL}" y1="{yy}" x2="{RR}" y2="{yy}" stroke="{INK}" stroke-width="3"/>'
# 坡道横纹（防滑条）
for yy in range(56,262,22): b+=f'<line x1="{RL+6}" y1="{yy}" x2="{RR-6}" y2="{yy}" stroke="{INK}" stroke-width="1.8"/>'
# 路边石
b+=f'<line x1="{RL}" y1="0" x2="{RL}" y2="540" stroke="{INK}" stroke-width="3.5"/><line x1="{RR}" y1="0" x2="{RR}" y2="540" stroke="{INK}" stroke-width="3.5"/>'
# 车道虚线
for i in (1,2):
    x=RL+LW*i
    for yy in range(-10,540,40): b+=f'<rect x="{x-2}" y="{yy}" width="4" height="22" fill="{INK}"/>'
# 路面碎点
for k in range(160):
    x=random.uniform(RL+4,RR-4); y=random.uniform(272,540)
    b+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{random.uniform(.5,1.2):.1f}" fill="{INK}"/>'
# 上坡 地面字 + 箭头
b+=f'<rect x="{lane(0)-40}" y="274" width="80" height="38" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
b+=T(lane(0),302,'上坡',22,anchor='middle',family=SERIF)
b+=f'<path d="M{lane(2)-10},312 v-20 h-10 l20,-16 l20,16 h-10 v20z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
# 斑马线（行人横穿）y 440
b+=''
for k in range(9): b+=f'<rect x="{RL+10+k*40}" y="318" width="22" height="42" fill="{PAPER}" stroke="{INK}" stroke-width="1.6"/>'
b+=f'<rect x="{RL}" y="424" width="{RR-RL}" height="50" fill="none"/>'
# 樟树两侧
for i,(x,y,r) in enumerate([(120,40,76),(210,170,62),(90,300,80),(200,440,66),(60,520,50),(850,60,80),(760,200,58),(880,330,76),(770,470,64)]):
    b+=canopy(x,y,r,seed=40+i)
# 岳麓山远景切入格（左上下方）
mx,my,mw,mh=22,110,210,92
b+=f'<g transform="rotate(-2 {mx+mw/2} {my+mh/2})">'+frame(mx,my,mw,mh)
b+=f'<clipPath id="mt"><rect x="{mx}" y="{my}" width="{mw}" height="{mh}"/></clipPath><g clip-path="url(#mt)">'
b+=f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" fill="url(#t10)"/>'
b+=f'<path d="M{mx},{my+60} L{mx+40},{my+38} L{mx+70},{my+46} L{mx+110},{my+22} L{mx+150},{my+40} L{mx+190},{my+30} L{mx+mw},{my+44} V{my+mh} H{mx}Z" fill="url(#t50)" stroke="{INK}" stroke-width="2"/>'
b+=f'<path d="M{mx},{my+mh} L{mx+mw*0.42},{my+56} L{mx+mw*0.58},{my+56} L{mx+mw},{my+mh}Z" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
b+=f'<line x1="{mx+mw/2}" y1="{my+60}" x2="{mx+mw/2}" y2="{my+mh}" stroke="{INK}" stroke-width="1.5" stroke-dasharray="5 4"/>'
b+='</g>'
b+=T(mx+10,my+20,'前方：麓山大坡',13,outline=PAPER,ow=4)
b+='</g>'
# ===== 车辆（1.5×）=====
K=1.5
def put(g,x,y,w,h,k=K,flip=False):
    tx=x-w*k/2; ty=y-h*k/2
    if flip:
        return f'<g transform="translate({tx},{ty+h*k}) scale({k},{-k})">{g}</g>'
    return f'<g transform="translate({tx},{ty}) scale({k})">{g}</g>'
# 校车：左车道上坡中
b+=f'<ellipse cx="{lane(0)+6}" cy="{150}" rx="{50}" ry="{110}" fill="url(#h)" opacity=".6"/>'
b+=put(bus(),lane(0),138,64,140,1.35)
b+=vlines(lane(0)-36,lane(0)+36,236,290,n=8,seed=3,w=2)
# 逆行车：右车道迎面（翻转）
wx,wy=lane(2),150
b+=put(wrongway(),wx,wy,32,56,K,flip=True)
b+=vlines(wx-22,wx+22,70,110,n=7,seed=8,w=2)
b+=T(wx+56,wy-14,'逆行！',20,family=SERIF,outline=PAPER,ow=6,rot=10)
b+=sweat(wx+26,wy+18,.8)
# 行人横穿（斑马线）
for k,x in enumerate([lane(2)+30,lane(2)-12]):
    b+=f'<g transform="translate({x-21},{339-21}) scale(1.5) rotate(-90 14 14)">{walker(14,14,bag=(k==0))}</g>'
b+=f'<path d="M{lane(2)-44},339 h-30 m9,-8 l-9,8 l9,8" stroke="{INK}" stroke-width="3" fill="none"/>'
b+=T(lane(2)+60,312,'哒哒哒',14,family=SERIF,anchor='middle',outline=PAPER,ow=5,rot=-6)
# 主角：中车道
px,py=lane(1),408
b+=vlines(px-24,px+24,py+44,py+92,n=9,seed=11,w=2.2)
b+=f'<ellipse cx="{px+4}" cy="{py+6}" rx="22" ry="38" fill="url(#t50)" opacity=".7"/>'
b+=put(rider('yellow'),px,py,32,56,K)
b+=sweat(px+28,py-40,1)
b+=sweat(px+38,py-26,.7)
# 气泡（放在左侧樟树上方，尾巴指向主角）
b+=bubble(196,352,180,60,'',(px-22,py-14),size=17,lines=['又是这个大坡……','电量在哭。'],side='right')
bx,by=206,330
b+=f'<rect x="{bx}" y="{by}" width="34" height="20" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><rect x="{bx+34}" y="{by+6}" width="4" height="8" fill="{INK}"/><rect x="{bx+2}" y="{by+2}" width="8" height="16" fill="{Y}"/>'
b+=f'<path d="M{bx+12},{by+8} l4,0 M{bx+22},{by+8} l4,0" stroke="{INK}" stroke-width="1.6"/><path d="M{bx+15},{by+16} q4,-4 8,0" stroke="{INK}" stroke-width="1.4" fill="none"/>'
b+=f'<path d="M{bx+14},{by+10} q-1,6 1,8 M{bx+25},{by+10} q1,6 -1,8" stroke="{INK}" stroke-width="1.2" fill="none"/>'
# 外卖车：右车道后方冲上
dx,dy=lane(2),470
b+=f'<clipPath id="bot"><rect x="{RL+LW*2}" y="380" width="{LW}" height="120"/></clipPath>'
b+=f'<rect x="{RL+LW*2+2}" y="380" width="{LW-4}" height="120" fill="{PAPER}"/>'
b+=f'<g clip-path="url(#bot)">'+burst_lines(dx,dy+10,44,200,n=36,seed=5,w=2.2)+'</g>'
b+=put(delivery(),dx,dy,32,56,K)
b+=f'<g transform="translate({dx+44},{410})">'+spiky(0,0,24,22,n=12,seed=4,fill=Y,sw=2.5,jag=.35)+T(0,11,'！',28,anchor='middle',family=SERIF)+'</g>'
b+=T(dx-64,488,'嗖——',22,family=SERIF,outline=PAPER,ow=6,rot=-6,anchor='middle')
# HUD
b+=battery_hud(38,hp=2)
b+=clock_hud('07:52')
# 坡道耗电提示
b+=f'<g transform="translate(270,14)">'+frame(0,0,112,30)+T(56,21,'坡道 耗电×2',13,anchor='middle')+'</g>'
b+=hint_bar([(['W'],'前进'),(['S'],'刹车'),(['A','D'],'换道')])
render(svg(960,540,b),'02-ride.png')
