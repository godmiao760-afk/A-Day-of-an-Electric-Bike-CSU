from lib import *
random.seed(31)
b=''
NIGHT='url(#n80)'
# 夜空：深网点
b+=f'<rect x="0" y="0" width="960" height="540" fill="{INK}"/>'
b+=f'<rect x="0" y="0" width="960" height="200" fill="url(#t80)"/>'
# 星点
for k in range(30): b+=f'<circle cx="{random.uniform(0,960):.0f}" cy="{random.uniform(0,40):.0f}" r="{random.uniform(.6,1.4):.1f}" fill="{PAPER}"/>'
# 岳麓山剪影
b+=f'<path d="M0,40 L80,26 L170,34 L260,14 L340,28 L430,10 L520,26 L620,16 L720,30 L820,18 L960,28 L960,60 L0,60Z" fill="{INK}" stroke="{PAPER}" stroke-width="1.2"/>'
# 宿舍楼（夜：墨黑立面，窗户亮 = 纸白，少量黄）
bx0,bx1,by0,by1=20,940,34,176
b+=f'<rect x="{bx0}" y="{by0}" width="{bx1-bx0}" height="{by1-by0}" fill="url(#t80)" stroke="{PAPER}" stroke-width="2"/>'
for fl,fy in enumerate((44,84,124)):
    for i in range(15):
        wx=bx0+16+i*61
        lit=random.random()<.62
        f=PAPER if lit else INK
        b+=f'<rect x="{wx}" y="{fy}" width="42" height="28" fill="{f}" stroke="{PAPER}" stroke-width="1.2"/>'
        if lit:
            b+=f'<line x1="{wx+21}" y1="{fy}" x2="{wx+21}" y2="{fy+28}" stroke="{INK}" stroke-width="1"/>'
            if random.random()<.4: b+=f'<path d="M{wx+4},{fy+10} l5,-4 l5,4 v12 h-10z" fill="{INK}"/>'   # 晾衣剪影
            if random.random()<.3: b+=f'<circle cx="{wx+32}" cy="{fy+14}" r="4" fill="{INK}"/><rect x="{wx+27}" y="{fy+18}" width="10" height="10" fill="{INK}"/>'  # 人影
        b+=f'<rect x="{wx-2}" y="{fy+20}" width="46" height="9" fill="{INK}" stroke="{PAPER}" stroke-width="1"/>'
# 门禁 大门
b+=f'<rect x="420" y="120" width="120" height="56" fill="{PAPER}" stroke="{PAPER}" stroke-width="2"/>'
b+=f'<rect x="428" y="126" width="104" height="50" fill="url(#t30)"/><line x1="480" y1="126" x2="480" y2="176" stroke="{INK}" stroke-width="2"/>'
b+=f'<rect x="410" y="104" width="140" height="20" fill="{INK}" stroke="{PAPER}" stroke-width="2"/>'
b+=T(480,119,'门禁 23:00',13,fill=PAPER,anchor='middle')
# 地面
b+=f'<rect x="0" y="176" width="960" height="324" fill="url(#n80)"/>'
b+=f'<line x1="0" y1="177" x2="960" y2="177" stroke="{PAPER}" stroke-width="2.5"/>'
# 路灯光圈（纸白网点渐变：同心圆）
def lamp(x,y,r):
    s=''
    for k,(rr,pat) in enumerate([(r,'url(#t80)'),(r*.72,'url(#t50)'),(r*.45,'url(#t30)'),(r*.22,PAPER)]):
        s+=f'<ellipse cx="{x}" cy="{y+r*.6}" rx="{rr*1.3}" ry="{rr*.8}" fill="{pat}"/>'
    s+=f'<line x1="{x}" y1="{y+r*.6}" x2="{x}" y2="{y-40}" stroke="{PAPER}" stroke-width="3"/>'
    s+=f'<path d="M{x},{y-40} q16,-6 26,4" stroke="{PAPER}" stroke-width="3" fill="none"/><ellipse cx="{x+28}" cy="{y-34}" rx="8" ry="4" fill="{Y}" stroke="{PAPER}" stroke-width="1.5"/>'
    return s
b+=lamp(40,330,110)+lamp(900,330,110)
# 充电桩排（雨棚 + 桩）
b+=f'<rect x="60" y="238" width="840" height="16" fill="{INK}" stroke="{PAPER}" stroke-width="2"/>'
for k in range(22): b+=f'<line x1="{60+k*40}" y1="238" x2="{80+k*40}" y2="254" stroke="{PAPER}" stroke-width="1"/><line x1="{80+k*40}" y1="254" x2="{100+k*40}" y2="238" stroke="{PAPER}" stroke-width="1"/>'
states=['busy','broken','busy','free','on','busy','broken','free','busy']
PK=2.0
xs=[90+i*92 for i in range(9)]
ME=4
for i,(x,st) in enumerate(zip(xs,states)):
    # 车位线
    b+=f'<rect x="{x-6}" y="338" width="76" height="116" fill="none" stroke="{PAPER}" stroke-width="1.6" stroke-dasharray="6 4"/>'
    if st=='on':
        # 黄光晕
        b+=f'<ellipse cx="{x+32}" cy="{300}" rx="60" ry="46" fill="url(#yt)" opacity=".55"/>'
        b+=burst_lines(x+32,296,44,70,n=20,seed=6,w=2,color=Y)
    b+=f'<rect x="{x}" y="206" width="64" height="80" fill="{PAPER}" opacity="0"/>'
    b+=f'<g transform="translate({x},{254}) scale({PK})">{pile(st)}</g>'
    # 标签
    lab={'busy':'被占','broken':'坏了','free':'空闲','on':'充电中'}[st]
    lw=len(lab)*14+14
    fill=Y if st=='on' else (PAPER)
    b+=f'<rect x="{x+32-lw/2}" y="{462}" width="{lw}" height="22" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>'
    b+=T(x+32,478,lab,13,anchor='middle')
    if st=='busy':
        b+=f'<g transform="translate({x+14},{348}) scale(1.5)">{bike("other")}</g>'
    if st=='broken':
        b+=T(x+40,284,'？',22,fill=PAPER,family=SERIF,rot=12)
        b+=f'<path d="M{x+6},{346} q10,-6 16,2" stroke="{PAPER}" stroke-width="1.4" fill="none"/>'
# 主角的车（插在 ME 号桩）+ 主角推车
mx=xs[ME]
b+=f'<g transform="translate({mx+14},{350}) scale(1.5)">{bike("own")}</g>'
# 充电线（黄）
b+=f'<path d="M{mx+36},{311} C{mx+30},{336} {mx+50},{346} {mx+34},{376}" stroke="{Y}" stroke-width="4" fill="none"/><path d="M{mx+36},{311} C{mx+30},{336} {mx+50},{346} {mx+34},{376}" stroke="{INK}" stroke-width="1" fill="none"/>'
b+=T(mx+76,356,'咔哒',18,family=SERIF,fill=PAPER,rot=-10)
# 主角站在车旁
px,py=mx-28,414
b+=f'<g transform="translate({px-24},{py-24}) scale(1.5)">{walker(16,16,bag="y")}</g>'
b+=sweat(px+18,py-26,.9)
# 幻觉叹气
b+=f'<path d="M{px-30},{py-30} q-10,-6 -4,-14 q6,-6 -2,-12" stroke="{PAPER}" stroke-width="2" fill="none"/>'
# 气泡 （左侧）
b+=bubble(150,392,176,46,'',(px-18,py-8),size=17,lines=['……终于插上了。'],side='right')
# 樟树剪影
for i,(x,y,r) in enumerate([(20,470,60),(940,470,64)]):
    b+=canopy(x,y,r,seed=70+i,shadow=False,tone='url(#t80)')
# ===== 选项弹窗（漫画格） =====
X,Yp,Wd,Hd=280,26,430,198
b+=f'<g transform="rotate(-1.2 495 125)">'
b+=f'<rect x="{X+8}" y="{Yp+8}" width="{Wd}" height="{Hd}" fill="{Y}" stroke="{INK}" stroke-width="3"/>'
b+=f'<rect x="{X}" y="{Yp}" width="{Wd}" height="{Hd}" fill="{PAPER}" stroke="{INK}" stroke-width="4"/>'
b+=f'<rect x="{X+6}" y="{Yp+6}" width="{Wd-12}" height="{Hd-12}" fill="none" stroke="{INK}" stroke-width="1.2"/>'
# 角标
# 集中线背景（弹窗内上半）
b+=f'<clipPath id="dlg"><rect x="{X+7}" y="{Yp+7}" width="{Wd-14}" height="{Hd-14}"/></clipPath><g clip-path="url(#dlg)">'+burst_lines(X+Wd/2,Yp+62,150,400,n=60,seed=12,w=1.6)+'</g>'
b+=f'<ellipse cx="{X+Wd/2}" cy="{Yp+62}" rx="200" ry="40" fill="{PAPER}"/>'
b+=T(X+Wd/2,Yp+56,'终于插上了。',24,anchor='middle',family=SERIF)
b+=T(X+Wd/2,Yp+88,'守着它，还是先回宿舍？',20,anchor='middle')
# 选项
ox1,ox2,oy,ow,oh=X+26,X+Wd/2+10,Yp+112,Wd/2-36,48
b+=f'<rect x="{ox1+5}" y="{oy+5}" width="{ow}" height="{oh}" fill="{INK}"/>'
b+=f'<rect x="{ox1}" y="{oy}" width="{ow}" height="{oh}" fill="{Y}" stroke="{INK}" stroke-width="3"/>'
b+=f'<path d="M{ox1+16},{oy+14} l12,10 l-12,10z" fill="{INK}"/>'
b+=T(ox1+ow/2+8,oy+32,'守着它',21,anchor='middle')
b+=f'<rect x="{ox2}" y="{oy}" width="{ow}" height="{oh}" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
b+=T(ox2+ow/2,oy+32,'回宿舍',21,anchor='middle',weight='400')
b+=T(ox1+ow/2,oy+68,'每分钟 +0.5%，守到门禁',12,anchor='middle',weight='400')
b+=T(ox2+ow/2,oy+68,'赌一把：充满 or 被拔',12,anchor='middle',weight='400')
b+='</g>'
# HUD
b+=battery_hud(14)
b+=clock_hud('22:47')
b+=f'<g transform="translate(806,72)">'+f'<rect x="0" y="0" width="140" height="28" fill="{Y}" stroke="{INK}" stroke-width="2.5"/>'+T(70,20,'门禁 23:00',15,anchor='middle')+'</g>'
b+=T(826,126,'还剩 13 分钟！',16,fill=INK,family=SERIF,rot=-4,outline=PAPER,ow=6)
b+=hint_bar([(['A','D'],'切换'),(['F'],'确认')])
render(svg(960,540,b),'03-charge.png')
