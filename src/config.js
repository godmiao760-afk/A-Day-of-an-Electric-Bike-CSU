// ===== 数值表（D 负责，只改数字）=====
// 改完保存，刷新浏览器就能试玩。
const CONFIG = {
  timeScale: 15,             // 现实 1 秒 = 游戏 15 秒（v2：10 → 15，压缩演示时长）
  startClock: 7 * 60 + 35,   // 7:35 出门找车
  classStart: 8 * 60,        // 8:00 上课，停好车晚于此时刻算迟到
  noonClock: 12 * 60,        // 上午课结束
  afternoonClass: 14 * 60,   // 14:00 下午上课，中午选项花完时间晚于此算下午迟到
  eveningClock: 17 * 60 + 30,// 下午课结束
  nightClock: 22 * 60 + 40,  // 22:40 开始找充电桩
  curfew: 23 * 60,           // 23:00 宿舍门禁
  firstDayBattery: 50,       // 第一天早上的电量
  dayDrain: 20,              // 白天额外耗电（下午课结束时扣）
  chargedThreshold: 60,      // 明早电量 ≥ 此值算"充上电"

  ending: {
    totalDays: 5,            // 第几天下午课结束判最终结局（演示可改 3）
    passMaxLate: 5           // 迟到 0 次 = 完美；≤ 此值 = 合格；更多 = 不合格
  },

  money: {
    start: 100,              // 第一天的钱
    allowance: 30,           // 每天早上到账的生活费
    charge: 2,               // 充一次电的钱
    lowWarn: 20              // 低于此值 HUD 上的钱变红（预兆：钱 ≤ 0 进"没钱"结局）
  },
  hunger: {
    start: 80,               // 第一天饱腹度（0–100，越低越饿；≤ 0 进"昏倒"结局）
    perClass: 25,            // 每上一段课消耗
    overnight: 15,           // 过一夜消耗
    hungryBelow: 30,         // 低于此值算"饿"
    hungrySpeed: 0.7,        // 饿的时候移动速度倍率
    faintWarn: 15            // 低于此值独白"眼前发黑"（预兆）
  },
  places: {
    // minutes：去一趟花多少游戏分钟（随机区间）；中午花完晚于 14:00 下午就迟到
    canteen: { cost: 12, food: 45, minutes: [40, 60] },                // 食堂
    houhu:   { cost: 25, food: 70, battery: 10, minutes: [90, 130] },  // 后湖：贵、吃得饱、要骑车过去耗电
    license: { cost: 30, minutes: [100, 140] }                         // 办牌照
  },
  police: {
    chance: 0.5,             // 第 2 天起，每天有交警的概率（第 1 天必有）
    delayMinutes: 10,        // 被罚耽误的游戏分钟
    passMinutes: 1,          // 检查合格也要停一下
    encounterChance: 0.6,    // 有交警的日子，校外骑行 / 中午后湖 / 傍晚后湖 各自再掷一次，碰上的概率（第 1 天校外骑行必碰上）
    fines: { helmet: 20, license: 30, carry: 30 },  // 没戴头盔 / 没牌照 / 载人
    // 硬闯：被抓 → 隐藏结局"派出所"。被抓概率 = base + 之前成功闯过的次数 × step，最多 max
    runCatchBase: 0.3,
    runCatchStep: 0.15,
    runCatchMax: 0.9
  },
  passenger: {
    chance: 0.5,             // 第 2 天起，校门口有同学求搭车的概率（第 1 天必有）
    reward: 15,              // 送到后给的钱
    speedFactor: 0.85,       // 载人速度倍率
    drainFactor: 1.3         // 载人耗电倍率
  },

  findCar: {
    rows: 3, cols: 7,        // 宿舍背景中的三排车位
    world: { width: 960, height: 640, left: 240, right: 855, top: 48, bottom: 620 },
    layout: { left: 362, top: 125, colGap: 60, rowGap: 165 },
    spawn: { x: 285, y: 560 }, // 宿舍门外的步行通道
    bike: { width: 34, height: 78, bodyWidth: 28, bodyHeight: 65 },
    person: { width: 42, height: 64, bodyWidth: 22, bodyHeight: 16 },
    rider: { width: 36, height: 84 },
    walkFrameRate: 7,
    interactionRange: 40,   // 人物脚底到车辆碰撞框边缘的距离
    moveDistance: 40,
    moveAngle: 25,
    moveDuration: 350,
    mountDuration: 1000,
    signalStep: 120,
    beepDistanceFactor: 1.6, beepMin: 140, beepMax: 1400,
    walkSpeed: 160,          // 步行速度（像素/秒）
    moveCarMinutes: 1,       // 每挪开一辆车额外花的游戏分钟
    // 多米诺：挪开邻车时可能带倒一排，全部扶起来才能解锁
    dominoChance: 0.4,
    dominoMax: 4,
    dominoDelayMs: 90,       // 一辆接一辆倒下的间隔（毫秒）
    fallAngle: 80,           // 倒下的角度（纯画面）
    fallShift: 8,            // 倒下时顺带往外滑的像素（纯画面）
    liftMinutes: 0.5         // 每扶起一辆花的游戏分钟
  },
  ride: {
    speed: 240,              // 骑行最快速度（像素/秒）（v2：200 → 240）
    sideSpeed: 200,          // 左右移动速度（v2：180 → 200）
    slopeSpeedFactor: 0.7,   // 坡道速度倍率
    drainFlat: 0.8,          // 平路每秒耗电 %（路变短了，每秒耗电调高，一趟总耗电和 v1 差不多）
    drainSlope: 1.8,         // 坡道每秒耗电 %
    maxHp: 3,
    invincibleMs: 1000,      // 被撞后无敌时间
    pickupPresses: 5,        // 扶车需要按几次 F
    fallBatteryCost: 10,     // 每摔一次掉多少电
    deadBatteryMinutes: 15,  // 没电推车额外花的游戏分钟
    followGap: 90,           // 同车道前后车最小间距（像素），不够就减速排队 / 变道
    laneChangeSpeed: 400,    // NPC 换道的横向速度（像素/秒）
    wrongSameLane: 0.5,      // 平时逆行车出现在玩家这条道的概率
    runProtectMs: 2000,      // 硬闯成功后的无敌时间
    // 有真图时的显示尺寸（像素）；没图时按占位色块原尺寸
    // body：碰撞框占显示尺寸的比例 [宽, 高]；不在这里的障碍（汽车、校车）按 [0.8, 0.85]
    sizes: {
      rider:    { width: 36, height: 84, body: [0.75, 0.75] },  // 主角骑车（俯视）
      delivery: { width: 40, height: 86, body: [0.8, 0.85] },   // 外卖车
      wrong:    { width: 34, height: 80, body: [0.8, 0.85] },   // 逆行车（没专门的图时用别的同学骑车图 + 染色）
      walker:   { width: 42, height: 63, body: [0.5, 0.7] },    // 横穿的行人（原图左右留白多，碰撞框窄一点）
      bus:      { width: 58, height: 184, body: [0.85, 0.92] }, // 校车 / 洒水车
      car:      { width: 56, height: 100, body: [0.85, 0.9] },  // 小轿车（校外）
      fall:     { width: 190, height: 190 }, // 摔倒：趴地 / 站起来看车（1024 画布）
      lift:     { width: 144, height: 108 }, // 扶车逐帧（512×384 画布，和摔倒图人物一样大）
      police:   { width: 54, height: 81 }    // 检查点交警（342×512 逐帧）
    },
    policeFrameRate: 6,      // 交警挥指挥棒动画帧率
    // 道路真图：放大倍数 + 图里路面中线的 x（原图像素）；倍数按"图里路面宽 × 倍数 ≈ 游戏路宽 400"算
    roadArt:  { scale: 1.53, centerX: 517 },   // road_tile（图里路面约 386–648）
    landmark: { scale: 0.89, centerX: 766 },   // road_stadium（图里路面约 540–990）
    wrongTints: [0xa5d8ff, 0xfecaca, 0xbbf7d0, 0xe9d5ff],  // 逆行同学的染色，免得和主角长一样
    walkerFrameRate: 8,      // 行人走路动画帧率
    fallStandMs: 700,        // 趴在地上多久后站起来看着车（毫秒）
    liftDoneMs: 450,         // 扶正后停一下再骑上去（毫秒）
    // 早高峰单行道：每天每条路线掷一次 chance；range 路段（路程比例）里逆行权重 × wrongMul，
    // 逆行车出现在玩家这条道的概率变成 sameLaneChance（平时 0.5）
    oneWay: { chance: 0.5, range: [0.3, 0.7], wrongMul: 3, sameLaneChance: 0.8 },
    routes: {
      // length 路长（像素）；spawnEvery 平均每隔多少毫秒生成障碍；slope 坡道起止（路程比例，null=没坡）
      // policeAt 交警检查点位置（路程比例，null=没有）；npc 各类障碍出现权重
      // landmarkAt 体育场那张路图的中心位置（路程比例，null=没有）
      inside: {
        length: 7200, spawnEvery: 1100, slope: [0.45, 0.65], policeAt: null, landmarkAt: 0.25,
        npc: { delivery: 2, wrong: 2.5, walker: 3.5, bus: 2, car: 0 }
      },
      outside: {
        length: 4000, spawnEvery: 900, slope: null, policeAt: 0.55, landmarkAt: null,
        npc: { delivery: 3.5, wrong: 2.5, walker: 1, bus: 0, car: 3 }
      }
    }
  },
  park: {
    rideSpeed: 120,          // 车棚里骑车速度
    pushSpeedFactor: 0.5,    // 推车速度倍率
    freeSlots: 2,            // 空车位数量
    // 多米诺：骑 / 推着车撞到别人的车，可能倒一排，全部扶起来才能停车
    dominoChance: 0.5,       // 撞上一次倒下的概率
    dominoMax: 6,            // 最多连着倒几辆（遇到空位或排尾就停）
    dominoDelayMs: 90,       // 一辆接一辆倒下的间隔（毫秒）
    dominoCooldownMs: 1500,  // 撞车判定一次后，多久内不再判定（防止贴着车每帧都掷骰子）
    liftMinutes: 0.5,        // 每扶起一辆花的游戏分钟
    // 有真图时的显示尺寸（像素）；body 是碰撞框（像素）
    bike: { width: 30, height: 68, bodyWidth: 26, bodyHeight: 56 },   // 车棚里停着的车
    rider: { width: 30, height: 70, bodyWidth: 22, bodyHeight: 22 },  // 骑车的主角（碰撞框小一点，方便钻进车位）
    pusher: { width: 72, height: 54, bodyWidth: 22, bodyHeight: 22 }, // 推车的主角（侧视，只左右翻转）
    pushWalk: { width: 40, height: 60 },                              // 推车逐帧图（342×512）的显示尺寸，碰撞框沿用 pusher
    // 门口违停：离入口最近，省时间，但可能被贴条
    ticketChance: 0.5,       // 被贴条的概率
    ticketFine: 20           // 贴条罚款
  },
  charge: {
    piles: 8,                // 充电桩总数
    free: 1, qrFail: 2, broken: 2,  // 其余为 occupied
    walkSpeed: 110,          // 推车速度
    qrRetryChance: 0.5,      // 扫码重试成功率
    // v2：去掉"守着"。插上就回宿舍，看运气
    gambleWinRate: 0.6,      // 充满的概率
    unpluggedGain: 30,       // 被拔线时只充进去多少 %
    // 有真图时的显示尺寸（像素）；body 是碰撞框（像素）
    bike: { width: 34, height: 78 },                                   // 桩前停着的车（别人的 / 插上后自己的）
    pusher: { width: 96, height: 72, bodyWidth: 30, bodyHeight: 40 }, // 推车的主角（侧视，只左右翻转）
    pushWalk: { width: 53, height: 80 },                              // 推车逐帧图（342×512）的显示尺寸，碰撞框沿用 pusher
    // 有背景图 bg_charge 时：桩对准图里画出来的桩（图里画了 18 根，挑 8 根能用的，从左到右，屏幕像素）
    artPileX: [139, 219, 339, 430, 526, 611, 690, 795],   // 桩的 x（个数要 ≥ piles，不够就退回色块排法）
    artPileY: 140,                                         // 桩的 y
    artBayX:  [130, 214, 346, 435, 524, 614, 701, 790],   // 每根桩前面那个车位的中心 x（车停这里）
    artBayY:  198                                          // 车位中心 y
  }
};
