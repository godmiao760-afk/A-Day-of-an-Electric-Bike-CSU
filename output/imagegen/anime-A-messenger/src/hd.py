# 手绘赛璐璐 SVG 工具库（Messenger / abeto 风）
import math, random, base64, io

OUT = '#3A4040'      # 描边深灰
TEAL = '#65C1BE'     # 标志青绿
TEAL2 = '#81BFBC'
MIST = '#92CCC1'
VEG_D = '#5B6B58'
VEG_DD = '#46554A'
VEG_L = '#78A194'
VEG_LL = '#9DBB9A'
CONC = '#9DA098'
CONC2 = '#A7AEA0'
CREAM = '#F2F5E8'
CREAM2 = '#E9E8CE'
RUST = '#C8553D'
ORANGE = '#E07A3F'
MUSTARD = '#E8C547'
SHADOW = '#2E5E5E'   # 冷色阴影（配透明度用）
FONT = 'Noto Sans CJK SC'

R = random.Random(11)


def seed(s):
    R.seed(s)


class Noise1D:
    """平滑一维噪声，用于线宽和抖动"""
    def __init__(self, n=64):
        self.v = [R.uniform(-1, 1) for _ in range(n)]

    def __call__(self, t):
        n = len(self.v)
        i = int(math.floor(t)) % n
        f = t - math.floor(t)
        f = (1 - math.cos(f * math.pi)) / 2
        return self.v[i] * (1 - f) + self.v[(i + 1) % n] * f


def subdivide(pts, closed, step):
    out = []
    m = len(pts)
    rng = m if closed else m - 1
    for i in range(rng):
        a = pts[i]; b = pts[(i + 1) % m]
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        k = max(1, int(d / step))
        for j in range(k):
            t = j / k
            out.append((a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, j == 0))
    if not closed:
        out.append((pts[-1][0], pts[-1][1], True))
    return out


def wobble(pts, closed=True, step=6, amp=1.0):
    sp = subdivide(pts, closed, step)
    nz = Noise1D()
    ph = R.uniform(0, 50)
    res = []
    n = len(sp)
    for i, (x, y, corner) in enumerate(sp):
        # 法线方向
        p0 = sp[(i - 1) % n] if (closed or i > 0) else sp[i]
        p1 = sp[(i + 1) % n] if (closed or i < n - 1) else sp[i]
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        a = amp * nz(ph + i * 0.35) * (0.4 if corner else 1.0)
        res.append((x + nx * a, y + ny * a))
    return res


def d_of(pts, closed=True):
    s = 'M%.1f %.1f' % pts[0] + ''.join(' L%.1f %.1f' % p for p in pts[1:])
    return s + (' Z' if closed else '')


class SVG:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.p = []
        self.defs = []

    def add(self, s):
        self.p.append(s)

    def text(self, x, y, s, size=16, fill=OUT, weight='bold', anchor='start', family=FONT, extra=''):
        s = s.replace('&', '&amp;').replace('<', '&lt;')
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{family}" font-size="{size}" '
                 f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>')

    def xtext(self, x, y, s, size, fill=CREAM, side=OUT, depth=4, anchor='start', stroke=None, sw=0, family=FONT):
        """挤出阴影的标题字"""
        for k in range(depth, 0, -1):
            self.text(x + k * 0.7, y + k, s, size, side, anchor=anchor, family=family,
                      extra=f'stroke="{side}" stroke-width="{sw}" stroke-linejoin="round"' if sw else '')
        if stroke:  # cairosvg 不支持 paint-order：先画描边层，再盖填色层
            self.text(x, y, s, size, stroke, anchor=anchor, family=family,
                      extra=f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"')
        self.text(x, y, s, size, fill, anchor=anchor, family=family)

    def otext(self, x, y, s, size, fill=CREAM, stroke=OUT, sw=3, anchor='start', weight='bold'):
        """带描边的文字（先描边后填色）"""
        self.text(x, y, s, size, stroke, weight, anchor, extra=f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"')
        self.text(x, y, s, size, fill, weight, anchor)

    def render(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}">'
                f'<defs>{"".join(self.defs)}</defs>' + '\n'.join(self.p) + '</svg>')

    def save_png(self, path, post_grain=True, scale=1):
        import cairosvg
        svg = self.render()
        with open(path.replace('.png', '.svg'), 'w', encoding='utf-8') as f:
            f.write(svg)
        cairosvg.svg2png(bytestring=svg.encode('utf-8'), write_to=path, scale=scale)
        if post_grain:
            grain(path)

    # ---------- 基本图元 ----------
    def fill(self, pts, fill, amp=0.8, step=6, opacity=1, closed=True):
        wp = wobble(pts, closed, step, amp) if amp > 0 else pts
        op = f' fill-opacity="{opacity}"' if opacity < 1 else ''
        self.add(f'<path d="{d_of(wp)}" fill="{fill}"{op}/>')
        return wp

    def ink(self, pts, closed=True, w=2.0, var=0.45, color=OUT, amp=0.8, step=6, chunk=4, opacity=1):
        """粗细不均的手绘描边：分段绘制，每段线宽不同"""
        wp = wobble(pts, closed, step, amp) if amp > 0 else list(pts)
        if closed:
            wp = wp + [wp[0]]
        nz = Noise1D()
        ph = R.uniform(0, 40)
        i = 0
        op = f' stroke-opacity="{opacity}"' if opacity < 1 else ''
        segs = []
        while i < len(wp) - 1:
            j = min(len(wp), i + chunk + 1)
            seg = wp[i:j]
            ww = max(0.3, w * (1 + var * nz(ph + i * 0.25)))
            segs.append(f'<path d="{d_of(seg, False)}" fill="none" stroke="{color}" stroke-width="{ww:.2f}" '
                        f'stroke-linecap="round" stroke-linejoin="round"{op}/>')
            i = j - 1
        self.add(''.join(segs))
        return wp

    def shape(self, pts, fill, w=2.0, amp=0.8, step=6, var=0.45, color=OUT, opacity=1):
        wp = wobble(pts, True, step, amp) if amp > 0 else pts
        op = f' fill-opacity="{opacity}"' if opacity < 1 else ''
        self.add(f'<path d="{d_of(wp)}" fill="{fill}"{op}/>')
        if w > 0:
            self.ink(wp, True, w, var, color, amp=0.25, step=step * 2)
        return wp

    def line(self, a, b, w=2, color=OUT, amp=0.6, var=0.4, step=8, opacity=1):
        self.ink([a, b], False, w, var, color, amp, step, opacity=opacity)

    def sag(self, a, b, drop, w=1.2, color=OUT, opacity=0.8):
        """电线：下垂曲线"""
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2 + drop
        self.add(f'<path d="M{a[0]:.1f} {a[1]:.1f} Q{mx:.1f} {my:.1f} {b[0]:.1f} {b[1]:.1f}" fill="none" '
                 f'stroke="{color}" stroke-width="{w}" stroke-opacity="{opacity}"/>')


def rrect(x, y, w, h, r=4, n=4):
    """圆角矩形点列"""
    r = min(r, w / 2, h / 2)
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def rect(x, y, w, h):
    return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]


def ellipse(cx, cy, rx, ry, n=18):
    return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]


def jag(cx, cy, r, n=None, rough=0.28, sy=1.0):
    """不规则笔刷团块"""
    n = n or R.randint(11, 17)
    pts = []
    off = R.uniform(0, 6.28)
    for k in range(n):
        a = off + 2 * math.pi * k / n + R.uniform(-0.12, 0.12)
        rr = r * (1 + R.uniform(-rough, rough * 0.6)) * (0.82 if k % 2 else 1.0)
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a) * sy))
    return pts


# ---------- 复合元素 ----------
def speckles(s, x0, y0, w, h, n, colors, rmin=0.6, rmax=1.8, opacity=0.5):
    out = []
    for _ in range(n):
        x = R.uniform(x0, x0 + w); y = R.uniform(y0, y0 + h)
        c = R.choice(colors)
        if R.random() < 0.6:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{R.uniform(rmin, rmax):.1f}" fill="{c}" fill-opacity="{opacity}"/>')
        else:  # 小碎片
            a = R.uniform(0, 6.28); L = R.uniform(rmax, rmax * 2.4)
            out.append(f'<path d="M{x:.1f} {y:.1f} L{x + L * math.cos(a):.1f} {y + L * math.sin(a):.1f}" stroke="{c}" '
                       f'stroke-width="{R.uniform(0.8, 1.6):.1f}" stroke-linecap="round" stroke-opacity="{opacity}"/>')
    s.add(''.join(out))


def brush_strokes(s, x0, y0, w, h, n, color, lmin=4, lmax=10, wmin=1, wmax=2.5, ang=None, opacity=0.35):
    out = []
    for _ in range(n):
        x = R.uniform(x0, x0 + w); y = R.uniform(y0, y0 + h)
        a = ang if ang is not None else R.uniform(0, 6.28)
        a += R.uniform(-0.3, 0.3)
        L = R.uniform(lmin, lmax)
        out.append(f'<path d="M{x:.1f} {y:.1f} q{L * 0.5 * math.cos(a) + R.uniform(-1, 1):.1f} {L * 0.5 * math.sin(a) + R.uniform(-1, 1):.1f} '
                   f'{L * math.cos(a):.1f} {L * math.sin(a):.1f}" fill="none" stroke="{color}" stroke-width="{R.uniform(wmin, wmax):.1f}" '
                   f'stroke-linecap="round" stroke-opacity="{opacity}"/>')
    s.add(''.join(out))


def tree(s, cx, cy, r, dark=VEG_D, mid=VEG_L, light=VEG_LL, outline=OUT, shadow=True, w=2.2, night=False):
    """俯视樟树：不规则团簇 + 2~3 阶硬光影（光从左上）"""
    if shadow:
        for b in [jag(cx + r * 0.35 + R.uniform(-r * .3, r * .3), cy + r * 0.4 + R.uniform(-r * .3, r * .3), r * R.uniform(.45, .65)) for _ in range(6)]:
            s.fill(b, SHADOW, amp=0, opacity=0.28 if not night else 0.4)
    blobs = []
    for k in range(7):
        a = 2 * math.pi * k / 7 + R.uniform(-.3, .3)
        d = r * R.uniform(0.35, 0.55)
        blobs.append(jag(cx + d * math.cos(a), cy + d * math.sin(a), r * R.uniform(0.42, 0.58)))
    blobs.append(jag(cx, cy, r * 0.6))
    for b in blobs:  # 外轮廓（粗线，下一层填色盖住内部线）
        s.ink(b, True, w * 2, 0.5, outline, amp=0.4, step=5)
    for b in blobs:
        s.fill(b, dark, amp=0)
    # 中间调
    for k in range(6):
        a = 2 * math.pi * k / 6 + R.uniform(-.4, .4)
        d = r * R.uniform(0.15, 0.45)
        s.fill(jag(cx - r * 0.12 + d * math.cos(a), cy - r * 0.14 + d * math.sin(a), r * R.uniform(0.28, 0.42)), mid, amp=0)
    # 亮部
    for k in range(4):
        s.fill(jag(cx - r * R.uniform(0.15, 0.45), cy - r * R.uniform(0.15, 0.45), r * R.uniform(0.12, 0.22)), light, amp=0)
    # 叶片笔触
    brush_strokes(s, cx - r * .7, cy - r * .7, r * 1.3, r * 1.3, int(r * 0.9), dark, 3, 7, 1, 2, opacity=0.55)
    brush_strokes(s, cx - r * .6, cy - r * .7, r * .9, r * .8, int(r * 0.4), light, 2, 5, 1, 1.6, opacity=0.6)


def grain(path, amount=7):
    """后处理：纸面颗粒"""
    from PIL import Image
    import numpy as np
    im = Image.open(path).convert('RGB')
    a = np.asarray(im).astype(np.int16)
    rs = np.random.RandomState(3)
    n = rs.normal(0, amount, a.shape[:2])[..., None]
    a = np.clip(a + n, 0, 255).astype(np.uint8)
    Image.fromarray(a).save(path)


def png_data_uri(path):
    with open(path, 'rb') as f:
        return 'data:image/png;base64,' + base64.b64encode(f.read()).decode()


def tw(text, size):
    """估算文字宽度"""
    w = 0
    for ch in text:
        w += size * (0.58 if ord(ch) < 128 else 1.0)
    return w
