from datetime import date

from pytest import fixture

from .interface import LinkInterface, CreateInterface
from .model import Link
from .utils import make_expiration_date


@fixture()
def link_interface() -> LinkInterface:
    return LinkInterface(
        link_id=12,
        original_link='https://www.google.com.ua',
        short_id='testval',
        expires_at=date(2022, 2, 28)
    )


@fixture()
def create_interface() -> CreateInterface:
    return CreateInterface(
        link_id=12,
        original_link='https://www.google.com.ua',
        days_to_expiration=3
    )


def test_LinkInterface_create(link_interface: LinkInterface):
    return link_interface


def test_LinkInterface_work(link_interface: LinkInterface):
    link = Link(**link_interface)
    assert link


def test_CreateInterface_create(create_interface: CreateInterface):
    return create_interface


def test_CreateInterface_work(create_interface: CreateInterface):
    link = Link(
        link_id=create_interface['link_id'],
        original_link=create_interface['original_link'],
        expires_at=make_expiration_date(create_interface['days_to_expiration']),
    )
    assert link
