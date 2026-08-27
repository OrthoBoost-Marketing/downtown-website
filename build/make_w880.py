"""Generate 880px-wide derivatives of the client photographs.

Every photo slot on the site displays at ~440px CSS or less, so an 880px source
covers a 2x device pixel ratio exactly. The originals stay untouched in
assets/photos/ (they are still what og:image and the JSON-LD "image" point at);
the derivatives land in assets/photos/w880/ and are what every <img> and
<link rel=preload> uses.

Aspect ratio is preserved exactly and nothing is cropped.
Target: <=200KB, aiming near 120KB. Quality is stepped down per file until the
budget is met, so a busy frame is not forced to the same number as a plain one.
"""
import io
import os
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "photos")
OUT = os.path.join(SRC, "w880")
TARGET_W = 880
BUDGET = 140 * 1024          # aim
HARD_CAP = 200 * 1024        # must not exceed
FLOOR_Q = 76                 # below this, faces start to show artefacts

os.makedirs(OUT, exist_ok=True)


def derive(name):
    sp = os.path.join(SRC, name)
    op = os.path.join(OUT, name)
    before = os.path.getsize(sp)
    im = Image.open(sp)
    im = im.convert("RGB")
    w, h = im.size
    if w > TARGET_W:
        nh = int(round(h * TARGET_W / float(w)))
        im = im.resize((TARGET_W, nh), Image.LANCZOS)
    # Step quality down only as far as the budget needs. FLOOR_Q is where visible
    # JPEG artefacting starts on these portraits, so a frame that cannot reach the
    # 140KB aim is allowed to sit between the aim and the 200KB hard cap rather
    # than be crushed. Faces are the subject in six of the eight frames.
    chosen = None
    for q in (84, 82, 80, 78, 76, 72, 68, 64):
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=q, optimize=True, progressive=True,
                subsampling="4:2:0")
        data = buf.getvalue()
        chosen = (q, data)
        if len(data) <= BUDGET:
            break
        if q <= FLOOR_Q and len(data) <= HARD_CAP:
            break
    q, data = chosen
    assert len(data) <= HARD_CAP, "%s still %d bytes" % (name, len(data))
    if len(data) >= before and im.size == (w, h):
        # Already at display size and already better compressed than we can do.
        # Copy the original byte for byte rather than re-encode it worse.
        data = open(sp, "rb").read()
        q = 0
    with open(op, "wb") as f:
        f.write(data)
    print("  %-18s %5dx%-5d %7d B  ->  %4dx%-5d %7d B  q%d  (-%.0f%%)"
          % (name, w, h, before, im.size[0], im.size[1], len(data), q,
             100.0 * (before - len(data)) / before))
    return before, len(data), im.size


def main():
    names = sorted(n for n in os.listdir(SRC) if n.lower().endswith(".jpg"))
    tb = ta = 0
    for n in names:
        b, a, _ = derive(n)
        tb += b
        ta += a
    print("\n  total %d B -> %d B  (-%.0f%%)" % (tb, ta, 100.0 * (tb - ta) / tb))


if __name__ == "__main__":
    main()
