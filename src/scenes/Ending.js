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
    const base = hidden ? 0x1f0a0a : 0x0f172a;
    this.add.rectangle(0, 0, 960, 540, base).setOrigin(0);
    const endKey = 'end_' + this.key;
    const hasEnd = UI.hasArt(endKey);
    // 背景：有结局图就用它铺满（派出所没结局图时退回 bg_police），模糊 + 用底色压暗，让中间的插画卡和文字清楚
    const bgKey = hasEnd ? endKey : (this.key === 'police' && UI.hasArt('bg_police') ? 'bg_police' : null);
    if (bgKey) {
      const bg = this.add.image(480, 270, bgKey);
      bg.setScale(Math.max(960 / bg.width, 540 / bg.height));   // cover：按比例铺满，多的上下裁掉
      if (bg.preFX) bg.preFX.addBlur(1, 2, 2, 1.2);              // WebGL 才有模糊，Canvas 下跳过
      this.add.rectangle(0, 0, 960, 540, base, 0.72).setOrigin(0);
    }

    // 结局图：从小弹到正常大小。真图（1536×1024）缩成 378×252 的插画卡加描边；没图时是 320×240 色块
    const card = this.add.container(480, hasEnd ? 156 : 170).setScale(0.6).setAlpha(0);
    const img = this.add.image(0, 0, endKey);
    if (hasEnd) {
      img.setScale(252 / img.height);
      const w = img.displayWidth, h = img.displayHeight;
      card.add(this.add.rectangle(6, 8, w + 12, h + 12, 0x000000, 0.45));   // 投影
      card.add(this.add.rectangle(0, 0, w + 12, h + 12, 0xfef3c7).setStrokeStyle(2, 0x000000, 0.35)); // 米色相框
    }
    card.add(img);
    this.tweens.add({ targets: card, scale: 1, alpha: 1, duration: 500, ease: 'Back.Out' });
    // 派出所有背景图、但还没有结局图时，不显示占位色块
    if (!hasEnd && bgKey) card.setVisible(false);

    const t = this.add.text(480, 318, E.title, UI.style(34, color)).setOrigin(0.5).setAlpha(0);
    this.tweens.add({ targets: t, alpha: 1, duration: 400, delay: 400 });

    const d = this.add.text(480, 385, E.text, UI.style(18, '#e5e7eb', { align: 'center' }))
      .setOrigin(0.5).setAlpha(0);
    this.tweens.add({ targets: d, alpha: 1, duration: 400, delay: 800 });

    const money = s.money < 0 ? '欠 ¥' + (-s.money) : '¥' + s.money;
    const stats = LINES.endingUi.stats.replace('{day}', s.day).replace('{late}', s.lateCount)
      .replace('{runs}', s.runs).replace('{money}', money);
    this.add.text(480, 448, stats, UI.style(16, '#9ca3af')).setOrigin(0.5);

    const tip = this.add.text(480, 500,
      this.key === 'perfect' ? LINES.endingUi.dreamRestart : LINES.endingUi.restart,
      UI.style(20)).setOrigin(0.5);
    this.tweens.add({ targets: tip, alpha: 0.4, duration: 700, yoyo: true, repeat: -1 });

    // 结局各自使用专用音效：正常结局按评价播放，隐藏结局按触发原因播放。
    // 饥饿结局需要先有肚子叫，再播放昏倒声，增强因果感。
    const endingSfx = {
      perfect: 'ending_perfect',
      pass: 'ending_pass',
      fail: 'ending_fail',
      police: 'ending_police',
      broke: 'ending_broke'
    }[this.key];
    if (this.key === 'faint') {
      UI.sfx(this, 'ending_faint_belly');
      this.time.delayedCall(350, () => UI.sfx(this, 'ending_faint'));
    } else if (this.key === 'broke') {
      UI.sfx(this, endingSfx);
      this.time.delayedCall(500, () => UI.sfx(this, 'ending_broke_cry'));
    } else if (endingSfx) {
      UI.sfx(this, endingSfx);
    }

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
    // 完美结局彩蛋：先看小电驴的梦，梦醒了再回开始画面
    if (this.key === 'perfect') { UI.fadeTo(this, 'Ride', { dream: true }); return; }
    newGame();
    UI.fadeTo(this, 'Intro');
  }
}
