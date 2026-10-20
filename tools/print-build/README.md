# Print and social build scripts

Rebuild the files in /print and /social. Python 3 with reportlab, qrcode, fonttools, opencv-python-headless, potracer.

1. Fonts: download Bodoni Moda and Inter variable TTFs from github.com/google/fonts (ofl/bodonimoda, ofl/inter) and make static instances with fontTools.varLib.instancer (names and axis values are in gglib.py's font list; opsz/wght used: Display 72/400, Sub 28/400, Text 11/400, TextMed 11/500, Italic 28/400, Head 24/500, Small 8/500, ItalicMed 16/450, Head600 14/600, ItalicSm 9/500; Inter 14 at 400/500/600). Point FD in gglib.py at that folder.
2. seal.json is the vector trace of seal-light.png (seal_vec.py rebuilds it).
3. Run printfiles.py, gift.py, social.py. Output paths are at the top of each script.

Contact details live in gglib.py (MESSENGER, EMAIL). No phone number anywhere.
