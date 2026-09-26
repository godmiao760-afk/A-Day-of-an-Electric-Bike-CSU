// ===== 场景2 Ride：骑车去教学楼（A 负责）=====
// 唯一的动作场景：血量 + 电量。规则见 项目说明.md 第 8 节。
// W 前进，S 刹车，A/D 换道。被撞扣血 → 血为 0 摔倒 → 连按 F 扶车（回满血、掉电）。
// 没电 → 推车进 Park（迟到）；骑到顶部教学楼 → Park。
class Ride extends Phaser.Scene {
  constructor() { super('Ride'); }

  create() {
    UI.setup(this);
    const R = CONFIG.ride;
    GameState.hp = R.maxHp;

    // ---- 地图尺寸 ----
    this.ROAD_L = 280;
    this.ROAD_R = 680;
    this.LANES = [330, 430, 530, 630];
    this.goalY = 300;                       // 到达线
    this.startY = this.goalY + R.length;    // 起点
    const H = this.startY + 300;
    this.slopeTopY = this.startY - R.length * R.slopeEnd;
    this.slopeBotY = this.startY - R.length * R.slopeStart;

    this.physics.world.setBounds(this.ROAD_L, 0, this.ROAD_R - this.ROAD_L, H);
    this.cameras.main.setBounds(0, 0, 960, H);

    // ---- 画地图 ----
    // 草地和路面只做一屏大小，跟着镜头滚动纹理（避免生成超长贴图）
    this.bgGrass = this.add.tileSprite(0, 0, 960, 540, 'grass').setOrigin(0).setScrollFactor(0);
    this.bgRoad = this.add.tileSprite(this.ROAD_L, 0, this.ROAD_R - this.ROAD_L, 540, 'road')
      .setOrigin(0).setScrollFactor(0);
    this.add.tileSprite(this.ROAD_L, this.slopeTopY, this.ROAD_R - this.ROAD_L,
      this.slopeBotY - this.slopeTopY, 'slope').setOrigin(0).setAlpha(0.85);
    this.add.text(this.ROAD_R + 20, this.slopeBotY - 40, '⬆ 大坡\n耗电翻倍', UI.style(22, '#fde68a'));
    this.add.text(this.ROAD_L - 20, this.slopeTopY + 20, '坡顶', UI.style(20, '#fde68a')).setOrigin(1, 0);

    // 车道虚线
    const g = this.add.graphics();
    g.fillStyle(0xffffff, 0.35);
    for (let i = 1; i < this.LANES.length; i++) {
      const x = this.ROAD_L + i * 100 - 2;
      for (let y = 0; y < H; y += 80) g.fillRect(x, y, 4, 40);
    }
    // 路边线
    g.fillStyle(0xfacc15, 0.8).fillRect(this.ROAD_L, 0, 4, H).fillRect(this.ROAD_R - 4, 0, 4, H);

    // 终点：教学楼
    this.add.tileSprite(0, 0, 960, this.goalY - 60, 'building').setOrigin(0);
    this.add.text(480, (this.goalY - 60) / 2, '教 学 楼', UI.style(40, '#fecaca')).setOrigin(0.5);
    g.fillStyle(0xffffff, 0.9);
    for (let x = this.ROAD_L; x < this.ROAD_R; x += 40) g.fillRect(x, this.goalY, 20, 10);
    // 起点：宿舍
    this.add.text(480, this.startY + 120, '宿舍', UI.style(26, '#fecaca')).setOrigin(0.5);

    // ---- 主角 ----
    this.player = this.physics.add.sprite(this.LANES[1], this.startY, 'rider');
    this.player.setCollideWorldBounds(true);
    this.player.body.setSize(24, 48);
    this.player.setDepth(10);
    this.cameras.main.centerOn(480, this.startY - 150);
    this.cameras.main.startFollow(this.player, true, 0, 0.2, 0, 150);  // 主角偏下，多看前方
    this.vy = 0;

    // ---- 障碍 ----
    this.npcs = this.physics.add.group();
    this.physics.add.overlap(this.player, this.npcs, (p, o) => this.onHit(o));
    this.nextSpawn = this.time.now + 1500;

    // ---- 状态 ----
    this.invUntil = 0;
    this.fallen = false;
    this.presses = 0;
    this.ending = false;
    this.warnedLow = false;
    this.warnedSlope = false;

    // ---- 界面 ----
    UI.createClock(this);
    UI.createHud(this, true);
    this.distText = this.add.text(948, 56, '', UI.style(16, '#ffffff', {
      backgroundColor: 'rgba(0,0,0,0.6)', padding: { x: 8, y: 3 }
    })).setOrigin(1, 0).setScrollFactor(0).setDepth(1000);
    UI.hint(this, 'W 前进　S 刹车　A / D 换道');
    this.time.delayedCall(3000, () => { if (!this.fallen) UI.hint(this, null); });
    UI.say(this, LINES.ride.start, this.player);
  }

  update(time, delta) {
    // 背景纹理跟随镜头
    this.bgGrass.tilePositionY = this.bgRoad.tilePositionY = this.cameras.main.scrollY;
    UI.tickClock(this, delta);
    UI.updateHud(this);
    const f = UI.pressedF(this);
    if (UI.blocked(this) || this.ending) { this.player.setVelocity(0); return; }

    const R = CONFIG.ride;
    const dt = delta / 1000;
    const p = this.player;
    const onSlope = p.y > this.slopeTopY && p.y < this.slopeBotY;

    // ---- 摔倒：连按 F 扶车 ----
    if (this.fallen) {
      p.setVelocity(0);
      if (f) {
        this.presses++;
        this.tweens.add({ targets: p, x: p.x + Phaser.Math.Between(-4, 4), duration: 50, yoyo: true });
        UI.hint(this, '连按 F 扶车（' + this.presses + '/' + R.pickupPresses + '）');
        if (this.presses >= R.pickupPresses) this.getUp();
      }
      this.cleanupNpcs();
      return;
    }

    // ---- 移动 ----
    const d = UI.dir(this);
    const top = R.speed * (onSlope ? R.slopeSpeedFactor : 1);
    const target = d.y < 0 ? -top : 0;
    const rate = d.y > 0 ? 0.25 : (d.y < 0 ? 0.06 : 0.03);   // 刹车快，松手慢慢停
    this.vy = Phaser.Math.Linear(this.vy, target, rate);
    if (Math.abs(this.vy) < 2) this.vy = 0;
    p.setVelocity(d.x * R.sideSpeed, this.vy);
    p.setAngle(d.x * 8);

    // ---- 耗电：只在移动时掉，坡道掉得快 ----
    const moving = (this.vy < -5 || d.x !== 0) ? 1 : 0;
    GameState.battery -= moving * (onSlope ? R.drainSlope : R.drainFlat) * dt;

    // ---- 独白提示 ----
    if (onSlope && !this.warnedSlope) { this.warnedSlope = true; UI.say(this, LINES.ride.slope, p); }
    if (GameState.battery < 15 && !this.warnedLow) { this.warnedLow = true; UI.say(this, LINES.ride.lowBattery, p); }

    // ---- 剩余距离 ----
    this.distText.setText('距教学楼 ' + Math.max(0, Math.round((p.y - this.goalY) / 10)) + ' m');

    // ---- 结束判定 ----
    if (GameState.battery <= 0) { this.batteryDead(); return; }
    if (p.y <= this.goalY) { this.arrive(); return; }

    // ---- 生成 / 清理障碍 ----
    if (time > this.nextSpawn) {
      this.spawn();
      this.nextSpawn = time + R.spawnEvery * Phaser.Math.FloatBetween(0.6, 1.4);
    }
    this.cleanupNpcs();
  }

  // ---------- 障碍 ----------
  spawn() {
    const p = this.player;
    if (p.y < this.goalY + 600) return;   // 快到终点就不再生成
    const cam = this.cameras.main;
    const top = cam.scrollY;
    const bottom = cam.scrollY + 540;
    const lane = Phaser.Utils.Array.GetRandom(this.LANES);
    const r = Math.random();
    let o;

    if (r < 0.3) {
      // 外卖车：从后面冲上来
      o = this.npcs.create(lane, bottom + 60, 'npc_delivery');
      o.setVelocityY(-CONFIG.ride.speed * 1.7);
      // 屏幕底部闪一个"！"，提醒后面有车冲上来
      const warn = this.add.text(lane, 530, '！', UI.style(30, '#f97316'))
        .setOrigin(0.5, 1).setScrollFactor(0).setDepth(900);
      this.tweens.add({ targets: warn, alpha: 0, duration: 900, onComplete: () => warn.destroy() });
    } else if (r < 0.6) {
      // 逆行车：一半概率就在玩家这条道上
      const x = Math.random() < 0.5 ? this.nearestLane(p.x) : lane;
      o = this.npcs.create(x, top - 80, 'npc_wrong');
      o.setFlipY(true);
      o.setVelocityY(140);
    } else if (r < 0.85) {
      // 行人：突然横穿
      const fromLeft = Math.random() < 0.5;
      o = this.npcs.create(fromLeft ? this.ROAD_L - 20 : this.ROAD_R + 20,
        p.y - Phaser.Math.Between(300, 380), 'npc_walker');
      o.setVelocityX(fromLeft ? 110 : -110);
    } else {
      // 校车：又大又慢，挡在前面
      o = this.npcs.create(lane, top - 160, 'npc_bus');
      o.setVelocityY(-50);
    }
    o.body.setSize(o.width * 0.8, o.height * 0.85);
  }

  nearestLane(x) {
    return this.LANES.reduce((a, b) => Math.abs(b - x) < Math.abs(a - x) ? b : a);
  }

  cleanupNpcs() {
    const top = this.cameras.main.scrollY;
    this.npcs.getChildren().slice().forEach(o => {
      if (o.y > top + 900 || o.y < top - 900 || o.x < 150 || o.x > 810) o.destroy();
    });
  }

  // ---------- 被撞 ----------
  onHit(o) {
    if (this.fallen || this.ending || o.getData('hit')) return;
    if (this.time.now < this.invUntil) return;
    o.setData('hit', true);   // 同一个障碍只撞一次

    GameState.hp -= 1;
    GameState.hits += 1;
    UI.sfx(this, 'hit');
    this.cameras.main.shake(150, 0.008);
    this.vy = 60;   // 被撞得往后退一下

    if (GameState.hp <= 0) { this.fall(); return; }

    UI.say(this, LINES.ride.hit, this.player);
    this.invUntil = this.time.now + CONFIG.ride.invincibleMs;
    this.tweens.add({ targets: this.player, alpha: 0.2, duration: 100, yoyo: true,
      repeat: Math.floor(CONFIG.ride.invincibleMs / 200) - 1, onComplete: () => this.player.setAlpha(1) });
  }

  // ---------- 摔倒 / 扶车 ----------
  fall() {
    this.fallen = true;
    this.presses = 0;
    this.vy = 0;
    GameState.hp = 0;
    UI.sfx(this, 'fall');
    this.player.setVelocity(0);
    this.tweens.add({ targets: this.player, angle: 90, duration: 200 });
    UI.hint(this, '连按 F 扶车（0/' + CONFIG.ride.pickupPresses + '）');
  }

  getUp() {
    const R = CONFIG.ride;
    this.fallen = false;
    GameState.hp = R.maxHp;
    GameState.battery -= R.fallBatteryCost;
    GameState.falls += 1;
    UI.hint(this, null);
    UI.say(this, LINES.ride.fall, this.player);
    this.tweens.add({ targets: this.player, angle: 0, duration: 200 });
    this.invUntil = this.time.now + 1500;   // 扶起来后给 1.5 秒保护
    this.tweens.add({ targets: this.player, alpha: 0.3, duration: 150, yoyo: true, repeat: 4,
      onComplete: () => this.player.setAlpha(1) });
    if (GameState.battery <= 0) this.batteryDead();
  }

  // ---------- 结束 ----------
  batteryDead() {
    if (this.ending) return;
    this.ending = true;
    GameState.battery = 0;
    GameState.late = true;
    GameState.clock += CONFIG.ride.deadBatteryMinutes;
    UI.hint(this, null);
    UI.say(this, LINES.ride.dead, this.player);
    this.time.delayedCall(1500, () => UI.fadeTo(this, 'Park', { pushing: true }));
  }

  arrive() {
    if (this.ending) return;
    this.ending = true;
    UI.hint(this, null);
    UI.fadeTo(this, 'Park', { pushing: false });
  }
}
