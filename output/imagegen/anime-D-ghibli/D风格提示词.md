# 《小电驴的一天》D 风格（吉卜力水彩绘本）描述与提示词

> 用途：交给其他 AI 生图（即梦 / 可灵 / 通义万相 / GPT / Midjourney / Nano Banana 等），比较哪一版更像中南大学。
> 每个场景都有中文版和英文版，哪个效果好用哪个。

---

## 一、风格描述

**一句话：画真实的中南，用吉卜力的笔法。**
画面像宫崎骏电影的背景画：夏末的长沙，樟树成荫，宿舍阳台晾满衣服，车棚里电动车一辆挨一辆。整体温暖、有生活气，带一点"又是这样的一天"的疲惫和好笑。

**"写实"和"绘本"怎么分工：**
- **按真实来画的部分**：建筑的形状、层数和外墙；道路走向、路口结构；车棚、充电桩这些设施；电动车的比例。这些照着照片画，要让中南的同学一眼认出"这是升华 / 这是后湖路口 / 这是 A 座"。
- **风格化的部分**：只有笔触、颜色和光。用水彩平涂、颜料在边缘晕开、纸张纹理，描边是柔和的彩铅线。

**关键词**

| 维度 | 要求 |
|---|---|
| 技法 | 水彩 / 水粉平涂，颜料边缘自然晕开，能看到纸张纹理；描边用暖棕或墨绿的彩铅线，粗细不均，**不用纯黑** |
| 光 | 白天：长沙夏天的强日光 + 樟树的斑驳树影；傍晚：暖橙斜光、影子拉长；夜晚：深蓝底色 + 暖黄路灯和宿舍窗灯 |
| 形体 | 树冠是一大团一大团的，很蓬松；天上是有体积的积云；建筑稍微简化，但瓷砖分格、阳台、空调外机、防盗网都要保留 |
| 细节 | 生活细节要多：晾着的被子和 T 恤、车筐里的雨衣和外卖袋、挂在车把上的头盔、墙上的告示、猫 |
| 情绪 | 温暖、怀旧、有点累、好笑，是能引起共鸣的日常 |
| 界面 | 手账便签纸、木牌、纸胶带的质感，字体圆润 |

**调色板**

| 颜色 | 色值 | 用在哪 |
|---|---|---|
| 草绿 | `#8DB86B` | 草地、亮部树叶 |
| 樟树深绿 | `#3F6B3A` | 树冠暗部、树影 |
| 砖红 | `#B5553C` | 砖墙、屋顶、告示牌 |
| 奶油白 | `#F4EBD0` | 白墙、瓷砖、纸张（代替纯白） |
| 天蓝 | `#9CC9E0` | 天空、玻璃、湖面 |
| 木棕 | `#8A6A4A` | 描边、木牌、树干 |
| 电驴黄 | `#F2C14E` | **主角的车**、路灯光 |
| 夜蓝 | `#2E3A59` | 夜景底色 |

**规则：** 画面里只有主角的车是饱和的黄色，别人的车用浅色、颜色随机、饱和度低，这样一眼就能找到"我的车"。

---

## 二、通用风格段（每条提示词后面都要加上）

**中文**
```
吉卜力工作室动画背景风格，宫崎骏电影美术，手绘水彩与水粉，颜料边缘自然晕染，可见纸张纹理，柔和的暖棕色彩铅描边，线条粗细不均，蓬松团簇的樟树树冠，有体积感的夏日积云，温暖自然光与斑驳树影，低饱和暖色调（草绿、樟树深绿、砖红、奶油白、天蓝），真实的中国大学校园建筑与比例，丰富的生活细节，温馨怀旧又带点疲惫的日常氛围，高细节，干净构图
```

**English**
```
Studio Ghibli background art style, Hayao Miyazaki film aesthetic, hand-painted watercolor and gouache, soft pigment bleeding at edges, visible paper texture, gentle warm-brown colored-pencil outlines with uneven line weight, fluffy clustered camphor tree canopies, voluminous summer cumulus clouds, warm natural sunlight with dappled leaf shadows, muted warm palette (grass green, deep camphor green, brick red, cream white, sky blue), realistic Chinese university campus architecture and proportions, rich everyday-life details, nostalgic cozy slightly tired slice-of-life mood, highly detailed, clean composition
```

**负面提示词**
```
photorealistic photo, 3D render, CGI, glossy, plastic, neon, cyberpunk, pure black outlines, oversaturated, anime character close-up, text gibberish, watermark, logo, Japanese signage, Western campus, snow, blurry, lowres, deformed vehicles, cars instead of e-bikes, bicycles instead of electric scooters
```
中文版：`照片、3D 渲染、塑料感、霓虹、赛博朋克、纯黑描边、过饱和、乱码文字、水印、日文招牌、欧美校园、雪、模糊、变形的车辆、把电动车画成自行车或汽车`

---

## 三、场景提示词

每个场景分两种画法：
- **【插画】**：人视角或 3/4 俯视，偏写实，用来引起共鸣。适合放在 Intro「第 N 天」字幕、Class 上课过场、Result 结算的背景（要放进游戏得先和 A 商量）。
- **【界面】**：正俯视的游戏画面，带 UI，用来看这个风格落到可玩场景是什么样。

> **强烈建议上传真实照片当参考图**（垫图 / 图生图 / 风格参考），建筑会像很多。我没有这些地方的实景照片，下面写的建筑外观是一般描述，**有照片的话以照片为准，把对应描述改掉**。

---

### S1【插画】清晨 7:35 · 升华公寓楼下车棚找车

**中文**
```
清晨七点半，中南大学升华学生公寓楼下的电动车车棚，长条形钢架雨棚下几百辆电动车一辆挨一辆塞得满满当当，车把交错，一个背着双肩包、睡眼惺忪的大学生站在车阵中间的窄过道里四处张望找自己的车，远处一辆亮黄色电动车被左右两辆车死死夹住，车座上有露水和几片樟树落叶，别人的车把上挂着头盔、车筐里塞着雨衣和外卖袋，身后是六七层的学生宿舍楼，阳台晾满衣服和被子、挂着空调外机，墙上贴着"请有序停放"的告示，远处岳麓山在晨雾里，樟树透下清晨的斜光，人视角略俯拍，16:9
```
**English**
```
Early morning 7:35 at the e-scooter shelter below Shenghua student dormitory of Central South University in Changsha, hundreds of electric scooters packed tightly under a long steel-frame rain canopy with handlebars interlocking, a sleepy college student with a backpack standing in the narrow aisle looking around for his scooter, one bright yellow electric scooter jammed between two others, dew and camphor leaves on its seat, helmets hanging on other handlebars, raincoats and takeaway bags in baskets, six-to-seven-story dormitory behind with laundry and quilts on every balcony and AC units, a "please park in order" notice on the wall, Yuelu Mountain in morning mist in the distance, low slanted sunlight through camphor trees, slightly elevated eye-level view, 16:9
```

### S2【界面】找车 · 正俯视游戏画面

**中文**
```
2D 俯视角独立游戏截图，正上方俯视，宿舍楼下车棚，三排电动车整齐密集停放，所有车车头朝上，别人的车为浅色且颜色各异（浅粉、浅蓝、米白、浅灰），只有一辆亮黄色电动车被左右夹住并发出淡淡光圈，一个小人主角站在过道里，头顶有对话气泡"终于找到你了！"，画面上方是宿舍楼的楼顶和阳台，两侧是樟树和草地，左上角电量条"62%"，右上角木牌时钟"07:38"和信号格，底部便签纸提示"F 查看 · E 背包"，界面为手账便签和木牌质感，16:9
```
**English**
```
2D top-down indie game screenshot, straight overhead view, e-scooter parking shelter below a dormitory, three dense rows of electric scooters all facing up, other scooters in pale varied colors (light pink, light blue, off-white, light grey), only one bright yellow scooter squeezed between neighbors with a soft glow ring, tiny player character in the aisle with a speech bubble, dormitory rooftop and balconies along the top edge, camphor trees and grass on both sides, battery bar "62%" top-left, wooden-sign clock "07:38" with signal bars top-right, paper-note control hint at bottom, UI styled as journal sticky notes and wooden plaques, 16:9
```

### S3【插画】校内路线 · 湖边绿道和大坡

（对应地图上的蓝线：升华公寓 → 西侧体育场、体育馆旁的湖边绿道 → 过靳江路 → 潇湘校区南侧道路 → A 座）

**中文**
```
早上七点五十分，中南大学校内林荫道，一侧是狭长的湖和芦苇、一侧是体育场的红色跑道和看台，道路两旁高大的樟树形成绿色隧道，一段明显的上坡路，主角骑着亮黄色电动车吃力地上坡，仪表盘电量格在往下掉，前方有学生三三两两走路、戴着耳机横穿马路，一辆校园巴士慢悠悠开在前面，后方一个外卖骑手从旁边窜过，夏日强烈阳光透过树叶在路面洒下光斑，蝉鸣的感觉，人视角略俯，16:9
```
**English**
```
7:50 am on a tree-lined road inside Central South University campus, a long narrow lake with reeds on one side and a stadium with red running track and stands on the other, tall camphor trees forming a green tunnel, a noticeable uphill slope, the protagonist struggling uphill on a bright yellow electric scooter with the battery gauge dropping, students walking in small groups, one crossing with earphones on, a campus shuttle bus crawling ahead, a food-delivery rider darting past from behind, harsh summer sunlight making dappled light spots on the asphalt, cicada-summer feeling, slightly elevated eye-level view, 16:9
```

### S4【插画】校外路线 · 后湖十字路口查头盔

（对应地图上的红线和黄色路口：中南大学地铁站旁的后湖路口）

**中文**
```
早高峰的长沙城市十字路口，路口一角是"中南大学"地铁站出入口，红绿灯下挤满了等灯的电动车和学生，路边立着锥桶和临时路障，两名穿荧光黄绿色反光背心、戴白色警帽的交警正在拦车查头盔，几个没戴头盔的学生被叫到路边一脸心虚，主角骑着亮黄色电动车停在队伍里，车后座坐着一个抱着书的同学，两人互相看了一眼很慌，街边是有生活气的小店招牌、电线、公交站，远处是后湖方向的绿树，早晨阳光，人视角，16:9
```
**English**
```
Rush-hour city intersection in Changsha, a "Central South University" metro station entrance at one corner, crowds of electric scooters and students waiting at the traffic light, traffic cones and a temporary barrier at the roadside, two traffic police in fluorescent yellow-green reflective vests and white caps stopping riders to check helmets, a few helmetless students pulled over looking guilty, the protagonist on a bright yellow e-scooter in the queue with a classmate holding books on the back seat, both exchanging a panicked glance, lively small shop signs, overhead wires and a bus stop along the street, green trees toward Houhu lake in the distance, morning sunlight, eye-level view, 16:9
```

### S5【界面】骑行 · 纵向道路

**中文**
```
2D 俯视角独立游戏截图，正上方俯视，一条纵向三车道道路，所有车辆车头朝上，主角骑亮黄色电动车在中间车道，前方有一辆绿色校园巴士和一辆逆行的电动车，一个学生从斑马线横穿，后方一个带黄色外卖箱的骑手冲上来，屏幕底部有"！"警示，路面一段标着"上坡"的褐色坡道，道路两侧是蓬松的樟树、草地、路边长椅和社团招新展板，左上角电量条"41%"和三颗心的血量，右上角木牌时钟"07:52"，底部便签纸提示"W 前进 · S 刹车 · A/D 换道"，16:9
```
**English**
```
2D top-down indie game screenshot, straight overhead view, a vertical three-lane road, all vehicles facing up, protagonist on a bright yellow e-scooter in the middle lane, a green campus shuttle bus and a wrong-way scooter ahead, a student crossing at a zebra crossing, a rider with a yellow delivery box rushing from behind with a "!" warning at screen bottom, a brown uphill slope section marked "上坡" on the road, fluffy camphor trees, grass, benches and club-recruitment boards along both sides, battery bar "41%" and three hearts top-left, wooden-sign clock "07:52" top-right, paper-note control hint at bottom, 16:9
```

### S6【插画】7:59 · A 座教学楼前停车冲刺

**中文**
```
早上七点五十九分，中南大学潇湘校区综合教学楼 A 座前，端庄方正的浅灰色现代教学楼，楼与楼之间有墨绿色玻璃连廊，天井里种着香樟树，楼前的电动车停车区已经停满，主角推着没电的亮黄色电动车满头大汗地找空位，旁边同学拎着早餐一路小跑冲进楼里，远处能看到岳麓山，阳光明亮，稍俯视角度，16:9
```
**English**
```
7:59 am in front of Building A of the comprehensive teaching complex at Central South University Xiaoxiang campus, a dignified square light-grey modern teaching building with dark-green glass corridors connecting the wings, camphor trees growing in the atrium courtyard, the scooter parking area in front already full, the sweating protagonist pushing a dead bright yellow e-scooter looking for an empty spot, classmates sprinting into the building holding breakfast, Yuelu Mountain visible in the distance, bright sunlight, slightly elevated view, 16:9
```

### S7【插画】22:47 · 宿舍楼下找桩充电

**中文**
```
晚上十点四十七分，中南大学宿舍楼下的电动车充电区，一排挂在墙上的扫码充电插座，大部分已经被占满，小屏幕亮着，有一台屏幕黑着明显坏了，几辆早就充满却没人拔的车，充电线缠成一团，地上一个被人拔下来的插头，主角推着亮黄色电动车，举着手机扫码，一脸疲惫，宿舍楼每扇窗户透出暖黄灯光，阳台上还晾着衣服，一盏昏黄路灯下飞着小虫，宿舍大门上方写着"门禁 23:00"，一只猫蹲在车座上，深蓝夜色，温暖又有点心酸，人视角，16:9
```
**English**
```
10:47 pm at the e-scooter charging area below a Central South University dormitory, a row of wall-mounted QR-code charging sockets, most occupied with small screens glowing, one with a dark dead screen clearly broken, several scooters fully charged but nobody unplugged them, tangled charging cables, one plug yanked out lying on the ground, the tired protagonist pushing a bright yellow e-scooter and scanning a QR code with his phone, warm yellow light from every dorm window, laundry still hanging on balconies, insects circling a dim street lamp, a "curfew 23:00" sign above the dorm gate, a cat sitting on a scooter seat, deep blue night, warm yet bittersweet mood, eye-level view, 16:9
```

### S8【界面】充电 · 俯视 + 选项弹窗

**中文**
```
2D 俯视角独立游戏截图，正上方俯视，夜晚宿舍楼下，一排充电桩，桩上方有小标签"被占 / 空闲 / 充电中 / 坏了 / 扫码失败"，被占的桩旁停着浅色电动车，一台桩发出绿色光，旁边是插上电的亮黄色电动车和推车的小人主角，画面中间是一张横线便签纸样式的弹窗"终于插上了。守着它，还是先回宿舍？"，两个选项按钮"守着它""回宿舍"，左边被高亮，右上角木牌时钟"22:47"和"门禁 23:00"，左上角红色低电量条"18%"，深蓝夜色配暖黄路灯光圈，16:9
```
**English**
```
2D top-down indie game screenshot, straight overhead view, night below a dormitory, a row of charging posts with small labels (occupied / free / charging / broken / scan failed), pale scooters parked at occupied posts, one post glowing green with a plugged-in bright yellow scooter and the tiny protagonist beside it, a lined-notebook-paper dialog in the center reading "终于插上了。守着它，还是先回宿舍？" with two buttons "守着它" and "回宿舍", left one highlighted, wooden-sign clock "22:47" and "门禁 23:00" top-right, red low battery bar "18%" top-left, deep blue night with warm yellow lamp light pools, 16:9
```

### S9【插画】标题 / 结局 · 「明天还得推车」

**中文**
```
傍晚的中南大学校园，夕阳把天空染成橙粉色，主角推着没电的亮黄色电动车，走在长长的樟树林荫道上，影子拉得很长，远处是岳麓山剪影和宿舍楼亮起的第一批灯，路边桂花开了，落了一地金黄小花，画面留白适合放标题"小电驴的一天"，温暖、疲惫又好笑，电影感构图，16:9
```
**English**
```
Dusk on Central South University campus, sunset painting the sky orange-pink, the protagonist pushing a dead bright yellow electric scooter along a long camphor-tree avenue, long stretched shadow, Yuelu Mountain silhouette and the first dorm lights in the distance, osmanthus in bloom with tiny golden flowers scattered on the ground, empty space in the sky for a title, warm, tired and funny mood, cinematic composition, 16:9
```

---

## 四、单个素材（试试即可）

生图 AI **很难直接出能用的 32 像素精灵**：一般不是正俯视、背景不透明，比例也不对。建议只把它当造型参考，最后还是在 Aseprite / Piskel 里按尺寸重画。

```
game sprite sheet, straight top-down view, electric scooters facing up, one bright yellow scooter, several pale off-white scooters, a delivery rider with yellow box, a green campus shuttle bus, a traffic police officer in fluorescent vest seen from above, a wall-mounted QR charging post, pedestrians with varied hair and outfits seen from above, Studio Ghibli watercolor style with soft brown outlines, flat light, plain white background, evenly spaced, no perspective
```
中文：`游戏素材表，正俯视，车头朝上的电动车，一辆亮黄色、几辆米白色，带黄色外卖箱的骑手，绿色校园巴士，从上往下看的穿荧光背心的交警，墙挂式扫码充电桩，发型和衣服各不相同的俯视行人，吉卜力水彩风，柔和棕色描边，平光，纯白背景，间距均匀，无透视`

---

## 五、对比时看这几点

每个场景至少出 4 张，按下面 5 条打分（1–5 分）：

1. **像不像中南**：建筑、路口、车棚，中南的同学能不能认出来
2. **有没有共鸣**：有没有"对对对，就是这样"的细节（夹车、被拔插头、查头盔、门禁）
3. **风格统一**：几张放在一起像不像同一部作品
4. **主角的车醒目吗**：黄色是不是一眼就能找到
5. **能不能落到游戏里**：界面版能不能拆成俯视素材；插画版能不能当过场背景

**记录方法：** 文件名写成 `S1-即梦-01.png` 这样，放进 `output/imagegen/anime-D-ghibli/ai-tests/`，方便大家一起比。
