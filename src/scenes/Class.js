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
    const hungryBefore = isHungry();

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
    if (!hungryBefore && isHungry()) UI.sfx(this, 'hunger');
    const batBefore = Math.round(Math.max(0, s.battery));
    if (!morning) s.battery = Math.max(0, s.battery - CONFIG.dayDrain);
    s.clock = morning ? CONFIG.noonClock : CONFIG.eveningClock;

    const late = morning ? s.late : s.latePM;
    const arrive = morning ? (s.arriveClock || CONFIG.classStart) : pmArrive;
    // 保留原来的自动继续时长，以及上午/下午、饥饿预警的阅读时间差。
    const sections = 6 + (morning ? 0 : 1) + (s.hunger > 0 && s.hunger < H.faintWarn ? 1 : 0);
    const autoDelay = 300 + sections * 600 + 3000;
    const ending = hiddenEndingKey() || (!morning && isLastDay());
    this.ready = false;
    this._leaving = false;
    DailyUI.classResult(this, {
      morning, late, arrive, hungerBefore, batBefore,
      autoAt: this.time.now + autoDelay,
      nextLabel: ending ? '查看结局' : morning ? '前往午间行程' : '前往晚间行程'
    }, () => this.next());
    this.time.delayedCall(1000, () => { this.ready = true; });
    this.time.delayedCall(autoDelay, () => this.next());
  }

  update() {
    const f = UI.pressedF(this);
    if (this.ready && f) this.next();
  }

  next() {
    if (!this.ready || this._leaving || UI.blocked(this)) return;
    // 优先级：隐藏结局（昏倒 / 没钱）> 最后一天下午课结束的最终结局 > 照常进中午 / 傍晚
    // 按键、按钮和自动计时共用入口，避免重复进入下一场景。
    const k = hiddenEndingKey();
    if (k) { UI.fadeTo(this, 'Ending', { key: k }); return; }
    if (this.part === 'afternoon' && isLastDay()) { UI.fadeTo(this, 'Ending', { key: finalEndingKey() }); return; }
    UI.fadeTo(this, 'Node', { kind: this.part === 'morning' ? 'noon' : 'evening' });
  }
}
