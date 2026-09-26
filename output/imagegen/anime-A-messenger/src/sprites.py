# 04-sprites：按游戏真实像素尺寸渲染精灵，1× 原图 + 4× 最近邻放大
import sys, io
sys.path.insert(0, '.')
from hd import *
from comp import *
import cairosvg
from PIL import Image, ImageDraw, ImageFont

OUTDIR = '..'


def road_tile(s, x0=0, y0=0, slope=False):
    base = '#8E948C' if not slope else '#A89A84'
    s.fill(rect(x0, y0, 64, 64), base, amp=0)
    R2 = random.Random(5)
    # 沥青斑驳笔触
    for _ in range(26):
        x = x0 + R2.uniform(2, 62); y = y0 + R2.uniform(2, 62)
        L = R2.uniform(3, 8)
        c = R2.choice(['#7E857E', '#9FA59A', '#848B84'])
        s.add(f'<path d="M{x:.1f} {y:.1f} l{L:.1f} {R2.uniform(-1, 1):.1f}" stroke="{c}" stroke-width="{R2.uniform(1, 2.2):.1f}" stroke-linecap="round" stroke-opacity="0.8"/>')
    for _ in range(18):
        s.add(f'<circle cx="{x0 + R2.uniform(0, 64):.1f}" cy="{y0 + R2.uniform(0, 64):.1f}" r="{R2.uniform(.4, 1):.1f}" fill="#5F6663" fill-opacity=".6"/>')
    # 中间虚线（车道线，米黄白）
    s.fill([(x0 + 30.5, y0 + 6), (x0 + 33.5, y0 + 6.5), (x0 + 33.2, y0 + 28), (x0 + 30.8, y0 + 27.5)], CREAM2, amp=0)
    s.fill([(x0 + 30.5, y0 + 38), (x0 + 33.5, y0 + 38.5), (x0 + 33.2, y0 + 60), (x0 + 30.8, y0 + 59.5)], CREAM2, amp=0)
    if slope:
        for k in range(3):
            yy = y0 + 12 + k * 18
            s.add(f'<path d="M{x0 + 8} {yy + 6} L{x0 + 18} {yy} L{x0 + 28} {yy + 6}" fill="none" stroke="{RUST}" stroke-width="2.4" stroke-opacity=".8" stroke-linecap="round"/>')


def grass_tile(s, x0=0, y0=0):
    s.fill(rect(x0, y0, 64, 64), VEG_L, amp=0)
    R2 = random.Random(9)
    for _ in range(9):
        cx, cy = x0 + R2.uniform(4, 60), y0 + R2.uniform(4, 60)
        pts = [(cx + R2.uniform(4, 9) * math.cos(a), cy + R2.uniform(3, 7) * math.sin(a)) for a in [k * 0.9 for k in range(7)]]
        s.fill(pts, '#6C9585', amp=0)
    for _ in range(40):  # 草叶笔触
        x = x0 + R2.uniform(1, 63); y = y0 + R2.uniform(3, 63)
        c = R2.choice([VEG_D, '#5E7F70', VEG_LL])
        s.add(f'<path d="M{x:.1f} {y:.1f} l{R2.uniform(-1.5, 1.5):.1f} {-R2.uniform(2, 4.5):.1f}" stroke="{c}" stroke-width="1.2" stroke-linecap="round" stroke-opacity=".85"/>')
    for _ in range(3):  # 小花（桂花黄）
        x = x0 + R2.uniform(6, 58); y = y0 + R2.uniform(6, 58)
        s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="1.3" fill="{MUSTARD}"/>')


def render_sprite(fn, w, h):
    s = SVG(w, h)
    fn(s)
    buf = cairosvg.svg2png(bytestring=s.render().encode(), output_width=w, output_height=h)
    return Image.open(io.BytesIO(buf)).convert('RGBA')


SPR = [
    ('rider', 32, 56, lambda s: rider_local(s)),
    ('bike', 24, 48, lambda s: bike_local(s, body=MUSTARD, seat='#C9962E', own=True)),
    ('bike_other', 24, 48, lambda s: bike_local(s, body=CREAM, seat='#6E7A74')),
    ('npc_delivery', 32, 56, lambda s: rider_local(s, bike_body='#DCE0D2', seat='#5C6359', shirt=ORANGE, helmet=ORANGE, delivery=True)),
    ('npc_walker', 28, 28, lambda s: walker_local(s)),
    ('pile', 32, 40, lambda s: pile_local(s, 'idle')),
    ('road', 64, 64, lambda s: road_tile(s)),
    ('slope', 64, 64, lambda s: road_tile(s, slope=True)),
    ('grass', 64, 64, lambda s: grass_tile(s)),
]


def main():
    W = 64 + sum(max(w*4,90)+18 for _,w,_,_ in SPR) + 26
    H = 620
    bg = SVG(W, H)
    seed(4)
    bg.fill(rect(0, 0, W, H), TEAL, amp=0)
    speckles(bg, 0, 0, W, H, 420, ['#4E9E9B', '#8FD3CD', CREAM], 0.6, 1.8, 0.45)
    bg.defs.append('')
    bg.xtext(34, 58, '04 · 精灵实际尺寸预览', 34, CREAM, depth=4, stroke=OUT, sw=5)
    bg.text(38, 90, 'A · Messenger 原味（abeto 风）— 上排：游戏里的 1× 真实像素；下排：同一张 1× 图最近邻放大 4×（看像素级可读性）', 16, OUT, weight='normal')
    # 标注牌底座
    slab(bg, 20, 112, W - 40, 486, CREAM, OUT, depth=8, r=16, lw=3)
    bgp = io.BytesIO(cairosvg.svg2png(bytestring=bg.render().encode()))
    canvas = Image.open(bgp).convert('RGBA')
    d = ImageDraw.Draw(canvas)
    fb = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 16, index=2)
    fs = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 13, index=2)
    top1, top4 = 150, 250
    x = 64
    d.text((30, top1 + 20), '1×', font=fb, fill=(200, 85, 61, 255))
    d.text((30, top4 + 4), '4×', font=fb, fill=(200, 85, 61, 255))
    for name, w, h, fn in SPR:
        im = render_sprite(fn, w, h)
        im.save(f'{OUTDIR}/sprites_1x_{name}.png')
        big = im.resize((w * 4, h * 4), Image.NEAREST)
        colw = max(w * 4, 90)
        # 1× 放在格子里，底下有浅色托盘
        cx = x + colw // 2
        d.rounded_rectangle([cx - w // 2 - 8, top1 - 8, cx + w // 2 + 8, top1 + h + 8], 6, fill=(233, 232, 206, 255))
        canvas.alpha_composite(im, (cx - w // 2, top1))
        d.rounded_rectangle([cx - w * 2 - 4, top4 - 4, cx + w * 2 + 4, top4 + h * 4 + 4], 6, outline=(58, 64, 64, 255), width=2, fill=(233, 232, 206, 255))
        canvas.alpha_composite(big, (cx - w * 2, top4))
        d.text((cx, top4 + h * 4 + 14), name, font=fb, fill=(58, 64, 64, 255), anchor='mt')
        d.text((cx, top4 + h * 4 + 36), f'{w}×{h}', font=fs, fill=(92, 99, 89, 255), anchor='mt')
        x += colw + 18
    canvas = canvas.convert('RGB')
    canvas.save(f'{OUTDIR}/04-sprites.png')
    print('x end', x)


if __name__ == '__main__':
    main()
