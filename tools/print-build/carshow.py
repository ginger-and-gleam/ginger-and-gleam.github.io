from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
from reportlab.lib.colors import HexColor
import gglib as g, subprocess, os
OUT = '/home/claude/gg-push/print/carshow'
PRE = '/home/claude/gg-push/build/carshow'
B = 0.125*inch
CREAM = HexColor('#F7F3EE')

def page(c, PW, PH, bg):
    c.setFillColor(bg); c.rect(0, 0, PW, PH, fill=1, stroke=0)

def lines(c, x, y, text, font, size, maxw, color=g.INK, lead=1.3, align='left'):
    for ln in simpleSplit(text, font, size, maxw):
        c.setFillColor(color); c.setFont(font, size)
        if align == 'center': c.drawCentredString(x, y, ln)
        else: c.drawString(x, y, ln)
        y -= size*lead
    return y

def tracked(c, x, y, text, font, size, color, tracking, align='left'):
    w = g.width(text, font, size, tracking)
    c.saveState()
    t = c.beginText(); t.setFont(font, size); t.setCharSpace(tracking); t.setFillColor(color)
    t.setTextOrigin(x - (w/2 if align == 'center' else 0), y); t.textOut(text); c.drawText(t)
    c.restoreState()

AREA = 'HUTTO · ROUND ROCK · PFLUGERVILLE · GEORGETOWN'

# ---------------- A: Concours — 3.5 x 2 black business card ----------------
TW, TH = 3.5*inch, 2*inch; PW, PH = TW+2*B, TH+2*B
c = canvas.Canvas(f'{OUT}/A-concours-business-card-3.5x2.pdf', pagesize=(PW, PH), initialFontName='Sans-Reg')
c.setTitle('Ginger & Gleam car-show card A (Concours)')
page(c, PW, PH, g.INK)
g.seal(c, PW/2, PH/2, 1.52*inch, ink=g.COPPER_L, star=g.COPPER_L)
c.showPage()
page(c, PW, PH, CREAM)
x0 = B + 0.2*inch; top = B + TH - 0.24*inch
tracked(c, x0, top - 6, 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 5.4, g.COPPER, 0.9)
y = top - 24
for ln in ['Your car gets the', 'hand finish.', 'Your home should too.']:
    c.setFillColor(g.INK); c.setFont('BM-Head600', 11.2); c.drawString(x0, y, ln); y -= 13.4
y -= 5
c.setFillColor(g.MUTED); c.setFont('Sans-Reg', 6.1)
c.drawString(x0, y, 'Weekly & biweekly care · Deep cleans · Move-outs'); y -= 8.6
c.drawString(x0, y, 'Homes near Hutto, Round Rock, Pflugerville'); y -= 8.6
c.drawString(x0, y, '& Georgetown'); y -= 11.5
c.setFillColor(g.INK); c.setFont('Sans-Med', 6.4); c.drawString(x0, y, g.EMAIL)
qs = 0.86*inch; qx = B + TW - 0.2*inch - qs; qy = B + 0.42*inch
g.qr(c, qx, qy, qs, bg=CREAM)
tracked(c, qx + qs/2, qy - 9, 'SCAN TO MESSAGE US', 'Sans-Semi', 4.6, g.COPPER, 0.6, align='center')
c.showPage(); c.save()

# ---------------- B: Window Sticker — 4 x 6 portrait card ----------------
TW, TH = 4*inch, 6*inch; PW, PH = TW+2*B, TH+2*B
L, R = B + 0.28*inch, B + TW - 0.28*inch
def T(v): return B + TH - v
c = canvas.Canvas(f'{OUT}/B-window-sticker-card-4x6.pdf', pagesize=(PW, PH), initialFontName='Sans-Reg')
c.setTitle('Ginger & Gleam car-show card B (Window Sticker)')
page(c, PW, PH, g.PAPER)
band = 1.25*inch
c.setFillColor(g.INK); c.rect(0, T(band), PW, band + B, fill=1, stroke=0)
g.seal(c, L + 0.5*inch, T(band/2), 0.98*inch, ink=g.COPPER_L, star=g.COPPER_L)
tx = L + 1.17*inch
tracked(c, tx, T(0.43*inch), 'HOME CARE SPECIFICATION', 'Sans-Semi', 6.2, g.COPPER_L, 1.1)
c.setFillColor(HexColor('#F7F3EE')); c.setFont('BM-Head600', 21); c.drawString(tx, T(0.77*inch), 'Y'); c.drawString(tx + g.width('Y','BM-Head600',21) - 2.2, T(0.77*inch), 'our home,')
c.drawString(tx, T(1.06*inch), 'detailed.')
c.setStrokeColor(g.COPPER); c.setLineWidth(1.4); c.line(0, T(band) - 0.7, PW, T(band) - 0.7)
rows = [('MODEL', 'Weekly or biweekly home care'),
        ('FINISH', 'By hand, top to bottom'),
        ('FIRST VISIT', 'Baseboards, door frames, ceiling fans, vents, and grout, brought to baseline'),
        ('CREW', 'The same careful hands, every visit'),
        ('ALSO AVAILABLE', 'Deep cleans · Move-in & move-out'),
        ('SERVICE AREA', 'Hutto · Round Rock · Pflugerville · Georgetown'),
        ('RESPONSE', 'A price range, usually the same day, and a walk-through that week.')]
lx, vx = L, L + 1.12*inch; vw = R - vx
y = T(band + 0.34*inch)
c.setStrokeColor(g.LINE); c.setLineWidth(0.6)
for i, (lab, val) in enumerate(rows):
    tracked(c, lx, y, lab, 'Sans-Semi', 5.6, g.COPPER, 0.8)
    ny = lines(c, vx, y - 0.5, val, 'Sans-Reg', 8.1, vw, g.INK, lead=1.32)
    y = ny - 6.5
    c.line(L, y + 3.2, R, y + 3.2)
    y -= 7
# price + QR block
by = B + 0.38*inch; bh = 1.32*inch
c.setStrokeColor(g.INK); c.setLineWidth(0.9); c.rect(L, by, R - L, bh, fill=0, stroke=1)
qs = 1.08*inch; qx = R - 0.12*inch - qs; qy = by + (bh - qs)/2
g.qr(c, qx, qy, qs)
tracked(c, L + 0.14*inch, by + bh - 0.27*inch, 'PRICE', 'Sans-Semi', 5.6, g.COPPER, 0.8)
c.setFillColor(g.INK); c.setFont('BM-Head600', 10.5); c.drawString(L + 0.14*inch, by + bh - 0.47*inch, 'In writing,'); c.drawString(L + 0.14*inch, by + bh - 0.47*inch - 12.8, 'after we see the home.')
c.setFillColor(g.INK); c.setFont('Sans-Semi', 7); c.drawString(L + 0.14*inch, by + 0.33*inch, 'Scan to message us')
c.setFillColor(g.MUTED); c.setFont('Sans-Reg', 6.6); c.drawString(L + 0.14*inch, by + 0.18*inch, g.EMAIL)
tracked(c, PW/2, B + 0.17*inch, 'GINGER & GLEAM CLEANING CO.  ·  GINGER-AND-GLEAM.GITHUB.IO', 'Sans-Semi', 4.6, g.MUTED, 0.6, align='center')
c.showPage()
# back: simple seal on black
page(c, PW, PH, g.INK)
g.seal(c, PW/2, PH/2 + 0.25*inch, 2.5*inch, ink=g.COPPER_L, star=g.COPPER_L)
tracked(c, PW/2, B + 1.0*inch, 'RESIDENTIAL CLEANING FOR HOMES', 'Sans-Semi', 6, g.COPPER_L, 1.2, align='center')
tracked(c, PW/2, B + 0.82*inch, 'THAT DESERVE A CAREFUL HAND', 'Sans-Semi', 6, g.COPPER_L, 1.2, align='center')
c.showPage(); c.save()

# ---------------- C: The Care — 2.5 x 2.5 cream square ----------------
TW, TH = 2.5*inch, 2.5*inch; PW, PH = TW+2*B, TH+2*B; cx = PW/2
def T(v): return B + TH - v
c = canvas.Canvas(f'{OUT}/C-square-card-2.5x2.5.pdf', pagesize=(PW, PH), initialFontName='Sans-Reg')
c.setTitle('Ginger & Gleam car-show card C (The Care)')
page(c, PW, PH, CREAM)
c.setStrokeColor(g.COPPER); c.setLineWidth(0.5)
c.rect(B + 0.16*inch, B + 0.16*inch, TW - 0.32*inch, TH - 0.32*inch)
g.seal(c, cx, T(0.86*inch), 1.12*inch)
c.setFillColor(g.INK); c.setFont('BM-ItalicMed', 10.2)
c.drawCentredString(cx, T(1.73*inch), 'The care you give the car,')
c.drawCentredString(cx, T(1.73*inch) - 13, 'given to the home.')
c.showPage()
page(c, PW, PH, g.PAPER)
c.setStrokeColor(g.COPPER); c.setLineWidth(0.5)
c.rect(B + 0.16*inch, B + 0.16*inch, TW - 0.32*inch, TH - 0.32*inch)
tracked(c, cx, T(0.36*inch), 'SCAN TO MESSAGE US', 'Sans-Semi', 5.2, g.COPPER, 0.8, align='center')
qs = 0.98*inch
g.qr(c, cx - qs/2, T(0.45*inch) - qs, qs)
c.setFillColor(g.INK); c.setFont('Sans-Med', 6.4); c.drawCentredString(cx, T(1.66*inch), g.EMAIL)
c.setFillColor(g.MUTED); c.setFont('Sans-Reg', 5.7)
c.drawCentredString(cx, T(1.86*inch), 'Weekly & biweekly care · Deep cleans · Move-outs')
c.drawCentredString(cx, T(1.99*inch), 'Hutto · Round Rock · Pflugerville · Georgetown')
c.showPage(); c.save()

for f in ['A-concours-business-card-3.5x2', 'B-window-sticker-card-4x6', 'C-square-card-2.5x2.5']:
    subprocess.run(['pdftoppm', '-r', '300', '-png', f'{OUT}/{f}.pdf', f'{PRE}/{f}'], check=True)
print(sorted(os.listdir(PRE)))
