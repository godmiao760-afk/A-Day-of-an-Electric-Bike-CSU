// ===== 场景1 FindCar：宿舍楼下找车（B 负责）=====
// 规则见 项目说明.md 第 8 节。没有失败条件，时钟一直在走。
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
        b.setData({ mine, row: r, col: c, moved: false });
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

  createWalkAnimations() {
    for (const facing of ['left', 'right']) {
      const key = 'dorm_walk_' + facing;
      if (this.anims.exists(key)) continue; // 第二天沿用已有动画
      this.anims.create({ key,
        frames: [1, 2, 3, 2].map(n => ({ key: 'player_walk_' + facing + '_' + n })),
        frameRate: CONFIG.findCar.walkFrameRate, repeat: -1
      });
    }
  }

  updateWalkAnimation(d) {
    if (d.x) this.walkFacing = d.x < 0 ? 'left' : 'right';
    if (d.x || d.y) this.player.anims.play('dorm_walk_' + this.walkFacing, true);
    else {
      this.player.anims.stop();
      this.player.setTexture('player_walk_' + this.walkFacing + '_2');
    }
  }

  // 以人物脚底和车身边缘计算距离，较长的车图也能从上下方交互。
  nearestBike(range) {
    let best = null, bestD = range;
    this.bikes.getChildren().forEach(b => {
      if (b.getData('moved')) return;
      const p = this.player.body.center, body = b.body;
      const dx = Math.max(body.left - p.x, 0, p.x - body.right);
      const dy = Math.max(body.top - p.y, 0, p.y - body.bottom);
      const dd = Math.hypot(dx, dy);
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
    bike.setData('moved', true);
    this.physics.world.disable(bike);   // 不再挡路
    this.movedCount++;
    GameState.clock += CONFIG.findCar.moveCarMinutes;
    const dy = this.player.y > bike.y ? C.moveDistance : -C.moveDistance;
    this.tweens.add({ targets: bike, y: bike.y + dy,
      angle: Phaser.Math.Between(-C.moveAngle, C.moveAngle), duration: C.moveDuration,
      onUpdate: () => bike.setDepth(bike.y + C.bike.height / 2)
    });
    UI.say(this, LINES.findCar.moved, this.player);
  }

  unlock() {
    if (this.done) return;
    this.done = true;
    const C = CONFIG.findCar;
    this.player.setVelocity(0).disableBody(true, true);
    this.myBike.disableBody(true, true);
    this.bikeMarker.setVisible(false);
    const frame = this.textures.get('dorm_rider').has('trimmed') ? 'trimmed' : undefined;
    this.rider = this.add.image(this.myBike.x, this.myBike.y, 'dorm_rider', frame)
      .setDisplaySize(C.rider.width, C.rider.height).setDepth(this.myBike.depth);
    this.cameras.main.startFollow(this.rider, true, 0.15, 0.15);
    UI.hint(this, null);
    GameState.findCarMinutes = Math.round(GameState.clock - CONFIG.startClock);
    UI.sfx(this, 'park');
    UI.say(this, LINES.findCar.found, this.rider);
    this.time.delayedCall(C.mountDuration, () => UI.fadeTo(this, 'Node', { kind: 'gate' }));
  }
}
