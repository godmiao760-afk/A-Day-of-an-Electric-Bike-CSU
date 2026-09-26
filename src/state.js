// ===== 全局状态（A 负责）=====
// 字段名和含义不许改；要新增字段，先在群里说，再改 项目说明.md。
const GameState = {
  day: 1,               // 第几天
  clock: 455,           // 游戏内时间，单位"分钟"，可带小数。455 = 7:35
  clockPaused: false,   // 弹窗时为 true，时钟暂停
  battery: 50,          // 电量 0–100。唯一跨天保留的数据
  hp: 3,                // 血量，只在 Ride 使用
  late: false,          // 是否迟到
  hits: 0,              // 被撞次数（Ride 写入）
  falls: 0,             // 摔倒次数（Ride 写入）
  findCarMinutes: 0,    // 找车用了几分钟（FindCar 写入）
  arriveClock: null,    // 停好车的时刻（Park 写入）
  chargeResult: 'none', // 'none' | 'watch' | 'full' | 'unplugged'（Charge 写入）
  chargeGain: 0         // 今晚充进去多少电（Charge 写入）
};

// 重置一天内的数据（电量除外）
function resetDay() {
  GameState.clock = CONFIG.startClock;
  GameState.clockPaused = false;
  GameState.hp = CONFIG.ride.maxHp;
  GameState.late = false;
  GameState.hits = 0;
  GameState.falls = 0;
  GameState.findCarMinutes = 0;
  GameState.arriveClock = null;
  GameState.chargeResult = 'none';
  GameState.chargeGain = 0;
}

// 新游戏：全部重置
function newGame() {
  GameState.day = 1;
  GameState.battery = CONFIG.firstDayBattery;
  resetDay();
}

// 开始第二天：只保留电量
function nextDay() {
  GameState.day += 1;
  resetDay();
}
