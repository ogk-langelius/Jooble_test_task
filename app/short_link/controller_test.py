from datetime import date
from unittest.mock import patch

from flask.testing import FlaskClient

from app.test.fixtures import client, app  # noqa
from . import BASE_ROUTE
from .interface import LinkInterface
from .model import Link
from .schema import LinkSchema
from .service import LinkService


def make_link(
        link_id: int = 1,
        original_link: str = 'https://www.google.com',
        short_id: str = 'testval',
        expires_at: date = date(2022, 2, 28)
) -> Link:
    return Link(
        link_id=link_id,
        original_link=original_link,
        short_id=short_id,
        expires_at=expires_at)


class TestLinkResource:
    @patch.object(
        LinkService,
        'get_all',
        lambda: [
            make_link(1, short_id='testvl1'),
            make_link(2, short_id='testvl2'),
        ]
    )
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f'api/{BASE_ROUTE}', follow_redirects=True).get_json()
            expected = (
                LinkSchema(many=True).dump(
                    [
                        make_link(1, short_id='testvl1'),
                        make_link(2, short_id='testvl2'),
                    ]
                )
            )
            for r in result:
                assert r in expected

    @patch.object(
        LinkService, 'create', lambda create_request: Link(link_id=create_request['link_id'],
                                                           original_link=create_request['original_link'],
                                                           short_id='testval',
                                                           expires_at=date(2022, 2, 28))
    )
    def test_post(self, client: FlaskClient):
        with client:
            payload = dict(linkId=1,
                           originalLink='https://www.google.com', )
            result = client.post(f'/api/{BASE_ROUTE}/', json=payload).get_json()
            expected = LinkSchema().dump(Link(link_id=payload['linkId'],
                                              original_link=payload['originalLink'],
                                              short_id='testval',
                                              expires_at=date(2022, 2, 28)))
            assert result == expected


def fake_update(link: Link, changes: LinkInterface):
    # To fake an update just return new object
    updated_link: Link = Link(link_id=link.link_id,
                              original_link=changes['original_link'],
                              short_id=changes['short_id'],
                              expires_at=changes['expires_at'])
    return updated_link


class TestLinkIdResource:
    @patch.object(LinkService, 'get_by_id', lambda id: make_link(link_id=id))
    def test_get(self, client: FlaskClient):
        with client:
            result = client.get(f"/api/{BASE_ROUTE}/1").get_json()
            expected = make_link(link_id=1)
            assert result['linkId'] == expected.link_id

    @patch.object(LinkService, 'delete_by_id', lambda id: id)
    def test_delete(self, client: FlaskClient):
        with client:
            result = client.delete(f"/api/{BASE_ROUTE}/1").get_json()
            expected = dict(status="Success", id=1)
            assert result == expected

    @patch.object(LinkService, 'delete_by_id', lambda id: id)
    @patch.object(LinkService, 'update', fake_update)
    def test_put(self, client: FlaskClient):
        with client:
            result = client.put(f"/api/{BASE_ROUTE}/1",
                                json={
                                    'linkId': '1',
                                    'originalLink': 'https://www.google.com.ua',
                                    'shortId': 'testval',
                                    'expiresAt': '2022-02-28'
                                }).get_json()

            expected = LinkSchema().dump(Link(link_id=1,
                                              original_link='https://www.google.com.ua',
                                              short_id='testval',
                                              expires_at=date(2022, 2, 28)),
                                         many=False)

            assert result == expected
