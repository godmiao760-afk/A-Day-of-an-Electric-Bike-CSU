// ===== Boot：加载素材，缺图时生成色块占位（A 负责）=====
class Boot extends Phaser.Scene {
  constructor() { super('Boot'); }

  preload() {
    // 只加载 ASSETS 里标记 file: true 的素材
    for (const [key, a] of Object.entries(ASSETS.images)) {
      if (a.file) this.load.image(key, a.path || ('assets/img/' + key + '.png'));
    }
    for (const [key, sound] of Object.entries(ASSETS.sounds)) {
      const descriptor = sound && typeof sound === 'object' ? sound : null;
      const enabled = descriptor ? descriptor.file !== false : !!sound;
      if (!enabled) continue;
      this.load.audio(key, descriptor && descriptor.path
        ? descriptor.path
        : 'assets/sfx/' + key + '.mp3');
    }
    this.load.on('loaderror', (file) => console.warn('素材加载失败，将使用色块：', file.key));
  }

  create() {
    // 缺失的贴图生成色块
    for (const [key, a] of Object.entries(ASSETS.images)) {
      if (this.textures.exists(key)) {
        // 只为真实图片裁出显示帧；缺图时仍使用完整占位图。
        if (a.crop) {
          const c = a.crop;
          this.textures.get(key).add('trimmed', 0, c.x, c.y, c.w, c.h);
        }
        continue;
      }
      const g = this.add.graphics();
      if (a.outline) {
        g.lineStyle(3, a.color, 0.9).strokeRect(2, 2, a.w - 4, a.h - 4);
      } else {
        g.fillStyle(a.color, 1).fillRect(0, 0, a.w, a.h);
        // 车辆类加一条浅色"车头"，看得出朝向
        if (a.h > a.w && a.h >= 48) {
          g.fillStyle(0xffffff, 0.45).fillRect(3, 3, a.w - 6, 6);
        }
        // 瓦片加一点纹理
        if (a.w === 64 && a.h === 64) {
          g.lineStyle(1, 0x000000, 0.15).strokeRect(0, 0, 64, 64);
        }
      }
      g.generateTexture(key, a.w, a.h);
      g.destroy();
    }
    // 1×1 白色像素，画线条、特效用
    if (!this.textures.exists('px')) {
      const g = this.add.graphics();
      g.fillStyle(0xffffff, 1).fillRect(0, 0, 4, 4);
      g.generateTexture('px', 4, 4);
      g.destroy();
    }

    newGame();

    // 调试：直接跳到某个场景（在 main.js 里设置 DEBUG_START / DEBUG_STATE）
    if (typeof DEBUG_START !== 'undefined' && DEBUG_START) {
      if (DEBUG_START === 'Charge') GameState.clock = CONFIG.nightClock;
      Object.assign(GameState, DEBUG_STATE || {});
      this.scene.start(DEBUG_START, DEBUG_DATA || {});
    } else {
      this.scene.start('Title');   // 先进开始画面，按 F 再进 Intro
    }
  }
}
