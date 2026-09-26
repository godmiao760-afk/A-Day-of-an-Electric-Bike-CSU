from lib import *
import base64
def img(path,x,y,w,h):
    d=base64.b64encode(open(path,'rb').read()).decode()
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" href="data:image/png;base64,{d}" preserveAspectRatio="xMidYMid meet"/>'
b=''
# 标题栏
b+=f'<rect x="0" y="0" width="1920" height="130" fill="{INK}"/>'
b+='<clipPath id="hdr"><rect width="1920" height="130"/></clipPath><g clip-path="url(#hdr)">'+burst_lines(1780,65,60,420,n=60,seed=1,w=2,color='#3a3a3a')+'</g>'
b+=T(48,82,'G · 日漫网点风',56,fill=PAPER,family=SERIF)
b+=f'<rect x="460" y="36" width="64" height="56" fill="{Y}" stroke="{PAPER}" stroke-width="3"/>'+T(492,76,'黄',34,anchor='middle',family=SERIF)
b+=T(548,64,'黑白漫画 + 单一强调色「电驴黄」',26,fill=PAPER)
b+=T(548,102,'纸白底 · 墨线 · 网点纸灰阶 · 速度线 / 集中线 / 拟声词 —— 热血又囧的中南校园日常漫画',19,fill=PAPER,weight='400')
b+=T(1870,82,'小电驴的一天',30,fill=Y,family=SERIF,anchor='end')
# 三张缩略图 （每张 600×338），漫画分格
th=[('01-findcar.png','01 找车 · 07:38','宿舍楼下车棚，集中线 + 「滴滴！」认出黄色座套'),
    ('02-ride.png','02 骑行 · 07:52','麓山大坡交叉网点，外卖从后方冲上「！」'),
    ('03-charge.png','03 夜间充电 · 22:47','夜景 = 反相网点，弹窗是漫画格，只有插上的桩发黄光')]
for i,(f,t,sub) in enumerate(th):
    x=48+i*624; y=184
    rot=[-0.8,0.6,-0.5][i]
    b+=f'<g transform="rotate({rot} {x+300} {y+190})">'
    b+=f'<rect x="{x+8}" y="{y+8}" width="600" height="338" fill="url(#t50)"/>'
    b+=img(OUT+f,x,y,600,338)
    b+=f'<rect x="{x}" y="{y}" width="600" height="338" fill="none" stroke="{INK}" stroke-width="5"/>'
    b+=f'<rect x="{x}" y="{y-40}" width="{len(t)*17+40}" height="36" fill="{INK}"/>'+T(x+14,y-15,t,20,fill=Y)
    b+=T(x,y+370,sub,17,weight='400')
    b+='</g>'
# 下半：调色板
y0=600
b+=frame(48,y0,560,440)
b+=f'<rect x="48" y="{y0}" width="560" height="44" fill="{INK}"/>'+T(66,y0+30,'调色板 PALETTE',20,fill=PAPER)
pal=[(PAPER,'纸白','#F5F1E6','底色 / 高光'),(INK,'墨黑','#1E1E1E','线稿 / 夜景底'),('url(#t10)','网点 10%','#1E1E1E@10%','草地 / 远山'),
     ('url(#t30)','网点 30%','#1E1E1E@30%','树冠暗部 / 座套'),('url(#t50)','网点 50%','#1E1E1E@50%','阴影 / 投影'),('url(#t80)','网点 80%','#1E1E1E@80%','窗户 / 夜空'),
     ('url(#hx)','交叉斜线','hatch 45°×2','坡道 = 耗电区'),(Y,'电驴黄','#FFCC00','唯一强调色'),('url(#yt)','黄网点','#FFCC00+网点','黄色的暗部')]
for k,(f,n,c,u) in enumerate(pal):
    cx=66+(k%3)*180; cy=y0+62+(k//3)*120
    b+=f'<rect x="{cx}" y="{cy}" width="160" height="60" fill="{f}" stroke="{INK}" stroke-width="2.5"/>'
    b+=T(cx,cy+80,n,16)
    b+=T(cx+160,cy+80,c,12,anchor='end',weight='400',family='Noto Sans Mono CJK SC')
    b+=T(cx,cy+100,u,13,weight='400')
b+=T(66,y0+424,'规则：黄色只给「自己的车 / 电量 / 充电中 / 选中项」',15)
# 精灵预览
sx,sy=640,y0
b+=frame(sx,sy,560,440)
b+=f'<rect x="{sx}" y="{sy}" width="560" height="44" fill="{INK}"/>'+T(sx+18,sy+30,'精灵预览 1× / 4×（详见 04-sprites.png）',20,fill=PAPER)
b+=img(OUT+'04-sprites.png',sx+12,sy+56,536,340)
b+=T(sx+18,sy+424,'32px 下仍可辨：黄车 vs 白车对比极强，网点 = 灰阶',15)
# 评估
ex,ey=1232,y0
b+=frame(ex,ey,640,440)
b+=f'<rect x="{ex}" y="{ey}" width="640" height="44" fill="{INK}"/>'+T(ex+18,ey+30,'评估 · 优点 / 风险 / 工作量',20,fill=PAPER)
rows=[('优',['「找自己的黄车」天然成立：满屏黑白，唯一的黄','= 玩家视线焦点，玩法即画面。']),
      ('优',['1 种颜色 + 4 档网点，风格规则极简，','两个人画也不会"不像一套"。']),
      ('优',['速度线 / 集中线 /「滴滴！」「砰！」天生是','受击和提示特效，笑点直给。']),
      ('险',['网点缩放/旋转(setAngle)易出摩尔纹，','精灵里的网点要按 1× 像素对齐画。']),
      ('险',['俯视小精灵看不见表情，漫画感要靠 UI、','气泡、拟声词特效图来撑。']),
      ('险',['满屏墨线 + 网点易"脏"，障碍物需比背景','更粗的外轮廓来分层。'])]
yy=ey+74
for tag,ls in rows:
    f=Y if tag=='优' else INK; tf=INK if tag=='优' else PAPER
    b+=f'<rect x="{ex+18}" y="{yy-22}" width="32" height="30" fill="{f}" stroke="{INK}" stroke-width="2"/>'+T(ex+34,yy,tag,18,fill=tf,anchor='middle')
    for j,p in enumerate(ls): b+=T(ex+62,yy+j*21-2,p,16,weight='400')
    yy+=21*len(ls)+7
yy=ey+440-76
b+=f'<rect x="{ex+18}" y="{yy-10}" width="604" height="70" fill="{Y}" stroke="{INK}" stroke-width="2.5"/>'
b+=T(ex+34,yy+17,'工作量：低～中',21)
b+=T(ex+200,yy+17,'18 张 ≈ 5~6 小时 / 1 人',15,weight='400')
b+=T(ex+34,yy+44,'只画墨线 + 套 4 种网点 pattern，不用配色；难点在特效图。',15,weight='400')
render(svg(1920,1080,b),'00-board.png')
