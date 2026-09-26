// ===== Ending：最终结局 / 隐藏结局（A 负责）=====
// 用 UI.fadeTo(this, 'Ending', { key }) 进入。key：
//   perfect / pass / fail —— 第 CONFIG.ending.totalDays 天下午课结束（Class 判定）
//   police —— 硬闯被抓；faint —— 饥饿 ≤ 0；broke —— 钱 ≤ 0
// 显示结局图（没图用色块）、标题、描述、统计。F 或点击：newGame() 回 Intro。
class Ending extends Phaser.Scene {
  constructor() { super('Ending'); }

  init(data) {
    this.key = (data && data.key) || 'pass';
  }

  create() {
    UI.setup(this);
    const s = GameState;
    const E = LINES.finalEnding[this.key] || LINES.finalEnding.pass;
    const hidden = ['police', 'faint', 'broke'].includes(this.key);
    const color = { perfect: '#86efac', pass: '#93c5fd', fail: '#f87171' }[this.key] || '#fbbf24';

    // 隐藏结局用深红底，正常结局用深蓝底
    this.add.rectangle(0, 0, 960, 540, hidden ? 0x1f0a0a : 0x0f172a).setOrigin(0);

    // 结局图：从小弹到正常大小
    const img = this.add.image(480, 170, 'end_' + this.key).setScale(0.6).setAlpha(0);
    this.tweens.add({ targets: img, scale: 1, alpha: 1, duration: 500, ease: 'Back.Out' });

    const t = this.add.text(480, 318, E.title, UI.style(34, color)).setOrigin(0.5).setAlpha(0);
    this.tweens.add({ targets: t, alpha: 1, duration: 400, delay: 400 });

    const d = this.add.text(480, 385, E.text, UI.style(18, '#e5e7eb', { align: 'center' }))
      .setOrigin(0.5).setAlpha(0);
    this.tweens.add({ targets: d, alpha: 1, duration: 400, delay: 800 });

    const money = s.money < 0 ? '欠 ¥' + (-s.money) : '¥' + s.money;
    const stats = LINES.endingUi.stats.replace('{day}', s.day).replace('{late}', s.lateCount)
      .replace('{runs}', s.runs).replace('{money}', money);
    this.add.text(480, 448, stats, UI.style(16, '#9ca3af')).setOrigin(0.5);

    const tip = this.add.text(480, 500, LINES.endingUi.restart, UI.style(20)).setOrigin(0.5);
    this.tweens.add({ targets: tip, alpha: 0.4, duration: 700, yoyo: true, repeat: -1 });

    UI.sfx(this, hidden ? 'fall' : 'park');

    // 等动画播完再允许重开，防止上一个场景按的 F 直接跳过
    this.ready = false;
    this.time.delayedCall(1200, () => {
      this.ready = true;
      this.input.once('pointerdown', () => this.restart());
    });
  }

  update() {
    const f = UI.pressedF(this);
    if (this.ready && f) this.restart();
  }

  restart() {
    if (this._leaving) return;
    newGame();
    UI.fadeTo(this, 'Intro');
  }
}
