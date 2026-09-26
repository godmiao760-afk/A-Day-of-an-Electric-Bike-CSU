// ===== 公用工具（A 负责，所有场景调用）=====
// 时钟、独白气泡、提示、二选一弹窗、切场景、HUD、音效都在这里，场景里不要各自重写。

const FONT = '"Microsoft YaHei", "PingFang SC", "Noto Sans SC", sans-serif';

const UI = {
  busy: false,     // 弹窗打开时为 true
  lockUntil: 0,    // 弹窗关闭后短时间内屏蔽 F，防止一次按键触发两次

  // 文字样式
  style(size, color, extra) {
    return Object.assign(
      { fontFamily: FONT, fontSize: size + 'px', color: color || '#ffffff', resolution: 2 },
      extra || {}
    );
  },

  // 数组随机取一个；字符串原样返回
  rand(x) {
    return Array.isArray(x) ? Phaser.Utils.Array.GetRandom(x) : x;
  },

  // 455 → "07:35"
  fmt(clock) {
    const m = Math.floor(clock);
    const h = Math.floor(m / 60) % 24;
    const mm = m % 60;
    return String(h).padStart(2, '0') + ':' + String(mm).padStart(2, '0');
  },

  // 每个场景 create() 第一行调用：重置弹窗状态、注册按键、淡入
  setup(scene) {
    UI.busy = false;
    UI.lockUntil = scene.time.now + 300;   // 刚进场景 0.3 秒内不响应 F，防止上个场景按住的 F 连带触发
    GameState.clockPaused = false;
    scene._leaving = false;
    scene._bubble = null;
    scene._hint = null;
    scene._clock = null;
    scene._hud = null;
    scene.keys = scene.input.keyboard.addKeys('W,A,S,D,F,E,R,UP,DOWN,LEFT,RIGHT');
    scene.cameras.main.fadeIn(300, 0, 0, 0);
  },

  // 场景 update() 开头：if (UI.blocked(this)) return;
  blocked(scene) {
    return UI.busy || scene._leaving;
  },

  // WASD / 方向键 → {x, y}，各为 -1 / 0 / 1
  dir(scene) {
    const k = scene.keys;
    let x = 0, y = 0;
    if (k.A.isDown || k.LEFT.isDown) x -= 1;
    if (k.D.isDown || k.RIGHT.isDown) x += 1;
    if (k.W.isDown || k.UP.isDown) y -= 1;
    if (k.S.isDown || k.DOWN.isDown) y += 1;
    return { x, y };
  },

  // 这一帧是否"刚按下 F"。
  // 注意：每帧在 update 开头调用一次，存进变量再用：const f = UI.pressedF(this);
  // 不要写在 if 条件的后半截，否则之前按过的 F 会"留着"，走到物体旁边时突然触发。
  pressedF(scene) {
    const down = Phaser.Input.Keyboard.JustDown(scene.keys.F);
    return down && !UI.busy && !scene._leaving && scene.time.now >= UI.lockUntil;
  },

  // 这一帧是否"刚按下 E"（打开背包），用法同 pressedF
  pressedE(scene) {
    const down = Phaser.Input.Keyboard.JustDown(scene.keys.E);
    return down && !UI.busy && !scene._leaving && scene.time.now >= UI.lockUntil;
  },

  // ---------- 时钟 ----------
  createClock(scene) {
    scene._clock = scene.add.text(948, 12, UI.fmt(GameState.clock), UI.style(26, '#ffffff', {
      backgroundColor: 'rgba(0,0,0,0.6)', padding: { x: 10, y: 4 }
    })).setOrigin(1, 0).setScrollFactor(0).setDepth(1000);
    return scene._clock;
  },

  // 在 update(time, delta) 里每帧调用
  tickClock(scene, delta) {
    if (!UI.busy && !GameState.clockPaused && !scene._leaving) {
      GameState.clock += delta / 1000 * CONFIG.timeScale / 60;
    }
    if (scene._clock) {
      const c = GameState.clock;
      scene._clock.setText(UI.fmt(c));
      // 快到上课 / 快到门禁时变红
      const warn = (c >= CONFIG.classStart - 5 && c < 12 * 60) || c >= CONFIG.curfew - 5;
      scene._clock.setColor(warn ? '#f87171' : '#ffffff');
    }
  },

  // ---------- 独白气泡 ----------
  // target 传精灵时跟在它头顶；不传则显示在屏幕下方。text 可以是数组（随机一句）。
  say(scene, text, target) {
    text = UI.rand(text);
    if (scene._bubble && scene._bubble.active) scene._bubble.destroy();
    const b = scene.add.text(0, 0, text, UI.style(18, '#111111', {
      backgroundColor: '#ffffff', padding: { x: 10, y: 6 },
      wordWrap: { width: 360, useAdvancedWrap: true }
    })).setOrigin(0.5, 1).setDepth(1100);

    if (target) {
      const follow = () => {
        if (b.active && target.active) b.setPosition(target.x, target.y - target.displayHeight / 2 - 8);
      };
      follow();
      scene.events.on('postupdate', follow);
      b.once('destroy', () => scene.events.off('postupdate', follow));
    } else {
      b.setScrollFactor(0).setPosition(480, 470);
    }

    scene._bubble = b;
    scene.time.delayedCall(2200, () => {
      if (b.active) b.destroy();
      if (scene._bubble === b) scene._bubble = null;
    });
    return b;
  },

  // ---------- 底部操作提示 ----------
  hint(scene, text) {
    if (!scene._hint) {
      scene._hint = scene.add.text(480, 526, '', UI.style(18, '#fde68a', {
        backgroundColor: 'rgba(0,0,0,0.65)', padding: { x: 12, y: 5 }
      })).setOrigin(0.5, 1).setScrollFactor(0).setDepth(1000);
    }
    if (!text) { scene._hint.setVisible(false); return; }
    if (scene._hint.text !== text) scene._hint.setText(text);
    scene._hint.setVisible(true);
  },

  // ---------- 选项弹窗 ----------
  // options 里每项可以是字符串，也可以是 { label, disabled }（置灰、不能选）。
  // 2 个选项横排（A/D 切换），3 个及以上竖排（W/S 切换），F 确认，也可以鼠标点。
  // 打开时时钟暂停；选完调用 onPick(序号)
  choice(scene, question, options, onPick) {
    UI.busy = true;
    const openedAt = scene.time.now;
    const D = 2000;
    const objs = [];
    const opts = options.map(o => typeof o === 'string' ? { label: o } : o);
    const n = opts.length;
    const vertical = n > 2;
    let index = opts.findIndex(o => !o.disabled);
    if (index < 0) index = 0;
    let done = false;

    // 面板高度按内容算
    const qText = scene.add.text(480, 0, question, UI.style(21, '#ffffff', {
      align: 'center', wordWrap: { width: 540, useAdvancedWrap: true }
    })).setOrigin(0.5, 0).setScrollFactor(0).setDepth(D + 1);
    const btnH = 50;
    const listH = vertical ? n * btnH : btnH;
    const panelH = qText.height + listH + 90;
    const top = 270 - panelH / 2;
    qText.setY(top + 24);

    objs.push(scene.add.rectangle(480, 270, 960, 540, 0x000000, 0.55).setScrollFactor(0).setDepth(D));
    objs.push(scene.add.rectangle(480, 270, 620, panelH, 0x1f2937).setStrokeStyle(3, 0xfacc15)
      .setScrollFactor(0).setDepth(D));
    objs.push(qText);
    objs.push(scene.add.text(480, top + panelH - 18,
      (vertical ? 'W / S' : 'A / D') + ' 选择，F 确认（也可以用鼠标点）', UI.style(14, '#9ca3af'))
      .setOrigin(0.5).setScrollFactor(0).setDepth(D + 1));

    const listTop = top + 24 + qText.height + 20;
    const btns = opts.map((o, i) => {
      const x = vertical ? 480 : 480 + (i - (n - 1) / 2) * 260;
      const y = vertical ? listTop + i * btnH + btnH / 2 : listTop + btnH / 2;
      const b = scene.add.text(x, y, o.label, UI.style(20, '#ffffff', {
        backgroundColor: '#374151', padding: { x: 18, y: 7 }, fixedWidth: vertical ? 440 : 0,
        align: 'center'
      })).setOrigin(0.5).setScrollFactor(0).setDepth(D + 1);
      if (!o.disabled) {
        b.setInteractive({ useHandCursor: true });
        b.on('pointerover', () => { index = i; refresh(); });
        b.on('pointerdown', () => pick(i));
      }
      objs.push(b);
      return b;
    });

    function refresh() {
      btns.forEach((b, i) => {
        const dis = opts[i].disabled;
        b.setBackgroundColor(i === index && !dis ? '#facc15' : dis ? '#262c36' : '#374151');
        b.setColor(dis ? '#6b7280' : i === index ? '#111111' : '#ffffff');
      });
    }
    refresh();

    // 移动选中项，跳过置灰的
    function move(step) {
      for (let k = 0; k < n; k++) {
        index = (index + step + n) % n;
        if (!opts[index].disabled) break;
      }
      refresh();
    }

    const kb = scene.input.keyboard;
    const prev = () => move(-1);
    const next = () => move(1);
    const prevKeys = vertical ? ['keydown-W', 'keydown-UP'] : ['keydown-A', 'keydown-LEFT'];
    const nextKeys = vertical ? ['keydown-S', 'keydown-DOWN'] : ['keydown-D', 'keydown-RIGHT'];
    const confirm = (e) => {
      if (e && e.repeat) return;
      if (scene.time.now - openedAt < 200) return; // 防止打开弹窗的那次按键直接确认
      pick(index);
    };
    prevKeys.forEach(k => kb.on(k, prev));
    nextKeys.forEach(k => kb.on(k, next));
    kb.on('keydown-F', confirm);

    function pick(i) {
      if (done || opts[i].disabled) return;
      done = true;
      prevKeys.forEach(k => kb.off(k, prev));
      nextKeys.forEach(k => kb.off(k, next));
      kb.off('keydown-F', confirm);
      objs.forEach(o => o.destroy());
      UI.busy = false;
      UI.lockUntil = scene.time.now + 250;
      onPick(i);
    }
  },

  // ---------- 提示框：显示一段话，按 F 继续 ----------
  alert(scene, text, onClose) {
    UI.choice(scene, text, ['继续'], () => { if (onClose) onClose(); });
  },

  // ---------- 背包 ----------
  // 场景 update 里：if (Phaser.Input.Keyboard.JustDown(this.keys.E)) UI.backpack(this);
  // 打开时时钟暂停。onClose 可不传。
  backpack(scene, onClose) {
    if (UI.busy || scene._leaving) return;
    const s = GameState;
    const rows = [];
    if (s.items.helmet) rows.push({
      id: 'helmet',
      label: () => '头盔　' + (s.helmetOn ? '【已戴上】→ 摘下' : '【没戴】→ 戴上')
    });
    if (s.items.license) rows.push({ id: 'license', label: () => '牌照　【已装在车上】' });
    rows.push({ id: 'close', label: () => '关闭背包' });

    const show = () => {
      const status = '钱 ¥' + s.money + '　饥饿 ' + Math.round(s.hunger) + '/100' +
        (isHungry() ? '（饿了，走得慢）' : '');
      UI.choice(scene, LINES.backpack.title + '\n' + status, rows.map(r => r.label()), (i) => {
        const r = rows[i];
        if (r.id === 'helmet') {
          s.helmetOn = !s.helmetOn;
          UI.updateHud(scene);
          UI.say(scene, s.helmetOn ? LINES.backpack.helmetOn : LINES.backpack.helmetOff);
          show();   // 留在背包里
        } else if (r.id === 'license') {
          UI.say(scene, LINES.backpack.license);
          show();
        } else if (onClose) {
          onClose();
        }
      });
    };
    show();
  },

  // ---------- 切场景 ----------
  fadeTo(scene, key, data) {
    if (scene._leaving) return;
    scene._leaving = true;
    UI.busy = false;
    scene.cameras.main.fade(400, 0, 0, 0, true);   // true = 打断还没结束的淡入
    // 用计时器切换，不依赖淡出事件（淡入没结束时淡出事件可能不触发）
    scene.time.delayedCall(420, () => scene.scene.start(key, data));
  },

  // ---------- 左上角 HUD：电量条（+ 血量格）+ 钱 / 饥饿 / 头盔 ----------
  createHud(scene, showHp) {
    const hud = { showHp };
    const hpH = showHp ? 30 : 0;
    hud.bg = scene.add.rectangle(12, 12, 250, 72 + hpH, 0x000000, 0.55)
      .setOrigin(0).setScrollFactor(0).setDepth(1000);
    hud.g = scene.add.graphics().setScrollFactor(0).setDepth(1001);
    hud.batLabel = scene.add.text(22, 20, '电量', UI.style(16)).setScrollFactor(0).setDepth(1001);
    hud.batText = scene.add.text(206, 20, '', UI.style(16)).setScrollFactor(0).setDepth(1001);
    if (showHp) hud.hpLabel = scene.add.text(22, 50, '血量', UI.style(16)).setScrollFactor(0).setDepth(1001);
    hud.info = scene.add.text(22, 50 + hpH, '', UI.style(15)).setScrollFactor(0).setDepth(1001);
    scene._hud = hud;
    UI.updateHud(scene);
    return hud;
  },

  updateHud(scene) {
    const h = scene._hud;
    if (!h) return;
    const g = h.g;
    const s = GameState;
    const b = Phaser.Math.Clamp(s.battery, 0, 100);
    g.clear();
    // 电量条
    g.lineStyle(2, 0xffffff, 1).strokeRect(70, 22, 128, 16);
    g.fillStyle(b > 50 ? 0x22c55e : b > 20 ? 0xfacc15 : 0xef4444, 1).fillRect(72, 24, 124 * b / 100, 12);
    h.batText.setText(Math.ceil(b) + '%');
    // 血量格
    if (h.showHp) {
      for (let i = 0; i < CONFIG.ride.maxHp; i++) {
        const x = 70 + i * 28;
        if (i < s.hp) g.fillStyle(0xef4444, 1).fillRect(x, 52, 20, 18);
        g.lineStyle(2, 0xffffff, 1).strokeRect(x, 52, 20, 18);
      }
    }
    // 钱 / 饥饿 / 头盔
    const info = (s.money < 0 ? '欠 ¥' + (-s.money) : '¥' + s.money) +
      '　饥饿 ' + Math.round(s.hunger) + (isHungry() ? '(饿)' : '') +
      '　' + (s.helmetOn ? '⛑头盔' : '无头盔');
    if (h.info.text !== info) h.info.setText(info);
    h.info.setColor(s.money < 0 || isHungry() ? '#fca5a5' : '#e5e7eb');
  },

  // ---------- 音效 ----------
  // 有素材就播放 assets/sfx/<key>.mp3；没有就用合成音顶替
  sfx(scene, key) {
    if (scene.cache.audio.exists(key)) { scene.sound.play(key); return; }
    const presets = {
      beep: [1400, 0.06, 'sine'],
      hit:  [140, 0.18, 'square'],
      fall: [80, 0.45, 'sawtooth'],
      park: [880, 0.15, 'triangle'],
      plug: [660, 0.12, 'sine'],
      whistle: [2200, 0.35, 'square'],
      coin: [1200, 0.1, 'triangle']
    };
    const p = presets[key];
    if (p) UI.tone(scene, p[0], p[1], p[2]);
  },

  tone(scene, freq, dur, type) {
    try {
      const ctx = scene.sound.context;
      if (!ctx) return;
      const o = ctx.createOscillator();
      const v = ctx.createGain();
      o.type = type || 'sine';
      o.frequency.value = freq;
      v.gain.setValueAtTime(0.12, ctx.currentTime);
      v.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + dur);
      o.connect(v); v.connect(ctx.destination);
      o.start(); o.stop(ctx.currentTime + dur);
    } catch (e) { /* 没有声音也不影响游戏 */ }
  }
};
