// ===== 场景4 Charge：晚上找充电桩（B 负责）=====
// 22:40 → 23:00 门禁。逐个试充电桩：被占 / 坏了 / 扫码失败 / 空闲。
// 插上后二选一：守着（稳）/ 回宿舍（赌）。
class Charge extends Phaser.Scene {
  constructor() { super('Charge'); }

  create() {
    UI.setup(this);
    const C = CONFIG.charge;
    if (GameState.clock < CONFIG.nightClock) GameState.clock = CONFIG.nightClock;
    this.startBattery = GameState.battery;

    // ---- 布局 ----
    const W = 960, H = 540;
    this.physics.world.setBounds(0, 70, W, H - 70);
    this.add.tileSprite(0, 0, W, H, 'road').setOrigin(0);
    this.add.tileSprite(0, 0, W, 70, 'building').setOrigin(0);
    this.add.text(W / 2, 35, '充电区（23:00 宿舍门禁）', UI.style(24, '#fecaca')).setOrigin(0.5);
    // 夜晚滤镜
    this.add.rectangle(0, 0, W, H, 0x0b1026, 0.35).setOrigin(0).setDepth(500);

    // ---- 充电桩：状态随机分配 ----
    const states = [];
    for (let i = 0; i < C.free; i++) states.push('free');
    for (let i = 0; i < C.qrFail; i++) states.push('qrFail');
    for (let i = 0; i < C.broken; i++) states.push('broken');
    while (states.length < C.piles) states.push('occupied');
    Phaser.Utils.Array.Shuffle(states);

    this.piles = this.physics.add.staticGroup();
    const gap = 96;
    const startX = W / 2 - (C.piles - 1) * gap / 2;
    states.forEach((st, i) => {
      const x = startX + i * gap;
      const p = this.piles.create(x, 130, 'pile');
      p.setData({ state: st, tried: false });
      p.setDepth(10);
      // 被占的桩前面停着一辆别人的车
      if (st === 'occupied') {
        this.add.image(x, 190, 'bike_other').setDepth(9);
      }
      this.add.text(x, 100, String(i + 1), UI.style(14, '#e5e7eb')).setOrigin(0.5).setDepth(11);
    });

    // ---- 主角推车 ----
    this.player = this.physics.add.sprite(W / 2, 460, 'pusher');
    this.player.setCollideWorldBounds(true);
    this.player.body.setSize(30, 40);
    this.player.setDepth(20);
    this.physics.add.collider(this.player, this.piles);
    this.done = false;
    this.broke = false;   // 找到过能用的桩，但钱不够

    // ---- 界面 ----
    UI.createClock(this);
    UI.createHud(this, false);
    UI.say(this, LINES.charge.start, this.player);
  }

  update(time, delta) {
    UI.tickClock(this, delta);
    UI.updateHud(this);
    const f = UI.pressedF(this);
    if (UI.pressedE(this) && !this.done) { this.player.setVelocity(0); UI.backpack(this); }
    if (this.done || UI.blocked(this)) { this.player.setVelocity(0); return; }

    // ---- 门禁到了 ----
    if (GameState.clock >= CONFIG.curfew) { this.curfew(); return; }

    // ---- 移动（饿了更慢）----
    const d = UI.dir(this);
    const v = new Phaser.Math.Vector2(d.x, d.y).normalize().scale(CONFIG.charge.walkSpeed * speedMul());
    this.player.setVelocity(v.x, v.y);

    // ---- 最近的充电桩 ----
    let pile = null, best = 80;
    this.piles.getChildren().forEach(p => {
      const dd = Phaser.Math.Distance.BetweenPoints(this.player, p);
      if (dd < best) { best = dd; pile = p; }
    });
    if (!pile) { UI.hint(this, null); return; }
    UI.hint(this, (pile.getData('state') === 'qrFail' && pile.getData('tried') ? '按 F 重新扫码' : '按 F 扫码充电') +
      '（¥' + CONFIG.money.charge + '）');
    if (f) this.tryPile(pile);
  }

  tryPile(pile) {
    const st = pile.getData('state');
    const firstTry = !pile.getData('tried');
    pile.setData('tried', true);

    if (st === 'occupied') {
      UI.say(this, LINES.charge.occupied, this.player);
      pile.setTint(0x888888);
    } else if (st === 'broken') {
      UI.say(this, LINES.charge.broken, this.player);
      pile.setTint(0x555555);
    } else if (GameState.money < CONFIG.money.charge) {
      // 能扫码的桩，但钱不够
      UI.say(this, LINES.charge.noMoney, this.player);
      this.broke = true;
    } else if (st === 'qrFail') {
      // 第一次必定失败；之后每次按概率成功
      if (!firstTry && Math.random() < CONFIG.charge.qrRetryChance) {
        UI.say(this, LINES.charge.qrOk, this.player);
        this.plugIn(pile);
      } else {
        GameState.clock += 0.5;   // 扫码也要花时间
        UI.say(this, LINES.charge.qrFail, this.player);
        this.tweens.add({ targets: pile, x: pile.x + 3, duration: 40, yoyo: true, repeat: 2 });
      }
    } else {
      this.plugIn(pile);
    }
  }

  plugIn(pile) {
    this.done = true;
    UI.hint(this, null);
    UI.sfx(this, 'plug');
    spend(CONFIG.money.charge);   // 扫码付钱
    UI.updateHud(this);
    this.player.setVelocity(0);
    this.player.setPosition(pile.x, pile.y + 60);
    pile.setTint(0x22c55e);

    UI.choice(this, LINES.charge.question, ['守着它', '先回宿舍'], (i) => {
      const C = CONFIG.charge;
      const remain = Math.max(0, CONFIG.curfew - GameState.clock);
      if (i === 0) {
        // 守着：一直充到门禁，稳
        GameState.battery = Math.min(100, GameState.battery + C.watchPerMinute * remain);
        GameState.clock = CONFIG.curfew;
        GameState.chargeResult = 'watch';
        UI.say(this, LINES.charge.watchDone, this.player);
      } else if (Math.random() < C.gambleWinRate) {
        // 回宿舍：赌赢了
        GameState.battery = 100;
        GameState.chargeResult = 'full';
        UI.say(this, LINES.charge.full);
      } else {
        // 回宿舍：被拔线
        GameState.battery = Math.min(100, GameState.battery + C.unpluggedGain);
        GameState.chargeResult = 'unplugged';
        UI.say(this, LINES.charge.unplugged);
      }
      this.finish();
    });
  }

  curfew() {
    this.done = true;
    UI.hint(this, null);
    GameState.clock = CONFIG.curfew;
    GameState.chargeResult = this.broke ? 'noMoney' : 'none';
    UI.say(this, this.broke ? LINES.charge.noMoney : LINES.charge.curfew, this.player);
    this.finish();
  }

  finish() {
    GameState.chargeGain = Math.round(GameState.battery - this.startBattery);
    UI.updateHud(this);
    this.time.delayedCall(1800, () => UI.fadeTo(this, 'Result'));
  }
}
