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

    this.add.text(480, 80, '小电驴的一天', UI.style(22, '#9ca3af')).setOrigin(0.5);
    this.add.text(480, 140, '第 ' + s.day + ' 天', UI.style(52, '#ffffff')).setOrigin(0.5);
    this.add.text(480, 220, line, UI.style(22, '#fde68a', {
      align: 'center', wordWrap: { width: 800, useAdvancedWrap: true }
    })).setOrigin(0.5);

    // 今早状态
    const money = s.money < 0 ? '欠 ¥' + (-s.money) : '¥' + s.money;
    const allowance = s.day > 1 ? '（' + LINES.intro.allowance + ' +¥' + CONFIG.money.allowance + '）' : '';
    this.add.text(480, 290, '电量 ' + Math.round(s.battery) + '%', UI.style(22,
      s.battery < 40 ? '#f87171' : '#86efac')).setOrigin(0.5);
    this.add.text(480, 325, '钱 ' + money + allowance + '　　饥饿 ' + Math.round(s.hunger) + '/100' +
      (isHungry() ? '（饿）' : ''), UI.style(18, s.money < 0 || isHungry() ? '#fca5a5' : '#e5e7eb')).setOrigin(0.5);
    // 累计迟到；最后一天再提醒一句
    this.add.text(480, 360, LINES.intro.lateCount.replace('{n}', s.lateCount) +
      (isLastDay() ? '　　' + LINES.intro.lastDay : ''),
      UI.style(18, s.lateCount ? '#fca5a5' : '#e5e7eb')).setOrigin(0.5);

    if (s.day === 1) {
      this.add.text(480, 415, 'WASD 移动　F 交互　E 背包　8:00 前停好车', UI.style(16, '#9ca3af')).setOrigin(0.5);
    } else if (s.hunger < CONFIG.hunger.faintWarn) {
      // 快饿晕了：预兆（用固定文字而不是气泡，气泡会盖住下面的"按 F 出门"）
      this.add.text(480, 415, LINES.faintWarn, UI.style(18, '#f87171')).setOrigin(0.5);
    }
    const tip = this.add.text(480, 470, '按 F 出门', UI.style(20, '#ffffff')).setOrigin(0.5);
    this.tweens.add({ targets: tip, alpha: 0.3, duration: 700, yoyo: true, repeat: -1 });

    // 点击也能开始（顺便解锁浏览器音频）
    this.input.once('pointerdown', () => UI.fadeTo(this, 'FindCar'));
  }

  update() {
    if (UI.pressedF(this)) UI.fadeTo(this, 'FindCar');
  }
}
