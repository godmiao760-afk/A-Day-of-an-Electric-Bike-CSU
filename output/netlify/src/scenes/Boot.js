// ===== Boot：加载素材，缺图时生成色块占位（A 负责）=====
class Boot extends Phaser.Scene {
  constructor() { super('Boot'); }

  preload() {
    // 在线加载期间展示进度；资源超时仍走已有的色块回退。
    this.load.imageLoadType = 'XHR';
    this.load.xhr.timeout = CONFIG.loading.timeout;
    this.load.maxParallelDownloads = CONFIG.loading.parallel;
    this.add.text(480, 225, LINES.loading.title, { fontSize: '28px', color: '#ffffff' }).setOrigin(0.5);
    const progress = this.add.text(480, 280, '', { fontSize: '20px', color: '#d5e5ca' }).setOrigin(0.5);
    const updateProgress = value => progress.setText(LINES.loading.progress.replace('{n}', Math.round(value * 100)));
    updateProgress(0);
    this.load.on('progress', updateProgress);
    this.load.once('loaderror', () => this.add.text(480, 330, LINES.loading.failed, { fontSize: '16px', color: '#e5c99d' }).setOrigin(0.5));
    document.getElementById('startup-status')?.remove();
    // 只加载 ASSETS 里标记 file: true 的素材
    for (const [key, a] of Object.entries(ASSETS.images)) {
      if (a.file) this.load.image(key, a.path || ('assets/img/' + key + '.png'));
    }
    for (const [key, definition] of Object.entries(ASSETS.sounds)) {
      // Legacy boolean entries remain supported; explicit entries use { file: true, path }.
      // WAV, MP3, M4A and other extensions are loaded from the supplied path.
      const hasFile = definition === true || (definition && definition.file);
      if (!hasFile) continue;
      const path = typeof definition === 'object' && definition.path
        ? definition.path
        : 'assets/sfx/' + key + '.mp3';
      this.load.audio(key, path);
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
      // 让场景识别真正的缺图，使用原有的备用布局。
      a.file = false;
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
