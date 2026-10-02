// ===== Result：结算页 · 今日评价（A 负责）=====
// 每天的评价不影响最终结局；最后一天下午课结束直接进 Ending，不会走到这里。
class Result extends Phaser.Scene {
  constructor() { super('Result'); }

  create() {
    UI.setup(this);
    const s = GameState;
    const charged = isCharged();
    const key = getEndingKey();
    const title = LINES.endings[key];
    const color = { ontime_charged: '#f5f4dc', ontime_empty: '#e7d58f',
                    late_charged: '#c5ded4', late_empty: '#f0b595' }[key];

    const chargeText = {
      none: '没充上', noMoney: '没钱充电', full: '回宿舍，充满了', unplugged: '回宿舍，被拔线'
    }[s.chargeResult];
    const fineTotal = s.fines.reduce((a, f) => a + f.amount, 0);
    const fineText = s.fines.length
      ? '¥' + fineTotal + '（' + s.fines.map(f => f.reason).join('、') + '）'
      : '无';

    const rows = [
      ['路线', s.route === 'outside' ? '校外' : '校内'],
      ['找车用时', s.findCarMinutes + ' 分钟'],
      ['停好车时间', s.arriveClock != null ? UI.fmt(s.arriveClock) + (s.late ? '（迟到）' : '（准时）') : '—'],
      ['下午', s.latePM ? '迟到' : '准时'],
      ['累计迟到', s.lateCount + ' 次'],
      ['被撞 / 摔倒', s.hits + ' 次 / ' + s.falls + ' 次'],
      ['罚款', fineText],
      ['载人收入 / 花销', '+¥' + s.earned + ' / -¥' + s.spent],
      ['今天吃了', s.meals.length ? s.meals.join('、') : '什么都没吃'],
      ['今晚充电', chargeText + '（' + (s.chargeGain >= 0 ? '+' : '') + s.chargeGain + '%）'],
      ['明早电量', Math.round(s.battery) + '%' + (charged ? '' : '　⚠ 可能撑不到教学楼')],
      ['余额', s.money < 0 ? '欠 ¥' + (-s.money) : '¥' + s.money]
    ];
    this._dailyDetails = false;
    DailyUI.result(this, title, color, rows,
      () => this.continueDay(), () => this.restartGame());

    this.ready = false;
    this.time.delayedCall(800, () => { this.ready = true; });
  }

  canContinue() {
    return this.ready && !UI.blocked(this) && !this._dailyDetails && this.time.now >= UI.lockUntil;
  }

  continueDay() {
    if (!this.canContinue()) return;
    // nextDay() 会把 chargeResult 重置成 'none'，先记下，第二天早上揭晓。
    const cr = GameState.chargeResult;
    nextDay();
    UI.fadeTo(this, 'Intro', { lastCharge: cr });
  }

  restartGame() {
    if (!this.canContinue()) return;
    newGame();
    UI.fadeTo(this, 'Intro');
  }

  update() {
    const f = UI.pressedF(this);
    const r = Phaser.Input.Keyboard.JustDown(this.keys.R);
    if (!this.canContinue()) return;
    if (f) this.continueDay();
    else if (r) this.restartGame();
  }
}
