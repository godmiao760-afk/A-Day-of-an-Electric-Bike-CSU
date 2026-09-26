# -*- coding: utf-8 -*-
# 00 总览板 1920×1080
import sys
sys.path.insert(0, '.')
from PIL import Image, ImageDraw, ImageFont

INK = "#3D3A5C"
F_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
F_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
fb = lambda s: ImageFont.truetype(F_B, s, index=2)
fr = lambda s: ImageFont.truetype(F_R, s, index=2)

W, H = 1920, 1080
img = Image.new("RGBA", (W, H), "#FFF7FA")
d = ImageDraw.Draw(img)
for yy in range(0, H, 28):
    for xx in range((yy // 28) % 2 * 14, W, 28):
        d.ellipse([xx - 2, yy - 2, xx + 2, yy + 2], fill="#FFE1EA")


def card(box, fill="white", r=22, sh=7, width=4):
    x0, y0, x1, y1 = box
    d.rounded_rectangle([x0, y0 + sh, x1, y1 + sh], r, fill="#BDB9D3")
    d.rounded_rectangle(box, r, fill=fill, outline=INK, width=width)


def tag(x, y, label, fill, color="white", size=20, skew=10):
    tw = d.textlength(label, font=fb(size))
    w, h = tw + 36, size + 16
    pts = [(x + skew, y), (x + w, y), (x + w - skew, y + h), (x, y + h)]
    d.polygon([(px, py + 4) for px, py in pts], fill="#BDB9D3")
    d.polygon(pts, fill=fill, outline=INK, width=3)
    d.text((x + 18, y + 5), label, font=fb(size), fill=color)
    return w


# ---------- 标题 ----------
card([24, 20, 1896, 128], fill="#4FC3F7", r=30)
d.text((58, 30), "E · Q版萌系日系手游", font=fb(50), fill="white", stroke_width=4, stroke_fill=INK)
d.text((600, 44), "《小电驴的一天》—— 把找不到车、被外卖撞、桩被占，画成糖果色的校园段子", font=fb(28), fill=INK)
d.text((600, 84), "参考：蔚蓝档案 / 学园题材手游 · 2 头身 · 粗圆角描边 · 手游式 UI", font=fr(20), fill="white")
# 右上小贴纸
for i, (c, t) in enumerate([("#FFD54F", "找到了!"), ("#FF8FB1", "被撞 x_x")]):
    x = 1640 + i * 124
    d.rounded_rectangle([x, 44, x + 112, 92], 24, fill=c, outline=INK, width=3)
    d.text((x + 56 - d.textlength(t, font=fb(18)) / 2, 54), t, font=fb(18), fill=INK)

# ---------- 三张界面缩略图 ----------
shots = [("../01-findcar.png", "01 找车 · 07:38", "#FFD54F"),
         ("../02-ride.png", "02 骑行 · 07:52", "#4FC3F7"),
         ("../03-charge.png", "03 夜间充电 · 22:47", "#FF8FB1")]
TW, TH = 600, 338
for i, (p, lab, c) in enumerate(shots):
    x = 32 + i * (TW + 34)
    y = 170
    card([x - 8, y - 8, x + TW + 8, y + TH + 8], r=18)
    im = Image.open(p).convert("RGBA").resize((TW, TH), Image.LANCZOS)
    mask = Image.new("L", (TW, TH), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, TW, TH], 12, fill=255)
    img.paste(im, (x, y), mask)
    tag(x + 10, y - 26, lab, c, INK if c == "#FFD54F" else "white", 19)

# ---------- 调色板 ----------
PX0, PY0, PX1, PY1 = 24, 548, 470, 1056
card([PX0, PY0, PX1, PY1])
tag(PX0 + 18, PY0 - 18, "调色板", "#FFD54F", INK, 20)
pal = [("#4FC3F7", "天空蓝 · 主 UI"), ("#FF8FB1", "樱粉 · 强调/血量"), ("#FFD54F", "柠檬黄 · 主角车"),
       ("#FFFFFF", "白 · 卡片底"), ("#3D3A5C", "墨紫 · 统一描边"), ("#7EE0B5", "薄荷 · 校车/空闲"),
       ("#5CC98A", "樟树绿"), ("#8C92B5", "路面灰紫"), ("#B08CA8", "坡道暖紫"), ("#2E3470", "夜空蓝")]
for i, (c, n) in enumerate(pal):
    col, row = i % 2, i // 2
    x = PX0 + 26 + col * 216
    y = PY0 + 34 + row * 92
    d.rounded_rectangle([x, y + 4, x + 64, y + 68], 16, fill="#BDB9D3")
    d.rounded_rectangle([x, y, x + 64, y + 64], 16, fill=c, outline=INK, width=3)
    d.ellipse([x + 10, y + 10, x + 24, y + 20], fill="white" if c != "#FFFFFF" else "#E6E4F2")
    d.text((x + 76, y + 6), c.upper(), font=fb(18), fill=INK)
    d.text((x + 76, y + 34), n, font=fr(15), fill="#6E6A8E")

# ---------- 精灵预览 ----------
SX0, SY0 = 494, 548
sp = Image.open("../04-sprites.png").convert("RGBA").crop((0, 66, 1320, 940))
sw_, sh_ = 700, int(700 * sp.height / sp.width)
card([SX0, SY0, SX0 + sw_ + 20, SY0 + sh_ + 20])
img.paste(sp.resize((sw_, sh_), Image.LANCZOS), (SX0 + 10, SY0 + 10))
tag(SX0 + 18, SY0 - 18, "实际尺寸精灵 1× / 4×", "#7EE0B5", INK, 20)

# ---------- 评估 ----------
NX0, NY0, NX1, NY1 = SX0 + sw_ + 44, 548, 1896, 1056
card([NX0, NY0, NX1, NY1])
tag(NX0 + 18, NY0 - 18, "评估", "#FF8FB1", "white", 20)
blocks = [
    ("优点", "#5CC98A", [
        "辨识度高：黄车 / 白车 / 粗描边，32px 下也一眼分清",
        "段子感强：贴纸表情 + 漫画气泡，囧事天然好笑",
        "UI 与角色同一套圆角语言，整体统一、易上手",
    ]),
    ("风险", "#FF6F8E", [
        "俯视骑车只见后脑勺，Q 版脸要靠「回头帧」+ 贴纸",
        "糖果色偏轻快，夜间充电的焦虑感要靠暗色调补",
        "描边细了会糊：统一 1.5px+，缩小后要逐张检查",
    ]),
    ("工作量", "#29A9E0", [
        "中：18 张精灵都是「圆角矩形 + 粗描边」可复用模板",
        "车辆 7 张换色即可；角色 3~4 张共用一个大头",
        "一名美术 4~6 小时可画完（UI 用代码画更省）",
    ]),
]
y = NY0 + 30
for title, c, lines in blocks:
    d.rounded_rectangle([NX0 + 24, y, NX0 + 124, y + 34], 17, fill=c, outline=INK, width=3)
    d.text((NX0 + 74 - d.textlength(title, font=fb(18)) / 2, y + 3), title, font=fb(18), fill="white")
    y += 44
    for t in lines:
        d.ellipse([NX0 + 32, y + 10, NX0 + 42, y + 20], fill=c, outline=INK, width=2)
        d.text((NX0 + 54, y), t, font=fb(18), fill=INK)
        y += 34
    y += 16
# 工作量评级徽章
bx = NX1 - 150
d.rounded_rectangle([bx, NY0 + 26, bx + 124, NY0 + 90], 20, fill="#FFD54F", outline=INK, width=3)
d.text((bx + 16, NY0 + 30), "工作量", font=fb(16), fill=INK)
d.text((bx + 72, NY0 + 42), "中", font=fb(34), fill=INK)

img.convert("RGB").save("../00-board.png")
print("ok")
