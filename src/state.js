// ===== 全局状态（A 负责）=====
// 字段名和含义不许改；要新增字段，先在群里说，再改 CLAUDE.md。
const GameState = {
  day: 1,               // 第几天
  clock: 455,           // 游戏内时间，单位"分钟"，可带小数。455 = 7:35
  clockPaused: false,   // 弹窗时为 true，时钟暂停
  battery: 50,          // 电量 0–100（跨天保留）
  hp: 3,                // 血量，只在 Ride 使用
  late: false,          // 是否迟到
  hits: 0,              // 被撞次数（Ride 写入）
  falls: 0,             // 摔倒次数（Ride 写入）
  findCarMinutes: 0,    // 找车用了几分钟（FindCar 写入）
  arriveClock: null,    // 停好车的时刻（Park 写入）
  chargeResult: 'none', // 'none' | 'noMoney' | 'watch' | 'full' | 'unplugged'（Charge 写入）
  chargeGain: 0,        // 今晚充进去多少电（Charge 写入）

  // ---- 跨天保留 ----
  money: 100,           // 钱，可以为负（欠款）
  hunger: 70,           // 饱腹度 0–100，越低越饿
  items: { helmet: true, license: false },  // 背包：有没有头盔 / 车上有没有牌照
  helmetOn: false,      // 头盔戴上没有（背包里切换）

  // ---- 每天重置 ----
  route: 'inside',      // 'inside' 校内 | 'outside' 校外（Node 写入）
  passenger: false,     // 是否正载着同学（Node 写入，Ride 送到/跑掉后清掉）
  policeToday: false,   // 今天有没有交警
  fines: [],            // 今天的罚款 [{ reason, amount }]
  earned: 0,            // 今天赚的钱
  spent: 0,             // 今天花的钱（不含罚款）
  meals: []             // 今天吃了哪些 ['食堂', '后湖']
};

// 重置一天内的数据（跨天字段除外）
function resetDay() {
  const s = GameState;
  s.clock = CONFIG.startClock;
  s.clockPaused = false;
  s.hp = CONFIG.ride.maxHp;
  s.late = false;
  s.hits = 0;
  s.falls = 0;
  s.findCarMinutes = 0;
  s.arriveClock = null;
  s.chargeResult = 'none';
  s.chargeGain = 0;
  s.route = 'inside';
  s.passenger = false;
  s.policeToday = s.day === 1 ? true : Math.random() < CONFIG.police.chance;  // 第一天必有交警
  s.fines = [];
  s.earned = 0;
  s.spent = 0;
  s.meals = [];
}

// 新游戏：全部重置
function newGame() {
  const s = GameState;
  s.day = 1;
  s.battery = CONFIG.firstDayBattery;
  s.money = CONFIG.money.start;
  s.hunger = CONFIG.hunger.start;
  s.items = { helmet: true, license: false };
  s.helmetOn = false;
  resetDay();
}

// 开始第二天：保留电量、钱、背包；过夜变饿，生活费到账
function nextDay() {
  const s = GameState;
  s.day += 1;
  s.hunger = Math.max(0, s.hunger - CONFIG.hunger.overnight);
  s.money += CONFIG.money.allowance;
  resetDay();
}

// ---------- 小工具 ----------
function isHungry() { return GameState.hunger < CONFIG.hunger.hungryBelow; }
function speedMul() { return isHungry() ? CONFIG.hunger.hungrySpeed : 1; }   // 饿了移动变慢
function spend(amount) { GameState.money -= amount; GameState.spent += amount; }
function eat(food) { GameState.hunger = Math.min(100, GameState.hunger + food); }
function earn(amount) { GameState.money += amount; GameState.earned += amount; }

// 统一记录不计入日常花销的罚款（允许余额变成负数）
function addFine(reason, amount) {
  GameState.money -= amount;
  GameState.fines.push({ reason, amount });
}

// 结算规则集中在状态层，Result 只负责展示
function isCharged() {
  return GameState.battery >= CONFIG.chargedThreshold;
}

function getEndingKey() {
  return (GameState.late ? 'late' : 'ontime') + '_' + (isCharged() ? 'charged' : 'empty');
}

// 交警检查：返回 { passed, fines: [{reason, amount}], total }，并直接扣钱、加时间
function policeCheck(carrying) {
  const s = GameState, F = CONFIG.police.fines, L = LINES.police;
  const fines = [];
  if (!s.helmetOn) fines.push({ reason: L.helmet, amount: F.helmet });
  if (!s.items.license) fines.push({ reason: L.license, amount: F.license });
  if (carrying) fines.push({ reason: L.carry, amount: F.carry });
  const total = fines.reduce((a, f) => a + f.amount, 0);
  fines.forEach(f => addFine(f.reason, f.amount));
  s.clock += fines.length ? CONFIG.police.delayMinutes : CONFIG.police.passMinutes;
  return { passed: fines.length === 0, fines, total };
}

// 把检查结果变成弹窗文字
function policeText(r) {
  const L = LINES.police;
  if (r.passed) return L.pass;
  const lines = r.fines.map(f => '· ' + f.reason + '　罚 ¥' + f.amount);
  return L.fineHead + '\n' + lines.join('\n') + '\n合计 ¥' + r.total +
    '，耽误 ' + CONFIG.police.delayMinutes + ' 分钟';
}
