# 风格 B · Messenger 技法 × 长沙黄昏/桂花秋 —— 共用绘制库
# 手绘抖动描边、2~3 阶硬光影、笔刷树冠、有厚度的实体 UI
import math, random, base64

# ---------- 调色板 ----------
P = dict(
    ink='#3E3550',      # 描边：深紫灰（不用纯黑）
    ink2='#5A4E6E',     # 细结构线
    lav='#8E7FA8',      # 灰紫（主色）
    lavL='#B3A7C8',     # 灰紫亮
    mist='#DCD3E6',     # 晨雾淡紫
    pink='#D9A5A0',     # 暮粉（主色）
    pinkL='#EBC6BC',
    pinkD='#B5807E',
    gD='#2F4A3E',       # 樟树墨绿 暗
    gM='#48664F',       # 中
    gL='#6E8B64',       # 亮
    gXL='#93A77C',
    lamp='#F2C14E',     # 路灯黄 / 主角车
    lampD='#C98F2E',
    gold='#E3A73A',     # 桂花金
    goldL='#F7D98A',
    cream='#F3EDE2',    # 米白（不用纯白）
    creamD='#D8CFD6',
    road='#6F6580',
    roadD='#5B5270',
    roadL='#857A93',
    rust='#C8623F',     # 危险点缀（外卖车 / 锥桶）
    rustD='#9C4632',
    indigo='#2E3A59',   # 夜
    indigoD='#232B45',
    indigoL='#45517A',
    night_g='#2F4F4A',
    neon='#4FE3C1',     # 霓虹青
    neonD='#2BA88E',
    red='#D8645C',
    shadow='#4B3F66',   # 投影色（往冷紫偏）
)
FONT = "Noto Sans CJK SC"


class SVG:
    def __init__(self, w, h, seed=1, bg=None):
        self.w, self.h = w, h
        self.o = []
        self.defs = []
        self.r = random.Random(seed)
        if bg:
            self.rect(0, 0, w, h, bg)

    # ---------- 基础 ----------
    def add(self, s):
        self.o.append(s)

    def rect(self, x, y, w, h, fill, op=1, rx=0):
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" opacity="{op}"/>')

    def g(self, tf=''):
        self.add(f'<g transform="{tf}">')

    def eg(self):
        self.add('</g>')

    def save(self, path):
        s = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
             f'width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
             f'<defs>{"".join(self.defs)}</defs>' + ''.join(self.o) + '</svg>')
        open(path, 'w', encoding='utf-8').write(s)
        return s

    # ---------- 手绘抖动 ----------
    def jit(self, pts, amp=1.0, seg=10, closed=True):
        """把多边形每条边细分，并在法线方向加随机抖动"""
        out = []
        n = len(pts)
        m = n if closed else n - 1
        for i in range(m):
            x1, y1 = pts[i]
            x2, y2 = pts[(i + 1) % n]
            L = math.hypot(x2 - x1, y2 - y1)
            k = max(1, int(L / seg))
            nx, ny = (-(y2 - y1) / L, (x2 - x1) / L) if L else (0, 0)
            for j in range(k):
                t = j / k
                a = self.r.uniform(-amp, amp) if j else self.r.uniform(-amp, amp) * 0.4
                out.append((x1 + (x2 - x1) * t + nx * a, y1 + (y2 - y1) * t + ny * a))
        if not closed:
            out.append(pts[-1])
        return out

    @staticmethod
    def d_line(pts, closed=True):
        s = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
        return s + (' Z' if closed else '')

    @staticmethod
    def d_smooth(pts, closed=True):
        """中点二次曲线，适合团块"""
        n = len(pts)
        mid = lambda a, b: ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
        m0 = mid(pts[-1], pts[0]) if closed else pts[0]
        s = f'M{m0[0]:.1f},{m0[1]:.1f}'
        rng = range(n) if closed else range(n - 1)
        for i in rng:
            p = pts[i]
            m = mid(pts[i], pts[(i + 1) % n])
            s += f' Q{p[0]:.1f},{p[1]:.1f} {m[0]:.1f},{m[1]:.1f}'
        return s + (' Z' if closed else '')

    def path(self, d, fill='none', stroke=None, sw=0, op=1, extra=''):
        st = f' stroke="{stroke}" stroke-width="{sw:.2f}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ''
        self.add(f'<path d="{d}" fill="{fill}" opacity="{op}"{st} {extra}/>')

    def shape(self, pts, fill, lw=2.0, amp=0.9, seg=10, ink=None, smooth=False, op=1, double=True):
        """实心 + 手绘描边（两遍不同抖动 → 粗细不均）"""
        ink = ink or P['ink']
        jp = self.jit(pts, amp, seg)
        d = self.d_smooth(jp) if smooth else self.d_line(jp)
        self.path(d, fill=fill, op=op)
        if lw > 0:
            self.path(d, stroke=ink, sw=lw, op=op)
            if double:
                jp2 = self.jit(pts, amp * 1.1, seg * 1.3)
                d2 = self.d_smooth(jp2) if smooth else self.d_line(jp2)
                self.path(d2, stroke=ink, sw=lw * 0.45, op=0.7 * op)

    def fillj(self, pts, fill, amp=0.8, seg=10, op=1, smooth=False):
        jp = self.jit(pts, amp, seg)
        self.path(self.d_smooth(jp) if smooth else self.d_line(jp), fill=fill, op=op)

    def line(self, pts, stroke=None, sw=1.5, amp=0.6, seg=10, op=1):
        stroke = stroke or P['ink']
        jp = self.jit(pts, amp, seg, closed=False)
        self.path(self.d_line(jp, False), stroke=stroke, sw=sw, op=op)

    def box(self, x, y, w, h, fill, lw=2, amp=0.8, op=1, **k):
        self.shape([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], fill, lw, amp, op=op, **k)

    def rbox(self, x, y, w, h, r, fill, lw=2, amp=0.6, op=1, stroke=None):
        pts = rrect_pts(x, y, w, h, r)
        self.shape(pts, fill, lw, amp, seg=8, op=op, ink=stroke)

    def ellipse(self, cx, cy, rx, ry, fill, lw=1.8, amp=0.5, n=18, op=1, ink=None):
        pts = [(cx + rx * math.cos(2 * math.pi * i / n), cy + ry * math.sin(2 * math.pi * i / n)) for i in range(n)]
        self.shape(pts, fill, lw, amp, seg=100, smooth=True, op=op, ink=ink)

    def ell_fill(self, cx, cy, rx, ry, fill, op=1):
        self.add(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" opacity="{op}"/>')

    # ---------- 笔刷纹理 ----------
    def specks(self, x, y, w, h, n, color, rmin=0.6, rmax=1.8, op=0.5):
        for _ in range(n):
            px, py = self.r.uniform(x, x + w), self.r.uniform(y, y + h)
            rr = self.r.uniform(rmin, rmax)
            self.add(f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{rr * 1.6:.1f}" ry="{rr:.1f}" '
                     f'transform="rotate({self.r.uniform(0, 180):.0f} {px:.1f} {py:.1f})" fill="{color}" opacity="{op}"/>')

    def strokes(self, x, y, w, h, n, color, L=8, sw=2, ang=-20, op=0.5):
        """干笔刷短笔触"""
        for _ in range(n):
            px, py = self.r.uniform(x, x + w), self.r.uniform(y, y + h)
            a = math.radians(ang + self.r.uniform(-15, 15))
            l = L * self.r.uniform(0.5, 1.2)
            self.add(f'<path d="M{px:.1f},{py:.1f} q{l / 2 * math.cos(a) + 1:.1f},{l / 2 * math.sin(a) - 1:.1f} '
                     f'{l * math.cos(a):.1f},{l * math.sin(a):.1f}" stroke="{color}" stroke-width="{sw * self.r.uniform(0.6, 1.2):.1f}" '
                     f'stroke-linecap="round" fill="none" opacity="{op}"/>')

    def blob_pts(self, cx, cy, r, n=22, teeth=0.12, wob=0.12, sy=1.0):
        ph = self.r.uniform(0, 6.28)
        pts = []
        for i in range(n):
            a = 2 * math.pi * i / n
            rr = r * (1 + wob * math.sin(3 * a + ph) + self.r.uniform(-wob, wob) * 0.6)
            if i % 2:
                rr *= (1 - teeth)
            pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * sy))
        return pts

    def tree(self, cx, cy, r, lx=-0.45, ly=-0.55, osman=False, shadow=(0.0, 0.0), sh_op=0.3, pal=None, lw=2.2):
        """笔刷团簇树冠：投影 → 暗底(描边) → 中间调 → 亮部小团 → 暗部笔触"""
        pal = pal or (P['gD'], P['gM'], P['gL'], P['gXL'])
        dD, dM, dL, dXL = pal
        sx, sy = shadow
        if sx or sy:  # 长投影
            steps = 6
            for i in range(steps):
                t = (i + 1) / steps
                self.fillj(self.blob_pts(cx + sx * t, cy + sy * t, r * 0.95, 16, 0.05, 0.1), P['shadow'], 1, 20, op=sh_op / steps * 1.6, smooth=True)
        base = self.blob_pts(cx, cy, r, 26, 0.14, 0.1)
        self.shape(base, dD, lw, 0.8, seg=30, smooth=True)
        self.fillj(self.blob_pts(cx + lx * r * 0.22, cy + ly * r * 0.22, r * 0.78, 20, 0.16, 0.14), dM, 0.6, 30, smooth=True)
        for i in range(3):
            a = math.atan2(ly, lx) + self.r.uniform(-0.8, 0.8)
            d = r * self.r.uniform(0.25, 0.5)
            self.fillj(self.blob_pts(cx + math.cos(a) * d, cy + math.sin(a) * d, r * self.r.uniform(0.22, 0.34), 14, 0.2, 0.15), dL, 0.5, 30, smooth=True)
        a = math.atan2(ly, lx)
        self.fillj(self.blob_pts(cx + math.cos(a) * r * 0.5, cy + math.sin(a) * r * 0.5, r * 0.14, 10, 0.2, 0.15), dXL, 0.4, 30, smooth=True)
        # 暗部笔触
        for _ in range(int(r / 4)):
            a = math.atan2(-ly, -lx) + self.r.uniform(-1.2, 1.2)
            d = r * self.r.uniform(0.35, 0.8)
            px, py = cx + math.cos(a) * d, cy + math.sin(a) * d
            self.add(f'<path d="M{px:.1f},{py:.1f} q3,-2 {self.r.uniform(4, 8):.1f},{self.r.uniform(-2, 2):.1f}" stroke="{dD}" '
                     f'stroke-width="{self.r.uniform(1.5, 2.8):.1f}" stroke-linecap="round" fill="none" opacity="0.9"/>')
        if osman:  # 桂花：金色小点簇
            for _ in range(int(r * 0.9)):
                a = self.r.uniform(0, 6.28)
                d = r * math.sqrt(self.r.uniform(0.05, 0.85))
                px, py = cx + math.cos(a) * d, cy + math.sin(a) * d
                c = self.r.choice([P['gold'], P['goldL'], P['gold']])
                self.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{self.r.uniform(0.9, 1.9):.1f}" fill="{c}"/>')

    # ---------- 文字 ----------
    def text(self, x, y, s, size=16, fill=None, weight='bold', anchor='start', stroke=None, sw=0, op=1, font=FONT, ls=0):
        fill = fill or P['ink']
        esc = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        base = f'x="{x:.1f}" y="{y:.1f}" font-family="{font}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{ls}" opacity="{op}"'
        if stroke:
            self.add(f'<text {base} fill="{stroke}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round">{esc}</text>')
        self.add(f'<text {base} fill="{fill}">{esc}</text>')

    # ---------- 实体 UI（有厚度） ----------
    def slab(self, x, y, w, h, face, side, depth=5, r=8, lw=2.4, amp=0.5):
        self.fillj(rrect_pts(x + 2, y + depth + 3, w, h, r), P['shadow'], 0.4, 10, op=0.35)
        self.rbox(x, y + depth, w, h, r, side, lw, amp)
        self.rbox(x, y, w, h, r, face, lw, amp)

    def keycap(self, x, y, k, w=26, face=None, side=None, size=15):
        face = face or P['cream']
        side = side or P['lavL']
        self.slab(x, y, w, 24, face, side, depth=4, r=5, lw=1.8)
        self.text(x + w / 2, y + 18, k, size, P['ink'], anchor='middle')

    def hint(self, items, y=500, cx=None, dark=True):
        """底部操作提示：[键] 说明 · [键] 说明"""
        cx = cx or self.w / 2
        # 估算宽度
        tw = 0
        for k, t in items:
            tw += max(26, 12 * len(k) + 12) + 8 + 16 * len(t) + 26
        tw += 20
        x0 = cx - tw / 2
        self.slab(x0, y, tw, 34, P['ink'] if dark else P['cream'], '#2A2338' if dark else P['creamD'], depth=4, r=17, lw=2)
        x = x0 + 16
        for i, (k, t) in enumerate(items):
            kw = max(26, 12 * len(k) + 12)
            self.keycap(x, y + 4, k, kw)
            x += kw + 8
            self.text(x, y + 23, t, 15, P['cream'] if dark else P['ink'], weight='bold')
            x += 16 * len(t) + 8
            if i < len(items) - 1:
                self.text(x + 1, y + 23, '·', 16, P['lavL'])
                x += 18

    def battery(self, x, y, pct, label=None, warn=False):
        w = 196
        self.slab(x, y, w, 40, P['cream'], P['lavL'], depth=5, r=9)
        # 闪电
        self.shape([(x + 20, y + 7), (x + 12, y + 22), (x + 19, y + 22), (x + 15, y + 34), (x + 27, y + 16), (x + 20, y + 16), (x + 24, y + 7)],
                   P['lamp'], 1.6, 0.3)
        # 电池壳
        bx, by, bw, bh = x + 34, y + 10, 94, 20
        self.rbox(bx, by, bw, bh, 4, P['creamD'], 2, 0.4)
        self.box(bx + bw + 1, by + 6, 5, 8, P['ink'], 0, 0.2)
        c = P['red'] if pct < 25 else (P['lamp'] if pct < 50 else P['neonD'])
        segs = 5
        fill = pct / 100 * segs
        for i in range(segs):
            sx = bx + 4 + i * 17.6
            if i + 1 <= fill:
                self.box(sx, by + 4, 14.5, 12, c, 0, 0.3)
                self.box(sx, by + 11, 14.5, 5, P['ink'], 0, 0.2, op=0.18)
            elif i < fill:
                self.box(sx, by + 4, 14.5 * (fill - i), 12, c, 0, 0.3)
        self.text(x + w - 12, y + 27, f'{pct}%', 17, P['ink'], anchor='end')
        if label:
            self.text(x + 4, y + 66, label, 12, P['cream'], stroke=P['ink'], sw=3.5)

    def heart(self, x, y, s=1.0, full=True):
        pts = []
        for i in range(24):
            t = 2 * math.pi * i / 24
            hx = 16 * math.sin(t) ** 3
            hy = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
            pts.append((x + hx * s * 0.62, y + hy * s * 0.62))
        # 厚度
        self.fillj([(px + 1, py + 3) for px, py in pts], P['shadow'], 0.3, 50, op=0.35, smooth=True)
        self.shape(pts, P['red'] if full else P['creamD'], 1.8, 0.3, seg=50, smooth=True)
        if full:
            self.ell_fill(x - 4 * s, y - 3 * s, 2.6 * s, 1.8 * s, P['pinkL'], 0.9)

    def clock(self, x, y, t, sub=None, signal=None, night=False):
        w = 132
        face = P['cream']
        self.slab(x, y, w, 44, face, P['lavL'] if not night else P['indigoL'], depth=5, r=9)
        # 表盘小图标
        self.ellipse(x + 20, y + 22, 10, 10, P['pinkL'] if not night else P['lavL'], 1.6, 0.3)
        self.line([(x + 20, y + 22), (x + 20, y + 15)], sw=1.8, amp=0.1)
        self.line([(x + 20, y + 22), (x + 25, y + 24)], sw=1.8, amp=0.1)
        self.text(x + 82, y + 31, t, 25, P['ink'], anchor='middle', font='DejaVu Sans Mono')
        if signal is not None:
            sx = x - 58
            self.slab(sx, y, 50, 44, face, P['lavL'], depth=5, r=9)
            for i in range(4):
                h = 7 + i * 6
                on = i < signal
                self.box(sx + 9 + i * 9, y + 36 - h, 6, h, P['neonD'] if on else P['creamD'], 1.3, 0.2)
        if sub:
            self.slab(x + 10, y + 56, w - 10, 26, P['red'] if night else P['pink'], P['rustD'], depth=4, r=7, lw=2)
            self.text(x + 10 + (w - 10) / 2, y + 74, sub, 14, P['cream'], anchor='middle')

    def bubble(self, x, y, text, tail_x=None, tail_y=None, size=16, w=None, dark=False):
        w = w or (len(text) * size + 30)
        h = size + 22
        face = P['cream']
        tail_x = tail_x if tail_x is not None else x + w / 2
        tail_y = tail_y if tail_y is not None else y + h + 14
        # 投影
        self.fillj(rrect_pts(x + 3, y + 5, w, h, 12), P['shadow'], 0.4, 10, op=0.3)
        pts = rrect_pts(x, y, w, h, 12)
        # 尾巴并进轮廓
        tb = min(max(tail_x, x + 18), x + w - 30)
        tail = [(tb + 14, y + h), (tail_x, tail_y), (tb, y + h)]
        # 找底边插入点：rrect_pts 底边是从右到左
        full = []
        inserted = False
        for i, p in enumerate(pts):
            full.append(p)
            if not inserted and i + 1 < len(pts) and abs(p[1] - (y + h)) < 0.01 and abs(pts[i + 1][1] - (y + h)) < 0.01 and p[0] > tb + 14 >= pts[i + 1][0]:
                full += tail
                inserted = True
        if not inserted:
            full = pts[:] + []
        self.shape(full, face, 2.4, 0.6, seg=12)
        self.text(x + w / 2, y + h / 2 + size * 0.36, text, size, P['ink'], anchor='middle')


def rrect_pts(x, y, w, h, r, n=4):
    """圆角矩形点列（顺时针：上边左→右，右边，下边右→左，左边）"""
    r = min(r, w / 2, h / 2)
    pts = []
    corners = [(x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)]
    # 上边起点
    pts.append((x + r, y))
    for i, (cx, cy, a0) in enumerate(corners):
        if i == 0:
            pts.append((x + w - r, y))
        for k in range(1, n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        if i == 0:
            pts.append((x + w, y + h - r))
        elif i == 1:
            pts.append((x + r, y + h))
        elif i == 2:
            pts.append((x, y + r))
    return pts


def png_b64(path):
    return 'data:image/png;base64,' + base64.b64encode(open(path, 'rb').read()).decode()


def render(svg_path, png_path, scale=1):
    import cairosvg
    cairosvg.svg2png(url=svg_path, write_to=png_path, scale=scale)
