# 04-sprites：按真实像素尺寸渲染每个精灵，1× 原样 + 4× 最近邻放大
import os, io, cairosvg
from PIL import Image, ImageDraw, ImageFont
from lib import P, SVG
import sprites as S

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(OUT, 'src', 'tmp')
os.makedirs(TMP, exist_ok=True)

ITEMS = [
    ('rider', 32, 56, lambda s: S.rider(s, 0, 0)),
    ('bike', 24, 48, lambda s: S.bike(s, 0, 0, shadow=None)),
    ('bike_other', 24, 48, lambda s: S.other_bike(s, 0, 0, 1.0, 0, shadow=None)),
    ('npc_delivery', 32, 56, lambda s: S.npc_delivery(s, 0, 0)),
    ('pile', 32, 40, lambda s: S.pile(s, 0, 0, 1.0, 'free')),
    ('road', 64, 64, lambda s: S.tile_road(s, 0, 0)),
    ('grass', 64, 64, lambda s: S.tile_grass(s, 0, 0)),
]


def sprite_png(name, w, h, fn, seed=7):
    s = SVG(w, h, seed=seed)
    fn(s)
    p = os.path.join(TMP, name + '.svg')
    s.save(p)
    data = cairosvg.svg2png(url=p)
    return Image.open(io.BytesIO(data)).convert('RGBA')


def font(sz, bold=True):
    f = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc' if bold else '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
    return ImageFont.truetype(f, sz, index=2)  # index 2 = SC


def hexc(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def build(path=os.path.join(OUT, '04-sprites.png')):
    W, H = 1480, 540
    img = Image.new('RGBA', (W, H), hexc(P['mist']) + (255,))
    d = ImageDraw.Draw(img)
    # 纸面颗粒背景
    import random
    r = random.Random(3)
    for _ in range(900):
        x, y = r.randint(0, W), r.randint(0, H)
        d.ellipse([x, y, x + 2, y + 1], fill=hexc(P['lavL']) + (120,))
    d.text((28, 16), '04 · 实际尺寸精灵预览', font=font(26), fill=hexc(P['ink']))
    d.text((360, 24), '风格 B · Messenger 技法 × 长沙黄昏 —— 上排 1× 游戏真实像素，下排 4× 最近邻放大（每个像素看得见）', font=font(15, False), fill=hexc(P['ink2']))
    # 1× 背景条：浅 / 路面，两种底色都看一下
    x = 36
    base1 = 110
    base4 = 190
    for name, w, h, fn in ITEMS:
        im = sprite_png(name, w, h, fn)
        big = im.resize((w * 4, h * 4), Image.NEAREST)
        colw = max(w * 4, 110)
        # 1×：放在两种底上（路面 + 浅色）
        d.rounded_rectangle([x - 6, base1 - 36, x + colw + 6, base1 + 70], 10, fill=hexc(P['cream']) + (255,), outline=hexc(P['ink']), width=2)
        d.rectangle([x + 2, base1 - 28, x + 2 + 72, base1 + 62], fill=hexc(P['road']))
        img.alpha_composite(im, (x + 2 + (72 - w) // 2, base1 - 28 + (90 - h) // 2))
        img.alpha_composite(im, (x + 84 + max(0, (colw - 84 - w) // 2), base1 - 28 + (90 - h) // 2))
        # 4×
        d.rounded_rectangle([x - 6, base4 - 6, x + colw + 6, base4 + 262], 10, fill=hexc(P['cream']) + (255,), outline=hexc(P['ink']), width=2)
        img.alpha_composite(big, (x + (colw - w * 4) // 2, base4 + (256 - h * 4) // 2))
        d.text((x, base4 + 272 - 4), name, font=font(17), fill=hexc(P['ink']))
        d.text((x, base4 + 294), f'{w}×{h} px', font=font(13, False), fill=hexc(P['ink2']))
        x += colw + 34
    d.text((28, 508), '判读：1× 下主角黄车/外卖车靠「色块 + 深紫描边」仍能一眼区分；抖动描边在 24px 宽度会糊成 1px 线，笔刷纹理只在 64px 地砖上看得出。', font=font(14, False), fill=hexc(P['ink2']))
    img.convert('RGB').save(path)
    return path


if __name__ == '__main__':
    print(build())
