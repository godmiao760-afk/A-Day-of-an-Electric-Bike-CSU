# 小电驴的一天

中南大学电动车骑行困境 · 黑客松作品（Phaser 3，网页版）

## 怎么运行

1. VS Code 安装 **Live Server** 插件
2. 用 VS Code 打开本文件夹，右键 `index.html` → **Open with Live Server**
3. 浏览器自动打开，点一下画面，按 F 开始

> 不能直接双击 index.html 打开，素材会加载失败。
> 出问题按 **F12** 看控制台（Console）的红字报错，整段复制给 AI。

## 操作

| 按键 | 作用 |
|---|---|
| W A S D | 移动 |
| F | 交互 / 确认 / 扶车 |
| E | 背包（骑车时不能开） |

## 各自改哪里

| 人 | 文件 |
|---|---|
| A | `src/ui.js` `src/state.js` `src/scenes/Ride.js` `NodeScene.js` `Intro/Class/Result.js` |
| B | `src/scenes/FindCar.js` `Park.js` `Charge.js` |
| C | `assets/img/`、`assets/sfx/`、`src/assets.js` |
| D | `src/config.js`（数值）、`src/lines.js`（文案） |

详细约定见 **CLAUDE.md**，让 AI 干活前先让它读这个文件。
所有事件的触发条件、数值和随机概率见 **事件流程.md**。

## 调试

`src/main.js` 里把 `DEBUG_START` 改成 `'Ride'` / `'Park'` / `'Charge'` / `'Result'`，刷新后直接从该场景开始。**演示前改回 `null`。**
