from datetime import date, timedelta
from typing import List

from flask_sqlalchemy import SQLAlchemy

from app.test.fixtures import app, db

from app.short_link.interface import LinkInterface, CreateInterface
from app.short_link.model import Link
from app.short_link.service import LinkService


def test_get_all(db: SQLAlchemy):
    tlink1: Link = Link(
        link_id=12,
        original_link='https://www.google.com.ua',
        short_id='testv1',
        expires_at=date(2022, 2, 28)
    )

    tlink2: Link = Link(
        link_id=13,
        original_link='http://rozklad.kpi.ua',
        short_id='testv2',
        expires_at=date(2022, 2, 27)
    )

    db.session.add(tlink1)
    db.session.add(tlink2)
    db.session.commit()

    result: List[Link] = LinkService.get_all()

    assert len(result) == 2
    assert tlink1 in result and tlink2 in result


def test_update(db: SQLAlchemy):
    tlink1: Link = Link(
        link_id=12,
        original_link='https://www.google.com.ua',
        short_id='testv1',
        expires_at=date(2022, 2, 28)
    )

    db.session.add(tlink1)
    db.session.commit()

    update: LinkInterface = dict(short_id='testv3')

    LinkService.update(tlink1, update)

    result: Link = Link.query.get(tlink1.link_id)
    assert result.short_id == 'testv3'


def test_delete_by_id(db: SQLAlchemy):
    tlink1: Link = Link(
        link_id=12,
        original_link='https://www.google.com.ua',
        short_id='testv1',
        expires_at=date(2022, 2, 28)
    )

    tlink2: Link = Link(
        link_id=13,
        original_link='http://rozklad.kpi.ua',
        short_id='testv2',
        expires_at=date(2022, 2, 27)
    )

    db.session.add(tlink1)
    db.session.add(tlink2)
    db.session.commit()

    LinkService.delete_by_id(12)
    db.session.commit()

    result: List[Link] = Link.query.all()

    assert len(result) == 1
    assert tlink2 in result and tlink1 not in result


def test_create(db: SQLAlchemy):
    tlink1: CreateInterface = dict(
        link_id=1,
        original_link='https://www.google.com.ua',
        days_to_expiration=3
    )

    tlink2: LinkInterface = dict(
        link_id=1,
        original_link='https://www.google.com.ua',
        expires_at=date.today()+timedelta(days=3)
    )

    LinkService.create(tlink1)
    result: List[Link] = Link.query.all()

    assert len(result) == 1

    for key in tlink2.keys():
        assert getattr(result[0], key) == tlink2[key]


def test_get_by_id(db: SQLAlchemy):
    tlink1: Link = Link(
        link_id=12,
        original_link='https://www.google.com.ua',
        short_id='testv1',
        expires_at=date(2022, 2, 28)
    )

    db.session.add(tlink1)
    db.session.commit()

    assert Link.query.get(tlink1.link_id)


def test_redirect(db: SQLAlchemy):
    tlink1: Link = Link(
        link_id=1,
        original_link='https://www.google.com.ua',
        short_id='testv1',
        expires_at=date(2022, 2, 28)
    )

    db.session.add(tlink1)
    db.session.commit()

    result1 = LinkService.redirect('testv1')
    result2 = LinkService.redirect('testv2')

    assert result1.status_code == 302
    assert result2.status_code == 200
