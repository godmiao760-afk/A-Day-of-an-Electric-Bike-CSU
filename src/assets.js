// ===== 素材清单（C 负责）=====
// 把图片放进 assets/img/，文件名 = key，例如 assets/img/bike.png
// 然后把 file 那一栏改成 true。没有图片的保持 false，游戏会自动用色块占位。
// 子目录用 path 指定相对路径；w/h 是占位尺寸，crop 可去除透明留白。
// 所有图片默认朝上（车头朝屏幕上方）。
const ASSETS = {
  images: {
    //  key            宽   高   占位色      有图片了吗
    dorm:         { w: 1536, h: 1024, color: 0x365a32, file: true,
      path: 'assets/img/background/dorm.png' }, // 宿舍车棚背景
    player:       { w: 32, h: 32,  color: 0x3b82f6, file: false }, // 其他场景的步行占位图
    // 动画占位帧与原图保持同尺寸，缺少某一帧时也不会跳变缩放。
    player_walk_right_1: { w: 342, h: 512, color: 0x3b82f6, file: true,
      path: 'assets/img/character/player_walk_frames/walk_right_01.png' },
    player_walk_right_2: { w: 342, h: 512, color: 0x3b82f6, file: true,
      path: 'assets/img/character/player_walk_frames/walk_right_02.png' },
    player_walk_right_3: { w: 342, h: 512, color: 0x3b82f6, file: true,
      path: 'assets/img/character/player_walk_frames/walk_right_03.png' },
    player_walk_left_1: { w: 342, h: 512, color: 0x3b82f6, file: true,
      path: 'assets/img/character/player_walk_frames/walk_left_01.png' },
    player_walk_left_2: { w: 342, h: 512, color: 0x3b82f6, file: true,
      path: 'assets/img/character/player_walk_frames/walk_left_02.png' },
    player_walk_left_3: { w: 342, h: 512, color: 0x3b82f6, file: true,
      path: 'assets/img/character/player_walk_frames/walk_left_03.png' },
    dorm_rider:   { w: 36, h: 84, color: 0x2563eb, file: true,
      path: 'assets/img/character/riding/driving.png',
      crop: { x: 321, y: 47, w: 373, h: 877 } }, // 找车场景上车表现
    rider:        { w: 32, h: 56, color: 0x2563eb, file: false },
    pusher:       { w: 40, h: 56,  color: 0x93c5fd, file: false }, // 主角推车
    bike:         { w: 24, h: 48, color: 0xfacc15, file: false },
    bike_other:   { w: 24, h: 48, color: 0x9ca3af, file: false },
    dorm_bike:    { w: 34, h: 78, color: 0xfacc15, file: true,
      path: 'assets/img/vehical/protagonist.png' }, // 主角的车
    dorm_bike_1: { w: 34, h: 78, color: 0x9ca3af, file: true,
      path: 'assets/img/vehical/1.png' },
    dorm_bike_2: { w: 34, h: 78, color: 0x9ca3af, file: true,
      path: 'assets/img/vehical/2.png' },
    dorm_bike_3: { w: 34, h: 78, color: 0x9ca3af, file: true,
      path: 'assets/img/vehical/3.png' },
    dorm_bike_4: { w: 34, h: 78, color: 0x9ca3af, file: true,
      path: 'assets/img/vehical/4.png' },
    dorm_bike_5: { w: 34, h: 78, color: 0x9ca3af, file: true,
      path: 'assets/img/vehical/5.png' },
    dorm_bike_6: { w: 34, h: 78, color: 0x9ca3af, file: true,
      path: 'assets/img/vehical/6.png' },
    dorm_bike_7: { w: 34, h: 78, color: 0x9ca3af, file: true,
      path: 'assets/img/vehical/7.png' },
    npc_delivery: { w: 32, h: 56,  color: 0xf97316, file: false }, // 外卖车
    npc_wrong:    { w: 32, h: 56,  color: 0xef4444, file: false }, // 逆行车
    npc_walker:   { w: 28, h: 28,  color: 0xa855f7, file: false }, // 行人
    npc_bus:      { w: 64, h: 140, color: 0x16a34a, file: false }, // 校车
    pile:         { w: 32, h: 40,  color: 0x06b6d4, file: false }, // 充电桩
    slot:         { w: 32, h: 60,  color: 0xffffff, file: false, outline: true }, // 空车位
    road:         { w: 64, h: 64,  color: 0x374151, file: false }, // 路面
    slope:        { w: 64, h: 64,  color: 0x92400e, file: false }, // 坡道
    grass:        { w: 64, h: 64,  color: 0x166534, file: false }, // 草地
    building:     { w: 64, h: 64,  color: 0x7f1d1d, file: false }, // 楼（宿舍/教学楼）
    rider_carry:  { w: 32, h: 64,  color: 0x1d4ed8, file: false }, // 主角骑车载人
    npc_car:      { w: 56, h: 100, color: 0x64748b, file: false }, // 汽车（校外）
    police:       { w: 32, h: 32,  color: 0x1e3a8a, file: false }, // 交警
    barrier:      { w: 400, h: 16, color: 0xdc2626, file: false }, // 检查点路障
    // v2 结局图（Ending 场景，320×240）
    end_perfect:  { w: 320, h: 240, color: 0x16a34a, file: false }, // 完美：欢呼
    end_pass:     { w: 320, h: 240, color: 0x2563eb, file: false }, // 合格
    end_fail:     { w: 320, h: 240, color: 0x6b7280, file: false }, // 不合格：垂头丧气
    end_police:   { w: 320, h: 240, color: 0x1e3a8a, file: false }, // 派出所
    end_faint:    { w: 320, h: 240, color: 0x7c2d12, file: false }, // 昏倒
    end_broke:    { w: 320, h: 240, color: 0x991b1b, file: false }  // 跪地嚎啕大哭
  },
  // 音效放进 assets/sfx/，mp3 格式。有了就改成 true。
  sounds: {
    beep: false,  // 找车滴滴
    hit:  false,  // 被撞
    fall: false,  // 摔倒
    park: false,  // 停好车
    plug: false,  // 插上充电线
    whistle: false, // 交警哨声
    coin: false     // 花钱 / 收钱
  }
};
