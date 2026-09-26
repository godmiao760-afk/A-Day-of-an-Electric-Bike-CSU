// ===== 启动游戏（A 负责，最后加载）=====

// 调试：改成场景名就能直接从该场景开始，例如 'Node'、'Ride'、'Park'、'Class'、'Charge'、'Result'、'Ending'
// 正式演示前改回 null！
const DEBUG_START = null;
// 各场景的参数：
//   Node   { kind: 'gate' | 'noon' | 'evening' }
//   Park   { pushing: true }        测推车
//   Class  { part: 'morning' | 'afternoon' }
//   Ending { key: 'perfect' | 'pass' | 'fail' | 'police' | 'faint' | 'broke' }
const DEBUG_DATA = {};
// 调试时想改初始状态，在这里改，例如 { route: 'outside', passenger: true, helmetOn: false }
// 测最终结局：{ day: 5, lateCount: 3 }
const DEBUG_STATE = {};

// 场景注册表：所有可进入的 Phaser 场景集中声明，便于检查流程和调试入口。
const GAME_SCENES = [
  Boot, Intro, FindCar, NodeScene, Ride, Park, Class, Charge, Result, Ending
];

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
  scene: GAME_SCENES
});
