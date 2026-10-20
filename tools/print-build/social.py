from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.utils import simpleSplit
import gglib as g, subprocess, os
W, H = 4*inch, 5*inch   # 4:5, rendered at 270 dpi -> 1080x1350
OUT = '/home/claude/gg-push/social'

def para(c, text, font, size, y, color=g.INK, lead=1.25, maxw=3.1*inch):
    text = text
    lines = simpleSplit(text, font, size, maxw)
    for i, ln in enumerate(lines):
        g.ctext(c, W/2, y - i*size*lead, ln, font, size, color)
    return y - len(lines)*size*lead

def page(name, bg, draw):
    pdf = f'{OUT}/{name}.pdf'
    c = canvas.Canvas(pdf, pagesize=(W, H)); c.setFillColor(bg); c.rect(0, 0, W, H, fill=1, stroke=0)
    draw(c); c.showPage(); c.save()
    subprocess.run(['pdftoppm', '-r', '270', '-png', '-singlefile', pdf, f'{OUT}/{name}'], check=True)
    subprocess.run(['convert', f'{OUT}/{name}.png', '-quality', '92', f'{OUT}/{name}.jpg'], check=True)
    os.remove(pdf); os.remove(f'{OUT}/{name}.png')

def intro(c):
    g.seal(c, W/2, H*0.60, 2.55*inch)
    g.ctext(c, W/2, H*0.24, 'The same careful hands, every visit.', 'BM-ItalicMed', 15)
    g.ctext(c, W/2, H*0.15, 'HUTTO  ·  ROUND ROCK  ·  PFLUGERVILLE  ·  GEORGETOWN', 'Sans-Med', 6.0, g.MUTED, tracking=0.9)

def services(c):
    g.star4(c, W/2, H*0.83, 9)
    y = H*0.70
    for i, t in enumerate(['Weekly & biweekly care', 'Deep cleans', 'Move-in & move-out']):
        g.ctext(c, W/2, y, t, 'BM-Head', 21)
        if i < 2: g.star4(c, W/2, y - 0.33*inch, 3.2, g.COPPER)
        y -= 0.72*inch
    g.ctext(c, W/2, H*0.17, 'Message us for a walk-through and a clear price.', 'BM-ItalicMed', 10.5, g.MUTED)
    g.ctext(c, W/2, H*0.10, 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 6.2, g.COPPER, tracking=1.3)

def name(c):
    g.seal(c, W/2, H*0.60, 2.55*inch, ink=g.COPPER_L, star=g.COPPER_L)
    g.ctext(c, W/2, H*0.235, 'Ginger, for warmth.', 'BM-ItalicMed', 15, g.COPPER_L)
    g.ctext(c, W/2, H*0.235 - 22, 'Gleam, for the finish.', 'BM-ItalicMed', 15, g.COPPER_L)

def careful(c):
    g.star4(c, W/2, H*0.72, 9)
    para(c, 'Residential cleaning for homes that deserve a careful hand.', 'BM-Head', 24, H*0.60, lead=1.22, maxw=3.0*inch)
    g.ctext(c, W/2, H*0.16, 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 6.2, g.COPPER, tracking=1.3)

def noted(c):
    g.star4(c, W/2, H*0.74, 9)
    y = H*0.62
    for ln in ["If you'd ever like", 'something done', 'differently,', 'just say so.']:
        g.ctext(c, W/2, y, ln, 'BM-Head', 22); y -= 22*1.22
    g.ctext(c, W/2, y - 14, "It's noted for every visit after.", 'BM-ItalicMed', 13, g.MUTED)
    g.ctext(c, W/2, H*0.12, 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 6.2, g.COPPER, tracking=1.3)

def holiday(c):
    g.ctext(c, W/2, H*0.78, 'THE HOLIDAY FIRST VISIT', 'Sans-Semi', 6.8, g.COPPER, tracking=1.5)
    g.star4(c, W/2, H*0.70, 8)
    g.ctext(c, W/2, H*0.555, 'Before the', 'BM-Head', 34)
    g.ctext(c, W/2, H*0.555 - 40, 'guests arrive.', 'BM-Head', 34)
    para(c, 'Baseboards, door frames, ceiling fans, vents, and grout, brought to baseline.', 'BM-ItalicMed', 11, H*0.30, g.MUTED, maxw=2.9*inch)
    g.ctext(c, W/2, H*0.10, 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 6.2, g.COPPER, tracking=1.3)

def newyear(c):
    g.ctext(c, W/2, H*0.78, 'A NEW-YEAR RESET', 'Sans-Semi', 6.8, g.COPPER, tracking=1.5)
    g.star4(c, W/2, H*0.70, 8)
    para(c, 'Start the year in a home that feels finished.', 'BM-Head', 28, H*0.57, lead=1.2, maxw=3.0*inch)
    g.ctext(c, W/2, H*0.10, 'GINGER & GLEAM CLEANING CO.', 'Sans-Semi', 6.2, g.COPPER, tracking=1.3)

for n, bg, f in [('01-seal-intro', g.PAPER, intro), ('02-services', g.SOFT, services), ('03-the-name', g.INK, name),
                 ('04-careful-hand', g.PAPER, careful), ('05-done-differently', g.PAPER, noted),
                 ('06-holiday-first-visit', g.SOFT, holiday), ('08-new-year-reset', g.SOFT, newyear)]:
    page(n, bg, f)
print(sorted(os.listdir(OUT)))
