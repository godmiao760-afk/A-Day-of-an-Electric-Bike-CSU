// ===== 场景1 FindCar：宿舍楼下找车（B 负责）=====
// 规则见 项目说明.md 第 8 节。没有失败条件，时钟一直在走。
// 多米诺：挪开邻车时可能带倒同一排（往远离自己车的方向），全部扶起来才能解锁。
class FindCar extends Phaser.Scene {
  constructor() { super('FindCar'); }

  create() {
    UI.setup(this);
    const C = CONFIG.findCar;
    GameState.clock = CONFIG.startClock;

    // ---- 布局参数 ----
    const COL_GAP = 50;     // 车与车左右间距
    const ROW_GAP = 104;    // 行距（中间留出走道）
    const TOP = 190;        // 第一排车的 y
    const WORLD_W = 960;
    const WORLD_H = TOP + (C.rows - 1) * ROW_GAP + 170;
    const left = WORLD_W / 2 - (C.cols - 1) * COL_GAP / 2;

    this.physics.world.setBounds(0, 90, WORLD_W, WORLD_H - 90);
    this.cameras.main.setBounds(0, 0, WORLD_W, WORLD_H);

    // ---- 地面和宿舍楼 ----
    this.add.tileSprite(0, 0, WORLD_W, WORLD_H, 'road').setOrigin(0);
    this.add.tileSprite(0, 0, WORLD_W, 90, 'building').setOrigin(0);
    this.add.text(WORLD_W / 2, 45, '宿 舍 楼', UI.style(30, '#fecaca')).setOrigin(0.5);
    this.add.tileSprite(0, 90, 40, WORLD_H - 90, 'grass').setOrigin(0);
    this.add.tileSprite(WORLD_W - 40, 90, 40, WORLD_H - 90, 'grass').setOrigin(0);

    // ---- 车阵 ----
    this.bikes = this.physics.add.staticGroup();
    this.grid = [];
    const myRow = Phaser.Math.Between(0, C.rows - 1);
    const myCol = Phaser.Math.Between(1, C.cols - 2);   // 保证左右都有车夹着
    for (let r = 0; r < C.rows; r++) {
      this.grid[r] = [];
      for (let c = 0; c < C.cols; c++) {
        const mine = (r === myRow && c === myCol);
        // 自己的车在找到前和别人的车长得一样
        const b = this.bikes.create(left + c * COL_GAP, TOP + r * ROW_GAP, 'bike_other');
        b.setData({ mine, row: r, col: c, moved: false, fallen: false, x0: b.x });   // x0：扶起来时复原
        b.setTint(Phaser.Display.Color.HSVToRGB(Math.random(), 0.15, 1).color); // 稍微区分一下颜色
        if (mine) this.myBike = b;
        this.grid[r][c] = b;
      }
    }
    this.neighbors = [this.grid[myRow][myCol - 1], this.grid[myRow][myCol + 1]];
    this.discovered = false;  // 是否已经确认这是自己的车
    this.movedCount = 0;

    // ---- 主角 ----
    this.player = this.physics.add.sprite(WORLD_W / 2, WORLD_H - 60, 'player');
    this.player.setCollideWorldBounds(true);
    this.player.body.setSize(26, 26);
    this.physics.add.collider(this.player, this.bikes);
    this.cameras.main.centerOn(this.player.x, this.player.y);
    this.cameras.main.startFollow(this.player, true, 0.15, 0.15);

    // ---- 界面 ----
    UI.createClock(this);
    UI.createHud(this, false);
    this.signal = this.add.text(948, 56, '', UI.style(16, '#86efac', {
      backgroundColor: 'rgba(0,0,0,0.6)', padding: { x: 8, y: 3 }
    })).setOrigin(1, 0).setScrollFactor(0).setDepth(1000);
    this.nextBeep = 0;
    this.done = false;

    UI.say(this, isHungry() ? LINES.hungry : LINES.findCar.start, this.player);
    // 只提示背包在哪，不提醒要戴头盔
    this.bpTip = this.add.text(948, 90, LINES.findCar.backpackTip, UI.style(15, '#fde68a', {
      backgroundColor: 'rgba(0,0,0,0.6)', padding: { x: 8, y: 3 }
    })).setOrigin(1, 0).setScrollFactor(0).setDepth(1000);
  }

  update(time, delta) {
    UI.tickClock(this, delta);
    UI.updateHud(this);
    const f = UI.pressedF(this);
    if (UI.pressedE(this) && !this.done) {
      this.player.setVelocity(0);
      if (this.bpTip) { this.bpTip.destroy(); this.bpTip = null; }
      UI.backpack(this);
    }
    if (UI.blocked(this) || this.done) { this.player.setVelocity(0); return; }

    // ---- 移动（饿了走得慢）----
    const d = UI.dir(this);
    const v = new Phaser.Math.Vector2(d.x, d.y).normalize().scale(CONFIG.findCar.walkSpeed * speedMul());
    this.player.setVelocity(v.x, v.y);

    // ---- 找车提示：越近滴得越快，信号格越多 ----
    const dist = Phaser.Math.Distance.BetweenPoints(this.player, this.myBike);
    const level = Phaser.Math.Clamp(5 - Math.floor(dist / 120), 1, 5);
    this.signal.setText('钥匙信号 ' + '▮'.repeat(level) + '▯'.repeat(5 - level));
    if (time > this.nextBeep) {
      UI.sfx(this, 'beep');
      this.nextBeep = time + Phaser.Math.Clamp(dist * 1.6, 140, 1400);
    }

    // ---- 旁边有倒着的车：优先扶起来 ----
    const down = this.nearestFallen(64);
    if (down) {
      UI.hint(this, LINES.park.liftHint);
      if (f) this.liftBike(down);
      return;
    }

    // ---- 找最近的车 ----
    const target = this.nearestBike(64);
    if (!target) { UI.hint(this, null); return; }

    const mine = target.getData('mine');
    const isNeighbor = this.neighbors.includes(target) && !target.getData('moved');
    if (mine && this.discovered && this.movedCount > 0) UI.hint(this, '按 F 解锁');
    else if (isNeighbor && this.discovered) UI.hint(this, '按 F 挪开这辆车');
    else UI.hint(this, '按 F 查看');

    if (f) this.interact(target, mine, isNeighbor);
  }

  // 找离主角最近、在 range 以内的车（挪开的、倒着的不算）
  nearestBike(range) {
    let best = null, bestD = range;
    this.bikes.getChildren().forEach(b => {
      if (b.getData('moved') || b.getData('fallen')) return;
      const dd = Phaser.Math.Distance.BetweenPoints(this.player, b);
      if (dd < bestD) { bestD = dd; best = b; }
    });
    return best;
  }

  interact(bike, mine, isNeighbor) {
    if (mine) {
      if (!this.discovered) {
        // 第一次认出自己的车：换成黄色贴图
        this.discovered = true;
        bike.setTexture('bike').clearTint();
        this.tweens.add({ targets: bike, scale: 1.2, duration: 120, yoyo: true });
      }
      if (this.movedCount === 0) { UI.say(this, LINES.findCar.blocked, this.player); return; }
      if (this.hasFallen()) { UI.say(this, LINES.park.liftFirst, this.player); return; }   // 倒着的车没扶完，不让解锁
      this.unlock();
      return;
    }
    if (isNeighbor && this.discovered) { this.moveAway(bike); return; }
    UI.say(this, LINES.findCar.notMine, this.player);
  }

  // 把夹住自己车的那辆拖进走道
  moveAway(bike) {
    bike.setData('moved', true);
    this.physics.world.disable(bike);   // 不再挡路
    this.movedCount++;
    GameState.clock += CONFIG.findCar.moveCarMinutes;
    const dy = this.player.y > bike.y ? 34 : -34;
    this.tweens.add({ targets: bike, y: bike.y + dy, angle: Phaser.Math.Between(-35, 35), duration: 350 });
    if (!this.domino(bike)) UI.say(this, LINES.findCar.moved, this.player);
  }

  // ---- 多米诺：挪车时可能带倒同一排，返回有没有倒 ----
  domino(bike) {
    const C = CONFIG.findCar;
    const FALL_ANGLE = 80, FALL_SHIFT = 8;   // 倒下的角度、顺带往外滑的像素（纯画面）
    if (Math.random() >= C.dominoChance) return false;

    // 往远离自己车的方向，从被挪那辆的另一侧邻车开始；遇到挪开的 / 倒着的 / 排尾就停
    const dir = bike.getData('col') < this.myBike.getData('col') ? -1 : 1;
    const row = this.grid[bike.getData('row')];
    const chain = [];
    for (let c = bike.getData('col') + dir; c >= 0 && c < row.length && chain.length < C.dominoMax; c += dir) {
      const b = row[c];
      if (b.getData('moved') || b.getData('fallen')) break;
      chain.push(b);
    }
    if (!chain.length) return false;   // 被挪的车在排尾，没东西可倒

    // 先全部标记为倒下，再一辆接一辆播动画（节奏和车棚一致）
    chain.forEach((b, k) => {
      b.setData('fallen', true);
      this.time.delayedCall(k * CONFIG.findCar.dominoDelayMs, () => {
        if (!b.getData('fallen')) return;   // 还没倒就被扶起来了
        this.tweens.add({ targets: b, angle: dir * FALL_ANGLE, x: b.getData('x0') + dir * FALL_SHIFT,
          duration: 150, ease: 'Quad.In' });
      });
    });
    UI.sfx(this, 'fall');
    this.cameras.main.shake(120, 0.005);
    UI.say(this, LINES.park.domino, this.player);
    return true;
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

  // 扶起一辆：摆正、回到原位，花一点时间
  liftBike(b) {
    b.setData('fallen', false);
    this.tweens.killTweensOf(b);   // 正在倒的动画停掉
    this.tweens.add({ targets: b, angle: 0, x: b.getData('x0'), duration: 200 });
    GameState.clock += CONFIG.findCar.liftMinutes;
    UI.sfx(this, 'park');
    UI.say(this, this.hasFallen() ? LINES.park.lift : LINES.park.liftedAll, this.player);
  }

  unlock() {
    this.done = true;
    UI.hint(this, null);
    GameState.findCarMinutes = Math.round(GameState.clock - CONFIG.startClock);
    UI.sfx(this, 'park');
    UI.say(this, LINES.findCar.found, this.player);
    this.time.delayedCall(1000, () => UI.fadeTo(this, 'Node', { kind: 'gate' }));
  }
}
