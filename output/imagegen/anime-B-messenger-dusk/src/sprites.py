# 精灵（全部按游戏真实像素尺寸、在局部坐标里画；车辆俯视车头朝上）
from lib import P, SVG
import math


def _g(s, x, y, sc=1.0, rot=0, w=0, h=0):
    tf = f'translate({x:.1f},{y:.1f}) scale({sc})'
    if rot:
        tf += f' rotate({rot} {w / 2} {h / 2})'
    s.g(tf)


def ground_shadow(s, cx, cy, rx, ry, dx=0, dy=0, op=0.35):
    s.ell_fill(cx + dx, cy + dy, rx, ry, P['shadow'], op)


def bike(s, x, y, sc=1.0, body=None, seat=None, trim=None, rot=0, shadow=(2, 3), lw=1.3, basket=True, glow=None):
    """24×48 电动车，俯视车头朝上"""
    body = body or P['lamp']
    seat = seat or body
    trim = trim or P['ink2']
    _g(s, x, y, sc, rot, 24, 48)
    a = 0.35
    if shadow:
        s.fillj([(3 + shadow[0], 3 + shadow[1]), (21 + shadow[0], 3 + shadow[1]), (21 + shadow[0], 46 + shadow[1]), (3 + shadow[0], 46 + shadow[1])], P['shadow'], 0.6, 6, op=0.35)
    if glow:
        s.ell_fill(12, 24, 16, 28, glow, 0.25)
    # 前后轮
    s.rbox(9.5, 0.5, 5, 9, 2.2, '#3B3347', lw * 0.8, 0.2)
    s.rbox(9.5, 39, 5, 9, 2.2, '#3B3347', lw * 0.8, 0.2)
    # 车把
    s.shape([(1, 9), (23, 9), (23, 12), (1, 12)], trim, lw * 0.8, 0.2, seg=30)
    s.ell_fill(1.5, 7.5, 2.2, 1.6, P['creamD'])  # 后视镜
    s.ell_fill(22.5, 7.5, 2.2, 1.6, P['creamD'])
    # 车头罩
    s.shape([(6, 5), (18, 5), (19, 15), (5, 15)], body, lw, a, seg=6)
    s.ell_fill(12, 6.8, 3.2, 1.4, P['goldL'], 0.95)  # 大灯
    # 车身（脚踏板）
    s.shape([(5, 14), (19, 14), (18, 27), (6, 27)], body, lw, a, seg=6)
    s.box(7.5, 17, 9, 8, P['ink'], 0, 0.2, op=0.28)  # 踏板暗色
    # 座垫
    s.rbox(5.5, 26, 13, 16, 5, seat, lw, a)
    s.fillj([(6.5, 34), (17.5, 34), (17.5, 40), (6.5, 40)], P['ink'], 0.2, 5, op=0.18)  # 座垫暗面（硬光影）
    s.ell_fill(9.5, 30, 2.2, 3, P['cream'], 0.55)  # 亮
    # 尾部
    s.shape([(7, 41), (17, 41), (16, 44.5), (8, 44.5)], trim, lw * 0.8, 0.2)
    s.box(9, 42, 6, 1.6, P['red'], 0, 0.1)
    if basket:
        s.line([(8, 14.3), (16, 14.3)], P['ink2'], 0.8, 0.1)
    s.eg()


def other_bike(s, x, y, sc=1.0, variant=0, **k):
    bodies = [('#EEE8E4', '#C9C0CE'), ('#E4DDE6', '#B7ADC4'), ('#EAE2D6', '#8E7FA8'), ('#DCD6DF', '#6F6580'), ('#EFE9EC', '#D9A5A0')]
    b, st = bodies[variant % len(bodies)]
    bike(s, x, y, sc, body=b, seat=st, trim='#6A5F7A', **k)


def person_top(s, cx, cy, shirt, hair, helmet=None, arms_to=None, bag=None, lw=1.3, sc=1.0):
    """俯视小人（局部坐标，cx,cy 为头心）"""
    # 手臂
    if arms_to:
        for sx, (tx, ty) in zip((-8, 8), arms_to):
            s.line([(cx + sx, cy + 3), (tx, ty)], P['ink'], 3.8, 0.2)
            s.line([(cx + sx, cy + 3), (tx, ty)], shirt, 2.2, 0.2)
            s.ell_fill(tx, ty, 1.8, 1.8, '#E8C4AE')
    if bag:
        s.rbox(cx - 6, cy + 3, 12, 8, 3, bag, lw, 0.3)
    # 肩膀
    s.shape([(cx - 10, cy + 1), (cx - 5, cy - 3), (cx + 5, cy - 3), (cx + 10, cy + 1), (cx + 9, cy + 6), (cx - 9, cy + 6)], shirt, lw, 0.35, seg=5, smooth=True)
    s.fillj([(cx - 9, cy + 3), (cx + 9, cy + 3), (cx + 8.5, cy + 6), (cx - 8.5, cy + 6)], P['ink'], 0.2, 5, op=0.2)
    # 头
    if helmet:
        s.ellipse(cx, cy - 1, 6.2, 6.6, helmet, lw, 0.25, n=14)
        s.ell_fill(cx - 1.8, cy - 3.5, 2.2, 1.6, P['cream'], 0.6)
        s.line([(cx - 5, cy - 3.5), (cx + 5, cy - 3.5)], P['ink'], 0.9, 0.1, op=0.6)  # 帽檐
    else:
        s.ellipse(cx, cy - 1, 5.6, 6, hair, lw, 0.25, n=14)
        s.ell_fill(cx - 1.5, cy - 3, 1.8, 1.4, P['lavL'], 0.5)


def rider(s, x, y, sc=1.0, helmet=True, rot=0, glow=None):
    """32×56 主角骑车"""
    _g(s, x, y, sc, rot, 32, 56)
    s.fillj([(8, 8), (26, 8), (26, 56), (8, 56)], P['shadow'], 0.6, 6, op=0.3)
    bike(s, 4, 6, 1.0, shadow=None, glow=glow)
    person_top(s, 16, 30, P['lav'], '#4A3A48', helmet=P['pink'] if helmet else None,
               arms_to=[(6, 16.5), (26, 16.5)], bag=P['pinkD'])
    s.eg()


def rider_carry(s, x, y, sc=1.0):
    _g(s, x, y, sc)
    bike(s, 4, 6, 1.0, shadow=None)
    person_top(s, 16, 44, P['pink'], '#3D3340', helmet=None, bag=None)
    person_top(s, 16, 30, P['lav'], '#4A3A48', helmet=P['pink'], arms_to=[(6, 16.5), (26, 16.5)])
    s.eg()


def npc_delivery(s, x, y, sc=1.0):
    """32×56 外卖车：锈橙车身 + 方形保温箱"""
    _g(s, x, y, sc)
    s.fillj([(8, 8), (26, 8), (26, 56), (8, 56)], P['shadow'], 0.6, 6, op=0.3)
    bike(s, 4, 6, 1.0, body=P['rust'], seat='#5A4E6E', trim='#4A3E58', shadow=None)
    person_top(s, 16, 26, '#E07A3F', '#3B3040', helmet=P['rust'], arms_to=[(6, 16.5), (26, 16.5)])
    # 保温箱
    s.box(7, 34, 18, 16, '#E8B04A', 1.4, 0.3)
    s.box(7, 44, 18, 6, P['rustD'], 0, 0.2, op=0.45)
    s.line([(9, 37), (23, 37)], P['cream'], 1.2, 0.2)
    s.eg()


def npc_wrong(s, x, y, sc=1.0):
    """逆行车（游戏里 setFlipY）——这里直接画成车头朝下"""
    s.g(f'translate({x:.1f},{y:.1f}) scale({sc}) translate(0,56) scale(1,-1)')
    s.fillj([(8, 8), (26, 8), (26, 56), (8, 56)], P['shadow'], 0.6, 6, op=0.3)
    bike(s, 4, 6, 1.0, body=P['pink'], seat=P['pinkD'], trim='#6A5F7A', shadow=None)
    person_top(s, 16, 30, '#7A8FA0', '#302838', helmet=None, arms_to=[(6, 16.5), (26, 16.5)])
    s.eg()


def walker(s, x, y, sc=1.0, shirt=None, facing=90, umbrella=False):
    """28×28 行人（横穿），facing 90 = 朝右走"""
    _g(s, x, y, sc)
    s.ell_fill(16, 17, 11, 8, P['shadow'], 0.3)
    s.g(f'rotate({facing} 14 14)')  # 朝上画，再整体旋转到行走方向
    s.ellipse(9, 20, 3, 2.4, '#4A3E58', 1, 0.2, n=10)   # 脚（一前一后）
    s.ellipse(19, 7, 3, 2.4, '#4A3E58', 1, 0.2, n=10)
    person_top(s, 14, 15, shirt or P['gL'], '#3A2E3A', arms_to=[(5, 19), (23, 10)], bag=P['lavL'])
    s.eg()
    s.eg()


def npc_bus(s, x, y, sc=1.0):
    """64×140 校车：米白车身 + 灰紫腰线 + 顶上空调"""
    _g(s, x, y, sc)
    s.fillj([(6, 8), (64, 8), (64, 142), (6, 142)], P['shadow'], 1, 10, op=0.35)
    s.rbox(2, 2, 60, 136, 9, P['cream'], 2, 0.5)
    s.rbox(2, 2, 60, 18, 8, P['lavL'], 1.6, 0.4)   # 前挡风（车头朝上）
    s.fillj([(6, 6), (58, 6), (56, 16), (8, 16)], '#6F87A8', 0.4, 8, op=0.8)
    s.box(2, 20, 5, 110, P['lav'], 0, 0.3)
    s.box(57, 20, 5, 110, P['lav'], 0, 0.3)
    for i in range(6):  # 侧窗
        s.box(3, 26 + i * 17, 3, 12, '#6F87A8', 0, 0.2)
        s.box(58, 26 + i * 17, 3, 12, '#6F87A8', 0, 0.2)
    s.rbox(18, 40, 28, 26, 4, P['creamD'], 1.5, 0.4)  # 空调
    for i in range(4):
        s.line([(21, 45 + i * 5), (43, 45 + i * 5)], P['ink2'], 0.8, 0.2)
    s.rbox(22, 86, 20, 14, 3, P['creamD'], 1.3, 0.3)
    s.fillj([(3, 104), (61, 104), (61, 137), (3, 137)], P['ink'], 0.4, 10, op=0.12)  # 顶面暗阶
    s.text(32, 125, '校车', 11, P['lav'], anchor='middle')
    s.eg()


def npc_car(s, x, y, sc=1.0, body='#9FA7B8'):
    """56×100 小汽车"""
    _g(s, x, y, sc)
    s.fillj([(6, 8), (58, 8), (58, 102), (6, 102)], P['shadow'], 1, 10, op=0.35)
    s.rbox(3, 2, 50, 96, 14, body, 2, 0.5)
    s.fillj([(10, 22), (46, 22), (43, 36), (13, 36)], '#4E5E7E', 0.4, 8)  # 前挡
    s.rbox(12, 38, 32, 34, 5, body, 1.3, 0.3)  # 车顶
    s.fillj([(12, 56), (44, 56), (44, 72), (12, 72)], P['ink'], 0.3, 10, op=0.15)
    s.fillj([(14, 74), (42, 74), (44, 84), (12, 84)], '#4E5E7E', 0.4, 8)  # 后挡
    s.ell_fill(11, 6, 4, 2, P['goldL'])
    s.ell_fill(45, 6, 4, 2, P['goldL'])
    s.box(8, 93, 8, 3, P['red'], 0, 0.2)
    s.box(40, 93, 8, 3, P['red'], 0, 0.2)
    s.eg()


def pile(s, x, y, sc=1.0, state='free', t=0):
    """32×40 充电桩（带一点 3/4 立面）；state: free / occupied / broken / plugged / qrfail"""
    _g(s, x, y, sc)
    glow = state == 'plugged'
    if glow:
        s.ell_fill(16, 22, 22, 24, P['neon'], 0.22)
        s.ell_fill(16, 22, 13, 15, P['neon'], 0.25)
    s.ell_fill(18, 38, 14, 3, P['shadow'], 0.45)
    # 桩体：顶面 + 正面
    s.shape([(4, 5), (28, 5), (28, 37), (4, 37)], '#C9C2D6' if state != 'broken' else '#A9A1B6', 1.4, 0.3)
    s.shape([(4, 2), (28, 2), (28, 7), (4, 7)], P['cream'], 1.2, 0.2)  # 顶
    s.box(22, 7, 6, 30, P['ink'], 0, 0.2, op=0.18)  # 侧暗阶
    # 屏幕
    sc_col = {'free': '#8FE6CF', 'occupied': '#F2C14E', 'broken': '#2A2436', 'plugged': P['neon'], 'qrfail': '#E88A80'}[state]
    s.box(8, 10, 16, 10, sc_col, 1.1, 0.2)
    if state == 'broken':
        s.line([(10, 11), (15, 16), (13, 19)], '#6F6580', 0.8, 0.1)
        s.line([(15, 16), (22, 14)], '#6F6580', 0.8, 0.1)
    elif state == 'plugged':
        s.box(10, 16, 11, 2, P['indigo'], 0, 0.1, op=0.6)
    # 二维码
    s.box(9, 23, 8, 8, P['cream'], 0.9, 0.1)
    for (qx, qy) in [(10, 24), (14, 24), (10, 28), (13, 27), (15, 29)]:
        s.box(qx, qy, 1.6, 1.6, P['ink'], 0, 0)
    # 状态灯
    lc = {'free': P['neon'], 'occupied': P['lamp'], 'broken': '#5A4E6E', 'plugged': P['neon'], 'qrfail': P['red']}[state]
    s.ell_fill(21, 26, 2, 2, lc)
    # 枪线
    if state in ('occupied', 'plugged'):
        s.line([(26, 30), (31, 34), (33, 40)], P['ink'], 1.8, 0.2)
    else:
        s.line([(26, 30), (30, 31), (29, 35), (26, 35)], P['ink'], 1.6, 0.2)
    s.eg()


def tile_road(s, x, y, sc=1.0, dash=True, slope=False):
    _g(s, x, y, sc)
    base = P['road'] if not slope else '#8A6F7E'
    s.rect(0, 0, 64, 64, base)
    s.specks(0, 0, 64, 64, 26, P['roadD'], 0.4, 1.2, 0.8)
    s.specks(0, 0, 64, 64, 12, P['roadL'], 0.4, 1.0, 0.8)
    s.strokes(0, 0, 64, 64, 5, P['roadD'], 10, 1.5, 80, 0.6)
    if dash:
        s.rbox(30, 8, 4, 22, 1.5, P['creamD'], 0, 0)
        s.rbox(30, 40, 4, 16, 1.5, P['creamD'], 0, 0)
    if slope:
        for yy in (14, 36):
            s.line([(18, yy + 10), (32, yy), (46, yy + 10)], P['pinkL'], 3, 0.3)
    s.eg()


def tile_grass(s, x, y, sc=1.0, petals=True):
    _g(s, x, y, sc)
    s.rect(0, 0, 64, 64, P['gM'])
    s.strokes(0, 0, 64, 64, 22, P['gD'], 7, 2.2, -60, 0.8)
    s.strokes(0, 0, 64, 64, 14, P['gL'], 6, 1.8, -70, 0.9)
    s.strokes(0, 0, 64, 64, 5, P['gXL'], 5, 1.6, -70, 0.9)
    if petals:
        for _ in range(7):
            s.add(f'<circle cx="{s.r.uniform(3, 61):.1f}" cy="{s.r.uniform(3, 61):.1f}" r="{s.r.uniform(0.8, 1.4):.1f}" fill="{P["gold"]}"/>')
    s.eg()


def pusher(s, x, y, sc=1.0):
    """40×56 推车：人在车左侧"""
    _g(s, x, y, sc)
    s.fillj([(16, 6), (36, 6), (36, 56), (16, 56)], P['shadow'], 0.6, 6, op=0.3)
    bike(s, 14, 4, 1.0, shadow=None)
    person_top(s, 8, 26, P['lav'], '#4A3A48', helmet=None, arms_to=[(15, 16), (15, 20)], bag=P['pinkD'])
    s.eg()


def player(s, x, y, sc=1.0):
    """32×32 主角步行"""
    _g(s, x, y, sc)
    s.ell_fill(17, 19, 12, 8, P['shadow'], 0.3)
    s.ellipse(11, 26, 3, 2.4, '#4A3E58', 1, 0.2, n=10)
    s.ellipse(21, 23, 3, 2.4, '#4A3E58', 1, 0.2, n=10)
    person_top(s, 16, 15, P['lav'], '#4A3A48', helmet=None, arms_to=[(6, 20), (26, 18)], bag=P['pinkD'])
    s.eg()
