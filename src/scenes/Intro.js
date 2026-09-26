// ===== Intro："第 N 天"开场字幕（A 负责）=====
class Intro extends Phaser.Scene {
  constructor() { super('Intro'); }

  create() {
    UI.setup(this);
    const s = GameState;

    let line;
    if (s.day === 1) line = LINES.intro.day1;
    else if (s.battery < 40) line = LINES.intro.low;
    else line = LINES.intro.ok;

    this.add.text(480, 110, '小电驴的一天', UI.style(22, '#9ca3af')).setOrigin(0.5);
    this.add.text(480, 170, '第 ' + s.day + ' 天', UI.style(52, '#ffffff')).setOrigin(0.5);
    this.add.text(480, 245, line, UI.style(22, '#fde68a', {
      align: 'center', wordWrap: { width: 800, useAdvancedWrap: true }
    })).setOrigin(0.5);

    // 今早状态
    const money = s.money < 0 ? '欠 ¥' + (-s.money) : '¥' + s.money;
    const allowance = s.day > 1 ? '（' + LINES.intro.allowance + ' +¥' + CONFIG.money.allowance + '）' : '';
    this.add.text(480, 305, '电量 ' + Math.round(s.battery) + '%', UI.style(22,
      s.battery < 40 ? '#f87171' : '#86efac')).setOrigin(0.5);
    this.add.text(480, 340, '钱 ' + money + allowance + '　　饥饿 ' + Math.round(s.hunger) + '/100' +
      (isHungry() ? '（饿）' : ''), UI.style(18, s.money < 0 || isHungry() ? '#fca5a5' : '#e5e7eb')).setOrigin(0.5);

    if (s.day === 1) {
      this.add.text(480, 405, 'WASD 移动　F 交互　E 背包　8:00 前停好车', UI.style(16, '#9ca3af')).setOrigin(0.5);
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
