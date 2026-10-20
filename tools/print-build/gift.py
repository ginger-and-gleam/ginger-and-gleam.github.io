from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
import gglib as g, subprocess
OUT = '/home/claude/gg-push/print'
W, H = 7*inch, 5*inch

def cert(c, ox, oy, fields=True):
    c.saveState(); c.translate(ox, oy)
    c.setFillColor(g.PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
    # double hairline frame in copper
    c.setStrokeColor(g.COPPER); c.setLineWidth(0.9); c.rect(0.22*inch, 0.22*inch, W-0.44*inch, H-0.44*inch)
    c.setLineWidth(0.35); c.rect(0.28*inch, 0.28*inch, W-0.56*inch, H-0.56*inch)
    # left column: seal + title
    g.seal(c, 1.55*inch, H-1.45*inch, 1.75*inch)
    g.ctext(c, 1.55*inch, H-2.62*inch, 'A GIFT CERTIFICATE', 'Sans-Semi', 6.4, g.COPPER, tracking=1.3)
    g.ctext(c, 1.55*inch, H-2.98*inch, 'The First Visit', 'BM-Head600', 21)
    lines = simpleSplit('A deep clean that brings a home to baseline: baseboards, door frames, ceiling fans, vents, and grout. Regular visits keep it there.', 'BM-ItalicSm', 8.6, 2.25*inch)
    y = H-3.28*inch
    for ln in lines: g.ctext(c, 1.55*inch, y, ln, 'BM-ItalicSm', 8.6, g.MUTED); y -= 11.2
    # divider
    c.setStrokeColor(g.LINE); c.setLineWidth(0.6); c.line(2.95*inch, 0.6*inch, 2.95*inch, H-0.6*inch)
    # right column: fields
    x0, x1 = 3.25*inch, W-0.55*inch
    rows = [('For', 'for'), ('From', 'from'), ('A home of up to', 'size'), ('Amount', 'amount')]
    y = H-0.95*inch
    for label, key in rows:
        c.setFillColor(g.MUTED); c.setFont('Sans-Med', 6.6); c.drawString(x0, y+12, label.upper())
        c.setStrokeColor(g.INK); c.setLineWidth(0.4); c.line(x0, y, x1, y)
        if fields:
            c.acroForm.textfield(name=key, x=x0, y=y+1, width=x1-x0, height=14, borderWidth=0, fillColor=None,
                                 borderColor=None, textColor=g.INK, fontName='Times-Italic', fontSize=11, forceBorder=False)
        y -= 0.52*inch
    # message line
    c.setFillColor(g.MUTED); c.setFont('Sans-Med', 6.6); c.drawString(x0, y+12, 'A NOTE')
    c.line(x0, y, x1, y); c.line(x0, y-0.3*inch, x1, y-0.3*inch)
    if fields:
        c.acroForm.textfield(name='note1', x=x0, y=y+1, width=x1-x0, height=14, borderWidth=0, fillColor=None, borderColor=None, textColor=g.INK, fontName='Times-Italic', fontSize=10)
        c.acroForm.textfield(name='note2', x=x0, y=y-0.3*inch+1, width=x1-x0, height=14, borderWidth=0, fillColor=None, borderColor=None, textColor=g.INK, fontName='Times-Italic', fontSize=10)
    # booking block
    qs = 0.82*inch; qx = x1-qs; qy = 0.48*inch
    g.qr(c, qx, qy, qs)
    c.setFillColor(g.INK); c.setFont('Sans-Reg', 8.4); c.drawString(x0, qy+0.58*inch, 'To book, scan to message us,')
    c.setFont('Sans-Reg', 8.4); c.drawString(x0, qy+0.43*inch, 'or write to ' + g.EMAIL)
    c.setFillColor(g.MUTED); c.setFont('Sans-Med', 6.2); c.drawString(x0, qy+0.2*inch, 'NO.  GG-')
    c.setStrokeColor(g.INK); c.line(x0+0.42*inch, qy+0.19*inch, x0+1.25*inch, qy+0.19*inch)
    if fields:
        c.acroForm.textfield(name='number', x=x0+0.42*inch, y=qy+0.2*inch, width=0.83*inch, height=11, borderWidth=0, fillColor=None, borderColor=None, textColor=g.INK, fontName='Helvetica', fontSize=8)
    c.restoreState()

def terms(c, ox, oy):
    c.saveState(); c.translate(ox, oy)
    c.setFillColor(g.PAPER); c.rect(0, 0, W, H, fill=1, stroke=0)
    g.star4(c, W/2, H-0.85*inch, 7)
    g.ctext(c, W/2, H-1.25*inch, 'How this gift works', 'BM-Head600', 17)
    t = ['Message us with the city and a good time for a fifteen-minute walk-through. We will confirm a date for the First Visit.',
         'This certificate covers the First Visit for a home up to the size shown. If the home is larger, the difference is quoted at the walk-through. If it is smaller, the remainder goes toward the next visit.',
         'Inside the oven and inside the refrigerator are add-ons, quoted at the walk-through.',
         'For homes within about thirty minutes of Hutto. If we are not able to take on the home, the full amount goes back to the giver.',
         'This certificate does not expire.']
    y = H-1.65*inch
    for para in t:
        for ln in simpleSplit(para, 'Sans-Reg', 8.4, W-1.7*inch):
            g.ctext(c, W/2, y, ln, 'Sans-Reg', 8.4, g.INK); y -= 12.4
        y -= 6
    g.ctext(c, W/2, 0.5*inch, 'GINGER & GLEAM CLEANING CO.  ·  ' + g.EMAIL.upper(), 'Sans-Semi', 5.8, g.COPPER, tracking=1.0)
    c.restoreState()

# 1) 7x5 two-page fillable (front + back) for print shops and for typing names before sending
c = canvas.Canvas(f'{OUT}/GG-gift-certificate-7x5-fillable.pdf', pagesize=(W, H))
c.setTitle('Ginger & Gleam gift certificate'); cert(c, 0, 0); c.showPage(); terms(c, 0, 0); c.showPage(); c.save()
# 2) letter sheet with crop marks for home printing on cardstock (front page, then back page)
LW, LH = letter
def crops(c, ox, oy):
    c.setStrokeColor(g.MUTED); c.setLineWidth(0.3)
    for (x, y) in [(ox, oy), (ox+W, oy), (ox, oy+H), (ox+W, oy+H)]:
        dx = -1 if x == ox else 1; dy = -1 if y == oy else 1
        c.line(x+dx*0.08*inch, y, x+dx*0.35*inch, y); c.line(x, y+dy*0.08*inch, x, y+dy*0.35*inch)
c = canvas.Canvas(f'{OUT}/GG-gift-certificate-letter-home-print.pdf', pagesize=letter)
ox, oy = (LW-W)/2, (LH-H)/2
cert(c, ox, oy, fields=True); crops(c, ox, oy)
c.setFillColor(g.MUTED); c.setFont('Sans-Reg', 7); c.drawCentredString(LW/2, 0.5*inch, 'Print at 100% (Actual size) on 80-110 lb cardstock, then trim on the marks. Page 2 is the back.')
c.showPage(); terms(c, ox, oy); crops(c, ox, oy); c.showPage(); c.save()
subprocess.run(['pdftoppm', '-r', '300', '-png', f'{OUT}/GG-gift-certificate-7x5-fillable.pdf', '/home/claude/gg-push/build/gift'], check=True)
