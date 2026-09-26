# Messenger（abeto）美术风格分析与推荐

> 参考作品：[messenger.abeto.co](https://messenger.abeto.co)
> 开发者：Abeto（Vicente Lucendo & Michael Sungaila，两人团队），2025 年发布的浏览器 3D 多人小游戏
> 一句话简介："It's a small planet, but someone's gotta make the deliveries." 玩家扮演邮差，在一颗小星球上送信

参考截图（和本文档在同一目录）：`ref-messenger-social.jpg`、`ref-messenger-title.jpg`

---

## 1. 风格定位（一句话）

**「手绘质感的赛璐璐 3D + 迷你星球 + 东亚街景的安静与陌生感」**

可以用这个标签来描述它：**Painterly Cel-Shaded Low-Poly / 手绘风卡通渲染**。
坊间对它的比喻是："Jet Set Radio 的卡通渲染，套在 Mario Galaxy 那么大的星球上"。

作者自己说的创作意图：
- 想传达一种**介于「陌生」和「平静」之间的感觉**，就像去某些亚洲国家（日本街巷、东南亚老城区）旅行时的那种感受
- **描边和配色**是一开始就定下的核心，宁可放弃更"欢快"的方案，也要保留这股 **indie 味**
- 他们最满意的是**「手绘感」的图形**，以及 3D 环境里的细节密度

---

## 2. 风格关键词

| 维度 | 关键词 |
|---|---|
| 情绪 | 安静、慵懒、治愈、轻微的陌生感、日常、生活气息 |
| 渲染 | 卡通渲染 (Toon/Cel shading)、2~3 阶硬光影、几乎没有高光 |
| 线条 | 深色描边、粗细不均、带手绘抖动感，不是完美均匀的矢量线 |
| 形体 | 低中模 (low/mid-poly)、方块感的建筑、团簇状的树冠 |
| 色彩 | 低饱和、偏灰绿/灰蓝，中间点缀少量暖橙红 |
| 质感 | 平涂色块 + 笔刷纹理（树冠、岩石、地面都是"画上去"的） |
| 世界观 | 迷你星球 (tiny planet)、东亚城镇 + 山林 + 工业管道混搭 |

---

## 3. 色彩系统

从官方宣传图里提取的主色（取色结果，只做参考）：

| 用途 | 色值 | 说明 |
|---|---|---|
| 背景 / 天空 / 海 | `#65C1BE` ~ `#81BFBC` | **最标志性的颜色**：青绿、薄荷蓝，大面积使用 |
| 浅水 / 雾气 | `#92CCC1` / `#95C7C0` | 比背景稍亮，用来做水面和星球周围的光晕 |
| 植被暗部 | `#5B6B58` / `#5C6359` | 灰绿色，不是纯绿 |
| 植被亮部 | `#78A194` / `#7D8E7B` | 同样低饱和 |
| 建筑 / 混凝土 | `#9DA098` / `#A7AEA0` | 灰绿偏暖的水泥色 |
| 高光 / 白墙 / 云 | `#F2F5E8` / `#E9E8CE` | **偏米黄的白**，不用纯白 |
| 点缀色（管道 / 屋顶 / 灯塔） | 约 `#C8553D` / `#E07A3F` | 铁锈红、橙色，面积很小但很抢眼 |
| UI 强调色 | 约 `#E8C547` | 按钮的芥末黄 |
| 描边 | 约 `#3A4040` | 深灰偏冷，**不是纯黑** |

**配色原则：**
1. **大面积冷色（青绿）+ 小面积暖色（锈红 / 橙 / 黄）**，冷暖比例大概 85 : 15
2. 所有颜色都**降了饱和度、偏一点灰**，这是"安静感"的主要来源
3. 白色偏米黄、黑色偏灰，**画面里没有纯黑也没有纯白**
4. 阴影不是简单地把颜色调暗，而是**往冷色（蓝绿）偏**

---

## 4. 造型与渲染

### 4.1 光影
- 2~3 阶的硬边明暗（亮面 / 暗面，最多再加一个过渡），**不做平滑渐变**
- 基本没有镜面高光、没有 PBR 的金属或粗糙度质感
- 环境光比较亮，阴影不会死黑，整体是"阴天 / 柔光"的氛围

### 4.2 描边
- 物体的外轮廓有深色描边，**粗细会变化**，看起来像手画的
- 内部的结构线（窗框、屋檐、台阶）也会有线，但比外轮廓细
- 描边颜色跟着物体的颜色走（偏深灰或深绿），不用纯黑

### 4.3 纹理（这是和普通卡通渲染拉开差距的关键）
- 树冠：不是光滑的球，而是**不规则的笔刷块面**，边缘有锯齿和缺口
- 岩石 / 土地：棕色色块上叠了**干笔刷 / 斑驳的笔触**
- 云：白色的剪纸形状，边缘不规则，还带着描边
- 背景：纯色青绿上散落着**小颗粒、小碎片**，像纸上的墨点

### 4.4 形体与场景
- 建筑：方盒子 + 屋檐 + 空调外机 + 电线杆 + 晾衣架，**东亚老城区的杂乱感**
- 场景混搭：住宅区、山林、水池、红色工业管道 / 灯塔
- 因为是**小星球**，所有东西都沿着球面弯曲，走直线就能绕星球一圈，没有看不见的空气墙

---

## 5. 字体与 UI

- 标题字体：**方块 / 像素感的粗体几何字**，笔画转角是直角，带立体的挤出阴影（深灰色）
- 字的颜色：米白色 + 深灰描边 / 侧面
- 按钮：芥末黄的立体块状按钮（例如 "ENTER"），同样有描边和厚度
- UI 整体：**像实体小物件一样有厚度**，和 3D 世界的手绘感统一

---

## 6. 推荐的风格方向

根据你想做的东西，我推荐下面几个方向（从"最接近原作"到"更有自己特色"排列）：

### 方案 A：忠实还原「Messenger 风」⭐ 推荐入门
- 青绿背景 + 低饱和灰绿 + 锈橙点缀
- 卡通渲染 + 手绘描边 + 笔刷纹理
- 适合：小星球 / 城镇 / 生活模拟类的作品
- **注意**：直接照搬会显得像山寨版，建议至少换掉主色调或者题材

### 方案 B：换一套色调（同样的技法，不同的情绪）
| 变体 | 主色 | 点缀色 | 情绪 |
|---|---|---|---|
| 黄昏版 | 灰紫 `#8E7FA8` / 暮粉 `#D9A5A0` | 路灯黄 `#F2C14E` | 怀旧、下班路上 |
| 雪国版 | 灰蓝 `#A9BCC9` / 雪白 `#EEF1EC` | 朱红 `#C0392B` | 清冷、寂静 |
| 夏日版 | 天蓝 `#7EC8E3` / 草绿 `#9CC57A` | 西瓜红 `#E86A5B` | 明快、假期 |
| 夜晚版 | 深靛 `#2E3A59` / 墨绿 `#2F4F4A` | 霓虹青 `#4FE3C1`、粉 `#FF7AA2` | 城市夜景、赛博但温柔 |

### 方案 C：往更"绘本"的方向走
- 减弱描边，加强纸张纹理和水彩晕染
- 参考：*Sable*（Moebius 风线条）、*A Short Hike*（像素 + 低模）、*Wheel World*

### 方案 D：往更"日式动画"的方向走
- 描边更干净、配色更饱和、加入天空渐变和云的体积
- 参考：*Jet Set Radio*、*Hi-Fi Rush*、新海诚 / 吉卜力的背景配色

---

## 7. 可以一起参考的作品

| 作品 | 可以借鉴的点 |
|---|---|
| **Sable** | 线条、大面积平涂、安静的氛围 |
| **Wheel World** | 同样是低饱和 + 卡通渲染 |
| **A Short Hike** | 小世界、治愈感、探索感 |
| **Jet Set Radio** | 卡通渲染 + 描边的鼻祖 |
| **Super Mario Galaxy** | 小星球的结构设计 |
| **Townscaper / Tiny Glade** | 迷你世界的手感 |
| **吉卜力（尤其是背景美术）** | 生活气息、电线杆、晾衣架这类细节 |

---

## 8. 技术实现要点（如果要自己做 3D）

原作的技术栈：**Blender + Houdini 建模 → Substance 做纹理 → three.js 前端，Shader 全部自己写**；用 three-mesh-bvh 做碰撞优化，多人联机是 Node.js + WebSocket。

自己复刻时的简化思路：

1. **卡通光照**：`MeshToonMaterial` + 一张 2~3 阶的 gradientMap；或者自己写 shader，用 `step()` / `smoothstep()` 把 N·L 切成几档
2. **描边**
   - 简单方案：背面外扩法（inverted hull），把法线方向外扩后只渲染背面
   - 进阶方案：后处理，用深度 + 法线做边缘检测，再用噪声扰动线宽，得到手绘抖动感
3. **手绘纹理**：在 Substance / Procreate 里画笔刷质感的贴图，或者在 shader 里叠一层屏幕空间的纸张 / 笔触噪声
4. **树冠**：用多个不规则的面片或者 alpha 剪切的笔刷贴图拼成团簇，而不是一个球
5. **小星球**：场景在球面上，重力方向 = 指向球心，相机自动对准角色
6. **氛围**：背景用纯色 + 漂浮的小碎片粒子；用雾把远处的颜色往背景色混

可以参考的开源仿作（仅供学习技法，原作的美术资源版权归 Abeto 所有）：
- [Glowin/messager](https://github.com/Glowin/messager) — Vite + TS + three.js，MeshToonMaterial + OutlineEffect
- [arafays/messenger-copy](https://github.com/arafays/messenger-copy) — SvelteKit + three.js

---

## 9. AI 出图 / 概念图的提示词参考

**英文 Prompt（Midjourney / SD 等）：**
```
tiny planet diorama, cel-shaded low-poly 3D, hand-drawn ink outlines with varying line weight,
painterly brush textures, muted desaturated palette, teal mint background,
sage green foliage, concrete grey buildings, small rust-orange accents,
quiet East Asian town with power lines and air conditioners, calm and slightly strange atmosphere,
indie game art, soft overcast lighting, no specular highlights
```

**负面提示词：**
```
photorealistic, PBR, glossy, specular highlights, high saturation, neon, pure black, gradient sky, bloom, lens flare
```

---

## 10. Do / Don't 速查

| ✅ Do | ❌ Don't |
|---|---|
| 大面积用一个标志性的背景色 | 用很多高饱和的颜色互相打架 |
| 降低饱和度，颜色偏灰 | 用纯黑的描边和纯白的高光 |
| 描边粗细不均，带手绘感 | 用完美均匀的矢量描边 |
| 平涂色块 + 笔刷纹理 | 用 PBR 材质、反光、金属质感 |
| 少量暖色点缀，引导视线 | 暖色用得太多，失去安静感 |
| 塞满生活化的小细节（电线、招牌、晾衣架） | 场景干净到像样板间 |
| UI 做成有厚度、有描边的实体小物件 | 用扁平化的系统默认 UI |

---

### 资料来源
- [Messenger 官网](https://messenger.abeto.co)
- [Communication Arts 对作者 Vicente Lucendo 的采访](https://www.commarts.com/webpicks/messenger)
- [Wikipedia: Messenger (video game)](https://en.wikipedia.org/wiki/Messenger_(video_game))
- [Three.js Showcase: Messenger Abeto](https://threejsresources.com/showcase/messenger-abeto)
- [WebGPU Community Showcase: Messenger](https://www.webgpu.com/showcase/messenger/)
