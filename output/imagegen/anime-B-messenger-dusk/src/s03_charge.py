# 03-charge 夜间充电 · 22:47 · 深靛 + 墨绿 + 霓虹青小点缀
import os, sys
from lib import P, SVG, render, rrect_pts
import sprites as S

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def night_dorm(s, x0, y0, cols, floors, fw=46, fh=22):
    W, H = cols * fw, floors * fh
    s.shape([(x0 - 4, y0 - 12), (x0 + W + 4, y0 - 12), (x0 + W + 4, y0), (x0 - 4, y0)], P['indigoD'], 2, 0.6, ink='#161B2E')
    s.shape([(x0, y0), (x0 + W, y0), (x0 + W, y0 + H), (x0, y0 + H)], P['indigoL'], 2.4, 0.7, ink='#1B2138')
    for f in range(floors):
        for c in range(cols):
            wx, wy = x0 + c * fw, y0 + f * fh
            lit = s.r.random() < 0.62
            col = s.r.choice([P['lamp'], P['goldL'], '#F5D08A', '#FFE3A8']) if lit else '#2A3150'
            if lit:
                s.ell_fill(wx + fw / 2, wy + 8, fw * 0.5, 9, P['lamp'], 0.12)
            s.box(wx + 6, wy + 3, fw - 12, 10, col, 1.1, 0.3, ink='#1B2138')
            if lit and s.r.random() < 0.4:  # 窗帘半拉
                s.box(wx + 6, wy + 3, (fw - 12) * 0.4, 10, P['pink'], 0, 0.2, op=0.8)
            s.box(wx + 3, wy + 13, fw - 6, 8, '#3B4670', 1.2, 0.3, ink='#1B2138')
            if s.r.random() < 0.4:  # 晾的衣服剪影
                for k in range(s.r.randint(1, 3)):
                    s.box(wx + 8 + k * 10, wy + 5, 6, 8, '#3A3458', 0.8, 0.2, ink='#1B2138')
            if s.r.random() < 0.35:
                ax = wx + (fw - 13 if s.r.random() < 0.5 else 1)
                s.box(ax, wy + 14, 12, 7, '#5A6490', 1, 0.2, ink='#1B2138')
    # 楼门：门禁牌
    ex = x0 + W / 2 - 44
    ey = y0 + H - fh
    s.box(ex, ey + 1, 88, fh - 1, P['goldL'], 2, 0.4, ink='#1B2138')
    s.ell_fill(ex + 44, ey + fh, 90, 26, P['lamp'], 0.18)
    s.fillj([(x0 + W - 12, y0), (x0 + W, y0), (x0 + W, y0 + H), (x0 + W - 12, y0 + H)], '#1B2138', 0.3, 10, op=0.35)


def draw(path_png, seed=31, tag=''):
    s = SVG(960, 540, seed=seed, bg=P['indigo'])
    # ---- 夜空 + 远山（岳麓山深色剪影）----
    s.rect(0, 0, 960, 60, P['indigoD'])
    s.specks(0, 0, 960, 60, 40, P['lavL'], 0.5, 1.0, 0.6)
    s.ell_fill(880, 26, 14, 14, '#EDE3C8', 0.95)  # 月亮
    s.ell_fill(885, 22, 12, 12, P['indigoD'], 1)
    pts = [(0, 90)] + [(x, 62 - 22 * max(0, 1 - abs(x - 300) / 260) - 12 * max(0, 1 - abs(x - 760) / 200) + s.r.uniform(-1, 1)) for x in range(0, 961, 16)] + [(960, 90)]
    s.fillj(pts, '#27304C', 0.6, 14)
    # ---- 宿舍楼 ----
    night_dorm(s, 40, 30, 19, 4)
    # 门禁提示牌
    s.slab(392, 58, 176, 26, P['indigoD'], '#161B2E', depth=4, r=6, lw=2)
    s.text(480, 76, '升华公寓 · 门禁 23:00', 13, P['goldL'], anchor='middle')
    # ---- 地面 ----
    s.rect(0, 118, 960, 422, '#34405E')
    s.fillj([(0, 118), (960, 118), (960, 128), (0, 128)], '#232B45', 0.3, 20)
    s.strokes(0, 130, 960, 410, 90, '#2B3552', 16, 2.5, 5, 0.7)
    s.specks(0, 130, 960, 410, 140, '#46527A', 0.5, 1.4, 0.7)
    # 地砖缝
    for y in range(150, 540, 44):
        s.line([(0, y), (960, y)], '#2B3552', 1, 0.6, op=0.7)
    # ---- 路灯昏黄光池 ----
    lamps = [(92, 150), (880, 150)]
    for (lx, ly) in lamps:
        s.fillj(s.blob_pts(lx + 10, ly + 150, 150, 20, 0.03, 0.08, sy=0.55), P['lamp'], 1, 20, op=0.13, smooth=True)
        s.fillj(s.blob_pts(lx + 10, ly + 140, 90, 18, 0.03, 0.08, sy=0.55), P['lamp'], 1, 20, op=0.12, smooth=True)
    # ---- 充电桩一排 + 雨棚 ----
    y_p = 140
    states = ['occupied', 'broken', 'occupied', 'qrfail', 'broken', 'plugged', 'free', 'occupied']
    xs = [150 + i * 86 for i in range(8)]
    SC = 1.5
    # 桩后面的横杆
    s.box(120, y_p + 14, 720, 8, '#4A5680', 1.8, 0.4, ink='#161B2E')
    for i, (x, st) in enumerate(zip(xs, states)):
        S.pile(s, x - 16 * SC, y_p, SC, st)
        # 下方停车位线
        s.line([(x - 36, y_p + 70), (x - 36, y_p + 176)], '#566392', 1.4, 0.5)
        # 被占的车位停着别人的车
        if st == 'occupied':
            S.other_bike(s, x - 12 * SC, y_p + 82, SC, variant=i, shadow=(3, 4))
            s.line([(x + 14, y_p + 52), (x + 18, y_p + 84), (x + 6, y_p + 96)], '#1B2138', 2.2, 0.4)
        elif st == 'plugged':
            # 自己的车插上 → 绿光
            s.ell_fill(x, y_p + 110, 60, 70, P['neon'], 0.12)
            S.bike(s, x - 12 * SC, y_p + 82, SC, shadow=(3, 4), glow=P['neon'])
            # 主角站在自己车左边，扶着车把（推车到位）
            S.player(s, x + 22, y_p + 120, 1.5)
            s.line([(x + 14, y_p + 52), (x + 20, y_p + 86), (x + 8, y_p + 104)], P['neonD'], 2.6, 0.4)
            s.line([(x + 14, y_p + 52), (x + 20, y_p + 86), (x + 8, y_p + 104)], P['neon'], 1.2, 0.4)
        # 状态小标签
        lab = {'occupied': ('被占', P['lamp']), 'broken': ('坏了', '#8A84A0'), 'qrfail': ('扫码失败', P['red']),
               'plugged': ('充电中', P['neon']), 'free': ('空闲', P['neon'])}[st]
        s.text(x, y_p - 8, lab[0], 11, lab[1], anchor='middle', stroke='#161B2E', sw=3.5)
    s.line([(xs[-1] + 50, y_p + 70), (xs[-1] + 50, y_p + 176)], '#566392', 1.4, 0.5)
    # 路灯杆
    for (lx, ly) in lamps:
        s.ell_fill(lx + 4, ly + 4, 22, 22, P['lamp'], 0.18)
        s.ell_fill(lx + 4, ly + 4, 12, 12, P['lamp'], 0.35)
        s.ellipse(lx + 4, ly + 4, 7, 7, '#FFE7A0', 1.8, 0.3, n=12, ink='#161B2E')
    # ---- 墨绿樟树（夜）----
    npal = ('#1E3431', P['night_g'], '#3E6259', '#557A6C')
    s.tree(28, 300, 66, pal=npal, lx=0.3, ly=-0.8)
    s.tree(40, 480, 58, pal=npal, lx=0.3, ly=-0.8)
    s.tree(936, 330, 62, pal=npal, lx=-0.3, ly=-0.8, osman=True)
    s.tree(944, 500, 50, pal=npal, lx=-0.3, ly=-0.8)
    # ---- 主角推车（走在桩前的空地上，朝空闲桩方向）----
    # 一辆被推到一边的车（左下，小叙事）
    S.other_bike(s, 120, 380, 1.5, variant=2, rot=-80, shadow=(3, 4))
    # 萤火 / 飞虫 & 桂花
    for _ in range(18):
        s.add(f'<circle cx="{s.r.uniform(60, 900):.1f}" cy="{s.r.uniform(190, 520):.1f}" r="{s.r.uniform(0.8, 1.5):.1f}" fill="{P["goldL"]}" opacity="0.8"/>')
    # ---- 暗角（夜氛围，硬边分两阶）----
    s.fillj([(0, 470), (960, 470), (960, 540), (0, 540)], '#161B2E', 0.4, 30, op=0.25)
    # ---- 弹窗（实体、带厚度）----
    s.rect(0, 318, 960, 222, '#10142A', op=0.28)
    bx, by, bw, bh = 250, 336, 460, 146
    s.slab(bx, by, bw, bh, P['cream'], P['lavL'], depth=8, r=14, lw=2.8)
    # 顶部小标签
    s.slab(bx + 22, by - 16, 128, 30, P['neon'], P['neonD'], depth=4, r=8, lw=2)
    s.shape([(bx + 44, by - 10), (bx + 38, by + 1), (bx + 43, by + 1), (bx + 40, by + 9), (bx + 49, by - 3), (bx + 44, by - 3), (bx + 47, by - 10)], P['lamp'], 1.2, 0.2)
    s.text(bx + 96, by + 5, '已插上', 14, P['indigo'], anchor='middle')
    s.text(bx + bw / 2, by + 44, '终于插上了。守着它，还是先回宿舍？', 19, P['ink'], anchor='middle')
    s.text(bx + bw / 2, by + 68, '守着每分钟 +5%　·　回宿舍 50% 充满，否则可能被拔线', 12, P['ink2'], weight='normal', anchor='middle')
    # 两个选项横排：左高亮
    ow, oh = 170, 44
    o1x, o2x, oy = bx + 50, bx + bw - 50 - ow, by + 84
    s.slab(o1x, oy, ow, oh, P['lamp'], P['lampD'], depth=6, r=10, lw=2.6)
    s.text(o1x + ow / 2, oy + 29, '守着它', 19, P['ink'], anchor='middle')
    s.shape([(o1x - 20, oy + 14), (o1x - 8, oy + 22), (o1x - 20, oy + 30)], P['ink'], 1.4, 0.2)  # 选择箭头
    s.slab(o2x, oy, ow, oh, P['creamD'], '#B8AEC4', depth=6, r=10, lw=2.2)
    s.text(o2x + ow / 2, oy + 29, '回宿舍', 19, P['ink2'], anchor='middle')
    # ---- 气泡（主角头顶，在弹窗下方可见）----
    s.bubble(640, 232, '可别再被拔了……', tail_x=640, tail_y=266, size=14, w=136)
    # ---- UI ----
    s.battery(18, 16, 21)
    s.clock(810, 14, '22:47', sub='门禁 23:00', night=True)
    s.hint([('A/D', '切换'), ('F', '确认')], y=496)
    svg = os.path.join(OUT, 'src', 'tmp', f'03{tag}.svg')
    s.save(svg)
    render(svg, path_png)
    return path_png


if __name__ == '__main__':
    tag = sys.argv[1] if len(sys.argv) > 1 else ''
    print(draw(os.path.join(OUT, f'03-charge{tag}.png'), tag=tag))
