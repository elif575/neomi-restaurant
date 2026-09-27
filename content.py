# -*- coding: utf-8 -*-
"""Real-world details about the restaurant.

THIS IS THE ONE FILE THE OWNER NEEDS TO EDIT. Every phone number, address
and social link on the site comes from here, so nothing is hard-coded into
a template.

Values still marked PLACEHOLDER are invented and MUST be replaced before
the site goes live. See CONTENT_TODO.md.
"""

RESTAURANT = {
    "name_he": "נעמי",
    "name_latin": "Neomi",

    # Landline
    "phone_display": "09-7730201",
    "phone_tel": "+97297730201",

    # Mobile. Shown under the landline everywhere the landline appears -
    # on a phone it is the number that actually gets answered.
    "mobile_display": "052-708-1255",
    "mobile_tel": "+972527081255",

    # WhatsApp number in international format, no + or dashes
    "whatsapp": "972544452833",

    "address_he": "מלון בלו וייס, רחוב גד מכנס 22, נתניה",
    "address_fr": "Hôtel Blue Weiss, 22 rue Gad Mechans, Netanya",

    # PLACEHOLDER - used to build the map links. Either fill in coordinates
    # (most reliable) or leave them None and the address string is used.
    "lat": None,
    "lng": None,

    # PLACEHOLDER - social profiles. Set to None to hide the icon entirely.
    "instagram": "https://www.instagram.com/neomi.restaurant",
    "facebook": "https://www.facebook.com/p/Neomi-Restaurant-61589987793558/",
    "tiktok": None,

    "kosher_authority_he": "כשר למהדרין",
    "kosher_authority_fr": "Casher Lemehadrin",

    # ── The kashrut certificate shown on /kosher ────────────────
    # Read off the certificate itself (photos/לוגו/kosher.JPG).
    #
    # UPDATE kosher_valid_until WHEN THE CERTIFICATE IS RENEWED. The page
    # stops claiming the restaurant is certified once that date has passed,
    # because a stale kashrut claim is worse than no claim at all.
    "kosher_supervision_he": 'בד״ץ "בהידור הכשרות" · הרבנות הראשית נתניה',
    "kosher_supervision_fr": "Badatz « BeHidour HaKashrout » · Grand Rabbinat de Netanya",
    "kosher_holder_he": "מלון בלו וייס / מסעדת נעמי",
    "kosher_holder_fr": "Hôtel Blue Weiss / Restaurant Neomi",
    "kosher_type_he": "בשרי",
    "kosher_type_fr": "Viande",
    "kosher_valid_from": "2026-04-09",
    "kosher_valid_until": "2026-08-31",
}


def waze_url():
    """Deep link that opens Waze straight into navigation."""
    if RESTAURANT["lat"] and RESTAURANT["lng"]:
        return f"https://waze.com/ul?ll={RESTAURANT['lat']},{RESTAURANT['lng']}&navigate=yes"
    from urllib.parse import quote

    return f"https://waze.com/ul?q={quote(RESTAURANT['address_he'])}&navigate=yes"


def gmaps_url():
    from urllib.parse import quote

    if RESTAURANT["lat"] and RESTAURANT["lng"]:
        return f"https://www.google.com/maps/search/?api=1&query={RESTAURANT['lat']},{RESTAURANT['lng']}"
    return f"https://www.google.com/maps/search/?api=1&query={quote(RESTAURANT['address_he'])}"


def whatsapp_url(message=""):
    from urllib.parse import quote

    base = f"https://wa.me/{RESTAURANT['whatsapp']}"
    return f"{base}?text={quote(message)}" if message else base


# ── Gallery manifest ────────────────────────────────────────────
# Curated rather than a directory listing: order and grouping are editorial
# decisions. Available widths are discovered from disk at request time
# (see app.gallery) so this list can never drift out of sync with whatever
# build_assets.py actually produced.
#
# Each entry: (category, slug, alt-text i18n key)
GALLERY = [
    # The four shot at the restaurant. They open the gallery and the dishes
    # tab, at double size - see GALLERY_LEAD below. Real plates beat styled
    # renders at convincing somebody to come and eat, so they go first.
    ("dishes", "banatagge-plate", "dish_alt_banatagge"),
    ("dishes", "pargit-plate", "dish_alt_pargit"),
    ("dishes", "table-spread", "dish_alt_table_spread"),
    ("dishes", "spaghetti-bolognese", "dish_alt_spaghetti"),

    ("real", "real-poisson-table", "dish_alt_complet"),
    ("real", "real-croquettes-table", "atmos_real_alt"),
    ("dishes", "poisson-plated", "story_2_alt"),
    ("dishes", "poisson-with-salatim", "salatim_alt_spread"),
    ("dishes", "salatim-overhead", "salatim_alt_overhead"),
    ("dishes", "salatim-spread", "salatim_alt_spread"),
    ("dishes", "matbucha", "salatim_alt_matbucha"),
    ("dishes", "eggplant-salad", "salatim_alt_eggplant"),
    ("atmosphere", "family-table", "atmos_family_alt"),
    ("atmosphere", "neomi-portrait", "about_portrait_alt"),
    ("atmosphere", "grandmother-kitchen", "about_kitchen_alt"),
    ("atmosphere", "serving-couscous", "atmos_couscous_alt"),
    ("atmosphere", "hands-passing", "atmos_hands_alt"),
    ("atmosphere", "hands-passing-warm", "atmos_hands_alt"),
]

# Videos are grouped separately - they need a poster image and click-to-play.
GALLERY_VIDEOS = [
    {
        "src": "images/video/summer-at-neomi.mp4",
        "poster": "images/atmosphere/family-table-1280.webp",
        "label_he": "קיץ בנעמי",
        "label_fr": "L'été chez Neomi",
    },
]

# Shown at double size in a lead row above the rest of the gallery, in both
# languages. Keep this small: everything is emphasised means nothing is.
GALLERY_LEAD = {
    "banatagge-plate",
    "pargit-plate",
    "table-spread",
    "spaghetti-bolognese",
}

# Which gallery groups map to which filter tab.
GALLERY_TABS = {
    "dishes": ("dishes",),
    "atmos": ("atmosphere", "real"),
}
