from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# Menu sections, in the order they appear on the printed menu. The keys are
# stored in MenuItem.category; the display names live in i18n.py.
MENU_CATEGORIES = ['appetizer', 'main', 'grill', 'fish', 'drink']

# Grilled meats and fish are both served with a choice of side, which the
# printed menu states once per section rather than per dish.
CATEGORIES_WITH_SIDES = {'grill', 'fish'}


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # `name` holds the French/Latin name, `name_he` the Hebrew one, matching
    # the two printed menu pages.
    name = db.Column(db.String(100), nullable=False)
    name_he = db.Column(db.String(100))
    description = db.Column(db.Text)
    description_he = db.Column(db.Text)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_path = db.Column(db.String(200))
    is_available = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    # Printed-menu ordering; dishes are not alphabetical on the card.
    sort_order = db.Column(db.Integer, default=0)

    def display_name(self, lang):
        """Name in the requested language, falling back to the other one."""
        if lang == 'he':
            return self.name_he or self.name
        return self.name or self.name_he

    def display_description(self, lang):
        if lang == 'he':
            return self.description_he or ''
        return self.description or ''

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'name_he': self.name_he,
            'description': self.description,
            'description_he': self.description_he,
            'category': self.category,
            'price': self.price,
            'image_path': self.image_path,
            'is_available': self.is_available,
        }


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    order_type = db.Column(db.String(20), nullable=False)  # pickup / delivery
    address = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    total = db.Column(db.Float, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')


class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_order = db.Column(db.Float, nullable=False)
    menu_item = db.relationship('MenuItem')


class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(10), nullable=False)
    party_size = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='pending')
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class BusinessHours(db.Model):
    """One row per weekday, with up to two service windows.

    The kitchen runs lunch and dinner with a break in between, so a single
    open/close pair cannot describe a day: 13:00-16:00 and 18:00-22:00 is
    not the same as 13:00-22:00. The second window is optional - leave
    open_time2/close_time2 empty for a day that runs straight through.
    """

    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Sunday .. 6=Saturday
    open_time = db.Column(db.String(10))
    close_time = db.Column(db.String(10))
    open_time2 = db.Column(db.String(10))
    close_time2 = db.Column(db.String(10))
    is_closed = db.Column(db.Boolean, default=False)

    DAY_NAMES = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    DAY_NAMES_HE = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת']

    @property
    def day_name(self):
        return self.DAY_NAMES[self.day_of_week]

    @property
    def day_name_he(self):
        return self.DAY_NAMES_HE[self.day_of_week]

    @property
    def ranges(self):
        """The day's service windows as (open, close) pairs.

        Empty when the day is closed or half-filled, so templates and the
        open-now check can both just iterate and never special-case a
        missing second window.
        """
        if self.is_closed:
            return []
        pairs = [(self.open_time, self.close_time), (self.open_time2, self.close_time2)]
        return [(o, c) for o, c in pairs if o and c]


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
