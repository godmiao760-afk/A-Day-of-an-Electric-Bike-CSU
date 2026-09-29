// ===== 独白文案（D 负责，只改文字）=====
// 数组 = 随机抽一句，可以随意往里加。
const LINES = {
  // 开始画面（Title）
  title: {
    name:  "小电驴的一天",   // 没有封面图时显示的文字标题
    start: "按 F 开始"
  },
  intro: {
    day1: "大一新生，第一次骑电动车上学。\n昨晚充到一半，又被人拔了……",
    low:  "电不多了，今天祈祷别摔。",
    ok:   "电还算够，今天应该没问题……吧？",
    allowance: "生活费到账",
    lateCount: "本周已迟到 {n} 次",
    lastDay:   "今天是最后一天。"
  },
  findCar: {
    start:   "我的车……停哪来着？",
    notMine: ["不是我的。", "好像是……不是。", "谁的车跟我一模一样？", "这辆的座套好丑，不是我的。"],
    blocked: "被夹在中间了，得先把旁边的车挪开。",
    moved:   "嘿——咻！挪开了。",
    found:   "终于找到你了！",
    backpackTip: "按 E 打开背包",
    controls: "WASD / 方向键走路 · 靠近车辆按 F",
    signal: "钥匙信号 ",
    inspectHint: "按 F 查看",
    moveHint: "按 F 挪开这辆车",
    unlockHint: "按 F 解锁"
  },
  backpack: {
    title:     "背包",
    helmetOn:  "戴上头盔了。",
    helmetOff: "把头盔摘了。",
    license:   "牌照已经装在车上了。",
    close:     "关闭",
    noRide:    "骑车的时候可不能翻包！"
  },
  gate: {
    title:     "校门口",
    route:     "怎么去教学楼？",
    inside:    "校内（远，有大坡）",
    outside:   "校外（近，可能有交警）",
    backpack:  "先翻一下背包",
    goInside:  "走校内，稳一点。",
    goOutside: "抄个近路，应该没事吧。",
    // v2：校门口透露今天哪条路被挤成单行道
    rumorInside:  "（听说校内那条路今天挤成单行道了）",
    rumorOutside: "（听说校外那条路今天挤成单行道了）"
  },
  passenger: {
    ask:  "同学：「我要迟到了！载我一程呗，给你 15 块！」\n（载人来不及走校内，只能走校外）",
    yes:  "上来吧！",
    no:   "不好意思，我也快迟到了。",
    paid: "同学：「谢啦！」（+¥15）",
    fled: "同学：「我先走了，钱下次给你！」……人跑了。",
    leaveDead: "同学：「……我自己走过去吧。」人走了，钱也没给。"
  },
  police: {
    stop:     "【交警检查】\n「同学，停一下。」",
    helmet:   "没戴头盔",
    license:  "车没上牌照",
    carry:    "违规载人",
    fineHead: "「骑电动车要守规矩。」",
    pass:     "「同学，注意安全。」\n——检查合格，放行。",
    houhu:    "去后湖的路上碰到交警检查……",
    // v2：停车受检 / 硬闯
    askStop:  "前面交警在拦车检查。",
    optStop:  "停车接受检查",
    optRun:   "硬闯过去",
    runOk:    ["冲过去了！心跳好快……", "闯过去了，没人追上来。"],
    runOmen:  "交警好像记住我的车了……"
  },
  meals: {
    noonTitle:    "中午 · 上午课结束",
    eveningTitle: "傍晚 · 下午课结束",
    question:     "去哪？",
    canteen:      "食堂",
    houhu:        "后湖",
    license:      "去办牌照（吃不上饭）",
    skip:         "不吃了",
    noMoney:      "（钱不够）",
    noBattery:    "（电不够）",
    ateCanteen:   ["食堂还是那个味道。", "排了好久的队……总算吃上了。"],
    ateHouhu:     ["后湖的烧烤，值了！", "吃撑了，骑车回去。"],
    gotLicense:   "牌照办好了！以后不怕查了。",
    skipped:      "省点钱吧……肚子在叫。",
    fineNoFood:   "罚完款……后湖吃不起了，饿着回去吧。",
    lastMoney:    "（买完就身无分文了）",
    takes:        "约 {m} 分钟"     // 选项后面显示大概花多久，{m} 会被替换
  },
  ride: {
    start:        "出发！希望今天路上别出事。",
    startInside:  "校内路线：人多，还有那个大坡。",
    startOutside: "校外路线：车多，速度快。",
    hit:          ["哎哟！看路啊！", "外卖小哥又在赶时间……", "逆行还这么理直气壮？", "走路能不能看看车！"],
    fall:         "摔了一跤……电池好像松了。",
    slope:        "又是这个大坡……电量在哭。",
    lowBattery:   "电量告急，千万别再上坡了……",
    dead:         "没电了……只能推过去了。",
    policeAhead:  "前面好像有交警……",
    // v2：早高峰单行道
    oneWaySign:   "早高峰\n被挤成单行道",
    oneWayEnter:  ["怎么全是逆行的！", "这段路被挤成单行道了……"]
  },
  park: {
    riding:  "车棚到了，找个空位。",
    pushing: "今天又要被点名了。",
    full:    ["满了。", "这里也满了。", "这辆占了两个位置！"],
    parked:  "停好了，冲！",
    // 多米诺
    domino:    ["完了完了完了……", "哗啦——倒了一排。", "我就轻轻碰了一下！"],
    lift:      ["扶起来一辆。", "嘿——咻！", "这车怎么这么沉……"],
    liftFirst: "倒了一排车不管，良心过不去……先扶起来。",
    liftHint:  "按 F 扶起来",
    liftedAll: "总算都扶起来了。",
    // 门口违停
    noParkZone:    "禁停",
    illegalHint:   "按 F 停在门口（违停）",
    illegalAsk:    "教学楼门口不让停车。\n但这里离教室最近……停这儿？",
    illegalYes:    "就停一会儿",
    illegalNo:     "算了，去里面找",
    illegalParked: "停门口了，赶紧跑！",
    ticketHead:    "保安：「同学，这里禁止停车！」",
    ticketReason:  "教学楼门口违停",
    noTicket:      "好像没人管，运气不错。"
  },
  classScene: {
    morning:   "上午的课……",
    afternoon: "下午的课……",
    after:     "下课了。",
    drain:     "白天又骑了几趟",
    hungry:    "好饿……干什么都没力气。",
    lateTotal: "本周累计迟到 {n} 次"
  },
  charge: {
    start:     "22:40，得赶在门禁前充上电。",
    occupied:  ["有人在充。", "这个也被占了。", "充满了还不拔，谁的车啊……"],
    broken:    ["坏的。上周就是坏的。", "屏幕都不亮。"],
    qrFail:    "扫码失败……再试一次？",
    qrOk:      "扫上了！",
    plugged:   "终于插上了。回去睡觉，明早再看吧……",
    full:      "（第二天早上）满电！今天运气不错。",
    unplugged: "（第二天早上）……线又被拔了。",
    curfew:    "门禁了，今晚充不上了。",
    noMoney:   "余额不足……充电都充不起了。"
  },
  hungry: "饿得走不动了……",
  faintWarn: "眼前发黑……得赶紧吃点东西。",
  // 每日评价（Result 页每天显示，不影响最终结局）
  endings: {
    ontime_charged: "难得顺利的一天",
    ontime_empty:   "明天早上见分晓",
    late_charged:   "至少明天有电了",
    late_empty:     "明天还得推车"
  },
  // 最终结局（Ending 场景）：3 个正常 + 3 个隐藏
  finalEnding: {
    perfect: { title: "完美结局 · 全勤",     text: "三天，一次都没迟到。\n这辆小电驴，值得一个满电的周末。" },
    pass:    { title: "合格结局 · 还行",     text: "迟到了几次，但总算熬过了这一周。\n下周……再说吧。" },
    fail:    { title: "不合格结局 · 常驻迟到", text: "迟到次数太多，老师已经记住你的名字了。\n也许该早点起床，或者早点充电。" },
    police:  { title: "隐藏结局 · 派出所",   text: "硬闯没闯过去。\n小电驴被扣了，人被请去派出所喝茶。" },
    faint:   { title: "隐藏结局 · 昏倒",     text: "饿得眼前一黑，倒在了路上。\n醒来时在校医院，手上挂着葡萄糖。" },
    broke:   { title: "隐藏结局 · 身无分文", text: "钱包空了。\n跪在地上嚎啕大哭：连充电的两块钱都没有了……" }
  },
  endingUi: {
    stats:   "第 {day} 天　累计迟到 {late} 次　硬闯成功 {runs} 次　余额 {money}",
    restart: "按 F 重新开始"
  }
};
