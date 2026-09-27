# -*- coding: utf-8 -*-
"""Seed the database from the printed menu (תפריט חדש 11.8).

Transcribed from the two-language menu card: page 1 Hebrew, page 3 French.
Prices are in shekels and identical across both pages.

Running this wipes existing menu items and re-inserts them, so it is the
single source of truth for the menu. Orders and reservations are untouched.
"""
import getpass
import os
import secrets
import string
import sys

from sqlalchemy import inspect, text

from app import app, db
from models import MenuItem, BusinessHours, Admin
from werkzeug.security import generate_password_hash


# Columns added after the first version of the schema. SQLAlchemy's
# create_all() only creates missing tables, never missing columns, so an
# existing restaurant.db needs them added explicitly.
ADDED_COLUMNS = {
    'menu_item': [
        ('description_he', 'TEXT'),
        ('sort_order', 'INTEGER DEFAULT 0'),
    ],
    'business_hours': [
        ('open_time2', 'VARCHAR(10)'),
        ('close_time2', 'VARCHAR(10)'),
    ],
}


def ensure_schema():
    """Add columns the live database is missing. Safe to re-run."""
    inspector = inspect(db.engine)
    for table, columns in ADDED_COLUMNS.items():
        if table not in inspector.get_table_names():
            continue
        existing = {c['name'] for c in inspector.get_columns(table)}
        for name, ddl in columns:
            if name in existing:
                continue
            db.session.execute(text(f'ALTER TABLE {table} ADD COLUMN {name} {ddl}'))
            print(f"  migrated: added {table}.{name}")
    db.session.commit()


# (category, sort, name_fr, name_he, desc_fr, desc_he, price, featured)
MENU = [
    # ── מנות ראשונות · ENTRÉES ──────────────────────────────────
    ("appetizer", 1, "Salade Nisoise", "סלט ניסואז", "", "", 65, False),
    ("appetizer", 2, "Plat Tunisien", "סלט טוניסאי", "", "", 65, False),
    ("appetizer", 3,
     "Brick à l'œuf / Brick à la pomme de terre", "בוריקה (בריק) תפוח אדמה / ביצה",
     "2 pièces", "2 יח׳", 50, True),
    ("appetizer", 4, "Banatagge", "בנטז׳",
     "Pomme de terre farcie à la viande (2 pièces)",
     "תפוח אדמה ממולא בבשר, מתובל בסגנון טוניסאי (2 יח׳)", 50, True),

    # ── עיקריות · PLATS PRINCIPAUX ──────────────────────────────
    ("main", 1, "Shakshouka maison de Neomi", "שקשוקה ביתית של נעמי",
     "avec merguez", "עם מרגז", 75, True),
    ("main", 2, "Spaghetti tunisien", "ספגטי טוניסאי", "", "", 75, False),
    ("main", 3, "Spaghetti bolognaise", "ספגטי בולונז", "", "", 80, False),
    ("main", 4, "Plat du jour", "תבשיל היום",
     "Spécialité tunisienne maison préparée selon les recettes traditionnelles de la famille.",
     "מבחר תבשילים טוניסאים ביתיים משתנים", 85, True),

    # ── בשרים · GRILLADES & VIANDES ─────────────────────────────
    ("grill", 1, "Entrecôte grillée", "אנטריקוט על הגריל", "250 g", "250 ג׳", 135, True),
    ("grill", 2, "Escalope de poulet maison", "שניצל ביתי", "", "", 84, False),
    ("grill", 3, "Kebab maison", "קבב הבית", "", "", 84, False),
    ("grill", 4, "Merguez grillé", "נקניקיות מרגז", "", "", 84, False),
    ("grill", 5, "Parguit grillé", "פרגית", "", "", 95, False),

    # ── דגים · POISSONS & SPÉCIALITÉS TUNISIENNES ───────────────
    ("fish", 1, "Poissons du jour", "דגים היום אפוי / מטוגן",
     "Dorade / Mulet", "", 110, False),
    ("fish", 2, "Complet Poisson", "קומפלט פואסון",
     "Spécialité tunisienne à base de poisson, œuf au plat, aubergine frite et tastira",
     "ביצת עין, טסטירה וצ׳יפס", 139, True),

    # ── שתייה · BOISSONS & BIÈRES ───────────────────────────────
    ("drink", 1, "Eau minérale", "מים מינרליים", "", "", 15, False),
    ("drink", 2, "Soda", "סודה", "", "", 12, False),
    ("drink", 3, "Coca-Cola / Coca-Cola Zéro", "קולה / קולה זירו", "", "", 15, False),
    ("drink", 4, "Jus de fruits / Eaux aromatisées / Nestea",
     "תפוזים / אשכוליות / אייסטי", "", "", 15, False),
    ("drink", 5, "Carlsberg", "קרלסברג", "", "", 22, False),
    ("drink", 6, "Heineken", "הייניקן", "", "", 22, False),
    ("drink", 7, "Verre de vin maison", "כוס יין הבית", "", "", 38, False),
]

# Photos we actually have, matched to the dishes they show.
DISH_IMAGES = {
    # The four photographed at the restaurant come first - they show the
    # actual plate. The styled shots fill in where we have no real photo.
    "קומפלט פואסון": "images/real/real-poisson-table-960.webp",
    "בנטז׳": "images/dishes/banatagge-plate-1280.webp",
    "פרגית": "images/dishes/pargit-plate-1280.webp",
    "ספגטי בולונז": "images/dishes/spaghetti-bolognese-1280.webp",
    "דגים היום אפוי / מטוגן": "images/dishes/poisson-plated-960.webp",
    "סלט טוניסאי": "images/dishes/salatim-spread-960.webp",
}


def generate_password(length=16):
    """A password nobody has to invent, and nobody can guess.

    There is deliberately no default password in this file any more. A
    default that lives in the repository is a published password: anyone who
    can read the code can log into /admin.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def resolve_new_password(prompt_if_missing):
    """Where a new admin password comes from, in order of preference.

    NEOMI_ADMIN_PASSWORD lets a hosting dashboard set it without it ever
    being typed into a terminal. Otherwise ask for it interactively, and
    fall back to generating one when there is nobody to ask.
    """
    from_env = os.environ.get('NEOMI_ADMIN_PASSWORD')
    if from_env:
        return from_env, 'taken from NEOMI_ADMIN_PASSWORD'

    if prompt_if_missing and sys.stdin.isatty():
        first = getpass.getpass('New admin password (typing is hidden): ')
        if first != getpass.getpass('Repeat it: '):
            sys.exit('Passwords did not match; nothing was changed.')
        if len(first) < 10:
            sys.exit('Too short - use at least 10 characters.')
        return first, 'set from your input'

    generated = generate_password()
    return generated, f'GENERATED - write this down now: {generated}'

# Exactly one row per day: two services are two windows on the same row,
# not two rows. Extra rows for the same day are invisible on the site -
# every reader takes the first row it finds for that weekday.
DEFAULT_HOURS = [
    # (day_of_week, open, close, open2, close2, is_closed) - 0 = Sunday
    (0, '16:00', '20:00', None, None, False),        # Sunday
    (1, '16:00', '20:00', None, None, False),        # Monday
    (2, '16:00', '20:00', None, None, False),        # Tuesday
    (3, '16:00', '20:00', None, None, False),        # Wednesday
    (4, '16:00', '20:00', None, None, False),        # Thursday
    (5, None, None, None, None, True),               # Friday: closed
    (6, None, None, None, None, True),               # Saturday: Shabbat
]


def seed():
    with app.app_context():
        db.create_all()
        ensure_schema()

        # The menu card is the source of truth, so replace rather than skip.
        deleted = MenuItem.query.delete()
        for (category, sort, name_fr, name_he, desc_fr, desc_he, price, featured) in MENU:
            db.session.add(MenuItem(
                name=name_fr,
                name_he=name_he,
                description=desc_fr,
                description_he=desc_he,
                category=category,
                price=price,
                sort_order=sort,
                is_featured=featured,
                is_available=True,
                image_path=DISH_IMAGES.get(name_he, ''),
            ))

        # Hours are owner-editable in /admin/hours, so they are never
        # clobbered by a reseed. Pass --reset-hours to force the defaults.
        reset_hours = '--reset-hours' in sys.argv
        if reset_hours or not BusinessHours.query.first():
            if reset_hours:
                BusinessHours.query.delete()
            for day, open_t, close_t, open_t2, close_t2, closed in DEFAULT_HOURS:
                db.session.add(BusinessHours(
                    day_of_week=day, open_time=open_t, close_time=close_t,
                    open_time2=open_t2, close_time2=close_t2, is_closed=closed,
                ))
            print("Business hours set to defaults.")

        # An existing admin password is never overwritten by a reseed.
        # Use --set-admin-password to change it.
        admin = Admin.query.filter_by(username='admin').first()
        changing = '--set-admin-password' in sys.argv or '--reset-admin' in sys.argv
        if admin is None:
            password, how = resolve_new_password(prompt_if_missing=True)
            db.session.add(Admin(
                username='admin',
                password_hash=generate_password_hash(password),
            ))
            print(f"Created admin - password {how}")
        elif changing:
            password, how = resolve_new_password(prompt_if_missing=True)
            admin.password_hash = generate_password_hash(password)
            print(f"Admin password changed - {how}")
        else:
            print("Admin already exists; password left unchanged "
                  "(use --set-admin-password to change it).")

        db.session.commit()

        print(f"\nReplaced {deleted} old menu items with {len(MENU)} from the printed menu.")
        print("Sections: " + ", ".join(
            f"{c}={sum(1 for m in MENU if m[0] == c)}"
            for c in ['appetizer', 'main', 'grill', 'fish', 'drink']
        ))


if __name__ == '__main__':
    seed()
