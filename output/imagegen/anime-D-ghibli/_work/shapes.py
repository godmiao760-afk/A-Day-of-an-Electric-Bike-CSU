# 常用 SVG 部件（俯视车辆、人物、樟树、云、UI 便签等）
import math, random
from wc import SANS, SERIF

C = dict(grass='#8DB86B', tree='#3F6B3A', brick='#B5553C', cream='#F4EBD0', sky='#9CC9E0',
         wood='#9A6B43', wood_d='#6E4A2E', ink='#5A3E2B', pine='#2F5233', yellow='#F2C14E',
         yellow_d='#D99A2B', white='#F7F3EA', grey='#B9B4A8', road='#8F8A80', dark='#3B3531',
         osm='#F0B642', red='#C8553D', blue='#5B8DB8', leaf2='#5E8C4A', leaf3='#A9C77E')

def T(x, y, s, txt, size=16, fill='#4a3526', weight='bold', anchor='middle', family=SANS, extra=''):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-weight="{weight}" font-size="{size*s if s else size}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{txt}</text>')

def txt(x, y, t, size=16, fill='#4a3526', weight='bold', anchor='middle', family=SANS, extra=''):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-weight="{weight}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}" {extra}>{t}</text>')

# ---------- 俯视电动车，局部坐标 24x48，车头朝上 ----------
def bike(x, y, s=1.0, body='#F2C14E', seat='#E8A93A', basket=True, rot=0, cargo=None, dim=1.0, mirror=True):
    """x,y = 左上角；s = 缩放"""
    g = []
    sh = f'<ellipse cx="13.5" cy="25.5" rx="10.5" ry="23" fill="#3a2e22" opacity="0.22"/>'
    g.append(sh)
    g.append('<rect x="10" y="0" width="4" height="10" rx="2" fill="#3b3531"/>')        # 前轮
    g.append('<rect x="10" y="39" width="4" height="9" rx="2" fill="#3b3531"/>')        # 后轮
    if basket:
        g.append('<rect x="6" y="3" width="12" height="8" rx="1.5" fill="#cfc8b8" stroke="#7d7466" stroke-width="0.8"/>'
                 '<path d="M8 3v8M10.5 3v8M13.5 3v8M16 3v8M6 7h12" stroke="#8d8474" stroke-width="0.5"/>')
        if cargo == 'bread':
            g.append('<ellipse cx="10" cy="7" rx="3" ry="2.2" fill="#d9a15a"/><rect x="13" y="4.5" width="3" height="5" rx="1" fill="#f3f0e6" stroke="#b9b09c" stroke-width="0.4"/>')
        if cargo == 'leaf':
            g.append('<circle cx="9" cy="6" r="1.4" fill="#e0a43a"/><circle cx="14" cy="8" r="1.2" fill="#b86b3a"/>')
    # 车把 + 后视镜
    g.append('<rect x="1.5" y="11.5" width="21" height="2.6" rx="1.3" fill="#4a4440"/>'
             '<rect x="0.5" y="11" width="4" height="3.6" rx="1.5" fill="#2e2a27"/><rect x="19.5" y="11" width="4" height="3.6" rx="1.5" fill="#2e2a27"/>')
    if mirror:
        g.append('<path d="M5 12 L3.5 8" stroke="#4a4440" stroke-width="0.9"/><path d="M19 12 L20.5 8" stroke="#4a4440" stroke-width="0.9"/>'
                 '<ellipse cx="3.2" cy="7.2" rx="2" ry="1.4" fill="#dfe8ee" stroke="#4a4440" stroke-width="0.6"/>'
                 '<ellipse cx="20.8" cy="7.2" rx="2" ry="1.4" fill="#dfe8ee" stroke="#4a4440" stroke-width="0.6"/>')
    # 前挡 + 车身
    g.append(f'<path d="M5 13.5 Q12 10.5 19 13.5 L17.5 22 Q12 23.5 6.5 22 Z" fill="{body}"/>')
    g.append('<path d="M7.5 14.5 Q12 13 16.5 14.5" stroke="#ffffff" stroke-opacity="0.55" stroke-width="1.1" fill="none"/>')
    g.append('<rect x="7" y="21.5" width="10" height="8" rx="1.5" fill="#6d665e"/>'
             '<path d="M8 23.5h8M8 25.5h8M8 27.5h8" stroke="#8a837a" stroke-width="0.5"/>')          # 脚踏板
    g.append(f'<path d="M6.5 29 Q12 27 17.5 29 L18 42 Q12 45.5 6 42 Z" fill="{body}"/>')        # 后车身
    g.append(f'<ellipse cx="12" cy="35" rx="5.3" ry="7.5" fill="{seat}"/>'
             f'<ellipse cx="11" cy="33" rx="2.2" ry="4" fill="#ffffff" opacity="0.28"/>')               # 座垫
    g.append('<rect x="9" y="43.3" width="6" height="1.8" rx="0.8" fill="#c84a3a"/>')                # 尾灯
    inner = ''.join(g)
    tr = f'translate({x},{y}) scale({s})'
    if rot: tr = f'translate({x+12*s},{y+24*s}) rotate({rot}) translate({-12*s},{-24*s}) scale({s})'
    op = f' opacity="{dim}"' if dim < 1 else ''
    return f'<g transform="{tr}"{op}>{inner}</g>'

# ---------- 骑车的人（32x56）：车 + 人 ----------
def person_top(cx, cy, s=1, shirt='#5B8DB8', hair='#2f2622', helmet=None, bag='#7a9a5a', arms_to=None):
    """俯视的人上半身（肩宽 ~20），cx,cy = 头心"""
    g = []
    if bag:
        g.append(f'<rect x="{cx-7*s}" y="{cy+4*s}" width="{14*s}" height="{10*s}" rx="{3*s}" fill="{bag}"/>'
                 f'<rect x="{cx-5*s}" y="{cy+9*s}" width="{10*s}" height="{3.5*s}" rx="{1.2*s}" fill="#000" opacity="0.15"/>')
    g.append(f'<ellipse cx="{cx}" cy="{cy+1*s}" rx="{10.5*s}" ry="{5.5*s}" fill="{shirt}"/>')
    if arms_to:
        (lx, ly), (rx_, ry_) = arms_to
        g.append(f'<path d="M{cx-8*s} {cy-1*s} Q{cx-10*s} {cy-6*s} {lx} {ly}" stroke="{shirt}" stroke-width="{3.6*s}" fill="none" stroke-linecap="round"/>'
                 f'<path d="M{cx+8*s} {cy-1*s} Q{cx+10*s} {cy-6*s} {rx_} {ry_}" stroke="{shirt}" stroke-width="{3.6*s}" fill="none" stroke-linecap="round"/>'
                 f'<circle cx="{lx}" cy="{ly}" r="{1.8*s}" fill="#f1c9a5"/><circle cx="{rx_}" cy="{ry_}" r="{1.8*s}" fill="#f1c9a5"/>')
    if helmet:
        g.append(f'<circle cx="{cx}" cy="{cy-1*s}" r="{6.6*s}" fill="{helmet}"/>'
                 f'<path d="M{cx-4*s} {cy-5*s} Q{cx} {cy-7.5*s} {cx+4*s} {cy-5*s}" stroke="#fff" stroke-opacity=".6" stroke-width="{1.2*s}" fill="none"/>'
                 f'<path d="M{cx} {cy-7.4*s} V{cy+5*s}" stroke="#000" stroke-opacity=".15" stroke-width="{1*s}"/>')
    else:
        g.append(f'<circle cx="{cx}" cy="{cy-1*s}" r="{6*s}" fill="{hair}"/>'
                 f'<path d="M{cx-3*s} {cy-4*s} q{3*s} {-2*s} {6*s} 0" stroke="#fff" stroke-opacity=".25" stroke-width="{1*s}" fill="none"/>')
    return ''.join(g)

def rider(x, y, s=1.0, body='#F2C14E', seat='#E8A93A', shirt='#F4EBD0', helmet='#E86F4F', bag='#7a9a5a', cargo=None, box=None):
    """x,y 左上角，尺寸 32x56*s；车在内部偏移 (4,4)"""
    g = [f'<g transform="translate({x},{y}) scale({s})">']
    g.append(bike(4, 4, 1.0, body, seat, basket=True, cargo=cargo))
    if box:   # 外卖箱
        g.append(f'<rect x="6" y="36" width="20" height="18" rx="2" fill="{box}"/>'
                 f'<rect x="6" y="36" width="20" height="4" rx="1.5" fill="#fff" opacity=".35"/>'
                 f'<path d="M10 45h12" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity=".85"/>')
    g.append(person_top(16, 30, 1, shirt=shirt, helmet=helmet, bag=None if box else bag,
                        arms_to=((6.5, 16.5), (25.5, 16.5))))
    g.append('</g>')
    return ''.join(g)

def walker(x, y, s=1.0, shirt='#C8553D', hair='#2f2622', dirx=1, step=0, bag=None, pants='#5a6a86'):
    """行人 28x28 俯视，朝 dirx 方向走（1 右 / -1 左 / 0 上）"""
    g = [f'<g transform="translate({x+14*s},{y+14*s}) scale({s})">']
    rot = {1: 90, -1: -90, 0: 0, 2: 180}[dirx]
    g.append(f'<g transform="rotate({rot})">')
    g.append('<ellipse cx="1" cy="2" rx="11" ry="8" fill="#3a2e22" opacity=".2"/>')
    g.append(f'<ellipse cx="-4" cy="{-6+step}" rx="2.6" ry="4" fill="{pants}"/><ellipse cx="4" cy="{6-step-4}" rx="2.6" ry="4" fill="{pants}"/>')
    if bag: g.append(f'<rect x="-6" y="3" width="12" height="7" rx="2.5" fill="{bag}"/>')
    g.append(f'<ellipse cx="0" cy="0" rx="10" ry="5.2" fill="{shirt}"/>')
    g.append(f'<ellipse cx="-10" cy="{-1-step*0.6}" rx="2.3" ry="3.4" fill="{shirt}"/><ellipse cx="10" cy="{-1+step*0.6}" rx="2.3" ry="3.4" fill="{shirt}"/>')
    g.append(f'<circle cx="0" cy="-1" r="5.6" fill="{hair}"/><path d="M-2.5 -4.5 q2.5 -1.5 5 0" stroke="#fff" stroke-opacity=".3" stroke-width="1" fill="none"/>')
    g.append('</g></g>')
    return ''.join(g)

# ---------- 樟树（俯视团簇） ----------
def camphor(cx, cy, r, rng, dark='#3F6B3A', mid='#5E8C4A', light='#8DB86B', hl='#B5D38A', shadow=True, n=9, osm=False):
    g = []
    if shadow:
        g.append(f'<ellipse cx="{cx+r*0.25}" cy="{cy+r*0.3}" rx="{r*1.05}" ry="{r*0.9}" fill="#2c3a22" opacity="0.28"/>')
    pts = []
    for i in range(n):
        a = rng.random()*math.tau; d = rng.random()*r*0.55
        pts.append((cx+math.cos(a)*d, cy+math.sin(a)*d*0.9, r*(0.42+rng.random()*0.25)))
    for (x, y, rr) in pts: g.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{dark}"/>')
    for (x, y, rr) in pts: g.append(f'<circle cx="{x-rr*0.12:.1f}" cy="{y-rr*0.15:.1f}" r="{rr*0.82:.1f}" fill="{mid}"/>')
    for (x, y, rr) in pts[: n//2+2]: g.append(f'<circle cx="{x-rr*0.3:.1f}" cy="{y-rr*0.35:.1f}" r="{rr*0.5:.1f}" fill="{light}"/>')
    for (x, y, rr) in pts[: n//3+1]: g.append(f'<circle cx="{x-rr*0.42:.1f}" cy="{y-rr*0.45:.1f}" r="{rr*0.2:.1f}" fill="{hl}"/>')
    if osm:   # 桂花小黄点
        for _ in range(int(r*1.6)):
            a = rng.random()*math.tau; d = rng.random()*r*0.9
            g.append(f'<circle cx="{cx+math.cos(a)*d:.1f}" cy="{cy+math.sin(a)*d:.1f}" r="{1.1+rng.random()*0.9:.1f}" fill="#F0B642"/>')
    return ''.join(g)

def cloud(cx, cy, w, h, fill='#FFFDF6', shade='#D9E4EA'):
    """夏日积云（侧视）"""
    g = [f'<ellipse cx="{cx}" cy="{cy+h*0.3}" rx="{w*0.5}" ry="{h*0.22}" fill="{shade}"/>']
    bumps = [(-0.32, 0.05, 0.22), (-0.12, -0.18, 0.3), (0.12, -0.28, 0.33), (0.32, -0.02, 0.24), (0.0, 0.1, 0.3)]
    for bx, by, br in bumps:
        g.append(f'<circle cx="{cx+bx*w}" cy="{cy+by*h}" r="{br*h*1.2}" fill="{fill}"/>')
    g.append(f'<ellipse cx="{cx}" cy="{cy+h*0.25}" rx="{w*0.46}" ry="{h*0.14}" fill="{shade}" opacity=".7"/>')
    return ''.join(g)

# ---------- 便签 / 木牌 / 胶带 ----------
def tape(x, y, w, h, rot=0, col='#E7B7A3'):
    return (f'<g transform="translate({x},{y}) rotate({rot})"><rect x="{-w/2}" y="{-h/2}" width="{w}" height="{h}" fill="{col}" opacity=".78"/>'
            f'<path d="M{-w/2} {-h/2} l3 {h/4} -3 {h/4} 3 {h/4} -3 {h/4} M{w/2} {-h/2} l-3 {h/4} 3 {h/4} -3 {h/4} 3 {h/4}" stroke="#fff" stroke-opacity=".4" fill="none"/></g>')

def note(x, y, w, h, fill='#FBF3DC', rot=0, lines=True, shadow=True):
    g = []
    if shadow: g.append(f'<rect x="{x+3}" y="{y+4}" width="{w}" height="{h}" rx="4" fill="#3a2a1a" opacity=".22" transform="rotate({rot} {x+w/2} {y+h/2})"/>')
    g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{fill}" transform="rotate({rot} {x+w/2} {y+h/2})"/>')
    if lines:
        for ly in range(int(y+18), int(y+h-6), 14):
            g.append(f'<path d="M{x+8} {ly} H{x+w-8}" stroke="#C9B89A" stroke-width="0.8" opacity=".6" transform="rotate({rot} {x+w/2} {y+h/2})"/>')
    return ''.join(g)

def woodboard(x, y, w, h, col='#B07D4F'):
    g = [f'<rect x="{x+3}" y="{y+4}" width="{w}" height="{h}" rx="6" fill="#3a2a1a" opacity=".25"/>',
         f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{col}"/>']
    for i in range(1, 3):
        yy = y+h*i/3
        g.append(f'<path d="M{x+4} {yy} Q{x+w/2} {yy+2} {x+w-4} {yy}" stroke="#7a5230" stroke-width="1" opacity=".5" fill="none"/>')
    g.append(f'<rect x="{x+4}" y="{y+4}" width="{w-8}" height="{h-8}" rx="4" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="1.2"/>')
    g.append(f'<circle cx="{x+8}" cy="{y+8}" r="2" fill="#5a3e2b"/><circle cx="{x+w-8}" cy="{y+8}" r="2" fill="#5a3e2b"/>')
    return ''.join(g)

def bubble(x, y, w, h, tail_x, tail_y, fill='#FFFBF0', stroke='#6b4f3a'):
    """圆润的对话气泡（x,y 左上角；尾巴指向 tail_x,tail_y）"""
    r = h/2
    tx = min(max(tail_x, x+r), x+w-r)
    return (f'<path d="M{x+r} {y} H{x+w-r} A{r} {r} 0 0 1 {x+w-r} {y+h} H{tx+7} L{tail_x} {tail_y} L{tx-5} {y+h} H{x+r} A{r} {r} 0 0 1 {x+r} {y} Z" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="2" stroke-linejoin="round"/>')

def battery_bar(x, y, pct, w=120, h=20, col='#7FB35A'):
    g = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#fffaf0" stroke="#5a3e2b" stroke-width="2"/>',
         f'<rect x="{x+w}" y="{y+h*0.3}" width="5" height="{h*0.4}" rx="1.5" fill="#5a3e2b"/>',
         f'<rect x="{x+3}" y="{y+3}" width="{(w-6)*pct/100}" height="{h-6}" rx="4" fill="{col}"/>',
         f'<rect x="{x+5}" y="{y+4.5}" width="{(w-10)*pct/100}" height="3" rx="1.5" fill="#fff" opacity=".45"/>']
    return ''.join(g)

def heart(cx, cy, s, fill='#D9574A', empty=False):
    col = '#e8dccb' if empty else fill
    st = '#8a5a44'
    return (f'<path transform="translate({cx},{cy}) scale({s})" d="M0 6 C-9 -1 -7 -9 -2.5 -8 C-0.8 -7.6 0 -6 0 -5 C0 -6 0.8 -7.6 2.5 -8 C7 -9 9 -1 0 6 Z" '
            f'fill="{col}" stroke="{st}" stroke-width="{1.4/s}"/>'
            + ('' if empty else f'<ellipse transform="translate({cx},{cy}) scale({s})" cx="-3" cy="-4.5" rx="1.6" ry="1.1" fill="#fff" opacity=".6"/>'))

def signal(x, y, n=4, on=3, col='#6E9E4A'):
    g = []
    for i in range(n):
        hh = 6+i*5
        g.append(f'<rect x="{x+i*8}" y="{y-hh}" width="5.5" height="{hh}" rx="1.5" fill="{col if i < on else "#e3d7c0"}" stroke="#5a3e2b" stroke-width="1.2"/>')
    return ''.join(g)

def keycap(x, y, k, w=24):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="6" fill="#FFF8E8" stroke="#6b4f3a" stroke-width="1.8"/>'
            f'<rect x="{x}" y="{y+18}" width="{w}" height="6" rx="3" fill="#6b4f3a" opacity=".18"/>'
            + txt(x+w/2, y+17, k, 14, '#5a3e2b', family=SANS))
