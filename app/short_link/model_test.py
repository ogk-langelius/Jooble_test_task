from datetime import date

from pytest import fixture

from .model import Link


@fixture()
def link() -> Link:
    return Link(
        link_id=12,
        original_link='https://www.google.com.ua',
        short_id='testval',
        expires_at=date(2022, 2, 28)
    )


def test_Link_cteate(link: Link):
    assert link
