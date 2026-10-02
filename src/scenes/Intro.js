// ===== Intro："第 N 天"开场字幕（A 负责）=====
// data.lastCharge：昨晚的充电结果（Result 按 F 时传进来，因为 nextDay() 已经把 chargeResult 重置了）
class Intro extends Phaser.Scene {
  constructor() { super('Intro'); }

  init(data) {
    this.lastCharge = (data && data.lastCharge) || 'none';
  }

  create() {
    UI.setup(this);
    const s = GameState;

    // 过夜扣完饥饿可能饿晕（nextDay 已在 Result 里调用过）；钱 ≤ 0 同理
    if (s.day > 1) {
      const k = hiddenEndingKey();
      if (k) { UI.fadeTo(this, 'Ending', { key: k }); return; }
    }

    let line;
    if (s.day === 1) line = LINES.intro.day1;
    else if (s.battery < 40) line = LINES.intro.low;
    else line = LINES.intro.ok;
    // 昨晚插上桩的结果到今天早上才揭晓，放在开场文案前面
    if (s.day > 1 && (this.lastCharge === 'full' || this.lastCharge === 'unplugged')) {
      line = LINES.charge[this.lastCharge] + '\n' + line;
    }

    DailyUI.intro(this, line, () => this.leave());
  }

  leave() {
    if (UI.blocked(this) || this.time.now < UI.lockUntil) return;
    UI.fadeTo(this, 'FindCar');
  }

  update() {
    if (UI.pressedF(this)) this.leave();
  }
}
