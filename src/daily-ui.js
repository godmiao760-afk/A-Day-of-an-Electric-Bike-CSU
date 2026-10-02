// 每日开场和结算共用的「骑行仪表盘」。只负责绘制，不改变 GameState。
const DailyUI = {
  colors: { text: '#f5f4dc', muted: '#b5c8b5', accent: '#d5ec8d', warning: '#f0b595' },

  text(scene, x, y, value, size = 16, color = this.colors.text, extra = {}) {
    return scene.add.text(x, y, String(value), UI.style(size, color, extra));
  },

  box(scene, x, y, width, height, color, radius = 0, alpha = 1, border = null) {
    const g = scene.add.graphics().fillStyle(color, alpha);
    if (radius) g.fillRoundedRect(x, y, width, height, radius);
    else g.fillRect(x, y, width, height);
    if (border != null) {
      g.lineStyle(1, border);
      if (radius) g.strokeRoundedRect(x, y, width, height, radius);
      else g.strokeRect(x, y, width, height);
    }
    return g;
  },

  rule(scene, x1, y1, x2, y2, alpha = 0.4) {
    return scene.add.graphics().lineStyle(1, 0x8ba88a, alpha).lineBetween(x1, y1, x2, y2);
  },

  base(scene, night = false) {
    const key = night ? 'bg_charge' : 'dorm';
    this.box(scene, 0, 0, 960, 540, 0x183d38);
    if (UI.hasArt(key) && scene.textures.exists(key)) {
      const image = scene.add.image(480, 270, key);
      image.setScale(Math.max(960 / image.width, 540 / image.height));
    }
    this.box(scene, 0, 0, 960, 540, 0x183d38, 0, 0.87);
    this.box(scene, 22, 22, 916, 496, 0x173b36, 19, 0.35, 0x637d63);
    this.text(scene, 45, 41, '小电驴 / 骑行日志', 14, this.colors.muted);
    const total = CONFIG.ending.totalDays;
    this.text(scene, 718, 41, 'DAY ' + String(GameState.day).padStart(2, '0') +
      ' / ' + String(total).padStart(2, '0'), 14, this.colors.accent);
    // 默认五天；演示天数调整时，刻度仍保持在同一块区域内。
    for (let i = 0; i < Math.min(total, 10); i++) {
      const x = 738 + i * Math.min(35, 152 / Math.max(1, total - 1));
      scene.add.circle(x, 75, 4, i < GameState.day ? 0xd5ec8d : 0x4a6054);
      if (i < Math.min(total, 10) - 1) {
        this.rule(scene, x + 6, 75, x + Math.min(35, 152 / Math.max(1, total - 1)) - 6, 75, 0.5);
      }
    }
    this.rule(scene, 45, 82, 691, 82);
  },

  button(scene, x, y, width, key, label, action, primary = true) {
    const bg = primary ? 0xd5ec8d : 0x2b5047;
    const fg = primary ? '#233f35' : this.colors.muted;
    const shape = this.box(scene, x, y, width, 44, bg, 22);
    this.text(scene, x + 19, y + 10, key, 18, fg, { fontStyle: 'bold' });
    this.text(scene, x + 49, y + 12, label, 16, fg, { fontStyle: 'bold' });
    if (primary) this.text(scene, x + width - 31, y + 9, '→', 20, fg);
    const hit = scene.add.zone(x, y, width, 44).setOrigin(0).setInteractive({ useHandCursor: true });
    hit.on('pointerover', () => shape.setAlpha(0.82));
    hit.on('pointerout', () => shape.setAlpha(1));
    hit.on('pointerdown', action);
    return hit;
  },

  gauge(scene, battery) {
    const { text, muted, warning } = this.colors;
    const value = Phaser.Math.Clamp(battery, 0, 100);
    const low = battery < 40;
    const g = scene.add.graphics();
    g.lineStyle(17, 0x688576, 0.35).beginPath()
      .arc(724, 252, 115, Math.PI * 0.75, Math.PI * 2.25, false).strokePath();
    if (value > 0) {
      g.lineStyle(17, low ? 0xe7a076 : 0xd5ec8d).beginPath()
        .arc(724, 252, 115, Math.PI * 0.75, Math.PI * (0.75 + 1.5 * value / 100), false).strokePath();
    }
    for (let i = 0; i <= 20; i++) {
      const a = Math.PI * (0.75 + i * 1.5 / 20);
      g.lineStyle(2, 0xb0c49e, 0.5).lineBetween(724 + Math.cos(a) * 135, 252 + Math.sin(a) * 135,
        724 + Math.cos(a) * 142, 252 + Math.sin(a) * 142);
    }
    this.text(scene, 724, 181, '当前电量', 14, muted).setOrigin(0.5, 0);
    this.text(scene, 713, 213, Math.round(battery), 72, text, { fontFamily: 'Georgia, serif' }).setOrigin(0.5, 0);
    this.text(scene, 790, 251, '%', 22, low ? warning : this.colors.accent);
    this.text(scene, 724, 316, low ? '低电量 · 留意续航' : '续航准备就绪', 14,
      low ? warning : muted).setOrigin(0.5, 0);
  },

  intro(scene, line, leave) {
    const s = GameState;
    const c = this.colors;
    this.base(scene);
    this.text(scene, 45, 101, '第 ' + s.day + ' 天', 69, c.text, { fontStyle: 'bold' });
    this.text(scene, 49, 188, s.battery < 40 ? '电量不多，也要出发。' : '准备好了，出发吧。', 27, c.accent);
    const story = this.text(scene, 49, 237, line, 18, c.muted,
      { lineSpacing: 5, wordWrap: { width: 467, useAdvancedWrap: true } });
    // 充电结果与每日文案共存时允许换行，给下方数值留出空间。
    for (let size = 18; story.height > 88 && size > 14; ) story.setFontSize(--size);
    this.gauge(scene, s.battery);
    const stats = [
      ['余额', s.money < 0 ? '欠 ¥' + (-s.money) : '¥' + s.money, s.money < 0],
      ['饱腹度' + (isHungry() ? ' · 饿了' : ''), Math.round(s.hunger) + '/100', isHungry()],
      ['本周迟到', s.lateCount + ' 次', s.lateCount > 0]
    ];
    stats.forEach(([label, value, warn], i) => {
      const x = 49 + i * 177;
      this.text(scene, x, 337, label, 13, c.muted);
      const number = this.text(scene, x, 361, value, 30, warn ? c.warning : c.text);
      if (number.width > 163) number.setFontSize(24);
    });
    if (s.day > 1) this.text(scene, 49, 402, LINES.intro.allowance + ' +¥' + CONFIG.money.allowance, 13, c.accent);
    if (isLastDay()) this.text(scene, 403, 402, LINES.intro.lastDay, 13, c.accent);
    this.rule(scene, 49, 426, 905, 426);
    this.text(scene, 49, 448, s.hunger < CONFIG.hunger.faintWarn ? LINES.faintWarn : '8:00 前停好车，别忘了戴头盔。',
      15, s.hunger < CONFIG.hunger.faintWarn ? c.warning : c.muted);
    this.text(scene, 49, 477, 'WASD 移动     F 交互     E 背包', 13, c.muted);
    this.button(scene, 648, 449, 258, 'F', '出发找车', leave);
  },

  result(scene, title, color, rows, continueDay, restart) {
    const c = this.colors;
    this.base(scene, true);
    this.text(scene, 47, 106, title, 38, color, { fontStyle: 'bold' });
    this.text(scene, 49, 160, '第 ' + GameState.day + ' 天结束 / 每一段路，都有记录。', 15, c.muted);
    this.box(scene, 766, 113, 133, 48, isCharged() ? 0x3c5e43 : 0x87563f, 6);
    this.text(scene, 779, 128, '电量 ' + Math.round(GameState.battery) + '%', 17);
    this.box(scene, 43, 204, 874, 247, 0x12352f, 12, 0.82);
    rows.forEach(([label, value], i) => {
      const x = 60 + (i < 6 ? 0 : 447);
      const y = 216 + (i % 6) * 39;
      const warn = (label === '罚款' && GameState.fines.length > 0) ||
        (label === '明早电量' && !isCharged()) ||
        (label === '余额' && GameState.money < 0) ||
        ((label === '停好车时间' || label === '下午') && value.includes('迟到'));
      this.text(scene, x, y + 3, label, 13, c.muted);
      const valueText = this.text(scene, x + 113, y, value, 15, warn ? c.warning : c.text,
        { wordWrap: { width: 279, useAdvancedWrap: true }, lineSpacing: 0 });
      if (valueText.getWrappedText(value).length > 1) valueText.setFontSize(14);
      const wrapped = valueText.getWrappedText(value);
      if (wrapped.length > 2) {
        // 明细可以累积很多条；在表中保留摘要，点击后分页查看完整内容。
        let second = wrapped[1];
        const summary = () => wrapped[0] + '\n' + second + '… 详情';
        while (second.length && valueText.getWrappedText(summary()).length > 2) second = second.slice(0, -1);
        valueText.setText(summary());
        valueText.setInteractive({ useHandCursor: true });
        valueText.on('pointerdown', () => this.details(scene, label, value));
      }
      this.rule(scene, x, y + 34, x + 403, y + 34, 0.32);
    });
    this.button(scene, 49, 465, 179, 'R', '重新开始', restart, false);
    this.button(scene, 603, 465, 303, 'F', '开始第 ' + (GameState.day + 1) + ' 天', continueDay);
  },

  details(scene, label, value) {
    if (scene._dailyDetails || scene._leaving) return;
    scene._dailyDetails = true;
    UI.busy = true;
    const objects = [];
    const add = obj => { obj.setDepth(2000); objects.push(obj); return obj; };
    add(scene.add.rectangle(480, 270, 960, 540, 0x061f1b, 0.9).setInteractive());
    add(this.box(scene, 120, 66, 720, 408, 0x23483e, 18, 1, 0x829777));
    add(this.text(scene, 152, 94, label + ' · 完整明细', 24));
    const body = add(this.text(scene, 152, 146, '', 18, this.colors.text,
      { wordWrap: { width: 650, useAdvancedWrap: true }, lineSpacing: 5 }));
    const lines = body.getWrappedText(value);
    const pages = Math.max(1, Math.ceil(lines.length / 10));
    let page = 0;
    const counter = add(this.text(scene, 152, 427, '', 14, this.colors.muted));
    const render = () => { body.setText(lines.slice(page * 10, (page + 1) * 10).join('\n')); counter.setText((page + 1) + ' / ' + pages + '   ← → 翻页'); };
    const change = delta => { page = Phaser.Math.Clamp(page + delta, 0, pages - 1); render(); };
    const back = add(this.text(scene, 500, 426, '← 上一页', 15, this.colors.accent)).setInteractive({ useHandCursor: true });
    const next = add(this.text(scene, 604, 426, '下一页 →', 15, this.colors.accent)).setInteractive({ useHandCursor: true });
    const closeButton = add(this.text(scene, 734, 426, 'F 关闭', 15, this.colors.accent)).setInteractive({ useHandCursor: true });
    const cleanup = () => scene.input.keyboard.off('keydown', keyboard);
    const close = () => {
      objects.forEach(obj => obj.destroy());
      cleanup();
      scene.events.off('shutdown', cleanup);
      scene._dailyDetails = false;
      UI.busy = false;
      UI.lockUntil = scene.time.now + 300;
    };
    const keyboard = event => {
      if (event.repeat) return;
      if (event.code === 'Escape' || event.code === 'KeyF') close();
      else if (event.code === 'ArrowLeft') change(-1);
      else if (event.code === 'ArrowRight') change(1);
    };
    back.on('pointerdown', () => change(-1));
    next.on('pointerdown', () => change(1));
    closeButton.on('pointerdown', close);
    scene.input.keyboard.on('keydown', keyboard);
    scene.events.once('shutdown', cleanup);
    render();
  }
};
