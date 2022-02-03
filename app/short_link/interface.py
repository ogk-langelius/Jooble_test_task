from datetime import datetime

from mypy_extensions import TypedDict


class LinkInterface(TypedDict, total=False):
    """Link interface"""
    link_id: int
    original_link: str
    short_id: str
    expires_at: datetime


class CreateInterface(TypedDict, total=False):
    """interface for link creation"""
    link_id: int
    original_link: str
    days_to_expiration: int
