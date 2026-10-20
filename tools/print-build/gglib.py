import json, os, qrcode
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
from reportlab.pdfgen.canvas import FILL_EVEN_ODD
FD = '/tmp/claude-0/-home-claude/2fcd9f31-4970-58e7-839c-3aef28e9cce9/scratchpad/fonts'
for n in ['BM-Display','BM-Sub','BM-Text','BM-TextMed','BM-Italic','BM-Head','BM-Small','BM-ItalicMed','Sans-Semi','Sans-Reg','Sans-Med','BM-Head600','BM-ItalicSm']:
    pdfmetrics.registerFont(TTFont(n, os.path.join(FD, n+'.ttf')))
INK = HexColor('#1C1B1A'); COPPER = HexColor('#A9582F'); COPPER_L = HexColor('#C68A5E')
PAPER = HexColor('#FFFFFF'); SOFT = HexColor('#F7F3EE'); MUTED = HexColor('#6E655C'); LINE = HexColor('#E6DED5')
MESSENGER = 'https://m.me/61587592953067'
EMAIL = 'gingerandgleam@gmail.com'
SEAL = json.load(open(os.path.join(os.path.dirname(__file__), 'seal.json')))

def _path(c, curves, x0, y0, s):
    p = c.beginPath()
    T = lambda x, y: (x0 + x*s, y0 - y*s)   # image y grows down
    for cv in curves:
        p.moveTo(*T(*cv['start']))
        for sg in cv['segs']:
            if sg[0] == 'L':
                p.lineTo(*T(sg[1], sg[2])); p.lineTo(*T(sg[3], sg[4]))
            else:
                p.curveTo(*T(sg[1], sg[2]), *T(sg[3], sg[4]), *T(sg[5], sg[6]))
        p.close()
    return p

def seal(c, cx, cy, d, ink=INK, star=COPPER):
    """Draw the vector seal centered at (cx, cy) with diameter-ish width d (points)."""
    s = d / SEAL['size']; x0 = cx - d/2; y0 = cy + d/2
    c.saveState()
    c.setFillColor(ink); c.drawPath(_path(c, SEAL['ink'], x0, y0, s), fill=1, stroke=0, fillMode=FILL_EVEN_ODD)
    c.setFillColor(star); c.drawPath(_path(c, SEAL['star'], x0, y0, s), fill=1, stroke=0, fillMode=FILL_EVEN_ODD)
    c.restoreState()

def star4(c, cx, cy, r, color=COPPER):
    """Four-point copper sparkle like the seal's stars."""
    c.saveState(); c.setFillColor(color)
    p = c.beginPath(); k = 0.18*r
    p.moveTo(cx, cy+r)
    p.curveTo(cx+k*0.4, cy+k, cx+k, cy+k*0.4, cx+r, cy)
    p.curveTo(cx+k, cy-k*0.4, cx+k*0.4, cy-k, cx, cy-r)
    p.curveTo(cx-k*0.4, cy-k, cx-k, cy-k*0.4, cx-r, cy)
    p.curveTo(cx-k, cy+k*0.4, cx-k*0.4, cy+k, cx, cy+r)
    p.close(); c.drawPath(p, fill=1, stroke=0); c.restoreState()

def qr(c, x, y, size, data=MESSENGER, color=INK, bg=PAPER, quiet=True):
    """Vector QR, bottom-left at (x, y), total size incl. 4-module quiet zone if quiet."""
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    q.add_data(data); q.make(fit=True); m = q.get_matrix(); n = len(m)
    border = 4 if quiet else 0; mod = size / (n + 2*border)
    c.saveState(); c.setFillColor(bg); c.rect(x, y, size, size, fill=1, stroke=0)
    c.setFillColor(color)
    for r, row in enumerate(m):
        run = None
        for col, v in enumerate(row + [False]):
            if v and run is None: run = col
            if not v and run is not None:
                c.rect(x + (border+run)*mod, y + size - (border+r+1)*mod, (col-run)*mod + 0.01, mod + 0.01, fill=1, stroke=0)
                run = None
    c.restoreState()

def ctext(c, x, y, text, font, size, color=INK, tracking=0):
    c.saveState(); c.setFillColor(color)
    if tracking:
        t = c.beginText(); t.setFont(font, size); t.setCharSpace(tracking)
        w = pdfmetrics.stringWidth(text, font, size) + tracking*(len(text)-1)
        t.setTextOrigin(x - w/2, y); t.textOut(text); c.drawText(t)
    else:
        c.setFont(font, size); c.drawCentredString(x, y, text)
    c.restoreState()

def width(text, font, size, tracking=0):
    return pdfmetrics.stringWidth(text, font, size) + tracking*(len(text)-1)
