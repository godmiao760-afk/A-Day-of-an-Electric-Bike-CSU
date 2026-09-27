// ===== 场景4 Charge：晚上找充电桩（B 负责）=====
// 22:40 → 23:00 门禁。逐个试充电桩：被占 / 坏了 / 扫码失败 / 空闲。
// 插上就回宿舍睡觉：按 gambleWinRate 充满，否则被拔线只充一点；结果不当场揭晓，第二天 Intro 再说。
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
      // 被占的桩前面停着一辆别人的车（有真图就随机一种颜色）
      if (st === 'occupied') {
        if (UI.hasArt('dorm_bike_1')) {
          this.add.image(x, 190, 'dorm_bike_' + Phaser.Math.Between(1, 7))
            .setDisplaySize(C.bike.width, C.bike.height).setDepth(9);
        } else {
          this.add.image(x, 190, 'bike_other').setDepth(9);
        }
      }
      this.add.text(x, 100, String(i + 1), UI.style(14, '#e5e7eb')).setOrigin(0.5).setDepth(11);
    });

    // ---- 主角推车（有真图：侧视，往左走就翻过来）----
    this.player = this.physics.add.sprite(W / 2, 460, 'pusher');
    if (UI.hasArt('pusher')) UI.look(this.player, 'pusher', C.pusher.width, C.pusher.height);
    this.player.setCollideWorldBounds(true);
    const bw = C.pusher.bodyWidth / this.player.scaleX, bh = C.pusher.bodyHeight / this.player.scaleY;
    this.player.body.setSize(bw, bh).setOffset((this.player.width - bw) / 2, (this.player.height - bh) / 2);
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
    if (!this.done) UI.updateHud(this);   // 插上后不再刷新，免得电量条当场露出充没充满
    const f = UI.pressedF(this);
    if (UI.pressedE(this) && !this.done) { this.player.setVelocity(0); UI.backpack(this); }
    if (this.done || UI.blocked(this)) { this.player.setVelocity(0); return; }

    // ---- 门禁到了 ----
    if (GameState.clock >= CONFIG.curfew) { this.curfew(); return; }

    // ---- 移动（饿了更慢）----
    const d = UI.dir(this);
    const v = new Phaser.Math.Vector2(d.x, d.y).normalize().scale(CONFIG.charge.walkSpeed * speedMul());
    this.player.setVelocity(v.x, v.y);
    if (d.x && UI.hasArt('pusher')) this.player.setFlipX(d.x < 0);   // 原图车头朝右

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
    UI.updateHud(this);           // 只刷这一次（显示扣钱），之后 HUD 冻住
    this.player.setVelocity(0);
    this.player.disableBody();   // 插上了不再碰撞
    this.player.setPosition(pile.x, pile.y + 60);
    // 有真图：车停在桩前充电（和被占的桩一样），人不再显示
    if (UI.hasArt('dorm_bike')) {
      const C = CONFIG.charge;
      this.player.setTexture('dorm_bike').setFlipX(false).setDisplaySize(C.bike.width, C.bike.height);
    }
    pile.setTint(0x22c55e);

    // 插上就回宿舍：现在就定结果，但不说出来（第二天 Intro 揭晓）
    const C = CONFIG.charge;
    if (Math.random() < C.gambleWinRate) {
      GameState.battery = 100;
      GameState.chargeResult = 'full';
    } else {
      // 半夜被拔线
      GameState.battery = Math.min(100, GameState.battery + C.unpluggedGain);
      GameState.chargeResult = 'unplugged';
    }
    UI.say(this, LINES.charge.plugged, this.player);
    this.finish();
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
    // 扫码 ¥2 可能正好把钱扣到 ≤ 0 → 隐藏结局，不进结算
    const k = hiddenEndingKey();
    this.time.delayedCall(1800, () => {
      if (k) UI.fadeTo(this, 'Ending', { key: k });
      else UI.fadeTo(this, 'Result');
    });
  }
}
