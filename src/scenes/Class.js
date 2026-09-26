// ===== Class：上课过场（A 负责）=====
// data.part = 'morning'（上午课，结束后进中午节点）| 'afternoon'（下午课，结束后进傍晚节点）
// 每段课扣饥饿；下午课结束时扣白天耗电。
class Class extends Phaser.Scene {
  constructor() { super('Class'); }

  init(data) {
    this.part = (data && data.part) || 'morning';
  }

  create() {
    UI.setup(this);
    const s = GameState;
    const morning = this.part === 'morning';
    const H = CONFIG.hunger;

    const hungerBefore = Math.round(s.hunger);
    s.hunger = Math.max(0, s.hunger - H.perClass);
    const batBefore = Math.round(Math.max(0, s.battery));
    if (!morning) s.battery = Math.max(0, s.battery - CONFIG.dayDrain);
    s.clock = morning ? CONFIG.noonClock : CONFIG.eveningClock;

    const lines = [];
    lines.push([morning ? LINES.classScene.morning : LINES.classScene.afternoon, 34, '#ffffff']);
    if (morning) {
      const status = s.late
        ? '到教室时间：' + UI.fmt(s.arriveClock || CONFIG.classStart) + '　——　迟到了'
        : '到教室时间：' + UI.fmt(s.arriveClock) + '　——　准时！';
      lines.push([status, 20, s.late ? '#f87171' : '#86efac']);
    }
    lines.push([LINES.classScene.after, 34, '#ffffff']);
    lines.push(['饥饿 ' + hungerBefore + ' → ' + Math.round(s.hunger) +
      (isHungry() ? '　' + LINES.classScene.hungry : ''), 20, isHungry() ? '#f87171' : '#fde68a']);
    if (!morning) {
      lines.push([LINES.classScene.drain + '，电量 ' + batBefore + '% → ' + Math.round(s.battery) + '%', 20, '#fde68a']);
    }
    lines.push([UI.fmt(s.clock) + '　按 F 继续', 18, '#9ca3af']);

    const top = 270 - (lines.length - 1) * 32;
    lines.forEach((l, i) => {
      const t = this.add.text(480, top + i * 64, l[0], UI.style(l[1], l[2])).setOrigin(0.5).setAlpha(0);
      this.tweens.add({ targets: t, alpha: 1, duration: 400, delay: 300 + i * 600 });
    });

    this.ready = false;
    this.time.delayedCall(1000, () => { this.ready = true; });
    this.time.delayedCall(300 + lines.length * 600 + 3000, () => this.next());  // 等 3 秒自动继续
  }

  update() {
    const f = UI.pressedF(this);
    if (this.ready && f) this.next();
  }

  next() {
    UI.fadeTo(this, 'Node', { kind: this.part === 'morning' ? 'noon' : 'evening' });
  }
}
