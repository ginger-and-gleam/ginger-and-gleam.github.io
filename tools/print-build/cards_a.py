from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import gglib as g, subprocess, os
OUT = '/home/claude/gg-push/print/carshow/A-options'
PRE = '/home/claude/gg-push/build/carshowA'
B = 0.125*inch
CREAM = HexColor('#F7F3EE'); LIGHT = HexColor('#C9C1B8')

def page(c, PW, PH, bg):
    c.setFillColor(bg); c.rect(0, 0, PW, PH, fill=1, stroke=0)
def tracked(c, x, y, text, font, size, color, tracking, align='left'):
    w = g.width(text, font, size, tracking)
    c.saveState(); t = c.beginText(); t.setFont(font, size); t.setCharSpace(tracking); t.setFillColor(color)
    t.setTextOrigin(x - (w/2 if align == 'center' else 0), y); t.textOut(text); c.drawText(t); c.restoreState()
def text(c, x, y, s, font, size, color, align='left'):
    c.setFillColor(color); c.setFont(font, size)
    (c.drawCentredString if align == 'center' else c.drawString)(x, y, s)

# ---------- A1 Classic: black front, cream back ----------
TW, TH = 3.5*inch, 2*inch; PW, PH = TW+2*B, TH+2*B
c = canvas.Canvas(f'{OUT}/A1-classic-3.5x2.pdf', pagesize=(PW, PH), initialFontName='Sans-Reg'); c.setTitle('Ginger & Gleam card A1 Classic')
page(c, PW, PH, g.INK); g.seal(c, PW/2, PH/2, 1.52*inch, ink=g.COPPER_L, star=g.COPPER_L); c.showPage()
page(c, PW, PH, CREAM)
x0 = B + 0.2*inch; top = B + TH - 0.26*inch
tracked(c, x0, top - 6, 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 5.4, g.COPPER, 0.9)
y = top - 26
for ln in ['Your car gets the', 'hand finish.', 'Your home should too.']:
    text(c, x0, y, ln, 'BM-Head600', 11.6, g.INK); y -= 14
y -= 7
text(c, x0, y, 'Weekly & biweekly care · Deep cleans · Move-outs', 'Sans-Reg', 6.1, g.MUTED); y -= 12
text(c, x0, y, g.EMAIL, 'Sans-Med', 6.6, g.INK)
qs = 0.88*inch; qx = B + TW - 0.2*inch - qs; qy = B + 0.4*inch
g.qr(c, qx, qy, qs, bg=CREAM)
tracked(c, qx + qs/2, qy - 9, 'SCAN TO MESSAGE US', 'Sans-Semi', 4.6, g.COPPER, 0.6, align='center')
c.showPage(); c.save()

# ---------- A2 All black: black both sides, QR on a cream tile ----------
c = canvas.Canvas(f'{OUT}/A2-all-black-3.5x2.pdf', pagesize=(PW, PH), initialFontName='Sans-Reg'); c.setTitle('Ginger & Gleam card A2 All black')
page(c, PW, PH, g.INK); g.seal(c, PW/2, PH/2, 1.52*inch, ink=g.COPPER_L, star=g.COPPER_L); c.showPage()
page(c, PW, PH, g.INK)
x0 = B + 0.2*inch; top = B + TH - 0.26*inch
tracked(c, x0, top - 6, 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 5.4, g.COPPER_L, 0.9)
y = top - 26
for ln in ["You’d never hand your", 'car to just anyone.', 'Your home deserves', 'the same.']:
    text(c, x0, y, ln, 'BM-Head600', 10.6, CREAM); y -= 12.8
y -= 6
text(c, x0, y, 'Weekly & biweekly care · Deep cleans · Move-outs', 'Sans-Reg', 6.1, LIGHT); y -= 11.5
text(c, x0, y, g.EMAIL, 'Sans-Med', 6.6, CREAM)
tile = 0.98*inch; tx = B + TW - 0.18*inch - tile; ty = B + 0.4*inch
c.setFillColor(CREAM); c.roundRect(tx, ty, tile, tile, 4, fill=1, stroke=0)
qs = 0.9*inch; g.qr(c, tx + (tile-qs)/2, ty + (tile-qs)/2, qs, bg=CREAM)
tracked(c, tx + tile/2, ty - 9, 'SCAN TO MESSAGE US', 'Sans-Semi', 4.6, g.COPPER_L, 0.6, align='center')
c.showPage(); c.save()

# ---------- A3 Vertical: 2 x 3.5 portrait ----------
TW, TH = 2*inch, 3.5*inch; PW, PH = TW+2*B, TH+2*B; cx = PW/2
def T(v): return B + TH - v
c = canvas.Canvas(f'{OUT}/A3-vertical-2x3.5.pdf', pagesize=(PW, PH), initialFontName='Sans-Reg'); c.setTitle('Ginger & Gleam card A3 Vertical')
page(c, PW, PH, g.INK)
g.seal(c, cx, T(1.45*inch), 1.5*inch, ink=g.COPPER_L, star=g.COPPER_L)
tracked(c, cx, T(2.75*inch), 'HAND-FINISHED HOME CARE', 'Sans-Semi', 5.4, g.COPPER_L, 1.0, align='center')
c.showPage()
page(c, PW, PH, CREAM)
tracked(c, cx, T(0.42*inch), 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 4.9, g.COPPER, 0.8, align='center')
text(c, cx, T(0.74*inch), 'Your home,', 'BM-Head600', 13, g.INK, 'center')
text(c, cx, T(0.74*inch) - 15.5, 'detailed by hand.', 'BM-Head600', 13, g.INK, 'center')
text(c, cx, T(1.24*inch), 'Weekly & biweekly care', 'Sans-Reg', 6.1, g.MUTED, 'center')
text(c, cx, T(1.24*inch) - 8.6, 'Deep cleans · Move-outs', 'Sans-Reg', 6.1, g.MUTED, 'center')
qs = 1.0*inch
g.qr(c, cx - qs/2, T(1.55*inch) - qs, qs, bg=CREAM)
tracked(c, cx, T(2.72*inch), 'SCAN TO MESSAGE US', 'Sans-Semi', 4.8, g.COPPER, 0.7, align='center')
text(c, cx, T(2.95*inch), g.EMAIL, 'Sans-Med', 6.4, g.INK, 'center')
c.showPage(); c.save()

for f in ['A1-classic-3.5x2', 'A2-all-black-3.5x2', 'A3-vertical-2x3.5']:
    subprocess.run(['pdftoppm', '-r', '300', '-png', f'{OUT}/{f}.pdf', f'{PRE}/{f}'], check=True)
print(sorted(os.listdir(PRE)))
