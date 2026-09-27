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
    // 校门口有真图：交警路口背景（按宽铺满、竖直居中），压暗一点让标题清楚
    if (this.kind === 'gate' && UI.hasArt('bg_traffic')) {
      this.add.image(480, 270, 'bg_traffic').setDisplaySize(960, 640);
      this.add.rectangle(0, 0, 960, 540, 0x000000, 0.35).setOrigin(0);
    }
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
    // 早高峰单行道：两条路线各掷一次，在这里掷好才能透露给玩家，再传给 Ride
    const W = CONFIG.ride.oneWay.chance;
    this.oneWay = { inside: Math.random() < W, outside: Math.random() < W };
    // 同学搭车：第一天必出现，之后按概率
    const ask = s.day === 1 || Math.random() < CONFIG.passenger.chance;
    if (ask) {
      // 载人只能走校外，校外堵的话也提一句
      const q = LINES.passenger.ask + (this.oneWay.outside ? '\n' + LINES.gate.rumorOutside : '');
      UI.choice(this, q, [LINES.passenger.yes, LINES.passenger.no], (i) => {
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
    const G = LINES.gate;
    // 哪条路堵就透露一句（都堵就两句都加）
    const rumor = (this.oneWay.inside ? '\n' + G.rumorInside : '') + (this.oneWay.outside ? '\n' + G.rumorOutside : '');
    UI.choice(this, G.route + '\n（现在 ' + UI.fmt(GameState.clock) + '，8:00 上课）' + rumor,
      [G.inside, G.outside, G.backpack], (i) => {
        if (i === 0) this.go('inside');
        else if (i === 1) this.go('outside');
        else UI.backpack(this, () => this.pickRoute());   // 看完背包回来继续选
      });
  }

  go(route, text) {
    GameState.route = route;
    UI.say(this, text || (route === 'inside' ? LINES.gate.goInside : LINES.gate.goOutside));
    // 今天这条路堵不堵，通过 data 传给 Ride
    this.time.delayedCall(800, () => UI.fadeTo(this, 'Ride', { oneWay: this.oneWay[route] }));
  }

  // ================= 中午 / 傍晚 =================
  meal() {
    const s = GameState, P = CONFIG.places, M = LINES.meals;
    const opts = [];
    // 大概花多久：取 minutes 区间平均值，"约 50 分钟"
    const takes = (p) => '　' + M.takes.replace('{m}', Math.round((p.minutes[0] + p.minutes[1]) / 2));
    // 加一个选项；detail 是括号里的说明；cost 不够或 ok 为 false 时置灰。
    // 花完钱 ≤ 0 时提醒（不置灰，让玩家自己选）。竖排按钮固定 520 宽，超出会被裁掉，所以：
    // 置灰的不显示时间；"买完就身无分文"的选了就进结局，也省掉说明和时间
    const add = (id, name, detail, cost, ok = true, note = '') => {
      const noMoney = cost > 0 && s.money < cost;
      const last = cost > 0 && !noMoney && ok && s.money - cost <= 0;
      const showTime = P[id] && !noMoney && ok && !last;
      opts.push({
        id,
        label: name + (last ? '' : detail) + (cost ? '　¥' + cost : '') + (showTime ? takes(P[id]) : '') +
          (noMoney ? M.noMoney : !ok ? note : last ? M.lastMoney : ''),
        disabled: noMoney || !ok
      });
    };
    add('canteen', M.canteen, '（+' + P.canteen.food + ' 饱）', P.canteen.cost);
    add('houhu', M.houhu, '（+' + P.houhu.food + ' 饱，耗电 ' + P.houhu.battery + '%）', P.houhu.cost,
      s.battery >= P.houhu.battery, M.noBattery);
    if (this.kind === 'noon' && !s.items.license) add('license', M.license, '', P.license.cost);
    add('skip', M.skip, '', 0);   // 不吃：不花时间
    opts.push({ id: 'backpack', label: LINES.gate.backpack });

    UI.choice(this, M.question + '（饥饿 ' + Math.round(s.hunger) + '/100）', opts, (i) => {
      const id = opts[i].id;
      if (id === 'backpack') { UI.backpack(this, () => this.meal()); return; }
      // 每个选项都花时间（中午花完晚于 14:00 下午就迟到）；不吃 = 0
      if (P[id]) s.clock += Phaser.Math.Between(P[id].minutes[0], P[id].minutes[1]);
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

  // 去后湖：要出校门，耗电，今天有交警就可能碰上（停车受检 / 硬闯）
  houhu() {
    const s = GameState, P = CONFIG.places, L = LINES.police;
    s.battery = Math.max(0, s.battery - P.houhu.battery);
    // extra：吃完那句后面再补一句（硬闯成功的预兆）
    const eatThere = (extra) => {
      spend(P.houhu.cost); eat(P.houhu.food); s.meals.push('后湖');
      UI.sfx(this, 'coin');
      this.finish(extra ? UI.rand(LINES.meals.ateHouhu) + '\n' + extra : LINES.meals.ateHouhu);
    };
    if (s.policeToday && Math.random() < CONFIG.police.encounterChance) {   // 每次单独掷一次是否碰上交警
      UI.choice(this, L.askStop, [L.optStop, L.optRun], (i) => {
        UI.sfx(this, 'whistle');
        if (i === 0) {
          // 停车受检：和原来一样
          const r = policeCheck(false);
          UI.updateHud(this);
          UI.alert(this, L.houhu + '\n\n' + policeText(r), () => {
            // 罚完钱还够不够吃
            if (s.money >= P.houhu.cost) eatThere();
            else this.finish(LINES.meals.fineNoFood);
          });
        } else if (!tryRun()) {
          // 硬闯被抓 → 隐藏结局「派出所」
          UI.fadeTo(this, 'Ending', { key: 'police' });
        } else {
          // 闯过去了：不罚款、不耽误时间（runs 已在 tryRun 里 +1）
          UI.say(this, L.runOk);
          this.time.delayedCall(1200, () => eatThere(L.runOmen));
        }
      });
    } else {
      eatThere();
    }
  }

  finish(text) {
    UI.updateHud(this);
    UI.say(this, text);
    // 先让独白显示再切场景：钱花光 → 隐藏结局；中午 → 下午课；傍晚 → 晚上充电
    const k = hiddenEndingKey();
    const nextKey = k ? 'Ending' : this.kind === 'noon' ? 'Class' : 'Charge';
    const data = k ? { key: k } : this.kind === 'noon' ? { part: 'afternoon' } : undefined;
    this.time.delayedCall(1400, () => UI.fadeTo(this, nextKey, data));
  }
}
