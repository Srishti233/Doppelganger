"""The 'look' part. The avatar is always faceless. A photo in data/images/ only sets three colors
(hair, head tone, clothing); the photo itself is never stored or sent anywhere."""
from . import config


def photo():
    for p in sorted(config.IMAGES.glob("*")):
        if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp"):
            return p
    return None


def palette():
    p = photo()
    if not p:
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    im = Image.open(p).convert("RGB")
    im.thumbnail((120, 120))
    w, h = im.size

    def avg(box):
        r, g, b = im.crop(box).resize((1, 1), Image.BILINEAR).getpixel((0, 0))
        return "#%02x%02x%02x" % (r, g, b)

    return {
        "hair": avg((int(w * .3), 0, int(w * .7), int(h * .12))),
        "head": avg((int(w * .38), int(h * .2), int(w * .62), int(h * .4))),
        "body": avg((int(w * .3), int(h * .65), int(w * .7), h)),
    }
