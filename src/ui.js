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

  // assets.js 里这张图 file 为 true（有真图，不是色块）
  hasArt(key) {
    const a = ASSETS.images[key];
    return !!(a && a.file);
  },

  // 戴着头盔、而且有 <key>_helmet 这张图时，返回戴头盔版本的 key
  withHelmet(key) {
    return GameState.helmetOn && UI.hasArt(key + '_helmet') ? key + '_helmet' : key;
  },

  // 换贴图（自动选头盔版本），按宽度 w 等比缩放（传了 h 就用 h）；和上次一样就跳过
  look(obj, key, w, h) {
    const k = UI.withHelmet(key);
    if (obj._look === k) return obj;
    obj._look = k;
    obj.setTexture(k);
    if (w) obj.setDisplaySize(w, h || w * obj.frame.height / obj.frame.width);
    return obj;
  },

  // 推车走路逐帧（左 / 右各 3 帧，另有头盔版）；d 是 UI.dir 的方向，不动时停在第 2 帧。
  // 没有推车逐帧图时返回 false，场景继续用 pusher 单图
  pushWalk(scene, obj, d) {
    if (!UI.hasArt('push_right_1')) return false;
    for (const side of ['left', 'right']) {
      for (const tail of ['', '_helmet']) {
        const key = 'push_walk_' + side + tail;
        if (scene.anims.exists(key) || (tail && !UI.hasArt('push_' + side + '_1' + tail))) continue;
        scene.anims.create({ key,
          frames: [1, 2, 3, 2].map(n => ({ key: 'push_' + side + '_' + n + tail })),
          frameRate: CONFIG.findCar.walkFrameRate, repeat: -1   // 和步行同一帧率
        });
      }
    }
    if (d.x) obj._pushSide = d.x < 0 ? 'left' : 'right';
    const side = obj._pushSide || 'right';
    const tail = GameState.helmetOn && scene.anims.exists('push_walk_' + side + '_helmet') ? '_helmet' : '';
    if (d.x || d.y) obj.anims.play('push_walk_' + side + tail, true);
    else { obj.anims.stop(); obj.setTexture('push_' + side + '_2' + tail); }
    return true;
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
    scene._sfxInstances = [];
    scene.events.once('shutdown', () => {
      scene._sfxInstances.forEach(s => {
        if (!s) return;
        if (s.isPlaying) s.stop();
        s.destroy();
      });
      scene._sfxInstances.length = 0;
    });
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

  // 这一帧是否"刚按下 E"（开背包）。用法同 pressedF，每帧调用一次。
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

  // ---------- 文本框底板 ----------
  // 有 ui_controls_panel 图（而且是 WebGL）时返回一个九宫格底板，四角不变形；没有返回 null，调用方继续用纯色背景
  canPanel(scene) {
    return UI.hasArt('ui_controls_panel') && scene.sys.game.renderer.type === Phaser.WEBGL;
  },
  panel(scene, x, y, w, h) {
    if (!UI.canPanel(scene)) return null;
    const P = CONFIG.panel, c = P.corner, s = P.scale;
    // 九宫格按缩小后的尺寸画，再整体放大回去：四角看起来是 corner × scale 像素
    return scene.add.nineslice(x, y, 'ui_controls_panel', null, w / s, h / s, c, c, c, c).setScale(s);
  },
  // 给一段文字垫上底板（跟着文字的位置、原点、滚动、深度、大小），文字改成深色；返回底板或 null
  backText(scene, t) {
    const P = CONFIG.panel, s = P.scale;
    const bg = UI.panel(scene, 0, 0, 10, 10);
    if (!bg) return null;
    t.setBackgroundColor(null).setColor(P.textColor);
    bg.setOrigin(0.5).setScrollFactor(t.scrollFactorX, t.scrollFactorY).setDepth(t.depth - 0.01);
    let lw = -1, lh = -1;
    const sync = () => {
      if (!t.active) return;
      if (t.width !== lw || t.height !== lh) {   // 文字变了就跟着改框的大小
        lw = t.width; lh = t.height;
        bg.setSize((lw + P.padX * 2) / s, (lh + P.padY * 2) / s);
      }
      // 框中心 = 文字中心（文字自己的留白由 padX / padY 决定）
      bg.setPosition(t.x + (0.5 - t.originX) * lw, t.y + (0.5 - t.originY) * lh);
      bg.setVisible(t.visible).setAlpha(t.alpha);
    };
    sync();
    scene.events.on('postupdate', sync);
    t.once('destroy', () => { scene.events.off('postupdate', sync); bg.destroy(); });
    t._panel = bg;
    return bg;
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
    UI.backText(scene, b);   // 有文本框图就垫上米色底板

    if (target) {
      const follow = () => {
        // 按精灵原点计算头顶，兼容脚底为原点的步行人物。
        if (b.active && target.active) b.setPosition(target.x,
          target.y - target.displayHeight * (target.originY ?? 0.5) - 8);
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
      if (UI.backText(scene, scene._hint)) scene._hint.setY(522);   // 有底板：往上挪一点，框底不贴屏幕边
    }
    if (!text) { scene._hint.setVisible(false); return; }
    if (scene._hint.text !== text) scene._hint.setText(text);
    scene._hint.setVisible(true);
  },

  // ---------- 选项弹窗 ----------
  // options：字符串，或 { label, disabled }（disabled 的选项置灰、选不了）
  // 2 个选项横排（A/D 切换），3 个以上竖排（W/S 切换）。F 确认，也可以鼠标点。
  // 打开时时钟暂停；选完调用 onPick(序号)
  // nudge：LINES.nudge 里的分组名，玩家发呆超过 3 秒时底部小字会换成交促文案（直到选出为止）
  choice(scene, question, options, onPick, nudge) {
    UI.busy = true;
    const openedAt = scene.time.now;
    const D = 2000;
    const objs = [];
    let done = false;

    const opts = options.map(o => typeof o === 'string' ? { label: o } : o);
    const n = opts.length;
    const vertical = n > 2;
    const enabled = (i) => !opts[i].disabled;
    let index = opts.findIndex(o => !o.disabled);
    if (index < 0) index = 0;

    // 先算问题文字高度，面板高度随内容变化
    const q = scene.add.text(480, 0, question, UI.style(22, '#ffffff', {
      align: 'center', wordWrap: { width: 560, useAdvancedWrap: true }
    })).setOrigin(0.5, 0).setScrollFactor(0).setDepth(D + 1);
    const BTN_H = 48;
    const btnArea = vertical ? n * BTN_H : BTN_H + 10;
    const panelH = Math.min(520, 40 + q.height + 24 + btnArea + 44);
    const panelTop = 270 - panelH / 2;
    q.setY(panelTop + 24);
    const btnTop = panelTop + 24 + q.height + 24;

    objs.push(scene.add.rectangle(480, 270, 960, 540, 0x000000, 0.55).setScrollFactor(0).setDepth(D));
    // 面板：有文本框图就用米色底板 + 深色字，没有就用深色矩形 + 黄边
    const art = UI.panel(scene, 480, 270, 640, panelH);
    if (art) {
      objs.push(art.setScrollFactor(0).setDepth(D));
      q.setColor(CONFIG.panel.textColor);
    } else {
      objs.push(scene.add.rectangle(480, 270, 640, panelH, 0x1f2937).setStrokeStyle(3, 0xfacc15).setScrollFactor(0).setDepth(D));
    }
    objs.push(q);
    const tipText = (vertical ? 'W / S' : 'A / D') + ' 选择，F 确认（也可以用鼠标点）';
    const tip = scene.add.text(480, panelTop + panelH - 20, tipText,
      UI.style(14, art ? '#8a6a4a' : '#9ca3af'))
      .setOrigin(0.5).setScrollFactor(0).setDepth(D + 1);
    objs.push(tip);

    // 发呆 3 秒就开始催，之后每 4 秒换一句，直到玩家真的选了
    const tipColor = art ? '#8a6a4a' : '#9ca3af';
    let nudgeTimer = null;
    const nudgeTip = () => {
      const pool = LINES.nudge[nudge] || LINES.nudge.generic;
      tip.setText(UI.rand(pool)).setColor('#fca5a5');
      scene.tweens.add({ targets: tip, x: 474, duration: 70, yoyo: true, repeat: 3,
        onComplete: () => tip.setX(480) });
      nudgeTimer = scene.time.delayedCall(4000, nudgeTip);
    };
    if (nudge) nudgeTimer = scene.time.delayedCall(3000, nudgeTip);

    const btns = opts.map((o, i) => {
      const x = vertical ? 480 : 480 + (i - (n - 1) / 2) * 260;
      const y = vertical ? btnTop + i * BTN_H + BTN_H / 2 : btnTop + BTN_H / 2;
      const b = scene.add.text(x, y, o.label, UI.style(20, '#ffffff', {
        backgroundColor: '#374151', padding: { x: 16, y: 7 },
        align: 'center', fixedWidth: vertical ? 520 : 0
      })).setOrigin(0.5).setScrollFactor(0).setDepth(D + 1).setInteractive({ useHandCursor: enabled(i) });
      b.on('pointerover', () => { if (enabled(i)) { index = i; refresh(); } });
      b.on('pointerdown', () => { if (enabled(i)) pick(i); });
      objs.push(b);
      return b;
    });

    // 按钮配色：米色底板上用暖棕色，深色面板上用灰色
    const C = art ? { off: '#e6cfa8', offText: '#4a3421', dis: '#efe2cc', disText: '#b8a488' }
                  : { off: '#374151', offText: '#ffffff', dis: '#27272a', disText: '#6b7280' };
    function refresh() {
      btns.forEach((b, i) => {
        if (!enabled(i)) { b.setBackgroundColor(C.dis); b.setColor(C.disText); return; }
        b.setBackgroundColor(i === index ? '#facc15' : C.off);
        b.setColor(i === index ? '#111111' : C.offText);
      });
    }
    refresh();

    // 切换时跳过置灰的选项
    const move = (step) => {
      for (let k = 1; k <= n; k++) {
        const j = (index + step * k + n * k) % n;
        if (enabled(j)) { index = j; break; }
      }
      refresh();
    };
    const prev = () => move(-1);
    const next = () => move(1);
    const confirm = (e) => {
      if (e && e.repeat) return;
      if (scene.time.now - openedAt < 200) return; // 防止打开弹窗的那次按键直接确认
      if (enabled(index)) pick(index);
    };
    const kb = scene.input.keyboard;
    const keysPrev = vertical ? ['keydown-W', 'keydown-UP'] : ['keydown-A', 'keydown-LEFT'];
    const keysNext = vertical ? ['keydown-S', 'keydown-DOWN'] : ['keydown-D', 'keydown-RIGHT'];
    keysPrev.forEach(k => kb.on(k, prev));
    keysNext.forEach(k => kb.on(k, next));
    kb.on('keydown-F', confirm);

    function pick(i) {
      if (done) return;
      done = true;
      if (nudgeTimer) { nudgeTimer.remove(false); nudgeTimer = null; }
      tip.setText(tipText).setColor(tipColor);   // 催完收回去，别带着半句玩笑进下一屏
      keysPrev.forEach(k => kb.off(k, prev));
      keysNext.forEach(k => kb.off(k, next));
      kb.off('keydown-F', confirm);
      objs.forEach(o => o.destroy());
      UI.busy = false;
      UI.lockUntil = scene.time.now + 250;
      onPick(i);
    }
    // 场景切走时顺手解绑，避免残留监听
    scene.events.once('shutdown', () => { if (!done) { done = true;
      keysPrev.forEach(k => kb.off(k, prev)); keysNext.forEach(k => kb.off(k, next)); kb.off('keydown-F', confirm); } });
  },

  // ---------- 提示弹窗：只有一个"继续" ----------
  alert(scene, text, onClose, nudge) {
    UI.choice(scene, text, ['继续'], () => { if (onClose) onClose(); }, nudge);
  },

  // ---------- 背包 ----------
  // 显示钱、饥饿、物品；可以戴 / 摘头盔。关掉后调用 onClose
  backpack(scene, onClose) {
    const s = GameState, L = LINES.backpack;
    const money = s.money < 0 ? '欠 ¥' + (-s.money) : '¥' + s.money;
    const q = '【' + L.title + '】　钱 ' + money + '　饥饿 ' + Math.round(s.hunger) + '/100' +
      (isHungry() ? '（饿）' : '');
    const opts = [];
    if (s.items.helmet) {
      opts.push({ id: 'helmet', label: '头盔：' + (s.helmetOn ? '已戴上（摘下）' : '没戴（戴上）') });
    }
    opts.push({ id: 'license', label: '牌照：' + (s.items.license ? '已上牌' : '没有'), disabled: true });
    opts.push({ id: 'close', label: L.close });

    UI.choice(scene, q, opts, (i) => {
      if (opts[i].id === 'helmet') {
        s.helmetOn = !s.helmetOn;
        UI.updateHud(scene);
        UI.say(scene, s.helmetOn ? L.helmetOn : L.helmetOff);
        UI.backpack(scene, onClose);   // 切换完继续留在背包里
        return;
      }
      if (onClose) onClose();
    }, 'generic');
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

  // ---------- 左上角 HUD：电量条（+ 血量格）----------
  createHud(scene, showHp) {
    const hud = { showHp };
    const infoY = showHp ? 78 : 48;   // 钱 / 饥饿 / 头盔 那一行
    hud.bg = scene.add.rectangle(12, 12, 250, infoY + 26, 0x000000, 0.55)
      .setOrigin(0).setScrollFactor(0).setDepth(1000);
    hud.g = scene.add.graphics().setScrollFactor(0).setDepth(1001);
    hud.batLabel = scene.add.text(22, 20, '电量', UI.style(16)).setScrollFactor(0).setDepth(1001);
    hud.batText = scene.add.text(206, 20, '', UI.style(16)).setScrollFactor(0).setDepth(1001);
    if (showHp) hud.hpLabel = scene.add.text(22, 50, '血量', UI.style(16)).setScrollFactor(0).setDepth(1001);
    hud.info = scene.add.text(22, infoY, '', UI.style(15)).setScrollFactor(0).setDepth(1001);
    scene._hud = hud;
    UI.updateHud(scene);
    return hud;
  },

  updateHud(scene) {
    const h = scene._hud;
    if (!h) return;
    const s = GameState;
    const g = h.g;
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
    const money = s.money < 0 ? '欠¥' + (-s.money) : '¥' + s.money;
    const info = money + '　饥饿 ' + Math.round(s.hunger) + '　' + (s.helmetOn ? '⛑头盔' : '无头盔');
    if (h.info.text !== info) h.info.setText(info);
    h.info.setColor(s.money < CONFIG.money.lowWarn || isHungry() ? '#fca5a5' : '#e5e7eb');   // 钱快没了 / 饿了变红（预兆）
  },

  // ---------- 音效 ----------
  // 有素材就播放 Boot 载入的音频；没有就用合成音顶替
  sfx(scene, key, config) {
    if (scene.cache.audio.exists(key)) {
      const sound = scene.sound.add(key, config || {});
      scene._sfxInstances.push(sound);
      sound.once('complete', () => {
        const i = scene._sfxInstances.indexOf(sound);
        if (i >= 0) scene._sfxInstances.splice(i, 1);
        sound.destroy();
      });
      sound.play();
      return sound;
    }
    const presets = {
      beep: [1400, 0.06, 'sine'],
      hit:  [140, 0.18, 'square'],
      fall: [80, 0.45, 'sawtooth'],
      park: [880, 0.15, 'triangle'],
      plug: [660, 0.12, 'sine'],
      whistle: [2200, 0.35, 'square'],
      coin: [1200, 0.1, 'triangle'],
      domino: [110, 0.28, 'square'],
      policeVoice: [180, 0.32, 'sawtooth'],
      pay: [220, 0.16, 'square'],
      hunger: [95, 0.5, 'sawtooth']
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
