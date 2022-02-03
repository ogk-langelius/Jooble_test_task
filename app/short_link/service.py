from typing import List
from app import db
from flask import redirect, jsonify

from .interface import CreateInterface, LinkInterface
from .model import Link
from .utils import generate_short_id, make_expiration_date


class LinkService:
    @staticmethod
    def get_all() -> List[Link]:
        """Get all links"""
        return Link.query.all()

    @staticmethod
    def get_by_id(link_id: int) -> Link:
        """Get single link by id"""
        return Link.query.get(link_id)

    @staticmethod
    def update(link: Link, link_change_updates: LinkInterface) -> Link:
        link.update(link_change_updates)
        db.session.commit()
        return link

    @staticmethod
    def delete_by_id(link_id: int) -> List[int]:
        """Delete single post by id"""
        link = Link.query.filter(Link.link_id == link_id).first()
        if not link:
            return []
        db.session.delete(link)
        db.session.commit()
        return [link_id]

    @staticmethod
    def create(new_attrs: CreateInterface) -> Link:
        """Create link"""
        new_link = Link(
            original_link=new_attrs['original_link'],
            short_id=generate_short_id(7),
            expires_at=make_expiration_date(new_attrs['days_to_expiration']),
        )

        db.session.add(new_link)
        db.session.commit()

        return new_link

    @staticmethod
    def redirect(short_id: str):
        link = Link.query.filter_by(short_id=short_id).first()
        if link:
            return redirect(link.original_link)
        else:
            return jsonify('invalid link')
