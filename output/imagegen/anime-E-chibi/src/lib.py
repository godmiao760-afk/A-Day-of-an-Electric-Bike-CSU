# -*- coding: utf-8 -*-
# E · Q版萌系日系手游 —— 公用绘制库（SVG 字符串）
import math, random, base64, io

INK = "#3D3A5C"      # 描边墨色（深紫蓝）
SKY = "#4FC3F7"
SKY_D = "#29A9E0"
SKY_L = "#B3E5FC"
PINK = "#FF8FB1"
PINK_D = "#F2668F"
PINK_L = "#FFD1DF"
LEMON = "#FFD54F"
LEMON_D = "#F5B82E"
WHITE = "#FFFFFF"
MINT = "#7EE0B5"
GREEN = "#5CC98A"
GREEN_D = "#3FA46F"
SKIN = "#FFE6D6"
FONT = "Noto Sans CJK SC"


def svg_open(w, h, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">{extra}')


def defs():
    return f'''<defs>
<filter id="ds" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="0" flood-color="{INK}" flood-opacity="0.35"/></filter>
<radialGradient id="glowY"><stop offset="0" stop-color="#FFF3A0" stop-opacity="0.95"/><stop offset="0.6" stop-color="{LEMON}" stop-opacity="0.45"/><stop offset="1" stop-color="{LEMON}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowG"><stop offset="0" stop-color="#C8FFD9" stop-opacity="0.95"/><stop offset="0.55" stop-color="#5CF09A" stop-opacity="0.45"/><stop offset="1" stop-color="#5CF09A" stop-opacity="0"/></radialGradient>
<radialGradient id="glowLamp"><stop offset="0" stop-color="#FFE9A8" stop-opacity="0.75"/><stop offset="0.5" stop-color="#FFC870" stop-opacity="0.28"/><stop offset="1" stop-color="#FFC870" stop-opacity="0"/></radialGradient>
<radialGradient id="glowR"><stop offset="0" stop-color="#FF8A8A" stop-opacity="0.8"/><stop offset="1" stop-color="#FF5A7A" stop-opacity="0"/></radialGradient>
</defs>'''


def T(x, y, s=1.0, rot=0):
    r = f" rotate({rot})" if rot else ""
    return f'transform="translate({x},{y}){r} scale({s})"'


# ---------------- 文字 ----------------
def text(x, y, t, size=20, fill=INK, stroke=None, sw=5, anchor="middle", weight="bold", extra=""):
    base = f'x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" {extra}'
    out = ""
    if stroke:
        out += f'<text {base} fill="{stroke}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round">{t}</text>'
    out += f'<text {base} fill="{fill}">{t}</text>'
    return out


# ---------------- 车 ----------------
def bike(x, y, s=1.0, body=LEMON, dark=LEMON_D, seat="#F6A623", rot=0, sw=1.6, basket=False, glow=False, plug=False):
    """俯视电动车，车头朝上。本地框 24x48，中心(0,0)。"""
    w = sw / s * 1.0
    g = ""
    if glow:
        g += f'<ellipse cx="0" cy="0" rx="26" ry="38" fill="url(#glowY)"/>'
    g += f'''
<rect x="-10" y="-22" width="22" height="47" rx="9" fill="{INK}" opacity="0.18"/>
<rect x="-3.6" y="-24" width="7.2" height="11" rx="3.6" fill="{INK}"/>
<rect x="-4.2" y="13" width="8.4" height="11" rx="4.2" fill="{INK}"/>
<rect x="-11.2" y="-17.2" width="22.4" height="3.6" rx="1.8" fill="{INK}"/>
<circle cx="-10" cy="-19.5" r="2.1" fill="{WHITE}" stroke="{INK}" stroke-width="{w*0.8}"/>
<circle cx="10" cy="-19.5" r="2.1" fill="{WHITE}" stroke="{INK}" stroke-width="{w*0.8}"/>
<path d="M-7.5,-8 Q-8.5,-20 0,-21 Q8.5,-20 7.5,-8 Z" fill="{body}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>
<ellipse cx="0" cy="-18" rx="2.8" ry="1.9" fill="#FFF7C9" stroke="{INK}" stroke-width="{w*0.6}"/>
<rect x="-8.3" y="-9" width="16.6" height="27.5" rx="7.5" fill="{body}" stroke="{INK}" stroke-width="{w}"/>
<rect x="-6" y="-6.5" width="12" height="9" rx="3" fill="{dark}"/>
<rect x="-6.4" y="2.5" width="12.8" height="13" rx="5.6" fill="{seat}" stroke="{INK}" stroke-width="{w*0.8}"/>
<ellipse cx="-2.2" cy="6.2" rx="2.4" ry="1.6" fill="{WHITE}" opacity="0.55"/>
<rect x="-3" y="16.8" width="6" height="2.3" rx="1.1" fill="#FF6B8B"/>
<path d="M-6,-12 Q-3,-16 1,-17" stroke="{WHITE}" stroke-width="{w*0.9}" fill="none" stroke-linecap="round" opacity="0.8"/>
'''
    if basket:
        g += f'<rect x="-5.5" y="-27.5" width="11" height="6" rx="2" fill="#F3E3C2" stroke="{INK}" stroke-width="{w*0.7}"/><path d="M-3,-27 v5 M0,-27 v5 M3,-27 v5" stroke="{INK}" stroke-width="{w*0.4}"/>'
    if plug:
        g += f'<path d="M8,4 C16,6 18,-4 22,-8" stroke="#2BD47A" stroke-width="{w*1.4}" fill="none" stroke-linecap="round"/>'
    return f'<g {T(x,y,s,rot)}>{g}</g>'


OTHER_BIKES = [
    ("#F7F8FC", "#DADFEA", "#B8C4D9"),
    ("#FFFFFF", "#E3E7F0", "#9FD0EA"),
    ("#F2F5F3", "#D8E3DC", "#A9DBBE"),
    ("#FAF7FD", "#E4DCEE", "#CDB8E6"),
    ("#FFFFFF", "#E8E2E6", "#F2B8C9"),
    ("#F3F4F7", "#D5D9E3", "#6E7391"),
    ("#FBFBF6", "#E7E6D8", "#E8D7A8"),
]


def bike_other(x, y, s=1.0, i=0, rot=0, sw=1.6, **kw):
    b, d, st = OTHER_BIKES[i % len(OTHER_BIKES)]
    return bike(x, y, s, b, d, st, rot, sw, **kw)


# ---------------- Q版角色（步行，3/4 俯视，看得到脸） ----------------
def face(expr, sw):
    """脸部五官，头心在 (0,-8)"""
    e = ""
    if expr == "happy":
        e += f'<path d="M-7.5,-2 Q-5,-6 -2.5,-2" stroke="{INK}" stroke-width="{sw*1.1}" fill="none" stroke-linecap="round"/>'
        e += f'<path d="M2.5,-2 Q5,-6 7.5,-2" stroke="{INK}" stroke-width="{sw*1.1}" fill="none" stroke-linecap="round"/>'
        e += f'<path d="M-2.6,1.5 Q0,5.5 2.6,1.5 Z" fill="#E4506F" stroke="{INK}" stroke-width="{sw*0.6}" stroke-linejoin="round"/>'
    elif expr == "dizzy":
        for cx in (-5, 5):
            e += f'<path d="M{cx-2.3},-4.3 L{cx+2.3},0.3 M{cx+2.3},-4.3 L{cx-2.3},0.3" stroke="{INK}" stroke-width="{sw*1.1}" stroke-linecap="round"/>'
        e += f'<path d="M-2.5,3 Q-1.2,1.8 0,3 Q1.2,4.2 2.5,3" stroke="{INK}" stroke-width="{sw*0.8}" fill="none" stroke-linecap="round"/>'
    elif expr == "worry":
        for cx in (-5, 5):
            e += f'<ellipse cx="{cx}" cy="-2" rx="2.3" ry="3" fill="{INK}"/><circle cx="{cx-0.8}" cy="-3.2" r="1" fill="{WHITE}"/>'
        e += f'<path d="M-8,-7 L-3,-6 M8,-7 L3,-6" stroke="{INK}" stroke-width="{sw*0.8}" stroke-linecap="round"/>'
        e += f'<ellipse cx="0" cy="3" rx="1.6" ry="1.3" fill="{INK}"/>'
    elif expr == "tired":
        e += f'<path d="M-7.5,-2 L-2.5,-2 M2.5,-2 L7.5,-2" stroke="{INK}" stroke-width="{sw*1.1}" stroke-linecap="round"/>'
        e += f'<path d="M-2,3 Q0,1.8 2,3" stroke="{INK}" stroke-width="{sw*0.8}" fill="none" stroke-linecap="round"/>'
    else:  # normal
        for cx in (-5, 5):
            e += f'<ellipse cx="{cx}" cy="-2" rx="2.3" ry="3.1" fill="{INK}"/><circle cx="{cx-0.8}" cy="-3.3" r="1.05" fill="{WHITE}"/>'
        e += f'<path d="M-1.8,2.3 Q0,3.8 1.8,2.3" stroke="{INK}" stroke-width="{sw*0.8}" fill="none" stroke-linecap="round"/>'
    e += f'<ellipse cx="-8.2" cy="2" rx="2.4" ry="1.4" fill="{PINK}" opacity="0.7"/><ellipse cx="8.2" cy="2" rx="2.4" ry="1.4" fill="{PINK}" opacity="0.7"/>'
    return e


def chibi(x, y, s=1.0, hair="#7A4E3A", top=SKY, top2=WHITE, expr="normal", sw=1.6, clip=True, arms="side", hat=None):
    """Q版 2 头身。本地：头心(0,-8) r=12.5；脚底 y≈20。"""
    w = sw / s
    g = f'<ellipse cx="0" cy="20" rx="11" ry="3.6" fill="{INK}" opacity="0.2"/>'
    # 腿
    g += f'<rect x="-5.5" y="12" width="4.6" height="8" rx="2.3" fill="{INK}"/><rect x="0.9" y="12" width="4.6" height="8" rx="2.3" fill="{INK}"/>'
    # 身体
    g += f'<path d="M-8,15 Q-8.5,4 0,3.5 Q8.5,4 8,15 Z" fill="{top}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>'
    g += f'<path d="M-2.5,4.5 L0,9 L2.5,4.5" fill="{top2}" stroke="{INK}" stroke-width="{w*0.6}" stroke-linejoin="round"/>'
    if arms == "side":
        g += f'<ellipse cx="-9" cy="10" rx="2.8" ry="3.8" fill="{top}" stroke="{INK}" stroke-width="{w*0.9}"/><ellipse cx="9" cy="10" rx="2.8" ry="3.8" fill="{top}" stroke="{INK}" stroke-width="{w*0.9}"/>'
    elif arms == "up":  # 欢呼
        g += f'<path d="M-6,7 L-12,-2" stroke="{top}" stroke-width="5" stroke-linecap="round"/><circle cx="-12.5" cy="-3" r="2.4" fill="{SKIN}" stroke="{INK}" stroke-width="{w*0.8}"/>'
        g += f'<path d="M6,7 L12,-2" stroke="{top}" stroke-width="5" stroke-linecap="round"/><circle cx="12.5" cy="-3" r="2.4" fill="{SKIN}" stroke="{INK}" stroke-width="{w*0.8}"/>'
    elif arms == "front":  # 推车：双手向上
        g += f'<path d="M-6,7 L-7,-6" stroke="{top}" stroke-width="4.6" stroke-linecap="round"/><path d="M6,7 L7,-6" stroke="{top}" stroke-width="4.6" stroke-linecap="round"/>'
    # 头后发
    g += f'<path d="M-13.5,-6 Q-15,8 -9,9 L9,9 Q15,8 13.5,-6 Z" fill="{hair}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>'
    # 脸
    g += f'<circle cx="0" cy="-7" r="12.2" fill="{SKIN}" stroke="{INK}" stroke-width="{w}"/>'
    # 刘海
    g += (f'<path d="M-13,-5 Q-14,-21 0,-21.5 Q14,-21 13,-5 Q11,-9 9.5,-7.5 Q8,-11 5,-8 Q3,-12 0,-8.5 Q-3,-12 -5,-8 Q-8,-11 -9.5,-7.5 Q-11,-9 -13,-5 Z" '
          f'fill="{hair}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>')
    g += f'<path d="M-6,-17.5 Q-1,-20 4,-18.5" stroke="{WHITE}" stroke-width="{w*1.2}" fill="none" stroke-linecap="round" opacity="0.55"/>'
    # 呆毛
    g += f'<path d="M1,-21 Q3,-28 7,-26 Q4,-25 3.5,-21" fill="{hair}" stroke="{INK}" stroke-width="{w*0.8}" stroke-linejoin="round"/>'
    if clip:  # 闪电发卡
        g += f'<path d="M8.5,-17 L6,-12.5 L8.5,-12.8 L7,-9 L11.2,-14 L8.7,-13.8 L10.5,-17 Z" fill="{LEMON}" stroke="{INK}" stroke-width="{w*0.6}" stroke-linejoin="round"/>'
    if hat == "helmet_delivery":
        g += f'<path d="M-13.5,-8 Q-13,-24 0,-24 Q13,-24 13.5,-8 Z" fill="#FFB020" stroke="{INK}" stroke-width="{w}"/><rect x="-14" y="-10" width="28" height="3.4" rx="1.7" fill="#FF8A00" stroke="{INK}" stroke-width="{w*0.7}"/>'
    g += face(expr, w)
    return f'<g {T(x,y,s)}>{g}</g>'


# ---------------- 骑车的主角（俯视，车头朝上） ----------------
def rider(x, y, s=1.0, sw=1.6, look_back=False, expr="worry", helmet=True, body=LEMON, dark=LEMON_D, seat="#F6A623",
          top=SKY, hair="#7A4E3A", rot=0, glow=False, bag=None):
    """本地框 32x56，中心(0,0)：车 24x48 + 身体 + 大脑袋"""
    w = sw / s
    g = bike(0, 2, 1.0, body, dark, seat, 0, sw=sw * 1.0 / 1.0 * 1, glow=glow).replace(f'scale(1.0)', 'scale(1)')
    # 手臂伸向车把
    g += f'<path d="M-8,4 Q-11,-6 -10,-13" stroke="{INK}" stroke-width="{5.6}" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M8,4 Q11,-6 10,-13" stroke="{INK}" stroke-width="{5.6}" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M-8,4 Q-11,-6 -10,-13" stroke="{top}" stroke-width="{3.6}" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M8,4 Q11,-6 10,-13" stroke="{top}" stroke-width="{3.6}" fill="none" stroke-linecap="round"/>'
    g += f'<circle cx="-10" cy="-14" r="2" fill="{SKIN}" stroke="{INK}" stroke-width="{w*0.7}"/><circle cx="10" cy="-14" r="2" fill="{SKIN}" stroke="{INK}" stroke-width="{w*0.7}"/>'
    # 身体（肩背）
    if bag:
        g += f'<rect x="-9" y="6" width="18" height="15" rx="4" fill="{bag}" stroke="{INK}" stroke-width="{w}"/>'
    g += f'<ellipse cx="0" cy="7" rx="10" ry="8" fill="{top}" stroke="{INK}" stroke-width="{w}"/>'
    g += f'<path d="M-5,11 Q0,13 5,11" stroke="{WHITE}" stroke-width="{w*0.9}" fill="none" stroke-linecap="round"/>'
    # 大脑袋
    hy = -3
    if look_back:
        g += f'<g transform="translate(0,{hy})">'
        g += f'<path d="M-12,-2 Q-13.5,9 -8,9.5 L8,9.5 Q13.5,9 12,-2 Z" fill="{hair}" stroke="{INK}" stroke-width="{w}"/>'
        g += f'<circle cx="0" cy="0" r="11" fill="{SKIN}" stroke="{INK}" stroke-width="{w}"/>'
        if helmet:
            g += f'<path d="M-12,1 Q-12.5,-13.5 0,-13.5 Q12.5,-13.5 12,1 Q6,-4 0,-4 Q-6,-4 -12,1 Z" fill="{LEMON}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>'
            g += f'<path d="M-10,-9 L-12,-15 L-6,-12 Z M10,-9 L12,-15 L6,-12 Z" fill="{LEMON}" stroke="{INK}" stroke-width="{w*0.8}" stroke-linejoin="round"/>'
            g += f'<path d="M-5,-10 Q0,-12 5,-10" stroke="{WHITE}" stroke-width="{w*1.1}" fill="none" stroke-linecap="round"/>'
        g += f'<g transform="translate(0,7) scale(0.85)">{face(expr, w)}</g>'
        g += '</g>'
    else:
        g += f'<g transform="translate(0,{hy})">'
        g += f'<circle cx="0" cy="0" r="11" fill="{hair}" stroke="{INK}" stroke-width="{w}"/>'
        g += f'<ellipse cx="-11" cy="2.5" rx="2.2" ry="3" fill="{SKIN}" stroke="{INK}" stroke-width="{w*0.7}"/><ellipse cx="11" cy="2.5" rx="2.2" ry="3" fill="{SKIN}" stroke="{INK}" stroke-width="{w*0.7}"/>'
        if helmet:
            g += f'<path d="M-11,3 Q-12,-11.5 0,-11.5 Q12,-11.5 11,3 Q0,-1 -11,3 Z" fill="{LEMON}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>'
            g += f'<path d="M-9,-7 L-12,-13 L-5,-10.5 Z M9,-7 L12,-13 L5,-10.5 Z" fill="{LEMON}" stroke="{INK}" stroke-width="{w*0.8}" stroke-linejoin="round"/>'
            g += f'<path d="M-4.5,-8 Q0,-10 4.5,-8" stroke="{WHITE}" stroke-width="{w*1.1}" fill="none" stroke-linecap="round"/>'
            g += f'<path d="M-3,5 Q0,8 3,5" stroke="{hair}" stroke-width="{3}" fill="none"/>'
        else:
            g += f'<path d="M0,-11 Q3,-17 6,-15" stroke="{INK}" stroke-width="{w}" fill="none"/>'
        g += '</g>'
    return f'<g {T(x,y,s,rot)}>{g}</g>'


def delivery(x, y, s=1.0, sw=1.6, rot=0):
    """外卖车 32x56：橙色车 + 大外卖箱 + 骑手"""
    w = sw / s
    g = bike(0, 2, 1, "#FF9F43", "#F07F1A", "#5A5F7A", 0, sw=sw)
    g += f'<path d="M-8,0 Q-11,-7 -10,-13 M8,0 Q11,-7 10,-13" stroke="{INK}" stroke-width="5.4" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M-8,0 Q-11,-7 -10,-13 M8,0 Q11,-7 10,-13" stroke="#FFC247" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
    g += f'<ellipse cx="0" cy="3" rx="9.5" ry="7" fill="#FFC247" stroke="{INK}" stroke-width="{w}"/>'
    g += f'<g transform="translate(0,-6)"><circle cx="0" cy="0" r="9.5" fill="#FFB020" stroke="{INK}" stroke-width="{w}"/><path d="M-9,1 Q0,-2 9,1" stroke="#FF8A00" stroke-width="2.6" fill="none"/><path d="M-4,-6 Q0,-8 4,-6" stroke="{WHITE}" stroke-width="{w}" fill="none" stroke-linecap="round"/></g>'
    # 外卖箱
    g += f'<rect x="-11" y="9" width="22" height="17" rx="3.5" fill="#FFD54F" stroke="{INK}" stroke-width="{w}"/>'
    g += f'<rect x="-11" y="9" width="22" height="5" rx="2.5" fill="#FFB020" stroke="{INK}" stroke-width="{w*0.7}"/>'
    g += f'<path d="M-5,19 Q0,23 5,19" stroke="{INK}" stroke-width="{w*1.1}" fill="none" stroke-linecap="round"/><circle cx="-4" cy="17" r="1.1" fill="{INK}"/><circle cx="4" cy="17" r="1.1" fill="{INK}"/>'
    return f'<g {T(x,y,s,rot)}>{g}</g>'


def wrongway(x, y, s=1.0, sw=1.6, rot=0):
    """逆行车：红车 + 墨镜骑手"""
    w = sw / s
    g = bike(0, 2, 1, "#FF7A8A", "#E85468", "#3D3A5C", 0, sw=sw)
    g += f'<path d="M-8,4 Q-11,-6 -10,-13 M8,4 Q11,-6 10,-13" stroke="{INK}" stroke-width="5.4" fill="none" stroke-linecap="round"/>'
    g += f'<path d="M-8,4 Q-11,-6 -10,-13 M8,4 Q11,-6 10,-13" stroke="#6B6F8E" stroke-width="3.4" fill="none" stroke-linecap="round"/>'
    g += f'<ellipse cx="0" cy="7" rx="10" ry="8" fill="#6B6F8E" stroke="{INK}" stroke-width="{w}"/>'
    g += f'<circle cx="0" cy="-3" r="10.5" fill="#2F2B45" stroke="{INK}" stroke-width="{w}"/><path d="M-3,-10 Q3,-15 6,-9" stroke="#56507A" stroke-width="2" fill="none"/>'
    return f'<g {T(x,y,s,rot)}>{g}</g>'


def bus(x, y, s=1.0, sw=2.0, rot=0):
    """校车 64x140 俯视：圆胖面包车顶"""
    w = sw / s
    g = f'<rect x="-30" y="-66" width="64" height="140" rx="22" fill="{INK}" opacity="0.18"/>'
    g += f'<rect x="-32" y="-70" width="64" height="140" rx="22" fill="#7EE0B5" stroke="{INK}" stroke-width="{w}"/>'
    g += f'<path d="M-28,-50 Q-28,-66 0,-66 Q28,-66 28,-50 L28,-44 L-28,-44 Z" fill="#BFEFFF" stroke="{INK}" stroke-width="{w*0.8}"/>'
    g += f'<path d="M-18,-60 L-8,-50" stroke="{WHITE}" stroke-width="3" stroke-linecap="round"/>'
    g += f'<rect x="-24" y="-36" width="48" height="96" rx="12" fill="#A6F0CF" stroke="{INK}" stroke-width="{w*0.7}"/>'
    for i in range(4):
        yy = -28 + i * 22
        g += f'<rect x="-18" y="{yy}" width="36" height="14" rx="5" fill="{WHITE}" stroke="{INK}" stroke-width="{w*0.6}"/>'
    g += f'<rect x="-30" y="-12" width="60" height="8" fill="{LEMON}" stroke="{INK}" stroke-width="{w*0.6}"/>'
    g += text(0, -6.5, "校车", 7, INK, None, anchor="middle")
    g += f'<rect x="-36" y="-58" width="6" height="10" rx="3" fill="{INK}"/><rect x="30" y="-58" width="6" height="10" rx="3" fill="{INK}"/>'
    g += f'<circle cx="-20" cy="-66" r="3.5" fill="#FFF7C9" stroke="{INK}" stroke-width="{w*0.6}"/><circle cx="20" cy="-66" r="3.5" fill="#FFF7C9" stroke="{INK}" stroke-width="{w*0.6}"/>'
    return f'<g {T(x,y,s,rot)}>{g}</g>'


def walker(x, y, s=1.0, sw=1.6, hair="#2F2B45", top=PINK, expr="normal", phone=True):
    """行人（俯视 3/4）28x28 框，低头看手机"""
    g = chibi(0, 0, 1, hair, top, WHITE, expr, sw, clip=False)
    if phone:
        g += f'<rect x="-4" y="5" width="8" height="6" rx="1.4" fill="#5A5F7A" stroke="{INK}" stroke-width="{sw*0.6/s}"/><rect x="-3" y="6" width="6" height="3.5" fill="#9FE3FF"/>'
    return f'<g {T(x,y,s)}>{g}</g>'


# ---------------- 充电桩 ----------------
def pile(x, y, s=1.0, state="free", sw=1.6):
    """32x40 本地框。state: free / occupied / broken / qr / plugged"""
    w = sw / s
    scr = {"free": "#6BEFA0", "occupied": "#FF6F8E", "broken": "#3A3F55", "qr": "#FFD54F", "plugged": "#5CF09A"}[state]
    g = ""
    if state == "plugged":
        g += f'<circle cx="0" cy="-4" r="30" fill="url(#glowG)"/>'
    g += f'<rect x="-13" y="-17" width="28" height="38" rx="7" fill="{INK}" opacity="0.2"/>'
    g += f'<rect x="-14" y="-20" width="28" height="38" rx="7" fill="{WHITE}" stroke="{INK}" stroke-width="{w}"/>'
    g += f'<path d="M-14,-12 L-14,-13 Q-14,-20 -7,-20 L7,-20 Q14,-20 14,-13 L14,-12 Z" fill="{SKY}" stroke="{INK}" stroke-width="{w}"/>'
    g += f'<path d="M-2.5,-19 L-4.5,-15 L-1.5,-15.5 L-3,-12.5 L2.5,-17 L-0.5,-16.6 L1,-19 Z" fill="{LEMON}"/>'
    g += f'<rect x="-9" y="-9" width="18" height="12" rx="3" fill="{scr}" stroke="{INK}" stroke-width="{w*0.8}"/>'
    if state == "free":
        g += f'<path d="M-4,-3 L-1,0 L4.5,-6" stroke="{WHITE}" stroke-width="{w*1.4}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
    elif state == "occupied":
        g += f'<path d="M-3.5,-6.5 L3.5,0.5 M3.5,-6.5 L-3.5,0.5" stroke="{WHITE}" stroke-width="{w*1.4}" stroke-linecap="round"/>'
    elif state == "broken":
        g += f'<path d="M-6,-8 L-1,-3 L-4,-1 L2,2" stroke="#8A90AA" stroke-width="{w*0.7}" fill="none"/>'
        g += f'<g transform="rotate(-25 3 -3)"><rect x="-3" y="-6" width="12" height="5" rx="1.5" fill="#FFE0C7" stroke="{INK}" stroke-width="{w*0.5}"/></g>'
    elif state == "qr":
        g += text(0, 1.2, "?", 10, INK, None)
    elif state == "plugged":
        g += f'<path d="M-1,-8 L-4,-2 L0,-2.5 L-2,2 L4,-4.5 L0,-4 L2,-8 Z" fill="{WHITE}"/>'
    # 二维码
    g += f'<rect x="-6" y="6" width="8" height="8" rx="1" fill="{WHITE}" stroke="{INK}" stroke-width="{w*0.6}"/>'
    g += f'<rect x="-5" y="7" width="2.5" height="2.5" fill="{INK}"/><rect x="-1.5" y="10.5" width="2.5" height="2.5" fill="{INK}"/><rect x="-5" y="10.5" width="1.4" height="1.4" fill="{INK}"/>'
    # 插口/线
    g += f'<circle cx="7" cy="10" r="3" fill="{SKY_L}" stroke="{INK}" stroke-width="{w*0.6}"/>'
    return f'<g {T(x,y,s)}>{g}</g>'


# ---------------- 樟树 / 景物 ----------------
def tree(x, y, s=1.0, sw=2.0, c1=GREEN, c2="#86E0A8", c3=GREEN_D, flowers=True, seed=0):
    """胖胖的樟树（俯视树冠）"""
    rnd = random.Random(seed)
    w = sw / s
    g = f'<ellipse cx="4" cy="8" rx="30" ry="24" fill="{INK}" opacity="0.18"/>'
    blobs = [(-14, -2, 15), (12, -4, 16), (0, -14, 16), (-4, 10, 15), (15, 10, 13), (-17, 12, 11)]
    path = ""
    for bx, by, br in blobs:
        g += f'<circle cx="{bx}" cy="{by}" r="{br}" fill="{c1}" stroke="{INK}" stroke-width="{w}"/>'
    for bx, by, br in blobs:
        g += f'<circle cx="{bx}" cy="{by}" r="{br - w}" fill="{c1}"/>'
    for bx, by, br in [(-6, -10, 8), (8, -8, 7), (-12, 2, 6)]:
        g += f'<circle cx="{bx}" cy="{by}" r="{br}" fill="{c2}"/>'
    for bx, by, br in [(10, 12, 7), (-5, 14, 6)]:
        g += f'<circle cx="{bx}" cy="{by}" r="{br}" fill="{c3}" opacity="0.55"/>'
    g += f'<path d="M-10,-16 Q-6,-20 -1,-20" stroke="{WHITE}" stroke-width="{w*1.3}" fill="none" stroke-linecap="round" opacity="0.7"/>'
    if flowers:
        for _ in range(9):
            fx, fy = rnd.uniform(-22, 22), rnd.uniform(-22, 18)
            g += f'<circle cx="{fx:.1f}" cy="{fy:.1f}" r="1.4" fill="#FFC93C" stroke="#E8A21A" stroke-width="0.4"/>'
    return f'<g {T(x,y,s)}>{g}</g>'


def cone(x, y, s=1.0, sw=1.6):
    w = sw / s
    return (f'<g {T(x,y,s)}><ellipse cx="0" cy="6" rx="9" ry="4" fill="{INK}" opacity="0.2"/>'
            f'<rect x="-8" y="2" width="16" height="5" rx="2" fill="#FF7A45" stroke="{INK}" stroke-width="{w}"/>'
            f'<path d="M-5,3 L-1.5,-10 Q0,-12 1.5,-10 L5,3 Z" fill="#FF8A50" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>'
            f'<path d="M-3.5,-2 L3.5,-2" stroke="{WHITE}" stroke-width="2.2"/></g>')


def mountain(x, y, s=1.0, sw=2.2, face_on=True):
    """Q版岳麓山：圆胖双峰 + 小亭子 + 表情"""
    w = sw / s
    g = f'<path d="M-90,30 Q-70,-10 -40,-20 Q-20,-50 10,-48 Q40,-46 55,-18 Q80,-10 95,30 Z" fill="#6FD39A" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/>'
    g += f'<path d="M-60,30 Q-40,0 -10,-8 Q20,-14 40,8 Q60,14 70,30 Z" fill="#4FBF84" opacity="0.8"/>'
    g += f'<path d="M-20,-38 Q0,-50 20,-42" stroke="{WHITE}" stroke-width="{w*1.4}" fill="none" stroke-linecap="round" opacity="0.7"/>'
    # 枫叶红点（爱晚亭秋色）
    for (px, py) in [(-50, 5), (-30, -12), (30, -20), (55, 0), (-5, 10), (20, 12)]:
        g += f'<circle cx="{px}" cy="{py}" r="4" fill="#FF8C7A" stroke="{INK}" stroke-width="{w*0.5}"/>'
    # 小亭子
    g += f'<g transform="translate(8,-50)"><path d="M-10,0 L0,-8 L10,0 Z" fill="#FF6F6F" stroke="{INK}" stroke-width="{w*0.7}" stroke-linejoin="round"/><rect x="-6" y="0" width="12" height="6" fill="#FFF3D6" stroke="{INK}" stroke-width="{w*0.6}"/></g>'
    if face_on:
        g += f'<ellipse cx="-12" cy="-8" rx="2.4" ry="3.2" fill="{INK}"/><ellipse cx="12" cy="-8" rx="2.4" ry="3.2" fill="{INK}"/>'
        g += f'<path d="M-4,-1 Q0,3 4,-1" stroke="{INK}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
        g += f'<ellipse cx="-20" cy="-2" rx="4" ry="2.2" fill="{PINK}" opacity="0.7"/><ellipse cx="20" cy="-2" rx="4" ry="2.2" fill="{PINK}" opacity="0.7"/>'
    return f'<g {T(x,y,s)}>{g}</g>'


def cloud(x, y, s=1.0, sw=2.0, fill=WHITE):
    w = sw / s
    return (f'<g {T(x,y,s)}><path d="M-30,10 Q-34,-4 -20,-6 Q-18,-20 -2,-18 Q8,-28 20,-16 Q34,-16 32,0 Q40,10 28,12 Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="{w}" stroke-linejoin="round"/></g>')


# ---------------- UI（手游风） ----------------
def card(x, y, w, h, fill=WHITE, stroke=INK, sw=3, r=16, shadow=True, sh=5):
    out = ""
    if shadow:
        out += f'<rect x="{x}" y="{y+sh}" width="{w}" height="{h}" rx="{r}" fill="{INK}" opacity="0.35"/>'
    out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    return out


def slant_tag(x, y, w, h, label, fill=PINK, color=WHITE, size=15, skew=8):
    """斜切标签（平行四边形）"""
    p = f"{x+skew},{y} {x+w},{y} {x+w-skew},{y+h} {x},{y+h}"
    p2 = f"{x+skew},{y+3} {x+w},{y+3} {x+w-skew},{y+h+3} {x},{y+h+3}"
    return (f'<polygon points="{p2}" fill="{INK}" opacity="0.35"/><polygon points="{p}" fill="{fill}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
            + text(x + w / 2, y + h / 2 + size * 0.36, label, size, color, None))


def battery_hud(x, y, pct, hearts=None, low=False):
    """左上角：电池图标 + 百分比；可选爱心血量"""
    W = 250 if hearts is None else 250
    H = 64 if hearts is None else 96
    o = card(x, y, W, H, WHITE, INK, 3, 18)
    o += f'<rect x="{x+6}" y="{y+6}" width="{W-12}" height="{H-12}" rx="13" fill="none" stroke="{SKY_L}" stroke-width="2" stroke-dasharray="1 0"/>'
    # 电池图标
    bx, by = x + 16, y + 14
    col = "#5CD68A" if pct >= 40 else ("#FFB23F" if pct >= 20 else "#FF5A7A")
    o += f'<rect x="{bx}" y="{by}" width="118" height="36" rx="10" fill="#EEF4FF" stroke="{INK}" stroke-width="3"/>'
    o += f'<rect x="{bx+118}" y="{by+11}" width="8" height="14" rx="3" fill="{INK}"/>'
    segs = 5
    fill_n = pct / 100 * segs
    for i in range(segs):
        sx = bx + 6 + i * 22
        k = min(1, max(0, fill_n - i))
        if k > 0:
            o += f'<rect x="{sx}" y="{by+6}" width="{19*k:.1f}" height="24" rx="5" fill="{col}"/>'
            o += f'<rect x="{sx+2}" y="{by+8}" width="{max(0,19*k-6):.1f}" height="5" rx="2.5" fill="{WHITE}" opacity="0.55"/>'
    o += f'<path d="M{bx+62},{by+3} L{bx+50},{by+20} L{bx+58},{by+20} L{bx+53},{by+33} L{bx+68},{by+15} L{bx+60},{by+15} L{bx+65},{by+3} Z" fill="{LEMON}" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
    o += text(x + 190, y + 45, f"{pct}%", 30, WHITE if not low else "#FFE3EA", INK, 7)
    if hearts is not None:
        full, total = hearts
        for i in range(total):
            hx, hy = x + 24 + i * 36, y + 74
            f = PINK if i < full else "#E4E1EE"
            o += heart(hx, hy, 1.0, f)
        o += text(x + 200, y + 81, "HP", 15, SKY_D, None)
    return o


def heart(x, y, s, fill):
    return (f'<g {T(x,y,s)}><path d="M0,10 C-14,0 -14,-12 -6,-12 C-2,-12 0,-8 0,-6 C0,-8 2,-12 6,-12 C14,-12 14,0 0,10 Z" '
            f'fill="{fill}" stroke="{INK}" stroke-width="2.4" stroke-linejoin="round"/>'
            f'<ellipse cx="-6" cy="-6" rx="2.6" ry="1.8" fill="{WHITE}" opacity="0.8"/></g>')


def clock_hud(x, y, t, day="DAY 1", sub=None, signal=None, night=False, icon="sun"):
    """右上角时钟卡片。x,y 为卡片左上角；宽 220"""
    W = 220
    o = card(x, y, W, 64, WHITE, INK, 3, 18)
    o += slant_tag(x - 14, y - 14, 86, 26, day, PINK, WHITE, 14)
    if icon == "sun":
        o += f'<g transform="translate({x+30},{y+38})">' + "".join(
            f'<path d="M0,-14 L0,-10" stroke="#FFB23F" stroke-width="3" stroke-linecap="round" transform="rotate({a})"/>' for a in range(0, 360, 45)) \
            + f'<circle r="7" fill="{LEMON}" stroke="{INK}" stroke-width="2"/></g>'
    else:
        o += f'<g transform="translate({x+30},{y+38})"><path d="M4,-11 A11,11 0 1,0 8,7 A9,9 0 1,1 4,-11 Z" fill="{LEMON}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/></g>'
    o += text(x + 108, y + 50, t, 34, INK, None)
    if signal is not None:
        # 信号格
        for i in range(4):
            hh = 8 + i * 7
            f = SKY if i < signal else "#E1E6F0"
            o += f'<rect x="{x+168+i*10}" y="{y+50-hh}" width="7" height="{hh}" rx="2" fill="{f}" stroke="{INK}" stroke-width="1.8"/>'
    if sub:
        o += sub
    return o


def keycap(x, y, k, w=30, fill=WHITE, col=INK):
    return (f'<rect x="{x}" y="{y+4}" width="{w}" height="30" rx="8" fill="{INK}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="30" rx="8" fill="{fill}" stroke="{INK}" stroke-width="2.5"/>'
            + text(x + w / 2, y + 21, k, 17, col, None))


def hint_bar(cx, y, items):
    """底部操作提示：[(key, label), ...]"""
    # 估算宽度
    widths = []
    for k, lab in items:
        kw = 30 if len(k) == 1 else 22 + 11 * len(k)
        widths.append(kw + 8 + 17 * len(lab) + 26)
    total = sum(widths) + 30
    x0 = cx - total / 2
    o = f'<rect x="{x0}" y="{y+4}" width="{total}" height="46" rx="23" fill="{INK}" opacity="0.35"/>'
    o += f'<rect x="{x0}" y="{y}" width="{total}" height="46" rx="23" fill="{WHITE}" stroke="{INK}" stroke-width="3" opacity="0.96"/>'
    xx = x0 + 18
    for (k, lab), wd in zip(items, widths):
        kw = 30 if len(k) == 1 else 22 + 11 * len(k)
        o += keycap(xx, y + 6, k, kw, LEMON if k in ("F",) else WHITE)
        o += text(xx + kw + 8, y + 29, lab, 17, INK, None, anchor="start")
        xx += wd
    return o


def bubble(x, y, w, h, t, tail_x, tail_y, size=19, fill=WHITE):
    """漫画对话框（带尾巴）。x,y 左上角"""
    tx = max(x + 20, min(x + w - 20, tail_x))
    by = y + h
    path = (f'M{x+16},{y} L{x+w-16},{y} Q{x+w},{y} {x+w},{y+16} L{x+w},{by-16} Q{x+w},{by} {x+w-16},{by} '
            f'L{tx+10},{by} L{tail_x},{tail_y} L{tx-6},{by} L{x+16},{by} Q{x},{by} {x},{by-16} L{x},{y+16} Q{x},{y} {x+16},{y} Z')
    o = f'<path d="{path}" fill="{INK}" opacity="0.3" transform="translate(0,4)"/>'
    o += f'<path d="{path}" fill="{fill}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
    o += text(x + w / 2, y + h / 2 + size * 0.36, t, size, INK, None)
    return o


def sticker_sparkle(x, y, s=1.0):
    """✨ 贴纸：白边圆贴 + 黄星"""
    star = "M0,-14 Q2,-2 14,0 Q2,2 0,14 Q-2,2 -14,0 Q-2,-2 0,-14 Z"
    o = f'<g {T(x,y,s)}><circle r="20" fill="{WHITE}" stroke="{INK}" stroke-width="2.5"/>'
    o += f'<path d="{star}" fill="{LEMON}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
    o += f'<path d="{star}" fill="{PINK}" stroke="{INK}" stroke-width="1.5" transform="translate(10,-9) scale(0.4)"/>'
    o += f'<path d="{star}" fill="{SKY}" stroke="{INK}" stroke-width="1.5" transform="translate(-10,9) scale(0.33)"/></g>'
    return o


def sticker_dizzy(x, y, s=1.0):
    """😵 贴纸"""
    o = f'<g {T(x,y,s)}><circle r="20" fill="{WHITE}" stroke="{INK}" stroke-width="2.5"/>'
    o += f'<circle r="14" fill="{LEMON}" stroke="{INK}" stroke-width="2"/>'
    for cx in (-5, 5):
        o += f'<path d="M{cx-3},-6 L{cx+3},0 M{cx+3},-6 L{cx-3},0" stroke="{INK}" stroke-width="2.2" stroke-linecap="round"/>'
    o += f'<ellipse cx="0" cy="6" rx="3.5" ry="2.8" fill="{INK}"/></g>'
    return o


def sticker_sweat(x, y, s=1.0):
    o = f'<g {T(x,y,s)}><path d="M0,-12 Q10,2 6,8 Q0,14 -6,8 Q-10,2 0,-12 Z" fill="#9FE3FF" stroke="{INK}" stroke-width="2.2" stroke-linejoin="round"/>'
    o += f'<ellipse cx="-2" cy="4" rx="2" ry="3" fill="{WHITE}"/></g>'
    return o


def sticker_bang(x, y, s=1.0, fill=PINK):
    """！ 爆炸贴纸"""
    pts = []
    for i in range(20):
        r = 24 if i % 2 == 0 else 15
        a = math.pi * 2 * i / 20
        pts.append(f"{r*math.cos(a):.1f},{r*math.sin(a):.1f}")
    o = f'<g {T(x,y,s)}><polygon points="{" ".join(pts)}" fill="{fill}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>'
    o += text(0, 9, "!", 26, WHITE, INK, 5) + '</g>'
    return o


def png_b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render(svg, out_png, w=None, h=None):
    import cairosvg
    cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=out_png, output_width=w, output_height=h)
