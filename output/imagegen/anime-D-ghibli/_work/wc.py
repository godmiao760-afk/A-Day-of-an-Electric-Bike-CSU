# 水彩绘本渲染管线：SVG(cairosvg) -> numpy 水彩化（扭曲/边缘积色/斑驳/颗粒/晕开/自动铅笔描边）-> 纸纹
import io, numpy as np, cairosvg
from PIL import Image

SANS = "Noto Sans CJK SC"; SERIF = "Noto Serif CJK SC"

def doc(w, h, body, defs=''):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>{defs}</defs>{body}</svg>')

def render(body, w, h, S=2, defs=''):
    png = cairosvg.svg2png(bytestring=doc(w, h, body, defs).encode('utf-8'),
                           output_width=int(w*S), output_height=int(h*S))
    im = Image.open(io.BytesIO(png)).convert('RGBA')
    return np.asarray(im).astype(np.float32)/255.0

# ---------- 噪声 ----------
def vnoise(H, W, cell, rng):
    if cell <= 1.01:
        return rng.random((H, W)).astype(np.float32)
    gh = int(np.ceil(H/cell))+3; gw = int(np.ceil(W/cell))+3
    g = rng.random((gh, gw)).astype(np.float32)
    im = Image.fromarray(g, 'F').resize((int(gw*cell), int(gh*cell)), Image.BICUBIC)
    return np.clip(np.asarray(im)[:H, :W], 0, 1)

def fbm(H, W, cell, rng, oct=3):
    acc = np.zeros((H, W), np.float32); amp = 1.0; tot = 0
    for i in range(oct):
        acc += vnoise(H, W, max(1, cell/(2**i)), rng)*amp; tot += amp; amp *= 0.5
    return acc/tot

# ---------- 滤波 ----------
def _box1(a, r, axis):
    if r < 1: return a
    pad = [(0, 0)]*a.ndim; pad[axis] = (r+1, r)
    p = np.pad(a, pad, mode='edge')
    c = np.cumsum(p, axis=axis, dtype=np.float32)
    n = a.shape[axis]
    hi = np.take(c, np.arange(2*r+1, 2*r+1+n), axis=axis)
    lo = np.take(c, np.arange(0, n), axis=axis)
    return (hi-lo)/(2*r+1)

def gblur(a, sigma):
    if sigma <= 0.3: return a
    w = np.sqrt(4*sigma*sigma/3+1); r = max(1, int(round((w-1)/2)))
    for _ in range(3):
        a = _box1(_box1(a, r, 0), r, 1)
    return a

def _nb(a, fn):
    p = np.pad(a, [(1, 1), (1, 1)] + [(0, 0)]*(a.ndim-2), mode='edge')
    H, W = a.shape[:2]; out = a.copy()
    for dy in range(3):
        for dx in range(3):
            out = fn(out, p[dy:dy+H, dx:dx+W])
    return out
def maxf(a): return _nb(a, np.maximum)
def minf(a): return _nb(a, np.minimum)

_grid = {}
def warp(arr, dx, dy):
    H, W = arr.shape[:2]
    if (H, W) not in _grid:
        _grid[(H, W)] = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    X, Y = _grid[(H, W)]
    x = np.clip(X+dx, 0, W-1.001); y = np.clip(Y+dy, 0, H-1.001)
    x0 = x.astype(np.int32); y0 = y.astype(np.int32)
    fx = (x-x0); fy = (y-y0)
    if arr.ndim == 3: fx = fx[..., None]; fy = fy[..., None]
    a = arr[y0, x0]; b = arr[y0, x0+1]; c = arr[y0+1, x0]; d = arr[y0+1, x0+1]
    return (a*(1-fx)+b*fx)*(1-fy)+(c*(1-fx)+d*fx)*fy

# ---------- 水彩层 ----------
DEF = dict(warp=2.0, edge=0.55, edge_r=3.0, mottle=0.10, gran=0.05, bleed=0.22,
           lines=0.75, line_col=(0.36, 0.24, 0.16), glaze=0.2, opacity=0.96, blend='normal')

def paint(canvas, layer, S, seed, **kw):
    """canvas: HxWx3 不透明；layer: HxWx4 直通 alpha。返回新 canvas"""
    o = dict(DEF); o.update(kw)
    rng = np.random.default_rng(seed)
    H, W = layer.shape[:2]
    a0 = layer[..., 3]
    if a0.max() < 0.003: return canvas
    P0 = layer[..., :3]*a0[..., None]
    if o['blend'] == 'screen':      # 发光层：只做柔化，屏幕叠加
        P = gblur(np.dstack([P0, a0]), 0.6*S)
        m = fbm(H, W, 40*S, rng, 2)
        P[..., :3] *= (0.85+0.3*m)[..., None]*o['opacity']
        return 1-(1-canvas)*(1-np.clip(P[..., :3], 0, 1))
    # 1) 铅笔描边（从未扭曲的图提取）
    lines = None
    if o['lines'] > 0:
        R = np.dstack([P0, a0])
        rg = (maxf(R)-minf(R)).max(axis=2)
        if S >= 2: rg = maxf(rg)*0.6 + rg*0.4
        la = np.clip((rg-0.10)*2.2, 0, 1)
        brk = np.clip((fbm(H, W, 26*S, rng, 2)-0.28)*4, 0, 1)
        grain = 0.55+0.6*vnoise(H, W, 1.2, rng)
        la = np.clip(la*brk*grain, 0, 1)*o['lines']
        ab = gblur(a0, 2*S)[..., None]+1e-4
        cav = gblur(P0, 2*S)/ab
        lc = np.clip(cav*0.42 + np.array(o['line_col'], np.float32)*0.45, 0, 1)
        ldx = (fbm(H, W, 30*S, rng, 2)-0.5)*2*1.2*S; ldy = (fbm(H, W, 30*S, rng, 2)-0.5)*2*1.2*S
        L = warp(np.dstack([lc*la[..., None], la]), ldx, ldy)
        lines = L
    # 2) 扭曲（颜料边缘不规则）
    w = o['warp']*S
    dx = (fbm(H, W, 34*S, rng, 3)-0.5)*2*w; dy = (fbm(H, W, 34*S, rng, 3)-0.5)*2*w
    R = warp(np.dstack([P0, a0]), dx, dy)
    P, a = R[..., :3], R[..., 3]
    # 3) 晕开（向外渗一点）
    if o['bleed'] > 0:
        Rb = gblur(R, 3.5*S)
        n = fbm(H, W, 12*S, rng, 2)
        k = (o['bleed']*(0.4+0.9*n)*(1-a))[..., None]
        P = P + Rb[..., :3]*k; a = a + Rb[..., 3]*k[..., 0]
    rgb = P/np.maximum(a, 1e-4)[..., None]
    # 4) 边缘积色
    if o['edge'] > 0:
        b = gblur(a, o['edge_r']*S)
        d = np.clip(a-b, 0, 1)
        dark = np.clip(1-o['edge']*d*1.8, 0.35, 1)
        rgb = rgb*dark[..., None]
    # 5) 斑驳 + 颗粒
    m = fbm(H, W, 55*S, rng, 3)
    rgb = rgb*(1+(m-0.5)*2*o['mottle'])[..., None]
    a = a*(1-o['mottle']*0.8*fbm(H, W, 30*S, rng, 2))
    g = gblur(vnoise(H, W, 1.3, rng), 0.5*S)
    rgb = rgb*(1-o['gran']*(g-0.3))[..., None]
    rgb = np.clip(rgb, 0, 1)
    a = np.clip(a*o['opacity'], 0, 1)[..., None]
    src = rgb*(1-o['glaze']) + rgb*canvas*o['glaze']
    out = src*a + canvas*(1-a)
    if lines is not None:
        la = np.clip(lines[..., 3], 0, 1)[..., None]
        lc = lines[..., :3]/np.maximum(la, 1e-4)
        out = out*(1-la*(1-np.clip(lc, 0, 1)))
    return out

def crisp(canvas, layer):
    a = layer[..., 3:4]
    return layer[..., :3]*a + canvas*(1-a)

def paper(canvas, S, seed, strength=1.0, warm=(1.0, 0.985, 0.95)):
    rng = np.random.default_rng(seed)
    H, W = canvas.shape[:2]
    f = 0.5*vnoise(H, W, 1.5*S, rng)+0.3*vnoise(H, W, 5*S, rng)+0.2*vnoise(H, W, 40*S, rng)
    bump = fbm(H, W, 6*S, rng, 2)
    sh = np.roll(bump, S, axis=0)-bump
    tex = 1-strength*(0.07*(1-f) + 0.9*np.clip(sh, -0.05, 0.05))
    out = canvas*tex[..., None]*np.array(warm, np.float32)
    # 轻微暗角
    Y, X = np.mgrid[0:H, 0:W].astype(np.float32)
    v = ((X/W-0.5)**2+(Y/H-0.5)**2)
    out = out*(1-strength*0.18*v)[..., None]
    return np.clip(out, 0, 1)

def save(canvas, path, size=None):
    im = Image.fromarray((np.clip(canvas, 0, 1)*255+0.5).astype(np.uint8), 'RGB')
    if size: im = im.resize(size, Image.LANCZOS)
    im.save(path)
    return im

class Scene:
    """按层累积 SVG；每层有自己的水彩参数"""
    def __init__(self, w, h, S=2, bg=(0.957, 0.922, 0.816)):
        self.w, self.h, self.S = w, h, S
        self.order = []; self.layers = {}; self.opts = {}
        self.bg = bg; self.defs = ''
    def layer(self, name, **kw):
        if name not in self.layers:
            self.order.append(name); self.layers[name] = []; self.opts[name] = kw
        return self
    def add(self, name, svg):
        self.layers[name].append(svg)
    def build(self, seed=1, paper_strength=1.0, warm=(1.0, 0.985, 0.95), post=None):
        H, W = self.h*self.S, self.w*self.S
        cv = np.ones((H, W, 3), np.float32)*np.array(self.bg, np.float32)
        for i, n in enumerate(self.order):
            body = ''.join(self.layers[n])
            if not body.strip(): continue
            L = render(body, self.w, self.h, self.S, self.defs)
            o = dict(self.opts[n])
            if o.pop('crisp', False):
                cv = crisp(cv, L); continue
            if o.pop('paper_here', False):
                cv = paper(cv, self.S, seed+99, paper_strength, warm)
            cv = paint(cv, L, self.S, seed*100+i, **o)
        if not any(self.opts[n].get('paper_here') for n in self.order):
            cv = paper(cv, self.S, seed+99, paper_strength, warm)
        if post: cv = post(cv)
        return cv
