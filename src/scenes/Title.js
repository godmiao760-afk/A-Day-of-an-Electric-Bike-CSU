// ===== Title：开始画面（封面图 + 按 F 开始）=====
// Boot 加载完 → Title → 按 F / 点击 → Intro（第 1 天）。
// 封面图 cover 已经画好了标题字，这里只铺满画面、加一句"按 F 开始"。没图时显示文字标题。
class Title extends Phaser.Scene {
  constructor() { super('Title'); }

  create() {
    UI.setup(this);

    if (UI.hasArt('cover')) {
      // 封面：按比例铺满 960×540（多出来的上下裁掉），再慢慢推近一点，画面不死板
      const bg = this.add.image(480, 270, 'cover');
      const s = Math.max(960 / bg.width, 540 / bg.height);
      bg.setScale(s);
      this.tweens.add({ targets: bg, scale: s * 1.05, duration: 9000, ease: 'Sine.InOut', yoyo: true, repeat: -1 });
    } else {
      // 没图：深色底 + 文字标题
      this.add.rectangle(0, 0, 960, 540, 0x14301a).setOrigin(0);
      this.add.text(480, 230, LINES.title.name, UI.style(64, '#fef3c7', {
        stroke: '#2f5d1e', strokeThickness: 10
      })).setOrigin(0.5);
    }

    // 底部"按 F 开始"：半透明圆角底 + 描边字，一闪一闪
    const g = this.add.graphics();
    g.fillStyle(0x000000, 0.4).fillRoundedRect(480 - 130, 470 - 24, 260, 48, 24);
    const tip = this.add.text(480, 470, LINES.title.start, UI.style(24, '#ffffff', {
      stroke: '#2f5d1e', strokeThickness: 5
    })).setOrigin(0.5);
    this.tweens.add({ targets: tip, alpha: 0.35, duration: 700, yoyo: true, repeat: -1 });

    // 点击也能开始（顺便解锁浏览器音频）
    this.input.once('pointerdown', () => this.start());
  }

  update() {
    const f = UI.pressedF(this);
    if (f) this.start();
  }

  start() {
    if (this._leaving) return;
    UI.fadeTo(this, 'Intro');
  }
}
