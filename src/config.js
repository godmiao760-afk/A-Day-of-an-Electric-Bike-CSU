// ===== 数值表（D 负责，只改数字）=====
// 改完保存，刷新浏览器就能试玩。
const CONFIG = {
  timeScale: 10,             // 现实 1 秒 = 游戏 10 秒
  startClock: 7 * 60 + 35,   // 7:35 出门找车
  classStart: 8 * 60,        // 8:00 上课，停好车晚于此时刻算迟到
  nightClock: 22 * 60 + 40,  // 22:40 开始找充电桩
  curfew: 23 * 60,           // 23:00 宿舍门禁
  firstDayBattery: 50,       // 第一天早上的电量
  dayDrain: 20,              // 白天额外耗电
  chargedThreshold: 60,      // 明早电量 ≥ 此值算"充上电"

  findCar: {
    rows: 5, cols: 10,       // 车阵行列数
    walkSpeed: 160,          // 步行速度（像素/秒）
    moveCarMinutes: 1        // 每挪开一辆车额外花的游戏分钟
  },
  ride: {
    length: 11000,           // 路长（像素），约骑 60 秒
    speed: 200,              // 骑行速度（像素/秒）
    sideSpeed: 180,          // 左右移动速度
    slopeSpeedFactor: 0.7,   // 坡道速度倍率
    slopeStart: 0.45,        // 坡道起点（路程比例）
    slopeEnd: 0.65,          // 坡道终点（路程比例）
    drainFlat: 0.5,          // 平路每秒耗电 %
    drainSlope: 1.0,         // 坡道每秒耗电 %
    maxHp: 3,
    invincibleMs: 1000,      // 被撞后无敌时间
    pickupPresses: 5,        // 扶车需要按几次 F
    fallBatteryCost: 10,     // 每摔一次掉多少电
    deadBatteryMinutes: 15,  // 没电推车额外花的游戏分钟
    spawnEvery: 1100         // 平均每隔多少毫秒生成一个障碍
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
