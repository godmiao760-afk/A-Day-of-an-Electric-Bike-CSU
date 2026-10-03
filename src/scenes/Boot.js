// ===== Boot：加载素材，缺图时生成色块占位（A 负责）=====
class Boot extends Phaser.Scene {
  constructor() { super('Boot'); }

  preload() {
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
        if (a.removeCheckerBackground) this.prepareRiderTexture(key);
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

  // 只清除与画布边缘连通的浅灰棋盘格，保留人物内部的浅色衣服和车身。
  prepareRiderTexture(key) {
    const source = this.textures.get(key).getSourceImage();
    const canvas = document.createElement('canvas');
    canvas.width = source.width;
    canvas.height = source.height;
    const ctx = canvas.getContext('2d', { willReadFrequently: true });
    ctx.drawImage(source, 0, 0);
    const pixels = ctx.getImageData(0, 0, canvas.width, canvas.height);
    const { data, width, height } = pixels;
    const seen = new Uint8Array(width * height);
    const queue = new Int32Array(width * height);
    let head = 0, tail = 0;
    const visit = i => {
      if (seen[i]) return;
      seen[i] = 1;
      const p = i * 4;
      const min = Math.min(data[p], data[p + 1], data[p + 2]);
      const max = Math.max(data[p], data[p + 1], data[p + 2]);
      if (data[p + 3] === 0 || (min >= 185 && max - min <= 18)) {
        data[p + 3] = 0;
        queue[tail++] = i;
      }
    };
    for (let x = 0; x < width; x++) { visit(x); visit((height - 1) * width + x); }
    for (let y = 0; y < height; y++) { visit(y * width); visit(y * width + width - 1); }
    while (head < tail) {
      const i = queue[head++], x = i % width, y = Math.floor(i / width);
      if (x > 0) visit(i - 1);
      if (x < width - 1) visit(i + 1);
      if (y > 0) visit(i - width);
      if (y < height - 1) visit(i + width);
    }
    let left = width, top = height, right = -1, bottom = -1;
    for (let y = 0; y < height; y++) for (let x = 0; x < width; x++) {
      if (!data[(y * width + x) * 4 + 3]) continue;
      left = Math.min(left, x); right = Math.max(right, x);
      top = Math.min(top, y); bottom = Math.max(bottom, y);
    }
    if (right < left) return;
    ctx.putImageData(pixels, 0, 0);
    const texture = this.textures.createCanvas(key + '_clean', right - left + 1, bottom - top + 1);
    texture.context.drawImage(canvas, left, top, texture.width, texture.height,
      0, 0, texture.width, texture.height);
    texture.refresh();
    this.textures.remove(key);
    this.textures.renameTexture(key + '_clean', key);
  }
}
