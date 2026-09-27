#!/usr/bin/env python3
"""Convert the source photo library into web-ready responsive assets.

Source photos live outside the repo (OneDrive) as 2-3 MB PNGs, HEICs and
QuickTime videos. None of that is servable, so this script normalises
everything into static/images/ as WebP at a few widths.

Re-run it whenever photos are added or replaced:

    python3 tools/build_assets.py

Requires: pillow, pillow-heif   (pip install -r requirements.txt)
"""
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageOps

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except ImportError:
    pillow_heif = None

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.environ.get(
    "NEOMI_PHOTOS",
    "/mnt/c/Users/karen/OneDrive/מסמכים/Uri/photos",
)
OUT = os.path.join(HERE, "static", "images")

# Widths generated per orientation. Cards need small, heroes need large.
WIDTHS_WIDE = (640, 1280, 1920)
WIDTHS_TALL = (480, 960, 1440)

# ── Manifest ────────────────────────────────────────────────────
# (source-relative-path, output-category, output-slug)
#
# Slugs are semantic on purpose: the templates reference them by meaning,
# so replacing a photo is a matter of re-pointing one manifest row rather
# than editing markup.
IMAGES = [
    # Brand marks
    ("לוגו/לוגו.jpeg", "brand", "logo-badge"),
    ("לוגו/לוגו שלט_.png", "brand", "logo-sign"),

    # The kashrut certificate, shown in full on /kosher. Photographed
    # portrait, so it depends on the EXIF rotation handled in build_image().
    ("לוגו/kosher.JPG", "brand", "kosher-certificate"),

    # The Complet Poisson scroll story. Hebrew captions are baked into
    # these frames by the designer, so ORDER IS MEANINGFUL - it reads as
    # one sentence across six images.
    ("מנות/1.png", "story", "story-1-intro"),
    ("מנות/2 חדש.png", "story", "story-2-fish"),
    ("מנות/3.png", "story", "story-3-egg"),
    ("מנות/4.png", "story", "story-4-fries"),
    ("מנות/5.png", "story", "story-5-harissa"),
    ("מנות/6 חדש.png", "story", "story-6-full"),

    # Real plates, shot at the restaurant. These are the dish photos that
    # go on the menu and lead the gallery - the styled set below is
    # decoration, this is what the food actually looks like.
    ("מנות/DSC00062.JPG", "dishes", "banatagge-plate"),
    ("מנות/DSC00071.JPG", "dishes", "pargit-plate"),
    ("מנות/DSC00077.JPG", "dishes", "spaghetti-bolognese"),
    ("מנות/DSC00082.JPG", "dishes", "table-spread"),

    # Clean dish photography (no baked-in text - safe for menu/hero use)
    ("מנות/ChatGPT Image Jul 15, 2026, 08_38_07 PM.png", "dishes", "poisson-plated"),
    ("מנות/ChatGPT Image Jul 15, 2026, 08_55_45 PM.png", "dishes", "poisson-with-salatim"),
    ("מנות/1 (1).png", "dishes", "salatim-overhead"),
    ("מנות/ChatGPT Image Jul 15, 2026, 08_41_54 PM.png", "dishes", "salatim-spread"),
    ("מנות/ChatGPT Image Jul 15, 2026, 08_44_43 PM.png", "dishes", "matbucha"),
    ("מנות/ChatGPT Image Jul 15, 2026, 09_20_43 PM.png", "dishes", "eggplant-salad"),

    # Unretouched photos from the restaurant itself. These are the
    # authenticity anchors - same tablecloth and plates as the styled set.
    ("מנות/IMG_7790.HEIC", "real", "real-poisson-table"),
    ("מנות/IMG_7797.HEIC", "real", "real-croquettes-table"),

    # Atmosphere: warm, low-light, human. This set sells the visit.
    ("רקע/05_ChatGPT Image Jun 14, 2026 at 09_34_36 PM.png", "atmosphere", "neomi-portrait"),
    ("רקע/03_ChatGPT Image Jun 10, 2026 at 07_45_22 PM(1).png", "atmosphere", "grandmother-kitchen"),
    ("רקע/23_ארוחה_משפחתית_חמה_וכפרית.png", "atmosphere", "family-table"),
    ("רקע/22_ארוחה_חמה_בסביבת_מטבח_רטרו.png", "atmosphere", "serving-couscous"),
    ("רקע/21_ארוחה_חמה_בידיים_אוהבות.png", "atmosphere", "hands-passing"),
    ("רקע/24_ארוחת_ערב_חמה_וינטאז_לבית.png", "atmosphere", "hands-passing-warm"),
]

# Videos are re-encoded, not copied. The camera originals are shot for
# archival, not for a phone on hotel wifi: the gallery clip is 4K vertical
# at 26 Mbit/s, which is roughly twenty times more pixels than its player
# will ever display. Each entry says what the clip is FOR, and the encoder
# settings follow from that.
VIDEOS = [
    {
        "src": "אוירה/hf_20260807_101456_f2c37284-e8d6-4edd-9e1c-b76eb7347eb8.mp4",
        "out": "hero-loop.mp4",
        # Muted background loop behind the hero, and main.js only loads it on
        # screens >= 768px on a fast connection. Nobody ever hears it, so the
        # audio track is pure waste, and the quality bar is "does not look
        # blocky behind the headline".
        "height": 1280,
        "crf": 30,
        "audio": None,
    },
    {
        "src": "אוירה/קיץ בנעמי .mp4",
        "out": "summer-at-neomi.mp4",
        # Gallery clip, played deliberately with the sound on, so it keeps
        # its audio and a tighter CRF. 1080 tall is more than any phone
        # gallery shows.
        "height": 1920,
        "crf": 26,
        "audio": "96k",
    },
]

# HEVC in a QuickTime container. Now that ffmpeg is available these could be
# converted, but neither is referenced by the site yet - see CONTENT_TODO.md.
SKIPPED_VIDEOS = [
    ("אוירה/ערוך קטעים.MOV", "HEVC/QuickTime, and not used by any page yet"),
    ("רקע/מסעדת נעמי בואו לטעום(1).mov", "HEVC/QuickTime, and not used by any page yet"),
]


def ffmpeg_exe():
    """A usable ffmpeg, from the system or from the pip package.

    imageio-ffmpeg ships a static build, which means the video step works
    without apt and without root - useful on a machine where the photo
    library is the only thing anybody wants to touch.
    """
    found = shutil.which("ffmpeg")
    if found:
        return found
    try:
        import imageio_ffmpeg
    except ImportError:
        return None
    return imageio_ffmpeg.get_ffmpeg_exe()


def build_video(exe, src_path, dest, height, crf, audio):
    """Re-encode one clip for the web.

    scale=-2 keeps the aspect ratio and rounds the width to an even number,
    which H.264 requires. faststart moves the index to the front of the file
    so playback can begin before the whole thing has arrived.
    """
    scale = f"scale=-2:'min({height},ih)'"
    cmd = [
        exe, "-y", "-loglevel", "error",
        "-i", src_path,
        "-vf", scale,
        "-c:v", "libx264", "-crf", str(crf), "-preset", "slow",
        "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    ]
    cmd += ["-an"] if audio is None else ["-c:a", "aac", "-b:a", audio]
    cmd.append(dest)
    subprocess.run(cmd, check=True)


def build_image(src_path, category, slug):
    im = Image.open(src_path)
    # Cameras record rotation as an EXIF flag rather than rotating the
    # pixels. Browsers honour that flag for JPEG, but resizing here drops it
    # and the output is WebP either way - so the rotation has to be baked in
    # now or a portrait photo is served on its side.
    im = ImageOps.exif_transpose(im)
    im = im.convert("RGB")
    out_dir = os.path.join(OUT, category)
    os.makedirs(out_dir, exist_ok=True)

    widths = WIDTHS_TALL if im.height > im.width else WIDTHS_WIDE
    written = []
    for w in widths:
        if w > im.width:
            # Never upscale - a smaller source just gets fewer variants.
            continue
        resized = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
        dest = os.path.join(out_dir, f"{slug}-{w}.webp")
        resized.save(dest, "WEBP", quality=82, method=6)
        written.append(dest)

    if not written:
        # Source narrower than the smallest variant: emit it at full width.
        dest = os.path.join(out_dir, f"{slug}-{im.width}.webp")
        im.save(dest, "WEBP", quality=82, method=6)
        written.append(dest)

    return written, im.size


def sweep_retired():
    """Delete webp variants of slugs no longer in the manifest.

    build_image() only ever writes, so a photo retired from the library
    leaves its old variants behind and the templates keep serving a picture
    that is supposed to be gone. Anything in static/images that no manifest
    row claims is removed here.
    """
    wanted = {}
    for _, category, slug in IMAGES:
        wanted.setdefault(category, set()).add(slug)

    removed = []
    for category, slugs in wanted.items():
        out_dir = os.path.join(OUT, category)
        if not os.path.isdir(out_dir):
            continue
        for name in os.listdir(out_dir):
            if not name.endswith(".webp"):
                continue
            slug = name.rsplit(".", 1)[0].rsplit("-", 1)[0]
            if slug not in slugs:
                os.remove(os.path.join(out_dir, name))
                removed.append(f"{category}/{name}")
    return removed


def main():
    if not os.path.isdir(SRC):
        sys.exit(f"Photo library not found: {SRC}\nSet NEOMI_PHOTOS to override.")

    total_bytes = 0
    missing = []

    for rel, category, slug in IMAGES:
        src_path = os.path.join(SRC, rel)
        if not os.path.exists(src_path):
            missing.append(rel)
            continue
        if rel.lower().endswith(".heic") and pillow_heif is None:
            missing.append(f"{rel} (needs pillow-heif)")
            continue
        written, size = build_image(src_path, category, slug)
        got = sum(os.path.getsize(p) for p in written)
        total_bytes += got
        print(f"  {category}/{slug:<24} {size[0]}x{size[1]} -> {len(written)} webp, {got // 1024} KB")

    video_dir = os.path.join(OUT, "video")
    os.makedirs(video_dir, exist_ok=True)
    exe = ffmpeg_exe()
    if exe is None:
        print("\n  ffmpeg not found - videos skipped.")
        print("  Install one of:  sudo apt install ffmpeg")
        print("                   pip install imageio-ffmpeg")
    else:
        for spec in VIDEOS:
            src_path = os.path.join(SRC, spec["src"])
            if not os.path.exists(src_path):
                missing.append(spec["src"])
                continue
            dest = os.path.join(video_dir, spec["out"])
            before = os.path.getsize(src_path)
            build_video(exe, src_path, dest,
                        spec["height"], spec["crf"], spec["audio"])
            got = os.path.getsize(dest)
            total_bytes += got
            print(f"  video/{spec['out']:<26} "
                  f"{before / 1024 / 1024:>5.1f} MB -> {got / 1024 / 1024:>4.1f} MB "
                  f"({100 - got * 100 // before}% smaller)")

    print(f"\nTotal written: {total_bytes / 1024 / 1024:.1f} MB")

    retired = sweep_retired()
    if retired:
        print(f"\nRemoved {len(retired)} stale variants of retired photos:")
        for r in retired:
            print(f"  - {r}")

    if missing:
        print("\nMissing sources:")
        for m in missing:
            print(f"  - {m}")

    print("\nNot converted:")
    for rel, why in SKIPPED_VIDEOS:
        print(f"  - {rel}: {why}")


if __name__ == "__main__":
    main()
