# -*- coding: utf-8 -*-
# 04 实际尺寸精灵预览：1× 真实像素 + 4× 最近邻放大（看缩到 32px 能不能认出来）
import sys, io
sys.path.insert(0, '.')
from lib import *
from PIL import Image, ImageDraw, ImageFont
import cairosvg


def road_tile(sw=1.2):
    g = f'<rect x="0" y="0" width="64" height="64" fill="#8C92B5"/>'
    g += f'<rect x="0" y="0" width="64" height="64" fill="none"/>'
    g += f'<path d="M32,4 V26 M32,38 V60" stroke="{WHITE}" stroke-width="3" stroke-linecap="round"/>'
    g += f'<circle cx="12" cy="16" r="1.4" fill="#7A80A6"/><circle cx="50" cy="44" r="1.6" fill="#7A80A6"/><circle cx="18" cy="52" r="1" fill="#A3A8C8"/>'
    g += f'<path d="M44,12 q4,-2 8,0" stroke="#A3A8C8" stroke-width="1.4" fill="none" stroke-linecap="round"/>'
    return g


def grass_tile(sw=1.2):
    g = f'<rect x="0" y="0" width="64" height="64" fill="#9BE3A8"/>'
    for (x, y) in [(8, 14), (40, 8), (26, 34), (52, 40), (12, 52), (44, 58)]:
        g += f'<path d="M{x},{y} q1.5,-4 3,0 q1.5,-3.5 3,0" stroke="#6CCB86" stroke-width="1.6" fill="none" stroke-linecap="round"/>'
    g += f'<circle cx="54" cy="18" r="2.2" fill="{PINK}" stroke="{INK}" stroke-width="0.8"/><circle cx="20" cy="24" r="1.8" fill="{WHITE}" stroke="{INK}" stroke-width="0.8"/>'
    g += f'<circle cx="34" cy="52" r="1.8" fill="{LEMON}" stroke="{INK}" stroke-width="0.8"/>'
    return g


SW = 1.3
items = [
    ("rider", 32, 56, rider(16, 29, 1, sw=SW, expr="worry", helmet=True)),
    ("bike", 24, 48, bike(12, 24, 1, sw=SW)),
    ("bike_other", 24, 48, bike_other(12, 24, 1, 1, sw=SW)),
    ("npc_delivery", 32, 56, delivery(16, 27, 1, sw=SW)),
    ("pile", 32, 40, pile(16, 21, 1, "free", sw=SW)),
    ("pile·插上", 32, 40, pile(16, 21, 1, "plugged", sw=SW)),
    ("road", 64, 64, road_tile()),
    ("grass", 64, 64, grass_tile()),
]


def raster(w, h, body):
    svg = svg_open(w, h) + defs() + body + '</svg>'
    png = cairosvg.svg2png(bytestring=svg.encode())
    return Image.open(io.BytesIO(png)).convert("RGBA")


F_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
fb = lambda s: ImageFont.truetype(F_B, s, index=2)  # index 2 = SC


items.insert(1, ("rider·回头", 32, 56, rider(16, 29, 1, sw=SW, expr="dizzy", helmet=True, look_back=True)))
items.insert(6, ("npc_walker", 28, 28, walker(14, 13, 0.62, sw=SW*0.62, top=MINT)))

CW, CH = 1320, 940
img = Image.new("RGBA", (CW, CH), "#FFF7FA")
d = ImageDraw.Draw(img)
for yy in range(0, CH, 24):
    for xx in range((yy // 24) % 2 * 12, CW, 24):
        d.ellipse([xx - 1.5, yy - 1.5, xx + 1.5, yy + 1.5], fill="#FFE1EA")
d.rounded_rectangle([16, 14, 640, 58], 22, fill="#4FC3F7", outline="#3D3A5C", width=3)
d.text((34, 18), "E · Q版萌系  精灵实际尺寸预览（1× / 4× 最近邻）", font=fb(22), fill="white")
d.text((660, 26), "每张卡：上 = 1× 真实像素（白底 / 路面底各一份），下 = 放大 4 倍", font=fb(15), fill="#3D3A5C")

def column(x, top, bottom, name, w, h, body, tile=False):
    im1 = raster(w, h, body)
    im4 = im1.resize((w * 4, h * 4), Image.NEAREST)
    colw = max(w * 4, 120)
    cx = x + colw // 2
    d.rounded_rectangle([x - 8, top, x + colw + 8, bottom], 16, fill="white", outline="#3D3A5C", width=3)
    tw = d.textlength(name, font=fb(15))
    d.rounded_rectangle([cx - tw / 2 - 10, top + 10, cx + tw / 2 + 10, top + 36], 13, fill="#FFD54F", outline="#3D3A5C", width=2)
    d.text((cx - tw / 2, top + 11), name, font=fb(15), fill="#3D3A5C")
    lab = f"{w}×{h}"
    d.text((cx - d.textlength(lab, font=fb(12)) / 2, top + 40), lab, font=fb(12), fill="#8A87A8")
    y1 = top + 62
    if tile:
        img.alpha_composite(im1, (cx - w // 2, y1))
        y4 = y1 + h + 14
    else:
        img.alpha_composite(im1, (cx - w - 6, y1))
        d.rounded_rectangle([cx + 2, y1 - 4, cx + w + 10, y1 + h + 4], 6, fill="#8C92B5")
        img.alpha_composite(im1, (cx + 6, y1))
        y4 = y1 + 56 + 26
    d.text((x + 2, y4 - 4), "4×", font=fb(13), fill="#FF8FB1")
    img.alpha_composite(im4, (cx - w * 2, y4 + ((224 - h * 4) // 2 if not tile else 0) + 18))
    return colw

x = 26
for name, w, h, body in items[:8]:
    x += column(x, 76, 478, name, w, h, body) + 26
# 第二行：地砖 + 说明
x = 26
for name, w, h, body in items[8:]:
    x += column(x, 498, 922, name, w, h, body, tile=True) + 26
# 说明卡
nx = x
d.rounded_rectangle([nx, 498, CW - 20, 922], 16, fill="#FFFFFF", outline="#3D3A5C", width=3)
d.rounded_rectangle([nx + 16, 516, nx + 176, 544], 14, fill="#FF8FB1", outline="#3D3A5C", width=2)
d.text((nx + 30, 517), "缩到 32px 的结论", font=fb(16), fill="white")
notes = [
    "✓ 黄车 vs 近白车：色相差大，1× 一眼分得清",
    "✓ 粗描边 #3D3A5C 让 24px 宽的车在灰路面上不糊",
    "✓ 充电桩靠屏幕颜色区分 空闲/插上/被占",
    "△ 骑车俯视只看到后脑+头盔，Q版脸要靠「回头」帧",
    "△ 1× 下五官只剩 1~2 像素，表情改用头顶贴纸（😵✨）",
    "△ 描边在 32px 下建议 1.5px，别用 1px 细线",
    "→ 画法：矢量画 4× 稿再缩小，别直接画 1×",
]
for i, t in enumerate(notes):
    col = "#3D3A5C" if t[0] != "→" else "#29A9E0"
    d.text((nx + 22, 572 + i * 44), t.replace("😵✨", "晕 / 闪"), font=fb(18), fill=col)
img.convert("RGB").save("../04-sprites.png")
print("done")
