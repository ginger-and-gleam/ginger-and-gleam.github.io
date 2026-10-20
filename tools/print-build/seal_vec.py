"""Vectorize the G&G seal (light version) into ink + star path sets, cached as JSON."""
import json, sys, numpy as np, cv2, potrace
from PIL import Image
src = sys.argv[1]; out = sys.argv[2]
im = Image.open(src).convert('RGBA')
bg = Image.new('RGBA', im.size, (255,255,255,255)); bg.alpha_composite(im)
rgb = np.array(bg.convert('RGB')).astype(np.float32)
SCALE = 3
big = cv2.resize(rgb, None, fx=SCALE, fy=SCALE, interpolation=cv2.INTER_CUBIC)
r,g,b = big[...,0],big[...,1],big[...,2]
mx = big.max(axis=2); mn = big.min(axis=2)
sat = (mx-mn)/(mx+1e-6)
ink  = (mx < 205) & (sat < 0.30)          # near-black linework and type
star = (sat > 0.35) & (r > g) & (r > 90) & (mx < 245)  # copper stars
def trace(mask):
    bm = potrace.Bitmap(~mask)
    path = bm.trace(turdsize=6, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0, opticurve=True, opttolerance=0.2)
    curves=[]
    for c in path:
        segs=[]
        for s in c.segments:
            if s.is_corner: segs.append(['L', s.c.x, s.c.y, s.end_point.x, s.end_point.y])
            else: segs.append(['C', s.c1.x, s.c1.y, s.c2.x, s.c2.y, s.end_point.x, s.end_point.y])
        curves.append({'start':[c.start_point.x, c.start_point.y], 'segs':segs})
    return curves
data = {'size': big.shape[1], 'ink': trace(ink), 'star': trace(star)}
json.dump(data, open(out,'w'))
print('ink curves', len(data['ink']), 'star curves', len(data['star']), 'size', data['size'])
