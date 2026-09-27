"""只将游戏运行所需文件放到 output/netlify，避免上传原图和项目文档。"""
from pathlib import Path
import re
import shutil

root = Path(__file__).resolve().parents[1]
target = root / 'output/netlify'
paths = {'index.html', 'assets/vendor/phaser-3.90.0.min.js', 'assets/vendor/PHASER-LICENSE.md'}
paths.update(p.relative_to(root).as_posix() for p in (root / 'src').rglob('*.js'))
paths.update(re.findall(r"path:\s*'([^']+)'", (root / 'src/assets.js').read_text(encoding='utf-8')))
for path in sorted(paths):
    destination = target / path
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(root / path, destination)
print(f'Prepared {len(paths)} runtime files in {target}')
