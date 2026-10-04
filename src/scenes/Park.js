// ===== 场景3 / 3′ Park：停车（B 负责）=====
// data.place：'teach' 教学楼车棚（默认，完整玩法：多米诺 + 门口违停）
//             'canteen' / 'houhu' / 'library' 中午 / 傍晚的简易停车（车少好停、撞不倒）
// data.meal：停好车后要做的事（'canteen' | 'houhu' | 'library'，吃饭 / 自习，teach 不用）
// data.evening：傍晚吃的（吃完直接进晚上充电）；中午的吃完骑回教学楼上下午课
// data.pushing = true 时是推车（没电），速度减半。
class Park extends Phaser.Scene {
  constructor() { super('Park'); }

  init(data) {
    data = data || {};
    this.place = data.place || 'teach';
    this.meal = data.meal || null;
    this.evening = !!data.evening;
    this.pushing = !!data.pushing;
  }

  create() {
    UI.setup(this);
    UI.sfx(this, 'tow', { loop: true });
    const P = CONFIG.park;
    const PL = P.places[this.place];   // 这个停车场景的布局参数
    const art = PL.art && UI.hasArt(PL.art.key) && this.textures.exists(PL.art.key) ? PL.art : null;
    this.speed = P.rideSpeed * (this.pushing ? P.pushSpeedFactor : 1) * speedMul();   // 饿了更慢

    // ---- 布局：两排车棚，中间是通道（宽窄跟着车位数走）----
    const W = Math.max(960, 260 + PL.perRow * 44 + 108), H = 540;
    if (art) this.physics.world.setBounds(...art.bounds);
    else this.physics.world.setBounds(0, 70, W, H - 70);
    this.cameras.main.setBounds(0, 0, W, H);

    if (art) {
      this.add.image(0, 0, art.key).setOrigin(0).setDisplaySize(W, H);
    } else if (this.place === 'teach' && UI.hasArt('bg_park')) {
      // 有真图：按宽铺满、保持比例，底对齐（车棚空地铺满画面），顶上加一条暗色标题栏
      this.add.image(0, H, 'bg_park').setOrigin(0, 1).setDisplaySize(W, W * 1024 / 1536);
      this.add.rectangle(0, 0, W, 70, 0x000000, 0.55).setOrigin(0);
    } else {
      this.add.tileSprite(0, 0, W, H, 'road').setOrigin(0);
      this.add.tileSprite(0, 0, W, 70, 'building').setOrigin(0);
    }
    if (!art) this.add.text(W / 2, 35, LINES.park.places[this.place], UI.style(26, '#fecaca')).setOrigin(0.5);
    // 教学楼门口（左侧入口）
    this.add.text(art ? 106 : 20, art ? 319 : 470, '← 入口', UI.style(18, art ? '#fff2d7' : '#9ca3af',
      art ? { backgroundColor: '#253c3c', padding: { x: 6, y: 3 } } : {}));

    // 车位：上排 y=150，下排 y=400
    const SLOT_GAP = 44, FIRST_X = 260, PER_ROW = art ? art.columns.length : PL.perRow;
    const sx = art ? W / art.width : 1, sy = art ? H / art.height : 1;
    const rowsY = art ? art.rows.map(y => y * sy) : [150, 400];
    this.parkBikeSize = art ? {
      width: Math.min(P.bike.width, art.slotWidth * sx - 8),
      height: Math.min(P.bike.height, art.slotHeight * sy - 6)
    } : P.bike;
    const all = [];
    rowsY.forEach((y, r) => {
      for (let i = 0; i < PER_ROW; i++) all.push({ x: art ? art.columns[i] * sx : FIRST_X + i * SLOT_GAP, y, row: r, idx: i });
    });
    // 车棚顶棚示意
    if (!art) {
      const g = this.add.graphics();
      g.fillStyle(0x000000, 0.25);
      rowsY.forEach(y => g.fillRect(FIRST_X - 30, y - 45, PER_ROW * SLOT_GAP + 16, 90));
    }

    // 门口禁停区：入口旁、上排车棚左边，只画出来，不挡路（只有教学楼有）
    this.noPark = null;
    if (PL.illegal) {
      const zone = this.add.rectangle(160, 150, 70, 90, 0xef4444, 0.2).setStrokeStyle(3, 0xef4444);
      this.add.text(160, 150, LINES.park.noParkZone, UI.style(20, '#fca5a5')).setOrigin(0.5);
      this.noPark = zone.getBounds();
    }

    // 随机挑空位（教学楼不放在最靠近入口的 6 个里，逼玩家往里找；小场景随便放）
    const skip = this.place === 'teach' ? 6 : 2;
    const candidates = all.filter((s, i) => (i % PER_ROW) >= skip);
    const free = Phaser.Utils.Array.Shuffle(candidates.slice()).slice(0, PL.free);

    this.bikes = this.physics.add.staticGroup();
    this.slots = [];
    // this.rows[排][序号] = 那辆车；空位为 null（多米诺找邻车用）
    this.rows = rowsY.map(() => new Array(PER_ROW).fill(null));
    all.forEach(s => {
      if (free.includes(s)) {
        const slot = this.add.image(s.x, s.y, 'slot');
        if (art) slot.setDisplaySize(art.slotWidth * sx - 4, art.slotHeight * sy - 4).setTint(0xd5ec8d);
        this.tweens.add({ targets: slot, alpha: 0.4, duration: 600, yoyo: true, repeat: -1 });
        this.slots.push(slot);
      } else {
        // 有真图就用 7 种颜色的别人的车，没图用 bike_other + 随机染色
        const bikeArt = UI.hasArt('dorm_bike_1');
        const key = bikeArt ? 'dorm_bike_' + Phaser.Math.Between(1, 7) : 'bike_other';
        const jitter = art ? 1 : 4;
        const b = this.bikes.create(s.x + Phaser.Math.Between(-jitter, jitter), s.y, key);
        if (bikeArt) b.setDisplaySize(this.parkBikeSize.width, this.parkBikeSize.height);
        else b.setTint(Phaser.Display.Color.HSVToRGB(Math.random(), 0.15, 1).color);
        b.setAngle(art ? Phaser.Math.Between(-4, 4) : Phaser.Math.Between(-12, 12));
        b.refreshBody();
        if (bikeArt) b.body.setSize(Math.min(P.bike.bodyWidth, this.parkBikeSize.width - 4),
          Math.min(P.bike.bodyHeight, this.parkBikeSize.height - 4));   // 静态体按世界像素，要放在 refreshBody 之后
        // 记下排号、序号、原来的角度和 x（扶起来时复原）
        b.setData({ row: s.row, idx: s.idx, angle0: b.angle, x0: b.x, fallen: false });
        this.rows[s.row][s.idx] = b;
      }
    });

    // ---- 主角 ----
    // 骑车：俯视图，跟着方向转；推车：侧视图（人扶着车），不转，只按左右翻转
    this.player = this.physics.add.sprite(art ? 130 : 80, 275, this.pushing ? 'pusher' : 'rider');
    const look = this.pushing ? P.pusher : P.rider;
    const key = this.pushing ? 'pusher' : 'rider';
    if (UI.hasArt(key)) UI.look(this.player, key, look.width, look.height);
    // 推车有逐帧图：换成推车走路图（左右两套，不用翻转）
    this.pushFrames = this.pushing && UI.pushWalk(this, this.player, { x: 1, y: 0 });
    if (this.pushFrames) this.player.setDisplaySize(P.pushWalk.width, P.pushWalk.height);
    this.player.setCollideWorldBounds(true);
    // 碰撞框小一点，方便钻进车位；动态体要换算回纹理像素
    const bw = look.bodyWidth / this.player.scaleX, bh = look.bodyHeight / this.player.scaleY;
    this.player.body.setSize(bw, bh).setOffset((this.player.width - bw) / 2, (this.player.height - bh) / 2);
    this.turn(1, 0);                    // 面朝右（往车棚里走）
    this.physics.add.collider(this.player, this.bikes, (player, bike) => this.bump(bike));
    this.cameras.main.startFollow(this.player, true, 0.15, 0);
    this.done = false;
    this.lastBump = -Infinity;   // 上次撞车判定的时刻（多米诺冷却用）

    // ---- 界面 ----
    UI.createClock(this);
    UI.createHud(this, false);
    if (this.pushing && this.place === 'teach') {   // "已迟到"是上午的判定，中午/傍晚推车不显示
      this.add.text(12, 92, '已迟到', UI.style(20, '#ffffff', {
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
    UI.updateHud(this);
    const f = UI.pressedF(this);
    if (UI.pressedE(this) && !this.done) { this.player.setVelocity(0); UI.backpack(this); }
    if (UI.blocked(this) || this.done) {
      this.player.setVelocity(0);
      if (this.pushFrames && !this.done) UI.pushWalk(this, this.player, { x: 0, y: 0 });   // 停下时站着不动
      return;
    }

    // ---- 移动 ----
    const d = UI.dir(this);
    const v = new Phaser.Math.Vector2(d.x, d.y).normalize().scale(this.speed);
    this.player.setVelocity(v.x, v.y);
    if (this.pushFrames) UI.pushWalk(this, this.player, d);
    else if (d.x || d.y) this.turn(d.x, d.y);

    // ---- 旁边有倒着的车：优先扶起来 ----
    const down = this.nearestFallen(50);
    if (down) {
      UI.hint(this, LINES.park.liftHint);
      if (f) this.liftBike(down);
      return;
    }

    // ---- 是否在空车位上 ----
    const slot = this.slots.find(s => Phaser.Math.Distance.BetweenPoints(this.player, s) < 30);
    if (slot) {
      UI.hint(this, '按 F 停车');
      if (f) {
        if (this.hasFallen()) UI.say(this, LINES.park.liftFirst, this.player);   // 倒着的车没扶完，不让停
        else this.parkAt(slot);
      }
      return;
    }

    // ---- 是否在门口禁停区 ----
    if (this.noPark && this.noPark.contains(this.player.x, this.player.y)) {
      UI.hint(this, LINES.park.illegalHint);
      if (f) {
        if (this.hasFallen()) UI.say(this, LINES.park.liftFirst, this.player);
        else this.askIllegal();
      }
      return;
    }

    // ---- 靠近别人的车：按 F 吐槽 ----
    const near = this.bikes.getChildren().some(b => Phaser.Math.Distance.BetweenPoints(this.player, b) < 50);
    UI.hint(this, near ? '按 F 查看' : null);
    if (near && f) UI.say(this, LINES.park.full, this.player);
  }

  // 朝向：骑车按方向转（车头朝上的图 +90°）；推车的侧视图不转，往左走就翻过来（原图车头朝右）
  turn(x, y) {
    if (this.pushFrames) return;   // 推车逐帧图自带左右朝向
    if (this.pushing && UI.hasArt('pusher')) { if (x) this.player.setFlipX(x < 0); return; }
    this.player.setAngle(Phaser.Math.RadToDeg(Math.atan2(y, x)) + 90);
  }

  // 停车公共部分：记录到达时间、判迟到、把车停到 (x, y)
  // 到达时间 / 迟到只属于上午的教学楼停车；中午 / 傍晚停车不覆盖上午记录
  parkHere(x, y) {
    this.done = true;
    UI.hint(this, null);
    if (this.place === 'teach') {
      GameState.arriveClock = GameState.clock;
      if (GameState.clock > CONFIG.classStart) GameState.late = true;
    }

    this.player.setVelocity(0);
    this.player.disableBody();   // 停好了不再碰撞（换图后碰撞框会跟着缩放变大，会被旁边的车挤开）
    this.player.anims.stop();    // 推车走路动画停掉，不然会把停好的车图换回去
    this.player.setTexture('bike').setAngle(0).setFlipX(false);
    // 有真图：和车棚里别人的车一样大
    if (UI.hasArt('bike')) this.player.setDisplaySize(this.parkBikeSize.width, this.parkBikeSize.height);
    else this.player.setScale(1);
    this.player.setPosition(x, y);
    UI.sfx(this, 'park');
  }

  parkAt(slot) {
    // 把车停进车位
    this.parkHere(slot.x, slot.y);
    slot.destroy();
    UI.say(this, LINES.park.parked, this.player);
    if (this.place === 'teach') {
      this.time.delayedCall(1200, () => UI.fadeTo(this, 'Class', { part: 'morning' }));
    } else {
      this.time.delayedCall(1200, () => this.interlude());
    }
  }

  // ---- 停好车之后的正事：吃饭 / 自习（结算钱、饥饿、时间），再回教学楼或进夜晚 ----
  interlude() {
    const s = GameState, P = CONFIG.places, M = LINES.meals;
    let text;
    if (this.meal === 'canteen') {
      spend(P.canteen.cost); eat(P.canteen.food); s.meals.push('食堂');
      s.clock += Phaser.Math.Between(P.canteen.minutes[0], P.canteen.minutes[1]);
      UI.sfx(this, 'pay');
      text = UI.rand(M.ateCanteen);
    } else if (this.meal === 'houhu') {
      if (s.money < P.houhu.cost) {
        // 路上被罚款，到地方已经吃不起
        text = M.fineNoFood;
      } else {
        s.battery = Math.max(0, s.battery - P.houhu.battery);
        spend(P.houhu.cost); eat(P.houhu.food); s.meals.push('后湖');
        s.clock += Phaser.Math.Between(P.houhu.minutes[0], P.houhu.minutes[1]);
        UI.sfx(this, 'pay');
        text = UI.rand(M.ateHouhu);
      }
    } else if (this.meal === 'library') {
      s.clock += Phaser.Math.Between(P.library.minutes[0], P.library.minutes[1]);
      text = UI.rand(M.studied);
    } else {
      text = M.skipped;
    }
    UI.updateHud(this);
    UI.alert(this, text, () => {
      const k = hiddenEndingKey();   // 吃饭花光钱 / 饿晕 → 隐藏结局
      if (k) { UI.fadeTo(this, 'Ending', { key: k }); return; }
      // 中午：骑回教学楼上下午课；傍晚：直接进夜晚充电
      if (this.evening) UI.fadeTo(this, 'Charge');
      else UI.fadeTo(this, 'Ride', { trip: 'back' });
    });
  }

  // ---- 门口违停：问一下，停了之后可能被贴条 ----
  askIllegal() {
    const L = LINES.park, P = CONFIG.park;
    this.player.setVelocity(0);
    UI.choice(this, L.illegalAsk, [L.illegalYes, L.illegalNo], i => {
      if (i !== 0) return;   // 算了，继续找车位
      this.parkHere(this.noPark.centerX, this.noPark.centerY);   // 里面会立刻把 done 设 true
      UI.say(this, L.illegalParked, this.player);
      const toClass = () => UI.fadeTo(this, 'Class', { part: 'morning' });

      if (Math.random() < P.ticketChance) {
        // 被贴条：罚款可以扣成负数，不算进 spent（和 policeCheck 一致）
        addFine(L.ticketReason, P.ticketFine);
        UI.sfx(this, 'pay');
        UI.updateHud(this);
        // 弹窗关掉时：罚到没钱 → 隐藏结局，否则照常去上课
        const afterTicket = () => {
          const k = hiddenEndingKey();
          if (k) UI.fadeTo(this, 'Ending', { key: k });
          else toClass();
        };
        this.time.delayedCall(800, () =>
          UI.alert(this, L.ticketHead + '\n' + L.ticketReason + '　罚 ¥' + P.ticketFine, afterTicket));
      } else {
        this.time.delayedCall(1200, () => UI.say(this, L.noTicket, this.player));
        this.time.delayedCall(2600, toClass);
      }
    }, 'illegal');
  }

  // ---- 多米诺：撞到别人的车，可能倒一排（collider 回调；简易停车场景撞不倒）----
  bump(bike) {
    const P = CONFIG.park;
    if (!P.places[this.place].domino) return;
    if (this.done || bike.getData('fallen')) return;              // 倒着的车不当新起点
    if (this.time.now - this.lastBump < P.dominoCooldownMs) return;
    if (this.player.body.speed < this.speed * 0.3) return;         // 基本没在动（body.speed 是这一步碰撞前的速度）
    this.lastBump = this.time.now;
    if (Math.random() >= P.dominoChance) return;

    // 玩家在车左边就往右倒，反之往左；沿同一排找，遇到空位 / 倒着的车 / 排尾就停
    const dir = this.player.x < bike.x ? 1 : -1;
    const row = this.rows[bike.getData('row')];
    const chain = [];
    for (let i = bike.getData('idx'); i >= 0 && i < row.length && chain.length < P.dominoMax; i += dir) {
      const b = row[i];
      if (!b || b.getData('fallen')) break;
      chain.push(b);
    }

    // 先全部标记为倒下（防止重复触发），再一辆接一辆播动画
    chain.forEach((b, k) => {
      b.setData('fallen', true);
      this.time.delayedCall(k * P.dominoDelayMs, () => {
        if (!b.getData('fallen')) return;   // 还没倒就被扶起来了
        this.tweens.add({ targets: b, angle: dir * CONFIG.findCar.fallAngle, x: b.getData('x0') + dir * CONFIG.findCar.fallShift,
          duration: 150, ease: 'Quad.In' });
      });
    });
    UI.sfx(this, 'domino');
    this.cameras.main.shake(120, 0.005);
    UI.say(this, LINES.park.domino, this.player);
  }

  // 还有没有倒着的车
  hasFallen() {
    return this.bikes.getChildren().some(b => b.getData('fallen'));
  }

  // 距离 r 以内最近的一辆倒着的车，没有返回 null
  nearestFallen(r) {
    let best = null, bestD = r;
    this.bikes.getChildren().forEach(b => {
      if (!b.getData('fallen')) return;
      const dist = Phaser.Math.Distance.BetweenPoints(this.player, b);
      if (dist < bestD) { best = b; bestD = dist; }
    });
    return best;
  }

  // 扶起一辆：回到原来的角度和位置，花一点时间
  liftBike(b) {
    b.setData('fallen', false);
    this.tweens.killTweensOf(b);   // 正在倒的动画停掉
    this.tweens.add({ targets: b, angle: b.getData('angle0'), x: b.getData('x0'), duration: 200 });
    GameState.clock += CONFIG.park.liftMinutes;
    UI.sfx(this, 'park');
    UI.say(this, this.hasFallen() ? LINES.park.lift : LINES.park.liftedAll, this.player);
  }
}
