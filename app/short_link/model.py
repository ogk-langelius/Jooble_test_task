from app import db
from datetime import date, timedelta
from sqlalchemy import Integer, Column, String, Date

from .interface import LinkInterface


class Link(db.Model):
    """Link model."""

    __tablename__ = 'shortlinks'

    link_id = Column(Integer(), primary_key=True)
    original_link = Column(String(2048), nullable=False)
    short_id = Column(String(8), nullable=False, unique=True)
    expires_at = Column(Date(), nullable=False, default=date.today() + timedelta(days=90))

    def update(self, changes: LinkInterface):
        """Update via dictionary."""
        for column, value in changes.items():
            setattr(self, column, value)
        return self
