# 03-charge：夜间宿舍楼下充电 · 22:47
import sys
sys.path.insert(0, '.')
from scene_common import *

W, H = 960, 540
seed(44)
s = SVG(W, H)
NIGHT_SKY = '#2F5E62'      # 夜晚仍然保持青绿系，只是压暗

# ---- 夜空 + 岳麓山剪影 ----
s.fill(rect(0, 0, W, 200), NIGHT_SKY, amp=0)
speckles(s, 0, 0, W, 120, 70, ['#CFE8DF', '#8FC2BD'], 0.5, 1.3, 0.7)
mountain(s, 130, 560, 980, 70, color='#274B4E', dark='#1E3B3E', light='#33595B')
s.shape(ellipse(120, 40, 18, 18, 16), '#F2EBC4', 2, amp=0.4)   # 月亮
s.fill(ellipse(127, 36, 14, 16, 16), NIGHT_SKY, amp=0.2)

# ---- 宿舍楼（亮灯）----
dorm_facade(s, -10, 780, -40, 196, 3, wall='#8C9A94', night=True, lit=0.55, tile=True)
slab(s, 330, 150, 120, 26, '#7A3A2E', '#3A1E18', depth=3, r=4, lw=2)
s.text(390, 169, '升华公寓 7 舍', 15, '#F2E6C4', anchor='middle')
# 门禁大门（右）
s.shape(rect(780, 60, 200, 140), '#6E7C76', 2.8, amp=0.6)
s.shape(rect(820, 100, 110, 100), '#F4D27A', 2.4, amp=0.4)
s.fill(rect(822, 102, 106, 96), '#FFE8A6', amp=0, opacity=0.6)
s.line((875, 100), (875, 200), 2, OUT, amp=0.2)
slab(s, 800, 66, 160, 26, '#3A4A48', '#1E2828', depth=3, r=4, lw=2)
s.text(880, 85, '门禁 23:00 · 刷卡', 14, '#F4D27A', anchor='middle')

# ---- 地面 ----
ground(s, 0, 196, W, H - 196, '#4F605C', night=True, seed_=7)
s.fill(rect(0, 196, W, 20), '#1E3336', amp=0.4, opacity=0.5)
# 门口洒出的暖光
s.fill([(820, 200), (930, 200), (990, 330), (770, 330)], '#F4D27A', amp=0.5, opacity=0.18)

# ---- 路灯 + 光池（2 阶硬光圈，不做平滑渐变）----
def lamp(x, y):
    s.fill(ellipse(x, y + 20, 150, 70, 22), '#E8C98A', amp=1.2, opacity=0.16)
    s.fill(ellipse(x, y + 20, 95, 44, 22), '#F2D99A', amp=1.0, opacity=0.2)
    s.shape(rect(x - 3, y - 150, 6, 150), '#3F4A48', 2, amp=0.3)
    s.shape([(x - 3, y - 150), (x + 26, y - 156), (x + 26, y - 150), (x + 3, y - 144)], '#3F4A48', 1.8, amp=0.2)
    s.shape(rrect(x + 16, y - 156, 22, 9, 3), '#F4D27A', 1.8, amp=0.2)
    for k in range(6):  # 飞虫
        s.add(f'<circle cx="{x + 27 + R.uniform(-18, 18):.1f}" cy="{y - 140 + R.uniform(-14, 14):.1f}" r="1" fill="#FFF1B0"/>')
lamp(210, 330)
lamp(700, 330)

# ---- 充电桩一排 + 雨棚 ----
s.fill(rect(40, 226, 700, 20), '#1E3336', amp=0.4, opacity=0.4)
s.shape(rect(40, 214, 700, 12), '#3E6E6A', 2.2, amp=0.5, step=8)
states = ['occupied', 'occupied', 'broken', 'idle', 'plugged', 'occupied', 'broken', 'idle']
xs = [80 + i * 88 for i in range(8)]
PSC = 1.55
glow_i = 4
for i, (x, st) in enumerate(zip(xs, states)):
    if st == 'plugged':
        for k, op in ((26, 0.14), (18, 0.22), (11, 0.32)):
            s.fill(ellipse(x, 262, 20 + k, 28 + k, 18), '#9BF0A6', amp=0.6, opacity=op)
    pile(s, x, 262, st, PSC, night=True)
    # 状态牌
    lab = {'occupied': '被占', 'broken': '坏了', 'idle': '空闲', 'plugged': '充电中'}[st]
    col = {'occupied': ORANGE, 'broken': '#6F7A78', 'idle': TEAL, 'plugged': '#7FC98A'}[st]
    s.otext(x, 310, lab, 13, col, '#1E2828', 3.5, anchor='middle')
# 桩前停着的车
Rb = random.Random(3)
for i, (x, st) in enumerate(zip(xs, states)):
    if st == 'occupied':
        bike(s, x + Rb.uniform(-4, 4), 368, 1.3, Rb.uniform(-6, 6), body=Rb.choice(['#B9C3BC', '#C9C7B4', '#A9B8B6']), seat='#3F4747', night=True)
        # 充电线
        s.add(f'<path d="M{x + 14} {262} q10 50 -6 84" fill="none" stroke="#1E2828" stroke-width="4.5"/>')
        s.add(f'<path d="M{x + 14} {262} q10 50 -6 84" fill="none" stroke="{ORANGE}" stroke-width="2.2"/>')
# 主角的车：插在第 5 个桩，电缆发绿光
gx = xs[glow_i]
bike(s, gx, 372, 1.3, 0, body=MUSTARD, seat='#C9962E', own=True, basket=True, night=True)
s.add(f'<path d="M{gx + 14} 262 q16 48 -4 88" fill="none" stroke="#1E2828" stroke-width="5"/>')
s.add(f'<path d="M{gx + 14} 262 q16 48 -4 88" fill="none" stroke="#9BF0A6" stroke-width="2.6"/>')
# 主角：站在车左边（推车姿势刚停下）
pusher(s, gx - 44, 380, 1.3, night=True)
# 远处还有几辆没桩可插的车
for k, x in enumerate((70, 104, 138)):
    bike(s, x, 460, 1.25, Rb.uniform(-8, 8), body='#A9B8B6', seat='#3F4747', night=True)
tree(s, 930, 470, 64, dark='#2A3F3A', mid='#3A5A50', light='#4E7266', night=True)
tree(s, -10, 360, 50, dark='#2A3F3A', mid='#3A5A50', light='#4E7266', night=True)

# ---- 夜色压暗：整体冷色半透明 ----
s.fill(rect(0, 0, W, H), '#12303A', amp=0, opacity=0.22)
leaves(s, 0, 300, W, 240, 50, night=True)
speckles(s, 0, 196, W, 344, 160, ['#8FC2BD', '#2A3F3A'], 0.5, 1.3, 0.35)

# ---- 电线 ----
s.sag((-10, 20), (980, 12), 30, 1.2, '#1E2828', 0.9)
s.sag((-10, 34), (980, 30), 26, 1.0, '#1E2828', 0.9)

# ---- UI ----
battery_hud(s, 14, 12, 18, low=True)
clock_hud(s, '22:47', curfew='门禁 23:00', night=True)
dialog(s, '终于插上了。守着它，还是先回宿舍？', ['守着它', '回宿舍'], sel=0, cy=252)
bubble(s, gx - 60, 452, '别再跳闸了……', gx - 46, 408, size=16)
hint_bar(s, [('A/D', '切换'), ('F', '确认')])

s.save_png('../03-charge.png')
print('ok')
