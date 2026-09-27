"""生成网页素材，保留原始图片和声音；尺寸不变以兼容裁切帧。"""
from pathlib import Path
import re
import subprocess
from PIL import Image
import imageio_ffmpeg

root = Path(__file__).resolve().parents[1]
manifest = root / 'src/assets.js'
text = manifest.read_text(encoding='utf-8')
original_bytes = web_bytes = 0
paths = set(re.findall(r"path:\s*'([^']+)'", text))
for path in sorted(paths):
    original = path.replace('assets/web/', 'assets/', 1)
    source = root / original
    # 已转换的路径可再次生成，从原始目录恢复音频扩展名。
    if original.endswith('.webp'):
        source = source.with_suffix('.png')
    if not source.exists() and source.suffix == '.mp3':
        source = next((p for ext in ('.wav', '.m4a')
                       if (p := source.with_suffix(ext)).exists()), source)
    if not source.exists():
        raise FileNotFoundError(source)
    target = root / 'assets/web' / source.relative_to(root / 'assets')
    target = target.with_suffix('.webp' if source.suffix == '.png' else '.mp3')
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.suffix == '.png':
        with Image.open(source) as im:
            im.save(target, 'WEBP', quality=85, method=6)
    else:
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-y', '-v', 'error',
                        '-i', str(source), '-map_metadata', '-1', '-ac', '1',
                        '-ar', '44100', '-b:a', '96k', str(target)], check=True)
    original_bytes += source.stat().st_size
    web_bytes += target.stat().st_size
    text = text.replace("'" + path + "'", "'" + target.relative_to(root).as_posix() + "'")
manifest.write_text(text, encoding='utf-8')
print(f'Referenced assets: {original_bytes:,} -> {web_bytes:,} bytes')
