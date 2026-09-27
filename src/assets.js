// ===== 素材清单（C 负责）=====
// 把图片放进 assets/img/，文件名 = key，例如 assets/img/bike.png
// 然后把 file 那一栏改成 true。没有图片的保持 false，游戏会自动用色块占位。
// 子目录用 path 指定相对路径；w/h 是占位尺寸，crop 可去除透明留白。
// 美术原图比占位大很多，实际显示尺寸由场景按 CONFIG 缩放。
// 带 _helmet 的是戴头盔版本，场景用 UI.withHelmet() 按 GameState.helmetOn 自动切换。
// 所有图片默认朝上（车头朝屏幕上方）。
const ASSETS = {
  images: {
    //  key            宽   高   占位色      有图片了吗
    dorm:         { w: 1536, h: 1024, color: 0x365a32, file: true,
      path: 'assets/img/background/dorm.png' }, // 宿舍车棚背景
    player:       { w: 32, h: 32,  color: 0x3b82f6, file: false }, // 其他场景的步行占位图
    // 找车步行：前 / 后 / 左 / 右各 3 帧（342×512），另有戴头盔版。占位帧与原图同尺寸，缺帧时不会跳变缩放。
    player_walk_front_1: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_front_01.png' },
    player_walk_front_2: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_front_02.png' },
    player_walk_front_3: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_front_03.png' },
    player_walk_back_1:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_back_01.png' },
    player_walk_back_2:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_back_02.png' },
    player_walk_back_3:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_back_03.png' },
    player_walk_left_1:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_left_01.png' },
    player_walk_left_2:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_left_02.png' },
    player_walk_left_3:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_left_03.png' },
    player_walk_right_1: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_right_01.png' },
    player_walk_right_2: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_right_02.png' },
    player_walk_right_3: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_right_03.png' },
    player_walk_front_1_helmet: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_front_01_helmet.png' },
    player_walk_front_2_helmet: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_front_02_helmet.png' },
    player_walk_front_3_helmet: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_front_03_helmet.png' },
    player_walk_back_1_helmet:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_back_01_helmet.png' },
    player_walk_back_2_helmet:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_back_02_helmet.png' },
    player_walk_back_3_helmet:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_back_03_helmet.png' },
    player_walk_left_1_helmet:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_left_01_helmet.png' },
    player_walk_left_2_helmet:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_left_02_helmet.png' },
    player_walk_left_3_helmet:  { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_left_03_helmet.png' },
    player_walk_right_1_helmet: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_right_01_helmet.png' },
    player_walk_right_2_helmet: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_right_02_helmet.png' },
    player_walk_right_3_helmet: { w: 342, h: 512, color: 0x3b82f6, file: true, path: 'assets/img/character/player_walk_frames/walk_right_03_helmet.png' },
    // 骑车主角（俯视，1024×1024，crop 去掉透明留白）：骑行、车棚骑车、找车上车
    dorm_rider:   { w: 36, h: 84, color: 0x2563eb, file: true,
      path: 'assets/img/character/riding/driving.png', crop: { x: 321, y: 47, w: 373, h: 877 } }, // 找车场景上车表现
    dorm_rider_helmet: { w: 36, h: 84, color: 0x2563eb, file: true,
      path: 'assets/img/character/riding/driving_helmet.png', crop: { x: 321, y: 47, w: 373, h: 877 } },
    rider:        { w: 36, h: 84, color: 0x2563eb, file: true,
      path: 'assets/img/character/riding/driving.png', crop: { x: 321, y: 47, w: 373, h: 877 } },
    rider_helmet: { w: 36, h: 84, color: 0x2563eb, file: true,
      path: 'assets/img/character/riding/driving_helmet.png', crop: { x: 321, y: 47, w: 373, h: 877 } },
    // 骑行摔倒（1024×1024）：先趴在地上（hurt），再站起来看着倒地的车（stand）
    fall_hurt:         { w: 128, h: 128, color: 0x2563eb, file: true, path: 'assets/img/character/riding/rider-fallen_hurt.png' },
    fall_hurt_helmet:  { w: 128, h: 128, color: 0x2563eb, file: true, path: 'assets/img/character/riding/rider-fallen_hurt_helmet.png' },
    fall_stand:        { w: 128, h: 128, color: 0x2563eb, file: true, path: 'assets/img/character/riding/ride_fallen.png' },
    fall_stand_helmet: { w: 128, h: 128, color: 0x2563eb, file: true, path: 'assets/img/character/riding/ride_fallen_helmet.png' },
    // 连按 F 扶车的逐帧（512×384），每按一次换下一帧
    lift_1: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/1.png' },
    lift_2: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/2.png' },
    lift_3: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/3.png' },
    lift_4: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/4.png' },
    lift_5: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/5.png' },
    lift_6: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/6.png' },
    lift_1_helmet: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/1_helmet.png' },
    lift_2_helmet: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/2_helmet.png' },
    lift_3_helmet: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/3_helmet.png' },
    lift_4_helmet: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/4_helmet.png' },
    lift_5_helmet: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/5_helmet.png' },
    lift_6_helmet: { w: 112, h: 84, color: 0x2563eb, file: true, path: 'assets/img/character/scooter-lift/6_helmet.png' },
    // 主角推车（侧面，扶车最后一帧：人扶着立起来的车）：车棚推车、晚上找桩
    pusher:        { w: 40, h: 56, color: 0x93c5fd, file: true, path: 'assets/img/character/scooter-lift/6.png' },
    pusher_helmet: { w: 40, h: 56, color: 0x93c5fd, file: true, path: 'assets/img/character/scooter-lift/6_helmet.png' },
    bike:         { w: 24, h: 48, color: 0xfacc15, file: true,
      path: 'assets/img/vehical/protagonist.png' }, // 自己的车（车棚停好后）
    bike_other:   { w: 24, h: 48, color: 0x9ca3af, file: false }, // 已由 dorm_bike_1~7 代替
    dorm_bike:    { w: 34, h: 78, color: 0xfacc15, file: true,
      path: 'assets/img/vehical/protagonist.png' }, // 主角的车
    // 别人的车（7 种颜色）：找车车阵、车棚、被占的充电桩
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
    npc_delivery: { w: 32, h: 56,  color: 0xf97316, file: true,
      path: 'assets/img/vehical_with_driver/delivery.png' }, // 外卖车（带骑手）
    npc_wrong:    { w: 32, h: 56,  color: 0xef4444, file: false }, // 逆行车
    npc_walker:   { w: 28, h: 28,  color: 0xa855f7, file: false }, // 行人（缺下面的逐帧时才用）
    // 骑行横穿马路的行人：男生 / 女生，左右各 3 帧（342×512）
    walker_boy_left_1:   { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/boy_walker/walk-left-1.png' },
    walker_boy_left_2:   { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/boy_walker/walk-left-2.png' },
    walker_boy_left_3:   { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/boy_walker/walk-left-3.png' },
    walker_boy_right_1:  { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/boy_walker/walk-right-1.png' },
    walker_boy_right_2:  { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/boy_walker/walk-right-2.png' },
    walker_boy_right_3:  { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/boy_walker/walk-right-3.png' },
    walker_girl_left_1:  { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/girl_walker/walk-left-1.png' },
    walker_girl_left_2:  { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/girl_walker/walk-left-2.png' },
    walker_girl_left_3:  { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/girl_walker/walk-left-3.png' },
    walker_girl_right_1: { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/girl_walker/walk-right-1.png' },
    walker_girl_right_2: { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/girl_walker/walk-right-2.png' },
    walker_girl_right_3: { w: 342, h: 512, color: 0xa855f7, file: true, path: 'assets/img/character/girl_walker/walk-right-3.png' },
    npc_bus:      { w: 64, h: 140, color: 0x16a34a, file: false }, // 校车
    pile:         { w: 32, h: 40,  color: 0x06b6d4, file: false }, // 充电桩
    slot:         { w: 32, h: 60,  color: 0xffffff, file: false, outline: true }, // 空车位
    road:         { w: 64, h: 64,  color: 0x374151, file: false }, // 路面
    slope:        { w: 64, h: 64,  color: 0x92400e, file: false }, // 坡道
    grass:        { w: 64, h: 64,  color: 0x166534, file: false }, // 草地
    building:     { w: 64, h: 64,  color: 0x7f1d1d, file: false }, // 楼（宿舍/教学楼）
    rider_carry:  { w: 32, h: 64,  color: 0x1d4ed8, file: false }, // 主角骑车载人（没图时沿用 rider）
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
