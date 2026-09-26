// ===== Result：结算页（A 负责）=====
class Result extends Phaser.Scene {
  constructor() { super('Result'); }

  create() {
    UI.setup(this);
    const s = GameState;
    const charged = s.battery >= CONFIG.chargedThreshold;
    const key = (s.late ? 'late' : 'ontime') + '_' + (charged ? 'charged' : 'empty');
    const title = LINES.endings[key];
    const color = { ontime_charged: '#86efac', ontime_empty: '#fde68a',
                    late_charged: '#93c5fd', late_empty: '#f87171' }[key];

    const chargeText = {
      none: '没充上', watch: '守着充', full: '回宿舍，充满了', unplugged: '回宿舍，被拔线'
    }[s.chargeResult];

    this.add.text(480, 60, '第 ' + s.day + ' 天 · 结算', UI.style(22, '#9ca3af')).setOrigin(0.5);
    const t = this.add.text(480, 120, '「' + title + '」', UI.style(44, color)).setOrigin(0.5).setScale(0.6);
    this.tweens.add({ targets: t, scale: 1, duration: 400, ease: 'Back.Out' });

    const rows = [
      ['找车用时', s.findCarMinutes + ' 分钟'],
      ['停好车时间', s.arriveClock != null ? UI.fmt(s.arriveClock) + (s.late ? '（迟到）' : '（准时）') : '—'],
      ['被撞次数', s.hits + ' 次'],
      ['摔倒次数', s.falls + ' 次'],
      ['今晚充电', chargeText + '（' + (s.chargeGain >= 0 ? '+' : '') + s.chargeGain + '%）'],
      ['明早电量', Math.round(s.battery) + '%' + (charged ? '' : '　⚠ 可能撑不到教学楼')]
    ];
    rows.forEach((r, i) => {
      this.add.text(330, 200 + i * 40, r[0], UI.style(20, '#9ca3af'));
      this.add.text(500, 200 + i * 40, r[1], UI.style(20, '#ffffff'));
    });

    const tip = this.add.text(480, 480, '按 F 开始第 ' + (s.day + 1) + ' 天　　按 R 重新开始',
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
