// ===== 场景3 / 3′ Park：教学楼车棚停车（B 负责）=====
// data.pushing = true 时是推车（没电），速度减半、已迟到。
class Park extends Phaser.Scene {
  constructor() { super('Park'); }

  init(data) {
    this.pushing = !!(data && data.pushing);
  }

  create() {
    UI.setup(this);
    const P = CONFIG.park;
    this.speed = P.rideSpeed * (this.pushing ? P.pushSpeedFactor : 1);

    // ---- 布局：两排车棚，中间是通道 ----
    const W = 1600, H = 540;
    this.physics.world.setBounds(0, 70, W, H - 70);
    this.cameras.main.setBounds(0, 0, W, H);

    this.add.tileSprite(0, 0, W, H, 'road').setOrigin(0);
    this.add.tileSprite(0, 0, W, 70, 'building').setOrigin(0);
    this.add.text(W / 2, 35, '教学楼 · 车棚', UI.style(26, '#fecaca')).setOrigin(0.5);
    // 教学楼门口（左侧入口）
    this.add.text(20, 470, '← 入口', UI.style(18, '#9ca3af'));

    // 车位：上排 y=150，下排 y=400，每排 26 个
    const SLOT_GAP = 44, FIRST_X = 260, PER_ROW = 28;
    const rowsY = [150, 400];
    const all = [];
    rowsY.forEach(y => {
      for (let i = 0; i < PER_ROW; i++) all.push({ x: FIRST_X + i * SLOT_GAP, y });
    });
    // 车棚顶棚示意
    const g = this.add.graphics();
    g.fillStyle(0x000000, 0.25);
    rowsY.forEach(y => g.fillRect(FIRST_X - 30, y - 45, PER_ROW * SLOT_GAP + 16, 90));

    // 随机挑空位（不放在最靠近入口的 6 个里，逼玩家往里找）
    const candidates = all.filter((s, i) => (i % PER_ROW) >= 6);
    const free = Phaser.Utils.Array.Shuffle(candidates.slice()).slice(0, P.freeSlots);

    this.bikes = this.physics.add.staticGroup();
    this.slots = [];
    all.forEach(s => {
      if (free.includes(s)) {
        const slot = this.add.image(s.x, s.y, 'slot');
        this.tweens.add({ targets: slot, alpha: 0.4, duration: 600, yoyo: true, repeat: -1 });
        this.slots.push(slot);
      } else {
        const b = this.bikes.create(s.x + Phaser.Math.Between(-4, 4), s.y, 'bike_other');
        b.setAngle(Phaser.Math.Between(-12, 12));
        b.setTint(Phaser.Display.Color.HSVToRGB(Math.random(), 0.15, 1).color);
        b.refreshBody();
      }
    });

    // ---- 主角 ----
    this.player = this.physics.add.sprite(80, 275, this.pushing ? 'pusher' : 'rider');
    this.player.setCollideWorldBounds(true);
    this.player.body.setSize(22, 22);   // 碰撞框小一点，方便钻进车位
    this.player.setAngle(90);           // 面朝右（往车棚里走）
    this.physics.add.collider(this.player, this.bikes);
    this.cameras.main.startFollow(this.player, true, 0.15, 0);
    this.done = false;

    // ---- 界面 ----
    UI.createClock(this);
    UI.createHud(this, false);
    if (this.pushing) {
      this.add.text(12, 64, '已迟到', UI.style(20, '#ffffff', {
        backgroundColor: '#dc2626', padding: { x: 10, y: 4 }
      })).setScrollFactor(0).setDepth(1000);
      UI.say(this, LINES.park.pushing, this.player);
    } else {
      UI.say(this, LINES.park.riding, this.player);
    }
    this.lastFull = 0;
  }

  update(time, delta) {
    UI.tickClock(this, delta);
    const f = UI.pressedF(this);
    if (UI.blocked(this) || this.done) { this.player.setVelocity(0); return; }

    // ---- 移动 ----
    const d = UI.dir(this);
    const v = new Phaser.Math.Vector2(d.x, d.y).normalize().scale(this.speed);
    this.player.setVelocity(v.x, v.y);
    if (d.x || d.y) this.player.setAngle(Phaser.Math.RadToDeg(Math.atan2(d.y, d.x)) + 90);

    // ---- 是否在空车位上 ----
    const slot = this.slots.find(s => Phaser.Math.Distance.BetweenPoints(this.player, s) < 30);
    if (slot) {
      UI.hint(this, '按 F 停车');
      if (f) this.parkAt(slot);
      return;
    }

    // ---- 靠近别人的车：按 F 吐槽 ----
    const near = this.bikes.getChildren().some(b => Phaser.Math.Distance.BetweenPoints(this.player, b) < 50);
    UI.hint(this, near ? '按 F 查看' : null);
    if (near && f) UI.say(this, LINES.park.full, this.player);
  }

  parkAt(slot) {
    this.done = true;
    UI.hint(this, null);
    GameState.arriveClock = GameState.clock;
    if (GameState.clock > CONFIG.classStart) GameState.late = true;

    // 把车停进车位
    this.player.setVelocity(0);
    this.player.setTexture('bike').setAngle(0);
    this.player.setPosition(slot.x, slot.y);
    slot.destroy();
    UI.sfx(this, 'park');
    UI.say(this, LINES.park.parked, this.player);
    this.time.delayedCall(1200, () => UI.fadeTo(this, 'Class'));
  }
}
