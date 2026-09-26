// ===== NodeScene：选择节点（校门口 / 中午 / 傍晚 共用）=====
// 用 UI.fadeTo(this, 'Node', { kind: 'gate' | 'noon' | 'evening' }) 进入。
// 纯菜单场景，不走时钟（时间在各选项里直接加）。
// 注意：类名叫 NodeScene（Node 和浏览器自带的全局对象重名），场景 key 仍是 'Node'。
class NodeScene extends Phaser.Scene {
  constructor() { super('Node'); }

  init(data) {
    this.kind = (data && data.kind) || 'gate';
  }

  create() {
    UI.setup(this);
    const titles = { gate: LINES.gate.title, noon: LINES.meals.noonTitle, evening: LINES.meals.eveningTitle };
    const bg = { gate: 0x1e293b, noon: 0x3f2d0f, evening: 0x2a1a3a }[this.kind];
    this.add.rectangle(0, 0, 960, 540, bg).setOrigin(0);
    this.add.text(480, 60, titles[this.kind], UI.style(34, '#fde68a')).setOrigin(0.5);
    UI.createClock(this);
    UI.createHud(this, false);

    // 等淡入结束再弹菜单
    this.time.delayedCall(350, () => {
      if (this.kind === 'gate') this.gate();
      else this.meal();
    });
  }

  update() {
    UI.tickClock(this, 0);   // 只刷新显示，不走时间
    UI.updateHud(this);
  }

  // ================= 校门口 =================
  gate() {
    const s = GameState;
    // 同学搭车：第一天必出现，之后按概率
    const ask = s.day === 1 || Math.random() < CONFIG.passenger.chance;
    if (ask) {
      UI.choice(this, LINES.passenger.ask, [LINES.passenger.yes, LINES.passenger.no], (i) => {
        if (i === 0) {
          s.passenger = true;
          this.go('outside', LINES.passenger.yes);   // 载人只能走校外
        } else {
          UI.say(this, LINES.passenger.no);
          this.time.delayedCall(600, () => this.pickRoute());
        }
      });
    } else {
      this.pickRoute();
    }
  }

  pickRoute() {
    UI.choice(this, LINES.gate.route + '\n（现在 ' + UI.fmt(GameState.clock) + '，8:00 上课）',
      [LINES.gate.inside, LINES.gate.outside, LINES.gate.backpack], (i) => {
        if (i === 0) this.go('inside');
        else if (i === 1) this.go('outside');
        else UI.backpack(this, () => this.pickRoute());   // 看完背包回来继续选
      });
  }

  go(route, text) {
    GameState.route = route;
    UI.say(this, text || (route === 'inside' ? LINES.gate.goInside : LINES.gate.goOutside));
    this.time.delayedCall(800, () => UI.fadeTo(this, 'Ride'));
  }

  // ================= 中午 / 傍晚 =================
  meal() {
    const s = GameState, P = CONFIG.places, M = LINES.meals;
    const opts = [];
    // 加一个选项；cost 不够或 ok 为 false 时置灰
    const add = (id, label, cost, ok = true, note = '') => {
      const noMoney = cost > 0 && s.money < cost;
      opts.push({
        id,
        label: label + (cost ? '　¥' + cost : '') + (noMoney ? M.noMoney : !ok ? note : ''),
        disabled: noMoney || !ok
      });
    };
    add('canteen', M.canteen + '（+' + P.canteen.food + ' 饱）', P.canteen.cost);
    add('houhu', M.houhu + '（+' + P.houhu.food + ' 饱，耗电 ' + P.houhu.battery + '%）', P.houhu.cost,
      s.battery >= P.houhu.battery, M.noBattery);
    if (this.kind === 'noon' && !s.items.license) add('license', M.license, P.license.cost);
    add('skip', M.skip, 0);
    opts.push({ id: 'backpack', label: LINES.gate.backpack });

    UI.choice(this, M.question + '（饥饿 ' + Math.round(s.hunger) + '/100）', opts, (i) => {
      const id = opts[i].id;
      if (id === 'backpack') { UI.backpack(this, () => this.meal()); return; }
      if (id === 'canteen') {
        spend(P.canteen.cost); eat(P.canteen.food); s.meals.push('食堂');
        UI.sfx(this, 'coin');
        this.finish(M.ateCanteen);
      } else if (id === 'houhu') {
        this.houhu();
      } else if (id === 'license') {
        spend(P.license.cost); s.items.license = true;
        UI.sfx(this, 'coin');
        this.finish(M.gotLicense);
      } else {
        this.finish(M.skipped);
      }
    });
  }

  // 去后湖：要出校门，耗电，今天有交警就会被查
  houhu() {
    const s = GameState, P = CONFIG.places;
    s.battery = Math.max(0, s.battery - P.houhu.battery);
    const eatThere = () => {
      spend(P.houhu.cost); eat(P.houhu.food); s.meals.push('后湖');
      UI.sfx(this, 'coin');
      this.finish(LINES.meals.ateHouhu);
    };
    if (s.policeToday && Math.random() < CONFIG.police.encounterChance) {   // 每次单独掷一次是否碰上交警
      UI.sfx(this, 'whistle');
      const r = policeCheck(false);
      UI.updateHud(this);
      UI.alert(this, LINES.police.houhu + '\n\n' + policeText(r), () => {
        // 罚完钱还够不够吃
        if (s.money >= P.houhu.cost) eatThere();
        else this.finish(LINES.meals.fineNoFood);
      });
    } else {
      eatThere();
    }
  }

  finish(text) {
    UI.updateHud(this);
    UI.say(this, text);
    // 中午 → 下午课；傍晚 → 晚上充电
    const nextKey = this.kind === 'noon' ? 'Class' : 'Charge';
    const data = this.kind === 'noon' ? { part: 'afternoon' } : undefined;
    this.time.delayedCall(1400, () => UI.fadeTo(this, nextKey, data));
  }
}
