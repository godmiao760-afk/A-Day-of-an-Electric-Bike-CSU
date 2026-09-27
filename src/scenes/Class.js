// ===== Class：上课过场（A 负责）=====
// data.part = 'morning'（上午课，结束后进中午节点）| 'afternoon'（下午课，结束后进傍晚节点）
// 每段课判迟到（lateCount 累计）、扣饥饿；下午课结束时扣白天耗电。
// 饿晕 / 没钱 → 隐藏结局；最后一天下午课结束 → 最终结局。
class Class extends Phaser.Scene {
  constructor() { super('Class'); }

  init(data) {
    this.part = (data && data.part) || 'morning';
  }

  create() {
    UI.setup(this);
    UI.sfx(this, 'class_bell');
    const s = GameState;
    const morning = this.part === 'morning';
    const H = CONFIG.hunger;

    // 判迟到：上午看 late（Ride / Park 判好的）；下午看中午选项花完的时间
    const pmArrive = s.clock;
    if (morning) {
      if (s.late) s.lateCount += 1;
    } else if (s.clock > CONFIG.afternoonClass) {
      s.latePM = true;
      s.lateCount += 1;
    }

    const hungerBefore = Math.round(s.hunger);
    s.hunger = Math.max(0, s.hunger - H.perClass);
    const batBefore = Math.round(Math.max(0, s.battery));
    if (!morning) s.battery = Math.max(0, s.battery - CONFIG.dayDrain);
    s.clock = morning ? CONFIG.noonClock : CONFIG.eveningClock;

    const lines = [];
    lines.push([morning ? LINES.classScene.morning : LINES.classScene.afternoon, 34, '#ffffff']);
    const late = morning ? s.late : s.latePM;
    const arrive = morning ? (s.arriveClock || CONFIG.classStart) : pmArrive;
    lines.push(['到教室时间：' + UI.fmt(arrive) + (late ? '　——　迟到了' : '　——　准时！'), 20,
      late ? '#f87171' : '#86efac']);
    lines.push([LINES.classScene.lateTotal.replace('{n}', s.lateCount), 18, s.lateCount ? '#fca5a5' : '#9ca3af']);
    lines.push([LINES.classScene.after, 34, '#ffffff']);
    lines.push(['饥饿 ' + hungerBefore + ' → ' + Math.round(s.hunger) +
      (isHungry() ? '　' + LINES.classScene.hungry : ''), 20, isHungry() ? '#f87171' : '#fde68a']);
    // 快饿晕了：预兆（饿晕的话下一步直接进结局，不用提示）
    if (s.hunger > 0 && s.hunger < H.faintWarn) lines.push([LINES.faintWarn, 20, '#f87171']);
    if (!morning) {
      lines.push([LINES.classScene.drain + '，电量 ' + batBefore + '% → ' + Math.round(s.battery) + '%', 20, '#fde68a']);
    }
    lines.push([UI.fmt(s.clock) + '　按 F 继续', 18, '#9ca3af']);

    // 行数变多了，行距从 64 收一点，保证最多 8 行也放得下
    const gap = lines.length > 6 ? 56 : 64;
    const top = 270 - (lines.length - 1) * gap / 2;
    lines.forEach((l, i) => {
      const t = this.add.text(480, top + i * gap, l[0], UI.style(l[1], l[2])).setOrigin(0.5).setAlpha(0);
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
    // 优先级：隐藏结局（昏倒 / 没钱）> 最后一天下午课结束的最终结局 > 照常进中午 / 傍晚
    // 自动计时和按 F 可能各调一次，fadeTo 自己会防重
    const k = hiddenEndingKey();
    if (k) { UI.fadeTo(this, 'Ending', { key: k }); return; }
    if (this.part === 'afternoon' && isLastDay()) { UI.fadeTo(this, 'Ending', { key: finalEndingKey() }); return; }
    UI.fadeTo(this, 'Node', { kind: this.part === 'morning' ? 'noon' : 'evening' });
  }
}
