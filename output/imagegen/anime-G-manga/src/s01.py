from lib import *
random.seed(11)
b=''
# 远景：岳麓山（网点剪影）
b+=f'<path d="M0,44 L60,30 L120,36 L200,14 L250,22 L300,8 L360,20 L430,12 L520,28 L600,18 L680,30 L760,16 L840,26 L960,20 L960,60 L0,60Z" fill="url(#t10)" stroke="{INK}" stroke-width="1.6"/>'
b+=f'<path d="M270,20 q10,6 20,2 M400,18 q15,8 30,0 M720,26 q12,5 24,0" stroke="{INK}" stroke-width="1" fill="none"/>'
b+=T(470,24,'岳麓山',10,weight='400',anchor='middle')
# 宿舍楼立面（3/4）
bx0,bx1,by0,by1=40,920,34,160
b+=f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" fill="{PAPER}" stroke="{INK}" stroke-width="3"/>'
b+=f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="8" fill="url(#t50)" stroke="{INK}" stroke-width="2"/>'
# 瓷砖网格
for yy in range(by0+10,by1,6): b+=f'<line x1="{bx0}" y1="{yy}" x2="{bx1}" y2="{yy}" stroke="{INK}" stroke-width="0.3"/>'
for fl,fy in enumerate((48,98)):
    for i in range(14):
        wx=bx0+22+i*62
        if 400<wx<520 and fl==1: continue
        # 阳台
        b+=f'<rect x="{wx}" y="{fy}" width="46" height="40" fill="url(#t80)" stroke="{INK}" stroke-width="1.6"/>'
        b+=f'<line x1="{wx+23}" y1="{fy}" x2="{wx+23}" y2="{fy+40}" stroke="{PAPER}" stroke-width="1"/>'
        b+=f'<rect x="{wx-3}" y="{fy+24}" width="52" height="16" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/>'
        for k in range(8): b+=f'<line x1="{wx+2+k*6}" y1="{fy+24}" x2="{wx+2+k*6}" y2="{fy+40}" stroke="{INK}" stroke-width="0.8"/>'
        # 晾衣
        b+=f'<line x1="{wx+2}" y1="{fy+4}" x2="{wx+44}" y2="{fy+4}" stroke="{PAPER}" stroke-width="1"/>'
        for c in range(random.randint(1,3)):
            cx=wx+6+c*13+random.randint(0,3)
            kind=random.choice(['shirt','pants','towel'])
            if kind=='shirt': b+=f'<path d="M{cx},{fy+4} l-4,3 l2,2 l1,-1 v9 h8 v-9 l1,1 l2,-2 l-4,-3 z" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>'
            elif kind=='pants': b+=f'<path d="M{cx},{fy+4} h8 l1,14 h-3 l-2,-9 l-2,9 h-3z" fill="url(#t30)" stroke="{INK}" stroke-width="0.9"/>'
            else: b+=f'<rect x="{cx}" y="{fy+4}" width="7" height="13" fill="url(#hv)" stroke="{INK}" stroke-width="0.9"/>'
        # 空调外机
        if random.random()<.55:
            ax=wx+48 if i<13 else wx-16
            b+=f'<rect x="{wx+47}" y="{fy+10}" width="12" height="10" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/><circle cx="{wx+53}" cy="{fy+15}" r="3" fill="none" stroke="{INK}" stroke-width="0.9"/>'
# 楼门
b+=f'<rect x="440" y="100" width="80" height="60" fill="url(#t80)" stroke="{INK}" stroke-width="2.5"/><rect x="430" y="92" width="100" height="12" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
b+=T(480,102,'十二舍',10,anchor='middle')
b+=f'<line x1="480" y1="104" x2="480" y2="160" stroke="{PAPER}" stroke-width="1.5"/>'
# 地面
b+=f'<rect x="0" y="160" width="960" height="340" fill="{PAPER}"/>'
b+=f'<line x1="0" y1="161" x2="960" y2="161" stroke="{INK}" stroke-width="3"/>'
# 地砖细线
for yy in range(236,300,16): b+=f'<line x1="90" y1="{yy}" x2="880" y2="{yy}" stroke="{INK}" stroke-width="0.4" stroke-dasharray="1 5"/>'
for yy in range(420,500,16): b+=f'<line x1="0" y1="{yy}" x2="960" y2="{yy}" stroke="{INK}" stroke-width="0.4" stroke-dasharray="1 5"/>'
# 车棚雨棚投影（斜线网点带）
b+=f'<rect x="84" y="164" width="800" height="72" fill="url(#h)" opacity="0.45"/>'
b+=f'<rect x="84" y="296" width="800" height="120" fill="url(#h)" opacity="0.35"/>'

S=1.2
OWN=(12,1)
def bikeat(x,y,kind,rot=0,mark=None):
    g=f'<g transform="translate({x},{y}) rotate({rot} 14 29) scale({S})">{bike(kind)}</g>'
    return g
rows=[(170,0),(300,1),(358,2)]
bikes=''
own_xy=None
for yrow,ri in rows:
    for i in range(24):
        x=98+i*32+random.uniform(-2,2); y=yrow+random.uniform(-3,3)
        rot=random.uniform(-5,5)
        if (i,ri)==OWN:
            own_xy=(x,y); rot=0
            continue
        if random.random()<0.06 and ri==0: continue
        bikes+=bikeat(x,y,'other',rot)
        # 车座上的头盔/车罩
        r=random.random()
        if r<.18: bikes+=f'<circle cx="{x+14.4}" cy="{y+38}" r="6" fill="{PAPER}" stroke="{INK}" stroke-width="1.4"/><path d="M{x+10},{y+36} q4,-4 9,0" stroke="{INK}" stroke-width="1.5" fill="none"/>'
        elif r<.28: bikes+=f'<rect x="{x+6}" y="{y+22}" width="17" height="28" rx="7" fill="url(#t50)" stroke="{INK}" stroke-width="1.3"/>'
        elif r<.36: bikes+=f'<rect x="{x+7}" y="{y+2}" width="15" height="9" fill="url(#hx)" stroke="{INK}" stroke-width="1.2"/>'
        # 查过不是的：× 记号
        if (ri==1 and i in (6,8,9,17)) or (ri==0 and i in (10,11,15)):
            bikes+=f'<path d="M{x+6},{y+22} l16,16 M{x+22},{y+22} l-16,16" stroke="{INK}" stroke-width="3" stroke-linecap="round"/>'
b+=bikes
# 雨棚钢架：柱子 + 桁架
for yy in (166,298):
    b+=f'<line x1="84" y1="{yy}" x2="884" y2="{yy}" stroke="{INK}" stroke-width="3.2"/><line x1="84" y1="{yy+5}" x2="884" y2="{yy+5}" stroke="{INK}" stroke-width="1.2"/>'
    for k in range(20): b+=f'<line x1="{84+k*40}" y1="{yy}" x2="{104+k*40}" y2="{yy+5}" stroke="{INK}" stroke-width="1"/><line x1="{104+k*40}" y1="{yy+5}" x2="{124+k*40}" y2="{yy}" stroke="{INK}" stroke-width="1"/>'
for xx in range(84,900,160):
    for yy in (166,298,414):
        b+=f'<rect x="{xx-5}" y="{yy-5}" width="10" height="10" fill="{INK}"/><rect x="{xx-2}" y="{yy-2}" width="4" height="4" fill="{PAPER}"/>'
    b+=f'<line x1="{xx}" y1="298" x2="{xx}" y2="414" stroke="{INK}" stroke-width="1.2" stroke-dasharray="6 3"/>'
b+=f'<line x1="84" y1="414" x2="884" y2="414" stroke="{INK}" stroke-width="3.2"/>'
# 主角的车 + 集中效果线
ox,oy=own_xy
cx,cy=ox+14.4,oy+29
b+=f'<clipPath id="lot"><rect x="84" y="170" width="800" height="244"/></clipPath><g clip-path="url(#lot)">'+burst_lines(cx,cy,64,300,n=64,seed=9,w=2.4)+'</g>'
# 被夹住的两辆邻车（重画盖住效果线）
for dx in (-32,32):
    b+=bikeat(ox+dx,oy+random.uniform(-1,1),'other',dx/12)
b+=f'<ellipse cx="{cx}" cy="{cy}" rx="22" ry="38" fill="{Y}" stroke="{INK}" stroke-width="2.5"/><ellipse cx="{cx}" cy="{cy}" rx="27" ry="43" fill="none" stroke="{INK}" stroke-width="1.2" stroke-dasharray="4 3"/>'+f'<g transform="translate({ox},{oy}) scale({S})">{bike("own")}</g>'
# 闪光
def star(x,y,r):
    return f'<path d="M{x},{y-r} Q{x+r*.15},{y-r*.15} {x+r},{y} Q{x+r*.15},{y+r*.15} {x},{y+r} Q{x-r*.15},{y+r*.15} {x-r},{y} Q{x-r*.15},{y-r*.15} {x},{y-r}Z" fill="{Y}" stroke="{INK}" stroke-width="1.5"/>'
b+=star(cx+22,oy+4,8)+star(cx-24,oy+50,6)
# 夹住箭头
b+=f'<path d="M{ox-40},{oy+30} l12,0 m-5,-5 l5,5 l-5,5" stroke="{INK}" stroke-width="3" fill="none"/><path d="M{ox+68},{oy+30} l-12,0 m5,-5 l-5,5 l5,5" stroke="{INK}" stroke-width="3" fill="none"/>'
# 拟声词 滴滴！
b+=T(cx+60,oy-12,'滴',46,family=SERIF,weight='700',outline=PAPER,ow=8,rot=-12,fill=INK)
b+=T(cx+104,oy+4,'滴',40,family=SERIF,weight='700',outline=PAPER,ow=8,rot=8,fill=INK)
b+=T(cx+142,oy+12,'！',42,family=SERIF,weight='700',outline=PAPER,ow=8,rot=10,fill=Y,extra=f'stroke="{INK}" stroke-width="1.5"')
# 主角（步行）在过道
px,py=cx-6,262
b+=f'<ellipse cx="{px}" cy="{py+22}" rx="16" ry="6" fill="url(#t50)"/>'
b+=f'<g transform="translate({px-16*1.8},{py-16*1.8}) scale(1.8)">{player()}</g>'
# 脚步
for k,(fx,fy) in enumerate([(px-150,py+10),(px-128,py+2),(px-106,py+10),(px-84,py+2),(px-62,py+10),(px-40,py+2)]):
    b+=f'<ellipse cx="{fx}" cy="{fy}" rx="3" ry="4.5" fill="none" stroke="{INK}" stroke-width="1" opacity="{0.3+k*0.14}"/>'
b+=sweat(px+22,py-28,1.1)
# 气泡
b+=bubble(px-250,176,200,46,'',(px-22,py-8),size=20,lines=['终于找到你了！'])
# 樟树（左右）
b+=canopy(40,300,74,seed=21)
b+=canopy(930,250,70,seed=22)
b+=canopy(900,470,56,seed=23)
b+=canopy(60,480,50,seed=24)
# 桂花小点
for k in range(10):
    b+=f'<circle cx="{random.uniform(20,90):.0f}" cy="{random.uniform(250,360):.0f}" r="1.6" fill="{PAPER}" stroke="{INK}" stroke-width="0.8"/>'
# 旁白框（漫画方框旁白）+ 表情切入格
nx,ny=560,428
b+=frame(nx,ny,250,58)
b+=T(nx+12,ny+24,'左右都被夹死了！',17)
b+=T(nx+12,ny+46,'先挪开一辆邻车（+1 分钟）',13,weight='400')
b+=f'<path d="M{nx+30},{ny} L{ox+10},{oy+62}" stroke="{INK}" stroke-width="2"/>'
fx,fy,fw,fh=170,424,150,66
b+=f'<g transform="rotate(-3 {fx+fw/2} {fy+fh/2})">'+frame(fx,fy,fw,fh)
b+=f'<clipPath id="inset"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}"/></clipPath><g clip-path="url(#inset)">'+burst_lines(fx+38,fy+34,22,80,n=26,seed=3,w=2)+'</g>'
b+=f'<circle cx="{fx+38}" cy="{fy+36}" r="19" fill="{PAPER}" stroke="{INK}" stroke-width="2"/><path d="M{fx+20},{fy+32} q18,-26 36,0 q-8,-6 -18,-4 q-10,-2 -18,4z" fill="{INK}"/>'
b+=f'<path d="M{fx+28},{fy+36} l4,4 l4,-4 M{fx+41},{fy+36} l4,4 l4,-4" stroke="{INK}" stroke-width="2" fill="none"/>'
b+=f'<path d="M{fx+31},{fy+45} q7,8 14,0 z" fill="{INK}"/>'
b+=f'<path d="M{fx+21},{fy+42} l4,1 M{fx+22},{fy+45} l4,1 M{fx+51},{fy+43} l4,-1 M{fx+50},{fy+46} l4,-1" stroke="{INK}" stroke-width="1"/>'
b+=T(fx+100,fy+30,'黄色',17,anchor='middle',fill=INK)
b+=f'<rect x="{fx+78}" y="{fy+38}" width="44" height="16" fill="{Y}" stroke="{INK}" stroke-width="1.5"/>'
b+=T(fx+100,fy+51,'座套！',13,anchor='middle')
b+='</g>'
# HUD
b+=battery_hud(62)
b+=signal(708,12,4)
b+=T(752,82,'信号',11,anchor='middle',weight='400',outline=PAPER,ow=4)
b+=clock_hud('07:38')
b+=hint_bar([(['F'],'查看'),(['E'],'背包')])
render(svg(960,540,b),'01-findcar.png')
