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
  // data.dream = true：完美结局彩蛋"小电驴的梦"，路线和规则见 CONFIG.ride.routes.dream
  // data.trip：中午 / 傍晚的短途骑行（'canteen' | 'houhu' | 'back' | 'library'），place / meal / evening 原样转给 Park
  init(data) {
    data = data || {};
    this.dream = !!data.dream;
    this.oneWay = !!data.oneWay && !this.dream;
    this.trip = data.trip || null;
    this.place = data.place || null;
    this.meal = data.meal || null;
    this.evening = !!data.evening;
  }

  create() {
    UI.setup(this);
    const R = CONFIG.ride;
    const s = GameState;
    if (this.dream) GameState.clockPaused = true;   // 梦里没有时间
    this.route = this.dream ? R.routes.dream
      : this.trip ? R.routes[this.trip]
      : (R.routes[s.route] || R.routes.inside);
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
    // 早高峰单行道路段（和坡道一样按路程比例算 y 区间；梦里没有单行道）
    if (this.oneWay && !this.dream) {
      this.oneWayTopY = this.startY - len * R.oneWay.range[1];
      this.oneWayBotY = this.startY - len * R.oneWay.range[0];
    } else {
      this.oneWayTopY = this.oneWayBotY = -1;
    }
    // 红绿灯（梦里没有灯；起始相位随机，每局不一样）
    if (this.route.lightAt != null) {
      this.lightY = this.startY - len * this.route.lightAt;
      this.lightPhase = Math.random() * (R.trafficLight.greenMs + R.trafficLight.yellowMs + R.trafficLight.redMs);
      this.lightPassed = false;   // 这一局是否已经过线（闯红灯判定只做一次）
      this.buildLight();
    } else {
      this.lightY = null;
    }
    // 交警检查点（校外 / 去后湖的路上，而且今天有交警）：每次单独掷一次是否真的碰上，第一天早晨的校外路线必碰上
    const rideEncounter = (!this.trip && s.day === 1) || Math.random() < CONFIG.police.encounterChance;
    this.policeY = (this.route.policeAt && s.policeToday && rideEncounter) ? this.startY - len * this.route.policeAt : null;
    this.policeDone = false;

    this.physics.world.setBounds(this.ROAD_L, 0, this.ROAD_R - this.ROAD_L, H);
    this.cameras.main.setBounds(0, 0, 960, H);

    // ---- 画地图 ----
    // 有道路真图：校正路沿并混合首尾后循环；地标只叠加两侧景观。
    // 没图：草地 / 街道 + 灰色路面色块（避免生成超长贴图）
    this.roadArt = UI.hasArt('road_tile');
    this.bgRoad = null;
    if (this.roadArt) {
      RideRoad.prepare(this, this.ROAD_L, this.ROAD_R);
      this.bgGrass = this.add.tileSprite(0, 0, 960, 540, RideRoad.tileKey).setOrigin(0).setScrollFactor(0);
      if (this.route.landmarkAt && UI.hasArt('road_stadium')) {
        const centerY = this.startY - len * this.route.landmarkAt;
        const key = RideRoad.landmark(this, centerY, this.ROAD_L, this.ROAD_R);
        const height = this.textures.get(key).getSourceImage().height;
        this.add.image(0, Math.round(centerY - height / 2), key).setOrigin(0);
      }
    } else {
      const sideTex = this.route.side || (s.route === 'outside' ? 'road' : 'grass');   // 校外两边是街道
      this.bgGrass = this.add.tileSprite(0, 0, 960, 540, sideTex).setOrigin(0).setScrollFactor(0);
      if (sideTex === 'road') this.bgGrass.setTint(0x9ca3af);
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

    // 终点：教学楼（短途骑行换成食堂 / 后湖 / 图书馆）
    this.goalLabel = this.trip ? LINES.ride.tripGoal[this.trip] : '教学楼';
    this.add.tileSprite(0, 0, 960, this.goalY - 60, 'building').setOrigin(0);
    this.add.text(480, (this.goalY - 60) / 2, this.goalLabel.split('').join(' '), UI.style(40, '#fecaca')).setOrigin(0.5);
    g.fillStyle(0xffffff, 0.9);
    for (let x = this.ROAD_L; x < this.ROAD_R; x += 40) g.fillRect(x, this.goalY, 20, 10);
    // 起点
    this.add.text(480, this.startY + 120, this.trip ? '出发' :
      (s.route === 'outside' ? '校门口（校外路线）' : '宿舍（校内路线）'),
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
    this.player = this.physics.add.sprite(this.LANES[2], this.startY, 'rider');
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
    this.balance = null;      // 被撞后的稳车 QTE，非空时车停下来等人按 A / D
    this.fallen = false;
    this.getting = false;      // 扶正了、正停着准备骑上去
    this.presses = 0;
    this.ending = false;
    this.wateringBgm = null;
    this.events.once('shutdown', () => this.stopWateringBgm());
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
    UI.say(this, this.dream ? LINES.ride.dreamStart : this.trip ? LINES.ride.tripStart[this.trip] :
      (s.route === 'outside' ? LINES.ride.startOutside : LINES.ride.startInside), this.player);
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
    this.updateWateringBgm();
    if (this.lightY) { this.updateLight(); this.checkLightPass(); }   // 红绿灯：灯色刷新 + 闯灯判定
    if (UI.blocked(this) || this.ending) { this.player.setVelocity(0); return; }

    // ---- 平衡：被撞之后车歪一下，限时按 A / D 稳住 ----
    if (this.balance) { this.updateBalance(); return; }

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

    // ---- 耗电：只在移动时掉，坡道、载人掉得快（梦里不掉电）----
    const moving = (this.vy < -5 || d.x !== 0) ? 1 : 0;
    if (!this.dream) {
      s.battery -= moving * (onSlope ? R.drainSlope : R.drainFlat) *
        (s.passenger ? CONFIG.passenger.drainFactor : 1) * dt;
    }

    // ---- 独白提示 ----
    if (onSlope && !this.warnedSlope) { this.warnedSlope = true; UI.say(this, LINES.ride.slope, p); }
    if (this.inOneWay(p.y) && !this.warnedOneWay) { this.warnedOneWay = true; UI.say(this, LINES.ride.oneWayEnter, p); }
    if (s.battery < 15 && !this.warnedLow) { this.warnedLow = true; UI.say(this, LINES.ride.lowBattery, p); }
    if (this.policeY && !this.warnedPolice && p.y - this.policeY < 700) {
      this.warnedPolice = true;
      UI.say(this, LINES.ride.policeAhead, p);
    }

    // ---- 剩余距离 ----
    this.distText.setText('距' + this.goalLabel + ' ' + Math.max(0, Math.round((p.y - this.goalY) / 10)) + ' m');

    // ---- 结束判定（梦里不会没电）----
    if (!this.dream && s.battery <= 0) { this.batteryDead(); return; }
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
    }, 'police');
  }

  // 停车接受检查：和 v1 一样，没头盔 / 没牌照 / 载人各罚一笔，被罚耽误时间
  policeStop() {
    const s = GameState;
    const r = policeCheck(s.passenger);
    if (r.fines.length) UI.sfx(this, 'pay');
    UI.updateHud(this);
    // 去后湖的路上碰上的，先交代一句场景
    const head = this.trip ? LINES.police.houhu + '\n\n' : '';
    UI.alert(this, head + LINES.police.stop + '\n\n' + policeText(r), () => {
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
    const type = this.pickType();
    const T = CONFIG.ride.traffic;
    // 来车往下、去车往上；先选方向，再选对应半幅，车型不再绑定方向。
    const dir = Math.random() < T.oncomingChance ? 1 : -1;
    const isRider = type === 'delivery' || type === 'wrong';
    const wrongChance = T.wrongWayChance * (this.inOneWay(p.y) ? CONFIG.ride.oneWay.wrongMul : 1);
    const wrongWay = !this.dream && isRider && Math.random() < wrongChance;
    const lane = Phaser.Utils.Array.GetRandom(this.directionLanes(wrongWay ? -dir : dir));
    let o;

    if (type === 'delivery') {
      // 外卖车两向都有：去车从后方赶上，来车从前方驶近。
      const rush = this.dream ? 1.1 : 1.7;
      o = this.addCar(type, 'npc_delivery', lane, dir > 0 ? top - 80 : bottom + 60, dir * CONFIG.ride.speed * rush);
      if (!o) return;
      if (!this.dream && dir < 0) {
        // 屏幕底部闪一个"！"，提醒后面有车冲上来
        const warn = this.add.text(o.x, 530, '！', UI.style(30, '#f97316'))
          .setOrigin(0.5, 1).setScrollFactor(0).setDepth(900);
        this.tweens.add({ targets: warn, alpha: 0, duration: 900, onComplete: () => warn.destroy() });
      }
    } else if (type === 'wrong') {
      // 旧配置里的 wrong 权重代表普通电动车，不再把所有电动车都当成逆行。
      // 从独立的电动车骑手素材里随机选，保留原本的服装和车辆颜色。
      const riders = ['npc_wrong', 'npc_rider_green', 'npc_rider_helmet_blue',
        'npc_rider_helmet_yellow', 'npc_rider_scooter_blue'].filter(k => UI.hasArt(k));
      const key = riders.length ? Phaser.Utils.Array.GetRandom(riders) : 'npc_wrong';
      o = this.addCar(type, key, lane, top - 80, dir * Phaser.Math.Between(125, 175));
      if (!o) return;
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
      // 汽车（校外）：两向通行；两款小轿车里随机挑一辆有图的。
      const cars = ['npc_car', 'npc_car_2'].filter(k => UI.hasArt(k));
      o = this.addCar(type, cars.length ? Phaser.Utils.Array.GetRandom(cars) : 'npc_car', lane, top - 120, dir * 90);
    } else {
      // 校车：又大又慢，挡在前面
      // 大车：校车 / 洒水车各两款，有图的里面随机挑一辆（都没图就用 npc_bus 色块）
      const bigs = ['npc_bus', 'npc_bus_2', 'npc_cart', 'npc_cart_2'].filter(k => UI.hasArt(k));
      const big = bigs.length ? Phaser.Utils.Array.GetRandom(bigs) : 'npc_bus';
      o = this.addCar('bus', big, lane, top - 160, dir * 50);
    }
    if (!o) return;
    this.sizeNpc(o, type);
  }

  // 方向对应的正常半幅：左侧来车，右侧去车。
  directionLanes(dir) {
    return dir > 0 ? this.LANES.slice(0, 2) : this.LANES.slice(2);
  }

  // 出生点被占用只尝试同一半幅，避免拥堵时把车流随机塞进对向车道。
  addCar(type, key, want, y, vy) {
    // 出生点检查用实际显示高度：有真图按 sizes，没图按占位图
    const S = CONFIG.ride.sizes[type];
    const h = S && UI.hasArt(key) ? S.height : this.textures.getFrame(key).height;
    const half = this.directionLanes(want < (this.ROAD_L + this.ROAD_R) / 2 ? 1 : -1);
    const lanes = [want].concat(Phaser.Utils.Array.Shuffle(half.filter(x => x !== want)));
    const x = lanes.find(x => this.laneFree(x, y, h, null));
    if (x === undefined) return null;
    const o = this.npcs.create(x, y, key);
    o.setVelocityY(vy);
    o.setAngle(vy > 0 ? 180 : 0);
    // type：障碍类型；lane：所在（或正要换去）的车道；speed：正常车速，排队 / 停下后恢复用
    o.setData('type', type).setData('lane', x).setData('speed', vy);
    const rider = type === 'wrong' || type === 'delivery';
    o.setData('wrongWay', !this.directionLanes(Math.sign(vy)).includes(x));
    o.setData('canCrossLane', !this.dream && rider && Math.random() < CONFIG.ride.traffic.crossLaneChance);
    o.setData('nextLaneChange', 0);
    return o;
  }

  // 按路线配置权重选车型；逆行概率在选好方向后独立决定。
  pickType() {
    const w = Object.assign({}, this.route.npc);
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

  // ---------- 红绿灯 ----------
  // 灯的相位：绿 → 黄 → 红 循环（时间从进场起算）
  lightColor() {
    const T = CONFIG.ride.trafficLight;
    let t = (this.time.now + this.lightPhase) % (T.greenMs + T.yellowMs + T.redMs);
    if (t < T.greenMs) return 'green';
    if (t < T.greenMs + T.yellowMs) return 'yellow';
    return 'red';
  }

  // 停止线 + 斑马线 + 路边灯箱（灯泡颜色每帧在 updateLight 里刷）
  buildLight() {
    const y = this.lightY;
    const g = this.add.graphics().setDepth(3);
    // 停止线（横跨路面）
    g.fillStyle(0xffffff, 0.9).fillRect(this.ROAD_L, y, this.ROAD_R - this.ROAD_L, 6);
    // 斑马线（停止线上方，玩家过来先看到）
    g.fillStyle(0xffffff, 0.55);
    for (let x = this.ROAD_L + 14; x < this.ROAD_R; x += 34) g.fillRect(x, y - 58, 20, 40);
    // 灯箱：路右边一根杆 + 三个灯泡位置
    this.lightBulbs = {};
    const px = this.ROAD_R + 26;
    g.fillStyle(0x1f2937, 1).fillRect(px - 3, y - 52, 6, 52);          // 灯杆
    g.fillStyle(0x111827, 1).fillRoundedRect(px - 10, y - 78, 20, 52, 6); // 灯箱
    const colors = { red: 0xef4444, yellow: 0xfacc15, green: 0x22c55e };
    for (const c of ['red', 'yellow', 'green']) {
      this.lightBulbs[c] = this.add.circle(px, y - 66 + ['red', 'yellow', 'green'].indexOf(c) * 17, 6, colors[c])
        .setDepth(4).setAlpha(0.15);
    }
    this.add.text(px + 16, y - 40, '红灯停', UI.style(14, '#fca5a5')).setOrigin(0, 1);
  }

  // 每帧刷新灯泡显示
  updateLight() {
    const c = this.lightColor();
    for (const k in this.lightBulbs) this.lightBulbs[k].setAlpha(k === c ? 1 : 0.15);
  }

  // 玩家过停止线：红灯（含黄灯）算闯灯，按概率被抓拍
  checkLightPass() {
    if (this.lightPassed || !this.lightY || this.ending) return;
    const p = this.player;
    if (p.y > this.lightY) return;   // 还没过线
    this.lightPassed = true;
    const c = this.lightColor();
    if (c === 'green') return;
    // 闯红灯了：先闪光灯吓一下，稍后罚单寄到
    const T = CONFIG.ride.trafficLight;
    if (Math.random() >= T.catchChance) return;
    this.cameras.main.flash(180, 255, 255, 255);
    UI.sfx(this, 'whistle');
    UI.say(this, LINES.ride.lightFlash, this.player);
    this.time.delayedCall(1800, () => {
      if (this.ending) return;   // 快到终点被别的结算抢先就算了
      addFine(LINES.ride.lightFineReason, T.fine);
      UI.sfx(this, 'pay');
      UI.updateHud(this);
      UI.alert(this, LINES.ride.lightFineHead.replace('{m}', T.fine), () => {
        const k = hiddenEndingKey();   // 罚到没钱 → 隐藏结局
        if (k) UI.fadeTo(this, 'Ending', { key: k });
      });
    });
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
    if (this.time.now < o.getData('nextLaneChange')) return false;
    const i = this.LANES.indexOf(o.getData('lane'));
    const home = this.directionLanes(Math.sign(o.getData('speed')));
    const adjacent = Phaser.Utils.Array.Shuffle([i - 1, i + 1])
      .map(j => this.LANES[j]).filter(x => x !== undefined);
    // 优先本方向的车道；少量骑手在本侧堵住时允许越线，之后优先回本侧。
    const candidates = adjacent.filter(x => home.includes(x));
    if (o.getData('canCrossLane')) candidates.push(...adjacent.filter(x => !home.includes(x)));
    const side = candidates.find(x => this.laneFree(x, o.y, o.displayHeight, o));
    if (side === undefined) return false;
    o.setData('lane', side);   // x 在 trafficStep 里慢慢挪过去
    o.setData('wrongWay', !home.includes(side));
    o.setData('nextLaneChange', this.time.now + CONFIG.ride.traffic.laneChangeCooldownMs);
    return true;
  }

  // 每帧：排队、变道、躲让、行人等车
  trafficStep(delta) {
    if (this.balance) return;   // 稳车时车停住了，别让别的车从身上碾过去
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

      // 红灯（含黄灯）：同向车在停止线前排队；逆行车（往下开）不看这个灯
      if (this.lightY && this.lightColor() !== 'green' && speed < 0 &&
          o.y > this.lightY && o.y - this.lightY < CONFIG.ride.followGap) {
        o.setVelocityY(0);
        return;
      }

      const front = this.carAhead(o);
      if (!front) {
        // 借道 / 逆行的骑手有空位就回到正常半幅，避免长期占住对向车流。
        if (!changing && o.getData('wrongWay')) this.changeLane(o);
        o.setVelocityY(speed);
        return;
      }
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
        // 普通电动车也会绕过慢车；无法变道时按前车速度排队。
        if (!this.changeLane(o)) o.setVelocityY(follow);
      } else {
        // 汽车 / 校车：减速排队
        o.setVelocityY(follow);
      }
    });
  }

  // 行人：红灯（含黄灯）在路边等灯；绿灯再看车让行——再走一步就进某辆车的道、而那辆车在 followGap 内驶近（或正挡着）→ 停一下，车过去再走
  walkerStep(o, speed) {
    if (this.lightY && this.lightColor() !== 'green') { o.setVelocityX(0); return; }
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
  }

  // 最近的洒水车决定音量，使用世界坐标，镜头滚动不影响距离。
  updateWateringBgm() {
    let distance = Infinity;
    for (const o of this.npcs.getChildren()) {
      if (!o.active || !String(o.texture.key).startsWith('npc_cart')) continue;
      distance = Math.min(distance, Math.hypot(o.x - this.player.x, o.y - this.player.y));
    }
    if (distance === Infinity) { this.stopWateringBgm(); return; }
    const { nearDistance, farDistance, maxVolume } = CONFIG.ride.wateringAudio;
    const t = Phaser.Math.Clamp((distance - nearDistance) / (farDistance - nearDistance), 0, 1);
    const volume = maxVolume * (1 - t * t * (3 - 2 * t));
    // 范围外保留播放进度，来回经过边界时音乐不会重复从头开始。
    if (!this.wateringBgm && volume > 0) this.startWateringBgm();
    if (this.wateringBgm) this.wateringBgm.setVolume(volume);
  }

  startWateringBgm() {
    if (this.wateringBgm || !this.cache.audio.exists('watering_bgm')) return;
    this.wateringBgm = this.sound.add('watering_bgm', { loop: true, volume: 0 });
    this.wateringBgm.play();
  }

  stopWateringBgm() {
    if (!this.wateringBgm) return;
    this.wateringBgm.stop();
    this.wateringBgm.destroy();
    this.wateringBgm = null;
  }

  // ---------- 被撞 ----------
  onHit(o) {
    if (this.dream) return;   // 梦里大家都守规矩，撞不到一起
    if (this.fallen || this.getting || this.ending || UI.busy || o.getData('hit')) return;
    if (this.time.now < this.invUntil || this.balance) return;
    o.setData('hit', true);   // 同一个障碍只撞一次

    GameState.hits += 1;
    UI.sfx(this, 'hit');
    this.cameras.main.shake(150, 0.008);
    this.vy = 60;   // 被撞得往后退一下

    // 先进入稳车：撞完这一次先扔给平衡环节处理，按对 / 按错再决定掉不掉血
    if (CONFIG.ride.balanceEnabled && !this.balance) { this.startBalance(); return; }

    // 关掉稳车时退回原来的扣血流程
    GameState.hp -= 1;
    if (GameState.hp <= 0) { this.fall(); return; }

    // 没摔死：可能触发"争辩判责"（按交通规范判这事儿谁负责）
    if (Math.random() < CONFIG.ride.dispute.chance) {
      this.dispute(o.getData('type'), o);
      this.invUntil = this.time.now + CONFIG.ride.invincibleMs;
      return;
    }
    UI.say(this, LINES.ride.hit, this.player);
    this.invUntil = this.time.now + CONFIG.ride.invincibleMs;
    this.tweens.add({ targets: this.player, alpha: 0.2, duration: 100, yoyo: true,
      repeat: Math.floor(CONFIG.ride.invincibleMs / 200) - 1, onComplete: () => this.player.setAlpha(1) });
  }

  // ---------- 被撞后的稳车：冒出左右方向，限时按 A / D 把车扶正 ----------
  // 车停下、车身慢慢歪过去（歪得越多越像要倒），进度条走完 / 按错方向就算失手。
  startBalance() {
    const B = CONFIG.ride.balance;
    const dir = Math.random() < 0.5 ? -1 : 1;
    this.balance = { dir, start: this.time.now, ms: B.windowMs };
    this.player.setVelocity(0);
    const L = LINES.ride;
    const arrow = this.add.text(480, 118, dir < 0 ? L.balanceLeft : L.balanceRight,
      UI.style(72, '#fde047', { stroke: '#1f2937', strokeThickness: 8 }))
      .setOrigin(0.5).setScrollFactor(0).setDepth(1200);
    const tip = this.add.text(480, 190, L.balanceTip, UI.style(18, '#fca5a5'))
      .setOrigin(0.5).setScrollFactor(0).setDepth(1200);
    this.balObjs = [arrow, tip];
    this.balBar = this.add.graphics().setScrollFactor(0).setDepth(1201);
  }

  updateBalance() {
    const k = this.keys;
    const left = Phaser.Input.Keyboard.JustDown(k.A) || Phaser.Input.Keyboard.JustDown(k.LEFT);
    const right = Phaser.Input.Keyboard.JustDown(k.D) || Phaser.Input.Keyboard.JustDown(k.RIGHT);
    if (left || right) {
      if ((right ? 1 : -1) === this.balance.dir) this.balanceOk();
      else this.balanceLose();
      return;
    }
    const t = (this.time.now - this.balance.start) / this.balance.ms;
    if (t >= 1) { this.balanceLose(); return; }
    this.player.setVelocity(0).setAngle(this.balance.dir * CONFIG.ride.balance.nudgeDeg * t);
    const g = this.balBar;
    g.clear();
    g.fillStyle(0x000000, 0.6).fillRect(370, 214, 220, 10);
    g.fillStyle(t > 0.7 ? 0xef4444 : t > 0.45 ? 0xfacc15 : 0x22c55e, 1).fillRect(372, 216, 216 * (1 - t), 6);
  }

  clearBalance() {
    this.balance = null;
    if (this.balObjs) { this.balObjs.forEach(o => o.destroy()); this.balObjs = null; }
    if (this.balBar) { this.balBar.destroy(); this.balBar = null; }
  }

  balanceOk() {
    const B = CONFIG.ride.balance;
    this.clearBalance();
    this.vy = 0;
    this.player.setAngle(0);
    UI.say(this, LINES.ride.balanceOk, this.player);
    this.tweens.add({ targets: this.player, angle: 5, duration: B.okSwayMs / 2, yoyo: true,
      onComplete: () => this.player.setAngle(0) });
    this.invUntil = this.time.now + CONFIG.ride.invincibleMs;
  }

  balanceLose() {
    const B = CONFIG.ride.balance;
    this.clearBalance();
    this.vy = 0;
    this.player.setAngle(0);
    if (B.failFall) { this.fall(); return; }
    // 关掉"失手即倒"时：扣一血 + 掉点电，车晃一下继续骑
    GameState.hp -= 1;
    GameState.battery -= CONFIG.ride.fallBatteryCost;
    UI.updateHud(this);
    UI.sfx(this, 'fall');
    UI.say(this, LINES.ride.balanceNearly, this.player);
    this.invUntil = this.time.now + CONFIG.ride.invincibleMs;
    if (GameState.hp <= 0) this.fall();
  }

  // ---------- 争辩判责 ----------
  // 撞上 type 类型的障碍后随机出题：判对和平解决；判错对方报警（等交警 + 自己有责任时吃罚单）
  dispute(type, obstacle) {
    const D = CONFIG.ride.dispute;
    const all = LINES.dispute.questions;
    const fit = all.filter(q => {
      if (!q.types || !q.types.includes(type)) return false;
      // 车型已经与方向分离，正常电动车不能被题目误称为逆行车，来向外卖车也不是后方追尾。
      if (q.types.length === 1 && q.types[0] === 'wrong') return obstacle.getData('wrongWay');
      if (q.types.length === 1 && q.types[0] === 'delivery') return obstacle.getData('speed') < 0;
      return true;
    });
    const q = UI.rand(fit.length ? fit : all);
    this.player.setVelocity(0);
    UI.choice(this, q.q, q.opts, i => {
      if (i === q.answer) {
        GameState.clock += D.settleMinutes;   // 说清楚了，各走各的
        UI.say(this, q.right, this.player);
      } else if (q.fault) {
        // 判错 + 事故里自己有责任：对方报警，交警按交规罚自己
        GameState.clock += D.alarmMinutes;
        addFine(q.reason, q.fine);
        UI.sfx(this, 'policeVoice');
        UI.sfx(this, 'pay');
        UI.updateHud(this);
        UI.alert(this, q.wrong + '\n' + LINES.dispute.fineLine.replace('{m}', q.fine), () => {
          const k = hiddenEndingKey();   // 罚到没钱 → 隐藏结局
          if (k) UI.fadeTo(this, 'Ending', { key: k });
        });
        return;
      } else {
        // 判错但责任在对方：白等一场交警
        GameState.clock += D.alarmMinutes;
        UI.sfx(this, 'policeVoice');
        UI.say(this, q.wrong, this.player);
      }
      this.invUntil = this.time.now + 1500;
    }, 'dispute');
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
    s.clock += CONFIG.ride.deadBatteryMinutes;
    UI.hint(this, null);
    const dead = () => UI.say(this, LINES.ride.dead, this.player);
    // 短途骑行没电：不记上午迟到（latePM 由到教室的钟点判），推到目的地接着走流程
    if (this.trip) {
      dead();
      if (this.trip === 'back') {
        // 回教学楼的路上没电：推过去直接进教室
        this.time.delayedCall(1600, () => UI.fadeTo(this, 'Class', { part: 'afternoon' }));
      } else {
        this.time.delayedCall(1600, () => UI.fadeTo(this, 'Park',
          { place: this.place, meal: this.meal, evening: this.evening, pushing: true }));
      }
      return;
    }
    s.late = true;
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
    if (this.dream) { this.dreamWake(); return; }   // 彩蛋：梦到教学楼就醒了
    if (this.trip) {
      // 短途骑行：到了地方停车（吃饭 / 自习）；回程直接进下午课
      if (this.trip === 'back') UI.fadeTo(this, 'Class', { part: 'afternoon' });
      else UI.fadeTo(this, 'Park', { place: this.place, meal: this.meal, evening: this.evening, pushing: false });
      return;
    }
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

  // ---------- 彩蛋：梦醒了 ----------
  dreamWake() {
    GameState.clockPaused = false;
    this.time.delayedCall(900, () => {
      UI.alert(this, LINES.ride.dreamWake, () => {
        newGame();
        UI.fadeTo(this, 'Title');
      });
    });
  }
}
