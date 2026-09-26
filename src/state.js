// ===== 全局状态（A 负责）=====
// 字段名和含义不许改；要新增字段，先在群里说，再改 CLAUDE.md。
const GameState = {
  // ---- 跨天保留 ----
  day: 1,               // 第几天
  battery: 50,          // 电量 0–100
  money: 100,           // 钱，可以是负数（欠款）
  hunger: 70,           // 饥饿值 0–100，越高越饱
  items: { helmet: true, license: false },  // 背包：有没有这件东西
  helmetOn: false,      // 头盔戴没戴

  // ---- 每天重置 ----
  clock: 455,           // 游戏内时间，单位"分钟"，可带小数。455 = 7:35
  clockPaused: false,   // 为 true 时时钟暂停
  hp: 3,                // 血量，只在 Ride 使用
  late: false,          // 是否迟到
  hits: 0,              // 被撞次数（Ride 写入）
  falls: 0,             // 摔倒次数（Ride 写入）
  findCarMinutes: 0,    // 找车用了几分钟（FindCar 写入）
  arriveClock: null,    // 停好车的时刻（Park 写入）
  route: 'inside',      // 'inside' 校内 | 'outside' 校外（Node 写入）
  passenger: false,     // 是否载着同学（Node 写入，Ride 结束时清掉）
  policeToday: false,   // 今天校外有没有交警（resetDay 决定）
  fines: [],            // 今天的罚款明细 [{ reason, amount }]
  earned: 0,            // 今天载人赚的钱
  spent: 0,             // 今天吃饭 / 办事 / 充电花的钱
  meals: [],            // 今天吃了什么，如 ['食堂', '后湖']
  chargeResult: 'none', // 'none' | 'watch' | 'full' | 'unplugged' | 'noMoney'（Charge 写入）
  chargeGain: 0         // 今晚充进去多少电（Charge 写入）
};

// 重置一天内的数据（跨天字段不动）
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
  s.route = 'inside';
  s.passenger = false;
  s.policeToday = s.day === 1 ? true : Math.random() < CONFIG.police.chance;  // 第一天必有交警
  s.fines = [];
  s.earned = 0;
  s.spent = 0;
  s.meals = [];
  s.chargeResult = 'none';
  s.chargeGain = 0;
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

// 开始第二天：保留电量、钱、饥饿、物品
function nextDay() {
  const s = GameState;
  s.day += 1;
  s.hunger = Math.max(0, s.hunger - CONFIG.hunger.overnight);
  s.money += CONFIG.money.allowance;   // 有欠款时自然先抵扣
  resetDay();
}

// ---- 小工具 ----
function isHungry() { return GameState.hunger < CONFIG.hunger.hungryBelow; }
// 所有移动速度都乘上它
function speedMul() { return isHungry() ? CONFIG.hunger.hungrySpeed : 1; }
// 花钱（记入今日支出），钱不够也照扣（变欠款）
function spend(amount) { GameState.money -= amount; GameState.spent += amount; }
// 吃东西
function eat(food) { GameState.hunger = Math.min(100, GameState.hunger + food); }

// ---- 交警检查（Ride 和 Node 去后湖时共用）----
// 返回 { passed, fines: [{reason, amount}], total }，并直接扣钱、加时间、记录罚款。
// carrying：这次是否载着人
function policeCheck(carrying) {
  const s = GameState, P = CONFIG.police;
  const list = [];
  if (!s.helmetOn) list.push({ reason: LINES.police.helmet, amount: P.fines.helmet });
  if (!s.items.license) list.push({ reason: LINES.police.license, amount: P.fines.license });
  if (carrying) list.push({ reason: LINES.police.carry, amount: P.fines.carry });
  const total = list.reduce((a, f) => a + f.amount, 0);
  s.money -= total;
  s.fines.push(...list);
  s.clock += list.length ? P.delayMinutes : P.passMinutes;
  return { passed: list.length === 0, fines: list, total };
}

// 交警检查结果的文字（弹窗用）
function policeText(r) {
  if (r.passed) return LINES.police.pass;
  const lines = r.fines.map(f => '· ' + f.reason + '　罚 ¥' + f.amount).join('\n');
  return LINES.police.fineHead + '\n' + lines + '\n合计 ¥' + r.total +
    '　耽误 ' + CONFIG.police.delayMinutes + ' 分钟';
}
