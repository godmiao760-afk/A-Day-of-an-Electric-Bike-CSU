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
    cover:        { w: 960, h: 540, color: 0x14301a, file: true,
      path: 'assets/img/cover/cover.png' }, // 开始画面封面（1396×926，标题字已画在图里）
    dorm:        { w: 1536, h: 1024, color: 0x365a32, file: true,
      path: 'assets/img/background/dorm.png' }, // 宿舍车棚背景
    // 其它场景背景（1536×1024 俯视图）
    bg_ride_inside:  { w: 1536, h: 1024, color: 0x166534, file: true, path: 'assets/img/background/stadium_clear.png' },      // 校内骑行两侧：体育场
    bg_ride_outside: { w: 1536, h: 1024, color: 0x374151, file: true, path: 'assets/img/background/bridge_clear.png' },       // 校外骑行两侧：过江桥
    bg_traffic:      { w: 1536, h: 1024, color: 0x1e293b, file: true, path: 'assets/img/background/traffic_scene_clear.png' }, // 校门口选路线：交警路口
    bg_park:         { w: 1536, h: 1024, color: 0x374151, file: true, path: 'assets/img/background/parking_compact_day.png' }, // 教学楼车棚
    bg_park_clear:   { w: 1536, h: 1024, color: 0x374151, file: true, path: 'assets/img/background/parking_clear_day.png' },   // 备用：白天车棚
    bg_charge:       { w: 1536, h: 1024, color: 0x0b1026, file: true, path: 'assets/img/background/charging_bays_compact_night.png' }, // 夜晚充电区
    bg_charge_day:   { w: 1536, h: 1024, color: 0x374151, file: true, path: 'assets/img/background/charging_bays_clear.png' }, // 备用：白天充电区
    bg_police:       { w: 1536, h: 1024, color: 0x1e3a8a, file: true, path: 'assets/img/background/police_station.png' },     // 派出所结局背景
    ui_controls_panel: { w: 1164, h: 138, color: 0x000000, file: true, path: 'assets/img/ui/controls_panel_blank.png' },    // 操作说明底板
    // 骑行道路（路 + 两边景观画在一张图里，代替原来的 road 色块和两侧背景）
    road_tile:    { w: 1024, h: 1536, color: 0x374151, file: true, path: 'assets/img/road/xiaodianlv-vertical-tileable.png' },   // 竖向可重复的路，两条路线都用
    road_stadium: { w: 1536, h: 1024, color: 0x374151, file: true, path: 'assets/img/road/620880161592b4a6cd53ef40b6066d93.png' }, // 校内路线中间插一张：体育场路段
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
    // 主角推车走路：左 / 右各 3 帧（342×512），另有戴头盔版；有图时车棚推车、晚上找桩都用它播动画
    push_left_1:  { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_left_01.png' },
    push_left_2:  { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_left_02.png' },
    push_left_3:  { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_left_03.png' },
    push_right_1: { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_right_01.png' },
    push_right_2: { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_right_02.png' },
    push_right_3: { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_right_03.png' },
    push_left_1_helmet:  { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_left_01_helmet.png' },
    push_left_2_helmet:  { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_left_02_helmet.png' },
    push_left_3_helmet:  { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_left_03_helmet.png' },
    push_right_1_helmet: { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_right_01_helmet.png' },
    push_right_2_helmet: { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_right_02_helmet.png' },
    push_right_3_helmet: { w: 342, h: 512, color: 0x93c5fd, file: true, path: 'assets/img/character/player_push_frames/push_right_03_helmet.png' },
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
    npc_bus:      { w: 64, h: 140, color: 0x16a34a, file: true,
      path: 'assets/img/vehical/school_bus_up.png' }, // 校车（原图车头朝右，已转成朝上）
    npc_cart:     { w: 64, h: 140, color: 0x16a34a, file: true,
      path: 'assets/img/vehical/watering_cart_up.png' }, // 洒水车（和校车一样挡路，已转成朝上）
    npc_bus_2:    { w: 64, h: 140, color: 0x16a34a, file: true,
      path: 'assets/img/vehical/school_bus_2_up.png' }, // 校车款式 2（school_bus_1 抠掉假透明格子、转成朝上）
    npc_cart_2:   { w: 64, h: 140, color: 0x16a34a, file: true,
      path: 'assets/img/vehical/watering_cart_2_up.png' }, // 洒水车款式 2（已转成朝上）
    pile:         { w: 32, h: 40,  color: 0x06b6d4, file: false }, // 充电桩
    slot:         { w: 32, h: 60,  color: 0xffffff, file: false, outline: true }, // 空车位
    road:         { w: 64, h: 64,  color: 0x374151, file: false }, // 路面
    slope:        { w: 64, h: 64,  color: 0x92400e, file: false }, // 坡道
    grass:        { w: 64, h: 64,  color: 0x166534, file: false }, // 草地
    building:     { w: 64, h: 64,  color: 0x7f1d1d, file: false }, // 楼（宿舍/教学楼）
    rider_carry:  { w: 32, h: 64,  color: 0x1d4ed8, file: false }, // 主角骑车载人（没图时沿用 rider）
    npc_car:      { w: 56, h: 100, color: 0x64748b, file: true,
      path: 'assets/img/vehical/car_8_up.png' },  // 汽车（校外）：红色小轿车（vehical/8.png 转成车头朝上）
    npc_car_2:    { w: 56, h: 100, color: 0x64748b, file: true,
      path: 'assets/img/vehical/car_11_up.png' }, // 蓝色小轿车（vehical/11.png 转成朝上）
    police:       { w: 32, h: 32,  color: 0x1e3a8a, file: true,
      path: 'assets/img/character/police/bat_bottom_01.png' }, // 交警（静止帧，342×512）
    // 交警挥指挥棒逐帧（342×512）：低位 3 帧 + 高位 3 帧，骑行检查点循环播放
    police_bottom_1: { w: 342, h: 512, color: 0x1e3a8a, file: true, path: 'assets/img/character/police/bat_bottom_01.png' },
    police_bottom_2: { w: 342, h: 512, color: 0x1e3a8a, file: true, path: 'assets/img/character/police/bat_bottom_02.png' },
    police_bottom_3: { w: 342, h: 512, color: 0x1e3a8a, file: true, path: 'assets/img/character/police/bat_bottom_03.png' },
    police_top_1:    { w: 342, h: 512, color: 0x1e3a8a, file: true, path: 'assets/img/character/police/bat_top_01.png' },
    police_top_2:    { w: 342, h: 512, color: 0x1e3a8a, file: true, path: 'assets/img/character/police/bat_top_02.png' },
    police_top_3:    { w: 342, h: 512, color: 0x1e3a8a, file: true, path: 'assets/img/character/police/bat_top_03.png' },
    barrier:      { w: 400, h: 16, color: 0xdc2626, file: false }, // 检查点路障
    // v2 结局图（Ending 场景）：真图是 1536×1024 整幅插画，Ending 缩成插画卡 + 压暗铺满当背景；没图时 320×240 色块
    end_perfect:  { w: 320, h: 240, color: 0x16a34a, file: true,
      path: 'assets/img/ending-backgrounds/perfect_ending.png' },        // 完美：捧着花笑
    end_pass:     { w: 320, h: 240, color: 0x2563eb, file: true,
      path: 'assets/img/ending-backgrounds/qualified_ending.png' },      // 合格：教室里坐着
    end_fail:     { w: 320, h: 240, color: 0x6b7280, file: true,
      path: 'assets/img/ending-backgrounds/unqualified_ending.png' },    // 不合格：门口被老师瞪
    end_police:   { w: 320, h: 240, color: 0x1e3a8a, file: true,
      path: 'assets/img/ending-backgrounds/police_station_ending.png' }, // 派出所：戴手铐
    end_faint:    { w: 320, h: 240, color: 0x7c2d12, file: true,
      path: 'assets/img/ending-backgrounds/collapsed_ending.png' },      // 昏倒：校医院挂葡萄糖
    end_broke:    { w: 320, h: 240, color: 0x991b1b, file: true,
      path: 'assets/img/ending-backgrounds/begging_ending.png' }         // 身无分文：跪地捧碗
  },
  // Sound assets may use booleans (default assets/sfx/<key>.mp3) or explicit paths.
  sounds: {
    beep: { file: true, path: 'assets/sfx/电动车解锁_越近越响.mp3' },
    hit: { file: true, path: 'assets/sfx/电驴相撞触发.mp3' },
    fall: false,
    park: false,
    plug: { file: true, path: 'assets/sfx/插插座声音_调高响度.mp3' },
    whistle: { file: true, path: 'assets/sfx/交警吹哨.wav' },
    coin: false,
    domino: { file: true, path: 'assets/sfx/碰撞音效_调高响度.wav' },
    policeVoice: { file: true, path: 'assets/sfx/交警呵斥.mp3' },
    pay: { file: true, path: 'assets/sfx/扣款声.wav' },
    hunger: { file: true, path: 'assets/sfx/肚子咕咕叫.wav' },
    move_alarm: { file: true, path: 'assets/sfx/挪车报警声.wav' },
    class_bell: { file: true, path: 'assets/sfx/上课铃声.m4a' },
    tow: { file: true, path: 'assets/sfx/违者拖车.mp3' },
    watering_bgm: { file: true, path: 'assets/sfx/洒水车bgm.mp3' },
    ending_perfect: { file: true, path: 'assets/sfx/完美音效.mp3' },
    ending_pass: { file: true, path: 'assets/sfx/合格音效.wav' },
    ending_fail: { file: true, path: 'assets/sfx/游戏失败哭声.mp3' },
    ending_faint_belly: { file: true, path: 'assets/sfx/肚子咕咕叫.wav' },
    ending_faint: { file: true, path: 'assets/sfx/饿晕倒.mp3' },
    ending_police: { file: true, path: 'assets/sfx/镣铐声_派出所.wav' },
    ending_broke: { file: true, path: 'assets/sfx/乞讨.mp3' }
  }
};
