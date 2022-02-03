from datetime import date, timedelta

from pytest import fixture

from .interface import LinkInterface, CreateInterface
from .schema import LinkSchema, CreateLinkSchema
from .model import Link
from .utils import make_expiration_date

@fixture()
def link_schema() -> LinkSchema:
    return LinkSchema()


@fixture()
def create_schema() -> CreateLinkSchema:
    return CreateLinkSchema()


def test_LinkSchema_create(link_schema: LinkSchema):
    assert link_schema


def test_LinkSchema_work(link_schema: LinkSchema):
    param: LinkInterface = link_schema.load({
        'linkId': '12',
        'originalLink': 'https://www.google.com.ua',
        'shortId': 'testval',
        'expiresAt': '2022-02-28'
    })
    link = Link(**param)

    assert link.link_id == 12
    assert link.original_link == 'https://www.google.com.ua'
    assert link.short_id == 'testval'
    assert link.expires_at == date(2022, 2, 28)


def test_CreateLinkSchema_create(create_schema: CreateLinkSchema):
    assert create_schema


def test_CreateLinkSchema_work(create_schema: CreateLinkSchema):
    param: CreateInterface = create_schema.load({
        'linkId': '12',
        'originalLink': 'https://www.google.com.ua',
        'daysToExpiration': '3'
    })
    link = Link(
        link_id=param['link_id'],
        original_link=param['original_link'],
        expires_at=make_expiration_date(param['days_to_expiration']),
    )

    assert link.link_id == 12
    assert link.original_link == 'https://www.google.com.ua'
    assert link.expires_at == date.today() + timedelta(days=3)
