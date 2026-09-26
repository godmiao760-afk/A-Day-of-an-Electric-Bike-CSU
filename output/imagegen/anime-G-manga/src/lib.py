import random, math, cairosvg
PAPER='#F5F1E6'; INK='#1E1E1E'; Y='#FFCC00'
SANS='Noto Sans CJK SC'; SERIF='Noto Serif CJK SC'
OUT='/sessions/stoic-happy-lamport/mnt/Demo1/output/imagegen/anime-G-manga/'

def defs():
    return f'''<defs>
<pattern id="t10" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="6" height="6" fill="{PAPER}"/><circle cx="3" cy="3" r="0.9" fill="{INK}"/></pattern>
<pattern id="t30" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="{PAPER}"/><circle cx="2.5" cy="2.5" r="1.35" fill="{INK}"/></pattern>
<pattern id="t50" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="4" fill="{PAPER}"/><circle cx="2" cy="2" r="1.45" fill="{INK}"/></pattern>
<pattern id="t80" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="4" fill="{INK}"/><circle cx="2" cy="2" r="0.9" fill="{PAPER}"/></pattern>
<pattern id="n80" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="#2a2a2a"/><circle cx="2.5" cy="2.5" r="0.7" fill="#8a877f"/></pattern>
<pattern id="yt" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="4" fill="{Y}"/><circle cx="2" cy="2" r="0.9" fill="{INK}"/></pattern>
<pattern id="h" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="4" height="4" fill="{PAPER}"/><line x1="0" y1="0" x2="0" y2="4" stroke="{INK}" stroke-width="1"/></pattern>
<pattern id="hk" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><rect width="4" height="4" fill="{PAPER}"/><line x1="0" y1="0" x2="0" y2="4" stroke="{INK}" stroke-width="1.6"/></pattern>
<pattern id="hx" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="5" height="5" fill="{PAPER}"/><line x1="0" y1="0" x2="0" y2="5" stroke="{INK}" stroke-width="1"/><line x1="0" y1="0" x2="5" y2="0" stroke="{INK}" stroke-width="1"/></pattern>
<pattern id="hv" width="3" height="10" patternUnits="userSpaceOnUse"><rect width="3" height="10" fill="{PAPER}"/><line x1="1" y1="0" x2="1" y2="10" stroke="{INK}" stroke-width="0.8"/></pattern>
</defs>'''

def T(x,y,s,size=16,fill=INK,anchor='start',weight='700',family=SANS,outline=None,ow=4,rot=0,ls=0,extra=''):
    tr=f' transform="rotate({rot} {x} {y})"' if rot else ''
    base=f'x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{ls}"{tr}'
    s=s.replace('&','&amp;').replace('<','&lt;')
    o=''
    if outline:
        o=f'<text {base} fill="{outline}" stroke="{outline}" stroke-width="{ow}" stroke-linejoin="round">{s}</text>'
    return o+f'<text {base} fill="{fill}" {extra}>{s}</text>'

def svg(w,h,body,bg=PAPER):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{defs()}<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>'

def render(s,name,w=None):
    open('/tmp/g/'+name.replace('.png','.svg'),'w').write(s)
    cairosvg.svg2png(bytestring=s.encode(),write_to=OUT+name)

# ---------- 精灵（原生尺寸坐标） ----------
def bike(kind='own',state=''):
    body = Y if kind=='own' else PAPER
    seat = 'url(#yt)' if kind=='own' else 'url(#t30)'
    if kind=='dark': body='url(#t30)'; seat=INK
    return f'''<g>
<rect x="9.5" y="0.5" width="5" height="9" rx="2" fill="{INK}"/>
<rect x="9.5" y="38.5" width="5" height="9.5" rx="2" fill="{INK}"/>
<path d="M12,4.5 C18,4.5 19,8 19,12 L18,21 C20.5,23 20.5,27 19.2,30 L19.2,40 C19.2,44 16,45.5 12,45.5 C8,45.5 4.8,44 4.8,40 L4.8,30 C3.5,27 3.5,23 6,21 L5,12 C5,8 6,4.5 12,4.5 Z" fill="{body}" stroke="{INK}" stroke-width="1.3"/>
<rect x="7.5" y="14" width="9" height="8.5" fill="url(#h)" stroke="{INK}" stroke-width="0.8"/>
<rect x="7" y="25" width="10" height="15.5" rx="4.5" fill="{seat}" stroke="{INK}" stroke-width="1.1"/>
<path d="M9,27 Q12,26 15,27" stroke="{PAPER}" stroke-width="1" fill="none"/>
<ellipse cx="12" cy="6.3" rx="3" ry="1.5" fill="{PAPER}" stroke="{INK}" stroke-width="0.8"/>
<line x1="2" y1="10.5" x2="22" y2="10.5" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>
<line x1="5" y1="10" x2="3.2" y2="6.8" stroke="{INK}" stroke-width="0.9"/><line x1="19" y1="10" x2="20.8" y2="6.8" stroke="{INK}" stroke-width="0.9"/>
<circle cx="3" cy="6.3" r="1.7" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/><circle cx="21" cy="6.3" r="1.7" fill="{PAPER}" stroke="{INK}" stroke-width="0.9"/>
<rect x="9.5" y="43" width="5" height="1.6" fill="{INK}"/>
</g>'''

def person_top(helmet='white',shirt='url(#h)',cx=16,cy=28,arms_to=None,box=False):
    # 俯视骑车人：肩、手臂、头/头盔
    s=''
    if box:
        s+=f'<rect x="{cx-12}" y="{cy+9}" width="24" height="17" rx="2" fill="url(#hk)" stroke="{INK}" stroke-width="1.4"/><rect x="{cx-7}" y="{cy+14}" width="14" height="7" fill="{PAPER}" stroke="{INK}" stroke-width="0.8"/><path d="M{cx-4},{cy+17.5} h8" stroke="{INK}" stroke-width="1.2"/>'
    if arms_to:
        (lx,ly),(rx,ry)=arms_to
        s+=f'<path d="M{cx-9},{cy} Q{cx-12},{cy-6} {lx},{ly}" stroke="{INK}" stroke-width="4.6" fill="none" stroke-linecap="round"/><path d="M{cx-9},{cy} Q{cx-12},{cy-6} {lx},{ly}" stroke="{PAPER}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
        s+=f'<path d="M{cx+9},{cy} Q{cx+12},{cy-6} {rx},{ry}" stroke="{INK}" stroke-width="4.6" fill="none" stroke-linecap="round"/><path d="M{cx+9},{cy} Q{cx+12},{cy-6} {rx},{ry}" stroke="{PAPER}" stroke-width="2.2" fill="none" stroke-linecap="round"/>'
    s+=f'<ellipse cx="{cx}" cy="{cy+2}" rx="10.5" ry="7" fill="{shirt}" stroke="{INK}" stroke-width="1.4"/>'
    if helmet=='white':
        s+=f'<circle cx="{cx}" cy="{cy-1}" r="6.8" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/><path d="M{cx},{cy-7.5} L{cx},{cy+5.5}" stroke="{INK}" stroke-width="1.6"/><path d="M{cx-5},{cy-4.5} Q{cx},{cy-8.5} {cx+5},{cy-4.5}" stroke="{INK}" stroke-width="2.2" fill="none"/>'
    elif helmet=='yellow':
        s+=f'<circle cx="{cx}" cy="{cy-1}" r="6.8" fill="{Y}" stroke="{INK}" stroke-width="1.5"/><path d="M{cx},{cy-7.5} L{cx},{cy+5.5}" stroke="{INK}" stroke-width="1.4"/><path d="M{cx-5},{cy-4.5} Q{cx},{cy-8.5} {cx+5},{cy-4.5}" stroke="{INK}" stroke-width="2.2" fill="none"/>'
    elif helmet=='black':
        s+=f'<circle cx="{cx}" cy="{cy-1}" r="6.8" fill="{INK}"/><path d="M{cx-3},{cy-5} Q{cx},{cy-6.5} {cx+3},{cy-5}" stroke="{PAPER}" stroke-width="1.4" fill="none"/>'
    else: # 头发
        s+=f'<circle cx="{cx}" cy="{cy-1}" r="6.3" fill="{INK}"/><path d="M{cx-3.5},{cy-3} Q{cx-1},{cy-5.5} {cx+2},{cy-4.5}" stroke="{PAPER}" stroke-width="1.1" fill="none"/>'
    return s

def rider(helmet='yellow'):
    return f'<g transform="translate(4,4)">{bike("own")}</g>'+person_top(helmet,'url(#h)',16,32,((6,15),(26,15)))

def delivery():
    return f'<g transform="translate(4,2)">{bike("dark")}</g>'+person_top('black',PAPER,16,26,((6,13),(26,13)),box=True)

def wrongway():
    return f'<g transform="translate(4,4)">{bike("other")}</g>'+person_top('hair','url(#t30)',16,32,((6,15),(26,15)))

def walker(cx=14,cy=14,hair=True,bag=False):
    s=f'<ellipse cx="{cx-8}" cy="{cy+1}" rx="2.6" ry="3.4" fill="{PAPER}" stroke="{INK}" stroke-width="1.1"/><ellipse cx="{cx+8}" cy="{cy-1}" rx="2.6" ry="3.4" fill="{PAPER}" stroke="{INK}" stroke-width="1.1"/>'
    s+=f'<ellipse cx="{cx}" cy="{cy}" rx="9" ry="5.5" fill="url(#t30)" stroke="{INK}" stroke-width="1.3"/>'
    if bag: s+=f'<rect x="{cx-6}" y="{cy+2}" width="12" height="8" rx="2.5" fill="{Y if bag=="y" else PAPER}" stroke="{INK}" stroke-width="1.3"/><path d="M{cx-3.5},{cy+5.5} h7" stroke="{INK}" stroke-width="1"/>'
    s+=f'<circle cx="{cx}" cy="{cy-2.5}" r="5.3" fill="{INK}"/><path d="M{cx-3},{cy-5} Q{cx},{cy-7} {cx+2.5},{cy-5.5}" stroke="{PAPER}" stroke-width="1.1" fill="none"/>'
    return s

def player():
    return walker(16,15,bag='y')

def pile(state='free'):
    # 32x40 正面稍俯视的充电桩
    scr={'free':PAPER,'busy':PAPER,'broken':INK,'on':Y}[state]
    s=f'<rect x="7" y="36" width="18" height="4" fill="{INK}"/>'
    s+=f'<path d="M7,37 L7,6 Q7,1 12,1 L20,1 Q25,1 25,6 L25,37 Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.5"/>'
    s+=f'<rect x="22" y="4" width="3" height="33" fill="url(#t50)"/>'
    s+=f'<rect x="10" y="6" width="12" height="9" rx="1" fill="{scr}" stroke="{INK}" stroke-width="1.1"/>'
    if state=='broken':
        s+=f'<path d="M12,7 L15,11 L13,12 L17,15" stroke="{PAPER}" stroke-width="0.9" fill="none"/>'
    elif state=='on':
        s+=f'<path d="M16.5,7 L13.5,11 L16,11 L14.5,14" stroke="{INK}" stroke-width="1.1" fill="none"/>'
    else:
        s+=f'<rect x="12" y="8" width="3" height="3" fill="{INK}"/><rect x="17" y="8" width="3" height="3" fill="{INK}"/><rect x="12" y="12" width="2" height="2" fill="{INK}"/><rect x="16" y="12" width="4" height="1.5" fill="{INK}"/>'
    lamp = Y if state in ('on','free') else (INK if state=='busy' else PAPER)
    s+=f'<circle cx="16" cy="19.5" r="2" fill="{lamp}" stroke="{INK}" stroke-width="1"/>'
    s+=f'<rect x="11" y="24" width="10" height="5" rx="1" fill="{INK}"/><circle cx="13.5" cy="26.5" r="1" fill="{PAPER}"/><circle cx="18.5" cy="26.5" r="1" fill="{PAPER}"/>'
    if state in ('on','busy'):
        s+=f'<path d="M16,29 Q14,36 5,38" stroke="{INK}" stroke-width="1.8" fill="none"/>'
    return s

def bus():
    s=f'<rect x="3" y="2" width="58" height="136" rx="10" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    s+=f'<rect x="3" y="2" width="58" height="18" rx="10" fill="url(#t80)"/>'  # 前挡风
    s+=f'<rect x="8" y="26" width="48" height="104" rx="4" fill="url(#t10)" stroke="{INK}" stroke-width="1"/>'
    for yy in (40,70,100): s+=f'<rect x="20" y="{yy}" width="24" height="14" rx="2" fill="{PAPER}" stroke="{INK}" stroke-width="1.2"/><line x1="24" y1="{yy+4}" x2="40" y2="{yy+4}" stroke="{INK}" stroke-width="0.8"/>'
    s+=f'<rect x="0" y="22" width="3" height="10" fill="{INK}"/><rect x="61" y="22" width="3" height="10" fill="{INK}"/>'
    s+=f'<line x1="3" y1="128" x2="61" y2="128" stroke="{INK}" stroke-width="1.4"/>'
    return s

def car():
    s=f'<rect x="4" y="3" width="48" height="94" rx="14" fill="{PAPER}" stroke="{INK}" stroke-width="2"/>'
    s+=f'<path d="M10,30 Q28,20 46,30 L44,42 L12,42 Z" fill="url(#t80)" stroke="{INK}" stroke-width="1.2"/>'
    s+=f'<rect x="12" y="44" width="32" height="30" rx="4" fill="url(#t10)" stroke="{INK}" stroke-width="1"/>'
    s+=f'<path d="M12,76 L44,76 L42,86 Q28,90 14,86 Z" fill="url(#t50)" stroke="{INK}" stroke-width="1.2"/>'
    s+=f'<rect x="0" y="32" width="4" height="6" fill="{INK}"/><rect x="52" y="32" width="4" height="6" fill="{INK}"/>'
    return s

def road_tile(slope=False):
    f='url(#hx)' if slope else 'url(#t10)'
    s=f'<rect width="64" height="64" fill="{PAPER}"/><rect width="64" height="64" fill="{f}"/>'
    if not slope:
        random.seed(3)
        for i in range(14):
            x=random.uniform(2,62); y=random.uniform(2,62)
            s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(.5,1.1):.1f}" fill="{INK}"/>'
        s+='<path d="M8,48 l6,-3 l4,2 l5,-4" stroke="#1E1E1E" stroke-width="1" fill="none"/><path d="M40,14 l4,3 l6,-1" stroke="#1E1E1E" stroke-width="1" fill="none"/>'
    return s

def grass_tile():
    random.seed(5)
    s=f'<rect width="64" height="64" fill="url(#t30)"/>'
    for i in range(9):
        x=random.uniform(6,58); y=random.uniform(8,60)
        s+=f'<path d="M{x-3:.1f},{y:.1f} L{x-1:.1f},{y-5:.1f} L{x:.1f},{y:.1f} L{x+2:.1f},{y-6:.1f} L{x+3:.1f},{y:.1f}" stroke="{INK}" stroke-width="1.1" fill="none" stroke-linejoin="round"/>'
    return s

# ---------- 场景元件 ----------
def canopy(cx,cy,r,seed=1,shadow=True,tone='url(#t30)'):
    random.seed(seed)
    n=14; pts=[]
    for i in range(n):
        a=2*math.pi*i/n; rr=r*random.uniform(.82,1.0)
        pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    d='M'+'%.1f,%.1f'%pts[0]
    for i in range(n):
        p=pts[i]; q=pts[(i+1)%n]
        mx=(p[0]+q[0])/2; my=(p[1]+q[1])/2
        dx=mx-cx; dy=my-cy; L=math.hypot(dx,dy)
        bx=mx+dx/L*r*.28; by=my+dy/L*r*.28
        d+=' Q%.1f,%.1f %.1f,%.1f'%(bx,by,q[0],q[1])
    d+='Z'
    s=''
    if shadow: s+=f'<ellipse cx="{cx+r*.25}" cy="{cy+r*.3}" rx="{r*1.05}" ry="{r*.95}" fill="url(#h)" opacity="0.9"/>'
    cid=f'cp{seed}_{int(cx)}_{int(cy)}'
    s+=f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
    s+=f'<path d="{d}" fill="{PAPER}"/>'
    s+=f'<g clip-path="url(#{cid})"><circle cx="{cx+r*.45}" cy="{cy+r*.5}" r="{r*.95}" fill="{tone}"/></g>'
    for i in range(6):
        a=random.uniform(0,6.28); rr=random.uniform(.2,.6)*r
        x=cx+rr*math.cos(a); y=cy+rr*math.sin(a)
        s+=f'<path d="M{x-r*.15:.1f},{y:.1f} q{r*.15:.1f},{-r*.14:.1f} {r*.3:.1f},0" stroke="{INK}" stroke-width="1.2" fill="none"/>'
    s+=f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{max(1.6,r*.06):.1f}" stroke-linejoin="round"/>'
    return s

def burst_lines(cx,cy,r1,r2,n=40,seed=2,w=3,color=INK,clip=None):
    random.seed(seed); s=''
    for i in range(n):
        a=2*math.pi*i/n+random.uniform(-.05,.05)
        ri=r1*random.uniform(.9,1.35); da=w/r2*random.uniform(.6,1.4)
        p1=(cx+r2*math.cos(a-da),cy+r2*math.sin(a-da)); p2=(cx+r2*math.cos(a+da),cy+r2*math.sin(a+da)); p0=(cx+ri*math.cos(a),cy+ri*math.sin(a))
        s+=f'<path d="M{p0[0]:.1f},{p0[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f}Z" fill="{color}"/>'
    return s

def vlines(x0,x1,y0,y1,n=10,seed=4,w=2.2,color=INK):
    random.seed(seed); s=''
    for i in range(n):
        x=random.uniform(x0,x1); L=random.uniform(.4,1)*(y1-y0); yy=random.uniform(y0,y1-L)
        ww=random.uniform(.6,1)*w
        s+=f'<path d="M{x:.1f},{yy:.1f} L{x+ww/2:.1f},{yy+L*.7:.1f} L{x:.1f},{yy+L:.1f} L{x-ww/2:.1f},{yy+L*.7:.1f}Z" fill="{color}"/>'
    return s

def spiky(cx,cy,rx,ry,n=18,seed=7,fill=PAPER,sw=2.5,jag=.22):
    random.seed(seed); pts=[]
    for i in range(2*n):
        a=math.pi*i/n
        k=1+jag*random.uniform(.6,1.3) if i%2==0 else 1
        pts.append((cx+rx*k*math.cos(a),cy+ry*k*math.sin(a)))
    d='M'+' L'.join('%.1f,%.1f'%p for p in pts)+'Z'
    return f'<path d="{d}" fill="{fill}" stroke="{INK}" stroke-width="{sw}" stroke-linejoin="miter"/>'

def bubble(x,y,w,h,text,tail,size=18,lines=None,side='bottom'):
    # 圆角对白框；tail=(tx,ty) 尖端
    tx,ty=tail
    bx=x+w/2
    if side=='right':
        cy=y+h/2
        s=f'<path d="M{x+w-6},{cy-10} L{tx},{ty} L{x+w-6},{cy+8}Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
        s+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2 if h<60 else 22}" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>'
        s+=f'<path d="M{x+w-4},{cy-8} L{x+w-4},{cy+6}" stroke="{PAPER}" stroke-width="4"/>'
        ls=lines or [text]
        for i,l in enumerate(ls):
            s+=T(x+w/2,y+h/2+size*.36+(i-(len(ls)-1)/2)*size*1.3,l,size,anchor='middle',weight='700')
        return s
    s=f'<path d="M{bx-12},{y+h-4} L{tx},{ty} L{bx+8},{y+h-4}Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
    s+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2 if h<60 else 22}" fill="{PAPER}" stroke="{INK}" stroke-width="2.5"/>'
    s+=f'<path d="M{bx-10},{y+h-3.5} L{bx+6},{y+h-3.5}" stroke="{PAPER}" stroke-width="4"/>'
    ls=lines or [text]
    for i,l in enumerate(ls):
        s+=T(x+w/2,y+h/2+size*.36+(i-(len(ls)-1)/2)*size*1.3,l,size,anchor='middle',weight='700')
    return s

def sweat(x,y,s=1):
    return f'<path transform="translate({x},{y}) scale({s})" d="M0,0 C-5,8 -6,12 0,14 C6,12 5,8 0,0Z" fill="{PAPER}" stroke="{INK}" stroke-width="1.8"/><path transform="translate({x},{y}) scale({s})" d="M-1.5,8 q0,3 2,4" stroke="{INK}" stroke-width="1" fill="none"/>'

def vein(x,y,s=1):
    g=f'<g transform="translate({x},{y}) scale({s})">'
    for r in (0,90,180,270):
        g+=f'<path transform="rotate({r})" d="M3,-9 Q3,-3 9,-3" stroke="{INK}" stroke-width="3" fill="none" stroke-linecap="round"/>'
    return g+'</g>'

def frame(x,y,w,h,fill=PAPER,sw=3,shadow=True):
    s=''
    if shadow: s+=f'<rect x="{x+5}" y="{y+5}" width="{w}" height="{h}" fill="url(#t50)"/>'
    s+=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="{sw}"/>'
    return s

def battery_hud(pct,x=14,y=12,hp=None,cry=False):
    w=250 if hp is None else 250
    h=54 if hp is None else 80
    s=frame(x,y,w,h)
    s+=T(x+12,y+24,'电量',15)
    bx=x+56; by=y+10; bw=140; bh=20
    s+=f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" fill="url(#t10)" stroke="{INK}" stroke-width="2.4"/>'
    s+=f'<rect x="{bx+bw}" y="{by+6}" width="5" height="8" fill="{INK}"/>'
    s+=f'<rect x="{bx+2}" y="{by+2}" width="{(bw-4)*pct/100:.1f}" height="{bh-4}" fill="{Y}"/>'
    s+=f'<rect x="{bx+2}" y="{by+bh-7}" width="{(bw-4)*pct/100:.1f}" height="5" fill="url(#yt)"/>'
    for i in range(1,5): s+=f'<line x1="{bx+bw*i/5}" y1="{by}" x2="{bx+bw*i/5}" y2="{by+bh}" stroke="{INK}" stroke-width="1"/>'
    s+=f'<path d="M{bx+bw*pct/100/2-4},{by+3} l-4,8 h5 l-3,7 l9,-10 h-5 l3,-5z" fill="{INK}"/>' if pct>12 else ''
    s+=T(x+w-10,y+26,f'{pct}%',17,anchor='end',family=SANS)
    s+=T(x+12,y+44,'BATTERY',9,weight='400',ls=2) if hp is None else ''
    if hp is not None:
        s+=T(x+12,y+64,'血量',15)
        for i in range(3):
            hx=x+72+i*30; hy=y+54
            f=INK if i<hp else PAPER
            s+=f'<path d="M{hx},{hy+5} C{hx},{hy-2} {hx+10},{hy-2} {hx+10},{hy+5} C{hx+10},{hy-2} {hx+20},{hy-2} {hx+20},{hy+5} C{hx+20},{hy+11} {hx+13},{hy+15} {hx+10},{hy+19} C{hx+7},{hy+15} {hx},{hy+11} {hx},{hy+5}Z" fill="{f}" stroke="{INK}" stroke-width="2"/>'
            if i<hp: s+=f'<circle cx="{hx+5}" cy="{hy+4}" r="1.8" fill="{PAPER}"/>'
    return s

def clock_hud(t,x=806,y=12,extra=None):
    s=frame(x,y,140,54,fill=INK)
    s+=T(x+70,y+39,t,32,fill=PAPER,anchor='middle',family='Noto Sans Mono CJK SC',ls=1)
    return s

def signal(x,y,n=4,total=5):
    s=frame(x,y,88,54)
    for i in range(total):
        h=8+i*7
        f=INK if i<n else PAPER
        s+=f'<rect x="{x+10+i*14}" y="{y+44-h}" width="9" height="{h}" fill="{f}" stroke="{INK}" stroke-width="1.6"/>'
    return s

def keycap(x,y,k,w=28):
    return f'<rect x="{x}" y="{y}" width="{w}" height="26" rx="4" fill="{PAPER}" stroke="{PAPER}" stroke-width="1"/><rect x="{x+2}" y="{y+21}" width="{w-4}" height="3" fill="url(#t50)"/>'+T(x+w/2,y+19,k,16,anchor='middle')

def hint_bar(items,y=500):
    # items: [(keys,label)]
    s=f'<rect x="0" y="{y}" width="960" height="{540-y}" fill="{INK}"/><line x1="0" y1="{y-4}" x2="960" y2="{y-4}" stroke="{INK}" stroke-width="2"/>'
    # 估算总宽
    parts=[]; tot=0
    for keys,label in items:
        kw=sum(28 if len(k)==1 else 16+10*len(k) for k in keys)+6*(len(keys)-1)
        lw=len(label)*17
        parts.append((keys,label,kw,lw)); tot+=kw+10+lw
    tot+=40*(len(items)-1)
    x=480-tot/2
    for i,(keys,label,kw,lw) in enumerate(parts):
        for k in keys:
            w=28 if len(k)==1 else 16+10*len(k)
            s+=keycap(x,y+7,k,w); x+=w+6
        x+=4
        s+=T(x,y+27,label,17,fill=PAPER); x+=lw
        if i<len(parts)-1:
            s+=f'<circle cx="{x+20}" cy="{y+20}" r="3" fill="{Y}"/>'; x+=40
    return s
