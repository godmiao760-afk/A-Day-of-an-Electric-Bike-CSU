// ===== 启动游戏（A 负责，最后加载）=====

// 调试：改成场景名就能直接从该场景开始，例如 'Ride'、'Park'、'Charge'、'Result'
// 正式演示前改回 null！
const DEBUG_START = null;
// Park 场景可以传 { pushing: true } 测试推车
const DEBUG_DATA = {};

const game = new Phaser.Game({
  type: Phaser.AUTO,
  parent: 'game',
  width: 960,
  height: 540,
  backgroundColor: '#111111',
  pixelArt: false,   // 用像素风素材时改成 true（中文字会变糊，需要把字号调大）
  physics: {
    default: 'arcade',
    arcade: { gravity: { x: 0, y: 0 }, debug: false }  // debug 改 true 可以看到碰撞框
  },
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  scene: [Boot, Intro, FindCar, Ride, Park, Class, Charge, Result]
});
