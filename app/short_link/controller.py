from typing import List

from flask import request
from flask.wrappers import Response
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource

from .interface import LinkInterface
from .model import Link
from .schema import CreateLinkSchema, LinkSchema
from .service import LinkService

api = Namespace('Link', description='Namespace for link')


@api.route('/')
class LinkResource(Resource):
    """Links"""

    @responds(schema=LinkSchema(many=True))
    def get(self) -> List[Link]:
        """Get all links"""
        return LinkService.get_all()

    @accepts(schema=CreateLinkSchema, api=api)
    @responds(schema=LinkSchema)
    def post(self) -> Link:
        """Create link"""
        return LinkService.create(request.parsed_obj)


@api.route('/<int:linkID>')
@api.param('linkID', 'Link database ID')
class LinkIDResource(Resource):
    """Single link operations"""
    @responds(schema=LinkSchema)
    def get(self, linkID: int) -> Link:
        """Get link by id"""
        return LinkService.get_by_id(linkID)

    def delete(self, linkID: int) -> Response:
        """Delete link by id"""
        from flask import jsonify

        return jsonify(dict(status='Success',
                            id=LinkService.delete_by_id(linkID)))

    @accepts(schema=LinkSchema, api=api)
    @responds(schema=LinkSchema)
    def put(self, linkID: int) -> Link:
        """Update link by id"""
        changes: LinkInterface = request.parsed_obj
        return LinkService.update(LinkService.get_by_id(linkID), changes)


@api.route('/<shortID>')
@api.param('shortID')
class RedirectResource(Resource):
    """Redirect to actual url"""
    def get(self, shortID: str):
        return LinkService.redirect(shortID)
