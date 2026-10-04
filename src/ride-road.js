// 将美术图逐行校正到游戏路宽；生成的纹理只缓存一次，不在每帧处理图片。
const RideRoad = {
  tileKey: 'ride_road_aligned',

  prepare(scene, left, right) {
    const textures = scene.textures;
    if (!textures.exists(this.tileKey)) {
      const source = textures.get('road_tile').getSourceImage();
      const aligned = this.align(source, CONFIG.ride.roadArt, left, right);
      // 首尾重叠一段：循环的两侧读取同一段原图，消除硬切接缝。
      const overlap = 160;
      const period = aligned.height - overlap;
      const texture = textures.createCanvas(this.tileKey, 960, period);
      const ctx = texture.context;
      ctx.drawImage(aligned, 0, 0, 960, period, 0, 0, 960, period);
      const tail = aligned.getContext('2d').getImageData(0, period, 960, overlap);
      const head = aligned.getContext('2d').getImageData(0, 0, 960, overlap);
      ctx.putImageData(this.join(tail, head), 0, 0);
      texture.refresh();
    }
  },

  landmark(scene, centerY, left, right) {
    const textures = scene.textures;
    // 每条路线的地标位置不同，要按其实际世界坐标对接循环背景。
    const key = 'ride_stadium_aligned_' + centerY;
    if (!textures.exists(key)) {
      const source = textures.get('road_stadium').getSourceImage();
      const aligned = this.align(source, CONFIG.ride.landmark, left, right);
      const texture = textures.createCanvas(key, 960, aligned.height);
      const ctx = texture.context;
      const base = textures.get(this.tileKey).getSourceImage();
      const top = Math.round(centerY - aligned.height / 2);
      const background = document.createElement('canvas');
      background.width = 960;
      background.height = aligned.height;
      const bg = background.getContext('2d');
      const offset = ((top % base.height) + base.height) % base.height;
      for (let y = -offset; y < aligned.height; y += base.height) bg.drawImage(base, 0, y);
      ctx.drawImage(aligned, 0, 0);
      const overlap = 160;
      const end = aligned.height - overlap;
      ctx.putImageData(this.join(bg.getImageData(0, 0, 960, overlap),
        ctx.getImageData(0, 0, 960, overlap)), 0, 0);
      ctx.putImageData(this.join(ctx.getImageData(0, end, 960, overlap),
        bg.getImageData(0, end, 960, overlap)), 0, end);
      // 地标只替换路边景观，车道使用下层连续的路面，标线不会换位。
      ctx.clearRect(left, 0, right - left, aligned.height);
      texture.refresh();
    }
    return key;
  },

  // 沿颜色差最小的路径拼接景观，只在路径附近做窄幅柔化。
  // 相比整段透明叠加，这样不会出现半透明的树和重复灯柱。
  join(upper, lower) {
    const { width: w, height: h } = upper;
    const a = upper.data, b = lower.data;
    const parents = new Int16Array(w * h);
    let previous = new Float64Array(h);
    const margin = 8;
    for (let x = 0; x < w; x++) {
      const current = new Float64Array(h).fill(Infinity);
      for (let y = margin; y < h - margin; y++) {
        let best = y;
        for (let k = Math.max(margin, y - 2); k <= Math.min(h - margin - 1, y + 2); k++) {
          if (previous[k] < previous[best]) best = k;
        }
        const p = (y * w + x) * 4;
        const cost = (a[p] - b[p]) ** 2 + (a[p + 1] - b[p + 1]) ** 2 + (a[p + 2] - b[p + 2]) ** 2;
        current[y] = previous[best] + cost + Math.abs(y - h / 2) * 0.1;
        parents[x * h + y] = best;
      }
      previous = current;
    }
    let y = margin;
    for (let k = margin + 1; k < h - margin; k++) if (previous[k] < previous[y]) y = k;
    const seam = new Int16Array(w);
    for (let x = w - 1; x >= 0; x--) { seam[x] = y; y = parents[x * h + y]; }
    const result = new ImageData(w, h);
    for (let row = 0; row < h; row++) for (let x = 0; x < w; x++) {
      const p = (row * w + x) * 4;
      const feather = 16;
      const t = Phaser.Math.Clamp((row - seam[x] + feather / 2) / feather, 0, 1);
      for (let c = 0; c < 4; c++) result.data[p + c] = Math.round(a[p + c] * (1 - t) + b[p + c] * t);
    }
    return result;
  },

  align(source, art, left, right) {
    const canvas = document.createElement('canvas');
    canvas.width = 960;
    canvas.height = Math.round(source.height * art.scale);
    const ctx = canvas.getContext('2d');
    const center = (left + right) / 2;
    // edgeRows 是原图从上到下的等距路沿采样；分别校正左右半幅，
    // 固定左右路沿和中线，同时保留两侧景物原有的缩放比例。
    for (let y = 0; y < canvas.height; y++) {
      const sy = y / art.scale;
      const pos = Math.min(sy / (source.height - 1), 1) * (art.edgeRows.length - 1);
      const i = Math.min(Math.floor(pos), art.edgeRows.length - 2);
      const t = pos - i;
      const a = art.edgeRows[i], b = art.edgeRows[i + 1];
      const l = a[0] + (b[0] - a[0]) * t;
      const r = a[1] + (b[1] - a[1]) * t;
      const c = art.centerRows ? art.centerRows[i] + (art.centerRows[i + 1] - art.centerRows[i]) * t : art.centerX;
      const sh = Math.min(1 / art.scale, source.height - sy);
      if (art.sideRows) {
        const sl = art.sideRows[i][0] + (art.sideRows[i + 1][0] - art.sideRows[i][0]) * t;
        const sr = art.sideRows[i][1] + (art.sideRows[i + 1][1] - art.sideRows[i][1]) * t;
        const walk = 160;
        ctx.drawImage(source, sl - (left - walk) / art.scale, sy, (left - walk) / art.scale, sh,
          0, y, left - walk, 1);
        ctx.drawImage(source, sl, sy, l - sl, sh, left - walk, y, walk, 1);
        ctx.drawImage(source, r, sy, sr - r, sh, right, y, walk, 1);
        ctx.drawImage(source, sr, sy, (960 - right - walk) / art.scale, sh,
          right + walk, y, 960 - right - walk, 1);
      } else {
        ctx.drawImage(source, l - left / art.scale, sy, left / art.scale, sh, 0, y, left, 1);
        ctx.drawImage(source, r, sy, (960 - right) / art.scale, sh, right, y, 960 - right, 1);
      }
      ctx.drawImage(source, l, sy, c - l, sh, left, y, center - left, 1);
      ctx.drawImage(source, c, sy, r - c, sh, center, y, right - center, 1);
    }
    return canvas;
  }
};
