import os
import glob
import json
from datetime import datetime, date, timedelta
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import (db, MenuItem, Order, OrderItem, Reservation, BusinessHours, Admin,
                    MENU_CATEGORIES, CATEGORIES_WITH_SIDES)
import content
import i18n
import notify

app = Flask(__name__)


def load_secret_key():
    """Stable secret key so admin sessions survive a restart.

    os.urandom() on every boot meant the admin was silently logged out each
    time the dev server reloaded. Prefer an env var in production; fall back
    to a generated file kept out of git.
    """
    env_key = os.environ.get('NEOMI_SECRET_KEY')
    if env_key:
        return env_key
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'secret_key')
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    if os.path.exists(key_path):
        with open(key_path) as fh:
            return fh.read().strip()
    key = os.urandom(32).hex()
    with open(key_path, 'w') as fh:
        fh.write(key)
    return key


app.config['SECRET_KEY'] = load_secret_key()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'images', 'menu')
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB

# Session hardening. Once the owner logs in, the session cookie IS the
# credential - so it must not be readable from JavaScript or sent across
# sites. Secure is opt-in via NEOMI_HTTPS because local development runs on
# plain HTTP, where a Secure cookie would simply never be sent back.
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    SESSION_COOKIE_SECURE=os.environ.get('NEOMI_HTTPS') == '1',
)

db.init_app(app)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Language handling ──────────────────────────────────────────

def current_lang():
    lang = session.get('lang')
    if lang in i18n.LANGUAGES:
        return lang
    return i18n.DEFAULT_LANG


@app.route('/lang/<code>')
def set_language(code):
    if code in i18n.LANGUAGES:
        session['lang'] = code
    return redirect(request.referrer or url_for('index'))


@app.context_processor
def inject_globals():
    """Expose copy, language metadata and restaurant details to every template."""
    lang = current_lang()
    return {
        'lang': lang,
        'dir': i18n.LANGUAGES[lang]['dir'],
        'languages': i18n.LANGUAGES,
        't': lambda key: i18n.translate(key, lang),
        'day_name': lambda idx: i18n.day_name(idx, lang),
        'r': content.RESTAURANT,
        'waze_url': content.waze_url(),
        'gmaps_url': content.gmaps_url(),
        'whatsapp_url': content.whatsapp_url,
        'current_year': date.today().year,
        'static_v': static_v,
    }


def static_v(filename):
    """Static URL with the file's mtime appended, so browsers refetch it after every change."""
    path = os.path.join(app.static_folder, filename)
    try:
        version = int(os.path.getmtime(path))
    except OSError:
        version = 0
    return url_for('static', filename=filename, v=version)


def available_widths(category, slug):
    """Widths build_assets.py actually produced for one photo.

    Sources vary in size and the build never upscales, so the set of widths
    differs per photo. Reading them off disk keeps templates honest instead
    of hard-coding a width that may not exist.
    """
    pattern = os.path.join(app.static_folder, 'images', category, f'{slug}-*.webp')
    widths = []
    for path in glob.glob(pattern):
        stem = os.path.basename(path).rsplit('.', 1)[0]
        suffix = stem.rsplit('-', 1)[-1]
        if suffix.isdigit():
            widths.append(int(suffix))
    return sorted(widths)


def is_open_now(hours):
    """Whether the restaurant is open at this moment, for the live badge.

    A day can have two service windows (lunch and dinner), so every window
    is checked - the old single-pair test reported "open" right through the
    afternoon break.
    """
    now = datetime.now()
    # BusinessHours uses 0=Sunday; Python's weekday() is 0=Monday.
    today_index = (now.weekday() + 1) % 7
    for h in hours:
        if h.day_of_week != today_index:
            continue
        for open_str, close_str in h.ranges:
            try:
                open_t = datetime.strptime(open_str, '%H:%M').time()
                close_t = datetime.strptime(close_str, '%H:%M').time()
            except (ValueError, TypeError):
                continue
            if open_t <= now.time() <= close_t:
                return True
        return False
    return False


def reservation_slots(hours):
    """Bookable half-hour slots, keyed by weekday, taken from the hours.

    The booking form used to offer a fixed 11:00-22:30 list, so a guest
    could ask for 17:00 on a day the kitchen shuts at 16:00 and reopens at
    18:00. Slots now come from the service windows themselves, and the last
    one sits half an hour before a window closes.
    """
    slots = {}
    for h in hours:
        day = []
        for open_str, close_str in h.ranges:
            try:
                cursor = datetime.strptime(open_str, '%H:%M')
                end = datetime.strptime(close_str, '%H:%M')
            except (ValueError, TypeError):
                continue
            while cursor + timedelta(minutes=30) <= end:
                day.append(cursor.strftime('%H:%M'))
                cursor += timedelta(minutes=30)
        slots[h.day_of_week] = day
    return slots


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated


# ── Public Routes ──────────────────────────────────────────────

@app.route('/')
def index():
    featured = MenuItem.query.filter_by(is_featured=True, is_available=True).limit(6).all()
    hours = BusinessHours.query.order_by(BusinessHours.day_of_week).all()
    return render_template(
        'index.html',
        featured=featured,
        hours=hours,
        open_now=is_open_now(hours),
    )


@app.route('/menu')
def menu():
    """Menu grouped into the printed card's sections, in printed order."""
    sections = []
    for cat in MENU_CATEGORIES:
        items = (MenuItem.query
                 .filter_by(category=cat, is_available=True)
                 .order_by(MenuItem.sort_order, MenuItem.id)
                 .all())
        if items:
            sections.append({
                'key': cat,
                # Not 'items': Jinja resolves section.items to dict.items().
                'dishes': items,
                'has_sides_note': cat in CATEGORIES_WITH_SIDES,
            })

    pdf_rel = 'menu/neomi-menu.pdf'
    has_pdf = os.path.exists(os.path.join(app.static_folder, pdf_rel))
    return render_template(
        'menu.html',
        sections=sections,
        pdf_path=pdf_rel if has_pdf else None,
    )


@app.route('/order')
def order_page():
    items = (MenuItem.query
             .filter_by(is_available=True)
             .order_by(MenuItem.sort_order, MenuItem.id)
             .all())
    categories = {}
    for item in items:
        categories.setdefault(item.category, []).append(item)
    return render_template(
        'order.html',
        categories=categories,
        category_order=MENU_CATEGORIES,
    )


@app.route('/order', methods=['POST'])
def place_order():
    data = request.get_json()
    if not data or not data.get('items') or not data.get('customer_name') or not data.get('phone'):
        return jsonify({'error': 'Missing required fields'}), 400

    order = Order(
        customer_name=data['customer_name'],
        phone=data['phone'],
        order_type=data.get('order_type', 'pickup'),
        address=data.get('address', ''),
        notes=data.get('notes', ''),
        total=0
    )
    db.session.add(order)
    db.session.flush()

    total = 0
    for item_data in data['items']:
        menu_item = MenuItem.query.get(item_data['id'])
        if not menu_item or not menu_item.is_available:
            db.session.rollback()
            return jsonify({'error': f'Item not available'}), 400
        qty = int(item_data['quantity'])
        order_item = OrderItem(
            order_id=order.id,
            menu_item_id=menu_item.id,
            quantity=qty,
            price_at_order=menu_item.price
        )
        total += menu_item.price * qty
        db.session.add(order_item)

    order.total = total
    db.session.commit()
    return jsonify({'order_id': order.id, 'total': total})


@app.route('/order/confirmation/<int:order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)


@app.route('/reservations')
def reservations_page():
    hours = BusinessHours.query.order_by(BusinessHours.day_of_week).all()
    slots = reservation_slots(hours)
    return render_template(
        'reservations.html',
        hours=hours,
        slots=slots,
        # Union of every day's slots: the <select> is rendered once and
        # narrowed per weekday by JS, so it still works without scripting.
        all_slots=sorted({t for day in slots.values() for t in day}),
        today=date.today().isoformat(),
    )


@app.route('/reservations', methods=['POST'])
def make_reservation():
    data = request.form
    lang = current_lang()
    if not data.get('customer_name') or not data.get('phone') or not data.get('date') or not data.get('time'):
        flash(i18n.translate('res_error', lang), 'error')
        return redirect(url_for('reservations_page'))

    reservation = Reservation(
        customer_name=data['customer_name'],
        phone=data['phone'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        time=data['time'],
        party_size=int(data.get('party_size', 2)),
        notes=data.get('notes', '')
    )
    db.session.add(reservation)
    # Committed before the hand-off is built: a booking must survive the
    # customer closing the tab without sending the WhatsApp message.
    db.session.commit()

    booking = {
        'customer_name': reservation.customer_name,
        'phone': reservation.phone,
        'date': reservation.date.strftime('%d/%m/%Y'),
        'time': reservation.time,
        'party_size': reservation.party_size,
        'notes': reservation.notes,
    }

    # Handed on through the session rather than the URL. A /sent/<id> route
    # would let anyone read somebody else's booking by counting upwards.
    session['pending_whatsapp'] = {
        'url': notify.whatsapp_url(booking, lang),
        'summary': f"{booking['date']} · {booking['time']} · {booking['party_size']}",
    }
    return redirect(url_for('reservation_sent'))


@app.route('/reservations/sent')
def reservation_sent():
    """Confirmation, and the hand-off to WhatsApp.

    The booking is already saved and visible in /admin. This page exists so
    the customer can fire the WhatsApp message too, which is what actually
    reaches somebody within the minute.
    """
    handoff = session.pop('pending_whatsapp', None)
    if not handoff:
        # Reached directly, or after a refresh - nothing to confirm.
        return redirect(url_for('reservations_page'))
    return render_template('reservation_sent.html', handoff=handoff)


@app.route('/about')
def about():
    """The restaurant's story, at length.

    The homepage carries a two-paragraph version of this; here it gets the
    room to be a story rather than a teaser. All the copy lives in i18n.py
    so it stays translatable and editable in one place.
    """
    return render_template('about.html')


@app.route('/kosher')
def kosher():
    """The kashrut certificate, shown in full.

    The certificate carries an expiry date, so the page checks it rather
    than asserting the restaurant is certified for ever. Once it lapses the
    page says so plainly instead - for a kosher restaurant an out-of-date
    claim on its own website is a real problem, not a cosmetic one.
    """
    widths = available_widths('brand', 'kosher-certificate')

    def parse(key):
        try:
            return datetime.strptime(content.RESTAURANT[key], '%Y-%m-%d').date()
        except (ValueError, TypeError, KeyError):
            return None

    valid_until = parse('kosher_valid_until')
    return render_template(
        'kosher.html',
        widths=widths,
        valid_from=parse('kosher_valid_from'),
        valid_until=valid_until,
        expired=bool(valid_until and valid_until < date.today()),
    )


@app.route('/gallery')
def gallery():
    """Curated gallery built from content.GALLERY.

    Entries whose files are missing are dropped, so a half-finished asset
    build degrades to a smaller gallery instead of broken images.
    """
    items = []
    for category, slug, alt_key in content.GALLERY:
        widths = available_widths(category, slug)
        if not widths:
            continue
        group = next(
            (tab for tab, cats in content.GALLERY_TABS.items() if category in cats),
            'dishes',
        )
        # Lead tiles are rendered at roughly double the width of the rest,
        # so the smallest variant would visibly soften on a retina screen.
        # Step up one width where the photo has one to give.
        lead = slug in content.GALLERY_LEAD
        thumb_w = widths[min(1, len(widths) - 1)] if lead else min(widths)

        items.append({
            'thumb': f'images/{category}/{slug}-{thumb_w}.webp',
            'full': f'images/{category}/{slug}-{max(widths)}.webp',
            'alt_key': alt_key,
            'group': group,
            'lead': lead,
        })

    videos = [
        v for v in content.GALLERY_VIDEOS
        if os.path.exists(os.path.join(app.static_folder, v['src']))
    ]
    return render_template('gallery.html', items=items, videos=videos)


# ── Admin Routes ───────────────────────────────────────────────

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials.', 'error')
    return render_template('admin/login.html')


@app.route('/admin/logout')
def admin_logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    today = date.today()
    today_orders = Order.query.filter(db.func.date(Order.created_at) == today).all()
    today_revenue = sum(o.total for o in today_orders)
    today_reservations = Reservation.query.filter_by(date=today).all()
    pending_orders = Order.query.filter_by(status='pending').count()
    pending_reservations = Reservation.query.filter_by(status='pending').count()

    # Popular items (top 5)
    popular = db.session.query(
        MenuItem.name,
        db.func.sum(OrderItem.quantity).label('total_qty')
    ).join(OrderItem, MenuItem.id == OrderItem.menu_item_id
    ).group_by(MenuItem.name
    ).order_by(db.func.sum(OrderItem.quantity).desc()
    ).limit(5).all()

    return render_template('admin/dashboard.html',
        today_orders=len(today_orders),
        today_revenue=today_revenue,
        today_reservations=len(today_reservations),
        pending_orders=pending_orders,
        pending_reservations=pending_reservations,
        popular_items=popular
    )


@app.route('/admin/orders')
@admin_required
def admin_orders():
    status_filter = request.args.get('status', '')
    query = Order.query.order_by(Order.created_at.desc())
    if status_filter:
        query = query.filter_by(status=status_filter)
    orders = query.all()
    return render_template('admin/orders.html', orders=orders, current_filter=status_filter)


@app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    if new_status in ('pending', 'preparing', 'ready', 'completed', 'cancelled'):
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.id} updated to {new_status}.', 'success')
    return redirect(url_for('admin_orders'))


@app.route('/admin/reservations')
@admin_required
def admin_reservations():
    status_filter = request.args.get('status', '')
    query = Reservation.query.order_by(Reservation.date.desc(), Reservation.time.desc())
    if status_filter:
        query = query.filter_by(status=status_filter)
    reservations = query.all()
    return render_template('admin/reservations.html', reservations=reservations, current_filter=status_filter)


@app.route('/admin/reservations/<int:res_id>/status', methods=['POST'])
@admin_required
def update_reservation_status(res_id):
    res = Reservation.query.get_or_404(res_id)
    new_status = request.form.get('status')
    if new_status in ('pending', 'confirmed', 'cancelled'):
        res.status = new_status
        db.session.commit()
        flash(f'Reservation #{res.id} updated to {new_status}.', 'success')
    return redirect(url_for('admin_reservations'))


@app.route('/admin/menu')
@admin_required
def admin_menu():
    items = MenuItem.query.order_by(MenuItem.category, MenuItem.sort_order, MenuItem.id).all()
    # Passed in rather than hard-coded in the template: a stale list there
    # would silently reset a dish's section on save.
    return render_template('admin/menu_edit.html', items=items,
                           categories=MENU_CATEGORIES)


@app.route('/admin/menu/add', methods=['POST'])
@admin_required
def admin_menu_add():
    image_path = ''
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = f'images/menu/{filename}'

    item = MenuItem(
        name=request.form['name'],
        name_he=request.form.get('name_he', ''),
        description=request.form.get('description', ''),
        description_he=request.form.get('description_he', ''),
        category=request.form['category'],
        price=float(request.form['price']),
        sort_order=int(request.form.get('sort_order') or 0),
        image_path=image_path,
        is_available='is_available' in request.form,
        is_featured='is_featured' in request.form
    )
    db.session.add(item)
    db.session.commit()
    flash(f'Added "{item.name}" to menu.', 'success')
    return redirect(url_for('admin_menu'))


@app.route('/admin/menu/<int:item_id>/edit', methods=['POST'])
@admin_required
def admin_menu_edit(item_id):
    item = MenuItem.query.get_or_404(item_id)
    item.name = request.form['name']
    item.name_he = request.form.get('name_he', '')
    item.description = request.form.get('description', '')
    item.description_he = request.form.get('description_he', '')
    item.category = request.form['category']
    item.price = float(request.form['price'])
    item.sort_order = int(request.form.get('sort_order') or 0)
    item.is_available = 'is_available' in request.form
    item.is_featured = 'is_featured' in request.form

    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            item.image_path = f'images/menu/{filename}'

    db.session.commit()
    flash(f'Updated "{item.name}".', 'success')
    return redirect(url_for('admin_menu'))


@app.route('/admin/menu/<int:item_id>/delete', methods=['POST'])
@admin_required
def admin_menu_delete(item_id):
    item = MenuItem.query.get_or_404(item_id)
    name = item.name
    db.session.delete(item)
    db.session.commit()
    flash(f'Deleted "{name}" from menu.', 'success')
    return redirect(url_for('admin_menu'))


@app.route('/admin/hours', methods=['GET', 'POST'])
@admin_required
def admin_hours():
    if request.method == 'POST':
        for day in range(7):
            hours = BusinessHours.query.filter_by(day_of_week=day).first()
            if not hours:
                hours = BusinessHours(day_of_week=day)
                db.session.add(hours)
            hours.is_closed = f'closed_{day}' in request.form
            hours.open_time = request.form.get(f'open_{day}') or None
            hours.close_time = request.form.get(f'close_{day}') or None
            # Second (evening) window. Blank means the day has one service,
            # so store None rather than an empty string - BusinessHours.ranges
            # drops the pair either way, but None is what a closed slot means.
            hours.open_time2 = request.form.get(f'open2_{day}') or None
            hours.close_time2 = request.form.get(f'close2_{day}') or None
        db.session.commit()
        flash('Business hours updated.', 'success')
        return redirect(url_for('admin_hours'))

    hours = BusinessHours.query.order_by(BusinessHours.day_of_week).all()
    return render_template('admin/hours.html', hours=hours)


# ── API endpoint for menu data (used by ordering JS) ──────────

@app.route('/api/menu')
def api_menu():
    items = MenuItem.query.filter_by(is_available=True).all()
    return jsonify([item.to_dict() for item in items])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    # Debug mode hands an interactive Python console to anyone who can
    # trigger an error, which on a public server is a full takeover. It is
    # therefore opt-in and never the default: set NEOMI_DEBUG=1 while
    # working locally, and never anywhere the internet can reach.
    #
    # This whole block only runs under `python3 app.py`. In production the
    # app is served by gunicorn, which imports `app` and ignores all of it:
    #
    #     gunicorn --bind 0.0.0.0:$PORT app:app
    debug = os.environ.get('NEOMI_DEBUG') == '1'
    host = os.environ.get('NEOMI_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))

    if debug:
        print('WARNING: debug mode is on. Never expose this to the internet.')

    app.run(debug=debug, host=host, port=port)
