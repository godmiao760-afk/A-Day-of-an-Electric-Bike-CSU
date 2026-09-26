// ===== 素材清单（C 负责）=====
// 把图片放进 assets/img/，文件名 = key，例如 assets/img/bike.png
// 然后把 file 那一栏改成 true。没有图片的保持 false，游戏会自动用色块占位。
// 所有图片默认朝上（车头朝屏幕上方）。
const ASSETS = {
  images: {
    //  key            宽   高   占位色      有图片了吗
    player:       { w: 32, h: 32,  color: 0x3b82f6, file: false }, // 主角（步行）
    rider:        { w: 32, h: 56,  color: 0x2563eb, file: false }, // 主角骑车
    pusher:       { w: 40, h: 56,  color: 0x93c5fd, file: false }, // 主角推车
    bike:         { w: 24, h: 48,  color: 0xfacc15, file: false }, // 自己的车（停着）
    bike_other:   { w: 24, h: 48,  color: 0x9ca3af, file: false }, // 别人的车
    npc_delivery: { w: 32, h: 56,  color: 0xf97316, file: false }, // 外卖车
    npc_wrong:    { w: 32, h: 56,  color: 0xef4444, file: false }, // 逆行车
    npc_walker:   { w: 28, h: 28,  color: 0xa855f7, file: false }, // 行人
    npc_bus:      { w: 64, h: 140, color: 0x16a34a, file: false }, // 校车
    pile:         { w: 32, h: 40,  color: 0x06b6d4, file: false }, // 充电桩
    slot:         { w: 32, h: 60,  color: 0xffffff, file: false, outline: true }, // 空车位
    road:         { w: 64, h: 64,  color: 0x374151, file: false }, // 路面
    slope:        { w: 64, h: 64,  color: 0x92400e, file: false }, // 坡道
    grass:        { w: 64, h: 64,  color: 0x166534, file: false }, // 草地
    building:     { w: 64, h: 64,  color: 0x7f1d1d, file: false }  // 楼（宿舍/教学楼）
  },
  // 音效放进 assets/sfx/，mp3 格式。有了就改成 true。
  sounds: {
    beep: false,  // 找车滴滴
    hit:  false,  // 被撞
    fall: false,  // 摔倒
    park: false,  // 停好车
    plug: false   // 插上充电线
  }
};
