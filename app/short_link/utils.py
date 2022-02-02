from app import db, create_app
from random import choice
from datetime import date, timedelta
import string

from .model import Link


def generate_short_id(num_of_chars=7) -> str:
    """Function to generate short_id of specified number of characters"""
    short_id = ''.join(choice(string.ascii_letters+string.digits) for _ in range(num_of_chars))
    while db.session.query(db.exists().where(Link.short_id == short_id)).scalar():
        short_id = ''.join(choice(string.ascii_letters + string.digits) for _ in range(num_of_chars))
    return short_id


def make_expiration_date(num_of_days=90) -> date:
    """Function to make expiration date from number days to expiration"""
    return date.today() + timedelta(days=num_of_days)


def clear_expired_links():
    """Function to clear expired links"""
    app = create_app('dev')
    app.app_context().push()
    Link.query.filter(Link.expires_at == date.today()).delete()
    print('expired')
