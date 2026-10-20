from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
import gglib as g, subprocess
OUT = '/home/claude/gg-push/print'
B = 0.125*inch

def lines_c(c, cx, y, text, font, size, maxw, color=g.INK, lead=1.25):
    for ln in simpleSplit(text, font, size, maxw):
        g.ctext(c, cx, y, ln, font, size, color); y -= size*lead
    return y

# ---------- Door hanger 4.25 x 11 trim, 0.125 bleed ----------
TW, TH = 4.25*inch, 11*inch; PW, PH = TW+2*B, TH+2*B
cx = PW/2
def top(y_from_top): return B + TH - y_from_top   # y measured from trim top
c = canvas.Canvas(f'{OUT}/GG-door-hanger-4.25x11-print.pdf', pagesize=(PW, PH), initialFontName='Sans-Reg'); c.setTitle('Ginger & Gleam door hanger')
# front
c.setFillColor(g.PAPER); c.rect(0, 0, PW, PH, fill=1, stroke=0)
g.seal(c, cx, top(4.55*inch), 2.55*inch)
lines_c(c, cx, top(6.55*inch), 'Residential cleaning for homes that deserve a careful hand.', 'BM-Head600', 16.5, 3.3*inch, lead=1.22)
g.star4(c, cx, top(7.85*inch), 6)
lines_c(c, cx, top(8.4*inch), 'The same careful hands, every visit.', 'BM-ItalicSm', 11.5, 3.4*inch, g.MUTED)
g.ctext(c, cx, top(10.35*inch), 'HUTTO  ·  ROUND ROCK  ·  PFLUGERVILLE  ·  GEORGETOWN', 'Sans-Semi', 5.6, g.COPPER, tracking=0.7)
c.showPage()
# back
c.setFillColor(g.SOFT); c.rect(0, 0, PW, PH, fill=1, stroke=0)
g.ctext(c, cx, top(3.35*inch), 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 6.4, g.COPPER, tracking=1.2)
y = top(3.95*inch)
for i, t in enumerate(['Weekly & biweekly care', 'Deep cleans', 'Move-in & move-out']):
    g.ctext(c, cx, y, t, 'BM-Head600', 17)
    if i < 2: g.star4(c, cx, y - 0.27*inch, 3.2)
    y -= 0.56*inch
y = lines_c(c, cx, top(5.85*inch), 'Message us with the city and roughly how big the home is. We usually send a price range the same day, and come by for a walk-through that week.', 'Sans-Reg', 8.6, 3.35*inch, lead=1.4)
qs = 1.6*inch
g.ctext(c, cx, top(7.45*inch), 'Scan to message us', 'BM-Head600', 13)
g.qr(c, cx - qs/2, top(7.6*inch) - qs, qs)
g.ctext(c, cx, top(9.55*inch), g.EMAIL, 'Sans-Med', 8.8)
g.ctext(c, cx, top(10.35*inch), 'GINGER-AND-GLEAM.GITHUB.IO', 'Sans-Semi', 5.6, g.MUTED, tracking=0.9)
c.showPage(); c.save()

# ---------- Leave-behind card 4 x 6 portrait, 0.125 bleed ----------
TW, TH = 4*inch, 6*inch; PW, PH = TW+2*B, TH+2*B; cx = PW/2
def top(y_from_top): return B + TH - y_from_top
c = canvas.Canvas(f'{OUT}/GG-leave-behind-card-4x6-print.pdf', pagesize=(PW, PH), initialFontName='Sans-Reg'); c.setTitle('Ginger & Gleam leave-behind card')
c.setFillColor(g.PAPER); c.rect(0, 0, PW, PH, fill=1, stroke=0)
g.seal(c, cx, top(1.35*inch), 1.65*inch)
g.ctext(c, cx, top(2.75*inch), 'Your home was cared for today.', 'BM-Head600', 15)
c.setStrokeColor(g.LINE); c.setLineWidth(0.6)
for yy in [3.55, 4.05, 4.55]:
    c.line(B + 0.55*inch, top(yy*inch), B + TW - 0.55*inch, top(yy*inch))
g.star4(c, cx, top(5.35*inch), 5)
c.showPage()
c.setFillColor(g.SOFT); c.rect(0, 0, PW, PH, fill=1, stroke=0)
g.star4(c, cx, top(0.75*inch), 5)
y = top(1.2*inch)
for ln in ["If you'd ever like something", 'done differently, just say so.']:
    g.ctext(c, cx, y, ln, 'BM-Head600', 13); y -= 17
g.ctext(c, cx, y - 4, "It's noted for every visit after.", 'BM-ItalicSm', 10.5, g.MUTED)
lines_c(c, cx, top(2.65*inch), 'Know someone who would love a home cared for this way? This is how to find us.', 'Sans-Reg', 8.2, 3.0*inch, lead=1.4)
qs = 1.25*inch
g.qr(c, cx - qs/2, top(3.15*inch) - qs, qs)
g.ctext(c, cx, top(4.75*inch), g.EMAIL, 'Sans-Med', 8.4)
g.ctext(c, cx, top(5.45*inch), 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 6, g.COPPER, tracking=1.2)
c.showPage(); c.save()

# ---------- Yard sign 24 x 18 landscape (no bleed; white) ----------
PW, PH = 24*inch, 18*inch
c = canvas.Canvas(f'{OUT}/GG-yard-sign-24x18-print.pdf', pagesize=(PW, PH), initialFontName='Sans-Reg'); c.setTitle('Ginger & Gleam yard sign')
c.setFillColor(g.PAPER); c.rect(0, 0, PW, PH, fill=1, stroke=0)
lx = 6.6*inch
g.ctext(c, lx, 16.3*inch, 'THIS HOME IS CARED FOR BY', 'Sans-Semi', 30, g.COPPER, tracking=7)
g.seal(c, lx, 10.6*inch, 9.4*inch)
name = 'Ginger & Gleam'; sz = 100
while g.width(name, 'BM-Head600', sz) > 11.3*inch: sz -= 1
g.ctext(c, lx, 3.35*inch, name, 'BM-Head600', sz)
g.ctext(c, lx, 1.65*inch, 'CLEANING CO.', 'Sans-Semi', 34, g.COPPER, tracking=9)
c.setStrokeColor(g.LINE); c.setLineWidth(2); c.line(13.2*inch, 2*inch, 13.2*inch, 16*inch)
rx = 18.6*inch; qs = 7.6*inch
g.ctext(c, rx, 15.2*inch, 'Scan to message us', 'BM-Head600', 62)
g.qr(c, rx - qs/2, 6.5*inch, qs)
g.ctext(c, rx, 4.6*inch, 'for a walk-through and a clear price', 'Sans-Reg', 34, g.MUTED)
g.ctext(c, rx, 2.6*inch, g.EMAIL, 'Sans-Med', 38)
c.showPage(); c.save()
print('name size', sz)
for f in ['GG-door-hanger-4.25x11-print', 'GG-leave-behind-card-4x6-print', 'GG-yard-sign-24x18-print']:
    subprocess.run(['pdftoppm', '-r', '40' if 'yard' in f else '110', '-png', f'{OUT}/{f}.pdf', f'/home/claude/gg-push/build/prev-{f}'], check=True)
