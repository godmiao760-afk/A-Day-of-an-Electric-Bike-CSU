# 项目说明（CLAUDE.md）：《小电驴的一天》

> 全队和 AI 共用的唯一依据。**让 AI 写代码前，先让它读这份文件。**
> 设计有变动，先改这里，再改代码。Claude Code 会自动读取本文件。

## 1. 一句话介绍

以一辆电动车的视角，体验中南大学学生骑电动车的一天：早上找车 → 骑车上课 → 教学楼停车 → 晚上找桩充电。俯视角 2D，键盘操作。今晚充了多少电，就是明早出门时的电量。

## 2. 技术约定（AI 必须遵守）

- 引擎 **Phaser 3.90.0**，CDN 引入（见 index.html）。**只用 Phaser 3 写法**，不要用 Phaser 2/CE 或 Phaser 4 的 API。
- 纯 JavaScript。不用 TypeScript、npm、打包工具、第三方库。
- 普通 `<script>` 按顺序加载，**不用 import / export**。
- 全局对象：`CONFIG`、`LINES`、`ASSETS`、`GameState`、`UI`、各场景类、`newGame()`、`nextDay()`。
- 画面 960×540，Arcade 物理，无重力（俯视角）。
- 本地运行：VS Code + Live Server 插件，右键 index.html → Open with Live Server。
- 没有美术时自动用色块占位（Boot 场景生成）。

## 3. 操作

WASD 移动；F 交互（查看、挪车、解锁、停车、扫码、扶车、确认）；扶车既指 Ride 里摔倒后自己扶车，也指 Park 里撞倒别人的车后逐辆扶起。E 背包（骑车时不能开）；弹窗里 A/D（竖排时 W/S）切换、F 确认，也可鼠标点。

## 4. 文件与负责人

```
index.html              A   加载顺序：config → lines → assets → state → ui → scenes → main
src/config.js           D   数值表 CONFIG（只改数字）
src/lines.js            D   文案 LINES（只改文字）
src/assets.js           C   素材清单 ASSETS（放了图片就把 file 改成 true）
src/state.js            A   GameState、newGame()、nextDay()
src/ui.js               A   公用工具（见第 7 节）
src/main.js             A   创建游戏；DEBUG_START 调试开关
src/scenes/Boot.js      A   加载素材、生成色块
src/scenes/Intro.js     A   "第 N 天"字幕
src/scenes/FindCar.js   B   场景1 找车
src/scenes/Ride.js      A   场景2 骑行
src/scenes/NodeScene.js A   选择节点（校门口 / 中午 / 傍晚）
src/scenes/Park.js      B   场景3/3′ 停车
src/scenes/Class.js     A   上课过场
src/scenes/Charge.js    B   场景4 充电
src/scenes/Result.js    A   结算
assets/img/  assets/sfx/    C
```

**调试：** main.js 里 `DEBUG_START = 'Ride'`（或 'Park' / 'Charge' / 'Result'）直接从该场景开始；测推车用 `DEBUG_START = 'Park'` + `DEBUG_DATA = { pushing: true }`。**演示前改回 null。** 物理碰撞框：main.js 里 `debug: true`。

## 5. 全局状态 GameState

```js
day            // 第几天
clock          // 游戏内分钟数，可带小数。455 = 7:35
clockPaused    // 为 true 时时钟暂停
battery        // 电量 0–100，唯一跨天保留的数据
hp             // 血量，只在 Ride 使用
late           // 是否迟到
hits, falls    // 被撞 / 摔倒次数（Ride 写）
findCarMinutes // 找车用时（FindCar 写）
arriveClock    // 停好车的时刻（Park 写）
chargeResult   // 'none' | 'noMoney' | 'watch' | 'full' | 'unplugged'（Charge 写）
chargeGain     // 今晚充进去多少电（Charge 写）

// 跨天保留
money          // 钱，可为负（欠款）
hunger         // 饱腹度 0–100，< hunger.hungryBelow 算饿，移动变慢
items          // { helmet: true, license: false }
helmetOn       // 头盔戴上没有（背包里切换）

// 每天重置
route          // 'inside' | 'outside'（Node 校门口写）
passenger      // 是否载着同学（Node 写，Ride 送到/跑掉后清掉）
policeToday    // 今天有没有交警（第 1 天必有）；有的话每个可能碰上的地方再单独掷 police.encounterChance
fines          // [{ reason, amount }]（交警罚款 + 门口违停贴条）
earned, spent  // 今天赚 / 花的钱（花销不含罚款）
meals          // ['食堂', '后湖']
```
字段名和含义不许改；新增字段先在群里说，再改这里。

state.js 里的工具函数：`isHungry()`、`speedMul()`（饿了返回 hungrySpeed）、`spend(钱)`、`eat(饱腹)`、`policeCheck(是否载人)`（扣钱、加时间、返回 {passed, fines, total}）、`policeText(结果)`。

## 6. 时钟

- 现实 1 秒 = 游戏 `CONFIG.timeScale` 秒。统一用 `UI.tickClock(this, delta)`，不要自己写。
- 走钟的场景：FindCar、Ride、Park、Charge。弹窗打开时自动暂停，独白气泡不暂停。

## 7. 公用工具 UI（ui.js）

```js
UI.setup(scene)           // 每个场景 create() 第一行调用：注册按键 this.keys、重置状态、淡入
UI.blocked(scene)         // 弹窗中或正在切场景时为 true
UI.dir(scene)             // WASD → {x, y}
UI.pressedF(scene)        // 这一帧刚按下 F。★ 每帧在 update 开头调用一次存进变量：const f = UI.pressedF(this);
UI.fmt(clock)             // 455 → "07:35"
UI.createClock(scene)     // 右上角时钟
UI.tickClock(scene, delta)
UI.createHud(scene, showHp) / UI.updateHud(scene)   // 左上角电量条（+ 血量格）
UI.say(scene, text, target)   // 独白气泡，text 可以是数组（随机一句），target 传精灵则跟随头顶
UI.hint(scene, text)          // 底部操作提示，传 null 隐藏
UI.choice(scene, question, options, onPick)   // 选项弹窗。options 是字符串或 {label, disabled}；2 个横排 A/D，3 个以上竖排 W/S；onPick(序号)
UI.alert(scene, text, onClose)                // 只有"继续"的提示框
UI.backpack(scene, onClose)                   // 背包（钱、饥饿、戴/摘头盔、牌照）
UI.pressedE(scene)                            // 这一帧刚按下 E（开背包），用法同 pressedF
UI.fadeTo(scene, key, data)   // 淡出切场景
UI.sfx(scene, key)            // 播放音效；没有素材时用合成音
UI.rand(arrOrStr)             // 数组随机取一个
```

## 8. 场景流程

```
Boot → Intro → FindCar → Node{gate} → Ride ─┬─ 到达 → Park {pushing:false} ─┐
                                            └─ 没电 → Park {pushing:true}  ─┤
   Class{morning} ←─────────────────────────────────────────────────────────┘
   → Node{noon} → Class{afternoon} → Node{evening} → Charge → Result → [F] Intro（第二天）
```

- **Node**（NodeScene.js，类名 NodeScene、场景 key 'Node'，因为 Node 和浏览器全局重名）：纯菜单。
  - gate 校门口：同学求搭车（第 1 天必出现，之后按 `passenger.chance`）。答应 → passenger=true，强制走校外；否则选 校内 / 校外 / 背包。
  - noon / evening：食堂、后湖（耗电 `places.houhu.battery`，今天有交警时按 `encounterChance` 可能被查）、办牌照（仅中午）、不吃、背包。钱或电不够的选项置灰。
- **交警**：`policeToday` 每天掷一次（第 1 天必有）。有交警的日子，校外骑行、中午后湖、傍晚后湖**各自再掷一次** `police.encounterChance`，碰上才查（第 1 天校外骑行必碰上）。校外路线检查点在 `policeAt` 处。没戴头盔 / 没牌照 / 载人各罚一笔，被罚耽误 `delayMinutes`。载人被罚 → 同学跑掉不给钱；安全送到 → +`passenger.reward`。
- **饥饿**：每段课 −`perClass`，过夜 −`overnight`；饿了 FindCar / Park / Charge / Ride 移动都变慢。
- **钱**：每天早上 +`allowance`；充电扫码 −`money.charge`，钱不够 → chargeResult='noMoney'。

- **Intro**：第 1 天用 `LINES.intro.day1`；之后电量 < 40 用 `low`，否则 `ok`。
- **FindCar**：7:35 开始。在 `background/dorm.png` 的三排停车区找车；主角车使用 `vehical/protagonist.png`，其他车使用 `1.png`～`7.png`。主角车位置随机且左右有邻车，按 F 确认后亮起标记；先挪开一辆邻车（每辆 +`moveCarMinutes` 分钟）才能解锁。步行使用左右三帧动画，上下移动沿用最近的左右朝向；解锁后隐藏步行人物和原地车辆，显示 `character/riding/driving.png` 的骑车合成图，再进入校门口。越近"滴滴"越快 + 右上角信号格。无失败条件。
- **Ride**：纵向长路，W 前进 S 刹车 A/D 换道。只在移动时耗电，坡道更快更慢。障碍：外卖车（后方冲上）、逆行车（迎面）、行人（横穿）、校车（慢、大）。被撞 hp−1 + 无敌闪烁；hp=0 摔倒，连按 F 扶车 → 回满血、掉 `fallBatteryCost` 电、falls+1。电量 ≤ 0 → late=true、clock+`deadBatteryMinutes` → 推车进 Park。到顶 → Park。
- **Park**：车棚大多满，`freeSlots` 个空位（不在入口附近）。推车时速度减半、显示"已迟到"。站到空位按 F 停车 → 记录 arriveClock，晚于 8:00 则 late=true。
  - **多米诺**：骑 / 推着车撞到别人的车，按 `dominoChance` 从被撞那辆开始往远离玩家的方向倒一排（最多 `dominoMax` 辆，遇到空位 / 排尾停）。靠近倒着的车按 F 扶起（每辆 +`liftMinutes` 分钟）；没扶完不能停车。
  - **门口违停**：入口旁红色"禁停"区，按 F → 二选一。停了照常记 arriveClock / 迟到，然后按 `ticketChance` 被保安贴条：罚 `ticketFine`，记进 `fines`（不算 spent）。
- **Class**：上午课结束时钟跳到 12:00；下午课结束扣 `dayDrain` 电，时钟跳到 17:30。
- **Charge**：到 23:00 门禁。桩状态随机：被占 / 坏了 / 扫码失败（第一次必失败，之后按概率成功）/ 空闲。插上后二选一：守着（每分钟 +`watchPerMinute`% 到 23:00）/ 回宿舍（`gambleWinRate` 充满，否则只 +`unpluggedGain`%）。门禁前没插上 → 'none'。
- **Result**：充上电 = battery ≥ `chargedThreshold`。结局：准时+充上「难得顺利的一天」；准时+没充上「明天早上见分晓」；迟到+充上「至少明天有电了」；迟到+没充上「明天还得推车」。F 开始第二天（保留电量、钱、饥饿、背包；过夜饿 `overnight`，到账 `allowance`），R 重新开始。

## 9. 素材约定（C）

图片默认放 `assets/img/<key>.png`，也可在 `src/assets.js` 使用 `path` 指向项目内的相对路径，然后把 `file` 改成 `true`。`w/h` 为占位图尺寸；实际显示尺寸和碰撞框由场景配置。可选 `crop: { x, y, w, h }` 由 Boot 注册 `trimmed` 帧，用于去除透明留白，不改原图。**车辆类图片车头朝上。** 找车使用独立的 `dorm_*` 和 `player_walk_*` key，其他场景的原有贴图约定保持不变。音效放 `assets/sfx/<key>.mp3`，同样在 assets.js 里改 true。

## 10. 给 AI 的工作规则

1. 只改被指定的文件；要改别人的文件，先说明原因。
2. 不改约定：GameState 字段、CONFIG 结构、UI 函数名、贴图 key、场景 key。
3. 数字进 CONFIG，文字进 LINES，不要写死在场景里。
4. 场景间只通过 GameState 和 `UI.fadeTo(scene, key, data)` 传信息。
5. 新场景 create() 第一行 `UI.setup(this)`；update 开头 `const f = UI.pressedF(this);`。
6. 一次只做一个功能，改动尽量小，不要顺手重构。
7. 代码加简短中文注释。
8. 改完说明：改了哪里、怎么测试（DEBUG_START 设成什么、按什么键、应看到什么）。

### 提示词模板

```
先阅读 CLAUDE.md。
任务：在 src/scenes/Park.js 里加"碰到旁边的车会倒一排，要按 F 扶起来"。
只改 Park.js，必要的新数值加到 config.js 的 park 里，新文案加到 lines.js 的 park 里。
完成后告诉我怎么测试。
```
```
先阅读 CLAUDE.md。
现象：（描述）
F12 控制台报错：（粘贴完整报错）
相关文件：src/scenes/xxx.js
找出原因并修复，只改必要的地方。
```

## 11. 分支协作（Git）

| 分支 | 谁用 | 只改这些 |
|---|---|---|
| `main` | 写代码的两位（A / B / D） | `src/**`（除了 assets.js 的 `file` 那一栏）、`index.html`、`CLAUDE.md` |
| `branch-v1` | 美工（C） | `assets/img/`、`assets/sfx/`、`src/assets.js` 里的 `file: true/false` |

规则：
1. **切分支前先提交**（`git add -A && git commit -m "..."`），否则没提交的改动会被覆盖。AI 正在改文件时不要切分支。
2. 新贴图 key 由 main 加到 assets.js（写代码的人知道要用什么）；美工只把 `file` 改成 true，不增删 key。这样两边几乎不会冲突。
3. 同步节奏：每 1–2 小时一次，或者美工交一批素材后。
   ```
   # 美工：先拿到最新代码
   git checkout branch-v1
   git pull
   git merge origin/main
   git push

   # 写代码的：再把素材合进来
   git checkout main
   git pull
   git merge origin/branch-v1
   git push
   ```
4. 合并冲突时：`src/**` 里的代码以 main 为准；`assets/` 和 `file` 标记以 branch-v1 为准。解决完 `git add` + `git commit`。
5. CLAUDE.md 只在 main 上改，随合并同步到 branch-v1；美工有意见在群里说。
6. 演示用 main 分支（先合一次 branch-v1）。

## 12. 加分项（第 9 小时功能冻结前有空再做）

~~停车多米诺效果~~（已做）；~~门口违停选项~~（已做）；背景音乐；手机虚拟摇杆；下雨天气。
