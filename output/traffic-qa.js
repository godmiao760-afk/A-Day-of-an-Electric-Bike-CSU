const panel = document.createElement('pre');
panel.style = 'position:fixed;top:0;left:0;max-height:130px;overflow:auto;color:white;background:#111d;font:12px monospace;margin:0;z-index:9999';
document.body.appendChild(panel);
window.addEventListener('error', e => { panel.textContent += 'ERROR: ' + e.message; });
const ready = setInterval(() => {
  const ride = game.scene.getScene('Ride');
  if (!ride.sys.isActive() || ride.time.now < 100) return;
  clearInterval(ready);
  try {
    const originalRandom = Math.random;
    let seed = 391073;
    Math.random = () => { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; };
    const originalPick = ride.pickType;
    const results = {}, checks = [];
    const assert = (ok, msg) => { if (!ok) throw Error(msg); checks.push(msg); };
    for (const type of ['wrong', 'delivery', 'car', 'bus']) {
      ride.pickType = () => type;
      let incoming = 0, outgoing = 0, wrongSide = 0;
      for (let i = 0; i < 800; i++) {
        ride.npcs.clear(true, true); ride.spawn();
        const o = ride.npcs.getChildren()[0];
        if (!o) throw Error('missing ' + type);
        const speed = o.getData('speed');
        speed > 0 ? incoming++ : outgoing++;
        if (!ride.directionLanes(Math.sign(speed)).includes(o.getData('lane'))) wrongSide++;
        if ((speed > 0 && Math.abs(o.angle) !== 180) || (speed < 0 && o.angle !== 0)) throw Error('heading ' + type);
      }
      results[type] = { incoming, outgoing, wrongSide };
      assert(incoming > 320 && incoming < 480 && outgoing > 320, 'both directions: ' + type);
      assert(type === 'wrong' || type === 'delivery' ? wrongSide > 25 && wrongSide < 100 : wrongSide === 0, 'lane distribution: ' + type);
    }
    ride.npcs.clear(true, true);
    for (const x of [530, 630]) ride.addCar('car', 'npc_car', x, ride.startY - 200, -90);
    assert(ride.addCar('car', 'npc_car', 530, ride.startY - 200, -90) === null, 'blocked half stays in own lanes');
    ride.npcs.clear(true, true);
    const a = ride.addCar('wrong', 'npc_wrong', 530, ride.startY - 200, -140);
    a.setData('canCrossLane', false);
    ride.addCar('car', 'npc_car', 630, a.y, -90);
    assert(!ride.changeLane(a), 'ordinary rider cannot cross center');
    a.setData('canCrossLane', true);
    assert(ride.changeLane(a) && a.getData('lane') === 430, 'selected rider can cross center');
    assert(!ride.changeLane(a), 'lane change cooldown');
    ride.npcs.clear(true, true); ride.dream = true;
    for (let i = 0; i < 100; i++) {
      ride.pickType = () => 'delivery'; ride.spawn();
      const o = ride.npcs.getChildren()[0];
      if (o.getData('wrongWay') || o.getData('canCrossLane')) throw Error('dream violation');
      ride.npcs.clear(true, true);
    }
    checks.push('dream obeys lane directions');
    ride.dream = false; ride.pickType = originalPick; Math.random = originalRandom;
    panel.textContent = 'PASS ' + checks.length + ' checks — ' + JSON.stringify(results) + ' 左来 ↓ / 右去 ↑';
    const top = ride.cameras.main.scrollY;
    const samples = [
      ['wrong', 'npc_rider_green', 330, top + 180, 140],
      ['delivery', 'npc_delivery', 430, top + 310, 250],
      ['wrong', 'npc_rider_helmet_blue', 530, top + 150, -140],
      ['delivery', 'npc_delivery', 630, top + 290, -250],
      ['bus', 'npc_bus', 330, top + 450, 50],
      ['car', 'npc_car_2', 630, top + 500, -90],
    ];
    samples.forEach(([type, key, x, y, v]) => { const o = ride.addCar(type, key, x, y, v); if (o) ride.sizeNpc(o, type); });
    ride.cameras.main.resetFX(); ride.physics.pause(); ride.scene.pause();
  } catch (e) { panel.textContent += 'FAIL ' + e.stack; ride.scene.pause(); }
}, 100);
