"""背景雕刻插画：codex 生成的白底黑线稿 → 透明 WebP。

源：content/illustrations/*.png（白底黑线；2026-09-21 起为 hero-alps / contour / chip-die / epfl-lausanne 四张居中构图，
    旧的 bg-*.png 保留作存档，不再转换）
出：docs/public/img/bg/<名>.webp（线条为深蓝 #143152，alpha = 线条浓度）
    INVERT 里的几张另出 <名>-inv.webp（白线），给炭黑/深蓝色带用
用法：python scripts/make_bg.py
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'content', 'illustrations')
OUT = os.path.join(ROOT, 'docs', 'public', 'img', 'bg')
os.makedirs(OUT, exist_ok=True)
# 每页一张背景；chip-die、epfl-lausanne 为页内插画段；contour 用于 404
NAMES = ['custom-asic-farm', 'world-link', 'cham-panorama', 'jungfrau', 'matterhorn', 'wafer-probe', 'neuchatel', 'cham-ikarus', 'chip-die', 'epfl-lausanne', 'contour']
INVERT = {'custom-asic-farm', 'world-link', 'cham-panorama', 'jungfrau', 'matterhorn', 'wafer-probe', 'neuchatel', 'cham-ikarus'}   # 反白版给同页的深色引言带/行动区


def to_alpha(path, rgb=(20, 49, 82)):
    im = Image.open(path).convert('RGBA')
    flat = Image.new('RGBA', im.size, (255, 255, 255, 255))
    flat.alpha_composite(im)                       # 源图若自带透明底，先铺白
    a = np.asarray(flat.convert('L'), dtype=np.float32) / 255.0
    alpha = np.clip((1.0 - a - 0.04) / 0.96, 0, 1)  # 纯白（含压缩噪点）完全透明
    out = np.zeros((*alpha.shape, 4), dtype=np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = rgb
    out[..., 3] = (alpha * 255).astype(np.uint8)
    res = Image.fromarray(out, 'RGBA')
    res.thumbnail((2400, 2400), Image.LANCZOS)
    return res


for name in NAMES:
    fn = os.path.join(SRC, name + '.png')
    if not os.path.exists(fn):
        print('missing', name); continue
    res = to_alpha(fn)
    res.save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=86, method=6)
    print(name, res.size, os.path.getsize(os.path.join(OUT, name + '.webp')) // 1024, 'KB')
    if name in INVERT:
        inv = to_alpha(fn, rgb=(255, 255, 255))
        inv.save(os.path.join(OUT, name + '-inv.webp'), 'WEBP', quality=86, method=6)
