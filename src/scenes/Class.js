// ===== Class：上课过场（A 负责）=====
class Class extends Phaser.Scene {
  constructor() { super('Class'); }

  create() {
    UI.setup(this);
    const s = GameState;
    const before = Math.max(0, s.battery);
    s.battery = Math.max(0, s.battery - CONFIG.dayDrain);
    s.clock = CONFIG.nightClock;

    const status = s.late
      ? '到教室时间：' + UI.fmt(s.arriveClock || CONFIG.classStart) + '　——　迟到了'
      : '到教室时间：' + UI.fmt(s.arriveClock) + '　——　准时！';

    const t1 = this.add.text(480, 170, LINES.classScene.during, UI.style(34)).setOrigin(0.5).setAlpha(0);
    const t2 = this.add.text(480, 230, status, UI.style(20, s.late ? '#f87171' : '#86efac')).setOrigin(0.5).setAlpha(0);
    const t3 = this.add.text(480, 300, LINES.classScene.after, UI.style(34)).setOrigin(0.5).setAlpha(0);
    const t4 = this.add.text(480, 360,
      LINES.classScene.drain + '，电量 ' + Math.round(before) + '% → ' + Math.round(s.battery) + '%',
      UI.style(20, '#fde68a')).setOrigin(0.5).setAlpha(0);
    const t5 = this.add.text(480, 440, '晚上 ' + UI.fmt(CONFIG.nightClock) + '，去找充电桩（按 F）',
      UI.style(18, '#9ca3af')).setOrigin(0.5).setAlpha(0);

    [t1, t2, t3, t4, t5].forEach((t, i) => {
      this.tweens.add({ targets: t, alpha: 1, duration: 400, delay: 300 + i * 700 });
    });

    this.ready = false;
    this.time.delayedCall(1200, () => { this.ready = true; });
    this.time.delayedCall(300 + 5 * 700 + 3000, () => UI.fadeTo(this, 'Charge'));  // 等 3 秒自动继续
  }

  update() {
    const f = UI.pressedF(this);
    if (this.ready && f) UI.fadeTo(this, 'Charge');
  }
}
