// ===== 数值表（D 负责，只改数字）=====
// 改完保存，刷新浏览器就能试玩。
const CONFIG = {
  timeScale: 10,             // 现实 1 秒 = 游戏 10 秒
  startClock: 7 * 60 + 35,   // 7:35 出门找车
  classStart: 8 * 60,        // 8:00 上课，停好车晚于此时刻算迟到
  noonClock: 12 * 60,        // 上午课结束
  eveningClock: 17 * 60 + 30,// 下午课结束
  nightClock: 22 * 60 + 40,  // 22:40 开始找充电桩
  curfew: 23 * 60,           // 23:00 宿舍门禁
  firstDayBattery: 50,       // 第一天早上的电量
  dayDrain: 20,              // 白天额外耗电（下午课结束时扣）
  chargedThreshold: 60,      // 明早电量 ≥ 此值算"充上电"

  money: {
    start: 100,              // 第一天的钱
    allowance: 30,           // 每天早上到账的生活费
    charge: 2                // 充一次电的钱
  },
  hunger: {
    start: 70,               // 第一天饱腹度（0–100，越低越饿）
    perClass: 35,            // 每上一段课消耗
    overnight: 20,           // 过一夜消耗
    hungryBelow: 30,         // 低于此值算"饿"
    hungrySpeed: 0.7         // 饿的时候移动速度倍率
  },
  places: {
    canteen: { cost: 12, food: 45 },               // 食堂
    houhu:   { cost: 25, food: 70, battery: 10 },  // 后湖：贵、吃得饱、要骑车过去耗电
    license: { cost: 30 }                          // 办牌照
  },
  police: {
    chance: 0.5,             // 第 2 天起，每天有交警的概率（第 1 天必有）
    delayMinutes: 10,        // 被罚耽误的游戏分钟
    passMinutes: 1,          // 检查合格也要停一下
    fines: { helmet: 20, license: 30, carry: 30 }  // 没戴头盔 / 没牌照 / 载人
  },
  passenger: {
    chance: 0.5,             // 第 2 天起，校门口有同学求搭车的概率（第 1 天必有）
    reward: 15,              // 送到后给的钱
    speedFactor: 0.85,       // 载人速度倍率
    drainFactor: 1.3         // 载人耗电倍率
  },

  findCar: {
    rows: 5, cols: 10,       // 车阵行列数
    walkSpeed: 160,          // 步行速度（像素/秒）
    moveCarMinutes: 1        // 每挪开一辆车额外花的游戏分钟
  },
  ride: {
    speed: 200,              // 骑行速度（像素/秒）
    sideSpeed: 180,          // 左右移动速度
    slopeSpeedFactor: 0.7,   // 坡道速度倍率
    drainFlat: 0.45,         // 平路每秒耗电 %
    drainSlope: 1.0,         // 坡道每秒耗电 %
    maxHp: 3,
    invincibleMs: 1000,      // 被撞后无敌时间
    pickupPresses: 5,        // 扶车需要按几次 F
    fallBatteryCost: 10,     // 每摔一次掉多少电
    deadBatteryMinutes: 15,  // 没电推车额外花的游戏分钟
    routes: {
      // length 路长（像素）；spawnEvery 平均每隔多少毫秒生成障碍；slope 坡道起止（路程比例，null=没坡）
      // policeAt 交警检查点位置（路程比例，null=没有）；npc 各类障碍出现权重
      inside: {
        length: 12000, spawnEvery: 1100, slope: [0.45, 0.65], policeAt: null,
        npc: { delivery: 2, wrong: 2.5, walker: 3.5, bus: 2, car: 0 }
      },
      outside: {
        length: 6500, spawnEvery: 900, slope: null, policeAt: 0.55,
        npc: { delivery: 3.5, wrong: 2.5, walker: 1, bus: 0, car: 3 }
      }
    }
  },
  park: {
    rideSpeed: 120,          // 车棚里骑车速度
    pushSpeedFactor: 0.5,    // 推车速度倍率
    freeSlots: 2             // 空车位数量
  },
  charge: {
    piles: 8,                // 充电桩总数
    free: 1, qrFail: 2, broken: 2,  // 其余为 occupied
    walkSpeed: 110,          // 推车速度
    qrRetryChance: 0.5,      // 扫码重试成功率
    watchPerMinute: 5,       // 守着时每游戏分钟充多少 %（15 分钟 ≈ 75%）
    gambleWinRate: 0.5,      // 回宿舍后充满的概率
    unpluggedGain: 20        // 被拔线时只充进去多少 %
  }
};
