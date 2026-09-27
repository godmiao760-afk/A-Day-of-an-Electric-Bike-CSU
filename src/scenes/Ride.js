// ===== 场景2 Ride：骑车去教学楼（A 负责）=====
// 唯一的动作场景：血量 + 电量。规则见 CLAUDE.md 第 8 节。
// W 前进，S 刹车，A/D 换道。被撞扣血 → 血为 0 摔倒 → 连按 F 扶车（回满血、掉电）。
// 两条路线（GameState.route）：校内远、有坡、没交警；校外近、车多、可能有交警检查点。
// 载人（GameState.passenger）时更慢更耗电，到了拿报酬；交警检查点二选一：停车受检（被罚同学会跑掉）/ 硬闯。
// 车和车不开物理碰撞，按车道规则让行（trafficStep）；早高峰可能有一段单行道，逆行车变多。
// 没电 → 推车进 Park（迟到）；骑到顶部教学楼 → Park。
class Ride extends Phaser.Scene {
  constructor() { super('Ride'); }

  // NodeScene 传进来今天这条路堵不堵（单行道）；DEBUG 直接进来时 data 可能是 {}
  init(data) { this.oneWay = !!(data && data.oneWay); }

  create() {
    UI.setup(this);
    const R = CONFIG.ride;
    const s = GameState;
    this.route = R.routes[s.route] || R.routes.inside;
    s.hp = R.maxHp;

    // ---- 地图尺寸 ----
    const len = this.route.length;
    this.ROAD_L = 280;
    this.ROAD_R = 680;
    this.LANES = [330, 430, 530, 630];
    this.goalY = 300;                       // 到达线
    this.startY = this.goalY + len;         // 起点
    const H = this.startY + 300;
    // 坡道（校外没有坡）
    if (this.route.slope) {
      this.slopeTopY = this.startY - len * this.route.slope[1];
      this.slopeBotY = this.startY - len * this.route.slope[0];
    } else {
      this.slopeTopY = this.slopeBotY = -1;
    }
    // 早高峰单行道路段（和坡道一样按路程比例算 y 区间）
    if (this.oneWay) {
      this.oneWayTopY = this.startY - len * R.oneWay.range[1];
      this.oneWayBotY = this.startY - len * R.oneWay.range[0];
    } else {
      this.oneWayTopY = this.oneWayBotY = -1;
    }
    // 交警检查点（只有校外路线、而且今天有交警）：每次单独掷一次是否真的碰上，第一天新手教学必碰上
    const rideEncounter = s.day === 1 || Math.random() < CONFIG.police.encounterChance;
    this.policeY = (this.route.policeAt && s.policeToday && rideEncounter) ? this.startY - len * this.route.policeAt : null;
    this.policeDone = false;

    this.physics.world.setBounds(this.ROAD_L, 0, this.ROAD_R - this.ROAD_L, H);
    this.cameras.main.setBounds(0, 0, 960, H);

    // ---- 画地图 ----
    // 有道路真图：路 + 两边景观是一张竖向可重复的图，只做一屏大小，跟着镜头滚动纹理；校内在 landmarkAt 处插一张体育场
    // 没图：草地 / 街道 + 灰色路面色块（避免生成超长贴图）
    this.roadArt = UI.hasArt('road_tile');
    this.bgRoad = null;
    if (this.roadArt) {
      const A = R.roadArt;
      this.bgGrass = this.add.tileSprite(0, 0, 960, 540, 'road_tile').setOrigin(0).setScrollFactor(0)
        .setTileScale(A.scale);
      this.bgGrass.tilePositionX = A.centerX - 480 / A.scale;   // 图里路中线对准屏幕中间
      if (this.route.landmarkAt && UI.hasArt('road_stadium')) {
        const L = R.landmark;
        const img = this.add.image(0, this.startY - len * this.route.landmarkAt, 'road_stadium').setScale(L.scale);
        img.setX(480 + (img.width / 2 - L.centerX) * L.scale);   // 同样让图里路中线对准屏幕中间
      }
    } else {
      const sideTex = s.route === 'outside' ? 'road' : 'grass';   // 校外两边是街道
      this.bgGrass = this.add.tileSprite(0, 0, 960, 540, sideTex).setOrigin(0).setScrollFactor(0);
      if (s.route === 'outside') this.bgGrass.setTint(0x9ca3af);
      this.bgRoad = this.add.tileSprite(this.ROAD_L, 0, this.ROAD_R - this.ROAD_L, 540, 'road')
        .setOrigin(0).setScrollFactor(0);
    }
    if (this.route.slope) {
      this.add.tileSprite(this.ROAD_L, this.slopeTopY, this.ROAD_R - this.ROAD_L,
        this.slopeBotY - this.slopeTopY, 'slope').setOrigin(0).setAlpha(this.roadArt ? 0.35 : 0.85);   // 有路图就淡一点，别把路盖住
      this.add.text(this.ROAD_R + 20, this.slopeBotY - 40, '⬆ 大坡\n耗电翻倍', UI.style(22, '#fde68a'));
      this.add.text(this.ROAD_L - 20, this.slopeTopY + 20, '坡顶', UI.style(20, '#fde68a')).setOrigin(1, 0);
    }
    if (this.oneWay) {
      // 单行道路段：路面盖一层淡红色，路边立牌子
      this.add.rectangle(this.ROAD_L, this.oneWayTopY, this.ROAD_R - this.ROAD_L,
        this.oneWayBotY - this.oneWayTopY, 0xef4444, 0.12).setOrigin(0);
      this.add.text(this.ROAD_L - 20, this.oneWayBotY - 60, LINES.ride.oneWaySign,
        UI.style(20, '#fca5a5', { align: 'right' })).setOrigin(1, 0);
    }

    // 车道虚线 + 路边线（路图里自带标线，有图就不画）
    const g = this.add.graphics();
    if (!this.roadArt) {
      g.fillStyle(0xffffff, 0.35);
      for (let i = 1; i < this.LANES.length; i++) {
        const x = this.ROAD_L + i * 100 - 2;
        for (let y = 0; y < H; y += 80) g.fillRect(x, y, 4, 40);
      }
      g.fillStyle(0xfacc15, 0.8).fillRect(this.ROAD_L, 0, 4, H).fillRect(this.ROAD_R - 4, 0, 4, H);
    }

    // 终点：教学楼
    this.add.tileSprite(0, 0, 960, this.goalY - 60, 'building').setOrigin(0);
    this.add.text(480, (this.goalY - 60) / 2, '教 学 楼', UI.style(40, '#fecaca')).setOrigin(0.5);
    g.fillStyle(0xffffff, 0.9);
    for (let x = this.ROAD_L; x < this.ROAD_R; x += 40) g.fillRect(x, this.goalY, 20, 10);
    // 起点
    this.add.text(480, this.startY + 120, s.route === 'outside' ? '校门口（校外路线）' : '宿舍（校内路线）',
      UI.style(24, '#fecaca')).setOrigin(0.5);

    // 交警检查点
    this.barrier = null;
    if (this.policeY) {
      this.barrier = this.add.image(480, this.policeY, 'barrier').setDepth(5);
      // 路两边各站一个交警：有真图就挥指挥棒（右边的翻过来，棒子都朝路中间），两人错开节奏
      const wave = this.policeAnim();
      [this.ROAD_R - 30, this.ROAD_L + 30].forEach((x, i) => {
        const cop = this.add.sprite(x, this.policeY - 30, 'police').setDepth(6);
        if (!UI.hasArt('police')) return;
        const S = CONFIG.ride.sizes.police;
        cop.setDisplaySize(S.width, S.height).setFlipX(i === 0);
        if (wave) cop.anims.play({ key: 'police_wave', startFrame: i * 3 });
      });
      this.add.text(this.ROAD_R + 20, this.policeY - 20, '交警检查', UI.style(22, '#93c5fd'));
    }

    // ---- 主角 ----
    this.player = this.physics.add.sprite(this.LANES[1], this.startY, 'rider');
    this.setRiderLook();
    this.player.setCollideWorldBounds(true);
    this.player.setDepth(10);
    this.cameras.main.centerOn(480, this.startY - 150);
    this.cameras.main.startFollow(this.player, true, 0, 0.2, 0, 150);  // 主角偏下，多看前方
    this.vy = 0;
    this.fallImg = null;       // 摔倒 / 扶车时代替主角显示的图
    this.createWalkerAnims();

    // ---- 障碍 ----
    this.npcs = this.physics.add.group();
    this.physics.add.overlap(this.player, this.npcs, (p, o) => this.onHit(o));
    this.nextSpawn = this.time.now + 1500;

    // ---- 状态 ----
    this.invUntil = 0;
    this.fallen = false;
    this.getting = false;      // 扶正了、正停着准备骑上去
    this.presses = 0;
    this.ending = false;
    this.wateringBgm = null;
    this.events.once('shutdown', () => this.stopWateringBgm(true));
    this.warnedLow = false;
    this.warnedSlope = false;
    this.warnedPolice = false;
    this.warnedOneWay = false;

    // ---- 界面 ----
    UI.createClock(this);
    UI.createHud(this, true);
    this.distText = this.add.text(948, 56, '', UI.style(16, '#ffffff', {
      backgroundColor: 'rgba(0,0,0,0.6)', padding: { x: 8, y: 3 }
    })).setOrigin(1, 0).setScrollFactor(0).setDepth(1000);
    UI.hint(this, 'W 前进　S 刹车　A / D 换道');
    this.time.delayedCall(3000, () => { if (!this.fallen) UI.hint(this, null); });
    UI.say(this, s.route === 'outside' ? LINES.ride.startOutside : LINES.ride.startInside, this.player);
  }

  update(time, delta) {
    // 背景纹理跟随镜头
    const sy = this.cameras.main.scrollY;
    if (this.bgRoad) this.bgRoad.tilePositionY = sy;
    this.bgGrass.tilePositionY = sy / this.bgGrass.tileScaleY;   // 缩放过的纹理按纹理像素滚
    UI.tickClock(this, delta);
    UI.updateHud(this);
    const f = UI.pressedF(this);
    if (UI.pressedE(this)) UI.say(this, LINES.backpack.noRide, this.player);
    this.trafficStep(delta);   // 车道让行规则：弹窗、摔倒时障碍照样在动，所以放在最前面每帧都跑
    if (UI.blocked(this) || this.ending) { this.player.setVelocity(0); return; }

    const R = CONFIG.ride;
    const s = GameState;
    const dt = delta / 1000;
    const p = this.player;
    const onSlope = p.y > this.slopeTopY && p.y < this.slopeBotY;

    // ---- 摔倒：连按 F 扶车 ----
    if (this.fallen || this.getting) {
      p.setVelocity(0);
      if (f && this.fallen) {
        this.presses++;
        const shake = this.fallImg || p;
        this.tweens.add({ targets: shake, x: shake.x + Phaser.Math.Between(-4, 4), duration: 50, yoyo: true });
        this.liftFrame(this.presses);
        UI.hint(this, '连按 F 扶车（' + this.presses + '/' + R.pickupPresses + '）');
        if (this.presses >= R.pickupPresses) this.getUp();
      }
      this.cleanupNpcs();
      return;
    }

    // ---- 移动（坡道、载人、饥饿都会变慢）----
    const mul = (onSlope ? R.slopeSpeedFactor : 1) *
      (s.passenger ? CONFIG.passenger.speedFactor : 1) * speedMul();
    const d = UI.dir(this);
    const top = R.speed * mul;
    const target = d.y < 0 ? -top : 0;
    const rate = d.y > 0 ? 0.25 : (d.y < 0 ? 0.06 : 0.03);   // 刹车快，松手慢慢停（按 60fps 标定）
    const k = 1 - Math.pow(1 - rate, delta / 16.67);          // 换算成和帧率无关的系数，144Hz 和 60Hz 手感一致
    this.vy = Phaser.Math.Linear(this.vy, target, k);
    if (Math.abs(this.vy) < 2) this.vy = 0;
    p.setVelocity(d.x * R.sideSpeed * speedMul(), this.vy);
    p.setAngle(d.x * 8);

    // ---- 耗电：只在移动时掉，坡道、载人掉得快 ----
    const moving = (this.vy < -5 || d.x !== 0) ? 1 : 0;
    s.battery -= moving * (onSlope ? R.drainSlope : R.drainFlat) *
      (s.passenger ? CONFIG.passenger.drainFactor : 1) * dt;

    // ---- 独白提示 ----
    if (onSlope && !this.warnedSlope) { this.warnedSlope = true; UI.say(this, LINES.ride.slope, p); }
    if (this.inOneWay(p.y) && !this.warnedOneWay) { this.warnedOneWay = true; UI.say(this, LINES.ride.oneWayEnter, p); }
    if (s.battery < 15 && !this.warnedLow) { this.warnedLow = true; UI.say(this, LINES.ride.lowBattery, p); }
    if (this.policeY && !this.warnedPolice && p.y - this.policeY < 700) {
      this.warnedPolice = true;
      UI.say(this, LINES.ride.policeAhead, p);
    }

    // ---- 剩余距离 ----
    this.distText.setText('距教学楼 ' + Math.max(0, Math.round((p.y - this.goalY) / 10)) + ' m');

    // ---- 结束判定 ----
    if (s.battery <= 0) { this.batteryDead(); return; }
    if (this.policeY && !this.policeDone && p.y <= this.policeY + 50) { this.police(); return; }
    if (p.y <= this.goalY) { this.arrive(); return; }

    // ---- 生成 / 清理障碍 ----
    if (time > this.nextSpawn) {
      this.spawn();
      this.nextSpawn = time + this.route.spawnEvery * Phaser.Math.FloatBetween(0.6, 1.4);
    }
    this.cleanupNpcs();
  }

  // ---------- 交警检查点 ----------
  police() {
    this.policeDone = true;
    this.vy = 0;
    this.player.setVelocity(0);
    UI.sfx(this, 'whistle');
    UI.sfx(this, 'policeVoice');
    // 检查点附近的障碍清掉，免得弹窗关掉后立刻被撞
    this.npcs.getChildren().slice().forEach(o => {
      if (Math.abs(o.y - this.player.y) < 500) o.destroy();
    });

    // v2：先二选一，停车受检 / 硬闯
    const L = LINES.police;
    UI.choice(this, L.askStop, [L.optStop, L.optRun], i => {
      if (i === 0) this.policeStop(); else this.policeRun();
    });
  }

  // 停车接受检查：和 v1 一样，没头盔 / 没牌照 / 载人各罚一笔，被罚耽误时间
  policeStop() {
    const s = GameState;
    const r = policeCheck(s.passenger);
    if (r.fines.length) UI.sfx(this, 'pay');
    UI.updateHud(this);
    UI.alert(this, LINES.police.stop + '\n\n' + policeText(r), () => {
      // 罚款可能把钱扣到 ≤ 0 → 隐藏结局
      const key = hiddenEndingKey();
      if (key) { UI.fadeTo(this, 'Ending', { key }); return; }
      // 被罚了且载着人：同学跑掉，报酬也没了
      if (!r.passed && s.passenger) {
        s.passenger = false;
        this.setRiderLook();
        UI.say(this, LINES.passenger.fled, this.player);
      }
      this.invUntil = this.time.now + 1500;
    });
  }

  // 硬闯：被抓 → 派出所结局；闯过去不罚款、不耽误时间，载的同学也不跑（runs 在 tryRun 里 +1）
  policeRun() {
    if (!tryRun()) { UI.fadeTo(this, 'Ending', { key: 'police' }); return; }
    UI.sfx(this, 'whistle');
    UI.say(this, LINES.police.runOk, this.player);
    // 过一会儿再说预兆（交警记住车了，下次更容易被抓）
    this.time.delayedCall(2400, () => { if (!this.ending) UI.say(this, LINES.police.runOmen, this.player); });
    // 路障本来就不挡玩家，变淡表示冲过去了；给一点保护时间
    if (this.barrier) this.barrier.setAlpha(0.35);
    this.invUntil = this.time.now + CONFIG.ride.runProtectMs;
    this.tweens.add({ targets: this.player, alpha: 0.3, duration: 150, yoyo: true, repeat: 5,
      onComplete: () => this.player.setAlpha(1) });
  }

  // ---------- 贴图 ----------
  // 主角骑车贴图：载人且有 rider_carry 图就用它，否则用 rider（戴头盔自动换版本）；真图按 sizes.rider 缩放
  setRiderLook() {
    const p = this.player;
    const key = GameState.passenger && UI.hasArt('rider_carry') ? 'rider_carry' : 'rider';
    const S = CONFIG.ride.sizes.rider;
    if (UI.hasArt(key)) UI.look(p, key, S.width, S.height);
    else { p._look = null; p.setTexture(GameState.passenger ? 'rider_carry' : 'rider').setScale(1); }
    this.fitBody(p, S.body);
  }

  // 碰撞框 = 显示尺寸 × ratio，换算回纹理像素后居中
  fitBody(o, ratio) {
    const bw = o.displayWidth * ratio[0] / o.scaleX;
    const bh = o.displayHeight * ratio[1] / o.scaleY;
    o.body.setSize(bw, bh).setOffset((o.width - bw) / 2, (o.height - bh) / 2);
  }

  // 障碍有真图就按 sizes 缩放，然后设碰撞框
  sizeNpc(o, type) {
    const S = CONFIG.ride.sizes[type];
    if (S && UI.hasArt(o.texture.key)) o.setDisplaySize(S.width, S.height);
    this.fitBody(o, S ? S.body : [0.8, 0.85]);
  }

  // 行人左右走的动画（男生 / 女生各一套）；缺图就不建，用 npc_walker 色块
  // 交警挥棒动画（低位 3 帧 + 高位 3 帧循环），没有逐帧图返回 false
  policeAnim() {
    if (!UI.hasArt('police_top_1')) return false;
    if (!this.anims.exists('police_wave')) this.anims.create({ key: 'police_wave',
      frames: ['bottom_1', 'bottom_2', 'bottom_3', 'top_1', 'top_2', 'top_3'].map(n => ({ key: 'police_' + n })),
      frameRate: CONFIG.ride.policeFrameRate, repeat: -1
    });
    return true;
  }

  createWalkerAnims() {
    this.walkerKinds = [];
    for (const who of ['boy', 'girl']) {
      if (!UI.hasArt('walker_' + who + '_left_1')) continue;
      this.walkerKinds.push(who);
      for (const side of ['left', 'right']) {
        const key = 'ride_walker_' + who + '_' + side;
        if (this.anims.exists(key)) continue;
        this.anims.create({ key,
          frames: [1, 2, 3, 2].map(n => ({ key: 'walker_' + who + '_' + side + '_' + n })),
          frameRate: CONFIG.ride.walkerFrameRate, repeat: -1
        });
      }
    }
  }

  // ---------- 障碍 ----------
  spawn() {
    const p = this.player;
    if (p.y < this.goalY + 600) return;   // 快到终点就不再生成
    // 检查点前后不生成
    if (this.policeY && !this.policeDone && Math.abs(p.y - this.policeY) < 600) return;
    const cam = this.cameras.main;
    const top = cam.scrollY;
    const bottom = cam.scrollY + 540;
    const lane = Phaser.Utils.Array.GetRandom(this.LANES);
    const type = this.pickType();
    let o;

    if (type === 'delivery') {
      // 外卖车：从后面冲上来
      o = this.addCar(type, 'npc_delivery', lane, bottom + 60, -CONFIG.ride.speed * 1.7);
      if (!o) return;
      // 屏幕底部闪一个"！"，提醒后面有车冲上来
      const warn = this.add.text(o.x, 530, '！', UI.style(30, '#f97316'))
        .setOrigin(0.5, 1).setScrollFactor(0).setDepth(900);
      this.tweens.add({ targets: warn, alpha: 0, duration: 900, onComplete: () => warn.destroy() });
    } else if (type === 'wrong') {
      // 逆行车：平时一半概率就在玩家这条道上，单行道路段概率更高
      // 没有专门的逆行图时，用"别的同学骑车"（rider 图 + 染色，不戴头盔）
      const same = this.inOneWay(p.y) ? CONFIG.ride.oneWay.sameLaneChance : CONFIG.ride.wrongSameLane;
      const key = UI.hasArt('npc_wrong') || !UI.hasArt('rider') ? 'npc_wrong' : 'rider';
      o = this.addCar(type, key, Math.random() < same ? this.nearestLane(p.x) : lane, top - 80, 140);
      if (!o) return;
      o.setFlipY(true);
      if (key === 'rider') o.setTint(Phaser.Utils.Array.GetRandom(CONFIG.ride.wrongTints));
    } else if (type === 'walker') {
      // 行人：突然横穿（横着走，不占车道）；有图就随机男生 / 女生，朝走的方向播动画
      const fromLeft = Math.random() < 0.5;
      const vx = fromLeft ? 110 : -110;
      const who = this.walkerKinds.length ? Phaser.Utils.Array.GetRandom(this.walkerKinds) : null;
      const side = fromLeft ? 'right' : 'left';
      o = this.npcs.create(fromLeft ? this.ROAD_L - 20 : this.ROAD_R + 20,
        p.y - Phaser.Math.Between(300, 380), who ? 'walker_' + who + '_' + side + '_1' : 'npc_walker');
      if (who) o.play('ride_walker_' + who + '_' + side);
      o.setVelocityX(vx);
      o.setData('type', type).setData('lane', null).setData('speed', vx);
    } else if (type === 'car') {
      // 汽车（校外）：体积大，同向慢慢开，挡路；两款小轿车里随机挑一辆有图的
      const cars = ['npc_car', 'npc_car_2'].filter(k => UI.hasArt(k));
      o = this.addCar(type, cars.length ? Phaser.Utils.Array.GetRandom(cars) : 'npc_car', lane, top - 120, -90);
    } else {
      // 校车：又大又慢，挡在前面
      // 大车：校车 / 洒水车各两款，有图的里面随机挑一辆（都没图就用 npc_bus 色块）
      const bigs = ['npc_bus', 'npc_bus_2', 'npc_cart', 'npc_cart_2'].filter(k => UI.hasArt(k));
      const big = bigs.length ? Phaser.Utils.Array.GetRandom(bigs) : 'npc_bus';
      o = this.addCar('bus', big, lane, top - 160, -50);
      if (o && big.startsWith('npc_cart')) this.startWateringBgm();
    }
    if (!o) return;
    this.sizeNpc(o, type);
  }

  // 在车道上放一辆车：出生点 followGap 内同道已有车就换一条空道；四条都有就这次不生成（返回 null）
  addCar(type, key, want, y, vy) {
    // 出生点检查用实际显示高度：有真图按 sizes，没图按占位图
    const S = CONFIG.ride.sizes[type];
    const h = S && UI.hasArt(key) ? S.height : this.textures.getFrame(key).height;
    const lanes = [want].concat(Phaser.Utils.Array.Shuffle(this.LANES.filter(x => x !== want)));
    const x = lanes.find(x => this.laneFree(x, y, h, null));
    if (x === undefined) return null;
    const o = this.npcs.create(x, y, key);
    o.setVelocityY(vy);
    // type：障碍类型；lane：所在（或正要换去）的车道；speed：正常车速，排队 / 停下后恢复用
    o.setData('type', type).setData('lane', x).setData('speed', vy);
    return o;
  }

  // 按路线配置的权重随机选障碍类型；玩家在单行道路段时逆行权重 × wrongMul
  pickType() {
    const w = Object.assign({}, this.route.npc);
    if (w.wrong && this.inOneWay(this.player.y)) w.wrong *= CONFIG.ride.oneWay.wrongMul;
    const total = Object.values(w).reduce((a, b) => a + b, 0);
    let r = Math.random() * total;
    for (const [k, v] of Object.entries(w)) {
      if ((r -= v) < 0) return k;
    }
    return 'walker';
  }

  nearestLane(x) {
    return this.LANES.reduce((a, b) => Math.abs(b - x) < Math.abs(a - x) ? b : a);
  }

  // 这个 y 在不在今天的单行道路段里
  inOneWay(y) {
    return this.oneWay && y > this.oneWayTopY && y < this.oneWayBotY;
  }

  // ---------- 车道交通规则（车和车不开物理碰撞，靠这些规则避免穿模）----------
  // 占着车道 lane 的车：本来在这条道，或正在换进 / 换出这条道
  inLane(o, lane) {
    return o.getData('lane') === lane || this.nearestLane(o.x) === lane;
  }

  // 两车前后之间的空隙（车头到车尾），负数就是已经叠上了
  gapY(y, h, o) {
    return Math.abs(o.y - y) - (h + o.displayHeight) / 2;
  }

  // 车道 lane 在 y 附近（前后 followGap 内）有没有空位；self 是自己，不算
  laneFree(lane, y, h, self) {
    const gap = CONFIG.ride.followGap;
    return !this.npcs.getChildren().some(o => o !== self && o.active && o.getData('lane') !== null &&
      this.inLane(o, lane) && this.gapY(y, h, o) < gap);
  }

  // 前方（按自己行驶方向）followGap 内最近的一辆车，没有返回 null
  // 挡路的车：在自己（要去）的车道上，或者横向和自己叠着（换道途中）
  carAhead(o) {
    const dir = Math.sign(o.getData('speed'));   // -1 往上开，1 往下开（逆行）
    const lane = o.getData('lane');
    let best = null, bestGap = CONFIG.ride.followGap;
    this.npcs.getChildren().forEach(b => {
      if (b === o || !b.active || b.getData('lane') === null) return;
      if (!this.inLane(b, lane) && Math.abs(b.x - o.x) >= (b.displayWidth + o.displayWidth) / 2) return;
      if ((b.y - o.y) * dir <= 0) return;   // 在身后
      const g = this.gapY(o.y, o.displayHeight, b);
      if (g < bestGap) { best = b; bestGap = g; }
    });
    return best;
  }

  // 往左右相邻的空道换，换成功返回 true
  changeLane(o) {
    const i = this.LANES.indexOf(o.getData('lane'));
    const side = Phaser.Utils.Array.Shuffle([i - 1, i + 1])
      .map(j => this.LANES[j])
      .find(x => x !== undefined && this.laneFree(x, o.y, o.displayHeight, o));
    if (side === undefined) return false;
    o.setData('lane', side);   // x 在 trafficStep 里慢慢挪过去
    return true;
  }

  // 每帧：排队、变道、躲让、行人等车
  trafficStep(delta) {
    const shift = CONFIG.ride.laneChangeSpeed * delta / 1000;   // 换道横向速度，够快才不会在换道途中蹭到前车
    this.npcs.getChildren().forEach(o => {
      if (!o.active) return;
      const type = o.getData('type');
      const speed = o.getData('speed');
      if (type === 'walker') { this.walkerStep(o, speed); return; }

      // 正在换道：横着挪向目标车道
      const lane = o.getData('lane');
      const changing = Math.abs(lane - o.x) > 0.5;
      if (changing) o.x = Math.abs(lane - o.x) <= shift ? lane : o.x + Math.sign(lane - o.x) * shift;

      const front = this.carAhead(o);
      if (!front) { o.setVelocityY(speed); return; }   // 前面空了，恢复正常车速
      // 前车的速度夹在 [自己的速度, 0] 之间：同向慢车 → 跟着排队；迎面来车 / 停着的车 → 停下
      const follow = speed < 0 ? Phaser.Math.Clamp(front.body.velocity.y, speed, 0)
                               : Phaser.Math.Clamp(front.body.velocity.y, 0, speed);
      if (changing) {
        // 换道途中前面有车：先跟着，换完再说
        o.setVelocityY(follow);
      } else if (type === 'delivery') {
        // 外卖车：换到旁边空道超车（可能并进玩家的道），换不了就先跟着
        if (!this.changeLane(o)) o.setVelocityY(follow);
      } else if (type === 'wrong') {
        // 逆行车：迎面有车就往旁边空道躲，躲不开就停下
        if (!this.changeLane(o)) o.setVelocityY(0);
      } else {
        // 汽车 / 校车：减速排队
        o.setVelocityY(follow);
      }
    });
  }

  // 行人：再走一步就进某辆车的道、而那辆车在 followGap 内驶近（或正挡着）→ 停一下，车过去再走
  walkerStep(o, speed) {
    const nextX = o.x + Math.sign(speed) * 40;   // 往前看一步
    let wait = false, inPath = false;
    this.npcs.getChildren().forEach(c => {
      if (!c.active || c.getData('lane') === null) return;
      const g = this.gapY(o.y, o.displayHeight, c);
      const coming = c.body.velocity.y * (o.y - c.y) > 0;   // 车正朝行人这一行开过来
      if (!(g < 0 || (coming && g < CONFIG.ride.followGap))) return;
      const reach = (c.displayWidth + o.displayWidth) / 2;
      if (Math.abs(o.x - c.x) < reach) inPath = true;         // 已经站在这辆车的道上：赶紧走完
      else if (Math.abs(nextX - c.x) < reach) wait = true;    // 再走一步就进它的道：先等
    });
    o.setVelocityX(wait && !inPath ? 0 : speed);
  }

  cleanupNpcs() {
    const top = this.cameras.main.scrollY;
    this.npcs.getChildren().slice().forEach(o => {
      if (o.y > top + 900 || o.y < top - 900 || o.x < 150 || o.x > 810) o.destroy();
    });
    if (!this.npcs.getChildren().some(o => String(o.texture.key).startsWith('npc_cart'))) {
      this.stopWateringBgm();
    }
  }

  startWateringBgm() {
    if (this.wateringBgm || !this.cache.audio.exists('watering_bgm')) return;
    this.wateringBgm = this.sound.add('watering_bgm', { loop: true, volume: 0.35 });
    this.wateringBgm.play();
  }

  stopWateringBgm(immediate = false) {
    if (!this.wateringBgm) return;
    const sound = this.wateringBgm;
    this.wateringBgm = null;
    if (immediate) {
      sound.stop();
      sound.destroy();
      return;
    }
    this.tweens.add({ targets: sound, volume: 0, duration: 900,
      onComplete: () => { sound.stop(); sound.destroy(); } });
  }

  // ---------- 被撞 ----------
  onHit(o) {
    if (this.fallen || this.getting || this.ending || UI.busy || o.getData('hit')) return;
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
  // 有图：趴地（fall_hurt）→ 站起来看着车（fall_stand）→ 每按一次 F 换一帧扶车图（lift_1~6）
  // 没图：主角转 90° 躺下（旧表现）
  fall() {
    this.fallen = true;
    this.presses = 0;
    this.vy = 0;
    GameState.hp = 0;
    UI.sfx(this, 'fall');
    this.player.setVelocity(0);
    UI.hint(this, '连按 F 扶车（0/' + CONFIG.ride.pickupPresses + '）');
    if (!UI.hasArt('fall_hurt')) {
      this.tweens.add({ targets: this.player, angle: 90, duration: 200 });
      return;
    }
    const S = CONFIG.ride.sizes.fall;
    this.tweens.killTweensOf(this.player);
    this.player.setAlpha(1).setAngle(0).setVisible(false);
    this.fallImg = this.add.image(this.player.x, this.player.y, UI.withHelmet('fall_hurt'))
      .setDisplaySize(S.width, S.height).setDepth(this.player.depth);
    // 趴一会儿再站起来；这期间按 F 也算数，第一下就直接开始扶
    this.time.delayedCall(CONFIG.ride.fallStandMs, () => {
      if (this.fallImg && this.presses === 0) UI.look(this.fallImg, 'fall_stand', S.width, S.height);
    });
  }

  // 按了第 n 次 F：换到对应的扶车帧（按 pickupPresses 均匀分到 6 帧上，最后一下一定是扶正）
  liftFrame(n) {
    if (!this.fallImg || !UI.hasArt('lift_1')) return;
    const frames = 6;
    const i = Math.max(1, Math.round(n / CONFIG.ride.pickupPresses * frames));
    const S = CONFIG.ride.sizes.lift;
    UI.look(this.fallImg, 'lift_' + Math.min(i, frames), S.width, S.height);
  }

  getUp() {
    const R = CONFIG.ride;
    this.fallen = false;
    GameState.hp = R.maxHp;
    GameState.battery -= R.fallBatteryCost;
    GameState.falls += 1;
    UI.hint(this, null);
    if (this.fallImg) {
      // 扶正的那一帧停一下，再换回骑车的样子
      this.getting = true;
      this.time.delayedCall(R.liftDoneMs, () => {
        this.getting = false;
        if (this.fallImg) { this.fallImg.destroy(); this.fallImg = null; }
        this.player.setVisible(true);
        this.afterGetUp();
      });
      return;
    }
    this.tweens.add({ targets: this.player, angle: 0, duration: 200 });
    this.afterGetUp();
  }

  // 重新骑上车：说一句、短暂保护；电被摔没了就推车
  afterGetUp() {
    UI.say(this, LINES.ride.fall, this.player);
    this.invUntil = this.time.now + 1500;   // 扶起来后给 1.5 秒保护
    this.tweens.add({ targets: this.player, alpha: 0.3, duration: 150, yoyo: true, repeat: 4,
      onComplete: () => this.player.setAlpha(1) });
    if (GameState.battery <= 0) this.batteryDead();
  }

  // ---------- 结束 ----------
  batteryDead() {
    if (this.ending) return;
    const s = GameState;
    this.ending = true;
    s.battery = 0;
    s.late = true;
    s.clock += CONFIG.ride.deadBatteryMinutes;
    UI.hint(this, null);
    if (s.passenger) {
      // 没电了，同学自己走了，钱也没给
      s.passenger = false;
      UI.say(this, LINES.passenger.leaveDead, this.player);
      this.time.delayedCall(1600, () => UI.say(this, LINES.ride.dead, this.player));
      this.time.delayedCall(3200, () => UI.fadeTo(this, 'Park', { pushing: true }));
    } else {
      UI.say(this, LINES.ride.dead, this.player);
      this.time.delayedCall(1500, () => UI.fadeTo(this, 'Park', { pushing: true }));
    }
  }

  arrive() {
    if (this.ending) return;
    const s = GameState;
    this.ending = true;
    UI.hint(this, null);
    this.player.setVelocity(0);
    if (s.passenger) {
      // 安全送到，拿报酬
      s.passenger = false;
      earn(CONFIG.passenger.reward);
      UI.sfx(this, 'coin');
      UI.updateHud(this);
      UI.say(this, LINES.passenger.paid, this.player);
      this.time.delayedCall(1300, () => UI.fadeTo(this, 'Park', { pushing: false }));
    } else {
      UI.fadeTo(this, 'Park', { pushing: false });
    }
  }
}
