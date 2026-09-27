// ===== 场景1 FindCar：宿舍楼下找车（B 负责）=====
// 规则见 项目说明.md 第 8 节。没有失败条件，时钟一直在走。
// 多米诺：挪开邻车时可能带倒同一排（往远离自己车的方向），全部扶起来才能解锁。
class FindCar extends Phaser.Scene {
  constructor() { super('FindCar'); }

  create() {
    UI.setup(this);
    const C = CONFIG.findCar;
    GameState.clock = CONFIG.startClock;

    // 背景按原始比例缩放；活动范围避开左侧宿舍楼和外围围栏。
    const W = C.world;
    this.physics.world.setBounds(W.left, W.top, W.right - W.left, W.bottom - W.top);
    this.cameras.main.setBounds(0, 0, W.width, W.height);
    this.add.image(0, 0, 'dorm').setOrigin(0).setDisplaySize(W.width, W.height);

    // ---- 车阵 ----
    this.bikes = this.physics.add.staticGroup();
    this.grid = [];
    const myRow = Phaser.Math.Between(0, C.rows - 1);
    const myCol = Phaser.Math.Between(1, C.cols - 2);   // 保证左右都有车夹着
    for (let r = 0; r < C.rows; r++) {
      this.grid[r] = [];
      for (let c = 0; c < C.cols; c++) {
        const mine = (r === myRow && c === myCol);
        const texture = mine ? 'dorm_bike' : 'dorm_bike_' + ((r * C.cols + c) % 7 + 1);
        const b = this.bikes.create(C.layout.left + c * C.layout.colGap,
          C.layout.top + r * C.layout.rowGap, texture);
        b.setDisplaySize(C.bike.width, C.bike.height).refreshBody();
        // 静态碰撞框用世界像素设置，不能沿用原 PNG 的 85×193。
        b.body.setSize(C.bike.bodyWidth, C.bike.bodyHeight);
        b.setDepth(b.y + C.bike.height / 2);
        b.setData({ mine, row: r, col: c, moved: false, fallen: false, x0: b.x });   // x0：扶起来时复原
        if (mine) this.myBike = b;
        this.grid[r][c] = b;
      }
    }
    this.neighbors = [this.grid[myRow][myCol - 1], this.grid[myRow][myCol + 1]];
    this.discovered = false;  // 是否已经确认这是自己的车
    this.movedCount = 0;
    this.bikeMarker = this.add.rectangle(this.myBike.x, this.myBike.y,
      C.bike.width + 8, C.bike.height + 8).setStrokeStyle(2, 0xfde047)
      .setDepth(this.myBike.depth + 1).setVisible(false);

    // ---- 主角 ----
    this.createWalkAnimations();
    this.walkFacing = 'right';
    this.rider = null;
    this.player = this.physics.add.sprite(C.spawn.x, C.spawn.y, 'player_walk_right_2');
    this.player.setOrigin(0.5, 1).setDisplaySize(C.person.width, C.person.height);
    this.player.setCollideWorldBounds(true);
    // 人物坐标在脚底；动态碰撞框必须换算回纹理像素。
    const bw = C.person.bodyWidth / this.player.scaleX;
    const bh = C.person.bodyHeight / this.player.scaleY;
    this.player.body.setSize(bw, bh).setOffset((this.player.width - bw) / 2, this.player.height - bh);
    this.player.setDepth(this.player.y);
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
    this.add.text(12, 510, LINES.findCar.controls, UI.style(14, '#ffffff', {
      backgroundColor: 'rgba(0,0,0,0.65)', padding: { x: 8, y: 3 }
    })).setScrollFactor(0).setDepth(1000);

    UI.say(this, isHungry() ? LINES.hungry : LINES.findCar.start, this.player);
    // 只提示背包在哪，不提醒要戴头盔
    this.bpTip = this.add.text(948, 90, LINES.findCar.backpackTip, UI.style(15, '#fde68a', {
      backgroundColor: 'rgba(0,0,0,0.6)', padding: { x: 8, y: 3 }
    })).setOrigin(1, 0).setScrollFactor(0).setDepth(1000);
  }

  update(time, delta) {
    const f = UI.pressedF(this);
    UI.tickClock(this, delta);
    UI.updateHud(this);
    if (UI.pressedE(this) && !this.done) {
      this.player.setVelocity(0);
      if (this.bpTip) { this.bpTip.destroy(); this.bpTip = null; }
      UI.backpack(this);
    }
    if (UI.blocked(this) || this.done) {
      this.player.setVelocity(0);
      this.updateWalkAnimation({ x: 0, y: 0 });
      return;
    }

    // ---- 移动（饿了走得慢）----
    const d = UI.dir(this);
    const v = new Phaser.Math.Vector2(d.x, d.y).normalize().scale(CONFIG.findCar.walkSpeed * speedMul());
    this.player.setVelocity(v.x, v.y);
    this.updateWalkAnimation(d);
    this.player.setDepth(this.player.y);

    // ---- 找车提示：越近滴得越快，信号格越多 ----
    const dist = Phaser.Math.Distance.BetweenPoints(this.player, this.myBike);
    const C = CONFIG.findCar;
    const level = Phaser.Math.Clamp(5 - Math.floor(dist / C.signalStep), 1, 5);
    this.signal.setText(LINES.findCar.signal + '▮'.repeat(level) + '▯'.repeat(5 - level));
    if (time > this.nextBeep) {
      UI.sfx(this, 'beep');
      this.nextBeep = time + Phaser.Math.Clamp(dist * C.beepDistanceFactor, C.beepMin, C.beepMax);
    }

    // ---- 旁边有倒着的车：优先扶起来 ----
    const down = this.nearestFallen(64);
    if (down) {
      UI.hint(this, LINES.park.liftHint);
      if (f) this.liftBike(down);
      return;
    }

    // ---- 找最近的车 ----
    const target = this.nearestBike(C.interactionRange);
    if (!target) { UI.hint(this, null); return; }

    const mine = target.getData('mine');
    const isNeighbor = this.neighbors.includes(target) && !target.getData('moved');
    if (mine && this.discovered && this.movedCount > 0) UI.hint(this, LINES.findCar.unlockHint);
    else if (isNeighbor && this.discovered) UI.hint(this, LINES.findCar.moveHint);
    else UI.hint(this, LINES.findCar.inspectHint);

    if (f) this.interact(target, mine, isNeighbor);
  }

  // 四个方向 × 有无头盔各一套走路动画（front 往下走，back 往上走）
  createWalkAnimations() {
    for (const facing of ['front', 'back', 'left', 'right']) {
      for (const tail of ['', '_helmet']) {
        const key = 'dorm_walk_' + facing + tail;
        if (this.anims.exists(key)) continue; // 第二天沿用已有动画
        if (tail && !UI.hasArt('player_walk_' + facing + '_1' + tail)) continue;
        this.anims.create({ key,
          frames: [1, 2, 3, 2].map(n => ({ key: 'player_walk_' + facing + '_' + n + tail })),
          frameRate: CONFIG.findCar.walkFrameRate, repeat: -1
        });
      }
    }
  }

  // 横向优先决定朝向；戴着头盔（且有图）就播戴头盔的那套
  updateWalkAnimation(d) {
    if (d.x) this.walkFacing = d.x < 0 ? 'left' : 'right';
    else if (d.y) this.walkFacing = d.y < 0 ? 'back' : 'front';
    const tail = GameState.helmetOn && this.anims.exists('dorm_walk_' + this.walkFacing + '_helmet') ? '_helmet' : '';
    if (d.x || d.y) this.player.anims.play('dorm_walk_' + this.walkFacing + tail, true);
    else {
      this.player.anims.stop();
      this.player.setTexture(UI.withHelmet('player_walk_' + this.walkFacing + '_2'));
    }
  }

  // 人物脚底到车身碰撞框边缘的距离，较长的车图也能从上下方交互。
  edgeDist(b) {
    const p = this.player.body.center, body = b.body;
    const dx = Math.max(body.left - p.x, 0, p.x - body.right);
    const dy = Math.max(body.top - p.y, 0, p.y - body.bottom);
    return Math.hypot(dx, dy);
  }

  // 找离主角最近、在 range 以内的车（挪开的、倒着的不算）
  nearestBike(range) {
    let best = null, bestD = range;
    this.bikes.getChildren().forEach(b => {
      if (b.getData('moved') || b.getData('fallen')) return;
      const dd = this.edgeDist(b);
      if (dd < bestD) { bestD = dd; best = b; }
    });
    return best;
  }

  interact(bike, mine, isNeighbor) {
    if (mine) {
      if (!this.discovered) {
        // 确认车辆后亮起边框，保持 protagonist 原图的尺寸和颜色。
        this.discovered = true;
        this.bikeMarker.setVisible(true);
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
    if (bike.getData('moved')) return;
    const C = CONFIG.findCar;
    UI.sfx(this, 'move_alarm');
    bike.setData('moved', true);
    this.physics.world.disable(bike);   // 不再挡路
    this.movedCount++;
    GameState.clock += CONFIG.findCar.moveCarMinutes;
    const dy = this.player.y > bike.y ? C.moveDistance : -C.moveDistance;
    this.tweens.add({ targets: bike, y: bike.y + dy,
      angle: Phaser.Math.Between(-C.moveAngle, C.moveAngle), duration: C.moveDuration,
      onUpdate: () => bike.setDepth(bike.y + C.bike.height / 2)
    });
    if (!this.domino(bike)) UI.say(this, LINES.findCar.moved, this.player);
  }

  // ---- 多米诺：挪车时可能带倒同一排，返回有没有倒 ----
  domino(bike) {
    const C = CONFIG.findCar;
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
      this.time.delayedCall(k * C.dominoDelayMs, () => {
        if (!b.getData('fallen')) return;   // 还没倒就被扶起来了
        this.tweens.add({ targets: b, angle: dir * C.fallAngle, x: b.getData('x0') + dir * C.fallShift,
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

  // 距离 range 以内最近的一辆倒着的车，没有返回 null
  nearestFallen(range) {
    let best = null, bestD = range;
    this.bikes.getChildren().forEach(b => {
      if (!b.getData('fallen')) return;
      const dd = this.edgeDist(b);
      if (dd < bestD) { best = b; bestD = dd; }
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
    if (this.done) return;
    this.done = true;
    const C = CONFIG.findCar;
    this.player.setVelocity(0).disableBody(true, true);
    this.myBike.disableBody(true, true);
    this.bikeMarker.setVisible(false);
    this.rider = this.add.image(this.myBike.x, this.myBike.y, UI.withHelmet('dorm_rider'))
      .setDisplaySize(C.rider.width, C.rider.height).setDepth(this.myBike.depth);
    this.cameras.main.startFollow(this.rider, true, 0.15, 0.15);
    UI.hint(this, null);
    GameState.findCarMinutes = Math.round(GameState.clock - CONFIG.startClock);
    UI.sfx(this, 'park');
    UI.say(this, LINES.findCar.found, this.rider);
    this.time.delayedCall(C.mountDuration, () => UI.fadeTo(this, 'Node', { kind: 'gate' }));
  }
}
