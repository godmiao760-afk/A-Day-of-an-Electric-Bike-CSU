// ===== Result：结算页（A 负责）=====
class Result extends Phaser.Scene {
  constructor() { super('Result'); }

  create() {
    UI.setup(this);
    const s = GameState;
    const charged = isCharged();
    const key = getEndingKey();
    const title = LINES.endings[key];
    const color = { ontime_charged: '#86efac', ontime_empty: '#fde68a',
                    late_charged: '#93c5fd', late_empty: '#f87171' }[key];

    const chargeText = {
      none: '没充上', noMoney: '没钱充电', watch: '守着充', full: '回宿舍，充满了', unplugged: '回宿舍，被拔线'
    }[s.chargeResult];
    const fineTotal = s.fines.reduce((a, f) => a + f.amount, 0);
    const fineText = s.fines.length
      ? '¥' + fineTotal + '（' + s.fines.map(f => f.reason).join('、') + '）'
      : '无';

    this.add.text(480, 40, '第 ' + s.day + ' 天 · 结算', UI.style(20, '#9ca3af')).setOrigin(0.5);
    const t = this.add.text(480, 90, '「' + title + '」', UI.style(40, color)).setOrigin(0.5).setScale(0.6);
    this.tweens.add({ targets: t, scale: 1, duration: 400, ease: 'Back.Out' });

    const rows = [
      ['路线', s.route === 'outside' ? '校外' : '校内'],
      ['找车用时', s.findCarMinutes + ' 分钟'],
      ['停好车时间', s.arriveClock != null ? UI.fmt(s.arriveClock) + (s.late ? '（迟到）' : '（准时）') : '—'],
      ['被撞 / 摔倒', s.hits + ' 次 / ' + s.falls + ' 次'],
      ['罚款', fineText],
      ['载人收入 / 花销', '+¥' + s.earned + ' / -¥' + s.spent],
      ['今天吃了', s.meals.length ? s.meals.join('、') : '什么都没吃'],
      ['今晚充电', chargeText + '（' + (s.chargeGain >= 0 ? '+' : '') + s.chargeGain + '%）'],
      ['明早电量', Math.round(s.battery) + '%' + (charged ? '' : '　⚠ 可能撑不到教学楼')],
      ['余额', s.money < 0 ? '欠 ¥' + (-s.money) : '¥' + s.money]
    ];
    rows.forEach((r, i) => {
      this.add.text(290, 140 + i * 31, r[0], UI.style(18, '#9ca3af'));
      this.add.text(460, 140 + i * 31, r[1], UI.style(18, i === 4 && s.fines.length ? '#fca5a5' : '#ffffff'));
    });

    const tip = this.add.text(480, 505, '按 F 开始第 ' + (s.day + 1) + ' 天　　按 R 重新开始',
      UI.style(20)).setOrigin(0.5);
    this.tweens.add({ targets: tip, alpha: 0.4, duration: 700, yoyo: true, repeat: -1 });

    this.ready = false;
    this.time.delayedCall(800, () => { this.ready = true; });
  }

  update() {
    const f = UI.pressedF(this);
    const r = Phaser.Input.Keyboard.JustDown(this.keys.R);
    if (!this.ready || this._leaving) return;
    if (f) { nextDay(); UI.fadeTo(this, 'Intro'); }
    else if (r) { newGame(); UI.fadeTo(this, 'Intro'); }
  }
}
